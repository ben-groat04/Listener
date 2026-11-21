"""Score predictors.   Dev:  python -m evalkit.run [pred.py ...]      (no args = the baselines)      Sealed (final, gated, logged): python -m evalkit.run --sealed [pred.py ...]
A predictor module exposes `predict(train, cands, meta, cutoff) -> np.ndarray` (or a dict `PREDICTORS = {name: fn}`).
The score of a candidate must depend only on (train, that candidate, its meta): the harness checks this (see score_predictor).
Slices: TUNE = 10 folds 2021-07..2023-10 (all iteration); LATE = 4 held-out dev folds 2024-01..2024-10 (`--late`, logged in .cache/late_runs.log); ALL = both.
Options: --fast (TUNE, nboot 100, no independence check, no LATE)  --late  --nboot N  --indep-n N  --null-control  --window all|730|365|sub365  --sealed."""
import sys, os, json, hashlib, importlib.util, datetime, pickle, glob
from pathlib import Path
import numpy as np, pandas as pd
from . import data, metrics
from .baselines import BASELINES, DIAGNOSTIC

REGISTRY = data.ROOT / "evalkit" / "registry.json"
LATE_LOG = data.ROOT / ".cache" / "late_runs.log"

def _null_control(train, cands, rng, relabel=True):
    """Null control. (1) Identity shuffle: every train song takes another train song's identity (ids, title, artist) while keeping its own timestamps.
    (2) relabel=True (null v2, the gated control): additionally a random bijection over ALL artist ids of train + cands (and one over all album ids) is applied to
    train only (artistIds, artist, albumId, and the artist part of the song key, consistently), so a candidate's artist now points at a random OTHER artist's
    (or no) history and per-artist song counts no longer line up with the candidates' artists. The identity-only shuffle (relabel=False) PRESERVES per-artist
    song counts, which is real history information, so it is a diagnostic only. Returns (train', amap, bmap)."""
    cols = ["trackId", "albumId", "artistIds", "artist", "trackName"]
    ident = train.drop_duplicates("song").set_index("song")[cols]
    perm = rng.permutation(len(ident))
    ids = pd.DataFrame({c: ident[c].values[perm] for c in cols}, index=ident.index)
    new_song = pd.Series(ident.index.values[perm], index=ident.index); amap = bmap = None
    if relabel:
        arts = np.array(sorted(set(pd.unique(train.artistIds.explode().dropna())) | set(pd.unique(cands.artistIds.explode().dropna())) | set(train.artist) | set(cands.artist)))
        albs = np.array(sorted(set(train.albumId) | set(cands.albumId)))
        amap = dict(zip(arts.tolist(), arts[rng.permutation(len(arts))].tolist())); bmap = dict(zip(albs.tolist(), albs[rng.permutation(len(albs))].tolist()))
        ids["artistIds"] = ids.artistIds.map(lambda l: [amap[a] for a in l]); ids["artist"] = ids.artist.map(amap); ids["albumId"] = ids.albumId.map(bmap)
    ids["song"] = new_song.str.rsplit("|", n=1).str[0] + "|" + ids.artist.astype(str)   # the artist part of the song key follows the (relabelled) artist
    out = train.copy(); rows = train.song.values
    for c in cols + ["song"]: out[c] = ids[c].reindex(rows).values
    return out, amap, bmap

def _null_meta(meta, train, cands, null_train, amap, bmap):
    """Under null v2 the meta of the (shuffled) train tracks must follow the relabelling, otherwise artistNames / albumName would still name the true artist.
    name_of[artist id] / album_of[album id] are read from the ORIGINAL train + cands rows joined to meta; each null-train track gets the names of its relabelled ids."""
    if amap is None: return meta
    rows = pd.concat([train[["trackId", "artistIds", "albumId"]], cands[["trackId", "artistIds", "albumId"]]]).drop_duplicates("trackId")
    an, bn = {}, {}
    for t, ai, al in zip(rows.trackId, rows.artistIds, rows.albumId):
        if t not in meta.index: continue
        names = meta.artistNames.get(t)
        if isinstance(names, list) and len(names) == len(ai):
            for a, n in zip(ai, names): an.setdefault(a, n)
        bn.setdefault(al, meta.albumName.get(t))
    nt = null_train.drop_duplicates("trackId"); m = meta.copy(); keep = nt.trackId.isin(m.index).values; nt = nt[keep]
    nan_ = m.artistNames.to_dict(); nal = m.albumName.to_dict()
    for t, l, al in zip(nt.trackId, nt.artistIds, nt.albumId): nan_[t] = [an.get(a, "?") for a in l]; nal[t] = bn.get(al)
    m["artistNames"] = pd.Series(nan_, dtype=object); m["albumName"] = pd.Series(nal, dtype=object)
    return m

