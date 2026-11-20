"""Score predictors.  Dev (open):   python -m evalkit.run [module.py ...]
Sealed (final, logged): python -m evalkit.run --sealed [module.py ...]
A predictor module exposes `predict(train, cands, meta, cutoff) -> np.ndarray` (or a BASELINES-style dict `PREDICTORS`)."""
import sys, json, hashlib, importlib.util, datetime
import numpy as np, pandas as pd
from . import data, metrics
from .baselines import BASELINES

def score_predictor(fn, cutoffs, sealed=False):
    d = data._load_all()
    rows = []
    for c, fold in data.make_folds(cutoffs, d):
        train = d[d.t < c]
        meta = data.load_meta()
        sc = np.asarray(fn(train.copy(), data.public_candidates(fold), meta, c), float)
        assert len(sc) == len(fold) and np.isfinite(sc).all(), "need one finite score per candidate"
        rows.append(fold.assign(fold=str(c.date()), score=sc))
    return pd.concat(rows, ignore_index=True)

def summarize(preds, nboot=200, ref=None):
    """preds: {name: scored df}. Macro metrics over folds (+95% bootstrap CI over songs; paired CI of AUC diff vs ref)."""
    lines = []; q = lambda x: tuple(np.nanpercentile(x, [2.5, 97.5]).round(3))
    for label in ("love", "strong"):
        for sub, nm in ((None, "all"), (True, "new-artist"), (False, "known-artist")):
            A = {n: metrics.folds_arrays(df, label, sub) for n, df in preds.items()}
            rng = np.random.default_rng(0)
            idxs = [metrics.boot_idx(next(iter(A.values())), rng) for _ in range(nboot)]  # shared => paired
            B = {n: [metrics.macro(a, ix) for ix in idxs] for n, a in A.items()}
            for n, a in A.items():
                y = np.concatenate([f[0] for f in a])
                row = dict(label=label, subset=nm, model=n, base=round(y.mean(), 3),
                           **{k: round(v, 3) for k, v in metrics.macro(a).items()},
                           auc_ci=q([b["auc"] for b in B[n]]), lift_ci=q([b["lift"] for b in B[n]]))
                if ref and n != ref: row["dAUC_vs_" + ref] = q([x["auc"] - z["auc"] for x, z in zip(B[n], B[ref])])
                lines.append(row)
    return pd.DataFrame(lines)

def main(argv):
    sealed = "--sealed" in argv; mods = [a for a in argv if not a.startswith("--")]
    cutoffs = data.SEALED_CUTOFFS if sealed else data.DEV_CUTOFFS
    if sealed:
        from . import make_sealed; assert make_sealed.main(), "sealed labels do not match manifest (data changed?)"
    preds = {}
    for p in mods:
        spec = importlib.util.spec_from_file_location("pred", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for k, f in (getattr(m, "PREDICTORS", None) or {p: m.predict}).items(): preds[k] = f
    if not mods: preds = dict(BASELINES)
    scored = {k: score_predictor(f, cutoffs, sealed) for k, f in preds.items()}
    if sealed:  # log every sealed evaluation so overuse is visible
        data.SEALED_DIR.mkdir(exist_ok=True)
        with open(data.SEALED_DIR / "runs.log", "a") as fh: fh.write(f"{datetime.datetime.utcnow().isoformat()} {list(preds)}\n")
    pd.set_option("display.width", 250, "display.max_columns", 30)
    print(summarize(scored, ref="artist_love_rate" if "artist_love_rate" in scored else None).to_string(index=False))
    print("\nper-fold AUC (love, all songs)")
    print(pd.DataFrame({k: v.groupby("fold").apply(lambda g: metrics.auc(g.love, g.score)) for k, v in scored.items()}).round(3).to_string())
    return scored

if __name__ == "__main__": main(sys.argv[1:])
