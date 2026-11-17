"""Music 'listening views' for agents (video-agnostic; run as VID=<name> python3 07_audio_views.py).
Per 20 s window: stacked image of the mix + stem mel-spectrograms, chroma with chords, then TWO pitch rows (voice/speech contour from the
vocals stem; lead riff from the 'other' stem). Plus whole-song chords, loudness, stereo width and a summary. Uses demucs stems if present, else the mix.

Outputs in v1/data/<VID>/music_views/ (or $LISTENER_OUT):
  chords.json   list of bar-sized segments {start,end,chord,root,quality,root_conf,quality_conf,match,pitch_class_set,pcs_names}. The beat grid is
                extended to the end of the audio at the median beat interval before beat-synchronising (the tracker usually stops early; without
                this one segment would span the tail). Identical neighbouring beats merge only within one 4-beat bar, so no segment exceeds a bar.
                Templates: major, minor, power chord (root+fifth, 'D5'), sus2, sus4, dom7 ('D7'); 'N' = match < 0.6.
                root_conf = 1 - runner-up-root score / best-root score; quality_conf = same margin among qualities of the chosen root
                (0 = tie, 1 = clear). match = cosine of the winning template. pitch_class_set = pitch classes (0 = C) holding >= 50% of the
                strongest chroma bin in the segment. Chords come from other+bass stems, so they are a harmonic sketch, not a transcription.
  chords_runs.json  the same chords, identical neighbours merged into runs (compact view; may be long).
  voice_f0.json  {label:'voice/speech contour', method:'pyin', source, fmin, fmax, notes[], contour[[t,hz]]}: pYIN on the VOCALS stem, fmin 80 Hz,
                fmax capped at 600 Hz. For speech/narration this is an intonation contour, NOT a sung melody.
  lead_riff.json {label:'lead riff', method:'basic-pitch'|'pyin_on_other_stem', source, caveat, notes[{start,end,note,midi}]}: monophonic notes
                from the 'other' stem (basic-pitch if installed, else pYIN, which is unreliable on dense polyphony: treat as a sketch).
  lead_notes.json  DEPRECATED copy of voice_f0.json (old name; it used to hold the vocals pitch, now a dict with a 'deprecated' field).
  per_second_levels.json, summary.json, window_XXXXs.png.
Test hooks: LISTENER_OUT=<dir> redirects outputs; LISTENER_SLICE=<start_s>,<len_s> processes only that slice of the audio."""
import json, os, glob
import numpy as np, librosa, librosa.display, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from _common import require_vid, find_video
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VID = require_vid(); D = os.path.join(root, f"v1/data/{VID}"); O = os.environ.get("LISTENER_OUT") or os.path.join(D, "music_views"); os.makedirs(O, exist_ok=True)
SR = 22050; HOP = 512
_sl = os.environ.get("LISTENER_SLICE"); OFF, LEN = (float(x) for x in _sl.split(",")) if _sl else (0.0, None)
def ld(p, mono=True): return librosa.load(p, sr=SR, mono=mono, offset=OFF, duration=LEN)[0]
mix = ld(f"{D}/audio/song.wav")
st_dir = glob.glob(f"{D}/stems_raw/htdemucs/song")
stems = {k: ld(f"{st_dir[0]}/{k}.wav") for k in ("vocals", "drums", "bass", "other")} if st_dir else {}
dur = len(mix) / SR
# --- chords: beat-synchronous chroma vs templates (+ 'N' for no chord) ---
NAMES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
harm = stems.get("other", mix) + stems.get("bass", 0 * mix) if stems else librosa.effects.harmonic(mix)
chroma = librosa.feature.chroma_cqt(y=harm, sr=SR, hop_length=HOP); NF = chroma.shape[1]
QUAL = (("", (0, 4, 7)), ("m", (0, 3, 7)), ("5", (0, 7)), ("sus2", (0, 2, 7)), ("sus4", (0, 5, 7)), ("7", (0, 4, 7, 10)))
tpl, lab, troot, tq = [], [], [], []
for i in range(12):
    for q, iv in QUAL:
        v = np.zeros(12); v[[(i + k) % 12 for k in iv]] = 1; tpl.append(v / np.linalg.norm(v)); lab.append(NAMES[i] + q); troot.append(i); tq.append(q)
