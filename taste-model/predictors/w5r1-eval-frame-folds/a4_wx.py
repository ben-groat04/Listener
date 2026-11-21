"""Item 2b: wx sensitivity: exposure-bucket edges (from the dump's exposure_before) and session gap (recomputed from TUNE-era streams via data.load_streams, streams < 2024-01-01 only, data.song_diag with the gap patched in this process)."""
import lib, numpy as np, pandas as pd, sys
sys.path.insert(0, str(lib.Path(__file__).resolve().parents[2]))
from evalkit import data
d = lib.dump(); MODS = lib.MODELS; out = []
st = data.load_streams(until="2024-01-01").sort_values("t", kind="stable").reset_index(drop=True)
GAPS = [30, 5, 10, 60, 120]; EXP = {}
for gap in GAPS:
    data.SESSION_GAP_MIN = gap; sd = data.song_diag(st); EXP[gap] = pd.Series(sd.exp_before.values, index=[data.h(s) for s in sd.index]); 
T = d[d.fold_set == "tune"]; chk = EXP[30].reindex(T.song.values).values; out.append(f"check: gap-30 exp_before recomputed equals dump for {np.mean(chk == T.exposure_before.values):.4f} of rows (nan {np.isnan(chk.astype(float)).sum()})")
def run(label, edges=None, gap=None, group="fold"):
    ex = None if gap is None or gap == 30 else (lambda g, gap=gap: pd.Series(EXP[gap].reindex(g.song.values).values, index=g.index).fillna(0))
    g = lib.frame(d, "tune", group, exp=ex); res = lib.evaluate(g, MODS, nboot=300, which=("wx",), new=False, edges=edges)
    pt = {m: res[m]["wx"][0] for m in MODS}; br = lib.best_ref(res, "wx")
    r = dict(variant=label, best_ref=br, ar=round(pt["artist_recent"], 3), listening=round(pt["ref_w4r1_listening"], 3), music=round(pt["ref_w4r1_music"], 3), audio=round(pt["ref_audio_final"], 3), stack3=round(pt["w5r1_stack3"], 3), duration=round(pt["duration"], 3), nonaudio=round(pt["nonaudio_gbm"], 3), tau_vs_default=None)
    for a in ("w5r1_stack3", "ref_w4r1_music", "ref_w4r1_listening", "ref_audio_final"):
        dd = lib.delta(res, a, "artist_recent", "wx"); r[f"{a[:12]}-ar"] = round(dd["d"], 3); r[f"{a[:12]}-ar_lo80"] = round(dd["lo80"], 3)
    return r, [pt[m] for m in MODS]
rows = []; base = None
VAR = [("edges default (0 | 1-2 | 3-8 | 9+)", None, None), ("edges (0|1+)", (1,), None), ("edges (0|1|2+)", (1, 2), None), ("edges (0|1-3|4-12|13+)", (1, 4, 13), None), ("edges (0|1|2-3|4-7|8-15|16+)", (1, 2, 4, 8, 16), None), ("edges (0-4|5-19|20+)", (5, 20), None), ("edges (0|1-5|6+)", (1, 6), None)]
VAR += [(f"gap {g} min, default edges", None, g) for g in GAPS[1:]]
VAR += [("gap 10 min, edges (0|1|2-3|4-7|8-15|16+)", (1, 2, 4, 8, 16), 10), ("gap 120 min, edges (0|1|2-3|4-7|8-15|16+)", (1, 2, 4, 8, 16), 120)]
for lab, e, gp in VAR:
    r, sc = run(lab, e, gp)
    if base is None: base = sc
    r["tau_vs_default"] = round(lib.kendall(sc, base), 2); rows.append(r)
R = pd.DataFrame(rows); R.to_csv(lib.OUT / "a4_wx.csv", index=False); pd.set_option("display.width", 300); pd.set_option("display.max_columns", 40)
out.append("=== wx (pooled pairs within fold x exposure bucket) variants, TUNE default folds\n" + R.to_string(index=False))
out.append("\n=== distribution of exposure_before by gap (share of songs with 0 / 1-2 / 3-8 / 9+)")
for gp in GAPS:
    e = EXP[gp].reindex(T.song.values).fillna(0).values; out.append(f"gap {gp:>3}: " + ", ".join(f"{n}={np.mean(m):.2f}" for n, m in (("0", e == 0), ("1-2", (e >= 1) & (e <= 2)), ("3-8", (e >= 3) & (e <= 8)), ("9+", e >= 9))))
(lib.OUT / "a4_wx.txt").write_text("\n".join(out)); print("\n".join(out))
