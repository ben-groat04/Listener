# t_birdwalk: rhythm specialist, round 1

Evidence base: the ten window notes (`win_0000.md` to `win_0180.md`), `audio_features/summary.json` and `beat_times.json`, `stems/stem_rms_per_second.json`, `per_second_levels.json`, window images, and my own measurements from `audio/song.wav` and `stems_raw/htdemucs/song/*.wav` (scripts `v1/scripts/agents/birdwalk_rhythm_r1.py`, `_r1b.py`, `_r1c.py`; drum, bass and 150 Hz low-passed drum-stem onsets with librosa, hop 256 at 44.1 kHz, so about 6 ms resolution). I could not hear anything; every statement is a measurement or an inference from one. Tags: measured, INFERRED, speculative; confidence high/medium/low. Timestamps m:ss.

## 1. Summary

- The track is a loop-built hip-hop / trap-style rhythm piece on a pulse of about 154 BPM in the stripped passages (bar 1.556 s) and about 160-162 BPM in the full-groove passages (bar about 1.48 s), felt in half-time (about 77-81 BPM) because the backbeat hit lands once per four pulses. The tracker's single 152 BPM is about 1.5-6 % slower than what the passages measure; it is a good enough octave-correct label, not the exact tempo.
- Form of the pulse: a repeating alternation between "full groove" (bass + dense drums, 4-5 hits/s) and "rhythm-section dropout" (drums on one hit per bar, no bass, voice and stabs continue). Dropouts: 0:00-0:12, 0:47-0:59, 2:00-2:11 (2:11.4 return), 2:23.4-2:35.7, plus a voice-out drum-led passage 2:47-2:56. Each return is a bass re-entry (+50 dB in the bass stem) with the mix rising 5 to 9 dB.
- The ending is a fade, not a stop (section 9).

## 2. True tempo and octave (measured)

| Evidence | Figure | Reading |
|---|---|---|
| Tracker (`summary.json`) | 152.0 BPM, 484 beats, median IOI 0.395 s; per-20 s medians 152 except 40-60 s 156.7, 60-80 s 161.7, 160-180 s 161.3 | 152 global; local readings rise where the groove has bass |
| Sparse one-hit-per-bar passages, linear fit to hit times | 0:00.8-0:11.7: period 1.558 s (7 hits, residual SD 40.6 ms); 0:47.8-0:58.7: 1.5565 s (8 hits, SD 26 ms); 2:01.3-2:10.6: 1.5555 s (7 hits, SD 23 ms) | three independent fits agree to 0.3 ms: bar = 1.556 s, so 4 pulses = 154.2 BPM. measured, high |
| Full-groove bass onsets, 1:00-1:10 | backbeat hits 1:01.59, 1:03.04, 1:04.53, 1:06.02, 1:07.54, 1:08.98: fitted period 1.484 s, i.e. 161.7 BPM per 4 pulses; bass onsets on bar positions 0.9-1.0, 1.9-2.1, 2.85-3.0, 3.96 (quarter positions), none on the off-beats | groove runs about 5 % faster than the stripped passages. measured, medium (onset detector error about 10 ms; 6 backbeats) |
| 0:25-0:47 hits | win_0020 IOIs 1.37-1.51 s, median 1.44 s (about 167 BPM per 4 pulses); my drum-onset IOIs there cluster at 0.35-0.42 s and 0.67-0.78 s | groove pulse 0.36-0.39 s; the figure is loosely held (SD about 0.04 s) |
| Autocorrelation of onset strength | peak at 0.395-0.401 s (150-152 BPM) in every section, and a strong peak at 1.13-1.19 s (3 pulses) in 0:12-0:24, 1:00-1:10, 1:11-1:23, 2:12-2:23, 2:51-2:56 | pulse 0.39 s everywhere; 3-pulse cycle = the 2-and-3 bass spacing (section 4) |
| Onset density | 12-24 s 3.4/s; 1:34-2:00 4.2/s; 2:50-2:56 4.7/s (median IOI 0.197 s = half a 0.395 s beat) | the drum stem carries a 16th/8th tick of about 0.2 s over the 0.39 s pulse |

