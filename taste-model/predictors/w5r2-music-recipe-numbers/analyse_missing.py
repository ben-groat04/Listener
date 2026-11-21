"""Missing-audio analysis (dev data only): who are the songs without audio, is the 'fill high' gain within artist / exposure / new-artist, partial association controlling for popularity/exposure.
Needs $W5R2_OUT/probe_*.pkl (probe.py) and grid_merged.pkl (analyse_grid.py)."""
import os, sys, glob
import numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import metrics
OUT = os.environ["W5R2_OUT"]
def f1(x): return float(np.ravel(x)[0])
d = pd.read_pickle(f"{OUT}/grid_merged.pkl")
# availability / metadata per tried song from the harness' dev pools (TUNE folds) and the public meta (evalkit.data.load_meta); join key = data.h(pool song) = dump 'song'
import pickle
from evalkit import data, run
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import recipe
meta = data.load_meta(); pools = pickle.load(open(run._pool_path(), "rb")); rows = []
for c in data.TUNE_CUTOFFS:
    t = pools[c]; t = t[t.is_decoy == 0]; tid = t.trackId.values; u = meta.previewUrl.reindex(tid).values; m = meta.reindex(tid)
    rows.append(pd.DataFrame(dict(fold=c, song=[data.h(x) for x in t.song.values], ess=recipe._eidx(tid, meta) >= 0, mert=recipe._midx(tid, meta) >= 0, has_url=[isinstance(x, str) for x in u],
        dom=[x.split("/")[2] if isinstance(x, str) else "" for x in u], dur=m.durationMs.values, pop=m.popularity.values, expl=m.explicit.astype(float).values)))
p = pd.concat(rows).drop_duplicates(["fold", "song"])
d = d.merge(p, on=["fold", "song"], how="left", validate="one_to_one"); assert d.ess.notna().all()
d["miss_ess"] = ~d.ess; d["miss_mert"] = ~d.mert; d["miss_any"] = d.miss_ess | d.miss_mert
d["cause"] = np.where(~d.has_url, "no_url", np.where(d.miss_ess | d.miss_mert, "url_but_no_clip", "audio"))
d["year"] = d.first_play_date.str[:4]
print("N", len(d), "missing_any", d.miss_any.mean().round(3), "ess", d.miss_ess.sum(), "mert", d.miss_mert.sum(), "no_url", (~d.has_url).sum())
print(d.groupby("cause").agg(n=("love", "size"), love=("love", "mean"), pop=("pop", "mean"), pop0=("pop", lambda s: (s == 0).mean()), dur=("dur", lambda s: s.mean() / 1000), expl=("expl", "mean"), new=("new_artist", "mean"), exp_before=("exposure_before", "mean"), plays90=("plays90", "mean")).round(3))
print(d.groupby("cause").dom.agg(lambda s: s.value_counts().to_dict()))
print("by year (missing_any share, love | missing, love | audio):"); print(d.groupby("year").apply(lambda g: pd.Series(dict(n=len(g), miss=g.miss_any.mean(), love_miss=g.love[g.miss_any].mean(), love_aud=g.love[~g.miss_any].mean()))).round(3))
print("by new_artist:"); print(d.groupby("new_artist").apply(lambda g: pd.Series(dict(n=len(g), miss=g.miss_any.mean(), love_miss=g.love[g.miss_any].mean(), love_aud=g.love[~g.miss_any].mean()))).round(3))
d["expb"] = pd.cut(d.exposure_before, [-1, 0, 2, 5, 1e9], labels=["0", "1-2", "3-5", "6+"])
print("by exposure_before bucket:"); print(d.groupby("expb", observed=True).apply(lambda g: pd.Series(dict(n=len(g), miss=g.miss_any.mean(), love_miss=g.love[g.miss_any].mean(), love_aud=g.love[~g.miss_any].mean()))).round(3))
# repeated songs / artists among missing
print("distinct songs missing", d[d.miss_any].song.nunique(), "artists", d[d.miss_any].artist.nunique(), "top artists share", d[d.miss_any].artist.value_counts(normalize=True).head(5).round(3).tolist())
# partial association: logistic love ~ miss + pop + dur + expl + new + log exposure + fold fixed effects, artist-cluster SE via statsmodels if available
try:
    import statsmodels.api as sm
    X = pd.DataFrame(dict(miss=d.miss_any.astype(float), pop=d["pop"].fillna(0) / 100, dur=np.log1p(d.dur.fillna(0) / 1000), expl=d.expl.fillna(0), new=d.new_artist.astype(float), lexp=np.log1p(d.exposure_before)))
    X = pd.concat([X, pd.get_dummies(d.fold, drop_first=True).astype(float)], axis=1); X = sm.add_constant(X)
    for nm, cols in (("miss only + fold FE", ["const", "miss"] + [c for c in X.columns if c.startswith("20")]), ("+ pop,dur,expl,new,log exposure", list(X.columns))):
        m = sm.Logit(d.love.astype(float), X[cols]).fit(disp=0, cov_type="cluster", cov_kwds=dict(groups=pd.factorize(d.artist)[0]))
        print(nm, "miss coef %.3f se %.3f p %.3f" % (m.params["miss"], m.bse["miss"], m.pvalues["miss"]))
