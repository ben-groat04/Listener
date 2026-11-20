"""Builder B round 2: audio (CLAP + hand-crafted segment/dynamics features) x behaviour-learned metric (co-play factors) x artist recency.
All fitted on train only, z-constants derived from train-history, so scores of candidates are independent.
Components (see _components):
  den   : CLAP (10 s mid-window of the preview) play-weighted kernel density over train songs      [round-1 term]
  lr    : logistic regression on whitened CLAP-PCA -> 'loved' (mature train songs)                  [round-1 term]
  art   : log recency-weighted artist plays                                                          [round-1 term]
  hden  : kernel density in whitened hand-crafted feature space (MFCC/chroma/contrast/tempo/dynamics + per-segment loudness/brightness spread)
  cp    : co-play latent factors (PPMI-SVD of in-session co-occurrence of train songs) are regressed from audio (ridge);
          a candidate is scored by similarity of its predicted factor to the current rotation's factors
  cpl   : same but similarity to 'loved' mature songs' factors
Embedding caches: .cache/shared/clap-preview-emb/emb.pkl and .cache/shared/hand-audio-feat-v1/feat.pkl (built by build_hand.py).
"""
import os, pickle, numpy as np, pandas as pd
from scipy import sparse
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression, Ridge

ROOT = "/home/user/Listener/taste-model/.cache/shared/"
def _load(p):
    try: return pickle.load(open(p, "rb"))
    except Exception: return {}
_E = {}
def _seg():
    if "s" not in _E: _E["s"] = _load(os.environ.get("B_SEG", ROOT + "hand-audio-feat-v1/seg.pkl"))
    return _E["s"]
def _lc():
    if "l" not in _E: _E["l"] = _load(os.environ.get("B_LC", ROOT + "larger-clap-music-mid-v1/emb.pkl"))
    return _E["l"]
def _clap():
    if "c" not in _E: _E["c"] = _load(os.environ.get("B_EMB", ROOT + "clap-preview-emb/emb.pkl"))
    return _E["c"]
def _hand():
    if "h" not in _E: _E["h"] = _load(os.environ.get("B_HAND", ROOT + "hand-audio-feat-v1/feat.pkl"))
    return _E["h"]

def _sqd(a, b):
    return np.maximum((a * a).sum(1)[:, None] + (b * b).sum(1)[None, :] - 2 * a @ b.T, 0)

def _unit(v): return v / (np.linalg.norm(v) + 1e-9)
def _vecs(meta, table):
    out = {}
    for tid, u in zip(meta.index, meta.previewUrl):
        v = table.get(u) if isinstance(u, str) else None
        if v is not None: out[tid] = v
    return out

def _song_vecs(tr, tv, norm=True):
    vec = {}
    for s, tid in zip(tr.song, tr.trackId):
        if tid in tv: vec.setdefault(s, []).append(tv[tid])
    return {s: (_unit(np.mean(v, 0)) if norm else np.mean(v, 0)) for s, v in vec.items()}

def _factors(t, songs, dim=32, gap=1800, win=4):
    """PPMI-SVD embedding of songs from in-session co-occurrence (positions within `win` of each other, same session)."""
    d = t[["t", "song"]].sort_values("t", kind="stable")
    ts = d.t.values.astype("datetime64[s]").astype("int64")
    sg = pd.Categorical(d.song.values, categories=songs).codes.astype(np.int64)
    sess = np.cumsum(np.diff(ts, prepend=ts[0]) > gap)
    n = len(songs); R = []; Cc = []
    for k in range(1, win + 1):
        m = (sess[k:] == sess[:-k]) & (sg[k:] != sg[:-k])
        R.append(sg[:-k][m]); Cc.append(sg[k:][m])
    R = np.concatenate(R); Cc = np.concatenate(Cc)
    C = sparse.coo_matrix((np.ones(len(R)), (R, Cc)), shape=(n, n)).tocsr(); C = C + C.T
    C.sum_duplicates()
    r = np.asarray(C.sum(1)).ravel(); tot = r.sum()
    C = C.tocoo()
    pc = r ** 0.75 / (r ** 0.75).sum()
    pmi = np.log((C.data / tot) / ((r[C.row] / tot) * pc[C.col] + 1e-12) + 1e-12)
    pmi = np.maximum(pmi - np.log(2.0), 0)
    P = sparse.coo_matrix((pmi, (C.row, C.col)), shape=(n, n)).tocsr()
    from scipy.sparse.linalg import svds
    k = min(dim, n - 2)
    U, S, _ = svds(P, k=k, random_state=0)
    F = U * np.sqrt(S)[None, :]
    return F, r

