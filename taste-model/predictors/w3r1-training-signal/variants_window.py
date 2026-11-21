"""Stage 4: window length x recency weight x target."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor
V = {}
for t in ("rank_plays", "lplays", "love_4_2", "rank_share", "grade"):
    for win in (180, 270, 365, 450):
        for hl in (None, 120):
            V[f"w_{t}_{win}_{hl}"] = dict(hl=hl, window=win, target=t)
PREDICTORS = {k: make_predictor(v) for k, v in V.items()}
