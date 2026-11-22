"""Groundwork export for the reachability map: a harness-called pseudo-predictor that WRITES (side effect) per fold: the pre-cutoff taste seeds (Deezer artist ids with decayed play weight, half-life 180 d, streams < cutoff)
and the candidate-artist -> Deezer artist id map.  No labels are read; returns a constant score.  Output dir: env W6_RECALL_OUT.
Run:  W6_RECALL_OUT=DIR python3 -W ignore -m evalkit.run --fast --dump-scores DIR/dump.pkl predictors/w6r1-catalogue-context/recall_export.py"""
import os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model/predictors/w6r1-catalogue-context")
import predict as P
def export(train, cands, meta, cutoff):
    out = os.environ["W6_RECALL_OUT"]; R = P._records(); taste = P._Taste(train, R)
    s, fwd, tot = taste.at(pd.Timestamp(cutoff))     # snapshot at the month start of the cutoff (= cutoff for quarterly folds)
    # seeds: all artists with weight (harness artist ids), top-60 by weight; dz id None if unmapped
    top = s.sort_values(ascending=False).head(60)
    seeds = [{"artist": int(a), "w": float(w), "dz": taste.a2d.get(a)} for a, w in top.items()]
    cm = {}
    tids = cands.trackId.values.astype(np.int64)
    for a, t in zip(cands.artist.values, tids):
        if t in R.index: cm[int(a)] = int(R.at[t, "dz_artist_id"])
    json.dump({"cutoff": str(pd.Timestamp(cutoff).date()), "seeds": seeds, "cand_artist_dz": cm, "cand_artists": sorted(set(int(a) for a in cands.artist.values))},
              open(f"{out}/fold_{pd.Timestamp(cutoff).date()}.json", "w"))
    return np.zeros(len(cands)) + 1e-9 * np.arange(len(cands))
PREDICTORS = {"recall_export": export}