SEG_DIM = 16
def _seg_score(Zc, M, mask=None, mode="topk"):
    """Zc: (n, nseg, d). For each candidate segment: log kernel density over (weighted) train segments; average the best 2 segments
    (= 'the parts of this song that sit in familiar territory')."""
    Zt, W = (M["sZ"], M["sW"]) if mask is None else (M["sZ"][mask], M["sW"][mask])
    n, k, d = Zc.shape; out = np.zeros(n)
    flat = Zc.reshape(-1, d); res = np.zeros(len(flat))
    for a in range(0, len(flat), 4000):
        sq = _sqd(flat[a:a + 4000], Zt)
        res[a:a + 4000] = np.log((np.exp(-sq / (0.25 * M["smed"])) * W[None, :]).sum(1) + 1e-6)
    res = res.reshape(n, k)
    return np.sort(res, 1)[:, -2:].mean(1) if mode == "topk" else res.mean(1)

_CACHE = {}
def _fit(train, meta, cutoff):
    key = (str(cutoff), len(train), len(meta))
    if key in _CACHE: return _CACHE[key]
    cv, hv = _vecs(meta, _clap()), _vecs(meta, _hand())
    t = train
    g = t.groupby("song"); first = g.t.min(); plays = g.size()
    d = t[["song", "t"]].merge(first.rename("first"), left_on="song", right_index=True)
    in90 = d[(d.t - d["first"]).dt.days < 90]
    p90 = in90.groupby("song").size(); d90 = in90.assign(day=in90.t.dt.floor("D")).groupby("song").day.nunique()
    S = pd.DataFrame({"first": first, "plays": plays, "p90": p90, "d90": d90}).fillna(0)
    S["love"] = ((S.p90 >= 6) & (S.d90 >= 3)).astype(int)
    S["age"] = (cutoff - S["first"]).dt.days
    S["rot"] = t[t.t >= cutoff - pd.Timedelta(days=120)].groupby("song").size().reindex(S.index).fillna(0)
    tr = t.drop_duplicates(["song", "trackId"])[["song", "trackId"]]
    cvec = _song_vecs(tr, cv); cvec2 = _song_vecs(tr, _vecs(meta, _lc())); hvec = _song_vecs(tr, hv, norm=False)
    S["hasc"] = S.index.isin(list(cvec)); S["hasc2"] = S.index.isin(list(cvec2)); S["hash"] = S.index.isin(list(hvec))
    M = {"S": S, "cvec": cvec}
    mat = S[(S.age >= 90) & S.hasc]
    M["ok"] = len(mat) >= 60 and mat.love.nunique() == 2
    # ---------- CLAP terms (round 1) ----------
    if len(cvec) >= 30:
        allv = np.array([cvec[s] for s in S.index[S.hasc]])
        pca = PCA(n_components=min(48, len(allv) - 1), whiten=True, random_state=0).fit(allv); M["pca"] = pca
        if M["ok"]:
            X = pca.transform(np.array([cvec[s] for s in mat.index])); w = 0.5 ** (mat.age.values / 730.0)
            lr = LogisticRegression(C=0.02, max_iter=500).fit(X, mat.love.values, sample_weight=w)
            sc = lr.decision_function(X); M["lr"] = lr; M["lr_mu"], M["lr_sd"] = sc.mean(), sc.std() + 1e-9
        al = S[S.hasc]
        M["dV"] = np.array([cvec[s] for s in al.index]); M["dW"] = np.log1p(al.plays.values)
        km = np.exp(10 * (M["dV"] @ M["dV"].T - 1)) * M["dW"][None, :]; np.fill_diagonal(km, 0)
        loo = np.log(km.sum(1) + 1e-6); M["den_mu"], M["den_sd"] = loo.mean(), loo.std() + 1e-9
    # ---------- larger_clap_music terms (same recipe) ----------
    if len(cvec2) >= 30:
        allv = np.array([cvec2[s] for s in S.index[S.hasc2]])
        pca2 = PCA(n_components=min(48, len(allv) - 1), whiten=True, random_state=0).fit(allv); M["pca2"] = pca
        if M["ok"]:
            X = pca2.transform(np.array([cvec2[s] for s in mat.index])); w = 0.5 ** (mat.age.values / 730.0)
            lr = LogisticRegression(C=0.02, max_iter=500).fit(X, mat.love.values, sample_weight=w)
            sc = lr.decision_function(X); M["lr2"] = lr; M["lr2_mu"], M["lr2_sd"] = sc.mean(), sc.std() + 1e-9
        al = S[S.hasc2]
        M["dV2"] = np.array([cvec2[s] for s in al.index]); M["dW2"] = np.log1p(al.plays.values)
        km = np.exp(10 * (M["dV2"] @ M["dV2"].T - 1)) * M["dW2"][None, :]; np.fill_diagonal(km, 0)
        loo = np.log(km.sum(1) + 1e-6); M["den2_mu"], M["den2_sd"] = loo.mean(), loo.std() + 1e-9
    # ---------- hand-feature density ----------
    if len(hvec) >= 60:
        hs = S.index[S.hash]; H = np.array([hvec[s] for s in hs])
        mu, sd = H.mean(0), H.std(0) + 1e-6; Z = np.clip((H - mu) / sd, -5, 5)
        hp = PCA(n_components=24, whiten=True, random_state=0).fit(Z); Zp = hp.transform(Z)
        M["h"] = (mu, sd, hp)
        sq = _sqd(Zp, Zp)
        M["hmed"] = float(np.median(sq)); M["hZ"] = Zp; M["hW"] = np.log1p(S.loc[hs].plays.values)
        km = np.exp(-sq / (0.25 * M["hmed"])) * M["hW"][None, :]; np.fill_diagonal(km, 0)
        loo = np.log(km.sum(1) + 1e-6); M["hden_mu"], M["hden_sd"] = loo.mean(), loo.std() + 1e-9
    # ---------- segment-level ("parts") density ----------
    sv = _vecs(meta, _seg())
    svec = {}
    for ss, tid in zip(tr.song, tr.trackId):
        if tid in sv and ss not in svec: svec[ss] = sv[tid]
    if len(svec) >= 60:
        ss_ = [x for x in S.index if x in svec]; A = np.array([svec[x] for x in ss_])        # (n, 6, 35)
        flat = A.reshape(-1, A.shape[-1]); mu, sd = flat.mean(0), flat.std(0) + 1e-6
        sp = PCA(n_components=SEG_DIM, whiten=True, random_state=0).fit(np.clip((flat - mu) / sd, -5, 5))
        Zs = sp.transform(np.clip((flat - mu) / sd, -5, 5))
        M["seg"] = (mu, sd, sp); M["sZ"] = Zs; M["sW"] = np.repeat(np.log1p(S.loc[ss_].plays.values), A.shape[1])
        M["sid"] = np.repeat(np.arange(len(ss_)), A.shape[1])
        rs = np.random.RandomState(0); sub = rs.choice(len(Zs), min(2000, len(Zs)), replace=False)
        M["smed"] = float(np.median(_sqd(Zs[sub], Zs[sub])))
        # leave-one-song-out score of train songs (subsample of 600 songs) for z constants
        pick = rs.choice(len(ss_), min(600, len(ss_)), replace=False); vals = []
        for j in pick:
            m = M["sid"] != j; zc = Zs[M["sid"] == j]
            vals.append(_seg_score(zc[None], M, mask=m)[0])
        vals = np.array(vals); M["sden_mu"], M["sden_sd"] = vals.mean(), vals.std() + 1e-9
    # ---------- co-play factors regressed from audio ----------
    songs = list(S.index)
    both = S[S.hasc & S.hash & (S.plays >= 3)]
    if len(both) >= 150 and "h" in M:
        F, r = _factors(t, songs)
        idx = pd.Series(np.arange(len(songs)), index=songs)
        bi = idx.loc[both.index].values
        Fb = F[bi]; nrm = np.linalg.norm(Fb, axis=1); ok = nrm > 1e-6
        both = both[ok]; Fb = Fb[ok] / nrm[ok, None]
        Xa = M["pca"].transform(np.array([cvec[s] for s in both.index]))
        mu, sd, hp = M["h"]
        Xh = hp.transform(np.clip((np.array([hvec[s] for s in both.index]) - mu) / sd, -5, 5))
        X = np.hstack([Xa, 0.7 * Xh]); sw = np.log1p(both.plays.values)
        rg = Ridge(alpha=float(os.environ.get("B_ALPHA", 300.0))).fit(X, Fb, sample_weight=sw)
        # cross-fitted predictions for z constants (5 folds, by song)
        rng = np.random.RandomState(0); fold = rng.randint(0, 5, len(both)); Pcv = np.zeros_like(Fb)
        for k in range(5):
            m = fold != k
            Pcv[~m] = Ridge(alpha=float(os.environ.get("B_ALPHA", 300.0))).fit(X[m], Fb[m], sample_weight=sw[m]).predict(X[~m])
        Pcv /= (np.linalg.norm(Pcv, axis=1, keepdims=True) + 1e-9)
        M["rg"] = rg; M["cpF"] = Fb; M["cpS"] = both
        rot = both.rot.values; M["cpRot"] = np.sqrt(rot)
        lv = both[(both.love == 1)]; M["cpLoveIdx"] = np.where((both.love.values == 1) & (both.age.values >= 90))[0]
        M["cpPcv"] = Pcv
        M["cp_stat"] = {}
        for name in ("cp", "cpl"):
            sc = _cp_score(M, Pcv, name, loo=True)
            M["cp_stat"][name] = (sc.mean(), sc.std() + 1e-9)
    d2 = t[["t", "artistIds"]].explode("artistIds").dropna()
    w = 0.5 ** ((cutoff - d2.t).dt.days.values / 180.0)
    M["art"] = pd.Series(w, index=d2.artistIds.values).groupby(level=0).sum()
    la = np.log1p(M["art"].reindex(t.artist.values).fillna(0).values); M["art_mu"], M["art_sd"] = la.mean(), la.std() + 1e-9
    _CACHE.clear(); _CACHE[key] = M
    return M

