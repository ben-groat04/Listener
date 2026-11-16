"""Lyrics transcription with faster-whisper (word timestamps). Usage: 03_whisper.py MODEL [AUDIO] [TAG]"""
import json, os, sys
from faster_whisper import WhisperModel
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VID = os.environ.get("VID", "video2")
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
res = {"model": model, "lang": info.language, "lang_prob": info.language_probability, "segments": []}
lines = []
for s in segs:
    res["segments"].append({"start": s.start, "end": s.end, "text": s.text, "avg_logprob": s.avg_logprob, "no_speech_prob": s.no_speech_prob,
                            "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in (s.words or [])]})
    lines.append(f"[{int(s.start//60)}:{s.start%60:05.2f} - {int(s.end//60)}:{s.end%60:05.2f}] {s.text.strip()}")
json.dump(res, open(f"{D}/whisper_{model}_{tag}.json", "w"), indent=1)
open(f"{D}/whisper_{model}_{tag}.txt", "w").write(f"# faster-whisper {model} on {tag} (lang={info.language} p={info.language_probability:.2f})\n" + "\n".join(lines) + "\n")
print("done", model, tag, len(lines))
