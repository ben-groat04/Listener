"""Builds .cache/shared-w6r0/ sample (groundwork only; no scoring). python3 catalogue/make_sample.py   (cwd = taste-model). ~15 min.
 1. coverage_sample.csv: 60 seeded songs of evalkit.data.load_meta() looked up in Deezer / Spotify-embed / MusicBrainz / AcousticBrainz / LRCLIB / iTunes.
 2. catalogue_enum.json: what can be enumerated without a key (Deezer genres, charts per genre, artist top/related/albums, iTunes top songs).
 3. catalogue_tracks.csv: ~3.7k Deezer tracks (chart per genre + top tracks of related artists) with preview URLs, isrc, rank, duration, release_date.
 4. previews/: 6 downloaded sample previews (deezer mp3, spotify mp3, itunes m4a) + sample_audio.csv (ffprobe durations)."""
import sys, os, json, subprocess, random, csv
sys.path = [p for p in sys.path if p != os.path.dirname(os.path.abspath(__file__))]
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, pandas as pd
from catalogue import catalogue as C
from evalkit import data
OUT = "/home/user/Listener/taste-model/.cache/shared-w6r0"; os.makedirs(OUT + "/previews", exist_ok=True)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
m = data.load_meta(); ids = list(m.index); rng = np.random.default_rng(0)
samp = [ids[i] for i in rng.permutation(len(ids))[:N]]
rows = []
for tid in samp:
    r = m.loc[tid]; a = r.artistNames[0] if len(r.artistNames) else ""; t = r["name"]; dur = r.durationMs
    row = dict(trackId=tid, artist=a, title=t, durationMs=dur, has_spotify_preview_in_meta=bool(isinstance(r.previewUrl, str) and "scdn" in r.previewUrl))
    d = C.dz_search(a, t, 5)
    best = None
    for x in d:
        if C.norm(x["title"].split(" (")[0]) == C.norm(t.split(" (")[0]) and C.norm(a) in C.norm(x["artist"]["name"]) + " " and abs(x["duration"] * 1000 - dur) <= 5000: best = x; break
    if best is None:
        for x in d:
            if C.norm(x["title"]) == C.norm(t) and C.norm(x["artist"]["name"]) == C.norm(a): best = x; break
    row.update(dz_match=best is not None, dz_id=best and best["id"], dz_has_preview=bool(best and best.get("preview")), dz_isrc=None, dz_rank=best and best.get("rank"))
    if best:
        full = C.dz_track(best["id"]) or {}
        row.update(dz_isrc=full.get("isrc"), dz_release=full.get("release_date"), dz_bpm=full.get("bpm"), dz_gain=full.get("gain"))
    e = C.sp_embed(r.spotifyId) if isinstance(r.spotifyId, str) else None
    row.update(sp_embed_ok=e is not None, sp_embed_preview=bool(e and e.get("preview_url")))
    mb = None
    if row.get("dz_isrc"):
        rec = C.mb_isrc(row["dz_isrc"]); mb = rec[0]["id"] if rec else None
    if mb is None:
        rec = C.mb_recording_search(a, t, 1); mb = rec[0]["id"] if rec and rec[0].get("score", 0) >= 95 else None
    row["mbid"] = mb
    if mb:
        lo = C.ab_low(mb); row["ab_low"] = bool(lo); hi = C.ab_high(mb); row["ab_high"] = bool(hi)
    else: row["ab_low"] = row["ab_high"] = False
    l = C.lrc_get(a, t, dur=dur / 1000); row["lrclib"] = bool(l and (l.get("plainLyrics") or l.get("syncedLyrics")))
    it = C.it_search(f"{a} {t}", limit=5); ok = [x for x in it if x.get("previewUrl") and C.norm(x["trackName"].split(" (")[0]) == C.norm(t.split(" (")[0]) and abs(x["trackTimeMillis"] - dur) <= 5000]
    row["itunes_match_preview"] = bool(ok); row["_it_url"] = ok[0]["previewUrl"] if ok else None
    rows.append(row); print(len(rows), row["dz_match"], row["sp_embed_preview"], row["mbid"] is not None, row["ab_low"], row["lrclib"], row["itunes_match_preview"], flush=True)
df = pd.DataFrame(rows); assert len(df) == N and not df[["trackId", "artist", "title"]].isna().any().any()
df.drop(columns=["_it_url"]).to_csv(OUT + "/coverage_sample.csv", index=False)
print(df.drop(columns=["trackId", "artist", "title", "durationMs", "dz_id", "dz_isrc", "dz_rank", "dz_release", "dz_bpm", "dz_gain", "mbid", "_it_url"], errors="ignore").mean())
# enumeration
enum = {"deezer_genres": [(g["id"], g["name"]) for g in C.dz_genres()]}
tr = {}
for gid, _ in enum["deezer_genres"]:
    for x in C.dz_chart(gid, "tracks", 100): tr[x["id"]] = dict(id=x["id"], title=x["title"], artist=x["artist"]["name"], artist_id=x["artist"]["id"], album=x["album"]["title"], duration=x["duration"], rank=x["rank"], explicit=x["explicit_lyrics"], preview=x.get("preview"), src=f"chart{gid}")
    enum[f"chart_{gid}"] = sum(1 for v in tr.values() if v["src"] == f"chart{gid}")
a0 = list({v["artist_id"] for v in tr.values()})[:25]
for ai in a0:
    for x in C.dz_artist_related(ai)[:5]:
        for y in C.dz_artist_top(x["id"], 10): tr.setdefault(y["id"], dict(id=y["id"], title=y["title"], artist=y["artist"]["name"], artist_id=y["artist"]["id"], album=y["album"]["title"], duration=y["duration"], rank=y["rank"], explicit=y["explicit_lyrics"], preview=y.get("preview"), src="related_top"))
t = pd.DataFrame(tr.values()); assert t.id.is_unique and len(t) > 100
t.to_csv(OUT + "/catalogue_tracks.csv", index=False)
enum.update(n_tracks=len(t), n_with_preview=int(t.preview.notna().sum()), itunes_top100_us=len(C.it_topsongs(limit=100)), related_artists_per_artist=len(C.dz_artist_related(27)), artist_albums_27=len(C.dz_artist_albums(27)))
json.dump(enum, open(OUT + "/catalogue_enum.json", "w"), indent=1)
# audio samples
au = []
def grab(name, url):
    p = f"{OUT}/previews/{name}"; n = C.download(url, p)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip() if n else ""
    au.append(dict(file=name, bytes=n, duration_s=d, url_host=url.split("/")[2]))
for i, x in enumerate(t[t.preview.notna()].head(3).itertuples()): grab(f"deezer_{x.id}.mp3", x.preview)
for r in rows[:40]:
    if r.get("sp_embed_preview") and sum(a["url_host"] == "p.scdn.co" for a in au) < 2:
        e = C.sp_embed(m.loc[r["trackId"]].spotifyId); grab(f"spotify_{m.loc[r['trackId']].spotifyId}.mp3", e["preview_url"])
for r in rows:
    if r["_it_url"] and sum("itunes" in a["url_host"] or "apple" in a["url_host"] for a in au) < 2: grab(f"itunes_{abs(hash(r['_it_url'])) % 10**8}.m4a", r["_it_url"])
pd.DataFrame(au).to_csv(OUT + "/sample_audio.csv", index=False); print(pd.DataFrame(au))