tpl = np.array(tpl); troot = np.array(troot)
_, beats = librosa.beat.beat_track(y=mix, sr=SR, hop_length=HOP); bt = librosa.frames_to_time(beats, sr=SR, hop_length=HOP)
bt = bt[bt > 0.05]
if len(bt) >= 2:
    iv = float(np.median(np.diff(bt))); grid = list(bt)
    while grid[-1] + iv < dur - 0.25 * iv: grid.append(grid[-1] + iv)   # extend over the post-tracker tail
    bt = np.array(grid)
else:
    iv = 0.5; bt = np.arange(iv, dur - 0.25 * iv, iv)                   # no usable tracker output: fixed 120 BPM grid
bt = bt[bt < dur - 0.05]
bfr = np.unique(np.clip(librosa.time_to_frames(bt, sr=SR, hop_length=HOP), 1, NF - 1)); bt = librosa.frames_to_time(bfr, sr=SR, hop_length=HOP)
cs = librosa.util.sync(chroma, bfr, aggregate=np.median); cn = cs / (np.linalg.norm(cs, axis=0, keepdims=True) + 1e-9)
edges = np.concatenate([[0], bt, [dur]]); NB = cs.shape[1]
sc = tpl @ cn
def margin(a, b): return round(float(np.clip(1 - b / max(a, 1e-9), 0, 1)), 2)
beat_rows = []
for j in range(NB):
    s = sc[:, j]; k = int(s.argmax()); r = troot[k]
    per_root = np.array([s[troot == x].max() for x in range(12)]); other_root = np.delete(per_root, r).max()
    same = np.sort(s[troot == r])[::-1]
    a, b = (0 if j == 0 else bfr[j - 1]), (bfr[j] if j < len(bfr) else NF)
    seg = chroma[:, a:max(b, a + 1)].mean(1); pcs = [int(x) for x in np.where(seg >= 0.5 * seg.max())[0]]
    n = s[k] <= 0.6
    beat_rows.append({"start": float(edges[j]), "end": float(edges[j + 1]), "chord": "N" if n else lab[k], "root": None if n else NAMES[r], "quality": None if n else (tq[k] or "maj"),
                      "root_conf": margin(per_root[r], other_root), "quality_conf": margin(same[0], same[1]), "match": round(float(s[k]), 2), "pcs": pcs, "_w": float(edges[j + 1] - edges[j])})
def build(max_beats):
    out, nb = [], 0
    for r in beat_rows:
        if out and out[-1]["chord"] == r["chord"] and nb < max_beats:
            o = out[-1]; w0, w1 = o["_w"], r["_w"]
            for k in ("root_conf", "quality_conf", "match"): o[k] = round((o[k] * w0 + r[k] * w1) / (w0 + w1), 2)
            o["pcs"] = sorted(set(o["pcs"]) & set(r["pcs"])) or o["pcs"]; o["end"] = r["end"]; o["_w"] = w0 + w1; nb += 1
        else: out.append(dict(r)); nb = 1
    return out
def fin(rows):
    rows = [r for r in rows if r["end"] - r["start"] >= 0.4 or r is rows[-1]]
    for a, b in zip(rows, rows[1:]): a["end"] = b["start"]                  # no gaps left by dropped slivers
    rows[-1]["end"] = dur
    return [{"start": round(r["start"], 2), "end": round(r["end"], 2), "chord": r["chord"], "root": r["root"], "quality": r["quality"], "root_conf": r["root_conf"],
             "quality_conf": r["quality_conf"], "match": r["match"], "pitch_class_set": r["pcs"], "pcs_names": [NAMES[p] for p in r["pcs"]]} for r in rows]
