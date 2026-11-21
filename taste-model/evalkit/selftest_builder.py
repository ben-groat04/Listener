"""Tiny deterministic builder file used only by the evalkit selftest (three cheap models; no training)."""
import numpy as np

def _dur(train, cands, meta, cutoff):
    d = meta["durationMs"].reindex(cands.trackId.values).astype(float).values
    return np.nan_to_num(d, nan=np.nanmedian(d) if np.isfinite(d).any() else 0.0)

def _rand_a(train, cands, meta, cutoff): return (cands.trackId.values % 1000003) / 1000003.0
def _rand_b(train, cands, meta, cutoff): return (cands.trackId.values % 999983) / 999983.0
PREDICTORS = {"sb_dur": _dur, "sb_rand_a": _rand_a, "sb_rand_b": _rand_b}
