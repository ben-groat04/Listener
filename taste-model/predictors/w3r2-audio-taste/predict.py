"""w3r2-audio-taste: how much does the MUSIC ITSELF (preview audio) predict which newly tried songs get loved?  Harness entry file.
Usage (from /home/user/Listener/taste-model):  python3 -W ignore -m evalkit.run --fast predictors/w3r2-audio-taste/predict.py
Inputs per song: ONLY cached per-clip audio embeddings (MERT-v1-95M 4 windows x 12 layers; CLAP middle-10s) -- no artist identity/history, no pool structure.
Optional separate metadata variant (names ending _meta): + duration, explicit, popularity, popularity-missing.
User history is used only for training targets (love label, plays90 / share90 rank within the quarter of first play) and weights of train songs
whose 90-day label horizon is complete before the cutoff. Standardiser, PCA, ridge/logistic: fitted on train-stream songs only. Score of a candidate
depends only on its own clip + the fitted model (candidate independent). No audio -> train-median neutral score.
Config in CFG; variants in PREDICTORS (see bottom).
"""
import glob, hashlib
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"
CFG = dict(blocks=(("mert", 4, 8),), ncomp=64, mode="whole", agg="mean", target="love", C=0.05, alpha=300.0, hl=None, window=None, mature=90, meta=False, miss="neutral", pca=True, learner="lin", adem=0.0)
_F = {}

def _store():
    if "mert" not in _F:
        import sys; sys.path.insert(0, ROOT[:-1]); from evalkit import features   # v5.3: dev shards, then the sealed-era shards (evalkit.features.mert_full)
        _F["mert"] = features.mert_full()
        z = np.load(ROOT + ".cache/shared/w3r1-clap/emb.npz"); _F["clap"] = ({k: i for i, k in enumerate(z["k"])}, z["v"])
    return _F

def _blocks(tids, meta, cfg):
    """list of [n, W, D] float32 blocks, ok mask (True = every block available)."""
    F = _store()
    from evalkit import features
    md = features.clip_keys(meta, tids)   # md5(previewUrl) as before; md5("spotify:"+id) only for rows without a previewUrl (sealed era)
    ok = np.ones(len(tids), bool); out = []
    for b in cfg["blocks"]:
        idx, arr = F[b[0]]; ii = np.array([idx.get(m, -1) if m else -1 for m in md]); has = ii >= 0
        if b[0] == "mert":
            X = np.zeros((len(tids), 4, 768), np.float32)
            if has.any(): X[has] = arr[ii[has]][:, :, b[1]:b[2] + 1].astype(np.float32).mean(2)
        else:
            X = np.zeros((len(tids), 1, 768), np.float32)
            if has.any(): X[has] = arr[ii[has]].astype(np.float32)[:, None]
        has &= np.isfinite(X).all((1, 2)); ok &= has; out.append(X)
    return out, ok

def _meta_cols(tids, meta):
    m = meta.reindex(tids)
    return np.c_[np.log1p(m.durationMs.fillna(0).values / 1000.0), m.explicit.astype(float).fillna(0).values, m.popularity.fillna(0).values / 100.0, (m.popularity.fillna(0).values == 0).astype(float)]

def _design(res, blocks, tids, meta, cfg, local):
    """standardise -> PCA(whiten) per block -> concat. local: window-level rows [n*W, d] else song-level [n, d]."""
    parts = []
    for b, X, (mu, sd, pca) in zip(cfg["blocks"], blocks, res["tf"]):
        Z = (X - mu) / sd
        if local and b[0] == "mert": P = pca.transform(Z.reshape(-1, Z.shape[-1])) if pca is not None else Z.reshape(-1, Z.shape[-1])
        else:
            Zs = Z.mean(1); P = pca.transform(Zs) if pca is not None else Zs
            if local: P = np.repeat(P, 4, 0)
        parts.append(P)
    P = np.concatenate(parts, 1)
    if cfg["meta"]:
        M = (_meta_cols(tids, meta) - res["mm"]) / res["ms"]; P = np.c_[P, np.repeat(M, 4, 0) if local else M]
    return P

