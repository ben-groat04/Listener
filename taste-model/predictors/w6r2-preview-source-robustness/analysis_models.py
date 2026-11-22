"""w6r2-preview-source-robustness ANALYSIS models (not a final file): the round-1 avg21 recipe (trained on dev clips) scored from alternative-source clips, with label-free source corrections
fitted only on clip pairs of TRAIN songs (first played before the fold cutoff = tried songs of earlier folds), and diagnostics. Run:
  python3 -W ignore -m evalkit.run --fast --dump-scores OUT.pkl predictors/w6r2-preview-source-robustness/analysis_models.py"""
import os, sys, glob, hashlib, importlib.util
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"; R1 = ROOT + "predictors/w6r1-content-ranker-final/"
sys.path.insert(0, ROOT); sys.path.insert(0, R1)
_s = importlib.util.spec_from_file_location("w6r1_core2", R1 + "predict.py"); core = importlib.util.module_from_spec(_s); _s.loader.exec_module(core)
G = core.G; FEATURES = ("mert",)
CTX = {}; _ALT = {}; _CORR = {}
SRC = {"dz": (ROOT + ".cache/shared-w6r1/p2_clips.csv", ROOT + ".cache/shared-w6r1/mert_deezer"), "it": (ROOT + ".cache/shared-w6r2/itunes_clips.csv", ROOT + ".cache/shared-w6r2/mert_itunes")}

def _alt(src):
    if src not in _ALT:
        f, d = SRC[src]; c = pd.read_csv(f)
        c = c[c.ok == True]
        if src == "dz": c = c[c.mert_ok == True]
        else: c = c[c.same_url == 0] if "same_url" in c else c   # iTunes clip identical to the dev clip: not a second source
        tid = {str(int(t)): m for t, m in zip(c.trackId, c.md5)}
        keys, arrs = [], []
        for fn in sorted(glob.glob(d + "/shard_*.npz")):
            z = np.load(fn); keys += [str(x) for x in z["md5"]]; arrs.append(z["feat"][:, :, 4:9].astype(np.float32).mean(2))
        _ALT[src] = dict(tid=tid, idx={k: i for i, k in enumerate(keys)}, arr=np.concatenate(arrs), meta=c.set_index(c.trackId.astype(int).astype(str)))
    return _ALT[src]

def alt_raw(tids, src):
    S = _alt(src); n = len(tids); X = np.zeros((n, 4, 768), np.float32)
    ii = np.array([S["idx"].get(S["tid"].get(str(int(t)), ""), -1) for t in tids]); has = ii >= 0
    if has.any(): X[has] = S["arr"][ii[has]]
    has &= np.isfinite(X.reshape(n, -1)).all(1); X[~has] = 0
    return X, has

def _sqrtm(C, inv):
    w, v = np.linalg.eigh(C); w = np.maximum(w, 1e-8); return (v * (w ** (-.5 if inv else .5))) @ v.T

def _corr(src, kind):
    """correction parameters for source `src`, fitted on the pairs of TRAIN songs of the current prep (CTX['P']); None -> identity"""
    P = CTX["P"]; key = (P["key"], src, kind)
    if key in _CORR: return _CORR[key]
    Xa, ha = alt_raw(P["tids"], src); hd = P["has"]; m = ha & hd; res = None
    if m.sum() >= 30:
        a = Xa[m].mean(1); d = P["X"][m].mean(1); ma, md = a.mean(0), d.mean(0); sa, sd = a.std(0) + 1e-6, d.std(0) + 1e-6
        if kind == "mu": res = (lambda x: x - (ma - md))
        elif kind == "std": res = (lambda x: (x - ma) * (sd / sa) + md)
        elif kind == "coral":
            lam = .3; Ca = np.cov(a.T); Cd = np.cov(d.T); Ca = (1 - lam) * Ca + lam * np.diag(np.diag(Ca)); Cd = (1 - lam) * Cd + lam * np.diag(np.diag(Cd))
            T = _sqrtm(Ca, True) @ _sqrtm(Cd, False); res = (lambda x: (x - ma) @ T + md)
        elif kind == "ridge":
            Za = (a - ma) / sa; Zd = (d - md) / sd; n = len(Za); B = np.linalg.solve(Za.T @ Za + n * np.eye(768), Za.T @ Zd); res = (lambda x: ((x - ma) / sa) @ B * sd + md)
    _CORR[key] = (res, int(m.sum())); return _CORR[key]

