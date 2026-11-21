"""Merge the truncated-history model score onto the d1 dump rows (tune, tune_m) -> dumps/d_merged_trunc.pkl"""
import sys; sys.path.insert(0, "."); from lib import *
a = pd.read_pickle(SCR + "/dumps/d1.pkl"); b = pd.read_pickle(SCR + "/dumps/d_trunc12.pkl")
b = b[b.fold_set.isin(["tune", "tune_m"])][["fold_set", "fold", "song", "score__pairz_trunc12"]]
a = a[a.fold_set.isin(["tune", "tune_m"])].merge(b, on=["fold_set", "fold", "song"], how="left"); assert a.score__pairz_trunc12.notna().all()
a.to_pickle(SCR + "/dumps/d_merged_trunc.pkl")
