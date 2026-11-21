"""Which configs the nested procedure picks per cutoff and whether they drift.  Usage: analyze_choices.py choices.jsonl"""
import sys, json, collections, numpy as np
rows = [json.loads(l) for l in open(sys.argv[1])]
seen = {}
for r in rows:   # a cutoff/label can be logged more than once (several predictors share a label): keep the first per (label, cutoff, null) 
    seen.setdefault((r["label"], r["cutoff"][:10], r["null"], r["chosen"] if False else None), r)
by = collections.defaultdict(dict)
for r in rows: by[r["label"]].setdefault(r["cutoff"][:10], r)   # same table for margin variants; chosen differs by margin, so only use label-level tables
fam = lambda c: ("default" if c == "default" else c.split("_")[0].rstrip("0123456789") if c[:3] in ("tgt", "grp", "pop", "win") else c.rstrip("0123456789"))
for lab, d in by.items():
    print("== inner spec", lab)
    for c, r in sorted(d.items()):
        t = r["table"]; vals = {k: v for k, v in t.items() if v is not None}
        if not vals: print(c, "no inner folds -> default"); continue
        v = np.array(list(vals.values())); top = sorted(vals, key=vals.get, reverse=True)[:3]
        print(c, "n_inner=%d chosen(margin0)=%s  inner best %.3f default %.3f gap %.3f | spread(SD) of inner sauc over configs %.3f | top3 %s" % (r["n_inner"], max(vals, key=vals.get), v.max(), vals.get("default", np.nan), v.max() - vals.get("default", np.nan), v.std(), top))
