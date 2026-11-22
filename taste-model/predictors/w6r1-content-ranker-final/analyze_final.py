"""Secondary checks from a score dump that holds the finals + comparators (run --fast --folds tune --refs ref_w4r1_listening,ref_w4r1_music --dump-scores X final files). usage: analyze_final.py dump.pkl"""
import sys; sys.path.insert(0, "/home/user/Listener/taste-model")
import numpy as np, pandas as pd
from evalkit import metrics, sanity
d = pd.read_pickle(sys.argv[1]); d = d[d.fold_set == "tune"].reset_index(drop=True)
F = ["combo_two_music", "combo_dev_music", "avg21_dev"]; CMP = ["artist_recent", "ref_w4r1_listening"]
for m in F + CMP: assert "score__" + m in d.columns, m
sanity.assert_no_nan(d[["score__" + m for m in F + CMP] + ["love", "strong", "fold"]], "dump"); sanity.assert_fold_count(d, "tune", name="dump"); assert len(d) == 1074, len(d)
dd = metrics.dump_frame(d, "tune"); dd["plays90"] = d["plays90"] if "plays90" in d else np.nan
def pc(a, lo=10, hi=90): return round(float(np.nanpercentile(a, lo)), 4), round(float(np.nanpercentile(a, hi)), 4)
def lab(lo, hi): return "POS" if lo > 0 else ("NEG" if hi < 0 else "UNDECIDED")
rows = []
def delta(B, par, name, which, a, b, label):
    sa = B.stats(par["score__" + a].values, True, (which,)); sb = B.stats(par["score__" + b].values, True, (which,))
    dpt = float(sa[which][0] - sb[which][0]); db = sa[which + "_b"] - sb[which + "_b"]; lo, hi = pc(db); rows.append(dict(check=name, a=a, b=b, sauc_a=round(float(sa[which][0]), 3), sauc_b=round(float(sb[which][0]), 3), d=round(dpt, 4), lo80=lo, hi80=hi, label=lab(lo, hi)))
dd2 = dd.copy(); dd2["plays90"] = d["plays90"].values if "plays90" in d.columns else 0
for label, nm in (("love", "love"), ("strong", "strong_label")):
    B = metrics.Block(dd2, label, 1000, 20260511)
    for a in F:
        for b in CMP + [x for x in F if x != a and x == "avg21_dev"]: delta(B, dd2, nm + " sauc", "sauc", a, b, label)
B = metrics.Block(dd2, "love", 1000, 20260511)
for a in F:
    for b in CMP + ["avg21_dev"]:
        if a == b: continue
        delta(B, dd2, "within-artist wa", "wa", a, b, "love")
new = dd2.new_artist.values.astype(bool); e0 = dd2.exp_before.values == 0
for nm, mask in (("new-artist sauc", new), ("known-artist sauc", ~new), ("exposure_before=0 sauc", e0)):
    Bs = B.sub(mask)
    for a in F:
        for b in CMP + ["avg21_dev"]:
            if a == b: continue
            sa = Bs.stats(dd2["score__" + a].values, True, ("sauc",)); sb = Bs.stats(dd2["score__" + b].values, True, ("sauc",)); db = sa["sauc_b"] - sb["sauc_b"]; lo, hi = pc(db)
            rows.append(dict(check=nm + " (n=%d, loved=%d)" % (mask.sum(), dd2.love.values[mask].sum()), a=a, b=b, sauc_a=round(float(sa["sauc"][0]), 3), sauc_b=round(float(sb["sauc"][0]), 3), d=round(float(sa["sauc"][0] - sb["sauc"][0]), 4), lo80=lo, hi80=hi, label=lab(lo, hi)))
t = pd.DataFrame(rows); sanity.assert_no_nan(t, "secondary table"); pd.set_option("display.width", 250); print(t.to_string())
# per-fold AUC
pf = []
for f, g in d.groupby("fold"):
    r = {"fold": f, "n": len(g), "loved": int(g.love.sum())}
    for m in F + CMP: r[m] = metrics.auc(g.love.values, g["score__" + m].values)
    pf.append(r)
pf = pd.DataFrame(pf); sanity.assert_table(pf, "per-fold AUC", fold_set="tune"); print(pf.round(3).to_string())
print("below 0.5 folds:", {m: pf.fold[pf[m] < 0.5].tolist() for m in F + CMP})
