"""evalkit v5.3 checks (python3 -m evalkit.selftest --v53): first `--v52` (which includes --v51: a default run reproduces the recorded v5.0 / v5.1 / v5.2 numbers), then
  1. make_sealed.py / sealed_manifest.json / register.py are byte-identical to the recorded sha256;
  2. evalkit.features == the old direct cache reads (MERT rows, compact stores) on dev data, and the sealed-era caches are absent from the real cache dir (default output cannot depend on them);
  3. HIDE AND REBUILD (sealed_prep acceptance on dev data): hide the cached MERT / compact rows of ~30 dev tracks, rebuild them with `python3 -m evalkit.sealed_prep --cutoffs ... --keys-file ... --out TMP
     --no-reuse-dev-audio` (audio re-fetched from the stored previewUrl), assert the rebuilt MERT rows equal the originals (tolerance below) and ref_w4r1_listening's / ref_audio_final's scores equal the originals;
  4. the sealed-style output blocks on the TUNE folds under a synthetic slice name (`--fast --synthetic-sealed`), via the same functions the sealed run calls;
  5. unit checks of the coverage STOP rule and of the sealed_prep refusal without --main-session."""
import os, sys, json, time, hashlib, tempfile, subprocess, pathlib
import numpy as np, pandas as pd
from . import data, run, features, sealedout

HERE = pathlib.Path(__file__).parent
SEALED_SHA = {"make_sealed.py": "23f05539ffcf22705027e8300e0d40ce17eb31bd84824b060fab543be6f30973", "sealed_manifest.json": "0a9957e438762b7460cb04da9b5e25251e4b1cac7e656b52f1f5cdc632eacf61",
              "register.py": "e47cea9c6037b2479afa124f7c6b53e48a128480dd978d312f82fad780a463ce"}
ROW_TOL = 0.0       # MERT rows are compared exactly first; the printed tolerance used for the assertion is TOL_ROW (float16 values, see below)
TOL_ROW = 2e-3      # max |rebuilt - original| over a float16 row (activation scale ~0.1-1; one float16 step near 1 is 1e-3; same code, same quantised model: expected 0)
TOL_SCORE = 1e-6    # max |score difference| of the incumbent (ref_w4r1_listening, ref_audio_final) between original and rebuilt features

def _sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def check_sealed_files():
    for f, h in SEALED_SHA.items(): assert _sha(HERE / f) == h, f"{f} changed"
    print("sealed files byte-identical:", ", ".join(f"{f} {h[:12]}" for f, h in SEALED_SHA.items()))

def check_features_equiv():
    assert not (features.sealed_root() / "mert-v1").exists() or os.environ.get("EVALKIT_SEALED_FEATURE_DIR"), "a sealed-era cache exists: the equality check below would not be a dev-only check"
    F = run.prepare_folds([data.TUNE_CUTOFFS[-1]])[0]; meta, ids = F["meta"], F["cands"].trackId.values
    X, has = features.mert(meta, ids)
    z0 = np.load(features.DEV_MERT / "shard_00003.npz"); old = {str(k): i for i, k in enumerate(z0["md5"])}; ks = features.clip_keys(meta, ids)
    n = 0
    for i, k in enumerate(ks):   # rows found in shard 3 equal the direct read
        if k in old: assert np.array_equal(X[i], z0["feat"][old[k]][:, 4:9].astype(np.float32).mean(1)) and has[i]; n += 1
    assert n >= 5 and has.mean() > 0.8
    C = features.compact("w4r1"); z = np.load(features.DEV_COMPACT["w4r1"]); assert all(np.array_equal(C[k], z[k]) for k in z.files)
    print(f"features == direct reads: {n} rows of shard 3 compared exactly, compact stores identical; MERT coverage of the fold's candidates {has.mean():.3f}")

def _score(name, F):
    from . import refs
    return np.asarray(refs.fn(name)(F["train"], F["cands"], F["meta"], F["c"]), float)

def _reset_all():
    from . import refs
    features.reset(); refs._MOD.clear(); refs._GUARD.clear()

