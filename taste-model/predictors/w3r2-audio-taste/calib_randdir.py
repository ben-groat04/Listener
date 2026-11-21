"""Calibration behind the null-control note in the report. Usage (from /home/user/Listener/taste-model): python3 -W ignore predictors/w3r2-audio-taste/calib_randdir.py
"""
# calibration: sauc of RANDOM linear directions (in the whitened audio PCA space of the final model) vs the real labels, TUNE tried pool, mean of 3 draws
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, "/home/user/Listener/taste-model/predictors/w3r2-audio-taste")
import predict as P
from evalkit import run, data
from scipy.stats import rankdata
folds = run.prepare_folds(data.TUNE_CUTOFFS); rng = np.random.default_rng(0); ND = 60
cfgs = [{**P.CFG, **c} for c in P.FINAL]
S = np.zeros((ND, 0)); per = []
for F in folds:
    cands, meta, c = F["cands"], F["meta"], F["c"]; pool = F["pool"].iloc[F["order"]].reset_index(drop=True)
    sc = np.zeros((ND, len(cands)))
    for cfg in cfgs:
        res = P._fit(F["train"], meta, c, cfg); bl, ok = P._blocks(cands.trackId.values, meta, cfg)
        Pm = P._design(res, [X[ok] for X in bl], cands.trackId.values[ok], meta, cfg, cfg["mode"] == "local")
        W = rng.standard_normal((Pm.shape[1], ND)); d = Pm @ W
        if cfg["mode"] == "local": d = d.reshape(ok.sum(), 4, ND).mean(1)
        s = np.zeros((len(cands), ND)); s[ok] = d; s = (s - s[ok].mean(0)) / (s[ok].std(0) + 1e-9); sc += s.T
    per.append((pool.love.values, (pool.is_decoy.values == 0), sc))
def sauc(draw):
    num = den = 0
    for y, tm, sc in per:
        yy = y[tm]; s = sc[draw][tm]; r = rankdata(s); n1 = yy.sum(); n0 = len(yy) - n1
        if n1 == 0 or n0 == 0: continue
        auc = (r[yy == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0); num += auc * n1 * n0; den += n1 * n0
    return num / den
a = np.array([sauc(i) for i in range(ND)]); m3 = a[:ND // 3 * 3].reshape(-1, 3).mean(1)
print("single random-direction sauc: mean %.3f sd %.3f  q2.5 %.3f q97.5 %.3f" % (a.mean(), a.std(), *np.percentile(a, [2.5, 97.5])))
print("3-draw mean: sd %.3f range %.3f..%.3f ; fraction outside harness band (0.475,0.519): %.2f" % (m3.std(), m3.min(), m3.max(), np.mean((m3 < 0.475) | (m3 > 0.519))))
