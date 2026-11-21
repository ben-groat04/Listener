"""w4r2-unseen-artist-generalisation: content-only taste model whose training choices aim at generalising to artists absent from the history.  Harness entry file.
Usage (from /home/user/Listener/taste-model; needs .cache/w4r2-unseen/compact.npz from build_compact.py):
    python3 -W ignore -m evalkit.run --fast predictors/w4r2-unseen-artist-generalisation/predict.py
Candidate input: ONLY per-clip content (MERT layer groups, CLAP, essentia head activations / effnet embedding, lyric embedding) of the candidate's own clip/lyrics.
Listening record (streams < cutoff): ONLY training targets + weights per train song ("signal": panel = last K 91-day periods percentile of plays; new = percentile of plays in
first 90 days within quarter of first play, for songs first played >= 90 d before cutoff; both = sum of the two weighted targets).
Artist handling in training (never a candidate input): adem = subtract lam * shrunk leave-one-out artist mean target; apow = weight 1/n_artist_rows**apow.
Model per block: whitened PCA (fit on train-stream songs) + weighted ridge with unpenalised intercept; alpha chosen by artist-grouped 5-fold CV INSIDE train (not on TUNE).
combine = 'concat' (all blocks in one ridge) or 'trust' (one ridge per block, weights = squared positive artist-grouped CV correlation).
noart=True: for each candidate the candidate's own primary artist's training rows are removed from the ridge exactly (sufficient statistics subtracted).
No audio -> neutral score 0.
"""
import hashlib, os, pickle
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"
_S = {}

def _store():
    if "c" not in _S:
        z = np.load(ROOT + ".cache/w4r2-unseen/compact.npz")
        _S["c"] = {k: z[k] for k in ("md5", "mert3", "clap", "eact", "eemb")}; _S["idx"] = {k: i for i, k in enumerate(_S["c"]["md5"])}
        with open(ROOT + ".cache/shared/w4-lyrics/emb.pkl", "rb") as f: _S["lyr"] = pickle.load(f)
    return _S

def feat(block, tids, meta):
    S = _store(); C = S["c"]; n = len(tids)
    if block == "lyr":
        L = S["lyr"]; v = [L.get(int(t)) if t in L or int(t) in L else None for t in tids]
        has = np.array([x is not None for x in v]); X = np.zeros((n, 384), np.float32)
        for i, x in enumerate(v):
            if x is not None: X[i] = x
        return X, has
    u = meta.previewUrl.reindex(tids).values
    ii = np.array([S["idx"].get(hashlib.md5(x.encode()).hexdigest(), -1) if isinstance(x, str) else -1 for x in u]); has = ii >= 0
    if block.startswith("mert"): g = {"mert_lo": 0, "mert_mid": 1, "mert_hi": 2}[block]; arr = C["mert3"][:, g]
    else: arr = C[{"clap": "clap", "eact": "eact", "eemb": "eemb"}[block]]
    X = np.zeros((n, arr.shape[1]), np.float32); X[has] = arr[ii[has]].astype(np.float32)
    has &= np.isfinite(X).all(1); X[~has] = 0
    return X, has

CFG = dict(blocks=("mert_mid",), ncomp=48, signal="panel", K=2, P=91, hl=180.0, adem=0.0, apow=0.0, combine="concat", noart=False,
           alphas=(30., 100., 300., 1000., 3000.), alpha=None, minplays=2, learner="ridge", kalphas=(0.3, 1.0, 3.0), gam=0.25)

def _pct(v): return pd.Series(v).rank(pct=True).values

def _signal(train, st, cutoff, cfg):
    idx = {s: i for i, s in enumerate(st.index)}; n = len(st); W = np.zeros(n); Y = np.zeros(n)
    if cfg["signal"] in ("panel", "both"):
        si = train.song.map(idx).values; ok = ~pd.isna(si); si = si[ok].astype(int); tt = train.t.values[ok]
        for k in range(cfg["K"]):
            e = cutoff - pd.Timedelta(days=cfg["P"] * k); s0 = e - pd.Timedelta(days=cfg["P"])
            m = (tt >= np.datetime64(s0)) & (tt < np.datetime64(e))
            if m.sum() == 0: continue
            cnt = np.bincount(si[m], minlength=n); pl = cnt >= cfg["minplays"]
            if pl.sum() < 20: continue
            y = np.zeros(n); y[pl] = _pct(cnt[pl]); w = 0.5 ** (cfg["P"] * (k + 0.5) / cfg["hl"]) * pl
            W += w; Y += w * y
    if cfg["signal"] in ("new", "both"):
        mat = (st["first"] < cutoff - pd.Timedelta(days=90)).values
        if mat.sum() > 20:
            qa = st["first"].dt.to_period("Q").astype(str).values
            y = np.zeros(n); y[mat] = pd.Series(st.plays90.values[mat]).groupby(qa[mat]).rank(pct=True).values
            w = mat.astype(float) * (0.5 if cfg["signal"] == "both" else 1.0); W += w; Y += w * y
    return W, Y

