"""Stage 7: exposure-context handling and within-context comparison re-tested on the best time setting (window 365, hl 120)."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor
V = {}
for mn, mo in (("gbm", dict(gbm=dict(max_iter=60))), ("ridge", dict(model="ridge", alpha=100))):
    for tn, t in (("rkp", "rank_plays"), ("love", "love")):
        if mn == "ridge" and t == "love": continue
        b = dict(hl=120, window=365, target=t, **mo)
        for ex in ("none", "w0.5", "w1", "drop5", "sole", "resid", "marg"):
            V[f"x_{mn}_{tn}_{ex}"] = dict(b, exposure=ex)
        if mn == "gbm":
            for g in ("quarter", "week", "session"): V[f"x_{mn}_{tn}_dm{g}"] = dict(b, group=g)
PREDICTORS = {k: make_predictor(v) for k, v in V.items()}
