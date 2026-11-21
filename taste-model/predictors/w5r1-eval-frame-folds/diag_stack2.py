"""Diagnostic only (never a declared final; never run with --late/--holdout): rank average of the two content-only references."""
import sys, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evalkit import refs
from scipy.stats import rankdata
def _r(x): return (rankdata(x) - 0.5) / len(x)
def stack2_content(train, cands, meta, cutoff):
    return np.mean([_r(refs.score(n, train, cands, meta, cutoff)) for n in ("ref_audio_final", "ref_w4r1_music")], axis=0)
PREDICTORS = {"w5r1_stack2_content": stack2_content}
