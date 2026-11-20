import numpy as np
from scipy.stats import rankdata, spearmanr

def auc(y, s):
    y = np.asarray(y); n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return np.nan
    r = rankdata(s)  # average ranks => ties count half
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def _order(s, rng):  # random tie-break so constant scores cannot look good
    return np.lexsort((rng.random(len(s)), -np.asarray(s, float)))

def fold_metrics(y, s, seed=0):
    """AUC; AP and lift over base rate; precision in top 10% (p10) and top-20 songs (p20); recall in top 20% (r20);
    hits = positives in the top 10% and exp = hits expected at the fold's base rate (for pooled lift)."""
    y = np.asarray(y); n = len(y)
    nan = dict(auc=np.nan, ap=np.nan, lift=np.nan, p10=np.nan, p20=np.nan, r20=np.nan, hits=np.nan, exp=np.nan, n=n, n1=y.sum())
    if n < 10 or y.sum() == 0 or y.sum() == n: return nan
    o = y[_order(s, np.random.default_rng(seed))]
    prec = np.cumsum(o) / np.arange(1, n + 1)
    ap = prec[o == 1].mean(); base = y.mean(); k = max(1, round(.1 * n)); k2 = max(1, round(.2 * n))
    return dict(auc=auc(y, s), ap=ap, lift=ap / base, p10=o[:k].mean(), p20=o[:20].mean(), r20=o[:k2].sum() / y.sum(),
                hits=o[:k].sum(), exp=k * base, n=n, n1=y.sum())

def folds_arrays(df, label, subset=None, pool="tried"):
    """List of (y, score, artist) arrays per fold. subset: None=all, True=new-artist, False=known-artist.
    pool='tried' keeps only songs the user actually played (is_decoy==0); 'open' keeps tried songs + decoys."""
    out = []
    for _, g in df.groupby("fold"):
        if pool == "tried": g = g[g.is_decoy == 0]
        if subset is not None: g = g[g.new_artist == subset]
        out.append((g[label].values, g.score.values, g.artist.values))
    return out

def macro(arrs, idx=None):
    """Fold-averaged metrics (macro) plus stratified quantities that pool folds without mixing their base rates:
    sauc = AUC over all within-fold (positive, negative) pairs; plift = pooled top-10% hits / hits expected at each fold's base rate."""
    out = [fold_metrics(y[i], s[i]) if idx is not None else fold_metrics(y, s)
           for (y, s, _), i in zip(arrs, idx if idx is not None else arrs)]
    r = {k: float(np.nanmean([o[k] for o in out])) for k in ("auc", "ap", "lift", "p10", "p20", "r20")}
    w = np.array([o["n1"] * (o["n"] - o["n1"]) if np.isfinite(o["auc"]) else 0 for o in out], float)
    a = np.array([o["auc"] if np.isfinite(o["auc"]) else 0 for o in out])
    r["sauc"] = float((w * a).sum() / w.sum()) if w.sum() else np.nan
    e = np.nansum([o["exp"] for o in out]); r["plift"] = float(np.nansum([o["hits"] for o in out]) / e) if e else np.nan
    return r

def cluster_idx(cl, rng):
    """Resample whole artists (songs by one artist are correlated, so a song-level bootstrap would give CIs that are too narrow)."""
    u, inv = np.unique(cl, return_inverse=True)
    groups = np.split(np.argsort(inv, kind="stable"), np.cumsum(np.bincount(inv))[:-1])
    pick = rng.integers(0, len(u), len(u))
    return np.concatenate([groups[k] for k in pick])

def boot_idx(arrs, rng):
    return [cluster_idx(cl, rng) for _, _, cl in arrs]

def spearman_cont(df, col="days90"):
    """Mean over folds of the Spearman correlation between score and a continuous outcome (tried songs only)."""
    r = [spearmanr(g.score, g[col])[0] for _, g in df[df.is_decoy == 0].groupby("fold")]
    return float(np.nanmean(r))
