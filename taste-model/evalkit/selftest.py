"""Leakage/sanity checks:  python -m evalkit.selftest"""
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from . import data, metrics
from .run import score_predictor
from .baselines import BASELINES

def main():
    d = data._load_all(); cuts = data.DEV_CUTOFFS; pub = data.anon_streams(d); meta_all = data.load_meta_all()
    for c, pool in data.make_open_folds(cuts, d):
        tr = d[d.t < c]; tried = pool[pool.is_decoy == 0]; dec = pool[pool.is_decoy == 1]
        assert tr.t.max() < c and not set(tried.song) & set(tr.song), "train/candidate overlap"
        trk = set(d.loc[d.song.isin(set(tried.song)), "trackId"]); assert not trk & set(tr.trackId), "a candidate's trackId was played before the cutoff"
        assert (tried["first"] >= c).all() and (tried["first"] < c + pd.DateOffset(months=3)).all()
        assert (tried["first"] + pd.Timedelta(days=data.HORIZON_DAYS) <= data.DEV_END).all(), "dev label horizon crosses DEV_END"
        assert not set(dec.song) & set(d.song) and not set(dec.trackId) & set(d.trackId), "decoy was played by the user at some point"
        u = data._decoys().set_index("trackId")
        assert (u.loc[dec.trackId, "release"] < c + pd.DateOffset(months=3)).all(), "decoy not yet released in the window"
        assert dec.love.sum() == 0 and len(dec) <= data.DECOY_RATIO * len(tried)
        # public view: opaque ids consistent between train and candidates, no order/time information, meta restricted
        cands, meta, order = data.public_view(pool, meta_all, tr, seed=int(c.strftime("%Y%m%d")))
        trp = pub[d.t < c]
        kn = (~pool.new_artist.values[order]); assert set(cands.artist[kn]) <= set(trp.artist), "ids not consistent between train and cands"
        assert not (set(cands.artist[~kn]) & set(trp.artist)), "new-artist candidate shares an id with train"
        assert set(meta.index) <= set(trp.trackId) | set(cands.trackId), "meta leaks tracks outside train+pool"
        assert meta.loc[cands.trackId, "popularity"].notna().mean() > .9, "meta coverage of candidates too low"
        first = pool["first"].values[order]; m = ~pd.isna(first)  # tried songs only have a first-listen time
        for nm, v in (("row order", np.arange(len(cands))), ("trackId", cands.trackId.values)):  # (album/artist tokens are clustered categories, so a rank correlation is not meaningful for them)
            r = abs(spearmanr(v[m], first[m].astype("int64"))[0]); assert r < .2, f"{nm} correlates with first-listen time ({r:.2f}) in fold {c.date()}"
    try: data.load_streams("2026-01-01"); raise SystemExit("sealed guard failed")
    except PermissionError: pass
    # chance and leaky-oracle checks on the full pipeline
    p = score_predictor(BASELINES["random"], cuts, "random", indep_n=3); a = metrics.auc(p[p.is_decoy == 0].love, p[p.is_decoy == 0].score)
    assert p.attrs["indep"] < 1e-6, "random baseline must be pool independent"
    full = d.groupby("song").t.agg(["min"])
    # oracle needs raw song keys: score straight on the tried pool instead of through the anonymised interface
    ao = []
    for cc, pool in data.make_open_folds(cuts, d):
        t = pool[pool.is_decoy == 0]; x = d[d.song.isin(set(t.song))].merge(full, left_on="song", right_index=True)
        n = x[x.t < x["min"] + pd.Timedelta(days=7)].groupby("song").size()
        ao.append(metrics.auc(t.love, t.song.map(n).fillna(0)))
    ao = float(np.mean(ao))
    # pool-dependence detection: the sibling diagnostic is flagged (indep check skipped for it), and a pool-dependent
    # predictor that is NOT whitelisted must show a large singleton/pool discrepancy
    dep = score_predictor(lambda tr, cs, me, k: cs.groupby("artist").artist.transform("size").values.astype(float), cuts[:2], "x", indep_n=5)
    print(f"random AUC {a:.3f} (expect ~0.5), leaky 7-day oracle AUC {ao:.3f} (expect >0.85), pool-dependent predictor indep stat {dep.attrs['indep']:.2f} (expect >0.1)")
    assert abs(a - .5) < .05 and ao > .85 and dep.attrs["indep"] > .1
    print("selftest OK")

if __name__ == "__main__": main()
