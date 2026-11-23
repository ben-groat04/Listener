import sys, os, json, re, collections, unicodedata, time, hashlib, concurrent.futures as cf
sys.path.insert(0, "/home/user/Listener/taste-model")
import pandas as pd, numpy as np
from catalogue import catalogue as C
from evalkit import data
OUT = "/home/user/Listener/taste-model/.cache/suggest/"
def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\W+", " ", s).strip()
d = data.load_streams(until="2027-01-01", _sealed=True); m = data.load_meta()
d = d.assign(an=d.trackId.map(m.artistNames.map(lambda a: a[0] if a else None)), nm=d.trackId.map(m.name))
d["nm"] = d.nm.fillna(d.trackName)
played = set(zip(d.nm.map(lambda x: data.song_key(str(x))), d.an.map(norm)))
played |= set(zip(d.trackName.map(lambda x: data.song_key(str(x))), d.an.map(norm)))
known_art = set(norm(a) for l in m.artistNames for a in l)
r = d[d.t >= d.t.max() - pd.Timedelta(days=365)]
top = r.an.value_counts().head(50)
json.dump(dict(played=[list(x) for x in played], known_art=sorted(known_art), top=top.to_dict()), open(OUT + "history.json", "w"))
print("played keys", len(played), "known artists", len(known_art), flush=True)
def find_artist(name):
    res = (C.http("https://api.deezer.com/search/artist?" + C.q(q=name, limit=5)) or {}).get("data", [])
    for a in res:
        if norm(a["name"]) == norm(name): return a
    return None
seeds = {}
for n, c in top.items():
    a = find_artist(n)
    if a: seeds[a["id"]] = (a["name"], c)
print("seeds", len(seeds), flush=True)
score = collections.defaultdict(float); names = {}; hop1 = {}
tot = sum(c for _, c in seeds.values())
for i, (n, c) in seeds.items():
    for a in C.dz_artist_related(i):
        names[a["id"]] = a["name"]; w = c / tot; hop1[a["id"]] = hop1.get(a["id"], 0) + w; score[a["id"]] += w
print("hop1", len(hop1), flush=True)
t0 = time.time()
for k, (i, w) in enumerate(sorted(hop1.items(), key=lambda x: -x[1])[:700]):
    for a in C.dz_artist_related(i):
        names[a["id"]] = a["name"]; score[a["id"]] += 0.5 * w
    if k % 100 == 0: print("hop2", k, int(time.time() - t0), flush=True)
for i in seeds: score.pop(i, None)
walk = sorted(score.items(), key=lambda x: -x[1])
print("walk artists", len(walk), flush=True)
rows = []
def add(t, src, sc=0):
    if not t.get("preview"): return
    rows.append(dict(dz_id=t["id"], title=t["title"], artist=t["artist"]["name"], artist_id=t["artist"]["id"], link=t.get("link"), preview=t["preview"], rank=t.get("rank"), src=src, walkscore=sc))
for i, (n, c) in seeds.items():
    for t in C.dz_artist_top(i, 15): add(t, "seed-artist-top")
print("seed rows", len(rows), flush=True)
for k, (i, s) in enumerate(walk[:260]):
    for t in C.dz_artist_top(i, 8): add(t, "related-walk", s)
    if k % 50 == 0: print("walk top", k, len(rows), flush=True)
gs = {g["name"].lower(): g["id"] for g in C.dz_genres()}
for gname in ("rock", "alternative", "pop", "singer & songwriter"):
    if gname in gs:
        for t in C.dz_chart(gs[gname], "tracks", 100): add(t, "chart-" + gname)
df = pd.DataFrame(rows).drop_duplicates("dz_id")
df["tkey"] = df.title.map(lambda x: data.song_key(x)); df["akey"] = df.artist.map(norm)
df["played"] = [(a, b) in played for a, b in zip(df.tkey, df.akey)]
df["known_artist"] = df.akey.isin(known_art)
print("total", len(df), "played", df.played.sum(), "known artist", df.known_artist.sum(), flush=True)
df = df[~df.played].reset_index(drop=True)
df["key"] = df.preview.map(lambda u: hashlib.md5(u.encode()).hexdigest())
def dl(r):
    p = OUT + "audio/" + r.key + ".mp3"
    if os.path.exists(p): return True
    for k in range(3):
        try:
            import urllib.request
            b = urllib.request.urlopen(urllib.request.Request(r.preview, headers={"User-Agent": C.UA}), timeout=30).read()
            if len(b) > 5000: open(p, "wb").write(b); return True
        except Exception: time.sleep(1)
    return False
with cf.ThreadPoolExecutor(8) as ex: ok = list(ex.map(dl, [r for r in df.itertuples()]))
df["audio_ok"] = ok; df.to_csv(OUT + "candidates.csv", index=False)
print("DONE downloaded", sum(ok), "of", len(df), flush=True)
