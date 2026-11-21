"""Heterogeneity, equal-weight vs pooled vs IV, trend: global artist-cluster bootstrap of per-fold AUCs (keeps cross-fold artist correlation).
usage: python a3_weighting.py [dump] ; output results/a3_<tag>.csv"""
import sys; sys.path.insert(0, ".")
from lib import *
import lib
from scipy.stats import chi2
NB = 400; MIN = 5
dump = sys.argv[1] if len(sys.argv) > 1 else lib.DUMP; tag = sys.argv[2] if len(sys.argv) > 2 else "main"
lib.DUMP = dump
SETS = sys.argv[3].split(",") if len(sys.argv) > 3 else ["tune", "tune_q1", "tune_q2", "tune_h", "tune_m"]
PAIRS = [("pair_z", "artist_recent"), ("ref_w4r1_listening", "artist_recent"), ("ref_w4r1_music", "artist_recent"), ("ref_audio_final", "artist_recent"),
         ("ref_w4r1_listening", "ref_w4r1_music"), ("ref_w4r1_listening", "ref_audio_final"), ("ref_w4r1_music", "ref_audio_final"), ("pair_z", "ref_w4r1_listening"), ("pair_z", "ref_w4r1_music"),
         ("pairz_trunc12", "artist_recent"), ("pairz_trunc12", "pair_z"), ("pairz_trunc12", "ref_w4r1_listening"), ("pairz_trunc12", "ref_w4r1_music")]
PAIRS = [p for p in PAIRS if p[0] in MODELS and p[1] in MODELS]
rows = []
def fold_aucs(dd, cols, folds):
    """returns (F, M) AUC, (F,) npos, nneg, U-parts"""
    A = np.full((len(folds), len(cols)), np.nan); N1 = np.zeros(len(folds)); N0 = np.zeros(len(folds))
    for i, f in enumerate(folds):
        m = (dd.fold.values == f); y = dd.love.values[m]; n1 = y.sum(); n0 = len(y) - n1; N1[i] = n1; N0[i] = n0
        if n1 == 0 or n0 == 0: continue
        for j, c in enumerate(cols):
            r = rankdata(dd[c].values[m]); A[i, j] = (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    return A, N1, N0
for fs in SETS:
    d = load(fs); d = d.copy()
    DROP = int(os.environ.get("W5R2_DROPFIRST", "0"))
    if DROP: d = d[d.fold.isin(sorted(d.fold.unique())[DROP:])].reset_index(drop=True)   # drop the first DROP folds (earliest cutoffs)
    folds = sorted(d.fold.unique()); cuts = pd.to_datetime(d.groupby("fold").cutoff.first().reindex(folds)).values
    xyr = (cuts.astype("datetime64[D]").astype(float) / 365.25)
    cols = ["score__" + m for m in MODELS]; rng = np.random.default_rng(7)
    A0, P0, N0_ = fold_aucs(d, cols, folds); elig = (P0 >= MIN) & (N0_ >= MIN)
    Bs = []; Ns = []
    for b in range(NB):
        dd = d.iloc[artist_resample(d, rng)].reset_index(drop=True); A, p1, p0 = fold_aucs(dd, cols, folds); Bs.append(A); Ns.append(p1 * p0)
    Bs = np.array(Bs); Ns = np.array(Ns)   # (B,F,M), (B,F)
    for a, b_ in PAIRS:
        ia, ib = MODELS.index(a), MODELS.index(b_)
        D0 = A0[:, ia] - A0[:, ib]; DB = Bs[:, :, ia] - Bs[:, :, ib]
        ok = elig & np.isfinite(DB).all(0)
        se = DB[:, ok].std(0, ddof=1); w = 1 / se ** 2; x = xyr[ok]; d0 = D0[ok]
        def stats(dv, npairs):
            pooled = (dv * npairs).sum() / npairs.sum(); ew = dv.mean(); iv = (w * dv).sum() / w.sum()
            m = iv; Q = (w * (dv - m) ** 2).sum()
            xb = (w * x).sum() / w.sum(); tr = (w * (x - xb) * dv).sum() / (w * (x - xb) ** 2).sum()
            return pooled, ew, iv, Q, tr
        pairs0 = (P0 * N0_)[ok]; o = stats(d0, pairs0)
        BB = np.array([stats(DB[i, ok], Ns[i, ok]) for i in range(NB)])
        # bootstrap null for Q: recentre bootstrap deltas at common IV mean
        mu = o[2]; Qn = []
        for i in range(NB):
            dv = DB[i, ok] - D0[ok] + mu; Qn.append((w * (dv - (w * dv).sum() / w.sum()) ** 2).sum())
        pQ_boot = float(np.mean(np.array(Qn) >= o[3])); df = ok.sum() - 1
        # analytic Q power at tau = 0.03 (simulated, 20% level)
        sim = np.random.default_rng(1); pw = []
        for lvl in (0.2,):
            crit = chi2.ppf(1 - lvl, df); cnt = 0
            for _ in range(2000):
                dv = sim.normal(0, np.sqrt(se ** 2 + 0.03 ** 2)); cnt += (w * (dv - (w * dv).sum() / w.sum()) ** 2).sum() > crit
            pw.append(cnt / 2000)
        diff = BB[:, 1] - BB[:, 0]; diff_iv = BB[:, 2] - BB[:, 0]
        rows.append(dict(fold_set=fs, a=a, b=b_, k=int(ok.sum()), pooled=o[0], ew=o[1], iv=o[2], pooled_lo80=np.percentile(BB[:, 0], 10), pooled_hi80=np.percentile(BB[:, 0], 90),
                         ew_lo80=np.percentile(BB[:, 1], 10), ew_hi80=np.percentile(BB[:, 1], 90), iv_lo80=np.percentile(BB[:, 2], 10), iv_hi80=np.percentile(BB[:, 2], 90),
                         ew_minus_pooled=o[1] - o[0], ew_minus_pooled_se=diff.std(ddof=1), iv_minus_pooled_se=diff_iv.std(ddof=1), iv_minus_pooled=o[2] - o[0],
                         Q=o[3], df=df, p_Q_chi2=float(chi2.sf(o[3], df)), p_Q_boot=pQ_boot, Q_power_tau03_at20=pw[0], tau_DL=float(np.sqrt(max(0, (o[3] - df) / (w.sum() - (w ** 2).sum() / w.sum())))),
                         trend_per_yr=o[4], trend_lo80=np.percentile(BB[:, 4], 10), trend_hi80=np.percentile(BB[:, 4], 90), trend_se_boot=BB[:, 4].std(ddof=1),
                         wshare_top2=float(np.sort(pairs0)[-2:].sum() / pairs0.sum())))
    print(fs, "done", flush=True)
out = pd.DataFrame(rows); os.makedirs("results", exist_ok=True); out.to_csv(f"results/a3_{tag}.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print(out[["fold_set", "a", "b", "k", "pooled", "ew", "iv", "ew_minus_pooled", "ew_minus_pooled_se", "Q", "df", "p_Q_boot", "Q_power_tau03_at20", "tau_DL", "trend_per_yr", "trend_lo80", "trend_hi80"]].round(3).to_string())
