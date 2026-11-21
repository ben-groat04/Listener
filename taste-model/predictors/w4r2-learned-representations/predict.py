"""w4r2-learned-representations: learned (nonlinear / patch-level) models on the per-patch essentia inputs (effnet embeddings 1280-d, 605 head activations),
vs clip-mean linear baselines. Harness entry file; PREDICTORS dict (see bottom).  From /home/user/Listener/taste-model:
  python3 -W ignore predictors/w4r2-learned-representations/build_patches.py   # builds .cache/w4r2-lr/ (5 s)
  python3 -W ignore -m evalkit.run --fast predictors/w4r2-learned-representations/predict.py
Inputs per song: ONLY the song's own essentia patches (+ optional MERT window means). No artist/history input. User history -> training targets only
(rank_plays = percentile of 90-day plays within quarter of first play, mature songs only; optional panel rows not used). Standardiser, PCA, nets: fitted on
train-stream songs only; fit cache keyed on train identities (or off with EVALKIT_NO_FIT_CACHE). Songs without audio get the train-median score."""
import hashlib, os
import numpy as np, pandas as pd
ROOT = "/home/user/Listener/taste-model/"; D = ROOT + ".cache/w4r2-lr/"
CFG = dict(feat="emb", nc=64, model="attn", h=32, ep=60, lr=3e-3, wd=1e-2, drop=0.3, pdrop=0.3, loss="mse", seeds=5, alpha=300.0, target="rank_plays", mert=False, ncm=32, excl_artist=False)
_S = {}

def _store():
    if not _S:
        import os
        if not os.path.exists(D + "md5.npy"):
            import subprocess, sys; subprocess.run([sys.executable, "-W", "ignore", ROOT + "predictors/w4r2-learned-representations/build_patches.py"], check=True, cwd=ROOT)
        md = np.load(D + "md5.npy"); _S["idx"] = {k: i for i, k in enumerate(md)}
        _S["emb"] = np.load(D + "emb.npy", mmap_mode="r"); _S["act"] = np.load(D + "act.npy", mmap_mode="r"); _S["n"] = np.load(D + "n.npy")
    return _S

def _rows(tids, meta):
    S = _store(); u = meta.previewUrl.reindex(tids).values
    ii = np.array([S["idx"].get(hashlib.md5(x.encode()).hexdigest(), -1) if isinstance(x, str) else -1 for x in u]); return ii

def _gather_t(tids, meta, feat):
    """[n,P,d] float32, mask [n,P], ok [n] for the song set tids. feat: emb, act, both (essentia patches) | mert (4 window tokens, layers 4-8 mean) | mertL (4 windows x layers 4,6,8 as 12 tokens)"""
    if feat.startswith("mert"):
        X, ok = _mertw(tids, meta, feat); return X[ok], np.ones(X[ok].shape[:2], bool), ok
    ii = _rows(tids, meta); ok = ii >= 0; X, M = _gather(ii[ok], feat); return X, M, ok

def _gather(ii, feat):
    """[n,29,d] float32 and mask [n,29] for rows ii>=0"""
    S = _store(); o = np.argsort(ii); inv = np.argsort(o); sel = ii[o]
    parts = []
    if feat in ("emb", "both"): parts.append(np.asarray(S["emb"][sel], np.float32))
    if feat in ("act", "both"): parts.append(np.asarray(S["act"][sel], np.float32))
    X = np.concatenate(parts, -1)[inv]; n = S["n"][ii]; M = np.arange(X.shape[1])[None] < n[:, None]
    return X, M

def _mertw(tids, meta, feat="mert"):
    import glob
    if "mert" not in _S:
        keys, arrs = [], []
        for f in sorted(glob.glob(ROOT + ".cache/shared/w3r1-mert-v1/shard_*.npz")):
            z = np.load(f); keys += list(z["md5"]); arrs.append(z["feat"][:, :, [4, 5, 6, 7, 8]].astype(np.float16))
        _S["mert"] = ({k: i for i, k in enumerate(keys)}, np.concatenate(arrs))   # [n,4,5,768]
    idx, arr = _S["mert"]; u = meta.previewUrl.reindex(tids).values
    ii = np.array([idx.get(hashlib.md5(x.encode()).hexdigest(), -1) if isinstance(x, str) else -1 for x in u]); ok = ii >= 0
    if feat == "mertL": X = np.zeros((len(tids), 12, 768), np.float32); sel = [0, 2, 4]
    else: X = np.zeros((len(tids), 4, 768), np.float32)
    if ok.any():
        a = arr[ii[ok]].astype(np.float32)
        X[ok] = a[:, :, [0, 2, 4]].reshape(a.shape[0], 12, 768) if feat == "mertL" else a.mean(2)
    return X, ok

