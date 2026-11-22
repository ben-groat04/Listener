"""W6 round 2 / E1: verify the essentia sealed path on dev data (modelled on evalkit.selftest_v53.hide_and_rebuild, evalkit untouched).
~30 TUNE tried tracks of one dev cutoff with a stored previewUrl (seeded draw), hide their dev MERT/compact rows (EVALKIT_HIDE_KEYS_FILE), run `evalkit.sealed_prep --cutoffs C --keys-file --out TMP
--no-reuse-dev-audio --essentia` (stages fetch,mert,compact + essentia), compare rebuilt rows with the dev rows and ref_w4r1_music / ref_w4r1_listening scores (original vs hidden vs rebuilt).
    python3 -W ignore -m catalogue.w6r2_e1 OUTDIR"""
import os, sys, json, time, glob, subprocess, tempfile, pathlib
import numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import data, run, features, refs
OUT = pathlib.Path(sys.argv[1]); CUT = str(data.TUNE_CUTOFFS[-1].date()) if hasattr(data.TUNE_CUTOFFS[-1], "date") else str(data.TUNE_CUTOFFS[-1]); N = 30; SEED = 62
TOL_ROW = 2e-3; TOL_ESS = 2e-2; TOL_SCORE = 1e-6
def reset(): features.reset(); refs._MOD.clear(); refs._GUARD.clear()
def score(nm, F): return np.asarray(refs.fn(nm)(F["train"], F["cands"], F["meta"], F["c"]), float)
F = run.prepare_folds([CUT])[0]; meta = F["meta"]; ids = F["cands"].trackId.values; dec = F["pool"].is_decoy.values[F["order"]] == 1
idx, arr = features.mert_full(); ks = pd.Series(features.clip_keys(meta, ids)); eidx = features.compact_index("w4r1-what-in-the-music")
has_url = pd.Series([isinstance(u, str) for u in meta.previewUrl.reindex(ids).values])
ok = ks.notna() & ks.isin(set(idx)) & ks.isin(set(eidx)) & pd.Series(~dec) & has_url
pick = np.random.default_rng(SEED).permutation(np.flatnonzero(ok.values))[:N]; keys = sorted(set(ks.iloc[pick])); assert len(keys) >= 25, len(keys)
tmp = pathlib.Path(tempfile.mkdtemp(prefix="w6r2_e1_")); (tmp / "keys.txt").write_text("\n".join(keys)); out = tmp / "feats"
res = dict(cutoff=CUT, n_clips=len(keys), seed=SEED); names = ("ref_w4r1_music", "ref_w4r1_listening")
reset(); s0 = {n: score(n, F) for n in names}
os.environ["EVALKIT_HIDE_KEYS_FILE"] = str(tmp / "keys.txt"); os.environ["EVALKIT_SEALED_FEATURE_DIR"] = str(out); reset()
sh = {n: score(n, F) for n in names}
for n in names: res[f"hidden_changes_{n}"] = float(np.abs(sh[n] - s0[n]).max())
res["hide_nonvacuous"] = {n: res[f"hidden_changes_{n}"] > 1e-4 for n in names}
res["hide_hook_covers"] = "MERT shards (features.mert_full), both compact stores (features.compact incl. w4r1-what-in-the-music = essentia); NOT the raw essentia shards (not read at score time)"
t0 = time.time()
r = subprocess.run([sys.executable, "-W", "ignore", "-m", "evalkit.sealed_prep", "--cutoffs", CUT, "--keys-file", str(tmp / "keys.txt"), "--out", str(out), "--no-reuse-dev-audio", "--threads", "2", "--essentia"],
                   cwd=str(data.ROOT), env=dict(os.environ), capture_output=True, text=True); res["prep_wall_s"] = time.time() - t0
(OUT / "e1_prep_stdout.txt").write_text(r.stdout[-6000:] + "\n---STDERR---\n" + r.stderr[-3000:])
if r.returncode != 0: res["status"] = "ERROR"; res["error"] = (r.stdout[-1500:] + r.stderr[-1500:]); json.dump(res, open(OUT / "essentia_check_raw.json", "w"), indent=1); sys.exit(1)
log = [json.loads(l) for l in open(out / "prep_log.jsonl")][-1]; res["prep_log"] = log
man = pd.read_csv(out / "previews" / "manifest.csv"); man = man[man.key.isin(keys)]; assert man.ok.all() and len(man) == len(keys) and (man.source == "stored").all(); res["sources"] = man.source.value_counts().to_dict()
# MERT rows
nb = {}
for f in sorted((out / "mert-v1").glob("shard_*.npz")):
    z = np.load(f); nb.update({str(k): z["feat"][i] for i, k in enumerate(z["md5"])})
