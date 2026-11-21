"""Build the open-universe decoy universe (real songs the user never played) from the public stats.fm API.
    python -m evalkit.make_decoys [--sealed]   # fetch (cached in .cache/decoy_raw) and write .cache/decoy_universe.csv.gz
Build-time only (reads the history to choose seed artists): builders must not run it or read its output.
v3: seeds are chosen PER FOLD from pre-cutoff streams only (data.fold_seed_artists: top-300 artists by plays before the cutoff + up to 6 stats.fm
related artists of each of the top 150). This script fetches every artist needed by any dev fold (and the sealed folds with --sealed) and writes ONE
universe file (a track carries the set of artists whose track list contained it, `source_artists`); data.make_open_folds then selects, per fold, the
tracks whose source artists intersect that fold's seed set and that were released by the end of the fold window.
Each decoy carries its release date (earliest album) so a fold only uses songs that existed by the end of its window.
Limitation: /artists/<id>/tracks returns at most 200 tracks per artist. Exclusion of anything the user ever played happens in data.make_open_folds."""
import json, time, urllib.request, sys
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from . import data

API, RAW, OUT = data.API, data.RAW, data.DECOYS

def get(path, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(API + path, headers={"User-Agent": "taste-eval-research/0.1"})
            return json.load(urllib.request.urlopen(req, timeout=40))
        except Exception as e:
            time.sleep(1.5 * (i + 1)); err = e
    return {"error": str(err), "items": []}

def fetch_related(a):
    f = RAW / f"rel_{a}.json"
    if not f.exists():
        r = get(f"/artists/{a}/related")
        if "error" in r: return
        f.write_text(json.dumps(r["items"])); time.sleep(0.1)

def fetch_artist(aid):
    f = RAW / f"{aid}.json"
    if f.exists(): return json.loads(f.read_text())
    t, al = get(f"/artists/{aid}/tracks?limit=200"), get(f"/artists/{aid}/albums?limit=200")
    if "error" in t or "error" in al: return None   # not cached: retried by the next run
    out = dict(tracks=t["items"], albums=al["items"]); f.write_text(json.dumps(out)); time.sleep(0.1); return out

def main(sealed=False):
    RAW.mkdir(parents=True, exist_ok=True)
    d = data._load_all(); cuts = data.DEV_CUTOFFS + (data.SEALED_CUTOFFS if sealed else [])
    seeds_by = {}
    for c in cuts:
        cnt = d.loc[d.t < pd.Timestamp(c), "artistIds"].explode().dropna().value_counts()
        seeds_by[c] = [int(a) for a in cnt.index[:data.N_SEED]]
    top = sorted({a for s in seeds_by.values() for a in s[:data.N_REL_SEEDS]})
    with ThreadPoolExecutor(4) as ex: list(ex.map(fetch_related, top))
    arts = set()
    for c in cuts: sd, rl = data.fold_seed_artists(d, pd.Timestamp(c)); arts |= set(sd) | set(rl)
    arts = sorted(arts); print(len(arts), "artists over", len(cuts), "folds", flush=True)
    with ThreadPoolExecutor(4) as ex: res = list(ex.map(fetch_artist, arts))
    miss = [a for a, r in zip(arts, res) if r is None]
    if miss: print("WARNING: could not fetch", len(miss), "artists (rerun to retry):", miss[:10])
    rows = {}
    for a, r in zip(arts, res):
        if r is None: continue
        rd = {al["id"]: al.get("releaseDate") for al in r["albums"]}
        for t in r["tracks"]:
            dates = [rd.get(al["id"]) for al in t.get("albums", []) if data._valid_ms(rd.get(al["id"]))]
            if not dates or not t.get("artists"): continue
            if t["id"] in rows: rows[t["id"]]["src"].add(a); continue
            rows[t["id"]] = dict(trackId=t["id"], trackName=t["name"], albumId=t["albums"][0]["id"], albumName=t["albums"][0]["name"],
                                 artistIds=[x["id"] for x in t["artists"]], artistNames=[x["name"] for x in t["artists"]],
                                 durationMs=t.get("durationMs"), explicit=t.get("explicit"), popularity=t.get("spotifyPopularity"),
                                 spotifyId=(t.get("externalIds", {}).get("spotify") or [None])[0],
                                 previewUrl=t.get("spotifyPreview") or t.get("appleMusicPreview"),
                                 release=pd.to_datetime(min(dates), unit="ms").strftime("%Y-%m-%d"), src={a})
    df = pd.DataFrame(sorted(rows.values(), key=lambda r: r["trackId"]))
    df["source_artists"] = df.pop("src").map(lambda s: ";".join(map(str, sorted(s))))
    df["artistIds"] = df.artistIds.map(lambda x: ";".join(map(str, x))); df["artistNames"] = df.artistNames.map(";".join)
    df.to_csv(OUT, index=False); print("wrote", OUT, len(df))

if __name__ == "__main__": main("--sealed" in sys.argv)
