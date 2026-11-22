"""Leakage/sanity checks:  python -m evalkit.selftest"""
import os, sys, json, glob, hashlib, tempfile, pickle
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from . import data, metrics, run
from .run import score_predictor
from .baselines import BASELINES

def _random(train, cands, meta, cutoff):   # chance level; keyed on the opaque track id => pool independent
    return (cands.trackId.values % 1000003) / 1000003.0

def br_idx(yy, ss, g):
    """Brute-force pooled grouped AUC of a (resampled, row-duplicated) sample: every positive/negative pair in a group, ties half."""
    num = den = 0.0
    for k in np.unique(g):
        m = g == k; a, b = ss[m][yy[m] == 1], ss[m][yy[m] == 0]
        if len(a) and len(b): num += ((a[:, None] > b[None]) + .5 * (a[:, None] == b[None])).sum(); den += len(a) * len(b)
    return num / den

def main():
    from threadpoolctl import threadpool_limits; threadpool_limits(2)
    os.environ.setdefault("EVALKIT_RUN_LOG_DIR", tempfile.mkdtemp(prefix="evalkit_runlog_"))   # selftest runs must not append to the real run log
    if "--v41" in sys.argv: P_ = run.prepare_folds(data.DEV_CUTOFFS); v41_checks(data._load_all(), P_, _tune_tried(P_)); return
    if "--v5" in sys.argv: P_ = run.prepare_folds(data.DEV_CUTOFFS); v5_checks(data._load_all(), P_); return
    if "--v51" in sys.argv: v51_checks(); return
    if "--v52" in sys.argv: v52_checks(); return   # no raw-stream access (the harness builds / reads its pools itself)
    if "--v53" in sys.argv: from . import selftest_v53; selftest_v53.v53_checks(); return   # v5.3: --v52 first, then the sealed-era pipeline / lookup / output checks (dev data and synthetic slices only)
    d = data._load_all(); cuts = data.DEV_CUTOFFS; pub = data.anon_streams(d); meta_all = data.load_meta_all()
    assert data.TUNE_CUTOFFS + data.LATE_CUTOFFS == cuts and len(cuts) == 14
    # ---- metrics engine vs brute force
    rng = np.random.default_rng(1); n = 600; fold = np.repeat([0, 1, 2], 200); y = (rng.random(n) < .3).astype(int); s = np.round(rng.random(n) + .5 * y, 1); art = rng.integers(0, 40, n)
    xb = rng.integers(0, 14, n).astype(float)
    df = pd.DataFrame(dict(fold=fold.astype(str), artist=art, new_artist=rng.random(n) < .5, is_decoy=0, love=y, week=rng.integers(0, 20, n), sess=rng.integers(0, 60, n), plays90=rng.integers(1, 15, n), exp_before=xb))
    B = metrics.Block(df, "love", 20, 0); st = B.stats(s); pw = lambda k, g: y[g == k].sum() * (1 - y[g == k]).sum(); br = lambda g: sum(metrics.auc(y[g == k], s[g == k]) * pw(k, g) for k in np.unique(g) if pw(k, g) > 0) / sum(pw(k, g) for k in np.unique(g))
    xbk = metrics.exp_bucket(xb).astype(int); assert set(np.unique(metrics.exp_bucket([0, 1, 2, 3, 8, 9, 40]))) == {0, 1, 2, 3} and list(metrics.exp_bucket([0, 1, 2, 3, 8, 9, 40])) == [0, 1, 1, 2, 2, 3, 3]
    assert abs(st["sauc"][0] - br(fold)) < 1e-9 and abs(st["ww"][0] - br(df.week.values + 100 * fold)) < 1e-9 and abs(st["ws"][0] - br(df.sess.values + 100 * fold)) < 1e-9 and abs(st["wa"][0] - br(art + 100 * fold)) < 1e-9, "grouped AUC != brute force"
    assert abs(st["wx"][0] - br(xbk + 10 * fold)) < 1e-9, "wx != brute force (pairs sharing fold and exposure_before bucket)"
    macro_br = lambda yy, ss, ff: np.mean([metrics.auc(yy[ff == k], ss[ff == k]) for k in np.unique(ff) if (yy[ff == k] == 1).sum() >= 10 and (yy[ff == k] == 0).sum() >= 10])
    assert abs(st["macro"][0] - macro_br(y, s, fold)) < 1e-9, "macro_sauc != mean of per-fold AUC"
    ms = [metrics.fold_metrics(y[fold == f], s[fold == f], nseeds=300) for f in range(3)]
    assert abs(st["plift"][0] - sum(m["hits"] for m in ms) / sum(m["exp"] for m in ms)) < 1e-9 and abs(st["p20"][0] - np.mean([m["p20"] for m in ms])) < .01, "tie-averaged top-k != seed average"
    # v4 bootstrap: a cluster is the primary artist GLOBALLY (the same draw count for all rows of an artist in every fold); brute force on the resampled (duplicated) rows, product pair weights
    for a_ in np.unique(art): assert (B.W[:, art == a_] == B.W[:, art == a_][:, :1]).all(), "rows of one artist must share their draw count across folds"
    assert (B.W.sum(1) > 0).all() and abs(B.C.sum(1) - len(np.unique(art))).max() < 1e-9, "a bootstrap draw takes as many artist clusters as there are artists"
    for r_ in (3, 7):
        idx = np.repeat(np.arange(n), B.W[r_].astype(int)); yi, si, fi, ai, xi = y[idx], s[idx], fold[idx], art[idx], xbk[idx]
        assert abs(st["sauc_b"][r_] - br_idx(yi, si, fi)) < 1e-9, "bootstrap sauc != brute force on resampled rows"
        assert abs(st["wa_b"][r_] - br_idx(yi, si, ai + 100 * fi)) < 1e-9, "bootstrap wa != brute force (product pair weights)"
        assert abs(st["wx_b"][r_] - br_idx(yi, si, xi + 10 * fi)) < 1e-9, "bootstrap wx != brute force"
        assert abs(st["macro_b"][r_] - macro_br(yi, si, fi)) < 1e-9, "bootstrap macro != brute force"
    # graded concordance gc / gc_wa vs brute force over all ordered pairs (same group, plays90 differ; score ties 0.5), point and one bootstrap replicate
    sg = B.stats(s, True, ("gc", "gc_wa")); pl = df.plays90.values
    def gbr(g, w):
        num = den = 0.0
        for i in range(n):
            m = (g == g[i]) & (pl[i] > pl); ww = w[i] * w * m; den += ww.sum(); num += (ww * ((s[i] > s) + .5 * (s[i] == s))).sum()
        return num / den
    assert abs(sg["gc"][0] - gbr(fold, np.ones(n))) < 1e-9 and abs(sg["gc_wa"][0] - gbr(art + 100 * fold, np.ones(n))) < 1e-9, "gc != brute force"
    assert abs(sg["gc_b"][3] - gbr(fold, B.W[3])) < 1e-9 and abs(sg["gc_wa_b"][3] - gbr(art + 100 * fold, B.W[3])) < 1e-9, "gc bootstrap != brute force"
    print("metrics engine matches brute force (incl. wa, wx, macro, gc, gc_wa, global-artist-cluster bootstrap)")
    # ---- pools
    P = run.prepare_folds(cuts); u = data._decoys().set_index("trackId")
    # ---- v4: the dev pools are bit-identical to the v3.1 cache (digests recorded in pool_reference.json BEFORE any v4 change), and the content of the files the pools were built from is unchanged
    ref = json.load(open(run.POOL_REFERENCE)); PA = run.prepare_folds(cuts, "all"); PH = run.prepare_folds(cuts, "holdout")
    pk = pickle.load(open(run._pool_path(), "rb"))
    for F in PA:
        k = str(F["c"].date()); assert len(F["pool"]) == ref["pool_rows"][k]["n"] and run._pool_digest(F["pool"]) == ref["pool_rows"][k]["digest"], f"pool {k} differs from the recorded v3.1 pool"
        assert run._pool_digest(pk[k]) == ref["pool_rows"][k]["digest"]
    assert run._content_hashes() == ref["content_hashes"], "itunes_fallback.csv / album_release.json / decoy_raw content differs from the recorded hashes (the pools would no longer be reproducible)"
    print("pools bit-identical to the recorded v3.1 pools (14 folds); itunes_fallback.csv, album_release.json, decoy_raw content hashes match the recorded values")
    # ---- HOLDOUT: artist-disjoint, salted hash; shares reported; main / holdout partition the pools; predictors never see holdout rows
    import hashlib as _hl
    assert data.is_holdout(-1) is False and data.is_holdout(12345) == (int(_hl.sha256(b"w4-holdout|12345").hexdigest(), 16) % 100 < 25) and data.HOLDOUT_SALT == "w4-holdout|", "holdout definition"
    tt = th = lt = lh = 0; print("HOLDOUT share (tried songs / loved songs) per fold:")
    for FA, FM, FH in zip(PA, P, PH):
        pa, pm, ph = FA["pool"], FM["pool"], FH["pool"]; ho = data.is_holdout(pa.artist.values)
        assert len(pm) + len(ph) == len(pa) and not data.is_holdout(pm.artist.values).any() and data.is_holdout(ph.artist.values).all(), "main / holdout rows do not partition the pool"
        assert not (set(pm.artist) & set(ph.artist)), "HOLDOUT is not artist-disjoint"
        ta, la = (pa.is_decoy == 0).values, ((pa.is_decoy == 0) & (pa.love == 1)).values; tt += ta.sum(); th += (ho & ta).sum(); lt += la.sum(); lh += (ho & la).sum()
        print(f"  {FA['c'].date()}: tried {(ho & ta).sum()}/{ta.sum()} = {(ho & ta).sum() / ta.sum():.3f}   loved {(ho & la).sum()}/{la.sum()} = {(ho & la).sum() / max(1, la.sum()):.3f}")
        rem = {run.data.h(t) for t in pa.trackId[ho]}; assert not (rem & set(FM["cands"].trackId)) and not (rem & set(FM["meta"].index) - set(FM["train"].trackId)), "HOLDOUT rows leaked into cands / meta of a main run"
        assert len(FM["cands"]) == len(pm) and len(FH["cands"]) == len(ph)
        mt = set(FM["train"].trackId); assert not (set(FH["cands"].trackId) & set(FM["cands"].trackId))
    shr = th / tt; print(f"  OVERALL: tried {th}/{tt} = {shr:.3f}   loved {lh}/{lt} = {lh / lt:.3f}   (salt '{data.HOLDOUT_SALT}')"); assert .18 <= shr <= .32, "HOLDOUT share of tried songs outside 18-32%: change the salt suffix once (w4-holdout-2) and document it"
    PAd = {F["c"]: F["pool"] for F in PA}
    for F in P:
        c, pool = F["c"], F["pool"]
        tr = d[d.t < c]; tried = pool[pool.is_decoy == 0]; dec = pool[pool.is_decoy == 1]
        assert tr.t.max() < c and not set(tried.song) & set(tr.song), "train/candidate overlap"
        trk = set(d.loc[d.song.isin(set(tried.song)), "trackId"]); assert not trk & set(tr.trackId), "a candidate's trackId was played before the cutoff"
        assert (tried["first"] >= c).all() and (tried["first"] < c + pd.DateOffset(months=3)).all()
        assert (tried["first"] + pd.Timedelta(days=data.HORIZON_DAYS) <= data.DEV_END).all(), "dev label horizon crosses DEV_END"
        assert not set(dec.song) & set(d.song) and not set(dec.trackId) & set(d.trackId), "decoy was played by the user at some point"
        assert (u.loc[dec.trackId, "release"] < c + pd.DateOffset(months=3)).all(), "decoy not yet released in the window"
        pa_ = PAd[c]; assert dec.love.sum() == 0 and (pa_.is_decoy == 1).sum() <= data.DECOY_RATIO * (pa_.is_decoy == 0).sum(), "decoy ratio (full pool)"
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
    # ---- null control v3: every seed in a FRESH process; an identity-blind module-level cache must NOT survive across seeds (asserted)
    dummy = tempfile.mkdtemp(prefix="evalkit_dummy_") + "/dummy_blind.py"
    open(dummy, "w").write("import numpy as np\n_C = {}\ndef predict(train, cands, meta, cutoff):\n    k = str(cutoff)   # identity-blind module-level cache (keyed on the cutoff only)\n    if k not in _C: _C[k] = train.groupby('artist').size().to_dict()\n    return np.array([_C[k].get(a, 0) for a in cands.artist], float)\n")
    spec = __import__("importlib.util").util.spec_from_file_location("dummy_blind", dummy); dm = __import__("importlib.util").util.module_from_spec(spec); spec.loader.exec_module(dm)
    nc = cuts[:3]
    s0 = score_predictor(dm.predict, nc, "d", 0, ("v2", 0), None, None, "all").score.values; s1 = score_predictor(dm.predict, nc, "d", 0, ("v2", 1), None, None, "all").score.values
    assert np.array_equal(s0, s1), "premise of the check: in ONE process the identity-blind cache gives identical scores for different seeds"
    res_seed = {k: run.run_null_worker([dummy], k, "tune3", ["dummy_blind"])["dummy_blind"] for k in range(3)}
    for i in range(3):
        for j in range(i + 1, 3): assert not np.array_equal(res_seed[i], res_seed[j]), f"null seeds {i} and {j} give IDENTICAL scores in fresh processes: caches carry over"
    print("null control v3: identity-blind module-level cache gives identical scores in one process but 3 DIFFERENT score vectors across 3 fresh-process seeds (asserted)")
    assert os.environ.get("EVALKIT_NO_FIT_CACHE") is None and run._null_env(2)["EVALKIT_NULL_SEED"] == "2" and run._null_env(2)["EVALKIT_NO_FIT_CACHE"] == "1"
    # the harness' own baselines (fit caches keyed on seed / identities) and the null-report table on 3 TUNE folds, 3 seeds
    res = run.null_report([], {k: BASELINES[k] for k in ("artist_recent", "nonaudio_gbm")}, "tune3", [("TUNE[:3]", nc)], "v2", 3, None)
    tb = res["TUNE[:3]"]["table"]; print("NULL CONTROL v4 (3 TUNE folds, 3 seeds; printed; song-level band of the 3-seed mean)"); print(res["TUNE[:3]"]["band"]); print(tb.drop(columns="slice").to_string(index=False))
    for _, r in tb.iterrows(): assert len({r["sauc_s1"], r["sauc_s2"], r["sauc_s3"], r["wa_sauc_s1"], r["wa_sauc_s2"], r["wa_sauc_s3"]}) > 1 or r["model"] == "artist_recent", f"{r['model']}: the 3 null seeds gave identical results"
    assert tb[tb.model == "nonaudio_gbm"].iloc[0][["sauc_s1", "sauc_s2", "sauc_s3"]].nunique() == 3, "nonaudio_gbm null seeds must differ"
    # the reference row (audio_final) must be identity-safe: different null seeds in one process give different scores
    ra = score_predictor(run.ref_fn(), cuts[:1], "r", 0, ("v2", 0), None, None, "all").score.values; rb_ = score_predictor(run.ref_fn(), cuts[:1], "r", 0, ("v2", 1), None, None, "all").score.values
    assert not np.array_equal(ra, rb_), "ref_audio_final reused a fit across null seeds (cache key not identity-safe)"
    # ---- caps (temp logs): --late 2 runs per predictor hash, --holdout 1 run per hash
    tl = tempfile.mkdtemp(prefix="evalkit_caplog_"); lg = __import__("pathlib").Path(tl) / "late.log"; hg = __import__("pathlib").Path(tl) / "holdout.log"; hh = "ab" * 32
    run.late_cap_check([hh], lg); lg.write_text(json.dumps(dict(sha256=[hh])) + "\n"); run.late_cap_check([hh], lg); lg.write_text(lg.read_text() + json.dumps(dict(sha256=[hh, "cd" * 32])) + "\n")
    try: run.late_cap_check([hh], lg); raise AssertionError("third --late run of the same predictor hash was not refused")
    except SystemExit as e: assert "REFUSED" in str(e) and "cap 2" in str(e)
    run.late_cap_check(["ef" * 32], lg); run.holdout_cap_check([hh], hg); hg.write_text(json.dumps(dict(sha256=[hh])) + "\n")
    try: run.holdout_cap_check([hh], hg); raise AssertionError("second --holdout run of the same hash was not refused")
    except SystemExit as e: assert "REFUSED" in str(e)
    for bad in (["--holdout", "--fast"], ["--holdout", "--null-control"], ["--holdout", "--late"], ["--holdout", "--sealed"]):
        try: run.main(bad); raise SystemExit("--holdout combination was accepted: " + " ".join(bad))
        except AssertionError: pass
    tp = run.late_write_tables(["ab" * 32], "x", __import__("pathlib").Path(tl) / "tables"); assert oct(os.stat(tp[0]).st_mode & 0o777) == "0o444"
    print("caps: third --late run and second --holdout run of the same hash are refused; --holdout with --fast / --null-control / --late / --sealed is refused; late tables are mode 444")
    # ---- cache-key hygiene of the shared harness caches: the baseline fit key contains the null seed and the train identities
    from . import baselines as bl
    k1 = bl._train_key("x", F["train"], F["c"]); os.environ["EVALKIT_NULL_SEED"] = "1"; k2 = bl._train_key("x", F["train"], F["c"]); del os.environ["EVALKIT_NULL_SEED"]
    tr_sh = F["train"].copy(); tr_sh["artist"] = tr_sh.artist.values[::-1]; assert k1 != k2 and k1 != bl._train_key("x", tr_sh, F["c"]), "fit-cache key ignores the seed / artist identities"
    v41_checks(d, P, T)
    v5_checks(d, P)
    v51_checks()
    v52_checks()
    print("selftest OK")

