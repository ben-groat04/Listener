"""W6 round 2 / E2 step 2: MERT-v1-95M for the iTunes clips (exactly the dev extractor, catalogue.w6_mert) + alignment against the dev clip (same method/fields as shared-w6r1 align.csv).
Runs the equivalence check first (10 existing dev clips re-extracted vs the cached rows; stops if not equal). Loops until the lookup process has finished and everything is processed.
Outputs in .cache/shared-w6r2/: equivalence_check.json, mert_itunes/shard_*.npz (md5 [n] = md5 of the m4a FILE bytes, feat [n,4,12,768] fp16), align.csv.
    python3 -W ignore -m catalogue.w6r2_mert"""
import sys, os, time, glob, json
import numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import data
from catalogue.w6_mert import Extractor
from catalogue import w6_p2
D = data.ROOT / ".cache" / "shared-w6r2"; D1 = data.ROOT / ".cache" / "shared-w6r1"; R = data.ROOT / ".cache"; PRE = R / "shared" / "previews"
TOL = 1e-2
def equiv(ex, n=10):
    cache = {}
    for f in sorted(glob.glob(str(R / "shared/w3r1-mert-v1/shard_*.npz")))[3:6]:
        z = np.load(f); cache.update(zip(z["md5"], z["feat"]))
    man = pd.read_csv(PRE / "manifest.csv"); man = man[man.ok.astype(bool) & man.md5.isin(cache)]; sm = man.sample(n, random_state=62)
    mx, rel, exact, t0 = 0, 0, 0, time.time()
    for _, r in sm.iterrows():
        a = ex(PRE / "audio" / f"{r.md5}.{r.ext}").astype(np.float32); b = cache[r.md5].astype(np.float32)
        assert np.isfinite(a).all() and a.shape == b.shape == (4, 12, 768)
        d = np.abs(a - b).max(); mx = max(mx, float(d)); rel = max(rel, float(np.linalg.norm(a - b) / np.linalg.norm(b))); exact += int(d == 0)
    res = dict(n=n, max_abs_diff=mx, max_rel_l2=rel, n_bitwise_equal=exact, sec_per_clip=(time.time() - t0) / n, tolerance=f"max rel L2 <= {TOL} per clip (fp16 storage, int8 dynamic quantisation)", passed=bool(rel <= TOL))
    json.dump(res, open(D / "equivalence_check.json", "w"), indent=1); print(res, flush=True); assert res["passed"], "equivalence failed: stop E2"
def main():
    ex = Extractor(); (D / "mert_itunes").mkdir(exist_ok=True)
    if not (D / "equivalence_check.json").exists(): equiv(ex)
    U = pd.read_csv(D1 / "universe_tracks.csv").set_index("trackId"); man = pd.read_csv(PRE / "manifest.csv"); man = man[man.ok.astype(bool)].set_index("md5")
    done = set(); [done.update(np.load(f)["md5"]) for f in glob.glob(str(D / "mert_itunes/shard_*.npz"))]
    ap = D / "align.csv"; arows = pd.read_csv(ap) if ap.exists() else pd.DataFrame()
    nsh = len(glob.glob(str(D / "mert_itunes/shard_*.npz"))); keys, feats = [], []; idle = 0; t0 = time.time(); nd = 0
    def flush():
        nonlocal nsh, keys, feats
        if keys:
            np.savez(D / "mert_itunes/tmp.npz", md5=np.array(keys), feat=np.stack(feats)); os.replace(D / "mert_itunes/tmp.npz", D / f"mert_itunes/shard_{nsh:05d}.npz"); nsh += 1; keys, feats = [], []
    while True:
        fin = os.path.exists(D / "lookup_finished.flag")
        pm = pd.read_csv(D / "previews_manifest.csv"); pm = pm[pm.ok.astype(bool)].drop_duplicates("md5"); todo = [r for r in pm.to_dict("records") if r["md5"] not in done]
        for r in todo:
            p = D / "previews_itunes" / f"{r['md5']}.m4a"; u = U.loc[r["trackId"]]; dev = u.md5 if isinstance(u.md5, str) else ""
            a = dict(trackId=r["trackId"], md5=r["md5"], dev_md5=dev, align_offset_s=np.nan, align_score=np.nan, align_margin=np.nan, dev_is_itunes=int(isinstance(u.previewUrl, str) and "itunes.apple.com" in u.previewUrl),
                     same_url=int(r["url_md5"] == dev))
            if dev and dev in man.index:
                try: a.update(w6_p2.align(PRE / "audio" / f"{dev}.{man.loc[dev, 'ext']}", p))
                except Exception as e: a["err"] = str(e)[:80]
            arows = pd.concat([arows, pd.DataFrame([a])]); keys.append(r["md5"]); feats.append(ex(p)); done.add(r["md5"]); nd += 1
            if len(keys) >= 50: flush(); arows.to_csv(ap, index=False); print("mert", nd, round((time.time() - t0) / nd, 2), "s/clip incl align", flush=True)
        flush()
        if len(arows): arows.drop_duplicates("md5").to_csv(ap, index=False)
        if not todo:
            idle += 1
            if fin and idle >= 2: break
            time.sleep(30)
        else: idle = 0
    print("mert done", len(done), "clips", nd, "this run, wall", round(time.time() - t0), "s", flush=True)
if __name__ == "__main__": main()
