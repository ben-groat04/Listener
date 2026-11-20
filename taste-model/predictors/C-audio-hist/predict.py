"""Predictor C: behavioural-history + pretrained-text-semantics model, trained on pseudo-folds carved out of the visible history.
For every pseudo cutoff c' in the visible past (c' <= cutoff - 6 months so the 90-day love label is fully observed) it builds the same
candidate set the harness uses (songs first played in [c', c'+3m)), features from streams < c' only, and the love label.
A LightGBM model fit on those rows scores the real candidates. Model + feature tables are cached by cutoff (independence gate).
"""
import os, sys, hashlib, pickle
from pathlib import Path
import numpy as np, pandas as pd

OUT = Path("/home/user/Listener/taste-model/.cache/shared/C-textemb-v1"); EMB_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
W0 = 0.5; LAM = 0.5
_E = {}; _MODEL = []; _FIT = {}
CLAP = Path("/home/user/Listener/taste-model/.cache/shared/clap-preview-emb/emb.pkl")   # {previewUrl: 768-d} (built by B-audio/build_*.py)
HAND = Path("/home/user/Listener/taste-model/.cache/shared/hand-audio-feat-v1/feat.pkl")  # {previewUrl: 93-d handcrafted}
USE = dict(clap=True, hand=True, text=True, pcs=8)
for _kv in os.environ.get("C_USE", "").split(","):
    if "=" in _kv: _k, _v = _kv.split("="); USE[_k] = int(_v)
TARGET = os.environ.get("C_TARGET", "love"); LAM_ENV = float(os.environ.get("C_LAM", "1.0"))
def _aud():
    if "aud" not in _E:
        try:
            cl = pickle.load(open(CLAP, "rb")); hd = pickle.load(open(HAND, "rb"))
        except Exception: cl, hd = {}, {}
        urls = sorted(set(cl) & set(hd))
        C = np.stack([cl[u] for u in urls]).astype(np.float32) if urls else np.zeros((0, 768), np.float32)
        H = np.stack([hd[u] for u in urls]).astype(np.float32) if urls else np.zeros((0, 93), np.float32)
        C = C / np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-9)
        mu, sd = H.mean(0), H.std(0) + 1e-6; Hz = (H - mu) / sd
        U, S, Vt = np.linalg.svd(Hz - Hz.mean(0), full_matrices=False) if len(Hz) else (None, None, np.zeros((16, 93)))
        P = (Hz @ Vt[:24].T); P = P / np.maximum(np.linalg.norm(P, axis=1, keepdims=True), 1e-9)   # PCA-24 of handcrafted, unit norm
        Cc = C - C.mean(0); Uc, Sc, Vc = np.linalg.svd(Cc, full_matrices=False) if len(C) else (None, None, np.zeros((16, 768)))
        Pc = Cc @ Vc[:16].T / (Sc[:16] / np.sqrt(max(1, len(C))))   # whitened first 16 PCs of CLAP
        _E["aud"] = dict(idx={u: i for i, u in enumerate(urls)}, C=C, H=P, Pc=Pc.astype(np.float32))
    return _E["aud"]


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

