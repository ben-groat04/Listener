"""Diagnostic probe (not a reported model): logs scale of reference scores per cutoff."""
import numpy as np, json, os
from evalkit import refs
LOG = os.environ.get("PROBE_LOG", "/tmp/probe.jsonl")
def probe(train, cands, meta, cutoff):
    a = refs.score("ref_w4r1_listening", train, cands, meta, cutoff); b = refs.score("ref_w4r1_music", train, cands, meta, cutoff)
    with open(LOG, "a") as f:
        f.write(json.dumps(dict(cutoff=str(cutoff), n=len(cands), a=[float(np.mean(a)), float(np.std(a)), float(a.min()), float(a.max())], b=[float(np.mean(b)), float(np.std(b)), float(b.min()), float(b.max())], corr=float(np.corrcoef(a, b)[0, 1])))+"\n")
    return a
PREDICTORS = {"probe": probe}
