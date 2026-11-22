"""Signal config family for w5r2-signal-fresh-and-averaging (written BEFORE any new scoring; see PREREG.md).
Keys as in the round-1 copy; stale (whole record cut back, days) is split into stale_new / stale_pan for the staleness decomposition."""
DEFAULT = dict(tgt="pct_plays", grp="quarter", gdays=91, mingrp=0, hor=90, mat=90, partial="trunc", pop="meta", newhl=None, window=None,
               K=2, P=91, hl=180.0, minplays=2, minsongs=20, wnew=0.5, stale=0, stale_new=0, stale_pan=0)
GRPS = {"q": dict(grp="quarter"), "r91": dict(grp="roll", gdays=91), "all": dict(grp="all")}
# lead (a) family: 20 non-default configs (+ default m90t_q).  mat 90 + scale == default (age>=90 for every population song), so it is not listed.
FAMILY = {}
for mat in (60, 30, 0):
    for part in ("trunc", "scale"):
        for gk, gv in GRPS.items():
            FAMILY["m%d%s_%s" % (mat, part[0], gk)] = dict(mat=mat, partial=part, **gv)
for gk in ("r91", "all"): FAMILY["m90t_" + gk] = dict(mat=90, partial="trunc", **GRPS[gk])
assert len(FAMILY) == 20
PRIMARY = "m0s_q"                       # = round-1 mat0_scale
ALL21 = ["default"] + list(FAMILY)
CFG = dict(default={}, **FAMILY)
# lead (b) averaging procedures: equal-weight mean of the members' standardised scores
AVG = {"avg21": ALL21,
       "avg_mat": ["default", "m60s_q", "m30s_q", "m0s_q"],
       "avg_grp": ["default", "m90t_r91", "m90t_all"],
       "avg_fresh2": ["default", "m0s_q"]}
# staleness decomposition (secondary): cut back ONLY the new-song signal or ONLY the panel signal
STALE = {}
for D in (30, 90, 180):
    STALE["stale_new%d" % D] = dict(stale_new=D); STALE["stale_pan%d" % D] = dict(stale_pan=D); STALE["stale_all%d" % D] = dict(stale=D)
