"""diagnostic columns for the score dump (NOT candidates): per tried song, Deezer-clip availability and alignment against the dev clip (shared-w6r1/p2_clips.csv)."""
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"
_C = {}
def _tab():
    if "t" not in _C:
        c = pd.read_csv(ROOT + ".cache/shared-w6r1/p2_clips.csv"); c = c[(c.ok == True) & (c.mert_ok == True)]; _C["t"] = c.set_index(c.trackId.astype(np.int64).astype(str))
    return _C["t"]
def col(name, fill):
    def predict(train, cands, meta, cutoff):
        t = _tab()[name].reindex([str(int(x)) for x in cands.trackId.values]).values.astype(float); return np.where(np.isfinite(t), t, fill)
    return predict
def hasdz(train, cands, meta, cutoff): return np.array([float(str(int(x)) in _tab().index) for x in cands.trackId.values])
PREDICTORS = {"diag_hasdz": hasdz, "diag_same": col("same_excerpt", -1.0), "diag_off": col("align_offset_s", 999.0), "diag_aln": col("align_score", -1.0)}
