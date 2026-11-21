"""Reliability: bootstrap SE of paired deltas and split-half (by artist) agreement, per metric. Output: results/a1_*.npz, a1_summary.csv"""
import sys, itertools, time, json; sys.path.insert(0, ".")
from lib import *
from scipy.stats import spearmanr
NB = int(sys.argv[1]) if len(sys.argv) > 1 else 200; NS = NB
d = load("tune"); rng = np.random.default_rng(20260521)
cols = ["score__" + m for m in MODELS]
os.makedirs("results", exist_ok=True)
t0 = time.time(); boot = {}; half = {}
for k, f in METRICS.items():
    B = np.zeros((NB, len(MODELS))); H = np.zeros((NS, 2, len(MODELS)))
    r1 = np.random.default_rng(1); r2 = np.random.default_rng(2)
    for b in range(NB):
        ix = artist_resample(d, r1); dd = d.iloc[ix].reset_index(drop=True)
        B[b] = [f(dd, c) for c in cols]
    for b in range(NS):
        ia, ib = artist_resample(d, r2, 0.5)
        for j, ix in enumerate((ia, ib)):
            dd = d.iloc[ix].reset_index(drop=True); H[b, j] = [f(dd, c) for c in cols]
    P = np.array([f(d, c) for c in cols]); boot[k] = (P, B); half[k] = H
    print(k, round(time.time() - t0), flush=True)
np.savez("results/a1_raw.npz", **{k + "__point": v[0] for k, v in boot.items()}, **{k + "__boot": v[1] for k, v in boot.items()}, **{k + "__half": half[k] for k in half})
