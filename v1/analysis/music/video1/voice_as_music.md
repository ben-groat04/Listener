# Video1: the narrator as a musical voice (Elfstedentocht Part 1)

Measured from the vocals stem (`v1/data/video1/stems/vocals.mp3`) with scratchpad scripts in `/tmp/claude-0/-home-user-Listener/cb832643-599e-5a16-8ae7-147fc9b20f96/scratchpad/t7/` (`measure.py` helpers, `run_main.py` pitch/rate/bass table, `analyse.py` alignment, rate and bass tests, `tables2.py` the phrase table; logs `analyse.out` and `main.log`). Scratchpad files can be cleared, so the methods are written out below. Tags: OBSERVED (measured, with the stated error), INFERRED (follows from measurement plus a stated assumption), SPECULATED (idea only).

Whisper is a hint for where speech sits, nothing more. "MUZIEK" and "Bedankt voor het kijken" (3:07 to 3:08) are hallucinations and non-events: the vocals stem has no phrase at 3:07 (its last phrase ends at 2:48.2). Words below are ASR hints, not transcription. Narrator identity, sex, intent and emotion are not claimed.

## In plain words

Treated as an instrument, the narrator is a **low, dry, unsung voice**. Over the main narration the pitch tracker puts its typical pitch at about 130 to 180 Hz (C3 to G3); the median of the phrase medians is 175 Hz (F3), 21 phrases. The town-list passage (2:15 to 2:25) sits higher, at about 200 to 250 Hz (G3 to B3). For scale, D3 is 147 Hz, so the voice lives around the low D of the guitar region and two to three octaves above the sub-bass.

It is **not steady in pitch**. Within one phrase the middle half of the pitch values spans a median 4.2 semitones, so this is speech inflection, not a held note. It does not settle on the bass note or the key in any way the data can show (section 4).

It is **moderately steady in speed**: 4.4 envelope peaks a second inside a phrase (a peak is roughly one syllable), spread 0.8 between phrases, with no detectable drift through the piece. Counting the gaps in and around phrases the rate is lower, 3.6 a second, and the town list is slower still.

Against the beat it is **free**. Phrase starts and ends are no closer to the 78 BPM beat, to the 156 BPM subdivision or to the four-beat bar than chance would put them (all permutation p-values above 0.09, most above 0.2). The voice talks over the groove; it is not cut to it.

**The earlier claim "four or five syllables a second" is replaced** by the measured figures in section 2: 4.4 peaks a second within phrases (range 2.9 to 5.7, 16 phrases), 3.6 once gaps are counted, 2.9 to 4.1 in the town list. "Four to five" survives only as the upper part of the range (0:51 to 0:56 and 1:19 to 1:25).

## 1. Pitch

Method: pyin (librosa 1.0.1) on the stem band-limited to 70 Hz to 1.6 kHz, search range 70 to 400 Hz, 10 ms hop, a lenient voicing prior (a stricter setting found almost no voiced frames in this noisy stem), run at 2048 and 4096 sample windows. A phrase is a run of stem energy within 30 dB of the stem's 99th-percentile level, gaps under 0.35 s merged, longer than 0.25 s. f0 is reported only where at least 30 voiced frames exist. Error: the two window sizes agree to a median 0.45 semitone but differ by up to 7 semitones on some phrases (octave jumps). The first-quarter to last-quarter medians are shown but are not trusted as contours.

The table shows narration phrases (those that overlap a trusted ASR segment). Three further stem runs have no ASR text (1:03.6, 1:46.6, 1:57.0) and are not used.

