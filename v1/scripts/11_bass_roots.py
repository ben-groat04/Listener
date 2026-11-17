"""Bass root tracker plus kick-grid autodetect, video-agnostic. All outputs are measurements (OBS), not readings.
Usage: VID=<video> python3 11_bass_roots.py   (or --vid <video>; no default video)
Input: v1/data/<VID>/stems/bass.(wav|mp3); fallback: a 250 Hz low-pass of audio/song.wav (CAVEAT recorded in the JSON).
Output: v1/data/<VID>/music_views/bass_roots.json (see --out; an existing file made by another tool is never overwritten without --force,
the result then goes to bass_roots_grid.json). Prints the exact 09b_kick_grid.py command (not run)."""
import json, os, sys, argparse, math
import numpy as np, librosa
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import require_vid

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
ap = argparse.ArgumentParser(); ap.add_argument("--vid"); ap.add_argument("--step", type=float, default=0.25)
ap.add_argument("--out", default="bass_roots.json"); ap.add_argument("--force", action="store_true"); a = ap.parse_args()
if a.vid: os.environ["VID"] = a.vid
VID = require_vid()
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
D = os.path.join(root, "v1", "data", VID)
if not os.path.isdir(D): sys.exit(f"ERROR: no data folder for {VID}: {D}")

def find(folder, base):
    for e in (".wav", ".mp3", ".flac"):
        p = os.path.join(D, folder, base + e)
        if os.path.exists(p): return p
bass_p, drums_p = find("stems", "bass"), find("stems", "drums")
caveat = None
SR = 22050
if bass_p:
    y, _ = librosa.load(bass_p, sr=SR, mono=True); source = os.path.relpath(bass_p, D)
else:
    mix = find("audio", "song")
    if not mix: sys.exit(f"ERROR: {VID} has neither stems/bass.(wav|mp3) nor audio/song.wav; run 06_stem_one.sh / 01_extract.sh first. Nothing written.")
    from scipy.signal import butter, sosfiltfilt
    y, _ = librosa.load(mix, sr=SR, mono=True); y = sosfiltfilt(butter(4, 250, "low", fs=SR, output="sos"), y).astype(np.float32)
    source = os.path.relpath(mix, D) + " (250 Hz low-pass)"
    caveat = "No bass stem: low-passed full mix used. Kick, sub and other low content can be mistaken for bass; treat roots as weaker."
    print("CAVEAT:", caveat)
if drums_p is None: print("NOTE: no stems/drums.(wav|mp3): kick grid skipped.")
dur = len(y) / SR
hop = 256
f0, vf, vp = librosa.pyin(y, fmin=30, fmax=300, sr=SR, frame_length=4096, hop_length=hop)
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
n = min(len(f0), len(rms)); f0, vf, vp, rms = f0[:n], vf[:n], vp[:n], rms[:n]
tf = librosa.frames_to_time(np.arange(n), sr=SR, hop_length=hop)
floor = rms.max() * 10 ** (-40 / 20)  # silence rule: more than 40 dB under file maximum
ok = vf & np.isfinite(f0) & (rms > floor)
midi = np.full(n, np.nan); midi[ok] = librosa.hz_to_midi(f0[ok])

def name(m): m = int(round(m)); return f"{NOTES[m % 12]}{m // 12 - 1}"
wins = []
for k in range(int(math.ceil(dur / a.step))):
    t0, t1 = k * a.step, min(dur, (k + 1) * a.step); m = (tf >= t0) & (tf < t1)
    w = {"start": round(t0, 3), "end": round(t1, 3), "hz": None, "note": None, "pc": None, "confidence": 0.0, "octave_error_likely": False}
    sel = m & ok
    if m.sum() == 0 or sel.sum() < 2: wins.append(w); continue
    mm = np.round(midi[sel]).astype(int); ww = rms[sel]
    tot = ww.sum(); hist = {}
    for q, x in zip(mm, ww): hist[q] = hist.get(q, 0) + x
    top = max(hist, key=hist.get); sel_top = mm == top
    hz = float(np.median(f0[sel][sel_top]))
    # octave check: other mass at +-12 semitones of the same pitch class, or a pitch below 41 Hz / above 200 Hz
    other_oct = sum(v for q, v in hist.items() if q != top and (q - top) % 12 == 0)
    w.update(hz=round(hz, 2), note=name(top), pc=int(top % 12),
             confidence=round(float(hist[top] / tot * sel.sum() / m.sum()), 3),
             octave_error_likely=bool(other_oct / tot >= 0.25 or hz < 41 or hz > 200))
    wins.append(w)

