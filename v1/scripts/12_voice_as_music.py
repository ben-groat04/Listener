"""Voice as a musical element (video-agnostic; run as VID=<name> python3 12_voice_as_music.py, or pass --vid <name>; no default video).
Inputs (all under v1/data/<VID>/): stems_raw/htdemucs/song/{vocals,bass,drums,other}.wav, audio/song.wav,
  audio_features/summary.json (key_whole_song_top3), audio_features/beat_times.json, music_views/chords.json (optional),
  lyrics/*.json (+ *_doubtful.txt) (optional, whisper segments with avg_logprob / no_speech_prob).
Five blocks, every number is a measurement (OBS); nothing is concluded here:
  1 vad        voiced segments from the vocals stem with a BLEED RULE: a 10 ms block counts as voice only if the vocal-stem
               level is within --bleed-db of the mix level (default 20 dB) and above an absolute floor (--floor-db, default -55 dBFS),
               so music bleeding into the vocal stem is not counted as speech. Gaps < --gap s are closed, segments < --min-seg s dropped.
  2 pitch      pYIN f0 per voiced segment; interval to the song's tonic (whole-song top key) in semitones (0-11, plus cents off
               equal temperament, A=440); whether the median pitch class is in the key's scale and whether it is a chord tone of the
               chords.json chord at that time; frame-level chord-tone share with the chance share for the same chords.
               NOTE: speech f0 is not an intended note; these are measurements of where it happens to sit.
  3 beat_phase onset of each kept segment against the beat grid: phase 0..1 within the beat interval, signed offset to nearest beat (ms),
               circular mean and resultant length R (uniform chance expectation about 1/sqrt(n)).
  4 ducking    accompaniment (bass+drums+other stems) and other-stem level (dB RMS): during voiced segments, in the 1 s margin
               before/after them, and elsewhere (not within 1 s of any voiced segment); per-segment change onset-minus-previous-1 s.
  5 whisper_filter  whisper segments from lyrics/*.json; a segment is doubtful if listed in its *_doubtful.txt, or avg_logprob < -1.0,
               or no_speech_prob > 0.6. VAD segments that overlap only doubtful whisper text (>=50 % of their length, no reliable overlap)
               are dropped from blocks 2-4 and listed. Also compares VAD voiced time with whisper time (plausibility check).
Instrumental / no voice: if kept voiced time < --min-total s the result is status 'no voice found' with the measured vocal-to-mix levels.
Outputs: data/<VID>/music_views/voice_as_music.json and .txt (or $LISTENER_OUT)."""
import os, sys, json, glob, re, argparse
import numpy as np
import soundfile as sf
from scipy import signal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from _common import require_vid

ap = argparse.ArgumentParser()
ap.add_argument("--vid")
ap.add_argument("--bleed-db", type=float, default=20.0, help="vocal block counts only if within this many dB of the mix level")
ap.add_argument("--floor-db", type=float, default=-55.0, help="absolute vocal-stem floor in dBFS")
ap.add_argument("--gap", type=float, default=0.25)
ap.add_argument("--min-seg", type=float, default=0.30)
ap.add_argument("--min-total", type=float, default=1.0)
a = ap.parse_args()
if a.vid: os.environ["VID"] = a.vid
VID = require_vid()
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
D = os.path.join(root, f"v1/data/{VID}")
O = os.environ.get("LISTENER_OUT") or os.path.join(D, "music_views"); os.makedirs(O, exist_ok=True)
ST = os.path.join(D, "stems_raw/htdemucs/song")
SONG = os.path.join(D, "audio/song.wav")
for p in (SONG, os.path.join(ST, "vocals.wav")):
    if not os.path.exists(p): sys.exit(f"ERROR: {p} missing (run extraction / stem separation first)")
EPS = 1e-10
HOP_S = 0.01
def db(x): return 20 * np.log10(np.maximum(x, EPS))
def rd(p):
    x, sr = sf.read(p, dtype="float32", always_2d=True)
    return x.mean(axis=1), sr
def rms_blocks(x, sr):
    n = int(round(sr * HOP_S)); k = len(x) // n
    return np.sqrt((x[:k * n].reshape(k, n).astype(np.float64) ** 2).mean(axis=1))

