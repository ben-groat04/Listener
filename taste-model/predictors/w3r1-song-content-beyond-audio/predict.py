"""w3r1 song-content: predicts love from public LYRICS of the song (lrclib.net) only. Artist identity/history is never an input.
Inputs per track: (a) hand lyric statistics (features.NAMES), (b) multilingual MiniLM embedding of the lyrics (mean of chunk embeddings), PCA fit on train songs only.
Training: train songs first played before cutoff-90d WITH lyrics, label = love (data.song_table), 180-day recency weights. Songs without lyrics get the neutral (intercept) score.
Models (all on lyrics only; no artist/meta input):
 lyr_resid_nodur  PRIMARY: ridge on lyric statistics WITHOUT duration-derived columns; target = love minus leave-one-out smoothed artist love rate (artist used ONLY to build the training target).
 lyr_resid_orth   stats residualised on log duration (slope fit on train songs; meta duration used only to remove it) + PCA(24) of lyric embedding; same ridge target.
 lyr_all          logistic on all stats (incl. duration-derived) + PCA emb, plain love target.   lyr_stats / lyr_emb: ablations of lyr_all.
 cov_only         has-lyrics indicator alone (missing-information control)."""
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

DURCOLS = ["n_words", "n_lines", "words_per_sec", "first_lyric_frac", "lyric_span_frac", "n_stanzas", "line_gap_mean", "gap_long_frac"]
def _prep(kind, S, ids, meta, ref=None):
    """nodur: drop duration-derived columns; orth: residualise every stat on log duration (slope fit on train songs only, `ref`)."""
    if kind == "lyr_resid_nodur":
        S = S.copy(); S[:, [NAMES.index(c) for c in DURCOLS]] = np.nan; return S, None
    if kind in ("lyr_resid_orth",):
        ld = np.log1p(meta.durationMs.astype(float).reindex(list(ids)).values)
        if ref is None:
            ok = ~np.isnan(S) & ~np.isnan(ld)[:, None]; ref = []
            for j in range(S.shape[1]):
                o = ok[:, j]
                if o.sum() < 20 or np.std(ld[o]) == 0: ref.append((0.0, 0.0, 0.0)); continue
                b = np.polyfit(ld[o], S[o, j], 1); ref.append((b[0], b[1], 1.0))
        S = S.copy()
        for j, (a, b, f) in enumerate(ref):
            if f: S[:, j] = S[:, j] - (a * ld + b)
        return S, ref
    return S, None

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
    key = (kind, str(cutoff), len(train), float(train.t.astype("int64").sum() % 1e12), int(pd.util.hash_array(train.trackId.values).sum() % (1 << 60)))
    if key in _FIT: return _FIT[key]
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression, Ridge
    from sklearn.preprocessing import StandardScaler
    from threadpoolctl import threadpool_limits
    mt, S, M, ok, y, yres, w = _train(train, cutoff, meta)
    S, ref = _prep(kind, S, mt.trackId.values, meta)
    use_s = kind in ("lyr_all", "lyr_stats", "lyr_resid_nodur", "lyr_resid_orth"); use_e = kind in ("lyr_all", "lyr_emb", "lyr_resid_orth")
    hasE = ok & ~np.isnan(M).any(1)
    tr = ok & (hasE if use_e else True)
    if tr.sum() < 40 or y[tr].sum() < 5 or (1 - y[tr]).sum() < 5: _FIT[key] = None; return None
    import warnings; warnings.simplefilter("ignore"); med = np.nan_to_num(np.nanmedian(S[tr], 0))
    def design(S, M, X0):
        Sx = np.where(np.isnan(S), med, S); cols = []
        if use_s: cols.append(sc.transform(Sx))
        if use_e: cols.append(pca.transform(np.nan_to_num(M)) / ps)
        return np.hstack(cols)
    sc = StandardScaler().fit(np.where(np.isnan(S[tr]), med, S[tr])) if use_s else None
    if use_e: pca = PCA(24, random_state=0).fit(M[tr]); ps = np.sqrt(pca.explained_variance_[0])
    X = design(S[tr], M[tr], None)
    with threadpool_limits(2):
        if kind.startswith("lyr_resid"):
            m = Ridge(alpha=300.0).fit(X, yres[tr], sample_weight=w[tr])
        else:
            m = LogisticRegression(C=0.02, max_iter=500).fit(X, y[tr], sample_weight=w[tr])
    out = (m, design, med, None, ref)
    _FIT[key] = out; return out

def _score(kind, train, cands, meta, cutoff):
    if kind == "cov_only":
        F, _ = _cache(); return np.array([0.0 if F.get(i) is None else 1.0 for i in cands.trackId.values])
    fit = _build(kind, train, cutoff, meta)
    if fit is None: return np.zeros(len(cands))
    m, design, med, X0n, ref = fit
    ids = cands.trackId.values; S, M = _mats(ids); S0 = S; S, _ = _prep(kind, S, ids, meta, ref)
    cov = ~np.isnan(S0).all(1) & (~np.isnan(M).any(1) if kind in ("lyr_all", "lyr_emb", "lyr_resid_orth") else True)
    X = design(S, M, None)
    if kind.startswith("lyr_resid"): s = m.predict(X); neutral = float(m.intercept_)
    else: s = m.decision_function(X); neutral = float(m.intercept_[0])
    return np.where(cov, s, neutral)

def _mk(kind):
    return lambda train, cands, meta, cutoff: _score(kind, train, cands, meta, cutoff)

KINDS = os.environ.get("W3R1_KINDS", "lyr_resid_nodur,lyr_resid_orth,lyr_all,cov_only").split(",")
PREDICTORS = {k: _mk(k) for k in KINDS}
