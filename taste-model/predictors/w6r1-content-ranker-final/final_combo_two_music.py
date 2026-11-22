"""FINAL FILE final_combo_two_music (one model). Thin wrapper over predict.py of this folder (importlib, so the harness' own module names cannot collide). Feature kinds: FEATURES below; also reads the Deezer-excerpt MERT shards when present (shared-w6r1/mert_deezer, or sealed-feats-v1/mert-deezer); songs without such a clip use their dev-excerpt score only."""
import importlib.util, os
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "predict.py")
_s = importlib.util.spec_from_file_location("w6r1_core", _p); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
FEATURES = ("mert","essentia")
PREDICTORS = {"combo_two_music": _m.PREDICTORS["combo_two_music"]}
