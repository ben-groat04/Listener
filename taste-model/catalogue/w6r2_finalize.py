"""W6 round 2 finalize: essentia_check.json, itunes_clips.csv (manifest + alignment + flags), coverage_by_fold.csv, README.md, MANIFEST.txt, DONE.
    python3 -W ignore -m catalogue.w6r2_finalize ESSENTIA_RAW_JSON [--no-done]"""
import sys, json, glob, hashlib, os
import numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import data
D = data.ROOT / ".cache" / "shared-w6r2"; D1 = data.ROOT / ".cache" / "shared-w6r1"; PRE = data.ROOT / ".cache" / "shared" / "previews"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def main():
    M = pd.read_csv(D1 / "universe_membership.csv"); U = pd.read_csv(D1 / "universe_tracks.csv").set_index("trackId")
    pm = pd.read_csv(D / "previews_manifest.csv"); pm = pm[pm.ok.astype(bool)].drop_duplicates("md5"); al = pd.read_csv(D / "align.csv")
    nm = pd.read_csv(D / "itunes_lookup.csv").drop_duplicates("trackId", keep="last")
    z = set(); [z.update(map(str, np.load(f)["md5"])) for f in glob.glob(str(D / "mert_itunes/shard_*.npz"))]
    assert set(pm.md5) <= z and set(al.md5) == set(pm.md5), (len(set(pm.md5) - z), len(set(al.md5) ^ set(pm.md5)))
    c = pm[["md5", "trackId", "itunes_track_id", "bytes", "duration_s", "ok", "url_md5"]].merge(al.drop(columns=["trackId"]), on="md5", how="left")
    c["same_excerpt"] = ((c.align_offset_s.abs() <= 2) & (c.align_score >= 0.5)).astype(float); c.loc[c.align_score.isna(), "same_excerpt"] = np.nan
    c.to_csv(D / "itunes_clips.csv", index=False)
    dz = pd.read_csv(D1 / "previews_manifest.csv"); dz = dz[dz.ok.astype(bool)]; dman = pd.read_csv(PRE / "manifest.csv"); dman = dman[dman.ok.astype(bool)]
    T = M[M.group == "tried"].copy(); T["itunes_attempted"] = T.trackId.isin(nm.trackId); T["itunes"] = T.trackId.isin(pm.trackId); T["deezer"] = T.trackId.isin(dz.trackId)
    T["dev"] = T.trackId.map(lambda t: isinstance(U.loc[t, "md5"], str) and U.loc[t, "md5"] in set(dman.md5)); T["all3"] = T.itunes & T.deezer & T.dev
    T["itunes_or_deezer"] = T.itunes | T.deezer
    g = T.groupby(["slice", "fold"]).agg(tried=("trackId", "size"), itunes_attempted=("itunes_attempted", "mean"), itunes=("itunes", "mean"), deezer=("deezer", "mean"), dev=("dev", "mean"), all3=("all3", "mean"), itunes_or_deezer=("itunes_or_deezer", "mean")).round(3).reset_index()
    for s, d in T.groupby("slice"):
        g.loc[len(g)] = [s, "ALL_" + s, len(d), d.itunes_attempted.mean(), d.itunes.mean(), d.deezer.mean(), d.dev.mean(), d.all3.mean(), d.itunes_or_deezer.mean()]
    g = g.round(3); assert not g.drop(columns=[]).isna().any().any(); g.to_csv(D / "coverage_by_fold.csv", index=False); print(g.to_string(index=False))
    dist = T.drop_duplicates("trackId"); summ = dict(tried_distinct_tune=int(dist[dist.slice == "TUNE"].trackId.nunique()), itunes_clips=len(c), itunes_match_rows=int((nm.status == "match").sum()), nomatch=int((nm.status == "nomatch").sum()),
                    skipped_no_title=int((nm.status == "skipped_no_title").sum()), dev_is_itunes=int(c.dev_is_itunes.sum()), same_url=int(c.same_url.sum()), same_excerpt1=int((c.same_excerpt == 1).sum()), same_excerpt0=int((c.same_excerpt == 0).sum()), no_dev_audio=int(c.same_excerpt.isna().sum()))
    json.dump(summ, open(D / "summary.json", "w"), indent=1); print(summ)
if __name__ == "__main__": main()
