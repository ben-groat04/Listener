# video1: harmony and melody specialist, round 2 (debate)

Evidence keys: [ch] chords.json; [af] audio_features/summary.json; [img NNNN] music_views/window_NNNNs.png; [R1-x] another specialist's round-1 file; [h2] v1/scripts/agents/harmony_r2.py, harmony_r2b.py, harmony_r2c.py (new this round: 3-bins-per-semitone CQT power chroma of the `other` stem, tuning-checked; FFT peak of the bass stem; pyin note sequence of `other`; chord-change phase histograms). I cannot hear; all is inferred. Times m:ss. Tempo 78.3 bpm: beat 0.77 s, 4 beats 3.07 s, 8 beats 6.1 s [af].

## 1. What changed since round 1 (short)
1. The third (F or F sharp) is **weak everywhere**, and F sharp slightly beats F. The D tonic plus open fifth is solid; major or minor is not decided by anything I can measure. (Answers Feeling.)
2. The 2:00 to 2:40 sub is **not F1**. It is a fixed 42.6 Hz tone, 42 cents flat of F1, identical at all six drops. It does not follow the chords. (Corrects my round 1 and answers Sound.)
3. The playing bass pedal is **D2 (about 73 Hz)**, not D1 (36.7 Hz). My round-1 pyin octave was wrong.
4. 1:15 to 1:40 is **not a chord loop**. The `other` stem plays a slow stepwise line (A, C, B, G, then D) with the tonic D almost absent for about 8 s. This is the track's nearest thing to a melody.
5. 2:12 to 2:33 is **A-centred** (A strongest in the `other` stem), not "Dm held". The chord walks start 2.2 s after each sub drop.

## 2. Answers to questions put to me

### 2.1 Feeling: is the third ever really present? (high on "weak", medium on the detail)
Power chroma of `other`, 3 bins per semitone, summed over octaves, normalised to the strongest class [h2]:

| Stretch | F | F sharp | Frames with F > F sharp | Strongest classes |
|---|---|---|---|---|
| 0:01 to 0:08 | 0.02 | 0.06 | 1% | D 1.00, A 0.38 |
| 0:20 to 0:40 | below 0.12 (not in top 8) | 0.15 | 18% | D 1.00, C 0.36, G 0.29, C# 0.29, A 0.23 |
| 1:00 to 1:15 | 0.14 | not in top 8 | 25% | D 1.00, A 0.40, C 0.33, B 0.32 |
| 1:27 to 1:40 | 0.16 | below 0.13 | 33% | D 1.00, C# 0.43, C 0.41, A 0.36 |
| 1:40 to 1:56 | 0.13 | 0.09 or lower | 51% | D 1.00, C 0.34, C# 0.34, A 0.30 |
| 2:49 to 3:08 | not in top 8 | not in top 8 | 23% | D 1.00, B 0.50, C 0.39, C# 0.27, D# 0.20 |

Reading: the third is never above about 0.16 in power (amplitude about 0.4). Only 1:40 to 1:56 is balanced between F and F sharp. This is a bare D5 wall. Note the scale: round 1 quoted F at 0.52 (0:40 to 1:00) from librosa chroma_cqt, which max-normalises each frame and so inflates weak classes. The two methods agree that the third is not dominant; this one is the more direct energy measure, so use this one.
- 0:20 to 0:40: the colour is C (flat seven) and G (the fourth), not a third. Cold and open.
- 1:27 to 1:40 ("yearning"): comes from texture and the line in 2.3 below, plus the mode-neutral flat seven. It does not come from a minor third. Feeling's reading (absence of bass, not harmony) is supported.
- 2:49 to 3:08 ("dark rim"): the extra darkness is chromatic neighbours around D (C, C sharp, D sharp, B, A sharp; see 2.4), not a minor third. So "dark" here is grit, not minor mode.

