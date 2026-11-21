"""Artist-excluded scoring of the FINAL predictors (TUNE, tried songs; diagnostic, not a harness run).  Per fold, the artists of the tried songs are split into 4 random buckets; for bucket k, the predictor is refitted on train streams
WITHOUT any stream whose primary artist is in bucket k and scores the tried songs of bucket k.  So no tried song is scored by a model that saw a same-artist training song.  Reported: fold-stratified AUC pooled over folds
(known = artist had train songs, new = no train songs, so identical to the normal fit), artist-cluster bootstrap CI of the paired difference excluded - normal.
Usage: python3 -W ignore predictors/w4r1-what-in-the-music/artist_excluded_cv.py OUT.pkl"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, "/home/user/Listener/taste-model/predictors/w4r1-what-in-the-music")
from evalkit import run, data
import predict as P
fns = dict(P.PREDICTORS); fns["ref_audio_final"] = run.ref_fn()
rec = []
for F in run.prepare_folds(data.TUNE_CUTOFFS, "main"):
    pool = F["pool"].iloc[F["order"]].reset_index(drop=True); cands, meta, train, c = F["cands"], F["meta"], F["train"], F["c"]
    tried = (pool.is_decoy == 0).values; art = cands.artist.values
    ua = np.unique(art[tried]); rng = np.random.default_rng(int(c.strftime("%Y%m%d"))); bucket = dict(zip(ua, rng.integers(0, 4, len(ua))))
    bk = np.array([bucket.get(a, -1) for a in art]); known = np.isin(art, train.artist.unique())
    out = {k: np.full(len(cands), np.nan) for k in fns}
    for k in range(4):
        rows = np.where(tried & (bk == k))[0]
        if not len(rows): continue
        tr = train[~train.artist.isin(ua[[bucket[a] == k for a in ua]])]
        for nm, fn in fns.items(): out[nm][rows] = fn(tr.copy(), cands.iloc[rows].reset_index(drop=True), meta, c)
    for nm, fn in fns.items():
        s0 = np.asarray(fn(train.copy(), cands, meta, c), float)
        rec.append(pd.DataFrame(dict(model=nm, fold=str(c.date()), artist=art, love=pool.love.values, s0=s0, s1=out[nm], known=known, tried=tried)).query("tried"))
    print("fold", c.date(), flush=True)
D = pd.concat(rec, ignore_index=True); D.to_pickle(sys.argv[1])
def sauc(df, col):
    num = den = 0.0
    for f, g in df.groupby("fold"):
        p = g[col][g.love == 1].values; n = g[col][g.love == 0].values
        if len(p) and len(n): num += ((p[:, None] > n[None]) + .5 * (p[:, None] == n[None])).sum(); den += len(p) * len(n)
    return num / den
def boot(df, nb=100, seed=0):
    rng = np.random.default_rng(seed); ua = df.artist.unique(); g = {a: x for a, x in df.groupby("artist")}; o = []
    for b in range(nb):
        d = pd.concat([g[a] for a in rng.choice(ua, len(ua))], ignore_index=True); o.append(sauc(d, "s1") - sauc(d, "s0"))
    return np.percentile(o, [2.5, 97.5]).round(3)
for nm in fns:
    d = D[D.model == nm]; k = d[d.known]
    print(f"{nm:16s} all: normal {sauc(d,'s0'):.3f} artist-excluded {sauc(d,'s1'):.3f} | known n={len(k)}: normal {sauc(k,'s0'):.3f} excluded {sauc(k,'s1'):.3f} delta CI95 {boot(k)}")
