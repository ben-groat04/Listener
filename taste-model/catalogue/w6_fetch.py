"""W6 reusable Deezer fetch (P1 records + P3 reusable script). Public catalogue info only; Deezer throttled to ~4 req/s (catalogue.MIN_GAP 0.25 s, shared by all threads).
Input: any DataFrame/CSV with columns trackId, title, artist (primary artist), durationMs (milliseconds), spotifyId (optional, carried through).
    python3 -W ignore -m catalogue.w6_fetch records IN.csv OUTDIR [--threads 3]      -> OUTDIR/{dz_tracks,dz_albums,dz_artists}.jsonl (resumable raw-field caches) + OUTDIR/records.csv
    python3 -W ignore -m catalogue.w6_fetch previews OUTDIR [--ids trackId,...]     -> OUTDIR/previews_deezer/<md5>.mp3 + OUTDIR/previews_manifest.csv  (re-queries a fresh signed URL right before each download)
Match rule: normalised title equal AND normalised primary artist equal to the Deezer result artist AND |duration diff| <= 5 s; best = smallest duration diff.  status: match | no_match | no_candidates.
records.csv columns: trackId, status, dz_id, isrc, dz_release_date, dz_rank, dz_bpm, dz_gain, dz_explicit, dz_has_preview, album_id, album_release_date, album_genre_ids, album_genre_names,
album_label, album_record_type, dz_artist_id, dz_artist_name, artist_nb_fan, artist_nb_album, artist_related_ids (up to 50, in order, '|'-joined), dur_diff_s."""
import sys, os, json, re, time, hashlib, subprocess, unicodedata, threading, urllib.request
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from catalogue import catalogue as C
_lk = threading.Lock()
def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\s*[\(\[][^)\]]*[\)\]]", "", s); s = re.sub(r"\s+-\s+.*$", "", s)
    s = re.sub(r"\W+", " ", s).strip(); return re.sub(r"^the ", "", s)
class Cache:
    def __init__(self, path):
        self.p = path; self.d = {}
        if os.path.exists(path):
            for l in open(path):
                try: r = json.loads(l); self.d[r["k"]] = r["v"]
                except Exception: pass
    def get(self, k): return self.d.get(str(k), "__miss__")
    def put(self, k, v):
        with _lk:
            self.d[str(k)] = v
            with open(self.p, "a") as f: f.write(json.dumps({"k": str(k), "v": v}) + "\n")
def search_match(title, artist, dur_ms):
    best = None; tn, an = norm(title), norm(artist); seen = False
    qs = [f'artist:"{artist}" track:"{title}"', f"{artist} {title}"]
    for qq in qs:
        r = C.http("https://api.deezer.com/search?" + C.q(q=qq, limit=10)); res = (r or {}).get("data", [])
        if res: seen = True
        for x in res:
            dd = abs((x.get("duration") or 0) - (dur_ms or 0) / 1000)
            if norm(x["title"]) == tn and norm(x["artist"]["name"]) == an and dd <= 5 and (best is None or dd < best[1]): best = (x, dd)
        if best: break
    return ("match", best[0], best[1]) if best else ("no_match" if seen else "no_candidates", None, None)
def track_record(row, T):
    k = row["trackId"]; v = T.get(k)
    if v != "__miss__": return v
    st, x, dd = search_match(row["title"], row["artist"], row["durationMs"]); v = dict(status=st)
    if x:
        t = C.http(f"https://api.deezer.com/track/{x['id']}") or {}
        v.update(dz_id=x["id"], isrc=t.get("isrc"), dz_release_date=t.get("release_date"), dz_rank=t.get("rank", x.get("rank")), dz_bpm=t.get("bpm"), dz_gain=t.get("gain"),
                 dz_explicit=t.get("explicit_lyrics", x.get("explicit_lyrics")), dz_has_preview=bool(t.get("preview") or x.get("preview")), album_id=(t.get("album") or x["album"]).get("id"),
                 dz_artist_id=(t.get("artist") or x["artist"]).get("id"), dz_artist_name=x["artist"]["name"], dur_diff_s=dd)
    T.put(k, v); return v
def album_record(aid, A):
    v = A.get(aid)
    if v != "__miss__": return v
    a = C.dz_album(aid) or {}
    v = dict(album_release_date=a.get("release_date"), album_genre_ids="|".join(str(g["id"]) for g in (a.get("genres") or {}).get("data", [])),
             album_genre_names="|".join(g["name"] for g in (a.get("genres") or {}).get("data", [])), album_label=a.get("label"), album_record_type=a.get("record_type"), ok=bool(a))
    A.put(aid, v); return v
