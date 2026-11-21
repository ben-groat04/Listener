"""Dense per-clip patch store from frozen essentia shards -> .cache/w4r2-lr/ (regenerable, ~1 min).  Run from /home/user/Listener/taste-model.
emb.npy [N,PM,1280] f16, act.npy [N,PM,605] f16 (zero padded), n.npy [N] patch counts, md5.npy."""
import glob, os, numpy as np
ROOT = "/home/user/Listener/taste-model/"; OUT = ROOT + ".cache/w4r2-lr/"; os.makedirs(OUT, exist_ok=True)
PM = 29
fs = sorted(glob.glob(ROOT + ".cache/shared/w4-essentia/shard_*.npz")); N = 0
for f in fs: N += len(np.load(f)["md5"])
E = np.lib.format.open_memmap(OUT + "emb.npy", "w+", np.float16, (N, PM, 1280)); A = np.lib.format.open_memmap(OUT + "act.npy", "w+", np.float16, (N, PM, 605))
md, ns = [], []; k = 0
for f in fs:
    z = np.load(f); off = z["patch_off"]; pe = z["patch_emb"]; pa = z["patch_act"]
    for i in range(len(z["md5"])):
        a, b = off[i], min(off[i + 1], off[i] + PM); n = b - a
        E[k, :n] = pe[a:b]; A[k, :n] = pa[a:b]; ns.append(n); md.append(z["md5"][i]); k += 1
E.flush(); A.flush(); np.save(OUT + "n.npy", np.array(ns)); np.save(OUT + "md5.npy", np.array(md)); print(N, min(ns), max(ns))