def _tune_tried(P):
    T = pd.concat([F["pool"].iloc[F["order"]].assign(fold=str(F["c"].date())) for F in P if F["c"] in pd.to_datetime(data.TUNE_CUTOFFS)]); return T[T.is_decoy == 0].reset_index(drop=True)

def v41_checks(d, P, T):
    """v4.1 checks (python3 -m evalkit.selftest --v41 runs only these)."""
    from threadpoolctl import threadpool_limits; threadpool_limits(2)
    import importlib.util as _iu, subprocess, shutil, pathlib
    from . import bundle, refs
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="evalkit_v41_"))
    # ---- `keep` label (>= 6 plays in days [90, 365) after the first play): brute force vs raw streams on 40 tried songs of the first TUNE fold; LATE folds are n/a; never public
    Pk = P[8]["pool"]; tr_ = Pk[Pk.is_decoy == 0]; assert tr_.keep.notna().all() and set(tr_.keep.unique()) <= {0.0, 1.0} and Pk[Pk.is_decoy == 1].keep.eq(0).all(), "keep missing for a TUNE fold"
    for _, r_ in tr_.sample(40, random_state=1).iterrows():
        dd = d[d.song == r_.song]; cnt = ((dd.t >= r_["first"] + pd.Timedelta(days=90)) & (dd.t < r_["first"] + pd.Timedelta(days=365))).sum(); assert float(cnt >= 6) == r_.keep, f"keep != brute force for {r_.song}"
    assert all(run.keep_qualifies(c_) for c_ in data.TUNE_CUTOFFS) and not any(run.keep_qualifies(c_) for c_ in data.LATE_CUTOFFS), "keep must be computed for all TUNE folds and n/a for LATE folds"
    assert all(F_["pool"].keep.isna().all() for F_ in P if str(F_["c"].date()) in data.LATE_CUTOFFS), "keep must be NaN on LATE folds"
    assert not ({"keep"} & set(P[0]["cands"].columns)) and "keep" not in P[0]["meta"].columns and "keep" not in P[0]["train"].columns, "keep leaked into the public view"
    print(f"keep label: matches brute force on 40 songs; {int(tr_.keep.sum())}/{len(tr_)} kept in TUNE fold 2023-07; LATE folds n/a; not public")
    # ---- bundle hash: an importing wrapper is refused (temp logs), also when the predictor is loaded lazily at call time; a docstring mention is not a dependency
    real = "/home/user/Listener/taste-model/predictors/w4r1-taste-from-all-listening/predict.py"; real_sha = run._sha(real)
    w1 = tmp / "wrapper_import.py"; w1.write_text(f"import importlib.util\n_s = importlib.util.spec_from_file_location('inner', '{real}'); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)\nPREDICTORS = {{'wrapped': _m.PREDICTORS['w4r1_final']}}\n")
    w2 = tmp / "wrapper_lazy.py"; w2.write_text(f"import importlib.util\ndef predict(train, cands, meta, cutoff):\n    s = importlib.util.spec_from_file_location('inner', ROOT + 'predictors/w4r1-taste-from-all-listening/predict.py'); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)\n    return m.PREDICTORS['w4r1_final'](train, cands, meta, cutoff)\nROOT = '/home/user/Listener/taste-model/'\n")
    w3 = tmp / "doc_only.py"; w3.write_text(f'"""see predictors/w4r1-taste-from-all-listening/predict.py for the idea"""\nimport numpy as np\ndef predict(train, cands, meta, cutoff): return np.zeros(len(cands))\n')
    lg2 = tmp / "late2.log"; hg2 = tmp / "holdout2.log"; lg2.write_text("".join(json.dumps(dict(sha256=[real_sha])) + "\n" for _ in range(2))); hg2.write_text(json.dumps(dict(sha256=[real_sha])) + "\n")
    for w, expect in ((w1, True), (w2, True), (w3, False)):
        bi = bundle.describe(str(w)); mem = sorted(bi["members"].values()); assert (real_sha in mem) == expect, f"bundle members of {w.name}: {list(bi['members'])}"
        for fn_, kw_ in ((run.late_cap_check, dict(log=lg2)), (run.holdout_cap_check, dict(log=hg2))):
            try: fn_([run._sha(w)], bundles=[bi["bundle_sha256"]], members=mem, **kw_); assert not expect, f"importing wrapper {w.name} was not refused"
            except SystemExit as e: assert expect and "REFUSED" in str(e) and "wrapper" in str(e), str(e)
    assert bundle.bundle_sha256([str(w1)]) != bundle.bundle_sha256([str(w3)]) and bundle.bundle_sha256([real]) == bundle.bundle_sha256([real])
    # the cap also applies to the bundle hash itself (v4.1 log lines carry it) and to the entry sha; old lines (entry sha only) keep counting
    lg3 = tmp / "late3.log"; bh = "cd" * 32; lg3.write_text(json.dumps(dict(sha256=["01" * 32], bundle_sha256=[bh])) + "\n" + json.dumps(dict(sha256=["02" * 32], bundle_sha256=[bh])) + "\n")
    try: run.late_cap_check(["03" * 32], lg3, bundles=[bh]); raise AssertionError("bundle-hash cap not enforced")
    except SystemExit as e: assert "bundle hash" in str(e)
    run.late_cap_check(["03" * 32], lg3, bundles=["ee" * 32])
    print("bundle hash: importing / lazily loading wrapper of a predictor that used up its runs is refused for --late and --holdout (temp logs); a docstring mention is not a dependency; bundle-hash cap enforced")
    # ---- fingerprints: a renamed / lightly edited copy of a logged model is refused (Spearman >= 0.999 on the first fold of the slice); a different scorer and a re-run of the same file are not
    for sl_ in ("late", "holdout"):
        fp = tmp / f"{sl_}_fp.pkl"; v1 = run.first_fold_vectors({"orig": _random}, sl_); run.fingerprint_check(fp, "aa" * 32, v1); run.fingerprint_record(fp, "aa" * 32, v1)
        run.fingerprint_check(fp, "aa" * 32, {"orig": v1["orig"]})   # same file again: not compared with itself
        run.fingerprint_check(fp, "bb" * 32, run.first_fold_vectors({"other": lambda tr, cs, me, k: ((cs.trackId.values * 7919) % 1000003) / 1000003.0}, sl_))
        try: run.fingerprint_check(fp, "cc" * 32, {"renamed_copy": v1["orig"] * 3 + 1}); raise AssertionError("renamed copy was not refused")
        except SystemExit as e: assert "REFUSED" in str(e) and "renamed" in str(e)
    print("fingerprints: a renamed copy of a logged model is refused on the first fold of the late / holdout slice (temp files); a different scorer and a re-run of the same file pass")
    # ---- holdout budget
    bj = tmp / "budget.json"
    try: run.holdout_budget_check(bj); raise AssertionError("missing budget file accepted")
    except SystemExit as e: assert "REFUSED" in str(e)
    bj.write_text(json.dumps(dict(round="t", remaining=1))); run.holdout_budget_check(bj); assert run.holdout_budget_use(bj)["remaining"] == 0
    try: run.holdout_budget_check(bj); raise AssertionError("budget 0 accepted")
    except SystemExit as e: assert "REFUSED" in str(e)
    assert json.load(open(run.HOLDOUT_BUDGET))["remaining"] >= 0   # v5.0: the file is regenerable (python3 -m evalkit.holdout_budget); v5_checks asserts the round
    print("holdout budget: refused when the file is missing or remaining is 0; each use decrements")
    # ---- walk-forward vs brute force on 3 dummy members (7 folds, two folds too small to count)
    rngw = np.random.default_rng(11); fn_ = ["f%d" % i for i in range(7)]; rows_ = []
    for i, (nf, nl) in enumerate([(30, 8), (200, 60), (200, 8), (22, 11), (200, 60), (200, 60), (200, 60)]):   # folds 0 and 2 have < 10 loved rows: never eligible
        rows_.append(pd.DataFrame(dict(fold=fn_[i], trackId=np.arange(nf) + 1000 * i, is_decoy=0, love=rngw.permutation(np.r_[np.ones(nl, int), np.zeros(nf - nl, int)]))))
    base = pd.concat(rows_, ignore_index=True); yb = base.love.values
    mem_ = {}
    for j, nm in enumerate(("m_a", "m_b", "m_c")): mem_[nm] = base.assign(score=np.round(rngw.random(len(base)) + (.2 * (j + 1) * yb if j != 1 else 0) * (base.fold.isin(fn_[:3])), 1))   # rounded: ties
    comp_, ch_ = run.walkforward_composite(mem_, fn_)
    exp_sc = np.zeros(len(base)); exp_ch = []
    for k, f_ in enumerate(fn_):
        elig = [g for g in fn_[:k] if (yb[(base.fold == g).values].sum() >= 10 and (1 - yb[(base.fold == g).values]).sum() >= 10)]; pick = "m_a"
        if elig:
            m_ = base.fold.isin(elig).values; vals = {n: br_idx(yb[m_], mem_[n].score.values[m_], pd.factorize(base.fold.values[m_])[0]) for n in mem_}; pick = max(vals, key=lambda n: (vals[n], -list(mem_).index(n)))
        exp_ch.append(pick); mk = (base.fold == f_).values; exp_sc[mk] = mem_[pick].score.values[mk]
    assert [c["member"] for c in ch_] == exp_ch and np.array_equal(comp_.score.values, exp_sc), "walk-forward != brute force"
    assert [c["eligible_folds"] for c in ch_] == [0, 0, 1, 1, 2, 3, 4] and ch_[0]["member"] == "m_a" and len(set(exp_ch)) > 1, "walk-forward dummy does not exercise the rule"
    print("walk-forward: chosen members", exp_ch, "- composite and choices equal the brute-force recomputation on 3 dummy members")
    # ---- null control v4: an ARTIST-CONSTANT random scorer must PASS under the cluster-aware band in >= 9 of 10 dummy runs (the song-level band is printed for comparison)
    Tn_rows = T.reset_index(drop=True); BT = metrics.Block(Tn_rows, "love", 2, 0); BTn = BT.sub(BT.new); au = pd.factorize(Tn_rows.artist.values)[0]; npass = 0; nsong = 0
    for rep_ in range(10):
        r_ = np.random.default_rng(100 + rep_); seeds_ = [r_.random(au.max() + 1)[au] for _ in range(5)]   # 5 'null seeds' of an artist-constant scorer (a constant per artist in every fold)
        vals_, cb_, inside_, avg_ = run.null_avg_stats(BT, BTn, Tn_rows, seeds_); npass += all(inside_)
        sb_ = metrics.permutation_band(Tn_rows, nperm=40, nmean=5, seed=rep_); nsong += all(sb_[k][0] <= v <= sb_[k][1] for k, v in zip(("sauc", "wa", "new"), vals_))
    print(f"artist-constant random scorer: PASS under the cluster-aware band in {npass}/10 dummy runs (song-level band for comparison: {nsong}/10)")
    assert npass >= 9, "artist-constant scorer FLAGs under the cluster-aware band"
    blocks_ = metrics.artist_blocks(BT.fold, Tn_rows.artist.values); yp_ = metrics.permute_artist_blocks(BT.y, blocks_, np.random.default_rng(0))
    assert yp_.sum() == BT.y.sum() and all(yp_[BT.fold == f_].sum() == BT.y[BT.fold == f_].sum() for f_ in np.unique(BT.fold)), "block permutation must keep the number of loved rows per fold"
    # ---- evalkit.refs: identity guard (strong key sees a row permutation that the references' own sum-keys do not), regeneration of missing caches from a build script
    Fk = P[3]; trk = Fk["train"]; t2_ = trk.copy(); perm_ = np.random.default_rng(0).permutation(len(t2_))
    for col in ("trackId", "song", "artist"): t2_[col] = t2_[col].values[perm_]
    assert refs.train_key(trk, Fk["c"]) != refs.train_key(t2_, Fk["c"]), "refs key is blind to a permutation of identities among rows"
    os.environ["EVALKIT_NULL_SEED"] = "1"; k_seed = refs.train_key(trk, Fk["c"]); del os.environ["EVALKIT_NULL_SEED"]; assert k_seed != refs.train_key(trk, Fk["c"]), "refs key ignores the null seed"
    out_ = tmp / "gen" / "out.npz"; scr_ = tmp / "build.py"; scr_.write_text(f"import numpy as np\nnp.savez('{out_}', a=np.arange(3))\n"); refs.REFS["tmp_ref"] = (scr_, "x", [(out_, scr_)]); refs.ensure("tmp_ref"); assert out_.exists(); del refs.REFS["tmp_ref"]
    for nm in refs.REFS:
        for outp, scr in refs.REFS[nm][2]: assert pathlib.Path(outp).exists() and pathlib.Path(scr).exists(), f"{nm}: cache or its build script missing"
    ra1 = refs.score("ref_audio_final", trk, Fk["cands"], Fk["meta"], Fk["c"]); ra2 = refs.score("ref_audio_final", trk, Fk["cands"], Fk["meta"])   # cutoff inferred from the train
    assert refs.infer_cutoff(trk) == Fk["c"] and np.array_equal(ra1, ra2) and len(ra1) == len(Fk["cands"]), "refs.score / cutoff inference"
    ra3 = refs.score("ref_audio_final", t2_, Fk["cands"], Fk["meta"], Fk["c"]); assert not np.array_equal(ra1, ra3), "refs reused a fit for a train with permuted identities"
    print("refs: strong identity key sees row permutations and the null seed; missing compact caches are rebuilt from their build scripts; refs.score fits on the given train (permuted identities give other scores)")
    print("v4.1 checks OK")

