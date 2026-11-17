# Video2: the narrator and the chopped voice as a musical voice (Elfstedentocht Part 2)

Measured from the vocals stem (`v1/data/video2/stems/vocals.mp3`) with scratchpad scripts in `/tmp/claude-0/-home-user-Listener/cb832643-599e-5a16-8ae7-147fc9b20f96/scratchpad/t7/` (`measure.py` helpers, `run_main.py` pitch/rate/bass table, `analyse.py` grid, alignment, rate and bass tests, `fragdur.py` beat-position counts, `prov3.py` and `sens.py` the provenance test and its sensitivity, `title_take.py` same-sentence check, `tables2.py` the phrase table; logs `analyse.out`, `main.log`, `prov3.log`). Scratchpad files can be cleared, so the methods are written out below. Tags: OBSERVED (measured, with the stated error), INFERRED (follows from measurement plus a stated assumption), SPECULATED (idea only).

Whisper is a hint only. "MUZIEK" (0:28.6, 3:21, 4:16.5, 4:58.9) and the Welsh-looking line "Cymysg y maraton ymlaen" (vocals pass, 0:50 to 1:00) are hallucinations and non-events; the stem has no phrase at 0:28 to 0:30. The Whisper words at 3:25 to 3:48 ("eerst", "slop", "in de ...") are not used. Words below are ASR hints, not transcription. Narrator identity, sex, intent and emotion are not claimed.

## In plain words

