"""evalkit.features (v5.3): THE lookup for per-clip audio features and catalogue context, dev era and sealed era alike.
Final model files and the references read features through this module and never open a cache path themselves, so the same code scores dev folds and sealed folds.

    from evalkit import features                      # (predictors: sys.path.insert(0, "/home/user/Listener/taste-model") first)
    X, has   = features.mert(meta, tids)              # [n, 4 windows, 768] float32 (mean of layers lo..hi, default 4..8 as in the references) and a has-audio mask [n]
    X, has   = features.mert(meta, tids, layers=None) # all 12 layers: [n, 4, 12, 768] float32
    ctx      = features.deezer(meta, tids)            # list of dict (Deezer context record of the track) or None, one per tid
    keys     = features.clip_keys(meta, tids)         # clip key per tid (None = no audio source): md5(previewUrl) as in every dev cache; md5("spotify:"+spotifyId) when the meta row has no previewUrl
    idx, arr = features.mert_full()                   # whole MERT store (dev shards, then sealed shards): key -> row, array [N,4,12,768] float16 (what ref_audio_final reads)
    C        = features.compact("w4r1")               # compact store (dict of arrays, key column `md5`) = dev compact + sealed-era compact; name in COMPACT_NAMES
    features.coverage(meta, tids)                     # share of tids with MERT / essentia / deezer features

Search order everywhere: the dev caches first (never modified), then the sealed-era caches (written only by `python3 -m evalkit.sealed_prep`, MAIN SESSION ONLY). A key found in both
keeps the dev row. With no sealed-era cache present every function returns exactly what the old direct reads returned (selftest --v53 asserts v5.2 equality of the default output).
Sealed-era cache root: .cache/evalkit-cache/sealed-feats-v1/ (env EVALKIT_SEALED_FEATURE_DIR overrides it: used by the acceptance test, never needed otherwise)
    mert-v1/shard_*.npz       md5 [n] (clip key), feat [n,4,12,768] float16 (same layout, extraction code and quantisation as the dev shards)
    previews/manifest.csv     key, previewUrl, source (stored | spotify_embed | itunes | deezer | dev_audio), ok, ext, bytes, duration_s, error;  previews/audio/<key>.<ext>
    compact/<name>/compact.npz  rebuilt derived caches (same build code as the dev compact files, sealed-era clips only)
    deezer/context.jsonl      one record per track: trackId (public opaque id), key, found, deezer_id, rank, ... (see sealed_prep)
Dev Deezer context: glob .cache/shared-w6r*/deezer*.jsonl (records with `trackId`); the first record found for a trackId wins (dev before sealed).
Test hook: EVALKIT_HIDE_KEYS_FILE = a text file of clip keys (one per line) that the DEV stores pretend not to have (used only by the hide-and-rebuild acceptance test)."""
import os, glob, json, hashlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEV_MERT = ROOT / ".cache" / "shared" / "w3r1-mert-v1"
DEV_COMPACT = {"w4r1": ROOT / ".cache" / "w4r1" / "compact.npz", "w4r1-what-in-the-music": ROOT / ".cache" / "w4r1-what-in-the-music" / "compact.npz"}
COMPACT_NAMES = tuple(DEV_COMPACT)
SEALED_VERSION = "sealed-feats-v1"

def sealed_root():
    return Path(os.environ.get("EVALKIT_SEALED_FEATURE_DIR") or (ROOT / ".cache" / "evalkit-cache" / SEALED_VERSION))

_C = {}
def reset():
    """Drop the in-process stores (after the environment variables / the sealed directory changed)."""
    _C.clear()

def _hidden():
    f = os.environ.get("EVALKIT_HIDE_KEYS_FILE")
    return set(Path(f).read_text().split()) if f and Path(f).exists() else set()

def md5(s): return hashlib.md5(s.encode()).hexdigest()

def clip_key_of(previewUrl, spotifyId=None):
    if isinstance(previewUrl, str) and previewUrl: return md5(previewUrl)
    if isinstance(spotifyId, str) and spotifyId: return md5("spotify:" + spotifyId)
    return None

def clip_keys(meta, tids):
    """Clip key of each track id of `meta` (None where the meta row has neither a previewUrl nor a spotifyId, or the id is not in meta)."""
    m = meta.reindex(tids); sid = m["spotifyId"].values if "spotifyId" in m.columns else [None] * len(m)
    return [clip_key_of(u, s) for u, s in zip(m["previewUrl"].values, sid)]

# ------------------------------------------------------------------ MERT
def _mert_dirs(): return [("dev", DEV_MERT), ("sealed", sealed_root() / "mert-v1")]

