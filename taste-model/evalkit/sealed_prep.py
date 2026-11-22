"""MAIN SESSION ONLY.  Sealed-era feature pipeline (evalkit v5.3):  python3 -m evalkit.sealed_prep --main-session [--count] [options]
Builders, leads and devil's advocates never run this (it enumerates the tracks of the SEALED folds; for the sealed cutoffs it refuses to start without --main-session). It prints only counts, runtimes and
per-fold coverage (share of tried songs / decoys / train tracks that have features): never labels, never track ids.

What it does (stages, in order; --stages a,b,c selects; default fetch,mert,compact):
  enumerate  the meta tracks of the folds (default: the five sealed cutoffs; --cutoffs 2023-10-01,... runs it on dev folds for tests): train tracks (in the fold's train history), tried pool, decoys.
             Priority: tried first, then train, decoys last (inside a group: fold order). One clip key per track (evalkit.features.clip_key_of).
  fetch      preview audio for every key without a MERT row (dev caches and the output directory are searched first), in this order of sources: (1) the stored meta previewUrl, (2) Spotify embed by
             spotifyId (p.scdn.co), (3) the iTunes Search fallback (title + primary artist + |duration difference| <= 5 s, as evalkit.fetch_itunes), (4) Deezer search (same acceptance rule).
             The source of each clip is recorded in OUT/previews/manifest.csv (column `source`: stored | spotify_embed | itunes | deezer | dev_audio). --no-reuse-dev-audio re-downloads clips whose audio
             is already in the dev preview cache (used by the acceptance test). Catalogue clients: catalogue.catalogue (throttled per host).
  mert       MERT-v1-95M extraction with EXACTLY the code path of the dev cache (predictors/w3r1-content-audio/build_mert.py: its `decode` and `windows`, 4 windows of 5 s, 24 kHz, per-clip z-score, dynamic
             int8 linear layers, 2 threads, mean over time of each of the 12 layers) into OUT/mert-v1/shard_*.npz (same layout: md5 = clip key, feat [n,4,12,768] float16). Resumable.
  compact    rebuilds the derived caches the references read from the sealed-era MERT shards (OUT/compact/w4r1/compact.npz: layers 4-8 mean per window, same code as build_compact.py), and, when sealed-era
             essentia shards exist, OUT/compact/w4r1-what-in-the-music/compact.npz (same code as that build_compact.py).
  essentia   (optional; ~0.46 s per clip, hours) essentia extraction on the sealed-era clips (predictors/w4-shared-prep/build_essentia.py --prev), only needed if a registered final uses essentia / ref_w4r1_music.
  deezer     (optional; only if a registered final uses catalogue context) Deezer lookup per track (search + track detail, ~2 API calls per track at ~4 req/s) -> OUT/deezer/context.jsonl, keyed by the
             public opaque trackId. Uses catalogue.catalogue (the shared prep's reusable client).
Options: --count (dry run: track counts, missing clips, runtime estimate; no network, no model)  --out DIR (default evalkit.features.sealed_root())  --threads N (downloads, default 3)  --limit N (first N missing
clips in priority order)  --retry (retry failed fetches)  --sec-per-clip S (estimate input, default 1.8)  --keys-file F (only these clip keys; acceptance test)  --report (coverage only).
Everything is resumable. The sealed-era cache directory is versioned (features.SEALED_VERSION); a change of the extraction code needs a new version name, never an overwrite."""
import sys, os, time, json, glob, hashlib, subprocess, threading, importlib.util, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np, pandas as pd
from . import data, features

ROOT = data.ROOT
SEC_PER_CLIP = 1.8     # MERT seconds per clip measured for the dev cache (shared FEATURES.md); the acceptance test measures it again
GROUP_RANK = {"tried": 0, "train": 1, "decoy": 2}
UA = "taste-eval-research/0.1"
MCOLS = ["key", "previewUrl", "source", "ok", "ext", "bytes", "duration_s", "error"]

