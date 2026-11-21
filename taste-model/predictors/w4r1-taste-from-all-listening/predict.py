"""w4r1-taste-from-all-listening: content-only taste model trained on the WHOLE pre-cutoff listening record.  Harness entry file.
Usage (from /home/user/Listener/taste-model):  python3 -W ignore -m evalkit.run --fast predictors/w4r1-taste-from-all-listening/predict.py

Inputs per candidate: ONLY cached per-clip content (MERT / CLAP / essentia heads+embedding of the preview; lyrics embedding).  No artist id, no artist history.
The listening record (streams < cutoff) is used ONLY to build per-song training targets and weights ("signal"):
  panel signal : for each of K consecutive periods of P days before the cutoff, every song played in that period gets target = percentile rank of its
                 (valid) plays in that period among the songs played then (old or new songs alike); rows weighted by recency 0.5**(age/hl).
  new signal   : W3-style target for songs first played >=90 d before cutoff: percentile of plays90 within the quarter of first play.
Both signals are accumulated per song as sufficient statistics of one weighted ridge (normal equations), so a candidate's own artist can be
removed from the training signal exactly (variants named *_noart: score of candidate c uses the ridge refit without every training song of c's primary artist).
Transforms (standardiser, PCA) are fit on train-stream songs only.  No audio -> block contributes zeros (train mean); no block at all -> neutral score.
"""
import hashlib
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"
_S = {}

def _store():
    if "c" not in _S:
        z = np.load(ROOT + ".cache/w4r1/compact.npz")
        _S["c"] = {k: z[k] for k in z.files}; _S["idx"] = {k: i for i, k in enumerate(_S["c"]["md5"])}
        import pickle
        _S["lyr"] = pickle.load(open(ROOT + ".cache/shared/w4-lyrics/emb.pkl", "rb"))
    return _S

CFG = dict(blocks=("mert",), ncomp=64, alpha=300.0, signal="panel", K=8, P=91, hl=180.0, newhl=120.0, w_new=1.0, w_panel=1.0, valid_ms=0,
           tgt="rank", minplays=1, prune=0, noart=False, mode="whole", learner="ridge", k=50, tau=0.1, wt=1.0, zw=0.0)

def _raw_block(name, tids, meta):
    S = _store(); n = len(tids)
    if name == "lyr":
        L = S["lyr"]; X = np.zeros((n, 384), np.float32); has = np.zeros(n, bool)
        for i, t in enumerate(tids):
            v = L.get(int(t));
            if v is not None: X[i] = v; has[i] = True
        return X, has
    u = meta.previewUrl.reindex(tids).values
    ii = np.array([S["idx"].get(hashlib.md5(x.encode()).hexdigest(), -1) if isinstance(x, str) else -1 for x in u]); C = S["c"]
    if name == "mert": has = ii >= 0; X = np.zeros((n, 4, 768), np.float32); X[has] = C["mert"][ii[has]].astype(np.float32); has &= C["has_mert"][np.maximum(ii, 0)]
    elif name == "clap": has = (ii >= 0) & C["has_clap"][np.maximum(ii, 0)]; X = np.zeros((n, 768), np.float32); X[has] = C["clap"][ii[has]].astype(np.float32)
    elif name == "ess": has = (ii >= 0) & C["has_ess"][np.maximum(ii, 0)]; X = np.zeros((n, 605), np.float32); X[has] = C["ess_act"][ii[has]].astype(np.float32)
    elif name == "esse": has = (ii >= 0) & C["has_ess"][np.maximum(ii, 0)]; X = np.zeros((n, 1280), np.float32); X[has] = C["ess_emb"][ii[has]].astype(np.float32)
    else: raise ValueError(name)
    has &= np.isfinite(X).reshape(n, -1).all(1); X[~has] = 0
    return X, has

def _design(res, tids, meta, cfg):
    """[n*rep, d] design (rep = 4 windows in local mode, else 1), any-block-present mask [n]"""
    parts, anyhas, n = [], np.zeros(len(tids), bool), len(tids); local = cfg["mode"] == "local"; rep = 4 if local else 1
    for b, (mu, sd, pca) in zip(cfg["blocks"], res["tf"]):
        X, has = _raw_block(b, tids, meta)
        if X.ndim == 3:
            if local: P = pca.transform(((X - mu) / sd).reshape(n * 4, -1)); P[np.repeat(~has, 4)] = 0
            else: P = pca.transform(((X.mean(1) - mu) / sd)); P[~has] = 0
        else:
            P = pca.transform((X - mu) / sd); P[~has] = 0
            if local: P = np.repeat(P, 4, 0)
        parts.append(P); anyhas |= has
    return np.concatenate(parts, 1), anyhas

def _pct(vals, groups):
    return pd.Series(vals).groupby(groups).rank(pct=True).values

