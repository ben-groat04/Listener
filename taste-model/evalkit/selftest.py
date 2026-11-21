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
    if "--v41" in sys.argv: P_ = run.prepare_folds(data.DEV_CUTOFFS); v41_checks(data._load_all(), P_, _tune_tried(P_)); return
    if "--v5" in sys.argv: P_ = run.prepare_folds(data.DEV_CUTOFFS); v5_checks(data._load_all(), P_); return
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

if __name__ == "__main__": main()
