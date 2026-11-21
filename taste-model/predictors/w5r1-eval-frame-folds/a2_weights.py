"""Item 1 (cont.): which quarters drive conclusions. On default TUNE folds (10 quarters): pair-weight share, per-quarter AUC, leave-one-quarter-out, alternative weightings
(pooled pairs, macro over quarters, equal weight per half-year, equal weight per year), drop-first-k-quarters (start date), early/late halves and a time trend of the paired delta."""
import lib, numpy as np, pandas as pd
d = lib.dump(); g = lib.frame(d, "tune", "quarter"); NB = 300; W = lib.boot_W(g, NB, 0); y = g._lab.values; Q = g.fold.values
qs = sorted(set(Q)); half = {q: q[:4] + "H" + str((int(q[-1]) - 1) // 2 + 1) for q in qs}; year = {q: q[:4] for q in qs}
MOD = lib.MODELS
NUM, DEN = {}, {}
for m in MOD:
    gv, num, den = lib.groupstats(g, g["score__" + m].values, np.vstack([np.ones((1, len(y))), W]))
    NUM[m], DEN[m] = num, den     # (1+NB, G); row 0 = point
gv = list(gv); idx = {q: i for i, q in enumerate(gv)}
out = []
# pair weight share and per-quarter AUC, n per quarter
den0 = DEN["artist_recent"][0]; share = den0 / den0.sum()
tab = pd.DataFrame({"n": [int((Q == q).sum()) for q in gv], "n_love": [int(y[Q == q].sum()) for q in gv], "pair_share": share.round(3)}, index=gv)
for m in MOD: tab[m] = (NUM[m][0] / DEN[m][0]).round(3)
out.append("=== per-quarter table: n, loved, share of pooled pair weight, AUC per model (rows = quarters)\n" + tab.to_string())
def combine(m, wts, sel=None):
    """AUC for each of 1+NB resamples under a weighting: wts = dict group-> weight function of den (callable on (B,)) ; here generic: returns array(1+NB)."""
    num, den = NUM[m], DEN[m]; return wts(num, den)
def pooled(sel): 
    ii = [idx[q] for q in sel]; return lambda n, dn: n[:, ii].sum(1) / dn[:, ii].sum(1)
def macro(sel, grp):
    def f(n, dn):
        parts = {}
        for q in sel: parts.setdefault(grp(q), []).append(idx[q])
        a = [n[:, ii].sum(1) / dn[:, ii].sum(1) for ii in parts.values()]; return np.mean(a, axis=0)
    return f
def macro_q(sel):
    def f(n, dn): return np.mean([n[:, idx[q]] / dn[:, idx[q]] for q in sel], axis=0)
    return f
variants = {"pooled_pairs": pooled(qs), "macro_quarter": macro_q(qs), "equal_per_half": macro(qs, lambda q: half[q]), "equal_per_year": macro(qs, lambda q: year[q])}
for q in qs: variants[f"LOO_{q}"] = pooled([x for x in qs if x != q])
for k in (1, 2, 3, 4): variants[f"drop_first_{k}q"] = pooled(qs[k:])
variants["only_first_half_of_TUNE"] = pooled(qs[:5]); variants["only_second_half_of_TUNE"] = pooled(qs[5:])
variants["drop_2023Q1_and_Q4"] = pooled([q for q in qs if q not in ("2023Q1", "2023Q4")])
RES = {}
for v, f in variants.items():
    RES[v] = {m: f(NUM[m], DEN[m]) for m in MOD}
rows = []
base_rank = {m: RES["pooled_pairs"][m][0] for m in MOD}
for v in variants:
    r = RES[v]; pt = {m: r[m][0] for m in MOD}; br = max(lib.REFROWS, key=lambda m: pt[m])
    row = dict(variant=v, best_ref=br, tau_vs_pooled=round(lib.kendall([pt[m] for m in MOD], [base_rank[m] for m in MOD]), 2))
    for m in ("artist_recent", "ref_w4r1_listening", "ref_w4r1_music", "ref_audio_final", "w5r1_stack3"): row[m] = round(pt[m], 3)
    for a, b, tag in (("w5r1_stack3", "artist_recent", "stack3-ar"), ("ref_w4r1_music", "artist_recent", "music-ar"), ("ref_w4r1_listening", "artist_recent", "listening-ar"), ("ref_audio_final", "artist_recent", "audio-ar"), ("w5r1_stack3", "ref_w4r1_listening", "stack3-listening")):
        x = r[a][1:] - r[b][1:]; x = x[np.isfinite(x)]; row[tag] = round(r[a][0] - r[b][0], 3); row[tag + "_lo80"] = round(float(np.percentile(x, 10)), 3)
    rows.append(row)
T = pd.DataFrame(rows); T.to_csv(lib.OUT / "a2_weights.csv", index=False); pd.set_option("display.width", 300); pd.set_option("display.max_columns", 40)
out.append("\n=== weighting / leave-one-out variants (point; delta columns with lo80 of paired artist-cluster bootstrap, nboot 300)\n" + T.to_string(index=False))
# pair share of the heavy quarters
out.append(f"\npair share of 2023Q1 + 2023Q4 = {share[idx['2023Q1']] + share[idx['2023Q4']]:.3f}; max single-quarter share {share.max():.3f}")
# time trend of delta (stack3 - artist_recent, content - ar) per quarter: slope per year with bootstrap
def slope(m1, m2):
    t = np.array([(int(q[:4]) - 2021) + (int(q[-1]) - 1) / 4 for q in gv]); res = []
    for b in range(1 + NB):
        a = NUM[m1][b] / DEN[m1][b] - NUM[m2][b] / DEN[m2][b]; ok = np.isfinite(a); res.append(np.polyfit(t[ok], a[ok], 1)[0])
    res = np.array(res); return res[0], np.percentile(res[1:], 10), np.percentile(res[1:], 90)
out.append("\n=== per-quarter AUC delta vs artist_recent (rows quarters) and linear slope per year (point, 80% interval)")
D = pd.DataFrame({m: (NUM[m][0] / DEN[m][0] - NUM["artist_recent"][0] / DEN["artist_recent"][0]).round(3) for m in ("ref_audio_final", "ref_w4r1_listening", "ref_w4r1_music", "w5r1_stack3")}, index=gv)
out.append(D.to_string())
for m in ("ref_audio_final", "ref_w4r1_listening", "ref_w4r1_music", "w5r1_stack3"):
    s = slope(m, "artist_recent"); out.append(f"slope of ({m} - artist_recent) per quarter-year: {s[0]:+.3f} [80%: {s[1]:+.3f}, {s[2]:+.3f}]")
# candidates and love rates per quarter
out.append("\n=== love rate and new_artist share per quarter\n" + pd.DataFrame({"love_rate": g.groupby("fold")._lab.mean().round(3), "new_artist_share": g.groupby("fold").new_artist.mean().round(3)}).to_string())
(lib.OUT / "a2_weights.txt").write_text("\n".join(out)); print("\n".join(out))
