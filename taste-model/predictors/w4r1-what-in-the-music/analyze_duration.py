"""Descriptive (TUNE tried songs only): love rate by duration bucket and title flags, within-artist AUC of duration and of log duration relative to the artist's median over that artist's tried songs in the fold."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import run, data
folds = run.prepare_folds(data.TUNE_CUTOFFS, "main"); R = []
for F in folds:
    pool = F["pool"].iloc[F["order"]].reset_index(drop=True); m = F["meta"].reindex(F["cands"].trackId.values)
    d = pd.DataFrame(dict(fold=str(F["c"].date()), artist=F["cands"].artist.values, love=pool.love.values, tried=(pool.is_decoy == 0).values, dur=m.durationMs.values / 1000, name=pool.trackName.values, album=m.albumName.values, plays90=pool.plays90.values))
    R.append(d[d.tried])
D = pd.concat(R, ignore_index=True); print(len(D), D.love.mean())
D["b"] = pd.cut(D.dur, [0, 90, 150, 180, 210, 240, 270, 300, 360, 1e5]); print(D.groupby("b", observed=True).love.agg(["size", "mean"]).round(3))
low = D.name.str.lower().fillna("")
for k, rx in dict(live=r"\blive\b", remix=r"remix|mix\)|edit", remaster=r"remaster", feat=r"feat\.|with ", acoustic="acoustic", interlude=r"interlude|intro|outro|skit", version="version").items():
    f = low.str.contains(rx); print(k, f.sum(), round(D.love[f].mean(), 3), "vs rest", round(D.love[~f].mean(), 3))
def wa_auc(x):
    num = den = 0
    for (f, a), g in D.assign(x=x).groupby(["fold", "artist"]):
        p = g.x[g.love == 1].values; n = g.x[g.love == 0].values
        if len(p) and len(n): num += ((p[:, None] > n[None]) + .5 * (p[:, None] == n[None])).sum(); den += len(p) * len(n)
    return num / den, den
print("within-artist AUC of duration (longer->loved)", wa_auc(D.dur.values))
print("within-artist AUC of |log(dur/180)|", wa_auc(np.abs(np.log(D.dur.values / 180))))
D["rel"] = D.dur / D.groupby(["fold", "artist"]).dur.transform("median"); print("rel dur", wa_auc(D.rel.values))
print("pooled stratified AUC dur:", np.mean([ (lambda g: ((g.dur[g.love==1].values[:,None]>g.dur[g.love==0].values[None]).mean()))(g) for _, g in D.groupby("fold")]))
# artist-level: do multi-track artists' songs differ in duration vs loved?
g = D.groupby(["fold", "artist"]).filter(lambda x: len(x) > 1 and 0 < x.love.sum() < len(x)); print("mixed-label artist groups songs", len(g), "mean dur loved", g.dur[g.love == 1].mean(), "not", g.dur[g.love == 0].mean())
