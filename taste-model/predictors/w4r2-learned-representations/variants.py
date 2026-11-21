"""Exploration variants scored on TUNE in --fast (reported in the report); not part of the final. Same code as predict.py. Also the artist-exclusion diagnostic."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from predict import make, ens, excl, FINAL, PRM, MLP, ATT, ARP
PREDICTORS = {
    "final_excl_artist": excl(FINAL),
    "v_ridge_mean_emb": make(model="ridge", feat="emb"), "v_patchridge_emb": make(model="patchridge", feat="emb"),
    "v_mlp_mean_emb": make(model="mean", feat="emb"), "v_attn_emb": make(model="attn", feat="emb"),
    "v_attn_act": make(model="attn", feat="act"), "v_patchridge_mert": make(model="patchridge", feat="mert", alpha=1200.0, nc=64),
    "v_mlp_mert_reg": make(model="mean", feat="mert", nc=32, h=16, ep=30, drop=0.5, wd=0.1),
    "v_attn_mert_rank": make(model="attn", feat="mert", nc=32, loss="rank", pdrop=0.25),
    "v_attn_mertL": make(model="attn", feat="mertL", nc=32, pdrop=0.25),
    "v_conv_act_panel": make(model="conv", feat="act", nc=64, h=16, ep=30, drop=0.5, wd=0.1, pdrop=0.25, panel=0.5),
    "v_attn_act_panel": make(model="attn", feat="act", nc=64, h=16, ep=30, drop=0.5, wd=0.1, pdrop=0.25, panel=0.5),
    "v_patchridge_emb_panel": make(model="patchridge", feat="emb", panel=0.5),
}
