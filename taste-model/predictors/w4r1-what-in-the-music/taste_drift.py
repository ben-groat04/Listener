"""Descriptive: stability of the learned 'taste axis' over cutoffs. For each TUNE cutoff, ridge (the final A config) is fitted on train songs; we report the cosine between coefficient vectors of cutoffs i and j and the number of mature train songs.
Also the Spearman of per-head Spearman-with-target between the first and the last cutoff. Run: python3 -W ignore predictors/w4r1-what-in-the-music/taste_drift.py"""
import sys, numpy as np, pandas as pd, json
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, "/home/user/Listener/taste-model/predictors/w4r1-what-in-the-music")
from evalkit import run, data
from sklearn.linear_model import Ridge
from scipy.stats import spearmanr
import predict as P
folds = run.prepare_folds(data.TUNE_CUTOFFS, "main"); cfg = {**P.CFG, "alpha": 10000.0}
L = json.load(open(P.ROOT + ".cache/shared/w4-essentia/labels.json")); names = [f"{h['name']}:{c}" for h in L["heads"] for c in h["classes"]]
W, SP, N = [], [], []
for F in folds:
    st = data.song_table(F["train"]).reset_index(); st = st[st.trackId.isin(F["meta"].index)].reset_index(drop=True)
    X, ok = P._view(st.trackId.values, F["meta"], cfg); X = X[:, 0]; mat = (st["first"] < F["c"] - pd.Timedelta(days=90)).values & ok
    qa = st["first"].dt.to_period("Q").astype(str).values; yr = pd.Series(st.plays90.values[mat]).groupby(qa[mat]).rank(pct=True).values
    mu = X[ok].mean(0); sd = X[ok].std(0) + 1e-6; Z = (X[mat] - mu) / sd
    W.append(Ridge(alpha=cfg["alpha"]).fit(Z, yr).coef_); N.append(mat.sum())
    SP.append(pd.DataFrame(Z).corrwith(pd.Series(yr), method="spearman").values)
W = np.array(W); Wn = W / np.linalg.norm(W, axis=1, keepdims=True); C = Wn @ Wn.T
print("n mature train songs per cutoff:", N)
print("cosine(coef) cutoff1 vs cutoff k:", C[0].round(2)); print("cosine(coef) consecutive:", np.diag(C, 1).round(2)); print("cosine last vs k:", C[-1].round(2))
print("spearman of per-head target-correlation between first (n=%d) and last (n=%d) cutoff: %.2f" % (N[0], N[-1], spearmanr(SP[0], SP[-1])[0]))
top = np.argsort(-np.abs(W[-1]))[:15]; print("top |coef| heads at last cutoff, coefficient by cutoff (x1e3):")
for t in top: print(f"{names[t]:55s}", (W[:, t] * 1e3).round(2))
