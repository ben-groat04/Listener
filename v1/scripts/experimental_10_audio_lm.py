"""EXPERIMENTAL / NOT WORKING (2026-11-17): on this 4-core CPU it took ~15 min per 20 s window and the audio was not actually
received by the thinker (it replied that it could not hear; token-id/config mismatch warnings). Kept for reference only.
A second pair of 'ears': an open audio-language model (Qwen2.5-Omni-3B, thinker only, CPU) listens to each 20 s window
of the mix and of the vocal stem and describes it in words. Video-agnostic. Slow on CPU (minutes per window); idempotent per window.
Output: v1/data/<VID>/audio_lm/window_NNNNs.json (+ all.md). Treat as one more noisy witness, not ground truth."""
import json, os, sys, time
import numpy as np, librosa, torch
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VID = os.environ.get("VID", "video2"); D = os.path.join(root, f"v1/data/{VID}"); O = os.path.join(D, "audio_lm"); os.makedirs(O, exist_ok=True)
MAXW = int(os.environ.get("MAXW", "999")); WIN = 20
from transformers import Qwen2_5OmniThinkerForConditionalGeneration, Qwen2_5OmniProcessor
torch.set_num_threads(int(os.environ.get("THREADS", "4")))
MID = "Qwen/Qwen2.5-Omni-3B"
proc = Qwen2_5OmniProcessor.from_pretrained(MID)
model = Qwen2_5OmniThinkerForConditionalGeneration.from_pretrained(MID, torch_dtype=torch.bfloat16).eval()
PROMPTS = {
 "mix": "You are a perceptive music listener. Describe this 20-second music excerpt concretely: which instruments you hear, the rhythm and tempo feel, the energy and how it changes within the clip, any voice (speech or singing, language, and any words you can make out), the mood it creates. Do not guess the artist. 4-6 sentences.",
 "vocals": "This is an isolated voice track (it may contain only silence or music bleed). Say whether there is speech or singing, the language, the speaker's tone and delivery, and transcribe any words you can make out. If nothing, say so. 2-4 sentences.",
}
def ask(audio, prompt):
    conv = [{"role": "system", "content": [{"type": "text", "text": "You are Qwen, a virtual human developed by the Qwen Team, Alibaba Group, capable of perceiving auditory and visual inputs, as well as generating text and speech."}]},
            {"role": "user", "content": [{"type": "audio", "audio": "clip"}, {"type": "text", "text": prompt}]}]
    text = proc.apply_chat_template(conv, add_generation_prompt=True, tokenize=False)
    inp = proc(text=text, audio=[audio], return_tensors="pt", padding=True)
    with torch.no_grad(): out = model.generate(**inp, max_new_tokens=180, do_sample=False)
    return proc.batch_decode(out[:, inp["input_ids"].shape[1]:], skip_special_tokens=True)[0].strip()
mix, _ = librosa.load(f"{D}/audio/song.wav", sr=16000, mono=True)
vp = f"{D}/stems_raw/htdemucs/song/vocals.wav"; voc = librosa.load(vp, sr=16000, mono=True)[0] if os.path.exists(vp) else None
for k, w in enumerate(range(0, int(len(mix) / 16000), WIN)):
    if k >= MAXW: break
    f = f"{O}/window_{w:04d}s.json"
    if os.path.exists(f): continue
    t0 = time.time(); a, b = w * 16000, (w + WIN) * 16000
    r = {"window_s": [w, w + WIN], "model": MID, "mix": ask(mix[a:b], PROMPTS["mix"])}
    if voc is not None: r["vocals"] = ask(voc[a:b], PROMPTS["vocals"])
    r["secs"] = round(time.time() - t0); json.dump(r, open(f, "w"), indent=1); print(w, r["secs"], "s", flush=True)
import glob
with open(f"{O}/all.md", "w") as fo:
    fo.write(f"# {VID}: audio-language model descriptions ({MID}, CPU). One noisy witness; cross-check against measurements.\n\n")
    for f in sorted(glob.glob(f"{O}/window_*.json")):
        r = json.load(open(f)); fo.write(f"## {r['window_s'][0]//60}:{r['window_s'][0]%60:02d}-{r['window_s'][1]//60}:{r['window_s'][1]%60:02d}\n- Mix: {r['mix']}\n" + (f"- Vocals: {r.get('vocals')}\n" if r.get("vocals") else "") + "\n")
