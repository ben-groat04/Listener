"""Honest tuning: at every outer cutoff choose the recipe from G_TUNE by pooled inner-fold AUC (evalkit.inner, built from the fold's own train only), refit the chosen recipe on the whole train, score cands.
Fallback: fewer than 2 usable inner folds -> default recipe. Ties / no gain beyond `margin` -> default (listed first)."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from core import member, combine, ens, BASE, FINAL
from grid import G_TUNE, OAT
from evalkit import inner

def _recipe_scores(recipe, tr, cands, meta, cut):
    ms, wts, miss = recipe; ms = [{**BASE, **m} for m in ms]
    return combine([member(tr, cands, meta, cut, m) for m in ms], wts or [1] * len(ms), miss)

def make_tuned(name, n_folds=4, spacing=3, margin=0.0, grid=None, min_folds=2):
    grid = grid or G_TUNE
    def predict(train, cands, meta, cutoff):
        folds = inner.make_inner_folds(train, meta, cutoff, n_folds=n_folds, spacing_months=spacing)
        best, info = "default", {}
        if len(folds) >= min_folds:
            for k, rc in grid.items():
                info[k] = float(inner.inner_sauc([_recipe_scores(rc, f["train_streams"], f["cands"], meta, f["inner_cutoff"]) for f in folds], folds))
            d0 = info["default"]
            cand = max(info, key=lambda k: (info[k], k == "default")); best = cand if info[cand] > d0 + margin else "default"
        p = os.environ.get("W5_CHOICELOG")
        if p and not os.environ.get("EVALKIT_NULL_SEED"):
            with open(p, "a") as f: f.write(json.dumps(dict(proc=name, cutoff=str(cutoff), n_inner=len(folds), chosen=best, inner=info)) + "\n")
        return _recipe_scores(grid[best], train, cands, meta, cutoff)
    return predict