voc, sr = rd(os.path.join(ST, "vocals.wav")); mix, sr2 = rd(SONG)
if sr2 != sr: sys.exit(f"ERROR: sample-rate mismatch vocals {sr} vs song {sr2}")
nmin = min(len(voc), len(mix)); voc, mix = voc[:nmin], mix[:nmin]
dur = nmin / sr
rv, rm = rms_blocks(voc, sr), rms_blocks(mix, sr)
dv, dm = db(rv), db(rm)
nb = len(rv)
tb = np.arange(nb) * HOP_S

# ---- 1 VAD with bleed rule
ok = (dv >= dm - a.bleed_db) & (dv >= a.floor_db)
ok_nobleed = dv >= a.floor_db  # for reporting how much the bleed rule removed
def runs(mask):
    m = np.concatenate([[0], mask.astype(np.int8), [0]]); d = np.diff(m)
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))
def clean(mask):
    r = runs(mask); out = []
    for s, e in r:
        if out and (s - out[-1][1]) * HOP_S < a.gap: out[-1] = (out[-1][0], e)
        else: out.append((s, e))
    return [(s, e) for s, e in out if (e - s) * HOP_S >= a.min_seg]
segs_all = clean(ok)
segs_nobleed = clean(ok_nobleed)
vad_all = [{"start_s": round(s * HOP_S, 2), "end_s": round(e * HOP_S, 2), "dur_s": round((e - s) * HOP_S, 2),
            "vocal_db_mean": round(float(dv[s:e].mean()), 1), "mix_db_mean": round(float(dm[s:e].mean()), 1),
            "vocal_minus_mix_db": round(float((dv[s:e] - dm[s:e]).mean()), 1)} for s, e in segs_all]
tot_vad = sum(x["dur_s"] for x in vad_all)
tot_nobleed = sum((e - s) * HOP_S for s, e in segs_nobleed)

# ---- 5 whisper (computed first, filters before 2-4)
def ts(t):
    m = re.match(r"(\d+):(\d+(?:\.\d+)?)", t); return int(m.group(1)) * 60 + float(m.group(2))
wfiles = sorted(glob.glob(os.path.join(D, "lyrics/*.json")))
wfiles = [f for f in wfiles if "translate" not in os.path.basename(f)]  # translations repeat the transcribe timings
wsrc = []
for f in wfiles:
    try: j = json.load(open(f))
    except Exception: continue
    segs = j.get("segments") if isinstance(j, dict) else j
    if not segs: continue
    dpath = f[:-5] + "_doubtful.txt"; dtimes = []
    if os.path.exists(dpath):
        for ln in open(dpath):
            m = re.match(r"\[([\d:.]+) - ([\d:.]+)\]", ln)
            if m: dtimes.append((ts(m.group(1)), ts(m.group(2))))
    items = []
    for sg in segs:
        s, e = float(sg["start"]), float(sg["end"])
        lp, ns = sg.get("avg_logprob"), sg.get("no_speech_prob")
        reasons = []
        if any(abs(s - ds) < 0.06 and abs(e - de) < 0.06 for ds, de in dtimes): reasons.append("listed_in_doubtful_txt")
        if lp is not None and lp < -1.0: reasons.append("avg_logprob<-1.0")
        if ns is not None and ns > 0.6: reasons.append("no_speech_prob>0.6")
        items.append({"start_s": round(s, 2), "end_s": round(e, 2), "avg_logprob": None if lp is None else round(lp, 2),
                      "no_speech_prob": None if ns is None else round(ns, 2), "doubtful": bool(reasons), "reasons": reasons})
    wsrc.append({"file": os.path.basename(f), "lang": j.get("lang") if isinstance(j, dict) else None,
                 "lang_prob": j.get("lang_prob") if isinstance(j, dict) else None, "segments": items})
def ov(s1, e1, s2, e2): return max(0.0, min(e1, e2) - max(s1, s2))
primary = None
if wsrc:
    vocs = [w for w in wsrc if "vocals" in w["file"]]
    primary = (vocs or wsrc)[0]
whisper_block = {"status": "no whisper segments found: filter not applied" if not wsrc else "applied",
                 "rule": "doubtful if in *_doubtful.txt, avg_logprob<-1.0 or no_speech_prob>0.6; VAD segment dropped if >=50% of its length overlaps doubtful whisper and none overlaps reliable whisper",
                 "primary_source": primary["file"] if primary else None, "sources": [], "dropped_vad_segments": []}