# run-length segmentation on pitch class; 1-window blips (< 0.5 s) merged into the neighbour that matches both sides, else dropped to neighbour
pcs = [w["pc"] for w in wins]
sm = list(pcs)
for i in range(1, len(pcs) - 1):
    if pcs[i] != pcs[i - 1] and pcs[i - 1] == pcs[i + 1] and pcs[i - 1] is not None: sm[i] = pcs[i - 1]
segs = []; i = 0
while i < len(sm):
    j = i
    while j + 1 < len(sm) and sm[j + 1] == sm[i]: j += 1
    ws = wins[i:j + 1]; v = [x for x in ws if x["pc"] is not None]
    segs.append({"start": ws[0]["start"], "end": ws[-1]["end"], "root_pc": sm[i], "root": None if sm[i] is None else NOTES[sm[i]],
                 "mean_confidence": round(float(np.mean([x["confidence"] for x in v])), 3) if v else 0.0,
                 "octave_flag_share": round(sum(x["octave_error_likely"] for x in v) / len(v), 3) if v else 0.0,
                 "median_hz": round(float(np.median([x["hz"] for x in v])), 2) if v else None})
    i = j + 1
tot_t = sum(s["end"] - s["start"] for s in segs if s["root"])
pcsec = {}
for s in segs:
    if s["root"]: pcsec[s["root"]] = pcsec.get(s["root"], 0) + s["end"] - s["start"]
pcsum = [{"pitch_class": k, "seconds": round(v, 2), "share": round(v / tot_t, 3)} for k, v in sorted(pcsec.items(), key=lambda kv: -kv[1])]
used = [p["pitch_class"] for p in pcsum if p["share"] >= 0.03]
nv = [w for w in wins if w["pc"] is not None]
summary = {"pitch_class_seconds": pcsum, "pitch_class_set_ge3pct": sorted(used, key=NOTES.index), "n_windows": len(wins), "n_voiced_windows": len(nv),
           "silent_or_unvoiced_share": round(1 - len(nv) / len(wins), 3), "octave_flag_windows": sum(w["octave_error_likely"] for w in nv),
           "octave_flag_share": round(sum(w["octave_error_likely"] for w in nv) / max(1, len(nv)), 3), "n_segments": sum(1 for s in segs if s["root"])}

# kick grid from drums stem: low-band onset strength -> autocorrelation -> period; phase by circular mean
kick = None
if drums_p:
    yd, _ = librosa.load(drums_p, sr=SR, mono=True); h = 128
    S = np.abs(librosa.stft(yd, n_fft=2048, hop_length=h)); fr = librosa.fft_frequencies(sr=SR, n_fft=2048)
    kb = S[(fr >= 40) & (fr <= 120)].sum(0); on = np.maximum(0, np.diff(kb, prepend=kb[0])); tt = librosa.frames_to_time(np.arange(len(on)), sr=SR, hop_length=h)
    if on.max() > 0 and len(on) > 400:
        o = on - on.mean(); ac = np.correlate(o, o, "full")[len(o) - 1:]; ac /= ac[0]
        lo, hi = int(0.3 * SR / h), int(1.0 * SR / h); seg = ac[lo:hi]
        peaks = [i for i in range(1, len(seg) - 1) if seg[i] > seg[i - 1] and seg[i] >= seg[i + 1]]
        if peaks:
            best = max(seg[p] for p in peaks); p0 = next(p for p in peaks if seg[p] >= 0.85 * best)  # first strong peak = shortest period
            P0 = (lo + p0) * h / SR; Ps = np.arange(P0 * 0.97, P0 * 1.03, 0.0002)
            thr = np.percentile(on, 97); idx = np.where(on > thr)[0]; tk, wk = tt[idx], on[idx]
            R = [abs(np.sum(wk * np.exp(2j * np.pi * tk / P))) / wk.sum() for P in Ps]; P = float(Ps[int(np.argmax(R))])
            z = np.sum(wk * np.exp(2j * np.pi * tk / P)); ph = (np.angle(z) / (2 * np.pi)) % 1 * P
            loud = tk[int(np.argmax(wk))]; anchor = ph + round((loud - ph) / P) * P
            kick = {"period_s": round(P, 5), "bpm": round(60 / P, 2), "anchor_s": round(float(anchor), 3), "phase_concentration_R": round(float(max(R)), 3),
                    "autocorr_peak": round(float(seg[p0]), 3), "n_onsets_used": int(len(idx)),
                    "note": "OBS: beat period and phase from 40-120 Hz drums-stem onsets; anchor is a kick-aligned beat (the strongest onset), NOT a confirmed bar downbeat. Half/double-time ambiguity is possible."}
            cmd = f"VID={VID} python3 v1/scripts/09b_kick_grid.py --period {kick['period_s']} --anchor {kick['anchor_s']} --bar-beats 4 --name grid_kick"
            kick["command_09b"] = cmd
