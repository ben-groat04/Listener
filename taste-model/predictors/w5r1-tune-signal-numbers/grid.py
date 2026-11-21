"""PRE-WRITTEN grid (written before any scoring).  One-at-a-time (OAT) ranges around the defaults + seeded random joint sample.
Default (W4 listening recipe numbers, the base) = DEFAULT.  Each OAT entry overrides ONE parameter (or one coupled pair: hor+mat).
Parameters:
 new-songs signal: tgt (target: pct_plays|pct_days|pd|love|logz|share), grp (quarter|roll|all), gdays (roll bin length), mingrp (drop groups with fewer songs),
   hor (horizon of the play counts, days), mat (maturity: only songs first played >= mat days before the cutoff), partial (trunc|scale: handling of songs younger than hor),
   pop (population of the percentile: meta|audio), newhl (recency half-life days, None=off), window (training window days, None=all)
 panel signal: K, P, hl (0 = no decay), minplays, minsongs (skip-period threshold)
 blend: wnew (weight of the two new-song members vs the two panel members; 0.5 = equal = default)
 stale: days by which the training record is cut back before the cutoff (staleness test; not in the tuner grid)"""
import random
DEFAULT = dict(tgt="pct_plays", grp="quarter", gdays=91, mingrp=0, hor=90, mat=90, partial="trunc", pop="meta", newhl=None, window=None,
               K=2, P=91, hl=180.0, minplays=2, minsongs=20, wnew=0.5, stale=0)
OAT = {  # name -> override
 "tgt_days": dict(tgt="pct_days"), "tgt_pd": dict(tgt="pd"), "tgt_love": dict(tgt="love"), "tgt_logz": dict(tgt="logz"), "tgt_share": dict(tgt="share"),
 "grp_roll91": dict(grp="roll"), "grp_roll61": dict(grp="roll", gdays=61), "grp_roll182": dict(grp="roll", gdays=182), "grp_all": dict(grp="all"), "grp_q_min30": dict(mingrp=30),
 "hor30": dict(hor=30, mat=30), "hor60": dict(hor=60, mat=60), "hor180": dict(hor=180, mat=180),
 "mat30": dict(mat=30), "mat60": dict(mat=60), "mat60_scale": dict(mat=60, partial="scale"), "mat120": dict(mat=120), "mat0_scale": dict(mat=0, partial="scale"),
 "pop_audio": dict(pop="audio"),
 "newhl180": dict(newhl=180.0), "newhl365": dict(newhl=365.0), "newhl730": dict(newhl=730.0),
 "win365": dict(window=365), "win730": dict(window=730), "win1095": dict(window=1095),
 "K1": dict(K=1), "K3": dict(K=3), "K4": dict(K=4), "K6": dict(K=6),
 "P30": dict(P=30, K=2), "P61": dict(P=61), "P182": dict(P=182),
 "hl90": dict(hl=90.0), "hl365": dict(hl=365.0), "hlinf": dict(hl=0.0),
 "mp1": dict(minplays=1), "mp3": dict(minplays=3), "mp5": dict(minplays=5), "ms5": dict(minsongs=5), "ms50": dict(minsongs=50),
 "wnew0": dict(wnew=0.0), "wnew25": dict(wnew=0.25), "wnew75": dict(wnew=0.75), "wnew1": dict(wnew=1.0),
}
STALE = {"stale30": dict(stale=30), "stale90": dict(stale=90), "stale180": dict(stale=180)}   # sensitivity map only
# values for the random joint sample: each parameter drawn independently and uniformly from these (default included)
CHOICES = dict(tgt=["pct_plays", "pct_days", "pd", "love", "logz", "share"], grp=["quarter", "roll", "all"], gdays=[61, 91, 182], mingrp=[0, 30],
               hor=[60, 90, 180], mat=[30, 60, 90, 120], partial=["trunc", "scale"], pop=["meta", "audio"], newhl=[None, 365.0, 730.0], window=[None, 730, 1095],
               K=[1, 2, 3, 4], P=[61, 91, 182], hl=[90.0, 180.0, 365.0, 0.0], minplays=[1, 2, 3], minsongs=[10, 20, 50], wnew=[0.0, 0.25, 0.5, 0.75, 1.0])
def random_configs(n=40, seed=20261121):
    rng = random.Random(seed); out = {}
    for i in range(n):
        c = {k: rng.choice(v) for k, v in CHOICES.items()}
        if c["mat"] < c["hor"] and c["partial"] == "trunc" and False: pass
        out["rj%02d" % i] = c
    return out
TUNER_GRID = dict(default={}, **OAT)   # the grid the nested tuner chooses from
SMALL_GRID = ["default", "grp_roll91", "grp_roll182", "grp_all", "mat60", "mat60_scale", "mat0_scale", "pop_audio"]   # the issues named in the brief (quarter stub M12, population M13, maturity/partial horizon)
# post-hoc combinations of the two signals that stood out in the OAT map / inner choices (added AFTER seeing the OAT table; counted as variants)
COMBO = {"cmb_mat0s_roll91": dict(mat=0, partial="scale", grp="roll"), "cmb_mat0s_all": dict(mat=0, partial="scale", grp="all"), "cmb_mat60s_roll91": dict(mat=60, partial="scale", grp="roll"),
         "cmb_mat0s_roll182": dict(mat=0, partial="scale", grp="roll", gdays=182)}
