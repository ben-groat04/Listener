"""Sensitivity of the declared final to its set-level rank normalisation (the harness independence gate flags it: a lone candidate has rank 0.5). On the default TUNE fold set of the dump:
(a) stack3 as declared (within-fold rank average); (b) average of per-reference z-scores with ONE mean/std per reference over the whole set (no per-fold normalisation); (c) average of raw reference scores."""
import lib, numpy as np, pandas as pd
d = lib.dump(); g = lib.frame(d, "tune", "fold"); R = ["ref_audio_final", "ref_w4r1_listening", "ref_w4r1_music"]
for r in R: g["score__" + r] = g["score__" + r].astype(float)
g["score__zglobal"] = np.mean([(g["score__" + r] - g["score__" + r].mean()) / g["score__" + r].std() for r in R], axis=0)
g["score__raw"] = np.mean([g["score__" + r] for r in R], axis=0)
res = lib.evaluate(g, ["w5r1_stack3", "zglobal", "raw", "artist_recent"], nboot=300, which=("sauc", "wx", "wa"), new=True)
out = []
for m in ("w5r1_stack3", "zglobal", "raw"):
    out.append(f"{m}: sauc {res[m]['sauc'][0]:.3f} wx {res[m]['wx'][0]:.3f} wa {res[m]['wa'][0]:.3f} new {res[m]['new'][0]:.3f}; vs artist_recent sauc {lib.delta(res, m, 'artist_recent')['d']:+.3f} lo80 {lib.delta(res, m, 'artist_recent')['lo80']:+.3f}")
t = "\n".join(out); (lib.OUT / "a10_indep_check.txt").write_text(t); print(t)
for r in R: print(r, g["score__" + r].describe()[["mean", "std", "min", "max"]].round(3).to_dict())
