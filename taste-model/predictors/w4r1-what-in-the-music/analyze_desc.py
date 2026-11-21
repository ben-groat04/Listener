"""Descriptive + out-of-sample (sign from train per fold) AUC of the 10 clip-level librosa descriptors (and duration) vs love, TUNE tried songs; artist-cluster bootstrap CI (60).  Run: python3 -W ignore predictors/w4r1-what-in-the-music/analyze_desc.py"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, "/home/user/Listener/taste-model/predictors/w4r1-what-in-the-music")
from evalkit import run, data
import predict as P
NM = ["loudness_dB", "spec_centroid", "spec_rolloff", "spec_flatness", "spec_bandwidth", "onset_strength", "zero_crossing", "loudness_std", "dyn_range_dB", "log2_tempo/120", "duration_s"]
cfg = {**P.CFG, "feat": "desc", "tf": "none"}
rows = []
for F in run.prepare_folds(data.TUNE_CUTOFFS, "main"):
    pool = F["pool"].iloc[F["order"]].reset_index(drop=True); cands, meta = F["cands"], F["meta"]; tried = (pool.is_decoy == 0).values
    def get(tids):
        X, ok = P._view(tids, meta, cfg); d = meta.durationMs.reindex(tids).values / 1000.0
        return np.c_[X[:, 0], d], ok & np.isfinite(d)
    X, ok = get(cands.trackId.values)
    st = data.song_table(F["train"]).reset_index(); st = st[st.trackId.isin(meta.index)].reset_index(drop=True); Xt, okt = get(st.trackId.values)
    mat = (st["first"] < F["c"] - pd.Timedelta(days=90)).values & okt; qa = st["first"].dt.to_period("Q").astype(str).values
    yr = pd.Series(st.plays90.values[mat]).groupby(qa[mat]).rank(pct=True).values
    sg = np.array([np.sign(pd.Series(Xt[mat][:, j]).corr(pd.Series(yr), method="spearman")) for j in range(Xt.shape[1])])
    k = tried & ok; rows.append((pd.DataFrame(dict(fold=str(F["c"].date()), artist=cands.artist.values[k], love=pool.love.values[k])), X[k], np.repeat(sg[None], k.sum(), 0)))
D = pd.concat([r[0] for r in rows], ignore_index=True); XA = np.concatenate([r[1] for r in rows]); SG = np.concatenate([r[2] for r in rows]); y = D.love.values; fold = D.fold.values
def auc(S, w):
    num = np.zeros(S.shape[1]); den = 0
    for f in np.unique(fold):
        m = fold == f; yy = y[m]; ww = w[m]; Sm = S[m]; pos = np.where(yy == 1)[0]; neg = np.where(yy == 0)[0]
        g = (Sm[pos][:, None, :] > Sm[neg][None]) + .5 * (Sm[pos][:, None, :] == Sm[neg][None]); W = ww[pos][:, None] * ww[neg][None]; num += np.einsum("ijd,ij->d", g, W); den += W.sum()
    return num / den
rng = np.random.default_rng(0); ua = D.artist.unique(); ai = pd.Series(range(len(ua)), index=ua); aidx = ai[D.artist].values
a0, o0 = auc(XA, np.ones(len(D))), auc(XA * SG, np.ones(len(D))); B = []; BO = []
for b in range(60):
    w = rng.multinomial(len(ua), np.ones(len(ua)) / len(ua))[aidx].astype(float); B.append(auc(XA, w)); BO.append(auc(XA * SG, w))
lo, hi = np.percentile(B, [2.5, 97.5], 0), np.percentile(BO, [2.5, 97.5], 0)   # [2, d]: row 0 = 2.5th, row 1 = 97.5th
print("n", len(D), "loved", y.sum())
for j, n in enumerate(NM): print(f"{n:16s} AUC {a0[j]:.3f} [{lo[0][j]:.3f},{lo[1][j]:.3f}]   out-of-sample signed AUC {o0[j]:.3f} [{hi[0][j]:.3f},{hi[1][j]:.3f}]  sign agreement {np.mean(SG[:, j] > 0):.2f}")
