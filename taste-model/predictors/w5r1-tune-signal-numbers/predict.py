"""w5r1-tune-signal-numbers: the W4 listening recipe (2 NEW members + 2 PANEL members; same features / PCA / ridge) with its TRAINING-SIGNAL and TIME numbers exposed as a config
(grid.py), plus a nested procedure that chooses them per outer cutoff from the fold's own training streams (evalkit.inner folds).  Harness entry file.
Features: .cache/w4r1/compact.npz (MERT layers 4-8, 4 windows); audio/learner numbers fixed at the base recipe's values (E: local 64/1200, W32: whole 32/150, PAN: local 128/2400, whole 64/300).
Env W5_SET selects which PREDICTORS entries exist (all by default): base,oat,stale,rj,tuned,final.  Env W5_CHOICE_LOG: jsonl file receiving the nested procedure's choices.
Nested tuning detail: the PCA of the outer fold (fit on the outer train's songs with audio, unsupervised) is reused inside the inner folds; labels/targets inside inner folds use only
streams before the inner cutoff (every signal function takes ce = inner cutoff and masks streams t < ce)."""
import hashlib, os, json, collections
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid as G
DAY = 86400 * 10**9
_S = {}
def _store():
    if "c" not in _S:
        z = np.load(ROOT + ".cache/w4r1/compact.npz"); _S["c"] = {k: z[k] for k in ("md5", "mert", "has_mert")}; _S["idx"] = {k: i for i, k in enumerate(_S["c"]["md5"])}
    return _S

def _raw(tids, meta):
    S = _store(); n = len(tids); C = S["c"]; u = meta.previewUrl.reindex(tids).values
    ii = np.array([S["idx"].get(hashlib.md5(x.encode()).hexdigest(), -1) if isinstance(x, str) else -1 for x in u])
    has = ii >= 0; X = np.zeros((n, 4, 768), np.float32); X[has] = C["mert"][ii[has]].astype(np.float32); has &= C["has_mert"][np.maximum(ii, 0)]
    has &= np.isfinite(X).reshape(n, -1).all(1); X[~has] = 0
    return X, has

