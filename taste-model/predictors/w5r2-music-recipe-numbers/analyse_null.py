"""Random-label refit calibration: for each permutation refit r, sauc of every grid variant (fit on randomly permuted training target) on the real TUNE tried songs; statistics of (variant - default) per refit,
compared with the real-label statistics from grid_table.csv.  Needs $W5R2_OUT/null_*.pkl (probe.py nullprobe) and grid_table.csv."""
import os, sys, glob, pickle
import numpy as np, pandas as pd
from scipy.stats import rankdata
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import data, run
OUT = os.environ["W5R2_OUT"]; pools = pickle.load(open(run._pool_path(), "rb"))
def pooled(U, Pn): return U / Pn
data_by_fold = {}; scores = {}
for c in data.TUNE_CUTOFFS:
    fns = [f for f in sorted(glob.glob(f"{OUT}/null*_{c}.pkl"))]
    if not fns: continue
    zs = [pickle.load(open(f, "rb")) for f in fns]; z = dict(song=zs[0]["song"], scores={k: v for q in zs for k, v in q["scores"].items()}); assert all((q["song"] == z["song"]).all() for q in zs); t = pools[c]; t = t[t.is_decoy == 0].copy(); t["anon"] = data.anon_song(t.song).values
    pos = {s: i for i, s in enumerate(z["song"])}; ii = np.array([pos.get(s, -1) for s in t.anon.values]); keep = ii >= 0   # HOLDOUT-artist rows are removed from cands before predictors are called
    data_by_fold[c] = t.love.values[keep].astype(int); scores[c] = {k: v[ii[keep]] for k, v in z["scores"].items()}
folds = list(data_by_fold); keys = list(next(iter(scores.values())).keys()); R = sorted({k[0] for k in keys}); names = sorted({k[1] for k in keys})
def sauc(r, n):
    U = Pn = 0.0
    for c in folds:
        y = data_by_fold[c]; s = scores[c][(r, n)]; P = y.sum(); N = len(y) - P
        if P == 0 or N == 0: continue
        rk = rankdata(s); U += rk[y == 1].sum() - P * (P + 1) / 2; Pn += P * N
    return U / Pn
tab = pd.DataFrame({r: {n: sauc(r, n) for n in names} for r in R})
print("folds", len(folds), "refits", len(R), "variants", len(names))
print("null sauc of default per refit:", tab.loc["default"].round(4).tolist())
dl = tab.sub(tab.loc["default"], axis=1).drop("default")
# exclude fill variants from the comparison class (fill matters through the missing-audio indicator, which a random target does not reproduce)
real = pd.read_csv(f"{OUT}/grid_table.csv").set_index("name").delta
def stat(x): return dict(sd=x.std(), max=x.max(), min=x.min(), q90abs=np.quantile(np.abs(x), 0.9), mean=x.mean())
for grp, sel in (("OAT", [n for n in dl.index if n.startswith("oat_")]), ("JOINT", [n for n in dl.index if n.startswith("joint_")]), ("OAT-without-fill", [n for n in dl.index if n.startswith("oat_") and "fill" not in n])):
    rs = pd.DataFrame([stat(dl.loc[sel, r]) for r in R]); rr = stat(real.loc[sel])
    print(f"{grp} n={len(sel)}: real-label spread sd {rr['sd']:.4f} max {rr['max']:+.4f} min {rr['min']:+.4f} q90|d| {rr['q90abs']:.4f} mean {rr['mean']:+.4f}")
    print(f"      null (random target) mean over refits: sd {rs.sd.mean():.4f} max {rs['max'].mean():+.4f} (refit range {rs['max'].min():+.4f}..{rs['max'].max():+.4f}) min {rs['min'].mean():+.4f} q90|d| {rs.q90abs.mean():.4f}")
dl.to_csv(f"{OUT}/null_deltas.csv"); tab.to_csv(f"{OUT}/null_sauc.csv")
