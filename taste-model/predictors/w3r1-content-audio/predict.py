"""w3r1 content-audio: does the MUSIC ITSELF (30 s preview audio) predict which new songs get loved?   Entry file for the evalkit harness.
Inputs per song: ONLY MERT-v1-95M features of its preview clip (.cache/shared/w3r1-mert-v1/, built by build_mert.py) -- no artist identity/history, no pool structure.
User history is used only to make training targets (song love label, first-play time) of train songs first played >= 90 d before the cutoff.
Every fitted transform (standardiser, PCA, classifier) is fitted on train-stream songs only; scoring a candidate is independent of the other candidates.
Variants (PREDICTORS):
  ca_whole      audio-only, whole-clip summary (mean of the 4 windows) -> PCA -> logistic regression      [reported headline audio-only whole-clip variant]
  ca_local      audio-only, time-local: each 5 s window is a training instance with the song's label; a song's score = aggregate of its window logits
  ca_ens        audio-only, time-local, ensemble of three layer groups (0-3, 4-7, 8-11) -- best on TUNE by a hair (differences between variants are within noise)
  ca_*_meta     the same + metadata (duration, explicit, popularity, popularity-missing flag) as extra inputs: the separate metadata variant
Ablations (ablations.py): whole vs local, missing-audio handling (neutral / min / max / indicator-only), recency half-life.
Knobs are module constants (CFG); the ablation variants override them via functools.partial-like dicts.
"""
import os, glob, hashlib, warnings
import numpy as np, pandas as pd

ROOT = "/home/user/Listener/taste-model/"
FEATDIR = ROOT + ".cache/shared/w3r1-mert-v1/"
CFG = dict(layers=(4, 8), ncomp=64, C=0.05, hl=None, balance=False, agg="mean", miss="neutral", meta=False, windows=(0, 1, 2, 3), mature=90, mode="whole", target="love", alpha=300.0)
_F = {}

def _store():
    if "idx" not in _F:
        keys, arrs = [], []
        for f in sorted(glob.glob(FEATDIR + "shard_*.npz")):
            z = np.load(f); keys += list(z["md5"]); arrs.append(z["feat"])
        _F["idx"] = {k: i for i, k in enumerate(keys)}; _F["arr"] = np.concatenate(arrs) if arrs else np.zeros((0, 4, 12, 768), np.float16)
    return _F["idx"], _F["arr"]

def _view(tids, meta, cfg):
    """[n, W, D] float32 window features (layers a..b averaged) and ok mask (False = no usable audio)."""
    idx, arr = _store(); u = meta.previewUrl.reindex(tids).values
    ii = np.array([idx.get(hashlib.md5(x.encode()).hexdigest(), -1) if isinstance(x, str) else -1 for x in u])
    a, b = cfg["layers"]; ok = ii >= 0
    X = np.full((len(tids), len(cfg["windows"]), 768), np.nan, np.float32)
    if ok.any(): X[ok] = arr[ii[ok]][:, list(cfg["windows"])][:, :, a:b + 1].astype(np.float32).mean(2)
    ok &= np.isfinite(X).all((1, 2)); return X, ok

def _meta_cols(tids, meta):
    m = meta.reindex(tids)
    return np.c_[np.log1p(m.durationMs.fillna(0).values / 1000.0), m.explicit.astype(float).fillna(0).values, m.popularity.fillna(0).values / 100.0, m.popularity.isna().values.astype(float) + (m.popularity.fillna(0).values == 0)]

