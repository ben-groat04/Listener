"""A-gbm-history: supervised 'as-of' model. Train examples = songs the user first tried before cutoff-90d (label = love, computed
inside train only); features of each example are computed from streams strictly before that song's first play, so the model learns
P(love | what I knew about the user when the song first appeared). The same feature function is applied to candidates at t0=cutoff.
Features: multi-scale artist/album history, artist exploration and love-rate history, metadata, title/album-name cues, a hashed
char-ngram text model (out-of-fold stacked)."""
import numpy as np, pandas as pd, re, pickle, os
BETA = float(os.environ.get('XB', 0.3))
GAMMA = float(os.environ.get('XG', 0.3))
WREG = float(os.environ.get('XR', 0.0))
WLR = float(os.environ.get('XL', 0.0))
import lightgbm as lgb
from evalkit.data import song_table

_CACHE = {}
_EMB = {}
def _emb_table():
    if not _EMB:
        p = "/home/user/Listener/taste-model/.cache/shared/clap-preview-emb/emb.pkl"
        try: d = pickle.load(open(p, "rb"))
        except Exception: d = {}
        _EMB["d"] = d
    return _EMB["d"]

def _emb_for(track_ids, meta):
    d = _emb_table(); pu = meta.previewUrl.reindex(list(track_ids)).values
    E = np.full((len(pu), 768), np.nan, dtype=np.float32)
    for i, u in enumerate(pu):
        v = d.get(u) if isinstance(u, str) else None
        if v is not None: E[i] = v / (np.linalg.norm(v) + 1e-9)
    return E

BETA_K = 10.0
def aud_feats(Eq, tq, Ej, fj, lovej, p90j):
    """Audio features of queries (time tq, days) vs train songs j (first day fj, love, plays90); strictly as-of tq."""
    m = len(Eq); out = np.full((m, 12), np.nan, dtype=np.float32)
    okq = ~np.isnan(Eq[:, 0]); okj = ~np.isnan(Ej[:, 0])
    if not okq.any(): return out
    S = Eq[okq] @ Ej[okj].T
    t = tq[okq][:, None]; f = fj[okj][None, :]
    prior = f < t; mat = (f + 90.0) <= t; rec = prior & (f >= t - 365.0)
    lv = lovej[okj][None, :] > 0; p90 = p90j[okj][None, :]
    K = np.exp(BETA_K * (S - 1.0)).astype(np.float32)
    def ks(mask): return (K * mask).sum(1)
    dall = ks(prior); dl = ks(mat & lv); dn = ks(mat & ~lv); drec = ks(rec)
    nl = (mat & lv).sum(1); nn = (mat & ~lv).sum(1)
    r = np.zeros((okq.sum(), 12), dtype=np.float32)
    r[:, 0] = np.log(dall + 1e-3); r[:, 1] = np.log(drec + 1e-3)
    r[:, 2] = np.log((dl + 0.05) / (nl + 1)) - np.log((dn + 0.05) / (nn + 1))
    r[:, 3] = np.log(dl + 1e-3); r[:, 4] = np.log(dn + 1e-3)
    def topk(mask, k):
        X = np.where(mask, S, -2.0); X = -np.sort(-X, axis=1)[:, :k]
        X = np.where(X < -1.5, np.nan, X); return np.nanmean(X, 1) if X.shape[1] else np.full(len(X), np.nan)
    import warnings; warnings.simplefilter("ignore")
    r[:, 5] = topk(mat & lv, 3); r[:, 6] = topk(prior, 3); r[:, 7] = topk(mat & lv, 1); r[:, 8] = topk(mat & ~lv, 3)
    r[:, 9] = (K * mat * np.log1p(p90)).sum(1) / ((K * mat).sum(1) + 1e-3)   # kernel-regressed log plays
    r[:, 10] = r[:, 5] - r[:, 8]
    r[:, 11] = (K * mat * lv).sum(1) / ((K * mat).sum(1) + 1e-3)
    out[okq] = r
    return out
AUD_COLS = [f"au{i}" for i in range(12)]
DAY = np.timedelta64(1, "D")

def _days(t): return t.values.astype("datetime64[s]").astype(np.int64) / 86400.0