_CACHE = {}
def _fit(train, meta, cutoff, cfg):
    key = (str(cutoff), len(train), int(train.t.values.astype("int64").sum() % (1 << 60)), int(pd.util.hash_pandas_object(train[["trackId", "song"]].astype(str), index=False).sum() % (1 << 60)), repr(sorted(cfg.items())))   # identity-aware: the null control keeps timestamps but shuffles identities
    if key in _CACHE: return _CACHE[key]
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression, Ridge
    from threadpoolctl import threadpool_limits
    from evalkit.data import song_table
    st = song_table(train).reset_index(); st = st[st.trackId.isin(meta.index)].reset_index(drop=True)
    blocks, ok = _blocks(st.trackId.values, meta, cfg)
    local = cfg["mode"] == "local"
    with threadpool_limits(2):
        tf = []
        for b, X in zip(cfg["blocks"], blocks):    # unsupervised transforms: every train song with audio
            Xo = X[ok]; mu = Xo.mean((0, 1)); sd = Xo.std((0, 1)) + 1e-6; Z = (Xo - mu) / sd
            pca = PCA(cfg["ncomp"], whiten=True, random_state=0).fit(Z.reshape(-1, Z.shape[-1]) if (local and b[0] == "mert") else Z.mean(1)) if cfg["pca"] else None
            tf.append((mu, sd, pca))
        res = dict(tf=tf, lr=None)
        if cfg["meta"]:
            M = _meta_cols(st.trackId.values[ok], meta); res["mm"], res["ms"] = M.mean(0), M.std(0) + 1e-6
        mat = ((st["first"] < cutoff - pd.Timedelta(days=cfg["mature"])).values) & ok
        if cfg["window"]: mat &= (st["first"] >= cutoff - pd.Timedelta(days=cfg["window"])).values | (mat.sum() < 250)
        qa = st["first"].dt.to_period("Q").astype(str).values
        y = st.love.values
        if cfg["target"] in ("rank_plays", "rank_share"):
            col = st.plays90 if cfg["target"] == "rank_plays" else st.share90
            yr = pd.Series(col.values[mat]).groupby(qa[mat]).rank(pct=True).values
        elif cfg["target"] == "rank_mix":   # mean of the two period-normalised ranks and the love label
            yr = (pd.Series(st.plays90.values[mat]).groupby(qa[mat]).rank(pct=True).values + pd.Series(st.share90.values[mat]).groupby(qa[mat]).rank(pct=True).values) / 2
        if cfg["adem"] and cfg["target"] != "love":   # target only: subtract (shrunk) mean target of the song's primary artist among mature train songs (artist never an input)
            ar = pd.Series(st.artist.values[mat]); g = pd.Series(yr).groupby(ar.values); mn = g.transform("sum").values; ct = g.transform("size").values
            loo = (mn - yr) / np.maximum(ct - 1, 1) * (ct - 1) / (ct - 1 + 2.0) + yr.mean() * 2.0 / (ct - 1 + 2.0)   # leave-one-out shrunk artist mean
            yr = yr - cfg["adem"] * (loo - yr.mean())
        w = np.ones(mat.sum())
        if cfg["hl"]: w *= 0.5 ** ((cutoff - st["first"][mat]).dt.days.values / cfg["hl"])
        if mat.sum() > 20:
            blm = [X[mat] for X in blocks]; P = _design(res, blm, st.trackId.values[mat], meta, cfg, local); rep = 4 if local else 1
            if cfg["target"] == "love":
                yy = y[mat]
                if 0 < yy.sum() < len(yy): res["lr"] = LogisticRegression(C=cfg["C"], max_iter=500).fit(P, np.repeat(yy, rep), sample_weight=np.repeat(w, rep))
            else:
                if cfg["learner"] == "gbm":
                    from sklearn.ensemble import HistGradientBoostingRegressor
                    r = HistGradientBoostingRegressor(max_iter=80, learning_rate=0.05, max_depth=3, min_samples_leaf=30, l2_regularization=5.0, random_state=0).fit(P, np.repeat(yr, rep), sample_weight=np.repeat(w, rep))
                elif cfg["learner"] == "svr":
                    from sklearn.svm import SVR
                    r = SVR(C=cfg["C"], epsilon=0.1, gamma="scale").fit(P, np.repeat(yr, rep), sample_weight=np.repeat(w, rep))
                else: r = Ridge(alpha=cfg["alpha"]).fit(P, np.repeat(yr, rep), sample_weight=np.repeat(w, rep))
                r.decision_function = r.predict; res["lr"] = r
        sc = _raw(res, [X[ok] for X in blocks], st.trackId.values[ok], meta, cfg)
        res["tm"], res["ts"], res["neutral"] = float(sc.mean()), float(sc.std() + 1e-9), float(np.median(sc))
        res["lo"], res["hi"] = float(np.percentile(sc, 1)), float(np.percentile(sc, 99))
    _CACHE[key] = res; return res

def _raw(res, blocks, tids, meta, cfg):
    n = len(tids)
    if res["lr"] is None: return np.zeros(n)
    local = cfg["mode"] == "local"; d = res["lr"].decision_function(_design(res, blocks, tids, meta, cfg, local))
    if not local: return d
    d = d.reshape(n, 4); a = cfg["agg"]
    return d.mean(1) if a == "mean" else d.max(1) if a == "max" else np.sort(d, 1)[:, -2:].mean(1) if a == "top2" else d.mean(1) + d.std(1)

def make_ens(cfgs, wts=None):
    """standardised mean of several configs (each standardised with its own train-song score mean/std)"""
    cfgs = [{**CFG, **c} for c in cfgs]; wts = wts or [1] * len(cfgs)
    def predict(train, cands, meta, cutoff):
        out = np.zeros(len(cands))
        for cfg, wt in zip(cfgs, wts):
            res = _fit(train, meta, cutoff, cfg); bl, ok = _blocks(cands.trackId.values, meta, cfg); s = np.full(len(cands), res["neutral"])
            if ok.any(): s[ok] = _raw(res, [X[ok] for X in bl], cands.trackId.values[ok], meta, cfg)
            if cfg["miss"] == "indicator": s = np.where(ok, 0.0, 1.0)
            elif cfg["miss"] == "min": s[~ok] = res["lo"] - 1
            elif cfg["miss"] == "max": s[~ok] = res["hi"] + 1
            out += wt * (s - res["tm"]) / res["ts"]
        return out / sum(wts)
    return predict

M = ("mert", 4, 8); CL = ("clap",)
L3 = [dict(blocks=(("mert", 0, 3),)), dict(blocks=(("mert", 4, 7),)), dict(blocks=(("mert", 8, 11),))]
R = dict(target="rank_plays")
E = dict(R, mode="local", alpha=1200.0)
W32 = dict(R, ncomp=32, alpha=150.0)
L37 = dict(R, blocks=(("mert", 3, 7),), mode="local", alpha=1200.0)
FINAL = [E, W32, L37]   # pre-declared final: three rank_plays members (local L4-8, whole L4-8 nc32, local L3-7), standardised mean
def _ab(**kw): return make_ens([dict(c, **kw) for c in FINAL])
PREDICTORS = {
    "audio_final": make_ens(FINAL),
    "audio_final_meta": _ab(meta=True),                 # ablation 1: separate metadata variant
    "audio_missing_indicator": _ab(miss="indicator"),   # ablation 2: NO audio content, only the 'no audio' flag
}
