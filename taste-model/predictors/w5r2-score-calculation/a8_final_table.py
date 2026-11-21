import re, sys; sys.path.insert(0, "."); from lib import *
L = open(SCR + "/run_full.txt").read().split("\n")
i = next(k for k, l in enumerate(L) if l.startswith("== [v5.1] TUNE dSAUC_80ci")); hdr = L[i + 1]; cols = re.findall(r"[A-Za-z_0-9]+", hdr.split("vs ->")[1])
row = next(l for l in L[i + 2:] if l.split()[0] == "pair_z"); vals = re.findall(r"\(([-0-9.]+), ([-0-9.]+)\)", row)
cc = [c for c in cols if c != "pair_z"]; assert len(vals) == len(cc), (len(vals), len(cc))
# point deltas from the full dump (pooled sauc)
d = pd.read_pickle(SCR + "/dumps/d_full.pkl"); f = d.fold.values; y = d.love.values
out = []
for c, (lo, hi) in zip(cc, vals):
    pt = sauc(d["score__pair_z"].values, y, f) - sauc(d["score__" + c].values, y, f); lo, hi = float(lo), float(hi)
    out.append((c, round(pt, 3), lo, hi, "POS80" if lo > 0.005 else "NEG80" if hi < -0.005 else "UNDECIDED"))
print(pd.DataFrame(out, columns=["comparator", "delta_sauc", "lo80", "hi80", "decision80"]).to_string(index=False))
