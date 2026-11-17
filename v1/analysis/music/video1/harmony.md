# Video1 (Elfstedentocht Part 1): functional harmony

Written for task T6. Tags: **OBSERVED** (read straight off a file or stem), **HEARD(measured)** (a number measured from the audio stems by an algorithm; no listening), **INFERRED** (my reading of those numbers). No claim comes from listening. `music_reading.md` is untouched; differences from it are listed under "Disagreements".

## Summary (plain language)

- The bass is a D drone with short pickup notes, not a walking bass. Wherever it plays (about 0:07 to 1:15, 1:40 to 1:55 and from 2:38 to the end) its strongest pitch class is D in 31 of 36 bars, with C in the other five. Per bar the D share is only 0.45 to 0.9, which fits a distorted, riff-like bass and not a clean sustained note.
- The bass is silent for 1:15 to 1:40 and 1:55 to 2:38, apart from six very low thumps from about 2:01 to 2:32. No bass root is claimed for those stretches. The "A, D, G walk" at 2:13 to 2:36 is therefore a pad (other stem) and chord-label finding only.
- The pad's strongest class is D in every bar where the bass plays. From 2:13.28 to 2:36.4 it is mostly A (22 of 31 beats) with brief G, D, C and B.
- The tonic is D (not in doubt). Whether it is major or minor is **ambiguous**: whole-song D major 0.76 against D minor 0.756.
- The chord turn is at 2:37.15 to 2:40.2 (F, C, D, C), not 2:38 to 2:48; after 2:40.98 the pad is on D again.
- Cannot be known from stems: instrument identity and voicings (list at the bottom).

## Method and grid

- Bass roots: `pyin` (30 to 250 Hz) on `stems/bass.mp3`, one RMS- and voicing-weighted pitch-class histogram per bar and per quarter-bar; octave ignored; confidence = share of the weight on the top class. Bars more than 40 dB below the bass maximum have no root. Bars containing the sub thumps (about 42.6 Hz, from `music_reading.md`) are flagged `root_claim: false` even though pyin reads F or F#.
- Pad: `chroma_cqt` of `stems/other.mp3`, per bar and (for 2:10 to 2:48) per tracker beat, scaled to a maximum of 1.0.
- Bar grid: `audio_features/beat_times.json` (78.3 BPM tracker, beats 0.77 s), bar = 4 beats from the first beat at 0.952 s. Which beat is "one" is not confirmed (tracker-derived), and 78 versus 156 BPM is open in `music_reading.md`. The beat file ends at 167.97; later bars (bars 56 to 60, flagged `extrapolated_grid`) are extrapolated [L].
- Chord labels quoted below are from `music_views/chords.json` (a detector on the whole mix, not the stems).
- Data: `v1/data/video1/music_views/bass_roots.json` (60 bars, plus `events` and `loops`). Helper scripts (scratchpad, may be cleared; regenerate from the method): `/tmp/claude-0/-home-user-Listener/cb832643-599e-5a16-8ae7-147fc9b20f96/scratchpad/bass_roots.py`, `post.py`, `probe.py`.
- Resolution: a pyin window is 0.25 to 0.5 s; edges are good to about 0.25 s.

## Loop and section structure with times

| Span (s, JSON bar starts or probe) | Bass | Pad's strongest class | What | Tag |
|---|---|---|---|---|
| 0.95 to ~6.2 | none (-52 dB bar at 0.95, -43 dB at 4.04) | D | Bass absent. No root claim. | HEARD(measured) |
| ~6.25 to 74.8 | faint G at 6.25 to 7.25, then C at 7.75; D from bar 4 (10.2) | D in all 22 bars | Bass on, 22 bars (7.1 to 74.8): D top in 19, C top in 3 (bars at 7.13, 13.28, 44.05); 11 of 22 bars weak (< 0.6). Pickup notes in the last quarter-bar are C, G, F, E, B or C#. | HEARD(measured) |
| 74.8 to 99.5 | none: bass leaves at about 75.3, floor from 75.5, returns at 99.75 (-22 dB, -9 dB at 100.0) | D mostly (bars 25 to 28 start A, C, B, D) | Bass-less float. No root claim. The pad's strongest class is not D in bars 25 to 27 (74.8 to 84.0: A, C, B). | HEARD(measured) |
| 99.45 to 114.8 | D (4 bars), C (bar at 111.7, weak) | D in all 5 | Bass back, 5 bars. | HEARD(measured) |
| ~115 to 121.0 | none: fades from 114.75, floor from 115.75 | D | Bass drops out about 1:55, five seconds before the thumps. No root claim. | HEARD(measured) |
| 121.0 to 157.9 | six sub thumps (bars at 121.0, 127.1, 133.3, 139.4, 145.6, 151.7), nothing between | D to 133.3, then A | pyin reads F or F# for the thumps (42.6 Hz, between E1 and F1 per `music_reading.md`): **no root claim**. | HEARD(measured) |
| ~158.25 to 188.7 | D (8 of 9 bars; C top at 157.9, weak) | D in all 9 | Bass back (-39 dB at 158.25, music_reading gives 2:38.4); D drone with C or G or B pickups. Bars from 170.3 onward are on an extrapolated grid [L]. | HEARD(measured) |

