"""Scores every OAT + random-joint recipe of grid.py as a model (fast TUNE, --dump-scores). Run with W5_PERMSEED=<k> for the random-label calibration."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import ens
from grid import ALL
PREDICTORS = {k: ens(*v) for k, v in ALL.items()}
