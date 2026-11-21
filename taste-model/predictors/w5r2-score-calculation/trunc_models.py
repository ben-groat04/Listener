"""Diagnostic models for the history-length control (NOT a final candidate): the two references and pair_z fitted on a train truncated to the last L months before the cutoff."""
import numpy as np, pandas as pd
from evalkit import refs
SA, SB = 0.70, 1.27
def _trunc(train, cutoff, months):
    lo = pd.Timestamp(cutoff) - pd.DateOffset(months=months)
    t = train.t
    if np.issubdtype(t.dtype, np.datetime64): m = t >= lo.to_datetime64()
    else: m = t.values.astype("int64") >= lo.value
    return train[m]
def mk(months):
    def f(train, cands, meta, cutoff):
        tr = _trunc(train, cutoff, months)
        a = refs.score("ref_w4r1_listening", tr, cands, meta, cutoff); b = refs.score("ref_w4r1_music", tr, cands, meta, cutoff)
        return np.asarray(a, float) / SA + np.asarray(b, float) / SB
    return f
PREDICTORS = {"pairz_trunc12": mk(12)}
