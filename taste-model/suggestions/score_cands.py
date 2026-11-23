import sys, os, glob, importlib.util
sys.path.insert(0, "/home/user/Listener/taste-model")
import numpy as np, pandas as pd
from evalkit import data, features as FT
R = "/home/user/Listener/taste-model/"; O = R + ".cache/suggest/"
today = pd.Timestamp("2026-11-23")
raw = data.load_streams(until=today, _sealed=True)
tr = data.anon_streams(raw)
ma = data.load_meta_all(fill=True)
rawids = pd.Index(raw.trackId.unique()); meta = ma.reindex(rawids); meta.index = [data.h(x) for x in rawids]; meta.index.name = "trackId"
df = pd.read_csv(O + "candidates.csv"); df = df[df.audio_ok].reset_index(drop=True)
keys, arrs = [], []
for f in sorted(glob.glob(O + "mert/p*/shard_*.npz")):
    z = np.load(f); keys += [str(x) for x in z["md5"]]; arrs.append(z["feat"])
have = {k: i for i, k in enumerate(keys)}; A = np.concatenate(arrs)
df = df[df.key.isin(have)].reset_index(drop=True); print("cands with MERT", len(df))
idx, arr = FT.mert_full(); n0 = len(arr)
idx = dict(idx); 
for k, i in have.items(): idx[k] = n0 + i
FT._C["mert"] = (idx, np.concatenate([arr, A[[have[k] for k in sorted(have, key=have.get)]]]))
df["tid"] = 9 * 10**18 + np.arange(len(df))
cm = pd.DataFrame(dict(name=df.title.values, durationMs=np.nan, explicit=False, popularity=np.nan, spotifyId=None, previewUrl=df.preview.values, albumName=None, artistNames=[[a] for a in df.artist]), index=pd.Index(df.tid, name="trackId"))
meta = pd.concat([meta, cm])
cands = pd.DataFrame(dict(song=df.title, trackId=df.tid, albumId=0, artistIds=[[0]] * len(df), artist=0, trackName=df.title))
sys.path.insert(0, R + "predictors/w6r1-content-ranker-final")
spec = importlib.util.spec_from_file_location("fin", R + "predictors/w6r1-content-ranker-final/final_avg21_dev.py"); fin = importlib.util.module_from_spec(spec); spec.loader.exec_module(fin)
fn = fin.PREDICTORS["avg21_dev"]
sc = np.asarray(fn(tr.copy(), cands, meta, today), float)
X, has = FT.mert(meta, df.tid.values); print("has mert", has.mean(), "train has-audio share", FT.mert(meta, meta.index[:5000].values)[1].mean())
df["score"] = sc; df["has_mert"] = has
df["pct"] = df.score.rank(pct=True) * 100
df.drop(columns=["tid", "preview"]).sort_values("score", ascending=False).to_csv(R + "suggestions/candidates_scored.csv", index=False)
print(df.sort_values("score", ascending=False).head(15)[["title", "artist", "score", "src"]])