Octave resolution. Candidates: about 77-81 BPM (half-time), 152-162 (tracker), about 305-324 (the 0.197 s tick). The 0.2 s tick is a subdivision (hat/roll-like, INFERRED low). Bass and backbeat structure (backbeat once per 4 pulses, bass on quarters at 2-3 pulse spacings) is the hip-hop "half-time" idiom; the tracker value 152-162 is the pulse, and the felt tempo is about 77-81 BPM. INFERRED, medium (the "felt" part is perceptual and cannot be measured; the pulse part is measured, high). I agree with the colleagues' repeated "152 vs 76 stays open" only in the sense that it is a listener choice; my measurement supports 154 (stripped) and 162 (groove) as the pulse.

Tempo variation. Pulse 154 in sparse sections versus about 162 in groove sections is a 5 % difference that persists across repeats (three sparse fits at 154.2; groove fits 159-163 at 1:00-1:10 and 2:50-3:07 see below). Likeliest cause: the sparse bars were separately programmed or sampled loops at a different speed from the groove loops (INFERRED, low), or the tracker's coarse grid blurs it. I cannot separate these. Note the 2:50-3:07 kick gaps (0.39-0.40 s and 0.77-0.80 s) imply 150-154 BPM, so the late groove is nearer 154 than the 162 of 1:00-1:10: the groove is not at one fixed tempo either. Treat "about 150-162, locally varying" as the honest figure; tracker local percentiles (`summary.json` tempo_local 10/50/90 = 103/152/161) agree with the spread.

## 3. Metre

- Beats group in fours: the sparse hit lands once per 4 pulses (bar 1.556 s) with IOI 1.47-1.61 s, uniform level (win_0000: -14.6 to -15.8 dB). 4/4 with the single snap on a bar boundary or beat 3 (INFERRED, medium; the stems cannot say which beat).
- The bass cuts across this: spacings of 2 and 3 pulses (0.74-0.77 s and 1.04-1.14 s, win_0060; my autocorrelation peak at 1.13-1.19 s), so against a 4-pulse backbeat the bass runs a 2+3 (or 3+2+3...) syncopated pattern. I counted bass IOIs in 16ths (0.1974 s): in 0:12-0:47 histogram of IOIs at 1,2,3,4,5,6 sixteenths = 5, 2, 10, 9, 11, 6 (dominantly 3, 4, 5, 6 16ths: dotted spacings, no run of straight 16ths); in 1:00-2:00 = 17, 20, 16, 15, 7, 13 (more short gaps: the bass also does fast runs). measured, medium.
- Not a 3/4 or 5/4 metre: the 0.395 s pulse and 1.556 s bar persist through all sparse passages. High.

## 4. Drum patterns by section (measured onsets from the drum stem)

