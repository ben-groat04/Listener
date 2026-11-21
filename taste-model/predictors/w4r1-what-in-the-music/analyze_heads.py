"""Findings analysis on TUNE (10 folds, non-HOLDOUT tried songs only).  Descriptive: per-head stratified AUC of the clip-mean head activation vs love (all TUNE tried songs, fold-stratified pairs, plus within-artist pairs) with artist-cluster bootstrap CI.
Out-of-sample: per fold, the sign of each head is learned ONLY on train songs (Spearman of head vs plays90 quarter-rank among mature train songs) and the signed head is scored on that fold's tried songs.
Run from /home/user/Listener/taste-model: python3 -W ignore predictors/w4r1-what-in-the-music/analyze_heads.py OUT.csv"""
import sys, json, hashlib, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, "/home/user/Listener/taste-model/predictors/w4r1-what-in-the-music")
from evalkit import run, data
import predict as P
folds = run.prepare_folds(data.TUNE_CUTOFFS, "main")
L = json.load(open(P.ROOT + ".cache/shared/w4-essentia/labels.json"))
names = [f"{h['name']}:{c}" for h in L["heads"] for c in h["classes"]]
cfg = {**P.CFG}
rows = []
for F in folds:
    pool = F["pool"].iloc[F["order"]].reset_index(drop=True); cands, meta = F["cands"], F["meta"]
    tried = (pool.is_decoy == 0).values
    X, ok = P._view(cands.trackId.values, meta, cfg); X = X[:, 0]
    st = data.song_table(F["train"]).reset_index(); st = st[st.trackId.isin(meta.index)].reset_index(drop=True)
    Xt, okt = P._view(st.trackId.values, meta, cfg); Xt = Xt[:, 0]
    mat = (st["first"] < F["c"] - pd.Timedelta(days=90)).values & okt
    qa = st["first"].dt.to_period("Q").astype(str).values
    yr = pd.Series(st.plays90.values[mat]).groupby(qa[mat]).rank(pct=True).values
    Xm = Xt[mat]; r = pd.DataFrame(Xm).rank().values; ry = pd.Series(yr).rank().values
    rz = (r - r.mean(0)) / (r.std(0) + 1e-9); yz = (ry - ry.mean()) / ry.std(); sign = np.sign((rz * yz[:, None]).mean(0))
    keep = tried & ok
    d = pd.DataFrame(dict(fold=str(F["c"].date()), artist=cands.artist.values[keep], love=pool.love.values[keep], tid=cands.trackId.values[keep]))
    rows.append((d, X[keep], sign, (rz * yz[:, None]).mean(0)))
D = pd.concat([r[0] for r in rows], ignore_index=True); XA = np.concatenate([r[1] for r in rows]); SG = np.concatenate([np.repeat(r[2][None], len(r[0]), 0) for r in rows])
y = D.love.values; fold = D.fold.values; art = D.artist.values
print("n tried with audio", len(D), "loved", y.sum())
def pair_auc(score, keyv, w=None):   # AUC over loved/not pairs sharing key, optional artist-draw weights
    num = den = 0.0
    for k in np.unique(keyv):
        m = keyv == k; yy = y[m]; s = score[m]; ww = np.ones(m.sum()) if w is None else w[m]
        if yy.sum() == 0 or yy.sum() == len(yy): continue
        P_, N_ = s[yy == 1], s[yy == 0]; wp, wn = ww[yy == 1], ww[yy == 0]
        g = (P_[:, None] > N_[None]) + 0.5 * (P_[:, None] == N_[None]); W = wp[:, None] * wn[None]
        num += (g * W).sum(); den += W.sum()
    return num / den if den > 0 else np.nan
# vectorised faster: rank-based per fold
def fast_auc(S, keyv, w):   # S [n, d] ; returns [d]
    num = np.zeros(S.shape[1]); den = 0.0
    for k in np.unique(keyv):
        m = keyv == k; yy = y[m]; ww = w[m]
        if yy.sum() == 0 or yy.sum() == len(yy): continue
        Sm = S[m]; R = pd.DataFrame(Sm).rank().values   # average ranks
        # weighted AUC via sorting is complex; use pairwise on weights: sum_{i pos, j neg} w_i w_j [s_i>s_j]
        pos = np.where(yy == 1)[0]; neg = np.where(yy == 0)[0]
        for a in range(0, len(pos), 50):
            pa = pos[a:a + 50]
            g = (Sm[pa][:, None, :] > Sm[neg][None]) + 0.5 * (Sm[pa][:, None, :] == Sm[neg][None])
            W = ww[pa][:, None] * ww[neg][None]; num += np.einsum("ijd,ij->d", g, W)
        den += (ww[pos].sum() * ww[neg].sum())
    return num / den
ua = np.unique(art); rng = np.random.default_rng(0); ai = {a: i for i, a in enumerate(ua)}; aidx = np.array([ai[a] for a in art])
# within-artist: key = fold+artist
key_wa = np.array([f + "|" + str(a) for f, a in zip(fold, art)])
res = {}
w1 = np.ones(len(D))
res["auc"] = fast_auc(XA, fold, w1)
res["oos_auc"] = fast_auc(XA * SG, fold, w1)
res["wa_auc"] = fast_auc(XA, key_wa, w1)
nb = 60; B = {k: [] for k in res}
for b in range(nb):
    cnt = rng.multinomial(len(ua), np.ones(len(ua)) / len(ua)); w = cnt[aidx].astype(float)
    for k, S, key in (("auc", XA, fold), ("oos_auc", XA * SG, fold), ("wa_auc", XA, key_wa)): B[k].append(fast_auc(S, key, w))
out = pd.DataFrame(dict(head=names, auc=res["auc"], auc_lo=np.nanpercentile(B["auc"], 2.5, 0), auc_hi=np.nanpercentile(B["auc"], 97.5, 0), wa_auc=res["wa_auc"], wa_lo=np.nanpercentile(B["wa_auc"], 2.5, 0), wa_hi=np.nanpercentile(B["wa_auc"], 97.5, 0),
                        oos_auc=res["oos_auc"], oos_lo=np.nanpercentile(B["oos_auc"], 2.5, 0), oos_hi=np.nanpercentile(B["oos_auc"], 97.5, 0), mean_act=XA.mean(0), sign_agree=np.mean(SG > 0, 0)))
# permutation null of max |auc-0.5| (labels permuted within fold)
y0 = y.copy(); mx = []
for p in range(30):
    y = y0.copy()
    for f in np.unique(fold): m = fold == f; y[m] = rng.permutation(y0[m])
    a = fast_auc(XA, fold, w1); mx.append(np.nanmax(np.abs(a - 0.5)))
y = y0
out.attrs = {}
out.to_csv(sys.argv[1], index=False)
print("perm max|auc-0.5| over 605 heads: mean %.3f max %.3f p95 %.3f" % (np.mean(mx), np.max(mx), np.percentile(mx, 95)))
