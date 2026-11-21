"""Artist-recognition check (fast TUNE only): final / linear-only / clip-mean control re-fitted with every stream of the candidate's artist group removed from train."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from predict import PREDICTORS as _P, excl
PREDICTORS = {"excl_final_ens": excl(_P["final_ens"]), "excl_abl_linear_only": excl(_P["abl_linear_only"]), "excl_ctl_clipmean_mert": excl(_P["ctl_clipmean_mert"])}
