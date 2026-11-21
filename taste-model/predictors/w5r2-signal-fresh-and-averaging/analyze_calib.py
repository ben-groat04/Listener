"""Summarise calib.jsonl (null-train refits, real labels): per seed delta vs default for every family member / average; best-of-20, family mean, primary, avgs.  Usage: python3 analyze_calib.py calib.jsonl [OBS_BEST OBS_PRIMARY]"""
import sys, json, numpy as np
R = [json.loads(l) for l in open(sys.argv[1])]; n = len(R); print("seeds", n)
fam = [k for k in R[0]["sauc"] if k.startswith("f_")]; avg = [k for k in R[0]["sauc"] if k.startswith("avg")]
D = np.array([[r["sauc"][m] - r["sauc"]["w5_default"] for m in fam] for r in R]); print("default null sauc per seed", [round(r["sauc"]["w5_default"], 3) for r in R])
best = D.max(1); print("best-of-20 null delta per seed", best.round(4), "mean %.4f max %.4f" % (best.mean(), best.max()))
print("family-mean null delta per seed", D.mean(1).round(4), "mean %.4f" % D.mean())
p = fam.index("f_m0s_q"); print("primary f_m0s_q null delta per seed", D[:, p].round(4), "mean %.4f sd %.4f" % (D[:, p].mean(), D[:, p].std(ddof=1)))
print("fraction of null (seed,config) deltas > 0: %.2f; all-20-positive in %d of %d seeds" % ((D > 0).mean(), ((D > 0).all(1)).sum(), n))
for a in avg: v = np.array([r["sauc"][a] - r["sauc"]["w5_default"] for r in R]); print("null delta", a, v.round(4), "mean %.4f" % v.mean())
print("null sauc range all models: %.3f - %.3f" % (min(min(r["sauc"].values()) for r in R), max(max(r["sauc"].values()) for r in R)))