| Time | Pattern | Evidence |
|---|---|---|
| 0:00.8-0:12.1 | one broadband hit per bar, 0.79, 2.26, 3.79, 5.35, 6.93, 8.53, 10.11, 11.65 (IOI 1.47-1.61, mean 1.556 s); voice chants about 0.2 s syllables | drum onsets; 9 hits, median IOI 1.553 s = 3.93 pulses |
| 0:12.1-0:24 | dense: median onset IOI 0.209 s (0.53 pulse), 3.4/s; bass enters at 0:12.1 | drum onsets; bass +50 dB (stem per-second -68 to -30 dB, 11 s to 12 s) |
| 0:24-0:47 | sparse backbeat about every 1.44 s plus bass stabs every 0.7-1.1 s; hit IOIs cluster 0.37-0.42 and 0.67-0.78 s (1 and 2 pulses); roll at 0:45.2-0:46.7 (bass run 0.13-0.27 s) | drum onsets (my list 25.01, 26.12, 26.82, 27.53 ...), win_0040 |
| 0:47-0:59.4 | back to one hit per 1.556 s (47.79 ... 58.67); bass out; hit at 59.39 ends the passage | fit above |
| 0:59.4-1:10.4 | bass back, backbeat 1.484 s, bass on quarter positions, drum-stem 16th ticks | fit above |
| 1:10.4-2:00 | roll leads into the rapped verse at 1:10.4; drum onset rate 3.9-4.2/s, median IOI 0.20 s; sparse bars at 1:25-1:37 (win_0080) | drum onsets 70-120 s |
| 2:00-2:11.4 | one hit per bar again: 2:01.29, 2:02.86, 2:04.46, 2:05.93, 2:07.54, 2:09.06, 2:10.64, then 2:11.38 (IOI 1.48-1.61; 0.75 s into the bass return = 2 pulses) | fit period 1.5555 s |
| 2:11.4-2:23.4 | kick on first bass note (2:11.39), then syncopated kick gaps 0.75, 0.24, 0.89, 1.23, 0.75 s, quickening to a 0.20 s roll at 2:22.4-2:23.0; stop at 2:23.4 | win_0120, win_0140 |
| 2:23.4-2:35.7 | no drums, no bass; pulse carried by voice and stabs (voice onsets 3.5-3.6/s) | win_0140 |
| 2:35.7-2:47.3 | groove with the voice chopped (median voice-chop IOI 0.33 s); full-mix cuts at 2:42.7 and 2:44.6 | win_0160 |
| 2:47.3-2:56.5 | voice removed; drum stem up about 10 dB from 2:50.3, kicks at 0.39 and 0.73-0.75 s spacing, ticks 0.19-0.22 s | win_0160 |
| 2:56.5-3:08.2 | 0.2 s tick continues, kick gaps 0.40 and 0.77-0.80 s, steady to the fade | win_0180 and my onsets: drum median IOI 0.197 s in 2:56-3:08 |

A kick versus snare split is not reliably measurable. Demucs gives a drum stem whose low band (below 150 Hz) holds only a few onsets in 0:00-0:47 (the "kick" there appears in the bass stem, win_0020, win_0060), so I do not separate kick from 808 bass. The "808-style" label is INFERRED, low (sub energy: share below 60 Hz is 0.35-0.41 in groove sections and 0.01-0.06 in sparse ones, `birdwalk_sections_measure.json`).

## 5. Syncopation and groove feel

- The groove comes from the interaction of three layers on one 0.39 s pulse: backbeat once per bar, a 2+3 bass cycle with a 1.1 s (3-pulse) autocorrelation peak, and a fast 0.2 s tick. The long-short bass spacing (0.75, 1.1, 0.75, 1.1) is the lopsided bounce the colleagues described. measured; feel claim INFERRED, medium.
- Syncopation is bass-led: bass onsets sit on quarter positions but in uneven groups, so the weight falls off the bar start. The drum stem itself is tidy (IOI multiples of 0.19-0.2 s).
- Looseness: the kick-band onsets sit a median 17-24 ms (MAD 12-23 ms, SD 96-164 ms, which mostly reflects detector confusion between kicks and other low-band events) before the tracker beats at 0:12-0:47, 1:00-2:00 and 2:36-3:08. The tracker beats come from the same audio, so this is not an independent test. Stem-level kick spread whole-song is 96 ms (`summary.json`). The spread is far wider than a strictly quantised kick (near 0 ms plus detector jitter of about 10 ms), which is a point against a strict-grid DAW kick; but my detector is not good enough to call it live. Low confidence.
- Hit strength is uniform in the sparse passages (-14.6 to -15.8 dB), which reads as a sample or programmed hit rather than a played one (INFERRED, low). In the bar-by-bar timing, the 7-8 hit fits show residual SD 23-41 ms around a straight line: slightly looser than a quantised hit (0-10 ms), tighter than a human drummer's drift would typically be over a 16 s span. Do not read much into it.

## 6. Stops, drops and accelerations: boundary evidence table (per-second stem dB from `stem_rms_per_second.json`, 10 ms detail from window notes)

Per-second levels are for the second before and after the boundary; "mix" is my 1 s RMS of `audio/song.wav`.

