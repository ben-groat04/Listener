"""Taste-drift / history-length views of `train` (apply to ANY predictor with `python -m evalkit.run pred.py --window W`).
v4: windows filter TRAINING SONGS by their first-play time (all streams of a song are kept or dropped together), they no longer truncate the stream log (truncating made an old
song that is replayed inside the window look like a NEW song first played inside it, and removed the history of every song first played before the window).
  all     everything before the cutoff            730 / 365  only songs first played in the last 730 / 365 days (all their streams)
  sub365  random subsample of the songs of ALL history with about as many streams as the songs first played in the last 365 days (sample-size control:
          compare 365 vs sub365 to separate 'recent is better' from 'less data is better/worse')
Run each window on dev, compare per-fold. Half-life weighting: use `train.t` and the cutoff inside the predictor."""
import numpy as np, pandas as pd

def _first(tr): return tr.groupby("song").t.transform("min")

def _last(days): return lambda tr, c: tr[(_first(tr) >= c - pd.Timedelta(days=days)).values]

def _sub365(tr, c):
    f = _first(tr); n = int((tr[(f >= c - pd.Timedelta(days=365)).values]).shape[0])
    cnt = tr.groupby("song").size(); order = np.random.default_rng(int(c.strftime("%Y%m%d"))).permutation(len(cnt))
    keep = cnt.index[order][np.cumsum(cnt.values[order]) <= n]
    return tr[tr.song.isin(set(keep)).values]

WINDOWS = {"all": None, "730": _last(730), "365": _last(365), "sub365": _sub365}
