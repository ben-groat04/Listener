# Per-section loudness, stereo phase and decay probe (D8)

Produced by `v1/scripts/agents/section_levels.py` (raw data: `v1/data/<video>/audio_features/section_levels.json`). Section times are copied from the song map in `v1/analysis/music/<video>/music_reading.md` (rows overlap in video1: 1:55 to 2:14, 2:00 to 2:38 and 2:14 to 2:38 share time, as do 2:48.2 to 3:08.4 and 3:06 to 3:08.4). Tables below are generated from the JSON.

Columns: **LUFS-I** = integrated loudness (own BS.1770 K-weighting, 400 ms blocks, -70 LUFS absolute gate, -10 LU relative gate, within the section). **ST max** = highest 3 s short-term LUFS inside the section (blank if the section is under 3 s). **Peak** = sample peak of the unweighted mix, dBFS. **L/R r** = Pearson correlation of left and right samples. **M/S dB** = 10 log10 of mid energy over side energy, M=(L+R)/2, S=(L-R)/2. **Side %** = side share of M+S energy.

## video1 (file length 188.662 s)

| Range | Section | Dur s | LUFS-I | ST max | Peak dBFS | L/R r | M/S dB | Side % | Note |
|---|---|---|---|---|---|---|---|---|---|
| 0:00 to 0:01 | Swell and hit | 1 | -16.0 | - | -0.58 | 0.890 | 12.3 | 5.5 |  |
| 0:01 to 0:10 | Intro build | 9 | -12.0 | -11.7 | -0.48 | 0.836 | 10.0 | 9.0 |  |
| 0:10 to 0:31.7 | Narration over the band | 21.7 | -9.4 | -8.3 | -0.39 | 0.785 | 8.9 | 11.4 |  |
| 0:31.7 to 0:41 | Band alone | 9.3 | -9.7 | -9.4 | -0.35 | 0.645 | 6.6 | 17.9 |  |
| 0:41 to 1:15 | The build | 34 | -7.8 | -6.5 | -0.00 | 0.547 | 5.3 | 22.8 |  |
| 1:15 to 1:27 | Bass-less float | 12 | -11.8 | -11.2 | -0.40 | 0.653 | 6.7 | 17.5 |  |
| 1:27 to 1:40 | The lift | 13 | -8.0 | -7.6 | -0.24 | 0.269 | 2.4 | 36.6 |  |
| 1:40 to 1:55 | Landing | 15 | -7.6 | -7.3 | -0.20 | 0.569 | 5.6 | 21.7 |  |
| 1:55 to 2:14 | Pull-down and thin block | 19 | -11.9 | -8.2 | -0.32 | 0.685 | 7.2 | 15.9 |  |
| 2:00 to 2:38 | Sub thumps | 38 | -9.7 | -6.9 | -0.28 | 0.654 | 6.8 | 17.4 |  |
| 2:14 to 2:38 | Re-ignition and town list | 24 | -8.5 | -6.9 | -0.28 | 0.599 | 6.0 | 20.1 |  |
| 2:38 to 2:47.8 | Run-up | 9.8 | -8.8 | -8.0 | -0.43 | 0.618 | 6.2 | 19.4 |  |
| 2:47.83 to 2:48.21 | The hole | 0.38 | -17.9 | - | -5.87 | 0.891 | 12.2 | 5.7 | ungated (under 0.4 s block) |
| 2:48.2 to 3:08.4 | Bright release plateau | 20.2 | -6.7 | -6.4 | -0.14 | 0.306 | 2.7 | 34.8 |  |
| 3:06 to 3:08.4 | Close | 2.4 | -6.7 | - | -0.22 | 0.289 | 2.6 | 35.7 |  |

**Decay probes (rough probe, not a room measurement).** Linear fit of dB against time on a 10 ms RMS envelope of the mono sum; RT60 = -60 / slope.

| Probe | Window s | Start dBFS | End dBFS | Slope dB/s | RT60-style s | R squared |
|---|---|---|---|---|---|---|
| ending_taper | 188.15 to 188.5 | -17.8 | -63.3 | -156.25 | 0.38 | 0.947 |

