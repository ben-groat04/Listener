"""Builder B round 2 ('B2'): audio typicality + audio->love logistic + artist recency, with two extra hand-crafted audio views.
All terms are fitted on train only and z-scored with train-derived constants, so a candidate's score never depends on the other candidates.
  den  : CLAP (laion/clap-htsat-unfused, 10 s middle of the 30 s preview) play-weighted kernel density over embedded train songs (leave-one-out z)
  lr   : logistic regression on whitened CLAP-PCA-48 -> 'loved' of mature train songs (first play >= 90 d before cutoff; 2-year half-life weights)
  art  : log recency-weighted (180 d half-life) artist plays
  hden : kernel density in whitened hand-crafted feature space (MFCC/chroma/contrast/mel/tempo/dynamics, 93 dims -> PCA-24)
  sden : 'parts' density: 6 x 5 s segments per preview (MFCC+chroma+loudness/brightness/onset), a candidate is scored by the mean log-density of its
         two best-fitting segments against all train segments
Caches (built by build_features.py / ../B-audio): .cache/shared/{clap-preview-emb,hand-audio-feat-v1}/ ; missing caches -> neutral zeros.
Predictors: B2_final = den + .5 lr + .5 art (the round-1 blend, re-validated; the extra views did not help), B2_plus = B2_final + .3 hden + .3 sden, ablations B2_*.
"""
import os, pickle, numpy as np, pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

ROOT = "/home/user/Listener/taste-model/.cache/shared/"
SEG_DIM = 16
def _load(p):
    try: return pickle.load(open(p, "rb"))
    except Exception: return {}
_E = {}
def _tab(k, env, rel):
    if k not in _E: _E[k] = _load(os.environ.get(env, ROOT + rel))
    return _E[k]
def _clap(): return _tab("c", "B_EMB", "clap-preview-emb/emb.pkl")
def _hand(): return _tab("h", "B_HAND", "hand-audio-feat-v1/feat.pkl")
def _seg(): return _tab("s", "B_SEG", "hand-audio-feat-v1/seg.pkl")

def _sqd(a, b): return np.maximum((a * a).sum(1)[:, None] + (b * b).sum(1)[None, :] - 2 * a @ b.T, 0)
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

def _seg_score(Zc, M, mask=None):
    Zt, W = (M["sZ"], M["sW"]) if mask is None else (M["sZ"][mask], M["sW"][mask])
    n, k, d = Zc.shape; flat = Zc.reshape(-1, d); res = np.zeros(len(flat))
    for a in range(0, len(flat), 4000):
        res[a:a + 4000] = np.log((np.exp(-_sqd(flat[a:a + 4000], Zt) / (0.25 * M["smed"])) * W[None, :]).sum(1) + 1e-6)
    return np.sort(res.reshape(n, k), 1)[:, -2:].mean(1)