### 2.2 Sound: what is the 42.6 Hz sub harmonically? (high on the measurement, low on the interpretation)
FFT peak of the bass stem, 1.2 s window after each drop, 16x zero-padded [h2]: 42.60, 42.55, 42.60, 42.60, 42.60, 42.60 Hz at 2:01.1, 2:07.3, 2:13.4, 2:19.6, 2:25.7, 2:31.9. That is -42 cents against F1 (43.65 Hz). It is not a tuning offset: librosa tuning estimate of the track is +0.05 semitone (+5 cents) [h2], and the playing bass elsewhere sits within about 30 cents of D2 (72.0 to 74.3 Hz).
- It is a constant-pitch tone. It does not move while the guitars walk Am, D, G (2.5 below). So it is a pedal, not a bass line and not a chord root.
- Relative to D: 258 cents above D1, or about 2.6 semitones: between major second and minor third. Relative to E1 (41.2 Hz) it is 58 cents sharp. So it is about "F, a bit flat", but a listener will hear a weight, not a note. Under D it leans to a minor-third colour (Dm/F); under the A-centred guitars it would be a flat sixth; under G a flat seventh. Because it never moves, it grates mildly against some chords and not others, which is a plausible source of the "coiled" feeling Feeling reports, but I cannot prove the listener perceives it as pitch at 43 Hz.
- Round-1 correction: I wrote F1 (about 43.7 Hz) from pyin rounded to MIDI note numbers, which hides a 42-cent error. 42.6 Hz is the number.
- At 2:38.4 the pulse becomes 72.6 Hz, D2: the bass has returned to the D pedal (end of the sub section).
- After the drops the 2.6 s peak picks read 94 to 104 Hz at 2:19, 2:25 and 2:31 (about G2, F sharp 2 to G2). Peak picking over distorted-free bass, but low confidence on the note and no claim of a riff.

### 2.3 Form: the 1:15 to 1:40 passage (medium)
The `other` stem in 3 s slices [h2]: 1:15 A 1.00 (D 0.08); 1:18 C 1.00 (D absent from top 6); 1:21 B 1.00, G 0.47, F sharp 0.35; 1:24 D 1.00, C 0.88. pyin on `other`, per 0.5 s (rough, polyphonic, treat as a contour): A3 for about 3 s (1:17 to 1:19.5), C4 (1:19 to 1:22), B3 (1:22 to 1:24), G3 (1:24 to 1:25), then D3 and D4 (1:26 to 1:29), B2, A2, C3 (1:29 to 1:36) [h2].
- Contour: A up a minor third to C, semitone down to B, minor third down to G, then D: stepwise-to-leaping, with natural B and flat C. Against a D tonic that is fifth, flat seven, sixth, fourth, root: pure D Dorian or Mixolydian pitches, consistent with R1.
- The tonic D is nearly absent from the `other` stem between about 1:15 and 1:23 (D 0.08 to 0.26). It is the only stretch in the track where the pedal does not hold, and the bass is already out (1:15 to 1:40, [R1-feeling]). So the "no floor" feel is double: no bass note and no D in the guitars. This supports Feeling's "suspended" reading, and it is probably why [ch] flickers through F, Bm, A, Am here: labels on a line, not chords.
- For Form: my harmony boundaries are 1:15 (bass out, D leaves), about 1:24 (D returns, C is next), 1:40 (bass and full pedal back), 1:56, 2:12 and 2:36 to 2:38 (see below), 2:48. The 1:15 and 1:40 boundaries match the stem on/off structure, so I accept the stem-based sections as the right frame for harmony, over the auto-segment points [af].

### 2.4 Lineage: what does the Am, D, G run at 2:00 to 2:30 do? (medium-low)
- Modulation: no. The bass returns to D2 at 2:38.4 and the 2:49 to 3:08 plateau is D again.
- Detector noise: partly. [ch] labels D and Dm are shaky, but A is genuinely strongest in `other` at 2:00, 2:12 to 2:29, 2:33 (A 1.00, D 0.33 to 0.91, G 0.27 to 0.52, E 0.30 to 0.38) [h2]. So this is a block that leans on A (the fifth of D, the minor v in Mixolydian), over the fixed sub. I read it as a hover on the dominant side of D, not a new key: a pedal turning away from the tonic, then at 2:36 to 2:39 D 1.00, G 0.97, C 0.96, F 0.79 (a quick return D, G, C, with F as the one place the third-ish F clearly appears for about 3 s) and finally D.
- Model for lineage: modal pedal, not "simply D major or minor". The evidence supports a Dorian or Mixolydian, power-chord, post-rock or motorik-adjacent reading (flat seven everywhere, no V to I, no third). I make no stylistic claim beyond that.