class Hist:
    def __init__(self, train, st):
        self.t0 = _days(train.t)
        ex = pd.DataFrame({"d": _days(train.t), "a": train.artistIds.values, "dayi": np.floor(_days(train.t)), "pm": train.playedMs.values / 1000.0}).explode("a").dropna(subset=["a"])
        self.art = {a: (g.d.values, g.dayi.values) for a, g in ex.groupby("a")}
        self.artpm = {a: np.concatenate([[0.0], np.cumsum(g.pm.values.astype(float))]) for a, g in ex.groupby("a")}   # sorted since train is time-sorted
        al = pd.DataFrame({"d": _days(train.t), "al": train.albumId.values, "s": train.song.values})
        self.alb = {k: (g.d.values, g.s.values) for k, g in al.groupby("al")}
        # artist -> arrays of (first day, love, song) for songs, love only trusted when mature (first+90 <= t)
        sx = st[["first", "artistIds", "love", "plays90"]].copy(); sx["fd"] = _days(sx["first"])
        sx = sx.explode("artistIds").dropna(subset=["artistIds"]).sort_values("fd")
        self.sa = {a: (g.fd.values, g.love.values, g.plays90.values) for a, g in sx.groupby("artistIds")}
        self.tot_sorted = np.sort(self.t0)

    def row(self, arts, album, t, song_rep=None):
        best = None
        out = {}
        f = []
        for a in arts:
            r = {}
            if a in self.art:
                d, dy = self.art[a]; i = np.searchsorted(d, t, "left")
                dd = d[:i]
                r["ap"] = i
                for w in (7, 30, 90, 365): r[f"ap{w}"] = i - np.searchsorted(d, t - w, "left")
                r["adays"] = len(np.unique(dy[:i])) if i else 0
                r["agap"] = (t - dd[-1]) if i else 9999.0
                r["aage"] = (t - dd[0]) if i else 0.0
                cs = self.artpm[a]; j = np.searchsorted(d, t - 365, "left")
                r["apm"] = cs[i] / i if i else 0.0
                r["apm365"] = (cs[i] - cs[j]) / (i - j) if i > j else 0.0
                r["adays90"] = len(np.unique(dy[np.searchsorted(d, t - 90, "left"):i])) if i else 0
            else:
                r = dict(apm=0.0, apm365=0.0, ap=0, ap7=0, ap30=0, ap90=0, ap365=0, adays=0, agap=9999.0, aage=0.0, adays90=0)
            if a in self.sa:
                fd, lv, p90 = self.sa[a]; i = np.searchsorted(fd, t, "left"); j = np.searchsorted(fd, t - 90, "left")
                r["as_n"] = i; r["as_n90"] = i - np.searchsorted(fd, t - 90, "left"); r["as_n365"] = i - np.searchsorted(fd, t - 365, "left")
                r["as_mat"] = j; r["as_love"] = lv[:j].sum(); r["as_love365"] = lv[np.searchsorted(fd, t - 455, "left"):j].sum()
                r["as_lr"] = (r["as_love"] + 0.2 * 2) / (j + 2)
                r["as_p90mean"] = p90[:j].mean() if j else 0.0
            else:
                r.update(as_n=0, as_n90=0, as_n365=0, as_mat=0, as_love=0, as_love365=0, as_lr=0.2 * 2 / 2, as_p90mean=0.0)
            f.append(r)
        # aggregate: max over artists for counts, first artist separately for a few
        keys = f[0].keys()
        for k in keys:
            v = [x[k] for x in f]; out[k] = min(v) if k == "agap" else max(v)
        out["p_ap"] = f[0]["ap"]; out["p_lr"] = f[0]["as_lr"]
        if album in self.alb:
            d, s = self.alb[album]; i = np.searchsorted(d, t, "left")
            out["alb_p"] = i; out["alb_songs"] = len(set(s[:i])); out["alb_p90"] = i - np.searchsorted(d, t - 90, "left")
        else: out["alb_p"] = out["alb_songs"] = out["alb_p90"] = 0
        k = np.searchsorted(self.tot_sorted, t, "left")
        out["tot90"] = k - np.searchsorted(self.tot_sorted, t - 90, "left")
        out["share90"] = out["ap90"] / (out["tot90"] + 1)
        out["share365"] = out["ap365"] / (k - np.searchsorted(self.tot_sorted, t - 365, "left") + 1)
        return out

_P = re.compile(r"[\(\[]")
def _static(df, meta):
    m = meta.reindex(df.trackId.values)
    nm = df.trackName.fillna("").values
    alb = m.albumName.fillna("").values
    o = pd.DataFrame(index=range(len(df)))
    o["pop"] = m.popularity.values; o["dur"] = m.durationMs.values / 1000.0; o["expl"] = m.explicit.astype(float).values
    o["nart"] = [len(a) for a in df.artistIds]; o["tlen"] = [len(x) for x in nm]
    o["paren"] = [1.0 if _P.search(x) else 0.0 for x in nm]
    o["dash"] = [1.0 if " - " in x else 0.0 for x in nm]
    o["t_eq_a"] = [1.0 if x.lower() == y.lower() else 0.0 for x, y in zip(nm, alb)]
    o["prev"] = m.previewUrl.notna().astype(float).values
    o["nonascii"] = [sum(ord(c) > 127 for c in x) / (len(x) + 1) for x in nm]
    o["nwords"] = [len(x.split()) for x in nm]
    o["alen"] = [len(x) for x in alb]
    o["feat"] = [1.0 if re.search(r"feat\.|ft\.|with ", x.lower()) else 0.0 for x in nm]
    return o

