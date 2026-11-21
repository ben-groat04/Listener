"""w5r1-eval-frame-folds FINAL (declared before any --late/--holdout run): untuned equal-weight rank average of the three harness references
(ref_audio_final, ref_w4r1_listening, ref_w4r1_music) through evalkit.refs.score. No hyper-parameter and no weight is tuned or selected."""
import sys, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evalkit import refs
from scipy.stats import rankdata

def _r(x): return (rankdata(x) - 0.5) / len(x)

def stack3(train, cands, meta, cutoff):
    s = [_r(refs.score(n, train, cands, meta, cutoff)) for n in ("ref_audio_final", "ref_w4r1_listening", "ref_w4r1_music")]
    return np.mean(s, axis=0)

PREDICTORS = {"w5r1_stack3": stack3}
