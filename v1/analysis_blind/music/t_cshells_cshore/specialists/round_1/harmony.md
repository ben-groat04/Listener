# t_cshells_cshore: HARMONY specialist, round 1 (blind, measurement-only)

Evidence: all 19 window notes (win_0000 to win_0360), chords.json, lead_notes.json, audio_features/summary.json, window images as described by the window notes, and my own runs: `v1/scripts/agents/harmony_check.py` (chord shares; CQT chroma per stem per section) and `harmony_tune.py` (tuning, bass f0, final-stack FFT). Tags: measured / INFERRED / speculative, with confidence.

## 1. Headline
- **One tonal centre, A, for the whole track.** Whole-song key A minor 0.675 vs A major 0.650 (summary.json); every 30 s slice has A as its top-two keys (A minor 0.54-0.87, A major 0.53-0.70). The A row of the "other" stem chroma is the maximum (1.00) in every section I measured (0:25-5:40). Measured, high.
- **The mode is genuinely unresolved, and I think the reason is that there is mostly no third.** chords.json time share (to 5:50): A 31.0%, Am 28.4%, N 11.2%, F 8.2%, G 8.2%, Dm 3.1%, D 2.7%, Em 2.2%, F#m 2.1%, Gm 1.2%. The near 50/50 A / Am split is a labeller coin-toss. My stem chroma shows C and C# both weak in "other" (0.3-0.45 against A = 1.0, e.g. 1:05-1:40 C 0.42, C# 0.37; 2:00-2:20 neither above 0.3), while E (0.40-0.86) and G (0.34-0.83) are the strongest non-A classes. So the dominant sonority is **A-E (open fifth, a power-chord/drone) with G (flat seventh) above it**, and the third is absent or masked by distortion. Measured, medium-high. Reading: A5 with b7 = a modal (Mixolydian/Aeolian-neutral) rock-and-drone harmony, not functional major or minor. INFERRED, medium.
- **Harmonic rhythm is very slow.** Chord changes are 1-4 s apart (1 bar at 123 BPM is 1.95 s) in the main body, and 0:25-0:39 and 1:00-1:20 are a single drone with only a 4 s hit cycle. Everything faster than about 1 s in chords.json (Dm, Gm, F#m, G#, Em, N flickers) I treat as transient/fill smear, not harmony (the window notes agree, e.g. 3:32 and 4:26-4:32).

## 2. Section-by-section harmony (checked against the window notes)
| Time | Harmonic content | Evidence | Confidence |
|---|---|---|---|
| 0:00-0:11.3 | Nothing. Mix is exactly zero; chords.json "F" is an artefact. | win_0000, per_second_levels | high |
| 0:11.3-0:24.4 | Pitchless noise/click collage; chords.json N; other-stem chroma near flat (C# 1.00, D 0.96 ... A 0.85). No key. | win_0000 | high |
| 0:24.4-0:32 | Drone on A: FFT 0:25-0:29 fundamental 109.5 Hz (A2) with partials 219, 329, 438 Hz (win_0020). My CQT on "other" 0:25-0:32: only A above 0.3. A bare tonic pedal, no third, no fifth worth naming at this point. | win_0020; harmony_check | high |
| 0:32-0:39 | Entry hit then quick chord labels G, Bm, A, D, Am, F, Am. Too fast to be a progression (0.5 s each). A stays the pedal. | chords.json | low on names |
| 0:39-0:59 | Slow-ish F / Am / Dm alternation: F 39.2, Dm 40.2, F, Am 41.1, F, Am, F 43.6-47.0, Am 47.0, F, Am 48.0, Dm 48.9-51.9, D/Dm flips 51.9-53.9. Reads as A pedal under bVI (F) and iv (Dm): the aeolian pair. The Dm/D flipping (F vs F#) is mode ambiguity, medium-low. My "other" chroma 0:40-1:00 shows F 0.37, G 0.36, F# 0.33. | win_0040; chords.json | medium |
| 1:00-1:20 | Pure A drone struck every ~4 s (hits 1:00.9, 1:04.8, 1:08.8, 1:12.9, 1:16.8). Chords flicker Am/A/F with no real change. Bass stem A (chroma 1.00, next best G# 0.31). | win_0060; harmony_check | medium-high |
| 1:20-1:40 | Same A pedal, 4 s stab cycle; F reached 1:33.5-1:36.0, and a **rising chroma climb C to G between about 1:31 and 1:33** into the 1:33 hit; the same F-A-C-A move at 1:36-1:37.5. | win_0080 | medium (climb), low (names) |
| 1:40-2:00 | A with E: "other" chroma A 1.00, E 0.44, G 0.34 (100-120 s). Bass sustained on A2/G2, pulsed from 1:53 (IOI 0.24-0.27 s, an eighth at 123 BPM is 0.244 s). | win_0100; harmony_check | medium |
| 2:00-2:40 | A-pedal with brief lifts: A/Am 2:00-2:07.5; F#m, D 2:07.5-2:09.5; A; F#m 2:17.6; D 2:21.7; Em-Gm-Am run 2:24.6-2:26.2; F-Am-Dm-Gm 2:29.6-2:33; chromatic walk F#m-Gm-G#-A at 2:38.6-2:42. Chroma: A, E and G; G heavy 2:24.5-2:26 and 2:37.5-2:39. The bass in this region has strong G# (0.82-0.88 in 2:00-3:20 bass chroma), but see section 4. | win_0120, win_0140, win_0160; harmony_check | medium (centre), low (names) |
| 2:40-3:20 | A held, with G colour (A-G over bass A), E (dominant, 2:47.5-2:49.5), F#m-D (2:54.5-2:56), long G 3:18-3:21 (win_0180: G 198-200.9 s), D, Em. Slow: one chord per 2-4 s. | win_0160, win_0180 | medium |
| 3:20-3:44 | A, Dm 3:25, Em 3:27, A, G 3:33-3:36 (3.4 s), then fast ladder A-Em-D-G-E-A before 3:43. | win_0200, win_0220 | medium (A, G), low (ladder) |
| 3:45-4:00 | **Bass leaves 3:45.2; A and G both lit continuously**, E weaker; chords A 3:46-3:48.7, G 3:48.7-3:52, A. Then A with E/B (open fifth), Dm/D flickers 3:56-3:58. Static A+G sustained, drone-like. | win_0220 | medium |
| 4:00-4:40 | **The clearest progression in the track: a two-chord vamp A to G (I to bVII)**, 3-4 s per chord: A 4:00.8-4:03.2, G 4:04.2-4:07.5, A 4:08.1-4:11.5, G 4:12-4:13.9, A 4:14.9-4:18.9, G 4:19.9-4:23.3, A 4:23.3-4:26.8, A 4:32.1-4:35, G 4:35.5-4:38.9, A 4:38.9. Bass pitch follows it: G2 4:12.2-4:14.5, A1 (55 Hz) 4:16-4:18.9, G1 4:19.3. Bass chroma 4:00-4:40: G 1.00, A 0.94. | win_0240, win_0260; harmony_check | high (A/G alternation) |
| 4:40-5:00 | A, E (4:46.9), G 4:51.3 held, then A; D at 4:54.7; N/Dm near 4:58. Chroma A, G, E dominant. | win_0280 | medium |
| 5:00-5:20 | A-centred with G; bass held notes A2, G2 5:07.5-5:08.5, A2 5:14.3-5:15.6, E3 5:17.5-5:20. Chroma A 1.00, E 0.86, G 0.72. | win_0300; harmony_check | medium |
| 5:20-5:42.8 | **Final A-E pad.** Bass leaves 5:22.5-5:24.5; drums gone since 5:18.5; "other" is a sustained tonal stack (spectral flatness 0.0026 at 5:20-5:28) that dissolves to noise by 5:39. My FFT of "other" 5:25-5:42: peaks 217.0 Hz, 437.3, 657.1, 875.6 Hz = A3, A4, E5 (659 Hz), A5 (880 Hz): octaves of A plus a fifth, and no third. Chroma at 5:20-5:40: A 1.00, E 0.80. Ends on an unresolved-sounding open A5 (no leading note; it is not a cadence, it is a tonic held then faded). The peaks are about 10-25 cents flat of equal temperament at A=440 (217.0 is -23 cents, 437.3 is -11 cents, 657.1 is -5 cents): a tape-like or detuned sample/instrument. | win_0320, win_0340; harmony_tune | high (A+E), medium (flatness reading) |
| 5:42.8-6:01 | Digital silence (win_0360). chords.json "Am" 301-361 s is a tracker tail artefact. | win_0360 | high |

## 3. Key centres, modal colour, and modulation
- **No modulation.** The 30 s keys never leave A (A major or A minor top-two in all 12 slices bar the NaN tail); D major is the third candidate throughout (0.36-0.53, highest 0.53 at 4:30-5:00), which is just the subdominant (D) and G/E neighbours in the same pitch set, not a key change. Measured, high.
- **Pitch set**: from the chroma of "other" (all sections) the strong classes are A, E, G with weaker D, B, F# and F. That is A, E, G with optional D = A minor pentatonic or Mixolydian/Dorian-leaning, with no third present as a stable pitch. If a third is heard, it is the player or the pad's choice moment to moment (the labeller flips A/Am every 0.5-3 s: A 31.0% vs Am 28.4%). INFERRED, medium.
- **bVII (G) and bVI (F) are the tonal colour.** G holds 8.2% of chord time, F 8.2%; D and Dm only 5.8% together. The home chord is A, the "other" chord is G. Minor-iv (Dm) only occurs in 0:39-0:59 and around 3:25 and 3:56; it is a brief darkening, not a recurring part of the vamp. Measured (shares), INFERRED (colour reading), medium.
- **Tension/brightening moves**: 2:07-2:21 lifts to F#m/D (vi-IV, a brightening), the chromatic walk F#m-Gm-G#-A at 2:38-2:42 (a rising scale into A), the rising chroma climb C-G at 1:31-1:33 (into the 1:33 hit). These are the only directed harmonic gestures other than the final fade. Medium (1:31-1:33, 2:38-2:42), low-medium (F#m/D names).

## 4. Caveats on the bass G#
Bass-stem chroma in 2:00-3:20 reads G# 0.82-0.88 (and A 1.00); G# is not a plausible tonal pitch class here. The bass stem tuning estimate is -0.13 to -0.41 semitone (median around -0.2; other stem about 0), and the median bass f0 in 2:30-3:00 is 54.5 Hz with 10-90th percentiles 48.5-59.9 Hz (A1 is 55 Hz, G#1 51.9 Hz). So the bass is a flat, glissing or detuned A (a bent, overdriven low note), and the G# reading is the flat-of-A bleed into the neighbouring bin. INFERRED, medium. The window notes' "D#2/G#1 glide at 4:14.8-4:15.9" (win_0240) is consistent with a real downward slide G to A, not a tracker glitch, but I cannot separate the two.

## 5. Melody and motifs
- **There is no sung or played lead melody in the measurements.** Vocals stem sits at the floor (-71 to -85 dB) except: 2:21.5-2:26.5 (peak -25 dBFS at 2:22, decay to -57 by 2:25: a processed speech-like burst; Whisper vocals pass gives one segment 2:21.7-2:24.3, language tag cy, p 0.49, low confidence); 5:12.3-5:12.8 and 5:16.7-5:17.2 (-28 to -43 dB flashes); 5:30-5:42 (rising from -62 to -50 dB as the pad fades, speech-like, an unmasking effect per win_0320). So lead_notes.json is a bass/pad tracker, not a voice. I agree with every window note on this. High.
- **Riff-like content is a bass or low-synth figure around the tonic.** Bass notes: A2 repeated with a fifth up to E3 (2:39-3:00: A2 159.4-165.4, E3 161.6-162.5, A2, E3 177.5-178.4), G2 to A1 to G1 root motion (4:12-4:19), and A2/G2/A2/E3 at 5:00-5:20. That is a root-and-fifth pedal with the flat-seven step, i.e. A, E, G, the same pitch set as the chroma. Eighth-note pulse from 1:53 (IOI 0.24-0.27 s, tracker beat 0.488 s, 123 BPM). No melodic hook with a repeatable contour is recoverable. Medium.
- **The one gesture that behaves like a melodic phrase**: the lead tracker's falling F5-F5-E5-C#5 at 3:44.5-3:50 (F5 698 Hz, E5, C#5 about 554 Hz). It follows the bass exit at 3:45.2. F is not in A major; it is b6 of A natural minor, and C#5 the major third of A. Tracker confidence weak, no voice in the stem. I could not confirm it as a sound; low. Do not use it as a melody claim.
- **The 1:03.6-1:04.6 F3-E3-G2 "falling four-note figure" (win_0060) and the 0:39-0:41 C4-D4-C#4-C#4-C4 cluster (win_0040)** are within-a-tone wobbles of tracker origin; low. The 4:07 G3-A3-G#3 wobble sits on the chord roots; low.
- **Rhythm-as-motif**: the 4 s hit-and-decay cycle (about 8 beats at 123 BPM, 1:00-1:40) is the main repeated gesture. It is rhythmic and tonal-static; a "riff" only in the sense of a repeating chord stab on A.

## 6. Production-era evidence relevant to harmony (rule 1)
- Pitch level: the "other"/final pad is about 10-25 cents flat of A=440 (figures above), and the bass stem tunes around -0.2 semitone: the track is not locked to a DAW A=440 grid in those layers. That mildly suggests played or sampled-from-tape tonal material, INFERRED, low-medium.
- Other era evidence is for the rhythm and sound specialists (peak -0.57 dBFS at 1:20-1:40 per win_0080, sample peak at 22.05 kHz; kick onset +10/-20/+30 ms from the beat grid in win_0060, n=3). I did not re-measure them. The 4 s repeated cycle regularity is a loop-style cue: hits at 1:00.9, 1:04.8, 1:08.8, 1:12.9, 1:16.8 (spacing 3.9, 4.0, 4.1, 3.9 s, a spread of 0.2 s, not machine-exact on this measure; those are the window-note times, which I did not re-run).

## 7. Boundary evidence for harmony-relevant boundaries (rule 3)
I did not re-run the stem-by-stem change test; the figures here are taken from the window notes and from my per-stem chroma. Carried with the notes' tags.
| Boundary | drums | bass | vocals | other | carried by |
|---|---|---|---|---|---|
| 0:24.4 drone enters (mix -49.7 to -39 dB, -37 by 0:25) | fades -54 to -69 dB by 0:29 | at floor | at floor | A2 109.5 Hz stack enters | other |
| 1:04.8-1:06 rhythm section arrives | enters, -81 to -35 dB | enters about 1:06 (-79 to -51 dB) | none | steady drone | drums then bass |
| 3:45.2 bass leaves, A+G wash | present | exits | none | A+G stack | bass |
| 4:00-4:40 A/G vamp | fills | pitch follows chord (G2, A1, G1) | floor | A, G, E | bass (root) |
| 5:17.1-5:18.9 drums exit; 5:22.5-5:24.5 bass exit | out 5:17.1-5:18.9 | out 5:22.5-5:24.5 | flashes 5:12, 5:17 | continues -15.5 dB to 5:29.5, fades to 5:42.8 | other holds the final harmony |
| 5:42.8 end | out | out | out | out | all |
(Mix dB drops at boundaries are as stated in the window notes; I did not re-measure.)

## 8. End of track (rule 4)
I did not re-measure the 10 ms envelope; I take the window notes: last audible sound 5:42.81 (342.83 s), digital silence after, file ends 360.98 s (about 18.1 s of silence), "other" stem -67 dB at 5:42 and falling from -15.5 dB at 5:29.5. The ending pitch stack is A-A-E-A (my FFT, section 2). No final hits (drums gone since 5:18.5; no count made).

## 9. Disagreements and corrections to the window notes
1. win_0220 and win_0240: "A vs G alternation, I-bVII" at 4:00-4:40 is confirmed, and I rate it high; it is the only recognisable progression. The earlier 3:45-3:52 note calls the A+G a "static sound, not a progression"; my reading agrees but the bass chroma (G 1.00 at 4:00-4:40, 0.99 at 3:00-3:20) shows G is a bass root at times, not only a colour on top.
2. win_0120 reads the F#m-D lift as "vi to IV in A major": possible, but with C/C# both weak, F#m is only a label; I rate "F#m" low.
3. win_0100 "A2, G2, C#2 style low pitches" for the bass: C#2 is not supported by my bass chroma (A 1.00, G# 0.44, no C#). I treat C#2 as a flat low-note artefact.

## 10. What I would feel, honestly (feeling, not a claim)
Open A with a droning fifth and G above it: stark, modal, neither sad nor bright, a held unresolved sonority. The hit-and-decay cycle sounds like waiting; the A/G vamp from 4:00 is the one place the harmony moves in a way that feels like a rock groove. The close is a bare A-E stack that thins into noise, then 18 s of nothing. (interpretation, medium)

## 11. Not recoverable by measurement
- Whether any chord is "really" major or minor: the third is absent or masked in the stems; labellers flip.
- Exact instrument identity of the drone, pad and bass (organ, synth, distorted guitar, sample): chroma and FFT give pitch classes and partials, not timbre source.
- Whether the F5-E5-C#5 figure (3:44-3:50) is a real sound or tracker noise.
- Whether the slightly-flat tuning (10-25 cents) is deliberate, a tape source, or a detuned synth.
- Composer or performer intent behind the A/G vamp, and whether the quick chords are real changes or fills.
- What the vocal-stem burst at 2:21.5 says, or its language (Whisper cy p 0.49).

## 12. Questions for fellow specialists
1. **Sound specialist**: is the final pad (5:20-5:42.8, partials 217, 437, 657, 876 Hz, flatness 0.0026 rising to 0.087) a sustained oscillator/organ-like tone or a processed sample, and does the 10-25 cents flat tuning fit a tape/older-source layer under a modern mix?
2. **Rhythm specialist**: does the bass pulse after 1:53 (IOI 0.24-0.27 s) lock to the kick grid, and do the four-second stabs from 1:00 to 1:40 (3.9-4.1 s spacing) fall on a bar grid (8 beats at 123 BPM = 3.9 s) or drift by loop-machine versus played spread?
3. **Form specialist**: does the A/G vamp (4:00-4:40) mark a distinct section from the A-pedal section before it (3:20-3:45), and do the rising-chroma gestures (1:31-1:33, 2:38-2:42) line up with section boundaries in your boundary table?
