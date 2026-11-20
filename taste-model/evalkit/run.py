"""Score predictors.   Dev (open):  python -m evalkit.run [pred.py ...]      (no args = the baselines)
Sealed (final, gated, logged):     python -m evalkit.run --sealed [pred.py ...]
A predictor module exposes `predict(train, cands, meta, cutoff) -> np.ndarray` (or a dict `PREDICTORS = {name: fn}`).
The score of a candidate must depend only on (train, that candidate, its meta): the harness checks this (see score_predictor).
Options: --nboot N  --indep-n N (singleton re-scores per fold, 0 = skip)  --null-control  --window all|730|365|sub365 (see ablate.py)."""
import sys, os, json, hashlib, importlib.util, datetime, pickle
from pathlib import Path
import numpy as np, pandas as pd
from . import data, metrics
from .baselines import BASELINES, DIAGNOSTIC

REGISTRY = data.ROOT / "evalkit" / "registry.json"

def _null_control(train, rng):
    """Break the link between song identity and play history: every train song takes another train song's identity
    (ids, title, artist) while keeping its own timestamps. A model that really learns from the user's history must fall to chance."""
    cols = ["trackId", "albumId", "artistIds", "artist", "trackName"]
    ident = train.drop_duplicates("song").set_index("song")[cols]
    perm = rng.permutation(len(ident))
    shuffled = pd.DataFrame({c: ident[c].values[perm] for c in cols}, index=ident.index).reindex(train.song.values)
    out = train.copy()
    for c in cols: out[c] = shuffled[c].values
    out["song"] = pd.Series(ident.index.values[perm], index=ident.index).reindex(train.song.values).values
    return out

_PREP = {}
def prepare_folds(cutoffs):
    """Everything about the folds that does not depend on the predictor (streams, pools, public views); built once per process."""
    key = tuple(map(str, cutoffs))
    if key not in _PREP:
        d = data._load_all(); pub = data.anon_streams(d); meta_all = data.load_meta_all(); out = []
        sealed_run = any(pd.Timestamp(c) >= data.DEV_END for c in cutoffs)
        pp = data.ROOT / ".cache" / "shared" / f"evalkit-pools-{_code_hash()}.pkl"   # dev open pools: label-/predictor-independent, slow to build (decoy matching)
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

def _code_hash():
    import glob
    h = hashlib.sha256()
    for p in sorted(glob.glob(str(data.ROOT / "evalkit" / "*.py"))) + [str(data.DECOYS), str(data.TOP_TRACKS), str(data.STREAMS)]:
        if not p.endswith(("run.py", "selftest.py", "register.py")): h.update(Path(p).read_bytes() if p.endswith(".py") else f"{p}{os.stat(p).st_size}".encode())
    return h.hexdigest()[:16]

def _cache_path():
    return data.ROOT / ".cache" / "shared" / f"evalkit-baseline-scores-{_code_hash()}.pkl"

def score_predictor(fn, cutoffs, name="", indep_n=8, null=False, window=None, cache=None, wname=""):
    """Run fn on the open pool (tried songs + decoys) of every fold. Returns the scored pool (shuffled public order) with
    attrs['indep'] = median and attrs['indep_p90'] of |score(pool) - score(candidate alone)| / std(score) over `indep_n` random candidates
    per fold. The singleton call gets `meta` restricted to train tracks + that candidate (the full meta lists every pool track, which would
    otherwise let a predictor read the pool composition and still pass this check).
    cache: optional dict {(name, cutoff, window?, null): (scores, dev)} used for deterministic baselines."""
    rows, dev = [], []
    for F in prepare_folds(cutoffs):
        c, pool, train, cands, meta, order = F["c"], F["pool"], F["train"], F["cands"], F["meta"], F["order"]
        ck = (name, str(c.date()), wname, null, indep_n)
        if cache is not None and ck in cache: sc, dv = cache[ck]
        else:
            tr = train
            if window: tr = window(tr, c)
            if null: tr = _null_control(tr, np.random.default_rng(int(c.strftime("%Y%m%d"))))
            sc = np.asarray(fn(tr.copy(), cands, meta, c), float); dv = []
            assert sc.shape == (len(cands),) and np.isfinite(sc).all(), "need one finite score per candidate"
            if indep_n and name not in DIAGNOSTIC:
                rng = np.random.default_rng(7); idx = rng.choice(len(cands), min(indep_n, len(cands)), replace=False)
                known = set(tr.trackId)
                one = []
                for i in idx:
                    ci = cands.iloc[[i]].reset_index(drop=True)
                    mi = meta[meta.index.isin(known) | (meta.index == ci.trackId[0])]
                    one.append(np.asarray(fn(tr.copy(), ci, mi, c), float)[0])
                dv = list(np.abs(np.array(one) - sc[idx]) / (sc.std() + 1e-12))
            if cache is not None: cache[ck] = (sc, dv)
        dev += dv
        rows.append(pool.iloc[order].assign(fold=str(c.date()), score=sc))
    out = pd.concat(rows, ignore_index=True)
    out.attrs["indep"] = float(np.median(dev)) if dev else np.nan
    out.attrs["indep_p90"] = float(np.percentile(dev, 90)) if dev else np.nan
    return out

