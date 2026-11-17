# Rhythm specialist, round 1 (blind, measurement only): t_cshells_cshore

Scripts: `v1/scripts/agents/rhythm_r1.py`, `rhythm_r1b.py`, `rhythm_r1c.py`, `rhythm_r1d.py` (all on audio/song.wav and stems_raw/htdemucs/song/{drums,bass}.wav, plus audio_features/beat_times.json). I read all 19 window notes and re-measured the main claims. Tags: measured / INFERRED / speculative, with confidence.

## 1. Verdict in brief
- **Metre: 4/4, with an eighth-note engine.** Tracker beat IOI median 0.488 s (122.95 BPM; 590 beats, 1st/99th percentile 0.441/0.538 s). No octave error: the 8-beat lag of 4.0 s and the bar lag of about 1.95 to 2.0 s agree with the 0.49 to 0.51 s beat, and the drum-stem eighth positions (IOI about 0.25 s) sit at twice that. Half-time (about 61 BPM) is not supported: onset density and block spacing both fit 4 beats per 2 s bar. Confidence high.
- **The tempo is not a constant 123 BPM.** The tracker's global 123.05 hides a slow drift (section 3): about 117.5 to 119.5 BPM at 1:00 to 2:20, about 121 at 2:20 to 3:20, about 123 from 3:40, about 125 to 127 near 5:00. Measured, medium confidence (two independent measures agree, tracker per 10 s and autocorrelation of onset envelope per 20 s; the tracker flips between 117.6 and 123.0 so is quantised and unreliable on its own).
- **Form of the pulse:** (a) 0:00 to 0:11.3 digital silence; (b) 0:11.3 to about 0:24 unlocked, stuttering noise-and-click prologue; (c) 0:24 to about 0:48 pulse implied, not played; (d) from 0:48.8 a pulse of struck hits, first every bar, then every 8 beats; (e) 1:04.8 onwards a full drum and bass groove built in four-second blocks; (f) 2:00 to 5:17 a steady driving eighth-note groove with fills; (g) 5:17 to 5:19 drums decay out, 5:24 bass out; (h) 5:19 to 5:42.8 free, pulseless, fading tail; (i) hard gate to digital zero at 5:42.9, 18.1 s of zeros to the file end at 6:01 (360.98 s).

## 2. Evidence for tempo and octave
| measure | result | where |
|---|---|---|
| Tracker beat IOI median, whole song | 0.488 s = 122.95 BPM | beat_times.json (590 beats), summary.json 123.05 |
| Bar lag (4 beats), mix onset-envelope AC, 220 to 300 s | 1.951 to 1.956 s = 123 BPM (AC 0.12 to 0.17; weak because the drums are busy and loose) | rhythm_r1c.py |
| 8-beat lag, 60 to 100 s | 4.011 s = 119.7 BPM (AC 0.54, strong) | rhythm_r1c.py |
| Big mix attacks 60.79, 64.79, 68.81, 72.83 s | IOI 4.00, 4.02, 4.02 s = 8 beats at 119.4 to 120 BPM | rhythm_r1b.py (10 ms mix jumps over 9 dB) |
| Drum-stem eighth IOI, 3:00 to 4:00 | about 0.245 to 0.255 s = eighths at 118 to 123 BPM | colleagues' windows 180 and 220, my phase histograms |
- Octave check: a 61.5 BPM reading would need a beat of 0.98 s. The drum stem has hits at 0.49 s multiples and at 0.245 s, and the bass plays quarter notes with IOI 0.476 to 0.479 s (my bass onsets, 140 to 160 s and 180 to 200 s). A 246 BPM reading would need 0.244 s as the beat; chord changes land every 2 to 4 s (1 to 2 bars), which fits 123 not 246. Confidence high for about 120 to 123 BPM in 4/4.

