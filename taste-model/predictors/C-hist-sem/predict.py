"""Predictor C: behavioural-history + pretrained-text-semantics model, trained on pseudo-folds carved out of the visible history.
For every pseudo cutoff c' in the visible past (c' <= cutoff - 6 months so the 90-day love label is fully observed) it builds the same
candidate set the harness uses (songs first played in [c', c'+3m)), features from streams < c' only, and the love label.
A LightGBM model fit on those rows scores the real candidates. Model + feature tables are cached by cutoff (independence gate).
"""
import os, sys, hashlib, pickle
from pathlib import Path
import numpy as np, pandas as pd

OUT = Path("/home/user/Listener/taste-model/.cache/shared/C-textemb-v1"); EMB_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
_E = {}; _MODEL = []; _FIT = {}

# ------------------------------------------------------------------ text embeddings (persistent cache, regenerable)
def _load_emb():
    if "d" not in _E:
        p = OUT / "emb.pkl"
        try: _E["d"] = pickle.load(open(p, "rb"))
        except Exception: _E["d"] = {}
    return _E["d"]

def embed(strings):
    d = _load_emb(); miss = sorted({s for s in strings if s not in d})
    if miss:
        import torch; torch.set_num_threads(1)
        from transformers import AutoTokenizer, AutoModel
        if not _MODEL: _MODEL.append((AutoTokenizer.from_pretrained(EMB_MODEL), AutoModel.from_pretrained(EMB_MODEL).eval()))
        tok, mod = _MODEL[0]; V = []
        with torch.no_grad():
            for i in range(0, len(miss), 64):
                b = tok(miss[i:i + 64], padding=True, truncation=True, max_length=48, return_tensors="pt"); h = mod(**b).last_hidden_state
                m_ = b["attention_mask"].unsqueeze(-1).float(); e = (h * m_).sum(1) / m_.sum(1); V.append(torch.nn.functional.normalize(e, dim=-1).numpy())
        V = np.concatenate(V)
        for s, v in zip(miss, V): d[s] = v.astype(np.float16)
        OUT.mkdir(parents=True, exist_ok=True); tmp = OUT / f"emb.tmp{os.getpid()}"; pickle.dump(d, open(tmp, "wb")); os.replace(tmp, OUT / "emb.pkl")
    return np.stack([d[s] for s in strings]).astype(np.float32)

# ------------------------------------------------------------------ helpers
def _artist_names(train, cands, meta):
    """artist hash -> name (from meta.artistNames of tracks whose first artist it is)."""
    nm = {}
    for df in (train.drop_duplicates("trackId")[["trackId", "artist"]], cands[["trackId", "artist"]]):
        j = df.join(meta.artistNames, on="trackId")
        for a, n in zip(j.artist.values, j.artistNames.values):
            if isinstance(n, (list, tuple, np.ndarray)) and len(n) and a not in nm: nm[a] = str(n[0])
    return nm

def _song_table(tr):
    """per song: first play, rep row, plays/days in 90d."""
    tr = tr.assign(day=tr.t.dt.normalize())
    first = tr.groupby("song").t.transform("min")
    inh = tr[tr.t < first + pd.Timedelta(days=90)]
    st = inh.groupby("song").agg(plays90=("t", "size"), days90=("day", "nunique"))
    nmd = tr[tr.named] if tr.named.any() else tr
    rep = nmd.drop_duplicates("song")[["song", "trackId", "albumId", "artist", "artistIds", "trackName"]].set_index("song")
    rep = rep.join(tr.groupby("song").t.min().rename("first"))
    rep = rep.join(st); rep["love"] = ((rep.plays90 >= 6) & (rep.days90 >= 3)).astype(int)
    return rep

def _agg(df, key, c, pre):
    """stats of a grouping key over streams df (all < c)."""
    g = df.groupby(key)
    o = pd.DataFrame({pre + "n": g.size(), pre + "songs": g.song.nunique(), pre + "days": g.day.nunique(),
                      pre + "last": (c - g.t.max()).dt.total_seconds() / 86400, pre + "firstage": (c - g.t.min()).dt.total_seconds() / 86400,
                      pre + "comp": g.comp.mean()})
    for w in (14, 60, 180, 365):
        o[pre + f"n{w}"] = df[df.t >= c - pd.Timedelta(days=w)].groupby(key).size().reindex(o.index).fillna(0)
    return o

