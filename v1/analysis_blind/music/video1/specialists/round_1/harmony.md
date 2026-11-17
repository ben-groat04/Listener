# video1: HARMONY specialist, round 1 (blind, measurements only)

Role: harmony and melody (key centres, loops, modal colour, motifs, lead contour). British spelling; times m:ss.
Evidence key: WIN = my reading of all ten `win_*.md` notes (and the images they cite); CH = `music_views/chords.json`; LN = `lead_notes.json`; KEY = `audio_features/summary.json`; IMG = `music_views/window_NNNNs.png`; my own runs: `v1/scripts/agents/harmony_probe.py`, `harmony_probe2.py`, `harmony_probe3.py` (chroma of the "other" stem per 20 s; spectral-peak and pYIN pitch of the bass stem).

## 1. Headline

The track is **one tonal centre, D, for 3:09**, with almost no functional chord progression. Harmony works as a **D pedal/drone with a flat-seventh (C) shuttle, an unresolved third (F vs F#), and brief A/G/Bm/F/Am visits**. The interest is in what is added to or taken away from the pedal, not in chord changes. The only measurable "tune" is the bass line's D–C–D shuttle and a long sub-bass on **F** at 2:01–2:40; there is no sung melody at all (the voice is speech). Confidence: tonic high; mode low-to-medium; "riff" notes low.

## 2. Key centre and mode

- KEY: whole song D major 0.760 vs D minor 0.756 (a tie), G major 0.511. CH time share: D 94 s, Dm 33 s, N 16 s, G 13 s, C 11 s, Am 6 s, Bm 5.5 s. 143 chord changes in 189 s, but most are one-beat flips on the 0.77 s beat grid (78.3 bpm), so they are mostly estimator noise on a dense, distorted mix (WIN agree).
- Third: my chroma of the "other" stem, normalised to D = 1 (harmony_probe.py), shows F and F# both weak and similar everywhere: 0:00 F 0.19 / F# 0.34; 0:40 F 0.52 / F# 0.34 (the only clear minor-leaning stretch); 1:00 0.36/0.40; 2:00 0.38/0.57; 2:20 0.41/0.46; 3:00 0.48/0.49. The fifth A is the second-strongest class almost throughout (0.54–1.16 of D). So the dominant sonority is **root + fifth (a power-chord/open-fifth D5)** with the third only flickering in either direction. This reconciles the major/minor tie: **the mix mostly has no third**, so "D major" and "D minor" labels are template guesses. Confidence medium-high for "no stable third", low for any one mode.
- Flat seventh: C is the third-strongest or so (0.34 at 0:00 rising to 0.70–0.73 at 0:40 and 1:20). A natural C against D gives **Mixolydian/Dorian-leaning colour** (D–C shuttle). B natural (needed for Dorian) is weak (0.21–0.59), so Dorian vs Mixolydian vs plain "D pedal with a b7" cannot be separated. Medium.

## 3. Bass as the clearest harmonic witness (new measurement)

The bass stem is the one place a single pitch can be read (spectral peak, 1.5 s frames, harmony_probe3.py; cross-checked with pYIN, probe 1):
- **0:03–0:16, the entry is not yet on D.** Peaks read F2 (0:03), **C2 (0:04–0:06; 65.7 Hz, steady over 0:04–0:07)**, G2, C3 (0:07–0:09), D3 (0:10), G2, C3 (0:13), G1 (0:15). So while CH says "D" for 0:01–0:08, the bass sits on **C** (then G/C/D). The strong D/A in chroma is the "other" layer; the low register briefly says C–G–C–D. This agrees with the one-per-beat G, C, D labels in CH at 0:08–0:10 and supports WIN 0000's "walk off the pedal" idea, now with note names. Medium-high.
- **0:20–1:13 and 1:40–2:00: D2 (73 Hz) as the root**, with steps to **C2 (65 Hz)** and sometimes **C#2** (0:37, 0:49, 2:43): e.g. 0:42 D2, 0:43 C2, 0:45 D2, 0:46 D2, 0:48 C2, 0:49 C#2; 2:37 D2, 2:39 C2, 2:40 D2, 2:42 D2, 2:43 C#2, 2:45 D2. So the bass line is a **D–C–D shuttle (I–bVII–I) with an occasional chromatic leaning note**; C# may be a pitch-bend/slide or an estimator error (low). This is the reliable "riff skeleton" in the whole piece. Medium-high.
- **1:15–1:39: no bass** (bass stem at floor; WIN 0060/0080). Harmony in that stretch is carried by "other" alone (see section 5).
- **2:01–2:40: a different bass behaviour.** Four sub bursts at 2:01–2:03, 2:07–2:09, 2:13–2:15, 2:25–2:27, 2:31–2:33 (about 6.1 s = 8 beats apart; WIN 0120/0140), each a near-sinusoid at **42.5–43.0 Hz**, which is **F1 (43.65 Hz) about 40 cents flat**, not D1 (36.7 Hz). So the sub is nearest **F** (the minor third of D, or the root of the relative major), possibly detuned or gliding. Meanwhile the "other" stem chroma at 2:01–2:03 is D 1.0, A 0.95, C 0.68, F# 0.59 (F# not F); at 2:13 and 2:20 A is actually the strongest class (1.00 vs D 0.63 / 1.16 vs 1.00 in the 2:20 window). So **bass on F, upper layers on D/A/F#** is a bitonal-feeling stack: either a sub-F under a D major-ish bed (a b3 under a major third, which would sound dark/clashing) or a tuning artefact of the separator. I flag this as a genuine open item. Confidence that the sub is near F rather than D: high (spectral peak, five bursts agree); on its musical meaning: low.
- **2:37–3:09: back to D2 with C2/C#2 neighbours** (and one F2 at 2:48); the final 3:00–3:08 sits at D2 (73.9 Hz).

## 4. Chord-label evidence, section by section (CH, validated against chroma)

| Span | CH / chroma reading | My verdict |
|---|---|---|
| 0:01–0:08 | D held 7 s | D/A pedal above, bass on C2. Static (high) |
| 0:08–0:40 | G, C, D, Gm, D, G, D, C, Dm ... loop; resolves to a long D hold 0:28.7–0:31 | D pedal with beat-rate colour from G, C, Gm, Dm; an 8-beat riff-like loop (WIN 0020), medium |
| 0:40–1:00 | C, Dm, **Fm, Cm** (0:43–0:44.8), D, F (0:52.5), A (0:55.6), G (0:58.7) | Most unsettled stretch; F natural is strongest here (chroma F 0.52). Fm/Cm coincide with a gap/cut at 0:43 so probably artefacts; F/Dm leaning minor is plausible (medium-low) |
| 1:00–1:15 | D, Dm, G, Bm cycle (Bm at 1:07, 1:10, 1:13) | The one loop with a clear relative-minor visit: D–Bm–D (a "VI" colour, bluesy-uplifting). Chroma A is strongest (0.92) here. Medium |
| 1:15–1:20 | bass out; held A (1:15–1:18), then Am, C (1:18.7), F (1:21) | A as a held suspension (V pedal), then C (bVII) as release: the most "functional" gesture in the track (medium-low, rests on upper layers only) |
| 1:20–1:27 | C, F, Bm, G, D, G | Loose C–F–G–D, a "bVII–bIII–IV–I" flavour under speech; noisy (low-medium) |
| 1:27–1:40 | D pedal; Am, D, Am, D, C, D, Dm, Am, Dm | D with A-minor/C alternation; Aeolian/Dorian feel (medium) |
| 1:40–2:00 | C, D, Dm, Am, Dm; Cm, D, Bm; D held 1:52.5–1:56 | Pedal D with neighbours; many N = noise density, not silence (medium) |
| 2:00–2:13 | D / Dm; static | Pulse-and-groove, sub bass F, no motion (medium) |
| 2:13–2:40 | **first real motion**: Dm–Am–D–G–D–Dm (2:15–2:19); then an 8-beat cycle anchored by a 3-beat **Dm** at 2:19.4, 2:25.6, 2:31.7, with one-beat Am–D–G–D–G / Em–D–Gm–Am–C / Am–D–G–Dm–F–C–D between | A repeating 8-beat loop, "Dm home, then lift through G/C/A, back". Anchor timing matches the sub-bass bursts (verified: bursts start 2:19.5, 2:25.7, 2:31.9, 2:38.3). Anchor high; individual flips low |
| 2:40–2:48 | C, Dm, D, Bm (2:47.1) then D | D–C–D and D–Bm–D shuttle; "arrival after wandering" (medium) |
| 2:48–3:09 | D, one 20.7 s unbroken label | Static D5. Chroma flat (D 0.15, others 0.07–0.10: WIN 0160) so dense distortion, no third. Last 2 s chroma drifts D to G/E/F (3:06.5–3:08.6): a tail gesture, low |

## 5. Melody, motifs and the lead line

- **There is no sung melody.** `lead_notes.json` is a pitch tracker on the vocal stem; every window note reports it follows speech or leakage (WIN 0000–0180 all agree). Speech pitch sits about B2–F3 (120–175 Hz) with excursions to G3–A4 and a stray C5 (2:44.4); that is a low male speaking voice (high for register, low for "tune"). Notes during silent vocal-stem passages (e.g. 0:00–0:09; 1:06–1:18; 2:50–3:08) are bleed from bass/guitar and must be ignored as vocal. I did not rerun the tracker; I agree with the window notes.
- **A riff exists but its notes are not recoverable.** Evidence for a looping figure: repeated D/G/C/Gm/Dm chord loops on the beat grid (0:08–0:40), a 4-beat cycle in the "other" stem (WIN 0060), the 8-beat loop at 2:19–2:40. Evidence against recovering it: "other" shows stacked partials, a thick wash, and chroma flat of a distorted wall (WIN 0040, 0160). The lead-tracker "wobble" at 3:00–3:08 (C3, C#3, D3, D#3, B2, A#2: semitones either side of D3) is bass/guitar bleed circling the tonic and flattened-second/seventh; very low confidence as a motif.
- **The one clear melodic event: the held tone at about 1:15.5–1:18.4** (a single sustained line near 1.2–1.6 kHz with partials, WIN 0060 IMG panel 1) with chroma on A, then a step to C as the voice returns at 1:18.7. Given the harmony, A over a D bed (a fifth held, unresolved) then falling a tone... in chroma terms A to C is a minor third up, so it is a pivot rather than a stepwise tune. Medium on the pitch (A), low on the instrument.
- **Bass line = the nearest thing to a theme**: D2–C2–D2 (with C#2 inflection), the sub-F sustain section, and the C–G–C–D opening. If a listener hums anything it would be this shuttle.
- **Harmonic rhythm:** the loop unit is the beat (0.77 s) in busy stretches, the 8-beat (6.1 s) cycle in 2:13–2:40, and no change at all at 2:00–2:13 and 2:48–3:09. Section boundaries are signalled more by what leaves (bass at 1:15, voice at 1:27) than by chord change.

## 6. Shape of harmonic tension through the track

1. 0:00–0:40 pedal D, bass walking in from C; beat-rate colours (settling in).
2. 0:40–1:00 most unstable: F/Fm/Cm labels, minor-leaning.
3. 1:00–1:15 locked loop with Bm visits (lift).
4. 1:15–1:40 bass-less: held A, then C, then D/Am/C (suspension, open).
5. 1:40–2:13 pedal D with sub-F bursts (static, ominous or hypnotic; interpretation).
6. 2:13–2:40 first real chord motion and 8-beat cycle (the "payoff", per WIN 0120 "lift at 2:13").
7. 2:40–3:09 settles onto an unbroken D5 and stays: harmonic arrival by stillness, not cadence. No V–I cadence appears anywhere; "resolution" is simply the stopping of motion.

## 7. What the measurements cannot tell me

Instrument identity (guitar vs synth); the actual riff notes; whether the third is genuinely absent or buried by distortion; whether the F1 sub is detuned, glided or a separator artefact; whether "Fm/Cm" at 0:43 are real. Chord labels are frame-level template matches at about 0.77 s and under distortion and speech should be treated as colour hints, not a score.

## 8. Three questions for fellow specialists

1. **Sound specialist:** the sub-bass at 2:01–2:40 reads about 42.6 Hz (F1, about 40 cents flat) while the rest of the track's bass is D2 at 73 Hz. Does your spectral/timbre evidence say it is a synthesised sine/808-style sub, and is its pitch moving (glide) or fixed? That decides whether it is a harmonic "b3" or a texture.
2. **Rhythm specialist:** do the 8-beat anchors (3-beat Dm at 2:19.4, 2:25.6, 2:31.7, matching bass bursts about 6.1 s apart) line up with a bar count and a drum fill or accent, so we can say whether the chord loop is a 2-bar cycle in 4/4, and does the bass-less 1:15–1:40 stretch keep the same bar grid?
3. **Form specialist:** my harmonic map puts boundaries at 0:40, 1:00, 1:15, 1:40, 2:13 and 2:40. Which of these coincide with your structural segmentation (voice entries/exits, drum changes, "other" level jumps), and is 2:13 or 2:40 the true climax/arrival of the form?
