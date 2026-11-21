"""Merge chunk dumps, compute per-variant sauc, paired delta vs default (80% interval, decision80 rule |lo80|<0.005 undecided), summary of spread.  Output: $W5R2_OUT/grid_table.csv"""
import os, sys, glob, json
import numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import metrics
OUT = os.environ["W5R2_OUT"]
ds = [pd.read_pickle(f) for f in sorted(glob.glob(f"{OUT}/dump_chunk*.pkl"))]
d = ds[0].copy()
for x in ds[1:]:
    assert (x[["fold", "artist", "song"]].values == d[["fold", "artist", "song"]].values).all()
    for c in x.columns:
        if c.startswith("score__") and c not in d.columns: d[c] = x[c].values
d.to_pickle(f"{OUT}/grid_merged.pkl")
names = [c[7:] for c in d.columns if c.startswith("score__") and (c[7:].startswith(("oat_", "joint_")) or c == "score__default"[7:])]
rows = []
for n in names:
    if n == "default": continue
    r = metrics.dump_sauc_delta(d, "tune", n, "default", "fold", nboot=300)
    s = metrics.dump_sauc(d, "tune", n, "fold", nboot=50)[0]
    dec = "POS" if r["lo80"] > 0.005 else "NEG" if r["hi80"] < -0.005 else "UNDECIDED"
    rows.append(dict(name=n, sauc=s, delta=r["d"], lo80=r["lo80"], hi80=r["hi80"], P=r["P"], decision80=dec))
t = pd.DataFrame(rows); t.to_csv(f"{OUT}/grid_table.csv", index=False)
print("default sauc", metrics.dump_sauc(d, "tune", "default", "fold", nboot=50)[0])
print(t.round(4).to_string(index=False))
for grp in ("oat_", "joint_"):
    g = t[t.name.str.startswith(grp)]
    print(grp, "n", len(g), "mean delta %.4f sd %.4f max %.4f min %.4f; POS %d NEG %d UNDEC %d" % (g.delta.mean(), g.delta.std(), g.delta.max(), g.delta.min(), (g.decision80 == "POS").sum(), (g.decision80 == "NEG").sum(), (g.decision80 == "UNDECIDED").sum()))
