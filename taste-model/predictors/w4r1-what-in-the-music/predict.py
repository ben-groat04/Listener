"""w4r1-what-in-the-music: which MUSICAL properties of the 30 s preview (essentia style/mood/instrument/voice/danceability activations, effnet embedding, 5-s time segments, MERT) separate new songs that get loved from those dropped?
Entry file for evalkit.  Inputs per song: ONLY per-clip audio-derived caches (.cache/shared/w4-essentia via compact store built by build_compact.py; MERT via the w3r2 predictor) and, in *_meta variants, track metadata.  No artist identity/history, no pool structure.
User history is used only for TRAINING TARGETS: per-song rank of plays90 within the quarter of first play (mature songs: first play < cutoff-90d).  Standardiser / PCA / ridge fitted on train-stream songs only.
Fit cache key hashes train identities; skipped when EVALKIT_NO_FIT_CACHE is set.  Candidate scores are independent of other candidates.  No audio -> train-median score.
"""
import os, sys, hashlib, importlib.util
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"
COMPACT = ROOT + ".cache/w4r1-what-in-the-music/compact.npz"
CFG = dict(feat="act", tf="logit", ncomp=0, alpha=300.0, seg=None, target="rank_plays", agg="mean", mature=90, hl=None, meta=False, learner="ridge", cols=None, k=50, temp=0.1)
_F = {}

def _store():
    if "idx" not in _F:
        if not os.path.exists(COMPACT):
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import build_compact  # noqa regenerate
        z = np.load(COMPACT); _F["idx"] = {k: i for i, k in enumerate(z["md5"])}
        for k in ("act_mean", "act_max", "emb_mean", "emb_std", "seg"): _F[k] = z[k]
    return _F

def _desc():
    """librosa descriptors (build_desc.py): md5 -> row; glob [n,10], seg [n,6,8]"""
    if "didx" not in _F:
        import glob as g
        ks, gl, sg = [], [], []
        for f in sorted(g.glob(ROOT + ".cache/w4r1-what-in-the-music/desc/shard_*.npz")):
            z = np.load(f); ks += list(z["md5"]); gl.append(z["glob"]); sg.append(z["seg"])
        _F["didx"] = {k: i for i, k in enumerate(ks)}; _F["dglob"] = np.concatenate(gl); _F["dseg"] = np.concatenate(sg)
    return _F

def _lg(a):
    a = np.clip(a.astype(np.float32), 1e-4, 1 - 1e-4); return np.log(a / (1 - a))

def _view(tids, meta, cfg):
    """float32 [n, S, D] (S = 1 for clip-level, else number of time segments) and ok mask."""
    F = _store(); u = meta.previewUrl.reindex(tids).values
    ii = np.array([F["idx"].get(hashlib.md5(x.encode()).hexdigest(), -1) if isinstance(x, str) else -1 for x in u]); ok = ii >= 0
    f = cfg["feat"]; ii2 = np.where(ok, ii, 0)
    if f in ("desc", "descmeta"):
        _desc(); jj = np.array([_F["didx"].get(hashlib.md5(x.encode()).hexdigest(), -1) if isinstance(x, str) else -1 for x in u]); okd = jj >= 0
        X = _F["dglob"][np.where(okd, jj, 0)].astype(np.float32)
        if f == "descmeta": X = np.c_[X, _meta_cols(tids, meta)]
        X = X[:, None]; return X, okd & np.isfinite(X).all((1, 2))
    if f == "meta": return _meta_cols(tids, meta)[:, None].astype(np.float32), np.ones(len(tids), bool)
    if f == "seg": X = F["seg"][ii2].astype(np.float32); X = X[:, list(cfg["seg"])] if cfg["seg"] is not None else X
    elif f == "act": X = F["act_mean"][ii2].astype(np.float32)[:, None]
    elif f == "actmax": X = F["act_max"][ii2].astype(np.float32)[:, None]
    elif f == "emb": X = F["emb_mean"][ii2].astype(np.float32)[:, None]
    elif f == "embstd": X = np.concatenate([F["emb_mean"][ii2], F["emb_std"][ii2]], 1).astype(np.float32)[:, None]
    if f in ("seg", "act", "actmax") and cfg["tf"] == "logit": X = _lg(X)
    if cfg["cols"] is not None: X = X[:, :, cfg["cols"]]
    ok &= np.isfinite(X).all((1, 2)) | (f == "seg")
    if f == "seg": X = np.where(np.isfinite(X), X, np.nanmean(np.where(np.isfinite(X), X, np.nan), 1, keepdims=True)); X = np.nan_to_num(X, nan=0.0)
    return X, ok