def _log(*a): print(*a, flush=True)

# ------------------------------------------------------------------ enumerate
def enumerate_tracks(cutoffs):
    """(membership frame [fold, group, trackId(public)], track frame indexed by public trackId with name, artistNames, durationMs, previewUrl, spotifyId, key). Labels are never read."""
    from . import run
    mem, metas = [], []
    for F in run.prepare_folds(cutoffs, part="all"):
        fold = str(F["c"].date()); m = F["meta"]; pool, order = F["pool"], F["order"]; dec = pool.is_decoy.values[order] == 1; ids = F["cands"].trackId.values
        for g, t in (("tried", ids[~dec]), ("decoy", ids[dec]), ("train", pd.Index(F["train"].trackId.unique()).values)): mem.append(pd.DataFrame(dict(fold=fold, group=g, trackId=t)))
        metas.append(m)
    mem = pd.concat(mem, ignore_index=True).drop_duplicates()
    U = pd.concat(metas); U = U[~U.index.duplicated()]
    U = U.reindex(mem.trackId.unique()); U["key"] = features.clip_keys(U, U.index.values)
    return mem, U

def work_list(mem, U):
    """Distinct clip keys in priority order (tried, train, decoy; inside a group by fold) with the meta fields needed to fetch them."""
    m = mem.assign(rank=mem.group.map(GROUP_RANK)).sort_values(["rank", "fold"], kind="stable")
    m = m.drop_duplicates("trackId"); W = m.join(U[["name", "artistNames", "durationMs", "previewUrl", "spotifyId", "key"]], on="trackId")
    return W[W.key.notna()].drop_duplicates("key").reset_index(drop=True)

# ------------------------------------------------------------------ stores
def have_mert(out):
    """Clip keys that have a MERT row: dev shards (minus the keys the acceptance test hides) plus the output directory's shards."""
    h = set()
    for f in glob.glob(str(features.DEV_MERT / "shard_*.npz")): h |= set(map(str, np.load(f)["md5"]))
    h -= features._hidden()
    for f in glob.glob(str(out / "mert-v1" / "shard_*.npz")): h |= set(map(str, np.load(f)["md5"]))
    return h

def manifest(out):
    p = out / "previews" / "manifest.csv"; return pd.read_csv(p) if p.exists() else pd.DataFrame(columns=MCOLS)

def _save_manifest(rows, out):
    p = out / "previews" / "manifest.csv"; p.parent.mkdir(parents=True, exist_ok=True); tmp = p.with_suffix(".tmp")
    pd.DataFrame(rows, columns=MCOLS).drop_duplicates("key", keep="last").to_csv(tmp, index=False); os.replace(tmp, p)

def dev_audio():
    """key -> path of the dev preview audio (md5 of previewUrl is the dev file name)."""
    man = pd.read_csv(ROOT / ".cache" / "shared" / "previews" / "manifest.csv"); man = man[man.ok.astype(bool)]
    return {r.md5: ROOT / ".cache" / "shared" / "previews" / "audio" / f"{r.md5}.{r.ext}" for r in man.itertuples()}

# ------------------------------------------------------------------ count / coverage
def coverage_table(mem, U, out):
    """Per fold and group: tracks, share with a clip key, share with a MERT row (dev or sealed-era store). No labels."""
    h = have_mert(out); rows = []
    for (fold, g), d in mem.groupby(["fold", "group"], sort=True):
        k = U.key.reindex(d.trackId.values); rows.append(dict(fold=fold, group=g, tracks=len(d), has_key=round(float(k.notna().mean()), 3), mert=round(float(k.isin(h).mean()), 3)))
    return pd.DataFrame(rows)

