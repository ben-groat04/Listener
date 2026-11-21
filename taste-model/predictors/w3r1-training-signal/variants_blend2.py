"""Stage 9: shrink the learned score toward the plain frequency statistic (artist_recent, standardised) -- user's 'listening statistics are the most reliable indicator'."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor, make_blend
G = dict(hl=120, window=365, gbm=dict(max_iter=60), target="rank_plays")
R = dict(hl=120, window=365, model="ridge", alpha=100, target="rank_plays")
AR = dict(fn="artist_recent")
PREDICTORS = {}
for w in (0.5, 1, 2):
    PREDICTORS[f"m_gbm+ar{w}"] = make_blend([G, AR], [1, w])
    PREDICTORS[f"m_gbm+ridge+ar{w}"] = make_blend([G, R, AR], [1, 1, 2 * w])
    PREDICTORS[f"m_mix+ar{w}"] = make_blend([G, dict(G, window=270), dict(G, window=730, hl=240), R, AR], [1, 1, 1, 1, 4 * w])
