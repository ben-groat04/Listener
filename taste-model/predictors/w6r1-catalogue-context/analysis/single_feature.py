"""Single-feature and new/known-artist breakdown from a --dump-scores pickle (TUNE, fast).  Usage: python3 -W ignore single_feature.py DUMP.pkl
Asserts: 10 folds, no NaN in love / new_artist / scores."""
import sys, pandas as pd, numpy as np
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import metrics
d = pd.read_pickle(sys.argv[1]); fs = d.fold_set.unique()[0]; x = d[d.fold_set == fs]
assert x.fold.nunique() == 10 and len(x) == 1074, (x.fold.nunique(), len(x))
sc = [c for c in x.columns if c.startswith("score__")]
assert not x[sc + ["love", "new_artist"]].isna().any().any()
def pooled(sub, c):
    num = den = 0
    for f, g in sub.groupby("fold"):
        p = g[g.love == 1][c].values; n = g[g.love == 0][c].values
        if len(p) == 0 or len(n) == 0: continue
        num += (p[:, None] > n[None, :]).sum() + 0.5 * (p[:, None] == n[None, :]).sum(); den += len(p) * len(n)
    return num / den, den
for c in [c for c in sc if "raw_" in c or "ctx_" in c or "blend" in c or "ref_w4r1_listening" in c or "artist_recent" in c]:
    a = metrics.dump_sauc(d, fs, c[7:], group="fold", nboot=300)
    print(f"{c[7:]:<18} sauc {a[0]:.3f} [{a[1]:.3f},{a[2]:.3f}]  new {pooled(x[x.new_artist == 1], c)[0]:.3f}  known {pooled(x[x.new_artist == 0], c)[0]:.3f}")
