"""Item 4: stability of 80% lower bounds across nboot (100/300/1000) and resample seeds (0..4) for key paired deltas, default TUNE folds."""
import lib, numpy as np, pandas as pd
d = lib.dump(); g = lib.frame(d, "tune", "fold"); PAIRS = [("w5r1_stack3", "artist_recent"), ("ref_w4r1_listening", "artist_recent"), ("ref_w4r1_music", "artist_recent"), ("ref_audio_final", "artist_recent"), ("w5r1_stack3", "ref_w4r1_listening"), ("ref_w4r1_music", "ref_w4r1_listening"), ("ref_w4r1_music", "ref_audio_final")]
mods = sorted({m for p in PAIRS for m in p}); rows = []
for nb in (100, 300, 1000):
    for seed in range(5):
        res = lib.evaluate(g, mods, nboot=nb, seed=seed, which=("sauc", "wx"), new=False)
        for a, b in PAIRS:
            for k in ("sauc", "wx"):
                x = lib.delta(res, a, b, k); rows.append(dict(nboot=nb, seed=seed, pair=f"{a}-{b}", metric=k, d=x["d"], lo80=x["lo80"], P=x["P"]))
R = pd.DataFrame(rows); R.to_csv(lib.OUT / "a6_nboot.csv", index=False)
S = R.groupby(["pair", "metric", "nboot"]).agg(d=("d", "first"), lo80_mean=("lo80", "mean"), lo80_sd=("lo80", "std"), lo80_min=("lo80", "min"), lo80_max=("lo80", "max"), P_min=("P", "min"), P_max=("P", "max"), sign_flips=("lo80", lambda v: int((v > 0).sum()))).round(4)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200); t = S.to_string(); (lib.OUT / "a6_nboot.txt").write_text(t); print(t)
