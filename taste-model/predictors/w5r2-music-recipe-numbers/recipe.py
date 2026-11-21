"""w5r2 recipe engine: own copy of the W4 music-content recipe (ref_w4r1_music = final_content) with every number a parameter.
final = (zA + zS + 1.5 zD)/3.5 + wm * (zE + zW + zL)/3   (z = (raw - train mean)/train sd; missing audio -> fill)
 A  essentia head activations (clip mean) logit(clip eps) -> standardise -> Ridge(alphaA) on rank_plays target
 S  same heads, mean per 5-s segment, segments `seg`, one training row per segment, Ridge(alphaS)
 D  duration/explicit/popularity HistGB
 E,W,L: W3 MERT audio_final members (fixed; only the blend weight varies).
Member outputs are cached per (cutoff, train hash, cand hash, member key) in-process and on disk (skipped with EVALKIT_NO_FIT_CACHE)."""
import os, sys, hashlib, pickle
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"
COMPACT = ROOT + ".cache/w4r1-what-in-the-music/compact.npz"
SH = ROOT + ".cache/shared-w5r1/"
CACHE = ROOT + ".cache/w5r2-music-recipe-numbers/"
_F = {}
PERM = None   # null-calibration only: seed; training target is randomly permuted (same permutation for all members/variants of one cutoff and seed)
DEFAULT = dict(eps=1e-4, alphaA=1e4, alphaS=1e4, seg=(3, 4, 5), gbm=(80, 0.05, 3, 30, 5.0), w=(1.0, 1.0, 1.5), wm=1.0, fill="median", mfill=None)

def _md5(u): return hashlib.md5(u.encode()).hexdigest() if isinstance(u, str) else None

def _ess():
    if "act" not in _F:
        z = np.load(COMPACT); _F["eidx"] = {k: i for i, k in enumerate(z["md5"])}; _F["act"] = z["act_mean"]; _F["seg"] = z["seg"]
    return _F

def _mert(layers):
    key = f"mert{layers[0]}_{layers[1]}"
    if key not in _F:
        md = np.load(SH + "mert_md5.npy"); _F["midx"] = {k: i for i, k in enumerate(md)}
        fn = CACHE + f"mert_L{layers[0]}-{layers[1]}.npy"
        if not os.path.exists(fn):
            full = np.load(SH + "mert_full.npy", mmap_mode="r"); out = np.zeros((len(md), 4, 768), np.float16)
            for a in range(0, len(md), 500): out[a:a + 500] = np.asarray(full[a:a + 500, :, layers[0]:layers[1] + 1], np.float32).mean(2).astype(np.float16)
            np.save(fn + ".tmp.npy", out); os.replace(fn + ".tmp.npy", fn)
        _F[key] = np.load(fn)
    return _F[key]

def _lg(a, eps):
    a = np.clip(a.astype(np.float32), eps, 1 - eps); return np.log(a / (1 - a))

def _meta_cols(tids, meta):
    m = meta.reindex(tids)
    return np.c_[np.log1p(m.durationMs.fillna(0).values / 1000.0), m.explicit.astype(float).fillna(0).values, m.popularity.fillna(0).values / 100.0, (m.popularity.fillna(0).values == 0).astype(float)]

def _eidx(tids, meta):
    F = _ess(); u = meta.previewUrl.reindex(tids).values
    ii = np.array([F["eidx"].get(_md5(x), -1) if isinstance(x, str) else -1 for x in u]); return ii

def _midx(tids, meta):
    _mert((4, 8)); u = meta.previewUrl.reindex(tids).values
    return np.array([_F["midx"].get(_md5(x), -1) if isinstance(x, str) else -1 for x in u])

def _view(tids, meta, mk):
    """float32 [n,S,D], ok mask for member key mk = (kind, ...)."""
    kind = mk[0]
    if kind == "D": return _meta_cols(tids, meta)[:, None].astype(np.float32), np.ones(len(tids), bool)
    if kind in ("A", "S"):
        F = _ess(); ii = _eidx(tids, meta); ok = ii >= 0; i2 = np.where(ok, ii, 0); eps = mk[1]
        if kind == "A":
            X = _lg(F["act"][i2], eps)[:, None]; ok &= np.isfinite(X).all((1, 2)); return X, ok
        seg = mk[3]; X = _lg(F["seg"][i2][:, list(seg)], eps)
        X = np.where(np.isfinite(X), X, np.nanmean(np.where(np.isfinite(X), X, np.nan), 1, keepdims=True)); X = np.nan_to_num(X, nan=0.0); return X, ok
    ii = _midx(tids, meta); ok = ii >= 0; i2 = np.where(ok, ii, 0); L = mk[1]
    X = _mert(L)[i2].astype(np.float32); X[~ok] = 0; ok &= np.isfinite(X).all((1, 2)); return X, ok

# member keys. A:("A",eps,alpha) S:("S",eps,alpha,seg) D:("D",gbm) mert: ("M", layers, mode, ncomp, alpha)
MERT_KEYS = [("M", (4, 8), "local", 64, 1200.0), ("M", (4, 8), "whole", 32, 150.0), ("M", (3, 7), "local", 64, 1200.0)]

def _train_hash(train, cutoff, cands):
    return (str(cutoff), len(train), int(train.t.values.astype("int64").sum() % (1 << 60)),
            int(pd.util.hash_pandas_object(train[["trackId", "song", "artist"]].astype(str), index=False).sum() % (1 << 60)),
            int(pd.util.hash_pandas_object(cands[["trackId"]].astype(str), index=False).sum() % (1 << 60)), len(cands))

