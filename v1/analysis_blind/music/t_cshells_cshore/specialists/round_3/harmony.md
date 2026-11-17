# t_cshells_cshore: HARMONY specialist, round 3 (blind, measurement-only)

Read: all seven round_2 files. New script: `v1/scripts/agents/harmony_r3_cshells.py` (chord labels against stab times; partial series of the A drone; third-against-fifth in the final pad; A3/E4 at 2:22 in the "other" and vocal stems; 1.0-1.8 kHz peaks at 3:44 and 5:12; bass onset density by block). Tags: measured / INFERRED with confidence; round-2 tags are kept unless I say otherwise. Times m:ss.

## 1. Answers to questions put to me

**Rhythm Q1: do chord changes land on the stabs (60.8, 64.8, 68.8, 72.9, 76.8 s) and later stabs?**
Grid: chords.json label starts (a roughly 0.5 s labeller frame) against the stab attack times from Rhythm, tolerance 0.3 s. Measured: in 1:00-2:00 there are 60 label changes. Of ten stab times (60.8, 64.8, 68.8, 72.9, 76.8, 80.8, 82.8, 88.9, 97.0, 113.4) eight have a label starting within 0.03 s (60.84, 68.87, 72.86, 80.81, 82.83, 88.91, 96.99, 113.43); 64.8 and 76.8 have none. The label that starts on the stab is A in six of the eight (Am at 72.9, F at 68.9). The labels between stabs flicker (Dm, F, N, F#m, C, D at 61.4, 62.4, 68.4, 72.4, 84.4, 92.4, 93.5, 96.5). Chance level: with about one change per second, a 0.6 s window catches one about 45% of the time, so 8 of 10 is only mildly above chance. Verdict: the stable A is what lands on stab attacks; the off-stab labels are decay, smear and noise. No harmonic movement is tied to the 4 s cycle. Medium-low. The harmonic rate cannot be said to follow the tempo rise (4.0 to 3.95 s): the labeller frame is fixed, so it cannot show drift (low).

**Rhythm / Harmony Q2 and my own Q2 (does the bass change character at about 3:20, or only pitch?).** Measured with pYIN-free onset detection on the bass stem: onsets per second 2.92 (2:30-3:10), 5.68 (3:20-3:45), 7.36 (4:15-4:40), mean onset strength 2.46, 0.74, 0.63; the ratio of 95th to 20th percentile RMS (a crude pulse depth) 16, 22 and 29 dB. So after about 3:20 the bass has more, softer-edged onsets and a deeper dip between them, and the pitch offset also moved from -22 to -2 cents. Both change at once, which fits a different take or part (INFERRED, low-medium), not only a retune. Onset detection on a separated stem is noisy; I do not overread the absolute rates.

**Sound Q1: is the final pad an open fifth or does it have a third?** Peak levels (dB, arbitrary, "other" stem, FFT):
- 5:22-5:30: E5 (659 Hz) 55.7 is the strongest; E4 36.8; C#4 30.3; C4 18.3; A4 21.8.
- 5:30-5:38: A4 61.0 strongest; A3 44.8; E5 44.7; E4 23.8; C4 16.0; C#4 13.0.
So in the second half the pad is A and E (A4 about 37 dB above E4, 45 dB above C4/C#4), with no third; in the first half C# is 12 dB over C but 25 dB under E5. It is an open A-E fifth with the weight moving from the fifth (E5) to the A (A4): the "missing fundamental" reading fits (A3 is 16 dB under A4). Measured, high that no third is established; medium on the E5-to-A4 shift. The chord labeller is no guide here: chords.json ends with a single Am label from 5:01 to 6:01 (the audio ends at 5:42.8), so the "Am" is a smoothed tail label, not a measured minor third. This corrects my round-2 phrase "A minor 0.87 at 5:30 on": it came from key-slice summaries, not from a measured C in the pad. Corrected, medium.

**Sound Q1 / my Q1: how much of C# and G is overtone?** The 0:25-0:32 drone ("other" stem), partials relative to the fundamental (219.0 Hz, about 10 cents flat of A3): 2nd -7.0 dB, 3rd -10.2, 4th -32.5, 5th (C#, 1095 Hz) -36.8, 6th -43.6, 7th (G, 1533 Hz) -44.4, 8th -42.3. Inside that drone, C and C# at 262/277 Hz are -31 and -34 dB, E4 is +4.6 dB (the 3rd-partial family). So the drone is nearly a pure, low-harmonic tone (2nd and 3rd strong, partials 4-8 gone below -32 dB): its own overtones cannot supply the C# (-37) or G (-44). My round-2 idea that C# and a flat G in the loud body are mostly overtones of a saturated A tone is therefore not supported by the drone (a clean source), and still untested for the distorted body (the stem at 2:00 onward is saturated; I did not isolate a single A tone there). Revised: G as an overtone is low; G as a played note (bass root at 4:12-4:40, 89 against 19 pYIN counts) stays medium-high. Measured; the drone is the only clean sample.

**Voice Q: is 2:22 (A3 219 Hz, E4 328 Hz) also present in the "other" stem; and are 3:44 and 5:12 lines (1.2-1.6 kHz) present there?**
- 2:21.5-2:22.5, level re arbitrary: other stem A3 50.5, E4 38.1, A4 30.6, E5 32.7; vocals stem A3 26.5, E4 35.3, A4 6.1. At 2:22.5-2:26 other: A3 53.8, E4 56.7; vocals A3 16.2, E4 31.8. So the A3/E4 pair is present in the "other" stem 24 to 25 dB stronger on A3 than in the vocal stem, and the E4 is about 21 dB stronger in "other" than in vocals in the second window. Conclusion: the vocal-stem harmonic series at 2:22 is a leak of the A-E pitched layer, not an independent vocal pitch (INFERRED, medium-high). This supports Voice's lowered reading.
- 3:44 (3:43-3:46): "other" peaks at 1069 Hz only 24.6 dB over its median; the vocal stem peaks at 1211 Hz, 36.1 dB over. No matching tone in "other": the 3:44 event exists mainly in the vocal stem (medium); no harmonic lead line.
- 5:12 (5:11-5:14): "other" peaks at 1571 Hz (36.5 dB over median; G6 is 1568 Hz); the vocal stem peaks at 1342 Hz and 72 dB over median. So the 1572 Hz line is in "other" too and sits on a G (the flat seven, an octave-plus above the bass G). It is a G-family note on a held A-centred bed, not an A chord tone (measured, medium). Whether it is a lead or a separation artefact I cannot say.

## 2. Corrections
1. My round-2 overtone hypothesis (C#/G from saturation) is weakened by the drone's partial series (section 1).
2. "A minor at 5:30 on" is withdrawn as a measured claim (single smoothed label; no C in the pad).
3. Chord labels at stabs: round 2 said 17 of 60 changes fall within 0.15 s of an "other" onset (28%); the stab-time test above gives 8 of 10 stabs with a change within 0.03 s, but at roughly 45% chance level. I keep "weak alignment", not "locked".
4. Form's redraw (G-centred bass block 4:11.5-4:36.5, bass edges) is accepted; I had tied it to 4:00-4:40 loosely.

## 3. Connections
- Rhythm and form: the sections come from the bass root and bass presence; the bass also changes behaviour at about 3:20 (more, softer onsets, tuning -22 to -2 cents), so the "loud plateau" is not one uniform texture.
- Sound: a clean low-harmonic drone at 0:25-0:32 against a saturated body later: the sound changes from pure tone to rich texture, while the pitch plan stays A.
- Voice: both pitched "voice-like" events (2:22, 4:56) sit on the track's A and E; the 2:22 one is a leak from the pitched layer.
- Feeling: bare A-E, flat seven and no heard third: stern, open, unresolved. Metaphor-level.

## 4. Era evidence (rule 1) and end of track (rule 4)
Harmony contributes only the bass offsets (-22 cents at 2:00-3:20, about -2 at 3:20-4:40, -12 at 5:00-5:22, pYIN), mild support for non-grid-locked tonal material (INFERRED, low-medium). The drone's near-pure partial series gives no band-limited or noisy layer. End of track and peak figures are carried from Sound's 10 ms work: last audible sound 5:42.8, a fade, no hits. Pad pitches A and E as above.

## 5. Boundary table (rule 3, harmony-relevant)
| Boundary | drums | bass | vocals | other | carried by |
|---|---|---|---|---|---|
| about 3:20 | carried: present | tuning -22 to -2 cents; onsets 2.9 to 5.7 per s | floor | E nearer A by 4 dB | bass only; not a Form boundary |
| 4:11.5-4:36.5 | fills (carried) | root G 89 to A 19 | floor | A top class, G and E -6 dB | bass |
| 5:22-5:38 | out 5:17.1-5:18.9 (carried) | out 5:22.5 (carried) | flashes | E5 to A4 weight shift, no third | other |
Mix-level drops: carried from Form, not re-measured.

## 6. Settled conclusions
- **Key and mode:** A centre with a bare fifth (E), a flat seven (G) and no established third: bass has no C or C# at all, the pad has none, the "other" stem has a weak C# lead of 4-6 dB over C in the body only. A Mixolydian or A-pentatonic reading is better supported than minor or major. Medium-high.
- **Progression:** essentially one chord; the stable A lands on stab attacks and the flicker (Dm, F, F#m, C) is decay and smear. The F#m/D lifts are not sections. The one real move is the bass root going to G at 4:11.5-4:36.5 (I to bVII). Medium-high.
- **Form is carried by the bass root and presence, not chords:** A pedal, bass tuning/onset change at about 3:20, G-root block, then an A-E open pad. Medium.
- **Overtones and leaks:** the clean drone shows C# and G are not its overtones; the 2:22 vocal-stem pitch is a leak of the A-E layer (high in A3/E4, medium-high on leak). G at 5:12 (1571 Hz) is a real tone in "other".
- **Final pad:** open A-E fifth, weight moving from E5 to A4, no third, fading to 5:42.8; "Am" at the end is a labeller artefact. Medium-high.

## Not recoverable by measurement
- Major or minor as a listener would hear it: the third is masked or absent.
- Whether G in the loud body is a played note or an overtone of a distorted A: only the clean drone was tested.
- Instrument identity of drone, pad and bass: not measurable from a separated stem.
- Meaning of the bass tuning offset (tape, detune, bend, separator): one number cannot say.
- Whether the 3:44, 4:56 and 5:12 pitched fragments are voice, lead or artefact.
- Performer, recording date, intent.