def _q(x, alpha): return tuple(np.nanpercentile(x, [100 * alpha / 2, 100 * (1 - alpha / 2)]).round(3))

def summarize(preds, nboot=300, refs=(), n_looks=1):
    """Tables. Bootstrap CIs resample whole primary artists within folds (shared across models => paired differences). CI level is 95% for
    a single look and Bonferroni-widened to 1-0.05/n_looks when several sealed looks have been spent."""
    alpha = 0.05 / max(1, n_looks); rng = np.random.default_rng(0)
    tabs = {}
    def block(label, pool, subs):
        L = []
        for sub, nm in subs:
            A = {n: metrics.folds_arrays(df, label, sub, pool) for n, df in preds.items()}
            idxs = [metrics.boot_idx(next(iter(A.values())), rng) for _ in range(nboot)]
            B = {n: [metrics.macro(a, ix) for ix in idxs] for n, a in A.items()}
            for n, a in A.items():
                y = np.concatenate([f[0] for f in a]); m = metrics.macro(a)
                row = dict(label=label, pool=pool, subset=nm, model=n, n=len(y), base=round(y.mean(), 3),
                           **{k: round(v, 3) for k, v in m.items()},
                           sauc_ci=_q([b["sauc"] for b in B[n]], alpha), plift_ci=_q([b["plift"] for b in B[n]], alpha),
                           p20_ci=_q([b["p20"] for b in B[n]], alpha))
                rr = [r for r in refs if r in preds and r != n]
                if rr:
                    lo = {r: np.nanpercentile([x["sauc"] - z["sauc"] for x, z in zip(B[n], B[r])], 100 * alpha / 2) for r in rr}
                    w = min(lo, key=lo.get); row["dSAUC_worst_ref"] = w; row["dSAUC_lo"] = round(lo[w], 3)
                L.append(row)
        return L
    allsub = ((None, "all"), (True, "new-artist"), (False, "known-artist"))
    tabs["tried_love"] = pd.DataFrame(block("love", "tried", allsub))
    tabs["tried_strong"] = pd.DataFrame(block("strong", "tried", ((None, "all"),)))
    tabs["open_love"] = pd.DataFrame(block("love", "open", allsub))
    sens = []
    for n, df in preds.items():
        r = dict(model=n)
        for lab in ("love", "love_4_2", "love_10_4", "strong"):
            r[lab] = round(metrics.macro(metrics.folds_arrays(df, lab, None, "tried"))["sauc"], 3)
        r["spearman_days90"] = round(metrics.spearman_cont(df), 3); sens.append(r)
    tabs["label_sensitivity_sauc"] = pd.DataFrame(sens)
    fa = {}
    for n, df in preds.items():
        for f, g in df[df.is_decoy == 0].groupby("fold"):
            fa.setdefault(n, {})[f] = metrics.auc(g.love, g.score)
    tabs["fold_auc_tried"] = pd.DataFrame(fa).round(3)
    # per-fold lower 95% bound (bootstrap over songs) -- sanity condition, not a test
    lo = {}
    for n, df in preds.items():
        for f, g in df[df.is_decoy == 0].groupby("fold"):
            y, s, cl = g.love.values, g.score.values, g.artist.values
            lo.setdefault(n, {})[f] = np.nanpercentile([metrics.auc(y[i], s[i]) for i in (metrics.cluster_idx(cl, rng) for _ in range(200))], 100 * alpha / 2).round(3)
    tabs["fold_auc_lower_bound"] = pd.DataFrame(lo)
    tabs["independence"] = pd.DataFrame({"median": {n: df.attrs.get("indep", np.nan) for n, df in preds.items()},
                                         "p90": {n: df.attrs.get("indep_p90", np.nan) for n, df in preds.items()}}).round(4)  # rel. score change, candidate alone vs in pool
    return tabs

