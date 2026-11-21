"""w5r1-tune-content-numbers core: re-implementation of the W3 audio_final MERT ridge recipe on the consolidated store
(.cache/shared-w5r1/mert_full.npy, float16 [N, window, layer, 768]) with every representation/learner number as a config field.
Member cfg: lo,hi (inclusive 0-based layer slice, mean over layers), mode whole|local, agg (local: mean|max|top2), ncomp (None = no PCA), whiten, alpha,
wins (window subset), pool (whole mode: mean|max over windows). Target fixed at the base recipe (rank_plays within first-play quarter, maturity 90 d).
Missing audio policy is applied at the ensemble level (neutral|min|max|zero)."""
import hashlib, os
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"; SH = ROOT + ".cache/shared-w5r1/"
_S = {}; _ST = {}; _FIT = {}; _SC = {}
PERM = int(os.environ.get("W5_PERMSEED", "-1"))   # >=0: random-label refit calibration (permute the training target among mature songs)

def store():
    if "full" not in _S:
        md5 = np.load(SH + "mert_md5.npy"); _S["idx"] = {str(k): i for i, k in enumerate(md5)}
        _S["full"] = np.load(SH + "mert_full.npy", mmap_mode="r")
    return _S

def md5s(tids, meta):
    u = meta.previewUrl.reindex(tids).values
    return [hashlib.md5(x.encode()).hexdigest() if isinstance(x, str) else None for x in u]

def feats(tids, meta, cfg):
    """X [n, W, 768] float32, has mask"""
    S = store(); md = md5s(tids, meta); ii = np.array([S["idx"].get(m, -1) if m else -1 for m in md]); has = ii >= 0
    W = len(cfg["wins"]); X = np.zeros((len(tids), W, 768), np.float32)
    if has.any():
        j = ii[has]; o = np.argsort(j); js = j[o]
        a = np.asarray(S["full"][js][:, list(cfg["wins"]), cfg["lo"]:cfg["hi"] + 1], np.float32).mean(2)
        tmp = np.empty_like(a); tmp[o] = a; X[has] = tmp
    has &= np.isfinite(X).all((1, 2)); return X, has

def train_key(train, cutoff):
    return (str(cutoff), len(train), int(train.t.values.astype("int64").sum() % (1 << 60)),
            int(pd.util.hash_pandas_object(train[["trackId", "song"]].astype(str), index=False).sum() % (1 << 60)))

def songs(train, meta, key):
    if key not in _ST:
        from evalkit.data import song_table
        st = song_table(train).reset_index(); st = st[st.trackId.isin(meta.index)].reset_index(drop=True); _ST[key] = st
    return _ST[key]

def mkey(cfg): return repr(sorted(cfg.items()))

def _pool(Z, cfg, local):
    return Z.reshape(-1, Z.shape[-1]) if local else (Z.max(1) if cfg["pool"] == "max" else Z.mean(1))

def member(train, cands, meta, cutoff, cfg):
    """standardised-scale raw scores of `cands` plus (neutral, lo, hi) in that scale, ok mask. Cached."""
    key = train_key(train, cutoff); ck = (key, mkey(cfg), len(cands), int(pd.util.hash_pandas_object(cands[["trackId"]].astype(str), index=False).sum() % (1 << 60)), PERM)
    if ck in _SC: return _SC[ck]   # in-process only; key holds train identity hash + perm seed
    from sklearn.decomposition import PCA
    from sklearn.linear_model import Ridge
    from threadpoolctl import threadpool_limits
    st = songs(train, meta, key); X, ok = feats(st.trackId.values, meta, cfg); local = cfg["mode"] == "local"
    with threadpool_limits(2):
        Xo = X[ok]; mu = Xo.mean((0, 1)); sd = Xo.std((0, 1)) + 1e-6
        pca = PCA(min(cfg["ncomp"], _pool((Xo - mu) / sd, cfg, local).shape[0] - 1, 768), whiten=cfg["whiten"], random_state=0).fit(_pool((Xo - mu) / sd, cfg, local)) if cfg["ncomp"] else None
        def design(Xb):
            Z = (Xb - mu) / sd; P = _pool(Z, cfg, local) if local else _pool(Z, cfg, False)
            return pca.transform(P) if pca is not None else P
        mat = ((st["first"] < cutoff - pd.Timedelta(days=90)).values) & ok
        qa = st["first"].dt.to_period("Q").astype(str).values
        yr = pd.Series(st.plays90.values[mat]).groupby(qa[mat]).rank(pct=True).values
        if PERM >= 0: yr = np.random.default_rng(PERM + 7919 * len(yr)).permutation(yr)
        r = None; W = len(cfg["wins"])
        if mat.sum() > 20: r = Ridge(alpha=cfg["alpha"]).fit(design(X[mat]), np.repeat(yr, W) if local else yr)
        def raw(Xb):
            if r is None: return np.zeros(len(Xb))
            d = r.predict(design(Xb))
            if not local: return d
            d = d.reshape(len(Xb), W); a = cfg["agg"]
            return d.mean(1) if a == "mean" else d.max(1) if a == "max" else np.sort(d, 1)[:, -2:].mean(1) if a == "top2" else d.mean(1) + d.std(1)
        sc = raw(Xo); tm, ts = float(sc.mean()), float(sc.std() + 1e-9)
        out = dict(tm=tm, ts=ts, neutral=float(np.median(sc)), lo=float(np.percentile(sc, 1)), hi=float(np.percentile(sc, 99)))
        Xc, okc = feats(cands.trackId.values, meta, cfg); s = np.zeros(len(cands))
        if okc.any(): s[okc] = raw(Xc[okc])
    out = (s, okc, out); _SC[ck] = out; return out

def combine(parts, wts, miss):
    """parts: list of (s, ok, stats). Standardised weighted mean, missing-audio policy per member (base recipe: train-median neutral)."""
    n = len(parts[0][0]); tot = np.zeros(n)
    for (s, ok, st), w in zip(parts, wts):
        s = s.copy()
        if miss == "neutral": s[~ok] = st["neutral"]
        elif miss == "min": s[~ok] = st["lo"] - 1
        elif miss == "max": s[~ok] = st["hi"] + 1
        elif miss == "mean": s[~ok] = st["tm"]
        tot += w * (s - st["tm"]) / st["ts"]
    return tot / sum(wts)

BASE = dict(lo=4, hi=8, mode="local", agg="mean", ncomp=64, whiten=True, alpha=1200.0, wins=(0, 1, 2, 3), pool="mean")
E = dict(BASE)
W32 = dict(BASE, mode="whole", ncomp=32, alpha=150.0)
L37 = dict(BASE, lo=3, hi=7)
FINAL = [E, W32, L37]

def ens(members, wts=None, miss="neutral"):
    members = [{**BASE, **m} for m in members]; wts = wts or [1] * len(members)
    def predict(train, cands, meta, cutoff):
        return combine([member(train, cands, meta, cutoff, m) for m in members], wts, miss)
    return predict
