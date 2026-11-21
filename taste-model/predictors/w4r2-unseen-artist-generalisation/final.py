"""w4r2-unseen-artist-generalisation: DECLARED FINAL (entry file for the full TUNE / null / LATE / HOLDOUT runs).  Code lives in predict.py (variants V, ensembles V2).
  w4r2_unseen_final       = predict.py f1_ens_ridge  : standardised mean of 4 ridge members (signal 'both' = panel + new-song targets; MERT layer-group blocks, essentia heads/embedding; alpha by artist-grouped CV inside train)
  w4r2_unseen_final_noart = f2_ens_ridge_noart       : the same with every candidate's own primary-artist training rows removed from the ridge (exact)
  w4r2_unseen_auto        = g2_auto_top3             : config chosen inside train by artist-grouped CV (top 3 of a 16-config grid), honest-procedure variant
Run from /home/user/Listener/taste-model; needs .cache/w4r2-unseen/compact.npz and compact2.npz (build_compact.py, build_compact2.py)."""
import importlib.util, os
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "predict.py")
_s = importlib.util.spec_from_file_location("w4r2_unseen_predict", _p); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
PREDICTORS = {"w4r2_unseen_final": _m.PREDICTORS["f1_ens_ridge"], "w4r2_unseen_final_noart": _m.PREDICTORS["f2_ens_ridge_noart"], "w4r2_unseen_auto": _m.PREDICTORS["g2_auto_top3"]}
