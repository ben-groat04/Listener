"""Compact per-clip store from the frozen essentia shards: act_mean, act_max, emb_mean, emb_std, 6 time segments (5 s each) of mean head activations.
Output: .cache/w4r1-what-in-the-music/compact.npz (regenerable, ~1 min).  Run from /home/user/Listener/taste-model."""
import glob, os, numpy as np
ROOT = "/home/user/Listener/taste-model/"; OUT = ROOT + ".cache/w4r1-what-in-the-music/"; os.makedirs(OUT, exist_ok=True)
md, am, ax, em, es, sg = [], [], [], [], [], []
for f in sorted(glob.glob(ROOT + ".cache/shared/w4-essentia/shard_*.npz")):
    z = np.load(f); off = z["patch_off"]; t = z["patch_t"]; pa = z["patch_act"].astype(np.float32)
    md += list(z["md5"]); am.append(z["act_mean"]); ax.append(z["act_max"]); em.append(z["emb_mean"]); es.append(z["emb_std"])
    S = np.zeros((len(z["md5"]), 6, pa.shape[1]), np.float32)
    for i in range(len(z["md5"])):
        a, b = off[i], off[i + 1]; seg = np.minimum((t[a:b] / 5.0).astype(int), 5)
        for s in range(6):
            m = seg == s
            S[i, s] = pa[a:b][m].mean(0) if m.any() else np.nan
    sg.append(S.astype(np.float16))
np.savez(OUT + "compact.npz", md5=np.array(md), act_mean=np.concatenate(am), act_max=np.concatenate(ax), emb_mean=np.concatenate(em), emb_std=np.concatenate(es), seg=np.concatenate(sg))
print(len(md))
