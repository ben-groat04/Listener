"""Item 1: fold-set sensitivity. Scores of every model on each TUNE-era fold set (same 1074 songs), fold pairing and calendar-quarter pairing; spread vs 80% bootstrap half-width; Kendall tau."""
import lib, numpy as np, pandas as pd, itertools, json
d = lib.dump(); SETS = ["tune", "tune_q1", "tune_q2", "tune_h", "tune_y", "tune_m"]; MET = ["sauc", "wx", "new", "wa", "macro"]
rows = []; R = {}
for grp in ("fold", "quarter"):
    for s in SETS:
        if grp == "quarter" and s in ("tune", "tune_m") is False: pass
        g = lib.frame(d, s, grp); R[(grp, s)] = res = lib.evaluate(g, lib.MODELS, nboot=300)
        br = lib.best_ref(res); 
        for m in lib.MODELS:
            r = dict(group=grp, set=s, model=m, best_ref_set=br)
            for k in MET: r[k] = res[m][k][0]; r["hw80_" + k] = lib.hw80(res, m, k)
            for ref, tag in ((br, "own"), (lib.FIXED_BEST, "fixed"), ("artist_recent", "ar")):
                if m != ref:
                    for k in ("sauc", "wx", "new"):
                        dd = lib.delta(res, m, ref, k); r[f"d_{k}_{tag}"] = dd["d"]; r[f"lo80_{k}_{tag}"] = dd["lo80"]
            rows.append(r)
T = pd.DataFrame(rows); T.to_csv(lib.OUT / "a1_folds_table.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
out = []
for grp in ("fold", "quarter"):
    out.append(f"\n=== pairing group = {grp}; best_ref per set: " + ", ".join(f"{s}:{T[(T.group==grp)&(T.set==s)].best_ref_set.iloc[0]}" for s in SETS))
    for k in MET:
        P = T[T.group == grp].pivot(index="model", columns="set", values=k).loc[lib.MODELS, SETS].round(3)
        out.append(f"-- {k} (rows models)\n" + P.to_string())
# spread vs 80% half width (sets compared: the 5 non-monthly + monthly separately)
out.append("\n=== spread across fold sets (fold pairing) vs bootstrap 80% half-width (tune); spread = max-min across tune,q1,q2,h,y ; spread_m includes tune_m")
for k in MET:
    P = T[T.group == "fold"].pivot(index="model", columns="set", values=k); hw = T[(T.group == "fold") & (T.set == "tune")].set_index("model")["hw80_" + k]
    sp = (P[["tune", "tune_q1", "tune_q2", "tune_h", "tune_y"]].max(1) - P[["tune", "tune_q1", "tune_q2", "tune_h", "tune_y"]].min(1)); spm = P.max(1) - P.min(1)
    X = pd.DataFrame(dict(spread=sp, spread_with_m=spm, hw80=hw, ratio=sp / hw)).loc[lib.MODELS].round(3); out.append(f"-- {k}\n" + X.to_string() + f"\n   median spread {sp.median():.3f}, median hw80 {hw.median():.3f}")
# paired-delta spread
out.append("\n=== paired deltas vs artist_recent (d, lo80) per set, fold pairing")
for k in ("sauc", "wx", "new"):
    for tag in ("ar", "fixed", "own"):
        Dm = T[T.group == "fold"].pivot(index="model", columns="set", values=f"d_{k}_{tag}").loc[[m for m in lib.REFS + lib.STACK + ["nonaudio_gbm", "duration"]], SETS].round(3)
        Lm = T[T.group == "fold"].pivot(index="model", columns="set", values=f"lo80_{k}_{tag}").loc[Dm.index, SETS].round(3)
        out.append(f"-- delta {k} vs {tag}\n" + Dm.to_string() + f"\n   lo80:\n" + Lm.to_string())
# Kendall tau between sets
out.append("\n=== Kendall tau of model ranking between fold sets (12 models), fold pairing")
for k in ("sauc", "wx", "new", "wa", "macro"):
    P = T[T.group == "fold"].pivot(index="model", columns="set", values=k).loc[lib.MODELS, SETS]
    tau = pd.DataFrame({a: {b: lib.kendall(P[a], P[b]) for b in SETS} for a in SETS}).round(2); out.append(f"-- {k}\n" + tau.to_string())
out.append("\n=== Kendall tau fold-pairing vs quarter-pairing, per set")
for k in ("sauc", "wx", "new", "wa"):
    out.append(k + ": " + ", ".join(f"{s}={lib.kendall(T[(T.group=='fold')&(T.set==s)].set_index('model')[k].loc[lib.MODELS], T[(T.group=='quarter')&(T.set==s)].set_index('model')[k].loc[lib.MODELS]):.2f}" for s in SETS))
# decomposition staleness vs grouping
out.append("\n=== Staleness vs grouping (sauc). tune[quarter]=quarterly cutoffs & quarter pairs; tune_m[quarter]=monthly cutoffs & quarter pairs; tune_m[fold]=monthly cutoffs & month pairs")
for k in ("sauc", "wx", "new"):
    a = T[(T.group == "quarter") & (T.set == "tune")].set_index("model")[k]; b = T[(T.group == "quarter") & (T.set == "tune_m")].set_index("model")[k]; c = T[(T.group == "fold") & (T.set == "tune_m")].set_index("model")[k]
    h = T[(T.group == "quarter") & (T.set == "tune_h")].set_index("model")[k]; hf = T[(T.group == "fold") & (T.set == "tune_h")].set_index("model")[k]
    X = pd.DataFrame(dict(tuneQ=a, staleness_m_minus_tuneQ=b - a, grouping_mfold_minus_mQ=c - b, hQ_minus_tuneQ=h - a, hfold_minus_hQ=hf - h)).loc[lib.MODELS].round(3)
    out.append(f"-- {k}\n" + X.to_string())
(lib.OUT / "a1_folds.txt").write_text("\n".join(out)); print("\n".join(out))
