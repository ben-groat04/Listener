"""Metrics. Point estimates and bootstrap replicates share ONE implementation: every quantity is computed with row weights W (B x n), where a point
estimate is W = 1 and a bootstrap replicate is the number of times a row's artist cluster was drawn (clusters = (fold, primary artist); whole artists are
resampled because songs of one artist are correlated). Ties: AUC counts ties half; top-k quantities average over random tie-breaks (exactly, as an expectation)."""
import numpy as np, pandas as pd
from scipy.stats import rankdata, spearmanr

def auc(y, s):
    y = np.asarray(y); n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return np.nan
    r = rankdata(s)  # average ranks => ties count half
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def _order(s, rng):  # random tie-break so constant scores cannot look good
    return np.lexsort((rng.random(len(s)), -np.asarray(s, float)))

def fold_metrics(y, s, nseeds=20):
    """AUC; AP and lift over base rate; precision in top 10% (p10) and top-20 songs (p20); recall in top 20% (r20); hits = positives in the top 10% and
    exp = hits expected at the fold's base rate. Everything except AUC is averaged over `nseeds` random tie-break orders (one order if no ties)."""
    y = np.asarray(y); s = np.asarray(s, float); n = len(y)
    nan = dict(auc=np.nan, ap=np.nan, lift=np.nan, p10=np.nan, p20=np.nan, r20=np.nan, hits=np.nan, exp=np.nan, n=n, n1=y.sum())
    if n < 10 or y.sum() == 0 or y.sum() == n: return nan
    base = y.mean(); k = max(1, round(.1 * n)); k2 = max(1, round(.2 * n)); acc = []
    for seed in range(nseeds if len(np.unique(s)) < n else 1):
        o = y[_order(s, np.random.default_rng(seed))]; prec = np.cumsum(o) / np.arange(1, n + 1)
        acc.append((prec[o == 1].mean(), o[:k].mean(), o[:20].mean(), o[:k2].sum() / y.sum(), o[:k].sum()))
    ap, p10, p20, r20, hits = np.mean(acc, axis=0)
    return dict(auc=auc(y, s), ap=ap, lift=ap / base, p10=p10, p20=p20, r20=r20, hits=hits, exp=k * base, n=n, n1=y.sum())

def spearman_cont(df, col="days90", transform=None):
    """Mean over folds of the Spearman correlation between score and a continuous outcome (tried songs only)."""
    r = []
    for _, g in df[df.is_decoy == 0].groupby("fold"):
        v = g[col].values if transform is None else transform(g[col].values)
        r.append(spearmanr(g.score, v)[0])
    return float(np.nanmean(r))

# ---------------------------------------------------------------- weighted engine
def _sorted(g, s):
    """Sort rows by (group, score) and describe tie blocks / groups in the sorted order."""
    order = np.lexsort((s, g)); gg, ss = g[order], s[order]; n = len(order); idx = np.arange(n)
    newb = np.r_[True, (gg[1:] != gg[:-1]) | (ss[1:] != ss[:-1])]; newg = np.r_[True, gg[1:] != gg[:-1]]
    bs = np.maximum.accumulate(np.where(newb, idx, 0)); gst = np.maximum.accumulate(np.where(newg, idx, 0))
    be = np.minimum.accumulate(np.where(np.r_[newb[1:], True], idx + 1, n + 1)[::-1])[::-1]
    return order, bs, be, gst, np.flatnonzero(newg), gg[np.flatnonzero(newg)]

def group_auc(y, s, g, W):
    """Weighted AUC per group g: returns (group values, num, den) with num/den of shape (B, G); pooled AUC = num.sum / den.sum (= all within-group
    positive/negative pairs, ties half, pair weight = product of the row weights). W: (B, n) row weights."""
    order, bs, be, gst, gidx, gval = _sorted(g, s)
    yy = y[order].astype(float); Ww = W[:, order]; neg = Ww * (1 - yy); pos = Ww * yy
    E = np.zeros((W.shape[0], len(y) + 1)); np.cumsum(neg, axis=1, out=E[:, 1:])
    row = pos * (E[:, bs] - E[:, gst] + .5 * (E[:, be] - E[:, bs]))
    num = np.add.reduceat(row, gidx, axis=1); den = np.add.reduceat(pos, gidx, axis=1) * np.add.reduceat(neg, gidx, axis=1)
    return gval, num, den

