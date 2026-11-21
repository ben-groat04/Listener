"""Stage 2: handling of exposure context (#new songs in the session of the first play) of HISTORY songs when building training examples; target fixed per block."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor
V = {}
for tn, t in (("love", "love"), ("rkp", "rank_plays")):
    b = dict(hl=180, target=t)
    V[f"e_{tn}_none"] = dict(b)
    V[f"e_{tn}_w0.5"] = dict(b, exposure="w0.5")
    V[f"e_{tn}_w1"] = dict(b, exposure="w1")
    V[f"e_{tn}_drop5"] = dict(b, exposure="drop5")
    V[f"e_{tn}_sole"] = dict(b, exposure="sole")
    V[f"e_{tn}_resid"] = dict(b, exposure="resid")
    V[f"e_{tn}_marg"] = dict(b, exposure="marg")
PREDICTORS = {k: make_predictor(v) for k, v in V.items()}
