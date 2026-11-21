"""Stage 1: training-target comparison with the representation (nonaudio_gbm features) held fixed. Run: python3 -W ignore -m evalkit.run --fast variants_targets.py"""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import make_predictor
BASE = dict(hl=180)
V = {
 "t_love": dict(BASE),
 "t_love42": dict(BASE, target="love_4_2"),
 "t_love104": dict(BASE, target="love_10_4"),
 "t_strong": dict(BASE, target="strong"),
 "t_ge2": dict(BASE, target="plays_ge2"),
 "t_lplays": dict(BASE, target="lplays"),
 "t_ldays": dict(BASE, target="ldays"),
 "t_lshare": dict(BASE, target="lshare"),
 "t_grade": dict(BASE, target="grade"),
 "t_rankshare": dict(BASE, target="rank_share"),
 "t_rankplays": dict(BASE, target="rank_plays"),
 "t_love+share": dict(BASE, target="love+share"),
}
PREDICTORS = {k: make_predictor(v) for k, v in V.items()}
