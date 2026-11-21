"""Ablation predictors (harness entry file; TUNE only, --fast).  usage (from taste-model/):  python3 -W ignore -m evalkit.run --fast predictors/w3r1-content-audio/ablations.py
(1) whole-clip vs time-local; (2) missing-audio handling; (3) training-history recency weighting (hl = half-life in days, None = uniform).  All audio-only unless named meta."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from predict import make
PREDICTORS = {
 "ab1_whole": make(), "ab1_local_mean": make(mode="local"), "ab1_local_max": make(mode="local", agg="max"), "ab1_local_top2": make(mode="local", agg="top2"),
 "ab1_local_meanstd": make(mode="local", agg="meanstd"), "ab1_local_win1": make(mode="whole", windows=(0,)), "ab1_local_win2": make(mode="whole", windows=(1,)),
 "ab2_miss_neutral": make(), "ab2_miss_min": make(miss="min"), "ab2_miss_max": make(miss="max"), "ab2_indicator_only": make(miss="indicator"),
 "ab3_hl_none": make(hl=None), "ab3_hl_730": make(hl=730), "ab3_hl_365": make(hl=365), "ab3_hl_180": make(hl=180), "ab3_hl_90": make(hl=90), "ab3_hl_45": make(hl=45),
}