def _cell(x):
    if isinstance(x, (tuple, list)): return [float(v) for v in x]
    if hasattr(x, "item") and not isinstance(x, str): x = x.item()
    return None if isinstance(x, float) and x != x else x

def _quiet_main(argv):
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): r = run.main(argv)
    return r, buf.getvalue()

def v5_checks(d, P):
    """v5.0 checks (python3 -m evalkit.selftest --v5 runs only these; target < 3 min once the caches exist)."""
    from threadpoolctl import threadpool_limits; threadpool_limits(2)
    import pathlib, time
    from . import folds as fs, inner, holdout_budget
    t0 = time.time(); tmp = pathlib.Path(tempfile.mkdtemp(prefix="evalkit_v5_")); ds = run._dev_streams()
    # ---- fold-set definitions
    want = dict(tune=10, tune_q1=11, tune_q2=11, tune_m=30, tune_h=5, tune_y=3)
    for n, k in want.items():
        w = fs.windows(n); assert len(w) == k, (n, len(w)); assert w[0][0] == pd.Timestamp("2021-07-01") and w[-1][1] == pd.Timestamp("2024-01-01")
        assert all(a < b for a, b in w) and all(w[i][1] == w[i + 1][0] for i in range(len(w) - 1)), f"{n}: windows must be contiguous"
        assert all(b <= pd.Timestamp("2024-01-01") for a, b in w) and not any(a >= pd.Timestamp(data.LATE_CUTOFFS[0]) for a, b in w), f"{n}: a window reaches the LATE era"
    assert [str(a.date()) for a, b in fs.windows("tune")] == data.TUNE_CUTOFFS
    assert [str(b.date()) for a, b in fs.windows("tune_q1")][:3] == ["2021-08-01", "2021-11-01", "2022-02-01"] and [str(b.date()) for a, b in fs.windows("tune_q2")][:3] == ["2021-09-01", "2021-12-01", "2022-03-01"]
    assert [str(a.date()) for a, b in fs.windows("tune_y")] == ["2021-07-01", "2022-07-01", "2023-07-01"] and [str(a.date()) for a, b in fs.windows("tune_h")] == ["2021-07-01", "2022-01-01", "2022-07-01", "2023-01-01", "2023-07-01"]
    try: fs.parse("tune_m,nope"); raise AssertionError("unknown fold set accepted")
    except KeyError: pass
    print("folds: tune 10, tune_q1 11, tune_q2 11, tune_m 30, tune_h 5, tune_y 3 folds; contiguous, inside [2021-07-01, 2024-01-01), tune == the 10 default cutoffs")
    # ---- refusals (checked before any work is done)
    for bad in (["--folds", "tune_m", "--late"], ["--folds", "tune_m", "--holdout", "x.py"], ["--folds", "tune_m", "--sealed"], ["--folds", "tune_m", "--null-control"], ["--dump-scores", "x.pkl", "--late"], ["--dump-scores", "x.pkl", "--holdout", "x.py"],
                ["--dump-scores", "x.pkl", "--sealed"], ["--dump-scores", "x.pkl", "--null-control"], ["--pair-group", "quarter", "--late"], ["--walkforward", "--fast", "--folds", "tune"], ["--walkforward", "--fast", "--folds", "tune_m,tune_h"]):
        try: run.main(bad); raise SystemExit("accepted: " + " ".join(bad))
        except AssertionError: pass
    print("refusals: --folds / --dump-scores / --pair-group quarter with --late / --holdout / --sealed / --null-control; --walkforward needs exactly one non-default set")
    # ---- default run reproduces v4.1: fast TUNE tried_within_group table and VERDICT point values identical to the recorded v4.1 output
    ref = json.load(open(pathlib.Path(__file__).parent / "v41_fast_reference.json")); (sc0, out0), txt0 = _quiet_main(["--fast"]); t_ = out0["TUNE"]
    got = dict(columns=list(t_["tried_within_group"].columns), data=[[_cell(v) for v in r] for r in t_["tried_within_group"].astype(object).values.tolist()])
    assert got == ref["tried_within_group"], "fast TUNE tried_within_group differs from v4.1"
    V = t_["VERDICT"]; vc = ref["verdict_point"]["columns"]; gotv = [[_cell(v) for v in r] for r in V[vc].astype(object).values.tolist()]
    assert gotv == ref["verdict_point"]["data"], "VERDICT point values differ from v4.1"
    assert "evidence80_sauc" in V.columns and "lo80_sauc" in V.columns and f"[{run.VERSION}]" in txt0
    print("default fast run: tried_within_group (20 rows, point values and CIs) and VERDICT point values are identical to the recorded v4.1 output; version label in every table heading")
    # ---- the alternative-fold builder reproduces the default tried rows of the default folds (digest per fold), HOLDOUT artists absent, no row beyond 2024-01-01
    F_alt = run.prepare_alt(["tune_m", "tune_h", "tune_y", "tune_q1", "tune_q2", "tune"]); byc = {F["c"]: F for F in F_alt}
    cols = ["song", "trackId", "albumId", "artist", "is_decoy", "love", "plays90", "rb", "exp_before", "first"]
    for Fd in P[:10]:
        c = Fd["c"]; a = byc[c]["pool"]; a = a[a["first"] < c + pd.DateOffset(months=3)]; b = Fd["pool"]; b = b[b.is_decoy == 0]
        assert len(a) == len(b) and run._pool_digest(a[cols].astype({"exp_before": float})) == run._pool_digest(b[cols]), f"alt builder != default tried rows at {c.date()}"
        assert (a.keep.values[np.argsort(a.song.values)] == b.keep.values[np.argsort(b.song.values)]).all(), "keep differs"
    assert all(not data.is_holdout(F["pool"].artist.values).any() and F["pool"]["first"].max() < pd.Timestamp("2024-01-01") and F["pool"]["first"].min() >= F["c"] and F["train"].t.max() < F["c"] and (F["pool"].is_decoy == 0).all() for F in F_alt)
    assert len(F_alt) == 30 and all(F["pool"].keep.notna().all() for F in F_alt)
    Fm = byc[pd.Timestamp("2022-03-01")]; pm = Fm["pool"][Fm["pool"]["first"] < pd.Timestamp("2022-04-01")]; assert len(pm) > 20   # brute force labels of a monthly fold from the raw dev streams
    for _, r_ in pm.sample(25, random_state=2).iterrows():
        dd = ds[ds.song == r_.song]; assert dd.t.min() == r_["first"] and r_["first"] >= pd.Timestamp("2022-03-01")
        w = dd[dd.t < r_["first"] + pd.Timedelta(days=90)]; nd = w.t.dt.normalize().nunique(); assert len(w) == r_.plays90 and nd == r_.days90 and int(len(w) >= 6 and nd >= 3) == r_.love
    print("alt folds: tried rows of fold set 'tune' equal the default pools' tried rows (digest per fold, 10 folds); 30 monthly cutoffs prepared; labels of 25 monthly-fold songs equal a brute-force recomputation from raw dev streams; no HOLDOUT artist, no first play >= 2024-01-01")
    # ---- one call per distinct cutoff on the union, then split; a pool-independent scorer gives the same scores when a set is scored alone
    calls = []
    def counting(train, cands, meta, cutoff): calls.append(str(cutoff.date())); return ((cands.trackId.values % 1000003) / 1000003.0) + 0.001 * np.array([len(a) for a in cands.artistIds])
    un = run.score_predictor(counting, None, "cnt", 0, None, None, None, "", "main", F_alt); assert len(calls) == 30 == len(set(calls)), "one call per distinct cutoff on the union"
    sh = run.split_alt(un, "tune_h", F_alt); sy = run.split_alt(un, "tune_y", F_alt); assert len(sh) == len(sy) == len(run.split_alt(un, "tune", F_alt)) == len(sc0["popularity"][sc0["popularity"].is_decoy == 0])
    solo = run.prepare_alt(["tune_h"]); us = run.score_predictor(counting, None, "cnt", 0, None, None, None, "", "main", solo); sh2 = run.split_alt(us, "tune_h", solo)
    m_ = sh.merge(sh2, on="trackId", suffixes=("", "_2")); assert len(m_) == len(sh) and np.allclose(m_.score, m_.score_2), "score of a candidate depends on the union"
    print("union scoring: 30 distinct cutoffs for 6 sets -> 30 predictor calls; split sets have identical rows (same tried songs); a pool-independent scorer gives the same scores when the set is scored alone")
    # ---- alternative-fold run with a builder file: score dump, FILE_DELTAS80, --refs none, --pair-group quarter, macro count
    pf = tmp / "pair.py"; pf.write_text("import numpy as np\nfrom evalkit import baselines as B\ndef a(train, cands, meta, cutoff): return B.artist_recent(train, cands, meta, cutoff) + 0.01 * meta.popularity.reindex(cands.trackId).fillna(0).values\n"
                                        "def b(train, cands, meta, cutoff): return B.duration(train, cands, meta, cutoff)\nPREDICTORS = {'mod_a': a, 'mod_b': b}\n")
    dp = tmp / "dump.pkl"; (sc1, out1), txt1 = _quiet_main(["--fast", "--folds", "tune,tune_q1,tune_h", "--refs", "none", "--dump-scores", str(dp), str(pf)])
    dmp = pd.read_pickle(dp); assert set(dmp.fold_set) == {"tune", "tune_q1", "tune_h"} and all(c in dmp.columns for c in ["fold_set", "fold", "cutoff", "month", "artist", "song", "new_artist", "exposure_before", "exposure_after", "replays_s1", "love", "strong", "love_4_2", "love_10_4", "keep", "plays90", "days90", "share90",
        "plays_h30", "days_h30", "plays_h60", "days_h60", "plays_h180", "days_h180", "plays_h365", "days_h365", "score__mod_a", "score__popularity", "score__nonaudio_gbm", "score__exposure_before", "score__oracle_7d"])
    assert "ref_audio_final" not in sc1["tune"] and "FILE_DELTAS80" in txt1 and len(out1["tune"]["FILE_DELTAS80"]) == 1 and "computed among the SCORED references only" in txt1 and "macro_sauc keeps min_each 10" in txt1
    assert (dmp.love == ((dmp.plays90 >= 6) & (dmp.days90 >= 3)).astype(int)).all()
    sub_ = dmp[dmp.fold_set == "tune_q1"].reset_index(drop=True); fr = out1["tune_q1"]["_P"]["mod_a"]; fr = fr[fr.is_decoy == 0].reset_index(drop=True)
    assert (fr.love.values == sub_.love.values).all() and np.allclose(fr.score.values, sub_["score__mod_a"].values)
    for h in run.HORIZONS: assert (sub_[f"plays_h{h}"] >= 1).all() and (sub_[f"plays_h{h}"] <= sub_["plays_h365"]).all() and (sub_[f"days_h{h}"] <= sub_[f"plays_h{h}"]).all()
    pool_ = run.prepare_alt(["tune_q1"]); wq = dict(fs.windows("tune_q1")); up = pd.concat([F["pool"].iloc[F["order"]] for F in pool_]); up = up[up["first"] < up.cutoff.map(wq)]
    h90 = run.horizon_counts(up.set_index("song")["first"], (90,)); assert (h90.plays_h90.values == up.plays90.values).all() and (h90.days_h90.values == up.days90.values).all(), "horizon counts differ from plays90 / days90"
    chk = run.horizon_counts(up.set_index("song")["first"])
    for song, f0 in list(up.set_index("song")["first"].items())[:15]:
        dd = ds[ds.song == song]; assert (dd.t < data.DEV_END).all()
        for h in run.HORIZONS: w = dd[dd.t < f0 + pd.Timedelta(days=h)]; assert chk.loc[song, f"plays_h{h}"] == len(w) and chk.loc[song, f"days_h{h}"] == w.t.dt.normalize().nunique()
    S_ = out1["tune_q1"]["_S"]["mod_a"]["all"]["sauc"][0]; assert abs(metrics.dump_sauc(dmp, "tune_q1", "mod_a", nboot=20)[0] - S_) < 1e-12   # dump_sauc == harness sauc (point); brute force pooled AUC for both groupings
    g_ = metrics.dump_frame(dmp, "tune_q1", "quarter"); assert abs(metrics.dump_sauc(dmp, "tune_q1", "mod_a", "quarter", nboot=20)[0] - br_idx(g_.love.values, g_["score__mod_a"].values, pd.factorize(g_.fold.values)[0])) < 1e-12
    assert abs(S_ - br_idx(sub_.love.values, sub_["score__mod_a"].values, pd.factorize(sub_.fold.values)[0])) < 1e-12
    e_ = metrics.dump_sauc_delta(dmp, "tune_q1", "mod_a", "mod_b", nboot=60); assert e_["lo80"] <= e_["hi80"]
    (sc2, out2), txt2 = _quiet_main(["--fast", "--folds", "tune,tune_q1", "--refs", "none", "--pair-group", "quarter", str(pf)])
    sa1 = lambda o, k: o[k]["tried_within_group"].set_index("model").sauc["mod_a"]
    assert sa1(out2, "tune") == sa1(out1, "tune"), "tune with quarter pairing must equal fold pairing"
    sq = sa1(out2, "tune_q1"); assert abs(sq - metrics.dump_sauc(dmp, "tune_q1", "mod_a", "quarter", nboot=20)[0]) < 1e-3 and sq != sa1(out1, "tune_q1")
    mf = out2["tune_q1"]["_macro_folds"]; assert mf[1] in (10, 11), mf
    print(f"alt run: dump {len(dmp)} rows x {dmp.shape[1]} cols (3 fold sets); horizon counts == plays90 / days90 at 90 d and == raw streams at 30/60/180/365; dump_sauc == harness sauc == brute force (fold and quarter pairing); "
          f"--pair-group quarter: tune == fold pairing, tune_q1 sauc {sq:.4f} != fold pairing {sa1(out1, 'tune_q1'):.4f}; FILE_DELTAS80, --refs none, macro count OK")
    # ---- 80% grade columns
    V = out1["tune"]["VERDICT"].set_index("model"); assert (V["evidence80_sauc"].isin(["TUNE80+", "TUNE80-"])).all() and ((V["lo80_sauc"] > 0) == (V["evidence80_sauc"] == "TUNE80+")).all()
    def fake(lo, d):
        e = {k: dict(d=d, lo95=lo - .02, lo80=lo, hi80=lo + .1, P=.9) for k in run.GRADED_KEYS}; kn = [run.KEY_NAME.get(k, k) for k in run.GRADED_KEYS]
        return dict(VERDICT=pd.DataFrame([dict(model="m", **{f"evidence80_{k}": "" for k in kn}, **{f"evidence_{k}": "" for k in kn})]), _evidence={"m": e})
    o = {"TUNE": fake(.01, .02), "LATE": fake(-.01, .03), "ALL": fake(.01, .02)}; run.finish_verdicts(o, True); assert o["ALL"]["VERDICT"].evidence80_sauc[0] == "SUPPORTED80" and o["TUNE"]["VERDICT"].evidence80_sauc[0] == "see ALL"
    o = {"TUNE": fake(.01, .02), "LATE": fake(-.01, -.03), "ALL": fake(.01, .02)}; run.finish_verdicts(o, True); assert o["ALL"]["VERDICT"].evidence80_wx[0] == "NOT80"
    o = {"TUNE": fake(-.01, .02), "LATE": fake(-.01, .03), "ALL": fake(-.01, .02)}; run.finish_verdicts(o, True); assert o["ALL"]["VERDICT"].evidence80_gc[0] == "NOT80"
    print("80% grade: TUNE80+ / TUNE80- from lo80; with --late SUPPORTED80 needs ALL lo80 > 0 and LATE point delta > 0 (3 synthetic cases)")
    # ---- walk-forward on a non-default set
    (sc3, out3), txt3 = _quiet_main(["--fast", "--folds", "tune_h", "--refs", "none", "--walkforward", str(pf)]); assert "WALK-FORWARD walkforward[" in txt3 and "walkforward[" + pf.parent.name + "]" in sc3["tune_h"]
    print("walk-forward with --folds tune_h: composite scored on the set's own earlier folds")
    # ---- inner folds
    F = P[5]; tr, me, c = F["train"], F["meta"], F["c"]; tr_copy = tr.copy(); real_load = (data._load_all, data.load_streams)
    def boom(*a, **k): raise AssertionError("inner folds touched raw data")
    data._load_all = boom; data.load_streams = boom
    try: fl = inner.make_inner_folds(tr, me, c)
    finally: data._load_all, data.load_streams = real_load
    assert tr.equals(tr_copy) and len(fl) >= 3, "train mutated / too few inner folds"
    dtab = data.song_table(d[d.t < data.DEV_END]); dtab = dtab.assign(anon=data.anon_song(pd.Series(dtab.index, index=dtab.index)).values).set_index("anon"); songs_tr = set(tr.song)
    for f in fl:
        ic = f["inner_cutoff"]; assert f["train_streams"].t.max() < ic and ic + pd.DateOffset(months=3) + pd.Timedelta(days=90) <= c and len(f["cands"]) >= 20 and len(f["cands"]) == len(f["labels"])
        assert set(f["cands"].song) <= songs_tr and list(f["cands"].columns) == list(F["cands"].columns), "inner cands: songs outside train / columns differ from the harness cands"
        assert not set(f["cands"].song) & set(f["train_streams"].song), "an inner candidate was played before the inner cutoff"
        lab = dtab.loc[f["cands"].song.values]; assert (lab[["love", "plays90", "days90"]].values == f["labels"][["love", "plays90", "days90"]].values).all() and np.allclose(lab.share90.values, f["labels"].share90.values), "inner labels != harness labels from raw dev data"
        assert (lab["first"].values >= np.datetime64(ic)).all() and (lab["first"].values < np.datetime64(ic + pd.DateOffset(months=3))).all()
    sv = [np.random.default_rng(i).random(len(f["cands"])) for i, f in enumerate(fl)]; ia = inner.inner_sauc(sv, fl); yy = np.concatenate([f["labels"].love.values for f in fl]); gg = np.concatenate([np.full(len(f["cands"]), i) for i, f in enumerate(fl)])
    assert abs(ia - br_idx(yy, np.concatenate(sv), gg)) < 1e-12; a2, lo2, hi2 = inner.inner_sauc(sv, fl, nboot=40); assert abs(a2 - ia) < 1e-12 and lo2 <= hi2
    fl2 = inner.make_inner_folds(tr, me, c, n_folds=2, spacing_months=2, horizon_days=60, min_tried=5); assert len(fl2) == 2 and fl2[0]["inner_cutoff"] + pd.DateOffset(months=2) + pd.Timedelta(days=60) <= c
    print(f"inner folds: {len(fl)} folds (sizes {[len(f['cands']) for f in fl]}); only the given train is touched (raw loaders disabled during the call, train unchanged); labels equal the harness labels from raw dev data; inner_sauc == brute force; parameters vary the geometry")
    ip = tmp / "inner_pred.py"; ip.write_text("import numpy as np\nfrom evalkit import inner, baselines as B\ndef predict(train, cands, meta, cutoff):\n    fl = inner.make_inner_folds(train, meta, cutoff, n_folds=2)\n    best = max((30.0, 400.0), key=lambda h: inner.inner_sauc([B._artist_score(f['train_streams'], f['cands'], f['inner_cutoff'], h) for f in fl], fl))\n    return B._artist_score(train, cands, cutoff, best)\n")
    spec = __import__("importlib.util").util.spec_from_file_location("inner_pred", ip); im = __import__("importlib.util").util.module_from_spec(spec); spec.loader.exec_module(im)
    r_ = run.score_predictor(im.predict, None, "innerp", 4, None, None, None, "all", "main", [F]); assert r_.attrs["indep_p90"] < 1e-9, f"inner-fold predictor fails the independence check: {r_.attrs['indep_p90']}"
    rn = run.score_predictor(im.predict, None, "innerp", 0, ("v2", 0), None, None, "all", "main", [F]); assert np.isfinite(rn.score.values).all()
    tn, am, bm = run._null_control(tr, F["cands"], np.random.default_rng(5)); mn = run._null_meta(me, tr, F["cands"], tn, am, bm); fn_ = inner.make_inner_folds(tn, mn, c); stn = data.song_table(tn)
    assert len(fn_) >= 2 and all(np.array_equal(f["labels"].love.values, stn.loc[f["cands"].song.values].love.values) for f in fn_), "under the null control the inner labels must come from the null train"
    print("inner folds: a predictor choosing its config with evalkit.inner passes the independence check (p90 %.1e) and runs under the null control (inner labels from the null train: %d folds)" % (r_.attrs["indep_p90"], len(fn_)))
    # ---- HOLDOUT budget module
    bj = tmp / "b.json"; assert holdout_budget.write("x1", 3, bj)["remaining"] == 3
    try: holdout_budget.write("x1", 3, bj); raise AssertionError("same round overwritten")
    except SystemExit as e: assert "REFUSED" in str(e)
    assert holdout_budget.write("x2", 2, bj) == dict(round="x2", remaining=2)
    live = json.load(open(run.HOLDOUT_BUDGET)); assert live["round"] == "w5r1" and 0 <= live["remaining"] <= 3, live
    print(f"holdout budget module: writes, refuses to reset the same round, replaces another round; live budget file: {live}")
    print(f"v5.0 checks OK ({time.time() - t0:.0f}s)")

