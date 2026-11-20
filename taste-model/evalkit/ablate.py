"""Taste-drift / history-length views of `train` (apply to ANY predictor with `python -m evalkit.run pred.py --window W`).
  all     everything before the cutoff            730 / 365  only the last 730 / 365 days of streams
  sub365  random subsample of ALL history with the same number of streams as the last 365 days (sample-size control:
          compare 365 vs sub365 to separate 'recent is better' from 'less data is better/worse')
Run each window on dev, compare per-fold. Half-life weighting: use `train.t` and the cutoff inside the predictor."""
import numpy as np, pandas as pd

def _last(days): return lambda tr, c: tr[tr.t >= c - pd.Timedelta(days=days)]

def _sub365(tr, c):
    n = int((tr.t >= c - pd.Timedelta(days=365)).sum()); n = min(n, len(tr))
    keep = np.sort(np.random.default_rng(int(c.strftime("%Y%m%d"))).choice(len(tr), n, replace=False))
    return tr.iloc[keep]

WINDOWS = {"all": None, "730": _last(730), "365": _last(365), "sub365": _sub365}
