"""Mix meters (video-agnostic; run as VID=<name> python3 14_mix_meters.py, or pass --vid <name>; no default video).
Measures from data/<VID>/audio/song.wav (and, if present, stems_raw/htdemucs/song/*.wav; git-ignored, skipped with a note when absent):
  - integrated LUFS (BS.1770-4 K-weighting, absolute -70 and relative -10 LU gates) and short-term loudness (3 s window) per second.
    Method: pyloudnorm if importable, else ffmpeg ebur128, else own K-weighted implementation (scipy) / RMS; the method used is recorded.
    The per-second short-term series is always computed with the built-in K-weighting (so it is identical whichever method gave the integrated value).
  - sample peak and true peak (4x oversampled) in dBFS with time, crest factor (peak minus RMS, dB)
  - per-stem band energy as share of total energy: sub <60 Hz, bass 60-250, mid 250-2k, high 2k-8k, air >8k (mix too)
  - L/R correlation and mid/side energy ratio, whole track and per 10 s window; loudest 10 s stretch (by mean per-second momentary power)
  - long-FFT sub peak frequency (strongest bin 20-120 Hz of the whole-track spectrum)
Outputs: data/<VID>/music_views/mix_meters.json and mix_meters.txt (or $LISTENER_OUT). Observations (OBS) from measurement, no interpretation."""
import os, sys, json, glob, argparse, subprocess, re
import numpy as np
from scipy import signal
import soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from _common import require_vid
ap = argparse.ArgumentParser(); ap.add_argument("--vid"); a = ap.parse_args()
if a.vid: os.environ["VID"] = a.vid
VID = require_vid()
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
D = os.path.join(root, f"v1/data/{VID}"); O = os.environ.get("LISTENER_OUT") or os.path.join(D, "music_views"); os.makedirs(O, exist_ok=True)
SONG = os.path.join(D, "audio/song.wav")
if not os.path.exists(SONG): sys.exit(f"ERROR: {SONG} missing (run extraction first)")
STEMDIR = os.path.join(D, "stems_raw/htdemucs/song")
BANDS = (("sub", 0, 60), ("bass", 60, 250), ("mid", 250, 2000), ("high", 2000, 8000), ("air", 8000, 1e9))
EPS = 1e-12
def db(x): return float(20 * np.log10(max(x, EPS)))
def load(p):
    x, sr = sf.read(p, dtype="float64", always_2d=True)
    return x, sr
def kweight(x, sr):
    """BS.1770 K-weighting per channel (high shelf then 38 Hz high-pass), filters designed for any sample rate."""
    def shelf(f0, G, Q):
        K = np.tan(np.pi * f0 / sr); Vh = 10 ** (G / 20); Vb = Vh ** 0.4996667741545416
        a0 = 1 + K / Q + K * K
        return [(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0], [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]
    def hp(f0, Q):
        K = np.tan(np.pi * f0 / sr); a0 = 1 + K / Q + K * K
        return [1, -2, 1], [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]
    b1, a1 = shelf(1681.974450955533, 3.999843853973347, 0.7071752369554196); b2, a2 = hp(38.13547087602444, 0.5003270373238773)
    return signal.lfilter(b2, a2, signal.lfilter(b1, a1, x, axis=0), axis=0)
def block_powers(x, sr, win, hop):
    """Mean-square per block, channel-summed (equal weights for L/R; mono = one channel)."""
    k = kweight(x, sr); z = (k ** 2).sum(axis=1); c = np.concatenate([[0], np.cumsum(z)])
    n = int(win * sr); h = int(hop * sr); starts = np.arange(0, len(z) - n + 1, h)
    return starts / sr, (c[starts + n] - c[starts]) / n
def lufs_of(p): return -0.691 + 10 * np.log10(np.maximum(p, EPS))
def integrated_own(x, sr):
    t, p = block_powers(x, sr, 0.4, 0.1); l = lufs_of(p); g = p[l > -70]
    if not len(g): return -70.0
    rel = lufs_of(g.mean()) - 10; g2 = p[(l > -70) & (l > rel)]
    return float(lufs_of(g2.mean())) if len(g2) else -70.0
def integrated(x, sr, path):
    try:
        import pyloudnorm as pyln
        return float(pyln.Meter(sr).integrated_loudness(x)), "pyloudnorm"
    except Exception: pass
    try:
        r = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True, timeout=600)
        m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
        if m: return float(m[-1]), "ffmpeg ebur128"
    except Exception: pass
    return integrated_own(x, sr), "own BS.1770 K-weighting (scipy; pyloudnorm and ffmpeg unavailable)"