_CACHE = {}
def _fit(train, meta, cutoff, cfg):
    key = (str(cutoff), len(train), int(train.t.values.astype("int64").sum() % (1 << 60)), repr(sorted(cfg.items())))
    if key in _CACHE: return _CACHE[key]
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression
    from threadpoolctl import threadpool_limits
    from evalkit.data import song_table
    st = song_table(train).reset_index()
    st = st[st.trackId.isin(meta.index)].reset_index(drop=True)
    X, ok = _view(st.trackId.values, meta, cfg)
    with threadpool_limits(2):
        # standardiser + PCA: fitted on ALL train songs with audio (features only, no labels)
        mu = X[ok].mean((0, 1)); sd = X[ok].std((0, 1)) + 1e-6
        Z = (X[ok][:, :, :] - mu) / sd; pca = PCA(cfg["ncomp"], whiten=True, random_state=0).fit(Z.reshape(-1, Z.shape[-1]) if cfg["mode"] == "local" else Z.mean(1))
        # supervised part: mature songs only (label horizon complete), with audio
        mat = (st["first"] < cutoff - pd.Timedelta(days=cfg["mature"])).values & ok
        y = st.love.values[mat]; w = np.ones(mat.sum())
        if cfg["hl"]: w *= 0.5 ** ((cutoff - st["first"][mat]).dt.days.values / cfg["hl"])
        if cfg["balance"]:   # per discovery quarter, positives and negatives get equal total weight (removes the drift of the base rate with calendar time)
            q = st["first"][mat].dt.to_period("Q").astype(str).values
            for g in np.unique(q):
                for c in (0, 1):
                    s = (q == g) & (y == c)
                    if s.any(): w[s] *= 0.5 * w[q == g].sum() / max(w[s].sum(), 1e-9)
        Zm = (X[mat] - mu) / sd
        extra = None
        if cfg["meta"]:
            M = _meta_cols(st.trackId.values[mat], meta); mm, ms = M.mean(0), M.std(0) + 1e-6; extra = (mm, ms)
        def build(Zw, M):
            P = pca.transform(Zw.reshape(-1, Zw.shape[-1]))
            if cfg["mode"] == "whole": P = P.reshape(len(Zw), len(cfg["windows"]), -1).mean(1) if False else pca.transform(Zw.mean(1))
            if M is not None: P = np.c_[P, np.repeat((M - extra[0]) / extra[1], 1 if cfg["mode"] == "whole" else len(cfg["windows"]), 0)]
            return P
        if cfg["mode"] == "whole": Ptr = build(Zm, M if cfg["meta"] else None); ytr, wtr = y, w
        else: Ptr = build(Zm, M if cfg["meta"] else None); ytr, wtr = np.repeat(y, len(cfg["windows"])), np.repeat(w, len(cfg["windows"]))
        lr = None
        if cfg["target"] == "rank":   # continuous target: percentile of share90 among the songs discovered in the same quarter (removes calendar drift), ridge
            from sklearn.linear_model import Ridge
            qq = st["first"][mat].dt.to_period("Q").astype(str).values
            yr = pd.Series(st.share90.values[mat]).groupby(qq).rank(pct=True).values
            lr = Ridge(alpha=cfg["alpha"]).fit(Ptr, np.repeat(yr, 1 if cfg["mode"] == "whole" else len(cfg["windows"])), sample_weight=wtr); lr.decision_function = lr.predict
        elif 0 < y.sum() < len(y): lr = LogisticRegression(C=cfg["C"], max_iter=500).fit(Ptr, ytr, sample_weight=wtr)
        # train-derived neutral value for songs without audio: median score of the train songs
        res = dict(mu=mu, sd=sd, pca=pca, lr=lr, extra=extra, build=build)
        sc_tr = _raw(res, X[ok], meta, st.trackId.values[ok], cfg) if lr is not None else np.zeros(ok.sum())
        res["tm"] = float(sc_tr.mean()); res["ts"] = float(sc_tr.std() + 1e-9); res["neutral"] = float(np.median(sc_tr)); res["lo"] = float(np.percentile(sc_tr, 1)); res["hi"] = float(np.percentile(sc_tr, 99))
        # missing-audio indicator model (variant 'indicator'): love rate of mature train songs without / with audio
        mm_ = (st["first"] < cutoff - pd.Timedelta(days=cfg["mature"])).values
        res["rate_missing"] = float(st.love.values[mm_ & ~ok].mean()) if (mm_ & ~ok).any() else np.nan; res["rate_audio"] = float(st.love.values[mm_ & ok].mean())
    _CACHE[key] = res; return res

def _raw(res, Xv, meta, tids, cfg):
    Z = (Xv - res["mu"]) / res["sd"]
    if res["lr"] is None: return np.zeros(len(Xv))
    P = res["build"](Z, _meta_cols(tids, meta) if cfg["meta"] else None)
    d = res["lr"].decision_function(P)
    if cfg["mode"] == "whole": return d
    d = d.reshape(len(Xv), len(cfg["windows"]))
    a = cfg["agg"]
    return d.mean(1) if a == "mean" else d.max(1) if a == "max" else np.sort(d, 1)[:, -2:].mean(1) if a == "top2" else d.min(1) if a == "min" else d.mean(1) + d.std(1)

def make(**over):
    cfg = {**CFG, **over}
    def predict(train, cands, meta, cutoff):
        res = _fit(train, meta, cutoff, cfg)
        X, ok = _view(cands.trackId.values, meta, cfg)
        s = np.zeros(len(cands))
        if cfg["miss"] == "indicator":   # indicator-only predictor: no audio content at all
            return np.where(ok, 0.0, 1.0 if (res["rate_missing"] > res["rate_audio"]) else -1.0)
        if ok.any(): s[ok] = _raw(res, X[ok], meta, cands.trackId.values[ok], cfg)
        s[~ok] = {"neutral": res["neutral"], "min": res["lo"] - 1.0, "max": res["hi"] + 1.0}[cfg["miss"]]
        return s
    return predict

def make_ens(*overs, **common):
    """Ensemble: mean of train-standardised scores of several configurations (each standardised with its own train-song score mean/std, so no dependence on the candidates)."""
    cfgs = [{**CFG, **common, **o} for o in overs]
    def predict(train, cands, meta, cutoff):
        out = np.zeros(len(cands)); 
        for cfg in cfgs:
            res = _fit(train, meta, cutoff, cfg); X, ok = _view(cands.trackId.values, meta, cfg); s = np.zeros(len(cands))
            if ok.any(): s[ok] = (_raw(res, X[ok], meta, cands.trackId.values[ok], cfg) - res["tm"]) / res["ts"]
            s[~ok] = (res["neutral"] - res["tm"]) / res["ts"]; out += s
        return out / len(cfgs)
    return predict

_L3 = (dict(layers=(0, 3)), dict(layers=(4, 7)), dict(layers=(8, 11)))
PREDICTORS = {"ca_whole": make(), "ca_local": make(mode="local"), "ca_ens": make_ens(*_L3, mode="local"),
              "ca_whole_meta": make(meta=True), "ca_ens_meta": make_ens(*_L3, mode="local", meta=True)}
