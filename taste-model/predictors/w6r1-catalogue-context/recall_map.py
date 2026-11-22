"""Groundwork: reachability map of the Deezer related-artist graph (dev TUNE only, labels allowed).  For each TUNE fold: seeds = top-K pre-cutoff artists by decayed plays (K=10, 20, 40);
share of loved / tried-not-loved tried songs whose artist is within 1, 2, 3 hops of the seeds (hop 0 = the seed itself); sizes of the walk.  This is a recall map, not a candidate list.
Inputs: DIR/fold_*.json + DIR/dump.pkl (from recall_export.py), shared-w6r1/p1_records.csv, .cache/w6r1-catalogue-context/{artist_related,artist_top}.jsonl.
Directed forward edges (artist -> its Deezer related list).  hop3 uses the undirected meet-in-the-middle approximation (documented in the output).  Usage: python3 recall_map.py DIR"""
import sys, json, glob, numpy as np, pandas as pd
D = sys.argv[1]; ROOT = "/home/user/Listener/taste-model"
R = pd.read_csv(f"{ROOT}/.cache/shared-w6r1/p1_records.csv"); R = R[R.status == "match"].drop_duplicates("dz_artist_id").set_index("dz_artist_id")
rel = {int(a): [int(x) for x in str(s).split("|") if x != "nan"] for a, s in R.artist_related_ids.items()}
for l in open(f"{ROOT}/.cache/w6r1-catalogue-context/artist_related.jsonl"):
    r = json.loads(l); rel.setdefault(r["artist_id"], r["related"])
topn = {}
for l in open(f"{ROOT}/.cache/w6r1-catalogue-context/artist_top.jsonl"):
    r = json.loads(l); topn[r["artist_id"]] = len(r["top"])
d = pd.read_pickle(f"{D}/dump.pkl"); fs = d.fold_set.unique()[0]; d = d[d.fold_set == fs].copy()
rows = []; sizes = []
for f in sorted(glob.glob(f"{D}/fold_*.json")):
    j = json.load(open(f)); cut = j["cutoff"]; cm = {int(k): v for k, v in j["cand_artist_dz"].items()}
    x = d[d.cutoff.astype(str).str[:10] == cut]; assert len(x) > 0, cut
    for K in (10, 20, 40):
        seeds = [s["dz"] for s in j["seeds"] if s["dz"]][:K]
        h0 = set(seeds); h1 = set().union(*[set(rel.get(s, [])) for s in seeds]) - h0
        miss = [a for a in h1 if a not in rel]; assert not miss or K == 40 or len(miss) < 1, (cut, K, len(miss))
        h2 = set().union(*[set(rel.get(a, [])) for a in h1 if a in rel]) - h0 - h1
        sizes.append(dict(fold=cut, K=K, seeds=len(seeds), hop1_artists=len(h1), hop2_artists=len(h2), hop1_hop2_unfetched=len(miss)))
        for _, r in x.iterrows():
            t = cm.get(int(r.artist)); lv = int(r.love); na = int(r.new_artist)
            if t is None: lvl = "unmatched"
            else:
                lvl = 0 if t in h0 else 1 if t in h1 else 2 if t in h2 else None
                if lvl is None:
                    ts = set(rel.get(t, []))
                    lvl = 3 if (ts & h2) or (ts & h1) and False else 4
                    # undirected hop-3: some related artist y of t is in the hop-2 set, or t is in the related list of some hop-2 artist whose list is known
                    if lvl == 4 and any(t in rel.get(a, ()) for a in h2 if a in rel): lvl = 3
            rows.append(dict(fold=cut, K=K, love=lv, new_artist=na, lvl=lvl))
A = pd.DataFrame(rows); A["lvl"] = A.lvl.astype(str)
assert not A.isna().any().any()
out = []
for (K, na), g in A.groupby(["K", "new_artist"]):
    for lv, h in g.groupby("love"):
        m = h[h.lvl != "unmatched"]; n = len(h)
        out.append(dict(K=K, new_artist=na, love=lv, n=n, matched=len(m), **{f"<=hop{k}_of_all": float(m.lvl.isin([str(i) for i in range(k + 1)]).sum() / n) for k in (1, 2, 3)},
                        **{f"<=hop{k}_of_matched": float(m.lvl.isin([str(i) for i in range(k + 1)]).mean()) for k in (1, 2, 3)}))
O = pd.DataFrame(out).round(3); pd.set_option("display.width", 250); print(O.to_string(index=False))
# enrichment: love rate among new-artist songs reached within hop2 vs not reached (matched only)
for K in (10, 20, 40):
    g = A[(A.K == K) & (A.new_artist == 1) & (A.lvl != "unmatched")]; r = g.lvl.isin(["1", "2"])
    print(f"K={K} new-artist matched songs n={len(g)}: love rate reached<=hop2 {g[r].love.mean():.3f} (n={r.sum()}), not reached {g[~r].love.mean():.3f} (n={(~r).sum()}); hop1 only {g[g.lvl=='1'].love.mean():.3f} (n={(g.lvl=='1').sum()})")
S = pd.DataFrame(sizes); S["tracks_est_hop1"] = S.hop1_artists * 50; S["tracks_est_hop2"] = S.hop2_artists * 50
print(S.groupby("K")[["seeds", "hop1_artists", "hop2_artists", "tracks_est_hop1", "tracks_est_hop2"]].mean().round(0).to_string())
print("per-fold hop1/hop2 artists at K=20:"); print(S[S.K == 20][["fold", "hop1_artists", "hop2_artists"]].to_string(index=False))
print("mean top-list length in cache (tracks per artist, cap 100):", round(np.mean(list(topn.values())), 1), "n artists", len(topn))
print("folds", A.fold.nunique(), "rows", len(A))
A.to_csv(f"{D}/recall_rows.csv", index=False); O.to_csv(f"{D}/recall_table.csv", index=False)