def peaks(x, sr):
    sp = np.abs(x).max(axis=1); i = int(sp.argmax())
    # true peak: 4x oversample per channel (polyphase), local around the top candidates for speed would risk misses, so do all
    up = signal.resample_poly(x, 4, 1, axis=0); tp = np.abs(up).max(axis=1); j = int(tp.argmax())
    rms = float(np.sqrt((x ** 2).mean()))
    return dict(sample_peak_dbfs=round(db(sp[i]), 2), sample_peak_time_s=round(i / sr, 2), true_peak_dbfs=round(db(tp[j]), 2),
                true_peak_time_s=round(j / 4 / sr, 2), rms_dbfs=round(db(rms), 2), crest_factor_db=round(db(sp[i]) - db(rms), 2))
def bands(mono, sr):
    n = len(mono); sp = np.abs(np.fft.rfft(mono * np.hanning(n))) ** 2; f = np.fft.rfftfreq(n, 1 / sr); tot = sp.sum() + EPS
    return {k: round(float(sp[(f >= lo) & (f < hi)].sum() / tot), 4) for k, lo, hi in BANDS}
def stereo(x):
    if x.shape[1] < 2: return None
    L, R = x[:, 0], x[:, 1]; M, S = (L + R) / 2, (L - R) / 2
    den = np.sqrt((L ** 2).sum() * (R ** 2).sum())
    return dict(lr_correlation=round(float((L * R).sum() / den), 3) if den > 0 else None,
                side_to_mid_db=round(10 * np.log10(((S ** 2).sum() + EPS) / ((M ** 2).sum() + EPS)), 2))

x, sr = load(SONG); dur = len(x) / sr
integ, method = integrated(x, sr, SONG)
# per-second short-term (3 s window ending at each second) and momentary power per second (1 s window), built-in K-weighting
tst, pst = block_powers(x, sr, 3.0, 1.0); st = [dict(t_end_s=round(float(t + 3), 1), lufs=round(float(v), 2)) for t, v in zip(tst, lufs_of(pst))]
tm, pm = block_powers(x, sr, 1.0, 1.0); mom = lufs_of(pm)
res = dict(video=VID, source=os.path.relpath(SONG, root), sample_rate=sr, channels=int(x.shape[1]), duration_s=round(dur, 2),
           loudness=dict(integrated_lufs=round(integ, 2), method=method, short_term_per_second=st, short_term_max_lufs=round(float(lufs_of(pst).max()), 2),
                         loudness_range_note="short_term series is a 3 s window ending at t_end_s, ungated"),
           peaks=peaks(x, sr))
