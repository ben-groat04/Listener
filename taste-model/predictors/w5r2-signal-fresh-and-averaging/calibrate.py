"""Chance calibration: for each null seed k (harness null-v2 train: identity shuffle + artist/album relabelling, a FRESH relabelling per seed), score the family / averages (not nested) in a fresh process,
compute pooled sauc against the REAL tried-song labels, and record delta vs default.  Usage: python3 calibrate.py OUT.jsonl k0 k1  (run from taste-model/)"""
import sys, json, os, numpy as np
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evalkit import run, metrics
import grid as G
ENTRY = "/home/user/Listener/taste-model/predictors/w5r2-signal-fresh-and-averaging/predict.py"
out, k0, k1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
names = ["w5_default"] + ["f_" + k for k in G.FAMILY] + list(G.AVG)
cuts = run._cutoffs_of("tune")
real = run.score_predictor(lambda tr, c, m, ct: np.zeros(len(c)), cuts, "zero", 0, None, None, None, "all", "main")
sel = (real.is_decoy == 0).values; ft = real[sel].reset_index(drop=True)
T = metrics.Block(ft, "love", 0, 0)
for k in range(k0, k1):
    res = run.run_null_worker([ENTRY], k, "tune", names, "v2", "main")
    sa = {n: float(T.stats(np.asarray(res[n])[sel], False, ("sauc",))["sauc"][0]) for n in names}
    with open(out, "a") as fh: fh.write(json.dumps(dict(seed=k, sauc=sa)) + "\n")
