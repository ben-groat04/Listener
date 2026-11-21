"""w3r1 training-signal study: one fixed song representation (evalkit's nonaudio_gbm feature set = metadata + point-in-time artist history),
many ways of building the TRAINING TARGET / WEIGHTS / ROWS from the pre-cutoff streams.

Everything is computed from `train` (streams < cutoff) only. Training rows = train songs whose 90-day label horizon is complete before the cutoff
(first play < cutoff - 90 d); songs first played in the last 90 days before the cutoff are NOT used as training rows (their labels are truncated),
but their plays do count in the artist-history features of candidates (that is history, not label).
Exposure context of training songs (number of new songs in the session of the first play, `nnew`) is computed from train streams only.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evalkit import data, baselines as B

H = 90
_BUILD, _FIT = {}, {}


def _tkey(train, cutoff):
    return (str(cutoff), len(train), int(pd.util.hash_array(train.trackId.values).sum() % (1 << 60)), int(train.t.values.astype("int64").sum() % (1 << 60)))


def build(train, cutoff, meta):
    """Training rows + fixed-representation features, shared by all variants (cached per cutoff)."""
    k = _tkey(train, cutoff)
    if k in _BUILD: return _BUILD[k]
    st = data.song_table(train).reset_index()
    sd = data.song_diag(train)
    st = st.join(sd[["sess", "nnew_sess", "day1"]], on="song")
    # session length (streams in the session of the first play) from the train streams
    ss = data._sessions(train.sort_values("t", kind="stable"))
    slen = pd.Series(ss).value_counts()
    st["slen"] = st.sess.map(slen).fillna(1).values
    mt = st[st["first"] < cutoff - pd.Timedelta(days=H)]
    hist = B._Hist(train, st); prior = float(mt.love.mean()) if len(mt) else .25
    rows = mt[mt.trackId.isin(meta.index)].reset_index(drop=True)
    rows["age"] = (cutoff - rows["first"]).dt.days.values
    X = B._features(True, rows, B._sec(rows["first"].values), meta, hist, prior)
    rows["qtr"] = rows["first"].dt.to_period("Q").astype(str)
    rows["wk"] = rows["first"].dt.to_period("W").astype(str)
    rows["start_age"] = (rows["first"] - train.t.min()).dt.days.values
    _BUILD[k] = (rows, X, hist, prior, float(rows.love.mean()) if len(rows) else .5)
    return _BUILD[k]


# ---------------------------------------------------------------- targets
def grade(r):
    """0..4 ordinal engagement grade from plays/days in the 90-day horizon."""
    g = np.zeros(len(r), int)
    g += (r.plays90 >= 2).values; g += ((r.plays90 >= 4) & (r.days90 >= 2)).values
    g += ((r.plays90 >= 6) & (r.days90 >= 3)).values; g += ((r.plays90 >= 15) & (r.days90 >= 5)).values
    return g


def make_target(r, name, pre):
    """returns y (float array) and kind 'clf' | 'reg'."""
    if name == "love": return r.love.values, "clf"
    if name == "love_4_2": return r.love_4_2.values, "clf"
    if name == "love_10_4": return r.love_10_4.values, "clf"
    if name == "strong": return r.strong.values, "clf"
    if name == "plays_ge2": return (r.plays90 >= 2).astype(int).values, "clf"
    if name == "lplays": return np.log1p(r.plays90.values), "reg"
    if name == "ldays": return np.log1p(r.days90.values), "reg"
    if name == "lshare": return np.log(r.share90.values + 1e-4), "reg"
    if name == "grade": return grade(r).astype(float), "reg"
    if name == "love+share":   # average of the binary label and the within-quarter percentile of share90
        pr = r.groupby("qtr").share90.rank(pct=True).values; return 0.5 * r.love.values + 0.5 * pr, "reg"
    if name == "rank_share":   # within-quarter percentile of share90 (volume- and period-normalised graded target)
        return r.groupby("qtr").share90.rank(pct=True).values, "reg"
    if name == "rank_plays":
        return r.groupby("qtr").plays90.rank(pct=True).values, "reg"
    raise ValueError(name)


def exposure_adjust(r, y, kind):
    """remove the linear effect of log(#new songs in the session of first play) after period fixed effects (OLS), keeping the period means."""
    ln = np.log(r.nnew_sess.values.astype(float))
    d = pd.get_dummies(r.qtr).values.astype(float)
    A = np.c_[ln, d]; beta = np.linalg.lstsq(A, y.astype(float), rcond=None)[0][0]
    return y.astype(float) - beta * (ln - ln.mean()), "reg"


def fit_variant(train, cutoff, meta, o):
    """o: dict of options. Returns scorer(cands)->scores."""
    rows, X, hist, prior, base = build(train, cutoff, meta)
    csec = int(B._sec(np.array([np.datetime64(cutoff)]))[0])
    keep = np.ones(len(rows), bool)
    if o.get("window"): keep &= rows.age.values <= o["window"]
    if o.get("skip_start", 0): keep &= rows.start_age.values >= o["skip_start"]
    ex = o.get("exposure", "none")
    if ex.startswith("drop"): keep &= rows.nnew_sess.values <= int(ex[4:])
    if ex == "sole": keep &= rows.nnew_sess.values <= 1
    r = rows[keep].reset_index(drop=True); Xk = X[keep].reset_index(drop=True)
    if len(r) < 60: return lambda cands, meta: np.full(len(cands), 0.5)
    y, kind = make_target(r, o.get("target", "love"), prior)
    w = np.ones(len(r))
    if o.get("hl"): w *= 0.5 ** (r.age.values / o["hl"])
    if ex.startswith("w"):   # weight by 1/nnew^alpha, e.g. "w0.5"
        w *= r.nnew_sess.values.astype(float) ** (-float(ex[1:]))
    if ex == "resid": y, kind = exposure_adjust(r, y, kind)
    marg = ex == "marg"
    if marg: Xk = Xk.assign(lnnew=np.log(r.nnew_sess.values.astype(float)))
    gname = o.get("group")
    mdl_kind = o.get("model", "gbm")
    if gname:   # pairwise / within-context comparison
        gcol = dict(quarter="qtr", week="wk", session="sess", artist="artist")[gname]
        g = r[gcol]
        if mdl_kind == "gbm":   # regression on the group-demeaned target
            y = y - pd.Series(y).groupby(g.values).transform("mean").values; kind = "reg"
            w = w * np.sqrt(pd.Series(1, index=g.values).groupby(level=0).transform("size").values.astype(float) - 1 + 1e-9) / 3
    cols = list(Xk.columns)
    cst = [B.MONO.get(c, 0) for c in cols]
    if marg: cst[-1] = -1
    cst = [c * int(not o.get("nomono", False)) for c in cst]
    kw = dict(B.GBM_KW); kw.update({k: v for k, v in o.get("gbm", {}).items()})
    from threadpoolctl import threadpool_limits
    if mdl_kind == "rank":
        import lightgbm as lgb
        lab = grade(r) if o.get("target", "love") != "love" else r.love.values.astype(int)
        order = np.argsort(r[gcol].values, kind="stable"); gs = r[gcol].values[order]
        _, cnt = np.unique(gs, return_counts=True)
        with threadpool_limits(2):
            m = lgb.LGBMRanker(objective="lambdarank", n_estimators=kw["max_iter"], learning_rate=kw["learning_rate"], num_leaves=kw["max_leaf_nodes"],
                               min_child_samples=kw["min_samples_leaf"] // 2, reg_lambda=kw["l2_regularization"], monotone_constraints=cst, n_jobs=2,
                               random_state=0, verbose=-1, deterministic=True, force_row_wise=True)
            m.fit(Xk.values[order], lab[order], group=cnt, sample_weight=None)
        predict_raw = lambda Z: m.predict(Z.values)
    else:
        from sklearn.ensemble import HistGradientBoostingClassifier as C, HistGradientBoostingRegressor as R
        if kind == "clf":
            if not (0 < y.sum() < len(y)): return lambda cands, meta: np.full(len(cands), 0.5)
            with threadpool_limits(2): m = C(monotonic_cst=cst, **kw).fit(Xk, y, sample_weight=w)
            predict_raw = lambda Z: m.predict_proba(Z)[:, 1]
        else:
            with threadpool_limits(2): m = R(monotonic_cst=cst, **kw).fit(Xk, y, sample_weight=w)
            predict_raw = lambda Z: m.predict(Z)

    def scorer(cands, meta):
        Z = B._features(True, cands, np.full(len(cands), csec), meta, hist, prior)[[c for c in cols if c != "lnnew"]]
        with threadpool_limits(2):
            if marg:
                qs = np.quantile(np.log(r.nnew_sess.values.astype(float)), np.linspace(.05, .95, 7))
                return np.mean([predict_raw(Z.assign(lnnew=q)) for q in qs], axis=0)
            return predict_raw(Z)
    return scorer


def make_predictor(o):
    o = dict(o)
    def predict(train, cands, meta, cutoff):
        k = (_tkey(train, cutoff), repr(sorted(o.items(), key=lambda t: t[0])))
        if k not in _FIT: _FIT[k] = fit_variant(train, cutoff, meta, o)
        return _FIT[k](cands, meta)
    return predict
