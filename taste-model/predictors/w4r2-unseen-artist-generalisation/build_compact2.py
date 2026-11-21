"""Second compact cache (time-resolved summaries): .cache/w4r2-unseen/compact2.npz, same key order as compact.npz.
mstd [n,768]: std over the 4 MERT windows of the layer 4-8 mean; mdelta [n,768]: last window minus first window (layer 4-8 mean);
eactmax [n,605]: essentia act_max (max over patches); estd [n,1280]: essentia emb_std (std over patches)."""
import glob, numpy as np
R = "/home/user/Listener/taste-model/.cache/"
keys = np.load(R + "w4r2-unseen/compact.npz")["md5"]; pos = {k: i for i, k in enumerate(keys)}
n = len(keys); mstd = np.full((n, 768), np.nan, np.float16); mdelta = mstd.copy()
for f in sorted(glob.glob(R + "shared/w3r1-mert-v1/shard_*.npz")):
    z = np.load(f); a = z["feat"][:, :, 4:9].astype(np.float32).mean(2)   # [m,4,768]
    ii = [pos[k] for k in z["md5"]]; mstd[ii] = a.std(1); mdelta[ii] = a[:, -1] - a[:, 0]
eactmax = np.full((n, 605), np.nan, np.float16); estd = np.full((n, 1280), np.nan, np.float16)
for f in sorted(glob.glob(R + "shared/w4-essentia/shard_*.npz")):
    z = np.load(f); ii = [pos[k] for k in z["md5"] if k in pos]; m = [j for j, k in enumerate(z["md5"]) if k in pos]
    eactmax[ii] = z["act_max"][m]; estd[ii] = z["emb_std"][m]
np.savez(R + "w4r2-unseen/compact2.npz", md5=keys, mstd=mstd, mdelta=mdelta, eactmax=eactmax, estd=estd)
print("ok")
