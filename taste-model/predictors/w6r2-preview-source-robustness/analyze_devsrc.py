"""sauc of the dev-clip model by the source of the dev clip (stored URL iTunes vs other). usage: python3 analyze_devsrc.py dump.pkl"""
import sys; sys.path.insert(0, "/home/user/Listener/taste-model")
import numpy as np, pandas as pd
from evalkit import metrics, sanity
d = pd.read_pickle(sys.argv[1]); d = d[d.fold_set == "tune"].reset_index(drop=True)
sanity.assert_no_nan(d[["score__a_dev", "score__diag_devsrc", "love", "fold"]], "dump"); sanity.assert_fold_count(d, "tune", name="dump")
v = d["score__diag_devsrc"].values
print("rows %d | dev clip iTunes-URL %d (love rate %.3f) | other stored URL %d (%.3f) | none %d" % (len(d), (v == 1).sum(), d.love[v == 1].mean(), (v == 0).sum(), d.love[v == 0].mean(), (v == -1).sum()))
for nm, m in (("itunes-sourced dev clip", v == 1), ("other stored clip", v == 0)):
    sub = d[m].reset_index(drop=True); r = metrics.dump_sauc(sub, "tune", "a_dev", nboot=1000, seed=20260511); print("%-24s n=%d loved=%d sauc %.3f [95%% %.3f, %.3f]" % ((nm, len(sub), int(sub.love.sum())) + r))
