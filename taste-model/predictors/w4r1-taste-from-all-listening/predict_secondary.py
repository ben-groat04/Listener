"""SECONDARY models (rule 1: NOT the primary predictor). Imports the primary members from predict.py; adds
 sec_hist_*: w4r1_final z-score + w * z(log1p plays by the candidate's primary artist in the last 180 d before cutoff)  [content PLUS artist history]
 sec_cap  : content-only, panel members' PCA components capped by number of panel songs (sparse early folds fix); TUNE-seen variant, not declared before.
Usage: python3 -W ignore -m evalkit.run --fast predictors/w4r1-taste-from-all-listening/predict_secondary.py"""
import importlib.util, os, numpy as np, pandas as pd
_p = importlib.util.spec_from_file_location("w4r1_main", os.path.join(os.path.dirname(os.path.abspath(__file__)), "predict.py"))
M = importlib.util.module_from_spec(_p); _p.loader.exec_module(M)

def _z(x):
    return (x - x.mean()) / (x.std() + 1e-9)

def hist(train, cands, cutoff, days=180):
    tr = train[train.t >= np.datetime64(cutoff - pd.Timedelta(days=days))]
    c = tr.groupby("artist").size()
    return np.log1p(cands.artist.map(c).fillna(0).values.astype(float))

def mk_hist(w, days=180):
    base = M.make(*M.NEW, *M.PAN)
    def predict(train, cands, meta, cutoff):
        s = base(train, cands, meta, cutoff); h = hist(train, cands, cutoff, days)
        return s + w * h / 1.0      # s is a mean of standardised scores (unit-ish scale); h in log1p-count units
    return predict

def mk_cap():
    def predict(train, cands, meta, cutoff):
        from evalkit.data import song_table
        n = len(song_table(train))
        # fewer songs -> fewer components: cap 128 by n/6 and 64 by n/12 (n = songs in train streams)
        pan = [dict(M.PAN[0], ncomp=int(min(128, max(16, n // 6)))), dict(M.PAN[1], ncomp=int(min(64, max(16, n // 12))))]
        return M.make(*M.NEW, *pan)(train, cands, meta, cutoff)
    return predict

PREDICTORS = {"sec_hist_w0.3": mk_hist(0.3), "sec_hist_w1": mk_hist(1.0), "sec_cap": mk_cap()}
