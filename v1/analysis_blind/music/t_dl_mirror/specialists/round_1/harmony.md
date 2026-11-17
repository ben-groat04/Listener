# t_dl_mirror: HARMONY specialist, round 1 (blind, measurements only)

Evidence base: all twelve `win_*.md` window notes (read and cross-checked); `music_views/chords.json`, `lead_notes.json`, `window_0140s.png` (opened; chroma and lead panels), `audio_features/summary.json`, `lyrics/whisper_medium_vocals_auto_transcribe.txt`, and my own run `v1/scripts/agents/harmony_t_dl_mirror.py` (chord-run statistics, stem chroma, loop autocorrelation, level steps). Times m:ss. Demucs stems are estimates; the chord labeller is a chroma tracker and is crude.

## 1. Headline

The harmony is a **static D + A open-fifth drone bed with a very weak, unsettled third**, over which a hook is sung and verses are rapped. Real chord movement is rare and formulaic: a short **Gm - G - F - (C or Am) - Dm "side-step"** (about 2.5-4 s) that appears in eight places, always in pairs about 9 s apart, with the pairs about 60 s apart (about 24 bars). The whole song is therefore a one-chord vamp with a recurring four-bar-based turnaround. Key: D (D minor 0.69 whole-song, `audio_features/summary.json`). Mode: D minor is the best reading, but the evidence for the minor third comes from the voice, not the bed (section 3). Confidence: high on D and on the drone; medium on minor; medium on the side-step labels.

## 2. Chord statistics (measured, `chords.json`, 189 labels)

| Label | Time share (s) |
|---|---|
| D | 118.1 |
| Dm | 82.0 |
| N (none) | 11.9 |
| Gm | 7.7 |
| G | 5.0 |
| F | 5.0 |
| Am | 3.2 |
| C | 1.9 |
| A# (one, 3:55.7 over a very quiet tail) | 3.7 |
| F#m (one frame, 1:08.1) | 0.6 |

D and Dm together are about 200 s of roughly 239 s: about 84 % of the track. The D/Dm label flips every 0.6-2.5 s, with D held longer (e.g. 4.5 s at 2:58, 3.8 s at 3:08) but with no fixed positions. **Reading: not a real major/minor alternation.** Measured evidence in the other stem (my chroma, 30 s blocks): D 1.00, A 0.85-0.99 everywhere; strongest other classes are C 0.37-0.41, C# 0.29-0.33, G about 0.3; over 40-200 s F 0.17-0.19 against F# 0.24-0.26 (F and F# both under 0.26 while D and A sit at about 1.0). The third is at roughly a quarter of the strength of the root and fifth, and the sharp third is slightly stronger than the flat third in the bed, which is the opposite of what a labelled "minor" bed would show. Colleagues who wrote "D and Dm flicker = estimator noise on a thirdless fifth" are supported (INFERRED, medium-high). The Dm/D label split should not be reported as modal mixture or as a "major-minor clash" (one window note floated that; low, and I do not support it).

Bass stem chroma is D 1.00 with D#/C# next (0.6-0.76): that is smear from low-frequency pitch estimation and sub-bass, not harmony. Pyin on the bass stem (win_0160 note, 2:42-3:00) found D1 (about 37 Hz) and D2 (about 73-75 Hz) with glides D2 to D3 passing A2: the bass plays the root only (INFERRED, medium, octave placement uncertain). So the bass does not supply the third either.

## 3. Mode and the third: where the minor comes from

