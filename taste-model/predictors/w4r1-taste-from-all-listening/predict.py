"""w4r1-taste-from-all-listening: content-only taste model trained on the WHOLE pre-cutoff listening record.  Harness entry file.
Usage (from /home/user/Listener/taste-model; needs .cache/w4r1/compact.npz from build_compact.py):
    python3 -W ignore -m evalkit.run --fast predictors/w4r1-taste-from-all-listening/predict.py

Candidate input: ONLY the per-clip MERT-v1-95M features of the candidate's preview (4 windows, layers 4-8 averaged).  No artist id, no artist history,
no pool structure.  The listening record (streams < cutoff) is used ONLY to build per-song training targets and weights ("signal"):
  new   : W3-style: songs first played >= 90 d before the cutoff, target = percentile of plays in the first 90 days within the quarter of first play.
  panel : each of the last K=2 periods of P=91 days before the cutoff: every song (old or new) with >= 2 plays in that period gets target = percentile
          rank of its plays in that period among such songs; rows weighted by recency 0.5**(age_days/180).
Each member is a weighted ridge on whitened PCA of MERT (fit on train-stream songs with audio only), solved by normal equations; the score is the mean over
members of the standardised member scores (standardised with the member's own scores on its training rows).
Variants *_noart: for every candidate, its own primary artist's training songs are removed from the member's training signal (exact leave-artist-out ridge:
the artist's sufficient statistics are subtracted); PCA is not refit.  Depends only on the candidate's own artist id.
No audio -> neutral score 0 (= mean of the standardised training-row scores).
"""
import hashlib
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"
_S = {}

def _store():
    if "c" not in _S:
        z = np.load(ROOT + ".cache/w4r1/compact.npz")
        _S["c"] = {k: z[k] for k in ("md5", "mert", "has_mert")}; _S["idx"] = {k: i for i, k in enumerate(_S["c"]["md5"])}
    return _S

CFG = dict(ncomp=64, alpha=300.0, signal="panel", K=2, P=91, hl=180.0, newhl=None, minplays=2, noart=False, mode="whole", wt=1.0)

def _raw(tids, meta):
    """[n, 4, 768] MERT windows and has-audio mask; per-clip features, independent of other tracks"""
    S = _store(); n = len(tids); C = S["c"]; u = meta.previewUrl.reindex(tids).values
    ii = np.array([S["idx"].get(hashlib.md5(x.encode()).hexdigest(), -1) if isinstance(x, str) else -1 for x in u])
    has = ii >= 0; X = np.zeros((n, 4, 768), np.float32); X[has] = C["mert"][ii[has]].astype(np.float32); has &= C["has_mert"][np.maximum(ii, 0)]
    has &= np.isfinite(X).reshape(n, -1).all(1); X[~has] = 0
    return X, has

def _design(res, tids, meta, cfg):
    """[n*rep, d] whitened-PCA design (rep = 4 windows in local mode, else window mean) and has-audio mask [n]"""
    n = len(tids); mu, sd, pca = res["tf"]; X, has = _raw(tids, meta)
    if cfg["mode"] == "local": P = pca.transform(((X - mu) / sd).reshape(n * 4, -1)); P[np.repeat(~has, 4)] = 0
    else: P = pca.transform((X.mean(1) - mu) / sd); P[~has] = 0
    return P, has

def _pct(vals):
    return pd.Series(vals).rank(pct=True).values

def _signal(train, st, cutoff, cfg):
    """per-song sufficient statistics of the training signal: W = weight sum, Y = weight * target sum (rows with W == 0 are not used)."""
    idx = {s: i for i, s in enumerate(st.index)}; n = len(st); W = np.zeros(n); Y = np.zeros(n)
    if cfg["signal"] == "panel":
        si = train.song.map(idx).values; ok = ~pd.isna(si); si = si[ok].astype(int); tt = train.t.values[ok]
        for k in range(cfg["K"]):
            e = cutoff - pd.Timedelta(days=cfg["P"] * k); s0 = e - pd.Timedelta(days=cfg["P"])
            m = (tt >= np.datetime64(s0)) & (tt < np.datetime64(e))
            if m.sum() == 0: continue
            cnt = np.bincount(si[m], minlength=n); pl = cnt >= cfg["minplays"]
            if pl.sum() < 20: continue
            y = np.zeros(n); y[pl] = _pct(cnt[pl]); w = 0.5 ** (cfg["P"] * (k + 0.5) / cfg["hl"]) * pl
            W += w; Y += w * y
    else:   # "new"
        fi = st["first"]; mat = (fi < cutoff - pd.Timedelta(days=90)).values; qa = fi.dt.to_period("Q").astype(str).values
        y = np.zeros(n); y[mat] = pd.Series(st.plays90.values[mat]).groupby(qa[mat]).rank(pct=True).values
        w = (0.5 ** ((cutoff - fi).dt.days.values / cfg["newhl"]) if cfg["newhl"] else 1.0) * mat; W += w; Y += w * y
    return W, Y