BAR = """SUCCESS BAR ('works VERY WELL'); every line must pass on SEALED (and first on dev). CI = cluster bootstrap over artists,
Bonferroni-widened by the number of sealed looks. Fixed baseline set = all of baselines.BASELINES (incl. the pool diagnostics).
 T1 tried pool: stratified AUC (love, all songs) lower CI bound >= 0.65
 T2 tried pool: stratified AUC on new-artist songs lower CI bound >= 0.60
 T3 tried pool: paired dSAUC lower bound > 0 against EVERY baseline
 T4 tried pool: pooled top-10% lift >= 1.8 and its lower CI bound >= 1.3
 T5 sanity (not a test): fold AUC >= 0.55 in >= 4 of the 5 folds and no fold below 0.50
 T6 labels: sAUC for love_4_2, love_10_4, strong each >= love sAUC - 0.03 and mean Spearman(score, days90) >= 0.15
 O1 open pool (tried + decoys): sAUC (love) lower CI bound >= 0.75
 O2 open pool: paired dSAUC lower bound > 0 against EVERY baseline
 O3 open pool, new-artist subset: sAUC lower CI bound >= 0.65
 O4 open pool: precision in top 20 songs (macro) >= 0.40, >= 1.3 x best baseline, lower CI bound >= 0.30
 I  independence: 90th-percentile relative score change (alone vs pool, restricted meta) < 0.01 (NaN = not checked, e.g. --indep-n 0 / --fast: then NOT passed)
 N  null control (--null-control run): tried sAUC <= 0.56, i.e. the signal comes from the user's history, not from a static prior"""