_CACHE = {}
def _fit(train, meta, cutoff):
    key = (str(cutoff), len(train), len(meta))
    if key in _CACHE: return _CACHE[key]
    t = train
    g = t.groupby("song"); first = g.t.min(); plays = g.size()
    d = t[["song", "t"]].merge(first.rename("first"), left_on="song", right_index=True)
    in90 = d[(d.t - d["first"]).dt.days < 90]
    p90 = in90.groupby("song").size(); d90 = in90.assign(day=in90.t.dt.floor("D")).groupby("song").day.nunique()
    S = pd.DataFrame({"first": first, "plays": plays, "p90": p90, "d90": d90}).fillna(0)
    S["love"] = ((S.p90 >= 6) & (S.d90 >= 3)).astype(int); S["age"] = (cutoff - S["first"]).dt.days
    tr = t.drop_duplicates(["song", "trackId"])[["song", "trackId"]]
    cvec = _song_vecs(tr, _vecs(meta, _clap())); hvec = _song_vecs(tr, _vecs(meta, _hand()), norm=False)
    S["hasc"] = S.index.isin(list(cvec)); S["hash"] = S.index.isin(list(hvec))
    M = {}
    mat = S[(S.age >= 90) & S.hasc]
    if len(cvec) >= 30:
        allv = np.array([cvec[s] for s in S.index[S.hasc]])
        M["pca"] = pca = PCA(n_components=min(48, len(allv) - 1), whiten=True, random_state=0).fit(allv)
        if len(mat) >= 60 and mat.love.nunique() == 2:
            X = pca.transform(np.array([cvec[s] for s in mat.index])); w = 0.5 ** (mat.age.values / 730.0)
            lr = LogisticRegression(C=0.02, max_iter=500).fit(X, mat.love.values, sample_weight=w)
            sc = lr.decision_function(X); M["lr"] = lr; M["lr_mu"], M["lr_sd"] = sc.mean(), sc.std() + 1e-9
        al = S[S.hasc]
        M["dV"] = np.array([cvec[s] for s in al.index]); M["dW"] = np.log1p(al.plays.values)
        km = np.exp(10 * (M["dV"] @ M["dV"].T - 1)) * M["dW"][None, :]; np.fill_diagonal(km, 0)
        loo = np.log(km.sum(1) + 1e-6); M["den_mu"], M["den_sd"] = loo.mean(), loo.std() + 1e-9
    if len(hvec) >= 60:
        hs = S.index[S.hash]; H = np.array([hvec[s] for s in hs])
        mu, sd = H.mean(0), H.std(0) + 1e-6; Z = np.clip((H - mu) / sd, -5, 5)
        hp = PCA(n_components=24, whiten=True, random_state=0).fit(Z); Zp = hp.transform(Z)
        M["h"] = (mu, sd, hp); sq = _sqd(Zp, Zp); M["hmed"] = float(np.median(sq)); M["hZ"] = Zp; M["hW"] = np.log1p(S.loc[hs].plays.values)
        km = np.exp(-sq / (0.25 * M["hmed"])) * M["hW"][None, :]; np.fill_diagonal(km, 0)
        loo = np.log(km.sum(1) + 1e-6); M["hden_mu"], M["hden_sd"] = loo.mean(), loo.std() + 1e-9
    sv = _vecs(meta, _seg()); svec = {}
    for ss, tid in zip(tr.song, tr.trackId):
        if tid in sv and ss not in svec: svec[ss] = sv[tid]
    if len(svec) >= 60:
        ss_ = [x for x in S.index if x in svec]; A = np.array([svec[x] for x in ss_])
        flat = A.reshape(-1, A.shape[-1]); mu, sd = flat.mean(0), flat.std(0) + 1e-6
        sp = PCA(n_components=SEG_DIM, whiten=True, random_state=0).fit(np.clip((flat - mu) / sd, -5, 5))
        Zs = sp.transform(np.clip((flat - mu) / sd, -5, 5))
        M["seg"] = (mu, sd, sp); M["sZ"] = Zs; M["sW"] = np.repeat(np.log1p(S.loc[ss_].plays.values), A.shape[1])
        M["sid"] = np.repeat(np.arange(len(ss_)), A.shape[1])
        rs = np.random.RandomState(0); sub = rs.choice(len(Zs), min(2000, len(Zs)), replace=False)
        M["smed"] = float(np.median(_sqd(Zs[sub], Zs[sub])))
        pick = rs.choice(len(ss_), min(600, len(ss_)), replace=False)
        vals = np.array([_seg_score(Zs[M["sid"] == j][None], M, mask=M["sid"] != j)[0] for j in pick])
        M["sden_mu"], M["sden_sd"] = vals.mean(), vals.std() + 1e-9
    d2 = t[["t", "artistIds"]].explode("artistIds").dropna()
    w = 0.5 ** ((cutoff - d2.t).dt.days.values / 180.0)
    M["art"] = pd.Series(w, index=d2.artistIds.values).groupby(level=0).sum()
    la = np.log1p(M["art"].reindex(t.artist.values).fillna(0).values); M["art_mu"], M["art_sd"] = la.mean(), la.std() + 1e-9
    _CACHE.clear(); _CACHE[key] = M
    return M

def _components(train, cands, meta, cutoff):
    M = _fit(train, meta, cutoff); n = len(cands); tid = cands.trackId.values
    cv, hv, sv = _vecs(meta, _clap()), _vecs(meta, _hand()), _vecs(meta, _seg())
    out = {k: np.zeros(n) for k in ("den", "lr", "hden", "sden")}
    ic = [i for i in range(n) if tid[i] in cv]
    if ic and "dV" in M:
        V = np.array([_unit(cv[tid[i]]) for i in ic])
        out["den"][ic] = (np.log((np.exp(10 * (V @ M["dV"].T - 1)) * M["dW"][None, :]).sum(1) + 1e-6) - M["den_mu"]) / M["den_sd"]
        if "lr" in M: out["lr"][ic] = (M["lr"].decision_function(M["pca"].transform(V)) - M["lr_mu"]) / M["lr_sd"]
    ih = [i for i in range(n) if tid[i] in hv]
    if ih and "h" in M:
        mu, sd, hp = M["h"]; Zp = hp.transform(np.clip((np.array([hv[tid[i]] for i in ih]) - mu) / sd, -5, 5))
        out["hden"][ih] = (np.log((np.exp(-_sqd(Zp, M["hZ"]) / (0.25 * M["hmed"])) * M["hW"][None, :]).sum(1) + 1e-6) - M["hden_mu"]) / M["hden_sd"]
    isg = [i for i in range(n) if tid[i] in sv]
    if isg and "seg" in M:
        mu, sd, sp = M["seg"]; A = np.array([sv[tid[i]] for i in isg])
        Zc = sp.transform(np.clip((A.reshape(-1, A.shape[-1]) - mu) / sd, -5, 5)).reshape(len(isg), A.shape[1], -1)
        out["sden"][isg] = (_seg_score(Zc, M) - M["sden_mu"]) / M["sden_sd"]
    art = np.array([max([M["art"].get(a, 0.0) for a in ids], default=0.0) for ids in cands.artistIds])
    out["art"] = (np.log1p(art) - M["art_mu"]) / M["art_sd"]
    return out

def _tie(c): return (c.trackId.values % 1000003) / 1e12
def _mk(w):
    def f(train, cands, meta, cutoff):
        c = _components(train, cands, meta, cutoff)
        return sum(v * c[k] for k, v in w.items()) + _tie(cands)
    return f

PREDICTORS = dict(
    B2_final=_mk(dict(den=1.0, lr=0.5, art=0.5)),
    B2_plus=_mk(dict(den=1.0, lr=0.5, art=0.5, hden=0.3, sden=0.3)),
    B2_den=_mk(dict(den=1.0)), B2_hden=_mk(dict(hden=1.0)), B2_sden=_mk(dict(sden=1.0)), B2_art=_mk(dict(art=1.0)),
)