def _sim_features(hist, cemb, has, c, Ehist, pre, Ts=(0.05, 0.1), beta=None):
    """similarity of candidates (cemb rows, valid where has) to the user's loved / recent / all songs at cutoff c, using vectors Ehist[song]."""
    n = len(cemb); names = ["cen_lov", "cen_r180", "cen_r45", "cen_all", "nn5_lov", "nn5_all", "nn5_r180", "nn1_all", "den", "den180"] + \
        [f"klove{T}" for T in Ts] + [f"kr180_{T}" for T in Ts] + ["nn5_lov_m_all"]
    g = hist.groupby("song"); tot = g.size(); days = g.day.nunique()
    r180 = hist[hist.t >= c - pd.Timedelta(days=180)].groupby("song").size().reindex(tot.index).fillna(0)
    r45 = hist[hist.t >= c - pd.Timedelta(days=45)].groupby("song").size().reindex(tot.index).fillna(0)
    idx = [s for s in tot.index if s in Ehist]
    out = {k: np.full(n, np.nan) for k in names}
    if len(idx) < 5 or not has.any(): return pd.DataFrame({pre + k: v for k, v in out.items()})
    H = np.stack([Ehist[s] for s in idx]); tt = tot.reindex(idx).values; dd = days.reindex(idx).values
    lov = ((tt >= 6) & (dd >= 3)).astype(float); w180 = r180.reindex(idx).values; w45 = r45.reindex(idx).values
    Sim = cemb[has] @ H.T; m = has.sum(); o = {}
    for nm, w in (("lov", lov), ("r180", w180), ("r45", w45), ("all", np.log1p(tt))):
        W = w / w.sum() if w.sum() > 0 else np.zeros_like(w); o["cen_" + nm] = (Sim * W[None, :]).sum(1)
    def topk(mask, k):
        if mask.sum() == 0: return np.full(m, np.nan)
        S = np.where(mask[None, :], Sim, -9); kk = min(k, int(mask.sum())); return np.sort(S, 1)[:, -kk:].mean(1)
    o["nn5_lov"] = topk(lov > 0, 5); o["nn5_all"] = topk(np.ones(len(idx), bool), 5); o["nn5_r180"] = topk(w180 > 0, 5); o["nn1_all"] = topk(np.ones(len(idx), bool), 1)
    o["nn5_lov_m_all"] = o["nn5_lov"] - o["nn5_all"]
    sc = (Sim.max() - Sim.min()) if beta is None else None
    for nm, w in (("den", np.log1p(tt)), ("den180", np.log1p(w180))):
        K = np.exp(10 * (Sim - 1)) if beta is None else np.exp(beta * (Sim - 1)); o[nm] = np.log((K * w[None, :]).sum(1) + 1e-6)
    for T in Ts:
        K = np.exp((Sim - Sim.max(1, keepdims=True)) / T); o[f"klove{T}"] = (K * lov[None, :]).sum(1) / K.sum(1); o[f"kr180_{T}"] = (K * np.log1p(w180)[None, :]).sum(1) / K.sum(1)
    for k, v in o.items(): out[k][has] = v
    return pd.DataFrame({pre + k: v for k, v in out.items()})

def _text_vecs(songs_names): return embed(songs_names)

def _aud_vec(trackIds, meta, kind):
    A = _aud(); urls = meta.previewUrl.reindex(list(trackIds)).values
    ix = np.array([A["idx"].get(u, -1) if isinstance(u, str) else -1 for u in urls]); has = ix >= 0
    M = A[kind]; V = np.zeros((len(ix), M.shape[1]), np.float32); V[has] = M[ix[has]]
    return V, has

def _audio_block(hist, cand, meta, c, Eaud, spmeta=None):
    """audio similarity features for candidate rows + raw PCs."""
    parts = []
    if USE["clap"]:
        V, has = _aud_vec(cand.trackId.values, meta, "C"); parts.append(_sim_features(hist, V, has, c, Eaud["C"], "ac_"))
    if USE["hand"]:
        V, has = _aud_vec(cand.trackId.values, meta, "H"); parts.append(_sim_features(hist, V, has, c, Eaud["H"], "ah_", beta=5.0))
    if USE["pcs"]:
        V, has = _aud_vec(cand.trackId.values, meta, "Pc"); V = V[:, :USE["pcs"]].astype(float); V[~has] = np.nan
        parts.append(pd.DataFrame(V, columns=[f"pc{i}" for i in range(V.shape[1])]))
    return pd.concat(parts, axis=1) if parts else pd.DataFrame(index=range(len(cand)))

def _song_aud(sp_all, meta):
    E = {}
    for kind in ("C", "H"):
        V, has = _aud_vec(sp_all.trackId.values, meta, kind); E[kind] = {s: V[i] for i, s in enumerate(sp_all.index) if has[i]}
    return E

def _sem_features(hist, cand, cemb, anm, c, sp_rep, Ehist):
    return _sim_features(hist, cemb, np.ones(len(cemb), bool), c, Ehist, "tx_")

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
    Ea = _song_aud(sp_all, meta)
    start = tr.t.min() + pd.Timedelta(days=150)
    last_c = pd.Timestamp(cutoff) - pd.DateOffset(months=3) - pd.Timedelta(days=90)
    rows, cs = [], []
    c = pd.Timestamp(start.date())
    while c <= last_c:
        hist = tr[tr.t < c]
        f = sp_all[(sp_all["first"] >= c) & (sp_all["first"] < c + pd.DateOffset(months=3))]
        if len(f) >= 5:
            isd = np.zeros(len(f))
            cand = f.reset_index()[["song", "trackId", "albumId", "artist", "artistIds", "trackName"]]
            X = _features(hist, meta, cand, c, anm, None)
            cemb = np.stack([E[s] for s in cand.song])
            Xs = _sem_features(hist, cand, cemb, anm, c, sp_all, E) if USE["text"] else pd.DataFrame(index=range(len(cand)))
            Xa = _audio_block(hist, cand, meta, c, Ea)
            X = pd.concat([X, Xs, Xa], axis=1); X["y"] = f.love.values * (1 - isd); X["lp"] = np.log1p(f.plays90.values) + 0.5 * np.log1p(f.days90.values); X["dec"] = isd; X["cut"] = c; X["age"] = (pd.Timestamp(cutoff) - c).days
            X["song"] = f.index.values
            rows.append(X)
        c += pd.Timedelta(days=step_days)
    return pd.concat(rows, ignore_index=True), tr, (E, Ea)