def mert_full():
    """(key -> row index, float16 array [N,4,12,768]) over the dev shards and then the sealed-era shards (a key present in both keeps its dev row)."""
    if "mert" not in _C:
        keys, arrs, hide = [], [], _hidden(); n_dev = None
        for era, d in _mert_dirs():
            if era == "sealed": n_dev = len(keys)
            for f in sorted(glob.glob(str(d / "shard_*.npz"))):
                z = np.load(f); k = [str(x) for x in z["md5"]]; feat = z["feat"]
                if era == "dev" and hide: keep = np.array([x not in hide for x in k]); k = [x for x, kp in zip(k, keep) if kp]; feat = feat[keep]
                if len(k): keys += k; arrs.append(feat)
        n_dev = len(keys) if n_dev is None else n_dev
        idx = {}
        for i in list(range(n_dev, len(keys))) + list(range(n_dev)): idx[keys[i]] = i   # sealed rows first, then dev rows override them; inside the dev era the last row of a key wins (as the old direct reads did)
        _C["mert"] = (idx, np.concatenate(arrs) if arrs else np.zeros((0, 4, 12, 768), np.float16))
    return _C["mert"]

def mert(meta, tids, layers=(4, 8)):
    """MERT-v1-95M features of the tracks' preview clips. layers=(lo, hi): mean over layers lo..hi inclusive -> [n,4,768]; layers=None: all layers [n,4,12,768]. Rows without audio are 0 and has=False
    (NaN rows count as missing). Per clip, independent of every other track."""
    idx, arr = mert_full(); ks = clip_keys(meta, tids); ii = np.array([idx.get(k, -1) if k else -1 for k in ks]); has = ii >= 0
    n = len(ks); shape = (n, 4, 768) if layers else (n, 4, 12, 768); X = np.zeros(shape, np.float32)
    if has.any():
        a = arr[ii[has]]; X[has] = a[:, :, layers[0]:layers[1] + 1].astype(np.float32).mean(2) if layers else a.astype(np.float32)
    has &= np.isfinite(X.reshape(n, -1)).all(1); X[~has] = 0
    return X, has

# ------------------------------------------------------------------ compact stores (derived caches the references read)
def compact(name):
    """Compact store `name` (COMPACT_NAMES) as a dict of arrays with key column `md5`: the dev file, with the sealed-era file's rows appended for keys the dev file does not have.
    A missing dev file is rebuilt by refs.ensure (as before)."""
    if name not in _C:
        assert name in DEV_COMPACT, f"unknown compact store {name!r}; choose from {COMPACT_NAMES}"
        dev = DEV_COMPACT[name]; sp = sealed_root() / "compact" / name / "compact.npz"
        z = np.load(dev); D = {k: z[k] for k in z.files}; hide = _hidden()
        if hide:
            keep = np.array([str(k) not in hide for k in D["md5"]]); D = {k: v[keep] for k, v in D.items()}
        if sp.exists():
            s = np.load(sp); have = set(map(str, D["md5"])); new = np.array([str(k) not in have for k in s["md5"]])
            if new.any():
                for k in D:
                    if k in s.files: D[k] = np.concatenate([D[k], s[k][new]])
                    else: raise KeyError(f"sealed-era compact store {sp} lacks array {k}")
        _C[name] = D
    return _C[name]

def compact_index(name):
    D = compact(name); key = ("cidx", name)
    if key not in _C: _C[key] = {str(k): i for i, k in enumerate(D["md5"])}
    return _C[key]

# ------------------------------------------------------------------ Deezer context records
def _deezer_files():
    dev = sorted(glob.glob(str(ROOT / ".cache" / "shared-w6r*" / "deezer*.jsonl"))); return dev + [str(sealed_root() / "deezer" / "context.jsonl")]

def deezer_all():
    """trackId (public opaque id) -> Deezer context record, dev files first (first record wins)."""
    if "deezer" not in _C:
        out = {}
        for f in _deezer_files():
            if not os.path.exists(f): continue
            for ln in open(f):
                if ln.strip():
                    r = json.loads(ln); out.setdefault(r.get("trackId"), r)
        _C["deezer"] = out
    return _C["deezer"]

def deezer(meta, tids):
    """Deezer context record (dict; `found` False when the lookup found no match) per track id, None where no lookup was made."""
    D = deezer_all(); return [D.get(t) for t in tids]

# ------------------------------------------------------------------ coverage
def essentia_has(meta, tids):
    """Has-essentia mask from the compact store of ref_w4r1_music (dev + sealed-era rows)."""
    idx = compact_index("w4r1-what-in-the-music"); return np.array([bool(k) and k in idx for k in clip_keys(meta, tids)])

def coverage(meta, tids, kinds=("mert", "essentia", "deezer")):
    """Share of `tids` with each feature kind available (dict kind -> float)."""
    out = {}
    if len(tids) == 0: return {k: float("nan") for k in kinds}
    if "mert" in kinds: out["mert"] = float(mert(meta, tids, layers=(4, 4))[1].mean())
    if "essentia" in kinds: out["essentia"] = float(essentia_has(meta, tids).mean())
    if "deezer" in kinds: out["deezer"] = float(np.mean([r is not None and bool(r.get("found")) for r in deezer(meta, tids)]))
    return out
