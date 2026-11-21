"""Iteration file: fixed default + tuned procedures (different inner-fold settings / grids). Family for --walkforward."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import ens, FINAL
from grid import G_TUNE, G_NARROW
from tuned import make_tuned
PREDICTORS = {
    "fixed_default": ens(FINAL),
    "tunedA": make_tuned("tunedA", 4, 3),                      # wide grid (24), 4 inner folds x 3 months
    "tunedA_m": make_tuned("tunedA_m", 4, 3, margin=0.01),     # same inner scores, only switch if inner sauc beats default by >= 0.01
    "tunedB": make_tuned("tunedB", 6, 2),                      # 6 inner folds x 2 months
    "tunedC": make_tuned("tunedC", 3, 6),                      # 3 inner folds x 6 months
    "tunedN": make_tuned("tunedN", 4, 3, grid=G_NARROW),       # narrow grid (14)
}
WALKFORWARD_FAMILY = list(PREDICTORS)