def pooled_auc(y, s, g, W):
    _, num, den = group_auc(y, s, g, W); d = den.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"): return np.where(d > 0, num.sum(1) / d, np.nan)

def topk(y, s, fold, W, ks=(20,), frac=.1):
    """Per fold, weighted top-k hits with exact expectation over random tie-breaks. Returns dict: p20 (macro mean over valid folds, B), plift (pooled), p10 (macro)."""
    B = W.shape[0]; p20, p10, hits, exp = [], [], np.zeros(B), np.zeros(B)
    for f in np.unique(fold):
        r = np.flatnonzero(fold == f); yf = y[r].astype(float); sf = s[r]; Wf = W[:, r]
        o = np.lexsort((np.arange(len(r)), -sf)); yf, sf, Wf = yf[o], sf[o], Wf[:, o]; n = len(r); idx = np.arange(n)
        newb = np.r_[True, sf[1:] != sf[:-1]]; bs = np.maximum.accumulate(np.where(newb, idx, 0)); be = np.minimum.accumulate(np.where(np.r_[newb[1:], True], idx + 1, n + 1)[::-1])[::-1]
        E = np.zeros((B, n + 1)); np.cumsum(Wf, axis=1, out=E[:, 1:]); Wb = E[:, be] - E[:, bs]; Cb = E[:, bs]
        P = np.zeros((B, n + 1)); np.cumsum(Wf * yf, axis=1, out=P[:, 1:]); Pb = P[:, be] - P[:, bs]   # positive weight in the tie block
        N = E[:, -1]; N1 = P[:, -1]; valid = (N >= 10) & (N1 > 0) & (N1 < N)
        hits_at = lambda k: _blocksum(Cb, Wb, Pb, k, bs, newb)   # expected positives in the top k of the weighted list
        k10 = np.maximum(1, np.rint(frac * N)); k20 = np.minimum(20, N)
        h10, h20 = hits_at(k10), hits_at(k20)
        base = np.divide(N1, N, out=np.zeros(B), where=N > 0)
        p10.append(np.where(valid, h10 / k10, np.nan)); p20.append(np.where(valid, h20 / k20, np.nan))
        hits += np.where(valid, h10, 0); exp += np.where(valid, k10 * base, 0)
    with np.errstate(invalid="ignore", divide="ignore"):
        return dict(p20=np.nanmean(np.array(p20), axis=0), p10=np.nanmean(np.array(p10), axis=0), plift=np.where(exp > 0, hits / exp, np.nan))

def _blocksum(Cb, Wb, Pb, k, bs, newb):
    """sum over tie blocks of Pb * clip(k - Cb, 0, Wb) / Wb  (one term per block: evaluated at block-start rows)."""
    t = np.divide(Pb * np.clip(k[:, None] - Cb, 0, Wb), Wb, out=np.zeros_like(Wb), where=Wb > 0)
    return (t * newb[None, :]).sum(1)

