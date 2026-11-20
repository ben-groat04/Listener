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

def macro(df, label, subset=None, rng=None):
    """Mean over folds of fold_metrics. df has columns fold, score, <label>, new_artist. With rng: bootstrap resample songs within fold."""
    out = []
    for _, g in df.groupby("fold"):
        if subset is not None: g = g[g.new_artist == subset]
        if rng is not None: g = g.iloc[rng.integers(0, len(g), len(g))]
        out.append(fold_metrics(g[label].values, g.score.values))
    return {k: float(np.nanmean([o[k] for o in out])) for k in out[0]}
