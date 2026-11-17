# Elfstedentocht Parts 1 and 2: the music compared (round 1, music colleague)

British English. Timestamps are `<video> m:ss`. Tags: H/M/L confidence as in the music readings. "Measured" means I re-checked it in `v1/data/`; "reported" means taken from the analysis files. Speculation is marked **[speculation]**.

Sources read in order: `analysis/music/video{1,2}/music_reading.md`, then `interpretation.md`, then `dossier.md`; checked against `per_second_levels.json`, `summary.json`, the Whisper transcripts, the stems and `analysis/research/part_mapping.md`.

## 0. The mapping (verified)

- ffprobe: video1 188.66 s, video2 305.95 s. Official lengths (MusicBrainz, via `part_mapping.md`) 3:09 and 5:04. The ordering video1 = Part 1, video2 = Part 2 holds; the only alternative fails by 115 s. The 1.9 s excess on video2 is the file's silent/black tail (measured: `per_second_levels` is -57 dBFS at video2 5:03, digital zero from about 5:04.2).
- The audio itself agrees with the press description (Part 1 "loud, rock"; Part 2 "calmer, electronic"), but only half of that holds. Part 1 is loud and flat (mean -12.5 dBFS, 10th to 90th percentile -15.0 to -10.9). Part 2 starts far quieter (first third mean -19.9 dBFS) and then reaches the same level as Part 1 or higher (peak per-second -9.3 against -9.5). "Calmer" is true of its surface and first 90 s, not of its second half (reported by the Part 2 reading; I confirm the numbers).
- I could not verify that our file is the PSBHQ upload; the mapping rests on lengths.

## 1. Side by side (the facts)

| | Part 1 (video1) | Part 2 (video2) |
|---|---|---|
| Length | 3:08.7 | 5:06 file (5:04 official) |
| Pitch centre | D pedal throughout, D5 power-chord world, third missing; mode undecided (key tracker: D major 0.76 against D minor 0.756) [H on D, L on mode] | One seven-note set, B C# D E F# G A, no modulation. B minor (pad, tracker 0.88) or E Dorian (bass in loop A) [M-L on centre] |
| Tempo | 78.0 to 78.3 BPM beat (octave 78 or 156 unsettled, 55/45 for 78) | 120 BPM, bar 2.000 s, kick period 0.49995 s, from 1:28.6 to 5:00; the tracker's 161.5 follows the bass's three-sixteenth figure |
| Harmonic motion | Almost none; pitch moves only at 1:15 to 1:40 (stepwise line A, C, B, G, D, over no bass) and 2:00 to 2:40 (A, D, G walk; F, C, D, C run-up) | Bass root loops: loop A (E G D E G D B, 28 s cycle) to 2:36.8, loop B (B A D, 12 s) to 4:48.8. Pad is a B pedal throughout. No cadence, no leading tone |
| Source of drama | Bass, "wall" and voice switched on and off on a bar grid; drums never change gear | One upper layer brightened over about 3:00 to 4:24 (about 24 to 28 dB more at 4 to 8 kHz), voice turned into bar-locked fragments, then subtraction |
| Loudness | Flat. -9.5 to -16.5 dBFS. K-weighted peaks at 1:07 and 2:48 to 3:08 | A rising staircase, about 15 dB: -25.5 intro, -18 at 0:28, -14.7 at 1:28.6, about -12 to 3:20, -9.9 at 4:24 |
| Drums | Dry, tight, present from 0:01 to the end (zero seconds below -50 dB); hat/kick interlock; no fills | Absent for 28 s; sparse until 1:24; hole; four-on-the-floor plus extra kick; flat -18/-19 dBFS; a few fills |
| Voice | 36% of seconds above -45 dB; sentence-level narration, last at 2:44.4 to 2:48.2 | 38% of seconds above -45 dB; narration 0:41.7 to 2:36.1, then fragments to about 4:59 |
| Texture | Rock band feel (guitar-like wall unproven; CLAP weak); bass present about 72% of seconds | Pad, bass, machine-like kit (instruments unrecoverable); bass present about 87% of seconds |
| Ending | 0.4 s taper to silence at 3:08.4, no cadence | Hard cut at 5:00.8, pad ring-out, a two-drum, three-bass tag at 5:02.34 to 5:02.9, digital zero from 5:04.24 |

