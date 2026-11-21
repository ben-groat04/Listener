"""Leakage/sanity checks:  python -m evalkit.selftest"""
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from . import data, metrics, run
from .run import score_predictor
from .baselines import BASELINES

def _random(train, cands, meta, cutoff):   # chance level; keyed on the opaque track id => pool independent
    return (cands.trackId.values % 1000003) / 1000003.0

def main():
    from threadpoolctl import threadpool_limits; threadpool_limits(2)
    d = data._load_all(); cuts = data.DEV_CUTOFFS; pub = data.anon_streams(d); meta_all = data.load_meta_all()
    assert data.TUNE_CUTOFFS + data.LATE_CUTOFFS == cuts and len(cuts) == 14
    # ---- metrics engine vs brute force
    rng = np.random.default_rng(1); n = 600; fold = np.repeat([0, 1, 2], 200); y = (rng.random(n) < .3).astype(int); s = np.round(rng.random(n) + .5 * y, 1); art = rng.integers(0, 40, n)
    df = pd.DataFrame(dict(fold=fold.astype(str), artist=art, new_artist=rng.random(n) < .5, is_decoy=0, love=y, week=rng.integers(0, 20, n), sess=rng.integers(0, 60, n), plays90=rng.integers(1, 15, n)))
    B = metrics.Block(df, "love", 20, 0); st = B.stats(s); pw = lambda k, g: y[g == k].sum() * (1 - y[g == k]).sum(); br = lambda g: sum(metrics.auc(y[g == k], s[g == k]) * pw(k, g) for k in np.unique(g) if pw(k, g) > 0) / sum(pw(k, g) for k in np.unique(g))
    assert abs(st["sauc"][0] - br(fold)) < 1e-9 and abs(st["ww"][0] - br(df.week.values + 100 * fold)) < 1e-9 and abs(st["ws"][0] - br(df.sess.values + 100 * fold)) < 1e-9 and abs(st["wa"][0] - br(art + 100 * fold)) < 1e-9, "grouped AUC != brute force"
    ms = [metrics.fold_metrics(y[fold == f], s[fold == f], nseeds=300) for f in range(3)]
    assert abs(st["plift"][0] - sum(m["hits"] for m in ms) / sum(m["exp"] for m in ms)) < 1e-9 and abs(st["p20"][0] - np.mean([m["p20"] for m in ms])) < .01, "tie-averaged top-k != seed average"
    idx = np.repeat(np.arange(n), B.W[3].astype(int)); assert abs(st["sauc_b"][3] - sum(metrics.auc(y[idx][fold[idx] == f], s[idx][fold[idx] == f]) * y[idx][fold[idx] == f].sum() * (1 - y[idx][fold[idx] == f]).sum() for f in range(3)) / sum(y[idx][fold[idx] == f].sum() * (1 - y[idx][fold[idx] == f]).sum() for f in range(3))) < 1e-9
    # graded concordance gc / gc_wa vs brute force over all ordered pairs (same group, plays90 differ; score ties 0.5), point and one bootstrap replicate
    sg = B.stats(s, True, ("gc", "gc_wa")); pl = df.plays90.values
    def gbr(g, w):
        num = den = 0.0
        for i in range(n):
            m = (g == g[i]) & (pl[i] > pl); ww = w[i] * w * m; den += ww.sum(); num += (ww * ((s[i] > s) + .5 * (s[i] == s))).sum()
        return num / den
    assert abs(sg["gc"][0] - gbr(fold, np.ones(n))) < 1e-9 and abs(sg["gc_wa"][0] - gbr(art + 100 * fold, np.ones(n))) < 1e-9, "gc != brute force"
    assert abs(sg["gc_b"][3] - gbr(fold, B.W[3])) < 1e-9 and abs(sg["gc_wa_b"][3] - gbr(art + 100 * fold, B.W[3])) < 1e-9, "gc bootstrap != brute force"
    print("metrics engine matches brute force (incl. gc, gc_wa)")
    # ---- pools
    P = run.prepare_folds(cuts); u = data._decoys().set_index("trackId")
    for F in P:
        c, pool = F["c"], F["pool"]
        tr = d[d.t < c]; tried = pool[pool.is_decoy == 0]; dec = pool[pool.is_decoy == 1]
        assert tr.t.max() < c and not set(tried.song) & set(tr.song), "train/candidate overlap"
        trk = set(d.loc[d.song.isin(set(tried.song)), "trackId"]); assert not trk & set(tr.trackId), "a candidate's trackId was played before the cutoff"
        assert (tried["first"] >= c).all() and (tried["first"] < c + pd.DateOffset(months=3)).all()
        assert (tried["first"] + pd.Timedelta(days=data.HORIZON_DAYS) <= data.DEV_END).all(), "dev label horizon crosses DEV_END"
        assert not set(dec.song) & set(d.song) and not set(dec.trackId) & set(d.trackId), "decoy was played by the user at some point"
        assert (u.loc[dec.trackId, "release"] < c + pd.DateOffset(months=3)).all(), "decoy not yet released in the window"
        assert dec.love.sum() == 0 and len(dec) <= data.DECOY_RATIO * len(tried)
        # per-fold seeds use pre-cutoff streams only: truncating the history at the cutoff must not change them
        assert data.fold_seed_artists(d[d.t < c], c) == data.fold_seed_artists(d, c), "fold seeds depend on post-cutoff plays"
        sd, rl = data.fold_seed_artists(d, c); src = set(sd) | set(rl); assert all(not s_.isdisjoint(src) for s_ in u.loc[dec.trackId, "src"]), "decoy not from a fold seed artist"
        assert (tried.exp_before + tried.exp_after + 1 == tried.nnew_sess).all() and (tried.exp_before >= 0).all() and (tried.replays_s1 >= 1).all() and tried.replays_s1.le(tried.plays90).all(), "session diagnostics inconsistent"
        assert dec.exp_before.isna().all() and (dec.replays_s1 == 0).all()
        assert tried.share90.between(0, 1).all() and tried.share90.gt(0).all() and tried.sess.notna().all() and (dec.day1 == 0).all() and (dec.d7 == 0).all()
        # public view: opaque ids consistent between train and candidates, no order/time information, meta restricted
        cands, meta, order = F["cands"], F["meta"], F["order"]; trp = F["train"]
        assert not {"sess", "week", "day1", "d7", "nnew_sess", "exp_before", "exp_after", "replays_s1", "rb", "share90"} & set(cands.columns) | set(trp.columns) & {"sess", "week"}, "harness columns leaked into the public view"
        kn = (~pool.new_artist.values[order]); assert set(cands.artist[kn]) <= set(trp.artist), "ids not consistent between train and cands"
        assert not (set(cands.artist[~kn]) & set(trp.artist)), "new-artist candidate shares an id with train"
        assert set(meta.index) <= set(trp.trackId) | set(cands.trackId), "meta leaks tracks outside train+pool"
        assert meta.loc[cands.trackId, "popularity"].notna().mean() > .9, "meta coverage of candidates too low"
        first = pool["first"].values[order]; m = ~pd.isna(first)  # tried songs only have a first-listen time
        for nm, v in (("row order", np.arange(len(cands))), ("trackId", cands.trackId.values)):
            r = abs(spearmanr(v[m], first[m].astype("int64"))[0]); assert r < max(.2, 4 / np.sqrt(m.sum() - 1)), f"{nm} correlates with first-listen time ({r:.2f}) in fold {c.date()}"
    try: data.load_streams("2026-01-01"); raise SystemExit("sealed guard failed")
    except PermissionError: pass
    # ---- chance, oracle and independence checks on the full pipeline
    p = score_predictor(_random, cuts, "random", indep_n=3); a = metrics.auc(p[p.is_decoy == 0].love, p[p.is_decoy == 0].score)
    assert p.attrs["indep"] < 1e-6, "random scorer must be pool independent"
    dg = run.score_diagnostics(cuts); o7 = dg["oracle_7d"]; ao = metrics.auc(o7[o7.is_decoy == 0].love, o7[o7.is_decoy == 0].score)
    dep = score_predictor(lambda tr, cs, me, k: cs.groupby("artist").artist.transform("size").values.astype(float), cuts[6:8], "x", indep_n=5)
    print(f"random AUC {a:.3f} (expect ~0.5), 7-day oracle AUC {ao:.3f} (expect >0.85), pool-dependent predictor indep stat {dep.attrs['indep']:.2f} (expect >0.1)")
    assert abs(a - .5) < .05 and ao > .85 and dep.attrs["indep"] > .1
    def meta_leaker(tr, cs, me, k):
        nm = me.artistNames.map(lambda l: l[0] if isinstance(l, list) and len(l) else "").reindex(cs.trackId).values
        vc = pd.Series(me.artistNames.map(lambda l: l[0] if isinstance(l, list) and len(l) else "").values).value_counts()
        return np.array([vc.get(x, 0) for x in nm], float)
    ml = score_predictor(meta_leaker, cuts[6:8], "y", indep_n=6)
    print(f"meta-composition leaker indep p90 {ml.attrs['indep_p90']:.2f} (expect >0.1)"); assert ml.attrs["indep_p90"] > .1
    # valid baselines pass the independence gate (GBM ones are the risky ones)
    for nm in ("meta_gbm", "nonaudio_gbm", "duration", "artist_love_rate"):
        q = score_predictor(BASELINES[nm], cuts[6:8], nm, indep_n=4); print(f"{nm}: independence p90 {q.attrs['indep_p90']:.4f}"); assert q.attrs["indep_p90"] < .01, f"{nm} is pool dependent"
    # point-in-time artist features: a training song's features must equal those computed from streams strictly before its first play
    from .baselines import _Hist, _artist_feats, _sec
    F = P[cuts.index("2023-07-01")]; tr = F["train"]; st = data.song_table(tr).reset_index(); st = st[st["first"] < F["c"] - pd.Timedelta(days=90)]
    h = _Hist(tr, data.song_table(tr).reset_index()); samp = st.sample(8, random_state=0); X = _artist_feats(h, list(samp.artistIds), _sec(samp["first"].values), .25)
    for i, (_, r) in enumerate(samp.iterrows()):
        t2 = tr[tr.t < r["first"]]; s2 = data.song_table(t2).reset_index()
        if len(t2) == 0: continue
        Y = _artist_feats(_Hist(t2, pd.concat([s2, st[st.song == r.song]])), [r.artistIds], _sec(np.array([r["first"]])), .25)
        # love rate: only compare when the prior is irrelevant (columns that do not depend on matured labels)
        assert np.allclose(X.iloc[i][["ap_all", "ap_hl", "n_songs", "feat_known", "new_artist"]].astype(float), Y.iloc[0][["ap_all", "ap_hl", "n_songs", "feat_known", "new_artist"]].astype(float)), "artist features use information after the song's first play"
    print("point-in-time artist features OK")
    # ---- permutation band contains chance
    T = pd.concat([F["pool"].iloc[F["order"]].assign(fold=str(F["c"].date())) for F in P if F["c"] in pd.to_datetime(data.TUNE_CUTOFFS)]); T = T[T.is_decoy == 0].reset_index(drop=True)
    band = metrics.permutation_band(T, nperm=60); sc = np.random.default_rng(5).random(len(T)); Bt = metrics.Block(T, "love", 2, 0).stats(sc, False, ("sauc", "wa", "ww", "ws"))
    print("permutation band (60 perms)", band, "random-score point", {k: round(float(v[0]), 3) for k, v in Bt.items()})
    for k in ("sauc", "wa", "ww", "ws"): assert band[k][0] - .05 <= Bt[k][0] <= band[k][1] + .05, f"random score far outside the permutation band for {k}"
    # ---- shortcut check: can tried be told from decoys using only public metadata shape (+ release-age bucket, which is NOT public)? v2.0 reached 0.73.
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.model_selection import GroupKFold, cross_val_predict
    rows = []
    for F in P:
        pool, order, cands, meta = F["pool"], F["order"], F["cands"], F["meta"]; p = pool.iloc[order].reset_index(drop=True); m = meta.loc[cands.trackId]
        rows.append(pd.DataFrame(dict(dec=p.is_decoy.values, g=cands.artist.values, dur=m.durationMs.values, ex=m.explicit.astype(float).values, pop=m.popularity.values,
                  pv=m.previewUrl.notna().values, sid=m.spotifyId.notna().values, alb=m.albumName.isna().values, nm=(m.name.values == cands.trackName.values),
                  ae=(m.albumName.values == cands.trackName.values), ln=cands.trackName.str.len().values, na=[len(x) for x in cands.artistIds], rb=p.rb.values)).astype(float))
    Fm = pd.concat(rows)
    print("preview coverage: tried %.3f, decoys %.3f; release-age bucket unknown: tried %.3f" % (Fm[Fm.dec == 0].pv.mean(), Fm[Fm.dec == 1].pv.mean(), (Fm[Fm.dec == 0].rb == 4).mean()))
    for nm, cols in (("public metadata only", [c for c in Fm.columns if c not in ("dec", "g", "rb")]), ("public metadata + release-age bucket", [c for c in Fm.columns if c not in ("dec", "g")])):
        pr = cross_val_predict(HistGradientBoostingClassifier(max_iter=100), Fm[cols].values, Fm.dec.values, groups=Fm.g.values, cv=GroupKFold(5), method="predict_proba")[:, 1]
        sa = metrics.auc(Fm.dec.values, pr); print(f"{nm}: tried-vs-decoy AUC {sa:.3f} (expect <0.62; v2.0 was 0.73)"); assert sa < .62
    # ---- null control v2: structural checks, then the printed (not asserted) result for artist_recent and nonaudio_gbm on 3 TUNE folds
    F = P[cuts.index("2023-07-01")]; tr0, cd = F["train"], F["cands"]
    for relabel in (True, False):
        tn, am, bm = run._null_control(tr0, cd, np.random.default_rng(3), relabel)
        assert (tn.artist.values == np.array([a[0] if len(a) else tn.artist.values[0] for a in tn.artistIds])).sum() > .9 * len(tn) and (tn.song.str.rsplit("|", n=1).str[1] == tn.artist.astype(str)).all(), "null train: artist / song key inconsistent"
        assert tn.groupby("song").trackId.nunique().max() == 1 and tn.groupby("song").artist.nunique().max() == 1, "null train: a song has several identities"
        assert (tn.t.values == tr0.t.values).all(), "null control must keep timestamps"
        if relabel:
            assert len(set(am.values())) == len(am) and set(am) == set(am.values()) and len(bm) == len(set(bm.values())), "relabelling is not a bijection"
            assert len(set(tn.artist) & set(tr0.artist)) < len(set(tr0.artist)), "artists not relabelled"
    nc = cuts[:3]; res = run.null_report({k: BASELINES[k] for k in ("artist_recent", "nonaudio_gbm")}, nc, [("TUNE[:3]", nc)], "v2", None)
    print("NULL CONTROL v2 (3 TUNE folds, 3 seeds; printed, not asserted; band = 95% band of the 3-seed mean)"); print(res["TUNE[:3]"]["band"]); print(res["TUNE[:3]"]["table"].drop(columns="slice").to_string(index=False))
    print("selftest OK")

if __name__ == "__main__": main()