except Exception as e: print("statsmodels unavailable", e)
# gain of the fill policy across slices: sauc / wa (within-artist) / wx (within exposure bucket) / new / known
B = metrics.dump_block(d, "tune", "fold", nboot=500); newm = d.new_artist.values.astype(bool)
def stats(col): return B.stats(d[col].values, True, ("sauc", "wa", "wx"))
base = stats("score__default")
for v in ("oat_fill_2", "oat_mfill_2", "oat_fill_0"):
    s = stats("score__" + v); print(v)
    for k in ("sauc", "wa", "wx"):
        x = s[k + "_b"] - base[k + "_b"]; x = x[np.isfinite(x)]
        print("  %s delta %.4f 80%% [%.4f, %.4f] P>0 %.2f" % (k, f1(s[k]) - f1(base[k]), np.percentile(x, 10), np.percentile(x, 90), (x > 0).mean()))
# tried rows with audio only: does the default itself change when missing rows are removed? (sauc among audio rows)
for nm, mask in (("audio rows only", ~d.miss_any.values), ("new-artist rows", newm), ("known-artist rows", ~newm)):
    sub = d[mask]; Bm = metrics.dump_block(sub, "tune", "fold", nboot=500)
    a = Bm.stats(sub.score__default.values, True, ("sauc",)); b = Bm.stats(sub.score__oat_fill_2.values, True, ("sauc",)); x = b["sauc_b"] - a["sauc_b"]; x = x[np.isfinite(x)]
    print("%-18s n=%d default sauc %.4f fill_high sauc %.4f delta %.4f 80%% [%.4f, %.4f]" % (nm, len(sub), f1(a["sauc"]), f1(b["sauc"]), f1(b["sauc"]) - f1(a["sauc"]), np.percentile(x, 10), np.percentile(x, 90)))
# 'missing' indicator as a stand-alone scorer
d["score__ind"] = d.miss_any.astype(float); Bi = B.stats(d.score__ind.values, True, ("sauc", "wa", "wx")); print("indicator alone: sauc %.4f wa %.4f wx %.4f" % (f1(Bi["sauc"]), f1(Bi["wa"]), f1(Bi["wx"])))
# --- extra: heterogeneity of the fill-high gain (fold_meta), exclusion of the artists with most missing songs, indicator CI
for v in ("oat_fill_2",):
    fm = metrics.fold_meta(d, "tune", v, "default"); print(v, "fold_meta mean %.4f 80%% [%.4f, %.4f] Q %.1f/%d p %.2f I2 %.2f trend/yr %.4f [%.4f, %.4f]" % (fm["mean"], fm["lo80"], fm["hi80"], fm["Q"], fm["df"], fm["p"], fm["I2"], fm["trend"], fm["trend_lo80"], fm["trend_hi80"]))
    print(fm["table"].round(4).to_string())
top = d[d.miss_any].artist.value_counts().index[:3]; sub = d[~d.artist.isin(top)]; Bm = metrics.dump_block(sub, "tune", "fold", nboot=500)
a = Bm.stats(sub.score__default.values, True, ("sauc",)); b = Bm.stats(sub.score__oat_fill_2.values, True, ("sauc",)); x = b["sauc_b"] - a["sauc_b"]; x = x[np.isfinite(x)]
print("excluding the 3 artists with most missing songs (%d rows removed): default %.4f fill_high %.4f delta %.4f 80%% [%.4f, %.4f]" % (len(d) - len(sub), f1(a["sauc"]), f1(b["sauc"]), f1(b["sauc"]) - f1(a["sauc"]), np.percentile(x, 10), np.percentile(x, 90)))
for k in ("sauc", "wa", "wx"):
    x = Bi[k + "_b"]; x = x[np.isfinite(x)]; print("indicator alone %s %.4f 80%% [%.4f, %.4f]" % (k, f1(Bi[k]), np.percentile(x, 10), np.percentile(x, 90)))
print("missing songs per artist (n artists with >=1 missing, with also >=1 audio song):", d[d.miss_any].artist.nunique(), d[d.miss_any].artist.isin(d[~d.miss_any].artist).sum())
