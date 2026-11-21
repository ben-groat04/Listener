"""Round-1 reference predictor ca_local (w3r1-content-audio, time-local MERT window logits), exposed under its own name for the final runs.
The w3r1 fit cache is keyed by (cutoff, n, sum of timestamps) and so is NOT invalidated by the null control's identity shuffle (timestamps unchanged);
this wrapper clears that cache whenever the train song/trackId identity hash changes.
Usage: python3 -W ignore -m evalkit.run predictors/w3r2-audio-taste/predict.py predictors/w3r2-audio-taste/ref_ca_local.py"""
import sys; sys.path.insert(0, "/home/user/Listener/taste-model/predictors/w3r1-content-audio")
import pandas as pd
import predict as _p
_f = _p.make(mode="local"); _last = [None]
def ca_local(train, cands, meta, cutoff):
    tag = (str(cutoff), int(pd.util.hash_pandas_object(train[["trackId", "song"]].astype(str), index=False).sum() % (1 << 60)))
    if tag != _last[0]: _p._CACHE.clear(); _last[0] = tag
    return _f(train, cands, meta, cutoff)
PREDICTORS = {"ca_local": ca_local}
