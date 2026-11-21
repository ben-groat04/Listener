"""Artist-proxy check (TUNE, tried songs).  For each fold and each artist with tried songs, the essentia ridge models are refitted on train songs WITHOUT that artist's songs, and that artist's tried songs are scored by the refit.
Compare the stratified AUC (fold-stratified, pooled) with the normal fit.  Also reported: songs whose artist has NO train songs (new artist; identical in both) vs artists with train songs.  Diagnostic only, not a predictor.
Run: python3 -W ignore predictors/w4r1-what-in-the-music/artist_proxy.py"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, "/home/user/Listener/taste-model/predictors/w4r1-what-in-the-music")
from evalkit import run, data
from sklearn.linear_model import Ridge
import predict as P
folds = run.prepare_folds(data.TUNE_CUTOFFS, "main")
CFGS = {"A_act": {**P.CFG, "alpha": 10000.0}, "SL_lateseg": {**P.CFG, "feat": "seg", "seg": (3, 4, 5), "alpha": 10000.0}, "EM_emb": {**P.CFG, "feat": "emb", "alpha": 30000.0}}
rec = []
for F in folds:
    pool = F["pool"].iloc[F["order"]].reset_index(drop=True); cands, meta = F["cands"], F["meta"]; tried = (pool.is_decoy == 0).values
    st = data.song_table(F["train"]).reset_index(); st = st[st.trackId.isin(meta.index)].reset_index(drop=True)
    qa = st["first"].dt.to_period("Q").astype(str).values
    for nm, cfg in CFGS.items():
        Xt, okt = P._view(st.trackId.values, meta, cfg); n, S, D = Xt.shape
        mat = (st["first"] < F["c"] - pd.Timedelta(days=90)).values & okt
        mu = Xt[okt].mean((0, 1)); sd = Xt[okt].std((0, 1)) + 1e-6; Z = (Xt - mu) / sd
        yr = np.full(len(st), np.nan); yr[mat] = pd.Series(st.plays90.values[mat]).groupby(qa[mat]).rank(pct=True).values
        Xc, okc = P._view(cands.trackId.values, meta, cfg); Zc = ((Xc - mu) / sd)
        def fit(keep):
            m = mat & keep; r = Ridge(alpha=cfg["alpha"]).fit(Z[m].reshape(-1, D), np.repeat(yr[m], S)); return r
        def score(r, rows): return r.predict(Zc[rows].reshape(-1, D)).reshape(-1, S).mean(1)
        r0 = fit(np.ones(len(st), bool)); s0 = np.full(len(cands), np.nan); s0[okc] = score(r0, np.where(okc)[0])
        s1 = s0.copy(); trart = st.artist.values
        for a in np.unique(cands.artist.values[tried & okc]):
            rows = np.where((cands.artist.values == a) & tried & okc)[0]
            has = (trart == a).any()
            if not has: continue
            r1 = fit(trart != a); s1[rows] = score(r1, rows)
        known = np.isin(cands.artist.values, trart)
        rec.append(pd.DataFrame(dict(model=nm, fold=str(F["c"].date()), artist=cands.artist.values, love=pool.love.values, s0=s0, s1=s1, known=known, tried=tried, ok=okc)).query("tried and ok"))
D = pd.concat(rec, ignore_index=True)
def sauc(df, col):
    num = den = 0.0
    for f, g in df.groupby("fold"):
        p = g[col][g.love == 1].values; n = g[col][g.love == 0].values
        if len(p) and len(n): num += ((p[:, None] > n[None]) + .5 * (p[:, None] == n[None])).sum(); den += len(p) * len(n)
    return num / den
def boot(df, col0, col1, nb=200, seed=0):
    rng = np.random.default_rng(seed); ua = df.artist.unique(); out = []
    g = {a: x for a, x in df.groupby("artist")}
    for b in range(nb):
        pick = rng.choice(ua, len(ua)); d = pd.concat([g[a] for a in pick], ignore_index=True); out.append(sauc(d, col1) - sauc(d, col0))
    return np.percentile(out, [2.5, 97.5])
for nm in CFGS:
    d = D[D.model == nm]; k = d[d.known]
    print(f"{nm}: all n={len(d)} sauc normal {sauc(d,'s0'):.3f} | known-artist n={len(k)} normal {sauc(k,'s0'):.3f}  same-artist-songs-excluded {sauc(k,'s1'):.3f}  delta CI95 {boot(k,'s0','s1',60)} | new-artist n={(~d.known).sum()} {sauc(d[~d.known],'s0'):.3f}")
D.to_pickle(sys.argv[1] if len(sys.argv) > 1 else "/tmp/proxy.pkl")
