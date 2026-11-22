"""evalkit v5.2 output-sanity helpers for analysis scripts.
    from evalkit import sanity
    sanity.assert_no_nan(table, "my table")                         # raises AssertionError naming the first NaN cells
    sanity.assert_fold_count(table, "tune")                         # table has a fold column (default 'fold'); the number of distinct folds must equal that of fold set 'tune' (10)
    sanity.assert_table(table, "my table", fold_set="tune")         # both
Expected counts: default folds tune 10 / late 4 / dev 14 (data.*_CUTOFFS) and every alternative set of evalkit.folds (tune_q1 11, tune_q2 11, tune_m 30, tune_h 5, tune_y 3).
Also accepts a plain integer as `expected`. Numeric NaN, inf and None are all refused; `allow` names columns that may legitimately hold NaN."""
import numpy as np, pandas as pd

def expected_folds(fold_set):
    if isinstance(fold_set, (int, np.integer)): return int(fold_set)
    from . import data, folds
    d = {"tune": len(data.TUNE_CUTOFFS), "late": len(data.LATE_CUTOFFS), "dev": len(data.DEV_CUTOFFS)}
    if fold_set in d: return d[fold_set]
    return len(folds.windows(fold_set))

def assert_no_nan(table, name="table", allow=()):
    t = pd.DataFrame(table) if not isinstance(table, pd.DataFrame) else table
    assert len(t) > 0, f"{name}: empty table"
    bad = {}
    for c in t.columns:
        if c in allow: continue
        col = t[c]; m = col.isna().values
        if pd.api.types.is_numeric_dtype(col): m = m | ~np.isfinite(col.values.astype(float))
        if m.any(): bad[c] = int(m.sum())
    assert not bad, f"{name}: NaN / inf / missing cells per column: {bad}"
    return t

def assert_fold_count(table, expected, fold_col="fold", name="table"):
    n = expected_folds(expected); t = pd.DataFrame(table) if not isinstance(table, pd.DataFrame) else table
    got = t.index if fold_col is None else t[fold_col]
    k = len(pd.unique(np.asarray(got).astype(str)))
    assert k == n, f"{name}: {k} distinct folds, expected {n} ({expected})"
    return k

def assert_table(table, name="table", fold_set=None, fold_col="fold", allow=()):
    assert_no_nan(table, name, allow)
    if fold_set is not None: assert_fold_count(table, fold_set, fold_col, name)
    return table
