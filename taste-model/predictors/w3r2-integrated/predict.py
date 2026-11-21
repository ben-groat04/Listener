"""w3r2-integrated: blend of history-GBM members (round-1 w3r1-training-signal code) and an artist-free MERT audio member (w3r1-content-audio code).
Each member is standardised with statistics of its OWN scores over TRAINING songs only (candidate independent). Missing audio -> the audio member
gets the train-derived neutral value (median train score); audio-bearing GBM member gets NaN audio features (explicit au_missing flag as in round 1).
Usage (from /home/user/Listener/taste-model):  python3 -W ignore -m evalkit.run predictors/w3r2-integrated/predict.py --fast
Entries in PREDICTORS: see bottom. Members: H = history GBM (rank_plays target, 365 d window, 120 d half-life), HA = H + CLAP similarity features,
A = MERT audio-only ensemble (ca_ens), AR = artist_recent (frequency statistic).
"""
import sys, importlib.util
HERE = __file__.rsplit("/", 1)[0]; R1 = HERE.rsplit("/", 1)[0]
sys.path.insert(0, R1 + "/w3r1-training-signal")
import numpy as np
import core as TS
_s = importlib.util.spec_from_file_location("w3r1_ca", R1 + "/w3r1-content-audio/predict.py"); CA = importlib.util.module_from_spec(_s); _s.loader.exec_module(CA)

G = dict(hl=120, window=365, gbm=dict(max_iter=60), target="rank_plays")
Ga = dict(G, rep="base+a")
AR = dict(fn="artist_recent")
_L3 = (dict(layers=(0, 3)), dict(layers=(4, 7)), dict(layers=(8, 11)))
A_ens = CA.make_ens(*_L3, mode="local")

def blend(members, weights):
    """members: dict specs (history members, core.make_blend format) or callables (audio predict fns, already train-standardised)."""
    hist = [(m, w) for m, w in zip(members, weights) if isinstance(m, dict)]
    aud = [(m, w) for m, w in zip(members, weights) if callable(m)]
    hb = TS.make_blend([m for m, _ in hist], [w for _, w in hist]) if hist else None
    def predict(train, cands, meta, cutoff):
        tot = hb(train, cands, meta, cutoff) if hb else 0
        for f, w in aud: tot = tot + w * f(train, cands, meta, cutoff)
        return tot
    return predict

A_missing_only = CA.make(miss="indicator")   # diagnostic: uses ONLY whether a preview exists (sign from train love rates of songs with / without audio)
PREDICTORS = {
    "w2i_final": blend([G, Ga, A_ens, AR], [1, 1, 1, 1]),   # FINAL (equal weights, chosen as the least tuned of the near-tied TUNE variants)
    "w2i_noaudio": blend([G, AR], [1, 1]),                   # ablation 1: audio inputs removed (no CLAP features, no MERT member)
    "w2i_nohist": blend([A_ens], [1]),                       # ablation 2: history inputs removed (artist-free MERT audio only)
    "w2i_missing_only": A_missing_only,                      # diagnostic: audio-missingness indicator alone
}
