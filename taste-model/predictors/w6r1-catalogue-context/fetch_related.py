"""Reusable: related-artist lists (Deezer /artist/<id>/related, <= 20 ids) for the given Deezer artist ids -> .cache/w6r1-catalogue-context/artist_related.jsonl (resumable). 1 call per artist.
Usage: python3 -W ignore predictors/w6r1-catalogue-context/fetch_related.py ids.txt"""
import sys, os, json
sys.path.insert(0, "/home/user/Listener/taste-model")
from catalogue import catalogue as C
OUT = "/home/user/Listener/taste-model/.cache/w6r1-catalogue-context/artist_related.jsonl"
done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        try: done.add(json.loads(l)["artist_id"])
        except Exception: pass
for i, a in enumerate(int(x) for x in open(sys.argv[1]).read().split()):
    if a in done: continue
    rel = C.dz_artist_related(a)
    with open(OUT, "a") as f: f.write(json.dumps({"artist_id": a, "related": [x["id"] for x in rel]}) + "\n")
    if i % 100 == 99: print(i + 1, flush=True)