def _cp_score(M, P, name, loo=False):
    """P: unit predicted factors (n, dim). similarity to the rotation (cp) / loved songs (cpl) in the behavioural factor space."""
    F = M["cpF"]
    if name == "cp": w = M["cpRot"]; sel = np.where(w > 0)[0]
    else: sel = M["cpLoveIdx"]; w = np.ones(len(F))
    if len(sel) == 0: return np.zeros(len(P))
    sim = P @ F[sel].T
    k = np.exp(6 * (sim - 1)) * w[sel][None, :]
    if loo:   # remove self when scoring train songs
        pos = {j: i for i, j in enumerate(sel)}
        for j, i in pos.items(): k[j, i] = 0
    return np.log(k.sum(1) + 1e-6)

def _components(train, cands, meta, cutoff):
    M = _fit(train, meta, cutoff); n = len(cands); out = {}
    cv, hv = _vecs(meta, _clap()), _vecs(meta, _hand())
    V = np.zeros((n, 768), np.float32); hc = np.zeros(n, bool)
    Hh = np.zeros((n, 93), np.float32); hh = np.zeros(n, bool)
    for i, tid in enumerate(cands.trackId.values):
        if tid in cv: V[i] = _unit(cv[tid]); hc[i] = True
        if tid in hv: Hh[i] = hv[tid]; hh[i] = True
    sden = np.zeros(n)
    if "seg" in M:
        sv = _vecs(meta, _seg()); idx = [i for i, tid in enumerate(cands.trackId.values) if tid in sv]
        if idx:
            mu, sd, sp = M["seg"]; A = np.array([sv[cands.trackId.values[i]] for i in idx])
            Zc = sp.transform(np.clip((A.reshape(-1, A.shape[-1]) - mu) / sd, -5, 5)).reshape(len(idx), A.shape[1], -1)
            sden[idx] = (_seg_score(Zc, M) - M["sden_mu"]) / M["sden_sd"]
    lr = np.zeros(n); den = np.zeros(n); hden = np.zeros(n); cp = np.zeros(n); cpl = np.zeros(n)
    if "lr" in M and hc.any():
        lr[hc] = (M["lr"].decision_function(M["pca"].transform(V[hc])) - M["lr_mu"]) / M["lr_sd"]
    if "dV" in M and hc.any():
        den[hc] = (np.log((np.exp(10 * (V[hc] @ M["dV"].T - 1)) * M["dW"][None, :]).sum(1) + 1e-6) - M["den_mu"]) / M["den_sd"]
    if "h" in M and hh.any():
        mu, sd, hp = M["h"]; Zp = hp.transform(np.clip((Hh[hh] - mu) / sd, -5, 5))
        sq = _sqd(Zp, M["hZ"])
        hden[hh] = (np.log((np.exp(-sq / (0.25 * M["hmed"])) * M["hW"][None, :]).sum(1) + 1e-6) - M["hden_mu"]) / M["hden_sd"]
        if "rg" in M and (hh & hc).any():
            b = hh & hc
            Xa = M["pca"].transform(V[b]); Xh = hp.transform(np.clip((Hh[b] - mu) / sd, -5, 5))
            P = M["rg"].predict(np.hstack([Xa, 0.7 * Xh])); P /= (np.linalg.norm(P, axis=1, keepdims=True) + 1e-9)
            for name, arr in (("cp", cp), ("cpl", cpl)):
                m_, s_ = M["cp_stat"][name]; arr[b] = (_cp_score(M, P, name) - m_) / s_
    art = np.array([max([M["art"].get(a, 0.0) for a in ids], default=0.0) for ids in cands.artistIds])
    out.update(sden=sden, den=den, lr=lr, hden=hden, cp=cp, cpl=cpl, art=(np.log1p(art) - M["art_mu"]) / M["art_sd"])
    return out

def _tie(c): return (c.trackId.values % 1000003) / 1e12

def _mk(w):
    def f(train, cands, meta, cutoff):
        c = _components(train, cands, meta, cutoff)
        return sum(w[k] * c[k] for k in w) + _tie(cands)
    return f

PREDICTORS = dict(
    B2_base=_mk(dict(den=1.0, lr=0.5, art=0.5)),                       # round-1 blend (control)
    B2_hden=_mk(dict(hden=1.0)),
    B2_cp=_mk(dict(cp=1.0)),
    B2_cpl=_mk(dict(cpl=1.0)),
    B2_blend=_mk(dict(den=1.0, lr=0.5, art=0.5, hden=0.5, cp=0.5, cpl=0.5)),
)
