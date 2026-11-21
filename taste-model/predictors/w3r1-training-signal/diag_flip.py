"""Diagnostic (not a predictor): in the TRAIN history of each cutoff, love rate of matured songs first played in the last 365 d, split by new-artist flag
(artist never played before the song's first play) and by familiarity tercile. Shows whether the familiarity->love relation is already visible before the cutoff."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0]); sys.path.insert(0, "/home/user/Listener/taste-model")
import numpy as np, pandas as pd
from evalkit import run
import core
for c in ["2022-10-01", "2023-04-01", "2023-10-01", "2024-01-01", "2024-04-01", "2024-07-01", "2024-10-01"]:
    F = run.prepare_folds([c])[0]; rows, X, *_ = core.build(F["train"], F["c"], F["meta"])
    m = rows.age.values <= 365; r = rows[m]; x = X[m]
    new = x.new_artist.values > 0; fam = pd.qcut(x.ap_all.rank(method="first"), 3, labels=["low", "mid", "high"])
    g = r.groupby([fam.values]).love.mean()
    print(c, "n", m.sum(), "love new-artist %.2f (n=%d) known %.2f (n=%d)" % (r.love[new].mean(), new.sum(), r.love[~new].mean(), (~new).sum()),
          "| by familiarity tercile low/mid/high:", " ".join("%.2f" % v for v in g.values))