def gates(tabs, model, null_tabs=None):
    t = tabs["tried_love"]; o = tabs["open_love"]; g = lambda df, sub: df[(df.subset == sub) & (df.model == model)].iloc[0]
    ta, tn, oa, on = g(t, "all"), g(t, "new-artist"), g(o, "all"), g(o, "new-artist")
    base_p20 = max(o[(o.subset == "all") & o.model.isin(BASELINES)].p20)
    fa = tabs["fold_auc_tried"][model]; s = tabs["label_sensitivity_sauc"].set_index("model").loc[model]
    res = {
     "T1": (ta.sauc_ci[0], ta.sauc_ci[0] >= .65), "T2": (tn.sauc_ci[0], tn.sauc_ci[0] >= .60),
     "T3": (ta.get("dSAUC_lo", np.nan), ta.get("dSAUC_lo", -1) > 0), "T4": (ta.plift, ta.plift >= 1.8 and ta.plift_ci[0] >= 1.3),
     "T5": ((fa >= .55).sum(), (fa >= .55).sum() >= len(fa) - 1 and (fa >= .5).all()),
     "T6": (s.spearman_days90, all(s[k] >= s["love"] - .03 for k in ("love_4_2", "love_10_4", "strong")) and s.spearman_days90 >= .15),
     "O1": (oa.sauc_ci[0], oa.sauc_ci[0] >= .75), "O2": (oa.get("dSAUC_lo", np.nan), oa.get("dSAUC_lo", -1) > 0),
     "O3": (on.sauc_ci[0], on.sauc_ci[0] >= .65), "O4": (oa.p20, oa.p20 >= .40 and oa.p20 >= 1.3 * base_p20 and oa.p20_ci[0] >= .30),
     "I": (tabs["independence"]["p90"][model], tabs["independence"]["p90"][model] < .01)}
    if null_tabs is not None:
        nv = g(null_tabs["tried_love"], "all").sauc; res["N"] = (nv, nv <= .56)
    return pd.DataFrame(res, index=["value", "pass"]).T

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
    sealed = "--sealed" in argv
    opt = lambda k, dflt: type(dflt)(argv[argv.index(k) + 1]) if k in argv else dflt
    fast = "--fast" in argv   # dev only: every 2nd dev cutoff (4 folds), nboot 100, no independence check unless asked; baselines cached
    nboot, indep_n, null, win = opt("--nboot", 100 if fast else 300), opt("--indep-n", 0 if fast else 8), "--null-control" in argv, opt("--window", "all")
    skip = {argv[i + 1] for i, a in enumerate(argv) if a in ("--nboot", "--indep-n", "--window")}
    mods = [a for a in argv if not a.startswith("--") and a not in skip]
    from .ablate import WINDOWS
    assert not (fast and sealed), "--fast is dev only"
    cutoffs = data.SEALED_CUTOFFS if sealed else data.DEV_CUTOFFS[::2] if fast else data.DEV_CUTOFFS
    hashes = [_sha(p) for p in mods]
    if sealed:
        from . import make_sealed; assert make_sealed.main(), "sealed labels do not match manifest (data changed?)"
        reg = json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}
        done = {h for l in _log_lines() if l.startswith("{") for h in json.loads(l).get("files", [])}
        for p, h in zip(mods, hashes):
            if h not in reg: sys.exit(f"{p}: sha256 {h[:12]} is not registered. Only the main session registers the final model(s): python -m evalkit.register {p} <name>")
            if h in done: sys.exit(f"{p}: this exact file was already evaluated on sealed (one look per registered model)")
    preds = dict(BASELINES)  # the fixed baseline set is always scored alongside, so paired comparisons use identical resamples
    for p in mods:
        spec = importlib.util.spec_from_file_location("pred", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for k, f in (getattr(m, "PREDICTORS", None) or {p: m.predict}).items(): preds[k] = f
    n_looks = max(1, sealed_looks(hashes)) if sealed else 1
    cp = _cache_path(); cache = None
    if not sealed:   # baselines are deterministic functions of (code, data, cutoff, window, null): reuse across runs (keyed on a hash of evalkit code + data files)
        try: cache = pickle.load(open(cp, "rb")) if cp.exists() else {}
        except Exception: cache = {}
    n0 = len(cache) if cache is not None else 0
    scored = {k: score_predictor(f, cutoffs, k, indep_n, null, WINDOWS[win], cache if k in BASELINES else None, win) for k, f in preds.items()}
    if cache is not None and len(cache) > n0:
        cp.parent.mkdir(parents=True, exist_ok=True); tmp = cp.with_suffix(f".tmp{os.getpid()}"); pickle.dump(cache, open(tmp, "wb")); os.replace(tmp, cp)
    if sealed:  # log every sealed evaluation (file hash included) so overuse is visible and multiplicity is counted
        data.SEALED_DIR.mkdir(exist_ok=True)
        with open(data.SEALED_DIR / "runs.log", "a") as fh:
            fh.write(json.dumps(dict(ts=datetime.datetime.utcnow().isoformat(), models=list(preds), files=hashes, looks_after=n_looks)) + "\n")
    pd.set_option("display.width", 260, "display.max_columns", 40, "display.max_colwidth", 40)
    refs = [b for b in BASELINES if b in scored]
    print(f"fast={fast} folds={len(cutoffs)} window={win} null_control={null} n_looks={n_looks} (CI level {100 * (1 - 0.05 / n_looks):.2f}%)")
    tabs = summarize(scored, nboot, refs=refs if mods else (), n_looks=n_looks)
    for k, t in tabs.items():
        print(f"\n== {k}"); print(t.to_string(index=k in ("fold_auc_tried", "fold_auc_lower_bound", "independence")))
    if mods:
        print("\n" + BAR)
        for m in [k for k in preds if k not in BASELINES]:
            print(f"\n-- gates for {m} (the N gate needs a separate --null-control run: compare tried sAUC)"); print(gates(tabs, m).to_string())
    return scored, tabs

if __name__ == "__main__": main(sys.argv[1:])
