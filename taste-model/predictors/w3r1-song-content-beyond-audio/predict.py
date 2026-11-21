"""w3r1 song-content: predicts love from public LYRICS of the song (lrclib.net) only. Artist identity/history is never an input.
Inputs per track: (a) hand lyric statistics (features.NAMES), (b) multilingual MiniLM embedding of the lyrics (mean of chunk embeddings), PCA fit on train songs only.
Training: train songs first played before cutoff-90d WITH lyrics, label = love (data.song_table), 180-day recency weights. Songs without lyrics get the neutral (intercept) score.
Models: lyr_all (logistic on stats+PCA emb), lyr_stats (logistic, stats only), lyr_emb (logistic, emb only), lyr_gbm (HGB on stats+PCA), lyr_resid (ridge on artist-residualised target; artist used ONLY to build the training target).
Variants reported separately: lyr_meta (+duration, explicit, popularity), lyr_ind (+has-lyrics indicator)."""
import os, sys, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from common import CACHE
from features import NAMES

_D = {}
def _cache():
    if not _D:
        try: F = pickle.load(open(CACHE / "feats.pkl", "rb"))
        except Exception: F = {}
        try: E = pickle.load(open(CACHE / "emb.pkl", "rb"))
        except Exception: E = {}
        _D["F"], _D["E"] = F, E
    return _D["F"], _D["E"]

def _mats(ids):
    F, E = _cache()
    S = np.full((len(ids), len(NAMES)), np.nan, np.float32); M = np.full((len(ids), 384), np.nan, np.float32)
    for k, i in enumerate(ids):
        f = F.get(i)
        if f is not None: S[k] = [f[n] for n in NAMES]
        e = E.get(i)
        if e is not None: M[k] = e
    return S, M

HL = 180.0
_FIT = {}

def _train(train, cutoff, meta):
    from evalkit.data import song_table, HORIZON_DAYS
    st = song_table(train).reset_index()
    mt = st[(st["first"] < cutoff - pd.Timedelta(days=HORIZON_DAYS)) & st.trackId.isin(meta.index)].reset_index(drop=True)
    S, M = _mats(mt.trackId.values)
    ok = ~np.isnan(S).all(1)
    # artist-residual target (artist only used for training target; leave-one-out smoothed love rate)
    a = mt.artist.values; g = pd.DataFrame({"a": a, "y": mt.love.values}).groupby("a").y.agg(["sum", "count"]).reindex(a)
    prior = mt.love.mean(); loo = (g["sum"].values - mt.love.values + 3 * prior) / (g["count"].values - 1 + 3)
    w = 0.5 ** ((cutoff - mt["first"]).dt.days.values / HL)
    return mt, S, M, ok, mt.love.values.astype(float), mt.love.values - loo, w

def _build(kind, train, cutoff, meta):
    key = (kind, str(cutoff), len(train), float(train.t.astype("int64").sum() % 1e12))
    if key in _FIT: return _FIT[key]
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression, Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import HistGradientBoostingClassifier
    from threadpoolctl import threadpool_limits
    mt, S, M, ok, y, yres, w = _train(train, cutoff, meta)
    use_s = kind in ("lyr_all", "lyr_stats", "lyr_gbm", "lyr_resid", "lyr_meta", "lyr_ind"); use_e = kind in ("lyr_all", "lyr_emb", "lyr_gbm", "lyr_resid", "lyr_meta", "lyr_ind")
    hasE = ok & ~np.isnan(M).any(1)
    tr = ok & (hasE if use_e else True)
    if tr.sum() < 40 or y[tr].sum() < 5 or (1 - y[tr]).sum() < 5: _FIT[key] = None; return None
    med = np.nanmedian(S[tr], 0)
    def design(S, M, X0):
        Sx = np.where(np.isnan(S), med, S); cols = []
        if use_s: cols.append(sc.transform(Sx))
        if use_e: cols.append(pca.transform(np.nan_to_num(M)) / ps)
        if kind == "lyr_meta": cols.append(X0)
        if kind == "lyr_ind": cols.append(np.zeros((len(S), 0)))
        return np.hstack(cols)
    sc = StandardScaler().fit(np.where(np.isnan(S[tr]), med, S[tr])) if use_s else None
    if use_e: pca = PCA(24, random_state=0).fit(M[tr]); ps = np.sqrt(pca.explained_variance_[0])
    X0tr = None
    if kind == "lyr_meta":
        X0tr = _meta_x(mt.trackId.values, meta); mu, sd = np.nanmean(X0tr[tr], 0), np.nanstd(X0tr[tr], 0) + 1e-6
        X0n = lambda X: np.nan_to_num((X - mu) / sd)
        X0tr = X0n(X0tr)
    X = design(S[tr], M[tr], X0tr[tr] if X0tr is not None else None)
    with threadpool_limits(2):
        if kind == "lyr_gbm":
            m = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=150, min_samples_leaf=40, l2_regularization=5.0, random_state=0).fit(X, y[tr], sample_weight=w[tr])
        elif kind == "lyr_resid":
            m = Ridge(alpha=300.0).fit(X, yres[tr], sample_weight=w[tr])
        else:
            m = LogisticRegression(C=0.02, max_iter=500).fit(X, y[tr], sample_weight=w[tr])
    out = (m, design, med, X0n if kind == "lyr_meta" else None, kind)
    _FIT[key] = out; return out

def _meta_x(ids, meta):
    m = meta.reindex(list(ids))
    return np.c_[np.log1p(m.durationMs.astype(float)), m.explicit.astype(float), m.popularity.astype(float) / 100.0]

def _score(kind, train, cands, meta, cutoff):
    fit = _build(kind, train, cutoff, meta)
    if fit is None: return np.zeros(len(cands))
    m, design, med, X0n, _ = fit
    ids = cands.trackId.values; S, M = _mats(ids)
    cov = ~np.isnan(S).all(1) & (~np.isnan(M).any(1) if kind in ("lyr_all", "lyr_emb", "lyr_gbm", "lyr_resid", "lyr_meta", "lyr_ind") else True)
    X0 = X0n(_meta_x(ids, meta)) if X0n else None
    X = design(S, M, X0)
    if kind in ("lyr_gbm",): s = m.predict_proba(X)[:, 1]; neutral = np.mean(m.predict_proba(design(np.tile(med, (1, 1)), np.zeros((1, 384)), None if X0 is None else np.zeros((1, 3))))[:, 1])
    elif kind == "lyr_resid": s = m.predict(X); neutral = float(m.intercept_)
    else: s = m.decision_function(X); neutral = float(m.intercept_[0])
    if kind == "lyr_ind": pass
    return np.where(cov, s, neutral)

def _mk(kind):
    return lambda train, cands, meta, cutoff: _score(kind, train, cands, meta, cutoff)

KINDS = os.environ.get("W3R1_KINDS", "lyr_all,lyr_stats,lyr_emb,lyr_gbm,lyr_resid").split(",")
PREDICTORS = {k: _mk(k) for k in KINDS}
