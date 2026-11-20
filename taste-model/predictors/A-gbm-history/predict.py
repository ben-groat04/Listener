"""A-gbm-history: supervised 'as-of' model. Train examples = songs the user first tried before cutoff-90d (label = love, computed
inside train only); features of each example are computed from streams strictly before that song's first play, so the model learns
P(love | what I knew about the user when the song first appeared). The same feature function is applied to candidates at t0=cutoff.
Features: multi-scale artist/album history, artist exploration and love-rate history, metadata, title/album-name cues, a hashed
char-ngram text model (out-of-fold stacked)."""
import numpy as np, pandas as pd, re, os
V=os.environ.get("AV","")
import lightgbm as lgb
from evalkit.data import song_table

_CACHE = {}
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

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
def _text(df, meta):
    m = meta.reindex(df.trackId.values)
    return [f"{a} | {b} | {', '.join(c) if isinstance(c, (list, np.ndarray)) else ''}" for a, b, c in zip(df.trackName.fillna(""), m.albumName.fillna(""), m.artistNames)]

def _fit_text(ex, meta, X_rows):
    txt = _text(ex.reset_index(), meta); y = ex.love.values
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=3, sublinear_tf=True, max_features=60000)
    M = vec.fit_transform(txt)
    oof = np.zeros(len(y)); grp = ex.artist.values
    for tr, te in GroupKFold(5).split(M, y, grp):
        oof[te] = LogisticRegression(C=0.3, max_iter=300).fit(M[tr], y[tr]).decision_function(M[te])
    clf = LogisticRegression(C=0.3, max_iter=300).fit(M, y)
    return vec, clf, oof

def _fit(train, meta, cutoff):
    train = train.sort_values("t", kind="stable").reset_index(drop=True)
    st = song_table(train)
    H = Hist(train, st)
    ex = st[st["first"] < cutoff - pd.Timedelta(days=90)]
    ex = ex[ex["first"] > train.t.min() + pd.Timedelta(days=45)].copy()
    ex["trackName"] = ex.trackName.fillna("")
    rows = [H.row(a, al, d) for a, al, d in zip(ex.artistIds, ex.albumId, _days(ex["first"]))]
    X = pd.concat([pd.DataFrame(rows).reset_index(drop=True), _static(ex.reset_index(), meta)], axis=1)
    y = ex.love.values
    tx = None
    if "T" in V:
        vec, clf, oof = _fit_text(ex, meta, None); X["txt"] = oof; tx = (vec, clf)
    age = (cutoff - ex["first"]).dt.days.values
    w = 0.5 ** (age / 500.0) + 0.1
    params = dict(objective="binary", learning_rate=0.03, num_leaves=7, min_data_in_leaf=60, feature_fraction=0.7, bagging_fraction=0.8,
                  bagging_freq=1, lambda_l2=10.0, num_threads=1, verbose=-1, seed=1)
    models = [lgb.train({**params, "seed": s}, lgb.Dataset(X, y, weight=w), num_boost_round=250) for s in range(3)]
    reg = []
    if "R" in V:
        yr = np.log1p(ex.plays90.values) + 0.5 * np.log1p(ex.days90.values)
        reg = [lgb.train({**params, "objective": "regression", "seed": s}, lgb.Dataset(X, yr, weight=w), num_boost_round=250) for s in range(3)]
    return H, (models, reg, tx), list(X.columns)

def predict(train, cands, meta, cutoff):
    key = (str(cutoff), len(train))
    if key not in _CACHE: _CACHE[key] = _fit(train, meta, cutoff)
    H, models, cols = _CACHE[key]
    models, reg, tx = models
    t = _days(pd.Series([cutoff]))[0]
    rows = [H.row(a, al, t) for a, al in zip(cands.artistIds, cands.albumId)]
    X = pd.concat([pd.DataFrame(rows).reset_index(drop=True), _static(cands.reset_index(drop=True), meta)], axis=1)
    if tx: X["txt"] = tx[1].decision_function(tx[0].transform(_text(cands.reset_index(drop=True), meta)))
    X = X[cols]
    from scipy.stats import rankdata
    p = np.mean([m.predict(X) for m in models], axis=0)
    sc = np.log(p / (1 - p))
    if reg:
        r = np.mean([m.predict(X) for m in reg], axis=0)
        sc = 0.5 * sc / 0.5 + 0.5 * r * 1.0   # crude blend of two comparably scaled scores
    beta = float(os.environ.get("AB", "0"))
    if beta: sc = sc + beta * np.log1p(X["ap90"].values + 0.3 * X["ap365"].values)
    return sc