## 3. Tempo drift (new finding, measured, medium confidence)
Tracker BPM per 10 s (rhythm_r1b.py): 50 to 140 s mostly 117.4 to 117.6 (period 0.51 s), 140 s onwards mostly 123.0 (0.488 s), 280 to 310 s intermittently 129. Onset-envelope autocorrelation beat lag (mix, per 20 s, rhythm_r1c.py):
| start | 60 | 80 | 100 | 120 | 140 | 160 | 180 | 200 | 240 | 260 | 300 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| beat BPM | 119.1 | 117.9 | 116.8 | 119.1 | 121.5 | 122.7 | 120.3 | 124.0 | 124.0 | 122.7 | 127.9 |
| 8-beat BPM | 119.7 | 118.5 | 117.5 | 119.4 | 121.0 | 121.6 | 121.2 | 118.8 | 123.7 | 125.1 | 126.9 |
So the track appears to start at about 120 BPM (1:00), dip to about 117.5 BPM at 1:40 to 2:00, and then rise to 121, 123 and about 126 by 5:00: a net push of roughly 6 to 7 percent over four minutes. The 4 s block spacing lengthens from 4.01 s (1:00) to 4.05 s (1:20) to 4.09 s (1:40) in the autocorrelation, then shortens to 3.95 s by 2:40. Interpretation (INFERRED, low to medium): played or tracked in real time, or a hand-drawn tempo map, rather than a rigid DAW clock; a fixed-tempo loop would give one constant lag. The alternative (a stem-separation or tracker artefact) cannot be excluded: the 20 s windows are short and the drum AC values at 200+ are only 0.1 to 0.3. A gradual accelerando is felt as quiet urgency even though the listener will not name a tempo change.

## 4. Section-by-section rhythm
### 0:00 to 0:11.3: silence
Mix -240 dBFS (exact zeros). Stem values -84 to -96 dB are the separator floor. Not a rhythm-section dropout (all stems and mix at floor). First non-zero sample 0:11.299 (colleague, win_0000; I did not re-derive). Confidence high.

### 0:11.3 to about 0:24: unlocked glitch prologue
Tracker gives beats from 11.331 s (11.33, 11.87, 12.35 ...) with 0.40 to 0.56 s spacing, but my drum-onset phase histogram against that grid is flat-ish (8 bins [1,3,6,4,6,8,0,12], n=40) and kick-band IOIs run 0.05 to 0.44 s (win_0000). Drum onset rate 3.1/s, drum stem -43 dB RMS at 10 to 20 s. So there is activity but no locked metre: stuttering, broken (INFERRED, medium).

### 0:24 to 0:48: pulse implied only
Drum stem -78 dB (20 to 30 s) and -87 dB (40 to 50 s): no drum evidence; my script finds too few drum onsets (under 8) to test. Tracker still beats at 123 BPM (30 to 60 s: 123.0), but the onset autocorrelation there peaks at only 0.27 (win_0020). The tracker is following chord flips or texture, not a played groove (low to medium). 0:43.4 to 0:47.4: a 4 s gap with no strokes (win_0040). Not silence: other stem continues.

### 0:48.8 to 1:04.8: struck pulse, drums bleed only
Mix attacks (jumps over 9 dB within 10 ms) at 48.81, 52.80, 54.82, 56.78, 58.85, 60.79, 62.81, 64.79 s: intervals 3.99, 2.02, 1.96, 2.07, 1.94, 2.02, 1.98 s, i.e. one hit per bar (4 beats at 0.49 to 0.505 s), then from 64.79 every 8 beats (4.02 s). Per win_0040 the strokes in 47.5 to 59.9 s fall within 0.03 s of the tracker grid. Drum stem -66 dB (50 to 60 s) to -37 dB (60 to 70 s): the first real drum hit is at 1:04.84 (win_0060: drum stem -81 dB RMS before, -35 dB after; I re-checked the 10 s levels). Grid: the tracker beat grid at about 119 to 123 BPM; hits are within +10/-20/+30 ms of tracker beats (n=3, win_0060, low).

