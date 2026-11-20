"""Leakage/sanity checks:  python -m evalkit.selftest"""
import numpy as np, pandas as pd
from . import data, metrics
from .run import score_predictor

def main():
    d = data._load_all(); cuts = data.DEV_CUTOFFS
    for c, f in data.make_folds(cuts, d):
        tr = d[d.t < c]
        assert tr.t.max() < c and not set(f.song) & set(tr.song), "train/candidate overlap"
        assert (f["first"] >= c).all() and (f["first"] < c + pd.DateOffset(months=3)).all()
        assert (f["first"] + pd.Timedelta(days=data.HORIZON_DAYS) <= data.DEV_END).all(), "dev label horizon crosses DEV_END"
    try: data.load_streams("2026-01-01"); raise SystemExit("sealed guard failed")
    except PermissionError: pass
    # shuffled scores must give AUC ~ 0.5; an (intentionally leaky) first-week-plays oracle must give high AUC
    rng = np.random.default_rng(0)
    p = score_predictor(lambda t, c, m, k: rng.random(len(c)), cuts); a = metrics.auc(p.love, p.score)
    full = d.groupby("song").t.agg(["min"])  # leaky oracle: uses plays AFTER cutoff, proves labels are meaningful
    def oracle(t, c, m, k):
        x = d[d.song.isin(c.song)].merge(full, left_on="song", right_index=True)
        n = x[x.t < x["min"] + pd.Timedelta(days=7)].groupby("song").size()
        return c.song.map(n).fillna(0).values
    o = score_predictor(oracle, cuts); ao = metrics.auc(o.love, o.score)
    print(f"random AUC {a:.3f} (expect ~0.5), leaky 7-day oracle AUC {ao:.3f} (expect >0.85)")
    assert abs(a - .5) < .05 and ao > .85
    print("selftest OK")

if __name__ == "__main__": main()
