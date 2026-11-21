"""Item 2a: alternative love definitions from the dump (plays/days thresholds, horizons 30/60/90/180/365 days, keep). Model sauc (default TUNE folds), ranking tau vs the default label, stack3 - artist_recent delta,
which short-horizon label best predicts the long-term (keep / days 90-365 plays) outcome."""
import lib, numpy as np, pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score
d = lib.dump(); T = d[d.fold_set == "tune"]
def L(h, p, dd): return lambda g: ((g[f"plays_h{h}"] >= p) & (g[f"days_h{h}"] >= dd)).astype(int)
LAB = {"love(90d,6/3)": lambda g: g.love, "strong(90d,15/5)": lambda g: g.strong, "love_4_2(90d)": lambda g: g.love_4_2, "love_10_4(90d)": lambda g: g.love_10_4, "keep(d90-365>=6 plays)": lambda g: g.keep}
for h, grid in ((30, [(3, 2), (4, 2), (6, 3)]), (60, [(4, 2), (6, 3), (10, 4)]), (180, [(6, 3), (10, 4), (15, 5)]), (365, [(6, 3), (10, 4), (15, 5), (30, 8)])):
    for p, dd in grid: LAB[f"h{h}_{p}/{dd}"] = L(h, p, dd)
MODS = lib.MODELS; out = []; rows = []; base = None
LONG = (T.plays_h365 - T.plays90).values; keep = T.keep.values.astype(int)
for name, f in LAB.items():
    g = lib.frame(d, "tune", "fold", label=f); y = g._lab.values; res = lib.evaluate(g, MODS, nboot=300, which=("sauc",), new=False); br = lib.best_ref(res)
    sc = [res[m]["sauc"][0] for m in MODS]; 
    if base is None: base = sc
    r = dict(label=name, base_rate=round(y.mean(), 3), best_ref=br, tau_vs_love=round(lib.kendall(sc, base), 2), ar=round(res["artist_recent"]["sauc"][0], 3), listening=round(res["ref_w4r1_listening"]["sauc"][0], 3), music=round(res["ref_w4r1_music"]["sauc"][0], 3), audio=round(res["ref_audio_final"]["sauc"][0], 3), stack3=round(res["w5r1_stack3"]["sauc"][0], 3), nonaudio=round(res["nonaudio_gbm"]["sauc"][0], 3))
    for a in ("w5r1_stack3", "ref_w4r1_music", "ref_w4r1_listening", "ref_audio_final"):
        dd_ = lib.delta(res, a, "artist_recent"); r[f"{a[:14]}-ar"] = round(dd_["d"], 3); r[f"{a[:14]}-ar_lo80"] = round(dd_["lo80"], 3)
    # label as predictor of the long-term outcome (pooled over songs; within-fold pooled AUC via metric on fold groups)
    try:
        r["AUC_vs_keep"] = round(float(roc_auc_score(keep, y)), 3); r["rho_vs_lt_plays"] = round(float(spearmanr(y, LONG)[0]), 3)
        from evalkit import metrics as M
        gv, num, den = lib.groupstats(g.assign(_lab=keep), y.astype(float)); r["sAUC_vs_keep_within_fold"] = round(float(num.sum() / den.sum()), 3)
    except Exception as e: r["AUC_vs_keep"] = str(e)
    rows.append(r)
R = pd.DataFrame(rows); R.to_csv(lib.OUT / "a3_labels.csv", index=False); pd.set_option("display.width", 300); pd.set_option("display.max_columns", 40)
out.append("=== label variants (TUNE default folds, fold pairing). sauc per model; deltas vs artist_recent with lo80; tau vs default-label model ranking over 12 models\n" + R.to_string(index=False))
# continuous short-horizon counts as predictors of long-term outcome
out.append("\n=== continuous predictors of the long-term outcome (keep; plays in days 90-365): AUC vs keep, Spearman vs lt plays")
rr = []
for c in ("plays_h30", "plays_h60", "plays90", "days_h30", "days_h60", "days90", "share90"):
    v = T[c].values.astype(float); rr.append(dict(col=c, AUC_vs_keep=round(float(roc_auc_score(keep, v)), 3), rho_lt=round(float(spearmanr(v, LONG)[0]), 3)))
out.append(pd.DataFrame(rr).to_string(index=False))
out.append(f"\nkeep rate {keep.mean():.3f}; keep given love {keep[T.love.values==1].mean():.3f}; keep given not love {keep[T.love.values==0].mean():.3f}")
(lib.OUT / "a3_labels.txt").write_text("\n".join(out)); print("\n".join(out))