_V51 = {}
def _pt(x): return float(x.split()[0][2:])   # "d=+0.118 80%[..." -> 0.118

def v51_checks():
    """v5.1 checks (python3 -m evalkit.selftest --v51; target < 3 min once the caches exist). No raw-stream access: everything goes through the harness runs."""
    from threadpoolctl import threadpool_limits; threadpool_limits(2)
    import pathlib, time
    from sklearn.metrics import roc_auc_score
    t0 = time.time(); here = pathlib.Path(__file__).parent; B = str(here / "selftest_builder.py"); tmp = pathlib.Path(tempfile.mkdtemp(prefix="evalkit_v51_"))
    assert run.VERSION in ("v5.1", "v5.2", "v5.3")
    # ---- refusals
    live = json.load(open(run.HOLDOUT_BUDGET)); assert live == dict(round="w5r1", remaining=0), f"no new HOLDOUT budget in round w5r2: {live}"
    for bad in (["--best-ref", "artist_recent", "--late"], ["--best-ref", "artist_recent", "--holdout", B], ["--best-ref", "artist_recent", "--sealed"], ["--best-ref", "artist_recent", "--null-control"], ["--best-ref", "nope", "--fast"]):
        try: run.main(bad); raise SystemExit("accepted: " + " ".join(bad))
        except AssertionError: pass
    try: run.main(["--holdout", B]); raise SystemExit("--holdout was not refused")
    except SystemExit as e: assert "REFUSED" in str(e), e
    print("refusals: --best-ref with --late / --holdout / --sealed / --null-control or an unknown name; --holdout refused for the builder file (budget file round w5r1, remaining 0, unchanged)")
    # ---- default run reproduces v5.0 (fast TUNE; baselines only and with the three-model test builder)
    ref = json.load(open(here / "v50_fast_reference.json")); chk = lambda t_, r_, tag: (
        _eq([[_cell(v) for v in r] for r in t_["tried_within_group"].astype(object).values.tolist()], r_["tried_within_group"]["data"], tag + " tried_within_group"),
        _eq([[_cell(v) for v in r] for r in t_["VERDICT"][r_["verdict_point"]["columns"]].astype(object).values.tolist()], r_["verdict_point"]["data"], tag + " VERDICT"))
    (_, o0), tx0 = _quiet_main(["--fast"]); chk(o0["TUNE"], ref, "baselines only")
    (_, o1), tx1 = _quiet_main(["--fast", B]); _V51.update(o1=o1, tx1=tx1, tx0=tx0); chk(o1["TUNE"], ref["builder"], "builder"); t1 = o1["TUNE"]; fd = t1["FILE_DELTAS80"]
    assert [[r.model_a, r.minus_model_b, f"d={_pt(r.sauc):+.3f}"] for r in fd.itertuples()] == ref["builder"]["file_deltas80_point"], "FILE_DELTAS80 point deltas differ from v5.0"
    assert "decision80" in fd.columns and set(fd.decision80) <= {"POS", "NEG", "UNDECIDED"} and "FOLD_META" in t1 and len(t1["FOLD_META"]) == 6 and "TUNE FOLD_META" in tx1 and "decision80_margin005" in tx1
    for r in fd.itertuples():   # decision80 follows the sauc interval
        lo, hi = [float(v) for v in r.sauc.split("80%[")[1].split("]")[0].split(",")]; assert r.decision80 == ("POS" if lo > 0 else "NEG" if hi < 0 else "UNDECIDED") and r.decision80_margin005 == ("POS" if lo > .005 else "NEG" if hi < -.005 else "UNDECIDED"), r   # v5.2: plain 80% rule + margin column
    (_, o1b), _ = _quiet_main(["--fast", "--nboot", "60", B]); assert o1b["TUNE"]["FILE_DELTAS80"].astype(str).equals(fd.astype(str)), "FILE_DELTAS80 must not depend on --nboot (1000 resamples, fixed seed)"
    print("default fast run: tried_within_group and VERDICT point values identical to the recorded v5.0 output (baselines only, and with the test builder); FILE_DELTAS80 point deltas identical, decision80 present and consistent, "
          "independent of --nboot; FOLD_META printed (6 rows: 3 models x best_ref, artist_recent)")
    # ---- alternative sets with a fixed reference, fixed comparator, dump
    dp = tmp / "d.pkl"; (_, o2), tx2 = _quiet_main(["--fast", "--folds", "tune,tune_h", "--best-ref", "artist_recent", "--dump-scores", str(dp), B])
    assert "FIXED by --best-ref" in tx2 and set(o2) == {"tune", "tune_h"}
    for sn, t_ in o2.items():
        assert (t_["VERDICT"].best_ref == "artist_recent").all() and "FIXED COMPARATOR" in tx2 and list(t_["FIXED_COMPARATOR"].model) == ["sb_dur", "sb_rand_a", "sb_rand_b"] and (t_["FIXED_COMPARATOR"].vs == "ref_w4r1_listening").all()
        assert set(t_["FOLD_META"].vs) == {"artist_recent (best_ref, fixed by --best-ref)"}, set(t_["FOLD_META"].vs)   # artist_recent is the fixed reference: the duplicate comparators are dropped
    for sn, t_ in o2.items(): fdx = t_["FILE_DELTAS80"]; assert len(fdx) == 6 and list(fdx.minus_model_b[3:]) == ["artist_recent"] * 3 and set(fdx.decision80) <= {"POS", "NEG", "UNDECIDED"}, fdx
    (_, o3), tx3 = _quiet_main(["--fast", "--folds", "tune_h", "--best-ref", "ref_w4r1_music", B])
    assert set(o3["tune_h"]["FOLD_META"].vs) == {"ref_w4r1_music (best_ref, fixed by --best-ref)", "artist_recent"} and (o3["tune_h"]["VERDICT"].best_ref == "ref_w4r1_music").all()
    print("--folds with --best-ref: VERDICT / FOLD_META use the fixed reference in every set; the FIXED COMPARATOR table (vs ref_w4r1_listening) is printed for every alternative set")
    # ---- dump: fold_set 'tune' rows, first_play_date
    dmp = pd.read_pickle(dp); assert set(dmp.fold_set) == {"tune", "tune_h"} and (dmp.fold_set == "tune").sum() > 0 and "first_play_date" in dmp.columns
    assert (dmp.first_play_date.str[:7] == dmp.month).all() and dmp.first_play_date.str.len().eq(10).all() and (pd.to_datetime(dmp.first_play_date) < pd.Timestamp("2024-01-01")).all()
    tn = dmp[dmp.fold_set == "tune"]; assert sorted(tn.fold.unique()) == data.TUNE_CUTOFFS
    print("dump: a --folds run including 'tune' labels those rows fold_set='tune' (10 default cutoffs); column first_play_date (YYYY-MM-DD) agrees with month and is before 2024-01-01")
    # ---- fold_meta against brute force
    for fs_ in ("tune", "tune_h"):
        r = metrics.fold_meta(dmp, fs_, "sb_dur", "sb_rand_a"); g = dmp[dmp.fold_set == fs_]; exp = {}
        for f, h in g.groupby("fold"):
            y = h.love.values.astype(int)
            if y.sum() >= 5 and (1 - y).sum() >= 5: exp[f] = roc_auc_score(y, h["score__sb_dur"].values) - roc_auc_score(y, h["score__sb_rand_a"].values)
        T_ = r["table"]; assert set(T_.fold) == set(exp) and r["n_excluded"] == g.fold.nunique() - len(exp), (fs_, r["n_excluded"])
        assert all(abs(row.delta - exp[row.fold]) < 1e-12 for row in T_.itertuples()), "fold_meta deltas differ from sklearn AUC differences"
        w = 1 / T_.se.values ** 2; assert abs(r["mean"] - (w * T_.delta.values).sum() / w.sum()) < 1e-12 and abs(r["se"] - w.sum() ** -.5) < 1e-12 and abs(r["hi80"] - r["lo80"] - 2 * metrics.Z80 * r["se"]) < 1e-12
        r2 = metrics.fold_meta(dmp, fs_, "sb_dur", "sb_rand_a", seed=5); assert (np.abs(r2["table"].se.values / T_.se.values - 1) < .5).all() and np.allclose(r2["table"].delta, T_.delta)
    # exclusion rule on a synthetic fold set, homogeneous case Q ~ df
    rng = np.random.default_rng(3); rows = []
    for k in range(14):
        n = 400 if k < 12 else 40; y = (rng.random(n) < (.3 if k < 12 else .05)).astype(int); a = rng.integers(0, 80, n); sa = y * .8 + rng.normal(0, 1, n); sb = y * .3 + rng.normal(0, 1, n)
        rows.append(pd.DataFrame(dict(fold_set="syn", fold=f"{2021 + k // 4}-{(k % 4) * 3 + 1:02d}-01", artist=a, love=y, score__a=sa, score__b=sb)))
    syn = pd.concat(rows, ignore_index=True); rs = metrics.fold_meta(syn, "syn", "a", "b", nboot=300); assert rs["n_excluded"] == 2 and rs["k"] == 12 and rs["df"] == 11
    assert 0.2 < rs["Q"] / rs["df"] < 2.5 and rs["p"] > 0.01, (rs["Q"], rs["df"]); assert rs["mean"] > 0.1 and abs(rs["trend"]) < 4 * rs["trend_se"]
    Qs = [metrics.iv_meta(rng.normal(.02, .03, 12), np.full(12, .03))["Q"] for _ in range(1500)]; assert abs(np.mean(Qs) / 11 - 1) < .06, np.mean(Qs)
    print(f"fold_meta: per-fold deltas equal sklearn AUC differences (< 1e-12) on both dump fold sets, IV mean / SE / 80% interval recomputed by hand; folds with < 5 positives excluded and counted; homogeneous synthetic case Q/df = {rs['Q'] / rs['df']:.2f} "
          f"(mean over 1500 simulated homogeneous sets {np.mean(Qs) / 11:.2f})")
    print(f"v5.1 checks OK ({time.time() - t0:.0f}s)")

