"""Paired comparison of the declared final (w5r1_stack3) against every harness baseline row and the diagnostic pool_artist_siblings, default TUNE folds, nboot 1000 (dump based; fast-mode scores)."""
import lib, numpy as np, pandas as pd
d = lib.dump(); g = lib.frame(d, "tune", "fold"); mods = lib.BASE + lib.REFS + ["w5r1_stack3", "pool_artist_siblings", "pool_album_siblings"]
res = lib.evaluate(g, mods, nboot=1000, which=("sauc", "wx", "wa", "macro"), new=True); rows = []
for b in lib.BASE + lib.REFS + ["pool_artist_siblings", "pool_album_siblings"]:
    r = dict(vs=b, sauc_b=round(res[b]["sauc"][0], 3), stack3_sauc=round(res["w5r1_stack3"]["sauc"][0], 3))
    for k in ("sauc", "wx", "new", "wa", "macro"):
        x = lib.delta(res, "w5r1_stack3", b, k); r[f"d_{k}"] = round(x["d"], 3); r[f"lo80_{k}"] = round(x["lo80"], 3); r[f"P_{k}"] = round(x["P"], 2)
    rows.append(r)
R = pd.DataFrame(rows); R.to_csv(lib.OUT / "a9_final_vs_baselines.csv", index=False); pd.set_option("display.width", 300); pd.set_option("display.max_columns", 30)
t = "stack3 (declared final) minus row, default TUNE folds, 80% bootstrap lower bound lo80 and P(d>0); nboot 1000\n" + R.to_string(index=False); (lib.OUT / "a9_final_vs_baselines.txt").write_text(t); print(t)
