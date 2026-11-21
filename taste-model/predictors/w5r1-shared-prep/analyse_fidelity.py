"""Facts table for artefact C -> prints markdown. Run: python3 -I predictors/w5r1-shared-prep/analyse_fidelity.py"""
import numpy as np
from scipy.stats import spearmanr
R = "/home/user/Listener/taste-model/.cache/shared-w5r1/"
z = np.load(R + "fidelity_sample.npz"); md = z["md5"]; f = z["fp32_4win"].astype(np.float32); q = z["int8_12win"].astype(np.float32)
mert = np.load(R + "mert_full.npy", mmap_mode="r"); ids = list(np.load(R + "mert_md5.npy")); c = np.stack([np.asarray(mert[ids.index(k)]) for k in md]).astype(np.float32)
v = ~np.isnan(f[:, 0, 0, 0]) & ~np.isnan(q[:, 0, 0, 0]); print("clips used", int(v.sum()), "of", len(md)); f, q, c = f[v], q[v], c[v]
def cos(a, b): return (a * b).sum(-1) / (np.linalg.norm(a, axis=-1) * np.linalg.norm(b, axis=-1) + 1e-12)
c1 = np.median(cos(f, c).transpose(2, 0, 1).reshape(12, -1), 1)      # [n,4,12] -> per layer
cm, qm = c.mean(1), q.mean(1); c2 = np.median(cos(cm, qm), 0)
def pcs(x, k=10):
    x = x - x.mean(0); u, s, vt = np.linalg.svd(x, full_matrices=False); return vt[:k]
sp = []
for L in range(12):
    vt = pcs(cm[:, L]); mu = cm[:, L].mean(0); a = (cm[:, L] - mu) @ vt.T; b = (qm[:, L] - mu) @ vt.T
    sp.append([spearmanr(a[:, j], b[:, j])[0] for j in range(10)])
sp = np.array(sp)
print("| layer | median cos fp32 vs cached (per window) | median cos cached 4-win mean vs 12-win mean | Spearman PC1-10 (median / min) cached vs 12-win |\n|---|---|---|---|")
for L in range(12): print(f"| {L+1} | {c1[L]:.4f} | {c2[L]:.4f} | {np.median(sp[L]):.3f} / {sp[L].min():.3f} |")
print("PC1-10 Spearman, layer 12:", np.round(sp[11], 3).tolist())
