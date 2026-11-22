"""w6r1-catalogue-context: does PUBLIC CATALOGUE CONTEXT (Deezer: release date, related-artist graph, popularity, genre) add to the incumbent content model?
Harness entry file (PREDICTORS dict).  Python from /home/user/Listener/taste-model.
Context model: L2 logistic regression fitted on TRAIN songs only: label = love (>=6 plays on >=3 distinct days within 90 d of first play, computed from the train streams) for songs
first played in the 730 days before cutoff-90d.  Features are evaluated at each song's first-play time using only listening before it (candidates: cutoff + 45 d).
Blend = ref_w4r1_listening (evalkit.refs.score, train-only) + LAMBDA * context logit / (sd of the context logit on training songs).  No artist id enters the incumbent.
Feature groups: age (release age at discovery), graph (related-artist graph proximity to recently played artists, own artist excluded), pop (Deezer rank, artist fans, rank within the
artist's top list: LOOK-AHEAD, measured 2026), genre (album genre ids), fam (own-artist decayed plays: familiarity control).
Catalogue records: dev = shared-w6r1/p1_records.csv keyed by trackId (+ artist_top cache); sealed era = records produced by catalogue/w6_fetch.py records into the same format
(env W6R1_CTX_EXTRA = extra records.csv paths, comma separated); tracks without a Deezer match get a neutral context logit (0).
FEATURES = ("mert", "deezer")"""
import os, sys, json, math
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model"
sys.path.insert(0, ROOT)
FEATURES = ("mert", "deezer")
_S = {}
GENRES = [85, 152, 132, 87, 86, 113, 522, 106, 154, 173, 174, 133]
HL = 180.0   # days, half-life of listening weights
GROUPS = {"age": ["age"], "graph": ["graph"], "pop": ["pop"], "genre": ["genre"], "fam": ["fam"]}
CFG = {
    "ctx_age": ("age",), "ctx_graph": ("graph",), "ctx_pop": ("pop",), "ctx_genre": ("genre",),
    "ctx_inv": ("age", "graph", "genre"), "ctx_all": ("age", "graph", "genre", "pop"), "ctx_inv_fam": ("age", "graph", "genre", "fam"),
}

def _records():
    if "R" in _S: return _S["R"]
    paths = [f"{ROOT}/.cache/shared-w6r1/p1_records.csv"] + [p for p in os.environ.get("W6R1_CTX_EXTRA", "").split(",") if p]
    R = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)
    R = R[R.status == "match"].drop_duplicates("trackId").copy()
    R["rel"] = pd.to_datetime(R[["dz_release_date", "album_release_date"]].apply(pd.to_datetime, errors="coerce").min(axis=1))
    R = R.set_index(R.trackId.astype("int64"))
    top = {}
    f = f"{ROOT}/.cache/w6r1-catalogue-context/artist_top.jsonl"
    if os.path.exists(f):
        for l in open(f):
            r = json.loads(l); top[r["artist_id"]] = {t[0]: i + 1 for i, t in enumerate(r["top"])}
    _S["R"] = R; _S["top"] = top
    return R

def _rel_ids(R, tid):
    s = R.at[tid, "artist_related_ids"]
    return set(int(x) for x in str(s).split("|") if x and x != "nan")

def _label_table(train, cutoff):
    """train songs with first play in [cutoff-730d, cutoff-90d), love label from train streams; first-play time"""
    g = train.groupby("song")
    first = g.t.min(); tid = g.trackId.first(); art = g.artist.first()
    ok = (first >= cutoff - pd.Timedelta(days=730)) & (first < cutoff - pd.Timedelta(days=90)) & (first >= pd.Timestamp("2020-09-01"))
    st = train[train.song.isin(first.index[ok])]
    f0 = st.song.map(first)
    w = st[(st.t < f0 + pd.Timedelta(days=90))]
    n = w.groupby("song").size(); d = w.assign(day=w.t.dt.floor("D")).groupby("song").day.nunique()
    out = pd.DataFrame({"t0": first[ok], "trackId": tid[ok], "artist": art[ok]})
    out["love"] = ((n.reindex(out.index).fillna(0) >= 6) & (d.reindex(out.index).fillna(0) >= 3)).astype(int)
    return out

