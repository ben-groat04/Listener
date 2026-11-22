"""combo_mean_oof: avg21 (MERT, mean pooling) + ref_w4r1_music, out-of-fold training-song scaling. Thin wrapper; code in core.py / grid.py (declared together)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core
FEATURES = core.FEATURES
PREDICTORS = {"combo_mean_oof": core.PREDICTORS["combo_mean_oof"]}
