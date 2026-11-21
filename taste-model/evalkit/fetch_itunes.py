"""Build the iTunes preview fallback cache (git-ignored): .cache/itunes_fallback.csv.   python3 -m evalkit.fetch_itunes [--max N] [--user-only] [--sealed]
For every user track and every pool decoy WITHOUT a previewUrl, query the iTunes Search API (entity=song) by 'primary artist + title'; accept a result only if the
normalised title (data.song_key + accent/punctuation stripping) and the primary artist (whole iTunes artist name or one of its '&', ',', 'feat', 'x' parts) match and
|duration difference| <= 5 s. data.load_meta_all fills meta.previewUrl from the accepted matches, for tried songs and decoys alike.
Resumable (rows already in the csv are skipped; HTTP errors are retried later); rate limit: the API answers 403 after ~20 requests/minute, so the loop
adapts its delay. Decoys looked up = the stage-1 decoy pre-sample of every DEV fold (data.decoy_presample), i.e. the only decoys that can enter a pool.
Run order: user tracks first, then decoys. --sealed (MAIN SESSION, after make_decoys --sealed) adds the sealed folds' decoy pre-samples."""
import sys, re, json, time, unicodedata, urllib.request, urllib.parse
import pandas as pd
from . import data

def norm(x):
    x = unicodedata.normalize("NFKD", str(x)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", x).strip()

def norm_title(x): return norm(data.song_key(str(x)))

def artist_parts(name):
    n = norm(name); parts = {n}
    for p in re.split(r"\s*(?:&|,|;| feat\.? | ft\.? | featuring | and | with | x )\s*", str(name).lower()): parts.add(norm(p))
    return parts

def accept(res, artist, title, dur):
    """Best acceptable iTunes result (with previewUrl) or None."""
    ok = []
    for r in res:
        if r.get("kind") != "song" or not r.get("previewUrl") or not r.get("trackTimeMillis") or dur is None or pd.isna(dur): continue
        if norm_title(r.get("trackName", "")) != norm_title(title): continue
        if norm(artist) not in artist_parts(r.get("artistName", "")): continue
        dd = abs(r["trackTimeMillis"] - dur)
        if dd <= 5000: ok.append((dd, r))
    return min(ok, key=lambda x: x[0])[1] if ok else None

def targets(user_only=False, sealed=False):
    m = data.load_meta(); t = m[m.previewUrl.isna()]
    seen = set(); out = []
    for tid, r in t.iterrows(): out.append((tid, r.artistNames[0] if r.artistNames else "", r["name"], r.durationMs)); seen.add(tid)
    if not user_only:
        mm = data.load_meta_all(fill=False)
        ids = []
        for c, l in data.decoy_presample(data.DEV_CUTOFFS + (data.SEALED_CUTOFFS if sealed else [])).items(): ids += l
        for tid in dict.fromkeys(ids):
            if tid in seen or tid not in mm.index or pd.notna(mm.previewUrl[tid]): continue
            r = mm.loc[tid]; out.append((tid, r.artistNames[0] if r.artistNames else "", r["name"], r.durationMs))
    return out

def main(argv):
    mx = int(argv[argv.index("--max") + 1]) if "--max" in argv else 10 ** 9
    tg = targets("--user-only" in argv, "--sealed" in argv)
    done = set(pd.read_csv(data.FALLBACK).trackId) if data.FALLBACK.exists() else set()
    todo = [x for x in tg if x[0] not in done][:mx]
    print(len(tg), "targets,", len(done), "done,", len(todo), "to do", flush=True)
    delay, buf, n_ok, t0 = 3.0, [], 0, time.time()
    def flush():
        if buf:
            pd.DataFrame(buf).to_csv(data.FALLBACK, mode="a", header=not data.FALLBACK.exists(), index=False); buf.clear()
    for i, (tid, artist, title, dur) in enumerate(todo):
        q = re.sub(r"\s*[\(\[][^)\]]*[\)\]]", "", str(title)); q = re.sub(r"\s+-\s+.*$", "", q) or str(title)
        url = "https://itunes.apple.com/search?" + urllib.parse.urlencode(dict(term=f"{artist} {q}", entity="song", limit=10))
        res = None
        for k in range(12):
            try:
                res = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "taste-eval-research/0.1"}), timeout=30))["results"]; break
            except Exception as e:
                if "403" in str(e) or "429" in str(e): delay = min(delay + 0.5, 12.0); time.sleep(20)
                else: time.sleep(5)
        if res is None: continue   # retried on the next run
        a = accept(res, artist, title, dur)
        buf.append(dict(trackId=tid, artist=artist, title=title, durationMs=dur, status="match" if a else "nomatch", previewUrl=a["previewUrl"] if a else None,
                        itunes_trackId=a["trackId"] if a else None, itunes_artist=a["artistName"] if a else None, itunes_title=a["trackName"] if a else None,
                        itunes_durationMs=a["trackTimeMillis"] if a else None))
        n_ok += 1
        if len(buf) >= 20: flush()
        if i % 50 == 0: print(i, len(todo), "delay", round(delay, 1), "elapsed", int(time.time() - t0), flush=True)
        time.sleep(delay); delay = max(2.2, delay - 0.02)
    flush(); print("done")

if __name__ == "__main__": main(sys.argv[1:])
