"""Analysis helpers run INSIDE the harness (fast, default folds) as models; they write side files to $W5R2_OUT and return the default recipe's score.
 'probe'     : per candidate availability / metadata (missing-audio analysis)
 'nullprobe' : random-label refits: for R permutation seeds, scores of all grid variants (permuted training target), saved for offline sauc."""
import os, sys, pickle, hashlib
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recipe, grid
OUT = os.environ.get("W5R2_OUT", "/tmp"); R = int(os.environ.get("W5R2_NULL_R", "8")); OFF = int(os.environ.get("W5R2_NULL_OFF", "0")); TAG = os.environ.get("W5R2_NULL_TAG", "")
def probe(train, cands, meta, cutoff):
    t = cands.trackId.values; u = meta.previewUrl.reindex(t).values; m = meta.reindex(t)
    df = pd.DataFrame(dict(song=cands.song.values, artist=cands.artist.values, cutoff=str(cutoff)[:10], ess=recipe._eidx(t, meta) >= 0, mert=recipe._midx(t, meta) >= 0,
        has_url=[isinstance(x, str) for x in u], dom=[x.split("/")[2] if isinstance(x, str) else "" for x in u], dur=m.durationMs.values, pop=m.popularity.values, expl=m.explicit.astype(float).values,
        n_train_songs=len(train)))
    df.to_pickle(f"{OUT}/probe_{str(cutoff)[:10]}.pkl"); return recipe.score(train, cands, meta, cutoff)
ALL = {"default": {}, **grid.OAT, **grid.JOINT}
def nullprobe(train, cands, meta, cutoff):
    out = {}
    for r in range(R):
        recipe.PERM = 1000 + OFF + r
        try:
            for n, P in ALL.items(): out[(OFF + r, n)] = recipe.score(train, cands, meta, cutoff, P).astype(np.float32)
        finally: recipe.PERM = None
        recipe._C.clear()
    pickle.dump(dict(song=cands.song.values, scores=out), open(f"{OUT}/null{TAG}_{str(cutoff)[:10]}.pkl", "wb"))
    return recipe.score(train, cands, meta, cutoff)
_all = {"probe": probe, "nullprobe": nullprobe}
PREDICTORS = {k: v for k, v in _all.items() if k in os.environ.get("W5R2_ONLY", "probe,nullprobe").split(",")}
