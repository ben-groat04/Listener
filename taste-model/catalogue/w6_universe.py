"""W6 shared-prep: dev universe from PUBLIC meta only (same scope as evalkit.fetch_previews.scope: run.prepare_folds(DEV_CUTOFFS), part='main').
Group per (fold, track): train (in fold train history), tried (non-decoy pool row), decoy (decoy pool row). Reads from pool only trackId + is_decoy (group flag), never label columns.
Output: DIR/universe_tracks.csv (one row per distinct public trackId) and DIR/universe_membership.csv (fold, group, trackId).
    python3 -m catalogue.w6_universe"""
import sys, hashlib, pandas as pd, numpy as np
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import data, run
DIR = data.ROOT / ".cache" / "shared-w6r1"
def md5(u): return hashlib.md5(u.encode()).hexdigest()
def build():
    mem = []; meta = {}
    for i, F in enumerate(run.prepare_folds(data.DEV_CUTOFFS)):
        fold = str(F["c"].date()); m = F["meta"]; meta.update({k: None for k in m.index if k not in meta})
        for t in pd.Index(F["train"].trackId.unique()): mem.append((fold, "train", t))
        pool, order = F["pool"], F["order"]; dec = pool.is_decoy.values[order] == 1
        for t, d in zip(F["cands"].trackId.values, dec): mem.append((fold, "decoy" if d else "tried", t))
        if i == 0: allm = m
        else: allm = pd.concat([allm, m[~m.index.isin(allm.index)]])
    mem = pd.DataFrame(mem, columns=["fold", "group", "trackId"]).drop_duplicates()
    mem["slice"] = np.where(mem.fold.isin(data.TUNE_CUTOFFS), "TUNE", "LATE")
    U = allm.loc[allm.index.isin(mem.trackId)].copy()
    ok = lambda a: isinstance(a, (list, tuple, np.ndarray)) and len(a) > 0
    U["artist"] = U.artistNames.map(lambda a: a[0] if ok(a) else "")
    U["artistNames"] = U.artistNames.map(lambda a: "|".join(a) if ok(a) else "")
    U["md5"] = U.previewUrl.map(lambda u: md5(u) if isinstance(u, str) else "")
    return mem, U.reset_index()
if __name__ == "__main__":
    DIR.mkdir(parents=True, exist_ok=True); mem, U = build()
    assert U.trackId.is_unique and set(mem.trackId) <= set(U.trackId) and mem.fold.nunique() == 14
    mem.to_csv(DIR / "universe_membership.csv", index=False); U.to_csv(DIR / "universe_tracks.csv", index=False)
    g = mem.groupby("group").trackId.nunique(); print(g.to_dict(), len(U)); print(mem.groupby(["fold", "group"]).size().unstack().to_string())