_ST = {}
def _fit_score(train, cands, meta, cutoff, mk, th):
    from sklearn.decomposition import PCA
    from sklearn.linear_model import Ridge
    from threadpoolctl import threadpool_limits
    from evalkit.data import song_table
    st = _ST.get(th)
    if st is None:
        st = song_table(train).reset_index(); st = st[st.trackId.isin(meta.index)].reset_index(drop=True)
        if len(_ST) > 60: _ST.clear()
        _ST[th] = st
    kind = mk[0]; X, ok = _view(st.trackId.values, meta, mk); S = X.shape[1]
    mat = ((st["first"] < cutoff - pd.Timedelta(days=90)).values) & ok
    qa = st["first"].dt.to_period("Q").astype(str).values
    yr = pd.Series(st.plays90.values[mat]).groupby(qa[mat]).rank(pct=True).values
    if PERM is not None: yr = np.random.default_rng([PERM, int(pd.Timestamp(cutoff).value // 86400000000000), len(yr)]).permutation(yr)
    Xc, okc = _view(cands.trackId.values, meta, mk)
    with threadpool_limits(2):
        Xo = X[ok]; mu = Xo.mean((0, 1)); sd = Xo.std((0, 1)) + 1e-6
        pca = None; mode = "local" if kind in ("A", "S", "D") else mk[2]
        if kind == "M":
            ncomp = mk[3]; Z = (Xo - mu) / sd
            pca = PCA(ncomp, whiten=True, random_state=0).fit(Z.reshape(-1, Z.shape[-1]) if mode == "local" else Z.mean(1))
        def design(X_):
            Z = (X_ - mu) / sd; n, S_, D = Z.shape
            if kind != "M": return Z.reshape(n * S_, D)
            if mode == "local": return pca.transform(Z.reshape(-1, D))
            return pca.transform(Z.mean(1))
        rep = S if (kind in ("A", "S") or (kind == "M" and mode == "local")) else 1
        if kind == "M" and mode == "local": rep = 4
        lr = None
        if mat.sum() > 20:
            P = design(X[mat]); yy = np.repeat(yr, rep)
            if kind == "D":
                from sklearn.ensemble import HistGradientBoostingRegressor
                it, lrate, md, ml, l2 = mk[1]
                lr = HistGradientBoostingRegressor(max_iter=it, learning_rate=lrate, max_depth=md, min_samples_leaf=ml, l2_regularization=l2, random_state=0).fit(P, yy)
            else:
                alpha = mk[2] if kind in ("A", "S") else mk[4]
                if kind == "A": alpha = mk[2]
                lr = Ridge(alpha=alpha).fit(P, yy)
        def raw(X_):
            n = len(X_)
            if lr is None: return np.zeros(n)
            d = lr.predict(design(X_)); return d.reshape(n, rep).mean(1) if rep > 1 else d
        sc = raw(X[ok]); tm, ts = float(sc.mean()), float(sc.std() + 1e-9)
        out = np.full(len(cands), np.nan)
        if okc.any(): out[okc] = raw(Xc[okc])
    return dict(raw=out, ok=okc, tm=tm, ts=ts, neutral=float(np.median(sc)), lo=float(np.percentile(sc, 1)), hi=float(np.percentile(sc, 99)))

_C = {}
def member(train, cands, meta, cutoff, mk, th=None):
    th = th or _train_hash(train, cutoff, cands); key = (th, repr(mk), PERM)
    if key in _C: return _C[key]
    use = not os.environ.get("EVALKIT_NO_FIT_CACHE") and PERM is None
    fn = CACHE + "m_" + hashlib.md5(repr(key).encode()).hexdigest() + ".pkl"
    if use and os.path.exists(fn):
        try:
            r = pickle.load(open(fn, "rb")); _C[key] = r; return r
        except Exception: pass
    r = _fit_score(train, cands, meta, cutoff, mk, th[:4]); _C[key] = r
    if use:
        try: pickle.dump(r, open(fn + f".{os.getpid()}.tmp", "wb")); os.replace(fn + f".{os.getpid()}.tmp", fn)
        except Exception: pass
    if len(_C) > 400: _C.clear(); _C[key] = r
    return r

def zfill(m, fill):
    """z-scored member score with the missing-audio fill: median (recipe), mean(0), low, high."""
    s = m["raw"].copy(); ok = m["ok"]
    v = {"median": m["neutral"], "mean": m["tm"], "low": m["lo"] - 1, "high": m["hi"] + 1}[fill]
    s[~ok] = v; return (s - m["tm"]) / m["ts"]

def keys_for(P):
    return dict(A=("A", P["eps"], P["alphaA"]), S=("S", P["eps"], P["alphaS"], tuple(P["seg"])), D=("D", tuple(P["gbm"])))

def score(train, cands, meta, cutoff, P=None, th=None):
    P = {**DEFAULT, **(P or {})}; th = th or _train_hash(train, cutoff, cands); K = keys_for(P)
    mf = P["mfill"] or P["fill"]
    zA = zfill(member(train, cands, meta, cutoff, K["A"], th), P["fill"]); zS = zfill(member(train, cands, meta, cutoff, K["S"], th), P["fill"])
    zD = zfill(member(train, cands, meta, cutoff, K["D"], th), "median")
    w = P["w"]; a = (w[0] * zA + w[1] * zS + w[2] * zD) / sum(w)
    zM = sum(zfill(member(train, cands, meta, cutoff, k, th), mf) for k in MERT_KEYS) / 3.0
    return a + P["wm"] * zM