## The pad walk, 2:10 to 2:41 (pad stem and chord labels)

Per tracker beat, strongest pad class (second class in brackets), with the mix chord label:

| Beat time | Pad | Chord label | Beat time | Pad | Chord label |
|---|---|---|---|---|---|
| 2:10.22 to 2:11.75 | D (A) | D | 2:30.21 | D (C) | Am |
| 2:12.52 | D (C) | N | 2:30.98 | C (B) | C |
| 2:13.28 to 2:14.81 | A (D) | Dm | 2:31.74 | B (D) | Dm |
| 2:15.60 | A (E) | Am | 2:32.53 to 2:33.30 | A (D) | Dm |
| 2:16.37 to 2:17.14 | A (D, G) | D | 2:34.06 | A (B) | Am |
| 2:17.90 | D (G) | G | 2:34.83 | A (G) | D |
| 2:18.67 | A (G) | D | 2:35.60 | G (A) | G |
| 2:19.44 to 2:20.99 | A (D) | Dm | 2:36.36 | A (G) | Dm |
| 2:21.76 | A (E) | Am | 2:37.15 | F (G) | F |
| 2:22.52 | A (D) | D | 2:37.92 | C (G) | C |
| 2:23.29 to 2:24.82 | G (A) | G, D, G | 2:38.69 to 2:39.45 | D (C) | D, N |
| 2:25.59 to 2:27.15 | A (D) | Dm | 2:40.19 | C (F) | C |
| 2:27.91 | A (B) | Em | 2:40.98 to 2:47.14 | D | Dm, D, N, Bm (labels vary) |
| 2:28.68 | A (D) | D | | | |
| 2:29.44 | D (G) | Gm | | | |

Between 2:13.28 and 2:36.4 (31 beats) the pad's top class is A on 22, G on 4, D on 3, C on 1 and B on 1 [HEARD(measured)]. A is not chord-labelled "A" for most of this: the mix detector says Dm, D, Am, G, Em, Gm, Am, C and so on, which is the A in the pad plus a D and G in the rest of the mix. Reading it as an A-centred pedal with D and G coloured excursions is INFERRED.

## Roman numerals under both candidate tonics

Both columns use the same pitches; only the labels change.

| Material | Where | D as tonic | A as tonic (only for the pad walk) | Tag |
|---|---|---|---|---|
| Bass root D | 7.1 to 74.8, 99.4 to 114.8, 157.9 to 188.7 | I | IV | INFERRED |
| Bass root C (3 + 1 + 1 bars) | 7.13, 13.28, 44.05, 111.7, 157.9 | bVII | bIII | INFERRED |
| Pickups G, F, B, E (quarter-bar) | within those bars | IV, bIII, VI, II | bVII, bII, II, V | INFERRED |
| Pad A | 2:13.28 to 2:36.4, mostly | V | i or I | INFERRED |
| Pad D | 2:17.90, 2:29.44 | I | IV | INFERRED |
| Pad G | 2:23.29 to 2:24.82, 2:35.60 | IV | bVII | INFERRED |
| Pad C, B | 2:30.98, 2:31.74 | bVII, VI | bIII, II | INFERRED |
| Pad F then C then D | 2:37.15, 2:37.92, 2:38.69 | bIII, bVII, I | bII, bIII, IV | INFERRED |

