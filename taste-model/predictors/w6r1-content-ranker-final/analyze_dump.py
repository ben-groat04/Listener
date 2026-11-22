"""Analysis of a --dump-scores pickle (TUNE, fast): excerpt comparison overall, by alignment group, cross-source correlation. usage: python3 analyze_dump.py dump.pkl"""
import sys; sys.path.insert(0, "/home/user/Listener/taste-model")
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from evalkit import metrics, sanity
d = pd.read_pickle(sys.argv[1]); d = d[d.fold_set == "tune"].reset_index(drop=True)
sc = [c for c in d.columns if c.startswith("score__")]
sanity.assert_no_nan(d[sc + ["love", "fold"]], "dump scores"); sanity.assert_fold_count(d, "tune", name="dump")
hasdz = d["score__diag_hasdz"].values == 1; off = d["score__diag_off"].values; aln = d["score__diag_aln"].values; same = d["score__diag_same"].values == 1
hasdev = d["score__avg21_dev"].values != 0
grp = np.where(~hasdz, "no_dz", np.where(~hasdev, "no_dev", np.where(same, "same_strict", np.where((np.abs(off) <= 10) & (aln >= .4), "same_broad", np.where(aln < 0, "unaligned", "different")))))
d["grp"] = grp
print("n tried rows", len(d), "love rate", d.love.mean().round(3)); print(pd.crosstab(d.grp, d.love))
print("share with a Deezer clip %.3f; dev clip missing %.3f; both %.3f" % (hasdz.mean(), (~hasdev).mean(), (hasdz & hasdev).mean()))
def S(sub, m): return metrics.dump_sauc(sub, "tune", m, nboot=300)
def D(sub, a, b): return metrics.dump_sauc_delta(sub, "tune", a, b, nboot=300)
both = d[hasdz & hasdev].reset_index(drop=True)
rows = []
for name, sub in [("all", d), ("both_clips", both)] + [(g, d[d.grp == g].reset_index(drop=True)) for g in ("same_strict", "same_broad", "different")]:
    if sub.love.sum() < 5 or (1 - sub.love).sum() < 5: print("skip", name, len(sub)); continue
    for a, b in [("avg21_two", "avg21_dev"), ("avg21_dz", "avg21_dev"), ("def_two", "def_dev"), ("def_dz", "def_dev"), ("avg21_dev_max", "avg21_dev"), ("avg21_two_max", "avg21_dev")]:
        r = D(sub, a, b); rows.append(dict(group=name, n=len(sub), loved=int(sub.love.sum()), a=a, b=b, sauc_a=S(sub, a)[0], sauc_b=S(sub, b)[0], **{k: round(v, 4) for k, v in r.items()}))
t = pd.DataFrame(rows); sanity.assert_no_nan(t, "excerpt table"); pd.set_option("display.width", 250); print(t.round(3).to_string())
# cross-source correlation of per-song scores (within fold, then mean of folds) on songs with both clips
for a, b in [("avg21_dev", "avg21_dz"), ("def_dev", "def_dz")]:
    pf = [spearmanr(g["score__" + a], g["score__" + b])[0] for _, g in both.groupby("fold") if len(g) > 20]
    print("cross-source spearman %s vs %s: mean over folds %.3f (min %.3f max %.3f, folds %d); pooled-song %.3f" % (a, b, np.mean(pf), np.min(pf), np.max(pf), len(pf), spearmanr(both["score__" + a], both["score__" + b])[0]))
    for g in ("same_strict", "same_broad", "different"):
        s = d[d.grp == g]
        if len(s) > 10: print("   ", g, len(s), "spearman %.3f" % spearmanr(s["score__" + a], s["score__" + b])[0])
