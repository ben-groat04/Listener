"""Paired deltas (model - w5_default) on TUNE from a score dump, 80% interval (10th..90th percentile, artist-cluster bootstrap, nboot 1000) and 95% bound.  Usage: analyze_tuned.py DUMP fold_set prefix1,prefix2 [group]"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import metrics
d = pd.read_pickle(sys.argv[1]); fs = sys.argv[2]; pre = sys.argv[3].split(","); grp = sys.argv[4] if len(sys.argv) > 4 else "fold"
models = [c[7:] for c in d.columns if c.startswith("score__") and any(c[7:].startswith(p) for p in pre)]
for m in models:
    r = metrics.dump_sauc_delta(d, fs, m, "w5_default", grp, nboot=1000)
    s = metrics.dump_sauc(d, fs, m, grp, nboot=200)[0]
    print("%-45s sauc %.4f  delta %+.4f  80%% [%+.4f, %+.4f]  lo95 %+.4f  P(d>0) %.2f" % (m, s, r["d"], r["lo80"], r["hi80"], r["lo95"], r["P"]))