- The bed is thirdless (above). The **voice** supplies a third: in the sung-hook stretches (0:10-0:30, 1:17-1:32, 2:12-2:32, 3:14-3:36; 40.8 s of tracked notes) the lead pitch-class share is A 39 %, G 24 %, F 17 %, G# 9 %, C# 6 %, F# 1 % (my tally of `lead_notes.json`). F natural (the minor third) is 17 %; F# (major third) about 1 %. That favours D minor (or a D-based minor/Dorian-type colour) over major (INFERRED, medium; tracker labels on a processed voice, +/- a semitone).
- The hook is built on the fifth (A4) and its neighbours G and F: a falling A - G - F fragment, which with D is a D minor pentatonic-style cell (D, F, G, A) (INFERRED, medium). The recurring **C#5 flick** (0:23, 1:24, 2:25, 3:26; the top of each hook) is the major seventh, a leading-tone pull to D. A recurring G#4 (9 %) is a passing tone between G and A. Together F, G#, C# give the hook a slightly smeared, bent contour. Whether these are deliberate chromatic notes or pitch-bend and tracker error cannot be told (low).
- C natural (0.37-0.41 in the bed) slightly above C# (0.29-0.33): too close to call a flat or a natural seventh from the bed (low). The side-step chords include F and C (III and VII of D minor), so C natural is genuinely present in those moments, which supports the natural-minor (Aeolian) reading over Dorian (Dorian would be G major, not Gm, as IV). Gm is the labelled minor chord (7.7 s Gm against 5.0 s G), so natural minor, not Dorian, is slightly favoured (INFERRED, medium-low: Gm and G also flip on the third).

## 4. The side-step and the form it implies (measured)

Chord runs away from D, from `chords.json`, with level steps from my script (2 s before > 2 s after, dBFS):

| Run (m:ss) | Labels | Mix | Drums | Bass | Vocals | Other | Carried by |
|---|---|---|---|---|---|---|---|
| 0:16.7-0:19.2 | Gm G F Am | -9.8>-9.2 | -19.5>-17.0 | -14.1>-14.9 | -19.1>-22.0 | -25.8>-26.2 | harmony (chroma), vocals dip about 3 dB |
| 0:25.6-0:29.4 | G Gm F C | -10.3>-10.7 | -19.5>-19.9 | -13.9>-16.2 | -23.7>-20.2 | -24.7>-24.9 | harmony; vocals up about 3.5 dB |
| 1:17.6-1:20.1 | Gm F C | -10.0>-10.0 | -20.3>-18.7 | -14.2>-14.6 | -18.4>-23.0 | -25.1>-25.3 | harmony; vocals dip about 4.6 dB |
| 1:26.5-1:30.3 | Gm F Am | -10.5>-11.0 | -19.9>-19.6 | -14.0>-17.6 | -23.0>-20.4 | -24.0>-24.0 | harmony; bass dips 3.6 dB |
| 2:17.4-2:21.2 | Gm G F Am | -10.0>-10.7 | -20.0>-19.1 | -14.4>-17.1 | -18.4>-19.9 | -25.4>-25.6 | harmony |
| 2:28.8-2:31.3 | G Gm F C | -10.1>-10.1 | -20.3>-19.1 | -14.5>-14.7 | -18.8>-24.5 | -24.7>-23.0 | harmony; vocals dip about 5.7 dB |
| 3:19.6-3:22.1 | Gm G F Am | -9.9>-10.0 | -19.8>-18.9 | -13.9>-14.4 | -18.7>-23.8 | -25.3>-26.8 | harmony |
| 3:28.5-3:32.3 | Gm G Gm F Am | -10.4>-10.8 | -19.9>-19.8 | -13.8>-15.9 | -23.6>-20.0 | -24.6>-25.0 | harmony |

The mix level never moves by more than 0.7 dB at any of these: they are **harmonic events, not level events** (the "other" stem moves under 2 dB, drums under 2.5 dB). The boundary is carried by the other stem's chroma (G and A rows lit, D row down: seen in `window_0140s.png` at 8-10 s and 15-16 s) and by the chord labeller; the vocal stem dips 3-6 dB in four of eight cases, the bass stem 2-4 dB in four. A silence is not involved.

Spacing (measured): the first side-step of each pair starts at 0:16.7, 1:17.6, 2:17.4, 3:19.6; the second at 0:25.6, 1:26.5, 2:28.8, 3:28.5. Gap within a pair: 8.9, 8.9, 11.4, 8.8 s. Gap between pair starts: 60.9, 59.7, 62.3 s (mean about 61 s, about 24 bars at 2.53 s per 4-beat bar from the 94-96 BPM tracker). The other stem's chroma autocorrelation over 0:40-1:40 peaks at a lag of 10.1-10.3 s (r about 0.92), about **four bars**, so the drone bed is a ten-second loop or is at least periodic at four bars (loop regularity: INFERRED, medium; consistent with a DAW or sampler loop, but a stable drone also gives high autocorrelation, so this is weak evidence of looping). The side-step then recurs with a 24-bar cycle, giving a form of hook (carrying a Gm run), verse (static D), and so on; form is another specialist's call. The third pair is closer in time (8.8 s) and a third repeat that would have fallen at about 3:37 did not occur: the harmony goes static, then the voice ends at 3:34.7.