assert set(nb) == set(keys); d = [float(np.abs(nb[k].astype(np.float32) - arr[idx[k]].astype(np.float32)).max()) for k in keys]
res["mert_row_max_abs_diff"] = max(d); res["mert_rows_exact"] = int(sum(x == 0 for x in d))
# raw essentia shards vs dev shards
dev = {}
for f in sorted(glob.glob(str(data.ROOT / ".cache/shared/w4-essentia/shard_*.npz"))):
    z = np.load(f); pk = set(map(str, z["md5"])) & set(keys)
    if not pk: continue
    off = z["patch_off"]; m = list(map(str, z["md5"]))
    for k in pk: i = m.index(k); dev[k] = {n: z[n][i] for n in ("act_mean", "act_max", "emb_mean", "emb_std")} | {"patch_act": z["patch_act"][off[i]:off[i + 1]], "patch_t": z["patch_t"][off[i]:off[i + 1]]}
new = {}
for f in sorted((out / "essentia").glob("shard_*.npz")):
    z = np.load(f); off = z["patch_off"]
    for i, k in enumerate(map(str, z["md5"])): new[k] = {n: z[n][i] for n in ("act_mean", "act_max", "emb_mean", "emb_std")} | {"patch_act": z["patch_act"][off[i]:off[i + 1]], "patch_t": z["patch_t"][off[i]:off[i + 1]]}
res["essentia_clips_rebuilt"] = len(new); res["essentia_clips_with_dev_rows"] = len(dev); assert set(new) == set(keys) and set(dev) == set(keys), (len(new), len(dev))
ed = {n: max(float(np.abs(new[k][n].astype(np.float32) - dev[k][n].astype(np.float32)).max()) for k in keys) for n in ("act_mean", "act_max", "emb_mean", "emb_std", "patch_act", "patch_t")}
res["essentia_raw_max_abs_diff"] = ed; res["essentia_patch_counts_equal"] = bool(all(len(new[k]["patch_act"]) == len(dev[k]["patch_act"]) for k in keys))
# compact rows
for nm in ("w4r1", "w4r1-what-in-the-music"):
    zr = np.load(out / "compact" / nm / "compact.npz"); zd = np.load(features.DEV_COMPACT[nm]); di = {str(k): i for i, k in enumerate(zd["md5"])}; mx = {}
    for a in zr.files:
        if a == "md5" or a not in zd.files: continue
        diffs = []
        for j, k in enumerate(map(str, zr["md5"])):
            if k in di and k in set(keys): diffs.append(float(np.nanmax(np.abs(zr[a][j].astype(np.float32) - zd[a][di[k]].astype(np.float32)))))
        mx[a] = max(diffs) if diffs else None
    res[f"compact_{nm}_max_abs_diff"] = mx; res[f"compact_{nm}_rows"] = int(sum(str(k) in set(keys) for k in zr["md5"]))
reset(); s1 = {n: score(n, F) for n in names}
for n in names: res[f"score_max_abs_diff_{n}"] = float(np.abs(s1[n] - s0[n]).max())
# essentia cost per clip: from the prep stdout shard lines (excludes model load) and the stage wall time
import re
m = re.findall(r"shard \d+/\d+ ok=(\d+) failed=(\d+) ([\d.]+)s", r.stdout + r.stderr)
res["essentia_stage_wall_s"] = log.get("essentia_s"); res["essentia_s_per_clip_stage_wall_incl_model_load"] = log.get("essentia_s", np.nan) / len(keys)
res["essentia_shard_lines"] = m
if m: res["essentia_s_per_clip_excl_model_load"] = sum(float(x[2]) for x in m) / sum(int(x[0]) for x in m)
res["tolerances"] = dict(mert_row=TOL_ROW, essentia_raw=TOL_ESS, compact=TOL_ESS, score=TOL_SCORE)
ok = (res["mert_row_max_abs_diff"] <= TOL_ROW and max(ed.values()) <= TOL_ESS and all(res[f"score_max_abs_diff_{n}"] <= TOL_SCORE for n in names) and all(res["hide_nonvacuous"].values()))
res["status"] = "PASS" if ok else "FAIL"; json.dump(res, open(OUT / "essentia_check_raw.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str))
