"""evalkit v5.0: inner folds for builders (`from evalkit import inner`): select configurations / hyper-parameters / feature sets INSIDE `predict(train, cands, meta, cutoff)` using only the given train.

    folds = inner.make_inner_folds(train, meta, cutoff)           # list of dicts: inner_cutoff, train_streams, cands, labels
    for cfg in configs:
        vecs = [score_with(cfg, f["train_streams"], f["cands"], meta, f["inner_cutoff"]) for f in folds]
        res[cfg] = inner.inner_sauc(vecs, folds)
    best = max(res, key=res.get)                                  # then fit `best` on the full train and score `cands`

Everything is derived from `train` (the anonymised pre-cutoff streams the harness passes) and the public `meta`: no raw data, no other file, no clock. Because `train` is what the harness hands over, the harness'
independence check and the null control apply unchanged (under --null-control `train` is the relabelled / shuffled null train and the inner labels are computed from it: the inner problem is then a null problem too).

Inner fold geometry (parameters exposed, defaults in the signature): inner cutoffs are placed backwards from `cutoff`: inner_cutoff_1 = cutoff - horizon_days - spacing_months (calendar months; the last inner window plus the
label horizon ends at or before the outer cutoff, so the labels are complete), inner_cutoff_{k+1} = inner_cutoff_k - spacing_months. Each inner fold's candidates are songs never played before the inner cutoff and first
played in [inner_cutoff, inner_cutoff + spacing_months) (the harness uses 3 months), with the harness candidate filter (meta has name and popularity; not an 'unknown' song). Labels (love, plays90, days90, share90)
come from data.song_table on `train` only, with the label horizon `horizon_days` (love rule: >= 6 plays on >= 3 distinct days inside the horizon, as in the harness). Folds with fewer than `min_tried` candidates are dropped
(the list may be shorter than n_folds; the order is newest inner fold first).

Note (documented, not hidden): holdout artists' history is part of `train` in the harness, so inner folds contain songs of the held-out artists' PAST; this is pre-cutoff information and is what any train-only
fit sees. The inner candidate set is NOT the harness candidate set of any fold (different windows), and its songs are anonymised like all train identities.
"""
import numpy as np, pandas as pd
from . import data, metrics

def _song_labels(train, horizon_days):
    """data.song_table on the given train with the label horizon set to `horizon_days` (the module constant is restored afterwards)."""
    old = data.HORIZON_DAYS; data.HORIZON_DAYS = int(horizon_days)
    try: return data.song_table(train)
    finally: data.HORIZON_DAYS = old

def make_inner_folds(train, meta, cutoff, n_folds=4, spacing_months=3, horizon_days=90, min_tried=20):
    """List of inner folds (newest first) = dict(inner_cutoff: Timestamp, train_streams: train rows before inner_cutoff, cands: DataFrame with the harness cand columns
    (song, trackId, albumId, artistIds, artist, trackName), labels: DataFrame aligned row by row to cands with columns love, plays90, days90, share90). See the module docstring."""
    cutoff = pd.Timestamp(cutoff)
    if not len(train): return []
    assert train.t.max() < cutoff, "train must lie strictly before the cutoff"
    st = _song_labels(train, horizon_days)   # all labels from the given train only (the song's first play inside `train` is its true first play: train holds the whole pre-cutoff history)
    ok_meta = set(meta.index[meta.name.notna() & meta.popularity.notna()]) if len(meta) else set()
    cand_cols = ["song", "trackId", "albumId", "artistIds", "artist", "trackName"]; out = []
    end = cutoff - pd.Timedelta(days=horizon_days)   # the newest inner window ends here, so its labels (horizon_days after the first play) are complete inside train
    for _ in range(n_folds):
        ic = end - pd.DateOffset(months=spacing_months); assert ic + pd.DateOffset(months=spacing_months) + pd.Timedelta(days=horizon_days) <= cutoff
        f = st[(st["first"] >= ic) & (st["first"] < end)].reset_index()   # never played before ic <=> first play >= ic (first = earliest stream of the song in train)
        f = f[f.trackId.isin(ok_meta) & ~f.song.str.startswith("unknown")].reset_index(drop=True)
        if len(f) >= min_tried:
            out.append(dict(inner_cutoff=ic, train_streams=train[train.t < ic], cands=f[cand_cols].copy(), labels=f[["love", "plays90", "days90", "share90"]].copy()))
        end = ic   # windows are contiguous: the next (older) inner window ends where this one starts
    return out

def inner_sauc(score_vectors, inner_folds, nboot=0, seed=0, label="love"):
    """Pooled within-inner-fold AUC: all loved / not-loved pairs inside one inner fold, ties half, pooled over the folds (the harness' sauc). score_vectors: list with one score array per inner fold, aligned to
    inner_folds[i]['cands'] (same length as that fold's candidates; use the same order as `inner_folds`). nboot = 0 -> returns the float sauc (nan if no pairs); nboot > 0 -> returns (sauc, lo, hi), the 2.5 / 97.5
    percentiles over `nboot` artist-cluster bootstrap resamples (whole primary artists drawn together across inner folds, as the harness bootstrap)."""
    assert len(score_vectors) == len(inner_folds), "one score vector per inner fold"
    if not inner_folds: return np.nan if not nboot else (np.nan, np.nan, np.nan)
    frames = []
    for i, (f, v) in enumerate(zip(inner_folds, score_vectors)):
        v = np.asarray(v, float); assert v.shape == (len(f["cands"]),) and np.isfinite(v).all(), "need one finite score per inner candidate"
        frames.append(pd.DataFrame(dict(fold=f"inner{i}", artist=f["cands"].artist.values, new_artist=False, is_decoy=0, love=f["labels"][label].values.astype(int), score=v)))
    df = pd.concat(frames, ignore_index=True); B = metrics.Block(df, "love", max(nboot, 1), seed)
    st = B.stats(df.score.values, bool(nboot), ("sauc",)); a = float(st["sauc"][0])
    if not nboot: return a
    b = st["sauc_b"]; return a, float(np.nanpercentile(b, 2.5)), float(np.nanpercentile(b, 97.5))
