"""w5r2-score-calculation: one untuned model, declared final.
pair_z = ref_w4r1_listening / 0.70 + ref_w4r1_music / 1.27.
The two constants are the (rounded) typical score standard deviations of the two reference outputs on dev candidate sets (probe on --fast default
folds: 0.63-0.84 and 1.09-1.39; scale_probe.py). They are FIXED numbers, not fitted to any label, so the score of a candidate does not depend on
the other candidates (no per-call normalisation). Not an exact copy of a reference (the two refs correlate ~0.7-0.8)."""
import numpy as np
from evalkit import refs
SA, SB = 0.70, 1.27
def pair_z(train, cands, meta, cutoff):
    a = refs.score("ref_w4r1_listening", train, cands, meta, cutoff); b = refs.score("ref_w4r1_music", train, cands, meta, cutoff)
    return np.asarray(a, float) / SA + np.asarray(b, float) / SB
PREDICTORS = {"pair_z": pair_z}
