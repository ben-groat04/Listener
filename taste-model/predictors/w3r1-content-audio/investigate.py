"""Investigation of below-chance cells (TUNE): per fold, size of the training set the model sees, label balance, audio coverage of candidates, and the train-vs-test relation of the
missing-audio indicator to the label.  usage (from taste-model/):  python3 -W ignore predictors/w3r1-content-audio/investigate.py"""
import os, sys, hashlib
sys.path.insert(0, "/home/user/Listener/taste-model"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from evalkit import data, run, metrics
import predict as P
idx, _ = P._store(); rows = []
for F in run.prepare_folds(data.TUNE_CUTOFFS):
    c, tr, meta = F["c"], F["train"], F["meta"]; st = data.song_table(tr).reset_index(); st = st[st.trackId.isin(meta.index)]
    mat = st[st["first"] < c - pd.Timedelta(days=90)]; u = meta.previewUrl.reindex(mat.trackId).values
    oka = np.array([isinstance(x, str) and hashlib.md5(x.encode()).hexdigest() in idx for x in u])
    pool = F["pool"].iloc[F["order"]]; ct = F["cands"]; u2 = meta.previewUrl.reindex(ct.trackId).values
    okc = np.array([isinstance(x, str) and hashlib.md5(x.encode()).hexdigest() in idx for x in u2]); m = (pool.is_decoy == 0).values; y = pool.love.values[m]
    sc = P.PREDICTORS["ca_whole"](tr.copy(), ct, meta, c); sc_i = P.make(miss="indicator")(tr.copy(), ct, meta, c)
    rows.append(dict(fold=str(c.date()), train_mature=len(mat), train_mature_audio=int(oka.sum()), train_love_rate=round(mat.love.mean(), 3), train_love_rate_missing=round(mat.love[~oka].mean(), 3) if (~oka).any() else np.nan,
                     train_love_rate_audio=round(mat.love[oka].mean(), 3), tried=int(m.sum()), tried_pos=int(y.sum()), test_love_rate=round(y.mean(), 3), tried_audio=round(okc[m].mean(), 3),
                     test_love_rate_missing=round(y[~okc[m]].mean(), 3) if (~okc[m]).any() else np.nan, test_love_rate_audio=round(y[okc[m]].mean(), 3), auc_whole=round(metrics.auc(y, sc[m]), 3),
                     auc_whole_audio_only_rows=round(metrics.auc(y[okc[m]], sc[m][okc[m]]), 3), auc_indicator=round(metrics.auc(y, sc_i[m]), 3)))
pd.set_option("display.width", 300, "display.max_columns", 30); print(pd.DataFrame(rows).to_string(index=False))