D as tonic with the labelled walk: V (A pedal) with I, IV and bVII visits, then bIII - bVII - I at 2:37 to 2:39: modal (no V to I cadence of a leading-tone type; no C# is claimed). Under A as tonic the walk is i/I with IV and bVII, which is Mixolydian or Aeolian colour on A and leaves D unresolved. The data cannot rank the two readings; the bass (D whenever present) and the whole-song key point to D.

## Key and mode: ambiguity flags

| Measurement | Top two | Gap | Verdict | Tag |
|---|---|---|---|---|
| Whole song (`audio_features/summary.json`) | D major 0.76, D minor 0.756 | 0.004 | **ambiguous** (mode) | OBSERVED |
| 30 s windows from 0, 30, 60, 89.9, 119.9, 149.9, 179.9 | D major 0.693 / 0.619; D minor 0.701 / 0.633; D major 0.726 / 0.579; D major 0.748 / 0.725; A minor 0.598 / F major 0.471; D minor 0.692 / 0.631; D minor 0.645 / 0.594 | 0.074, 0.068, 0.147, 0.023, 0.127, 0.061, 0.051 | ambiguous only in the 89.9 window; the 119.9 window (A minor first) is the pad walk | OBSERVED |
| Bass-root bar counts, 7.1 to 74.8 | D minor 0.670, D major 0.641 | 0.029 | **ambiguous** (crude: two classes only) | HEARD(measured) |
| Pad chroma, bass-on bars 7.1 to 74.8 | D major 0.772, D minor 0.722 | 0.050 | **ambiguous** (at the 0.05 line) | HEARD(measured) |
| Pad chroma, 99.4 to 114.8 | D minor 0.760, D major 0.718 | 0.042 | **ambiguous** | HEARD(measured) |
| Pad chroma, 157.9 to 188.7 | D major 0.596, D minor 0.579 | 0.017 | **ambiguous** | HEARD(measured) |

The tonic D is not ambiguous: the next non-D candidate (G major) is at least 0.18 behind in every row. The third (F or F#) is the open question, as `music_reading.md` says; the bass has F only as a sub-thump reading and as a pickup, which is not evidence for a minor third.

## Pad chroma against bass roots

Where the bass plays (36 bars with a root claim) the pad's strongest class is D in all 36; it equals the bass root in 31 (22: 19, 5: 4, 9: 8 by span); the five mismatches are exactly the five bars where the bass reads C [HEARD(measured)]. Mean pad chroma at the bass root: 0.94 (7.1 to 74.8), 0.91 (99.4 to 114.8), 1.0 (157.9 to 188.7). So pad and bass agree on D wherever both exist; they disagree only on the pickup notes. In the bass-less stretches the pad carries the harmony alone (the A walk above); at 74.8 to 84.0 the pad leaves D for A, C and B (bar chroma, A 1.0 with G# 0.36 at 74.8; C 1.0 at 77.9; B 1.0 at 81.0) [HEARD(measured)], which is the one stretch where the drone is absent from the pad too.

## Harmonic events

- **~75.3**: bass leaves; the pad's top class then moves off D (74.8 to 84.0). HEARD(measured).
- **99.75**: bass returns on D. HEARD(measured).
- **~115 to 121.0**: bass leaves again; then the six thumps. HEARD(measured).
- **133.28**: the pad's top class passes from D to A, in the bar that contains the third thump (2:13.4 per `music_reading.md`). HEARD(measured); no causal claim.
- **157.15 to 160.19**: F, C, D, (N), C in the pad and chord labels, with the bass back at about 158.25. HEARD(measured).
- **160.98**: pad back on D, and D stays on top through 2:47.14 in the beat table. HEARD(measured).

## Disagreements and refinements against earlier claims

1. Hypothesis "A-D-G walk from about 2:13": **partly confirmed**: the pad turns to A at 2:13.28. It is more an A pedal (22 of 31 beats) with D, G, C, B excursions than a three-note walk, and only the pad and chord labels show it (no bass).
2. `music_reading.md`: "A is strongest in `other` from 2:00". Bar chroma does not support that: the bars at 117.9 to 130.2 have D on top, with A second (0.79 to 0.98); the bar at 114.8 has D top and D# second (0.55). A passes D at 133.28.
3. Hypothesis "2:38 to 2:48 chord turn": the turn measured is **2:37.15 to 2:40.2** (F, C, D, C); from 2:40.98 the pad is D to at least 2:47.14. `music_reading.md`'s chord-label span 2:34.8 to 2:39.5 (D, G, Dm, F, C, D) agrees with this beat table.
4. Bass-less stretch: `music_reading.md` has the bass out 1:15.3 to 1:40.0. Measured 75.3 to 99.75, same. New detail: bass also drops at about 1:55 (114.75 to 115.75), before the thumps at 2:01, not at 2:00.
5. "D drone": confirmed for the bass (D top in 31 of 36 bars), with a weak per-bar share; C is the only other bass top class.

## Cannot be known from stems

- Instrument identity (guitar, bass guitar, synth; whether the bass is played or sequenced).
- Voicings and which notes are doubled; chroma shows pitch classes only, and a distorted wall can mask a third.
- Whether a listener hears D major or D minor, or hears the 2:13 to 2:36 passage as centred on A or on D.
- Bass roots in the silent stretches and at the sub thumps (pitch not a usable root).
- Beat one: the bar grid is tracker-derived; 78 versus 156 BPM is open.
- Octave of the bass roots (ignored).
