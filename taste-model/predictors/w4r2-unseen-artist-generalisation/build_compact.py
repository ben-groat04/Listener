"""Build compact per-clip feature cache (regenerable from frozen shared caches). Output: .cache/w4r2-unseen/compact.npz
keys = md5(previewUrl); mert3 [n,3,768] (layers 0-3, 4-8, 9-11 averaged over layers and 4 windows), clap [n,768], eact [n,605] (essentia act_mean), eemb [n,1280] (emb_mean); NaN rows if a cache lacks the clip."""
import glob, os, numpy as np
R = "/home/user/Listener/taste-model/.cache/"
out = R + "w4r2-unseen/"; os.makedirs(out, exist_ok=True)
mk, m3 = [], []
for f in sorted(glob.glob(R + "shared/w3r1-mert-v1/shard_*.npz")):
    z = np.load(f); a = z["feat"]
    mk += list(z["md5"])
    m3.append(np.stack([a[:, :, 0:4].astype(np.float32).mean((1, 2)), a[:, :, 4:9].astype(np.float32).mean((1, 2)), a[:, :, 9:12].astype(np.float32).mean((1, 2))], 1).astype(np.float16))
mk = np.array(mk); m3 = np.concatenate(m3)
z = np.load(R + "shared/w3r1-clap/emb.npz"); ci = {k: i for i, k in enumerate(z["k"])}
clap = np.full((len(mk), 768), np.nan, np.float16)
for j, k in enumerate(mk):
    if k in ci: clap[j] = z["v"][ci[k]]
ei = {}; ea = []; ee = []; n = 0
for f in sorted(glob.glob(R + "shared/w4-essentia/shard_*.npz")):
    z = np.load(f)
    for k in z["md5"]: ei[k] = n; n += 1
    ea.append(z["act_mean"]); ee.append(z["emb_mean"])
ea = np.concatenate(ea); ee = np.concatenate(ee)
eact = np.full((len(mk), ea.shape[1]), np.nan, np.float16); eemb = np.full((len(mk), ee.shape[1]), np.nan, np.float16)
for j, k in enumerate(mk):
    if k in ei: eact[j] = ea[ei[k]]; eemb[j] = ee[ei[k]]
np.savez(out + "compact.npz", md5=mk, mert3=m3, clap=clap, eact=eact, eemb=eemb)
print(len(mk), m3.shape, np.isnan(eact[:, 0]).mean())
