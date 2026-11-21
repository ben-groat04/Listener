"""Shared helpers: cache location and the universe of (opaque trackId, title, primary artist, duration) over all dev folds."""
import sys, re
from pathlib import Path
import pandas as pd
ROOT = Path("/home/user/Listener/taste-model")
sys.path.insert(0, str(ROOT))
CACHE = ROOT / ".cache" / "shared" / "w3r1-song-content-beyond-audio-lyrics"
CACHE.mkdir(parents=True, exist_ok=True)

def universe():
    """Distinct tracks over the meta of every dev fold (train + pool tracks), via the harness' public view. Ids are opaque hashes."""
    from evalkit import run, data
    rows = {}
    for f in run.prepare_folds(data.DEV_CUTOFFS):
        m = f["meta"]
        for tid, r in zip(m.index, m.itertuples()):
            if tid not in rows:
                a = r.artistNames if isinstance(r.artistNames, (list, tuple)) else []
                rows[tid] = (r.name if isinstance(r.name, str) else "", a[0] if len(a) else "", r.durationMs)
    return rows

def norm(s):
    s = re.sub(r"\s*[\(\[][^)\]]*[\)\]]", "", str(s).lower()); s = re.sub(r"\s+-\s+.*$", "", s)
    return re.sub(r"\W+", " ", s).strip()
