"""Transcription / translation with faster-whisper (CPU, int8, word timestamps). VID is mandatory (env var, no default).
Usage:  VID=<name> python3 03_whisper.py MODEL [AUDIO] [TAG] [LANG] [TASK]
  MODEL  faster-whisper model name, e.g. small, medium (default small).
  AUDIO  path to a wav; "" or omitted = v1/data/<VID>/audio/song_16k_mono.wav (e.g. pass the isolated vocals stem instead).
  TAG    label for the source in the output name, e.g. mix or vocals (default mix).
  LANG   ISO code (nl, en, ...) or "auto" to detect (default auto). Do not force a language you have not checked.
  TASK   transcribe (default) or translate (to English).
Writes v1/data/<VID>/lyrics/whisper_<MODEL>_<TAG>_<LANG|auto>_<TASK>.{json,txt}.
Segments with no_speech_prob > 0.6 or avg_logprob < -1.0 are likely hallucinations or music: they are kept in the .json (and
flagged there) but listed in a separate whisper_..._doubtful.txt instead of the main .txt. Treat the main .txt as the more reliable text."""
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
res = {"model": model, "lang": info.language, "lang_prob": info.language_probability, "segments": []}
lines = []; dlines = []
for s in segs:
    res["segments"].append({"start": s.start, "end": s.end, "text": s.text, "avg_logprob": s.avg_logprob, "no_speech_prob": s.no_speech_prob, "doubtful": doubtful(s),
                            "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in (s.words or [])]})
    ln = f"[{int(s.start//60)}:{s.start%60:05.2f} - {int(s.end//60)}:{s.end%60:05.2f}] {s.text.strip()}"
    if doubtful(s): dlines.append(ln + f"   (no_speech_prob={s.no_speech_prob:.2f}, avg_logprob={s.avg_logprob:.2f})")
    else: lines.append(ln)
json.dump(res, open(f"{D}/whisper_{model}_{tag}.json", "w"), indent=1)
open(f"{D}/whisper_{model}_{tag}.txt", "w").write(f"# faster-whisper {model} on {tag} (lang={info.language} p={info.language_probability:.2f})\n" + "\n".join(lines) + "\n")
open(f"{D}/whisper_{model}_{tag}_doubtful.txt", "w").write(f"# DOUBTFUL segments (no_speech_prob>0.6 or avg_logprob<-1.0), {model} on {tag}; likely hallucination or non-speech\n" + "\n".join(dlines) + "\n")
print("done", model, tag, len(lines), "kept,", len(dlines), "doubtful")
