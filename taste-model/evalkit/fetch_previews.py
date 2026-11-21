"""Shared preview-audio cache (git-ignored): .cache/shared/previews/audio/<md5(previewUrl)>.<ext> (original downloaded bytes, never resampled/trimmed/converted)
and previews/manifest.csv (md5, previewUrl, ext, bytes, duration_s, source, ok, error).  source = spotify | itunes_meta | itunes_fallback.
Scope: every distinct previewUrl in the (public) meta of any DEV fold = train tracks + tried and decoy pool tracks of all 14 dev cutoffs (run.prepare_folds(DEV_CUTOFFS)),
iTunes fallbacks included. No sealed cutoffs.
    python3 -m evalkit.fetch_previews [--threads N<=6] [--report]      resumable: files already downloaded are kept, failed ones retried only with --retry
Network-bound: run it when no builder is using CPU.  --report prints per-fold coverage (share of tried songs / decoys with ok audio)."""
import sys, os, hashlib, subprocess, time, urllib.request, threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd
from . import data, run

DIR = data.ROOT / ".cache" / "shared" / "previews"; AUDIO = DIR / "audio"; MAN = DIR / "manifest.csv"
COLS = ["md5", "previewUrl", "ext", "bytes", "duration_s", "source", "ok", "error"]

def md5(u): return hashlib.md5(u.encode()).hexdigest()

def source_of(u, fb):
    if "scdn.co" in u: return "spotify"
    return "itunes_fallback" if u in fb else "itunes_meta"

def scope():
    urls = {}
    fb = set(data.fallback_table().query("status == 'match'").previewUrl.dropna())
    for F in run.prepare_folds(data.DEV_CUTOFFS):
        for u in F["meta"].previewUrl.dropna(): urls.setdefault(u, source_of(u, fb))
    return urls

def ext_of(u, ctype):
    p = u.split("?")[0].lower()
    for e in ("mp3", "m4a", "mp4", "aac", "ogg", "wav"):
        if p.endswith("." + e): return e
    return {"audio/mpeg": "mp3", "audio/mp4": "m4a", "audio/x-m4a": "m4a", "audio/aac": "aac"}.get((ctype or "").split(";")[0], "bin")

def duration(path):
    try: return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True, timeout=30).stdout.strip())
    except Exception: return np.nan

def fetch(u, src):
    m = md5(u); err = ""
    for k in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "taste-eval-research/0.1"}), timeout=40)
            b = r.read(); e = ext_of(u, r.headers.get("Content-Type"))
            if len(b) < 1000: err = f"too small ({len(b)} bytes)"; continue
            p = AUDIO / f"{m}.{e}"; tmp = p.with_suffix(f".tmp{threading.get_ident()}"); tmp.write_bytes(b); os.replace(tmp, p)
            d = duration(p); return dict(md5=m, previewUrl=u, ext=e, bytes=len(b), duration_s=d, source=src, ok=bool(np.isfinite(d) and d > 1), error="" if np.isfinite(d) and d > 1 else "ffprobe failed")
        except Exception as ex:
            err = str(ex)[:120]; time.sleep(1.5 * (k + 1))
    return dict(md5=m, previewUrl=u, ext="", bytes=0, duration_s=np.nan, source=src, ok=False, error=err)

def report(man, cutoffs=data.DEV_CUTOFFS):
    ok = set(man[man.ok.astype(bool)].previewUrl); rows = []
    for F in run.prepare_folds(cutoffs):
        pool, order = F["pool"], F["order"]; m = F["meta"]; cands = F["cands"]
        pu = m.previewUrl.reindex(cands.trackId).values; has = np.array([isinstance(u, str) and u in ok for u in pu]); dec = pool.is_decoy.values[order] == 1
        rows.append(dict(fold=str(F["c"].date()), tried=int((~dec).sum()), tried_ok=round(has[~dec].mean(), 3), decoys=int(dec.sum()), decoys_ok=round(has[dec].mean(), 3)))
    return pd.DataFrame(rows)

def main(argv):
    nt = min(6, int(argv[argv.index("--threads") + 1])) if "--threads" in argv else 6
    AUDIO.mkdir(parents=True, exist_ok=True)
    man = pd.read_csv(MAN) if MAN.exists() else pd.DataFrame(columns=COLS)
    if "--report" in argv: print(report(man).to_string(index=False)); return
    urls = scope(); done = set(man[man.ok.astype(bool) | ("--retry" not in argv)].previewUrl) if len(man) else set()
    todo = [(u, s) for u, s in urls.items() if u not in done]
    print(len(urls), "distinct previewUrls in scope;", len(done & set(urls)), "done;", len(todo), "to fetch", flush=True)
    rows = man[man.previewUrl.isin(urls) & man.previewUrl.isin(done)].to_dict("records"); t0 = time.time()
    def save(): pd.DataFrame(rows, columns=COLS).drop_duplicates("previewUrl", keep="last").to_csv(MAN, index=False)
    with ThreadPoolExecutor(nt) as ex:
        for i, r in enumerate(ex.map(lambda x: fetch(*x), todo)):
            rows.append(r)
            if i % 200 == 199: save(); print(i + 1, len(todo), int(time.time() - t0), "s", flush=True)
    save(); man = pd.read_csv(MAN); print("ok", int(man.ok.sum()), "of", len(man)); print(report(man).to_string(index=False))

if __name__ == "__main__": main(sys.argv[1:])
