# t_cshells_cshore: HARMONY specialist, round 2 (blind, measurement-only)

Read: all seven round_1 files. New measurements: `v1/scripts/agents/harmony_r2.py` (third-vs-fifth test in the "other" stem with a 36-bins-per-octave CQT summed over four octaves; pYIN pitch-class counts and tuning of the bass stem per 20 s block; chord-change timing against "other" onsets). Tags: measured / INFERRED, with confidence. Where I carry a round-1 claim, its tag is kept unless stated.

## 1. Answers to questions put to me

**Form Q1 and Lineage Q2 / Feeling Q1: is the third present, and what is the mode?**
- Bass stem: the third is absent. pYIN pitch-class counts (confidence above 0.5) over 2:00-3:20: A 31/38, 25/29, 32/46, 15/23; G is the only other class with real counts (3, 1, 12, 8); C and C# give 0 in every block, and E 2-3. At 5:00-5:22: A 34, G 10, nothing else. Measured, high. Lineage's own count (A 458, G 154, C about 20) agrees.
- "Other" stem, dB relative to A (summed A, then the pitch class over four octaves): E is the strongest non-A class in every section (-14 dB at 0:25-0:32, -10 at 1:05-2:20, -8 at 2:20-3:20, -4 at 3:20-4:00, -6 at 4:00-4:40, -1 at 4:40-5:20, -5 at 5:25-5:40). G is second at times (-6 at 4:00-4:40 against E -6; -11 to -16 elsewhere). The third is weak and undecided: C# against C is -13/-18 (2:20-3:20), -8/-11 (3:20-4:00), -11/-17 (4:00-4:40), -8/-12 (4:40-5:20): the **major third (C#) leads the minor third (C) by 4-6 dB in four of six body sections**, but sits 8-13 dB below A and 5-12 dB below E, and C leads only at 1:05-1:40 (about -13 against -13, a tie) and in the 0:25-0:32 drone (C -15, C# -27). Measured, medium. Note two overtone facts: C# is the 5th partial of A and G the 7th partial (about 31 cents flat of equal-tempered G), so a distorted or saturated A tone alone would put both C# and a flat G into the chroma without any player choosing them. That is a plausible alternative to "G is a chord tone". INFERRED, medium-low; I cannot separate a played G from a partial 7.
- Verdict: the harmony is **A with a fifth (E), a flat seven (G) and an undecided, mostly masked third**. If a third is heard in the loud body it leans major (C# ahead of C by 4-6 dB), which matches Lineage's key-slice note that A major edges A minor from 3:30 to 5:30 (A major slightly ahead there per summary.json as Lineage quotes it; I did not re-read it). So "A Mixolydian-leaning, with an Aeolian/minor flavour only early (F/Am/Dm 0:39-0:59 and A minor 0.87 at 5:30 on)" is a better statement than my round-1 "neither". Medium. Feeling Q1 answer: closer to Mixolydian/pentatonic-with-flat-seven than to Aeolian, because there is no measured minor sixth in the bass (F: 0 counts) and the F labels are 0:39-0:59 and 1:33 only.
- F and Dm labels are not partial artefacts of the drone at 0:39-0:59: that region has no drums or bass to confuse them and the "other" chroma shows F 0.37 (round 1). They are real but weak (low-medium); in the loud body they are mostly fill smear.

**Form Q1 second half: is the A-G swing at 4:00-4:40 a section, and are the F#m/D lifts at 2:07.5 and 2:38 sections?**
- A-G at 4:00-4:40 is a genuine harmonic event but not a new harmonic world. In chords.json share: 4:00-4:40 A 46%, G 33%, F#m 5%, Am 4%, Dm 4%, Em 2%, 31 label changes; 3:20-3:45 A 45%, G 19%, Em 12%, N 8%, Dm 6%, D 4%, 24 changes. So G rises from 19% to 33% and the stray Em/D/Dm labels shrink. **The bass stem is what changes most**: at 4:12-4:40 (the blocks I could track, 4:12-4:40 counts G 89, A 19 over 252-280 s) the bass is on G about 4.7 times as often as on A, whereas at 2:00-3:20 and 5:00-5:22 it is on A by 2-4 times as often as G. Correction to my round 1: I called this "A to G, I to bVII" with the chord labeller's A-first emphasis; the bass says that during 4:12-4:40 the low root is **G**, not A. Measured, medium-high (pYIN, bass stem, separator caveat). So Form can honestly give 4:12-4:40 a separate label on the grounds of the bass root moving to G (matching its own 4:11.5 boundary "bass returns, A-G swing", which was carried by the bass), but the "other" stem keeps A as top chroma class, so it is a change of bass root and colour rather than a key change.
- F#m/D at 2:07.5-2:21 and the walk at 2:38-2:42: no stem corroboration of an F#m third (F#m needs C# plus F#; F# is -15 to -19 dB in the "other" stem in all sections). I rate them passing colour, **not sections** (low). The chord labeller's F#m is most likely A plus a loud E and a smeared G/F# neighbour. Form should not use them as boundaries.

**Rhythm Q1: do chord changes land on the stab attacks (1:24.9, 1:28.9, 1:33.0)?**
- Chord labeller changes in 1:00-2:00: 60 changes, on a 0.5 s-ish raster. Against the 21 onsets in the "other" stem, 17 of 60 changes fall within 0.15 s of an onset (28%), median distance 0.52 s. For scale: 21 onsets with a 0.3 s window in 60 s is about 10% by chance, so there is a **weak real alignment**: the changes that line up are the stab attacks (60.8, 64.3-64.8, 80.8, 82.8, 88.9, 97.0, 113.4 s) and between them the labels flicker with no onset. Chord changes are therefore best read as stab-attack changes plus noise. Grid: onsets from the "other" stem, chord times from chords.json, no beat grid claimed; the 4 s spacing (about 8 beats at 123 BPM, 3.9 s) is the rhythm specialist's. Medium-low.
- Does the harmonic rate drift with the tempo? The label rate is set by the labeller's own frame (about 0.5 s), so I cannot show harmonic drift; low.

**Sound Q1 (via Voice/Sound): is the 10-25 cent flat tuning meaningful?** New: bass tuning offsets (median cents from the nearest semitone over 20 s blocks): -22 at 2:00-3:20 (all four blocks), -2 at 3:20-3:45, -2 at 4:12-4:40, -12 at 5:00-5:22. The earlier "G# bass" reading is therefore **confirmed as flat A** (-22 cents, stable across 80 s) and not G#. The offset then moves to near 0 after about 3:20 and sags again by 5:00. Measured (pYIN, bass stem), medium. A sample/tape source or a detuned bass that is later re-tuned or pitch-drifted could produce this, so the figure is mild support for non-DAW-locked pitch (INFERRED, low-medium). It cannot, alone, say "old source". The final pad (-23, -11, -5 cents across partials, round 1) is not consistent with one constant offset either (the offset falls toward higher partials): possible stretched or inharmonic partials; INFERRED, low.

## 2. Corrections to my round 1 and to colleagues
1. My round 1 said the bass sits on A at 4:12-4:19 "G2 to A1 to G1"; the 20-40 s block count shows G dominant in 4:12-4:40 (section 1 above). I now give G as the main low root there. Revised tag: medium-high.
2. Round 1 said "no third present". Corrected: the third is not absent in the "other" stem; it is weak, and leaning major (C# 4-6 dB over C) in the body. It is absent from the bass stem. Tag: medium.
3. Voice and Form list lead-pitch values (E3, C#3, D#3, F3, F#3 at 4:56-4:58; F5 at 3:44-3:50). I keep my round-1 verdict: these trackers read bass/pad or noise, not melody. Voice's "stable voiced frames, f0 median 165 Hz (E3) at 4:56-4:58" fits an E (fifth of A) at the right octave for a male speaking voice, so it may be real speech on E; it is not a sung melody (semitone steps, 35 dB under the mix). I accept that as the one candidate pitched vocal event; low.
4. Sound says the sample peak is near 0 dBFS and Form says the loud plateau runs 2:00-5:30; neither contradicts harmony. The slow harmonic rhythm (one chord per 2-4 s over a loud plateau) is the reason "drama is texture": agreed.

## 3. How harmony serves the other areas
- **Rhythm and form**: the harmony hardly changes, so the 4 s stab cycle (1:00-1:40) is the only "phrase" and it carries a static A. Every long-scale harmonic change I can show is a bass-root event: A pedal (2:00-3:20), A on a flat bass (-22 cents) to a bass-in-tune A (about -2 cents) after 3:20, G-centred bass 4:12-4:40, A with E/G at 5:00-5:20 and the A-E pad. Those line up with Form's section edges (3:44-3:45 bass leaves; 4:11.5 bass returns). It is the **bass root and bass presence that give this track its form**, not chord progression.
- **Sound**: partial 7 (G) and partial 5 (C#) of a saturated A tone would explain much of the "other" chroma without extra notes; the "guitar-like" label (Lineage) is supportable only as "harmonically rich, distorted pitched layer" (INFERRED, low on identity).
- **Feeling**: bare fifth plus flat seven, and a third that is hidden, gives the unresolved, neither-bright-nor-sad colour that Feeling reports; the C# lean in the late body (3:20-5:20) would be the part that is slightly warmer; not audible to me, so it is metaphor-level (INFERRED, low).
- **Voice**: the E (fifth) pitch of the 4:56 voice-like event matches the harmony, but the level (about 35 dB under the mix) makes it texture, not melody.

## 4. Production-era evidence from harmony (rule 1)
Measured: bass stem offset -22 cents at 2:00-3:20 and about -2 cents at 3:20-4:40 (pYIN), final pad -23/-11/-5 cents. A mix with pitch offsets that vary by 20 cents across stems and time is not a plain DAW A=440 grid; mild evidence for played or sampled tonal material (INFERRED, low-medium). Other era figures (peak near 0 dBFS; kick spread; loop regularity) belong to Sound and Rhythm and I did not re-measure them. I do not see a band-limited harmonic layer under a full-range mix in my measures, so I make no "older source" claim from harmony.

## 5. Boundary table (rule 3), harmony-relevant boundaries, re-measured where stated
I re-measured only the bass stem (pitch class and tuning) around the boundaries below; drums, vocals and mix dB figures are carried from Form's round-1 table and the window notes.
| Boundary | drums | bass (re-measured) | vocals | other (re-measured) | carried by |
|---|---|---|---|---|---|
| about 3:20 (tuning step) | carried: present | median offset -22 to -2 cents; root A throughout | floor | E 4 dB nearer A | bass tuning only; not a Form boundary |
| 3:44-3:45.2 | carried: present | exits (round 1) | brief fragments | A+G stack continues | bass |
| 4:12-4:40 | carried: fills | root G 89 against A 19 (252-280 s) | floor | G -6, E -6 dB re A | bass root |
| 5:17-5:24 | out 5:17.1-5:18.9 | out 5:22.5-5:24.5; before: A 34, G 10 | flashes | A, E; E -1 dB | other holds the final A+E |
The last row is carried from round 1 for the exits; the pitch counts are new.

## 6. End of track (rule 4)
Not re-measured by me; carried from Sound's round-1 10 ms envelope work: last audible sound 5:42.8 (342.8 s), no final hits (10 shallow maxima at -47.5 to -58.3 dB, a fade, not hits). Pitch content of the last tone is A and E (round-1 FFT: 217.0, 437.3, 657.1, 875.6 Hz).

## 7. Two new questions
1. **Sound**: if the "other" layer is saturated, partial 5 (C#, about 14 dB below the fundamental in a pure harmonic series would be 14 dB; I measure -8 to -13 dB) and partial 7 (G) would appear without any chord tone being played. Can you measure harmonic ratios of the A drone at 0:25-0:32 (partials 2-8 against 1, in dB) to say how much of C# and G is overtone and how much separate note?
2. **Rhythm**: the bass tuning offset changes from -22 cents (2:00-3:20) to about -2 cents (3:20-4:40). Does the bass pulse, onset sharpness or swing change at about 3:20 too (for instance a different bass source or take), or is only the pitch different?

## 8. Not recoverable by measurement
- Whether the track is "A major" or "A minor": the third is hidden in the bass and weak in the "other" stem; the lean toward major (4-6 dB) is not strong enough to say what a listener hears.
- Whether G is a played note or the 7th overtone of a distorted A.
- The identity of the drone/pad/bass sound (organ, synth, guitar, sample).
- The meaning of the 20-cent bass offset (tape, detune, bend, separator).
- Whether the 4:56 voice fragment is on a deliberate E.
- Performer, date, intent.