def _wpear(p, y, w):
    mp = np.average(p, weights=w); my = np.average(y, weights=w)
    c = np.average((p - mp) * (y - my), weights=w); return c / (np.sqrt(np.average((p - mp) ** 2, weights=w) * np.average((y - my) ** 2, weights=w)) + 1e-12)

def _stats(P, y, w):
    A = np.c_[P, np.ones(len(P))]; return (A * w[:, None]).T @ A, (A * (w * y)[:, None]).sum(0), A

def _solve(G, b, alpha):
    d = len(b); pen = np.full(d, alpha); pen[-1] = 1e-6
    return np.linalg.solve(G + np.diag(pen), b)

def _cv_alpha(P, y, w, art, alphas, seed=0):
    """artist-grouped 5-fold CV inside train; returns (best alpha, cv score of best)"""
    ua, inv = np.unique(art, return_inverse=True); rng = np.random.RandomState(seed); fo = rng.randint(0, 5, len(ua))[inv]
    G, b, A = _stats(P, y, w); sc = []
    for al in alphas:
        pr = np.zeros(len(y))
        for f in range(5):
            m = fo == f
            if m.sum() == 0 or (~m).sum() < 10: continue
            Gf = G - (A[m] * w[m, None]).T @ A[m]; bf = b - (A[m] * (w[m] * y[m])[:, None]).sum(0)
            pr[m] = A[m] @ _solve(Gf, bf, al)
        sc.append(_wpear(pr, y, w))
    j = int(np.argmax(sc)); return alphas[j], sc[j]

_CACHE = {}
def _fit(train, meta, cutoff, cfg):
    ident = int(pd.util.hash_pandas_object(train[["trackId", "song", "artist"]].astype(str), index=False).sum() % (1 << 60))
    key = (str(cutoff), len(train), ident, int(train.t.values.astype("int64").sum() % (1 << 60)), repr(sorted(cfg.items())))
    if key in _CACHE: return _CACHE[key]
    from sklearn.decomposition import PCA
    from threadpoolctl import threadpool_limits
    from evalkit.data import song_table
    st = song_table(train); st = st[st.trackId.isin(meta.index)]
    W, Y = _signal(train, st, cutoff, cfg); art = st.artist.astype(str).values
    tids = st.trackId.values; res = dict(members=[])
    with threadpool_limits(2):
        feats = {}
        for b in cfg["blocks"]:
            X, has = feat(b, tids, meta); feats[b] = (X, has)
        use = (W > 0)
        for b in cfg["blocks"]: use &= feats[b][1] if cfg["combine"] == "concat" else True
        # per-block members
        groups = [list(cfg["blocks"])] if cfg["combine"] == "concat" else [[b] for b in cfg["blocks"]]
        for g in groups:
            ok = np.ones(len(st), bool)
            for b in g: ok &= feats[b][1]
            tf = []; Ps = []
            for b in g:
                X = feats[b][0]; mu = X[ok].mean(0); sd = X[ok].std(0) + 1e-6
                pca = PCA(cfg["ncomp"], whiten=True, random_state=0).fit((X[ok] - mu) / sd)
                tf.append((mu, sd, pca)); Ps.append(pca.transform((X - mu) / sd))
            P = np.concatenate(Ps, 1); r = ok & (W > 0)
            if r.sum() < 40: continue
            y = Y[r] / W[r]; w = W[r].copy(); ar = art[r]
            if cfg["adem"]:
                s = pd.Series(y); gs = s.groupby(ar).transform("sum").values; ct = s.groupby(ar).transform("size").values
                loo = (gs - y) / np.maximum(ct - 1, 1) * (ct - 1) / (ct - 1 + 2.0) + y.mean() * 2.0 / (ct - 1 + 2.0); y = y - cfg["adem"] * (loo - y.mean())
            if cfg["apow"]:
                ct = pd.Series(ar).groupby(ar).transform("size").values; w = w / ct ** cfg["apow"]
            w = w / w.mean()
            if cfg["learner"] == "krr":
                from sklearn.kernel_ridge import KernelRidge
                gm = cfg["gam"] / P.shape[1]; ua, inv = np.unique(ar, return_inverse=True); fo = np.random.RandomState(0).randint(0, 5, len(ua))[inv]; best = None
                for ka in cfg["kalphas"]:
                    pr = np.zeros(len(y))
                    for f in range(5):
                        mm = fo == f
                        if mm.sum() == 0 or (~mm).sum() < 10: continue
                        k = KernelRidge(alpha=ka, kernel="rbf", gamma=gm).fit(P[r][~mm], y[~mm] - np.average(y[~mm], weights=w[~mm]), sample_weight=w[~mm]); pr[mm] = k.predict(P[r][mm])
                    c = _wpear(pr, y, w)
                    if best is None or c > best[0]: best = (c, ka)
                ym = np.average(y, weights=w); k = KernelRidge(alpha=best[1], kernel="rbf", gamma=gm).fit(P[r], y - ym, sample_weight=w)
                sc = k.predict(P[r]); res["members"].append(dict(g=g, tf=tf, krr=k, ym=ym, cv=best[0], al=best[1], mu=float(sc.mean()), sd=float(sc.std() + 1e-9), ar=ar)); continue
            if cfg["alpha"]: al, cvs = cfg["alpha"], np.nan
            else: al, cvs = _cv_alpha(P[r], y, w, ar, cfg["alphas"])
            G, bb, A = _stats(P[r], y, w); beta = _solve(G, bb, al)
            sc = A @ beta; m = dict(g=g, tf=tf, beta=beta, G=G, b=bb, al=al, cv=cvs, ar=ar, A=A, y=y, w=w, mu=float(sc.mean()), sd=float(sc.std() + 1e-9), ok=ok)
            res["members"].append(m)
        if cfg["combine"] == "trust" and res["members"]:
            ws = np.array([max(m["cv"], 0) ** 2 if np.isfinite(m["cv"]) else 1.0 for m in res["members"]]); ws = ws / (ws.sum() + 1e-12) if ws.sum() > 0 else np.ones(len(ws)) / len(ws)
            for m, wt in zip(res["members"], ws): m["wt"] = float(wt)
        else:
            for m in res["members"]: m["wt"] = 1.0 / max(len(res["members"]), 1)
    _CACHE[key] = res; return res

