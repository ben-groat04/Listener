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

def summarize(preds, nboot=300, ref=None):
    """preds: {name: scored df}. Returns table of macro metrics (+95% bootstrap CI on auc/lift) per label/subset."""
    lines = []
    for label in ("love", "strong"):
        for sub, nm in ((None, "all"), (True, "new-artist"), (False, "known-artist")):
            for name, df in preds.items():
                m = metrics.macro(df, label, sub)
                rng = np.random.default_rng(0)
                b = [metrics.macro(df, label, sub, rng) for _ in range(nboot)]
                ci = lambda k: np.nanpercentile([x[k] for x in b], [2.5, 97.5])
                row = dict(label=label, subset=nm, model=name, base=df[df.new_artist == sub][label].mean() if sub is not None else df[label].mean(),
                           **{k: round(v, 3) for k, v in m.items()}, auc_ci=tuple(ci("auc").round(3)), lift_ci=tuple(ci("lift").round(2)))
                if ref and name != ref:  # paired bootstrap of AUC difference vs ref
                    rng = np.random.default_rng(0); dd = []
                    for _ in range(nboot):
                        seed = rng.integers(1 << 30)
                        dd.append(metrics.macro(df, label, sub, np.random.default_rng(seed))["auc"] - metrics.macro(preds[ref], label, sub, np.random.default_rng(seed))["auc"])
                    row["dAUC_vs_" + ref] = tuple(np.percentile(dd, [2.5, 97.5]).round(3))
                lines.append(row)
    return pd.DataFrame(lines)

def main(argv):
    sealed = "--sealed" in argv; mods = [a for a in argv if not a.startswith("--")]
    cutoffs = data.SEALED_CUTOFFS if sealed else data.DEV_CUTOFFS
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
    return scored

if __name__ == "__main__": main(sys.argv[1:])
