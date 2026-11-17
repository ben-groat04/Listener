# video2 ("Elfstedentocht Part 2"), round 1: HARMONY specialist

Scope: key centres, chord loops, modal colour, riffs and motifs, melodic contour. I cannot hear the audio; everything below is from measurements. Confidence is tagged (H/M/L). Timestamps are m:ss. Helper scripts: `v1/scripts/agents/harmony_r1.py`, `harmony_r1b.py`, `harmony_r1c.py`, `harmony_r1d.py`.

Evidence keys: [CH] chords.json; [LN] lead_notes.json; [IMG] window_NNNNs.png; [AF] audio_features/summary.json; [RMS] stems/stem_rms_per_second.json; [BC] my CQT chroma of the demucs bass stem (harmony_r1b.py); [OC] my CQT chroma and top-note read of the "other" stem (harmony_r1.py, harmony_r1d.py).

## 0. Headline findings

1. **The bass stem gives a much cleaner harmonic map than [CH].** Bass-root chroma (half-second steps, run-length merged) shows only three loop types, each made of 4-second roots: **Em-G-D(-B)** from 0:29 to 2:37, then **B-A-D** from 2:37 to about 4:48. [CH] muddles the second half into "Bm/D alternation" because a B pedal in the upper layer swamps chroma. (H for roots, M for chord quality.)
2. **The tempo is 120 bpm, not 161.** Drum-stem onset autocorrelation has its strongest peaks at 0.499, 0.998, 1.997 and 4.005 s in 1:00-1:40, 3:00-3:40 and 4:00-4:40 (harmony_r1c.py), an exact 0.5 s grid. [AF] reports 161.5 bpm, which is 4/3 of 120: its 0.372 s beat is a dotted quaver (three semiquavers) at 120 bpm. So each 4 s chord is **two bars of 4/4**, and the 12 s B-A-D loop is **six bars**; Em-G-D-B is **eight bars**. The window notes that count "10 to 11 beats per chord" inherit the tracker error. (H.)
3. **The mode is B natural minor (Aeolian), pivoting to its relative D major; it is not Dorian.** Every chord found (Bm, Em, G, D, A, F#m) is diatonic to B Aeolian; no C#-based or G#-based chord shows up in bass or chroma except stray tracker notes. The flat sixth (G) is a defining colour, present from the first second. (M-H.)
4. **There is no sung melody and no clearly extractable lead riff.** The lead tracker follows the vocal stem, which holds spoken narration, bass bleed and noise. The "tune" is the harmonic loop plus an arpeggiated or delayed figure in the "other" stem, whose pitch content I can read but whose exact contour I cannot (L-M).
5. **The harmony is built by subtraction and addition of layers, not by new chords.** The bass is entirely absent for the first 28 s and again from about 4:49 to the end ([RMS] bass 0.0000 before 0:29 and 0.000-0.001 from 4:49); the loop of the second half is the same bass-less B pedal.

## 1. Section-by-section harmonic map

| Time | Harmony | Evidence | Conf. |
|---|---|---|---|
| 0:00-0:28 | Bass stem silent ([RMS] first value above 0.01 at 0:29). Pad only. 0:00-0:08 B-F#-G-D (Bm with the flat sixth G, or Gmaj7-like); 0:08-0:12 D major lift (F#, D lit; G drops out); 0:12-0:20 back to Bm(G). Changes land on the two drum thuds at 0:08 and 0:12 in `window_0000s.png` (drums panel, chroma panel). | [IMG 0000], [OC] segment 0:00 "B G D F#", 0:08 "F# D B C#" | M-H |
| 0:20-0:28 | Move to E minor colour: top-note read shows G4-E4-E4-G4 repeating at 0.125 s steps (0:20-0:28), i.e. a G/E arpeggio over Em. | [OC] harmony_r1d.py 20 8; win_0020 | M |
| 0:29-0:40 | Em (bass E 0:28), G (0:32), D (0:36.5). Bass enters at 0:29 on E, a long sustained note per chord. | [BC] "0:28.0E 0:32.0G 0:36.5D" | H |
| 0:40-1:00 | Em, G, D, **B** (0:52.5-0:56), then Em again at 0:56. [CH] flickers A at 0:47.5 and E at 0:42.7; these are one-beat passing events, not new chords. | [BC], [CH] | H roots, M B quality |
| 1:00-1:20 | G (1:00), D (1:04.5), Em (1:08), G (1:12), D (1:16), B (1:20) | [BC] | H |
| 1:20-1:29 | Break. Bass B to about 1:25, then silent until 1:29 ([RMS] 1:25-1:28 near zero); upper layer holds Em/B (E, B, G, D in [OC] at 1:20 and 1:24). | [RMS], [OC] | M |
| 1:28-2:37 | Same loop, repeated twice more with and without the B bar: E 1:28.5, G 1:32.5, D 1:37, E 1:40.5, G 1:44.5, D 1:48.5, B 1:53; E 1:56.5, G 2:00.5, D 2:04.5; E 2:08.5, G 2:13, D 2:16.5, B 2:21; E 2:24.5, G 2:29, D 2:32.5, B 2:37. | [BC] | H |
| 2:37-4:48 | New bass loop **B - A - D**, 4 s each: B 2:37, A 2:40.5, D 2:45, B 2:48.5, A 2:52.5, D 2:57, B 3:00.5 ... repeating every ~12.0 s through 4:45. Upper layer keeps a B pedal; A and D appear above it as colour (A over B = Bm7/sus-like; D over B = Bm7/D). Brief E flicker at the end of some loops (3:24-3:25, 3:36-3:37 [IMG 0200]). | [BC], [IMG 0160/0200/0220], [OC] | H roots, M quality |
| 4:48-5:02 | Bass stem silent from about 4:49 ([RMS]). Remaining harmony is the pad/guitar-synth layer: B with F# and D (Bm), static. The bass-chroma "A#" at 4:48+ is noise, not a note. | [RMS], [OC] 4:48 "B F# A D" | H |
| 5:00-5:06 | Final stab and tail: B 1.0, F# 0.73 (open fifth, no audible third). The "B" label in [CH] is root-only; do not read it as a major ending. Final burst has A, A#, C neighbours = noise. | win_0300 own chroma; [CH] | M-H on B root, L on quality |

## 2. The loops and how to hear them

**Loop A, 0:29-2:37, "Em - G - D (- B)".** Bass roots E, G, D, then B in alternate or third cycles. Cycle lengths from bass change times: 12 s (E-G-D), 16 s (E-G-D-B). Sequence of cycles read from [BC]: 12, 16, 12, ~20 (the break), 12, 16, 12, 16, ... (timings 0:28, 0:40, 0:56, 1:08, 1:28.5, 1:40.5, 1:56.5, 2:08.5, 2:24.5). Two readings, both with the same notes:
- Heard from **B minor**: iv - VI - III - (V/V-ish B). The B-bass bar is the odd one: in the upper layer E, B, G, D are lit (1:20 and 0:52 segments), i.e. **Em over a B bass** (Em/B), or a Bsus4-like cluster, not B major. I cannot confirm the third. (M-L on its quality; labels B/E/Em in [CH] flip between them.)
- Heard from **D major**: ii - IV - I - (vi). The rocking Em-G-D is the classic "relative major" lift. The song's key estimates agree it is ambiguous: [AF] 30-s blocks list E minor, G major, D major as top keys through 0:30-2:30.
- My reading: the B pedal in the upper layer ("B" is in the top-4 of [OC] at nearly every 4 s step from 0:04 to 4:56) keeps B as the tonic even when the bass walks away to E, G and D. The effect is a **floating, unresolved plagal-flavoured loop around a fixed B drone**, which is why chroma key estimates wander but the whole-song result is B minor 0.88 ([AF]). (M.)

**Loop B, 2:37-4:48, "B - A - D".** Three chords, 12 s, repeated about nine times ([BC] cycle start times 2:37, 2:48.5, 3:00.5, 3:12.5, 3:24.5, 3:36.5, 3:48.5, 4:00.5, 4:13, 4:25, 4:37). In Bm: i - VII - III, or, heard with the pedal, **Bm - Bm7/A - D/B**: a descending whole tone (B to A) then a rise of a minor third (A to D), then a fall back to B. In D major that is vi - V - I. Both readings use the same three notes in the bass. This is the more driving, riff-like loop because the bass moves down then up, and it carries the song's climax. The window notes that describe "a Bm-D alternation with A as a minor seventh" are describing the same events from the pad side. (H for the bass loop, M for the labels.)

**Peak-density moment.** [AF] puts the loudest second at 4:48 (288.1 s). The bass stops about a second later. That is the harmonic hinge: the bass-led loop ends and what is left is the B pedal. (H for timing.)

## 3. Modal colour (what a listener would feel)

- Aeolian B minor, with G (b6) and A (b7) as the colour tones: both are in every layer. This is melancholic but not dark: the D major relative sits very close ("sunlit minor"). (M interpretation; the notes are measurement, the feeling is mine.)
- The flat-six G is the first colour heard at 0:00 and returns as the G chord in Loop A: a lift of a minor third from E, not a leading-tone tension.
- The progression avoids a V chord with a leading tone: the only dominant-like harmony is F#m (4:42-4:45 [CH]) and a brief A. There is **no functional V-I cadence** anywhere (no A#/F# major). This makes the harmony cyclical (modal-rock, drone-based), consistent with a track about endurance rather than arrival. (M-H on the absence, from [CH] chord share: Bm 135.8 s, D 44.0, Em 21.9, G 20.1, B 12.0, E 10.5, A 6.6, F#m 2.6.)
- The end has no resolution gesture: bass drops at ~4:49, a pad plateau fades, a last low stab on B with F#. Final chord is a bare fifth (M-H).

## 4. Riffs, motifs and melody

**Lead line.** [LN] range C#2-A#5 is dominated by speech and bass-bleed. Evidence that it is not a tune: it flags notes in windows where the vocal stem is at -75 to -87 dB (win_0100, win_0300 notes), it clusters on semitone clashes with the harmony (G#4, A#4, F4 over Bm, win_0240/0260), and the contour panels in `window_0200s.png` (lead panel, x=12-20 s) show scattered, jumpy dashes matching the narration bursts visible in the vocals panel. **No sung or played top melody is measurable.** (H.)

**The arpeggiated figure ("other" stem).** The one repeating melodic-rhythmic object I can read:
- 0:00-0:08: top-note read shows F#4 sustained, with B4, D5 and G4 alternating in a pulse (G4-D5-G4-D5, G4-B4-G4-B4 at about 0.25 s steps around 0:05-0:07). Onset autocorrelation gives a 1.51 s repeat and 0.75 s (harmony_r1d.py 0 8). The pad therefore has a slow arpeggiated motion over a held F#/B. (M-L.)
- 0:20-0:28: G4-E4-E4-G4 repeated, 0.25 s steps (M).
- 3:00-3:08 and 4:00-4:08: top notes B3, F#4, D4, B3, B3, F#4... i.e. broken Bm triad (B-F#-D) across two octaves with A3/A4 as a passing seventh. Onset autocorrelation of "other" peaks at 0.37 s (0.67 in 3:00), 0.24 s, 0.13 s, 0.5 s, 0.87 s: a **0.375 s dotted-quaver delay-like pulse** against the 120 bpm bar (3+3+2 semiquaver feel). This is the likely reason the beat tracker locks to 161 bpm. Inference: a repeated plucked or delayed figure, not a tune. The exact contour I cannot recover. (M on timing, L on instrument or delay.)

**Does the figure develop?** Through the track it changes *register and density*, not notes: 0:00-0:28 sparse, long-held pad; 0:29-2:37 Em/G/D arpeggio (G/E/B/D tops) with the bass; 2:37-4:48 denser B-F#-D pulsing with B pedal. The bass is the "riff": see below. (M.)

**Bass as the melodic line.** From 0:29 the bass plays one sustained root per chord (YIN about 41 Hz E1, 49 Hz G1, 36.7 Hz D1 in win_0020, i.e. likely sub-octave or low-octave notes; I did not re-measure the octave). Between chords it sometimes approaches chromatically: win_0100 reports A2-C3-B2-A#2 slides at 1:54.4-1:55.4 into the B, and G2-A2-C#2 climbs into D at 1:47.8-1:48.9 (these were in the "lead" file; the vocal stem was silent, so they are bass bleed). In win_0060 the bass alternates B2 and G2 at 0.5-0.7 s steps at 1:12-1:19, a rocking figure (L-M, bleed-derived). In the final groove (4:40-5:00) the bass is sparse short punches on B (win_0300 note). The "melody" is therefore the bass motion E-G-D-B then B-A-D, a three- or four-note descending-ascending contour. (M.)

## 5. Where I disagree with, or refine, the window notes

1. **161 bpm and "10-11 beats per chord" (win_0060, 0120, 0180, 0240).** Wrong grid. Tempo is 120 bpm; a chord is 8 beats = 2 bars. (H; drum autocorrelation at 0.5 s and 4.0 s.)
2. **win_0160 and win_0180 describe "Bm - D alternation", i-III.** The bass shows a three-chord loop B-A-D, with the A bar read as "A over B" in chroma. The cycle is 12 s, not an 8 s alternation. (H for bass roots.)
3. **win_0080 reads the 1:20-1:29 section as a long Em.** The bass root there is B (1:20-1:25) then silence; the upper layer has Em/B. I would call it a B-bass bar with a break, rather than an Em pedal. (M.)
4. **win_0280 "static Bm plateau 4:48-5:00 with bass punches".** The bass stem is silent from 4:49 ([RMS]), so the plateau is pad-only; the "bass punch" language in win_0300 refers to 4:40-4:48. Check: [RMS] bass is 0.145-0.179 until 4:48 and 0.000-0.001 after. (H.)
5. **win_0000 reads 0:00-0:08 as "Bm with flat sixth G" and the "B2/G2 lead" as a possible low-register movement.** Bass stem is silent in 0:00-0:28, so B2/G2 there are not bass notes; they are bleed. (H.)
6. **win_0020 reads Em from 0:20 to 0:32 with bass E at 0:28-0:32.** Agree for 0:28 onwards; the first bass note is at 0:29. (H.)

## 6. Limits

- Chroma cannot separate chord quality when a pedal is present: Bm vs Bm7 vs Bsus vs D/B are all one cloud (B, D, F#, A).
- I cannot identify the instruments (guitar, synth, or sampled?) playing the arpeggio, or confirm delay vs played rhythm.
- The bass-stem octave was not re-measured; I trust pitch classes only.
- The "B" bar in Loop A (0:52, 1:20, 1:53, 2:21, 2:37) could be B major, Bm, Bsus or Em/B; not resolved.
- Lead pitch data is not melody. Narration pitch (D3-A#5 range) is speech inflection.

## 7. Three questions for fellow specialists

1. **RHYTHM:** Can you confirm the 120 bpm half-grid and say what the 0.375 s (dotted-quaver, 3+3+2) pulse in the "other" stem is: a delay/echo, an arpeggiator, or a played pattern? Does the 0.375 s pulse appear in drums or bass stems as well, and where does it enter and leave?
2. **SOUND:** In 0:00-0:28 (no bass stem), which instrument carries the pad and the G4/E4 and G4/D5 pulses: bowed or sustained synth, organ, or guitar with a volume swell? What changes in the "other" stem at 0:29 (bass entry) and at about 1:25-1:29 (the break)?
3. **FORM (with VOICE):** The harmony changes loop type at 2:37 (Em-G-D-B to B-A-D) and the bass leaves at 4:49. Does the narration (voice) align with those two boundaries and with the 1:20-1:29 break? If the voice enters on chord boundaries (win_0140 reports bursts at 2:24.7, 2:28.5, 2:32.5, 2:36), is the loop switch at 2:37 a deliberate "new part" under the speech?

(Also for FEELING and LINEAGE, shorter: does the B-pedal drone plus rising-third lifts (Em to G, A to D) read as hopeful or elegiac to you, and is this modal, drone-over-arpeggio approach a known PSB or post-rock/krautrock device?)
