"""Build the iTunes preview fallback cache (git-ignored): .cache/itunes_fallback.csv.   python3 -m evalkit.fetch_itunes [--max N] [--user-only] [--sealed]
For every user track and every pool decoy WITHOUT a previewUrl, query the iTunes Search API (entity=song) by 'primary artist + title'; accept a result only if the
normalised title (data.song_key + accent/punctuation stripping) and the primary artist (whole iTunes artist name or one of its '&', ',', 'feat', 'x' parts) match and
|duration difference| <= 5 s. data.load_meta_all fills meta.previewUrl from the accepted matches, for tried songs and decoys alike.
Resumable (rows already in the csv are skipped; HTTP errors are retried later); rate limit: the API answers 403 after ~20 requests/minute, so the loop
adapts its delay. Decoys: only a seeded sample (N_DECOY_LOOKUPS) of preview-less decoys is looked up; preview-less decoys that were not looked up are not eligible for pools.
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

N_DECOY_LOOKUPS = 250   # rate limit (~15 requests/min) => only a seeded sample of preview-less decoys is looked up; the others are not eligible (data._open_parts)

def targets(user_only=False, sealed=False):
    """1) preview-less user tracks that are tried songs of a dev (or, with --sealed, sealed) fold (other preview-less train-only tracks are NOT looked up: rate limit), 2) a seeded sample of preview-less decoys."""
    import numpy as np
    d = data._load_all(); cuts = data.DEV_CUTOFFS + (data.SEALED_CUTOFFS if sealed else [])
    tried = set(pd.concat([f.trackId for c, f in data.make_folds(cuts, d)]))
    m = data.load_meta(); t = m[m.previewUrl.isna()]
    row = lambda tid, r: (tid, r.artistNames[0] if r.artistNames else "", r["name"], r.durationMs)
    out = [row(i, r) for i, r in t.iterrows() if i in tried]
    if not user_only:
        u = data._decoys().drop_duplicates("trackId"); u = u[u.previewUrl.isna() & ~u.trackId.isin(set(m.index))].sort_values("trackId")
        for _, r in u.iloc[np.random.default_rng(0).permutation(len(u))[:N_DECOY_LOOKUPS]].iterrows(): out.append((r.trackId, r.artistNames[0], r.trackName, r.durationMs))
    return out

def main(argv):
    mx = int(argv[argv.index("--max") + 1]) if "--max" in argv else 10 ** 9
    tg = targets("--user-only" in argv, "--sealed" in argv)
    done = set(pd.read_csv(data.FALLBACK).trackId) if data.FALLBACK.exists() else set()
    todo = [x for x in tg if x[0] not in done][:mx]
    print(len(tg), "targets,", len(done), "done,", len(todo), "to do", flush=True)
    delay, buf, n_ok, n403, t0 = 3.0, [], 0, 0, time.time()
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
                if "403" in str(e) or "429" in str(e): n403 += 1; delay = min(delay + 0.5, 12.0); time.sleep(20)
                else: time.sleep(5)
        if res is None: continue   # retried on the next run
        a = accept(res, artist, title, dur)
        buf.append(dict(trackId=tid, artist=artist, title=title, durationMs=dur, status="match" if a else "nomatch", previewUrl=a["previewUrl"] if a else None,
                        itunes_trackId=a["trackId"] if a else None, itunes_artist=a["artistName"] if a else None, itunes_title=a["trackName"] if a else None,
                        itunes_durationMs=a["trackTimeMillis"] if a else None))
        n_ok += 1
        if len(buf) >= 5: flush()
        if i % 10 == 0: print(i, len(todo), "delay", round(delay, 1), "n403", n403, "elapsed", int(time.time() - t0), flush=True)
        time.sleep(delay); delay = max(2.2, delay - 0.02)
    flush(); print("done")

if __name__ == "__main__": main(sys.argv[1:])