# members of the base recipe: (name, mode, ncomp, alpha, signal)
MEMBERS = [("newE", "local", 64, 1200.0, "new"), ("newW32", "whole", 32, 150.0, "new"), ("panE", "local", 128, 2400.0, "panel"), ("panW", "whole", 64, 300.0, "panel")]
NEWK = ("tgt", "grp", "gdays", "mingrp", "hor", "mat", "partial", "pop", "newhl", "window", "stale"); PANK = ("K", "P", "hl", "minplays", "minsongs", "stale")

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
    """plays / distinct days / all-plays-in-window inside [first, min(first+hor d, ce)) per song; only streams before ce."""
    k = (hor, ce)
    if k not in P["counts"]:
        si, tt, f = P["si"], P["tt"], P["first"]; end = np.minimum(f + hor * DAY, ce)
        m = (tt < end[si]) & (tt >= f[si]); plays = np.bincount(si[m], minlength=P["n"]).astype(float)
        u = np.unique(si[m].astype(np.int64) * 100000 + tt[m] // DAY); days = np.bincount(u // 100000, minlength=P["n"]).astype(float)
        tot = np.searchsorted(P["tt_all"], end) - np.searchsorted(P["tt_all"], f)
        P["counts"][k] = (plays, days, plays / np.maximum(tot, 1))
    return P["counts"][k]

def _pct(vals, g):
    return pd.Series(vals).groupby(g).rank(pct=True).values

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

def _fitmember(P, mem, C, ce):
    """ridge fit of one member with signal config C at effective cutoff ce (streams before ce only). Returns dict(beta, tm, ts) ."""
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
        s = (Xa @ beta).reshape(-1, rep).mean(1); r = dict(beta=beta, tm=float(s.mean()), ts=float(s.std() + 1e-9))
    if len(P["fits"]) > 6000: P["fits"].clear()
    P["fits"][key] = r; return r

def _cand_design(P, tids, mode, ncomp, tag):
    k = (hashlib.md5("|".join(map(str, tids)).encode()).hexdigest(), mode, ncomp)
    if k not in P["Pc"]:
        X, has = _raw(tids, P["meta"]); P["Pc"][k] = (_design(P, mode, ncomp, X, has), has)
    return P["Pc"][k]

def _score_with(P, C, tids, tag, ce):
    """blended standardised score of the base recipe under signal config C, fitted at ce, for candidates tids"""
    C = {**G.DEFAULT, **C}; ce = ce - C["stale"] * DAY; out = []; wts = []
    for mem in MEMBERS:
        sig = mem[4]; wt = C["wnew"] if sig == "new" else 1.0 - C["wnew"]
        if wt <= 0: continue
        r = _fitmember(P, mem, C, ce); D, has = _cand_design(P, tids, mem[1], mem[2], tag)
        if r is None: s = np.zeros(len(tids))
        else:
            rep = 4 if mem[1] == "local" else 1; Xa = np.c_[D, np.ones(len(D))]; s = (Xa @ r["beta"]).reshape(-1, rep).mean(1); s = (s - r["tm"]) / r["ts"]; s[~has] = 0.0
        out.append(s); wts.append(wt)
    return np.average(out, axis=0, weights=wts)

def fixed(cfg):
    def predict(train, cands, meta, cutoff):
        P = _prep(train, meta, cutoff); return _score_with(P, cfg, cands.trackId.values, ("c", len(cands)), pd.Timestamp(cutoff).value)
    return predict

# ---- nested tuning -------------------------------------------------------------------------------------------------------------------------------------------
_INNER = {}
def _inner_table(P, train, meta, cutoff, spec, grid):
    from evalkit import inner
    k = (P["key"], tuple(sorted(spec.items())), tuple(grid))
    if k in _INNER: return _INNER[k]
    folds = inner.make_inner_folds(train, meta, cutoff, **spec); tab = {}
    tids = [f["cands"].trackId.values for f in folds]
    for name in grid:
        vecs = [_score_with(P, G.TUNER_GRID[name], tids[i], ("in", spec.get("n_folds", 4), spec.get("spacing_months", 3), spec.get("horizon_days", 90), i), pd.Timestamp(f["inner_cutoff"]).value) for i, f in enumerate(folds)]
        tab[name] = inner.inner_sauc(vecs, folds) if folds else float("nan")
    if len(_INNER) > 30: _INNER.clear()
    _INNER[k] = (tab, len(folds)); return _INNER[k]

def _log(rec):
    p = os.environ.get("W5_CHOICE_LOG")
    if p:
        with open(p, "a") as fh: fh.write(json.dumps(rec) + "\n")

def tuned(label, spec, margin=0.0, grid=None):
    grid = list(grid or G.TUNER_GRID)
    for _g in grid: assert _g in G.TUNER_GRID
    def predict(train, cands, meta, cutoff):
        P = _prep(train, meta, cutoff); tab, nf = _inner_table(P, train, meta, cutoff, spec, grid)
        best = "default"
        if nf:
            vals = {k: v for k, v in tab.items() if np.isfinite(v)}
            if vals:
                b = max(vals, key=vals.get)
                if "default" in vals and vals[b] - vals["default"] > margin: best = b
                elif "default" not in vals: best = b
        _log(dict(label=label, cutoff=str(cutoff), n_inner=nf, chosen=best, inner_best=(max(tab.values()) if nf else None), inner_default=tab.get("default"), null=os.environ.get("EVALKIT_NULL_SEED", ""),
                  table={k: (round(v, 4) if np.isfinite(v) else None) for k, v in tab.items()}))
        return _score_with(P, G.TUNER_GRID[best], cands.trackId.values, ("c", len(cands)), pd.Timestamp(cutoff).value)
    return predict

SPEC_A = dict(n_folds=4, spacing_months=3, horizon_days=90)      # inner geometry A (harness-like)
SPEC_B = dict(n_folds=6, spacing_months=2, horizon_days=90)      # inner geometry B (more, shorter windows)
SPEC_C = dict(n_folds=4, spacing_months=3, horizon_days=60)      # inner geometry C (shorter label horizon)

SPEC_D = dict(n_folds=8, spacing_months=1, horizon_days=90)      # inner geometry D (monthly windows)
SPEC_E = dict(n_folds=2, spacing_months=6, horizon_days=90)      # inner geometry E (two half-year windows)

def build():
    sel = os.environ.get("W5_SET", "base,oat,stale,rj,tuned").split(","); out = {}
    if "base" in sel: out["w5_default"] = fixed({})
    if "oat" in sel: out.update({"oat_" + k: fixed(v) for k, v in G.OAT.items()})
    if "stale" in sel: out.update({"oat_" + k: fixed(v) for k, v in G.STALE.items()})
    if "rj" in sel: out.update({k: fixed(v) for k, v in G.random_configs().items()})
    if "tuned" in sel:
        out["tunedA"] = tuned("A", SPEC_A); out["tunedA_m02"] = tuned("A", SPEC_A, 0.02)
        out["tunedA_m05"] = tuned("A", SPEC_A, 0.05)
        out["tunedB"] = tuned("B", SPEC_B); out["tunedB_m02"] = tuned("B", SPEC_B, 0.02); out["tunedC"] = tuned("C", SPEC_C)
        out["tunedD"] = tuned("D", SPEC_D); out["tunedE"] = tuned("E", SPEC_E)
        out["tunedS"] = tuned("S", SPEC_A, 0.0, G.SMALL_GRID); out["tunedS_m02"] = tuned("S", SPEC_A, 0.02, G.SMALL_GRID)
    return out
PREDICTORS = build()
if os.environ.get("W5_ONLY"): PREDICTORS = {k: v for k, v in PREDICTORS.items() if k in os.environ["W5_ONLY"].split(",")}
_wf = os.environ.get("W5_WF", "")
if _wf == "oat": WALKFORWARD_FAMILY = ["w5_default"] + [k for k in PREDICTORS if k.startswith("oat_") and not k.startswith("oat_stale")]
elif _wf == "procs": WALKFORWARD_FAMILY = [k for k in PREDICTORS if k == "w5_default" or k.startswith("tuned")]