def _features(hist, meta, cand, c, anm, tot):
    """hist: streams < c (with day, comp). cand: DataFrame(song, trackId, albumId, artist, artistIds, trackName). Returns feature DataFrame."""
    X = pd.DataFrame(index=range(len(cand)))
    A = _agg(hist, "artist", c, "a_"); B = _agg(hist, "albumId", c, "b_")
    # song-level history of the artist: love rate of songs whose 90d window closed before c
    sd = _song_table(hist[hist.t < c - pd.Timedelta(days=90)]) if False else None
    S = hist.groupby("song").agg(n=("t", "size"), first=("t", "min"), art=("artist", "first"))
    S["old"] = S["first"] < c - pd.Timedelta(days=90)
    sp = _song_table(hist[hist.t < c]) ; sp["old"] = sp["first"] < c - pd.Timedelta(days=90)
    old = sp[sp.old]
    al = old.groupby("artist").agg(a_lr=("love", "mean"), a_lcnt=("love", "sum"), a_nold=("love", "size"), a_p90=("plays90", "mean"))
    sp["maxn"] = S.n.reindex(sp.index)
    am = sp.groupby("artist").agg(a_maxn=("maxn", "max"), a_medn=("maxn", "median"), a_ge3=("maxn", lambda s: (s >= 3).mean()))
    ab = old.groupby("albumId").agg(b_lr=("love", "mean"), b_lcnt=("love", "sum"))
    for T, k, cols in ((A, "artist", None), (al, "artist", None), (am, "artist", None), (B, "albumId", None), (ab, "albumId", None)):
        X = X.join(T.reindex(cand[k].values).reset_index(drop=True))
    # any-artist features for multi-artist tracks: max over listed artists of plays n180
    ai = cand.artistIds.map(lambda a: max([A.a_n180.get(x, 0) for x in a] + [0])).values; X["any_n180"] = ai
    X["a_share180"] = X.a_n180.fillna(0) / max(1, (hist.t >= c - pd.Timedelta(days=180)).sum())
    X["a_rank"] = X.a_n.rank(ascending=False).fillna(0) * 0 + pd.Series(cand.artist.values).map(A.a_n.rank(ascending=False)).fillna(9999).values
    X["rec_rate"] = (hist.t >= c - pd.Timedelta(days=30)).sum() / 30.0
    # meta
    m = meta.reindex(cand.trackId.values)
    X["pop"] = m.popularity.values; X["dur"] = m.durationMs.values; X["expl"] = m.explicit.astype(float).values
    X["nart"] = [len(a) for a in cand.artistIds]; X["ae"] = (m.albumName.fillna("").str.lower().values == cand.trackName.str.lower().values).astype(float)
    X["prev"] = m.previewUrl.notna().astype(float).values; X["tlen"] = cand.trackName.str.len().values
    tn = cand.trackName.str
    X["t_nonascii"] = tn.count(r"[^\x00-\x7f]").values / np.maximum(1, X.tlen); X["t_feat"] = tn.contains(r"(?i)feat|with ").astype(float).values
    return X

def _sem_features(hist, cand, cemb, anm, c, sp_rep, Ehist):
    """similarity of the candidate's text embedding to the user's loved / recent songs at cutoff c."""
    n = len(cand)
    # song weights: recent plays (last 180d) + log total plays; 'loved' songs = >=6 plays over >=3 days overall
    h = hist; g = h.groupby("song")
    tot = g.size(); days = g.day.nunique(); last = g.t.max()
    r180 = h[h.t >= c - pd.Timedelta(days=180)].groupby("song").size().reindex(tot.index).fillna(0)
    r45 = h[h.t >= c - pd.Timedelta(days=45)].groupby("song").size().reindex(tot.index).fillna(0)
    idx = [s for s in tot.index if s in Ehist]
    if not idx: return pd.DataFrame(np.zeros((n, 8)), columns=[f"sem{i}" for i in range(8)])
    H = np.stack([Ehist[s] for s in idx]); tt = tot.reindex(idx).values; dd = days.reindex(idx).values
    lov = ((tt >= 6) & (dd >= 3)).astype(float); w180 = r180.reindex(idx).values; w45 = r45.reindex(idx).values
    Sim = cemb @ H.T
    out = {}
    for nm, w in (("lov", lov), ("r180", w180), ("r45", w45), ("all", np.log1p(tt))):
        W = w / max(w.sum(), 1e-9) if w.sum() > 0 else np.zeros_like(w)
        out["cen_" + nm] = (Sim * W[None, :]).sum(1)                # kernel mean similarity
    # top-k nearest among loved / all
    def topk(mask, k):
        if mask.sum() == 0: return np.zeros(n)
        S = np.where(mask[None, :], Sim, -1); kk = min(k, int(mask.sum()))
        return np.sort(S, 1)[:, -kk:].mean(1)
    out["nn5_lov"] = topk(lov > 0, 5); out["nn5_all"] = topk(np.ones(len(idx), bool), 5); out["nn5_r180"] = topk(w180 > 0, 5)
    out["nn1_all"] = topk(np.ones(len(idx), bool), 1)
    # kernel-weighted love rate: softmax(sim/T) weights over previous songs, value = love
    for T in (0.05, 0.1):
        K = np.exp((Sim - Sim.max(1, keepdims=True)) / T); out[f"klove{T}"] = (K * lov[None, :]).sum(1) / K.sum(1)
        out[f"kr180_{T}"] = (K * np.log1p(w180)[None, :]).sum(1) / K.sum(1)
    return pd.DataFrame(out)

