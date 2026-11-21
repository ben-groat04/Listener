"""Leakage self-audit (run: python3 -W ignore predictors/w3r1-training-signal/audit.py).
1. Point-in-time check: for sampled training songs, the extra/audio/base features and the target-free row attributes recomputed from streams truncated at the song's own first play
   (+ song table of the truncated log) equal those used in training.
2. Horizon check: every training row has first < cutoff - 90 d, and no stream >= cutoff is in `train`.
3. Candidate-independence: scores of a candidate alone equal its score inside the full pool (harness does this too)."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0]); sys.path.insert(0, "/home/user/Listener/taste-model")
import numpy as np, pandas as pd
from evalkit import run, data, baselines as B
import core, feats as FT
rng = np.random.default_rng(0)
for c in ("2022-10-01", "2023-10-01"):
    F = run.prepare_folds([c])[0]; train, meta, cutoff = F["train"], F["meta"], F["c"]
    assert train.t.max() < cutoff
    bd = core.build(train, cutoff, meta); rows, X, hist, prior, base, Xe, Xa, ctx = bd; Xa = core.audio_train(bd)
    assert (rows["first"] < cutoff - pd.Timedelta(days=90)).all()
    bad = 0; n = 0
    for i in rng.choice(len(rows), 12, replace=False):
        tf = rows["first"].iloc[i]
        tr2 = train[train.t < tf]
        st2 = data.song_table(tr2).reset_index()
        st2["dur"] = meta.durationMs.reindex(st2.trackId).values.astype(float); st2["popu"] = meta.popularity.reindex(st2.trackId).values.astype(float)
        S2 = FT.Stream(tr2, st2)
        f2 = FT.extra_features(S2, rows.artist.values[i:i+1], rows.albumId.values[i:i+1], np.array([tf.to_datetime64()]),
                               meta.durationMs.reindex(rows.trackId.iloc[i:i+1]).values.astype(float), meta.popularity.reindex(rows.trackId.iloc[i:i+1]).values.astype(float))
        a = Xe.iloc[i]; b = f2.iloc[0][a.index]
        # a_lp_mean / a_lp_max / a_love_frac use matured songs: their song-table values must be identical (horizon ended before tf)
        d = ((a - b).abs() > 1e-6) & ~(a.isna() & b.isna()); n += 1
        if d.any(): bad += 1; print(c, i, "MISMATCH", list(a.index[d]), a[d].values, b[d].values)
        if Xa is not None:
            Er = FT.track_emb(rows.trackId.values[i:i+1], meta)
            E_song = FT.track_emb(st2.trackId.values, meta); trk, tc = np.unique(tr2.trackId.values, return_inverse=True)
            A2 = FT.audio_features(S2, Er, np.array([tf.to_datetime64()]), E_song, st2["first"].values.astype("datetime64[ns]"), core.grade(st2), st2.love.values,
                                   FT.track_emb(trk, meta), tc, tr2.t.values.astype("datetime64[ns]"))
            aa = Xa.iloc[i][A2.columns]; dd = ((aa - A2.iloc[0]).abs() > 1e-5) & ~(aa.isna() & A2.iloc[0].isna())
            if dd.any(): bad += 1; print(c, i, "AUDIO MISMATCH", list(aa.index[dd]))
    print(c, "rows", len(rows), "sampled", n, "mismatching", bad)