Treated as an instrument, the narrator is a **low, dry, unsung voice**, lower and a little tighter than in Part 1: the median of the phrase medians is 147.5 Hz (D3; nine phrases), individual medians 116 to 153 Hz (A#2 to D#3). Inside a phrase the pitch wanders about 5 semitones (middle half), so it is speech inflection, not a held note. It sits an octave and a half above the bass.

It is **moderately steady in speed**: 4.0 envelope peaks a second inside a phrase (roughly syllables; sd 0.57, range 3.4 to 5.1), 3.2 once the gaps are counted, with no trend that nine phrases can show.

**Against the beat the narration is free**: starts and ends fall where chance would put them against the 120 BPM grid (p above 0.07 on every pre-specified distance test; two phrase-end R values at the bar period, p_R 0.021 and 0.036, are explained in section 3 and not claimed). That grid is also not shown to exist before the 1:28.6 drop (its pulse phase differs there), so the narration before 1:28 cannot be tested against it at all.

**The chopped voice from 3:28 is the opposite.** Its fragments (34 stem phrases, median length 1.07 s, about two beats) **start on one fixed beat of the four-beat cycle** (22 of 34, binomial p about 5e-6 after allowing for four candidate beats; clustering at the one-bar period R 0.75, p below 1e-4) and **tend to stop two beats later** (19 of 34 end on the third beat of the cycle). They are repeated copies of each other (45 of 784 tested pairs match above the null range, 19 of 29 fragments have a partner with correlation over 0.5), and they are **not shown to be copies of the narration**: no fragment matches the narration recording forwards or reversed at pitch/speed ratios from 0.5 to 4 (0 of 29 below p of 0.05). The fragment pitch is also high (median about 400 Hz, G4, with a few near 850 Hz), about 17 semitones above the narrator.

**The earlier claim "four or five syllables a second" is replaced** by the measured figures in section 2: 4.0 within phrases, 3.2 including gaps.

## 1. Pitch

Method: pyin (librosa 1.0.1), 10 ms hop, lenient voicing prior (stricter settings found almost no voiced frames), run at 2048 and 4096 sample windows, on the stem band-limited from 70 Hz to four times the top search frequency. Narration (before 2:37): search 70 to 400 Hz. Fragments (from 3:28): search 70 to 1200 Hz. A phrase is a run of stem energy within 30 dB of the stem's 99th-percentile level, gaps under 0.35 s merged, longer than 0.25 s. f0 is reported only where at least 30 voiced frames exist. Error: the two window sizes agree to a median 0.30 semitone and at most 1.3 semitones on the narration; contour first-quarter to last-quarter medians are shown but are not trusted (octave jumps).

Narration phrases (those overlapping a trusted ASR segment). Two stem runs, 0:59.1 to 1:01.1 and 1:04.5 to 1:10.4, have no ASR text in the pass used here (earlier notes read them as narration, "200 km ... strongest", medium confidence); they are excluded from the statistics.

| Span | ASR hint (mix, Whisper medium) | Voiced frames | f0 median Hz (note) | f0 IQR (st) | f0 first to last quarter (Hz) | Envelope peaks | Rate within run (peaks/s) |
|---|---|---|---|---|---|---|---|
| 0:42.6 to 0:45.7 | 18 januari 1963. | 198 | 152 (D#3) | 3.8 | 153 to 144 | 10 | 3.41 |
| 0:51.3 to 0:53.9 | Van het schaatsmarathon Zonderweg. | 176 | 132 (C3) | 5.4 | 137 to 331 | 8 | 3.47 |
| 1:20.0 to 1:22.6 | Stort zijn voor de twaalfde elfste... | 124 | 152 (D#3) | 11.3 | 159 to 274 | 9 | 3.90 |
| 1:24.5 to 1:28.6 | Waar iedereen zich voor opmaakt,... | 180 | 116 (A#2) | 9.4 | 278 to 96 | 14 | 3.59 |
| 1:49.2 to 1:52.1 | Temperatuur 16 graden beneden. | 205 | 147 (D3) | 5.2 | 120 to 112 | 11 | 4.22 |
| 1:53.4 to 1:56.3 | Een monsteret van ruim 200 kilomet... | 197 | 131 (C3) | 4.4 | 171 to 115 | 12 | 4.66 |
| 2:25.4 to 2:28.4 | 575 metstrijdrijders, rond 9500 to... | 219 | 147 (D3) | 3.8 | 146 to 247 | 11 | 4.27 |
| 2:29.0 to 2:31.8 | (same ASR segment) | 202 | 147 (D3) | 2.7 | 143 to 138 | 11 | 5.10 |
| 2:32.5 to 2:36.1 | (same ASR segment) | 159 | 153 (D#3) | 13.8 | 110 to 300 | 11 | 3.40 |

Summary (n = 9): median of phrase medians 147.5 Hz (D3), range 116.0 to 152.7 Hz, between-phrase standard deviation 1.5 semitones (the narrator holds close to one pitch region), median interquartile range inside a phrase 5.2 semitones. Phrase-end minus phrase-start median -0.7 semitone, falling in 5 of 9: a falling tendency is not established. The pyin tracker cannot separate D3 (146.8 Hz) from D#3 (155.6 Hz) reliably here, so no pitch-class claim is made.

Fragments (3:28 to 5:00, 34 stem phrases, 23 with at least 30 voiced frames): median of phrase medians 401 Hz (G4), 10th to 90th percentile 193 to 835 Hz, range 156 to 1033 Hz. Twelve medians lie between 378 and 465 Hz (F#4 to A#4), four are at or above 800 Hz, four below 250 Hz. A quiet high fragment at 4:32.6 to 4:33.5 is tracked at 849 Hz (G#5; 91 voiced frames), which agrees with the earlier note of a high G#5 phrase near 4:31 to 4:35, but it spans 0.9 s here, not four seconds. The vocals stem leaks the "other" layer and hats, so these fragment pitches may be partly leakage and are held at low confidence: they show tonal content, not necessarily a voice pitch (INFERRED at best).

## 2. Syllable rate (replaces "four or five syllables a second")

Method: the stem is band-passed 300 Hz to 3 kHz, its short-time level (25 ms window, 10 ms hop, 50 ms smoothing) is peak-picked with at least 3 dB prominence, at least 80 ms apart, within 20 dB of the phrase maximum, over the phrase padded 0.15 s each side. No voicing gate. A peak is read as roughly one syllable nucleus. Rate within a run is (peaks minus one) divided by first-to-last peak time; "including edges" is peaks divided by (run length plus 0.3 s).

Calibration on the repeating sentence "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht" (nominal 15 syllables if fully pronounced, my own count, not verified against the audio): 14 peaks here (1:24 to 1:28.6), 15 and 14 in video1. Count error 0 to -1 of 15 (about -7 % at worst).

| Measure (9 phrases of at least 1.0 s with at least 5 peaks) | Value |
|---|---|
| Rate within runs, mean / median | 4.00 / 3.90 peaks per s |
| Spread between phrases (sd; CV) | 0.57 (CV 0.14) |
| Range | 3.40 (2:32.5) to 5.10 (2:29.0) |
| Rate including run edges, mean / median / range | 3.22 / 3.18 / 2.72 to 3.80 |
| Peak-to-peak interval, pooled median / mean / CV | 0.230 s / 0.253 s / 0.45 |
| Rate against phrase start time | Spearman rho +0.37, p 0.33 (no trend detected; nine points) |
| Title sentence rate (first to last peak) | 3.59 |

Reading: the old "four or five a second" is too high for Part 2 as a general figure. Measured: 4.0 within phrases (only one phrase above 5), 3.2 with gaps. It is roughly 0.4 peaks a second slower than Part 1 (4.4 and 3.6), a difference that nine against sixteen phrases cannot establish. The median interval of 0.23 s is close to an eighth note at 120 BPM (0.25 s), but the interval spread is wide and the alignment tests below show no locking, so this is a coincidence of one number (SPECULATED that it means anything). Rate was not measured for the fragments; they are not words.

## 3. Phrase against the 120 BPM bar grid

Grid: period 0.49995 s (the rhythm specialist's kick-fit period); pulse phase measured here as the circular mean of the kick-band (30 to 150 Hz) spectral flux of the drums stem over 1:32 to 4:58, phase 0.121 s after time zero (R 0.46; by sections 1:40 to 2:30, 2:30 to 3:30 and 3:30 to 4:58, 0.116, 0.118 and 0.124; the 150 Hz to 2 kHz band gives 0.117; the amplitude peaks of kick hits give 0.134 to 0.142; so the phase is good to about 0.02 s). **The grid does not exist before the drop**: over 0:44 to 1:24 the same flux has R 0.20 at a different phase (0.458 s), so narration before 1:28.6 has no verified grid and its results are shown only for completeness. The drum return at about 1:28.8 falls 0.19 s after a grid beat, and the later loop changes at about 2:36.8 and 3:24.8 also fall at about +0.2 s after grid beats, all on the beat whose index is 1 modulo 4 (beat indices counted from time zero); so I take that beat as "beat 1" of the four-beat cycle (INFERRED, because the sections start about 0.2 s after the kick phase and the three times are rounded values from earlier work).

Statistic: mean distance of each event to the nearest grid line as a fraction of the period (chance 0.25). Nulls: (a) grid slid to 500 even phases, (b) events redrawn uniformly over the same span (20,000 draws, fixed seed). R is the mean resultant length at the grid period; p_R its Monte Carlo p (20,000 draws). Event times come from the stem-energy threshold (starts may be up to about 0.1 s late, ends up to about 0.1 s early). Bars use four-beat lines at all four phases; **phase 1 is the pre-specified one** (the section-anchored beat 1); the others are post hoc.

Narration:

| Event, grid | n | mean dist / period | p (grid-shift) | p (uniform) | R (p_R) |
|---|---|---|---|---|---|
| Starts, beat, 0:42 to 2:36 (grid unverified before 1:28.6) | 9 | 0.238 | 0.46 | 0.40 | 0.33 (0.39) |
| Ends, beat, same | 9 | 0.220 | 0.074 | 0.27 | 0.12 (0.89) |
| Starts, bar phase 1, same | 9 | 0.228 | 0.42 | 0.32 | 0.26 (0.57) |
| Ends, bar phase 1, same | 9 | 0.223 | 0.44 | 0.29 | 0.60 (0.036) |
| Starts, beat, after 1:28.6 | 5 | 0.287 | 0.63 | 0.71 | 0.45 (0.38) |
| Ends, beat, after 1:28.6 | 5 | 0.274 | 0.90 | 0.64 | 0.13 (0.93) |
| Starts / ends, bar phase 1, after 1:28.6 | 5 | 0.275 / 0.237 | 0.59 / 0.48 | 0.64 / 0.42 | 0.57 (0.20) / 0.84 (0.021) |

The two R values with p_R of 0.021 to 0.036 are phrase **ends** at the bar period; they come from mean offsets away from beat 1 (the bar-phase-1 distance statistic is null, p 0.42 to 0.48), and they sit in 8 bar tests with n of 9 and 5. Post hoc, bar phase 0 ends show p 0.012 (shift) and 0.005 (uniform) with n = 9 (and 0.012 and 0.002 with n = 5 after 1:28.6); allowing for 8 bar tests this is about 0.1 and 0.04 for n = 9, on a grid unverified before 1:28.6. **Not claimed.** "Voice on the bar" is not supported for the narration; the narrator is free-timed. Power is low: nine and five phrases.

Fragments (3:28 to 5:00):

| Event, grid | n | mean dist / period | p (grid-shift) | p (uniform) | R (p_R) | Within 0.1 s |
|---|---|---|---|---|---|---|
| Starts, beat | 34 | 0.158 | 0.072 | below 0.0001 | 0.44 (0.0013) | 21 of 34 |
| Ends, beat | 34 | 0.227 | 0.38 | 0.18 | 0.32 (0.034) | 15 of 34 |
| Starts, bar phase 1 (beat 1) | 34 | 0.099 | 0.086 | below 0.0001 | 0.75 (below 0.0001) | 17 of 34 |
| Ends, bar phase 1 | 34 | 0.367 | 0.90 | 1.00 | 0.59 (below 0.0001) | 0 |
| Ends, bar phase 3 (post hoc) | 34 | 0.133 | 0.100 | below 0.0001 | 0.59 | 9 |
| Starts, bar phase 1, 3:28 to 4:37 only | 24 | 0.125 | 0.19 | below 0.0001 | 0.72 (below 0.0001) | 9 |
| Starts, beat, 3:28 to 4:37 only | 24 | 0.192 | 0.056 | 0.024 | 0.28 (0.15) | 12 of 24 |

Beat position (nearest beat, index counted modulo four; beat 1 = index 1): **starts** fall on beat 1 in 22 of 34 and on beat 4 (the beat before) in 10, with 1 each on beats 2 and 3 (chance 8.5 each; binomial P of 22 or more is 1.2e-6, 4.8e-6 allowing for four candidate beats); **ends** fall on beat 3 in 19, beat 2 in 11, beat 4 in 4, beat 1 in 0 (P of 19 or more on one beat 1.2e-4, 4.8e-4 allowing four candidates; the end result is post hoc). Median offset from the nearest beat line: starts +15 ms, ends -37 ms (inside the threshold-timing error). Fragment length (end minus start) is a median 1.07 s (2.1 beats); in beats the counts are 9 near one beat, 13 near two, 6 near three, 6 longer (one at 13.6 beats). Gaps between consecutive fragment starts: 18 of 33 are 3.5 to 4.6 beats (one bar) and 7 are 7.3 to 8.9 beats (two bars). The grid-shift p of 0.07 to 0.09 means the clustering is strongly present but its exact centre is not pinned to the kick phase more tightly than the roughly 0.1 s spread. The earlier work reported a 27-fragment Rayleigh at the 2.000 s period of R 0.69, p about 3e-6; this run (34 starts, R 0.75; 24 starts to 4:37, R 0.72) agrees. INFERRED: the fragments are placed, or gated, from beat 1 for about half a bar, on a beat-locked scheme; "voice on the bar" is supported here, only for the fragments.

## 4. Narrator pitch against the bass root

The bass stem is present for 8 of the 9 narration phrases (the exception is the title sentence at 1:24.5 to 1:28.6, which runs in the bass-less hole, bass about -72 dBFS). Bass pitch classes over the track by share: D 25 %, B 24 %, A 18 %, E 16 %, G 11 %. The pitch set is B Aeolian and an E-centred reading is open (see `music_reading.md`), so no single "key tonic" is assumed; the test is against the per-phrase bass root (most frequent pitch class of the bass stem's pyin track within the phrase).

| Test (8 phrases) | Result |
|---|---|
| Mean circular distance of narrator median pitch class from the bass root | 185 cents; a uniform-random narrator gives 299 (p 0.031) |
| Same, permuting the bass roots across phrases (keeps the narrator's pitch spread) | null mean 238 cents, p 0.10 |
| Narrator pitch within 1.5 semitones of the bass root | 5 of 8 (0:42 D#3 on E, -1; 0:51 and 1:53 C3 on B, +1; 1:49 D3 on D, 0; 2:32 D#3 on D, +1) |
| Narrator pitch class | D or D#, or C, in 8 of 8 (all medians 131 to 153 Hz) |

The uniform null is too easy, because the narrator hardly moves (131 to 153 Hz, one pitch region); the permutation null is the fair one, and at p 0.10 on 8 phrases the relation is **not supported**. All that can be said: the narrator's pitch region (C3 to D#3) contains D, which is the bass's most common pitch class, and the bass roots move among D, B, E, G and A underneath a voice that stays near one pitch (INFERRED from the two numbers; no tuned relationship is shown).

## 5. Provenance of the fragments (3:28 to 4:59)

Question: are the chopped fragments the same recording as the narration (0:42 to 2:36), repeated or reversed?

Method: waveform normalised cross-correlation (fine structure) on the stem band-passed 100 Hz to 3.5 kHz at 8,018 Hz, FFT-based, peak over all lags. The reference is the concatenation of the narration stem phrases. Q1 (fragment against narration): 29 fragments of at least 0.6 s (capped at 3 s), each correlated against 12 variants of the narration: forward and reversed at speed/pitch ratios 0.5, 1, 2, 2.67, 3 and 4. Statistic: the best score over the 12 variants. Null: 24 narration slices per length class (0.7, 1.5 and 3.0 s) against the same narration with their own location (plus or minus 1 s) removed, scored the same way (different words, same speaker, same recording). Q2 (fragment against fragment): a 0.6 s piece from 0.05 s into each fragment against every other fragment, forward and reversed query; 784 ordered pairs; null from 60 narration slices of 0.6 s against masked narration (mean 0.238, sd 0.055, maximum 0.374). Sensitivity (`sens.py`): an exact copy of a narration slice scores 1.00, a copy with noise at 0 dB signal-to-noise 0.71 and at -6 dB 0.45, but a copy sped up by only 2 percent scores 0.18 (null mean 0.16, maximum 0.30), by 5 or 10 percent 0.12.

Results:

- **No fragment matches the narration.** Best Q1 scores run 0.095 to 0.268 and none exceeds the null maximum for its length class (0.37, 0.30, 0.15); 0 of 29 have p of 0.05 or less (smallest p 0.08, for the fragments at 3:48.2, 4:08.5 and 4:16.3), where about 1.5 would be expected by chance. The best-matching variant is scattered across forward, reversed and several ratios, as chance would give. Reversed narration is not found either.
- **The fragments repeat each other.** Of 784 ordered pairs, forward-query correlation has median 0.109 and 90th percentile 0.233, with maximum 0.757; 45 pairs (5.7 %) exceed the null maximum of 0.374 (about 1.6 %, or 13 pairs, expected by chance), and 19 of the 29 fragments have a partner above 0.5. Top pairs: 4:40.6 (280.6 s) inside 3:54.2 at 0.76; 4:08.5 in 3:46.2 at 0.72; 3:36.4 in 3:56.1 at 0.70; 3:32.4 in 4:42.2 at 0.70; 3:40.6 in 4:02.4 at 0.69. Five clusters (fragment start times in seconds) have forward correlation above 0.5: [208.6, 234.2, 280.6]; [212.4, 216.4, 236.1, 256.3, 282.2]; [220.6, 224.6, 242.4, 244.6, 246.6, 264.2, 288.6]; [226.2, 248.5]; [230.0, 252.6]. Reversed-query pairs above the null maximum number 8, fewer than the roughly 13 chance expects, so reversal of repeats is not shown.
- **Same sentence, different takes.** As a reference for what "same words, different recording" scores, the three spoken copies of the title sentence (video1 0:27 and 2:44, video2 1:24) correlate at 0.07 to 0.14 (reversed 0.07 to 0.08), the level of unrelated speech.

Claims: the fragments are repeated material among themselves (OBSERVED, correlations up to 0.76, well above the null range); they are not a repeated or reversed copy of the narration recording within the tested family: forward or reversed, speed ratios 0.5, 1, 2, 2.67, 3, 4 (OBSERVED). They could still be the narrator's voice cut from other audio, a speech take sped or pitched by a rate not in the grid or processed beyond a noise level of about -6 dB, a vocal-like synth, or repeating leakage of other layers into the vocals stem (the stem is known to leak hats and the "other" layer, so a repeated non-voice sound would also correlate). The test cannot separate those (earlier notes' L-M undecided status stands). That the fragments are placed one per bar-half, starting on beat 1 (section 3), together with the exact repetition, fits a sampler pad or sequenced clip triggered on a grid (INFERRED); that it is archive speech is SPECULATED.

## Evidence table

| Finding | Value | Tag | Note |
|---|---|---|---|
| Typical narration pitch | median of phrase medians 147.5 Hz (D3), range 116 to 153 Hz, n = 9 | OBSERVED | pyin on a noisy stem; window sizes agree within 1.3 st |
| Pitch steadiness inside a phrase | median interquartile range 5.2 st; between-phrase sd 1.5 st | OBSERVED | speech inflection around one pitch region |
| Falling phrase ends | 5 of 9, median -0.7 st | OBSERVED, not significant | "falling" not established |
| Rate within phrases | 4.00 peaks/s mean (sd 0.57, range 3.40 to 5.10, n = 9) | OBSERVED | peaks are about syllables; sentence calibration gave 14 of a nominal 15 |
| Rate with gaps counted | 3.22 mean (2.72 to 3.80) | OBSERVED | |
| Old claim "4 to 5 a second" | replaced by the two rows above | OBSERVED | too high as a general figure for Part 2 |
| No trend in rate | rho +0.37, p 0.33, n = 9 | OBSERVED (low power) | |
| Narration on the beat or bar | pre-specified distance tests p 0.07 to 0.90; two end-R values at p_R 0.021 and 0.036 not claimed | OBSERVED | not claimed; grid unverified before 1:28.6 (flux R 0.20, other phase) |
| Fragment starts at a fixed place in the bar | 22 of 34 on one beat; R 0.75 at 2.000 s, p below 1e-4 | OBSERVED | agrees with earlier R 0.69 (27 starts) |
| That beat is the bar's beat 1 | all three section changes start about 0.2 s after the same beat index modulo four | INFERRED | rounded times from earlier work; sections lag the kick phase by about 0.2 s |
| Fragments end two beats later | 19 of 34 on the third beat; median length 1.07 s | OBSERVED (post hoc) | threshold timing error about 0.1 s |
| Fragment pitch | median 401 Hz (G4), 12 of 23 between 378 and 465 Hz, 4 at 800 Hz or more | OBSERVED, L | stem leakage possible |
| Narrator pitch against bass root | 5 of 8 within 1.5 st; permutation p 0.10 | OBSERVED | not supported |
| Fragments repeat each other | 45 of 784 pairs above null maximum; 19 of 29 with a partner over 0.5; top 0.76 | OBSERVED | stem content, may include leakage of a repeating sound |
| Fragments are copies of the narration | none of 29 (forward or reversed, ratios 0.5 to 4) | OBSERVED (negative) | blind to speed changes above about 2 percent off the grid and to heavy processing |
| Source of the fragments | undecided; consistent with a grid-triggered clip | INFERRED / SPECULATED | |

## Limits

- The vocals stem is a separation product that leaks drums and the "other" layer; pitch values of short or loud-section phrases are weak, and fragment pitches especially.
- Phrase edges come from an energy threshold, not linguistic boundaries; the beat-position counts depend on the grid phase (good to about 0.02 s) and on threshold timing (about 0.1 s).
- The grid before 1:28.6 is unverified, and the "beat 1" label rests on three rounded section times.
- Syllable peaks are an envelope proxy, calibrated on a single sentence taken as 15 syllables.
- The provenance test is a negative result inside a stated family of transforms; it does not prove the fragments come from elsewhere.
