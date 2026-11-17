"""Zero-shot audio tagging with CLAP (laion/larger_clap_music_and_speech): every 5 s window gets scores for
genre, instruments, mood, vocal/speech type and sound events. Video-agnostic label sets; per-video extra labels can be
added in v1/data/<VID>/clap_extra_labels.txt (one per line). Output: v1/data/<VID>/music_views/clap_tags.json + clap.png"""
import json, os
import numpy as np, librosa, torch, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from transformers import ClapModel, ClapProcessor
def _t(x):  # transformers 5 returns a ModelOutput instead of a tensor
    return x if torch.is_tensor(x) else (x.pooler_output if getattr(x, 'pooler_output', None) is not None else x[0])
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from _common import require_vid, find_video
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VID = require_vid(); D = os.path.join(root, f"v1/data/{VID}"); O = os.path.join(D, "music_views"); os.makedirs(O, exist_ok=True)
SETS = {
 "genre": ["rock", "post-rock", "electronic music", "ambient music", "techno", "hip hop", "pop", "folk", "classical music", "jazz", "metal", "soul", "country", "krautrock", "orchestral film score", "drum and bass", "indie rock", "synth-pop", "R&B", "reggae"],
 "instrument": ["electric guitar", "distorted guitar", "acoustic guitar", "bass guitar", "synthesizer", "piano", "drum kit", "drum machine", "strings", "brass", "banjo", "organ", "choir", "glockenspiel", "violin", "saxophone", "sampled voice"],
 "mood": ["happy", "sad", "tense", "calm", "triumphant", "melancholic", "eerie", "energetic", "hopeful", "nostalgic", "aggressive", "dreamy", "solemn", "playful"],
 "voice": ["male singing", "female singing", "male speech", "female speech", "radio announcer speech", "crowd chanting", "rapping", "no vocals", "choir singing"],
 "sound": ["wind", "crowd cheering", "applause", "ice skating", "footsteps in snow", "engine", "tape hiss", "vinyl crackle", "silence", "bells"],
}
extra = os.path.join(D, "clap_extra_labels.txt")
if os.path.exists(extra): SETS["extra"] = [l.strip() for l in open(extra) if l.strip()]
torch.set_num_threads(4)
m = ClapModel.from_pretrained("laion/larger_clap_music_and_speech").eval(); p = ClapProcessor.from_pretrained("laion/larger_clap_music_and_speech")
y, sr = librosa.load(os.path.join(D, "audio/song.wav"), sr=48000, mono=True)
W = 5; wins = [y[i:i + W * sr] for i in range(0, len(y) - sr, W * sr)]
with torch.no_grad():
    te = {k: _t(m.get_text_features(**p(text=[f"the sound of {l}" if k in ("instrument", "sound") else f"{l}" for l in v], return_tensors="pt", padding=True))) for k, v in SETS.items()}
    te = {k: torch.nn.functional.normalize(v, dim=-1) for k, v in te.items()}
    ae = []
    for i in range(0, len(wins), 8):
        b = p(audio=[w for w in wins[i:i + 8]], sampling_rate=48000, return_tensors="pt")
        ae.append(torch.nn.functional.normalize(_t(m.get_audio_features(**b)), dim=-1))
    ae = torch.cat(ae)
out = {"window_s": W, "labels": SETS, "windows": []}
for j in range(len(wins)):
    row = {"t": j * W}
    for k, v in SETS.items():
        s = (ae[j] @ te[k].T * 100).softmax(-1).numpy(); idx = s.argsort()[::-1][:3]
        row[k] = [[v[i], round(float(s[i]), 3)] for i in idx]
    out["windows"].append(row)
# whole-song averages
for k, v in SETS.items():
    s = (ae @ te[k].T * 100).softmax(-1).mean(0).numpy(); out.setdefault("song_average", {})[k] = [[v[i], round(float(s[i]), 3)] for i in s.argsort()[::-1][:6]]
json.dump(out, open(f"{O}/clap_tags.json", "w"), indent=0)
fig, ax = plt.subplots(len(SETS), 1, figsize=(16, 3 * len(SETS)))
for a, (k, v) in zip(ax, SETS.items()):
    S = (ae @ te[k].T * 100).softmax(-1).numpy().T; a.imshow(S, aspect="auto", cmap="magma", extent=[0, len(wins) * W, len(v) - .5, -.5])
    a.set_yticks(range(len(v))); a.set_yticklabels(v, fontsize=7); a.set_title(k)
plt.tight_layout(); plt.savefig(f"{O}/clap.png", dpi=60)
print(json.dumps(out["song_average"]))