def artist_record(aid, R):
    v = R.get(aid)
    if v != "__miss__": return v
    a = C.http(f"https://api.deezer.com/artist/{aid}") or {}; rel = C.dz_artist_related(aid)
    v = dict(artist_nb_fan=a.get("nb_fan"), artist_nb_album=a.get("nb_album"), artist_related_ids="|".join(str(x["id"]) for x in rel[:50]), ok=bool(a)); R.put(aid, v); return v
def run_records(inp, outdir, threads=3, stage_order=None, tracks_only=False):
    os.makedirs(outdir, exist_ok=True); T, A, R = (Cache(f"{outdir}/dz_{n}.jsonl") for n in ("tracks", "albums", "artists"))
    df = pd.read_csv(inp) if isinstance(inp, str) else inp; rows = df.to_dict("records"); t0 = time.time()
    with ThreadPoolExecutor(threads) as ex:
        for i, _ in enumerate(ex.map(lambda r: track_record(r, T), rows)):
            if i % 200 == 199: print("tracks", i + 1, len(rows), int(time.time() - t0), "s", flush=True)
        if not tracks_only:
            albs = sorted({v["album_id"] for v in T.d.values() if v.get("album_id")}); arts = sorted({v["dz_artist_id"] for v in T.d.values() if v.get("dz_artist_id")})
            print("albums", len(albs), "artists", len(arts), flush=True)
            list(ex.map(lambda a: album_record(a, A), albs)); print("albums done", int(time.time() - t0), flush=True)
            list(ex.map(lambda a: artist_record(a, R), arts)); print("artists done", int(time.time() - t0), flush=True)
    return assemble(df, outdir)
def assemble(df, outdir):
    T, A, R = (Cache(f"{outdir}/dz_{n}.jsonl") for n in ("tracks", "albums", "artists")); out = []
    for r in df.to_dict("records"):
        v = T.d.get(str(r["trackId"]))
        if v is None: continue
        o = dict(trackId=r["trackId"], **v)
        if v.get("album_id") is not None and str(v["album_id"]) in A.d: o.update({k: x for k, x in A.d[str(v["album_id"])].items() if k != "ok"})
        if v.get("dz_artist_id") is not None and str(v["dz_artist_id"]) in R.d: o.update({k: x for k, x in R.d[str(v["dz_artist_id"])].items() if k != "ok"})
        out.append(o)
    o = pd.DataFrame(out); o.to_csv(f"{outdir}/records.csv", index=False); return o
def fresh_preview(dz_id):
    t = C.http(f"https://api.deezer.com/track/{dz_id}") or {}; return t.get("preview")
def run_previews(outdir, pairs, threads=2):
    """pairs: list of (trackId, dz_id). Appends rows to previews_manifest.csv: md5, deezer_id, trackId, bytes, duration_s, ok, error."""
    pd_ = f"{outdir}/previews_deezer"; os.makedirs(pd_, exist_ok=True); mp = f"{outdir}/previews_manifest.csv"
    have = set(pd.read_csv(mp).trackId.astype(str)) if os.path.exists(mp) else set(); todo = [p for p in pairs if str(p[0]) not in have]
    def one(p):
        tid, did = p; err = ""
        for k in range(3):
            try:
                u = fresh_preview(did)
                if not u: err = "no preview url"; break
                b = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": C.UA}), timeout=40).read()
                if len(b) < 1000: err = "too small"; continue
                m = hashlib.md5(b).hexdigest(); path = f"{pd_}/{m}.mp3"; open(path, "wb").write(b)
                d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip() or "nan")
                return dict(md5=m, deezer_id=did, trackId=tid, bytes=len(b), duration_s=d, ok=bool(d > 1), error="")
            except Exception as e: err = str(e)[:100]; time.sleep(2 * (k + 1))
        return dict(md5="", deezer_id=did, trackId=tid, bytes=0, duration_s=float("nan"), ok=False, error=err)
    with ThreadPoolExecutor(threads) as ex:
        for i, r in enumerate(ex.map(one, todo)):
            with _lk: pd.DataFrame([r]).to_csv(mp, mode="a", header=not os.path.exists(mp), index=False)
            if i % 100 == 99: print("previews", i + 1, len(todo), flush=True)
if __name__ == "__main__":
    a = sys.argv[1:]; th = int(a[a.index("--threads") + 1]) if "--threads" in a else 3
    if a[0] == "records": run_records(a[1], a[2], th)
    elif a[0] == "previews":
        r = pd.read_csv(f"{a[1]}/records.csv"); r = r[(r.status == "match") & r.dz_has_preview.astype(bool)]
        if "--ids" in a: r = r[r.trackId.astype(str).isin(a[a.index("--ids") + 1].split(","))]
        run_previews(a[1], list(zip(r.trackId, r.dz_id.astype(int))), th)