def _fit(train, meta, cutoff):
    train = train.sort_values("t", kind="stable").reset_index(drop=True)
    st = song_table(train)
    H = Hist(train, st)
    ex = st[st["first"] < cutoff - pd.Timedelta(days=90)]
    ex = ex[ex["first"] > train.t.min() + pd.Timedelta(days=45)].copy()
    ex["trackName"] = ex.trackName.fillna("")
    rows = [H.row(a, al, d) for a, al, d in zip(ex.artistIds, ex.albumId, _days(ex["first"]))]
    Ej = _emb_for(st.trackId.values, meta); fj = _days(st["first"]); lj = st.love.values; pj = st.plays90.values
    Ee = _emb_for(ex.trackId.values, meta)
    A = aud_feats(Ee, _days(ex["first"]), Ej, fj, lj, pj)
    X = pd.concat([pd.DataFrame(rows).reset_index(drop=True), _static(ex.reset_index(), meta), pd.DataFrame(A, columns=AUD_COLS)], axis=1)
    y = ex.love.values
    age = (cutoff - ex["first"]).dt.days.values
    w = 0.5 ** (age / 500.0) + 0.1
    params = dict(objective="binary", learning_rate=0.03, num_leaves=7, min_data_in_leaf=60, feature_fraction=0.7, bagging_fraction=0.8,
                  bagging_freq=1, lambda_l2=10.0, num_threads=1, verbose=-1, seed=1)
    models = [lgb.train({**params, "seed": s}, lgb.Dataset(X, y, weight=w), num_boost_round=250) for s in range(3)]
    yr = np.log1p(ex.plays90.values.astype(float))
    reg = [lgb.train({**params, "objective": "regression", "seed": s}, lgb.Dataset(X, yr, weight=w), num_boost_round=250) for s in range(2)]
    pr = np.mean([m.predict(X) for m in reg], axis=0); rstat = (pr.mean(), pr.std() + 1e-6)
    pl = np.mean([m.predict(X) for m in models], axis=0); lg = np.log(pl / (1 - pl)); lstat = (lg.mean(), lg.std() + 1e-6)
    # logistic regression on whitened PCA audio of mature train songs
    lrm = None
    okj = ~np.isnan(Ej[:, 0]); matj = okj & (fj + 90 <= _days(pd.Series([cutoff]))[0])
    if matj.sum() > 200 and lj[matj].sum() > 20:
        from sklearn.decomposition import PCA; from sklearn.linear_model import LogisticRegression
        pca = PCA(48, whiten=True, random_state=0).fit(Ej[okj])
        ag = (_days(pd.Series([cutoff]))[0] - fj[matj]); sw = 0.5 ** (ag / 730.0)
        clf = LogisticRegression(C=0.05, max_iter=300).fit(pca.transform(Ej[matj]), lj[matj], sample_weight=sw)
        zt = clf.decision_function(pca.transform(Ej[matj])); lrm = (pca, clf, zt.mean(), zt.std() + 1e-6)
    return H, models, list(X.columns), (reg, rstat, lstat, lrm), (Ej, fj, lj, pj), (np.nanmean(X["au0"]), np.nanstd(X["au0"]) + 1e-6)

def predict(train, cands, meta, cutoff):
    key = (str(cutoff), len(train))
    if key not in _CACHE: _CACHE[key] = _fit(train, meta, cutoff)
    H, models, cols, ext, J, (m0, s0) = _CACHE[key]; reg, rstat, lstat, lrm = ext
    t = _days(pd.Series([cutoff]))[0]
    rows = [H.row(a, al, t) for a, al in zip(cands.artistIds, cands.albumId)]
    Eq = _emb_for(cands.trackId.values, meta)
    A = aud_feats(Eq, np.full(len(cands), t), *J)
    X = pd.concat([pd.DataFrame(rows).reset_index(drop=True), _static(cands.reset_index(drop=True), meta), pd.DataFrame(A, columns=AUD_COLS)], axis=1)
    X = X[cols]
    p = np.mean([m.predict(X) for m in models], axis=0)
    sc = np.log(p / (1 - p))
    # prominence prior: the open pool needs P(tried) as well as P(love | tried); BETA tuned (0 / 0.3 / 0.6) on dev open pool
    au = np.nan_to_num((X["au0"].values - m0) / s0, nan=0.0)
    out = sc
    if WREG:
        pr = np.mean([m.predict(X) for m in reg], axis=0)
        out = (sc - lstat[0]) / lstat[1] * 1.0 + WREG * (pr - rstat[0]) / rstat[1]
        out = out * lstat[1]
    if WLR and lrm is not None:
        pca, clf, a, b = lrm; z = np.zeros(len(X)); ok = ~np.isnan(Eq[:, 0])
        if ok.any(): z[ok] = (clf.decision_function(pca.transform(Eq[ok])) - a) / b
        out = out + WLR * z
    return out + BETA * np.log1p(X["ap90"].values + 0.3 * X["ap365"].values) + GAMMA * au
