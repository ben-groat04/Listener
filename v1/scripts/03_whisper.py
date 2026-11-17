"""Transcription / translation with faster-whisper (CPU, int8, word timestamps). VID is mandatory (env var, no default).
Usage:  VID=<name> python3 03_whisper.py MODEL [AUDIO] [TAG] [LANG] [TASK]
  MODEL  faster-whisper model name, e.g. small, medium (default small).
  AUDIO  path to a wav; "" or omitted = v1/data/<VID>/audio/song_16k_mono.wav (e.g. pass the isolated vocals stem instead).
  TAG    label for the source in the output name, e.g. mix or vocals (default mix).
  LANG   ISO code (nl, en, ...) = forced-language pass (preferred); "auto" = detect, as recorded fallback (default auto).
  TASK   transcribe (default) or translate (to English).
Writes v1/data/<VID>/lyrics/whisper_<MODEL>_<TAG>_<LANG|auto>_<TASK>.{json,txt} (names unchanged).
Reliability layer (L10/E8; all added fields, none removed). Per segment the .json gains `reliable` (bool) and `reliable_reason`
(list of strings; empty when reliable): 'low_confidence' (no_speech_prob > 0.6 or avg_logprob < -1.0, = the old `doubtful`),
'blacklisted_phrase:<phrase>' (known hallucination such as MUZIEK, Bedankt voor het kijken, Thanks for watching, Dalmatians; extend
HALLUCINATIONS or env WHISPER_BLACKLIST="a|b"), 'vocal_stem_quiet' (vocal stem silent over the segment: probably music bleed;
needs v1/data/<VID>/stems/stem_rms_per_second.json, 1 s bins; thresholds env VOCAL_RMS_MIN, default 0.003, and VOCAL_ACTIVE_FRAC,
default 0.3 = at least this fraction of the 1 s bins must exceed it), 'no_vocal_stem' is NOT a failure and is only noted in
`vocal_mask` at top level. Also added per segment `vocal_active_frac` (null if no stem data) and top level `lang_forced`
(bool), `lang_source` ('forced' | 'auto-fallback'), `lang_detected` (language + prob from a separate detect pass when forced,
else null), `lang_prob_meaningful` (false when forced, or when auto-detect prob >= 0.995, i.e. 1.00 says nothing), `vocal_mask`.
Forced language is preferred; use 'auto' only as a fallback, and the outcome is recorded in lang_source. Check a forced language
against lang_detected before trusting it. The main .txt keeps only reliable segments; the *_doubtful.txt lists all others with reasons.
Segments with no_speech_prob > 0.6 or avg_logprob < -1.0 stay in the .json (flagged). Treat the main .txt as the more reliable text.
Treat all Whisper output as a hint: quote only phrases that repeat across passes."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from _common import require_vid
VID = require_vid()
from faster_whisper import WhisperModel
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
model = sys.argv[1] if len(sys.argv) > 1 else "small"
audio = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else os.path.join(root, f"v1/data/{VID}/audio/song_16k_mono.wav")
tag = sys.argv[3] if len(sys.argv) > 3 else "mix"
lang = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "auto" else None
task = sys.argv[5] if len(sys.argv) > 5 else "transcribe"
tag = f"{tag}_{lang or 'auto'}_{task}"
D = os.path.join(root, f"v1/data/{VID}/lyrics"); os.makedirs(D, exist_ok=True)
m = WhisperModel(model, device="cpu", compute_type="int8", cpu_threads=4)
import soundfile as sf, numpy as np, librosa
wav, _ = librosa.load(audio, sr=16000, mono=True)  # numpy input avoids PyAV incompat
segs, info = m.transcribe(wav.astype(np.float32), word_timestamps=True, vad_filter=False, beam_size=5, language=lang, task=task, condition_on_previous_text=False)
def doubtful(s): return (s.no_speech_prob or 0) > 0.6 or (s.avg_logprob if s.avg_logprob is not None else 0) < -1.0
import re
HALLUCINATIONS = ["muziek", "bedankt voor het kijken", "bedankt voor het luisteren", "ondertitels", "dalmatians", "thanks for watching",
                  "thank you for watching", "thank you for listening", "subscribe", "amara.org", "bedankt"]
if os.environ.get("WHISPER_BLACKLIST"): HALLUCINATIONS += [x.strip().lower() for x in os.environ["WHISPER_BLACKLIST"].split("|") if x.strip()]
def norm(t): return re.sub(r"[^\w ]+", "", t.lower()).strip()
def blacklisted(t):
    n = norm(t)
    if not n: return None
    for h in HALLUCINATIONS:
        if n == h or (len(h) > 8 and h in n) or (h == "bedankt" and n.startswith("bedankt voor")): return h
    return None
RMS_MIN = float(os.environ.get("VOCAL_RMS_MIN", "0.003")); ACT_FRAC = float(os.environ.get("VOCAL_ACTIVE_FRAC", "0.3"))
vrms = None; vpath = os.path.join(root, f"v1/data/{VID}/stems/stem_rms_per_second.json")
try: vrms = json.load(open(vpath))["vocals"]
except Exception: vrms = None
def vocal_frac(s):
    if not vrms: return None
    i0, i1 = int(s.start), max(int(s.start) + 1, int(np.ceil(s.end)))
    b = vrms[i0:i1]
    return (sum(1 for x in b if x > RMS_MIN) / len(b)) if b else None
lang_detected = None
if lang:
    try:
        dl = m.detect_language(wav.astype(np.float32))[:2]; lang_detected = {"language": dl[0], "prob": dl[1]}
    except Exception as e: lang_detected = {"error": str(e)[:80]}
prob_ok = (not lang) and info.language_probability < 0.995
res = {"model": model, "lang": info.language, "lang_prob": info.language_probability, "lang_forced": bool(lang), "lang_source": "forced" if lang else "auto-fallback",
       "lang_detected": lang_detected, "lang_prob_meaningful": prob_ok,
       "vocal_mask": {"source": vpath if vrms else None, "rms_min": RMS_MIN, "active_frac": ACT_FRAC, "note": None if vrms else "no vocal stem data: bleed mask not applied"},
       "segments": []}
lines = []; dlines = []
for s in segs:
    vf = vocal_frac(s); why = []
    if doubtful(s): why.append("low_confidence")
    bl = blacklisted(s.text)
    if bl: why.append("blacklisted_phrase:" + bl)
    if vf is not None and vf < ACT_FRAC: why.append("vocal_stem_quiet")
    res["segments"].append({"start": s.start, "end": s.end, "text": s.text, "avg_logprob": s.avg_logprob, "no_speech_prob": s.no_speech_prob, "doubtful": doubtful(s),
                            "reliable": not why, "reliable_reason": why, "vocal_active_frac": vf,
                            "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in (s.words or [])]})
    ln = f"[{int(s.start//60)}:{s.start%60:05.2f} - {int(s.end//60)}:{s.end%60:05.2f}] {s.text.strip()}"
    if why: dlines.append(ln + f"   (no_speech_prob={s.no_speech_prob:.2f}, avg_logprob={s.avg_logprob:.2f}; {', '.join(why)})")
    else: lines.append(ln)
json.dump(res, open(f"{D}/whisper_{model}_{tag}.json", "w"), indent=1)
open(f"{D}/whisper_{model}_{tag}.txt", "w").write(f"# faster-whisper {model} on {tag} (lang={info.language} {'forced' if lang else 'auto-fallback'}; p={info.language_probability:.2f}{'' if prob_ok else ' not meaningful'})\n" + "\n".join(lines) + "\n")
open(f"{D}/whisper_{model}_{tag}_doubtful.txt", "w").write(f"# UNRELIABLE segments (low confidence, blacklisted phrase or quiet vocal stem; reasons per line), {model} on {tag}; likely hallucination or non-speech\n" + "\n".join(dlines) + "\n")
print("done", model, tag, len(lines), "kept,", len(dlines), "doubtful")