def _fit(train, meta, cutoff):
    import lightgbm as lgb
    key = (str(cutoff), len(train), int(train.t.max().value))
    if key in _FIT: return _FIT[key]
    # artist names need meta of train tracks; a singleton call restricts meta to train tracks + candidate, so this is complete for train
    anm = _artist_names(train, train.iloc[:0].assign(trackId=[]) if False else pd.DataFrame(dict(trackId=[], artist=[])), meta)
    D, tr, E = _pseudo(train, meta, anm, cutoff)
    feats = [c for c in D.columns if c not in ("y", "cut", "age", "song", "dec", "lp")]
    w = np.exp(-D.age.values / 900.0)  # mild recency weighting
    ms = []
    for seed in range(3):
        kw = dict(n_estimators=250, learning_rate=0.03, num_leaves=8, min_child_samples=30, subsample=0.8, subsample_freq=1,
                  colsample_bytree=0.7, reg_lambda=5.0, random_state=seed, n_jobs=1, verbose=-1)
        if TARGET in ("love", "both"):
            m = lgb.LGBMClassifier(**kw); m.fit(D[feats], D.y, sample_weight=w); ms.append(("c", m))
        if TARGET in ("reg", "both"):
            m = lgb.LGBMRegressor(**kw); m.fit(D[feats], D.lp, sample_weight=w); ms.append(("r", m))
    _FIT[key] = (ms, feats, anm, tr, E); return _FIT[key]

def predict(train, cands, meta, cutoff, lam=None, w0=None):
    ms, feats, anm, tr, E = _fit(train, meta, cutoff)
    c = pd.Timestamp(cutoff)
    anm2 = dict(anm)
    j = cands[["trackId", "artist"]].join(meta.artistNames, on="trackId")
    for a, n in zip(j.artist.values, j.artistNames.values):
        if isinstance(n, (list, tuple, np.ndarray)) and len(n) and a not in anm2: anm2[a] = str(n[0])
    X = _features(tr, meta, cands.reset_index(drop=True), c, anm2, None)
    names = (cands.artist.map(anm2).fillna("") + " - " + cands.trackName).tolist()
    cemb = embed(names)
    E, Ea = E
    Xs = _sem_features(tr, cands, cemb, anm2, c, None, E) if USE["text"] else pd.DataFrame(index=range(len(cands)))
    Xa = _audio_block(tr, cands.reset_index(drop=True), meta, c, Ea)
    X = pd.concat([X, Xs, Xa], axis=1)
    lg = lambda q: np.log(np.clip(q, 1e-4, 1 - 1e-4) / (1 - np.clip(q, 1e-4, 1 - 1e-4)))
    zs = []
    for kind in ("c", "r"):
        mm = [m for k_, m in ms if k_ == kind]
        if not mm: continue
        v = np.mean([lg(m.predict_proba(X[feats])[:, 1]) if kind == "c" else m.predict(X[feats]) for m in mm], axis=0)
        zs.append(v if kind == "c" else v * 1.5)   # regression output scaled to roughly logit units
    p = [np.mean(zs, axis=0)] * 2
    w0 = W0 if w0 is None else w0; lam = LAM if lam is None else lam
    fam = np.log1p(np.nan_to_num(X.a_n180.values) + 0.0)
    return w0 * p[0] + (1 - w0) * p[1] + lam * fam


PREDICTORS = {"C_audio_hist": lambda tr, ca, me, cu: predict(tr, ca, me, cu, lam=LAM_ENV, w0=1.0)}   # w0=1: love-among-tried head only (+ familiarity term); chosen on dev
