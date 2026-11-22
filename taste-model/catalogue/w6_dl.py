"""Deezer preview downloader loop for P2 (separate process so MERT is not blocked): downloads every matched tried-track preview from p1_user/dz_tracks.jsonl until records.csv exists.
    python3 -W ignore -m catalogue.w6_dl"""
import sys, os, time
sys.path.insert(0, "/home/user/Listener/taste-model")
import pandas as pd
from catalogue import w6_fetch as F, w6_p2
D = w6_p2.D
if __name__ == "__main__":
    ids = w6_p2.scope()
    while True:
        fin = os.path.exists(D / "p1_user" / "records.csv"); T = F.Cache(str(D / "p1_user" / "dz_tracks.jsonl"))
        pairs = [(int(t), v["dz_id"]) for t, v in T.d.items() if int(t) in ids and v.get("status") == "match" and v.get("dz_has_preview")]
        F.run_previews(str(D), pairs, threads=1)
        if fin: break
        time.sleep(20)
    print("dl done", flush=True)