Seconds-above-threshold figures are my own count from `per_second_levels.json` (bass below -50 dB: 52 s of 188 in video1, 40 s of 305 in video2; video2's silent drums, 37 s, are the 28 s intro plus the hole).

## 2. What is shared (the diptych is one design)

1. **The same sentence, held back and then used as a hinge.** "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht" appears in both parts and in both is the line that comes straight before a violent change of state.
   - Part 1: 0:27 to 0:31.7, exit on a bar line, after which the band opens up (width 0.35 to 0.55, drums brighten); and again 2:44 to 2:48.2, ending inside the 0.4 s hole at 2:47.8 before the loudest stretch.
   - Part 2: 1:24.0 to 1:28.5, ending into the 3.6 s (bass) / 4.3 s (drums) hole; the full groove lands about 0.3 s after the last word at 1:28.6 (`per_second_levels`: drums -75.1 dB at 1:27, -21.2 at 1:28; reported 50 dB return).
   Part 1 uses the hole as a half-second catch; Part 2 uses it as a four-second void. Same device, scaled to the form. [H on the facts; the "hinge" reading is interpretation, M]
2. **Narration content and order.** The Whisper passes recover, in both parts, the date (V1 0:10 to 0:31; V2 0:41.7), the twelfth Elfstedentocht (V1 0:41; V2 1:19.7), 16 degrees below (V1 0:51 to 0:56; V2 1:49.4), the 200 km "monster ride" (V1 0:51 to 0:56; V2 1:52.5), and "575 ... 9500 toerrijders" (V1 1:19 to 1:27; V2 2:25.8 to 2:36.1). So both parts draw on the same spoken script, with the town list (V1 2:16 to 2:36) the one block that Part 2 does not reproduce in Whisper. The order differs (V1 puts the title sentence before "twelfth"; V2 after). Same recording or a re-cut: **my test was inconclusive.** I ran MFCC DTW (cosine, vocal stems): the title sentence across parts gives 0.49 to 0.57, against 0.50 within Part 1 (0:27 against 2:44) and 0.74 to 0.89 for different-words controls; the riders line across parts 0.62. Same words clearly lowers the distance, but I cannot tell same take from same words (the Part 1 reading already notes the within-part pair is unresolved). [M that the words are shared, L on same take]
3. **A fixed pulse with the voice free over it.** In both, speech is untimed against the grid, apart from exits placed on a grid event (V1 0:31.7 on a bar line; V2 2:36.1 to 2:36.8 into the loop change). Neither band ducks for the voice (reported, both).
4. **Pitch is held, not developed.** Both are pedal pieces (D; B) with no V to I, no sung line, no tune. Emotion is carried by layers, level and timbre, not harmony. This is the central finding of each reading, and it is the same one. [H]
5. **Heavy limiting and a dry, band-limited narrator** (V1 roll-off about 4 kHz; V2 hard edge about 4 to 5 kHz), centred, clean, against a wide band. Same sample treatment.
6. **A near-identical short pulse.** V1's hat sits every 0.385 s (156 BPM octave); V2's bass grid is three sixteenths of 0.125 s, 0.375 s (160 BPM equivalent, which is why the tracker says 161.5). They differ by about 3%. **[speculation]**: possibly coincidence of a "quick walking" figure; there is no evidence the two were designed to share a pulse, and the tempi (78 or 156 against 120) do not stand in a simple ratio.

## 3. What changes between them

- **Where the energy lives.** Part 1 is a loud band from the first second; the drums run the whole piece and are never the event. Part 2 builds its whole first minute out of absence (drums and bass silent for 28 s, drums intermittent to 1:24) and only then locks to a grid.
- **Texture of the pulse.** Part 1: syncopated, kick on odd sixteenths, hat on the evens (M-H, reported). Part 2: four-on-the-floor kick, off-beat bass (never on beat 1, "slight limp"), backbeat only after about 3:20. The Part 1 pulse is stiff-rock or hip-hop-programmed; the Part 2 pulse is dance-like but not motorik (both readings withdraw motorik).
- **How the build works.** Part 1 builds and releases in blocks (24, 28, 32 bars to the bass events at 1:15, 1:27, 1:40, odd blocks after). Part 2 builds by a slow ramp that "no single event announces" (3:26 to 3:50 fastest, about +14 dB in 24 s). Block against ramp.
- **Peaks.** Part 1 has two: the arrival at 1:40 (bass back after 24 s: -53.8 to -19.1 dB in one second, measured, width 0.78 to 0.40) and the 2:48 to 3:08 sprint. Part 2 has one big event (the drop at 1:28.6) and then ends by unmaking itself: brightness off at 4:36.8, bass gated from 4:48.6, hard cut 5:00.8.
- **The voice's fate.** Part 1's voice stays narrator throughout and returns to frame the end. Part 2's voice moves from testimony to bar-locked wordless fragments (3:28.6 to 4:37; Rayleigh p about 3e-6 at the 2.000 s period, reported; word-less is inference, L-M) and then to one stab per bar. The narrator disappears after 2:36.1 and never comes back as speech.
- **Endings.** Part 1 stops mid-effort (taper at 3:08.4, no cadence; the Part 1 pieces read it as "continues offscreen"). Part 2 withdraws, stops, rings out and taps. Neither resolves.
- **Pitch colour.** Part 1 has a flat seven (C natural) and fifth in its pedal. Part 2's seven-note set has C sharp and no C natural. Both pitch sets contain D, A and G, and both pedal on a note a minor third apart (D, B). **[speculation]**: if D were the shared home, Part 2's set is the D major scale and Part 1's pedal-with-flat-seven is a one-note darkening of it; that would make Part 2 the "relative-major light" of Part 1's grit. No source says this was intended, and Part 2's own centre is B or E, not D.

## 4. Does one answer the other?

What the data supports:
- **Order of intensity.** Part 1 starts at full strength and holds; Part 2 starts at -25.5 dBFS and ends at the same level as Part 1 had at its peak. Heard back to back, Part 2's first 90 s is the answer in kind to Part 1's 3:08 of unbroken drive: held breath after the sprint (M; interpretive).
- **Part 1 is a half.** Its own readings flag the missing finish (no cadence, a 0.4 s taper, the black). Part 2 does not "finish" either: its ending is a stop-and-tag. So the pair resolves by exhaustion, not by arrival. [M]
- **A reversal of function.** In Part 1 the narration is delivered across the first 2:48 and the band takes the last 20 s alone; in Part 2 the narration ends at 2:36 and a mechanised pressure takes the remaining 2:30. The voice-to-band handover happens at 2:48 of 3:09 (88%) in Part 1 and at 2:36 of 5:06 (51%) in Part 2. [measured, interpretation M]
- **Hole as signature.** Both pieces contain exactly one event where the rhythm section stops under the title sentence and returns bigger. That is the nearest thing the pair has to a shared motif, and it is placed late in Part 1 (2:47.8, 88%) and early in Part 2 (1:24, 28%). Part 2 places its hole where Part 1 places its first-act voice exit (0:31.7); this is a placement comparison, not evidence of design. **[speculation]** on intent.

What I would not claim: that Part 2 quotes Part 1's riff, bass line or key. I found no shared melodic material. D appears in both as a strong pitch, but that is common pitch material, not a motif; the Part 2 bass never plays D as a tonic. Nor do I claim that either is "the sequel" musically. Release order, press description and track lengths support "two parts of one commission", not a through-composed argument.

## 5. Corrections and cautions on the existing files

- Part 1 reading says the hat comb is the sum of two layers; Part 2 reading says the bass is a 3-sixteenth grid. These are different mechanisms for similar surface speeds, so "same pulse" (point 6 above) should not be used in the diptych without a separate test.
- The Part 2 reading's "calm in press vs numbers" row is right: the press word is about timbre and early texture, not about level.
- Press language ("rock" against "electronic") comes from descriptions and from CLAP tags. Instrument identity is unproven in both (Part 1: guitar inferred; Part 2: nothing recoverable). Comparisons by instrument ("guitars against synths") should be written as hypotheses.
- I did not re-run bar-lock, key, or stem-derived tests beyond those stated.

## 6. Questions for colleagues

1. **To picture:** the two musical "holes" (Part 1 2:47.8, 0.4 s; Part 2 1:24 to 1:28.6, about 4 s) both fall under the title sentence. What is on screen at each, and do the pictures hold, cut or change at the moment the rhythm section returns? The measured sync files give no cut-to-beat alignment in either part (cuts within 80 ms of a beat: 7.8% in Part 1 against 19.7% by chance; 37.2% against 42.9% in Part 2), so I cannot tell whether the picture is meant to meet these two events.
2. **To story:** the Part 2 narration stops at 2:36.1 and the voice becomes bar-locked fragments (3:28.6 onward), while Part 1 keeps a narrator to the end. What do the pictures do in Part 2 while the voice is no longer a narrator, and does the story you read still require the words, or has it become a crowd and a rhythm? If you read Part 2 as continuing Part 1's story, which beat of the race does each part's final minute cover?

(Question for the listener colleague, if time allows: after Part 1, does Part 2's 28 s of pad and thuds feel like relief or like a restart?)