mono = x.mean(axis=1)
res["mix_band_energy_share"] = bands(mono, sr); res["stereo_whole_track"] = stereo(x)
# 10 s windows
W = 10; wins = []
for s in range(0, int(dur // W) * W + (W if dur % W >= 1 else 0), W):
    seg = x[int(s * sr):int(min(s + W, dur) * sr)]
    if len(seg) < sr: continue
    sel = (tm >= s) & (tm + 1 <= s + W + 1e-6)
    wins.append(dict(start_s=s, end_s=round(min(s + W, dur), 1), mean_momentary_lufs=round(float(lufs_of(pm[sel].mean())), 2) if sel.any() else None,
                     sample_peak_dbfs=round(db(np.abs(seg).max()), 2), peak_time_s=round((int(np.abs(seg).max(axis=1).argmax()) + int(s * sr)) / sr, 2),
                     stereo=stereo(seg)))
res["windows_10s"] = wins
# loudest 10 s stretch: sliding by 1 s over 1 s momentary powers
if len(pm) >= W:
    c = np.concatenate([[0], np.cumsum(pm)]); sl = (c[W:] - c[:-W]) / W; k = int(sl.argmax())
    seg = x[int(k * sr):int((k + W) * sr)]; ia = int(np.abs(seg).max(axis=1).argmax())
    res["loudest_10s"] = dict(start_s=k, end_s=k + W, mean_momentary_lufs=round(float(lufs_of(sl[k])), 2), sample_peak_dbfs_in_stretch=round(db(np.abs(seg).max()), 2),
                              peak_time_in_stretch_s=round(k + ia / sr, 2), basis="sliding 1 s steps, mean K-weighted power of 1 s blocks")
# long-FFT sub peak
n = len(mono); sp = np.abs(np.fft.rfft(mono * np.hanning(n))); f = np.fft.rfftfreq(n, 1 / sr); m = (f >= 20) & (f <= 120)
res["sub_peak_hz"] = round(float(f[m][sp[m].argmax()]), 2); res["sub_peak_note"] = f"strongest bin 20-120 Hz of one {n / sr:.0f} s FFT (resolution {sr / n:.3f} Hz)"
# stems
stems = {}
if os.path.isdir(STEMDIR) and glob.glob(STEMDIR + "/*.wav"):
    for p in sorted(glob.glob(STEMDIR + "/*.wav")):
        s_, ssr = load(p); name = os.path.basename(p)[:-4]
        stems[name] = dict(band_energy_share=bands(s_.mean(axis=1), ssr), rms_dbfs=round(db(np.sqrt((s_ ** 2).mean())), 2),
                           sample_peak_dbfs=round(db(np.abs(s_).max()), 2), stereo=stereo(s_))
    res["stems"] = stems
else:
    res["stems"] = None; res["stems_note"] = "stems_raw/htdemucs/song absent (git-ignored); measured on the mix only"
json.dump(res, open(os.path.join(O, "mix_meters.json"), "w"), indent=1)
# text
P = res["peaks"]; L = res["loudness"]; T = [f"Mix meters: {VID} (OBS, from measurement)", f"{dur:.1f} s, {sr} Hz, {res['channels']} ch; loudness method: {L['method']}",
 f"Integrated {L['integrated_lufs']} LUFS; max short-term (3 s) {L['short_term_max_lufs']} LUFS",
 f"Sample peak {P['sample_peak_dbfs']} dBFS at {P['sample_peak_time_s']} s; true peak (4x) {P['true_peak_dbfs']} dBFS at {P['true_peak_time_s']} s; RMS {P['rms_dbfs']} dBFS; crest {P['crest_factor_db']} dB"]
if "loudest_10s" in res:
    q = res["loudest_10s"]; T.append(f"Loudest 10 s: {q['start_s']}-{q['end_s']} s ({q['mean_momentary_lufs']} LUFS mean); peak in it {q['sample_peak_dbfs_in_stretch']} dBFS at {q['peak_time_in_stretch_s']} s")
T.append("Mix band share: " + ", ".join(f"{k} {v:.1%}" for k, v in res["mix_band_energy_share"].items()))
if res["stereo_whole_track"]: T.append(f"Stereo whole track: L/R correlation {res['stereo_whole_track']['lr_correlation']}, side/mid {res['stereo_whole_track']['side_to_mid_db']} dB")
T.append(f"Sub peak {res['sub_peak_hz']} Hz")
if stems:
    for k, v in stems.items(): T.append(f"Stem {k}: RMS {v['rms_dbfs']} dBFS; " + ", ".join(f"{b} {s:.1%}" for b, s in v["band_energy_share"].items()))
else: T.append("Stems: " + res["stems_note"])
T.append("10 s windows (start s, mean momentary LUFS, peak dBFS, L/R corr):")
for w in wins: T.append(f"  {w['start_s']:>4}  {w['mean_momentary_lufs']}  {w['sample_peak_dbfs']}  {w['stereo']['lr_correlation'] if w['stereo'] else '-'}")
open(os.path.join(O, "mix_meters.txt"), "w").write("\n".join(T) + "\n")
print("\n".join(T[:8]))
