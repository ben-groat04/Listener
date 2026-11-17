#!/usr/bin/env python3
"""Per-section loudness, stereo phase and rough decay probe (D8).

Usage:
  python3 v1/scripts/agents/section_levels.py <video_id> [--decay LABEL:START_S:END_S ...]

Reads  v1/data/<vid>/audio/song.wav (stereo mix) and the song map table in
v1/analysis/music/<vid>/music_reading.md (rows starting '| m:ss[.s] to m:ss[.s] |').
Writes v1/data/<vid>/audio_features/section_levels.json.

Method (own implementation, not a calibrated meter; no pyloudnorm installed):
 * K-weighting: ITU-R BS.1770 stage 1 (high shelf) + stage 2 (RLB high-pass), the
   48 kHz coefficients, after resampling to 48 kHz. Channel weights 1.0 (L, R).
 * integrated LUFS: 400 ms blocks, 75% overlap, absolute gate -70 LUFS, relative gate
   -10 LU, applied within the section. Sections shorter than 400 ms get an ungated
   mean-square value (flag 'ungated_short').
 * short-term max LUFS: 3 s windows, 0.1 s hop, fully inside the section (null if the
   section is shorter than 3 s).
 * peak dBFS: SAMPLE peak of the unweighted mix (not a true-peak/oversampled value).
 * L/R phase correlation: Pearson r of the L and R samples (1 = identical, 0 = unrelated,
   -1 = opposite polarity).
 * mid/side: M=(L+R)/2, S=(L-R)/2; ratio = 10*log10(sum M^2 / sum S^2) in dB, plus S share.
 * decay probe (rough): 10 ms RMS envelope (unweighted, mono sum) in the given window,
   linear fit of dB against time, RT60 = -60 / slope. This measures the decay of
   whatever is ringing (here the music's own tail), NOT a room impulse response.
"""
import sys, re, json, os
import numpy as np
import soundfile as sf
from scipy import signal

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
B1 = [1.53512485958697, -2.69169618940638, 1.19839281085285]
A1 = [1, -1.69065929318241, 0.73248077421585]
B2 = [1, -2, 1]
A2 = [1, -1.99004745483398, 0.99007225036621]
FS = 48000


def parse_time(s):
    m, r = s.strip().split(':')
    return int(m) * 60 + float(r)


def parse_map(path):
    rows = []
    for line in open(path, encoding='utf-8'):
        mm = re.match(r'\|\s*(\d+:\d+(?:\.\d+)?)\s+to\s+(\d+:\d+(?:\.\d+)?)\s*\|\s*([^|]+)\|', line)
        if mm:
            rows.append(dict(start_label=mm.group(1), end_label=mm.group(2),
                             start_s=parse_time(mm.group(1)), end_s=parse_time(mm.group(2)),
                             name=mm.group(3).replace('*', '').strip()))
    return rows


def kweight(x):
    return signal.lfilter(B2, A2, signal.lfilter(B1, A1, x, axis=0), axis=0)


def lufs_from_ms(ms):
    return -0.691 + 10 * np.log10(max(ms, 1e-12))


def integrated(k, a, b):
    seg = k[a:b]
    n = len(seg)
    blk, hop = int(0.4 * FS), int(0.1 * FS)
    if n < blk:
        return lufs_from_ms((seg ** 2).sum(1).mean()), 'ungated_short'
    z = np.array([(seg[i:i + blk] ** 2).sum(1).mean() for i in range(0, n - blk + 1, hop)])
    l = -0.691 + 10 * np.log10(z + 1e-12)
    g = z[l > -70]
    if len(g) == 0:
        return None, 'below_abs_gate'
    rel = lufs_from_ms(g.mean()) - 10
    g2 = z[l > max(-70, rel)]
    return lufs_from_ms(g2.mean()), 'gated'


def short_term_max(k, a, b):
    w, hop = 3 * FS, int(0.1 * FS)
    if b - a < w:
        return None
    ms = (k[a:b] ** 2).sum(1)
    c = np.concatenate([[0], np.cumsum(ms)])
    best = max((c[i + w] - c[i]) / w for i in range(0, len(ms) - w + 1, hop))
    return lufs_from_ms(best)


