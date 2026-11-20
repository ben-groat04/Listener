"""Builder B: CLAP audio embeddings (10 s middle of the 30 s preview) + a per-cutoff taste model fitted only on train history.
Embeddings: .cache/shared/clap-preview-emb/emb.pkl  {previewUrl: 768-d float32}  (built by build_dl.py + build_embed.py; keyed by preview URL).
Components (all fitted on train only, scores standardised with train-derived constants so candidates stay independent):
  lr   : logistic regression on PCA(audio) -> 'loved' label of mature train songs (recency weighted)
  rot  : similarity of the candidate to songs in current rotation (play-weighted kNN kernel)
  art  : log recency-weighted artist plays
"""
import os, pickle, numpy as np, pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

EMB_PATH = os.environ.get("B_EMB", "/home/user/Listener/taste-model/.cache/shared/clap-preview-emb/emb.pkl")
_E = {}
def _emb():
    if "e" not in _E:
        try: _E["e"] = pickle.load(open(EMB_PATH, "rb"))
        except Exception: _E["e"] = {}
    return _E["e"]

def _unit(v): return v / (np.linalg.norm(v) + 1e-9)

def _track_vecs(meta):
    e = _emb(); out = {}
    for tid, u in zip(meta.index, meta.previewUrl):
        v = e.get(u) if isinstance(u, str) else None
        if v is not None: out[tid] = v
    return out

_CACHE = {}
def _fit(train, meta, cutoff):
    key = (str(cutoff), len(train), len(meta))
    if key in _CACHE: return _CACHE[key]
    tv = _track_vecs(meta)
    t = train
    g = t.groupby("song")
    first = g.t.min(); plays = g.size()
    d = t[["song", "t", "trackId"]].merge(first.rename("first"), left_on="song", right_index=True)
    in90 = d[(d.t - d["first"]).dt.days < 90]
    p90 = in90.groupby("song").size(); d90 = in90.assign(day=in90.t.dt.floor("D")).groupby("song").day.nunique()
    S = pd.DataFrame({"first": first, "plays": plays, "p90": p90, "d90": d90}).fillna(0)
    S["love"] = ((S.p90 >= 6) & (S.d90 >= 3)).astype(int)
    S["age"] = (cutoff - S["first"]).dt.days
    # last-120d rotation
    rec = t[t.t >= cutoff - pd.Timedelta(days=120)].groupby("song").size()
    S["rot"] = rec.reindex(S.index).fillna(0)
    # song vectors
    tr = t.drop_duplicates(["song", "trackId"])[["song", "trackId"]]
    tr = tr[tr.trackId.isin(tv.keys())]
    vec = {}
    for s, tid in zip(tr.song, tr.trackId): vec.setdefault(s, []).append(tv[tid])
    vec = {s: _unit(np.mean(v, 0)) for s, v in vec.items()}
    S["has"] = S.index.isin(list(vec))
    M = {"S": S, "vec": vec}
    mat = S[(S.age >= 90) & S.has]
    M["ok"] = len(mat) >= 60 and mat.love.nunique() == 2
    if len(vec) >= 30:
        allv = np.array([vec[s] for s in S.index[S.has]])
        pca = PCA(n_components=min(48, len(allv) - 1), whiten=True, random_state=0).fit(allv)
        M["pca"] = pca
        if M["ok"]:
            X = pca.transform(np.array([vec[s] for s in mat.index]))
            w = 0.5 ** (mat.age.values / 730.0)
            lr = LogisticRegression(C=0.02, max_iter=500).fit(X, mat.love.values, sample_weight=w)
            M["lr"] = lr; sc = lr.decision_function(X); M["lr_mu"], M["lr_sd"] = sc.mean(), sc.std() + 1e-9
        if M["ok"]:
            M["mV"] = np.array([vec[s] for s in mat.index]); M["mY"] = mat.love.values.astype(float)
            M["mW"] = 0.5 ** (mat.age.values / 730.0); M["prior"] = float(np.average(M["mY"], weights=M["mW"]))
        al = S[S.has]
        M["dV"] = np.array([vec[s] for s in al.index]); M["dW"] = np.log1p(al.plays.values)
        rs = S[(S.rot > 0) & S.has]
        M["rotS"] = rs
        if len(rs):
            M["rotV"] = np.array([vec[s] for s in rs.index]); M["rotW"] = np.sqrt(rs.rot.values)
    # artist table
    d2 = t[["t", "artistIds"]].explode("artistIds").dropna()
    w = 0.5 ** ((cutoff - d2.t).dt.days.values / 180.0)
    M["art"] = pd.Series(w, index=d2.artistIds.values).groupby(level=0).sum()
    _CACHE.clear(); _CACHE[key] = M
    return M

def _cand_vecs(cands, meta):
    tv = _track_vecs(meta)
    V = np.zeros((len(cands), 768), np.float32); has = np.zeros(len(cands), bool)
    for i, tid in enumerate(cands.trackId.values):
        if tid in tv: V[i] = _unit(tv[tid]); has[i] = True
    return V, has

def _components(train, cands, meta, cutoff):
    M = _fit(train, meta, cutoff); V, has = _cand_vecs(cands, meta)
    n = len(cands); out = {}
    lr = np.zeros(n)
    if "lr" in M and has.any():
        lr[has] = (M["lr"].decision_function(M["pca"].transform(V[has])) - M["lr_mu"]) / M["lr_sd"]
    out["lr"] = lr
    rot = np.zeros(n)
    if "rotV" in M and has.any():
        sim = V[has] @ M["rotV"].T
        k = np.exp(8 * (sim - 1)) * M["rotW"][None, :]   # sharp kernel
        rot[has] = np.log(k.sum(1) + 1e-6)
    out["rot"] = rot
    knn = np.zeros(n); den = np.zeros(n)
    if has.any() and "dV" in M:
        sim = V[has] @ M["dV"].T
        den[has] = np.log((np.exp(10 * (sim - 1)) * M["dW"][None, :]).sum(1) + 1e-6)
        if "mV" in M:
            k = np.exp(10 * (V[has] @ M["mV"].T - 1)) * M["mW"][None, :]
            knn[has] = (k @ M["mY"] + 0.5 * M["prior"]) / (k.sum(1) + 0.5)
    out["knn"] = knn; out["den"] = den
    art = np.array([max([M["art"].get(a, 0.0) for a in ids], default=0.0) for ids in cands.artistIds])
    out["art"] = np.log1p(art)
    out["has"] = has.astype(float)
    return out

def _tie(c): return (c.trackId.values % 1000003) / 1e12

def lr_only(train, cands, meta, cutoff): return _components(train, cands, meta, cutoff)["lr"] + _tie(cands)
def rot_only(train, cands, meta, cutoff): return _components(train, cands, meta, cutoff)["rot"] + _tie(cands)
def art_only(train, cands, meta, cutoff): return _components(train, cands, meta, cutoff)["art"] + _tie(cands)

W = dict(lr=1.0, rot=0.3, art=0.3)
def blend(train, cands, meta, cutoff):
    c = _components(train, cands, meta, cutoff)
    return W["lr"] * c["lr"] + W["rot"] * c["rot"] / 3 + W["art"] * c["art"] + _tie(cands)

def knn_only(train, cands, meta, cutoff): return _components(train, cands, meta, cutoff)["knn"] + _tie(cands)
def den_only(train, cands, meta, cutoff): return _components(train, cands, meta, cutoff)["den"] + _tie(cands)

PREDICTORS = dict(B_knn=knn_only, B_den=den_only, B_lr=lr_only, B_rot=rot_only, B_art=art_only, B_blend=blend)