def _pca(Z, nc, seed=0):
    from sklearn.decomposition import PCA
    return PCA(nc, whiten=True, random_state=seed).fit(Z)

def _tf(res, X, M):
    mu, sd, p = res["tf"]; n, P, d = X.shape
    Z = ((X - mu) / sd).reshape(n * P, d); Y = p.transform(Z).reshape(n, P, -1).astype(np.float32); Y[~M] = 0; return Y

def _mk_net(d, cfg):
    import torch, torch.nn as nn
    class Net(nn.Module):
        def __init__(s):
            super().__init__(); s.enc = nn.Sequential(nn.Dropout(cfg["drop"]), nn.Linear(d, cfg["h"]), nn.GELU()); s.att = nn.Linear(cfg["h"], 1); s.out = nn.Linear(cfg["h"], 1); s.pool = cfg["model"]
        def forward(s, X, M):
            h = s.enc(X); m = M.float().unsqueeze(-1)
            if s.pool == "attn":
                a = s.att(h).masked_fill(~M.unsqueeze(-1), -1e9).softmax(1); z = (a * h).sum(1)
            elif s.pool == "max": z = h.masked_fill(~M.unsqueeze(-1), -1e9).max(1).values
            else: z = (h * m).sum(1) / m.sum(1).clamp(min=1)
            return s.out(z).squeeze(-1)
    return Net()

def _train_net(Y, M, y, cfg, seed):
    import torch
    torch.manual_seed(seed); g = torch.Generator().manual_seed(seed)
    net = _mk_net(Y.shape[-1], cfg); opt = torch.optim.AdamW(net.parameters(), lr=cfg["lr"], weight_decay=cfg["wd"])
    Yt, Mt, yt = torch.tensor(Y), torch.tensor(M), torch.tensor(y, dtype=torch.float32); n = len(yt); bs = 64
    for ep in range(cfg["ep"]):
        net.train(); perm = torch.randperm(n, generator=g)
        for i in range(0, n, bs):
            b = perm[i:i + bs]; m = Mt[b]
            if cfg["pdrop"] and cfg["model"] != "mean0":   # random patch dropout (augmentation): keep >=1 patch
                keep = torch.rand(m.shape, generator=g) > cfg["pdrop"]; m2 = m & keep; m2[:, 0] |= ~m2.any(1) & m[:, 0]; m = m2
            s = net(Yt[b], m)
            if cfg["loss"] == "mse": loss = ((s - yt[b]) ** 2).mean()
            else:
                dy = yt[b][:, None] - yt[b][None]; ds = s[:, None] - s[None]; w = (dy.abs() > 0.05).float(); loss = (w * torch.nn.functional.softplus(-torch.sign(dy) * ds)).sum() / w.sum().clamp(min=1)
            opt.zero_grad(); loss.backward(); opt.step()
    net.eval(); return net

def _net_score(nets, Y, M):
    import torch
    out = np.zeros(len(Y))
    with torch.no_grad():
        for net in nets:
            for i in range(0, len(Y), 512): out[i:i + 512] += net(torch.tensor(Y[i:i + 512]), torch.tensor(M[i:i + 512])).numpy()
    return out / len(nets)