def _hash(files):
    h = hashlib.sha256()
    for p in files:
        p = str(p); h.update(Path(p).read_bytes() if p.endswith(".py") else (f"{p}{os.stat(p).st_size}".encode() if os.path.exists(p) else p.encode()))
    return h.hexdigest()[:16]

def _data_files(): return [data.DECOYS, data.TOP_TRACKS, data.STREAMS, data.FALLBACK_DONE, data.ALBUM_REL]
def _pool_hash():   # pools depend on data.py, make_decoys.py and the data files only
    return _hash([data.ROOT / "evalkit" / "data.py", data.ROOT / "evalkit" / "make_decoys.py"] + _data_files())
def _code_hash():
    return _hash(sorted(p for p in glob.glob(str(data.ROOT / "evalkit" / "*.py")) if not p.endswith(("run.py", "selftest.py", "register.py", "fetch_previews.py", "fetch_itunes.py"))) + _data_files())

_PREP = {}
def prepare_folds(cutoffs):
    """Everything about the folds that does not depend on the predictor (streams, pools, public views); built once per process."""
    key = tuple(map(str, cutoffs))
    if key not in _PREP:
        d = data._load_all(); pub = data.anon_streams(d); meta_all = data.load_meta_all(); out = []
        sealed_run = any(pd.Timestamp(c) >= data.DEV_END for c in cutoffs)
        pp = data.ROOT / ".cache" / "shared" / f"evalkit-pools-{_pool_hash()}.pkl"   # dev open pools: label-/predictor-independent, slow to build (decoy matching)
        try: pools = {} if sealed_run or not pp.exists() else pickle.load(open(pp, "rb"))
        except Exception: pools = {}
        miss = [c for c in cutoffs if str(pd.Timestamp(c).date()) not in pools]
        if miss:
            for c, pool in data.make_open_folds(miss, d): pools[str(c.date())] = pool
            if not sealed_run:
                pp.parent.mkdir(parents=True, exist_ok=True); tmp = pp.with_suffix(f".tmp{os.getpid()}"); pickle.dump(pools, open(tmp, "wb")); os.replace(tmp, pp)
        for c in cutoffs:
            c = pd.Timestamp(c); pool = pools[str(c.date())]
            mask = (d.t < c).values
            cands, meta, order = data.public_view(pool, meta_all, d[mask], seed=int(c.strftime("%Y%m%d")))
            out.append(dict(c=c, pool=pool, train=pub[mask], cands=cands, meta=meta, order=order))
        _PREP[key] = out
    return _PREP[key]

def _cache_path():
    return data.ROOT / ".cache" / "shared" / f"evalkit-baseline-scores-{_code_hash()}.pkl"

def score_predictor(fn, cutoffs, name="", indep_n=8, null=None, window=None, cache=None, wname=""):
    """Run fn on the open pool (tried songs + decoys) of every fold. Returns the scored pool (shuffled public order) with
    attrs['indep'] = median and attrs['indep_p90'] of |score(pool) - score(candidate alone)| / std(score) over `indep_n` random candidates
    per fold. The singleton call gets `meta` restricted to train tracks + that candidate (the full meta lists every pool track, which would
    otherwise let a predictor read the pool composition and still pass this check).
    null: None or ("v2"|"identity", k): scored on the null-control train (see _null_control). cache: optional dict {(name, cutoff, window?, null): (scores, dev)} used for deterministic baselines."""
    rows, dev = [], []
    for F in prepare_folds(cutoffs):
        c, pool, train, cands, meta, order = F["c"], F["pool"], F["train"], F["cands"], F["meta"], F["order"]
        ck = (name, str(c.date()), wname, null, indep_n)
        if cache is not None and ck in cache: sc, dv = cache[ck]
        else:
            tr = train
            if window: tr = window(tr, c)
            me = meta
            if null:   # null = ("v2", k) or ("identity", 0); seed = cutoff + k
                tr0 = tr; tr, am, bm = _null_control(tr, cands, np.random.default_rng(int(c.strftime("%Y%m%d")) + null[1]), relabel=null[0] == "v2")
                me = _null_meta(meta, tr0, cands, tr, am, bm)
            sc = np.asarray(fn(tr.copy(), cands, me, c), float); dv = []
            assert sc.shape == (len(cands),) and np.isfinite(sc).all(), "need one finite score per candidate"
            if indep_n:
                rng = np.random.default_rng(7); idx = rng.choice(len(cands), min(indep_n, len(cands)), replace=False)
                known = set(tr.trackId)
                one = []
                for i in idx:
                    ci = cands.iloc[[i]].reset_index(drop=True)
                    mi = me[me.index.isin(known) | (meta.index == ci.trackId[0])]
                    one.append(np.asarray(fn(tr.copy(), ci, mi, c), float)[0])
                dv = list(np.abs(np.array(one) - sc[idx]) / (sc.std() + 1e-12))
            if cache is not None: cache[ck] = (sc, dv)
        dev += dv
        rows.append(pool.iloc[order].assign(fold=str(c.date()), score=sc))
    out = pd.concat(rows, ignore_index=True)
    out.attrs["indep"] = float(np.median(dev)) if dev else np.nan
    out.attrs["indep_p90"] = float(np.percentile(dev, 90)) if dev else np.nan
    return out

