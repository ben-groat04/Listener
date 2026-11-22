import hashlib, os, glob, collections
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
import grid as G
from evalkit import features as FT
FEATURES = ("mert",)
DAY = 86400 * 10**9
def _raw(tids, meta, src="dev"):
    assert src == "dev"
    return FT.mert(meta, tids)

MEMBERS = [("newE", "local", 64, 1200.0, "new"), ("newW32", "whole", 32, 150.0, "new"), ("panE", "local", 128, 2400.0, "panel"), ("panW", "whole", 64, 300.0, "panel")]
NEWK = ("tgt", "grp", "gdays", "mingrp", "hor", "mat", "partial", "pop", "newhl", "window", "stale", "stale_new"); PANK = ("K", "P", "hl", "minplays", "minsongs", "stale", "stale_pan")
_PREP = collections.OrderedDict()
def _tkey(train, cutoff):
    return (str(cutoff), len(train), hashlib.md5(pd.util.hash_array(train.song.values.astype(str).astype(object)).tobytes()).hexdigest(), hashlib.md5(train.t.values.tobytes()).hexdigest(),
            hashlib.md5(pd.util.hash_array(train.trackId.values.astype(str).astype(object)).tobytes()).hexdigest(), os.environ.get("EVALKIT_NULL_SEED", ""))

def _prep(train, meta, cutoff):
    from evalkit.data import song_table
    key = _tkey(train, cutoff)
    if key in _PREP: _PREP.move_to_end(key); return _PREP[key]
    st = song_table(train); st = st[st.trackId.isin(meta.index)]
    idx = pd.Series(np.arange(len(st)), index=st.index); si = train.song.map(idx).values; ok = ~pd.isna(si)
    X, has = _raw(st.trackId.values, meta)
    P = dict(key=key, st=st, n=len(st), tids=st.trackId.values, art=st.artist.values, si=si[ok].astype(int), tt=train.t.values[ok].astype("datetime64[ns]").astype(np.int64),
             tt_all=np.sort(train.t.values.astype("datetime64[ns]").astype(np.int64)), first=st["first"].values.astype("datetime64[ns]").astype(np.int64),
             firstdt=st["first"], X=X, has=has, pca={}, Ptr={}, Pc={}, counts={}, fits={}, cutoff=pd.Timestamp(cutoff), meta=meta)
    _PREP[key] = P
    while len(_PREP) > 4: _PREP.popitem(last=False)
    return P

def _pcaf(P, mode, ncomp):
    from sklearn.decomposition import PCA
    from threadpoolctl import threadpool_limits
    k = (mode, ncomp)
    if k not in P["pca"]:
        with threadpool_limits(2):
            Xo = P["X"][P["has"]]; Xo = Xo.reshape(-1, 768) if mode == "local" else Xo.mean(1)
            mu = Xo.mean(0); sd = Xo.std(0) + 1e-6
            P["pca"][k] = (mu, sd, PCA(min(ncomp, P["has"].sum() - 1), whiten=True, random_state=0).fit((Xo - mu) / sd))
    return P["pca"][k]

def _design(P, mode, ncomp, X, has):
    mu, sd, pca = _pcaf(P, mode, ncomp); n = len(X)
    if mode == "local": D = pca.transform(((X - mu) / sd).reshape(n * 4, -1)); D[np.repeat(~has, 4)] = 0
    else: D = pca.transform((X.mean(1) - mu) / sd); D[~has] = 0
    return D

def _train_design(P, mode, ncomp):
    k = (mode, ncomp)
    if k not in P["Ptr"]: P["Ptr"][k] = _design(P, mode, ncomp, P["X"], P["has"]).astype(np.float64)
    return P["Ptr"][k]