def _score(res, cands, meta, cfg):
    n = len(cands); out = np.zeros(n); tids = cands.trackId.values; carts = cands.artist.astype(str).values
    for m in res["members"]:
        Ps = []; ok = np.ones(n, bool)
        for b, (mu, sd, pca) in zip(m["g"], m["tf"]):
            X, has = feat(b, tids, meta); ok &= has; Ps.append(pca.transform((X - mu) / sd))
        A = np.c_[np.concatenate(Ps, 1), np.ones(n)]
        s = m["krr"].predict(A[:, :-1]) if "krr" in m else A @ m["beta"]
        if cfg["noart"] and "krr" not in m:
            ar = m["ar"]; ua = set(ar.tolist())
            for a in np.unique(carts[ok]):
                if a in ua:
                    r = ar == a; Ar = m["A"][r]; w = m["w"][r]; y = m["y"][r]
                    Gf = m["G"] - (Ar * w[:, None]).T @ Ar; bf = m["b"] - (Ar * (w * y)[:, None]).sum(0)
                    beta = _solve(Gf, bf, m["al"]); mk = ok & (carts == a); s[mk] = A[mk] @ beta
        z = (s - m["mu"]) / m["sd"]; z[~ok] = 0
        out += m["wt"] * z
    return out

def make(**kw):
    cfg = {**CFG, **kw}
    def predict(train, cands, meta, cutoff):
        res = _fit(train, meta, cutoff, cfg)
        if not res["members"]: return np.zeros(len(cands))
        return _score(res, cands, meta, cfg)
    return predict