def _meta_cols(tids, meta):
    m = meta.reindex(tids)
    return np.c_[np.log1p(m.durationMs.fillna(0).values / 1000.0), m.explicit.astype(float).fillna(0).values, m.popularity.fillna(0).values / 100.0, (m.popularity.fillna(0).values == 0).astype(float)]

def _design(res, X, tids, meta, cfg):
    n, S, D = X.shape; Z = ((X - res["mu"]) / res["sd"]).reshape(n * S, D)
    if res["pca"] is not None: Z = res["pca"].transform(Z)
    if cfg["meta"]: Z = np.c_[Z, np.repeat((_meta_cols(tids, meta) - res["mm"]) / res["ms"], S, 0)]
    return Z

class KNN:
    """similarity-weighted mean target of the k nearest train songs (cosine on the PCA-whitened design)"""
    def __init__(self, P, y, w, k, temp):
        self.P = (P / (np.linalg.norm(P, axis=1, keepdims=True) + 1e-9)).astype(np.float32); self.y = y; self.w = w; self.k = k; self.t = temp
    def predict(self, Q):
        Q = (Q / (np.linalg.norm(Q, axis=1, keepdims=True) + 1e-9)).astype(np.float32); out = np.zeros(len(Q))
        for a in range(0, len(Q), 2000):
            S = Q[a:a + 2000] @ self.P.T; ix = np.argpartition(-S, self.k, axis=1)[:, :self.k]; ss = np.take_along_axis(S, ix, 1)
            ww = np.exp((ss - ss.max(1, keepdims=True)) / self.t) * self.w[ix]; out[a:a + 2000] = (ww * self.y[ix]).sum(1) / ww.sum(1)
        return out

_CACHE = {}
def _fit(train, meta, cutoff, cfg):
    key = (str(cutoff), len(train), int(train.t.values.astype("int64").sum() % (1 << 60)), int(pd.util.hash_pandas_object(train[["trackId", "song", "artist"]].astype(str), index=False).sum() % (1 << 60)), repr(sorted(cfg.items(), key=lambda kv: kv[0])))
    use = not os.environ.get("EVALKIT_NO_FIT_CACHE")
    if use and key in _CACHE: return _CACHE[key]
    from sklearn.decomposition import PCA
    from sklearn.linear_model import Ridge, LogisticRegression
    from threadpoolctl import threadpool_limits
    from evalkit.data import song_table
    st = song_table(train).reset_index(); st = st[st.trackId.isin(meta.index)].reset_index(drop=True)
    X, ok = _view(st.trackId.values, meta, cfg); S = X.shape[1]
    with threadpool_limits(2):
        Xo = X[ok]; mu = Xo.mean((0, 1)); sd = Xo.std((0, 1)) + 1e-6
        pca = PCA(cfg["ncomp"], whiten=True, random_state=0).fit(((Xo - mu) / sd).reshape(-1, X.shape[2])) if cfg["ncomp"] else None
        res = dict(mu=mu, sd=sd, pca=pca, lr=None)
        if cfg["meta"]:
            M = _meta_cols(st.trackId.values[ok], meta); res["mm"], res["ms"] = M.mean(0), M.std(0) + 1e-6
        mat = ((st["first"] < cutoff - pd.Timedelta(days=cfg["mature"])).values) & ok
        qa = st["first"].dt.to_period("Q").astype(str).values
        if cfg["target"] == "love": yr = st.love.values[mat].astype(float)
        else:
            col = {"rank_plays": st.plays90, "rank_share": st.share90}[cfg["target"]]
            yr = pd.Series(col.values[mat]).groupby(qa[mat]).rank(pct=True).values
        w = np.ones(mat.sum())
        if cfg["hl"]: w *= 0.5 ** ((cutoff - st["first"][mat]).dt.days.values / cfg["hl"])
        if mat.sum() > 20:
            P = _design(res, X[mat], st.trackId.values[mat], meta, cfg)
            if cfg["target"] == "love":
                if 0 < yr.sum() < len(yr): res["lr"] = LogisticRegression(C=1.0 / cfg["alpha"], max_iter=300).fit(P, np.repeat(yr, S).astype(int), sample_weight=np.repeat(w, S)); res["lr"].predict = res["lr"].decision_function
            else:
                if cfg["learner"] == "gbm":
                    from sklearn.ensemble import HistGradientBoostingRegressor
                    res["lr"] = HistGradientBoostingRegressor(max_iter=80, learning_rate=0.05, max_depth=3, min_samples_leaf=30, l2_regularization=5.0, random_state=0).fit(P, np.repeat(yr, S), sample_weight=np.repeat(w, S))
                elif cfg["learner"] == "knn": res["lr"] = KNN(P, np.repeat(yr, S), np.repeat(w, S), cfg["k"], cfg["temp"])
                else: res["lr"] = Ridge(alpha=cfg["alpha"]).fit(P, np.repeat(yr, S), sample_weight=np.repeat(w, S))
        sc = _raw(res, X[ok], st.trackId.values[ok], meta, cfg)
        res["tm"], res["ts"], res["neutral"] = float(sc.mean()), float(sc.std() + 1e-9), float(np.median(sc))
    if use: _CACHE[key] = res
    return res