for w in wsrc:
    segs = w["segments"]; rel = [x for x in segs if not x["doubtful"]]; dbt = [x for x in segs if x["doubtful"]]
    def covered(lst):
        m = np.zeros(nb, bool)
        for x in lst: m[int(x["start_s"] / HOP_S):int(x["end_s"] / HOP_S)] = True
        return m
    mv = np.zeros(nb, bool)
    for s, e in segs_all: mv[s:e] = True
    mr, md = covered(rel), covered(dbt)
    whisper_block["sources"].append({
        "file": w["file"], "lang": w["lang"], "lang_prob": w["lang_prob"], "n_segments": len(segs), "n_doubtful": len(dbt),
        "whisper_time_s": round(float(covered(segs).sum() * HOP_S), 1), "whisper_reliable_time_s": round(float(mr.sum() * HOP_S), 1),
        "vad_time_s": round(tot_vad, 1),
        "vad_time_overlapping_any_whisper_s": round(float((mv & covered(segs)).sum() * HOP_S), 1),
        "vad_time_overlapping_reliable_whisper_s": round(float((mv & mr).sum() * HOP_S), 1),
        "reliable_whisper_time_with_vad_s": round(float((mv & mr).sum() * HOP_S), 1)})
keep = []
for v in vad_all:
    s, e = v["start_s"], v["end_s"]; v["whisper_support"] = "no_whisper_data"
    if primary:
        r = sum(ov(s, e, x["start_s"], x["end_s"]) for x in primary["segments"] if not x["doubtful"])
        d = sum(ov(s, e, x["start_s"], x["end_s"]) for x in primary["segments"] if x["doubtful"])
        v["whisper_support"] = "reliable" if r > 0 else ("doubtful_only" if d >= 0.5 * (e - s) else ("doubtful_partial" if d > 0 else "none"))
        if v["whisper_support"] == "doubtful_only":
            whisper_block["dropped_vad_segments"].append({"start_s": s, "end_s": e}); continue
    keep.append(v)
tot_keep = sum(v["dur_s"] for v in keep)

out = {"vid": VID, "duration_s": round(dur, 2), "evidence": "OBS (measurements only; no interpretation is stated)",
       "params": {"bleed_db": a.bleed_db, "floor_db": a.floor_db, "gap_s": a.gap, "min_seg_s": a.min_seg, "min_total_s": a.min_total, "hop_s": HOP_S}}
out["vad"] = {"n_segments_before_filter": len(vad_all), "voiced_time_before_filter_s": round(tot_vad, 1),
              "voiced_time_without_bleed_rule_s": round(tot_nobleed, 1),
              "n_segments_kept": len(keep), "voiced_time_kept_s": round(tot_keep, 1),
              "voiced_share_of_track": round(tot_keep / dur, 3) if dur else None,
              "max_vocal_minus_mix_db": round(float((dv - dm).max()), 1), "vocal_peak_db": round(float(dv.max()), 1),
              "segments": keep}
out["whisper_filter"] = whisper_block

if tot_keep < a.min_total:
    out["status"] = "no voice found"
    out["note"] = (f"OBS: kept voiced time {tot_keep:.1f} s < {a.min_total} s under bleed rule ({a.bleed_db} dB below mix, floor {a.floor_db} dBFS). "
                   f"Without the bleed rule the vocal stem exceeds the floor for {tot_nobleed:.1f} s. Blocks pitch, beat_phase, ducking not computed.")
    for k in ("pitch", "beat_phase", "ducking"): out[k] = {"status": "not computed (no voice found)"}