def _pseudo(train, meta, anm, cutoff, step_days=30):
    """Build training rows from pseudo-folds in the visible history."""
    tr = train.copy(); tr["day"] = tr.t.dt.normalize()
    mdur = meta.durationMs.reindex(tr.trackId.values).values
    tr["comp"] = np.minimum(1.5, tr.playedMs.values / np.where(np.isnan(mdur), np.nan, mdur))
    tr["comp"] = tr.comp.fillna(tr.comp.mean())
    tr["art_name"] = tr.artist.map(anm).fillna("")
    sp_all = _song_table(tr)
    sp_all["name"] = sp_all.artist.map(anm).fillna("") + " - " + sp_all.trackName
    E = dict(zip(sp_all.index, embed(sp_all.name.tolist())))
    start = tr.t.min() + pd.Timedelta(days=150)
    last_c = pd.Timestamp(cutoff) - pd.DateOffset(months=3) - pd.Timedelta(days=90)
    rows, cs = [], []
    c = pd.Timestamp(start.date())
    while c <= last_c:
        hist = tr[tr.t < c]
        f = sp_all[(sp_all["first"] >= c) & (sp_all["first"] < c + pd.DateOffset(months=3))]
        f = f[f.index.isin(set(tr.loc[tr.t < c + pd.DateOffset(months=3), "song"]))]
        if len(f) >= 5:
            cand = f.reset_index()[["song", "trackId", "albumId", "artist", "artistIds", "trackName"]]
            X = _features(hist, meta, cand, c, anm, None)
            cemb = np.stack([E[s] for s in cand.song])
            Xs = _sem_features(hist, cand, cemb, anm, c, sp_all, {k: v for k, v in E.items() if k in set(hist.song)})
            X = pd.concat([X, Xs], axis=1); X["y"] = f.love.values; X["cut"] = c; X["age"] = (pd.Timestamp(cutoff) - c).days
            X["song"] = f.index.values
            rows.append(X)
        c += pd.Timedelta(days=step_days)
    return pd.concat(rows, ignore_index=True), tr, E

def _fit(train, meta, cutoff):
    import lightgbm as lgb
    key = (str(cutoff), len(train), int(train.t.max().value))
    if key in _FIT: return _FIT[key]
    # artist names need meta of train tracks; a singleton call restricts meta to train tracks + candidate, so this is complete for train
    anm = _artist_names(train, train.iloc[:0].assign(trackId=[]) if False else pd.DataFrame(dict(trackId=[], artist=[])), meta)
    D, tr, E = _pseudo(train, meta, anm, cutoff)
    feats = [c for c in D.columns if c not in ("y", "cut", "age", "song")]
    w = np.exp(-D.age.values / 900.0)  # mild recency weighting
    ms = []
    for seed in range(3):
        m = lgb.LGBMClassifier(n_estimators=250, learning_rate=0.03, num_leaves=8, min_child_samples=30, subsample=0.8, subsample_freq=1,
                               colsample_bytree=0.7, reg_lambda=5.0, random_state=seed, n_jobs=1, verbose=-1)
        m.fit(D[feats], D.y, sample_weight=w); ms.append(m)
    _FIT[key] = (ms, feats, anm, tr, E); return _FIT[key]

def predict(train, cands, meta, cutoff):
    ms, feats, anm, tr, E = _fit(train, meta, cutoff)
    c = pd.Timestamp(cutoff)
    anm2 = dict(anm)
    j = cands[["trackId", "artist"]].join(meta.artistNames, on="trackId")
    for a, n in zip(j.artist.values, j.artistNames.values):
        if isinstance(n, (list, tuple, np.ndarray)) and len(n) and a not in anm2: anm2[a] = str(n[0])
    X = _features(tr, meta, cands.reset_index(drop=True), c, anm2, None)
    names = (cands.artist.map(anm2).fillna("") + " - " + cands.trackName).tolist()
    cemb = embed(names)
    Xs = _sem_features(tr, cands, cemb, anm2, c, None, E)
    X = pd.concat([X, Xs], axis=1)
    p = np.mean([m.predict_proba(X[feats])[:, 1] for m in ms], axis=0)
    return p