| Boundary | Drums | Bass | Vocals | Other | Mix (dB change) | Carried by |
|---|---|---|---|---|---|---|
| 0:12.1 groove in | -68 to -28 | -68 to -30 | -18 to -19 (none) | -33 to -33 (none) | -18.1 to -13.2 (+4.9) | drums and bass together |
| 0:46.7-0:48 dropout | -33 to -58 (hits go to one per bar from 47.8) | -15 to -70 across 47-48 s (last bass note about 46.65, win_0040) | -19 (continues) | -33 to -36 | -11.3 to -18.7 (-7.4) | bass (and the drum density); voice continues so this is a rhythm-section dropout, not silence |
| 0:59.4 groove back | -68 to -26 | -70 to -24 | -17 to -21 | -31 (none) | -19.1 to -13.3 (+5.8) | bass and drums together |
| 1:10.4 verse | drum roll into it; rate unchanged | unchanged -13 | steps up about nine semitones (win_0060) | -34 to -27 (+7) | -11.2 to -12.6 | vocals and other; rhythm section constant |
| 1:59-2:00 dropout | -23 to -29 then one hit per bar | -16 to -74 | -17 to -23 | -29 to -38 | -10.4 to -19.5 (-9) | bass and drums |
| 2:11.4 return | -68 to -29 | -68 to -20 then -15 | -17 to -20 | -33 to -31 | -19.4 to -13.7 (+5.7) | bass (first kick 2:11.39) |
| 2:23.4 stop | -24 to -60 | -13 to -74 | -20 to -21 (continues) | -28 to -47 | -11.7 to -20.7 (-9, over 2:23-2:24) | drums and bass out together; voice and a stab layer continue: a rhythm-section dropout, not silence (mix stays at -19 to -21 dB) |
| 2:35.7 return | -70 to -28 | -74 to -15 | -20 | -31 to -39 | -14.0 to -13.5 at the stem index; see win_0140 | bass and drums |
| 2:47.3 voice out | unchanged | unchanged | -19 to -70 over 3 s | rises about 8 dB | unchanged (0 to 2 dB) | vocals |
| 2:50.3 drums up | 10 ms: -64.9 to -16.8 | falls 5-8 dB | already -70 | unchanged | no net change | drums |
| 2:56.5 voice back | stays -16 to -20 | -19 to -17 | -56 to -34 (sweep) | unchanged | unchanged | vocals sweep |

Not every dropout is silence: at every dropout above the mix falls 6 to 9 dB only, never below about -19 dB, because voice and "other" stay. The word silence applies to none of them. The 0.07-0.12 s all-stem cuts (2:42.7, 2:44.6, 2:48.6, 2:50.2, 2:51.4, 2:53.3, 2:54.4, 2:56.3, 3:00.2; and 3:02.0, 3:03.2, 3:05.1, 3:06.3 in the last window) are different: all four stems go below -30 dB in the 10 ms envelope for 0.08-0.12 s (mix drop 20-31 dB, win_0160, win_0180). Spacings 1.95, 3.95, 1.65, 1.12, 1.92, 1.15, 1.87, 3.91 s equal 4.9, 10.0, 4.2, 2.8, 4.9, 2.9, 4.7, 9.9 pulses of 0.395 s: stop-start edits that mostly fall on multiples of about 5 pulses and 10 pulses, with the 1.1-1.2 s ones at 3 pulses. measured (window-note onsets, I did not re-derive each cut).

Accelerations: the 0.20 s roll at 2:22.4-2:23.0 (win_0140, 0.51 pulse), the bass run 0:45.2-0:46.7 (0.13-0.27 s gaps), the roll before 1:10.4. All end in a cut or a step, none is a tempo change: the tempo is steady in each passage (tracker beat SD 0.017-0.030 s per 20 s).

## 7. Grid statistics (rule 5)

