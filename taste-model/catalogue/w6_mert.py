"""MERT-v1-95M extractor identical to predictors/w3r1-content-audio/build_mert.py (4 x 5 s windows evenly spread (starts linspace(0.5, dur-5.5, 4)), clip z-scored, 24 kHz mono via ffmpeg -t 31,
dynamic int8 Linear quantisation, 2 threads, mean over time of each of the 12 layer outputs -> fp16 [4,12,768]).  Used for the W6 Deezer second-excerpt clips."""
import subprocess, numpy as np, torch
torch.set_num_threads(2)
SR = 24000; NW = 4; WL = 5.0
def decode(path):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-t", "31", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, dtype=np.float32)
def windows(a):
    dur = len(a) / SR
    if dur < WL + 1: return None
    a = (a - a.mean()) / (a.std() + 1e-7)
    starts = np.linspace(0.5, max(0.5, dur - WL - 0.5), NW)
    return torch.tensor(np.stack([a[int(s * SR):int(s * SR) + int(WL * SR)] for s in starts]))
class Extractor:
    def __init__(self):
        from transformers import AutoModel
        m = AutoModel.from_pretrained("m-a-p/MERT-v1-95M", trust_remote_code=True).eval(); self.H = []
        for l in m.encoder.layers: l.register_forward_hook(lambda mod, i, o: self.H.append((o[0] if isinstance(o, tuple) else o).detach()))
        self.m = torch.ao.quantization.quantize_dynamic(m, {torch.nn.Linear}, dtype=torch.qint8)
    def __call__(self, path):
        w = windows(decode(path))
        if w is None: return np.full((NW, 12, 768), np.nan, np.float16)
        self.H.clear()
        with torch.inference_mode(): self.m(w)
        return torch.stack(self.H).mean(2).permute(1, 0, 2).numpy().astype(np.float16)