Variation: the run's last chord is Am in four cases (0:19, 1:29.7, 2:20.6, 3:21.5, 3:31.6) and C in four (0:29, 1:19.5, 2:30.7, and none later); Am to Dm is v-i (minor dominant to tonic, a weak cadence) and C to Dm is VII-i; the A in the drone is common to both. Both pull back to the drone, so neither gives a strong dominant (A major / A7) cadence: there is no leading-tone C# in the chord labels (INFERRED, medium). The Gm - F - C - Dm shape is iv - bIII - bVII - i if C is VII, or iv - bIII - v - i with Am (INFERRED, medium; each chord is only 0.6-1.3 s). This is one chord per beat (0.63 s) which is the only place the harmonic rhythm is faster than a four-bar block.

## 5. Melody and lead line

Song-wide `lead_notes.json` range E3-D5 (`summary.json`). Two registers, alternating with the section:
1. **Verse (rap), low register**: A#3/B3 dominant (A# 38 %, B 22 %, A 16 %, G# 8 % of tracked time over 30-77, 92-137, 152-194 s), roughly 233-247 Hz, span 3-5 semitones; pyin on 2:40-3:00 gave a median 218.6 Hz, 10th-90th percentile 191-251 Hz, voiced 86 % of the time (win_0160). Narrow, near-monotone, speech-like. Rapped (INFERRED, high). Its pitch classes (Bb/B) are not chord tones of D minor (Bb is the minor sixth); this is speech intonation, not a melody tied to the bed. It also means harmony is **not** carried by the verse voice (INFERRED, high).
2. **Hook (sung-chanted), high register**: A4 is the centre (39 %), F4-A4-C#5 range (about 349-554 Hz), notes 0.1-0.4 s long, figure A4 - G4 - F4 falling with a C#5 flick and G#4 passing (see win_0140 and win_0200 note-by-note runs, which I checked against `lead_notes.json` and which are consistent). The register jump from verse to hook is 8-11 semitones, in one step: B3 to G4/A4 at 3:13 to 3:15; A4 to B3 at 2:32.8; and up at 1:11.7 (A4, D5 with a fifth then fourth leap) and at 2:12 (win_0060, win_0120 notes). Hook words (vocals pass): "You I see, I see / In my theory and my morning / I see you", at 3:14-3:34.7. Words are doubtful (the vocals pass has "theory", mix pass "carry/hair"); the repeated "You I see. I see." and "I see you" are legible (high).
3. The sung hook is **not** harmonised to the side-step: during Gm - F - C - Dm (e.g. 3:28.5-3:32.3) the voice stays on A4/G4/F4 (win_0200). Against Gm the A4 is a ninth and F4 a minor seventh, against F the A4 is the major third and G4 the ninth, against C the G4 is the fifth and F4 the fourth. The melody is therefore a pitch-centred chant over moving harmony, not a tune built from the chords (INFERRED, medium).
4. Early notes before 0:10.4 and after 3:36.2 in `lead_notes.json` (F4, G#4, A4, C#5 at 0:02-0:09; G4, A#4, F#4 at 3:38-3:52) are tracker noise: the vocal stem is at -65 to -78 dBFS there (win_0000, win_0200, win_0220). I disregard them (INFERRED, high). Isolated outliers (D5 at 3:13.6; D#4 at about 1:14; A#3 at 0:14.5) are probably octave or harmonic errors (low).

## 6. Riff and motif development

There is **no riff** in the "other" layer in any window view: it is a stable, banded harmonic wash from about 100 Hz to 2-3 kHz, partials at about 291-296 Hz (D4), 436-452 Hz (A4), 587-592 Hz (D5), 883-888 Hz (A5), a harmonic series on D with A and not a melodic line (win_0160 measurement, consistent with my chroma). Development is therefore by **layer, not by tune**: the bass gates in and out (bass stem out for 3-10 s stretches, about -60 dBFS against -14 dBFS in), the other stem lifts (3-4 dB at 1:11.5; a lift at 2:16-2:20), and the vocal moves between register. Pitch material does not develop: the hook returns almost note for note (A - G - F - A, C#5 peak) at 0:10-0:30, 1:20-1:32, 2:14-2:32, 3:14-3:36 (INFERRED, medium; tracker notes show the same pitch cell, rhythm not checked here).

The ending: from 3:49 the bass drops out and the other stem fades (-26 to -29 dBFS to 3:49, -47.8 at 3:54, -70 at 3:56; win_0220). My chroma over 3:45-3:55 shows the D+A block persisting (D 1.00, A 0.96 in the stem). The one A# label at 3:55.7 is low confidence. The track finishes on D + A, with no resolution chord and no cadence: it "resolves" by being the same chord it has been in throughout (INFERRED, medium; end timing from the rhythm/sound windows: last sound about 3:56.4, then digital zero to 3:59.4: I cite win_0220 and did not re-measure).

## 7. Production-era cues relevant to the harmony

- Sample peak 0.0 dBFS (my read of `audio/song.wav`; first at 0:03.46 per win_0220). Mix RMS about -10 dBFS in most sections. This is a limited, modern-level master (INFERRED, medium-high); it does not say anything on the source of the bed.
- The drone's high autocorrelation at four bars (0.92) and its near-constant level (other stem -24 to -26 dBFS) is consistent with a loop; but a held tone gives the same, so this is not decisive (low-medium).
- Stereo width is 0.0-0.024 (win_0220): effectively mono. A mono drone bed is a cue for older source material, or for a mono-summed or mono-sourced mix; I cannot separate those (low).
- I did not measure kick spread or a band-limited layer here; the rhythm and sound specialists hold those figures.

## 8. What I disagree with or tightened in the window notes

- win_0100 raised "a real clash between a minor-third bass/sample and a major-third element" for Dm/D alternation: I measured the bass stem has no F/F# strength to speak of (it shows D#/C#, the sub-bass leakage) and the bed has F and F# both weak, so the clash reading is unsupported; keep it at low.
- win_0020 (30-40 s) says "G, F, C" is iv, bVII, bIII: in D minor G is iv, F is bIII and C is bVII, so Gm-F-C-Dm = iv, bIII, bVII, i. The win_0020 wording "iv, bVII, bIII" has bVII and bIII swapped; the win_0060 wording (iv, III, VII) is right.
- Tags are carried as the window notes gave them. Where the window notes said "measured" for D+A, I agree. I lowered none.

## Questions for fellow specialists

1. **To rhythm:** the side-step is one chord per beat (about 0.63 s) while the drone changes at the four-bar or 24-bar scale: does the drum or bass pattern change at 0:16.7, 1:17.6, 2:17.4 and 3:19.6 (the start of each Gm run), or is the harmony the only thing that moves, and what is the real four-bar loop length in the drums (my chroma says about 10.2 s)?
2. **To voice:** is the hook voice really sung on pitch (A4-G4-F4 with a C#5 flick), or is it a doubled, pitch-processed or sample-triggered rap? Whether the F (minor third, 17 % of hook time) versus F# (1 %) is a real sung note matters for D minor versus a thirdless drone.
3. **To sound:** does the "other" bed contain any older, band-limited or noisy layer under the full-range drone (the stable partials at D4, A4, D5, A5 look like a sample or synth held note), and does a mono bed at -25 dBFS sit under a wider or full-band master, as the mono figure suggests?

## Not recoverable by measurement

- Which instrument makes the D + A bed (organ, synth pad, guitar, string sample): chroma and partials show pitch content, not timbre source.
- Whether the bed is a sample of older music or a new loop: periodicity and mono width are suggestive only.
- Whether F or F# is "really" sounding in the bed: both are weak and the stem is a separation estimate.
- Whether the C#5, G#4 and F4 colour notes are deliberate, pitch-bent, or tracker error: the tracker labels notes on a processed voice to about a semitone.
- The key by intention, the composer's chord names, or any recording date.
- The meaning of the lyrics: only the repeated "You I see / I see you" is legible; the rest of the words are doubtful in the transcripts.