_CACHE = {}
def _fit(train, meta, cutoff, cfg):
    key = (str(cutoff), len(train), int(train.t.values.astype("int64").sum() % (1 << 60)), int(pd.util.hash_pandas_object(train[["trackId", "song"]].astype(str), index=False).sum() % (1 << 60)), int(pd.util.hash_pandas_object(train[["trackId", "artist"]].astype(str), index=False).sum() % (1 << 60)), repr(sorted(cfg.items())))
    if key in _CACHE and not os.environ.get("EVALKIT_NO_FIT_CACHE"): return _CACHE[key]
    from threadpoolctl import threadpool_limits
    from sklearn.linear_model import Ridge
    import torch; torch.set_num_threads(2)
    from evalkit.data import song_table
    st = song_table(train).reset_index(); st = st[st.trackId.isin(meta.index)].reset_index(drop=True)
    with threadpool_limits(2):
        X, M, ok = _gather_t(st.trackId.values, meta, cfg["feat"]); rng = np.random.RandomState(0)
        flat = X[M]; mu = flat.mean(0); sd = flat.std(0) + 1e-6
        sub = flat[rng.choice(len(flat), min(len(flat), 30000), replace=False)]
        p = _pca((sub - mu) / sd, cfg["nc"]); res = dict(tf=(mu, sd, p)); Y = _tf(res, X, M)
        mat = ((st["first"] < cutoff - pd.Timedelta(days=90)).values)[ok]
        qa = st["first"].dt.to_period("Q").astype(str).values[ok]
        col = st.plays90.values[ok]
        if cfg["target"] == "rank_plays": yr = pd.Series(col[mat]).groupby(qa[mat]).rank(pct=True).values
        else: yr = st.love.values[ok][mat].astype(float)
        yr = yr - yr.mean(); arts = st.artist.values[ok][mat]
        res["m"] = None; res["nets"] = None; res["ridge"] = None
        if mat.sum() > 40:
            Ym, Mm = Y[mat], M[mat]
            if cfg["model"] == "ridge":   # clip-mean linear control
                cm = Ym.sum(1) / Mm.sum(1, keepdims=True); res["ridge"] = Ridge(alpha=cfg["alpha"]).fit(cm, yr)
            elif cfg["model"] == "patchridge":   # every patch a row (time-local linear control)
                res["ridge"] = Ridge(alpha=cfg["alpha"]).fit(Ym[Mm], np.repeat(yr, Mm.sum(1)))
            else:
                res["nets"] = [_train_net(Ym, Mm, yr * 3, cfg, s) for s in range(cfg["seeds"])]
        sc = _raw(res, Y, M, cfg); res["tm"], res["ts"], res["neutral"] = float(sc.mean()), float(sc.std() + 1e-9), float(np.median(sc))
    _CACHE[key] = res; return res

def _raw(res, Y, M, cfg):
    if res["nets"] is not None: return _net_score(res["nets"], Y, M)
    if res["ridge"] is None: return np.zeros(len(Y))
    if cfg["model"] == "ridge": return res["ridge"].predict(Y.sum(1) / M.sum(1, keepdims=True))
    s = res["ridge"].predict(Y.reshape(-1, Y.shape[-1])).reshape(Y.shape[0], -1); return (s * M).sum(1) / M.sum(1)

def make(**kw):
    cfg = {**CFG, **kw}
    def predict(train, cands, meta, cutoff):
        if cfg["excl_artist"]:   # diagnostic: for each candidate artist, refit without that artist's train songs (slow; used on a subsample only)
            raise NotImplementedError
        res = _fit(train, meta, cutoff, cfg); X, M, ok = _gather_t(cands.trackId.values, meta, cfg["feat"]); s = np.full(len(cands), res["neutral"])
        if ok.any(): s[ok] = _raw(res, _tf(res, X, M), M, cfg)
        return (s - res["tm"]) / res["ts"]
    return predict

def ens(*fns):
    def predict(train, cands, meta, cutoff):
        o = 0
        for f in fns:
            x = f(train, cands, meta, cutoff); o = o + (x - x.mean()) / (x.std() + 1e-9) if False else o + x
        return o / len(fns)
    return predict

M_PR = make(model="patchridge", feat="mert", alpha=1200.0, nc=64)
A_RM = make(model="ridge", feat="act")
E_PR = make(model="patchridge", feat="emb")
M_MLP = make(model="mean", feat="mert", nc=32)
M_ATT = make(model="attn", feat="mert", nc=32, pdrop=0.25)
PREDICTORS = {
    "mlp_mert_reg": make(model="mean", feat="mert", nc=32, h=16, ep=30, drop=0.5, wd=0.1),
    "attn_mert_rank": make(model="attn", feat="mert", nc=32, loss="rank", pdrop=0.25),
    "attn_mertL": make(model="attn", feat="mertL", nc=32, pdrop=0.25),
    "ens_lin3": ens(M_PR, A_RM, E_PR),
    "ens_lin2": ens(M_PR, A_RM),
    "ens_lin3_nets": ens(M_PR, A_RM, E_PR, M_MLP, M_ATT),
}
