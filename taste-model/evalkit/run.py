"""Score predictors.   Dev (open):  python -m evalkit.run [pred.py ...]      (no args = the baselines)
Sealed (final, gated, logged):     python -m evalkit.run --sealed [pred.py ...]
A predictor module exposes `predict(train, cands, meta, cutoff) -> np.ndarray` (or a dict `PREDICTORS = {name: fn}`).
The score of a candidate must depend only on (train, that candidate, its meta): the harness checks this (see score_predictor).
Options: --nboot N  --indep-n N (singleton re-scores per fold, 0 = skip)  --null-control  --window all|730|365|sub365 (see ablate.py)."""
import sys, json, hashlib, importlib.util, datetime
import numpy as np, pandas as pd
from . import data, metrics
from .baselines import BASELINES, DIAGNOSTIC

REGISTRY = data.ROOT / "evalkit" / "registry.json"

def _null_control(train, rng):
    """Break the link between song identity and play history: every train song takes another train song's identity
    (ids, title, artist) while keeping its own timestamps. A model that really learns from the user's history must fall to chance."""
    cols = ["trackId", "albumId", "artistIds", "artist", "trackName", "song"]
    ident = train.drop_duplicates("song").set_index("song")[cols]
    shuffled = pd.DataFrame(ident.values[rng.permutation(len(ident))], index=ident.index, columns=cols).reindex(train.song.values)
    out = train.copy()
    for c in cols: out[c] = shuffled[c].values
    return out

def score_predictor(fn, cutoffs, name="", indep_n=8, null=False, window=None):
    """Run fn on the open pool (tried songs + decoys) of every fold. Returns the scored pool (shuffled public order) with
    attrs['indep'] = median |score(pool) - score(candidate alone)| / std(score) over `indep_n` random candidates per fold."""
    d = data._load_all(); pub = data.anon_streams(d); meta_all = data.load_meta_all()
    rows, dev = [], []
    for c, pool in data.make_open_folds(cutoffs, d):
        mask = (d.t < c).values
        train = pub[mask]
        if window: train = window(train, c)
        if null: train = _null_control(train, np.random.default_rng(int(c.strftime("%Y%m%d"))))
        cands, meta, order = data.public_view(pool, meta_all, d[mask], seed=int(c.strftime("%Y%m%d")))
        sc = np.asarray(fn(train.copy(), cands, meta, c), float)
        assert sc.shape == (len(cands),) and np.isfinite(sc).all(), "need one finite score per candidate"
        if indep_n and name not in DIAGNOSTIC:
            rng = np.random.default_rng(7); idx = rng.choice(len(cands), min(indep_n, len(cands)), replace=False)
            one = np.array([np.asarray(fn(train.copy(), cands.iloc[[i]].reset_index(drop=True), meta, c), float)[0] for i in idx])
            dev.append(np.abs(one - sc[idx]) / (sc.std() + 1e-12))
        rows.append(pool.iloc[order].assign(fold=str(c.date()), score=sc))
    out = pd.concat(rows, ignore_index=True)
    out.attrs["indep"] = float(np.median(np.concatenate(dev))) if dev else np.nan
    return out

def _q(x, alpha): return tuple(np.nanpercentile(x, [100 * alpha / 2, 100 * (1 - alpha / 2)]).round(3))

def summarize(preds, nboot=300, refs=(), n_looks=1):
    """Tables. Bootstrap CIs resample songs within folds (shared across models => paired differences). CI level is 95% for
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
                           sauc_ci=_q([b["sauc"] for b in B[n]], alpha), plift_ci=_q([b["plift"] for b in B[n]], alpha))
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
            y, s = g.love.values, g.score.values
            lo.setdefault(n, {})[f] = np.nanpercentile([metrics.auc(y[i], s[i]) for i in (rng.integers(0, len(y), len(y)) for _ in range(200))], 100 * alpha / 2).round(3)
    tabs["fold_auc_lower_bound"] = pd.DataFrame(lo)
    tabs["independence"] = pd.Series({n: df.attrs.get("indep", np.nan) for n, df in preds.items()}, name="median_rel_score_change_alone_vs_pool").round(4)
    return tabs

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
    nboot, indep_n, null, win = opt("--nboot", 300), opt("--indep-n", 8), "--null-control" in argv, opt("--window", "all")
    skip = {argv[i + 1] for i, a in enumerate(argv) if a in ("--nboot", "--indep-n", "--window")}
    mods = [a for a in argv if not a.startswith("--") and a not in skip]
    from .ablate import WINDOWS
    cutoffs = data.SEALED_CUTOFFS if sealed else data.DEV_CUTOFFS
    hashes = [_sha(p) for p in mods]
    if sealed:
        from . import make_sealed; assert make_sealed.main(), "sealed labels do not match manifest (data changed?)"
        reg = json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}
        done = {h for l in _log_lines() if l.startswith("{") for h in json.loads(l).get("files", [])}
        for p, h in zip(mods, hashes):
            if h not in reg: sys.exit(f"{p}: sha256 {h[:12]} is not registered. Only the main session registers the final model(s): python -m evalkit.register {p} <name>")
            if h in done: sys.exit(f"{p}: this exact file was already evaluated on sealed (one look per registered model)")
    preds = {}
    for p in mods:
        spec = importlib.util.spec_from_file_location("pred", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for k, f in (getattr(m, "PREDICTORS", None) or {p: m.predict}).items(): preds[k] = f
    if not mods: preds = dict(BASELINES)
    n_looks = sealed_looks(hashes) if sealed else 1
    scored = {k: score_predictor(f, cutoffs, k, indep_n, null, WINDOWS[win]) for k, f in preds.items()}
    if sealed:  # log every sealed evaluation (file hash included) so overuse is visible and multiplicity is counted
        data.SEALED_DIR.mkdir(exist_ok=True)
        with open(data.SEALED_DIR / "runs.log", "a") as fh:
            fh.write(json.dumps(dict(ts=datetime.datetime.utcnow().isoformat(), models=list(preds), files=hashes, looks_after=n_looks)) + "\n")
    pd.set_option("display.width", 260, "display.max_columns", 40, "display.max_colwidth", 40)
    refs = [b for b in BASELINES if b in scored]
    print(f"window={win} null_control={null} n_looks={n_looks} (CI level {100 * (1 - 0.05 / n_looks):.2f}%)")
    tabs = summarize(scored, nboot, refs=refs if mods else (), n_looks=n_looks)
    for k, t in tabs.items():
        print(f"\n== {k}"); print(t.to_string(index=k in ("fold_auc_tried", "fold_auc_lower_bound", "independence")))
    return scored, tabs

if __name__ == "__main__": main(sys.argv[1:])
