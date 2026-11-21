"""DECLARED FINAL (w5r1-tune-content-numbers): inner-tuned MERT-ridge recipe with a conservative switch rule (tunedA_m): at each outer cutoff, 24 recipes (grid.G_TUNE) are scored by pooled AUC on 4 inner time-split folds x 3 months
(evalkit.inner, built from the fold's own train); the default recipe (W3 audio_final) is replaced only if the best recipe's inner sauc beats the default's by >= 0.01; otherwise (and with < 2 usable inner folds) the default is used."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tuned import make_tuned
PREDICTORS = {"w5_tuned_margin": make_tuned("w5_tuned_margin", 4, 3, margin=0.01)}