def _counts(P, hor, ce):
    k = (hor, ce)
    if k not in P["counts"]:
        si, tt, f = P["si"], P["tt"], P["first"]; end = np.minimum(f + hor * DAY, ce)
        m = (tt < end[si]) & (tt >= f[si]); plays = np.bincount(si[m], minlength=P["n"]).astype(float)
        u = np.unique(si[m].astype(np.int64) * 100000 + tt[m] // DAY); days = np.bincount(u // 100000, minlength=P["n"]).astype(float)
        tot = np.searchsorted(P["tt_all"], end) - np.searchsorted(P["tt_all"], f)
        P["counts"][k] = (plays, days, plays / np.maximum(tot, 1))
    return P["counts"][k]

def _pct(vals, g): return pd.Series(vals).groupby(g).rank(pct=True).values

def _newsig(P, C, ce):
    n = P["n"]; f = P["first"]; mat_ok = f < ce - C["mat"] * DAY
    plays, days, share = _counts(P, C["hor"], ce); age = (ce - f) / DAY
    if C["partial"] == "scale":
        fac = np.where(age < C["hor"], C["hor"] / np.maximum(age, 7.0), 1.0); plays = plays * fac; days = days * fac
    pop = mat_ok & (P["has"] if C["pop"] == "audio" else True)
    if C["grp"] == "quarter": g = (P["firstdt"].dt.year * 4 + P["firstdt"].dt.quarter).values
    elif C["grp"] == "roll": g = np.floor((ce - C["mat"] * DAY - f) / (C["gdays"] * DAY)).astype(int)
    else: g = np.zeros(n, int)
    if C["mingrp"]:
        sz = pd.Series(g[pop]).value_counts(); pop = pop & np.isin(g, sz.index[sz >= C["mingrp"]].values)
    y = np.zeros(n); ii = np.where(pop)[0]
    if len(ii):
        t = C["tgt"]; gi = g[ii]
        if t == "pct_plays": y[ii] = _pct(plays[ii], gi)
        elif t == "pct_days": y[ii] = _pct(days[ii], gi)
        elif t == "pd": y[ii] = 0.5 * (_pct(plays[ii], gi) + _pct(days[ii], gi))
        elif t == "share": y[ii] = _pct(share[ii], gi)
        elif t == "love": y[ii] = ((plays[ii] >= 6) & (days[ii] >= 3)).astype(float)
        elif t == "logz":
            v = pd.Series(np.log1p(plays[ii])); gr = v.groupby(gi); y[ii] = ((v - gr.transform("mean")) / (gr.transform("std").fillna(1.0) + 1e-6)).values
    w = pop.astype(float)
    if C["newhl"]: w = w * 0.5 ** (age / C["newhl"])
    if C["window"]: w = w * (age <= C["window"])
    return w, y * w

def _pansig(P, C, ce):
    n = P["n"]; si, tt = P["si"], P["tt"]; W = np.zeros(n); Y = np.zeros(n)
    for k in range(C["K"]):
        e = ce - C["P"] * k * DAY; s0 = e - C["P"] * DAY; m = (tt >= s0) & (tt < e)
        if m.sum() == 0: continue
        cnt = np.bincount(si[m], minlength=n); pl = cnt >= C["minplays"]
        if pl.sum() < C["minsongs"]: continue
        y = np.zeros(n); y[pl] = _pct(cnt[pl], np.zeros(pl.sum(), int)); w = (0.5 ** (C["P"] * (k + 0.5) / C["hl"]) if C["hl"] else 1.0) * pl
        W += w; Y += w * y
    return W, Y

def _pool(s, op):
    """pool window scores [n,4] -> [n]"""
    if op == "mean": return s.mean(1)
    if op == "max": return s.max(1)
    if op == "top2": return np.sort(s, 1)[:, -2:].mean(1)
    raise ValueError(op)

def _fitmember(P, mem, C, ce):
    name, mode, ncomp, alpha, sig = mem; ks = NEWK if sig == "new" else PANK
    key = (name, ce, tuple(C[k] for k in ks))
    if key in P["fits"]: return P["fits"][key]
    W, Y = (_newsig(P, C, ce) if sig == "new" else _pansig(P, C, ce))
    D = _train_design(P, mode, ncomp); rep = 4 if mode == "local" else 1
    keep = P["has"] & (W > 0)
    if keep.sum() < 10: r = None
    else:
        kr = np.repeat(keep, rep); Dk = D[kr]; Wk = np.repeat(W[keep], rep); Yk = np.repeat(Y[keep], rep)
        ws = Wk * len(Wk) / Wk.sum(); Yn = Yk / Wk
        Xa = np.c_[Dk, np.ones(len(Dk))]; reg = np.eye(Xa.shape[1]) * alpha; reg[-1, -1] = 1e-6
        A = (Xa * ws[:, None]).T @ Xa; b = (Xa * (ws * Yn)[:, None]).sum(0); beta = np.linalg.solve(A + reg, b)
        sw = (Xa @ beta).reshape(-1, rep); r = dict(beta=beta, sw=sw, norm={})
    if len(P["fits"]) > 3000: P["fits"].clear()
    P["fits"][key] = r; return r

def _norm(r, op):
    """train mean / sd of the pooled member score (pool op), cached on the fit"""
    if op not in r["norm"]: s = _pool(r["sw"], op) if r["sw"].shape[1] > 1 else r["sw"][:, 0]; r["norm"][op] = (float(s.mean()), float(s.std() + 1e-9))
    return r["norm"][op]

def _cand_design(P, tids, mode, ncomp, src):
    k = (hashlib.md5("|".join(map(str, tids)).encode()).hexdigest(), mode, ncomp, src)
    if k not in P["Pc"]:
        X, has = _raw(tids, P["meta"], src); P["Pc"][k] = (_design(P, mode, ncomp, X, has), has)
        if len(P["Pc"]) > 400: P["Pc"].pop(next(iter(P["Pc"])))
    return P["Pc"][k]

def _score_with(P, C, tids, ce, src="dev", pool="mean"):
    """blended standardised score of the recipe under signal config C for candidates tids, scored from clip `src`; returns (score, has-clip mask). Songs without that clip score 0."""
    C = {**G.DEFAULT, **C}; ce0 = ce; out = []; wts = []; hasm = None
    for mem in MEMBERS:
        sig = mem[4]; wt = C["wnew"] if sig == "new" else 1.0 - C["wnew"]
        if wt <= 0: continue
        ce = ce0 - (C["stale"] + (C["stale_new"] if sig == "new" else C["stale_pan"])) * DAY
        r = _fitmember(P, mem, C, ce); D, has = _cand_design(P, tids, mem[1], mem[2], src); hasm = has
        if r is None: s = np.zeros(len(tids))
        else:
            rep = 4 if mem[1] == "local" else 1; Xa = np.c_[D, np.ones(len(D))]; sw = (Xa @ r["beta"]).reshape(-1, rep)
            op = pool if rep > 1 else "mean"; s = _pool(sw, op) if rep > 1 else sw[:, 0]; m, sd = _norm(r, op); s = (s - m) / sd; s[~has] = 0.0
        out.append(s); wts.append(wt)
    return np.average(out, axis=0, weights=wts), hasm

def _configs(names): return [G.CFG[n] for n in names]
def _avg(names, src, pool):
    def parts(train, cands, meta, cutoff):
        P = _prep(train, meta, cutoff); ce = pd.Timestamp(cutoff).value; t = cands.trackId.values; S = []; H = None
        for c in _configs(names): s, H = _score_with(P, c, t, ce, src, pool); S.append(s)
        return np.mean(S, axis=0), H
    return parts

def one(names, src="dev", pool="mean"):
    f = _avg(names, src, pool)
    def predict(train, cands, meta, cutoff): return f(train, cands, meta, cutoff)[0]
    return predict


# ---------------- round 2: pool-independent scaling from TRAINING songs only ----------------
A21 = G.ALL21
_TS = collections.OrderedDict()
def _trainstats(train, meta, cutoff, tag, fn):
    """mean / sd of member score `tag` over the fold's TRAINING songs that have a MERT clip (song table of train; candidates never enter). fn(tids)->scores. cached per train identity."""
    P = _prep(train, meta, cutoff); k = (P["key"], tag)
    if k not in _TS:
        t = P["tids"][P["has"]]; s = np.asarray(fn(t), float); assert np.isfinite(s).all() and len(s) > 50
        _TS[k] = (float(s.mean()), float(s.std() + 1e-9))
        while len(_TS) > 64: _TS.popitem(last=False)
    return _TS[k]

def avg21(pool="mean"):
    f = _avg(A21, "dev", pool)
    def predict(train, cands, meta, cutoff): return f(train, cands, meta, cutoff)[0]
    return predict

def combo_ts(pool="mean", w=1.0):
    """avg21 (MERT, pooling `pool`) + w * ref_w4r1_music, each centred and scaled by its mean/sd over the training songs (fixed constants for the call; no candidate statistic)."""
    from evalkit import refs
    fa = _avg(A21, "dev", pool)
    def predict(train, cands, meta, cutoff):
        ce = pd.Timestamp(cutoff); P = _prep(train, meta, ce)
        ma, sa = _trainstats(train, meta, ce, "a21" + pool, lambda t: fa(train, pd.DataFrame({"trackId": t}), meta, ce)[0])
        mm, sm = _trainstats(train, meta, ce, "music", lambda t: refs.score("ref_w4r1_music", train, pd.DataFrame({"trackId": t}), meta, ce))
        a = fa(train, cands, meta, ce)[0]; m = refs.score("ref_w4r1_music", train, cands, meta, ce)
        return (a - ma) / sa + w * (m - mm) / sm
    return predict

PREDICTORS = {"avg21_dev": avg21("mean"), "avg21_max": avg21("max"), "combo_mean_ts": combo_ts("mean"), "combo_max_ts": combo_ts("max")}