### 1:04.8 to 2:00: building, four-second blocks (8 beats)
Pattern: full-band stab, then 25 dB decay over about 3 s, repeated 1:00.9, 1:04.8, 1:08.8, 1:12.9, 1:16.8 (win_0060), then 1:20.8, 1:24.9, 1:28.9, 1:33.0, 1:37.0 (win_0080). Onset-envelope AC peak at 4.0 s is 0.56 (60 to 100 s) and 0.54 (100 to 140 s), the strongest periodicity in the track. Drum stem rises to -34 dB by 1:10 and bass from -53 dB (1:00) to -29 dB (1:10), so the rhythm section is added piece by piece (drums 1:04.8, bass about 1:06, both forward 1:13). Drum onset rate 0.95/s (1:00 to 1:20) rising to 3.15/s (1:20 to 1:40) and 4.1/s (1:40 to 2:00). Drum phase histogram (8 bins of tracker beat, beat at bin 0 or 8, 1:20 to 1:40): [10,7,3,17,5,1,1,19] is concentrated at bins 3 and 7 (the 8th-note positions, with the tracker running about 12 to 33 ms late): eighth-note chatter. Before each stab there is a gap of 0.9 to 1.5 s (win_0080: 1.18, 1.07, 0.93, 1.53 s) then a run of 0.09 to 0.14 s hits: a fill-and-hit rhythm. Dropout: 1:33.8 to 1:36.6 bass stem -50 to -79 dB with mix at -20 to -40 dBFS (partial, not silence). Fill at 1:52.5 (drum stem -42 to -24 dB, one big hit), entry of pulsing bass quavers 1:53.4 (win_0100). Confidence: high for the 8-beat block structure, medium for the sub-structure.

### 2:00 to 5:17: the groove
From 2:00 drum stem -28 dB and bass -24 dB; both stay within about 5 dB for the next 3 minutes (10 s stem levels, rhythm_r1.py). Drum onset rate falls from 4.1/s (1:40 to 2:00) to 2.85/s (2:00 to 3:20), 2.25/s (3:20 to 4:00), 1.9/s (4:00 to 5:00) (fewer hits, bigger gaps, less chatter). Phase histograms 2:00 to 3:20: [7,4,3,31,3,9,0,57] (n=114) and 3:20 to 4:00: [0,6,3,34,1,5,0,41] (n=90): about 75 to 90 percent of drum onsets fall on eighth positions (beat and offbeat), nothing on the 16th-note spaces except fills. With the tracker offset removed (offset -33 to -38 ms, so the onset detector fires about 35 ms before the tracker's beat; a detector-versus-tracker latency, not a groove statement), the median deviation from the nearest sixteenth is 9 to 11 ms (p90 30 to 33 ms) against about 30 ms expected for uniform scatter (grid: tracker beat grid with offset removed, period 0.488 s, sixteenth 122 ms; the onsets' IOI of 0.245 s agrees with the eighth, so this is a valid grid check). So drum onsets in general are fairly quantised to a sixteenth grid. This disagrees with colleagues' kick-only figures of 108 to 132 ms (windows 200, 220), which come from a 40 to 120 Hz detector that picks up sub-bass leakage and toms; I treat their kick spread as an upper bound (see section 6). Hat/top band (6 to 10 kHz), 2:20 to 3:20: phase histogram [46,0,0,12,21,1,4,14] with IOI median 0.479 s: hats or noise on the beat, with a lesser accent on the offbeat. 3:20 to 5:17 the hats thin (n=36, n=19 per segment).

Specific events (from windows, I re-measured the drum envelope and levels):
- 2:07.5 dense roll (0.06 to 0.1 s), 2:09.5 hats open (centroid 2.5 to 5.2 kHz; win_0120).
- 2:21.5 voice sample enters; fills 2:20.2 to 2:21.9 and 2:24.4 to 2:25.1 (win_0140).
- 2:34.5 to 2:36 drum top (4 to 8 kHz) thins for about 1.5 s; bass continues; 2:40 dense burst; 2:53 to 2:54 drum stem dropout (win_0160).
- 3:00 to 3:07 bass plays sharp quarter notes (IOI 0.49 to 0.51 s; mine: 0.476 s for 3:00 to 3:20) with gaps; 3:07 to 3:13 bass quickens to eighths and sixteenths (0.23 to 0.26 s), then back to quarters (win_0180).
- 3:28 to about 3:30: gap in drums about 3:28.3 (win_0200 "dark vertical gap" at 208.3 s) and a half-time looser feel at 3:29 to 3:32 (kick IOIs 0.73, 1.31 s, low to medium).
- 3:30 to 4:00 bass stem falls to about -50 dB (10 s levels at 230 and 240 s: -50, -47 dB): bass out, drums continue at -26 dB, so the downbeat anchor goes and the pulse rides on drum clicks and pad (win_0220). Bass returns 4:06 to 4:13 and finally about 4:46.5 (win_0240, win_0280).
- 4:06 to 4:07.5 and 4:15 to 4:15.5 sixteenth-note rolls (0.12 to 0.16 s) (win_0240); 4:23 to 4:39 bunches of 0.25 s steps (win_0260).
- 5:00 to 5:07 drum-only tempo about 123 BPM, 5:12 to 5:13.5 dense burst (about 14 onsets in 1.5 s), 5:15.4 to 5:17.1 last cluster (about 11 onsets) (win_0300).

