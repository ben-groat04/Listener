"""Reusable: for each Deezer artist id fetch the artist's top-100 track ids (ordered by Deezer rank) -> .cache/w6r1-catalogue-context/artist_top.jsonl (resumable).
Usage: python3 -W ignore predictors/w6r1-catalogue-context/fetch_artist_top.py [ids.txt]   (default: all matched artists in shared-w6r1/p1_records.csv)
Cost: 1 Deezer call per artist (~4 req/s). Public catalogue information only."""
import sys, os, json
sys.path.insert(0, "/home/user/Listener/taste-model")
import pandas as pd
from catalogue import catalogue as C
OUT = "/home/user/Listener/taste-model/.cache/w6r1-catalogue-context/artist_top.jsonl"
def main(ids):
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            try: done.add(json.loads(l)["artist_id"])
            except Exception: pass
    for i, a in enumerate(ids):
        if int(a) in done: continue
        top = C.dz_artist_top(int(a), limit=100)
        with open(OUT, "a") as f: f.write(json.dumps({"artist_id": int(a), "top": [[t["id"], t.get("rank")] for t in top]}) + "\n")
        if i % 100 == 99: print(i + 1, len(ids), flush=True)
if __name__ == "__main__":
    if len(sys.argv) > 1: ids = [int(x) for x in open(sys.argv[1]).read().split()]
    else:
        R = pd.read_csv("/home/user/Listener/taste-model/.cache/shared-w6r1/p1_records.csv"); ids = sorted(set(R[R.status == "match"].dz_artist_id.dropna().astype(int)))
    main(ids)