def score_diagnostics(cutoffs):
    """DIAGNOSTIC references computed inside the harness from raw pool data (post-cutoff information; not valid predictors, exempt from independence checks).
    pool_artist_siblings / pool_album_siblings: number of OTHER pool songs by the same primary artist / on the same album.
    exposure_before: minus the number of distinct songs first played EARLIER in the same listening session (gap > 30 min) than the candidate's first play;
    exposure_after: minus the number first played LATER in that session; exposure_session: minus the total (before + after + 1). Decoys: below every tried song.
    replays_first_session: plays of the candidate inside its first session (decoys 0). 'after' and the replay count can be consequences of liking the
    song (a liked song is replayed, new songs follow); 'before' cannot. oracle_day1 / oracle_7d: plays on the first-listen day / in the first 7 days (decoys 0)."""
    names = ["pool_artist_siblings", "pool_album_siblings", "exposure_before", "exposure_after", "exposure_session", "replays_first_session", "oracle_day1", "oracle_7d"]
    rows = {n: [] for n in names}
    for F in prepare_folds(cutoffs):
        pool, order, c = F["pool"], F["order"], F["c"]; dec = pool.is_decoy.values == 1
        def below(v):
            x = np.where(dec, np.nan, v.astype(float)); x[dec] = np.nanmin(x) - 1; return x
        sc = dict(pool_artist_siblings=pool.groupby("artist").artist.transform("size").values - 1.0, pool_album_siblings=pool.groupby("albumId").albumId.transform("size").values - 1.0,
                  exposure_before=below(-pool.exp_before.values), exposure_after=below(-pool.exp_after.values), exposure_session=below(-pool.nnew_sess.values),
                  replays_first_session=np.where(dec, 0.0, pool.replays_s1.values.astype(float)), oracle_day1=pool.day1.values.astype(float), oracle_7d=pool.d7.values.astype(float))
        for n in names: rows[n].append(pool.iloc[order].assign(fold=str(c.date()), score=sc[n][order]))
    out = {}
    for n in names:
        out[n] = pd.concat(rows[n], ignore_index=True); out[n].attrs["indep"] = np.nan; out[n].attrs["indep_p90"] = np.nan; out[n].attrs["diagnostic"] = True
    return out

# ---------------------------------------------------------------- summaries
def _ci(x, alpha): return tuple(np.nanpercentile(x, [100 * alpha / 2, 100 * (1 - alpha / 2)]).round(3))
def _f(x): return float(np.asarray(x).ravel()[0])

def _band(df_tried, folds, label="love", nmean=1):
    """Permutation null band (cached; predictor independent). Keyed on the tried songs of the slice."""
    p = data.ROOT / ".cache" / "shared" / f"evalkit-nullband-{_pool_hash()}.pkl"
    try: cache = pickle.load(open(p, "rb")) if p.exists() else {}
    except Exception: cache = {}
    k = (tuple(folds), label, "v3.1") + (("mean", nmean) if nmean > 1 else ())   # v3.1: adds gc / gc_wa; mean-of-nmean band for the null control
    if k not in cache:
        cache[k] = metrics.permutation_band(df_tried, label, nmean=nmean)
        p.parent.mkdir(parents=True, exist_ok=True); tmp = p.with_suffix(f".tmp{os.getpid()}"); pickle.dump(cache, open(tmp, "wb")); os.replace(tmp, p)
    return cache[k]

