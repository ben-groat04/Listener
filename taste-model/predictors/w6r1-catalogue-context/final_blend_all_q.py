"""w6r1 final candidate 'blend_all_q' (thin entry file; single model; code in predict.py of this folder).  See predict.py docstring."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import predict as _P
FEATURES = _P.FEATURES
PREDICTORS = {"w6r1_blend_all_q": _P.PREDICTORS["blend_all_q"]}
