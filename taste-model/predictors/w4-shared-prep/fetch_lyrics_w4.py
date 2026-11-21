"""W4 shared prep P3: copy all existing W3 lyric records into .cache/shared/w4-lyrics/lyrics.jsonl, then look up (same lrclib query + acceptance rules as predictors/w3r1-song-content-beyond-audio/fetch_lyrics.py)
every dev-fold track (train, tried, decoy; main + holdout parts) with no record. Resumable. Usage: python3 fetch_lyrics_w4.py [time_box_minutes]"""
import sys, json, time, shutil, threading, urllib.parse, urllib.request, re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(Path(__file__).parent)); from universe import universe
ROOT = Path("/home/user/Listener/taste-model"); OLD = ROOT/".cache/shared/w3r1-song-content-beyond-audio-lyrics/lyrics.jsonl"
OUTD = ROOT/".cache/shared/w4-lyrics"; OUTD.mkdir(parents=True, exist_ok=True); OUT = OUTD/"lyrics.jsonl"
UA = "research-client/1.0"
def norm(s):
    s = re.sub(r"\s*[\(\[][^)\]]*[\)\]]", "", str(s).lower()); s = re.sub(r"\s+-\s+.*$", "", s)
    return re.sub(r"\W+", " ", s).strip()
def get(url):
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=25) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404: return []
            time.sleep(2 * (k + 1))
        except Exception: time.sleep(2 * (k + 1))
    return None
def lookup(item):
    tid, (name, artist, dur) = item
    time.sleep(0.3)
    res = get("https://lrclib.net/api/search?" + urllib.parse.urlencode({"track_name": name, "artist_name": artist}))
    if res is None: return None
    best, bd = None, 1e9
    for r in res:
        if norm(r.get("trackName", "")) != norm(name): continue
        if norm(r.get("artistName", "")) != norm(artist): continue
        d = abs((r.get("duration") or 0) - (dur or 0) / 1000)
        has = bool(r.get("plainLyrics")) or r.get("instrumental")
        sc = d - (0 if has else 100)
        if sc < bd: best, bd = r, sc
    if best is None or bd > 8: return dict(id=tid, found=False)
    return dict(id=tid, found=True, instrumental=bool(best.get("instrumental")), dur=best.get("duration"), plain=best.get("plainLyrics"), synced=best.get("syncedLyrics"), ddiff=bd)
if __name__ == "__main__":
    box = float(sys.argv[1]) * 60 if len(sys.argv) > 1 else 75 * 60; t0 = time.time()
    if not OUT.exists(): shutil.copyfile(OLD, OUT)
    done = {json.loads(l)["id"] for l in open(OUT)}
    U = universe(); todo = [kv for kv in U.items() if kv[0] not in done]
    print(len(U), "universe;", len(done), "records;", len(todo), "todo", flush=True)
    c = 0
    with ThreadPoolExecutor(3) as ex, open(OUT, "a") as fo:
        futs = []
        for it in todo:
            futs.append(ex.submit(lambda it=it: None if time.time() - t0 > box else lookup(it)))
        for f in futs:
            r = f.result()
            if r is None: continue
            fo.write(json.dumps(r) + "\n"); c += 1
            if c % 200 == 0: fo.flush(); print(c, round(time.time() - t0), flush=True)
    print("finished", c, "new records in", round(time.time() - t0), "s", flush=True)
