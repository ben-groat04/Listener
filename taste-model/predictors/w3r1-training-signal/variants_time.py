"""Stage 3: history window / recency weighting / old listening, and pairwise / within-context comparison; target fixed per block."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor
V = {}
for tn, t in (("love", "love"), ("rkp", "rank_plays")):
    for hl in (None, 60, 120, 365, 730):
        V[f"h_{tn}_hl{hl}"] = dict(hl=hl, target=t)
    for win in (365, 730, 1095):
        V[f"h_{tn}_win{win}"] = dict(hl=180, window=win, target=t)
    V[f"h_{tn}_skip120"] = dict(hl=180, skip_start=120, target=t)
    V[f"h_{tn}_nomono"] = dict(hl=180, nomono=True, target=t)
for g in ("quarter", "week", "session", "artist"):
    V[f"g_dm_{g}"] = dict(hl=180, target="lplays", group=g)
    V[f"g_rank_{g}"] = dict(hl=None, target="grade", group=g, model="rank")
PREDICTORS = {k: make_predictor(v) for k, v in V.items()}
