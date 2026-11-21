"""Coverage and covered-only analysis on TUNE (labels of LATE are not touched here). Run from taste-model: python3 -W ignore predictors/w3r1-song-content-beyond-audio/analysis.py"""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, os.path.dirname(__file__))
from evalkit import run, data, metrics
from evalkit.baselines import BASELINES
import predict as P
F, _ = P._cache()
def cov_of(cands): return np.array([F.get(i) is not None for i in cands.trackId.values])
for name, cuts in (("TUNE", data.TUNE_CUTOFFS), ("LATE", data.LATE_CUTOFFS)):
    fl = run.prepare_folds(cuts); tr = []; dc = []
    for f in fl:
        cv = cov_of(f["cands"]); dec = f["pool"].iloc[f["order"]].is_decoy.values == 1
        tr.append(cv[~dec].mean()); dc.append(cv[dec].mean()); 
    print(name, "coverage (lyrics found, per fold mean) tried", np.round(np.mean(tr), 3), "decoys", np.round(np.mean(dc), 3), "per-fold tried", np.round(tr, 2))
# covered-only on TUNE
cuts = data.TUNE_CUTOFFS; fl = run.prepare_folds(cuts)
models = {k: P.PREDICTORS[k] for k in ("lyr_resid_nodur", "lyr_resid_orth")}
models.update({k: BASELINES[k] for k in ("nonaudio_gbm", "meta_gbm", "duration")})
sc = {n: run.score_predictor(fn, cuts, name=n, indep_n=0) for n, fn in models.items()}
cov = np.concatenate([cov_of(f["cands"]) for f in fl])
first = next(iter(sc.values())); tm = (first.is_decoy == 0).values
T = metrics.Block(first[tm].reset_index(drop=True), "love", 300, 0)
ctm = cov[tm]
print("tried n", tm.sum(), "covered", ctm.sum(), "love rate covered", first.love.values[tm][ctm].mean().round(3), "uncovered", first.love.values[tm][~ctm].mean().round(3))
def ci(x): return tuple(float(v) for v in np.nanpercentile(x, [2.5, 97.5]).round(3))
for lab, blk, nmask in (("ALL tried songs", T, T.new), ("COVERED only", T.sub(ctm), T.new & ctm), ("UNCOVERED only", T.sub(~ctm), None)):
    print("==", lab, "n", blk.n)
    st = {}
    for n, df in sc.items():
        s = df.score.values[tm]; r = blk.stats(s, True, ("sauc", "wa", "ws")); st[n] = r
        nw = T.sub(nmask) if nmask is not None else None
        print(f"{n:18s} sauc {r['sauc'][0]:.3f} {ci(r['sauc_b'])}  wa {r['wa'][0]:.3f} {ci(r['wa_b'])}  ws {r['ws'][0]:.3f} {ci(r['ws_b'])}" + (f"  new {nw.stats(s, True, ('sauc',))['sauc'][0]:.3f}" if nw is not None else ""))
    for n in ("lyr_resid_nodur", "lyr_resid_orth"):
        for b in ("nonaudio_gbm", "meta_gbm", "duration"):
            print(f"  d({n}-{b}) sauc lower {np.nanpercentile(st[n]['sauc_b']-st[b]['sauc_b'],2.5):.3f} wa lower {np.nanpercentile(st[n]['wa_b']-st[b]['wa_b'],2.5):.3f}  point sauc {st[n]['sauc'][0]-st[b]['sauc'][0]:.3f} wa {st[n]['wa'][0]-st[b]['wa'][0]:.3f}")