def count_report(mem, U, W, out, spc):
    h = have_mert(out); miss = W[~W.key.isin(h)]; man = manifest(out); fetched = set(man[man.ok.astype(bool)].key)
    todo_fetch = miss[~miss.key.isin(fetched)]; has_url = todo_fetch.previewUrl.map(lambda u: isinstance(u, str)).sum()
    n_mert = len(miss); fetch_s = has_url * 0.5 / 3 + (len(todo_fetch) - has_url) * 2.5   # stored url ~0.5 s / 3 threads; other sources ~2.5 s per clip (1 s embed gap, iTunes 3.5 s gap when reached)
    _log(f"tracks: {mem.trackId.nunique()} distinct, {len(mem)} fold-group memberships; distinct clip keys {len(W)} (tracks without any audio source: {int(U.key.isna().sum())})")
    _log(f"clips without a MERT row: {n_mert} (to fetch: {len(todo_fetch)}, of which with stored previewUrl: {int(has_url)}); by group in priority order: " + ", ".join(f"{g}={int((miss.group == g).sum())}" for g in GROUP_RANK))
    _log(f"estimate: fetch ~{fetch_s / 60:.0f} min, MERT ~{n_mert * spc / 60:.0f} min at {spc} s per clip (2 threads) => ~{(fetch_s + n_mert * spc) / 60:.0f} min plus the optional stages: "
         f"deezer ~{2 * len(W) / 4 / 60:.0f} min for {len(W)} tracks (~2 calls each at ~4 req/s); essentia ~{n_mert * 0.46 / 60:.0f} min for {n_mert} clips (0.46 s per clip measured in W4)")
    print(coverage_table(mem, U, out).to_string(index=False), flush=True)

# ------------------------------------------------------------------ fetch
def _download(url):
    for k in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40); b = r.read()
            if len(b) > 1000: return b, r.headers.get("Content-Type")
        except Exception: time.sleep(1.5 * (k + 1))
    return None, None

def _ext(url, ctype):
    p = url.split("?")[0].lower()
    for e in ("mp3", "m4a", "mp4", "aac", "ogg", "wav"):
        if p.endswith("." + e): return e
    return {"audio/mpeg": "mp3", "audio/mp4": "m4a", "audio/x-m4a": "m4a", "audio/aac": "aac"}.get((ctype or "").split(";")[0], "bin")

def _duration(path):
    try: return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True, timeout=30).stdout.strip())
    except Exception: return float("nan")

def _catalogue():
    sys.path.insert(0, str(ROOT)); from catalogue import catalogue as C; return C

def _artist0(r):
    a = r.artistNames; return a[0] if isinstance(a, (list, np.ndarray)) and len(a) else ""

def deezer_match(C, r):
    """Deezer search result accepted by the iTunes rule (normalised title + primary artist, |duration difference| <= 5 s) or None."""
    from .fetch_itunes import norm, norm_title, artist_parts
    dur = r.durationMs
    if not isinstance(r.name, str) or not _artist0(r) or dur is None or pd.isna(dur): return None
    ok = []
    for x in C.dz_search(_artist0(r), r.name) or []:
        if norm_title(x.get("title", "")) != norm_title(r.name) and norm_title(x.get("title_short", "")) != norm_title(r.name): continue
        if norm(_artist0(r)) not in artist_parts((x.get("artist") or {}).get("name", "")): continue
        dd = abs(x.get("duration", 0) * 1000 - dur)
        if dd <= 5000: ok.append((dd, x))
    return min(ok, key=lambda t: t[0])[1] if ok else None

def candidate_urls(C, r):
    """Yield (source, url) in the fixed order: stored previewUrl, Spotify embed, iTunes fallback, Deezer. Later sources are queried only if the earlier ones failed (generator)."""
    from .fetch_itunes import accept
    if isinstance(r.previewUrl, str): yield "stored", r.previewUrl
    if isinstance(r.spotifyId, str):
        e = C.sp_embed(r.spotifyId)
        if e and e.get("preview_url"): yield "spotify_embed", e["preview_url"]
    if isinstance(r.name, str) and _artist0(r):
        a = accept(C.it_search(f"{_artist0(r)} {r.name}"), _artist0(r), r.name, r.durationMs)
        if a: yield "itunes", a["previewUrl"]
        d = deezer_match(C, r)
        if d and d.get("preview"): yield "deezer", d["preview"]

