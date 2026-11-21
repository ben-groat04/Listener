"""Builds artefacts A (MERT store) and B (essentia store) into .cache/shared-w5r1/. Run: python3 -I predictors/w5r1-shared-prep/build_ab.py  (2 threads max)"""
import glob, json, numpy as np, pandas as pd
R = "/home/user/Listener/taste-model/.cache/"; S = R + "shared/"; O = R + "shared-w5r1/"
man = pd.read_csv(S + "previews/manifest.csv"); ok = set(man[man.ok.astype(bool)].md5)
print("ok manifest", len(ok))
# ---- A
rows = {}  # md5 -> (shard, idx)
shards = sorted(glob.glob(S + "w3r1-mert-v1/shard_*.npz")); tot = 0; dup = 0
for f in shards:
    m = np.load(f)["md5"]; tot += len(m)
    for i, k in enumerate(m):
        if k in ok:
            if k in rows: dup += 1
            rows[str(k)] = (f, i)
md5 = sorted(rows); N = len(md5); print("shard rows", tot, "dups(ok)", dup, "N", N, "missing", len(ok - set(md5)))
assert N == len(ok), "ok manifest not fully covered by shards"
pos = {k: i for i, k in enumerate(md5)}
full = np.lib.format.open_memmap(O + "mert_full.npy", "w+", np.float16, (N, 4, 12, 768))
lm = np.lib.format.open_memmap(O + "mert_layer_mean.npy", "w+", np.float16, (N, 12, 768))
seen = np.zeros(N, bool)
for f in shards:
    z = np.load(f); m = z["md5"]; feat = z["feat"]
    idx = [i for i, k in enumerate(m) if str(k) in pos]
    if not idx: continue
    dst = np.array([pos[str(m[i])] for i in idx]); x = feat[idx]
    full[dst] = x; lm[dst] = x.astype(np.float32).mean(1).astype(np.float16); seen[dst] = True
full.flush(); lm.flush(); del full, lm
assert seen.all()
np.save(O + "mert_md5.npy", np.array(md5))
# verify
full = np.load(O + "mert_full.npy", mmap_mode="r"); lm = np.load(O + "mert_layer_mean.npy", mmap_mode="r")
rng = np.random.default_rng(0); samp = rng.choice(N, 200, replace=False); cache = {}
for i in samp:
    f, j = rows[md5[i]]
    if f not in cache: cache = {f: np.load(f)["feat"]}
    a = cache[f][j]; assert np.array_equal(a.view(np.uint16), np.asarray(full[i]).view(np.uint16)), md5[i]
    assert np.array_equal(a.astype(np.float32).mean(0).astype(np.float16).view(np.uint16), np.asarray(lm[i]).view(np.uint16))
print("A verified 200 rows (bit-equal), N =", N, "nan rows", int(np.isnan(np.asarray(lm[:, 0, 0], np.float32)).sum()))
# ---- B
md, am, ax, em, es, sg = [], [], [], [], [], []; failed = []
for f in sorted(glob.glob(S + "w4-essentia/shard_*.npz")):
    z = np.load(f); off = z["patch_off"]; t = z["patch_t"]; pa = z["patch_act"].astype(np.float32)
    md += [str(k) for k in z["md5"]]; failed += [str(k) for k in z["failed"]]
    am.append(z["act_mean"]); ax.append(z["act_max"]); em.append(z["emb_mean"]); es.append(z["emb_std"])
    Sg = np.zeros((len(z["md5"]), 6, pa.shape[1]), np.float32)
    for i in range(len(z["md5"])):
        a, b = off[i], off[i + 1]; seg = np.minimum((t[a:b] / 5.0).astype(int), 5)
        for s in range(6):
            mk = seg == s
            Sg[i, s] = pa[a:b][mk].mean(0) if mk.any() else np.nan
    sg.append(Sg.astype(np.float16))
o = np.argsort(md); md = np.array(md)[o]
assert len(set(md)) == len(md)
cat = lambda L: np.concatenate(L)[o]
d = dict(md5=md, act_mean=cat(am), act_max=cat(ax), emb_mean=cat(em), emb_std=cat(es), seg_act=cat(sg))
labels = json.load(open(S + "w4-essentia/labels.json"))
miss = sorted(ok - set(md)); extra = sorted(set(md) - ok)
print("essentia N", len(md), "ok-manifest clips absent", len(miss), "extra not in ok", len(extra), "failed listed", len(set(failed)))
np.savez(O + "essentia_compact.npz", **d)
json.dump(dict(labels=labels, missing_md5=miss, failed_in_shards=sorted(set(failed)), extra_not_in_ok_manifest=extra), open(O + "essentia_meta.json", "w"))
# verify seeded sample against shards
z = np.load(O + "essentia_compact.npz"); rng = np.random.default_rng(0); samp = rng.choice(len(md), 200, replace=False)
lookup = {}
for f in sorted(glob.glob(S + "w4-essentia/shard_*.npz")):
    zz = np.load(f); 
    for i, k in enumerate(zz["md5"]): lookup[str(k)] = (f, i)
c = {}
for i in samp:
    f, j = lookup[md[i]]
    if f not in c: c = {f: np.load(f)}
    for k in ["act_mean", "act_max", "emb_mean", "emb_std"]:
        assert np.array_equal(c[f][k][j].view(np.uint16), z[k][i].view(np.uint16)), (k, md[i])
print("B verified 200 rows; shapes", {k: z[k].shape for k in z.files})