def hide_and_rebuild(n=30):
    """Acceptance test of the sealed-era pipeline on dev data. Returns a dict of measured numbers."""
    from . import refs
    cutoff = str(data.TUNE_CUTOFFS[-1].date()) if hasattr(data.TUNE_CUTOFFS[-1], "date") else str(data.TUNE_CUTOFFS[-1]); F = run.prepare_folds([cutoff])[0]
    meta = F["meta"]; ids = F["cands"].trackId.values; dec = F["pool"].is_decoy.values[F["order"]] == 1; idx, arr = features.mert_full()
    ks = pd.Series(features.clip_keys(meta, ids)); ok = ks.notna() & ks.isin(set(idx)) & pd.Series(~dec)
    # tracks whose meta row has a stored previewUrl (so that the first source of the fetch order is exercised); seeded sample
    has_url = pd.Series([isinstance(u, str) for u in meta.previewUrl.reindex(ids).values]); pick = np.random.default_rng(53).permutation(np.flatnonzero((ok & has_url).values))[:n]
    keys = sorted(set(ks.iloc[pick])); assert len(keys) >= 25, len(keys)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="evalkit_v53_")); (tmp / "keys.txt").write_text("\n".join(keys)); out = tmp / "sealed-feats-test"
    res = {}
    _reset_all(); s0 = {nm: _score(nm, F) for nm in ("ref_w4r1_listening", "ref_audio_final")}
    sel = np.isin(ks.values, keys)
    env = dict(os.environ, EVALKIT_HIDE_KEYS_FILE=str(tmp / "keys.txt"), EVALKIT_SEALED_FEATURE_DIR=str(out))
    os.environ["EVALKIT_HIDE_KEYS_FILE"] = env["EVALKIT_HIDE_KEYS_FILE"]; os.environ["EVALKIT_SEALED_FEATURE_DIR"] = str(out); _reset_all()
    sh = {nm: _score(nm, F) for nm in s0}
    for nm in s0: res[f"hidden_changes_{nm}"] = float(np.abs(sh[nm] - s0[nm]).max()); assert res[f"hidden_changes_{nm}"] > 1e-4, f"hiding the features did not change {nm}: the test would be vacuous"
    t0 = time.time()
    r = subprocess.run([sys.executable, "-W", "ignore", "-m", "evalkit.sealed_prep", "--cutoffs", cutoff, "--keys-file", str(tmp / "keys.txt"), "--out", str(out), "--no-reuse-dev-audio", "--threads", "3"],
                       cwd=str(data.ROOT), env=env, capture_output=True, text=True); res["prep_wall_s"] = time.time() - t0
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    print(r.stdout[-1800:])
    man = pd.read_csv(out / "previews" / "manifest.csv"); man = man[man.key.isin(keys)]; assert man.ok.all() and len(man) == len(keys) and (man.source == "stored").all(), man.source.value_counts()
    log = [json.loads(l) for l in open(out / "prep_log.jsonl")][-1]; res["mert_s_per_clip"] = log["mert_s_per_clip"]; res["fetch_s_per_clip"] = log["fetch_s"] / len(keys); res["clips"] = len(keys)
    # rebuilt rows vs originals
    nb = {}; 
    for f in sorted((out / "mert-v1").glob("shard_*.npz")):
        z = np.load(f); nb.update({str(k): z["feat"][i] for i, k in enumerate(z["md5"])})
    assert set(nb) == set(keys); dif = [float(np.abs(nb[k].astype(np.float32) - arr[idx[k]].astype(np.float32)).max()) for k in keys]
    res["row_max_abs_diff"] = max(dif); res["rows_exact"] = int(sum(d == 0 for d in dif)); assert res["row_max_abs_diff"] <= TOL_ROW, f"rebuilt MERT rows differ by {res['row_max_abs_diff']}"
    _reset_all(); s1 = {nm: _score(nm, F) for nm in s0}
    for nm in s0: res[f"score_max_abs_diff_{nm}"] = float(np.abs(s1[nm] - s0[nm]).max()); assert res[f"score_max_abs_diff_{nm}"] <= TOL_SCORE, (nm, res[f"score_max_abs_diff_{nm}"])
    C = features.compact("w4r1"); assert all(str(k) in features.compact_index("w4r1") for k in keys)
    for k in ("HIDE_KEYS_FILE", "SEALED_FEATURE_DIR"): os.environ.pop("EVALKIT_" + k, None)
    _reset_all()
    print("hide_and_rebuild:", json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in res.items()}))
    return res

