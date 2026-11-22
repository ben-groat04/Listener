"""w6r1-content-ranker-final: the W5 listening recipe (4 members: 2 NEW-song + 2 PANEL; MERT layers 4-8; whitened PCA + weighted ridge; training signal configs of grid.py) scored from the dev preview excerpt,
the Deezer preview excerpt (second, independent clip; MERT features of the same extractor), or both, with a choice of window pooling.  Training always uses the dev excerpt.
FEATURES = ("mert",) for dev-excerpt variants; the two-excerpt variants additionally read the Deezer-excerpt MERT shards (see _dz_store; fall back to the dev excerpt when absent).
Features are read through evalkit.features (dev excerpt) / the shared-w6r1 Deezer shards (second excerpt).  Missing audio: a song without any clip gets the neutral member score 0 (as in the W5 code)."""
import hashlib, os, glob, collections
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
import grid as G
from evalkit import features as FT
FEATURES = ("mert",)
DAY = 86400 * 10**9
_DZ = {}
def _dz_store():
    if "m" not in _DZ:
        clips = pd.read_csv(ROOT + ".cache/shared-w6r1/p2_clips.csv"); clips = clips[(clips.ok == True) & (clips.mert_ok == True)]
        tid = {str(int(t)): m for t, m in zip(clips.trackId, clips.md5)}
        dirs = [ROOT + ".cache/shared-w6r1/mert_deezer"]; sp = FT.sealed_root() / "mert-deezer"
        if sp.exists(): dirs.append(str(sp))   # convention for a future sealed second-excerpt pipeline (not produced by sealed_prep)
        keys, arrs = [], []
        for d in dirs:
            for f in sorted(glob.glob(d + "/shard_*.npz")):
                z = np.load(f); keys += [str(x) for x in z["md5"]]; arrs.append(z["feat"])
        _DZ["m"] = dict(tid=tid, idx={k: i for i, k in enumerate(keys)}, arr=np.concatenate(arrs))
    return _DZ["m"]

def _raw(tids, meta, src="dev"):
    if src == "dev": return FT.mert(meta, tids)
    S = _dz_store(); n = len(tids); X = np.zeros((n, 4, 768), np.float32)
    ii = np.array([S["idx"].get(S["tid"].get(str(int(t)), ""), -1) for t in tids]); has = ii >= 0
    if has.any(): X[has] = S["arr"][ii[has]][:, :, 4:9].astype(np.float32).mean(2)
    has &= np.isfinite(X.reshape(n, -1)).all(1); X[~has] = 0
    return X, has

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

def two(names, pool="mean"):
    """mean of the dev-excerpt score and the Deezer-excerpt score; if only one clip exists, that clip's score; none -> 0"""
    fd, fz = _avg(names, "dev", pool), _avg(names, "dz", pool)
    def predict(train, cands, meta, cutoff):
        (a, ha), (b, hb) = fd(train, cands, meta, cutoff), fz(train, cands, meta, cutoff)
        n = ha.astype(float) + hb.astype(float); return (a * ha + b * hb) / np.maximum(n, 1)
    return predict

def dzfb(names, pool="mean"):
    """Deezer-excerpt score, dev-excerpt score where the Deezer clip is missing"""
    fd, fz = _avg(names, "dev", pool), _avg(names, "dz", pool)
    def predict(train, cands, meta, cutoff):
        (a, ha), (b, hb) = fd(train, cands, meta, cutoff), fz(train, cands, meta, cutoff)
        return np.where(hb, b, a)
    return predict

def _z(x): x = np.asarray(x, float); return (x - x.mean()) / (x.std() + 1e-9)
def combo(base, w=1.0):
    from evalkit import refs
    def predict(train, cands, meta, cutoff):
        m = refs.score("ref_w4r1_music", train, cands, meta, cutoff); return _z(base(train, cands, meta, cutoff)) + w * _z(m)
    return predict

A21, DEF = G.ALL21, ["default"]
def build():
    two21 = two(A21)
    return {"avg21_dev": one(A21), "avg21_dz": dzfb(A21), "avg21_two": two21, "avg21_dev_max": one(A21, "dev", "max"), "avg21_dev_top2": one(A21, "dev", "top2"), "avg21_two_max": two(A21, "max"),
            "def_dev": one(DEF), "def_dz": dzfb(DEF), "def_two": two(DEF), "combo_two_music": combo(two21), "combo_dev_music": combo(one(A21))}
PREDICTORS = build()
if os.environ.get("W6_ONLY"): PREDICTORS = {k: v for k, v in PREDICTORS.items() if k in os.environ["W6_ONLY"].split(",")}
