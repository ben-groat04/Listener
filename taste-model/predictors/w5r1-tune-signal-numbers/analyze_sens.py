"""Sensitivity map from score dumps: sauc and paired delta vs w5_default (artist-cluster bootstrap, shared resamples), chance calibration of best-of-N, early/late reproducibility.
Usage: python3 analyze_sens.py DUMP.pkl [DUMP2.pkl ...]   (run from taste-model/)"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import metrics
ds = [pd.read_pickle(p) for p in sys.argv[1:]]
base = ds[0]; cols = {}
for d in ds:
    for c in d.columns:
        if c.startswith("score__w5_") or c.startswith("score__oat_") or c.startswith("score__rj"): cols[c] = d
NB = 300
def stats(d, folds=None):
    g = d[d.fold_set == "tune"] if "fold_set" in d else d
    if folds is not None: g = g[g.fold.isin(folds)]
    B = metrics.Block(metrics.dump_frame(g.assign(fold_set="tune"), "tune"), "love", NB, 0)
    return B, g
res = {}
allf = sorted(base[base.fold_set == "tune"].fold.unique()); early, late = allf[:5], allf[5:]
for tag, folds in (("all", None), ("early", early), ("late", late)):
    B0, g0 = stats(base, folds); R = {}
    for c, d in cols.items():
        g = d[(d.fold_set == "tune")]
        if folds is not None: g = g[g.fold.isin(folds)]
        assert (g.song.values == g0.song.values).all()
        st = B0.stats(g[c].values, True, ("sauc",)); R[c[7:]] = (st["sauc"][0], st["sauc_b"])
    res[tag] = R
R = res["all"]; dflt = R["w5_default"]
rows = []
for k, (s, b) in R.items():
    d = b - dflt[1]; f = d[np.isfinite(d)]
    rows.append(dict(model=k, sauc=s, delta=s - dflt[0], lo80=np.nanpercentile(f, 10), hi80=np.nanpercentile(f, 90), lo95=np.nanpercentile(f, 2.5), hi95=np.nanpercentile(f, 97.5), P=np.mean(f > 0),
                     d_early=res["early"][k][0] - res["early"]["w5_default"][0], d_late=res["late"][k][0] - res["late"]["w5_default"][0]))
T = pd.DataFrame(rows).set_index("model"); T.to_csv("sens_table_%s.csv" % ("_".join(sorted(set(x.split('.')[0].split('_')[-1] for x in sys.argv[1:]))) ), float_format="%.4f")
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
print(T.sort_values("delta", ascending=False).round(4).to_string())
# chance calibration: under 'all true deltas are 0', observed deltas are noise ~ bootstrap deviations d_i^b - d_i.  best-of-N and spread.
names = [k for k in R if k != "w5_default"]; N = len(names)
D = np.array([R[k][1] - dflt[1] for k in names]); obs = np.array([R[k][0] - dflt[0] for k in names]); ok = np.isfinite(D).all(0); D = D[:, ok]
noise = D - obs[:, None]
mx = noise.max(0); mn = noise.min(0); sd_noise = noise.std(1)
print("\nN configs (excl default) =", N)
print("observed: max delta %.4f, min %.4f, SD of deltas %.4f, mean |delta| %.4f" % (obs.max(), obs.min(), obs.std(), np.abs(obs).mean()))
print("chance (bootstrap noise, true deltas=0): best-of-N delta median %.4f, 80%% %.4f, 95%% %.4f ; worst-of-N median %.4f" % (np.median(mx), np.percentile(mx, 80), np.percentile(mx, 95), np.median(mn)))
print("chance: mean per-config noise SD %.4f ; observed SD of deltas across configs %.4f (ratio %.2f)" % (sd_noise.mean(), obs.std(), obs.std() / sd_noise.mean()))
print("share of configs with |delta| > 1.28*own-noise-SD (two-sided 80%% excl. zero): %.2f (chance 0.20)" % np.mean(np.abs(obs) > 1.2816 * sd_noise))
de = T.loc[names, "d_early"].values; dl = T.loc[names, "d_late"].values
print("early(folds1-5) vs late(folds6-10) delta correlation across configs: pearson %.3f, spearman %.3f" % (np.corrcoef(de, dl)[0, 1], pd.Series(de).corr(pd.Series(dl), method="spearman")))
# winner's curse: best config on early folds, its delta on late folds
b = int(np.argmax(de)); print("best on early: %s early %.4f -> late %.4f ; best on late: %s late %.4f -> early %.4f" % (names[b], de[b], dl[b], names[int(np.argmax(dl))], dl.max(), de[int(np.argmax(dl))]))