def _signal(train, st, cutoff, cfg):
    """per-song sufficient statistics: W (weight sum) and Y (weight*target sum) over rows of the chosen signals."""
    idx = {s: i for i, s in enumerate(st.index)}; n = len(st); W = np.zeros(n); Y = np.zeros(n)
    d = train
    if cfg["valid_ms"]: d = d[d.playedMs >= cfg["valid_ms"]]
    si = d.song.map(idx).values; ok = ~pd.isna(si); si = si[ok].astype(int); tt = d.t.values[ok]
    if cfg["signal"] in ("panel", "both"):
        for k in range(cfg["K"]):
            e = cutoff - pd.Timedelta(days=cfg["P"] * k); s0 = e - pd.Timedelta(days=cfg["P"])
            m = (tt >= np.datetime64(s0)) & (tt < np.datetime64(e))
            if m.sum() == 0: continue
            cnt = np.bincount(si[m], minlength=n); pl = cnt >= cfg["minplays"]
            if pl.sum() < 20: continue
            if cfg["zw"] > 0:   # also use active-but-unplayed songs (first play before the period end) as low-rank rows with weight zw
                act = (st["first"].values < np.datetime64(e)); allr = act & (cnt >= 0); y = np.zeros(n); y[allr] = _pct(cnt[allr], np.zeros(allr.sum()))
                w = cfg["w_panel"] * 0.5 ** (cfg["P"] * (k + 0.5) / cfg["hl"]) * (pl + cfg["zw"] * (act & ~pl)); W += w; Y += w * y; continue
            if cfg["tgt"] == "rank": y = np.zeros(n); y[pl] = _pct(cnt[pl], np.zeros(pl.sum()))
            else: y = np.zeros(n); y[pl] = np.log1p(cnt[pl]); y[pl] = (y[pl] - y[pl].mean()) / (y[pl].std() + 1e-9) * 0.29 + 0.5
            w = cfg["w_panel"] * 0.5 ** (cfg["P"] * (k + 0.5) / cfg["hl"]) * pl
            W += w; Y += w * y
    if cfg["signal"] in ("new", "both"):
        fi = st["first"]; mat = (fi < cutoff - pd.Timedelta(days=90)).values
        p90 = st.plays90.values
        if cfg["valid_ms"]:   # valid plays inside 90 days of first play
            first = st["first"].reindex(d.song).values; dd = d[(d.t.values < first + np.timedelta64(90, "D"))]
            p90 = dd.groupby("song").size().reindex(st.index).fillna(0).values
        qa = fi.dt.to_period("Q").astype(str).values
        y = np.zeros(n); y[mat] = _pct(p90[mat], qa[mat])
        w = cfg["w_new"] * (0.5 ** ((cutoff - fi).dt.days.values / cfg["newhl"]) if cfg["newhl"] else 1.0) * mat
        W += w; Y += w * y
    return W, Y

def _fit(train, meta, cutoff, cfg):
    from sklearn.decomposition import PCA
    from threadpoolctl import threadpool_limits
    from evalkit.data import song_table
    st = song_table(train); st = st[st.trackId.isin(meta.index)]
    tids = st.trackId.values; art = st.artist.values
    with threadpool_limits(2):
        tf = []
        for b in cfg["blocks"]:
            X, has = _raw_block(b, tids, meta); Xo = X[has]
            if Xo.ndim == 3 and cfg["mode"] != "local": Xo = Xo.mean(1)
            else: Xo = Xo.reshape(-1, Xo.shape[-1]) if Xo.ndim == 3 else Xo
            mu = Xo.mean(0); sd = Xo.std(0) + 1e-6
            nc = min(cfg["ncomp"], max(2, has.sum() - 1)); pca = PCA(nc, whiten=True, random_state=0).fit((Xo - mu) / sd); tf.append((mu, sd, pca))
        res = dict(tf=tf); P, has = _design(res, tids, meta, cfg)
        W, Y = _signal(train, st, cutoff, cfg)
        keep = has & (W > 0)
        if cfg["prune"]: keep &= W > np.quantile(W[W > 0], cfg["prune"])
        rep = 4 if cfg["mode"] == "local" else 1; kr = np.repeat(keep, rep)
        P = P[kr]; W, Y, art2 = np.repeat(W[keep], rep), np.repeat(Y[keep], rep), np.repeat(art[keep], rep)
        sc = W.sum(); ws = W * len(W) / sc; Yn = Y / W            # mean weight 1 per row
        if cfg["learner"] == "knn":
            Pn = P / (np.linalg.norm(P, axis=1, keepdims=True) + 1e-9); res.update(Pn=Pn.astype(np.float32), ws=ws, Yn=Yn, art=art2)
            sa = _knn(res, Pn.astype(np.float32), None, cfg, self_excl=True); res["tm"], res["ts"] = float(sa.mean()), float(sa.std() + 1e-9); return res
        Xa = np.c_[P, np.ones(len(P))]; reg = np.eye(Xa.shape[1]) * cfg["alpha"]; reg[-1, -1] = 1e-6
        A = (Xa * ws[:, None]).T @ Xa; b = (Xa * (ws * Yn)[:, None]).T @ Xa[:, :0] if False else (Xa * (ws * Yn)[:, None]).sum(0)
        res.update(A=A, b=b, reg=reg, beta=np.linalg.solve(A + reg, b))
        if cfg["noart"]:   # per-artist normal-equation blocks for exact leave-artist-out refits
            g = pd.Series(np.arange(len(P))).groupby(art2).apply(lambda s: s.values)
            res["ablocks"] = {a: ((Xa[i] * ws[i, None]).T @ Xa[i], (Xa[i] * (ws[i] * Yn[i])[:, None]).sum(0)) for a, i in g.items()}
        s = (Xa @ res["beta"]).reshape(-1, rep).mean(1); res["tm"], res["ts"] = float(s.mean()), float(s.std() + 1e-9)
    return res

