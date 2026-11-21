"""Staleness ladder with FIXED calendar-quarter pairing (so only the training cutoff freshness changes): tune_m (<=1 mo), tune (<=3), tune_h (<=6), tune_y (<=12). From a1_folds_table.csv."""
import pandas as pd, lib
T = pd.read_csv(lib.OUT / "a1_folds_table.csv"); Q = T[T.group == "quarter"]; out = []
for k in ("sauc", "wx", "new"):
    out.append(f"-- {k}: point (and delta vs artist_recent [lo80]) by cutoff freshness, quarter pairing")
    for m in ["artist_recent", "nonaudio_gbm", "ref_audio_final", "ref_w4r1_listening", "ref_w4r1_music", "w5r1_stack3"]:
        s = []
        for st, lab in (("tune_m", "1mo"), ("tune", "3mo"), ("tune_h", "6mo"), ("tune_y", "12mo")):
            r = Q[(Q.set == st) & (Q.model == m)].iloc[0]; dl = "" if m == "artist_recent" else f" ({r[f'd_{k}_ar']:+.3f} [{r[f'lo80_{k}_ar']:+.3f}])"
            s.append(f"{lab}: {r[k]:.3f}{dl}")
        out.append(f"{m:20s} " + " | ".join(s))
(lib.OUT / "a8_staleness.txt").write_text("\n".join(out)); print("\n".join(out))
