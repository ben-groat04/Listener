"""Score predictors (evalkit v4.1).   Dev:  python -m evalkit.run [pred.py ...]      (no args = the baselines + references)      Sealed (final, gated, logged): python -m evalkit.run --sealed [pred.py ...]
A predictor module exposes `predict(train, cands, meta, cutoff) -> np.ndarray` (or a dict `PREDICTORS = {name: fn}`).
The score of a candidate must depend only on (train, that candidate, its meta): the harness checks this (see score_predictor).
Slices: TUNE = 10 folds 2021-07..2023-10 minus HOLDOUT (all iteration); LATE = 4 folds 2024-01..2024-10 minus HOLDOUT (`--late`, capped at 2 runs per predictor hash, logged in
.cache/late_runs.log, tables in .cache/late_tables/); ALL = both. HOLDOUT = tried songs + decoys of 25% of the artists (salted hash, see data.is_holdout) in all 14 dev folds: removed from every
non-holdout run BEFORE predictors are called, scored only by `--holdout` (one run per predictor hash, .cache/holdout_runs.log).
Options: --fast (TUNE, nboot 100, no independence check, no LATE)  --late  --holdout  --walkforward (with --fast)  --nboot N  --indep-n N  --null-control  --null-seeds N (default 5)  --window all|730|365|sub365  --sealed
         --log-dir DIR (tests only: cap logs, fingerprints, holdout budget and late tables of --late / --holdout go to DIR instead of .cache/)."""
import sys, os, json, hashlib, importlib.util, datetime, pickle, glob, subprocess, tempfile, io, time
from pathlib import Path
import numpy as np, pandas as pd
from . import data, metrics, refs, bundle
from .baselines import BASELINES, DIAGNOSTIC, SHORTCUTS, REFERENCES, _manifest_source

VERSION = "v4.1"
REGISTRY = data.ROOT / "evalkit" / "registry.json"
LATE_LOG = data.ROOT / ".cache" / "late_runs.log"
LATE_TABLES = data.ROOT / ".cache" / "late_tables"
HOLDOUT_LOG = data.ROOT / ".cache" / "holdout_runs.log"
LATE_CAP = 2
HOLDOUT_BUDGET = data.ROOT / ".cache" / "holdout_budget.json"
CACHE_DIR = data.ROOT / ".cache" / "evalkit-cache"        # v4.1: the harness' own caches (baseline / reference scores, null bands) live here; .cache/shared/ is frozen (only the pools are READ from there)
REF = "ref_audio_final"                                   # harness reference rows (evalkit.refs.REFS): ref_audio_final = Workflow 3's audio_final, ref_w4r1_listening, ref_w4r1_music; each scored once per (code hash, cutoff, slice part) and cached
REF_NAMES = tuple(refs.REFS)
POOL_REFERENCE = data.ROOT / "evalkit" / "pool_reference.json"
GRADED_KEYS = ("sauc", "wx", "new", "wa", "gc"); KEY_NAME = {"new": "new_artist"}   # metrics graded STRONG / SUGGESTIVE / NONE vs best_ref ('new' = new-artist sauc)
DEVHOLD = "DEV+HOLDOUT"
LABEL_VARIANTS = ("love", "strong", "love_4_2", "love_10_4", "keep")
RB_LABEL = {0: "<3m", 1: "3-12m", 2: "1-3y", 3: ">3y", 4: "unknown"}
XB_LABEL = {0: "0", 1: "1-2", 2: "3-8", 3: "9+"}