def summarize(preds, folds, nboot=300, n_looks=1, seed=0, valid=None):
    """Tables for ONE slice (list of fold names). Bootstrap CIs resample whole primary artists within folds (shared across models => paired differences).
    CI level 95% (Bonferroni-widened to 1-0.05/n_looks for several sealed looks)."""
    alpha = 0.05 / max(1, n_looks); valid = [m for m in preds if m in (valid or BASELINES)]
    P = {n: df[df.fold.isin(folds)].reset_index(drop=True) for n, df in preds.items()}
    for n, df in preds.items(): P[n].attrs.update(df.attrs)
    first = next(iter(P.values()))
    for n, df in P.items(): assert (df.trackId.values == first.trackId.values).all(), "rows must be in the same order for every model"
    tried_m = (first.is_decoy == 0).values
    T = metrics.Block(first[tried_m].reset_index(drop=True), "love", nboot, seed); Tstrong = {}
    O = metrics.Block(first, "love", nboot, seed + 1)
    wa_mask = (first.love.values == 1) | (first.is_decoy.values == 1); Owa = O.sub(wa_mask)   # open within-artist: loved tried vs decoys of the same artist
    subs = dict(all=(T, O), new=(T.sub(T.new), O.sub(O.new)), known=(T.sub(~T.new), O.sub(~O.new)))
    S, SO, Sa = {}, {}, {}
    for n, df in P.items():
        s = df.score.values; st = s[tried_m]
        S[n] = {k: subs[k][0].stats(st, True, ("sauc",) if k != "all" else ("sauc", "wa", "ww", "ws", "plift", "p20", "gc", "gc_wa")) for k in subs}
        SO[n] = {k: subs[k][1].stats(s, True, ("sauc",) if k != "all" else ("sauc", "plift", "p20")) for k in subs}
        SO[n]["wa"] = Owa.stats(s, True, ("wa",))
    band = _band(first[tried_m].reset_index(drop=True), folds)
    # ---- tables
    rows = []
    for n in P:
        for k in subs:
            st = S[n][k]; y = subs[k][0].y; r = dict(model=n, subset=k, n=len(y), base=round(y.mean(), 3), sauc=round(_f(st["sauc"]), 3), sauc_ci=_ci(st["sauc_b"], alpha))
            if k == "all":
                df = P[n][P[n].is_decoy == 0]; ms = [metrics.fold_metrics(g.love.values, g.score.values) for _, g in df.groupby("fold")]
                r.update({m: round(float(np.nanmean([o[m] for o in ms])), 3) for m in ("auc", "ap", "lift", "r20")})
                r.update(p10=round(_f(st["p10"]), 3), p20=round(_f(st["p20"]), 3), p20_ci=_ci(st["p20_b"], alpha), plift=round(_f(st["plift"]), 3), plift_ci=_ci(st["plift_b"], alpha))
            rows.append(r)
    tabs = {"tried_love": pd.DataFrame(rows)}
    wrows = []
    for n in P:
        st = S[n]["all"]; r = dict(model=n)
        for k in ("sauc", "wa", "ww", "ws", "gc", "gc_wa"): r[k] = round(_f(st[k]), 3); r[k + "_ci"] = _ci(st[k + "_b"], alpha)
        wrows.append(r)
    tabs["tried_within_group"] = pd.DataFrame(wrows)
    tabs["null_band_95"] = pd.DataFrame({k: [v] for k, v in band.items()}, index=["band"])
    refs = [m for m in P]
    def dtabs(name, get):
        """Paired deltas (shared bootstrap resamples) of every model vs every model: `<name>_lower_bound` (95% lower bound, as before), `<name>_P_gt0` (share of resamples with delta > 0),
        `<name>_80ci` (80% interval)."""
        d = lambda n, r: get(n) - get(r)
        tabs[name + "_lower_bound"] = pd.DataFrame({r: {n: round(float(np.nanpercentile(d(n, r), 100 * alpha / 2)), 3) if n != r else np.nan for n in P} for r in refs})
        tabs[name + "_P_gt0"] = pd.DataFrame({r: {n: round(float(np.mean(d(n, r)[np.isfinite(d(n, r))] > 0)), 3) if n != r else np.nan for n in P} for r in refs})
        tabs[name + "_80ci"] = pd.DataFrame({r: {n: tuple(np.nanpercentile(d(n, r), [10, 90]).round(3)) if n != r else "" for n in P} for r in refs})
        for t in ("_lower_bound", "_P_gt0", "_80ci"): tabs[name + t].columns.name = "vs ->"
    for key, nm in (("sauc", "dSAUC"), ("wa", "dWA"), ("gc", "dGC"), ("gc_wa", "dGCWA")): dtabs(nm, lambda n, key=key: S[n]["all"][key + "_b"])
    orows = []
    for n in P:
        r = dict(model=n)
        for k in subs: r["open_sauc_" + k] = round(_f(SO[n][k]["sauc"]), 3); r["ci_" + k] = _ci(SO[n][k]["sauc_b"], alpha)
        r["open_wa"] = round(_f(SO[n]["wa"]["wa"]), 3); r["open_wa_ci"] = _ci(SO[n]["wa"]["wa_b"], alpha)
        r["open_p20"] = round(_f(SO[n]["all"]["p20"]), 3); r["p20_ci"] = _ci(SO[n]["all"]["p20_b"], alpha)
        orows.append(r)
    tabs["open_love"] = pd.DataFrame(orows)
    dtabs("open_dSAUC", lambda n: SO[n]["all"]["sauc_b"])
    for k in ("new", "known"): dtabs(f"open_dSAUC_{k}", lambda n, k=k: SO[n][k]["sauc_b"])
    dtabs("open_dP20", lambda n: SO[n]["all"]["p20_b"]); dtabs("open_dWA", lambda n: SO[n]["wa"]["wa_b"])
    # label variants, continuous outcomes (tried pool, within-fold Spearman)
    sens = []
    for n in P:
        df = P[n][P[n].is_decoy == 0].reset_index(drop=True); r = dict(model=n)
        for lab in ("love", "love_4_2", "love_10_4", "strong"):
            r[lab] = round(_f(metrics.Block(df, lab, 2, 0).stats(df.score.values, False, ("sauc",))["sauc"]), 3)
        r["sp_days90"] = round(metrics.spearman_cont(P[n], "days90"), 3); r["sp_log_plays90"] = round(metrics.spearman_cont(P[n], "plays90", np.log1p), 3)
        r["sp_share90"] = round(metrics.spearman_cont(P[n], "share90"), 3); sens.append(r)
    tabs["label_variants_sauc_and_spearman"] = pd.DataFrame(sens)
    fa, fci, flags = {}, {}, []
    for n in P:
        for f, (a, lo, hi) in T.fold_auc_ci(P[n].score.values[tried_m]).items():
            fa.setdefault(n, {})[f] = round(a, 3); fci.setdefault(n, {})[f] = f"[{lo:.2f},{hi:.2f}]"
            if hi < .5 and n not in DIAGNOSTIC: flags.append(f"BELOW CHANCE - investigate: {n} fold {f} AUC {a:.3f} CI upper {hi:.3f}")
    tabs["fold_auc_tried"] = pd.DataFrame(fa); tabs["fold_auc_ci"] = pd.DataFrame(fci)
    tabs["independence"] = pd.DataFrame({"median": {n: df.attrs.get("indep", np.nan) for n, df in preds.items()},
                                         "p90": {n: df.attrs.get("indep_p90", np.nan) for n, df in preds.items()}}).round(4)   # rel. score change, candidate alone vs in pool (NaN = exempt/not checked)
    # ---- verdict (no fixed thresholds: graded evidence)
    models = [n for n in P if n not in BASELINES and n not in DIAGNOSTIC]; V = []; EV = {}
    if not models: models = [n for n in P if n in BASELINES]   # baseline-only run: VERDICT rows for the baselines themselves
    sa = lambda n: _f(S[n]["all"]["sauc"]); so = lambda n: _f(SO[n]["all"]["sauc"])
    def dstat(a, b):   # a, b: stats dicts, key = metric -> point delta, 95% lower bound, P(delta > 0), 80% interval (shared resamples)
        out = {}
        for key in ("sauc", "wa", "gc"):
            d = a[key + "_b"] - b[key + "_b"]; f = d[np.isfinite(d)]
            out[key] = dict(d=_f(a[key]) - _f(b[key]), lo95=float(np.nanpercentile(d, 100 * alpha / 2)), P=float(np.mean(f > 0)), lo80=float(np.nanpercentile(d, 10)), hi80=float(np.nanpercentile(d, 90)))
        return out
    metas = [m for m in ("duration", "meta_gbm", "nonaudio_gbm") if m in S]
    best_meta = max(metas, key=lambda m: _f(S[m]["all"]["wa"])) if metas else None   # chosen by the slice's point wa_sauc
    for n in models:
        vb = [b for b in valid if b != n]; bt = max(vb, key=sa) if vb else None; bo = max(vb, key=so) if vb else None
        lo = lambda a, b, key="sauc": float(np.nanpercentile(a[key + "_b"] - b[key + "_b"], 100 * alpha / 2)) if b is not None else np.nan
        st = S[n]["all"]; sv = tabs["label_variants_sauc_and_spearman"].set_index("model").loc[n]
        ev = dstat(st, S["nonaudio_gbm"]["all"]) if "nonaudio_gbm" in S and n != "nonaudio_gbm" else None; EV[n] = ev
        r = dict(model=n, sauc=round(sa(n), 3), sauc_ci=_ci(st["sauc_b"], alpha), perm_band=band["sauc"],
                 dSAUC_lo_vs_nonaudio_gbm=round(lo(st, S["nonaudio_gbm"]["all"]), 3) if "nonaudio_gbm" in S and n != "nonaudio_gbm" else np.nan,
                 dSAUC_lo_vs_best=round(lo(st, S[bt]["all"]), 3) if bt else np.nan, best_valid=bt,
                 wa_ci=_ci(st["wa_b"], alpha), dWA_lo_vs_nonaudio_gbm=round(lo(st, S["nonaudio_gbm"]["all"], "wa"), 3) if "nonaudio_gbm" in S else np.nan,
                 gc=round(_f(st["gc"]), 3), gc_ci=_ci(st["gc_b"], alpha), gc_band=band.get("gc"), gc_wa=round(_f(st["gc_wa"]), 3), gc_wa_ci=_ci(st["gc_wa_b"], alpha), gc_wa_band=band.get("gc_wa"),
                 dGC_lo_vs_nonaudio_gbm=round(lo(st, S["nonaudio_gbm"]["all"], "gc"), 3) if "nonaudio_gbm" in S and n != "nonaudio_gbm" else np.nan,
                 ww_ci=_ci(st["ww_b"], alpha), ws_ci=_ci(st["ws_b"], alpha), new_artist_sauc_ci=_ci(S[n]["new"]["sauc_b"], alpha), plift=round(_f(st["plift"]), 3),
                 sp_share90=sv.sp_share90, open_sauc_ci=_ci(SO[n]["all"]["sauc_b"], alpha),
                 open_dSAUC_lo_vs_best=round(float(np.nanpercentile(SO[n]["all"]["sauc_b"] - SO[bo]["all"]["sauc_b"], 100 * alpha / 2)), 3) if bo else np.nan,
                 open_wa_ci=_ci(SO[n]["wa"]["wa_b"], alpha), open_p20=round(_f(SO[n]["all"]["p20"]), 3), best_open_p20=round(max([_f(SO[b]["all"]["p20"]) for b in vb]), 3) if vb else np.nan,
                 indep_p90=tabs["independence"]["p90"][n], label_consistency="ok" if all(sv[k] >= sv["love"] - .03 for k in ("love_4_2", "love_10_4", "strong")) else "below")
        if ev:   # evidence columns vs nonaudio_gbm (the grade itself is set in finish_verdicts: it needs the TUNE and LATE slices)
            for key in ("sauc", "wa", "gc"):
                e = ev[key]; r.update({f"d_{key}_vs_nonaudio_gbm": round(e["d"], 3), f"P_{key}_gt0": round(e["P"], 3), f"ci80_{key}": (round(e["lo80"], 3), round(e["hi80"], 3)), f"evidence_{key}": ""})
        if best_meta and n not in metas:
            e = dstat(st, S[best_meta]["all"])["wa"]; r.update({"dWA vs best meta": best_meta, "dWA vs best meta lo95": round(e["lo95"], 3), "dWA vs best meta P(d>0)": round(e["P"], 3)})
        V.append(r)
    tabs["VERDICT"] = pd.DataFrame(V); tabs["_evidence"] = EV
    diag = tabs["tried_within_group"][tabs["tried_within_group"].model.isin(DIAGNOSTIC)].merge(
        tabs["open_love"][["model", "open_sauc_all", "ci_all", "open_wa", "open_p20"]], on="model", how="left")
    tabs["DIAGNOSTIC_REFERENCES"] = diag
    return tabs, flags

