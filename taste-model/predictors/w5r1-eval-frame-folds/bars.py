"""Bar variants for the frame study (item 3): alternative artist_recent half-lives and nonaudio_gbm settings, scored through the harness (--fast --folds ... --refs none) so
they land in the score dump. Pre-written list (11 variants): hl30, hl60, hl90, hl365, hl730 ; gbm_w_none (uniform training weights), gbm_w90, gbm_w365, gbm_nomono (no monotone
constraints), gbm_big (max_iter 300, 16 leaves, min leaf 20), gbm_small (max_iter 60). Nothing here is tuned to win; each variant is only a sensitivity of the bar."""
import sys, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evalkit import baselines as B

def _hl(h):
    def f(train, cands, meta, cutoff): return np.log1p(B._artist_score(train, cands, cutoff, h))
    return f

def _gbm(name, weight_hl=180.0, mono=True, kw=None):
    inner = B._make(name, True, True)
    def f(train, cands, meta, cutoff):
        old = (B.WEIGHT_HL, dict(B.GBM_KW), dict(B.MONO))
        try:
            B.WEIGHT_HL = weight_hl
            if kw: B.GBM_KW.update(kw)
            if not mono: B.MONO.clear()
            return inner(train, cands, meta, cutoff)
        finally:
            B.WEIGHT_HL, B.GBM_KW, B.MONO = old[0], old[1], old[2]
    return f

PREDICTORS = {f"bar_hl{h}": _hl(h) for h in (30, 60, 90, 365, 730)}
PREDICTORS.update({
    "bar_gbm_w_none": _gbm("bar_gbm_w_none", None), "bar_gbm_w90": _gbm("bar_gbm_w90", 90.0), "bar_gbm_w365": _gbm("bar_gbm_w365", 365.0),
    "bar_gbm_nomono": _gbm("bar_gbm_nomono", mono=False),
    "bar_gbm_big": _gbm("bar_gbm_big", kw=dict(max_iter=300, max_leaf_nodes=16, min_samples_leaf=20)),
    "bar_gbm_small": _gbm("bar_gbm_small", kw=dict(max_iter=60)),
})
