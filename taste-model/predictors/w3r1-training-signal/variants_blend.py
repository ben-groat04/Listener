"""Stage 8: blends of training signals / model types (each member standardised on its own training-row predictions)."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor, make_blend
G = dict(hl=120, window=365, gbm=dict(max_iter=60))
R = dict(hl=120, window=365, model="ridge", alpha=100)
gk = dict(G, target="rank_plays"); gl = dict(G, target="love"); gp = dict(G, target="lplays"); rk = dict(R, target="rank_plays"); rl = dict(R, target="lplays")
rs = dict(R, target="rank_share")
PREDICTORS = {
 "b_gbm_rkp": make_predictor(gk),
 "b_gbm_rkp+love": make_blend([gk, gl]),
 "b_gbm_rkp+lp": make_blend([gk, gp]),
 "b_gbm_rkp+ridge_rkp": make_blend([gk, rk]),
 "b_gbm_rkp+gbm_love+ridge_rkp": make_blend([gk, gl, rk]),
 "b_4way": make_blend([gk, gl, gp, rk, rl]),
 "b_gbm_rkp+ridge_rkp_resid": make_blend([dict(gk, exposure="resid"), dict(rk, exposure="resid")]),
 "b_gbm_rkp+ridge_share": make_blend([gk, rs]),
 "b_win_mix": make_blend([gk, dict(gk, window=270), dict(gk, window=730, hl=240), rk]),
}