def fetch_one(C, r, out, reuse):
    key = r.key
    if reuse is not None and key in reuse: return dict(key=key, previewUrl=r.previewUrl, source="dev_audio", ok=True, ext=reuse[key].suffix[1:], bytes=reuse[key].stat().st_size, duration_s=np.nan, error="")
    tried = []
    for src, url in candidate_urls(C, r):
        b, ct = _download(url)
        if b is None: tried.append(src + ":download failed"); continue
        e = _ext(url, ct); p = out / "previews" / "audio" / f"{key}.{e}"; p.parent.mkdir(parents=True, exist_ok=True); tmp = p.with_suffix(f".tmp{threading.get_ident()}"); tmp.write_bytes(b); os.replace(tmp, p)
        d = _duration(p)
        if np.isfinite(d) and d > 1: return dict(key=key, previewUrl=url if src != "stored" else r.previewUrl, source=src, ok=True, ext=e, bytes=len(b), duration_s=d, error="")
        tried.append(src + ":unreadable")
    return dict(key=key, previewUrl=r.previewUrl, source="", ok=False, ext="", bytes=0, duration_s=np.nan, error=";".join(tried) or "no source")

def stage_fetch(W, out, threads, limit, retry, reuse_dev):
    C = _catalogue(); h = have_mert(out); man = manifest(out); done = set(man[man.ok.astype(bool) | (not retry)].key)
    todo = W[~W.key.isin(h) & ~W.key.isin(done)]; todo = todo.head(limit) if limit else todo
    rows = man.to_dict("records"); reuse = dev_audio() if reuse_dev else None; t0 = time.time(); _log(f"fetch: {len(todo)} clips")
    with ThreadPoolExecutor(threads) as ex:
        for i, res in enumerate(ex.map(lambda r: fetch_one(C, r, out, reuse), list(todo.itertuples()))):
            rows.append(res)
            if i % 100 == 99: _save_manifest(rows, out); _log(f"fetch {i + 1}/{len(todo)} {int(time.time() - t0)} s")
    _save_manifest(rows, out); m = manifest(out); m = m[m.key.isin(W.key)]
    _log(f"fetch done in {time.time() - t0:.0f} s; manifest rows ok {int(m.ok.sum())} of {len(m)}; sources: " + ", ".join(f"{k}={v}" for k, v in m[m.ok.astype(bool)].source.value_counts().items()))