_raw0 = core._raw
def _raw(tids, meta, src="dev"):
    if src == "dev": return _raw0(tids, meta, "dev")
    s, _, kind = src.partition("_"); X, has = alt_raw(tids, s)
    if kind:
        f, npair = _corr(s, kind)
        if f is not None and has.any(): X = X.copy(); X[has] = f(X[has].reshape(-1, 768)).reshape(-1, 4, 768).astype(np.float32)
    return X, has
core._raw = _raw

A21 = G.ALL21
def _parts(src):
    f = core._avg(A21, src, "mean")
    def run(train, cands, meta, cutoff):
        CTX["P"] = core._prep(train, meta, cutoff); return f(train, cands, meta, cutoff)
    return run

def _hid(t): return int(hashlib.md5(str(int(t)).encode()).hexdigest(), 16)

def model_src(src, fallback=False):
    f = _parts(src)
    def predict(train, cands, meta, cutoff):
        s, h = f(train, cands, meta, cutoff); return s    # songs without that clip: 0 (analysis restricts to songs with both clips)
    return predict

def mix(kind):
    fd = _parts("dev"); fz = _parts("dz" + kind); fi = _parts("it" + kind)
    def predict(train, cands, meta, cutoff):
        t = cands.trackId.values; (a, ha), (b, hb), (c, hc) = fd(train, cands, meta, cutoff), fz(train, cands, meta, cutoff), fi(train, cands, meta, cutoff)
        H = np.c_[ha, hb, hc]; S = np.c_[a, b, c]; out = np.zeros(len(t))
        for i in range(len(t)):
            av = np.flatnonzero(H[i])
            if len(av): out[i] = S[i, av[_hid(t[i]) % len(av)]]
        return out
    return predict

def diag(field):
    def predict(train, cands, meta, cutoff):
        t = cands.trackId.values; out = np.zeros(len(t))
        if field == "devsrc":   # 1 = the dev clip's stored URL is iTunes (fallback fill), 0 = other stored URL, -1 = no clip
            u = meta.reindex(t)["previewUrl"].values; return np.array([(-1.0 if not isinstance(x, str) or not x else (1.0 if "itunes.apple.com" in x or "mzstatic" in x else 0.0)) for x in u])
        if field == "hasdev": return core._raw(t, meta, "dev")[1].astype(float)
        if field == "hasdz": return alt_raw(t, "dz")[1].astype(float)
        if field == "hasit": return alt_raw(t, "it")[1].astype(float)
        src, f = field.split("_"); S = _alt(src); m = S["meta"]
        col = {"off": "align_offset_s", "aln": "align_score", "same": "same_excerpt"}[f]
        v = m[col].reindex([str(int(x)) for x in t]).values.astype(float); return np.nan_to_num(v, nan=-9.0)
    return predict

PREDICTORS = {"a_dev": model_src("dev")}
for s in ("dz", "it"):
    for k in ("", "_mu", "_std", "_coral", "_ridge"): PREDICTORS["a_" + s + k] = model_src(s + k)
PREDICTORS.update({"a_mix_raw": mix(""), "a_mix_mu": mix("_mu"), "a_mix_std": mix("_std")})
for f in ("devsrc", "hasdev", "hasdz", "hasit", "dz_off", "dz_aln", "dz_same", "it_off", "it_aln", "it_same"): PREDICTORS["diag_" + f] = diag(f)
if os.environ.get("W6R2_ONLY"): PREDICTORS = {k: v for k, v in PREDICTORS.items() if k in os.environ["W6R2_ONLY"].split(",")}
