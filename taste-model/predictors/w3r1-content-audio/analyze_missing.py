"""Ablation 2 (missing audio): metrics with songs lacking usable audio EXCLUDED vs INCLUDED (all pool rows, tried + decoys, of the TUNE folds), plus the share of missing songs among
loved/not-loved/decoys.  usage (from taste-model/):  python3 -W ignore predictors/w3r1-content-audio/analyze_missing.py [--late]
Baselines come from the harness cache; the subset is applied identically to every model, then run.summarize is used unchanged."""
import os, sys, hashlib, pickle
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from evalkit import data, run
import predict as P
pd.set_option("display.width", 250, "display.max_columns", 50)
late = "--late" in sys.argv
cut = data.DEV_CUTOFFS if late else data.TUNE_CUTOFFS
models = {"ca_whole": P.PREDICTORS["ca_whole"], "ca_local": P.PREDICTORS["ca_local"], "ca_indicator_only": P.make(miss="indicator")}
cache = pickle.load(open(run._cache_path(), "rb"))
scored = {k: run.score_predictor(f, cut, k, 0, False, None, cache, "all") for k, f in run.BASELINES.items()}
scored.update({k: run.score_predictor(f, cut, k, 0) for k, f in models.items()})
idx, _ = P._store(); has = []
for F in run.prepare_folds(cut):
    u = F["meta"].previewUrl.reindex(F["cands"].trackId).values
    ok = np.array([isinstance(x, str) and hashlib.md5(x.encode()).hexdigest() in idx for x in u]); has.append(ok[np.argsort(F["order"])] if False else ok)
# score_predictor returns rows in public order (pool.iloc[order]) == cands order, so `has` aligns row by row
has = np.concatenate(has); first = next(iter(scored.values()))
print("rows", len(first), "with audio", has.mean().round(3))
tr = first[first.is_decoy == 0]; hh = has[(first.is_decoy == 0).values]
print("share WITH audio: loved %.3f  not-loved %.3f  decoys %.3f" % (hh[tr.love.values == 1].mean(), hh[tr.love.values == 0].mean(), has[(first.is_decoy == 1).values].mean()))
for nm, mask in (("INCLUDED (all songs)", np.ones(len(has), bool)), ("EXCLUDED (audio-only subset)", has)):
    sub = {k: v[mask].reset_index(drop=True) for k, v in scored.items()}
    for k in sub: sub[k].attrs.update(scored[k].attrs)
    for sl, fl in (("TUNE", data.TUNE_CUTOFFS),) + ((("LATE", data.LATE_CUTOFFS),) if late else ()):
        tabs, _ = run.summarize(sub, [str(c.date()) if hasattr(c, "date") else str(c) for c in fl], 100, 1, seed=5, valid=list(run.BASELINES))
        print("\\n=====", nm, sl); print(tabs["tried_within_group"].to_string(index=False)); print(tabs["open_love"][["model", "open_sauc_all", "open_wa", "open_p20"]].to_string(index=False))
