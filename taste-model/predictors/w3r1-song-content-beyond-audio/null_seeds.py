"""Extra null-control draws (the harness uses one fixed shuffle per fold): identity-shuffle with several seeds; prints tried sauc and wa on TUNE per seed."""
import sys, os, numpy as np
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, os.path.dirname(__file__))
from evalkit import run, data, metrics
import predict as P
cuts = data.TUNE_CUTOFFS; fl = run.prepare_folds(cuts)
for seed in range(6):
    out = {}
    for k in ("lyr_resid_nodur", "lyr_resid_orth", "lyr_all"):
        rows = []
        for f in fl:
            tr = run._null_control(f["train"], np.random.default_rng(1000 * seed + int(f["c"].strftime("%y%m"))))
            sc = P.PREDICTORS[k](tr, f["cands"], f["meta"], f["c"]); rows.append(f["pool"].iloc[f["order"]].assign(fold=str(f["c"].date()), score=sc))
        import pandas as pd; df = pd.concat(rows, ignore_index=True); df = df[df.is_decoy == 0].reset_index(drop=True)
        B = metrics.Block(df, "love", 1, 0); r = B.stats(df.score.values, False, ("sauc", "wa"))
        out[k] = (round(float(r["sauc"][0]), 3), round(float(r["wa"][0]), 3))
    print(seed, out, flush=True)
