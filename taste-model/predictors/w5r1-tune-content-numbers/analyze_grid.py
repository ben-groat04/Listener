"""Sensitivity map from score dumps. usage: analyze_grid.py real.pkl [perm1.pkl perm2.pkl ...]  -> prints per-model sauc, paired delta vs default (80% interval), spread vs random-label null."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import metrics
from grid import OAT, RJ
def stats(path, models, nboot=300):
    d = pd.read_pickle(path); B = metrics.dump_block(d, "tune", "fold", nboot=nboot); g = d[d.fold_set == "tune"]
    st = {m: B.stats(g["score__" + m].values, True, ("sauc",)) for m in models}; base = st["default"]
    rows = []
    for m in models:
        dd = st[m]["sauc_b"] - base["sauc_b"]; f = dd[np.isfinite(dd)]
        rows.append(dict(model=m, sauc=float(st[m]["sauc"][0]), d=float(st[m]["sauc"][0] - base["sauc"][0]), lo80=np.percentile(f, 10), hi80=np.percentile(f, 90), P=float((f > 0).mean())))
    return pd.DataFrame(rows).set_index("model")
if __name__ == "__main__":
    models = list(OAT) + list(RJ); R = stats(sys.argv[1], models); pd.set_option("display.width", 200); pd.set_option("display.max_rows", 500)
    print(R.round(4).to_string())
    for name, ms in [("OAT", list(OAT)[1:]), ("RJ", list(RJ)), ("ALL", list(OAT)[1:] + list(RJ))]:
        x = R.loc[ms]; print(f"\n{name}: N={len(ms)} sauc mean {x.sauc.mean():.4f} sd {x.sauc.std():.4f} min {x.sauc.min():.4f} max {x.sauc.max():.4f}; delta max {x.d.max():+.4f} (best {x.d.idxmax()}), #lo80>0: {(x.lo80>0).sum()}, #P>0.9: {(x.P>0.9).sum()}, #d>0 {(x.d>0).sum()}")
    nulls = []
    for p in sys.argv[2:]:
        Rn = stats(p, models, nboot=100); nulls.append(Rn); x = Rn.loc[list(OAT)[1:] + list(RJ)]
        print(f"\nPERM {os.path.basename(p)}: sauc mean {x.sauc.mean():.4f} sd {x.sauc.std():.4f} range [{x.sauc.min():.4f},{x.sauc.max():.4f}]; delta-vs-default sd {x.d.std():.4f} max {x.d.max():+.4f} min {x.d.min():+.4f}; #lo80>0 {(x.lo80>0).sum()}/{len(x)}")
    R.to_csv(os.environ.get("OUT", "/tmp/grid_real.csv"))