class _Taste:
    """decayed play weight per harness artist as of time t, from train streams before t (monthly snapshots, built lazily)"""
    def __init__(self, train, R):
        self.tr = train[["t", "artist", "trackId"]]
        self.tt = self.tr.t.values.astype("datetime64[ns]"); self.snap = {}
        # harness artist -> Deezer artist id (from any matched track of that artist)
        m = self.tr.drop_duplicates("trackId"); m = m[m.trackId.isin(R.index)]
        self.a2d = {a: int(R.at[t, "dz_artist_id"]) for a, t in zip(m.artist.values, m.trackId.values)}
        self.related = {}
        for a, t in zip(m.artist.values, m.trackId.values): self.related[int(R.at[t, "dz_artist_id"])] = _rel_ids(R, t)
    def at(self, t):
        key = pd.Timestamp(t).to_period("M")
        if key not in self.snap:
            t0 = key.to_timestamp()
            m = self.tt < np.datetime64(t0)
            age = (np.datetime64(t0) - self.tt[m]).astype("timedelta64[D]").astype(float)
            w = 0.5 ** (age / HL)
            s = pd.Series(w).groupby(self.tr.artist.values[m]).sum()
            dz = {}
            for a, v in s.items():
                d = self.a2d.get(a)
                if d is not None: dz[d] = dz.get(d, 0.0) + v
            tot = float(s.sum()) or 1.0
            fwd = {d: v / tot for d, v in dz.items()}
            self.snap[key] = (s, fwd, tot)
        return self.snap[key]

def _feats(R, taste, tids, arts, trefs, groups):
    """feature matrix [n, k] for the given groups; rows without a record are NaN-free zeros plus mask has"""
    n = len(tids); has = np.array([t in R.index for t in tids]); cols = []; names = []
    top = _S["top"]
    rows = {}
    if "age" in groups:
        a = np.zeros(n)
        for i in np.where(has)[0]:
            r = R.at[tids[i], "rel"]; a[i] = (trefs[i] - r).days / 365.25 if pd.notna(r) else np.nan
        a = np.where(np.isnan(a), np.nanmedian(a[has]) if has.any() else 0, a)
        cols += [np.log1p(np.clip(a, 0, None)), (a < 0.25).astype(float), (a < 1).astype(float), (a < 3).astype(float), (a > 15).astype(float)]
    if "graph" in groups:
        g1 = np.zeros(n); g2 = np.zeros(n); g3 = np.zeros(n)
        for i in np.where(has)[0]:
            s, fwd, tot = taste.at(trefs[i]); c = int(R.at[tids[i], "dz_artist_id"]); rel = _rel_ids(R, tids[i])
            g1[i] = sum(fwd.get(x, 0.0) for x in rel if x != c)                                         # listening share inside c's related list
            g2[i] = sum(v for d, v in fwd.items() if d != c and c in taste.related.get(d, ()))           # listening share of artists that list c as related
            top20 = sorted(fwd, key=fwd.get, reverse=True)[:20]
            g3[i] = float(any((x in rel) or (c in taste.related.get(x, ())) for x in top20 if x != c))
        cols += [np.log1p(100 * g1), np.log1p(100 * g2), g3]
    if "pop" in groups:
        rk = np.zeros(n); fan = np.zeros(n); wa = np.zeros(n)
        for i in np.where(has)[0]:
            rk[i] = np.log1p(R.at[tids[i], "dz_rank"] if pd.notna(R.at[tids[i], "dz_rank"]) else 0)
            fan[i] = np.log1p(R.at[tids[i], "artist_nb_fan"] if pd.notna(R.at[tids[i], "artist_nb_fan"]) else 0)
            tp = top.get(int(R.at[tids[i], "dz_artist_id"])); wa[i] = np.log(tp.get(int(R.at[tids[i], "dz_id"]), 101)) if tp else np.log(101)
        cols += [rk, fan, wa]
    if "genre" in groups:
        G = np.zeros((n, len(GENRES) + 1))
        for i in np.where(has)[0]:
            ids = [int(x) for x in str(R.at[tids[i], "album_genre_ids"]).split("|") if x and x != "nan"]
            for x in ids: G[i, GENRES.index(x) if x in GENRES else len(GENRES)] = 1
        cols += list(G.T)
    if "fam" in groups:
        f = np.zeros(n)
        for i in range(n):
            s, fwd, tot = taste.at(trefs[i]); f[i] = np.log1p(s.get(arts[i], 0.0))
        cols += [f]
    return np.column_stack(cols), has

