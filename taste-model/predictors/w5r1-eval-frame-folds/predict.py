"""w5r1-eval-frame-folds final: untuned equal-weight rank average of the three harness references (stack through evalkit.refs.score).
Declared before any --late/--holdout run. No hyper-parameters, no weights tuned."""
import sys, numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evalkit import refs
from scipy.stats import rankdata

def _r(x): return (rankdata(x) - 0.5) / len(x)

def stack3(train, cands, meta, cutoff):
    s = [_r(refs.score(n, train, cands, meta, cutoff)) for n in ("ref_audio_final", "ref_w4r1_listening", "ref_w4r1_music")]
    return np.mean(s, axis=0)

def stack2_content(train, cands, meta, cutoff):   # diagnostic: the two content-only references (listening ref excluded)
    s = [_r(refs.score(n, train, cands, meta, cutoff)) for n in ("ref_audio_final", "ref_w4r1_music")]
    return np.mean(s, axis=0)

PREDICTORS = {"w5r1_stack3": stack3, "w5r1_stack2_content": stack2_content}