def finish_verdicts(out, late):
    """Fill the VERDICT 'evidence_<metric>' columns (vs nonaudio_gbm; metrics sauc, wa, gc) with the graded scale:
      STRONG      ALL-slice 95% lower bound > 0 and point delta > 0 on both TUNE and LATE;
      SUGGESTIVE  P(delta > 0) >= 0.8 on both TUNE and LATE;
      NONE        otherwise.
    Without --late only TUNE exists: the column then reads 'TUNE only (P=..)'. With --late the grade is written into the ALL-slice VERDICT (14 folds), which also
    carries TUNE / LATE point deltas and P(delta > 0); the TUNE and LATE VERDICTs say 'see ALL'."""
    for nm, tabs in out.items():
        V = tabs["VERDICT"]
        for i, r in V.iterrows():
            ev = tabs["_evidence"].get(r["model"])
            if not ev: continue
            for key in ("sauc", "wa", "gc"):
                col = f"evidence_{key}"
                if not late: V.at[i, col] = f"TUNE only (P={ev[key]['P']:.2f})"
                elif nm != "ALL": V.at[i, col] = "see ALL"
                else:
                    t, l, a = out["TUNE"]["_evidence"][r["model"]][key], out["LATE"]["_evidence"][r["model"]][key], ev[key]
                    V.at[i, col] = "STRONG" if a["lo95"] > 0 and t["d"] > 0 and l["d"] > 0 else "SUGGESTIVE" if t["P"] >= .8 and l["P"] >= .8 else "NONE"
                    for sl, e in (("TUNE", t), ("LATE", l)):
                        V.at[i, f"{sl}_d_{key}"] = round(e["d"], 3); V.at[i, f"{sl}_P_{key}"] = round(e["P"], 3)

