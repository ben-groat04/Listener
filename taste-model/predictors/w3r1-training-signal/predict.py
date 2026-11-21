"""w3r1-training-signal: entry file for the harness.
Final predictor `w3r1_final`: standardised blend of
  (1) HistGradientBoosting on the evalkit nonaudio feature set (metadata + point-in-time artist history),
  (2) the same + CLAP audio-similarity features (preview audio: similarity to loved / dismissed songs of the last 450 days matured before the song's first play, and to recent listening),
  (3) 2 x the plain frequency statistic artist_recent (log1p of 180-day half-life weighted artist plays),
with members (1) and (2) trained on a GRADED, period-normalised target (percentile of plays in the 90-day horizon within the quarter of first play; `rank_plays`),
only on songs first played in the last 365 days before the cutoff (window widens to >= 250 songs in the earliest folds) with a 120-day half-life recency weight,
and only on songs whose 90-day horizon is complete before the cutoff. See report / core.py.
Other entries: ablations used for the report (same code path)."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor, make_blend
G = dict(hl=120, window=365, gbm=dict(max_iter=60), target="rank_plays")
Ga = dict(G, rep="base+a")
AR = dict(fn="artist_recent")
PREDICTORS = {
    "w3r1_final": make_blend([G, Ga, AR], [1, 1, 2]),
    "w3r1_noaudio": make_blend([G, AR], [1, 1]),
    "w3r1_learned_only": make_blend([G, Ga], [1, 1]),   # final without the artist_recent member: isolates the learned part (for the null control)
    "w3r1_final_lovetarget": make_blend([dict(G, target="love"), dict(Ga, target="love"), AR], [1, 1, 2]),   # ablation: binary love 6/3 target, same everything else
}
