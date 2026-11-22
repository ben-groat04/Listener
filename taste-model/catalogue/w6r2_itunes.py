"""W6 round 2 / E2 step 1: iTunes second-source preview lookup + original m4a download for tried-pool tracks (TUNE first, then LATE with --late), non-HOLDOUT only
(harness 'main' pools contain no HOLDOUT-artist rows; asserted via data.is_holdout on public-meta artist). Acceptance rule = evalkit.fetch_itunes.accept (same query building as the fallback).
Resumable. Outputs in .cache/shared-w6r2/: itunes_lookup.csv, previews_itunes/<md5 of file>.m4a, previews_manifest.csv.
    python3 -W ignore -m catalogue.w6r2_itunes [--late] [--max N]"""
import sys, re, json, time, hashlib, subprocess, urllib.request, urllib.parse, os
import pandas as pd, numpy as np
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import data, fetch_itunes as FI
D1 = data.ROOT / ".cache" / "shared-w6r1"; D = data.ROOT / ".cache" / "shared-w6r2"
DELAY = 3.5
def scope(late):
    M = pd.read_csv(D1 / "universe_membership.csv"); U = pd.read_csv(D1 / "universe_tracks.csv").set_index("trackId")
    sl = ["TUNE"] + (["LATE"] if late else [])
    ids = list(dict.fromkeys(M[(M.group == "tried") & M.slice.isin(sl)].sort_values(["slice", "fold"], ascending=[False, True]).trackId))
    from evalkit import run   # public meta has no artist id: as in round 1, assert on the raw artist column of the harness 'main' pool rows (no labels read)
    for Fd in run.prepare_folds(data.DEV_CUTOFFS): assert not data.is_holdout(Fd["pool"].artist.values).any()
    return ids, U
def search(artist, title):
    q = re.sub(r"\s*[\(\[][^)\]]*[\)\]]", "", str(title)); q = re.sub(r"\s+-\s+.*$", "", q) or str(title)
    url = "https://itunes.apple.com/search?" + urllib.parse.urlencode(dict(term=f"{artist} {q}", entity="song", limit=10))
    for k in range(8):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "taste-eval-research/0.1"}), timeout=30))["results"]
        except Exception as e:
            time.sleep(20 if ("403" in str(e) or "429" in str(e)) else 5)
    return None
def download(url):
    for k in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "taste-eval-research/0.1"}), timeout=60).read()
        except Exception as e: err = str(e)[:80]; time.sleep(3)
    return err
def main():
    late = "--late" in sys.argv; mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 10 ** 9
    ids, U = scope(late); (D / "previews_itunes").mkdir(parents=True, exist_ok=True)
    lp, mp = D / "itunes_lookup.csv", D / "previews_manifest.csv"
    done = set(pd.read_csv(lp).trackId) if lp.exists() else set()
    todo = [t for t in ids if t not in done][:mx]; print(len(ids), "scope", len(done), "done", len(todo), "todo", flush=True)
    import threading; from concurrent.futures import ThreadPoolExecutor
    lk = threading.Lock(); pool = ThreadPoolExecutor(2)
    def fetch_clip(t, a):   # download + ffprobe in a worker thread (different host from the search API), then append the manifest and the lookup row
        row = dict(trackId=t, status="match", itunes_trackId=a["trackId"], previewUrl=a["previewUrl"], itunes_artist=a["artistName"], itunes_title=a["trackName"], itunes_durationMs=a["trackTimeMillis"], md5=None)
        b = download(a["previewUrl"]); m = dict(md5=None, trackId=t, itunes_track_id=a["trackId"], bytes=0, duration_s=np.nan, ok=False, error="", url_md5=hashlib.md5(a["previewUrl"].encode()).hexdigest())
        if isinstance(b, bytes) and len(b) > 1000:
            h = hashlib.md5(b).hexdigest(); p = D / "previews_itunes" / f"{h}.m4a"; p.write_bytes(b)
            try:
                du = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())
                m.update(md5=h, bytes=len(b), duration_s=du, ok=du > 5); row["md5"] = h
            except Exception as e: m.update(md5=h, bytes=len(b), error="ffprobe " + str(e)[:50])
        else: m["error"] = str(b)[:80]
        with lk:
            pd.DataFrame([m]).to_csv(mp, mode="a", header=not mp.exists(), index=False); pd.DataFrame([row]).to_csv(lp, mode="a", header=not lp.exists(), index=False)
    futs = []; tnext = time.time()
    for i, t in enumerate(todo):
        r = U.loc[t]
        if not (isinstance(r["name"], str) and r["artist"] == r["artist"] and r["artist"]):
            with lk: pd.DataFrame([dict(trackId=t, status="skipped_no_title")]).to_csv(lp, mode="a", header=not lp.exists(), index=False)
            continue
        time.sleep(max(0, tnext - time.time())); tnext = time.time() + DELAY      # one search per 3.5 s (the download runs concurrently on the CDN host)
        res = search(r["artist"], r["name"])
        if res is None: continue
        a = FI.accept(res, r["artist"], r["name"], r["durationMs"])
        if a: futs.append(pool.submit(fetch_clip, t, a))
        else:
            with lk: pd.DataFrame([dict(trackId=t, status="nomatch")]).to_csv(lp, mode="a", header=not lp.exists(), index=False)
        if i % 20 == 0: print(i, len(todo), int(time.time()), flush=True)
    for f in futs: f.result()
    (D / "lookup_finished.flag").write_text("done"); print("lookup done", flush=True)
if __name__ == "__main__": main()