if drums_p and kick is None: print("NOTE: drums stem too quiet or sparse for a kick grid.")

out = {"video": VID, "label": "OBS: measurements only (pYIN f0 on the bass stem, 0.25 s windows); roots are pitch classes, not harmonic interpretation (INT)",
       "source_bass": source, "caveat": caveat, "method": {"f0": "librosa.pyin 30-300 Hz, hop 256 at 22050 Hz", "window_s": a.step,
       "dominant_pitch": "RMS-weighted histogram of rounded MIDI notes among voiced frames; confidence = weight share of the winner x voiced-frame fraction",
       "silence_rule": "RMS more than 40 dB below file maximum or unvoiced: null (no claim)",
       "octave_error_flag": "likely if >=25% of weighted mass sits on the same pitch class in another octave, or median f0 <41 Hz or >200 Hz (pYIN octave slips and sub-bass tracks are common); an unflagged window is not proof of the right octave",
       "segments": "run-length of pitch class; a single-window blip between two equal neighbours is absorbed"},
       "windows": wins, "segments": segs, "summary": summary, "kick_grid": kick}
mv = os.path.join(D, "music_views"); os.makedirs(mv, exist_ok=True); path = os.path.join(mv, a.out)
if os.path.exists(path) and not a.force:
    try: mine = "windows" in json.load(open(path))
    except Exception: mine = False
    if not mine:
        path = os.path.join(mv, "bass_roots_grid.json"); print(f"NOTE: existing {a.out} is a different (per-bar) file used by other tools; not overwritten (use --force). Wrote {os.path.basename(path)} instead.")
json.dump(out, open(path, "w"), indent=1)

print(f"[{VID}] OBS wrote {os.path.relpath(path, root)}: {len(wins)} windows, {summary['n_segments']} root segments, pitch-class set (>=3%): {summary['pitch_class_set_ge3pct']}, "
      f"octave-flag share {summary['octave_flag_share']}, silent/unvoiced {summary['silent_or_unvoiced_share']}")
if kick: print(f"[{VID}] OBS kick grid {kick['bpm']} BPM (period {kick['period_s']} s, R {kick['phase_concentration_R']}). Run (not run here):\n  {kick['command_09b']}")

# rough agreement with chords.json (run output only)
cp = os.path.join(mv, "chords.json")
if os.path.exists(cp):
    def croot(c):
        if c in ("N", None): return None, None
        r = c[:2] if len(c) > 1 and c[1] in "#b" else c[:1]
        pc = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[r[0]] + (1 if "#" in r else -1 if "b" in r else 0)
        return pc % 12, ("min" if c[len(r):len(r) + 1] == "m" and not c[len(r):].startswith("maj") else "maj")
    ch = json.load(open(cp)); nroot = nchord = nn = 0
    for w in nv:
        c = next((x["chord"] for x in ch if x["start"] <= (w["start"] + w["end"]) / 2 < x["end"]), None); r, q = croot(c)
        if r is None: continue
        nn += 1; nroot += w["pc"] == r; nchord += w["pc"] in (r, (r + (3 if q == "min" else 4)) % 12, (r + 7) % 12)
    if nn: print(f"[{VID}] OBS agreement with chords.json over {nn} windows: root {nroot / nn:.1%}, chord tone (root/third/fifth) {nchord / nn:.1%}")
