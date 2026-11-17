#!/usr/bin/env python3
"""Reconcile blind vs informed readings of a video from raw stems (D5).

Usage: python3 scripts/agents/reconcile_video2.py [video_id]   (default video2; run from v1/)
Reads  data/<video>/stems/{drums,bass,other,vocals}.mp3, data/<video>/audio/song.wav,
       data/<video>/music_views/bass_roots.json
Writes data/<video>/sync/reconcile.json (deterministic: no clocks, no randomness).

Measures four disputed items:
  1. hole: per stem (10 ms RMS envelope) when it drops and returns around 1:24 to 1:29
  2. loop A form: bass-root sequence per bar from bass_roots.json
  3. drum stops: runs of drums near silence lasting >= 1.5 s before loop B
  4. first voice fragment after the narration, from the vocals stem
The section windows below (hole search 80-92 s, loop A end 156.6 s) are video2 facts passed
as defaults; override with the optional --hole-lo/--hole-hi/--narr-end arguments.
"""
import argparse
import json
import os
import sys

import numpy as np
import librosa

HOP_S = 0.01
HERE = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.normpath(os.path.join(HERE, "..", ".."))


def env_db(path):
    y, sr = librosa.load(path, sr=None, mono=True)
    h = int(round(sr * HOP_S))
    m = len(y) // h
    rms = np.sqrt((y[: m * h].reshape(m, h) ** 2).mean(axis=1))
    return 20 * np.log10(rms + 1e-9)