def v52_checks():
    """v5.2 checks (python3 -m evalkit.selftest --v52; also run in the full selftest). Runs v51_checks first (a default run without new flags reproduces the recorded v5.0 / v5.1 numbers), then the v5.2 additions."""
    from threadpoolctl import threadpool_limits; threadpool_limits(2)
    import pathlib, time, stat
    from sklearn.metrics import roc_auc_score
    from . import cmpset, declare, sanity
    t0 = time.time(); here = pathlib.Path(__file__).parent; B = str(here / "selftest_builder.py"); tmp = pathlib.Path(tempfile.mkdtemp(prefix="evalkit_v52_"))
    assert run.VERSION in ("v5.2", "v5.3")
    v51_checks()   # includes: --holdout refused (budget file untouched), --best-ref refusals, default fast run == v5.0 reference (tried_within_group, VERDICT, FILE_DELTAS80 point values)
    o1, tx1 = _V51["o1"], _V51["tx1"]; print("default_output_unchanged: the default --fast run (baselines only and with the test builder) equals the recorded v5.0 / v5.1 output (v51_checks above)")
    # ---- plain 80% rule
    assert [cmpset.plain80(*x) for x in ((0.001, 0.05), (-0.02, 0.03), (-0.05, -0.0001), (0.0, 0.04), (-0.04, 0.0))] == ["POS", "UNDECIDED", "NEG", "UNDECIDED", "UNDECIDED"]
    assert cmpset.margin005(0.003, 0.05) == "UNDECIDED" and cmpset.plain80(0.003, 0.05) == "POS" and run.decision80 is cmpset.plain80
    t1 = o1["TUNE"]; fd = t1["FILE_DELTAS80"]; cols = list(fd.columns); assert cols[-1] == "decision80_margin005" and cols.index("decision80") < cols.index("decision80_margin005")
    cs = t1["COMPARATOR_SET"]; assert list(cs.columns)[-1] == "decision80_margin005" and list(cs.columns)[3] == "decision80"
    print("plain_80_rule: decision80 = POS if lo80 > 0, NEG if hi80 < 0 else UNDECIDED in FILE_DELTAS80, FIXED_COMPARATOR and COMPARATOR_SET; the 0.005-margin label is the last column decision80_margin005")
    # ---- COMPARATOR_SET in a default --fast run
    assert run.COMPARATORS == ("artist_recent", "ref_w4r1_listening") and len(cs) == 6 and set(cs.vs) == set(run.COMPARATORS) and "COMPARATOR_SET" in tx1 and "heaviest folds left out" in tx1
    for r in cs.itertuples():
        for col, dec in (("pooled", r.decision80), ("iv_weighted", r.decision80_iv), ("heaviest_out", r.decision80_heaviest_out)):
            lo, hi = [float(v) for v in getattr(r, col).split("80%[")[1].split("]")[0].split(",")]; assert dec == ("POS" if lo > 0 else "NEG" if hi < 0 else "UNDECIDED"), (col, r)
        assert len(r.folds_left_out.split(",")) == 2 and r.iv_folds.endswith("/10"), r   # 10 TUNE folds -> the 2 heaviest left out
    print("comparator_in_default_runs: the default --fast run prints COMPARATOR_SET (3 builder models x artist_recent, ref_w4r1_listening) with pooled, inverse-variance and heaviest-folds-out differences and plain labels")
    # ---- numbers against brute force on a synthetic scored set (K=10 folds, two heavy ones)
    rng = np.random.default_rng(11); K = 10; rows = []
    for k in range(K):
        n = 900 if k in (1, 6) else 300; y = (rng.random(n) < .3).astype(int)
        rows.append(pd.DataFrame(dict(fold=f"2021-{k + 1:02d}-01", trackId=np.arange(n) + 10000 * k, artist=rng.integers(0, 80, n), new_artist=rng.random(n) < .5, is_decoy=0, love=y, plays90=rng.integers(1, 9, n),
                                      exp_before=rng.integers(0, 12, n).astype(float), week=rng.integers(0, 30, n), sess=rng.integers(0, 90, n))))
    base = pd.concat(rows, ignore_index=True); yv = base.love.values; fr = {nm_: base.assign(score=yv * sh + rng.normal(0, 1, len(base))) for nm_, sh in (("m", .9), ("c1", .3), ("c2", 0.))}
    assert cmpset.heaviest_folds(base) == ["2021-02-01", "2021-07-01"], cmpset.heaviest_folds(base)
    num, pr = cmpset.comparator_table(fr, list(pd.unique(base.fold)), "syn", ["c1", "c2"], ["m"], nboot=60, seed=3, nboot_fold=60); assert len(num) == 2 and len(pr) == 2
    sanity.assert_no_nan(num.drop(columns=["dropped"]), "synthetic COMPARATOR_SET"); sanity.assert_no_nan(pr, "printable COMPARATOR_SET")
    def pooled(sub, a, b):
        def one(s):
            return sum(roc_auc_score(g.love, s[g.index]) * g.love.sum() * (len(g) - g.love.sum()) for _, g in sub.groupby("fold")) / sum(g.love.sum() * (len(g) - g.love.sum()) for _, g in sub.groupby("fold"))
        return one(fr[a].score.loc[sub.index]) - one(fr[b].score.loc[sub.index])
    for r in num.itertuples():
        assert abs(r.d - pooled(base, "m", r.vs)) < 1e-9 and abs(r.drop_d - pooled(base[~base.fold.isin(["2021-02-01", "2021-07-01"])], "m", r.vs)) < 1e-9, "pooled / heaviest-out point difference != brute force"
        dmp = pd.DataFrame(dict(fold_set="syn", fold=base.fold, artist=base.artist, love=base.love, score__m=fr["m"].score, **{"score__" + r.vs: fr[r.vs].score})); fm = metrics.fold_meta(dmp, "syn", "m", r.vs, nboot=60, seed=0)
        assert abs(r.iv_d - fm["mean"]) < 1e-12 and r.iv_folds == 10
    print("fold_weight_sensitivity: pooled and heaviest-folds-out point differences equal a brute-force pooled AUC difference (< 1e-9); inverse-variance mean equals metrics.fold_meta; the two heaviest folds (most pairs) are the ones left out")
    # ---- single-model file: FILE_DELTAS80 now has rows (vs the comparator set)
    one = tmp / "one_model.py"; one.write_text("import numpy as np\nfrom evalkit import baselines as B\ndef predict(train, cands, meta, cutoff): return B.duration(train, cands, meta, cutoff)\n")
    ld = tmp / "logs"; (_, o2), tx2 = _quiet_main(["--fast", "--log-dir", str(ld), str(one)]); f2 = o2["TUNE"]["FILE_DELTAS80"]
    assert list(f2.model_a) == ["one_model"] * 2 and list(f2.minus_model_b) == list(run.COMPARATORS) and set(f2.decision80) <= {"POS", "NEG", "UNDECIDED"}, f2
    # ---- declarations: UNDECLARED first, then declared; the run log is append-only, mode 444; a declaration cannot be overwritten
    assert "UNDECLARED" in tx2 and "declaration check:" in tx2
    dd = ld / "declarations"; rec = declare.declare("selftest-one", [str(one)], str(dd)); p_ = dd / "selftest-one.json"; assert oct(os.stat(p_).st_mode & 0o777) == "0o444" and rec["files"][str(one.resolve())] == declare.sha(str(one))
    try: declare.declare("selftest-one", [str(one)], str(dd)); raise SystemExit("declaration overwritten")
    except SystemExit as e: assert "REFUSED" in str(e), e
    assert declare.status(str(one), str(dd))["status"] == "DECLARED"; one2 = tmp / "one_model2.py"; one2.write_text(one.read_text() + "\n# edited\n"); assert declare.status(str(one2), str(dd))["status"] == "UNDECLARED"
    one.write_text(one.read_text() + "\n# edited after declaration\n"); s_ = declare.status(str(one), str(dd)); assert s_["status"] == "UNDECLARED" and "different hash" in s_["note"], s_
    one.write_text(one.read_text().replace("\n# edited after declaration\n", ""))   # restore
    (_, o3), tx3 = _quiet_main(["--fast", "--log-dir", str(ld), str(one)]); assert "DECLARED selftest-one" in tx3 and "UNDECLARED" not in tx3.split("declaration check:")[1].split("\n")[0]
    lg = [json.loads(l) for l in open(ld / "run_log.jsonl")]; assert len(lg) == 2 and [x["files"][0]["status"] for x in lg] == ["UNDECLARED", "DECLARED"] and lg[1]["files"][0]["declaration"] == "selftest-one" and lg[0]["utc"].endswith("Z") and lg[0]["version"] == "v5.2"
    assert oct(os.stat(ld / "run_log.jsonl").st_mode & 0o777) == "0o444"
    print("single_model_file_deltas: a file with one model prints FILE_DELTAS80 rows vs artist_recent and ref_w4r1_listening; declaration_hashing: UNDECLARED -> DECLARED after python -m evalkit.declare, overwrite refused, edited file reported, run log (UTC time, hashes) append-only mode 444")
    # ---- alternative sets print COMPARATOR_SET too (same comparators)
    (_, o4), tx4 = _quiet_main(["--fast", "--log-dir", str(ld), "--folds", "tune_h", str(one)]); c4 = o4["tune_h"]["COMPARATOR_SET"]; assert set(c4.vs) == set(run.COMPARATORS) and len(c4) == 2 and len(c4.folds_left_out.iloc[0].split(",")) == 1
    # ---- output sanity helpers
    ok = pd.DataFrame(dict(fold=list("abc"), v=[.1, .2, .3])); sanity.assert_table(ok, "ok", 3)
    for bad, kw in ((ok.assign(v=[.1, np.nan, .3]), dict(fold_set=3)), (ok, dict(fold_set=4)), (ok.assign(v=[.1, np.inf, .3]), {})):
        try: sanity.assert_table(bad, "bad", **kw); raise SystemExit("sanity helper accepted a bad table")
        except AssertionError: pass
    assert sanity.expected_folds("tune") == 10 and sanity.expected_folds("late") == 4 and sanity.expected_folds("dev") == 14 and sanity.expected_folds("tune_m") == 30 and sanity.expected_folds("tune_h") == 5
    sanity.assert_fold_count(pd.DataFrame(dict(fold=data.TUNE_CUTOFFS)), "tune")
    print("output_sanity_helpers: assert_no_nan / assert_fold_count / assert_table refuse NaN, inf and a wrong fold count; expected counts tune 10, late 4, dev 14, tune_m 30, tune_h 5")
    # ---- null control line: synthetic table -> one JSON line per model, gated values and bands
    tb = pd.DataFrame([dict(slice="TUNE", model="m1", avg_sauc=.52, avg_wa=.5, avg_new=.51, cluster_band_sauc=(.45, .55), cluster_band_wa=(.46, .54), cluster_band_new=(.44, .56), label="PASS"),
                       dict(slice="TUNE", model="m2", avg_sauc=.60, avg_wa=.5, avg_new=.51, cluster_band_sauc=(.45, .55), cluster_band_wa=(.46, .54), cluster_band_new=(.44, .56), label="FLAG")])
    ls = run.null_lines(tb, "v2", 5); assert len(ls) == 2 and all("\n" not in x and x.startswith("NULLCTRL {") for x in ls)
    j = [json.loads(x[len("NULLCTRL "):]) for x in ls]; assert j[0]["label"] == "PASS" and j[1]["label"] == "FLAG" and j[1]["gated"]["sauc"]["inside"] is False and j[0]["gated"]["wa"]["band"] == [.46, .54] and j[0]["version"] == "v5.2"
    # ---- three null seeds give three different results (fit / feature caches keyed on seed and relabelled identities); in-process, first TUNE fold, baseline artist_recent
    from . import baselines as bl
    F = run.prepare_folds(data.TUNE_CUTOFFS[:1])[0]; sc = []; keys = []
    for k in range(3):
        os.environ["EVALKIT_NULL_SEED"] = str(k)
        try:
            tr, am, bm = run._null_control(F["train"], F["cands"], np.random.default_rng(int(F["c"].strftime("%Y%m%d")) + k), relabel=True); keys.append(bl._train_key("artist_recent", tr, F["c"]))
            sc.append(np.asarray(bl.BASELINES["artist_recent"](tr.copy(), F["cands"], run._null_meta(F["meta"], F["train"], F["cands"], tr, am, bm), F["c"]), float))
        finally: del os.environ["EVALKIT_NULL_SEED"]
    assert len(set(keys)) == 3 and all(not np.array_equal(sc[i], sc[j_]) for i in range(3) for j_ in range(i + 1, 3)), "null seeds must give different fit keys and different scores"
    print("null seeds: 3 null seeds (seed-keyed fit cache, relabelled identities) give 3 different fit keys and 3 different artist_recent score vectors; NULLCTRL line format checked on a synthetic table")
    print(f"v5.2 checks OK ({time.time() - t0:.0f}s)")

def _eq(a, b, what): assert a == b, f"{what} differs from the recorded v5.0 output"

if __name__ == "__main__": main()
