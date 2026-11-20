import numpy as np
from scipy.stats import rankdata

def auc(y, s):
    y = np.asarray(y); n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return np.nan
    r = rankdata(s)  # average ranks => ties count half
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def _order(s, rng):  # random tie-break so constant scores cannot look good
    return np.lexsort((rng.random(len(s)), -np.asarray(s, float)))

def fold_metrics(y, s, seed=0):
    """AUC; AP and its lift over base rate; precision in top 10%; recall in top 20%."""
    y = np.asarray(y); n = len(y)
    if n < 10 or y.sum() == 0 or y.sum() == n: return dict(auc=np.nan, ap=np.nan, lift=np.nan, p10=np.nan, r20=np.nan)
    o = y[_order(s, np.random.default_rng(seed))]
    prec = np.cumsum(o) / np.arange(1, n + 1)
    ap = prec[o == 1].mean(); base = y.mean(); k = max(1, round(.1 * n)); k2 = max(1, round(.2 * n))
    return dict(auc=auc(y, s), ap=ap, lift=ap / base, p10=o[:k].mean(), r20=o[:k2].sum() / y.sum())

def folds_arrays(df, label, subset=None):
    """List of (y, score) arrays per fold, optionally restricted to new-artist (True) / known-artist (False) songs."""
    out = []
    for _, g in df.groupby("fold"):
        if subset is not None: g = g[g.new_artist == subset]
        out.append((g[label].values, g.score.values))
    return out

def macro(arrs, idx=None):
    """Mean over folds of fold_metrics. idx: optional list of per-fold resample indices (bootstrap)."""
    out = [fold_metrics(y[i], s[i]) if idx is not None else fold_metrics(y, s)
           for (y, s), i in zip(arrs, idx if idx is not None else arrs)]
    return {k: float(np.nanmean([o[k] for o in out])) for k in out[0]}

def boot_idx(arrs, rng):
    return [rng.integers(0, len(y), len(y)) for y, _ in arrs]