### 5:17 to 5:42.8: dissolve
Drum stem 10 ms max: -19 dBFS at 5:17.1, -27 (5:17.2), -37 (5:17.8), -48 (5:18.2), -70 (5:18.9) (win_0300), then about -72 to -75 dB (10 s level 320 to 330 s: -75 dB, then -84 to -96). So the drums decay over about 1.8 s with one weak residual (5:18.86): a decay-out, not a hard stop. Bass stem is out by about 5:24 (win_0300; below -60 dB at 324.5 s, win_0360), but the 10 s level at 320 s still reads -27.8 dB because of the first 4 s; consistent. Mix level 5:17 to 5:30 stays about -15 dBFS (my 10 ms RMS: -14.9 at 317 s, -15.9 at 320 s, -14.7 at 325 s, -19.0 at 330 s) so the loss of drums and bass is carried by the other stem, which is why the mix falls only about 0 to 1 dB across the drum exit (the drums were not the loudest layer; the other layer was). After 5:19 no pulse: the tracker has no beats after about 350 s and my autocorrelation lags there (0.46 to 0.56 s, AC 0.16 to 0.44) are just noise. Mix after 5:30: -19 (330 s), -36.8 (335), -51.6 (340), -63.6 (342), -70.6 dB (342.8). Voice-like envelope bumps at 5:41.3 to 5:42.6 (win_0340, win_0360) are syllables, not beats; I claim no grid.

## 5. Boundary evidence table (re-measured with 10 s stem levels and 10 ms mix jumps)
| boundary | drums | bass | vocals | other | carries it |
|---|---|---|---|---|---|
| 0:11.3 sound begins | -96 to -44 dB (+40) | floor (bleed only) | floor (bleed only) | -86 to -50 dB (+36) | drums + other; mix -240 dBFS to -48 dB RMS |
| 0:48.8 first struck hits | -87 to -66 dB over 40 to 60 s (still near floor, bleed) | floor | floor | strokes (win_0040) | other stem |
| 1:04.8 drums enter | -81 to -35 dB (about +45) | -84 (floor) to -53 over 60 to 70 s, rising to -29 | none (-75 dB or below) | continues about -32 dB | drums, then bass at about 1:06 |
| 1:33.8 to 1:36.6 | continue | -50 to -79 dB (gone) | none | gapped, not silent (mix -20 to -40 dBFS) | bass |
| 1:52.5 (fill) | -42 to -24 dB (one hit) | rises -28 to -25 | none | out (-73 to -67) | drums |
| 3:28 to 3:32 half-time | sparse; gap at 3:28.3 | absent | none | present | drums (sparse) |
| 3:30 to 4:00 | continue at -26 | -50 / -47 dB (10 s levels) | none (see voice colleague) | pad continues | bass out |
| 5:17 to 5:19 | -19 dBFS peak to -70 in 1.8 s | continues to about 5:24 | n/a | continues | drums exit |
| 5:24 | -75 dB | -62 to floor | n/a | continues | bass exit |
| 5:42.8 | floor | floor | -77 to -92 dB | -71 to -89 dB | vocals + other, then digital zero at 5:42.90 |
Not rechecked individually for every drum stop; all are re-confirmed from the 10 s stem table or from the window authors' 0.1 s tables. "Silence" is used only for 0:00 to 0:11.3 and from 5:42.9 (all stems and mix at floor, mix exact zero).