def null_report(preds, cutoffs, slices, mode, cache):
    """Null control. mode 'v2': identity shuffle + artist/album relabelling, 3 seeds per fold (seed = cutoff + k); GATED: PASS iff the 3-seed mean of sauc, wa_sauc and
    new-artist sauc each lie inside the 95% permutation band of a 3-seed mean (mean of 3 independent label permutations of a fixed random score, 200 times).
    mode 'identity': identity shuffle only (one seed = cutoff), diagnostic, not gated: it preserves per-artist song counts, which is real history information."""
    ks = range(3) if mode == "v2" else range(1); res = {}
    scored = {(n, k): score_predictor(f, cutoffs, n, 0, (mode, k), None, cache if n in BASELINES else None, "all") for n, f in preds.items() for k in ks}
    rows = []
    for sn, fl in slices:
        first = next(iter(scored.values())); first = first[first.fold.isin(fl) & (first.is_decoy == 0)].reset_index(drop=True)
        T = metrics.Block(first, "love", 2, 0); Tn = T.sub(T.new); band = _band(first, fl, nmean=len(ks))
        for n in preds:
            pt = []
            for k in ks:
                df = scored[(n, k)]; df = df[df.fold.isin(fl) & (df.is_decoy == 0)].reset_index(drop=True); s = df.score.values
                a = T.stats(s, False, ("sauc", "wa")); b = Tn.stats(s, False, ("sauc",))
                pt.append((_f(a["sauc"]), _f(a["wa"]), _f(b["sauc"])))
            pt = np.array(pt); mean = pt.mean(0); inb = [band[key][0] <= m <= band[key][1] for key, m in zip(("sauc", "wa", "new"), mean)]
            r = dict(slice=sn, model=n)
            for j, key in enumerate(("sauc", "wa_sauc", "new_sauc")):
                for k in ks: r[f"{key}_s{k + 1}"] = round(pt[k, j], 3)
                r[f"{key}_mean"] = round(mean[j], 3)
            r["pass"] = ("PASS" if all(inb) else "FAIL") if mode == "v2" else "diagnostic (not gated)"
            if mode == "v2": r["pass_detail"] = "sauc %s wa %s new %s" % tuple("in" if x else "OUT" for x in inb)
            rows.append(r)
        res[sn] = dict(band=band)
    df = pd.DataFrame(rows)
    for sn in res: res[sn]["table"] = df[df.slice == sn]
    return res