def now_iso(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

# ---------------------------------------------------------------- null control (train is modified, candidates are not)
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

# ---------------------------------------------------------------- hashes / caches
def _hash(files):
    h = hashlib.sha256()
    for p in files:
        p = str(p); h.update(Path(p).read_bytes() if p.endswith(".py") else (f"{p}{os.stat(p).st_size}".encode() if os.path.exists(p) else p.encode()))
    return h.hexdigest()[:16]

def _data_files(): return [data.DECOYS, data.TOP_TRACKS, data.STREAMS, data.FALLBACK_DONE, data.ALBUM_REL]
def _pool_hash():   # pools depend on data.py, make_decoys.py and the data files only (file SIZES of the data files; their CONTENT is checked by the selftest against pool_reference.json)
    return _hash([data.ROOT / "evalkit" / "data.py", data.ROOT / "evalkit" / "make_decoys.py"] + _data_files())
def _manifest_file(): return data.ROOT / ".cache" / "shared" / "previews" / "manifest.csv"
def _code_hash():   # v4: run.py is included (a change of the harness' own logic changes the cache key of baseline / reference scores)
    return _hash(sorted(p for p in glob.glob(str(data.ROOT / "evalkit" / "*.py")) if not p.endswith(("selftest.py", "register.py", "fetch_previews.py", "fetch_itunes.py"))) + _data_files() + [_manifest_file()])
def _pool_path():   # the dev pools are READ from the frozen shared folder; if absent they are built into the evalkit cache folder
    p = data.ROOT / ".cache" / "shared" / f"evalkit-pools-{_pool_hash()}.pkl"; return p if p.exists() else CACHE_DIR / p.name

def _pool_digest(df):
    """Order-independent digest of the rows of a pool (identity, label, release bucket, exposure, first-play time); recorded in pool_reference.json before v4."""
    cols = ["song", "trackId", "albumId", "artist", "is_decoy", "love", "plays90", "rb", "exp_before", "first"]
    return hashlib.sha256("\n".join(sorted("|".join(map(str, r)) for r in df[cols].itertuples(index=False))).encode()).hexdigest()

def _content_hashes():
    fh = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest(); h = hashlib.sha256()
    for f in sorted(glob.glob(str(data.RAW / "*"))): h.update(os.path.basename(f).encode()); h.update(open(f, "rb").read())
    return dict(itunes_fallback_csv=fh(data.FALLBACK), album_release_json=fh(data.ALBUM_REL), decoy_raw=h.hexdigest(), n_decoy_raw=len(glob.glob(str(data.RAW / "*"))))

_EDGES = []
def dev_edges():
    """Tercile edges of the user's total plays in a song's own 90-day window (= plays90 / share90) over ALL tried songs of the 14 dev folds (incl. HOLDOUT): fixed, label-independent of any slice."""
    if not _EDGES:
        pools = pickle.load(open(_pool_path(), "rb")); t = pd.concat([pools[c][pools[c].is_decoy == 0] for c in data.DEV_CUTOFFS])
        _EDGES.append(np.quantile((t.plays90 / t.share90).values, [1 / 3, 2 / 3]))
    return _EDGES[0]

KEEP_PLAYS, KEEP_FROM, KEEP_TO = 6, 90, 365   # label variant `keep` (never shown to predictors): >= 6 plays in days [90, 365) after the first play

def keep_qualifies(c):
    """`keep` is computed only for folds whose first-play window [c, c + 3 months) plus 365 days ends strictly before DEV_END (all TUNE folds; the LATE folds are n/a)."""
    return pd.Timestamp(c) + pd.DateOffset(months=3) + pd.Timedelta(days=KEEP_TO) < data.DEV_END

def keep_label(pool, c, ds):
    """`keep` for the tried rows of `pool` (decoys: 0); NaN column when the fold does not qualify. ds = dev-era streams (columns song, t; strictly before DEV_END)."""
    if not keep_qualifies(c): return np.full(len(pool), np.nan)
    tried = pool[pool.is_decoy == 0]; f = tried.set_index("song")["first"]; sub = ds[ds.song.isin(set(tried.song))]
    dl = sub.t.values - sub.song.map(f).values.astype("datetime64[ns]")
    m = (dl >= np.timedelta64(KEEP_FROM, "D")) & (dl < np.timedelta64(KEEP_TO, "D"))
    cnt = sub[m].groupby("song").size().reindex(tried.song).fillna(0).values
    out = np.zeros(len(pool)); out[(pool.is_decoy == 0).values] = (cnt >= KEEP_PLAYS).astype(float); return out

_PREP = {}
def prepare_folds(cutoffs, part="main"):
    """Everything about the folds that does not depend on the predictor (streams, pools, public views); built once per process.
    part: 'main' = pools WITHOUT the HOLDOUT rows (what every non-holdout run scores; predictors never see HOLDOUT rows in cands / meta), 'holdout' = HOLDOUT rows only, 'all' = everything (sealed)."""
    key = (tuple(map(str, cutoffs)), part)
    if key not in _PREP:
        d = data._load_all(); pub = data.anon_streams(d); meta_all = data.load_meta_all(); out = []
        sealed_run = any(pd.Timestamp(c) >= data.DEV_END for c in cutoffs)
        pp = _pool_path()   # dev open pools: label-/predictor-independent, slow to build (decoy matching)
        try: pools = {} if sealed_run or not pp.exists() else pickle.load(open(pp, "rb"))
        except Exception: pools = {}
        miss = [c for c in cutoffs if str(pd.Timestamp(c).date()) not in pools]
        if miss:
            for c, pool in data.make_open_folds(miss, d): pools[str(c.date())] = pool
            if not sealed_run:
                pp.parent.mkdir(parents=True, exist_ok=True); tmp = pp.with_suffix(f".tmp{os.getpid()}"); pickle.dump(pools, open(tmp, "wb")); os.replace(tmp, pp)
        man = _manifest_source(); edges = dev_edges(); ds = d[d.t < data.DEV_END][["song", "t"]]   # dev-era streams only (for the `keep` label)
        for c in cutoffs:
            c = pd.Timestamp(c); pool = pools[str(c.date())]; hold = data.is_holdout(pool.artist.values)
            if part == "main": pool = pool[~hold]
            elif part == "holdout": pool = pool[hold]
            pool = pool.reset_index(drop=True); pool["keep"] = keep_label(pool, c, ds)   # harness-only column (not in the pool digest, never in cands / meta)
            u = meta_all.previewUrl.reindex(pool.trackId).values
            pool["pv"] = [isinstance(x, str) for x in u]
            pool["psrc"] = ["none" if not isinstance(x, str) else ("spotify" if man.get(hashlib.md5(x.encode()).hexdigest()) == "spotify" else "itunes") for x in u]
            tot = (pool.plays90 / pool.share90).values; pool["tot_ter"] = np.where(pool.is_decoy == 1, -1, np.searchsorted(edges, tot, side="right"))   # 0/1/2 terciles of the user's total plays in the song's own 90-day window
            mask = (d.t < c).values
            cands, meta, order = data.public_view(pool, meta_all, d[mask], seed=int(c.strftime("%Y%m%d")))
            out.append(dict(c=c, pool=pool, train=pub[mask], cands=cands, meta=meta, order=order))
        _PREP[key] = out
    return _PREP[key]

def _cache_path(): return CACHE_DIR / f"evalkit-baseline-scores-{_code_hash()}.pkl"
_BH = {}
def _ref_cache_path(name):   # keyed on the code hash and on the bundle (entry file + project code it uses) of the reference
    if name not in _BH: _BH[name] = bundle.bundle_sha256([refs.REFS[name][0]])[:12]
    return CACHE_DIR / f"evalkit-ref-{name}-{_BH[name]}-{_code_hash()}.pkl"
def _load_pk(p):
    try: return pickle.load(open(p, "rb")) if p.exists() else {}
    except Exception: return {}
def _save_pk(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True); tmp = p.with_suffix(f".tmp{os.getpid()}"); pickle.dump(obj, open(tmp, "wb")); os.replace(tmp, p)

def ref_fn(name=REF):
    """Reference `name` (evalkit.refs): ref_audio_final = Workflow 3's audio_final; ref_w4r1_listening = w4r1_final (predictors/w4r1-taste-from-all-listening); ref_w4r1_music = final_content
    (predictors/w4r1-what-in-the-music). Fit caches are identity-keyed (see evalkit.refs); compact feature stores are rebuilt from the builders' scripts if absent."""
    return refs.fn(name)

def score_predictor(fn, cutoffs, name="", indep_n=8, null=None, window=None, cache=None, wname="", part="main"):
    """Run fn on the open pool (tried songs + decoys) of every fold. Returns the scored pool (shuffled public order) with
    attrs['indep'] = median and attrs['indep_p90'] of |score(pool) - score(candidate alone)| / std(score) over `indep_n` random candidates
    per fold. The singleton call gets `meta` restricted to train tracks + that candidate (the full meta lists every pool track, which would
    otherwise let a predictor read the pool composition and still pass this check).
    null: None or ("v2"|"identity", k): scored on the null-control train (see _null_control); seed = cutoff + k. cache: optional dict {(name, cutoff, window, null, indep_n, part): (scores, dev)} used for deterministic baselines."""
    rows, dev = [], []
    for F in prepare_folds(cutoffs, part):
        c, pool, train, cands, meta, order = F["c"], F["pool"], F["train"], F["cands"], F["meta"], F["order"]
        ck = (name, str(c.date()), wname, null, indep_n, part)
        if cache is not None and ck in cache: sc, dv = cache[ck]
        else:
            tr = train
            if window: tr = window(tr, c)
            me = meta
            if null:
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

def score_diagnostics(cutoffs, part="main"):
    """DIAGNOSTIC references computed inside the harness from raw pool data (post-cutoff information; not valid predictors, exempt from independence checks).
    pool_artist_siblings / pool_album_siblings: number of OTHER pool songs by the same primary artist / on the same album.
    exposure_before: minus the number of distinct songs first played EARLIER in the same listening session (gap > 30 min) than the candidate's first play;
    exposure_after: minus the number first played LATER in that session; exposure_session: minus the total (before + after + 1). Decoys: below every tried song.
    replays_first_session: plays of the candidate inside its first session (decoys 0). 'after' and the replay count can be consequences of liking the
    song (a liked song is replayed, new songs follow); 'before' cannot. oracle_day1 / oracle_7d: plays on the first-listen day / in the first 7 days (decoys 0)."""
    names = list(DIAGNOSTIC)
    rows = {n: [] for n in names}
    for F in prepare_folds(cutoffs, part):
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
def _ci(x, alpha): return tuple(np.nanpercentile(x, [100 * alpha / 2, 100 * (1 - alpha / 2)]).round(3))   # two-sided: "95% lower bound" elsewhere = the 2.5th percentile of this interval
def _f(x): return float(np.asarray(x).ravel()[0])

def _band(df_tried, folds, label="love", nmean=1, part="main"):
    """Permutation null band (cached; predictor independent). Keyed on the tried songs of the slice."""
    p = CACHE_DIR / f"evalkit-nullband-{_pool_hash()}.pkl"
    cache = _load_pk(p)
    k = (tuple(folds), label, "v4", part) + (("mean", nmean) if nmean > 1 else ())   # v4: rows without HOLDOUT, adds wx / macro
    if k not in cache:
        cache[k] = metrics.permutation_band(df_tried, label, nmean=nmean)
        cache = {**_load_pk(p), k: cache[k]}; _save_pk(p, cache)
    return cache[k]

def _tied_warnings(scored):
    """SUSPECT CONSTANT SCORES: a model with more than 50% of the scores of one fold in a single tie block (e.g. an all-constant or missing-feature fallback)."""
    w = []
    for n, df in scored.items():
        if n in DIAGNOSTIC or n in SHORTCUTS: continue
        for f, g in df.groupby("fold"):
            share = g.score.value_counts().iloc[0] / len(g)
            if share > .5: w.append(f"SUSPECT CONSTANT SCORES: {n} fold {f}: {share:.0%} of the {len(g)} scores are tied (largest tie block)")
    return w

def _fmt(a, lo, hi): return "-" if not np.isfinite(a) else f"{a:.3f} [{lo:.2f},{hi:.2f}]"

def summarize(preds, folds, nboot=300, n_looks=1, seed=0, valid=None, best_ref=None, graded=True, part="main"):
    """Tables for ONE slice (list of fold names). Bootstrap CIs resample whole primary artists GLOBALLY (all rows of an artist in every fold of the slice are drawn together; pair weights =
    products of the two rows' draw counts; resamples shared by all models => paired differences). CI level 95% (Bonferroni-widened to 1-0.05/n_looks for several sealed looks).
    best_ref: the reference (REFERENCES) with the highest TUNE point sauc, fixed outside this function; the evidence grade is based on it. graded=False (HOLDOUT): deltas and P only.
    part: which rows the slice holds ('main', 'holdout', 'devhold' = main + holdout), only used to key the cached permutation band."""
    alpha = 0.05 / max(1, n_looks); valid = [m for m in preds if m in (valid or BASELINES)]
    P = {n: df[df.fold.isin(folds)].reset_index(drop=True) for n, df in preds.items()}
    for n, df in preds.items(): P[n].attrs.update(df.attrs)
    first = next(iter(P.values()))
    for n, df in P.items(): assert (df.trackId.values == first.trackId.values).all(), "rows must be in the same order for every model"
    tried_m = (first.is_decoy == 0).values; ft = first[tried_m].reset_index(drop=True)
    T = metrics.Block(ft, "love", nboot, seed)
    sp = (first.psrc == "spotify").values   # open pool, primary: rows (tried AND decoys) whose preview is Spotify-sourced
    OB = {"sp": (first[sp].reset_index(drop=True), sp), "full": (first, np.ones(len(first), bool))}
    O = {k: metrics.Block(v[0], "love", nboot, seed + 1) for k, v in OB.items()}
    subs = {k: dict(all=(T, O[k]), new=(T.sub(T.new), O[k].sub(O[k].new)), known=(T.sub(~T.new), O[k].sub(~O[k].new))) for k in OB}
    Owa = {k: O[k].sub((OB[k][0].love.values == 1) | (OB[k][0].is_decoy.values == 1)) for k in OB}   # open within-artist: loved tried vs decoys of the same artist
    S, SO = {}, {k: {} for k in OB}
    for n, df in P.items():
        s = df.score.values; st = s[tried_m]
        S[n] = {k: subs["sp"][k][0].stats(st, True, ("sauc",) if k != "all" else ("sauc", "macro", "wa", "ww", "ws", "wx", "plift", "p20", "gc", "gc_wa")) for k in ("all", "new", "known")}
        for v in OB:
            so = s[OB[v][1]]
            SO[v][n] = {k: subs[v][k][1].stats(so, True, ("sauc",) if k != "all" else ("sauc", "plift", "p20")) for k in ("all", "new", "known")}
            SO[v][n]["wa"] = Owa[v].stats(so, True, ("wa",))
    band = _band(ft, folds, part=part)
    # ---- tables
    rows = []
    for n in P:
        for k in ("all", "new", "known"):
            st = S[n][k]; y = subs["sp"][k][0].y; r = dict(model=n, subset=k, n=len(y), base=round(y.mean(), 3), sauc=round(_f(st["sauc"]), 3), sauc_ci=_ci(st["sauc_b"], alpha))
            if k == "all":
                df = P[n][P[n].is_decoy == 0]; ms = [metrics.fold_metrics(g.love.values, g.score.values) for _, g in df.groupby("fold")]
                r.update({m: round(float(np.nanmean([o[m] for o in ms])), 3) for m in ("auc", "ap", "lift", "r20")})
                r.update(macro_sauc=round(_f(st["macro"]), 3), macro_ci=_ci(st["macro_b"], alpha), p10=round(_f(st["p10"]), 3), p20=round(_f(st["p20"]), 3), p20_ci=_ci(st["p20_b"], alpha), plift=round(_f(st["plift"]), 3), plift_ci=_ci(st["plift_b"], alpha))
            rows.append(r)
    tabs = {"tried_love": pd.DataFrame(rows)}
    wrows = []
    for n in P:
        st = S[n]["all"]; r = dict(model=n)
        for k in ("sauc", "macro", "wa", "ww", "ws", "wx", "gc", "gc_wa"): r[k] = round(_f(st[k]), 3); r[k + "_ci"] = _ci(st[k + "_b"], alpha)
        wrows.append(r)
    tabs["tried_within_group"] = pd.DataFrame(wrows)
    tabs["null_band_95"] = pd.DataFrame({k: [v] for k, v in band.items()}, index=["band"])
    refs = [m for m in P]
    def dtabs(name, get):
        """Paired deltas (shared bootstrap resamples) of every model vs every model: `<name>_lower_bound` (95% lower bound = 2.5th percentile of the two-sided interval), `<name>_P_gt0` (share of resamples with delta > 0),
        `<name>_80ci` (80% interval)."""
        d = lambda n, r: get(n) - get(r)
        tabs[name + "_lower_bound"] = pd.DataFrame({r: {n: round(float(np.nanpercentile(d(n, r), 100 * alpha / 2)), 3) if n != r else np.nan for n in P} for r in refs})
        tabs[name + "_P_gt0"] = pd.DataFrame({r: {n: round(float(np.mean(d(n, r)[np.isfinite(d(n, r))] > 0)), 3) if n != r else np.nan for n in P} for r in refs})
        tabs[name + "_80ci"] = pd.DataFrame({r: {n: tuple(np.nanpercentile(d(n, r), [10, 90]).round(3)) if n != r else "" for n in P} for r in refs})
        for t in ("_lower_bound", "_P_gt0", "_80ci"): tabs[name + t].columns.name = "vs ->"
    for key, nm in (("sauc", "dSAUC"), ("macro", "dMACRO"), ("wa", "dWA"), ("wx", "dWX"), ("gc", "dGC"), ("gc_wa", "dGCWA")): dtabs(nm, lambda n, key=key: S[n]["all"][key + "_b"])
    dtabs("dNEWSAUC", lambda n: S[n]["new"]["sauc_b"])
    # open pool: primary (Spotify-sourced previews for tried songs AND decoys), secondary (full pool)
    cnt = []
    for v, nm in (("sp", "open_love"), ("full", "open_love_full")):
        orows = []
        for n in P:
            r = dict(model=n)
            for k in ("all", "new", "known"): r["open_sauc_" + k] = round(_f(SO[v][n][k]["sauc"]), 3); r["ci_" + k] = _ci(SO[v][n][k]["sauc_b"], alpha)
            r["open_wa"] = round(_f(SO[v][n]["wa"]["wa"]), 3); r["open_wa_ci"] = _ci(SO[v][n]["wa"]["wa_b"], alpha)
            r["open_p20"] = round(_f(SO[v][n]["all"]["p20"]), 3); r["p20_ci"] = _ci(SO[v][n]["all"]["p20_b"], alpha)
            orows.append(r)
        tabs[nm] = pd.DataFrame(orows)
    cf = pd.DataFrame(dict(fold=first.fold.values, dec=first.is_decoy.values, sp=sp))
    tabs["open_subset_counts_per_fold"] = pd.DataFrame({"tried_all": cf[cf.dec == 0].groupby("fold").size(), "tried_spotify_preview": cf[(cf.dec == 0) & cf.sp].groupby("fold").size(),
                                                        "decoys_all": cf[cf.dec == 1].groupby("fold").size(), "decoys_spotify_preview": cf[(cf.dec == 1) & cf.sp].groupby("fold").size()}).fillna(0).astype(int)
    tabs["open_subset_counts_per_fold"].loc["TOTAL"] = tabs["open_subset_counts_per_fold"].sum()
    dtabs("open_dSAUC", lambda n: SO["sp"][n]["all"]["sauc_b"])
    for k in ("new", "known"): dtabs(f"open_dSAUC_{k}", lambda n, k=k: SO["sp"][n][k]["sauc_b"])
    dtabs("open_dP20", lambda n: SO["sp"][n]["all"]["p20_b"]); dtabs("open_dWA", lambda n: SO["sp"][n]["wa"]["wa_b"])
    # label variants, continuous outcomes (tried pool, within-fold Spearman)
    sens = []
    for n in P:
        df = P[n][P[n].is_decoy == 0].reset_index(drop=True); r = dict(model=n)
        for lab in ("love", "love_4_2", "love_10_4", "strong"):
            r[lab] = round(_f(metrics.Block(df, lab, 2, 0).stats(df.score.values, False, ("sauc",))["sauc"]), 3)
        r["sp_days90"] = round(metrics.spearman_cont(P[n], "days90"), 3); r["sp_log_plays90"] = round(metrics.spearman_cont(P[n], "plays90", np.log1p), 3)
        r["sp_share90"] = round(metrics.spearman_cont(P[n], "share90"), 3); sens.append(r)
    tabs["label_variants_sauc_and_spearman"] = pd.DataFrame(sens)
    if part == "main" and list(folds) == list(data.TUNE_CUTOFFS):   # LABEL VARIANTS (TUNE only): sauc [95% CI] of every model against each label definition; `keep` needs a year of follow-up (n/a where it is not computed)
        lb = {}
        for lab in LABEL_VARIANTS:
            ok = ft[lab].notna().values
            lb[lab] = (metrics.Block(ft[ok].reset_index(drop=True), lab, nboot, seed), ok) if ok.any() else None
        lt = {"n (loved/tried)": {lab: (f"{int(ft[lab][ft[lab].notna()].sum())}/{int(ft[lab].notna().sum())}" if lb[lab] else "n/a") for lab in LABEL_VARIANTS}}
        for n in P:
            if n in DIAGNOSTIC: continue
            lt[n] = {}
            for lab in LABEL_VARIANTS:
                if lb[lab] is None: lt[n][lab] = "n/a"; continue
                B_, ok = lb[lab]; b = B_.stats(P[n].score.values[tried_m][ok], True, ("sauc",)); lo_, hi_ = _ci(b["sauc_b"], alpha); lt[n][lab] = _fmt(_f(b["sauc"]), lo_, hi_)
        tabs["LABEL VARIANTS (sauc [95% CI]; TUNE only; keep = >= 6 plays in days [90, 365) after the first play, never a training or prediction label)"] = pd.DataFrame(lt).T
    fa, fci, flags, fci_raw = {}, {}, [], {}
    for n in P:
        for f, (a, lo, hi) in T.fold_auc_ci(P[n].score.values[tried_m]).items():
            fci_raw.setdefault(n, {})[f] = (a, lo, hi); fa.setdefault(n, {})[f] = round(a, 3); fci.setdefault(n, {})[f] = f"[{lo:.2f},{hi:.2f}]"
            if hi < .5 and n not in DIAGNOSTIC: flags.append(f"BELOW CHANCE - investigate: {n} fold {f} AUC {a:.3f} CI upper {hi:.3f}")
    tabs["fold_auc_tried"] = pd.DataFrame(fa); tabs["fold_auc_ci"] = pd.DataFrame(fci)
    tabs["independence"] = pd.DataFrame({"median": {n: df.attrs.get("indep", np.nan) for n, df in preds.items()},
                                         "p90": {n: df.attrs.get("indep_p90", np.nan) for n, df in preds.items()}}).round(4)   # rel. score change, candidate alone vs in pool (NaN = exempt/not checked)
    # ---- BREAKDOWN: sauc with CI by fold / new vs known artist / exposure_before bucket / tercile of the user's plays in the song's 90-day window / release age / preview presence
    xb = metrics.exp_bucket(ft.exp_before.values)
    dims = {"new_vs_known_artist": (np.where(ft.new_artist.values, "new", "known"), ["new", "known"]),
            "exposure_before": (np.array([XB_LABEL[int(v)] for v in xb]), list(XB_LABEL.values())),
            "plays_tercile_90d_window": (np.array(["T1 low", "T2", "T3 high"])[ft.tot_ter.values.astype(int)], ["T1 low", "T2", "T3 high"]),
            "release_age": (np.array([RB_LABEL[int(v)] for v in ft.rb.values]), list(RB_LABEL.values())),
            "preview": (np.where(ft.pv.values, "present", "absent"), ["present", "absent"])}
    bmodels = [n for n in P if n not in DIAGNOSTIC]
    for dim, (lab, levels) in dims.items():
        rowsb = {"n (loved/tried)": {}}
        for lv in levels:
            m = lab == lv; rowsb["n (loved/tried)"][lv] = f"{int(T.y[m].sum())}/{int(m.sum())}"
        for n in bmodels:
            st_all = P[n].score.values[tried_m]; rowsb[n] = {}
            for lv in levels:
                m = lab == lv
                if m.sum() < 2 or T.y[m].sum() == 0 or T.y[m].sum() == m.sum(): rowsb[n][lv] = "-"; continue
                b = T.sub(m).stats(st_all, True, ("sauc",)); lo, hi = _ci(b["sauc_b"], alpha); rowsb[n][lv] = _fmt(_f(b["sauc"]), lo, hi)
        tabs["BREAKDOWN by " + dim] = pd.DataFrame(rowsb).T
    fold_tab = {"n (loved/tried)": {f: f"{int(T.y[T.fold == i].sum())}/{int((T.fold == i).sum())}" for i, f in enumerate(T.fold_names)}}
    for n in bmodels: fold_tab[n] = {f: _fmt(*fci_raw[n][f]) for f in T.fold_names}
    tabs["BREAKDOWN by fold"] = pd.DataFrame(fold_tab).T
    # ---- verdict (no fixed thresholds: graded evidence vs best_ref; deltas vs every reference)
    models = [n for n in P if n not in BASELINES and n not in DIAGNOSTIC and n not in SHORTCUTS and n not in REF_NAMES]; V = []; EV = {}; VD = []; LOG = {}
    if not models: models = [n for n in P if n in BASELINES or n in SHORTCUTS or n in REF_NAMES]   # baseline-only run: VERDICT rows for the baselines / references themselves
    sa = lambda n: _f(S[n]["all"]["sauc"]); so = lambda n: _f(SO["sp"][n]["all"]["sauc"])
    def dstat(na, nb):   # na, nb: model names; key = metric -> point delta, 95% lower bound, P(delta > 0), 80% interval (shared resamples). 'new' = new-artist sauc, the others are the all-songs metrics
        out = {}
        for key in ("sauc", "wa", "gc", "macro", "wx", "new"):
            a, b = (S[na]["new"], S[nb]["new"]) if key == "new" else (S[na]["all"], S[nb]["all"]); k = "sauc" if key == "new" else key
            d = a[k + "_b"] - b[k + "_b"]; f = d[np.isfinite(d)]
            out[key] = dict(d=_f(a[k]) - _f(b[k]), lo95=float(np.nanpercentile(d, 100 * alpha / 2)), P=float(np.mean(f > 0)), lo80=float(np.nanpercentile(d, 10)), hi80=float(np.nanpercentile(d, 90)))
        return out
    metas = [m for m in ("duration", "meta_gbm", "nonaudio_gbm") if m in S]
    best_meta = max(metas, key=lambda m: _f(S[m]["all"]["wa"])) if metas else None   # chosen by the slice's point wa_sauc
    rlist = [r for r in REFERENCES if r in S]
    for n in models:
        vb = [b for b in valid if b != n]; bt = max(vb, key=sa) if vb else None; bo = max(vb, key=so) if vb else None
        lo = lambda a, b, key="sauc": float(np.nanpercentile(a[key + "_b"] - b[key + "_b"], 100 * alpha / 2)) if b is not None else np.nan
        st = S[n]["all"]; sv = tabs["label_variants_sauc_and_spearman"].set_index("model").loc[n]
        br_ok = best_ref in S and n != best_ref
        ev = dstat(n, best_ref) if br_ok else None; EV[n] = ev
        r = dict(model=n, best_ref=best_ref, sauc=round(sa(n), 3), sauc_ci=_ci(st["sauc_b"], alpha), perm_band=band["sauc"], macro_sauc=round(_f(st["macro"]), 3), macro_ci=_ci(st["macro_b"], alpha), macro_band=band.get("macro"),
                 dSAUC_lo_vs_best_ref=round(lo(st, S[best_ref]["all"]), 3) if br_ok else np.nan,
                 dSAUC_lo_vs_best=round(lo(st, S[bt]["all"]), 3) if bt else np.nan, best_valid=bt,
                 wa_ci=_ci(st["wa_b"], alpha), dWA_lo_vs_best_ref=round(lo(st, S[best_ref]["all"], "wa"), 3) if br_ok else np.nan,
                 gc=round(_f(st["gc"]), 3), gc_ci=_ci(st["gc_b"], alpha), gc_band=band.get("gc"), gc_wa=round(_f(st["gc_wa"]), 3), gc_wa_ci=_ci(st["gc_wa_b"], alpha), gc_wa_band=band.get("gc_wa"),
                 dGC_lo_vs_best_ref=round(lo(st, S[best_ref]["all"], "gc"), 3) if br_ok else np.nan,
                 ww_ci=_ci(st["ww_b"], alpha), ws_ci=_ci(st["ws_b"], alpha), ws_band=band.get("ws"), wx=round(_f(st["wx"]), 3), wx_ci=_ci(st["wx_b"], alpha), wx_band=band.get("wx"),
                 dWX_lo_vs_best_ref=round(ev["wx"]["lo95"], 3) if ev else np.nan,
                 new_artist_sauc=round(_f(S[n]["new"]["sauc"]), 3), new_artist_sauc_ci=_ci(S[n]["new"]["sauc_b"], alpha), dNEWSAUC_lo_vs_best_ref=round(ev["new"]["lo95"], 3) if ev else np.nan, plift=round(_f(st["plift"]), 3),
                 sp_share90=sv.sp_share90, open_sauc_ci=_ci(SO["sp"][n]["all"]["sauc_b"], alpha),
                 open_dSAUC_lo_vs_best=round(float(np.nanpercentile(SO["sp"][n]["all"]["sauc_b"] - SO["sp"][bo]["all"]["sauc_b"], 100 * alpha / 2)), 3) if bo else np.nan,
                 open_wa_ci=_ci(SO["sp"][n]["wa"]["wa_b"], alpha), open_p20=round(_f(SO["sp"][n]["all"]["p20"]), 3), best_open_p20=round(max([_f(SO["sp"][b]["all"]["p20"]) for b in vb]), 3) if vb else np.nan,
                 indep_p90=tabs["independence"]["p90"][n], label_consistency="ok" if all(sv[k] >= sv["love"] - .03 for k in ("love_4_2", "love_10_4", "strong")) else "below")
        if ev:   # evidence columns vs best_ref (the grade itself is set in finish_verdicts: it needs the TUNE and LATE slices)
            for key in GRADED_KEYS:
                e = ev[key]; kn = KEY_NAME.get(key, key); r.update({f"d_{kn}_vs_best_ref": round(e["d"], 3), f"P_{kn}_gt0": round(e["P"], 3), f"ci80_{kn}": (round(e["lo80"], 3), round(e["hi80"], 3)), f"evidence_{kn}": "not graded (HOLDOUT)" if not graded else ""})
        if best_meta and n not in metas:
            e = dstat(n, best_meta)["wa"]; r.update({"dWA vs best meta": best_meta, "dWA vs best meta lo95": round(e["lo95"], 3), "dWA vs best meta P(d>0)": round(e["P"], 3)})
        V.append(r)
        for rf in rlist:   # deltas vs EACH reference: point, 95% lower bound, P(d>0), 80% interval for sauc, wa, gc, macro_sauc
            if rf == n: continue
            e = dstat(n, rf); row = dict(model=n, vs=rf)
            for key in ("sauc", "wa", "gc", "macro", "wx", "new"): x = e[key]; row[{"macro": "macro_sauc", "new": "new_artist_sauc"}.get(key, key)] = f"d={x['d']:+.3f} lo95={x['lo95']:+.3f} P={x['P']:.2f} 80%[{x['lo80']:+.3f},{x['hi80']:+.3f}]"
            row["best_ref"] = "*" if rf == best_ref else ""; VD.append(row)
        LOG[n] = dict(sauc=round(sa(n), 4), sauc_ci=_ci(st["sauc_b"], alpha), wx=round(_f(st["wx"]), 4), wx_ci=_ci(st["wx_b"], alpha), wa=round(_f(st["wa"]), 4), wa_ci=_ci(st["wa_b"], alpha), gc=round(_f(st["gc"]), 4), gc_ci=_ci(st["gc_b"], alpha),
                      new_artist_sauc=round(_f(S[n]["new"]["sauc"]), 4), new_artist_sauc_ci=_ci(S[n]["new"]["sauc_b"], alpha))
    for n in P:
        if n not in LOG:
            st = S[n]["all"]; LOG[n] = dict(sauc=round(sa(n), 4), sauc_ci=_ci(st["sauc_b"], alpha), wx=round(_f(st["wx"]), 4), wx_ci=_ci(st["wx_b"], alpha), wa=round(_f(st["wa"]), 4), wa_ci=_ci(st["wa_b"], alpha), gc=round(_f(st["gc"]), 4), gc_ci=_ci(st["gc_b"], alpha),
                                           new_artist_sauc=round(_f(S[n]["new"]["sauc"]), 4), new_artist_sauc_ci=_ci(S[n]["new"]["sauc_b"], alpha))
    tabs["VERDICT"] = pd.DataFrame(V); tabs["VERDICT_DELTAS"] = pd.DataFrame(VD); tabs["_evidence"] = EV; tabs["_log"] = LOG; tabs["_S"] = S; tabs["_P"] = P
    diag = tabs["tried_within_group"][tabs["tried_within_group"].model.isin(DIAGNOSTIC)].merge(
        tabs["open_love"][["model", "open_sauc_all", "ci_all", "open_wa", "open_p20"]], on="model", how="left")
    tabs["DIAGNOSTIC_REFERENCES"] = diag
    return tabs, flags

def finish_verdicts(out, late):
    """Fill the VERDICT 'evidence_<metric>' columns (vs best_ref; metrics sauc, wx, new-artist sauc, wa, gc) with the graded scale (HOLDOUT and DEV+HOLDOUT are never graded):
      STRONG      ALL-slice 95% lower bound > 0 and point delta > 0 on both TUNE and LATE;
      SUGGESTIVE  P(delta > 0) >= 0.8 on both TUNE and LATE;
      NONE        otherwise.
    Without --late only TUNE exists: the column then reads 'TUNE only (P=..)'. With --late the grade is written into the ALL-slice VERDICT (14 folds minus HOLDOUT), which also
    carries TUNE / LATE point deltas and P(delta > 0); the TUNE and LATE VERDICTs say 'see ALL'."""
    for nm, tabs in out.items():
        if nm.startswith("HOLDOUT") or nm == DEVHOLD: continue
        V = tabs["VERDICT"]
        for i, r in V.iterrows():
            ev = tabs["_evidence"].get(r["model"])
            if not ev: continue
            for key in GRADED_KEYS:
                kn = KEY_NAME.get(key, key); col = f"evidence_{kn}"
                if not late: V.at[i, col] = f"TUNE only (P={ev[key]['P']:.2f})"
                elif nm != "ALL": V.at[i, col] = "see ALL"
                else:
                    t, l, a = out["TUNE"]["_evidence"][r["model"]][key], out["LATE"]["_evidence"][r["model"]][key], ev[key]
                    V.at[i, col] = "STRONG" if a["lo95"] > 0 and t["d"] > 0 and l["d"] > 0 else "SUGGESTIVE" if t["P"] >= .8 and l["P"] >= .8 else "NONE"
                    for sl, e in (("TUNE", t), ("LATE", l)):
                        V.at[i, f"{sl}_d_{kn}"] = round(e["d"], 3); V.at[i, f"{sl}_P_{kn}"] = round(e["P"], 3)

# ---------------------------------------------------------------- scoring sets, best_ref
def _load_mods(mods):
    preds = {}
    for p in mods:
        spec = importlib.util.spec_from_file_location("pred_" + Path(p).stem + hashlib.md5(str(p).encode()).hexdigest()[:6], p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for k, f in (getattr(m, "PREDICTORS", None) or {Path(p).stem: m.predict}).items(): preds[k] = f
    return preds

def _score_set(preds, cutoffs, part, indep_n, window, wname, bcache, rcaches):
    """Score every predictor: baselines / shortcuts through the baseline-score cache, each reference through its own cache (indep never checked), others uncached.
    attrs['runtime'] of every scored frame = seconds spent on it in this call (about 0 when it came from a cache)."""
    out = {}
    for k, f in preds.items():
        t0 = time.time()
        if k in REF_NAMES: out[k] = score_predictor(f, cutoffs, k, 0, None, window, (rcaches or {}).get(k), wname, part)
        elif k in BASELINES or k in SHORTCUTS: out[k] = score_predictor(f, cutoffs, k, 0 if k in SHORTCUTS else indep_n, None, window, bcache, wname, part)
        else: out[k] = score_predictor(f, cutoffs, k, indep_n, None, window, None, wname, part)
        out[k].attrs["runtime"] = time.time() - t0
    return out

def best_ref_from(scored, folds):
    """The reference with the highest TUNE point sauc (pooled within-fold AUC of the tried songs; non-HOLDOUT rows). Fixed from TUNE, applied to every slice."""
    res = {}
    for r in REFERENCES:
        if r not in scored: continue
        df = scored[r]; df = df[df.fold.isin(folds) & (df.is_decoy == 0)].reset_index(drop=True)
        res[r] = float(metrics.pooled_auc(df.love.values.astype(int), df.score.values, pd.factorize(df.fold.values)[0], np.ones((1, len(df))))[0])
    return max(res, key=res.get), res

# ---------------------------------------------------------------- caps and logs
def _log_lines_of(log):
    out = []
    if Path(log).exists():
        for l in Path(log).read_text().splitlines():
            if l.strip().startswith("{"): out.append(json.loads(l))
    return out

def _log_count(log, h, keys=("sha256",)):
    """Number of logged runs whose lists `keys` (default: entry-file sha256 list) contain hash h."""
    return sum(1 for j in _log_lines_of(log) if any(h in j.get(k, []) for k in keys))

def _cap_check(log, cap, hashes, bundles, members, what, where):
    """Refuse when the entry-file sha256 of any file (`hashes`) or its bundle hash (`bundles`) has already `cap` logged runs, or when a project file the predictor imports / loads
    (`members`) was itself logged as a predictor file `cap` times (a thin wrapper around a predictor that already used up its runs). Existing log lines count by their entry sha256;
    lines written by v4.1 also carry `bundle_sha256`."""
    for h in hashes:
        n = _log_count(log, h)
        if n >= cap: sys.exit(f"REFUSED: {what} already ran {n} time(s) for the predictor file with sha256 {h[:16]}.. (cap {cap} per predictor hash). {where}")
    for h in bundles:
        n = _log_count(log, h, ("bundle_sha256",))
        if n >= cap: sys.exit(f"REFUSED: {what} already ran {n} time(s) for a predictor with the same bundle hash {h[:16]}.. (entry file + the project code it imports; cap {cap} per bundle hash). {where}")
    for h in members:
        n = _log_count(log, h)
        if n >= cap: sys.exit(f"REFUSED: the predictor imports / loads a project file (sha256 {h[:16]}..) that was itself submitted as a predictor and has used up {what} ({n} run(s), cap {cap}): a wrapper around it is the same predictor. "
                              f"Use evalkit.refs.score for the references, or put your own code in the file you submit. {where}")

def late_cap_check(hashes, log=LATE_LOG, cap=LATE_CAP, bundles=(), members=(), tables=LATE_TABLES):
    """Refuse a --late run of a predictor whose entry-file sha256 or bundle hash already has `cap` logged --late runs (or that wraps a predictor file with that many)."""
    _cap_check(log, cap, hashes, bundles, members, "--late", f"The full table of each earlier run is in {tables}/<sha256>*.txt (read-only); read it instead of re-running.")

def holdout_cap_check(hashes, log=HOLDOUT_LOG, bundles=(), members=()):
    """Refuse a second --holdout run of the same entry-file sha256 / bundle hash (or of a wrapper around a predictor file already run)."""
    _cap_check(log, 1, hashes, bundles, members, "--holdout", f"One run per predictor hash; results are in {log}.")

def holdout_budget_check(path=HOLDOUT_BUDGET):
    if not Path(path).exists(): sys.exit(f"REFUSED: holdout budget file {path} is missing (the harness refuses --holdout without it).")
    b = json.loads(Path(path).read_text())
    if b.get("remaining", 0) <= 0: sys.exit(f"REFUSED: the --holdout budget of round {b.get('round')} is used up (remaining 0 in {path}): one run per round-2 builder, on its pre-declared final file; devil's advocates never run it.")
    return b

def holdout_budget_use(path=HOLDOUT_BUDGET):
    b = json.loads(Path(path).read_text()); b["remaining"] = int(b["remaining"]) - 1; tmp = Path(str(path) + ".tmp"); tmp.write_text(json.dumps(b)); os.replace(tmp, path); return b

def first_fold_vectors(fns, slice_name):
    """First-fold score vector of every model in fns ({name: predict}) on the first fold of the slice: 'late' = first LATE fold (main rows), 'holdout' = first dev fold (HOLDOUT rows)."""
    cut, part = (data.LATE_CUTOFFS[:1], "main") if slice_name == "late" else (data.DEV_CUTOFFS[:1], "holdout")
    return {n: score_predictor(f, cut, n, 0, None, None, None, "all", part).score.values.astype(np.float64) for n, f in fns.items()}

def fingerprint_check(path, entry_sha, vecs, thr=0.999, label=""):
    """Refuse when a model of the submitted file scores the first fold of the slice with Spearman >= thr to a model already logged for the slice by a DIFFERENT file (a renamed or lightly edited copy).
    `path` = .cache/<late|holdout>_fingerprints.pkl; vecs = {model: first-fold score vector}. Runs of the same file (same entry sha256) are not compared with themselves."""
    from scipy.stats import spearmanr
    store = _load_pk(Path(path))
    for model, v in vecs.items():
        for key, e in store.items():
            if e["sha"] == entry_sha or len(e["vec"]) != len(v) or np.ptp(v) == 0 or np.ptp(e["vec"]) == 0: continue
            r = float(spearmanr(v, e["vec"])[0])
            if r >= thr: sys.exit(f"REFUSED: model {model!r} {label}scores the first fold of this slice with Spearman {r:.4f} >= {thr} to model {e['model']!r} (file sha256 {e['sha'][:16]}..) already logged for the slice: a renamed or lightly edited copy is the same predictor.")

def fingerprint_record(path, entry_sha, vecs):
    store = _load_pk(Path(path))
    for model, v in vecs.items(): store.setdefault(f"{entry_sha}|{model}", dict(sha=entry_sha, model=model, vec=np.asarray(v, np.float32)))
    _save_pk(Path(path), store)

def late_write_tables(hashes, text, folder=LATE_TABLES):
    folder.mkdir(parents=True, exist_ok=True); paths = []
    for h in dict.fromkeys(hashes):
        k = 1; p = folder / f"{h}.txt"
        while p.exists(): k += 1; p = folder / f"{h}_run{k}.txt"
        p.write_text(text); os.chmod(p, 0o444); paths.append(str(p))
    return paths

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

# ---------------------------------------------------------------- null control v3: every seed in a FRESH python process
def _null_env(k):
    env = dict(os.environ); env["EVALKIT_NULL_SEED"] = str(k); env["EVALKIT_NO_FIT_CACHE"] = "1"; return env

def run_null_worker(mods, k, cutoff_set, names, mode="v2", part="main", timeout=None):
    """Score `names` (predictors of `mods` + baselines) on the null-control train of seed k in a fresh process (so no in-memory cache can carry over from another seed).
    Returns {name: score array concatenated over folds in cutoff order (same row order as score_predictor's output)}."""
    out = tempfile.mktemp(prefix="evalkit_null_", suffix=".pkl")
    cmd = [sys.executable, "-W", "ignore", "-m", "evalkit.run", "--_null-worker", "--seed", str(k), "--out", out, "--cutoff-set", cutoff_set, "--mode", mode, "--part", part, "--only", ",".join(names)] + [str(m) for m in mods]
    r = subprocess.run(cmd, env=_null_env(k), cwd=str(data.ROOT), timeout=timeout, capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(f"null worker (seed {k}) failed:\n{r.stdout[-2000:]}\n{r.stderr[-4000:]}")
    res = pickle.load(open(out, "rb")); os.remove(out); return res

def _cutoffs_of(name): return {"tune": data.TUNE_CUTOFFS, "dev": data.DEV_CUTOFFS, "tune3": data.TUNE_CUTOFFS[:3]}[name]   # tune3: selftest only

def _worker_main(argv):
    from threadpoolctl import threadpool_limits
    threadpool_limits(2)
    opt = lambda k: argv[argv.index(k) + 1]
    k = int(opt("--seed")); cuts = _cutoffs_of(opt("--cutoff-set")); mode = opt("--mode"); part = opt("--part"); only = [x for x in opt("--only").split(",") if x]
    skip = {argv[i + 1] for i, a in enumerate(argv) if a in ("--seed", "--out", "--cutoff-set", "--mode", "--part", "--only")}
    mods = [a for a in argv if not a.startswith("--") and a not in skip]
    preds = {**BASELINES, **_load_mods(mods)}; res = {}
    for n in only: res[n] = score_predictor(preds[n], cuts, n, 0, (mode, k), None, None, "all", part).score.values
    pickle.dump(res, open(opt("--out"), "wb"))

def null_report(mods, preds, cutoff_set, slices, mode, nseeds, cache, nboot=100, part="main"):
    """Null control v3. Per seed k (seed = cutoff + k, run in a fresh process with EVALKIT_NULL_SEED=k and EVALKIT_NO_FIT_CACHE=1): identity shuffle + artist/album relabelling of the train
    (mode 'v2') or identity shuffle only (mode 'identity', one seed, diagnostic). Per model and slice: real, per-seed and mean sauc / wa_sauc / new-artist sauc, the real-minus-null gap with an
    artist-cluster bootstrap CI (paired resamples), and PASS / FLAG: FLAG iff the mean of the N seeds is outside the 95% permutation band of an N-seed mean (mean of N independent label
    permutations of a fixed random score, 200 times; cached per N). A FLAG is not an automatic fail: a content model's FLAG must be explained by the builder or devil's advocate."""
    cuts = _cutoffs_of(cutoff_set); ks = list(range(nseeds if mode == "v2" else 1)); names = list(preds)
    real = {n: score_predictor(f, cuts, n, 0, None, None, cache if n in BASELINES else None, "all", part) for n, f in preds.items()}
    folds_n = [(F["c"], len(F["cands"])) for F in prepare_folds(cuts, part)]
    nulls = {}
    for k in ks:   # baselines: reuse cached null scores (their code hash is in the cache path); everything else in a fresh process
        got, need = {}, []
        for n in names:
            keys = [(n, str(c.date()), "all", (mode, k), 0, part) for c, _ in folds_n]
            if n in BASELINES and cache is not None and all(x in cache for x in keys): got[n] = np.concatenate([cache[x][0] for x in keys])
            else: need.append(n)
        if need:
            res = run_null_worker(mods, k, cutoff_set, need, mode, part)
            for n in need:
                got[n] = res[n]
                if n in BASELINES and cache is not None:
                    i = 0
                    for c, m in folds_n: cache[(n, str(c.date()), "all", (mode, k), 0, part)] = (res[n][i:i + m], []); i += m
        nulls[k] = got
    rows = []; out = {}
    for sn, fl in slices:
        first = real[names[0]]; sel = first.fold.isin(fl).values & (first.is_decoy == 0).values; ft = first[sel].reset_index(drop=True)
        T = metrics.Block(ft, "love", nboot, 0); Tn = T.sub(T.new); band = _band(ft, fl, nmean=len(ks), part=part)
        for n in names:
            def st(s):
                a = T.stats(s, True, ("sauc", "wa")); b = Tn.stats(s, True, ("sauc",)); return a, b
            ar, br = st(real[n].score.values[sel]); sk = [st(nulls[k][n][sel]) for k in ks]
            pt = np.array([[_f(a["sauc"]), _f(a["wa"]), _f(b["sauc"])] for a, b in sk]); mean = pt.mean(0); r0 = [_f(ar["sauc"]), _f(ar["wa"]), _f(br["sauc"])]
            inb = [band[key][0] <= m <= band[key][1] for key, m in zip(("sauc", "wa", "new"), mean)]
            r = dict(slice=sn, model=n)
            for j, (key, bk) in enumerate((("sauc", "sauc_b"), ("wa_sauc", "wa_b"), ("new_sauc", "sauc_b"))):
                r[f"{key}_real"] = round(r0[j], 3)
                for i, k in enumerate(ks): r[f"{key}_s{k + 1}"] = round(pt[i, j], 3)
                r[f"{key}_mean"] = round(mean[j], 3)
                rb = (ar if j < 2 else br)[bk]; nb = np.mean([(a if j < 2 else b)[bk] for a, b in sk], axis=0); gap = rb - nb
                r[f"{key}_gap"] = round(r0[j] - mean[j], 3); r[f"{key}_gap_ci"] = _ci(gap, 0.05)
            r["label"] = ("PASS" if all(inb) else "FLAG") if mode == "v2" else "diagnostic (not gated)"
            if mode == "v2": r["detail"] = "sauc %s wa %s new %s" % tuple("in" if x else "OUT" for x in inb)
            rows.append(r)
        out[sn] = dict(band=band)
    df = pd.DataFrame(rows)
    for sn in out: out[sn]["table"] = df[df.slice == sn]
    return out

# ---------------------------------------------------------------- main
class _Tee:
    def __init__(self, o): self.o = o; self.buf = io.StringIO()
    def write(self, s): self.o.write(s); self.buf.write(s); return len(s)
    def flush(self): self.o.flush()

def _print_slice(nm, fl, tabs, flags, nfold_total=None):
    print(f"\n{'=' * 30} SLICE {nm}: {len(fl)} folds {fl[0]} .. {fl[-1]} {'=' * 30}")
    print("\n== DIAGNOSTIC_REFERENCES (use post-cutoff information; NOT valid predictors; how much of the label is non-musical)"); print(tabs["DIAGNOSTIC_REFERENCES"].to_string(index=False))
    for k, t in tabs.items():
        if k in ("DIAGNOSTIC_REFERENCES", "VERDICT", "VERDICT_DELTAS") or k.startswith("_") or k.startswith("BREAKDOWN"): continue
        print(f"\n== {nm} {k}"); print(t.to_string(index=k in ("fold_auc_tried", "fold_auc_ci", "independence", "null_band_95") or k.endswith(("lower_bound", "P_gt0", "80ci"))))
    for k, t in tabs.items():
        if k.startswith("BREAKDOWN"): print(f"\n== {nm} {k} (sauc [95% CI]; pairs within fold inside the group)"); print(t.to_string())
    for f in flags: print(f)

def main(argv):
    from threadpoolctl import threadpool_limits
    threadpool_limits(2)
    if "--_null-worker" in argv: return _worker_main(argv)
    sealed = "--sealed" in argv; late = "--late" in argv; holdout = "--holdout" in argv
    opt = lambda k, dflt: type(dflt)(argv[argv.index(k) + 1]) if k in argv else dflt
    fast = "--fast" in argv   # TUNE slice only, nboot 100, no independence check, no LATE
    nboot, indep_n, nulls, win = opt("--nboot", 100 if fast else 300), opt("--indep-n", 0 if fast else 8), [md for md, fl in (("v2", "--null-control"), ("identity", "--null-control-identity")) if fl in argv], opt("--window", "all")
    nseeds = opt("--null-seeds", 3)
    skip = {argv[i + 1] for i, a in enumerate(argv) if a in ("--nboot", "--indep-n", "--window", "--null-seeds")}
    mods = [a for a in argv if not a.startswith("--") and a not in skip]
    from .ablate import WINDOWS
    assert not (fast and sealed), "--fast is dev only"
    assert not (fast and late), "--fast never touches the LATE slice"
    assert not (sealed and late), "--late is a dev option"
    assert not (holdout and (fast or nulls)), "--holdout cannot be combined with --fast or --null-control (one full, scored look per predictor file hash)"
    assert not (holdout and (late or sealed)), "--holdout is a dev option and cannot be combined with --late / --sealed"
    part = "all" if sealed else "holdout" if holdout else "main"
    cutoffs = data.SEALED_CUTOFFS if sealed else data.DEV_CUTOFFS if (late or holdout) else data.TUNE_CUTOFFS
    slices = ([("SEALED", list(map(str, cutoffs)))] if sealed else [("HOLDOUT-ALL", data.DEV_CUTOFFS), ("HOLDOUT-early", data.TUNE_CUTOFFS), ("HOLDOUT-late", data.LATE_CUTOFFS)] if holdout
              else [("TUNE", data.TUNE_CUTOFFS)] + ([("LATE", data.LATE_CUTOFFS), ("ALL", data.DEV_CUTOFFS)] if late else []))
    hashes = [_sha(p) for p in mods]
    if sealed:
        from . import make_sealed; assert make_sealed.main(), "sealed labels do not match manifest (data changed?)"
        reg = json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}
        done = {h for l in _log_lines() if l.startswith("{") for h in json.loads(l).get("files", [])}
        for p, h in zip(mods, hashes):
            if h not in reg: sys.exit(f"{p}: sha256 {h[:12]} is not registered. Only the main session registers the final model(s): python -m evalkit.register {p} <name>")
            if h in done: sys.exit(f"{p}: this exact file was already evaluated on sealed (one look per registered model)")
    if holdout: holdout_cap_check(hashes)
    tee = _Tee(sys.stdout); sys.stdout = tee; t_start = time.time()
    if late:   # auditable, capped use of the held-out dev slice
        late_cap_check(hashes)
        LATE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LATE_LOG, "a") as fh:
            fh.write(json.dumps(dict(ts=now_iso(), files=[str(Path(p).resolve()) for p in mods], sha256=hashes, null_control=("v2" in nulls), null_control_identity=("identity" in nulls), window=win)) + "\n")
    preds = dict(BASELINES); preds.update(SHORTCUTS)  # the fixed valid-baseline set + open-pool shortcuts are always scored alongside, so paired comparisons use identical resamples
    if not nulls: preds[REF] = ref_fn()
    cand_preds = _load_mods(mods); preds.update(cand_preds)
    n_looks = max(1, sealed_looks(hashes)) if sealed else 1
    cp, rp = _cache_path(), _ref_cache_path(); bcache = _load_pk(cp) if not sealed else None; rcache = _load_pk(rp) if not sealed else None
    n0 = (len(bcache) if bcache is not None else 0, len(rcache) if rcache is not None else 0)
    def save_caches():
        if bcache is not None and len(bcache) > n0[0]: _save_pk(cp, {**_load_pk(cp), **bcache})
        if rcache is not None and len(rcache) > n0[1]: _save_pk(rp, {**_load_pk(rp), **rcache})
    pd.set_option("display.width", 300, "display.max_columns", 60, "display.max_colwidth", 60, "display.max_rows", 400)
    if nulls:   # null control runs INSTEAD of the normal tables (slow: N seeds x folds x models, one fresh process per seed)
        assert not sealed, "null control is a dev option"
        cset = "dev" if late else "tune"
        nm_preds = {k: f for k, f in preds.items() if k in BASELINES or k in cand_preds}   # shortcuts and the reference row are exempt from the null control
        for md in nulls:
            res = null_report(mods, nm_preds, cset, slices, md, nseeds, bcache, nboot=min(nboot, 100), part=part)
            print(f"\n{'=' * 20} NULL CONTROL v3 {'(GATED: identity shuffle + artist/album relabelling, %d seeds, each in a fresh process)' % nseeds if md == 'v2' else 'identity-only shuffle (DIAGNOSTIC, not gated: preserves per-artist song counts)'} {'=' * 20}")
            print("PASS = the N-seed mean of sauc, wa_sauc and new-artist sauc is inside the 95% permutation band of an N-seed mean. FLAG = outside (not an automatic fail; a FLAG on a content model has to be explained by the builder / devil's advocate).")
            for sn, r in res.items():
                print(f"\n-- slice {sn}: 95% permutation band of the {nseeds if md == 'v2' else 1}-seed mean {r['band']}"); print(r["table"].drop(columns="slice").to_string(index=False))
        save_caches(); sys.stdout = tee.o
        return res
    # best_ref is fixed from TUNE (point sauc of the references, non-HOLDOUT rows)
    scored = _score_set(preds, cutoffs, part, indep_n, WINDOWS[win], win, bcache, rcache)
    if part == "main": best_ref, br_scores = best_ref_from(scored, data.TUNE_CUTOFFS if not sealed else data.TUNE_CUTOFFS)
    else:
        ref_preds = {k: preds[k] for k in REFERENCES if k in preds}; tune_sc = _score_set(ref_preds, data.TUNE_CUTOFFS, "main", 0, WINDOWS[win], win, bcache, rcache)
        best_ref, br_scores = best_ref_from(tune_sc, data.TUNE_CUTOFFS)
    save_caches()
    scored.update(score_diagnostics(cutoffs, part))
    if sealed:  # log every sealed evaluation (file hash included) so overuse is visible and multiplicity is counted
        data.SEALED_DIR.mkdir(exist_ok=True)
        with open(data.SEALED_DIR / "runs.log", "a") as fh:
            fh.write(json.dumps(dict(ts=now_iso(), models=list(preds), files=hashes, looks_after=n_looks)) + "\n")
    print(f"evalkit {VERSION}: fast={fast} late={late} holdout={holdout} folds={len(cutoffs)} window={win} nboot={nboot} n_looks={n_looks} (CI level {100 * (1 - 0.05 / n_looks):.2f}%; two-sided: '95% lower bound' = 2.5th percentile)")
    print(f"best_ref (fixed from TUNE point sauc of the references, non-HOLDOUT rows): {best_ref}   " + "  ".join(f"{k} {v:.3f}" for k, v in br_scores.items()))
    for w in _tied_warnings({k: v for k, v in scored.items()}): print(w)
    out = {}
    for si, (nm, fl) in enumerate(slices):
        tabs, flags = summarize(scored, fl, nboot, n_looks, seed=1000 * (si + 1), valid=list(BASELINES), best_ref=best_ref, graded=not holdout); out[nm] = tabs
        _print_slice(nm, fl, tabs, flags)
    finish_verdicts(out, late)
    if holdout:   # one JSON line per --holdout run so devil's advocates can read the result without re-running
        rec = dict(ts=now_iso(), files=[str(Path(p).resolve()) for p in mods], sha256=hashes, models=list(preds), best_ref=best_ref, window=win, nboot=nboot,
                   holdout_all={n: v for n, v in out["HOLDOUT-ALL"]["_log"].items() if n not in DIAGNOSTIC})
        HOLDOUT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(HOLDOUT_LOG, "a") as fh: fh.write(json.dumps(rec, default=str) + "\n")
    for si, (nm, fl) in enumerate(slices):
        tabs = out[nm]
        if len(tabs["VERDICT"]):
            print(f"\n== {nm} VERDICT ({'deltas and P only, NOT graded' if holdout else 'graded evidence vs best_ref'}; no fixed thresholds)"); print(tabs["VERDICT"].T.to_string(header=False) if len(tabs["VERDICT"]) == 1 else tabs["VERDICT"].to_string(index=False))
            if len(tabs["VERDICT_DELTAS"]):
                print(f"\n== {nm} VERDICT_DELTAS vs each reference ('*' = best_ref); d = point delta, lo95 = 2.5th percentile, P = P(d>0), 80% interval"); print(tabs["VERDICT_DELTAS"].to_string(index=False))
    print(f"\nruntime {time.time() - t_start:.0f}s")
    sys.stdout = tee.o
    if late and mods:
        for p in late_write_tables(hashes, f"# evalkit {VERSION} --late run {now_iso()}  files={mods}\n" + tee.buf.getvalue()): print("LATE table written (read-only):", p)
    return scored, out

if __name__ == "__main__": main(sys.argv[1:])