## 6. Drum patterns, kick, syncopation (with caveats)
- **Eighth-note engine** (measured, medium): drum-stem onset phases (tracker beat grid, 0.488 s, offset corrected) cluster at beat and "and": 120 to 200 s [57 at beat, 41+23 at 'and'], 200 to 320 s [55, 35+28]. A 16th-note layer exists but is sparse (bins 3,4,11,12: about 5 to 13 per segment), mostly fills (4:06, 4:15, 4:23, 4:31, 5:12 to 5:17).
- **Kick**: my 40 to 100 Hz kick detector (drum stem, 5 ms hop) is not a clean four-on-the-floor. Phase against the beat grid (R, 0 to 1): 0.13 (1:20 to 2:20), 0.06 (2:20 to 3:20), 0.06 (3:20 to 4:20), 0.04 (4:20 to 5:17). Only for 1:20 to 2:20 do kicks land on the tracker beat (44 percent within 30 ms of the offset-corrected beat against 12 percent chance; spread of those 13 ms). From 2:20 on they hit off the beat (bin positions 2 to 3 and 6 to 7 of 8, i.e. the offbeat and the "e"/"a"), 3 to 6 percent within 30 ms of the beat. Kick IOI median 0.26 to 0.29 s (eighths). I therefore read the 2:20 to 5:17 groove as **syncopated or offbeat low hits over an on-beat hat and a quarter-note bass**, but the kick band also catches toms and bass bleed and the demucs drum stem is a separation product (INFERRED, low to medium). Colleagues' earlier statements range from "tight, grid-like" (win_0120) to "loose, 108 to 132 ms SD" (win_0200, 0220); my measurement says: the drum hits as a whole are quantised to the sixteenth grid (median 9 to 11 ms) but the kick-band events do not sit on the beat. A strict kick inter-onset interval of 0.488 s (four-on-the-floor) was found only 14 to 17 percent of IOIs within 25 ms of 0.49 or 0.98 s: not four-on-the-floor.
- **Bass**: quarter notes at IOI 0.476 to 0.479 s in 2:20 to 2:40 and 3:00 to 3:20 (mine: median 0.479 and 0.476 s, n=48 and 35), eighths and sixteenths in 3:07 to 3:13, eighth quavers 0.20 to 0.27 s in 1:53 to 2:00 (win_0100, mine: 0.309 s median 1:40 to 2:00). Bass is the metronome; the drums supply the density and the fills.
- **Syncopation**: from the kick findings and the 0.5 s bass rests on offbeats (win_0120). INFERRED, low to medium.
- **Bar repetition**: bar-to-bar correlations of drum envelope are 0.0 to 0.3 (win_0120, 0200, 0260, 0300 all report values near zero) so there is no sample-identical loop. Yet the spectral/harmonic layer repeats at 4 bars (chroma 0.47). INFERRED: played or varied drums over a repeating harmonic loop (see section 7).

## 7. Production-era cues (rule 1; INFERRED)
- Peak: song.wav sample peak = 1.0 (0.0 dBFS); mix 10 ms RMS about -15 dBFS in the loud parts (my 10 ms envelope, 5:17 to 5:30), so a limited modern master (high).
- Loop regularity: 4.00 s hit spacing within 20 ms for five cycles (60.79, 64.79, 68.81, 72.83), but the content differs per cycle and the tempo drifts 117.5 to 127 BPM, which a rigid DAW loop would not do. A DAW-arranged repeated block with performed or hand-tempo-mapped content (medium to low).
- Kick onset spread: drum-stem all-onsets median deviation from the sixteenth grid 9 to 11 ms (p90 30 to 33 ms); kick-band spread 108 to 132 ms (colleagues; rhythm_r1d: kicks mostly off the beat). Neither is "strictly quantised kick on a grid". Together with the drifting tempo this suggests human-played or hand-programmed drums, not a plain quantised machine pattern (low to medium).
- Band-limited layer: not checked by me (sound specialist). From win_0000 the opening noise layer reaches 13 kHz.
- Net: modern production and mastering (digital zero edges, full-scale peak, stems with fill and drop-out edits) over a groove that is more human than machine (medium). No evidence either way about older source material from my rhythm data.

## 8. Sync statistics
I make no cut-versus-beat statistic (picture is not my task). The grids named and checked above: tracker beat grid, 122.95 BPM and per-section BPM; kick-band IOI (median 0.26 to 0.29 s on 2:20 to 5:17, 0.49 s on 1:20 to 2:20). Where the grid and the IOI disagree (2:20 onwards, kick against the beat), I give no beat-based sync claim for the kick. The 4 s (8-beat) block grid is the only one on which events (stabs) are within about 20 ms of each other.

