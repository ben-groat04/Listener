"""Procedures built on recipe.py: nested in-train selection (evalkit.inner) with shrinkage, selection-free averaging, and chunked variant files."""
import os, sys, json, itertools
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recipe, grid
from evalkit import inner

def _P(name): return grid.SELECT_FAMILY[name]

def variant(P):
    def predict(train, cands, meta, cutoff): return recipe.score(train, cands, meta, cutoff, P)
    return predict

def avg_family(fam=None):
    fam = fam or grid.FAMILY_AVG
    Ps = [dict(eps=e, alphaA=a, alphaS=a, gbm=g, wm=m) for e, a, g, m in itertools.product(fam["eps"], fam["alpha"], fam["gbm"], fam["wm"])]
    def predict(train, cands, meta, cutoff):
        th = recipe._train_hash(train, cutoff, cands)
        return sum(recipe.score(train, cands, meta, cutoff, P, th) for P in Ps) / len(Ps)
    return predict

_INNER = {}
MIN_TRAIN_SONGS = 300
def nchanged(P): return sum(1 for k, v in P.items() if grid.D[k] != v and not (k == "mfill" and v is None))

def inner_table(train, meta, cutoff, names, n_folds=4):
    key = (str(cutoff), len(train), int(train.t.values.astype("int64").sum() % (1 << 60)), tuple(names), n_folds)
    if key in _INNER: return _INNER[key]
    folds = inner.make_inner_folds(train, meta, cutoff, n_folds=n_folds)
    folds = [f for f in folds if f["labels"]["love"].sum() >= 3 and (1 - f["labels"]["love"]).sum() >= 3 and f["train_streams"].song.nunique() >= MIN_TRAIN_SONGS]   # tiny inner trains (earliest cutoffs) break song_table / are meaningless: such folds are dropped
    res = {}
    if len(folds) >= 2:
        for nm in names:
            P = grid.SELECT_FAMILY[nm]
            res[nm] = inner.inner_sauc([recipe.score(f["train_streams"], f["cands"], meta, f["inner_cutoff"], P) for f in folds], folds)
    _INNER[key] = (res, len(folds)); return _INNER[key]

def nested(margin=0.0, pen=0.0, names=None, n_folds=4):
    names = names or list(grid.SELECT_FAMILY)
    def predict(train, cands, meta, cutoff):
        res, nf = inner_table(train, meta, cutoff, names, n_folds)
        ch = "default"
        if nf >= 2 and res:
            d0 = res["default"]; best, bv = "default", 0.0
            for nm in names:
                v = res[nm] - d0 - pen * nchanged(grid.SELECT_FAMILY[nm])
                if np.isfinite(v) and v > bv: best, bv = nm, v
            if bv > margin: ch = best
        predict.chosen[str(cutoff)] = ch
        return recipe.score(train, cands, meta, cutoff, grid.SELECT_FAMILY[ch])
    predict.chosen = {}
    return predict
