"""Universe of (opaque trackId -> (title, primary artist, durationMs, previewUrl)) over every dev fold (main + holdout parts), via the harness' public view. Also writes per-fold group membership."""
import sys, pickle
from pathlib import Path
ROOT = Path("/home/user/Listener/taste-model"); sys.path.insert(0, str(ROOT))
def universe(with_groups=False):
    from evalkit import run, data
    rows, groups = {}, []
    for part in ("main", "holdout"):
        for f in run.prepare_folds(data.DEV_CUTOFFS, part=part):
            m = f["meta"]
            for tid, r in zip(m.index, m.itertuples()):
                if tid not in rows:
                    a = r.artistNames if isinstance(r.artistNames, (list, tuple)) else []
                    rows[tid] = (r.name if isinstance(r.name, str) else "", a[0] if len(a) else "", r.durationMs)
            if with_groups:
                p = f["pool"]; tr = set(f["train"].trackId) if "trackId" in f["train"] else set()
                groups.append(dict(part=part, c=str(f["c"].date()), tried=list(p.trackId[p.is_decoy == 0]), decoy=list(p.trackId[p.is_decoy == 1]), train=[t for t in m.index if t in tr]))
    return (rows, groups) if with_groups else rows
if __name__ == "__main__":
    import time; t = time.time(); U, G = universe(True)
    pickle.dump((U, G), open(sys.argv[1], "wb")); print(len(U), len(G), time.time() - t)
