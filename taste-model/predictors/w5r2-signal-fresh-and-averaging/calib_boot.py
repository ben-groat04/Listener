"""Chance calibration #2 (no refit): best-of-family under 'no true effect' by the artist-cluster bootstrap of the observed dump, deltas re-centred per config (so every config's true delta is 0 but the
cross-config correlation of the real scores is kept).  Usage: python3 calib_boot.py DUMP.pkl (run from taste-model/)"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, "/home/user/Listener/taste-model/predictors/w5r2-signal-fresh-and-averaging")
from evalkit import metrics
import grid as G
d = pd.read_pickle(sys.argv[1]); g = d[d.fold_set == "tune"]; B = metrics.dump_block(d, "tune", "fold", nboot=1000, seed=1)
st = lambda m: B.stats(g["score__" + m].values, True, ("sauc",))
b0 = st("w5_default"); fam = ["f_" + k for k in G.FAMILY]; res = {}
for m in fam + list(G.AVG):
    s = st(m); res[m] = (float(s["sauc"][0] - b0["sauc"][0]), s["sauc_b"] - b0["sauc_b"])
D = np.array([res[m][0] for m in fam]); Bt = np.array([res[m][1] for m in fam])      # 20 x 1000
C = Bt - D[:, None]                                                                  # centred
best = np.nanmax(C, axis=0); obs_best = D.max(); i = int(D.argmax())
print("observed deltas (family):", dict(zip(fam, D.round(4)))); print("observed best", fam[i], round(obs_best, 4), " mean over family", round(D.mean(), 4), " frac>0", (D > 0).mean())
print("null best-of-20 (centred bootstrap): mean %.4f  80%%q %.4f  90%%q %.4f  95%%q %.4f ; P(null best >= observed best)=%.3f" % (np.nanmean(best), *np.nanpercentile(best, [80, 90, 95]), np.mean(best >= obs_best)))
mean_null = np.nanmean(C, axis=0)
print("family MEAN delta: observed %.4f; centred-bootstrap sd %.4f; P(null mean >= obs)=%.3f" % (D.mean(), np.nanstd(mean_null), np.mean(mean_null >= D.mean())))
j = fam.index("f_" + G.PRIMARY); print("primary %s observed %.4f; null distribution of a single pre-specified delta: sd %.4f, 90%%q %.4f" % (fam[j], D[j], np.nanstd(C[j]), np.nanpercentile(C[j], 90)))
for m in G.AVG:
    d_, b_ = res[m]; c = b_ - d_; print("avg %s observed %.4f  null sd %.4f 90%%q %.4f" % (m, d_, np.nanstd(c), np.nanpercentile(c, 90)))
# sign test: how many of 20 family deltas are > 0 under null (centred bootstrap has mean 0): distribution of the count of positive *uncentred-shifted*? use rank: P(null count>=obs count) via bootstrap of centred deltas
cnt = (C > 0).sum(0); print("null count of positive deltas (of 20): mean %.1f; P(count>= %d)=%.3f" % (cnt.mean(), (D > 0).sum(), np.mean(cnt >= (D > 0).sum())))
