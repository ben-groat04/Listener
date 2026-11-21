"""Stage 10: audio-similarity features (CLAP of shared previews) added to the fixed base representation, at the best training-signal setting."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor, make_blend
G = dict(hl=120, window=365, gbm=dict(max_iter=60), target="rank_plays")
PREDICTORS = {"a_base": make_predictor(G), "a_base+a": make_predictor(dict(G, rep="base+a")), "a_base+x+a": make_predictor(dict(G, rep="base+x+a")),
              "a_love_base+a": make_predictor(dict(G, target="love", rep="base+a")),
              "a_lp_base+a": make_predictor(dict(G, target="lplays", rep="base+a")),
              "a_ridge_base+a": make_predictor(dict(hl=120, window=365, model="ridge", alpha=100, target="rank_plays", rep="base+a")),
              "a_blend+a+ar": make_blend([dict(G, rep="base+a"), dict(fn="artist_recent")], [1, 1]),
              "a_blend_ar": make_blend([G, dict(fn="artist_recent")], [1, 1])}
