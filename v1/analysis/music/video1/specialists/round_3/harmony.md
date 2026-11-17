# video1: harmony and melody specialist, round 3 (final)

Evidence keys: [ch] chords.json; [h2] harmony_r2*.py (round 2); [h3] v1/scripts/agents/harmony_r3.py (new: 3-bin-per-semitone CQT power chroma and 4x zero-padded FFT peak on the `other`, `bass` and `vocals` stems over given windows); [R2-x] another specialist's round-2 file. I cannot hear; everything is inferred. Times m:ss.

## 1. Answers to questions put to me

### 1.1 Voice: is there a sustained D3 at 1:57.0-1:58.2, i.e. does the D pedal bleed into the vocal stem? (high)
[h3] over 1:57.0-1:58.2: the FFT peak is 150.0 Hz in **all three** stems (`other`, `bass`, `vocals`). Chroma is D 1.00 in each, with a D sharp neighbour (0.55 other, 0.42 bass, 0.36 vocals) because 150 Hz is about 35 cents above D3 (146.8 Hz), so it straddles the D and D sharp bins. Reading: one sustained tone near D3 is present in every stem, so your vocal-stem 150 Hz tone is the same event, not a vocal. Leakage confirmed: it is a D-pedal note (a little sharp of D3, about 35 cents; the playing bass elsewhere is near D2 at 72 to 74 Hz, so 150 Hz is its octave or a held guitar D). I cannot say whether it is the bass octave or a guitar; either way it is D.

### 1.2 Voice: the harmony under the 1:46.6-1:48.4 noise burst: real chord change or detector reaction? (medium)
[ch] labels Dm to 107.9, Cm 107.9-108.7 (1:47.9-1:48.7), D from 108.7. [h3] 1:46.6-1:48.4: `other` is D 1.00, F 0.39, G 0.21, C 0.20, D sharp 0.18; `bass` D 1.00, C 0.36, G 0.31, C sharp 0.23; `vocals` is a broad smear (G sharp 1.00, E 0.74, D 0.64...), i.e. noise, not a pitch. So the guitar and bass hold D underneath. "Cm" is a detector reaction: C and D sharp are weak (0.20, 0.18) and D stays strongest. The one real feature is F at 0.39, the highest third I have measured in the whole 1:40 to 1:56 block (previous: 0.13); a transient raising it briefly is plausible but a single 1.8 s window is not a chord. Verdict: not a genuine chord change; D pedal continues, with a flicker of F and C (flat seven) from the noise or a fill.

### 1.3 Questions I put to others (answers seen in round 2)
- Sound (R2 2.1): the sub is a triggered synthesised tone with a fall to pitch (20 to 110 ms rise, starts 120 to 200 cents high, settles 42.6 Hz). Accepted. It is a thump with a falling edge, not a played root. My "minor-third colour" for it is withdrawn as a perception claim: I keep only the measurement (42.6 Hz, fixed, 42 cents under F1), because a 43 Hz tone with this envelope will be felt as weight.
- Rhythm (R2 file is empty): my question on the drum stem at drop + 2.2 s is unanswered and I do not rely on it. Without it, the "walk is guitar-led" reading stays unproven; what is measured is only that the label changes start 2.2 s after each drop.

## 2. Corrections and connections
- **Form (bar grid):** Form places 2:48 grid-aligned but not bar-aligned (0.7 beat after the line). Harmony has no independent bar-level cycle (R2 2.5: no 8-beat harmonic peak over the track), so I cannot confirm or refute the bar grid from chords; I take Form's grid as the frame for harmony, and note that the only bar-locked harmony is the 2:00 to 2:40 block.
- **Feeling:** accept "wistful at most", and agree "stoic" is texture, not mode. I go further: the track's only melodic yearning is the 1:15 to 1:40 stepwise line (A, C, B, G, D over a missing tonic), so if a listener feels longing it is from that line and the withdrawn bass, not from any chord.
- **Lineage:** the "dark rim" and the one-beat riff at 2:50 to 3:08 (chromatic neighbours of D) match a grit-on-a-drone idea, but the pitch evidence is pyin on distortion, so no claim of a particular riff tradition.
- **Voice:** the 150 Hz common tone shows the D pedal is audible even in the vocal stem; any pitch the voice appears to have around 1:57 is therefore the band's D. No speech-to-chord alignment is claimed.
- **Self-check on an earlier claim:** in round 2 I called F sharp slightly stronger than F; the F in 1:46.6 to 1:48.4 above shows F can briefly lead. Net: the third is never stable either way.

## 3. Still unknown
Major or minor; guitar versus synth in the 1:15 to 1:40 line; exact riff notes; whether the 42.6 Hz tone is meant as a pitch; whether the 150 Hz tone is guitar or bass octave.

## 4. Settled conclusions (5 bullets)
- **Key and mode (high on D, low on mode):** D is the tonic throughout (D 1.00 in every window, D2 bass pedal), the fifth A and the flat seven C are always present, and the third (F or F sharp) never exceeds about 0.16 in power except one flicker (F 0.39 at 1:47). So it is a modal D5 power-chord world, Dorian or Mixolydian by pitch content, undecided by the missing third.
- **Almost no chord progression (medium-high):** over the track the harmony is a pedal, not a loop. [ch] shows 125 changes, but most are detector labels on a static D (e.g. the Cm at 1:48); no 8-beat harmonic cycle exists across the track. The one real moving harmony is 2:00 to 2:40: an A-centred walk (A, D, G, then D, G, C at 2:36) every 0.77 s starting 2.2 s after each sub drop, over a fixed 42.6 Hz sub.
- **The one melody (medium):** 1:15 to 1:40 is a slow stepwise line (A3, C4, B3, G3, then D) with the tonic nearly absent for about 8 s and no bass. This is the track's emotional high point for pitch content: suspended and yearning, and it is built from texture and line rather than a minor third.
- **The 42.6 Hz sub is a designed impact (medium-high on measurement, low on perception):** fixed pitch, 42 cents flat of F1, triggered with a fall to pitch, identical at six drops. It adds weight, not harmony; it bears against some chords more than others, but I cannot prove it is heard as a note.
- **The ending is a drone with a chromatic riff (medium):** 2:49 to 3:08 is D 1.00 with C, B, C sharp, D sharp neighbours (a gritty circling figure around D, pyin-approximate), not a cadence; no V to I appears anywhere. Resolution is textural (bass returns at 2:38, drums stop and restart at 2:48), not harmonic.