_CACHE = {}
def _get(train, meta, cutoff, cfg):
    import os
    key = (str(cutoff), len(train), hashlib.md5(pd.util.hash_pandas_object(train[["trackId", "song", "artist"]].astype(str), index=False).values.tobytes()).hexdigest(),
           hashlib.md5(train.t.values.tobytes()).hexdigest(), repr(sorted(cfg.items())))
    if key in _CACHE and not os.environ.get("EVALKIT_NO_FIT_CACHE"): return _CACHE[key]
    r = _fit(train, meta, cutoff, cfg); _CACHE[key] = r; return r

def _knn(res, Q, qart, cfg, self_excl=False):
    """Nadaraya-Watson over the top-k most similar training songs (cosine in the whitened PCA space); same-artist training songs excluded when qart is given."""
    out = np.zeros(len(Q), np.float32); T = res["Pn"]; k = cfg["k"]
    for i0 in range(0, len(Q), 512):
        S = Q[i0:i0 + 512] @ T.T
        if self_excl: S[np.arange(S.shape[0]), np.arange(i0, i0 + S.shape[0])] = -9
        if qart is not None: S[qart[i0:i0 + 512, None] == res["art"][None, :]] = -9
        idx = np.argpartition(-S, k, axis=1)[:, :k]; sv = np.take_along_axis(S, idx, 1)
        w = np.exp((sv - sv.max(1, keepdims=True)) / cfg["tau"]) * res["ws"][idx]; out[i0:i0 + 512] = (w * res["Yn"][idx]).sum(1) / (w.sum(1) + 1e-12)
    return out

def _score(res, cands, meta, cfg):
    if cfg["learner"] == "knn":
        P, has = _design(res, cands.trackId.values, meta, cfg); Pn = (P / (np.linalg.norm(P, axis=1, keepdims=True) + 1e-9)).astype(np.float32)
        s = _knn(res, Pn, cands.artist.values if cfg["noart"] else None, cfg); s = (s - res["tm"]) / res["ts"]; s[~has] = 0.0; return s
    n = len(cands); rep = 4 if cfg["mode"] == "local" else 1
    P, has = _design(res, cands.trackId.values, meta, cfg); Xa = np.c_[P, np.ones(len(P))]; s = Xa @ res["beta"]
    if cfg["noart"]:
        art = np.repeat(cands.artist.values, rep)
        for a in np.unique(art):
            if a not in res["ablocks"]: continue
            Aa, ba = res["ablocks"][a]; beta = np.linalg.solve(res["A"] - Aa + res["reg"], res["b"] - ba); m = art == a; s[m] = Xa[m] @ beta
    s = s.reshape(n, rep).mean(1)
    s = (s - res["tm"]) / res["ts"]; s[~has] = 0.0   # train-song mean score as neutral
    return s

def make(*members, **kw):
    """standardised mean of one or more configs (each member: dict overriding CFG)"""
    cfgs = [{**CFG, **kw, **m} for m in (members or [{}])]
    def predict(train, cands, meta, cutoff):
        return np.average([_score(_get(train, meta, cutoff, c), cands, meta, c) for c in cfgs], axis=0, weights=[c["wt"] for c in cfgs])
    return predict

E = dict(mode="local", alpha=1200.0); W32 = dict(ncomp=32, alpha=150.0)
N0 = dict(signal="new", newhl=None)
def PM(**kw): return make(dict(E, **kw), dict(W32, **kw))
PN = [dict(E, **N0), dict(W32, **N0)]
def PK(extra=None, **kw): return [dict(E, K=2, minplays=2, **kw), dict(W32, K=2, minplays=2, **kw)]
def blk(ms, bl, nc): return [dict(m, blocks=bl, ncomp=nc if m is E else nc // 2) for m in ms]
PREDICTORS = {
 "ens3_k1": make(*PN, *PK(), dict(E, K=1, minplays=2), dict(W32, K=1, minplays=2)),
 "joint_k2m2": make(dict(E, signal="both", newhl=None, K=2, minplays=2), dict(W32, signal="both", newhl=None, K=2, minplays=2)),
 "ens_pan_ess": make(*PN, *blk(PK(), ("mert", "ess"), 48)),
 "ens_pan_clap": make(*PN, *blk(PK(), ("mert", "clap"), 48)),
 "ens_pan_w2": make(*PN, *[dict(m, wt=2.0) for m in PK()]),
 "ens_pan_hl90": make(*PN, *PK(hl=90.0)),
 "ens_new_ess": make(*blk(PN, ("mert", "ess"), 48), *PK()),
 "ens_pan_lyr": make(*PN, *blk(PK(), ("mert", "lyr"), 48)),
}