def _sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def _log_lines():
    f = data.SEALED_DIR / "runs.log"
    return [l for l in f.read_text().splitlines() if l.strip()] if f.exists() else []

def sealed_looks(extra=()):
    """Number of distinct non-baseline predictor files evaluated on sealed (+ ones about to be)."""
    s = set(extra)
    for l in _log_lines():
        if l.startswith("{"): s |= set(json.loads(l).get("files", []))
    return len(s)

def main(argv):
    from threadpoolctl import threadpool_limits
    threadpool_limits(2)
    sealed = "--sealed" in argv; late = "--late" in argv
    opt = lambda k, dflt: type(dflt)(argv[argv.index(k) + 1]) if k in argv else dflt
    fast = "--fast" in argv   # TUNE slice only, nboot 100, no independence check, no LATE
    nboot, indep_n, nulls, win = opt("--nboot", 100 if fast else 300), opt("--indep-n", 0 if fast else 8), [md for md, fl in (("v2", "--null-control"), ("identity", "--null-control-identity")) if fl in argv], opt("--window", "all")
    skip = {argv[i + 1] for i, a in enumerate(argv) if a in ("--nboot", "--indep-n", "--window")}
    mods = [a for a in argv if not a.startswith("--") and a not in skip]
    from .ablate import WINDOWS
    assert not (fast and sealed), "--fast is dev only"
    assert not (fast and late), "--fast never touches the LATE slice"
    assert not (sealed and late), "--late is a dev option"
    cutoffs = data.SEALED_CUTOFFS if sealed else data.DEV_CUTOFFS if late else data.TUNE_CUTOFFS
    slices = [("SEALED", list(map(str, cutoffs)))] if sealed else [("TUNE", data.TUNE_CUTOFFS)] + ([("LATE", data.LATE_CUTOFFS), ("ALL", data.DEV_CUTOFFS)] if late else [])
    hashes = [_sha(p) for p in mods]
    if sealed:
        from . import make_sealed; assert make_sealed.main(), "sealed labels do not match manifest (data changed?)"
        reg = json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}
        done = {h for l in _log_lines() if l.startswith("{") for h in json.loads(l).get("files", [])}
        for p, h in zip(mods, hashes):
            if h not in reg: sys.exit(f"{p}: sha256 {h[:12]} is not registered. Only the main session registers the final model(s): python -m evalkit.register {p} <name>")
            if h in done: sys.exit(f"{p}: this exact file was already evaluated on sealed (one look per registered model)")
    if late:   # auditable use of the held-out dev slice
        LATE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LATE_LOG, "a") as fh:
            fh.write(json.dumps(dict(ts=datetime.datetime.now(datetime.timezone.utc).isoformat(), files=[str(Path(p).resolve()) for p in mods], sha256=hashes, null_control=("v2" in nulls), null_control_identity=("identity" in nulls), window=win)) + "\n")
    preds = dict(BASELINES)  # the fixed valid-baseline set is always scored alongside, so paired comparisons use identical resamples
    for p in mods:
        spec = importlib.util.spec_from_file_location("pred", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for k, f in (getattr(m, "PREDICTORS", None) or {Path(p).stem: m.predict}).items(): preds[k] = f
    n_looks = max(1, sealed_looks(hashes)) if sealed else 1
    cp = _cache_path(); cache = None
    if not sealed:   # baselines are deterministic functions of (code, data, cutoff, window, null): reuse across runs (keyed on a hash of evalkit code + data files)
        try: cache = pickle.load(open(cp, "rb")) if cp.exists() else {}
        except Exception: cache = {}
    n0 = len(cache) if cache is not None else 0
    pd.set_option("display.width", 300, "display.max_columns", 60, "display.max_colwidth", 60, "display.max_rows", 200)
    if nulls:   # null control runs INSTEAD of the normal tables (slow: 3 seeds x folds x models)
        assert not sealed, "null control is a dev option"
        for md in nulls:
            res = null_report(preds, cutoffs, slices, md, cache)
            print(f"\n{'=' * 20} NULL CONTROL {'v2 (GATED: identity shuffle + artist/album relabelling, 3 seeds)' if md == 'v2' else 'identity-only shuffle (DIAGNOSTIC, not gated: preserves per-artist song counts)'} {'=' * 20}")
            for sn, r in res.items():
                print(f"\n-- slice {sn}: 95% permutation band {'of the 3-seed mean ' if md == 'v2' else ''}{ {k: v for k, v in r['band'].items()} }"); print(r["table"].drop(columns="slice").to_string(index=False))
        if cache is not None and len(cache) > n0:
            cp.parent.mkdir(parents=True, exist_ok=True); tmp = cp.with_suffix(f".tmp{os.getpid()}"); pickle.dump(cache, open(tmp, "wb")); os.replace(tmp, cp)
        return res
    scored = {k: score_predictor(f, cutoffs, k, indep_n, None, WINDOWS[win], cache if k in BASELINES else None, win) for k, f in preds.items()}
    if cache is not None and len(cache) > n0:
        cp.parent.mkdir(parents=True, exist_ok=True); tmp = cp.with_suffix(f".tmp{os.getpid()}"); pickle.dump(cache, open(tmp, "wb")); os.replace(tmp, cp)
    scored.update(score_diagnostics(cutoffs))
    if sealed:  # log every sealed evaluation (file hash included) so overuse is visible and multiplicity is counted
        data.SEALED_DIR.mkdir(exist_ok=True)
        with open(data.SEALED_DIR / "runs.log", "a") as fh:
            fh.write(json.dumps(dict(ts=datetime.datetime.utcnow().isoformat(), models=list(preds), files=hashes, looks_after=n_looks)) + "\n")
    print(f"fast={fast} late={late} folds={len(cutoffs)} window={win} nboot={nboot} n_looks={n_looks} (CI level {100 * (1 - 0.05 / n_looks):.2f}%)")
    out = {}
    for si, (nm, fl) in enumerate(slices):
        tabs, flags = summarize(scored, fl, nboot, n_looks, seed=1000 * (si + 1), valid=list(BASELINES)); out[nm] = tabs
        print(f"\n{'=' * 30} SLICE {nm}: {len(fl)} folds {fl[0]} .. {fl[-1]} {'=' * 30}")
        print("\n== DIAGNOSTIC_REFERENCES (use post-cutoff information; NOT valid predictors; how much of the label is non-musical)"); print(tabs["DIAGNOSTIC_REFERENCES"].to_string(index=False))
        for k, t in tabs.items():
            if k in ("DIAGNOSTIC_REFERENCES", "VERDICT") or k.startswith("_"): continue
            print(f"\n== {nm} {k}"); print(t.to_string(index=k in ("fold_auc_tried", "fold_auc_ci", "independence", "null_band_95") or k.endswith(("lower_bound", "P_gt0", "80ci"))))
        for f in flags: print(f)
    finish_verdicts(out, late)
    for si, (nm, fl) in enumerate(slices):
        tabs = out[nm]
        if len(tabs["VERDICT"]): print(f"\n== {nm} VERDICT (graded evidence vs nonaudio_gbm; no fixed thresholds)"); print(tabs["VERDICT"].T.to_string(header=False) if len(tabs["VERDICT"]) == 1 else tabs["VERDICT"].to_string(index=False))
    return scored, out

if __name__ == "__main__": main(sys.argv[1:])