# ------------------------------------------------------------------ MERT (exactly the dev code path)
def _build_mert_module():
    sp = importlib.util.spec_from_file_location("evalkit_build_mert", str(ROOT / "predictors" / "w3r1-content-audio" / "build_mert.py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m

def audio_path(out, key, source, ext, dev):
    if source == "dev_audio": return dev.get(key)
    return out / "previews" / "audio" / f"{key}.{ext}"

def stage_mert(W, out, limit, shard=100):
    import torch
    from transformers import AutoModel
    bm = _build_mert_module(); torch.set_num_threads(2); NW = bm.NW
    h = have_mert(out); man = manifest(out); man = man[man.ok.astype(bool)].set_index("key"); dev = dev_audio()
    todo = [(k, man.loc[k]) for k in W.key if k in man.index and k not in h]; todo = todo[:limit] if limit else todo
    _log(f"mert: {len(todo)} clips to do"); d = out / "mert-v1"; d.mkdir(parents=True, exist_ok=True)
    if not todo: return 0.0
    m = AutoModel.from_pretrained("m-a-p/MERT-v1-95M", trust_remote_code=True).eval(); H = []
    for l in m.encoder.layers: l.register_forward_hook(lambda mod, i, o: H.append((o[0] if isinstance(o, tuple) else o).detach()))
    m = torch.ao.quantization.quantize_dynamic(m, {torch.nn.Linear}, dtype=torch.qint8)
    nsh = len(glob.glob(str(d / "shard_*.npz"))); keys, feats = [], []; t0 = time.time()
    def flush():
        nonlocal nsh, keys, feats
        if keys:
            tmp = d / f"shard_{nsh:05d}.npz.tmp.npz"; np.savez(tmp, md5=np.array(keys), feat=np.stack(feats)); os.replace(tmp, d / f"shard_{nsh:05d}.npz"); nsh += 1; keys, feats = [], []
    for i, (k, r) in enumerate(todo):
        p = audio_path(out, k, r.source, r.ext, dev)
        w = bm.windows(bm.decode(p)) if p is not None and Path(p).exists() else None
        if w is None: keys.append(k); feats.append(np.full((NW, 12, 768), np.nan, np.float16)); continue
        H.clear()
        with torch.inference_mode(): m(w)
        keys.append(k); feats.append(torch.stack(H).mean(2).permute(1, 0, 2).numpy().astype(np.float16))
        if len(keys) >= shard: flush(); _log(f"mert {i + 1}/{len(todo)} {int(time.time() - t0)} s")
    flush(); spc = (time.time() - t0) / len(todo); _log(f"mert done: {len(todo)} clips in {time.time() - t0:.0f} s = {spc:.2f} s per clip"); return spc

# ------------------------------------------------------------------ compact caches (same build code as the dev compact files)
def stage_compact(out):
    cd = out / "compact" / "w4r1"; cd.mkdir(parents=True, exist_ok=True)
    mk, ma = [], []
    for f in sorted(glob.glob(str(out / "mert-v1" / "shard_*.npz"))):
        z = np.load(f); mk += list(z["md5"]); ma.append(z["feat"][:, :, 4:9].astype(np.float32).mean(2).astype(np.float16))   # build_compact.py: mean of layers 4-8 per window
    if mk:
        mk = np.array(mk); ma = np.concatenate(ma); N = len(mk); order = np.argsort(mk); mk, ma = mk[order], ma[order]
        np.savez(cd / "compact.npz", md5=mk, mert=ma, clap=np.zeros((N, 768), np.float16), ess_act=np.zeros((N, 605), np.float16), ess_emb=np.zeros((N, 1280), np.float16),
                 has_mert=np.ones(N, bool), has_clap=np.zeros(N, bool), has_ess=np.zeros(N, bool)); _log(f"compact w4r1: {N} rows")
    ess = sorted(glob.glob(str(out / "essentia" / "shard_*.npz")))
    if ess:
        md, am, ax, em, es, sg = [], [], [], [], [], []
        env = dict(os.environ, EVALKIT_ESSENTIA_DIR=str(out / "essentia"), EVALKIT_COMPACT_OUT=str(out / "compact" / "w4r1-what-in-the-music") + "/")
        subprocess.run([sys.executable, "-W", "ignore", str(ROOT / "predictors" / "w4r1-what-in-the-music" / "build_compact.py")], cwd=str(ROOT), env=env, check=True); _log("compact w4r1-what-in-the-music rebuilt")

def stage_essentia(out, threads):
    env = dict(os.environ); script = ROOT / "predictors" / "w4-shared-prep" / "build_essentia.py"
    r = subprocess.run([sys.executable, "-W", "ignore", str(script), "--prev", str(out / "previews"), "--out", str(out / "essentia"), "--workers", str(max(1, min(2, threads)))], cwd=str(ROOT), env=env)
    _log("essentia exit code", r.returncode)

# ------------------------------------------------------------------ Deezer context
def stage_deezer(W, out, limit):
    C = _catalogue(); p = out / "deezer" / "context.jsonl"; p.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["trackId"] for l in open(p)} if p.exists() else set(); todo = W[~W.trackId.isin(done)]; todo = todo.head(limit) if limit else todo
    _log(f"deezer: {len(todo)} tracks"); t0 = time.time(); nf = 0
    with open(p, "a") as fh:
        for i, r in enumerate(todo.itertuples()):
            x = deezer_match(C, r); rec = dict(trackId=int(r.trackId), key=r.key, found=bool(x))
            if x:
                t = C.dz_track(x["id"]) or {}; nf += 1
                rec.update(deezer_id=x["id"], rank=x.get("rank"), explicit=x.get("explicit_lyrics"), album_id=(x.get("album") or {}).get("id"), artist_id=(x.get("artist") or {}).get("id"),
                           isrc=t.get("isrc"), release_date=t.get("release_date"), bpm=t.get("bpm"), gain=t.get("gain"), n_contributors=len(t.get("contributors") or []))
            fh.write(json.dumps(rec) + "\n")
            if i % 200 == 199: fh.flush(); _log(f"deezer {i + 1}/{len(todo)} {int(time.time() - t0)} s")
    _log(f"deezer done in {time.time() - t0:.0f} s; found {nf} of {len(todo)}")

# ------------------------------------------------------------------ main
def main(argv):
    opt = lambda k, d: type(d)(argv[argv.index(k) + 1]) if k in argv else d
    cut = opt("--cutoffs", ""); cutoffs = [c for c in cut.split(",") if c] or list(data.SEALED_CUTOFFS); sealed = any(pd.Timestamp(c) >= data.DEV_END for c in cutoffs)
    if sealed and "--main-session" not in argv: sys.exit("evalkit.sealed_prep enumerates the SEALED folds: MAIN SESSION ONLY. Re-run with --main-session (the main session only), or use --cutoffs <dev cutoffs> for tests.")
    out = Path(opt("--out", "")) if "--out" in argv else features.sealed_root(); out.mkdir(parents=True, exist_ok=True)
    stages = opt("--stages", "fetch,mert,compact").split(","); stages += (["essentia"] if "--essentia" in argv else []) + (["deezer"] if "--deezer" in argv else [])
    threads = opt("--threads", 3); limit = opt("--limit", 0); spc = opt("--sec-per-clip", SEC_PER_CLIP); t0 = time.time()
    _log(f"sealed_prep (evalkit v5.3, feature cache {features.SEALED_VERSION}) cutoffs={','.join(cutoffs)} out={out}")
    mem, U = enumerate_tracks(cutoffs); W = work_list(mem, U)
    if "--keys-file" in argv: ks = set(Path(opt("--keys-file", "")).read_text().split()); W = W[W.key.isin(ks)].reset_index(drop=True)
    if "--count" in argv: count_report(mem, U, W, out, spc); return
    if "--report" in argv: print(coverage_table(mem, U, out).to_string(index=False)); return
    times = {}
    if "fetch" in stages: t = time.time(); stage_fetch(W, out, threads, limit, "--retry" in argv, "--no-reuse-dev-audio" not in argv); times["fetch_s"] = round(time.time() - t, 1)
    if "mert" in stages: t = time.time(); times["mert_s_per_clip"] = round(stage_mert(W, out, limit), 3); times["mert_s"] = round(time.time() - t, 1)
    if "essentia" in stages: t = time.time(); stage_essentia(out, threads); times["essentia_s"] = round(time.time() - t, 1)
    if "compact" in stages: t = time.time(); stage_compact(out); times["compact_s"] = round(time.time() - t, 1)
    if "deezer" in stages: t = time.time(); stage_deezer(W, out, limit); times["deezer_s"] = round(time.time() - t, 1)
    times["total_s"] = round(time.time() - t0, 1); features.reset()
    with open(out / "prep_log.jsonl", "a") as fh: fh.write(json.dumps(dict(utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), cutoffs=cutoffs, stages=stages, **times)) + "\n")
    _log("runtimes:", json.dumps(times)); print("per-fold coverage (share of tracks with a clip key / with a MERT row):"); print(coverage_table(mem, U, out).to_string(index=False), flush=True)

if __name__ == "__main__": main(sys.argv[1:])
