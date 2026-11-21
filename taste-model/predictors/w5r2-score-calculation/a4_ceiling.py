"""Ceiling / label-noise analysis on the TUNE dump (tried pool)."""
import sys; sys.path.insert(0, "."); from lib import *
d = load("tune"); y = d.love.values; f = d.fold.values
print("n", len(d), "loved", y.sum(), "base rate", y.mean().round(3))
# 1) near-threshold share
p = d.plays90.values; dy = d.days90.values
print("plays90 distribution (share): ", {k: round(float(v), 3) for k, v in pd.Series(np.clip(p, 0, 12)).value_counts(normalize=True).sort_index().items()})
near = ((p >= 4) & (p <= 8)) | ((dy >= 2) & (dy <= 4)); print("share within plays90 4..8 or days90 2..4:", near.mean().round(3), "; among loved:", near[y == 1].mean().round(3), "; among not loved:", near[y == 0].mean().round(3))
meets_p = p >= 6; meets_d = dy >= 3
print("loved by play rule only (>=6 plays):", meets_p.mean().round(3), "days rule only:", meets_d.mean().round(3), "both:", (meets_p & meets_d).mean().round(3))
print("loved songs with exactly 6-7 plays or exactly 3 days:", ((y == 1) & ((p <= 7) | (dy == 3))).sum() / y.sum())
# 2) agreement between neighbouring labels
def kappa(a, b):
    po = (a == b).mean(); pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean()); return (po - pe) / (1 - pe)
for nm in ["love_4_2", "love_10_4", "strong", "keep", "love_h180", "love_h365"]:
    z = d[nm].values.astype(int); print(f"love vs {nm}: base {z.mean():.3f} agree {(z == y).mean():.3f} kappa {kappa(y, z):.3f} P(other=1|love=1) {z[y == 1].mean():.3f} P(other=1|love=0) {z[y == 0].mean():.3f}")
# 3) outcome-reliability: AUC of one definition as predictor of another (within fold pooled)
for a, b in [("plays90", "keep"), ("days90", "keep"), ("love_4_2", "love"), ("love_10_4", "love"), ("plays_h30", "love"), ("plays_h60", "love"), ("plays_h30", "keep"), ("plays_h365", "love"), ("plays90", "strong")]:
    print(f"AUC {a} -> {b}: {sauc(d[a].values.astype(float) + 1e-9 * np.random.default_rng(0).random(len(d)), d[b].values.astype(int), f):.3f}")
# 4) Poisson-noise ceiling. Gamma-Poisson fit to plays90 (method of moments on pooled songs), latent rate mu_i ~ Gamma; label'=plays>=6 (and days>=3 approximated by plays only)
rng = np.random.default_rng(3); m = p.mean(); v = p.var(); print("plays90 mean", m.round(2), "var", v.round(2), "overdispersion var/mean", (v / m).round(2))
for lam in (1.0, 0.75, 0.5):
    # latent spread: true variance = lam*(v - m) (assume part of overdispersion is true signal), mu ~ Gamma(shape=m^2/vt, scale=vt/m)
    vt = max(lam * (v - m), 1e-6) + 0.0; vt = max(vt, 1e-6); shape = m ** 2 / vt; scale = vt / m
    A = []
    for _ in range(50):
        mu = rng.gamma(shape, scale, len(d)); pl = rng.poisson(mu); lab = (pl >= 6).astype(int)
        A.append(sauc(mu, lab, f))
    print(f"gamma-Poisson ceiling (true latent variance = {lam:.2f} x overdispersion): AUC(true rate, realised plays>=6 label) = {np.mean(A):.3f} (sd {np.std(A):.3f}); matching base rate sim {np.mean(pl>=6):.3f} vs real {(p>=6).mean():.3f}")
# replicate-label ceiling using observed plays as mu (upper bound)
A = []
for _ in range(50):
    pl = rng.poisson(p); lab = (pl >= 6).astype(int); A.append(sauc(p.astype(float) + 1e-9 * rng.random(len(p)), lab, f))
print("observed-plays as mu, Poisson replicate label (upper bound):", np.mean(A).round(3))
# 5) how much of the base-rate structure is within-fold: AUC of fold-only? and noise-level of model scores
for mname in ["pair_z", "ref_w4r1_listening", "artist_recent", "oracle_day1", "oracle_7d", "replays_first_session", "pool_artist_siblings"]:
    print(mname, "sauc", round(sauc(d["score__" + mname].values, y, f), 3), "keep-AUC", round(sauc(d["score__" + mname].values, d.keep.values.astype(int), f), 3))
# below chance? artist_plays on new artists
for mname in ["artist_plays", "artist_recent", "pool_artist_siblings", "popularity", "has_preview"]:
    for na in (0, 1):
        mm = d.new_artist.values == na; print("subset new_artist=", na, mname, "n", mm.sum(), "sauc", round(sauc(d["score__" + mname].values[mm], y[mm], f[mm]), 3))