def _fit(train, meta, cutoff, cfg):
    from sklearn.decomposition import PCA
    from threadpoolctl import threadpool_limits
    from evalkit.data import song_table
    st = song_table(train); st = st[st.trackId.isin(meta.index)]
    tids = st.trackId.values; art = st.artist.values
    with threadpool_limits(2):
        X, has = _raw(tids, meta); Xo = X[has]; Xo = Xo.reshape(-1, 768) if cfg["mode"] == "local" else Xo.mean(1)
        mu = Xo.mean(0); sd = Xo.std(0) + 1e-6
        res = dict(tf=(mu, sd, PCA(min(cfg["ncomp"], has.sum() - 1), whiten=True, random_state=0).fit((Xo - mu) / sd)))
        P, has = _design(res, tids, meta, cfg); W, Y = _signal(train, st, cutoff, cfg)
        keep = has & (W > 0); rep = 4 if cfg["mode"] == "local" else 1; kr = np.repeat(keep, rep)
        P = P[kr]; W, Y, art2 = np.repeat(W[keep], rep), np.repeat(Y[keep], rep), np.repeat(art[keep], rep)
        ws = W * len(W) / W.sum(); Yn = Y / W            # mean row weight 1
        Xa = np.c_[P, np.ones(len(P))]; reg = np.eye(Xa.shape[1]) * cfg["alpha"]; reg[-1, -1] = 1e-6
        A = (Xa * ws[:, None]).T @ Xa; b = (Xa * (ws * Yn)[:, None]).sum(0)
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
           hashlib.md5(train.t.values.tobytes()).hexdigest(), repr(sorted(cfg.items())))   # identity-aware key; bypassed with EVALKIT_NO_FIT_CACHE
    if key in _CACHE and not os.environ.get("EVALKIT_NO_FIT_CACHE"): return _CACHE[key]
    r = _fit(train, meta, cutoff, cfg); _CACHE[key] = r; return r

def _score(res, cands, meta, cfg):
    n = len(cands); rep = 4 if cfg["mode"] == "local" else 1
    P, has = _design(res, cands.trackId.values, meta, cfg); Xa = np.c_[P, np.ones(len(P))]; s = Xa @ res["beta"]
    if cfg["noart"]:
        art = np.repeat(cands.artist.values, rep)
        for a in np.unique(art):
            if a not in res["ablocks"]: continue
            Aa, ba = res["ablocks"][a]; beta = np.linalg.solve(res["A"] - Aa + res["reg"], res["b"] - ba); m = art == a; s[m] = Xa[m] @ beta
    s = (s.reshape(n, rep).mean(1) - res["tm"]) / res["ts"]; s[~has] = 0.0   # no audio: neutral
    return s

def make(*members, **kw):
    """weighted mean of standardised member scores (each member: dict overriding CFG)"""
    cfgs = [{**CFG, **kw, **m} for m in members]
    def predict(train, cands, meta, cutoff):
        return np.average([_score(_get(train, meta, cutoff, c), cands, meta, c) for c in cfgs], axis=0, weights=[c["wt"] for c in cfgs])
    return predict

E = dict(mode="local", alpha=1200.0); W32 = dict(ncomp=32, alpha=150.0)
NEW = [dict(E, signal="new"), dict(W32, signal="new")]                                   # W3-style members (new songs' within-quarter play rank)
PAN = [dict(E, ncomp=128, alpha=2400.0), dict(ncomp=64, alpha=300.0)]                     # panel members (last 2 x 91 days, songs with >= 2 plays, old or new)
def _na(ms): return [dict(m, noart=True) for m in ms]
PREDICTORS = {
    "w4r1_final": make(*NEW, *PAN),
    "w4r1_final_noart": make(*_na(NEW), *_na(PAN)),     # own-artist training songs removed from the signal (artist-recognition check)
    "w4r1_newonly": make(*NEW),                          # ablation: new-song signal only (= Workflow 3 recipe on the same code)
    "w4r1_panelonly": make(*PAN),                        # ablation: panel signal only
    "w4r1_panelonly_noart": make(*_na(PAN)),
}
