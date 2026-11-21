"""PRE-WRITTEN grid (written before any variant was scored). recipe = (members, weights, miss). Base = W3 audio_final: FINAL = [E (local L4-8 nc64 a1200), W32 (whole L4-8 nc32 a150), L37 (local L3-7 nc64 a1200)], equal weights, miss neutral.
Part 1: one-at-a-time (OAT) ranges around the defaults. Part 2: 40 seeded random joint configurations (seed 20251121). Layers are 0-based inclusive slices of the 12 MERT layers (4 -> 8 = layers 5..9 in 1-based numbering).
Part 3 (the inner-tuning grid G_TUNE) is a fixed 24-recipe subset used by the honest tuning procedure (tuned.py); it contains the default first."""
import numpy as np
from core import BASE, E, W32, L37, FINAL

def R(members=None, wts=None, miss="neutral"): return (members if members is not None else [dict(m) for m in FINAL], wts, miss)
def allm(**kw): return R([dict(m, **kw) for m in FINAL])
def localm(**kw): return R([dict(m, **kw) if m["mode"] == "local" else dict(m) for m in FINAL])
def wholem(**kw): return R([dict(m, **kw) if m["mode"] == "whole" else dict(m) for m in FINAL])

OAT = {"default": R()}
for lo, hi in [(0, 2), (0, 4), (2, 6), (3, 7), (5, 9), (6, 10), (7, 11), (0, 11), (4, 4), (8, 8), (11, 11), (2, 4), (9, 11)]:
    OAT[f"layers_{lo}_{hi}"] = allm(lo=lo, hi=hi)
for a in ["max", "top2"]: OAT[f"agg_{a}"] = localm(agg=a)
OAT["pool_max"] = wholem(pool="max")
for w in [(0, 1), (2, 3), (1, 2), (0, 3), (0,), (1,)]: OAT["wins_" + "".join(map(str, w))] = allm(wins=w)
for nc in [16, 32, 128, 256]: OAT[f"ncomp_{nc}"] = allm(ncomp=nc)
OAT["ncomp_none_local"] = localm(ncomp=None); OAT["ncomp_none_whole"] = wholem(ncomp=None)
OAT["nowhiten"] = allm(whiten=False)
for k in [0.1, 0.3, 3, 10, 30]: OAT[f"alpha_x{k}"] = R([dict(m, alpha=m["alpha"] * k) for m in FINAL])
for ms in ["min", "max", "mean"]: OAT[f"miss_{ms}"] = R(miss=ms)
OAT["only_E"] = R([E]); OAT["only_W32"] = R([W32]); OAT["only_L37"] = R([L37])
OAT["E_W32"] = R([E, W32]); OAT["E_L37"] = R([E, L37]); OAT["W32_L37"] = R([W32, L37])
OAT["wts_211"] = R(wts=[2, 1, 1]); OAT["wts_121"] = R(wts=[1, 2, 1]); OAT["wts_112"] = R(wts=[1, 1, 2])
OAT["add_whole_low"] = R(FINAL + [dict(W32, lo=0, hi=3)]); OAT["add_whole_high"] = R(FINAL + [dict(W32, lo=8, hi=11)]); OAT["add_whole_all"] = R(FINAL + [dict(W32, lo=0, hi=11)])
OAT["add_local_high"] = R(FINAL + [dict(E, lo=8, hi=11)])

def random_joint(n=40, seed=20251121):
    rng = np.random.default_rng(seed); out = {}
    for i in range(n):
        k = int(rng.integers(1, 5)); ms = []
        for _ in range(k):
            lo = int(rng.integers(0, 9)); hi = min(11, lo + int(rng.integers(0, 6)))
            mode = str(rng.choice(["whole", "local"])); nc = int(rng.choice([16, 32, 64, 128, 256]))
            a = float(10 ** rng.uniform(1.5, 3.7)); agg = str(rng.choice(["mean", "mean", "max", "top2"]))
            nw = int(rng.choice([2, 3, 4, 4, 4])); wins = tuple(sorted(rng.choice(4, nw, replace=False).tolist()))
            ms.append(dict(BASE, lo=lo, hi=hi, mode=mode, ncomp=nc, alpha=round(a, 1), agg=agg, wins=wins, pool=str(rng.choice(["mean", "mean", "max"])), whiten=bool(rng.random() < 0.8)))
        out[f"rj{i:02d}"] = R(ms, None, str(rng.choice(["neutral", "neutral", "min", "max", "mean"])))
    return out
RJ = random_joint()

# inner-tuning grid: 24 recipes (subset of OAT; default first)
G_TUNE_NAMES = ["default", "layers_0_4", "layers_2_6", "layers_5_9", "layers_6_10", "layers_7_11", "layers_0_11", "agg_max", "pool_max", "ncomp_32", "ncomp_128", "ncomp_256",
                "alpha_x0.3", "alpha_x3", "alpha_x10", "only_E", "only_W32", "only_L37", "E_W32", "add_whole_low", "add_whole_high", "add_whole_all", "wins_23", "nowhiten"]
G_TUNE = {k: OAT[k] for k in G_TUNE_NAMES}
ALL = {**OAT, **RJ}

# narrow inner-tuning grid (14 recipes: near-default neighbours only)
G_NARROW_NAMES = ["default", "layers_3_7", "layers_5_9", "ncomp_32", "ncomp_none_local", "alpha_x0.3", "alpha_x3", "agg_max", "agg_top2", "pool_max", "only_E", "add_whole_high", "wins_12", "nowhiten"]
G_NARROW = {k: OAT[k] for k in G_NARROW_NAMES}