# ---------------------------------------------------------------- blocks of rows shared by all models
class Block:
    """Rows of one (pool, subset, label) block of one slice, identical in the same order for every model. Holds the cluster-bootstrap weights."""
    def __init__(self, df, label="love", nboot=300, seed=0, pos_negs=None):
        self.y = df[label].values.astype(int); self.n = len(df)
        fk = df.fold.astype(str).values; self.fold = pd.factorize(fk)[0]; self.fold_names = list(pd.unique(fk))
        self.p = df.plays90.values.astype(float) if "plays90" in df else None
        self.art = df.artist.values; self.new = df.new_artist.values.astype(bool); self.decoy = df.is_decoy.values.astype(bool)
        key = pd.Series(fk) + "|" + pd.Series(self.art).astype(str); self.cl = pd.factorize(key)[0]; ncl = self.cl.max() + 1
        self.week = pd.factorize(pd.Series(fk) + "|" + df.week.astype(str).values)[0] if "week" in df and (~self.decoy).all() else None
        self.sess = pd.factorize(pd.Series(fk) + "|" + df.sess.astype(str).values)[0] if "sess" in df and (~self.decoy).all() else None
        rng = np.random.default_rng(seed); self.C = np.zeros((nboot, ncl))
        for f in range(self.fold.max() + 1):   # resample whole artists within each fold
            cl_f = np.unique(self.cl[self.fold == f]); m = len(cl_f)
            self.C[:, cl_f] = rng.multinomial(m, np.full(m, 1.0 / m), size=nboot)
        self.W = self.C[:, self.cl]; self.W1 = np.ones((1, self.n)); self._pairs = {}

    def sub(self, mask):
        """A view restricted to rows `mask` (same weights)."""
        o = object.__new__(Block); o.__dict__.update(self.__dict__)
        for k in ("y", "fold", "art", "new", "decoy", "cl"): setattr(o, k, getattr(self, k)[mask])
        o.p = None if self.p is None else self.p[mask]; o._pairs = {}
        for k in ("week", "sess"): setattr(o, k, None if getattr(self, k) is None else getattr(self, k)[mask])
        o.W = self.W[:, mask]; o.W1 = self.W1[:, mask]; o.n = int(mask.sum()); o._mask = mask; return o   # stats() then takes the PARENT's score vector

    def stats(self, s, boot=True, which=("sauc", "wa", "ww", "ws", "plift", "p20")):
        """dict of arrays: point estimate under key (name) -> shape (1,), bootstrap under (name+'_b') -> shape (B,)."""
        out = {}; s = np.asarray(s, float)
        if getattr(self, "_mask", None) is not None: s = s[self._mask]
        for tag, W in (("", self.W1),) + ((("_b", self.W),) if boot else ()):
            if "sauc" in which: out["sauc" + tag] = pooled_auc(self.y, s, self.fold, W)
            if "ww" in which and self.week is not None: out["ww" + tag] = pooled_auc(self.y, s, self.week, W)
            if "ws" in which and self.sess is not None: out["ws" + tag] = pooled_auc(self.y, s, self.sess, W)
            if "plift" in which or "p20" in which:
                t = topk(self.y, s, self.fold, W); out["plift" + tag] = t["plift"]; out["p20" + tag] = t["p20"]; out["p10" + tag] = t["p10"]
        for gk, grp in (("gc", self.fold), ("gc_wa", self.cl)):
            if gk in which and self.p is not None:
                I, J = self._graded_pairs(gk, grp)
                m = (s[I] > s[J]) + .5 * (s[I] == s[J])
                out[gk] = np.array([m.sum() / len(I)]) if len(I) else np.array([np.nan])
                if boot:
                    num = self._wsum(I, J, m); den = self._wsum(I, J, np.ones(len(I)))
                    with np.errstate(invalid="ignore", divide="ignore"): out[gk + "_b"] = np.where(den > 0, num / den, np.nan)
        if "wa" in which:
            gval, num, den = group_auc(self.y, s, self.cl, self.W1)
            d = den.sum()
            out["wa"] = np.array([num.sum() / d if d > 0 else np.nan])
            if boot:
                Cg = self.C[:, gval]; db = (Cg * den[0]).sum(1)
                with np.errstate(invalid="ignore", divide="ignore"): out["wa_b"] = np.where(db > 0, (Cg * num[0]).sum(1) / db, np.nan)
        return out

    def _graded_pairs(self, key, grp):
        """All ordered pairs (i, j) inside one group (fold / fold x primary artist) with plays90_i > plays90_j (ties in plays90 are excluded)."""
        if key not in self._pairs:
            order = np.argsort(grp, kind="stable"); gs = grp[order]; cuts = np.flatnonzero(np.r_[True, gs[1:] != gs[:-1], True]); I, J = [], []
            for a, b in zip(cuts[:-1], cuts[1:]):
                if b - a < 2: continue
                r = order[a:b]; ii, jj = np.meshgrid(r, r, indexing="ij"); m = self.p[ii] > self.p[jj]; I.append(ii[m]); J.append(jj[m])
            I = np.concatenate(I) if I else np.zeros(0, int); J = np.concatenate(J) if J else np.zeros(0, int)
            self._pairs[key] = (I, J)
        return self._pairs[key]

    def _wsum(self, I, J, v):
        """Bootstrap replicates (B,) of sum over pairs of v_ij * W_i * W_j (pair weight = product of the artist-cluster draw counts)."""
        from scipy.sparse import csr_matrix
        A = csr_matrix((v, (I, J)), shape=(self.n, self.n)); AW = A @ self.W.T      # (n, B)
        return (AW * self.W.T).sum(0)

    def fold_auc_ci(self, s, alpha=.05):
        """Per-fold AUC with artist-cluster bootstrap CI: dict fold -> (auc, lo, hi)."""
        res = {}
        for f, name in enumerate(self.fold_names):
            m = self.fold == f; y = self.y[m]
            if y.sum() == 0 or y.sum() == m.sum(): res[name] = (np.nan, np.nan, np.nan); continue
            a = pooled_auc(y, s[m], np.zeros(m.sum(), int), self.W1[:, m])[0]; b = pooled_auc(y, s[m], np.zeros(m.sum(), int), self.W[:, m])
            res[name] = (a, np.nanpercentile(b, 100 * alpha / 2), np.nanpercentile(b, 100 * (1 - alpha / 2)))
        return res