Every statistic names its grid.
- Kick grid (kick-band onsets, 150 Hz low-passed drum stem): in 2:11.4-2:23 the circular fit gives period 0.3855 s (R = 0.80, n = 17; R at the tracker 0.395 s = 0.40, at the 0.197 s tick = 0.02): the kick sits on a 0.386 s pulse, about 156 BPM, with a 3-pulse and 2-pulse spacing (IOIs 0.75, 0.24, 0.89, 1.23 s; the 0.24 s one is a hurried hit). In 2:36-3:08 the kick-band fit gives 0.386 s (R = 0.30, n = 76), IOI histogram in 16ths: 28 at 2, 18 at 3 (i.e. mostly 0.39-0.60 s gaps), 5 at 4, 16 at 5 to 6.
- Bass grid, 1:00-2:00: best period 0.3695 s (R = 0.27, n = 98): the bass sits on a pulse 7 % faster than the tracker 0.395 s (R at 0.395 = 0.09). 0:12-0:47: 0.3765 s (R = 0.36, n = 46; R at 0.395 = 0.11).
- All drum onsets: best period 0.188-0.192 s (R 0.20-0.59), R at the 0.1974 s grid 0.03-0.28. That is the tick, 0.19 s (a pulse subdivided by 2 at about 158 BPM per 0.38 s). The tracker 152 BPM grid (0.395 s) fits all of these worse than the groove-specific 0.37-0.386 s grids.
- Consequence: any cut-to-beat sync statistic computed against the 152 BPM tracker grid (0.395 s) would be misleading in the groove passages, whose own pulse is 0.37-0.386 s; the sparse passages fit it (0.389 s from 1.556 s / 4 = 154 BPM, 1.5 % faster). Use the kick or bass grid for the groove, and name it.
- Tracker beat IOI against the kick IOI: kick gaps in 2:50-3:07 are 0.40 and 0.77-0.80 s, i.e. 1 and 2 tracker beats (0.395 s). Consistent here. In the groove at 1:00-1:10 kick/bass gaps are 0.37 s multiples, not 0.395 s.

## 8. Production era (INFERRED, medium-high)

Modern production, not a period-consistent archive recording. Figures: sample peak 1.0 (0.0 dBFS), 223 samples at or above 0.999; crest factor 13.5 dB and RMS about -13 dBFS in groove passages (`summary.json` production_era, win_0140); sub (<60 Hz) energy share 0.35-0.41 in groove sections (`birdwalk_sections_measure.json`), a measured modern sub-bass weight with a stem that is empty (-68 dB) until the drop; loop regularity: identical one-per-bar hits, bar 1.5555-1.558 s in three separated passages (spread 0.3 ms between fits), and in-passage residual SD 23-41 ms: loop-like; kick spread against the tracker grid SD 96-164 ms, MAD 12-23 ms: not strictly quantised by my detector, which is rough. Band-limited layer: the whole mix has essentially no energy above about 7-8 kHz in every window (air >6 kHz share 0.0-0.001), so the full-range claim fails at the top. A hard top cut in the mix could mean a low-bitrate or low-pass source (an older or lossy layer) or deliberate filtering; I cannot separate those, and the tonal "other" layer being mid-heavy and wide (side/mid 0.47-0.55 in sparse sections versus 0.02-0.29 in groove) fits a sampled layer under a centred modern sub-and-drum stack. I leave the age of the sample to the sound and lineage specialists. Confidence in "modern production with sampled material" is medium; I give no date.

## 9. End of track (rule 4: 10 ms envelope, last 3 s)

- Duration 188.15 s (3:08.15). 10 ms RMS envelope of `audio/song.wav` (mean of channels): last 3 s ranges -68.3 to -23.0 dBFS; mean level in the last 0.5 s is -56.6 dB; in 0.25 s blocks over the last 3 s: -34.5, -29.3, -34.0, -37.5, -50.6, -34.6, -38.1, -43.8, -41.9, -45.2, -52.5, -60.7 dB.
- Stems, last 3 s min to max: drums -74.5 to -23.2; bass -85.0 to -33.5; other -72.4 to -47.2; vocals -73.1 to -72.1 (flat floor of separation, no voice). Last-0.5 s means: drums -63.9, bass -63.2, other -69.4, vocals -72.5.
- Last audible sound: the mix envelope stays above -60 dB until 3:08.01 and reaches the -70 dB floor at 3:08.14, the end of the file. The fade began at about 3:01.5 (mix -13 dB at 3:01 to -62 dB at 3:08.0, win_0180).
- Hits counted from the 10 ms envelope (peaks with prominence 3 dB or more) in the last 3 s: 6 peaks at 3:05.25 (-23.0), 3:06.02 (-32.3), 3:06.33 (-57.2, this is the edge of the 3:06.31-3:06.41 all-stem cut, an artefact), 3:06.43 (-30.0), 3:07.23 (-37.2), 3:07.62 (-44.9). That is 5 real decaying hits, and the last peak is -44.9 dB at 3:07.62 on a level that has been dropping about 6-7 dB per second. There is no final hit and no final chord: a fade-out. measured, high.