else:
    out["status"] = "voice found"
    # ---- 2 pitch
    import librosa
    NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    PC = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    tonic = None; keyname = None
    try:
        sm = json.load(open(os.path.join(D, "audio_features/summary.json")))
        keyname = sm["key_whole_song_top3"][0][0]; kr, km = keyname.split()
        tonic = (PC[kr], km)
    except Exception as ex:
        out["pitch_note"] = f"tonic unavailable ({ex}); intervals not computed"
    chords = []
    cp = os.path.join(D, "music_views/chords.json")
    if os.path.exists(cp): chords = json.load(open(cp))
    def chord_pcs(name):
        m = re.match(r"([A-G][#b]?)(.*)", name or "")
        if not m or m.group(1) not in PC: return None
        r = PC[m.group(1)]; q = m.group(2)
        third = 3 if (q.startswith("m") and not q.startswith("maj")) or q.startswith("dim") else (5 if q.startswith("sus4") else 4)
        if q.startswith("sus2"): third = 2
        fifth = 6 if q.startswith("dim") else (8 if "aug" in q else 7)
        s = {r % 12, (r + third) % 12, (r + fifth) % 12}
        if "maj7" in q: s.add((r + 11) % 12)
        elif "7" in q: s.add((r + 10) % 12)
        return s
    def chord_at(t):
        for c in chords:
            if c["start"] <= t < c["end"]: return c["chord"]
        return None
    SCALE = {"major": {0, 2, 4, 5, 7, 9, 11}, "minor": {0, 2, 3, 5, 7, 8, 10}}
    v22 = signal.resample_poly(voc, 22050, sr).astype(np.float32) if sr != 22050 else voc
    HOP = 441
    pitch_segs = []; tot_frames = 0; tot_ct = 0; chance_sum = 0.0; tot_chord_frames = 0
    for v in keep:
        a0, b0 = int(v["start_s"] * 22050), int(v["end_s"] * 22050)
        y = v22[a0:b0]
        rec = {"start_s": v["start_s"], "end_s": v["end_s"]}
        if len(y) < 2048:
            rec["f0"] = "segment too short for pYIN"; pitch_segs.append(rec); continue
        f0, vf, vp = librosa.pyin(y, fmin=65, fmax=800, sr=22050, frame_length=2048, hop_length=HOP)
        tt = v["start_s"] + np.arange(len(f0)) * HOP / 22050
        m = vf & np.isfinite(f0)
        rec["n_frames"] = int(len(f0)); rec["n_pitched_frames"] = int(m.sum()); rec["pitched_fraction"] = round(float(m.mean()), 2)
        if m.sum() < 5:
            rec["f0"] = "too few pitched frames (<5)"; pitch_segs.append(rec); continue
        f = f0[m]; med = float(np.median(f)); midi = 69 + 12 * np.log2(med / 440.0)
        rec["f0_median_hz"] = round(med, 1); rec["f0_p10_p90_hz"] = [round(float(np.percentile(f, 10)), 1), round(float(np.percentile(f, 90)), 1)]
        rec["nearest_note"] = NAMES[int(round(midi)) % 12] + str(int(round(midi)) // 12 - 1); rec["cents_from_nearest_semitone"] = int(round((midi - round(midi)) * 100))
        if tonic:
            pc = int(round(midi)) % 12; iv = (pc - tonic[0]) % 12
            rec["interval_to_tonic_semitones"] = iv; rec["in_scale_of_key"] = iv in SCALE[tonic[1]]
        ctmid = chord_at(float(np.median(tt[m])))
        rec["chord_at_median_time"] = ctmid
        cp_ = chord_pcs(ctmid)
        if cp_ is not None: rec["median_pc_is_chord_tone"] = (int(round(midi)) % 12) in cp_
        nct = 0; nfr = 0; ch = 0.0
        for t_, f_ in zip(tt[m], f):
            cs = chord_pcs(chord_at(float(t_)))
            if cs is None: continue
            nfr += 1; ch += len(cs) / 12.0
            if (int(round(69 + 12 * np.log2(f_ / 440.0))) % 12) in cs: nct += 1
        if nfr:
            rec["frame_chord_tone_share"] = round(nct / nfr, 2); rec["frame_chord_tone_chance"] = round(ch / nfr, 2); rec["frames_with_chord"] = nfr
            tot_frames += nfr; tot_ct += nct; chance_sum += ch
        pitch_segs.append(rec)
    n_med = [r for r in pitch_segs if "f0_median_hz" in r]
    out["pitch"] = {"tonic_source": f"audio_features/summary.json key_whole_song_top3[0] = {keyname}" if tonic else None,
                    "n_segments_with_f0": len(n_med), "n_segments": len(pitch_segs),
                    "interval_histogram_semitones": {str(i): sum(1 for r in n_med if r.get("interval_to_tonic_semitones") == i) for i in range(12)} if tonic else None,
                    "segments_in_scale": sum(1 for r in n_med if r.get("in_scale_of_key")) if tonic else None,
                    "segments_median_on_chord_tone": sum(1 for r in n_med if r.get("median_pc_is_chord_tone")),
                    "segments_with_chord_info": sum(1 for r in n_med if "median_pc_is_chord_tone" in r),
                    "pooled_frame_chord_tone_share": round(tot_ct / tot_frames, 3) if tot_frames else None,
                    "pooled_frame_chord_tone_chance": round(chance_sum / tot_frames, 3) if tot_frames else None,
                    "pooled_frames": tot_frames,
                    "note": "OBS: speech f0 is not a sung note; chance = share of the 12 pitch classes that are chord tones for the same frames. A gap between share and chance is possible evidence of pitch-matching, not shown here.",
                    "segments": pitch_segs}
    # ---- 3 beat phase
    bp = os.path.join(D, "audio_features/beat_times.json")
    if not os.path.exists(bp):
        out["beat_phase"] = {"status": "beat_times.json missing"}
    else:
        beats = np.array(json.load(open(bp)), float); rows = []
        for v in keep:
            t0 = v["start_s"]; i = int(np.searchsorted(beats, t0, side="right")) - 1
            if i < 0 or i + 1 >= len(beats): rows.append({"onset_s": t0, "phase": None, "note": "outside beat grid"}); continue
            ib = beats[i + 1] - beats[i]; ph = (t0 - beats[i]) / ib
            nearest = beats[i] if ph < 0.5 else beats[i + 1]
            rows.append({"onset_s": t0, "beat_interval_s": round(float(ib), 3), "phase": round(float(ph), 3), "offset_to_nearest_beat_ms": int(round((t0 - nearest) * 1000))})
        ph = np.array([r["phase"] for r in rows if r.get("phase") is not None])
        res = {"status": "ok", "beat_times_source": "audio_features/beat_times.json", "n_onsets": int(len(ph)), "onsets": rows}
        if len(ph):
            z = np.exp(2j * np.pi * ph).mean()
            res.update({"circular_mean_phase": round(float((np.angle(z) / (2 * np.pi)) % 1), 3), "resultant_length_R": round(float(abs(z)), 3),
                        "uniform_chance_R_approx": round(float(1 / np.sqrt(len(ph))), 3),
                        "share_within_100ms_of_beat": round(float(np.mean([abs(r["offset_to_nearest_beat_ms"]) <= 100 for r in rows if r.get("phase") is not None])), 3),
                        "note": "OBS: segment onsets are VAD onsets (>=gap s after previous voiced block), not syllable onsets. R near uniform_chance_R means no phase preference measurable at this n."})
        out["beat_phase"] = res
    # ---- 4 ducking
    stems = {}
    for nm in ("bass", "drums", "other"):
        p = os.path.join(ST, nm + ".wav")
        if os.path.exists(p):
            x, s_ = rd(p); stems[nm] = rms_blocks(x[:nmin], s_) if s_ == sr else None
    if "other" not in stems or stems["other"] is None:
        out["ducking"] = {"status": "other stem missing"}
    else:
        n = min(len(v) for v in stems.values() if v is not None); n = min(n, nb)
        pw = sum(stems[k][:n] ** 2 for k in stems if stems[k] is not None)
        acc = db(np.sqrt(pw)); oth = db(stems["other"][:n]); mixd = dm[:n]
        inside = np.zeros(n, bool); near = np.zeros(n, bool); M = int(round(1.0 / HOP_S))
        for v in keep:
            s, e = int(v["start_s"] / HOP_S), int(v["end_s"] / HOP_S)
            inside[s:min(e, n)] = True; near[max(0, s - M):min(e + M, n)] = True
        outside = ~near; margin = near & ~inside
        def st(arr, m): return None if m.sum() == 0 else round(float(db(np.sqrt((10 ** (arr[m] / 10)).mean()))) if False else float(10 * np.log10((10 ** (arr[m] / 10)).mean() + EPS)), 1)
        # power-mean dB per region
        def pm(arr, m): return None if m.sum() == 0 else round(float(10 * np.log10(np.mean(10 ** (arr[m] / 10)) + EPS)), 1)
        regions = {"during_voiced": inside, "margin_1s_around": margin, "elsewhere": outside}
        dd = {"status": "ok", "definition": "power-mean dB of 10 ms RMS blocks; elsewhere = not within 1 s of any kept voiced segment; mix includes the voice itself, accompaniment = bass+drums+other stems power sum",
              "seconds_per_region": {k: round(float(m.sum() * HOP_S), 1) for k, m in regions.items()},
              "accompaniment_db": {k: pm(acc, m) for k, m in regions.items()},
              "other_stem_db": {k: pm(oth, m) for k, m in regions.items()},
              "mix_db": {k: pm(mixd, m) for k, m in regions.items()}}
        if dd["accompaniment_db"]["elsewhere"] is not None and dd["accompaniment_db"]["during_voiced"] is not None:
            dd["accompaniment_during_minus_elsewhere_db"] = round(dd["accompaniment_db"]["during_voiced"] - dd["accompaniment_db"]["elsewhere"], 1)
            dd["other_during_minus_elsewhere_db"] = round(dd["other_stem_db"]["during_voiced"] - dd["other_stem_db"]["elsewhere"], 1)
        else:
            dd["note_regions"] = "no 'elsewhere' region (voiced margins cover the track): during-minus-elsewhere not computed"
        per = []
        for v in keep:
            s, e = int(v["start_s"] / HOP_S), min(int(v["end_s"] / HOP_S), n)
            if s - M < 0 or e <= s: continue
            pre = float(10 * np.log10(np.mean(10 ** (acc[s - M:s] / 10)) + EPS)); dur_ = float(10 * np.log10(np.mean(10 ** (acc[s:e] / 10)) + EPS))
            per.append({"start_s": v["start_s"], "accompaniment_pre1s_db": round(pre, 1), "accompaniment_during_db": round(dur_, 1), "change_db": round(dur_ - pre, 1)})
        if per:
            ch = np.array([p["change_db"] for p in per])
            dd["per_segment_change_db"] = {"n": len(per), "median": round(float(np.median(ch)), 1), "share_negative": round(float((ch < 0).mean()), 2), "segments": per}
        dd["note"] = "OBS: a level difference is not shown to be deliberate ducking; section changes (voice often enters with a section) confound it."
        out["ducking"] = dd

# ---- write
jp = os.path.join(O, "voice_as_music.json"); json.dump(out, open(jp, "w"), indent=1, ensure_ascii=False)
L = [f"voice_as_music: {VID} (all numbers OBS: measurements, no interpretation)", f"status: {out['status']}; track {dur:.1f} s",
     f"1 VAD (bleed rule {a.bleed_db} dB below mix, floor {a.floor_db} dBFS): {len(vad_all)} segments, {tot_vad:.1f} s voiced ({tot_nobleed:.1f} s without bleed rule); kept after whisper filter: {len(keep)} segments, {tot_keep:.1f} s"]
if out["status"] == "no voice found":
    L.append(out["note"])
else:
    p = out["pitch"]
    L.append(f"2 PITCH: tonic = {p['tonic_source']}; f0 in {p['n_segments_with_f0']}/{p['n_segments']} segments; interval histogram (semitones 0-11) {p['interval_histogram_semitones']}; in scale {p['segments_in_scale']}; median on chord tone {p['segments_median_on_chord_tone']}/{p['segments_with_chord_info']}; pooled frame chord-tone share {p['pooled_frame_chord_tone_share']} vs chance {p['pooled_frame_chord_tone_chance']} ({p['pooled_frames']} frames)")
    b = out["beat_phase"]
    L.append(f"3 BEAT PHASE: n={b.get('n_onsets')}, circular mean phase {b.get('circular_mean_phase')}, R={b.get('resultant_length_R')} (uniform chance about {b.get('uniform_chance_R_approx')}), within 100 ms of a beat {b.get('share_within_100ms_of_beat')}" if b.get("status") == "ok" else f"3 BEAT PHASE: {b.get('status')}")
    d = out["ducking"]
    if d.get("status") == "ok":
        L.append(f"4 DUCKING: accompaniment dB {d['accompaniment_db']}; other-stem dB {d['other_stem_db']}; during-minus-elsewhere {d.get('accompaniment_during_minus_elsewhere_db')} dB (accompaniment), {d.get('other_during_minus_elsewhere_db')} dB (other); per-segment change vs previous 1 s median {d.get('per_segment_change_db', {}).get('median')} dB, share negative {d.get('per_segment_change_db', {}).get('share_negative')}")
    else: L.append(f"4 DUCKING: {d.get('status')}")
w = out["whisper_filter"]
L.append(f"5 WHISPER FILTER: {w['status']}; primary {w['primary_source']}; dropped VAD segments {len(w['dropped_vad_segments'])}")
for s_ in w["sources"]:
    L.append(f"   {s_['file']}: {s_['n_segments']} segs ({s_['n_doubtful']} doubtful), whisper {s_['whisper_time_s']} s (reliable {s_['whisper_reliable_time_s']} s), VAD {s_['vad_time_s']} s, VAD overlapping any whisper {s_['vad_time_overlapping_any_whisper_s']} s, reliable whisper {s_['vad_time_overlapping_reliable_whisper_s']} s")
open(os.path.join(O, "voice_as_music.txt"), "w").write("\n".join(L) + "\n")
print("\n".join(L)); print("wrote", jp)