## video2 (file length 305.946 s)

| Range | Section | Dur s | LUFS-I | ST max | Peak dBFS | L/R r | M/S dB | Side % | Note |
|---|---|---|---|---|---|---|---|---|---|
| 0:00 to 0:28 | Prelude: pad and thuds | 28 | -19.3 | -16.8 | -5.93 | -0.067 | -0.6 | 53.3 |  |
| 0:28 to 0:42 | Groove enters, no voice yet | 14 | -14.9 | -14.3 | -0.92 | 0.238 | 2.1 | 38.2 |  |
| 0:42 to 1:24 | Narrator and a restrained band (loop A) | 42 | -13.5 | -10.5 | -0.02 | 0.304 | 2.7 | 34.9 |  |
| 1:24 to 1:28.6 | The hole | 4.6 | -16.7 | -16.4 | -2.86 | 0.457 | 4.2 | 27.6 |  |
| 1:28.6 to 2:36.8 | Body 1: the full groove | 68.2 | -10.1 | -8.4 | 0.00 | 0.787 | 9.2 | 10.7 |  |
| 2:36.8 to 2:48.8 | Clearing | 12 | -11.8 | -10.8 | 0.00 | 0.811 | 9.8 | 9.5 |  |
| 2:48.8 to 3:24.8 | Trance | 36 | -9.8 | -8.6 | 0.00 | 0.675 | 7.1 | 16.4 |  |
| 3:24.8 to 4:36.8 | Plateau: pressure and the voice as rhythm | 72 | -7.0 | -6.0 | 0.00 | 0.582 | 5.8 | 20.9 |  |
| 4:36.8 to 4:48.8 | Sag | 12 | -9.3 | -9.1 | 0.00 | 0.649 | 6.7 | 17.8 |  |
| 4:48.8 to 5:00.6 | Stutter | 11.8 | -10.0 | -9.7 | 0.00 | 0.547 | 5.3 | 22.9 |  |
| 5:00.6 to 5:04 | Cut and ring-out | 3.4 | -15.1 | -16.8 | -0.69 | 0.943 | 15.3 | 2.9 |  |

**Decay probes (rough probe, not a room measurement).** Linear fit of dB against time on a 10 ms RMS envelope of the mono sum; RT60 = -60 / slope.

| Probe | Window s | Start dBFS | End dBFS | Slope dB/s | RT60-style s | R squared |
|---|---|---|---|---|---|---|
| pad_ringout_after_stop | 300.9 to 302.25 | -28.1 | -45.6 | -10.59 | 5.67 | 0.547 |
| tail_after_tag | 302.95 to 304.2 | -47.5 | -87.3 | -32.27 | 1.86 | 0.918 |

## Reading the decay numbers

- video1 ending (188.15 to 188.50 s): -17.8 to -63.3 dBFS in 0.35 s, slope -156 dB/s, RT60-style 0.38 s, R squared 0.95. A decay this steep and this short matches the taper or gate already described in music_reading.md (below -60 dB by 3:08.4), not a reverberant tail. It says nothing about a room.
- video2 pad ring-out after the stop near 5:00.8 (300.9 to 302.25 s): -28.1 to -45.6 dBFS, slope -10.6 dB/s, RT60-style 5.67 s, but R squared is only 0.55 because the envelope is not a clean line (it falls to about -40.5 dBFS at 301.4, rises to about -32.3 at 301.8, then falls again, from the 50 ms values). Treat 5.7 s as a loose order of magnitude for the pad's fade, not a decay constant. The music_reading.md description "decaying from -30 to -50 dB over about 2 s" is a different, slightly shorter window and a stem-level figure; the two do not conflict.
- video2 tail after the closing tag (302.95 to 304.2 s): -47.5 to -87.3 dBFS, slope -32 dB/s, RT60-style 1.86 s, R squared 0.92. This is the file's last stretch before digital zero at about 304.24 s, so it may include an edit or fade, which this probe cannot separate from a natural decay.

## What this does and does not show

