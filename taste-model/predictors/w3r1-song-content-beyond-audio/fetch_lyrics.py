"""Resumable lrclib.net lyrics fetch (public, no key). Query = title + artist name + duration (artist name is used only as a search key, never as a feature).
Static per song; no information about the user is sent (generic client name). Output: CACHE/lyrics.jsonl, one line per trackId (opaque)."""
import json, time, sys, threading, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from common import *
OUT = CACHE / "lyrics.jsonl"
UA = "research-client/1.0"

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
    q = urllib.parse.urlencode({"track_name": name, "artist_name": artist})
    res = get("https://lrclib.net/api/search?" + q)
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
    n = int(sys.argv[1]) if len(sys.argv) > 1 else None
    U = universe()
    done = set()
    if OUT.exists():
        for l in open(OUT): done.add(json.loads(l)["id"])
    todo = [kv for kv in U.items() if kv[0] not in done][:n]
    print(len(U), "universe;", len(todo), "todo", flush=True)
    lock = threading.Lock(); c = 0
    with ThreadPoolExecutor(3) as ex, open(OUT, "a") as fo:
        for r in ex.map(lookup, todo):
            if r is None: continue
            with lock:
                fo.write(json.dumps(r) + "\n"); c += 1
                if c % 500 == 0: fo.flush(); print(c, flush=True)
