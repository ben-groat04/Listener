"""FINAL FILE w6r2 avg21_fb (one model): the round-1 avg21 recipe (21 listening-signal configs, 4 members each, MERT layers 4-8, whitened PCA + weighted ridge) trained and scored on whatever clip the harness feature
lookup holds for a track (features.mert: stored preview, else the sealed pipeline's fallback order Spotify embed, iTunes, Deezer). Explicit fallback handling: no source-specific correction (round-2 measurements showed
none that is label-free, fittable from sealed-producible inputs and helpful, see report); a track with no clip at all gets the neutral score 0. Scores are identical to round-1 avg21_dev (a round-1 variant).
Features only through evalkit.features (FEATURES below)."""
import importlib.util, os
_p = "/home/user/Listener/taste-model/predictors/w6r1-content-ranker-final/predict.py"
_s = importlib.util.spec_from_file_location("w6r2_core", _p); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
FEATURES = ("mert",)
PREDICTORS = {"avg21_fb": _m.PREDICTORS["avg21_dev"]}