| Span | ASR hint (mix, Whisper medium) | Voiced frames | f0 median Hz (note) | f0 IQR (st) | f0 first to last quarter (Hz) | Envelope peaks | Rate within run (peaks/s) |
|---|---|---|---|---|---|---|---|
| 0:09.9 to 0:12.2 | 18 januari 1963 | 202 | 150 (D3) | 3.0 | 159 to 150 | 10 | 4.39 |
| 0:13.6 to 0:15.7 | Het staatsmarathon zonder lieveren | 153 | 131 (C3) | 4.2 | 161 to 135 | 9 | 3.94 |
| 0:17.0 to 0:18.3 | half zes in de ochtend | 71 | 178 (F3) | 7.5 | 173 to 258 | 4 | - |
| 0:19.0 to 0:24.0 | Tweehonderd bezoekers door een Fri... | 328 | 153 (D#3) | 5.0 | 171 to 151 | 22 | 4.70 |
| 0:24.5 to 0:26.7 | Stad zijn voor de twaalfde elfste... | 98 | 198 (G3) | 9.1 | 189 to 307 | 8 | 3.93 |
| 0:27.9 to 0:31.7 | Waar iedereen zich voor op maakt,... | 164 | 176 (F3) | 15.8 | 318 to 123 | 15 | 4.13 |
| 0:41.1 to 0:42.4 | De 12e Elfstedentuin. | 56 | 175 (F3) | 6.4 | 203 to 122 | 6 | 4.24 |
| 0:50.9 to 0:53.1 | Temperatuur 16 graden beneden 0. | 180 | 176 (F3) | 5.9 | 145 to 126 | 12 | 5.47 |
| 0:54.0 to 0:56.1 | Een monsteret van ruim 200 kilomet... | 147 | 158 (D#3) | 4.2 | 199 to 140 | 11 | 4.98 |
| 1:18.9 to 1:21.0 | 575 wedstrijdrijders, rond 9500 to... | 166 | 156 (D#3) | 2.0 | 160 to 98 | 10 | 5.52 |
| 1:21.7 to 1:23.6 | (same ASR segment) | 132 | 172 (F3) | 2.7 | 163 to 231 | 9 | 5.67 |
| 1:24.3 to 1:27.0 | (same ASR segment) | 191 | 142 (C#3) | 2.2 | 120 to 141 | 13 | 4.94 |
| 2:15.0 to 2:17.1 | Sleek, eerst, slotten, staveren... | 178 | 246 (B3) | 1.8 | 227 to 248 | 5 | 2.90 |
| 2:18.2 to 2:20.0 | (same, town list) | 110 | 198 (G3) | 4.0 | 197 to 247 | 1 | - |
| 2:21.2 to 2:22.9 | (same, town list) | 141 | 247 (B3) | 1.4 | 230 to 249 | 3 | - |
| 2:24.1 to 2:26.5 | (same, town list) | 198 | 196 (G3) | 0.9 | 196 to 195 | 7 | 3.35 |
| 2:27.4 to 2:27.8 | Markum. | 15 | not reliable | - | - | 1 | - |
| 2:28.9 to 2:30.0 | Loftwacht. | 39 | 241 (B3) | 4.5 | 247 to 188 | 2 | - |
| 2:30.5 to 2:31.0 | Hartingen. | 14 | not reliable | - | - | 1 | - |
| 2:31.4 to 2:32.8 | Vranenken. | 88 | 152 (D#3) | 10.5 | 138 to 135 | 5 | 4.12 |
| 2:35.1 to 2:35.9 | Leeuwarden. | 50 | 119 (A#2) | 11.7 | 241 to 104 | 2 | - |
| 2:44.3 to 2:46.0 | Waar iedereen zich voor opmaakt,... | 92 | 166 (E3) | 3.8 | 148 to 142 | 7 | 5.08 |
| 2:46.5 to 2:48.2 | (same sentence, second half) | 72 | 222 (A3) | 16.2 | 149 to 380 | 5 | 3.48 |

Summary (phrases with at least 30 voiced frames, n = 21): median of phrase medians 174.9 Hz (F3), range 118.8 to 246.6 Hz; before 2:15 (n = 12) median 165.0 Hz (E3), range 130.6 to 198.0; from 2:15 (town list and close, n = 9) median 198.0 Hz (G3). Median per-phrase interquartile range 4.2 semitones; between-phrase standard deviation of medians 3.4 semitones. Phrase-end minus phrase-start median is -0.8 semitone and falls in 13 of 21 phrases (sign test p about 0.38 two-sided): a falling tendency is **not established** (this tempers the earlier "falling" wording, which rested on a polyphonic-stem pitch track).

## 2. Syllable rate (replaces "four or five syllables a second")

Method: the stem is band-passed 300 Hz to 3 kHz, its short-time level (25 ms window, 10 ms hop, 50 ms smoothing) is peak-picked with at least 3 dB prominence, at least 80 ms apart, within 20 dB of the phrase maximum, over the phrase padded by 0.15 s each side. No voicing gate (a voiced-only gate dropped real syllables in this stem). A peak is read as roughly one syllable nucleus. Rate within a run is (peaks minus one) divided by the time between first and last peak; "including edges" is peaks divided by (run length plus 0.3 s).

Calibration on a repeating sentence, "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht" (spoken three times across the two videos; nominal 15 syllables if fully pronounced: waar, ie-de-reen, zich, voor, op-maakt, dat, is, de, elf-ste-den-tocht). Detected peaks: 15 at 0:27 to 0:31.7 of this video, 14 at 2:44 to 2:48 here, and 14 in video2. Count error therefore 0 to -1 of 15 (about -7 % at worst, mean -4 %), assuming the nominal count is right; the nominal count is my own syllabification and not verified against the audio. Whisper words per second is a weaker cross-check (the sentence is 9 to 10 ASR words over about 3.8 s, 2.6 words a second; Dutch words average 1.5 or more syllables, so this fits 4 syllables a second but cannot refine it).

| Measure (16 phrases of at least 1.0 s with at least 5 peaks) | Value |
|---|---|
| Rate within runs, mean / median | 4.43 / 4.31 peaks per s |
| Spread between phrases (sd; CV) | 0.79 (CV 0.18) |
| Range | 2.90 (town list, 2:15) to 5.67 (1:21.7) |
| Rate including run edges, mean / median / range | 3.59 / 3.67 / 2.08 to 4.76 |
| Peak-to-peak interval, pooled median / mean / CV | 0.190 s / 0.224 s / 0.52 |
| Rate against phrase start time | Spearman rho -0.10, p 0.72 (no trend; low power) |
| Town list, 2:15 to 2:33 (3 phrases with enough peaks) | 2.90, 3.35, 4.12 within runs |
| Calibration sentence rate (first to last peak) | 4.13, 3.60 (2:44, padded window) |

Reading: the old figure "steady 4 to 5 peaks a second" was an upper-band, within-phrase number. The measured mean is 4.4 within phrases and 3.6 over speech including its pauses, so "about four syllables a second, slower in the list" is the supported wording. Within-phrase spacing is uneven (interval CV 0.24 to 0.71 per phrase), as ordinary speech is. The median interval of 0.19 s happens to match the drum-slot period of 0.1923 s found by the rhythm specialist, but the interval spread is wide and the alignment tests below show no phase locking, so this is a coincidence of one number (SPECULATED that it means anything).

## 3. Phrase against the bar grid

Grid: the beat tracker's own beat times (`audio_features/beat_times.json`, 78.3 BPM, beat 0.769 s, ends at 167.97 s), so only events before the last beat are tested. The quarter-note octave is open (78 versus 156 BPM; see `music_reading.md` section 5), so both are tested: the beat lines (period 0.769 s) and the beat lines plus midpoints (period 0.385 s, the 156 BPM quarter). Bar-one identity is tracker-derived and unverified, so a four-beat bar is tested at all four possible phases. Statistic: mean distance of each event to the nearest grid line as a fraction of the period (chance 0.25). Two nulls: (a) the whole grid slid to 500 evenly spaced phases (p = share of phases doing at least as well); (b) events redrawn uniformly over the same time span, 20,000 draws, seed fixed. R is the mean resultant length at the grid period and p_R its Monte Carlo p (20,000 draws). Event times come from the stem-energy threshold, which can start up to about 0.1 s late and end up to about 0.1 s early, so offsets under 0.1 s are not interpretable.

| Event, grid | n | mean distance / period | p (grid-shift null) | p (uniform null) | R (p_R) | Within 0.1 s of a line |
|---|---|---|---|---|---|---|
| Starts, beat 78 BPM | 23 | 0.278 | 0.65 | 0.82 | 0.32 (0.089) | 5 |
| Ends, beat 78 BPM | 22 | 0.255 | 0.50 | 0.56 | 0.13 (0.68) | 7 |
| Starts, 156 BPM quarter (half-beat lines) | 23 | 0.225 | 0.37 | 0.21 | 0.26 (0.20) | 15 |
| Ends, 156 BPM quarter | 22 | 0.216 | 0.096 | 0.14 | 0.14 (0.67) | 12 |
| Starts, 4-beat bar, phase 0 / 1 / 2 / 3 | 21 to 22 | 0.242 / 0.234 / 0.257 / 0.263 | 0.27 / 0.19 / 0.73 / 0.94 | 0.41 / 0.31 / 0.59 / 0.65 | 0.06 to 0.10 (0.80 to 0.93) | 1 to 2 |
| Ends, 4-beat bar, phase 0 / 1 / 2 / 3 | 21 | 0.244 / 0.249 / 0.258 / 0.253 | 0.12 / 0.45 / 0.92 / 0.58 | 0.43 / 0.49 / 0.60 / 0.53 | 0.04 (0.97) | 1 to 2 |

Result: nothing reaches p of 0.05, and with 20 tests one would expect about one by chance. The smallest are 0.096 (ends against the 156 BPM subdivision, grid-shift null) and 0.089 (start clustering at the 78 BPM beat period, p_R); neither is claimed. **"Voice on the bar" is not supported for this video**; the voice is free-timed against both candidate tempi. At 156 BPM the 0.1 s window covers 52 % of the period, so the 15 of 23 starts within it is exactly what chance gives. Statistical power is modest (n of 21 to 23); a lock as strong as video2's fragment starts would have been detected, a weak lock would not.

## 4. Narrator pitch against the bass root

The bass stem is present (level above -40 dBFS, bass pitch found for at least 20 % of frames) for only 11 of the narration phrases with a reliable f0 (0:10 to 0:56, 2:44 to 2:48); it is absent or faint for 1:15 to 1:40 (the lift), where the narration at 1:19 to 1:27 therefore has no bass partner, and mostly at the town list. The per-phrase bass root is the most frequent pitch class of the bass stem's pyin track within the phrase (30 to 250 Hz); its overall bass pitch-class shares are D 48 %, C 16 %, F 16 %, G 6 %, C# 5 %.

| Test (11 phrases) | Result |
|---|---|
| Mean circular distance of narrator median pitch class from the phrase's bass root | 284 cents; a uniform-random narrator gives 299 (p 0.38) |
| Same, permuting the bass roots across phrases (keeps the narrator's pitch spread) | null mean 275 cents, p 1.0 |
| Narrator pitch class equal to the bass root (within about a semitone) | 3 of 11 (9.9 s D3 on D; 19.0 s and 54.0 s D#3 on D) |
| Most common intervals above the bass root | 3 semitones (F on D) in 3 phrases (0:27.9, 0:41.1, 0:50.9), 1 semitone in 2, 5 semitones in 2 |

**Nothing supports a tuned relationship** between the narrator's median pitch and the bass root or key. The narrator's median pitch sits in the D3 to F3 band, which is 0 to 3 semitones above the D3 tonic frequency; D3 itself is the bass's most common pitch class, so the band overlaps the tonic region by position, not by any measured tuning. Speech inflection moves through about 4 semitones per phrase, and the tracker cannot separate D from D# reliably (the two window sizes differ by up to a semitone on some phrases).

## Evidence table

| Finding | Value | Tag | Note |
|---|---|---|---|
| Typical narration pitch | median of phrase medians 175 Hz (F3), main narration 130 to 180 Hz, n = 21 | OBSERVED | pyin on a noisy stem; octave jumps possible (window sizes differ up to 7 st on some phrases) |
| Town-list pitch | 196 to 247 Hz (G3 to B3) in 5 of 6 reliable phrases | OBSERVED | higher than the narrative lines by about 3 semitones in the median (165 to 198 Hz) |
| Pitch steadiness inside a phrase | median interquartile range 4.2 st | OBSERVED | speech inflection; a sung or held pitch would be under 1 st |
| Falling phrase ends | 13 of 21, median -0.8 st | OBSERVED, not significant | "falling" not established |
| Rate within phrases | 4.43 peaks/s mean (sd 0.79, range 2.90 to 5.67, n = 16) | OBSERVED | peaks are about syllables; calibrated on a 15-syllable sentence: 15, 14 and 14 peaks found |
| Rate with gaps counted | 3.59 mean (2.08 to 4.76) | OBSERVED | |
| Old claim "4 to 5 a second, steady" | replaced by the two rows above | OBSERVED | holds only for fast phrases (0:51 to 0:56, 1:19 to 1:25) |
| No quickening through the piece | rho -0.10, p 0.72, n = 16 | OBSERVED (low power) | agrees with the earlier "no quickening" but is a weak test |
| Voice on the beat or bar | no test below p 0.089 (20 tests) | OBSERVED | not claimed; free timing |
| Voice against bass root or key | 3 of 11 phrases on the root; permutation p 0.38 and 1.0 | OBSERVED | no tuned relationship shown |
| 156 versus 78 BPM from the voice | no support for either | OBSERVED | the voice cannot settle the octave |
| Voice as rhythm instrument | the voice carries phrase-scale pacing (0.2 to 0.5 s syllables, 1 to 5 s phrases) over a fixed pulse | INFERRED | from free timing against a steady grid |
| Why the free voice matters musically | the contrast of a free voice over a steady machine is the piece's human/machine layer | SPECULATED | interpretation only |

## Limits

- The vocals stem is a separation product: it leaks drums and the guitar wall (the stem is noisy at the loud sections), so pitch values of short phrases are weak and several phrases are not reportable.
- Phrase edges come from an energy threshold, not from linguistic boundaries; each phrase may contain one or two ASR segments.
- Syllable peaks are an envelope proxy; the calibration is a single sentence taken as 15 syllables.
- The bar grid is tracker-derived (78.3 BPM); the beat file ends at 167.97 s, so the final 0.2 s is untested.
