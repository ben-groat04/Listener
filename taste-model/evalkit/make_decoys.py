"""Build the open-universe decoy universe (real songs the user never played) from the public stats.fm API.
    python -m evalkit.make_decoys            # fetch (cached in .cache/decoy_raw) and write evalkit/decoy_universe.csv.gz
Build-time only: this reads the full listening history to choose seed artists and to exclude anything the user ever
played, so builders must not call it with their own seeds. Decoys: tracks of (a) the user's 300 most-played artists
(unplayed tracks by artists they love) and (b) up to 6 'related' artists for each of the top 150 (mostly new artists).
Each decoy carries its release date (earliest album) so a fold only uses songs that existed by the end of its window.
Limitation: /artists/<id>/tracks returns at most 200 tracks per artist."""
import json, time, urllib.request, sys
from pathlib import Path
import pandas as pd
from . import data

API = "https://api.stats.fm/api/v1"; RAW = data.ROOT / ".cache" / "decoy_raw"; OUT = data.ROOT / "evalkit" / "decoy_universe.csv.gz"
N_SEED, N_REL_SEEDS, N_REL = 300, 150, 6

def get(path, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(API + path, headers={"User-Agent": "taste-eval-research/0.1"})
            return json.load(urllib.request.urlopen(req, timeout=40))
        except Exception as e:
            time.sleep(1.5 * (i + 1)); err = e
    return {"error": str(err), "items": []}

def fetch_artist(aid):
    f = RAW / f"{aid}.json"
    if f.exists(): return json.loads(f.read_text())
    out = dict(tracks=get(f"/artists/{aid}/tracks?limit=200")["items"], albums=get(f"/artists/{aid}/albums?limit=200")["items"])
    time.sleep(0.15); f.write_text(json.dumps(out)); return out

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    d = data._load_all(); cnt = d.artistIds.explode().value_counts()
    seeds = [int(a) for a in cnt.index[:N_SEED]]
    rel = {}
    for a in seeds[:N_REL_SEEDS]:
        f = RAW / f"rel_{a}.json"
        if f.exists(): items = json.loads(f.read_text())
        else: items = get(f"/artists/{a}/related")["items"]; f.write_text(json.dumps(items)); time.sleep(0.15)
        for it in items[:N_REL]: rel[int(it["id"])] = it["name"]
    arts = list(dict.fromkeys(seeds + list(rel)))
    print(len(seeds), "seed artists;", len(rel), "related;", len(arts), "total", flush=True)
    rows = []
    for i, a in enumerate(arts):
        r = fetch_artist(a)
        rd = {al["id"]: al.get("releaseDate") for al in r["albums"]}
        for t in r["tracks"]:
            dates = [rd.get(al["id"]) for al in t.get("albums", []) if rd.get(al["id"])]
            if not dates or not t.get("artists"): continue
            rows.append(dict(trackId=t["id"], trackName=t["name"], albumId=t["albums"][0]["id"], albumName=t["albums"][0]["name"],
                             artistIds=[x["id"] for x in t["artists"]], artistNames=[x["name"] for x in t["artists"]],
                             durationMs=t.get("durationMs"), explicit=t.get("explicit"), popularity=t.get("spotifyPopularity"),
                             spotifyId=(t.get("externalIds", {}).get("spotify") or [None])[0],
                             previewUrl=t.get("spotifyPreview") or t.get("appleMusicPreview"),
                             release=pd.to_datetime(min(dates), unit="ms").strftime("%Y-%m-%d"), source_artist=a,
                             source="seed" if a in seeds else "related"))
        if i % 100 == 0: print(i, len(rows), flush=True)
    df = pd.DataFrame(rows).drop_duplicates("trackId")
    df["artistIds"] = df.artistIds.map(lambda x: ";".join(map(str, x))); df["artistNames"] = df.artistNames.map(";".join)
    df.to_csv(OUT, index=False); print("wrote", OUT, len(df))

if __name__ == "__main__": main()
