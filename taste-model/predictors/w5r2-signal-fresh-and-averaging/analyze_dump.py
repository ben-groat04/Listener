"""LOFO + per-fold table for a model pair from a --dump-scores pickle. Usage: python3 analyze_dump.py DUMP.pkl MODEL_A MODEL_B [fold_set]  (run from taste-model/)"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import metrics
d = pd.read_pickle(sys.argv[1]); a, b = sys.argv[2], sys.argv[3]; fs = sys.argv[4] if len(sys.argv) > 4 else "tune"
r = metrics.dump_sauc_delta(d, fs, a, b, nboot=300); print("ALL", {k: round(v, 4) for k, v in r.items()})
g = d[d.fold_set == fs]; folds = sorted(g.fold.astype(str).unique())
for f in folds:
    sub = d[(d.fold_set != fs) | (d.fold.astype(str) != f)]
    r = metrics.dump_sauc_delta(sub, fs, a, b, nboot=300); print("LOFO drop", f, {k: round(v, 4) for k, v in r.items()})
fm = metrics.fold_meta(d, fs, a, b, nboot=300)
print({k: v for k, v in fm.items() if k != "table"}); print(fm["table"].round(4).to_string())