def db(v):
    return float(20 * np.log10(max(v, 1e-12)))


def decay_probe(x, fs, lo, hi):
    mono = x.mean(1)[int(lo * fs):int(hi * fs)]
    h = int(0.01 * fs)
    n = len(mono) // h
    env = np.array([np.sqrt((mono[i * h:(i + 1) * h] ** 2).mean()) for i in range(n)])
    d = 20 * np.log10(env + 1e-12)
    t = lo + (np.arange(n) + 0.5) * 0.01
    ok = d > -90
    if ok.sum() < 5:
        return dict(window_s=[lo, hi], note='too little signal above -90 dBFS')
    p = np.polyfit(t[ok], d[ok], 1)
    pred = np.polyval(p, t[ok])
    ss = ((d[ok] - pred) ** 2).sum(); st = ((d[ok] - d[ok].mean()) ** 2).sum()
    return dict(window_s=[lo, hi], start_env_dbfs=round(float(d[ok][:5].mean()), 1),
                end_env_dbfs=round(float(d[ok][-5:].mean()), 1),
                slope_db_per_s=round(float(p[0]), 2),
                rt60_s=round(float(-60 / p[0]), 2) if p[0] < 0 else None,
                r2=round(float(1 - ss / st), 3) if st > 0 else None,
                caveat='rough probe: decay of the music tail (linear fit of 10 ms RMS dB), not a room measurement')


def main():
    args = sys.argv[1:]
    vid = args[0]
    decays = []
    i = 1
    while i < len(args):
        if args[i] == '--decay':
            lab, s, e = args[i + 1].split(':'); decays.append((lab, float(s), float(e))); i += 2
        else:
            i += 1
    secs = parse_map(os.path.join(ROOT, 'analysis/music', vid, 'music_reading.md'))
    x, fs = sf.read(os.path.join(ROOT, 'data', vid, 'audio/song.wav'))
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    xr = signal.resample_poly(x, FS, fs, axis=0) if fs != FS else x
    k = kweight(xr)
    out = []
    for s in secs:
        a, b = int(s['start_s'] * FS), int(s['end_s'] * FS)
        a0, b0 = int(s['start_s'] * fs), int(s['end_s'] * fs)
        seg = x[a0:b0]
        L, R = seg[:, 0], seg[:, 1]
        M, S = (L + R) / 2, (L - R) / 2
        lufs, gate = integrated(k, a, b)
        sm = short_term_max(k, a, b)
        r = float(np.corrcoef(L, R)[0, 1]) if len(L) > 2 and L.std() > 0 and R.std() > 0 else None
        em, es = (M ** 2).sum(), (S ** 2).sum()
        out.append(dict(s, duration_s=round(s['end_s'] - s['start_s'], 3),
                        integrated_lufs=None if lufs is None else round(float(lufs), 2), gating=gate,
                        short_term_max_lufs=None if sm is None else round(float(sm), 2),
                        sample_peak_dbfs=round(db(np.abs(seg).max()), 2),
                        lr_correlation=None if r is None else round(r, 3),
                        mid_side_ratio_db=round(float(10 * np.log10((em + 1e-20) / (es + 1e-20))), 2),
                        side_energy_share=round(float(es / (em + es + 1e-20)), 4)))
    res = dict(video=vid, source='data/%s/audio/song.wav' % vid, sample_rate_in=fs, duration_s=round(len(x) / fs, 3),
               method='own BS.1770 K-weighting (48 kHz coeffs), see script docstring; not a calibrated meter',
               sections_from='analysis/music/%s/music_reading.md song map (rows may overlap)' % vid,
               sections=out,
               decay_probes=[dict(label=l, **decay_probe(x, fs, a, b)) for l, a, b in decays])
    od = os.path.join(ROOT, 'data', vid, 'audio_features')
    os.makedirs(od, exist_ok=True)
    json.dump(res, open(os.path.join(od, 'section_levels.json'), 'w'), indent=1)
    for o in out:
        print(o['start_label'], o['end_label'], o['integrated_lufs'], o['short_term_max_lufs'], o['sample_peak_dbfs'], o['lr_correlation'], o['mid_side_ratio_db'])
    print(json.dumps(res['decay_probes'], indent=1))


if __name__ == '__main__':
    main()
