"""Lean harness entry for the full TUNE / null / LATE / HOLDOUT runs: the declared final (final_ens) and three of its ablations. Code lives in predict.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from predict import PREDICTORS as _P
PREDICTORS = {k: _P[k] for k in ["final_ens", "abl_linear_only", "abl_no_panel", "ctl_clipmean_mert"]}