chords = fin(build(4)); runs = fin(build(10 ** 9))
json.dump(chords, open(f"{O}/chords.json", "w")); json.dump(runs, open(f"{O}/chords_runs.json", "w"))
from collections import Counter
cc = Counter(); [cc.update({c["chord"]: c["end"] - c["start"]}) for c in chords]
# --- pitch: voice/speech contour (vocals stem) and lead riff ('other' stem) ---
def pyin_notes(y, fmin, fmax, minlen):
    f0, vflag, _ = librosa.pyin(librosa.resample(y, orig_sr=SR, target_sr=11025), fmin=fmin, fmax=fmax, sr=11025, hop_length=256)
    ft = librosa.times_like(f0, sr=11025, hop_length=256); notes, contour = [], []
    for t, f, v in zip(ft, f0, vflag):
        if v and not np.isnan(f):
            contour.append([round(float(t), 3), round(float(f), 1)]); n = librosa.hz_to_note(f)
            if notes and notes[-1]["note"] == n and t - notes[-1]["end"] < 0.05: notes[-1]["end"] = round(float(t), 2)
            else: notes.append({"start": round(float(t), 2), "end": round(float(t), 2), "note": n})
    notes = [n for n in notes if n["end"] - n["start"] >= minlen]
    for n in notes: n["midi"] = int(round(librosa.note_to_midi(n["note"])))
    return notes, contour
VF = (80, 600)
vsrc = "vocals stem" if "vocals" in stems else "full mix (no stems: contour is of whatever is loudest)"
vn, vc = pyin_notes(stems.get("vocals", mix), VF[0], VF[1], 0.12)
voice = {"label": "voice/speech contour", "method": "pyin", "source": vsrc, "fmin": VF[0], "fmax": VF[1], "slice_offset_s": OFF, "notes": vn, "contour": vc,
         "caveat": "intonation contour of the voice; for speech/narration it is not a sung melody"}
json.dump(voice, open(f"{O}/voice_f0.json", "w"))
json.dump({**voice, "deprecated": "DEPRECATED: copy of voice_f0.json kept for backward compatibility. It was the 'lead' pitch track but is the voice/speech contour; use voice_f0.json and lead_riff.json."}, open(f"{O}/lead_notes.json", "w"))
osrc = "other stem" if "other" in stems else "full mix (no stems)"; oy = stems.get("other", mix); rn, method = None, None
try:
    from basic_pitch.inference import predict
    import soundfile as sf, tempfile
    with tempfile.TemporaryDirectory(dir=O) as td:
        sf.write(f"{td}/o.wav", oy, SR); _, _, ev = predict(f"{td}/o.wav")
    ev = sorted(ev, key=lambda e: -e[3]); keep = []                      # monophonic: louder notes win overlaps
    for s0, e0, p, amp, _b in ev:
        if e0 - s0 >= 0.1 and not any(s0 < k[1] and e0 > k[0] for k in keep): keep.append((s0, e0, p))
    rn = [{"start": round(float(a), 2), "end": round(float(b), 2), "note": librosa.midi_to_note(int(p)), "midi": int(p)} for a, b, p in sorted(keep)]; method = "basic-pitch"
except Exception as ex:
    print("basic-pitch unavailable, using pYIN on the other stem:", type(ex).__name__)
if rn is None: rn, _ = pyin_notes(oy, 65, 1000, 0.1); method = "pyin_on_other_stem"
json.dump({"label": "lead riff", "method": method, "source": osrc, "slice_offset_s": OFF, "notes": rn,
           "caveat": "monophonic sketch from a polyphonic stem; pYIN on dense harmony is unreliable, so wrong octaves and dropouts are expected"}, open(f"{O}/lead_riff.json", "w"))
