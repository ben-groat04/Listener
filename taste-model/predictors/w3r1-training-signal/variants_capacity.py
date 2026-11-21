"""Stage 6: model capacity (GBM size, linear ridge) at fixed signal (window 365, hl 120, rank_plays / love) on base and plus representations."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor
V = {}
for tn, t in (("rkp", "rank_plays"), ("love", "love")):
    for rep in ("base", "plus"):
        b = dict(hl=120, window=365, target=t, rep=rep)
        V[f"c_{tn}_{rep}_it60"] = dict(b, gbm=dict(max_iter=60))
        V[f"c_{tn}_{rep}_leaf4"] = dict(b, gbm=dict(max_leaf_nodes=4, min_samples_leaf=20))
        V[f"c_{tn}_{rep}_msl80"] = dict(b, gbm=dict(min_samples_leaf=80, max_iter=100))
        if t != "love":
            for a in (10, 100, 1000):
                V[f"c_{tn}_{rep}_ridge{a}"] = dict(b, model="ridge", alpha=a)
PREDICTORS = {k: make_predictor(v) for k, v in V.items()}
