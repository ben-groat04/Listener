"""w3r2-integrated: blend of history-GBM members (round-1 w3r1-training-signal code) and an artist-free MERT audio member (w3r1-content-audio code).
Each member is standardised with statistics of its OWN scores over TRAINING songs only (candidate independent). Missing audio -> the audio member
gets the train-derived neutral value (median train score); audio-bearing GBM member gets NaN audio features (explicit au_missing flag as in round 1).
Usage (from /home/user/Listener/taste-model):  python3 -W ignore -m evalkit.run predictors/w3r2-integrated/predict.py --fast
Entries in PREDICTORS: see bottom. Members: H = history GBM (rank_plays target, 365 d window, 120 d half-life), HA = H + CLAP similarity features,
A = MERT audio-only ensemble (ca_ens), AR = artist_recent (frequency statistic), Am = A with meta (duration etc.) columns.
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
A_ens_meta = CA.make_ens(*_L3, mode="local", meta=True)
A_ens_rank = CA.make_ens(*_L3, mode="local", target="rank", hl=365)

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

PREDICTORS = {
    "w2i_hist_audio": blend([G, Ga, A_ens], [1, 1, 2]),             # history GBMs + audio-only, no plain artist-frequency member
    "w2i_hist_audio_ar": blend([G, Ga, A_ens, AR], [1, 1, 2, 1]),
    "w2i_audio": blend([A_ens], [1]),
    "w2i_hist": blend([G, Ga], [1, 1]),
    "w2i_ha_meta_ar": blend([G, Ga, A_ens_meta, AR], [1, 1, 2, 1]),
    "w2i_ha_rank_ar": blend([G, Ga, A_ens_rank, AR], [1, 1, 2, 1]),
    "w2i_ha_ar2": blend([G, Ga, A_ens, AR], [1, 1, 2, 2]),
    "w2i_ha_eq_ar": blend([G, Ga, A_ens, AR], [1, 1, 1, 1]),
    "w2i_g_a_ar": blend([G, A_ens, AR], [1, 2, 1]),
    "w2i_ga_a_ar": blend([Ga, A_ens, AR], [1, 2, 1]),
    "w2i_ha_a3_ar": blend([G, Ga, A_ens, AR], [1, 1, 3, 1]),
}