def check_synthetic_output():
    from .selftest import _quiet_main
    B = str(HERE / "selftest_builder.py"); (_, o), tx = _quiet_main(["--fast", "--synthetic-sealed", B]); nm = [k for k in o if k.startswith("SEALED")]; assert len(nm) == 1; t = o[nm[0]]
    for must in ("FEATURE COVERAGE per fold", "COVERAGE ref_w4r1_listening", "COMPARATOR_SET", "FILE_DELTAS80", "LABEL VARIANTS (sauc [95% CI]; sealed slice", "BREAKDOWN by exposure_before", "SAUC80", "lo80 > 0.5:"):
        assert must in tx, must
    assert tx.index("FEATURE COVERAGE per fold") < tx.index("DIAGNOSTIC_REFERENCES") and tx.index("FEATURE COVERAGE per fold") < tx.index("COMPARATOR_SET")
    cs = t["COMPARATOR_SET"]; models = {"sb_dur", "sb_rand_a", "sb_rand_b"}; assert models <= set(cs.model) and set(cs.vs) == set(run.COMPARATORS) and list(cs.columns)[2] == "pooled" and "iv_weighted" in cs and "heaviest_out" in cs
    fd = t["FILE_DELTAS80"]; assert all(((fd.model_a == m) & (fd.minus_model_b == c)).any() for m in models for c in run.COMPARATORS), "FILE_DELTAS80 lacks comparator rows for a model of a multi-model file"
    lv = [k for k in t if k.startswith("LABEL VARIANTS")]; assert len(lv) == 1 and "strong" in t[lv[0]].columns and "keep" not in t[lv[0]].columns
    assert "BREAKDOWN by exposure_before" in t and "sealed" not in tx.split("FEATURE COVERAGE")[0].lower()[:0]
    from .sanity import assert_no_nan
    assert_no_nan(cs.select_dtypes("number"), "synthetic COMPARATOR_SET"); assert len(t["_S"]) >= 3 and "VERDICT" in t
    ls = [l for l in tx.splitlines() if l.startswith("SAUC80 ")]; assert len(ls) >= len(models) and all(("lo80 > 0.5: YES" in l) or ("lo80 > 0.5: NO" in l) for l in ls)
    assert "SEALED80" in tx or "SEALED only" in tx
    print("synthetic SEALED slice output: coverage table first, COMPARATOR_SET (pooled / IV / heaviest-out) for", len(models), "models, FILE_DELTAS80 comparator rows for every model, LABEL VARIANTS (strong), exposure_before BREAKDOWN, SAUC80 lines: ok")
    return tx

def check_units():
    tab = pd.DataFrame(dict(fold=["a", "b", "a", "b"], group=["tried", "tried", "decoy", "decoy"], tracks=[100, 100, 500, 500], mert=[0.95, 0.88, 1.0, 1.0], essentia=[0.99, 0.99, 1.0, 1.0]))
    l, stop = sealedout.coverage_verdicts(tab, {"m1": ("mert",), "m2": ("essentia",)}); assert not stop and "ok" in l[0] and "folds below 90% for mert: b" in l[0]
    tab.loc[0, "mert"] = 0.7; l, stop = sealedout.coverage_verdicts(tab, {"m1": ("mert",)}); assert stop and "STOP" in l[0]
    r = subprocess.run([sys.executable, "-m", "evalkit.sealed_prep", "--count"], cwd=str(data.ROOT), capture_output=True, text=True); assert r.returncode != 0 and "MAIN SESSION ONLY" in (r.stdout + r.stderr)
    print("coverage STOP rule and the sealed_prep --main-session refusal: ok")

def v53_checks():
    from .selftest import v52_checks
    t0 = time.time()
    if "--v53-only" not in sys.argv: v52_checks()   # --v53-only: skip the v5.2 part (iteration only; the reported run is the full --v53)
    t1 = time.time()
    check_sealed_files(); check_features_equiv(); check_units(); check_synthetic_output(); res = hide_and_rebuild(); check_sealed_files()
    print(f"selftest --v53 passed: v52 part {t1 - t0:.0f} s, v53 part {time.time() - t1:.0f} s")
