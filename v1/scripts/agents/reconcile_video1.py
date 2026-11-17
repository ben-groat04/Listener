"""Reconcile blind vs informed readings of video1 against the stems and the level file.

Reads  v1/data/video1/stems/{bass,vocals,drums,other}.mp3 and
       v1/data/video1/music_views/per_second_levels.json
Writes v1/data/video1/sync/reconcile.json (deterministic: no clocks, no randomness).

Grid names: 'fine' = 20 ms non-overlapping RMS frames of the mp3 stems (time = frame start);
'level_file' = per_second_levels.json, 1 s bins labelled by integer t (bin start, see
bass_entry.grid_check); 'loud_1s_hop100ms' = 1 s windows, 100 ms hop, of the summed stems.
Thresholds are dBFS: bass on above -50, voice on above -40, drum hole below -35.
"""
import json, os
import numpy as np
import soundfile as sf

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
D = os.path.join(ROOT, 'data', 'video1')
HOP = 0.02
BASS_T, VOICE_T, HOLE_T = -50.0, -40.0, -35.0


def load(name):
    x, sr = sf.read(os.path.join(D, 'stems', name + '.mp3'))
    return x.mean(1), sr


def frame_db(x, sr, hop):
    n = int(round(hop * sr)); k = len(x) // n
    r = np.sqrt((x[:k * n].reshape(k, n) ** 2).mean(1))
    return 20 * np.log10(np.maximum(r, 1e-9))


def runs(mask, hop, min_gap_s, min_len_s):
    """(start, end) seconds of True runs; gaps shorter than min_gap_s merged; runs shorter than min_len_s dropped."""
    out = []; i = 0; n = len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j < n and mask[j]: j += 1
            out.append([i * hop, j * hop]); i = j
        else:
            i += 1
    merged = []
    for s, e in out:
        if merged and s - merged[-1][1] < min_gap_s: merged[-1][1] = e
        else: merged.append([s, e])
    return [[round(s, 2), round(e, 2)] for s, e in merged if e - s >= min_len_s]


def r2(x): return round(float(x), 2)


stems = {}
for nm in ('bass', 'vocals', 'drums', 'other'):
    x, sr = load(nm); stems[nm] = x
total_s = len(stems['bass']) / sr
bass = frame_db(stems['bass'], sr, HOP)
voc = frame_db(stems['vocals'], sr, HOP)
drm = frame_db(stems['drums'], sr, HOP)
L = json.load(open(os.path.join(D, 'music_views', 'per_second_levels.json')))
lv = {r['t']: r for r in L}

bass_runs = runs(bass > BASS_T, HOP, 0.5, 0.3)
voice_runs = runs(voc > VOICE_T, HOP, 1.0, 0.1)

# 1. bass entry
first_fine = float(np.argmax(bass > BASS_T) * HOP)
first_bin = min(t for t in lv if lv[t]['bass'] > BASS_T)
res = {'meta': {'track_length_s': r2(total_s), 'hop_s': HOP,
                'thresholds_dbfs': {'bass_on': BASS_T, 'voice_on': VOICE_T, 'drum_hole_below': HOLE_T},
                'grids': {'fine': '20 ms frames of the mp3 stems, time = frame start',
                          'level_file': 'per_second_levels.json, 1 s bins labelled t',
                          'loud_1s_hop100ms': '1 s windows, 0.1 s hop, of the four stems summed'}}}