def runs_below(e, thr, lo_s, hi_s, min_len_s, merge_s=0.3):
    """Runs of frames below thr in [lo_s, hi_s), gaps shorter than merge_s merged, length >= min_len_s."""
    a, b = int(lo_s / HOP_S), int(hi_s / HOP_S)
    low = e[a:b] < thr
    runs, s = [], None
    for i, v in enumerate(low):
        if v and s is None:
            s = i
        if (not v) and s is not None:
            runs.append([s, i])
            s = None
    if s is not None:
        runs.append([s, len(low)])
    merged = []
    for r in runs:
        if merged and (r[0] - merged[-1][1]) * HOP_S <= merge_s:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return [(round((a + s) * HOP_S, 2), round((a + t) * HOP_S, 2)) for s, t in merged
            if (t - s) * HOP_S >= min_len_s]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", nargs="?", default="video2")
    ap.add_argument("--hole-lo", type=float, default=80.0)
    ap.add_argument("--hole-hi", type=float, default=92.0)
    ap.add_argument("--narr-end", type=float, default=157.0,
                    help="seconds after which the first non-narration voice fragment is sought")
    ap.add_argument("--loop-a-end", type=float, default=156.6)
    a = ap.parse_args()
    d = os.path.join(V1, "data", a.video)
    E = {n: env_db(os.path.join(d, "stems", n + ".mp3")) for n in ("drums", "bass", "other", "vocals")}
    out = {"video": a.video, "method": "10 ms RMS envelope (dB re full scale) of stems/*.mp3; "
           "'low' = more than 25 dB below the stem's pre-hole level (median of 1 s peak envelope, "
           "70 s to hole start); run edges are the first/last 10 ms frame of the low run (gaps <= 0.3 s merged)"}

    # 1. hole
    lo, hi = a.hole_lo, a.hole_hi
    hole = {}
    for n in ("drums", "bass", "other"):
        e = E[n]
        sec = [e[int(t * 100):int(t * 100) + 100].max() for t in range(70, int(lo) + 3)]
        ref = float(np.median(sec))
        r = runs_below(e, ref - 25, lo, hi, 1.5)
        rec = {"pre_hole_level_db": round(ref, 1), "threshold_db": round(ref - 25, 1)}
        if r:
            s, t = r[0]
            rec.update(drop_s=s, return_s=t, length_s=round(t - s, 2), floor_db=round(float(e[int(s * 100):int(t * 100)].max()), 1))
        else:
            seg = e[int(lo * 100):int(hi * 100)]
            rec.update(no_drop_below_threshold=True, min_level_db=round(float(seg.min()), 1),
                       min_at_s=round(lo + float(seg.argmin()) * HOP_S, 2))
            r8 = runs_below(e, ref - 8, lo, hi, 0.5)
            rec["dip_run_more_than_8db_down"] = r8[0] if r8 else None
        hole[n] = rec
    dr, bs = hole["drums"], hole["bass"]
    both_lo, both_hi = max(dr["drop_s"], bs["drop_s"]), min(dr["return_s"], bs["return_s"])
    hole["both_drums_and_bass_low_s"] = [both_lo, both_hi, round(both_hi - both_lo, 2)]
    hole["pad_remains_throughout"] = "no_drop_below_threshold" in hole["other"]
    hole["vocals_stem_in_hole"] = {
        "level_db_per_half_second_peak": {str(t / 2): round(float(E['vocals'][int(t * 50):int(t * 50) + 50].max()), 1)
                                          for t in range(2 * int(lo) , 2 * int(hi))}}
    hole["bar_grid_note"] = "grid downbeat anchor 88.6165 s (sync/grid_120bpm.json), bar 2.000 s"
    out["item1_hole"] = hole

    # 2. loop A form
    br = json.load(open(os.path.join(d, "music_views", "bass_roots.json")))
    bars = [b for b in br["bars"] if 28.0 <= b["start"] < a.loop_a_end]
    seq = [(b["bar"], round(b["start"], 2), b["bass"]["root"]) for b in bars]
    slots = []  # run-length of bar roots
    for bar, st, rt in seq:
        if slots and slots[-1]["root"] == rt:
            slots[-1]["bars"] += 1
        else:
            slots.append({"root": rt, "start_s": st, "first_bar": bar, "bars": 1})
    play = [s["root"] for s in slots if s["root"] is not None]
    # smallest period of the played slot sequence (None slots = hole, skipped)
    period = next((p for p in range(1, len(play)) if all(play[i] == play[i % p] for i in range(len(play)))), None)
    # slot sequence with 2-bar slots ignoring the hole: collapse consecutive equal roots across 2-bar slots
    a_beats = []
    for b in bars:
        for k, r in enumerate(b["beat_roots"]):
            if r == "A":
                a_beats.append({"bar": b["bar"], "beat": k + 1, "start_s": round(b["start"] + k * 0.5, 2)})
    g_bars = [b["bar"] for b in bars if b["bass"]["root"] == "G"]
    out["item2_loop_a"] = {
        "span_s": [28.6, a.loop_a_end],
        "bar_roots": [r for _, _, r in seq],
        "slots": slots,
        "root_slot_sequence": play,
        "period_in_slots": period,
        "bars_per_cycle": sum(s["bars"] for s in slots[:period]) if period else None,
        "bass_root_bar_counts": {r: sum(1 for _, _, x in seq if x == r) for r in sorted({x for _, _, x in seq if x})},
        "bars_without_root_claim": [bar for bar, _, r in seq if r is None],
        "A_on_beat_roots": {"count": len(a_beats), "occurrences": a_beats,
                            "G_slots_total": sum(1 for s in slots if s["root"] == "G"),
                            "note": "beat_roots are per-beat pitch classes (0.5 s); A appears only as a brief pickup in some G to D transitions"},
        "bass_roots_json_loop_summary": br["loops"]["loop_A_pre_hole"]["bass_root_bar_counts"],
    }

    # 3. drum stops
    de = E["drums"]
    ref_d = float(np.median([de[int(t * 100):int(t * 100) + 100].max() for t in range(30, 60)]))
    stops = runs_below(de, ref_d - 25, 28.0, a.loop_a_end, 1.5)
    sparse = {}
    for (lo2, hi2) in ((70.0, 80.0),):
        seg = de[int(lo2 * 100):int(hi2 * 100)]
        sparse[f"{lo2}-{hi2}"] = {"max_db": round(float(seg.max()), 1), "median_db": round(float(np.median(seg)), 1),
                                  "frames_above_threshold_pct": round(float((seg >= ref_d - 25).mean() * 100), 1)}
    out["item3_drum_stops"] = {
        "reference_level_db_30_to_60s": round(ref_d, 1), "threshold_db": round(ref_d - 25, 1),
        "stops_at_least_1p5_s": [{"from_s": s, "to_s": t, "length_s": round(t - s, 2)} for s, t in stops],
        "window_70_to_80s_drums": sparse,
        "note": "shorter off-beat gaps of 0.5 to 1.0 s occur throughout the groove and are not counted",
    }

    # 4. first voice fragment after the narration
    ve = E["vocals"]
    nar = [t for t in np.arange(30, a.narr_end, 0.01) if ve[int(round(t * 100))] > -35]
    narr_last = round(float(nar[-1]), 2) if nar else None
    a0 = int(a.narr_end * 100)
    cand = {}
    for thr in (-55, -35, -25):
        idx = np.where(ve[a0:] > thr)[0]
        cand[str(thr)] = round((a0 + int(idx[0])) * HOP_S, 2) if len(idx) else None
    # sustained: first frame from which >= 50% of the next 0.5 s is above -35 dB
    sus = None
    for i in range(a0, len(ve) - 50):
        if ve[i] > -35 and (ve[i:i + 50] > -35).mean() >= 0.5:
            sus = round(i * HOP_S, 2)
            break
    blip = {}
    if cand["-55"] is not None:
        j = int(cand["-55"] * 100)
        blip = {"first_frame_above_-55_db_s": cand["-55"],
                "peak_db_within_1s": round(float(ve[j:j + 100].max()), 1)}
    out["item4_first_voice_fragment"] = {
        "search_from_s": a.narr_end, "last_narration_frame_above_-35_db_before_search_s": narr_last,
        "first_frame_above_db": cand, "first_sustained_fragment_start_s": sus, "faint_blip": blip,
        "vocals_stem_background_db": [round(float(np.percentile(ve[a0:a0 + 4000], 10)), 1),
                                      round(float(np.percentile(ve[a0:a0 + 4000], 50)), 1)],
        "per_0p25s_peak_db_201_to_210s": {str(t): round(float(ve[int(t * 100):int(t * 100) + 25].max()), 1)
                                          for t in np.arange(201.0, 210.0, 0.25)},
    }

    path = os.path.join(d, "sync", "reconcile.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote", path)


if __name__ == "__main__":
    sys.exit(main())
