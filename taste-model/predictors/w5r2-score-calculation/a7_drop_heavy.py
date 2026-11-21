"""Pooled sauc delta with the heaviest folds removed, and leave-one-fold-out range."""
import sys; sys.path.insert(0, "."); sys.path.insert(0, "/home/user/Listener/taste-model")
from lib import *; import evalkit.metrics as M
d = pd.read_pickle(DUMP); t = d[d.fold_set == "tune"]
n = t.groupby("fold").size(); print("fold sizes", n.to_dict())
# pair weight ~ npos*nneg
pw = t.groupby("fold").love.agg(lambda y: y.sum() * (len(y) - y.sum())); heavy = pw.sort_values(ascending=False).index[:2].tolist(); print("pair-weight shares", (pw / pw.sum()).round(3).to_dict(), "heavy", heavy)
def run(sub, label):
    sub = sub.copy(); sub["fold_set"] = "tune"
    for a, b in [("pair_z", "artist_recent"), ("ref_w4r1_listening", "artist_recent"), ("ref_w4r1_music", "artist_recent"), ("ref_audio_final", "artist_recent"), ("ref_w4r1_listening", "ref_w4r1_music"), ("ref_w4r1_music", "ref_audio_final"), ("pair_z", "ref_w4r1_listening"), ("pair_z", "ref_w4r1_music")]:
        r = M.dump_sauc_delta(sub, "tune", a, b, "fold", "love", 1000, 20260511)
        print(f"{label:28s} {a:20s}-{b:20s} d={r['d']:+.3f} 80% [{r['lo80']:+.3f},{r['hi80']:+.3f}]")
run(t[~t.fold.isin(heavy)], "drop 2 heaviest folds")
run(t[t.fold.isin(heavy)], "ONLY the 2 heaviest folds")
loo = {}
for f in t.fold.unique():
    s = t[t.fold != f].copy()
    for a, b in [("pair_z", "artist_recent"), ("ref_w4r1_listening", "artist_recent")]:
        loo.setdefault((a, b), []).append(M.dump_sauc_delta(s, "tune", a, b, "fold", "love", 200, 1)["d"])
for k, v in loo.items(): print("leave-one-fold-out", k, "range", round(min(v), 3), round(max(v), 3))
