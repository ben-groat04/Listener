"""evalkit v5.2: plain 80% decision rule and the comparator-set table (pooled difference, inverse-variance fold weights, heaviest folds left out).
Decision rule of this project (owner's risk preference): a paired difference is decided when the lower end of its 80% interval is above zero; no extra margin.
    decision (plain 80% rule): POS if lo80 > 0, NEG if hi80 < 0, else UNDECIDED.   The v5.1 label with a 0.005 margin is kept only as `decision80_margin005` and is never the leading column."""
import numpy as np, pandas as pd
from . import metrics

MARGIN = 0.005
def plain80(lo, hi): return "POS" if lo > 0 else "NEG" if hi < 0 else "UNDECIDED"
def margin005(lo, hi): return "POS" if lo > MARGIN else "NEG" if hi < -MARGIN else "UNDECIDED"
DROP_FRAC = 0.2   # the heaviest folds left out: the max(1, round(0.2 * k)) folds with the most loved x not-loved pairs (the weight of a fold in the pooled sauc)

def _f(x): return float(np.asarray(x).ravel()[0])
def _fmt(d, lo, hi): return "-" if not np.isfinite(d) else f"d={d:+.3f} 80%[{lo:+.3f},{hi:+.3f}]"

def heaviest_folds(base, frac=DROP_FRAC):
    """Folds with the largest number of loved x not-loved pairs (= weight in the pooled sauc), count max(1, round(frac * k)); ties by fold order."""
    g = base.assign(_y=base.love.astype(int)).groupby(base.fold.astype(str).values, sort=False)._y.agg(["sum", "count"]); w = g["sum"] * (g["count"] - g["sum"])
    k = max(1, int(round(frac * len(w)))); order = sorted(range(len(w)), key=lambda i: (-w.values[i], i)); return [str(w.index[i]) for i in order[:k]]

def _pooled(Bk, ca, cb, sa, sb):
    a = Bk.stats(sa, True, ("sauc",)); b = Bk.stats(sb, True, ("sauc",)); x = a["sauc_b"] - b["sauc_b"]
    return _f(a["sauc"]) - _f(b["sauc"]), float(np.nanpercentile(x, 10)), float(np.nanpercentile(x, 90))

def comparator_table(scored, fold_names, set_name, comps, models, nboot=1000, seed=20260511, drop_frac=DROP_FRAC, nboot_fold=400):
    """For every builder model and every comparator in `comps` (names present in `scored`, != the model): the pooled paired sauc difference (all folds, artist-cluster bootstrap, fixed seed) with its 80%
    interval and plain decision; the same difference with inverse-variance fold weights (metrics.fold_meta: per-fold paired AUC deltas, folds with < 5 loved or < 5 not-loved rows excluded) and with
    the heaviest folds left out (pooled again, same bootstrap size and seed). Returns (numeric DataFrame, printable DataFrame)."""
    first = next(iter(scored.values())); sel = ((first.is_decoy == 0) & first.fold.isin(fold_names)).values; base = first[sel].reset_index(drop=True)
    comps = [c for c in comps if c in scored]; rows = []
    if not models or not comps: return pd.DataFrame(), pd.DataFrame()
    drop = heaviest_folds(base, drop_frac); keep = ~base.fold.astype(str).isin(drop).values
    B1 = metrics.Block(base, "love", nboot, seed); B2 = metrics.Block(base[keep].reset_index(drop=True), "love", nboot, seed)
    need = list(dict.fromkeys(list(models) + comps)); vec = {}
    for n in need: assert (scored[n].trackId.values == first.trackId.values).all(); vec[n] = scored[n].score.values[sel]
    dmp = pd.DataFrame(dict(fold_set=set_name, fold=base.fold.astype(str).values, artist=base.artist.values, love=base.love.values))
    for n in need: dmp[metrics.score_col(n)] = vec[n]
    for n in models:
        for c in comps:
            if c == n: continue
            d1, l1, h1 = _pooled(B1, n, c, vec[n], vec[c]); d2, l2, h2 = _pooled(B2, n, c, vec[n][keep], vec[c][keep])
            r = metrics.fold_meta(dmp, set_name, n, c, "love", nboot_fold, 0)
            rows.append(dict(model=n, vs=c, folds=len(pd.unique(base.fold.astype(str))), d=d1, lo80=l1, hi80=h1, iv_d=r["mean"], iv_lo80=r["lo80"], iv_hi80=r["hi80"], iv_folds=r["k"], iv_excluded=r["n_excluded"],
                             drop_d=d2, drop_lo80=l2, drop_hi80=h2, dropped=",".join(drop)))
    num = pd.DataFrame(rows)
    pr = pd.DataFrame(dict(model=num.model, vs=num.vs, pooled=[_fmt(*x) for x in zip(num.d, num.lo80, num.hi80)], decision80=[plain80(a, b) for a, b in zip(num.lo80, num.hi80)],
                           iv_weighted=[_fmt(*x) for x in zip(num.iv_d, num.iv_lo80, num.iv_hi80)], decision80_iv=[plain80(a, b) if np.isfinite(a) else "-" for a, b in zip(num.iv_lo80, num.iv_hi80)],
                           iv_folds=[f"{k}/{k + e}" for k, e in zip(num.iv_folds, num.iv_excluded)],
                           heaviest_out=[_fmt(*x) for x in zip(num.drop_d, num.drop_lo80, num.drop_hi80)], decision80_heaviest_out=[plain80(a, b) for a, b in zip(num.drop_lo80, num.drop_hi80)],
                           folds_left_out=num.dropped, decision80_margin005=[margin005(a, b) for a, b in zip(num.lo80, num.hi80)]))
    return num, pr