def _context(train, cands, cutoff, groups, C=0.1):
    """context logit for each candidate (0 where no Deezer record), standardised by the training-song logit sd"""
    from sklearn.linear_model import LogisticRegression
    R = _records(); taste = _Taste(train, R)
    lt = _label_table(train, cutoff)
    lt = lt[lt.trackId.isin(R.index)]
    if len(lt) < 60 or lt.love.nunique() < 2: return np.zeros(len(cands))
    Xt, _ = _feats(R, taste, lt.trackId.values, lt.artist.values, list(lt.t0), groups)
    tids = cands.trackId.values.astype(np.int64); Xc, has = _feats(R, taste, tids, cands.artist.values, [pd.Timestamp(cutoff) + pd.Timedelta(days=45)] * len(tids), groups)
    mu, sd = Xt.mean(0), Xt.std(0) + 1e-9
    lr = LogisticRegression(C=C, max_iter=500).fit((Xt - mu) / sd, lt.love.values)
    zt = lr.decision_function((Xt - mu) / sd); zc = lr.decision_function((Xc - mu) / sd)
    z = (zc - zt.mean()) / (zt.std() + 1e-9); z[~has] = 0.0
    return z

def _inc(train, cands, meta, cutoff):
    from evalkit import refs
    return np.asarray(refs.score("ref_w4r1_listening", train, cands, meta, cutoff), float)

def _make(name, groups, lam):
    def fn(train, cands, meta, cutoff):
        z = _context(train, cands, pd.Timestamp(cutoff), groups)
        s = z if lam is None else _inc(train, cands, meta, cutoff) + lam * z
        assert np.isfinite(s).all()
        return s
    fn.__name__ = name; return fn

PREDICTORS = {}
for k, g in CFG.items(): PREDICTORS[k] = _make(k, g, None)
PREDICTORS.update({
    "blend_inv": _make("blend_inv", CFG["ctx_inv"], 1.0), "blend_all": _make("blend_all", CFG["ctx_all"], 1.0),
    "blend_inv_half": _make("blend_inv_half", CFG["ctx_inv"], 0.5), "blend_age": _make("blend_age", CFG["ctx_age"], 1.0),
    "blend_graph": _make("blend_graph", CFG["ctx_graph"], 1.0),
    "blend_inv_q": _make("blend_inv_q", CFG["ctx_inv"], 0.25), "blend_all_q": _make("blend_all_q", CFG["ctx_all"], 0.25),
    "blend_graph_q": _make("blend_graph_q", CFG["ctx_graph"], 0.25), "blend_all_half": _make("blend_all_half", CFG["ctx_all"], 0.5),
})

# ---- single-feature diagnostics (raw standardisation-free scores; sign = 'larger = more likely loved' only by convention, AUC < 0.5 means the opposite) ----
def _raw(name):
    def fn(train, cands, meta, cutoff):
        R = _records(); taste = _Taste(train, R); tids = cands.trackId.values.astype(np.int64)
        if name == "has": return np.array([float(t in R.index) for t in tids])
        grp = {"age": "age", "g1": "graph", "g2": "graph", "g3": "graph", "rank": "pop", "fan": "pop", "wa": "pop", "fam": "fam"}[name]
        X, has = _feats(R, taste, tids, cands.artist.values, [pd.Timestamp(cutoff) + pd.Timedelta(days=45)] * len(tids), (grp,))
        col = {"age": 0, "g1": 0, "g2": 1, "g3": 2, "rank": 0, "fan": 1, "wa": 2, "fam": 0}[name]
        x = X[:, col].astype(float); x = np.where(has, x, np.nan); m = np.nanmedian(x) if has.any() else 0
        return np.where(has, x, m) + 1e-9 * np.arange(len(x))
    return fn
for _k in ("has", "age", "g1", "g2", "g3", "rank", "fan", "wa", "fam"): PREDICTORS["raw_" + _k] = _raw(_k)

WALKFORWARD_FAMILY = ["blend_inv", "blend_all", "blend_inv_half", "blend_inv_q", "blend_all_q", "blend_graph_q", "blend_all_half"]