## 9. How the pulse drives the feeling
- The 11.3 s of exact silence then a hard attack at 0:11.3 creates tension and surprise (cause: mix -240 dBFS to peaks near -22 dBFS).
- Pulse withheld: 0:24 to 1:04 has no drums; hits arrive every bar then every 8 beats, and the groove is added one layer at a time (drums at 1:04.8, bass at about 1:06). The listener waits for the groove; arrival is felt as release (INFERRED, medium).
- The 4 s stab-and-decay cycle (25 dB fall in about 3 s) is breathing, in a metaphor sense: a recurring swell with a measured period of 4.0 s (0.25 Hz).
- From 2:00 the quarter-note bass over eighth-note drums at about 121 to 126 BPM and creeping tempo is propulsive and urgent. Off-beat low hits give push; roll bursts (4:06, 4:15, 5:12) are tension spikes.
- 5:17 to 5:19 the drums decay and the beat is gone, 5:24 bass is gone, leaving free time, then a fade to 5:42.8: a pulse that loosens into nothing.

## 10. End of track (rule 4; I verified the main figures)
10 ms mix envelope over 300 to 360.98 s: sample peak of the whole song 0.0 dBFS; mix at -14.9 dB (317 s), -19.0 (330), -36.8 (335), -51.6 (340), -63.6 (342), -70.6 dB (342.8); last 10 ms frame above -80 dB at 342.81 s; then exact zero (colleague: drop to zero at 342.90 s; the last 3 s (357.98 to 360.98 s) are all zero, so final hits counted in the last 3 s: 0). Last audible sound 5:42.8; level at the end of the audible tail about -70.6 dB; the file then runs 18.1 s of digital silence. Gate: a sharp step from -70 dB to zero after a roughly 12 to 13 s fade (starting about 5:30), consistent with a DAW/editor export. No final drum hits (drums left by 5:19).

## 11. Disagreements with colleagues' window notes
- win_0000: "beat tracker not locked 107 to 150 BPM" agrees; my phase histogram supports that.
- win_0040: "the pulse is carried by strokes of the other stem": agrees; my drum stem there is at -87 to -66 dB.
- win_0120 (tight, grid-like drums) versus win_0200/0220 (loose, 108 to 132 ms SD): both partly right. All-drum onsets sit within about 10 ms of a sixteenth grid; the kick band is off-beat and spread.
- win_0100 mean 118.5 BPM and win_0120 "123 BPM": my autocorrelation says 117 to 119 BPM until 2:20, 121 BPM from 2:20; the 123 BPM in the later windows is a tracker constant.
- win_0300 "decay over about 1.8 s": confirmed in my 10 s drum levels (-75 dB at 320 to 330 s).

## 12. Three questions for fellow specialists
1. **Harmony**: the chord changes at 2 to 4 s intervals (1 to 2 bars) and the 4 s stab cycle (8 beats) in 1:00 to 2:00: do chord changes land on the stab attacks (1:24.9, 1:28.9, 1:33.0) or between them, and does the harmonic rate also drift with the tempo (4.0 s then 3.95 s)?
2. **Sound**: is the layer that carries the pulse from 0:48.8 to 1:04.8 (stabs, drums at floor) a plucked, struck or sampled sound, and are the 4 s stab decays (about 25 dB in 3 s) a reverb or gate shape, to see whether the "other" stem is a sampled loop?
3. **Form**: if the tempo creeps from about 117.5 BPM (1:40 to 2:00) to about 126 BPM (5:00), does that match your section boundaries (2:00, 3:00, 4:00, 4:46), and is the 5:17 to 5:19 drum decay the start of an outro or a separate section?

## Not recoverable by measurement
- Whether the drums are a live kit, a sampled kit or a drum machine: only onset spacing and stem bleed are measurable; the separator smears kick, tom and bass.
- Whether the tempo drift is intentional (performed rubato or a tempo map) or an artefact of tracker and stem separation: only 20 s windows are available.
- The true kick pattern (position and count): kick-band detection includes toms and bass leakage.
- What the stabs and noisy opening layer are (instrument, sample, field recording) and their source or age: unpitched broadband energy only.
- Whether the 11.3 s opening silence and the 18.1 s trailing silence belong to the release or are artefacts of this file.
- Intent behind the rubato ending: only the level and envelope are measurable.
