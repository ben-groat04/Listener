"""Drift of the nested procedure's margin-0 choices over cutoffs (monthly cutoffs of tune_m).  Usage: analyze_drift.py choices_fs.jsonl LABEL..."""
import sys, json, collections, numpy as np
rows = [json.loads(l) for l in open(sys.argv[1])]
for lab in sys.argv[2:]:
    d = {}
    for r in rows:
        if r["label"] == lab: d.setdefault(r["cutoff"][:10], r)
    print("== label", lab, "cutoffs", len(d))
    per = collections.defaultdict(collections.Counter); gaps = collections.defaultdict(list)
    for c, r in sorted(d.items()):
        v = {k: x for k, x in r["table"].items() if x is not None}
        if not v: ch = "none"
        else: ch = max(v, key=v.get); gaps[c[:4] + ("H1" if int(c[5:7]) <= 6 else "H2")].append(v[ch] - v.get("default", v[ch]))
        per[c[:4] + ("H1" if int(c[5:7]) <= 6 else "H2")][ch] += 1
    for p in sorted(per): print(p, "mean inner gap best-default %.3f" % (np.mean(gaps[p]) if gaps[p] else float('nan')), dict(per[p].most_common(6)))
    allc = collections.Counter(); [allc.update(c) for c in per.values()]
    fam = lambda k: "default" if k == "default" else ("recency/time (newhl,win,hl,K,P,mp)" if k.split("_")[0].rstrip("0123456789") in ("newhl", "win", "hl", "hlinf", "K", "P", "mp", "ms") or k.startswith(("hl", "K", "P", "win", "newhl", "mp", "ms")) else ("mat/hor/grp/pop" if k.startswith(("mat", "hor", "grp", "pop")) else ("target" if k.startswith("tgt") else ("blend wnew" if k.startswith("wnew") else k))))
    fc = collections.Counter(); [fc.update({fam(k): n}) for k, n in allc.items()]; print("families overall", dict(fc))
