"""Assemble the W6 shared directory outputs: p1_records.csv (user + decoy records keyed by trackId and previewUrl md5), p1_coverage.csv, p2_clips.csv (manifest + alignment + flag), README/MANIFEST.
    python3 -W ignore -m catalogue.w6_finalize"""
import sys, os, glob, hashlib, json
import numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import data
from catalogue import w6_fetch as F
D = data.ROOT / ".cache" / "shared-w6r1"; SAME_OFFSET_S = 2.0; SAME_SCORE = 0.5
def main():
    U = pd.read_csv(D / "universe_tracks.csv"); M = pd.read_csv(D / "universe_membership.csv"); parts = []
    for sub, inp in (("p1_user", "in_user.csv"), ("p1_decoy", "in_decoy.csv")):
        if (D / sub / "dz_tracks.jsonl").exists(): parts.append(F.assemble(pd.read_csv(D / inp), str(D / sub)).assign(source_set=sub))
    R = pd.concat(parts, ignore_index=True); R = R.merge(U[["trackId", "md5"]].rename(columns={"md5": "previewUrl_md5"}), on="trackId", how="left")
    cols = ["trackId", "previewUrl_md5", "source_set"] + [c for c in R.columns if c not in ("trackId", "previewUrl_md5", "source_set")]; R = R[cols]
    assert R.trackId.is_unique; R.to_csv(D / "p1_records.csv", index=False)
    X = M.merge(R[["trackId", "status", "dz_has_preview", "album_genre_names", "artist_nb_fan"]], on="trackId", how="left"); X["attempted"] = X.status.notna()
    rows = []
    for (fold, g), d in X.groupby(["fold", "group"]):
        a = d[d.attempted]; rows.append(dict(fold=fold, slice=d["slice"].iloc[0], group=g, tracks=len(d), attempted=len(a), attempted_share=len(a) / len(d), matched=int((a.status == "match").sum()),
                                           matched_share_of_attempted=(a.status == "match").mean() if len(a) else np.nan, matched_with_preview=int(((a.status == "match") & a.dz_has_preview.astype(bool)).sum()),
                                           with_album_fields=int(a.album_genre_names.notna().sum()), with_artist_fields=int(a.artist_nb_fan.notna().sum())))
    C = pd.DataFrame(rows); C.to_csv(D / "p1_coverage.csv", index=False)
    pm = pd.read_csv(D / "previews_manifest.csv"); al = pd.read_csv(D / "align.csv")
    P = pm.merge(al.drop(columns=["trackId"], errors="ignore"), on="md5", how="left")
    P["same_excerpt"] = (P.align_offset_s.abs() <= SAME_OFFSET_S) & (P.align_score >= SAME_SCORE); P.loc[P.align_score.isna(), "same_excerpt"] = np.nan
    mk = set(); [mk.update(np.load(f)["md5"]) for f in glob.glob(str(D / "mert_deezer/shard_*.npz"))]; P["mert_ok"] = P.md5.isin(mk); P.to_csv(D / "p2_clips.csv", index=False)
    print(C.to_string(index=False)); print(P.ok.sum(), P.mert_ok.sum(), P.same_excerpt.value_counts(dropna=False).to_dict())
if __name__ == "__main__": main()