def _raw(res, X, tids, meta, cfg):
    n, S, _ = X.shape
    if res["lr"] is None: return np.zeros(n)
    d = res["lr"].predict(_design(res, X, tids, meta, cfg)).reshape(n, S)
    return d.max(1) if cfg["agg"] == "max" else d.mean(1)

def make_ens(cfgs, wts=None):
    cfgs = [{**CFG, **c} for c in cfgs]; wts = wts or [1] * len(cfgs)
    def predict(train, cands, meta, cutoff):
        out = np.zeros(len(cands))
        for cfg, wt in zip(cfgs, wts):
            res = _fit(train, meta, cutoff, cfg); X, ok = _view(cands.trackId.values, meta, cfg); s = np.full(len(cands), res["neutral"])
            if ok.any(): s[ok] = _raw(res, X[ok], cands.trackId.values[ok], meta, cfg)
            out += wt * (s - res["tm"]) / res["ts"]
        return out / sum(wts)
    return predict

_M = {}
def mert_final():
    """Workflow 3 audio_final (MERT) loaded from its own file, used as ensemble member."""
    if "f" not in _M:
        sp = importlib.util.spec_from_file_location("w3r2_audio", ROOT + "predictors/w3r2-audio-taste/predict.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); _M["f"] = m.PREDICTORS["audio_final"]
    return _M["f"]

def blend(cfgs, wm=1.0, wts=None):
    """standardised mean of essentia members and MERT audio_final (weight wm relative to total essentia weight 1)"""
    e = make_ens(cfgs, wts)
    def predict(train, cands, meta, cutoff):
        a = e(train, cands, meta, cutoff); b = mert_final()(train, cands, meta, cutoff)
        return a + wm * b
    return predict

G = dict(genre=list(range(0, 400)), mood=list(range(400, 456)), inst=list(range(456, 496)), mtg=list(range(496, 583)), misc=list(range(583, 605)))
DUR = dict(feat="meta", learner="gbm")
A = dict(alpha=10000.0)
# ---- pre-declared final model and ablations (declared in the report before any --late run) ----
DUR = dict(feat="meta", learner="gbm")                    # duration/explicit/popularity-missing GBM on rank_plays target (track metadata, no artist)
A = dict(alpha=10000.0)                                   # essentia head activations (clip mean, logit), standardised, ridge alpha 1e4, rank_plays target
SL = dict(feat="seg", seg=(3, 4, 5), alpha=10000.0)       # same heads, mean activation of 5-s segments 3-5 (15-30 s of the clip), one training row per segment, score = mean over the segments
PREDICTORS_FINAL = None
PREDICTORS = {
    "d_ridge_a100": make_ens([dict(feat="desc", tf="none", alpha=100.0)]), "d_ridge_a1000": make_ens([dict(feat="desc", tf="none", alpha=1000.0)]),
    "d_gbm": make_ens([dict(feat="desc", tf="none", learner="gbm")]),
    "dm_gbm": make_ens([dict(feat="descmeta", tf="none", learner="gbm")]),
    "b_final_dm": blend([A, SL, dict(feat="descmeta", tf="none", learner="gbm")], 1.0, [1, 1, 1.5]),
    "b_final_d": blend([A, SL, DUR, dict(feat="desc", tf="none", alpha=1000.0)], 1.0, [1, 1, 1.5, 0.5]),
    "final_content": blend([A, SL, DUR], 1.0, [1, 1, 1.5]),
}