# ---------------------------------------------------------------- permutation null (predictor independent)
def _perm_graded(s, p, g, rng):
    """Concordance of score s with plays p permuted inside groups g (all within-group pairs with differing permuted p; score ties half)."""
    n = len(s); o = np.lexsort((rng.random(n), g)); gs = np.argsort(g, kind="stable"); pp = np.empty(n); pp[gs] = p[o]
    return pp

def permutation_band(df, label="love", nperm=200, seed=0, nmean=1):
    """95% band of sauc, wa_sauc, ww_sauc, ws_sauc, new-artist sauc, gc and gc_wa when the score carries NO information: a fixed random score, labels permuted
    within fold (sauc, new-artist sauc, gc: plays90 permuted) or within group (fold x artist / ISO week / session). Tried songs only.
    nmean > 1: the band of the MEAN of `nmean` independent permutations (used for the null-control mean over seeds; keys sauc, wa, new only)."""
    rng = np.random.default_rng(seed); n = len(df); s = rng.random(n); y0 = df[label].values.astype(int)
    fk = df.fold.astype(str).values; fold = pd.factorize(fk)[0]
    grp = dict(sauc=fold, wa=pd.factorize(pd.Series(fk) + "|" + df.artist.astype(str).values)[0], ww=pd.factorize(pd.Series(fk) + "|" + df.week.astype(str).values)[0],
               ws=pd.factorize(pd.Series(fk) + "|" + df.sess.astype(str).values)[0], new=fold)
    if nmean > 1: grp = {k: grp[k] for k in ("sauc", "wa", "new")}
    new = df.new_artist.values.astype(bool); one = np.ones((1, n)); out = {k: [] for k in grp}
    def perm(g):
        o = np.lexsort((rng.random(n), g)); gs = np.argsort(g, kind="stable"); y = np.empty(n, int); y[gs] = y0[o]; return y
    def one_auc(k, g):
        y = perm(g)
        return pooled_auc(y[new], s[new], fold[new], one[:, new])[0] if k == "new" else pooled_auc(y, s, g, one)[0]
    for _ in range(nperm):
        for k, g in grp.items(): out[k].append(np.mean([one_auc(k, g) for _ in range(nmean)]))
    res = {k: tuple(np.nanpercentile(v, [2.5, 97.5]).round(3)) for k, v in out.items()}
    if nmean == 1 and "plays90" in df:   # graded concordance (needs pair structure: all within-group pairs, orientation by the permuted plays90)
        p0 = df.plays90.values.astype(float); cl = grp["wa"]
        for k, g in (("gc", fold), ("gc_wa", cl)):
            order = np.argsort(g, kind="stable"); gs = g[order]; cuts = np.flatnonzero(np.r_[True, gs[1:] != gs[:-1], True]); I, J = [], []
            for a, b in zip(cuts[:-1], cuts[1:]):
                if b - a < 2: continue
                r = order[a:b]; ii, jj = np.triu_indices(len(r), 1); I.append(r[ii]); J.append(r[jj])
            I = np.concatenate(I); J = np.concatenate(J); si = s[I] - s[J]; v = []
            for _ in range(nperm):
                pp = _perm_graded(s, p0, g, rng); d = pp[I] - pp[J]; m = d != 0
                v.append((((d > 0) == (si > 0)) & m).sum() / m.sum())
            res[k] = tuple(np.nanpercentile(v, [2.5, 97.5]).round(3))
    return res
