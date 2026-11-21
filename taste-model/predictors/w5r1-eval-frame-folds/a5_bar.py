"""Item 3: does the bar (artist_recent half-life, nonaudio_gbm weights / monotone map / size) change best_ref or the content models' lead? Variants from bars.py merged into the main dump."""
import lib, numpy as np, pandas as pd
a = lib.dump("dump_all.pkl"); b = lib.dump("dump_bars.pkl"); bc = [c for c in b.columns if c.startswith("score__bar_")]
d = a.merge(b[["fold_set", "song"] + bc], on=["fold_set", "song"], how="left", validate="1:1"); assert d[bc].notna().all().all()
BAR = [c[7:] for c in bc]; out = []; rows = []
ALLREF = lib.REFROWS + BAR
for s, grp in (("tune", "fold"), ("tune_m", "fold"), ("tune_q1", "fold"), ("tune_q2", "fold"), ("tune_h", "fold")):
    g = lib.frame(d, s, grp); res = lib.evaluate(g, lib.MODELS + BAR, nboot=300, which=("sauc", "wx"), new=False)
    best_hist = max(["artist_recent"] + [m for m in BAR if m.startswith("bar_hl")], key=lambda m: res[m]["sauc"][0]); best_all = max(ALLREF, key=lambda m: res[m]["sauc"][0])
    for m in ["artist_recent"] + BAR + ["nonaudio_gbm"]:
        r = dict(set=s, bar=m, sauc=round(res[m]["sauc"][0], 3), wx=round(res[m]["wx"][0], 3))
        for a_ in ("w5r1_stack3", "ref_w4r1_music", "ref_w4r1_listening", "ref_audio_final"):
            dd = lib.delta(res, a_, m); r[f"{a_[:12]}-bar"] = round(dd["d"], 3); r[f"{a_[:12]}-bar_lo80"] = round(dd["lo80"], 3)
        rows.append(r)
    out.append(f"{s}: best artist-history bar (artist_recent or hl variants) = {best_hist} {res[best_hist]['sauc'][0]:.3f}; best of all 7 refs + variants = {best_all} {res[best_all]['sauc'][0]:.3f}; default best_ref = {lib.best_ref(res)}")
R = pd.DataFrame(rows); R.to_csv(lib.OUT / "a5_bar.csv", index=False); pd.set_option("display.width", 300); pd.set_option("display.max_columns", 30); pd.set_option("display.max_rows", 300)
out.append(R[R.set == "tune"].to_string(index=False)); out.append("\n-- the same for the monthly set"); out.append(R[R.set == "tune_m"].to_string(index=False))
out.append("\n-- sauc of each bar across fold sets"); out.append(R.pivot(index="bar", columns="set", values="sauc").to_string())
(lib.OUT / "a5_bar.txt").write_text("\n".join(out)); print("\n".join(out))
