"""Reference predictors as a library (evalkit v4.1):  `evalkit.refs.score(name, train, cands, meta, cutoff=None)` for name in REFS.

The three references are the harness' reference rows (ref_audio_final, ref_w4r1_listening, ref_w4r1_music). `score` returns the reference's scores for `cands` by CALLING THE REFERENCE
CODE ON THE GIVEN `train` (train-only fits; nothing precomputed on the pools is read). So when a predictor that calls it is run on the null-control train (relabelled / shuffled
identities) the references run on that null train as well, like any other code of the predictor. Use it for stacking: members inherit the reference's training choices.
cutoff: the fold cutoff the predictor was called with (pass it); if None it is inferred as the first dev / sealed fold cutoff after the last stream of `train`.
Fit caches: the references keep an in-process fit cache keyed on the train identities (their own keys, see each predict.py). On top of that this module keeps ONE strong identity key per
reference (position-weighted hashes of trackId, song, artist, albumId, timestamps, the null seed and the cutoff) and DROPS the reference's fit caches whenever that key changes, so a cache can
never be reused for a different train, seed or relabelling even if a reference's own key were blind to a permutation of rows. EVALKIT_NO_FIT_CACHE is honoured by the references themselves.
Caches the references need (compact feature stores) are rebuilt from their build scripts if absent (`ensure`)."""
import os, sys, hashlib, importlib.util, subprocess
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "predictors"
# name -> (entry file, PREDICTORS key, [(output that must exist, build script)])
REFS = {
    "ref_audio_final": (P / "w3r2-audio-taste" / "predict.py", "audio_final", []),   # reads the frozen shared MERT / CLAP shards directly
    "ref_w4r1_listening": (P / "w4r1-taste-from-all-listening" / "predict.py", "w4r1_final", [(ROOT / ".cache" / "w4r1" / "compact.npz", P / "w4r1-taste-from-all-listening" / "build_compact.py")]),
    "ref_w4r1_music": (P / "w4r1-what-in-the-music" / "predict.py", "final_content", [(ROOT / ".cache" / "w4r1-what-in-the-music" / "compact.npz", P / "w4r1-what-in-the-music" / "build_compact.py")]),
}

def ensure(name):
    """Rebuild the compact caches of reference `name` from its build scripts if they are absent (run as a script from taste-model/, in a subprocess)."""
    for out, script in REFS[name][2]:
        if not Path(out).exists():
            Path(out).parent.mkdir(parents=True, exist_ok=True)
            r = subprocess.run([sys.executable, "-W", "ignore", str(script)], cwd=str(ROOT), capture_output=True, text=True)
            if r.returncode != 0 or not Path(out).exists(): raise RuntimeError(f"could not regenerate {out} with {script}:\n{r.stderr[-2000:]}")

_MOD = {}; _GUARD = {}
def _load(name):
    if name not in _MOD:
        ensure(name); f, key, _ = REFS[name]
        spec = importlib.util.spec_from_file_location("evalkit_ref_" + name, str(f)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        _MOD[name] = (m, m.PREDICTORS[key])
    return _MOD[name]

def _hid(a): return hashlib.md5(pd.util.hash_array(np.asarray(a).astype(str).astype(object)).tobytes()).hexdigest()

def train_key(train, cutoff):
    """Strong identity key of a train frame: order-sensitive hashes of the identity columns and the timestamps, the null seed and the cutoff."""
    return (str(cutoff), os.environ.get("EVALKIT_NULL_SEED", ""), len(train), _hid(train.trackId.values), _hid(train.song.values), _hid(train.artist.values), _hid(train.albumId.values),
            hashlib.md5(train.t.values.astype("int64").tobytes()).hexdigest())

def _clear_fit_caches(m, fn):
    for d in (m.__dict__.get("_CACHE"), fn.__globals__.get("_CACHE")):
        if isinstance(d, dict): d.clear()
    for v in (m.__dict__.get("_M") or {}).values():   # a reference that loads another predictor module lazily (w4r1_music -> w3r2 audio_final): clear that one's cache too
        g = getattr(v, "__globals__", {})
        if isinstance(g.get("_CACHE"), dict): g["_CACHE"].clear()

def fn(name):
    """The reference as a harness predictor `predict(train, cands, meta, cutoff)`, with the identity guard described in the module docstring."""
    m, f = _load(name)
    def predict(train, cands, meta, cutoff):
        k = train_key(train, cutoff)
        if _GUARD.get(name) != k: _clear_fit_caches(m, f); _GUARD[name] = k
        return np.asarray(f(train, cands, meta, cutoff), float)
    predict.__name__ = name
    return predict

def infer_cutoff(train):
    from . import data
    last = train.t.max(); cs = sorted(pd.Timestamp(c) for c in data.DEV_CUTOFFS + data.SEALED_CUTOFFS)
    for c in cs:
        if c > last: return c
    raise ValueError("cannot infer the cutoff from train; pass cutoff=")

def score(name, train, cands, meta, cutoff=None):
    """Scores of reference `name` for `cands` (np.ndarray, one per candidate), fitted on `train` only. See the module docstring."""
    if name not in REFS: raise KeyError(f"unknown reference {name!r}; choose from {sorted(REFS)}")
    return fn(name)(train, cands, meta, pd.Timestamp(cutoff) if cutoff is not None else infer_cutoff(train))