It shows, per song-map section, how loud the section is on a K-weighted scale, how far the 3 s loudness peaks above the section average, the highest sample value, how similar left and right are (r) and how much energy sits in the centre against the sides. In this data the K-weighted order is: video1 loudest sections are 2:48.2 to 3:08.4 (-6.7 LUFS-I, ST max -6.4) and 0:41 to 1:15 (-7.8, ST max -6.5), with 1:27 to 1:40 and 1:40 to 1:55 at -8.0 and -7.6; video2 loudest is 3:24.8 to 4:36.8 (-7.0, ST max -6.0). The left/right correlation is lowest where the song map reports the widest stereo (video1 1:27 to 1:40, r 0.27; 2:48.2 to 3:08.4, r 0.31) and highest in the short or mono-centred spans (video2 5:00.6 to 5:04, r 0.94, M/S 15.3 dB), which agrees in direction with the "width" columns in music_reading.md without being the same measure (those use a different width definition). The video2 0:00 to 0:28 prelude has r -0.07 and M/S -0.6 dB: left and right are close to unrelated and side energy slightly exceeds mid, consistent with the "wide pad" in its song map.

It does not show: any perceived loudness (K-weighting is a model of ear sensitivity, and this is an own implementation, not a calibrated meter or a listening test); true peaks (sample peaks only, so inter-sample overs are not counted); room acoustics (the RT60-style numbers are the decay of the music itself, with a fit quality given, not an impulse response); or why a section is wide or narrow (a correlation cannot separate panning, stereo effects and phase differences). Sections of different length are not equally reliable: those under 3 s have no short-term value, and the 0.38 s video1 hole (2:47.83 to 2:48.21) is an ungated mean-square value over a span that is mostly the silent drums and bass, so its -17.9 LUFS should not be compared with the long sections. The song-map ranges overlap in video1, so the same audio appears in more than one row.

## Consistency with the K-weighted versus raw dBFS caveats in music_reading.md

- video1: music_reading.md says K-weighted loudness peaks at 1:07 to 1:15 (about -6.6 LUFS-short) and 2:48 to 3:08 (-7.0 to -6.4, steady), whereas by raw dBFS 1:40 to 1:55 is the highest, and the trough is 2:02 to 2:13 (about -13.5). This probe agrees on the K-weighted ordering: 0:41 to 1:15 has ST max -6.5 and 2:48.2 to 3:08.4 has ST max -6.4 with LUFS-I -6.7; 1:40 to 1:55 is -7.6, about 0.9 LU below the final run, and the K-weighted level returns at 1:27 (1:27 to 1:40 is -8.0). No contradiction. Differences: the doc's trough figure (-13.5 at 2:05) is a 3 s value, and the 1:55 to 2:14 row here has LUFS-I -11.9 with ST max -8.2, which is above its LUFS-I because loudness varies inside the section; the section average is not the trough value, so there is no conflict. The video1 sample peaks run from -0.58 to -0.00 dBFS (file maximum 0.99997 of full scale, one sample at or above 0.9999), so "peak -9.5 dBFS at 1:52" in the doc refers to a per-second level, not a sample peak, and is not comparable with the Peak column.
- video2: music_reading.md gives raw dBFS per-second or 12 s mean figures (for example about -9.9 dBFS at 4:24 to 4:36 and a per-second maximum of -9.3). The K-weighted values here (3:24.8 to 4:36.8 at -7.0 LUFS-I) are on a different scale (K-weighting adds boost above about 2 kHz, and the integrated value is gated), so the dBFS and LUFS numbers differ by design and must not be read as a disagreement. The ordering is the same: the 3:24.8 to 4:36.8 plateau is the loudest section by both measures, and the 0:00 to 0:28 prelude is the quietest long section (-19.3 LUFS-I; about -25.5 dBFS in the doc). The sample peak of video2 reaches 0.0 dBFS in the 0:42 to 1:24 section and in every section from 1:28.6 to 4:48.8 (about 354 samples at or above 0.9999 of full scale in the file, so the master touches full scale); the doc does not mention it.