# --- loudness, stereo width per second ---
st = ld(f"{D}/audio/song.wav", mono=False)
L, Rr = st[0], st[1]; per = []
for s in range(int(dur)):
    a, b = s * SR, (s + 1) * SR; l, r = L[a:b], Rr[a:b]; m = (l + r) / 2; sd = (l - r) / 2
    rms = np.sqrt(np.mean(m ** 2)) + 1e-12
    per.append({"t": s, "dbfs": round(float(20 * np.log10(rms)), 1), "width": round(float(np.sqrt(np.mean(sd ** 2)) / rms), 3),
                **({k: round(float(20 * np.log10(np.sqrt(np.mean(v[a:b] ** 2)) + 1e-9)), 1) for k, v in stems.items()} if stems else {})})
json.dump(per, open(f"{O}/per_second_levels.json", "w"))
# --- per-window images ---
def mel(ax, y, title):
    S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=SR, hop_length=HOP, n_mels=96), ref=np.max)
    librosa.display.specshow(S, sr=SR, hop_length=HOP, x_axis="time", y_axis="mel", ax=ax, vmin=-80, vmax=0); ax.set_ylabel(title); ax.set_xlabel("")
def prow(ax, nts, label, col):
    ax.set_ylabel(label, fontsize=7)
    for n in nts:
        if w0 <= n["start"] < w0 + 20: ax.plot([n["start"] - w0, max(n["end"], n["start"] + 0.05) - w0], [n["midi"]] * 2, lw=3, color=col)
    if nts: ms = [n["midi"] for n in nts]; ax.set_ylim(min(ms) - 2, max(ms) + 2)
for w0 in range(0, int(np.ceil(dur)), 20):
    a, b = int(w0 * SR), int(min(dur, w0 + 20) * SR)
    rows = [("mix", mix)] + list(stems.items())
    fig, ax = plt.subplots(len(rows) + 3, 1, figsize=(14, 2.0 * (len(rows) + 3)))
    for i, (k, y) in enumerate(rows): mel(ax[i], y[a:b], k)
    c = chroma[:, a // HOP: b // HOP]; librosa.display.specshow(c, sr=SR, hop_length=HOP, x_axis="time", y_axis="chroma", ax=ax[-3]); ax[-3].set_ylabel("chroma")
    for ch in chords:
        if ch["end"] > w0 and ch["start"] < w0 + 20: ax[-3].text(max(ch["start"], w0) - w0, 11.3, ch["chord"], fontsize=8, color="w", va="top")
    prow(ax[-2], vn, f"voice/speech f0\n({vsrc.split(' (')[0]}, MIDI)", "tab:orange")
    prow(ax[-1], rn, f"lead riff\n({method}, MIDI)", "tab:blue")
    for x in ax: x.set_xlim(0, 20)
    ax[0].set_title(f"{VID} music view {w0//60}:{w0%60:02d}-{(w0+20)//60}:{(w0+20)%60:02d} (x axis = seconds into window)")
    plt.tight_layout(); plt.savefig(f"{O}/window_{w0:04d}s.png", dpi=60); plt.close()
def rng(ns): return [min((n["note"] for n in ns), key=librosa.note_to_midi), max((n["note"] for n in ns), key=librosa.note_to_midi)] if ns else None
summary = {"has_stems": bool(stems), "chord_time_share_top10": [(k, round(v, 1)) for k, v in cc.most_common(10)], "n_chord_changes": len(chords),
           "median_beat_interval_s": round(iv, 3), "bar_s_assumed_4_beats": round(4 * iv, 2), "longest_chord_segment_s": round(max(c["end"] - c["start"] for c in chords), 2), "voice_f0_note_range": rng(vn), "lead_riff_note_range": rng(rn), "lead_riff_method": method,
           "lead_note_range": rng(vn), "lead_note_range_note": "deprecated alias of voice_f0_note_range",
           "files": "chords.json, chords_runs.json, voice_f0.json, lead_riff.json, lead_notes.json (deprecated copy of voice_f0), per_second_levels.json, window_XXXXs.png (one per 20 s)"}
json.dump(summary, open(f"{O}/summary.json", "w"), indent=1); print(json.dumps(summary))