MERT3 = ("mert_lo", "mert_mid", "mert_hi")
V = {   # every variant scored on TUNE is listed here (counted)
    "v01_mid_panel": dict(),
    "v02_mid_new": dict(signal="new"),
    "v03_mid_both": dict(signal="both"),
    "v04_mid_panel_adem1": dict(adem=1.0),
    "v05_mid_panel_apow05": dict(apow=0.5),
    "v06_mid_panel_apow1": dict(apow=1.0),
    "v07_mid_panel_noart": dict(noart=True),
    "v08_clap": dict(blocks=("clap",)),
    "v09_eact": dict(blocks=("eact",)),
    "v10_eemb": dict(blocks=("eemb",)),
    "v11_lyr": dict(blocks=("lyr",)),
    "v12_mert_lo": dict(blocks=("mert_lo",)),
    "v13_mert_hi": dict(blocks=("mert_hi",)),
    "v14_trust_all": dict(blocks=MERT3 + ("clap", "eact", "eemb", "lyr"), combine="trust"),
    "v15_trust_all_adem1": dict(blocks=MERT3 + ("clap", "eact", "eemb", "lyr"), combine="trust", adem=1.0),
    "v16_concat_mert3_clap": dict(blocks=MERT3 + ("clap",), ncomp=32),
    "v17_both_trust_all": dict(signal="both", blocks=MERT3 + ("clap", "eact", "eemb", "lyr"), combine="trust"),
    "v18_both_mid_eact": dict(signal="both", blocks=("mert_mid", "eact"), ncomp=32),
    "v19_both_nc96": dict(signal="both", ncomp=96),
    "v20_both_nc24": dict(signal="both", ncomp=24),
    "v21_both_K3": dict(signal="both", K=3),
    "v22_both_hl90": dict(signal="both", hl=90.0),
    "v23_both_hi": dict(signal="both", blocks=("mert_hi",)),
    "v24_both_mert3_nc32": dict(signal="both", blocks=MERT3, ncomp=32),
    "v25_both_trust_mert3_eact_eemb": dict(signal="both", blocks=MERT3 + ("eact", "eemb"), combine="trust"),
    "v26_both_apow025": dict(signal="both", apow=0.25),
    "v27_both_noart": dict(signal="both", noart=True),
    "v28_both_P182": dict(signal="both", P=182, hl=360.0),
    "v29_both_P60_K3": dict(signal="both", P=60, K=3, hl=120.0),
    "v30_both_nc128": dict(signal="both", ncomp=128, alphas=(100., 300., 1000., 3000., 10000.)),
    "v31_both_krr": dict(signal="both", learner="krr"),
    "v32_both_krr_mert3": dict(signal="both", learner="krr", blocks=MERT3, ncomp=32),
    "v33_both_hl90_nc64": dict(signal="both", hl=90.0, ncomp=64),
}

def make_ens(members, noart=False, refs=()):
    """standardised mean of several member configs (each member's score is already standardised with its own train-row scores);
    refs: names of evalkit.refs references whose scores are standardised with their scores on the train songs and averaged in (stacking; secondary)"""
    ms = [make(**{**m, **({"noart": True} if noart else {})}) for m in members]
    def predict(train, cands, meta, cutoff):
        out = np.mean([f(train, cands, meta, cutoff) for f in ms], 0)
        if refs:
            from evalkit import refs as R
            from evalkit.data import song_table
            st = song_table(train); st = st[st.trackId.isin(meta.index)].reset_index()
            zs = []
            for nm in refs:
                a = np.asarray(R.score(nm, train, cands, meta, cutoff), float); b = np.asarray(R.score(nm, train, st, meta, cutoff), float)
                zs.append((a - b.mean()) / (b.std() + 1e-9))
            out = (out * len(ms) + sum(zs)) / (len(ms) + len(zs))
        return out
    return predict

H = dict(signal="both", hl=90.0)
E_RIDGE = [dict(H, ncomp=64), dict(H, blocks=MERT3, ncomp=32), dict(H, blocks=MERT3 + ("eact", "eemb"), combine="trust"), dict(signal="both", P=60, K=3, hl=120.0, ncomp=64)]
E_KRR = E_RIDGE + [dict(H, learner="krr", ncomp=64)]
V2 = {
    "f1_ens_ridge": make_ens(E_RIDGE),
    "f2_ens_ridge_noart": make_ens(E_RIDGE, noart=True),
    "f3_ens_ridge_krr": make_ens(E_KRR),
    "f4_stack_refs": make_ens(E_RIDGE, refs=("ref_audio_final", "ref_w4r1_music")),
}
_only = os.environ.get("W4R2_ONLY")
PREDICTORS = {k: make(**v) for k, v in V.items() if not _only or any(t in k for t in _only.split(","))}
for _b in ("mert_lo", "mert_mid", "mert_hi", "clap", "eact", "eemb", "lyr"):   # analysis variants: which input families act as artist fingerprints (full vs own-artist rows removed)
    for _na in (False, True): V["a_%s%s" % (_b, "_noart" if _na else "_full")] = dict(signal="both", hl=90.0, blocks=(_b,), noart=_na)
PREDICTORS.update({k: make(**v) for k, v in V.items() if k.startswith("a_") and (not _only or any(t in k for t in _only.split(",")))})
PREDICTORS.update({k: v for k, v in V2.items() if not _only or any(t in k for t in _only.split(","))})
WALKFORWARD_FAMILY = [k for k in PREDICTORS if k.startswith("v") or k in ("f1_ens_ridge", "f2_ens_ridge_noart", "f3_ens_ridge_krr")]
