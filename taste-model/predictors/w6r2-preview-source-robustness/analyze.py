"""Source-robustness analysis of a --dump-scores pickle from analysis_models.py (TUNE, tried songs). usage: python3 analyze.py dump.pkl"""
import sys; sys.path.insert(0, "/home/user/Listener/taste-model")
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from evalkit import metrics, sanity
NB, SEED = 1000, 20260511
d = pd.read_pickle(sys.argv[1]); d = d[d.fold_set == "tune"].reset_index(drop=True)
sc = [c for c in d.columns if c.startswith("score__a_") or c.startswith("score__diag_")]
sanity.assert_no_nan(d[sc + ["love", "fold"]], "dump"); sanity.assert_fold_count(d, "tune", name="dump")
g = lambda n: d["score__" + n].values
d["hasdev"], d["hasdz"], d["hasit"] = g("diag_hasdev") == 1, g("diag_hasdz") == 1, g("diag_hasit") == 1
FOLDS_IT = sorted(d.fold.unique())[:8]; assert len(FOLDS_IT) == 8 and FOLDS_IT[-1] == "2023-04-01", FOLDS_IT   # iTunes lookups complete for folds 2021-07..2023-04
d["same_dz"] = g("diag_dz_same") == 1; d["same_it"] = g("diag_it_same") == 1
print("rows", len(d), "love rate %.3f" % d.love.mean(), "| dev %d dz %d it %d | dev&dz %d | dev&it(8 folds) %d | all3 %d" % (d.hasdev.sum(), d.hasdz.sum(), d.hasit.sum(), (d.hasdev & d.hasdz).sum(),
      (d.hasdev & d.hasit & d.fold.isin(FOLDS_IT)).sum(), (d.hasdev & d.hasdz & d.hasit).sum()))
def S(sub, m): return metrics.dump_sauc(sub, "tune", m, nboot=NB, seed=SEED)[0]
def D(sub, a, b): return metrics.dump_sauc_delta(sub, "tune", a, b, nboot=NB, seed=SEED)
def lab(r): return "POS" if r["lo80"] > 0 else ("NEG" if r["hi80"] < 0 else "UNDECIDED")
def ok(sub): return sub.love.sum() >= 5 and (1 - sub.love).sum() >= 5
def sp(sub, a, b):
    pf = [spearmanr(x["score__" + a], x["score__" + b])[0] for _, x in sub.groupby("fold") if len(x) >= 10]
    return (np.mean(pf), np.min(pf), np.max(pf), len(pf)) if pf else (np.nan,) * 4
subsets = {"dz": d[d.hasdev & d.hasdz], "it": d[d.hasdev & d.hasit & d.fold.isin(FOLDS_IT)], "it_noSame": None}
rows = []; 
for s, base in (("dz", subsets["dz"]), ("it", subsets["it"])):
    parts = {"all": base, "samepart": base[base["same_" + s]], "diffpart": base[~base["same_" + s]], "new_artist": base[base.new_artist], "known_artist": base[~base.new_artist]}
    for gname, sub in parts.items():
        sub = sub.reset_index(drop=True)
        if not ok(sub): print("skip", s, gname, len(sub), int(sub.love.sum())); continue
        for k in ("", "_mu", "_std", "_coral", "_ridge"):
            a = "a_%s%s" % (s, k); r = D(sub, a, "a_dev"); m = sp(sub, a, "a_dev")
            rows.append(dict(src=s, group=gname, n=len(sub), loved=int(sub.love.sum()), model=a, sauc_alt=S(sub, a), sauc_dev=S(sub, "a_dev"), d=r["d"], lo80=r["lo80"], hi80=r["hi80"], lab=lab(r), sp_mean=m[0], sp_min=m[1], sp_max=m[2], nf=m[3]))
t = pd.DataFrame(rows); sanity.assert_no_nan(t.drop(columns=["sp_mean","sp_min","sp_max"]), "source table"); assert (t[t.group=="all"].nf >= 6).all(); pd.set_option("display.width", 250); print(t.round(3).to_string())
t.to_csv(sys.argv[1].replace(".pkl", "_table.csv"), index=False)
# mixing
rows = []
for name, sub in (("dev+dz rows (dev&dz)", subsets["dz"]), ("8 folds, rows with dev", d[d.hasdev & d.fold.isin(FOLDS_IT)]), ("8 folds, all3", d[d.hasdev & d.hasdz & d.hasit & d.fold.isin(FOLDS_IT)]), ("all folds, rows with dev", d[d.hasdev])):
    sub = sub.reset_index(drop=True); assert ok(sub)
    for m in ("a_mix_raw", "a_mix_mu", "a_mix_std") + (("a_dz", "a_it") if "all3" in name else ()):
        r = D(sub, m, "a_dev"); rows.append(dict(set=name, n=len(sub), model=m, sauc=S(sub, m), sauc_dev=S(sub, "a_dev"), d=r["d"], lo80=r["lo80"], hi80=r["hi80"], lab=lab(r)))
t2 = pd.DataFrame(rows); sanity.assert_no_nan(t2, "mix table"); print(t2.round(3).to_string())
# cross-source correlation of corrected vs raw alt (within fold) and mix versus dev
for s, sub in (("dz", subsets["dz"]), ("it", subsets["it"])):
    for a in ("a_%s" % s, "a_%s_mu" % s, "a_%s_std" % s, "a_%s_coral" % s, "a_%s_ridge" % s):
        m = sp(sub, a, "a_dev"); pm = (sub["score__" + a].mean() - sub["score__a_dev"].mean(), sub["score__" + a].std() / sub["score__a_dev"].std())
        print("spearman %-12s vs dev: mean %.3f min %.3f max %.3f folds %d | mean score shift %.3f, sd ratio %.3f" % ((a,) + m + pm))
# dev-clip source: songs whose dev clip is iTunes (from itunes_clips.dev_is_itunes) - AUC of dev scoring by dev-clip source
ic = pd.read_csv("/home/user/Listener/taste-model/.cache/shared-w6r2/itunes_clips.csv")
