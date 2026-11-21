"""Below-chance investigations: (1) wa under calendar-quarter pairing with monthly cutoffs (artist_recent 0.43); (2) popularity sauc < 0.5 on TUNE; (3) per-quarter AUC bootstrap of early quarters for content models."""
import lib, numpy as np, pandas as pd
d = lib.dump(); out = []
g = lib.frame(d, "tune_m", "quarter"); res = lib.evaluate(g, ["artist_recent", "artist_plays", "w5r1_stack3"], nboot=300, which=("wa",), new=False)
for m in res: out.append(f"tune_m quarter-paired wa {m}: {res[m]['wa'][0]:.3f} 80% [{np.percentile(res[m]['wa'][1],10):.3f},{np.percentile(res[m]['wa'][1],90):.3f}]")
# time-rank alone: AUC of month index within (quarter, artist) for love
g["_t"] = pd.factorize(g.month, sort=True)[0].astype(float); gv, num, den = lib.groupstats(g.assign(fa=g.fold + "|" + g.artist.astype(str)), g["_t"].values, None, "fa")
out.append(f"within (quarter,artist) AUC of 'later month' alone vs love on tune_m: {num.sum()/den.sum():.3f} (pairs {den.sum():.0f})")
# same artist: artist_recent differs only through cutoff; check within-pair monotonic relation
gg = g.assign(fa=g.fold + "|" + g.artist.astype(str)); n_pairs_diff = 0
out.append(f"share of rows in (quarter,artist) groups with >=2 distinct months: {gg.groupby('fa').month.transform('nunique').gt(1).mean():.3f}")
# popularity
for s in ("tune", "tune_q1", "tune_q2", "tune_m", "tune_h", "tune_y"):
    gs = lib.frame(d, s, "fold"); r = lib.evaluate(gs, ["popularity"], nboot=300, which=("sauc", "wa"), new=False)["popularity"]
    out.append(f"popularity {s}: sauc {r['sauc'][0]:.3f} [80% {np.percentile(r['sauc'][1],10):.3f},{np.percentile(r['sauc'][1],90):.3f}; 95% {np.percentile(r['sauc'][1],2.5):.3f},{np.percentile(r['sauc'][1],97.5):.3f}] P(<0.5)={np.mean(r['sauc'][1]<0.5):.2f}; wa {r['wa'][0]:.3f}")
# early-quarter content AUC with bootstrap
gq = lib.frame(d, "tune", "quarter"); W = lib.boot_W(gq, 300, 0); y = gq._lab.values
for m in ("ref_audio_final", "ref_w4r1_music", "ref_w4r1_listening", "artist_recent"):
    gv, num, den = lib.groupstats(gq, gq["score__" + m].values, np.vstack([np.ones((1, len(y))), W]))
    a = num / den; out.append(f"{m} per-quarter AUC [80% boot] " + "; ".join(f"{q}:{a[0,i]:.2f}[{np.nanpercentile(a[1:,i],10):.2f},{np.nanpercentile(a[1:,i],90):.2f}]" for i, q in enumerate(gv)))
(lib.OUT / "a7_below_chance.txt").write_text("\n".join(out)); print("\n".join(out))