res['bass_entry'] = {
    'claims_s': {'blind': 4.0, 'informed': 3.0},
    'first_frame_above_-50_dbfs_fine_s': r2(first_fine),
    'first_bass_run_fine_s': bass_runs[0],
    'level_file_first_bin_above_-50': first_bin,
    'level_file_bass_dbfs_bins_2_3_4': [lv[2]['bass'], lv[3]['bass'], lv[4]['bass']],
    'grid_check': 'bin 3 = %.1f dB is what a bin [3,4) holding only the last %.2f s of a burst at about %.1f dB would give'
                  % (lv[3]['bass'], 4 - first_fine, float(bass[int(first_fine / HOP) + 2])),
    'diff_to_claim_s': {'blind': r2(first_fine - 4.0), 'informed': r2(first_fine - 3.0)},
}
# bass out near 1:15 and slam near 1:40
i0 = int(70 / HOP); i1 = int(80 / HOP)
out_candidates = [e for s, e in bass_runs if 70 <= e <= 80]
bass_out = out_candidates[0]
after = [s for s, e in bass_runs if s > 90][0]
pre = float(bass[int((after - 0.2) / HOP):int(after / HOP)].mean())
post = float(bass[int(after / HOP):int((after + 0.2) / HOP)].max())
res['bass_out_and_slam'] = {
    'bass_out_claims_s': {'blind': '75.0-75.4', 'informed': 75.3},
    'bass_out_fine_s': bass_out,
    'bass_out_diff_to_informed_s': r2(bass_out - 75.3),
    'level_file_bass_dbfs_bins_74_75_76': [lv[74]['bass'], lv[75]['bass'], lv[76]['bass']],
    'slam_claims_s': {'blind': 100.0, 'informed': 100.0},
    'slam_onset_fine_s': r2(after),
    'slam_rise_db': {'mean_0.2s_before': r2(pre), 'max_0.2s_after': r2(post), 'rise': r2(post - pre),
                     'claims': {'blind': 'about 40 dB in 0.2 s', 'informed': 'about 35 dB in one-second bins'},
                     'level_file_bass_dbfs_bins_99_100': [lv[99]['bass'], lv[100]['bass']],
                     'level_file_rise_db': r2(lv[100]['bass'] - lv[99]['bass'])},
}
# voice
vr = voice_runs
ret = [s for s, e in vr if s > 75][0]
stop = [e for s, e in vr if 80 < e < 100][0]
res['voice'] = {
    'first_voice_onset_fine_s': vr[0][0], 'whisper_first_segment_start_s': 9.14,
    'last_voice_end_fine_s': vr[-1][1], 'whisper_last_segment_end_s': 168.28,
    'last_voice_run_s': vr[-1],
    'voice_return_after_bass_out_fine_s': ret, 'voice_return_claim_informed_s': 78.9,
    'level_file_vocals_dbfs_bins_77_78_79': [lv[77]['vocals'], lv[78]['vocals'], lv[79]['vocals']],
    'voice_stop_near_1_27_fine_s': stop, 'voice_stop_claim_informed_s': 87.0,
    'voice_runs_fine_s': vr,
    'note': 'Whisper segment times are text-model estimates; the stem is the sound.',
}
# bass runs = section edges
res['section_edges'] = {'bass_runs_fine_s': bass_runs,
                        'claims_blind_informed': {'bass_out': '75.0-75.4 / 75.3', 'bass_back': '100.0 / 100',
                                                  'end': '3:08.2 / 3:08.4'}}
# drum hole near 2:47.8
a, b = int(165 / HOP), int(171 / HOP)
m = drm[a:b] < HOLE_T
hr = runs(m, HOP, 0.0, 0.0)
hole = [[round(s + 165, 2), round(e + 165, 2)] for s, e in hr if 166.5 < s + 165 < 169]
# end of music
last_loud = float(np.where(drm > -50)[0][-1] * HOP + HOP)
mix_end_db = frame_db(sum(stems.values()), sr, HOP)
mix_last = float(np.where(mix_end_db > -40)[0][-1] * HOP + HOP)
res['drum_hole_and_end'] = {'drum_hole_runs_below_-35_dbfs_fine_s': hole,
                            'claims': {'blind': 'start 167.8, drums about 40 dB down', 'informed': 'start 167.8'},
                            'mix_last_frame_above_-40_dbfs_s': r2(mix_last),
                            'drums_last_frame_above_-50_dbfs_s': r2(last_loud),
                            'end_claims_s': {'blind': 188.2, 'informed': 188.4}}
# loudness
lvl = sorted(((r['t'], r['dbfs']) for r in L), key=lambda p: (p[1], p[0]))
inner = [(t, d) for t, d in lvl if 2 <= t <= 185]
mix = sum(stems.values())
sec = int(sr)
step = int(0.1 * sr)
starts = range(0, len(mix) - sec, step)
w = np.array([20 * np.log10(max(np.sqrt((mix[s:s + sec] ** 2).mean()), 1e-9)) for s in starts])
res['loudness'] = {
    'level_file_grid': '1 s bins labelled t (bin start)',
    'level_file_loudest_3': [[t, d] for t, d in lvl[-3:][::-1]],
    'level_file_quietest_3_all': [[t, d] for t, d in lvl[:3]],
    'level_file_quietest_3_excluding_first_2_and_last_3_bins': [[t, d] for t, d in inner[:3]],
    'level_file_median_dbfs': r2(np.median([d for _, d in lvl])),
    'claims': {'blind': 'loudest 1:52 about -9.5 dBFS', 'informed': 'loudest 1:52 raw dBFS; K-weighted peaks 1:07-1:15 and 2:48-3:08'},
    'summed_stems_1s_hop100ms': {'loudest_window_start_s': r2(float(np.argmax(w) * 0.1)), 'loudest_dbfs': r2(w.max()),
                                 'quietest_window_start_s': r2(float(np.argmin(w[:int((len(w)) - 20)]) * 0.1)),
                                 'quietest_dbfs': r2(w[:len(w) - 20].min()),
                                 'note': 'summed-stems dBFS is not the file mix level; use for relative comparison only'},
    'mean_level_file_dbfs_by_block': {k: r2(np.mean([lv[t]['dbfs'] for t in range(a, b)]))
                                      for k, (a, b) in {'1:07-1:15': (67, 75), '1:40-1:55': (100, 115),
                                                        '2:01-2:32_thin_block': (121, 152),
                                                        '2:48-3:08_plateau': (168, 188)}.items()},
}
op = os.path.join(D, 'sync', 'reconcile.json')
with open(op, 'w') as f:
    json.dump(res, f, indent=1, sort_keys=True); f.write('\n')
print('wrote', op)