## 10. Feeling the pulse drives (INFERRED; hypotheses a listener may form from the measurements)

- 0:00-0:12: one hit per 1.56 s under a fast chant (about 5 syllables per second, win_0000): a stalled, taunting slow pulse with an urgent voice on top. Cause: the 4-pulse gap against the quick vocal rate.
- 0:12 / 0:59 / 2:11: weight arrives through the bass (+50 dB) with a 5-9 dB mix rise and a narrowing of the stereo image (side/mid 0.47-0.55 down to 0.02-0.29): a release in the chest, not a build.
- Dropouts at 0:47, 2:00, 2:23: the groove removed for 12 s while voice and stabs go on, so the pulse is borrowed from the voice (onset rate 3.5-5.0/s). That is tension through absence, not through silence.
- 2:50-3:08: dense 0.2 s tick with 0.4 and 0.8 s kick gaps and repeated hard cuts every 1.1-3.9 s: a stuttering, mechanical, machine-driven ending, then dissolved by the 6.5 s fade.

## 11. Open points and disagreements with colleagues

- Several window notes quote 152 BPM as the pulse everywhere and treat 0.37 s fits as "half-time of 163". My fits say two tempos (154.2 BPM stripped, about 160-162 groove at 1:00-1:10, about 150-156 in the final minute); the tracker gives 156.7 and 161.7 in two of its 20 s medians, which agrees with the groove being faster.
- win_0020 says no separable kick in the drum stem in 0:20-0:40: my kick-band onset counts agree (very few); I treat the bass stem as carrying the kick-like events there.
- Window notes call some low-band hits "kick"; I do not separate kick from snare or tom body in the stem (demucs bleed); treat "kick" as "low-band drum-stem onset".

## Questions for fellow specialists

1. Sound specialist: the whole mix has no energy above about 7-8 kHz even in the full-groove sections where hats and a drum machine should reach higher. Is that a low-pass on a sample source, a lossy-codec ceiling, or a deliberate production choice, and does the same ceiling appear in the drum stem and the "other" stem separately?
2. Harmony specialist: the bass sits on A1 (55 Hz) while the bass onsets land in 2+3 pulse groups. Does the F#m and D colour at 2:53, 2:57 and 3:05 line up with any bass-pattern change (a note change in the bass stem), or is the bass a single note throughout, so that the harmony is carried only by the "other" layer?
3. Form specialist: the passages with one drum hit per 1.556 s (0:00, 0:47, 2:00) and the 12 s dropouts at 2:23-2:35 all return with a bass entry. Are these the same 12 s loop reused four times (same bar count: 12.1 s, 12.4 s, 11.4 s, 12.3 s), and do the stub passages share the same tonal layer so they can be labelled as one recurring section?

## Not recoverable by measurement

- Whether the felt tempo is 77-81 or 154-162 BPM: it is a listener's choice; measurements give pulse and backbeat spacing only.
- Which hit is a kick, snare, clap or sample: the drum stem is a separation product and low-band onsets in it bleed from the bass stem.
- Whether the drums and bass are a drum machine, a sample loop or a live player: onset spreads (23-41 ms line residuals, 96-164 ms detector spread) are not calibrated against a known live or quantised reference.
- Why the tempo differs by about 5 % between stripped and groove passages: could be separate loop sources, sample stretching or tracker error; the audio does not say.
- The real source and date of the tonal "other" layer and of any older material under the modern drums: the 7-8 kHz ceiling is consistent with several causes.
- Whether the stutter cuts were a performance (live mute, DJ-style) or an edit: the envelope shows hard 10-30 ms edges only.
- Intent and meaning of the half-time reading and of the final fade: not measurable.
