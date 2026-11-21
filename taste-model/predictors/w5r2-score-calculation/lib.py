"""Shared analysis code (dump-based). Dump path comes from env W5R2_DUMP (default scratch d1.pkl)."""
import os, numpy as np, pandas as pd
from scipy.stats import rankdata
SCR = "/tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf5/builder-r2-score-calculation"
DUMP = os.environ.get("W5R2_DUMP", SCR + "/dumps/d1.pkl")
BASE = ["popularity","artist_plays","artist_recent","artist_love_rate","duration","meta_gbm","nonaudio_gbm","has_preview","preview_source_itunes"]
REFS = ["ref_audio_final","ref_w4r1_listening","ref_w4r1_music"]
MODELS = BASE + REFS + ["pair_z"]
DIAG = ["pool_artist_siblings","pool_album_siblings","exposure_before","exposure_after","exposure_session","replays_first_session","oracle_day1","oracle_7d"]

def load(fold_set="tune"):
    d = pd.read_pickle(DUMP); d = d[d.fold_set == fold_set].reset_index(drop=True)
    d["love_h180"] = ((d.plays_h180 >= 6) & (d.days_h180 >= 3)).astype(int)
    d["love_h365"] = ((d.plays_h365 >= 6) & (d.days_h365 >= 3)).astype(int)
    return d

def auc_parts(s, y, g):
    """per-group (U, npos*nneg, npos, nneg) with average ties."""
    out = {}
    for k in np.unique(g):
        m = g == k; yy = y[m]; n1 = int(yy.sum()); n0 = len(yy) - n1
        if n1 == 0 or n0 == 0: continue
        r = rankdata(s[m]); U = r[yy == 1].sum() - n1 * (n1 + 1) / 2
        out[k] = (U, n1 * n0, n1, n0)
    return out

def sauc(s, y, g):
    p = auc_parts(s, y, g); den = sum(v[1] for v in p.values())
    return sum(v[0] for v in p.values()) / den if den else np.nan

def macro(s, y, g, minn=5):
    p = auc_parts(s, y, g); a = [v[0] / v[1] for v in p.values() if v[2] >= minn and v[3] >= minn]
    return np.mean(a) if a else np.nan

def iv_level(s, y, g, minn=5):
    """IV-weighted mean of per-fold AUC; weights = 1/Hanley-McNeil null variance (model independent)"""
    p = auc_parts(s, y, g); a = []; w = []
    for v in p.values():
        if v[2] >= minn and v[3] >= minn: a.append(v[0] / v[1]); w.append(12 * v[2] * v[3] / (v[2] + v[3] + 1))
    return np.average(a, weights=w) if a else np.nan

def topk(s, y, g, frac=0.1, k=None, rec=False, seed=0):
    rng = np.random.default_rng(seed); s = s + rng.random(len(s)) * 1e-9 * (np.ptp(s) + 1e-12)
    hit = exp = tot = n = 0.0
    for kk in np.unique(g):
        m = np.where(g == kk)[0]; yy = y[m]
        if len(m) < 5: continue
        kn = k if k else max(1, int(np.ceil(frac * len(m)))); kn = min(kn, len(m))
        top = np.argsort(-s[m])[:kn]; h = yy[top].sum()
        hit += h; exp += kn * yy.mean(); tot += yy.sum(); n += kn
    if rec: return hit / tot if tot else np.nan
    return hit / exp if exp else np.nan

def gcon(s, v, g):
    """within-group concordance with graded outcome v (ties in v excluded, score ties .5)"""
    num = den = 0.0
    for kk in np.unique(g):
        m = g == kk; ss = s[m]; vv = v[m]
        dv = np.sign(vv[:, None] - vv[None, :]); ds = np.sign(ss[:, None] - ss[None, :])
        nz = dv != 0; num += ((dv * ds > 0) & nz).sum() + 0.5 * ((ds == 0) & nz).sum(); den += nz.sum()
    return num / den if den else np.nan

METRICS = {
 "S1_sauc": lambda d, m: sauc(d[m].values, d.love.values, d.fold.values),
 "S3_macro": lambda d, m: macro(d[m].values, d.love.values, d.fold.values),
 "S2_ivlevel": lambda d, m: iv_level(d[m].values, d.love.values, d.fold.values),
 "S5_lift_top10pct": lambda d, m: topk(d[m].values, d.love.values, d.fold.values, 0.1),
 "S6_recall_top20pct": lambda d, m: topk(d[m].values, d.love.values, d.fold.values, 0.2, rec=True),
 "S7_prec_at10_lift": lambda d, m: topk(d[m].values, d.love.values, d.fold.values, k=10),
 "S8_gc_plays90": lambda d, m: gcon(d[m].values, d.plays90.values, d.fold.values),
 "S9_gc_share90": lambda d, m: gcon(d[m].values, d.share90.values, d.fold.values),
 "S10_auc_keep": lambda d, m: sauc(d[m].values, d.keep.fillna(0).values.astype(int), d.fold.values),
 "S11_auc_love_4_2": lambda d, m: sauc(d[m].values, d.love_4_2.values, d.fold.values),
 "S12_auc_love_10_4": lambda d, m: sauc(d[m].values, d.love_10_4.values, d.fold.values),
 "S13_auc_strong": lambda d, m: sauc(d[m].values, d.strong.values, d.fold.values),
 "S14_auc_love_h180": lambda d, m: sauc(d[m].values, d.love_h180.values, d.fold.values),
 "S15_auc_love_h365": lambda d, m: sauc(d[m].values, d.love_h365.values, d.fold.values),
}

def artist_resample(d, rng, frac=None):
    """cluster bootstrap (frac None) or random artist half (frac=.5 -> returns two index arrays)"""
    arts = d.artist.unique(); grp = d.groupby("artist").indices
    if frac is None:
        pick = rng.choice(len(arts), len(arts), replace=True)
        return np.concatenate([grp[arts[i]] for i in pick])
    perm = rng.permutation(len(arts)); h = len(arts) // 2
    return (np.concatenate([grp[arts[i]] for i in perm[:h]]), np.concatenate([grp[arts[i]] for i in perm[h:]]))
