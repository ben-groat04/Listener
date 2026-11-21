"""Compact per-clip feature store from the frozen shared caches (per-row independent, no fitted transform).
Writes .cache/w4r1/compact.npz: keys md5 (sorted union), mert [N,4,768] f16 (mean of layers 4-8 per window), clap [N,768] f16,
ess_act [N,605] f16 (clip mean of head activations), ess_emb [N,1280] f16 (clip mean embedding), has_* bool masks.
Run from /home/user/Listener/taste-model: python3 predictors/w4r1-taste-from-all-listening/build_compact.py"""
import glob, numpy as np
R = "/home/user/Listener/taste-model/.cache/"
mk, ma = [], []
for f in sorted(glob.glob(R + "shared/w3r1-mert-v1/shard_*.npz")):
    z = np.load(f); mk += list(z["md5"]); ma.append(z["feat"][:, :, 4:9].astype(np.float32).mean(2).astype(np.float16))
mk = np.array(mk); ma = np.concatenate(ma)
z = np.load(R + "shared/w3r1-clap/emb.npz"); ck = z["k"]; cv = z["v"]
ek, ea, ee = [], [], []
for f in sorted(glob.glob(R + "shared/w4-essentia/shard_*.npz")):
    z = np.load(f); ek += list(z["md5"]); ea.append(z["act_mean"]); ee.append(z["emb_mean"])
ek = np.array(ek); ea = np.concatenate(ea); ee = np.concatenate(ee)
keys = np.array(sorted(set(mk) | set(ck) | set(ek))); N = len(keys)
def put(k, v):
    out = np.zeros((N,) + v.shape[1:], np.float16); has = np.zeros(N, bool); i = np.searchsorted(keys, k); out[i] = v; has[i] = True; return out, has
mert, hm = put(mk, ma); clap, hc = put(ck, cv); act, he = put(ek, ea); emb, _ = put(ek, ee)
np.savez(R + "w4r1/compact.npz", md5=keys, mert=mert, clap=clap, ess_act=act, ess_emb=emb, has_mert=hm, has_clap=hc, has_ess=he)
print(N, hm.sum(), hc.sum(), he.sum())
