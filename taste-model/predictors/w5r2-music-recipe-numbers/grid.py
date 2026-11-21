"""Grid definition (written BEFORE any non-default variant was scored).  python3 grid.py writes grid.json.
OAT = one-at-a-time ranges; JOINT = 40 seeded random near-default joint configs (each parameter independently moved to an adjacent level with p=0.4);
FAMILY_AVG = selection-free average family (declared here, before scoring); SELECT_FAMILY = candidate set for nested selection (default + OAT + first 20 JOINT)."""
import json, itertools, numpy as np
D = dict(eps=1e-4, alphaA=1e4, alphaS=1e4, seg=(3, 4, 5), gbm=(80, 0.05, 3, 30, 5.0), w=(1.0, 1.0, 1.5), wm=1.0, fill="median", mfill=None)
LEVELS = dict(
    eps=[1e-5, 1e-3, 1e-2],
    alphaA=[1e3, 3e3, 3e4, 1e5], alphaS=[1e3, 3e3, 3e4, 1e5],
    seg=[(0, 1, 2, 3, 4, 5), (2, 3, 4, 5), (4, 5), (0, 1, 2)],
    gbm=[(40, 0.05, 3, 30, 5.0), (160, 0.05, 3, 30, 5.0), (80, 0.025, 3, 30, 5.0), (80, 0.1, 3, 30, 5.0), (80, 0.05, 2, 30, 5.0), (80, 0.05, 4, 30, 5.0), (80, 0.05, 3, 15, 5.0), (80, 0.05, 3, 60, 5.0), (80, 0.05, 3, 30, 1.0), (80, 0.05, 3, 30, 20.0)],
    w=[(1, 1, 0.0), (1, 1, 1.0), (1, 1, 3.0), (1, 0, 1.5), (0, 1, 1.5), (2, 1, 1.5), (1, 2, 1.5)],
    wm=[0.0, 0.5, 2.0, 3.0],
    fill=["mean", "low", "high"],
    mfill=["mean", "low", "high"])
OAT = {}
for k, vs in LEVELS.items():
    for i, v in enumerate(vs): OAT[f"oat_{k}_{i}"] = {k: v}
# adjacent levels for joint sampling: (value list including default in its natural order)
ORDER = dict(eps=[1e-5, 1e-4, 1e-3, 1e-2], alphaA=[1e3, 3e3, 1e4, 3e4, 1e5], alphaS=[1e3, 3e3, 1e4, 3e4, 1e5],
             seg=[(4, 5), (3, 4, 5), (2, 3, 4, 5), (0, 1, 2, 3, 4, 5)], gbm=[D["gbm"]] + LEVELS["gbm"], w=[(1, 1, 1.5)] + LEVELS["w"], wm=[0.5, 1.0, 2.0], fill=["median", "mean", "low", "high"])
rng = np.random.default_rng(20261121); JOINT = {}
for j in range(40):
    P = {}
    for k, lv in ORDER.items():
        cur = lv.index(D[k]) if D[k] in lv else 0
        if k in ("gbm", "w", "fill"):
            if rng.random() < 0.3: P[k] = lv[int(rng.integers(0, len(lv)))]
        elif rng.random() < 0.4:
            nxt = cur + int(rng.choice([-1, 1])); nxt = min(max(nxt, 0), len(lv) - 1)
            if lv[nxt] != D[k]: P[k] = lv[nxt]
    JOINT[f"joint_{j:02d}"] = P
FAMILY_AVG = dict(eps=[1e-5, 1e-4, 1e-3], alpha=[3e3, 1e4, 3e4], gbm=[(40, 0.05, 3, 30, 5.0), D["gbm"], (160, 0.05, 3, 30, 5.0)], wm=[0.5, 1.0, 2.0])   # full factorial 81 members, equal-weight mean of final scores, weights (1,1,1.5) fixed
SELECT_FAMILY = {"default": {}, **{k: v for k, v in OAT.items() if not k.startswith("oat_mfill") and not k.startswith("oat_fill")}, **{k: v for k, v in JOINT.items() if int(k[-2:]) < 20}}   # fill variants are excluded from selection (own section)
if __name__ == "__main__":
    json.dump(dict(default=D, OAT=OAT, JOINT=JOINT, FAMILY_AVG=FAMILY_AVG, SELECT_FAMILY=list(SELECT_FAMILY)), open("grid.json", "w"), indent=1, default=list)
    print(len(OAT), "OAT;", len(JOINT), "JOINT;", len(SELECT_FAMILY), "select family;", np.prod([len(v) for v in FAMILY_AVG.values()]), "avg family")