### 2.5 Rhythm: chord rate, 4 or 8 beats, and the 0:20 to 0:40 figure (medium-low)
- Over the whole track, [ch] has 125 chord changes after 0:01. Phase of the changes against the first sub drop: modulo 0.767 s they sit on the beat grid; modulo 3.07 s they use only four of eight bins, and beats 3 and 4 get 83 against 39 for beats 1 and 2 (about 2:1); modulo 6.14 s the histogram is flat (8 to 23 per bin, no peak) [h2]. So across the track there is **no 8-beat harmonic cycle**, and only a weak lean to the second half of a 4-beat bar. The label grid is the beat grid, so label timing mostly reflects the tracker.
- Inside 2:00 to 2:40 there **is** an 8-beat cycle: chord-walk blocks start at drop + 2.2 s (14.5, 20.66, 26.81, 32.96 s after the first drop, which is 6.15 s apart) and run about 3.8 s to the next drop, with a label every beat (0.77 s) [ch, h2]. So here the 8-beat phrase is: drop, about 3 beats of held sub and wall, then 5 one-beat chords, then the next drop.
- On the 78 vs 156 question: one chord per 0.77 s is a fast harmonic rate at 78 (a chord every beat) and an ordinary one at 156 (a chord every two beats). That mildly favours Rhythm's felt-156 reading. I give it low weight, since a guitarist riffing on a pedal does not care which tempo you call it.
- The 0:20 to 0:40 G flashes: autocorrelation of G chroma has a peak at 3.07 s (0.19, small) [h2]. That is a repeat on the one-bar (4-beat) cycle, matching Rhythm's hat rest cycle of 3.07 s. Weak, but the same period. The E chroma peak is at 0.46 s (0.22), not a bar.

## 3. Corrections
- **Mine, bass octave**: D pedal is D2 (72 to 74 Hz) not D1 [h2]. The F-sub claim is revised in 2.2.
- **Mine, "Dm held" at 2:00 to 2:15**: the `other` stem shows A and D, no third; Dm is a tracker label (see 2.4).
- **Mine, weak Aeolian hint**: B natural is stronger than A sharp in the 1:15 to 1:40 line (B3 sustained, A sharp only a 0.5 s glide at 1:15), so I drop the Aeolian hint. Dorian or Mixolydian remain, undecided by the missing third.
- **Mine, closing riff** (R1 5): the chromatic circling around D at 2:50 to 3:08 is not only vocal-stem bleed; pyin on `other` per 0.5 s gives C3 C3 B2 D3 D3 D3 C3 D3 A sharp 2 D3 D sharp 3 D3 C sharp 3 C3 and again C3 D3 C3 A sharp 2 D3 D sharp 3 C sharp 3 D3 C3 [h2]. D is the home, with both semitone neighbours (C sharp, D sharp) and C, B, A sharp below. Upgrade to medium: a gritty chromatic neighbour-note figure on a D pedal. Pitch accuracy of pyin on distortion is poor, so no exact notes.
- **Feeling R1**: "Am and D then C, Dm at 1:27" is [ch] label output; the underlying `other` content from 1:24 is D plus C (0.88), then D, C sharp, C at 1:33 (D 1.00, C sharp 0.66, C 0.46). I agree with the feeling but not with the chord names.
- **Sound R1**: it says chroma and chord labels call the sub passage "D/E". Chroma of the `other` stem is not reporting the sub (the sub lives in the bass stem), so this is leakage into the label; the F/E ambiguity is a property of a 42.6 Hz tone, not of the guitars.

## 4. Connections to the other specialists
- **Rhythm and harmony**: the only phrase-level structure is where the chords move on an 8-beat cycle locked to the sub drops (2:00 to 2:40). Everywhere else the harmony is static and the groove carries the form.
- **Sound and harmony**: the sound design decides the key feel. A clean fixed sine below a distorted open-fifth wall means nothing can establish major or minor; the track is "all weight, no third".
- **Form**: harmony changes at the stem boundaries, not at independent points. Texture drives form; harmony follows.
- **Feeling**: stern, not sad: no third, no V to I, flat seven. Lift comes from the tonic leaving (1:15 to 1:24) and from the A-centred walk (2:12 to 2:33); release comes from D returning with the bass (2:38.4).
- **Voice**: I could not find speech phrase ends tied to chord boundaries beyond what R1 noted (medium-low). Not re-checked this round.

## 5. What I still cannot say
Guitar or synth for the 1:15 to 1:40 line; exact riff notes; whether the 42.6 Hz tone is intended as a pitch; whether the 2:12 to 2:33 block is "Am" or "D over an A".

## 6. Two new questions
1. **To Sound:** the sub sits at a constant 42.6 Hz at all six drops, 42 cents under F1 and 58 cents over E1. Does its envelope or onset show a pitch glide, a click or a noise burst (which would make it a designed "impact" sample rather than a played note), and does the 1:15 to 1:40 stepwise line (A3, C4, B3, G3, D4, 220 to 520 Hz) have a plucked, bowed or organ-like attack in the `other` stem?
2. **To Rhythm:** the chord walks begin 2.2 s (about 3 beats) after every sub drop and then change every beat. What does the drum stem do at drop + 2.2 s (fill, accent, hat rest), and does the hat rest pattern change at that instant, so the walk might be a drum-led phrase rather than a guitar-led one?
