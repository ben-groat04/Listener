"""Stage 5: representation additions with the best training-signal settings fixed (window 365, hl 120, graded targets)."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor
V = {}
for tn, t in (("rkp", "rank_plays"), ("lp", "lplays"), ("love", "love")):
    for rep in ("base", "plus"):
        V[f"r_{tn}_{rep}"] = dict(hl=120, window=365, target=t, rep=rep)
PREDICTORS = {k: make_predictor(v) for k, v in V.items()}
