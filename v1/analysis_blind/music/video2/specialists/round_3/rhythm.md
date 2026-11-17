# video2: rhythm specialist, round 3 (blind, measurements only)

Evidence keys: [R2] my round-2 file; [F3] v1/scripts/agents/rhythm_v2_r3.py (coherence phase and beat folds, kick 30-150 Hz, snare 150 Hz-2 kHz from the drums stem); [F3b] rhythm_v2_r3b.py (peak-picked kick and snare onset times, 16 ms hop); [other specialists' round-2 files by name]. Times m:ss; file seconds in brackets where helpful. I cannot hear; everything is inferred from onsets.

## 1. A correction to my own round 2: the "re-phase" at 1:28.6 is a quaver, and it is the kick that moves

[F3b] Peak-picked kick onsets, taken modulo 0.5 s:
- 0:30-0:44: almost all at 0.37 s (30.37, 30.87, 31.87, 34.37, 38.87, 42.37, 43.87), with a few at 0.0/0.5 (31.5, 33.5, 38.5, 43.0).
- From 1:28.61: every one at 0.11-0.13 s (88.61, 89.12, 89.62 ... 95.61), and still at 0.12 at 2:30 and 4:57-5:00.
So the 0.5 s lattice is unchanged (120.0 BPM, as in [R2]), but the pre-1:28 kick mostly sits **0.25 s, one quaver, away from where the post-1:28 kick sits**. Mod 0.5 s one quaver later and one quaver earlier are the same thing. In my round 2 I called the shift "about a semiquaver, maybe an artefact of different patterns" and in round 1 "three semiquavers"; both were loose. The sharper statement (high confidence for the numbers, medium for the reading): **in 0:28-1:28 the kick mostly falls on the off-beat quaver; from 1:28.6 it falls on every beat.** The coherence phase in [F3] agrees (kick 0.05/0.05 in 0:30-1:10 against 0.39 from 1:28.6; snare 0.05 against 0.38; same sign convention, a quarter-beat apart for both bands).

This answers three questions put to me:
- **Feeling (is the kick on beat 1 at 1.125 s of the bar, and does the pre-1:28 phase differ by about 0.33 s, measured on the kick band?).** Measured on the kick band: the difference is 0.25 s (a quaver), not 0.33 s. Snare check [F3b] from 1:28.6: snare hits sit on the same 0.12 lattice, on alternate beats (89.13, 89.62, 90.13, 91.12 ...). Late in the piece the snare is on 298.12 and 299.12 only (1 s apart) with kicks between them. Which kick is "beat 1" is a convention I cannot fix from stems; what I can say is the snare takes every second beat, the voice call (below) falls on the other one.
- **Harmony (did the whole band move by a quaver, or only the bass line?).** The drum kit moved: kick off-beat before, on-beat after, with the grid itself fixed. A chord/bass arrival "about 0.25 s later" after 1:28.6 [harmony round 2] is exactly the size of the kick displacement, which supports a **whole-band quaver shift** (re-bar, or the kick moving to the beat while everything else stays) over "bass changed alone". It does not prove it: the 0.25 s is within the chord tracker's 0.37 s hop, and my bass-onset peak-picking [F3] is unusable (onsets at 102.0, 102.9, 104.4, 104.6 ... scatter over every phase of a 4 s cycle from either 88.61 or 0.14). So I **cannot answer harmony's earlier question about bass changes on 4 s multiples**. Low-medium.
- **Form (is the 1:24-1:28.6 hole a dropped beat or a 5/4 bar?).** [F3] kick/snare in 0.5 s bins: drum hits stop after the 83.5-84.0 bin and nothing registers from 84.0 until 88.5, and 88.61 is the first kick. That is about 4.6 s of silence, i.e. 9 beats plus one quaver (the last pre-hole hits are at the older 0.37 phase, the first post-hole hit at 0.12). So it is **neither a dropped beat nor a 5/4 bar**: the silence is not a whole number of bars (about 2.3 bars), and the extra quaver is the displacement above. I would call it "a gap that re-enters a quaver off the old phase", in other words the re-barring is built into the hole. Medium (the last pre-hole hit time is only good to my 0.5 s bin).

## 2. The final hits (Form's question)

[F3b] 4:57-5:00: kicks at 297.12, 298.62, 299.12, 300.10 (all on the 0.12 lattice); snare at 298.12, 299.12; then a kick at **302.34** (0.34 mod 0.5, so one quaver after a beat). Form reads the last three hits as 5:02.34, 5:02.60, 5:02.85. With the lattice at 302.12 and 302.62, those are: quaver after a beat, a beat, quaver after a beat. That is a syncopated **"and, beat, and"** figure, as Form proposes, and the stop at 5:00.86 (300.86 mod 0.5 = 0.36, again a quaver after a beat) is also an off-beat quaver. Medium: my onset picker finds only some of the end events (delta threshold), so I corroborate the timing arithmetic but not each hit. Pattern-wise it echoes the first half: the off-beat kick returns at the very end.

## 3. Other questions

**Voice call: which beat?** [F3] voice onsets 296.64 and 298.66 sit 0.03-0.05 s after the 88.61+2n lattice, so on a kick beat, once per bar. [F3b] the snare is at 298.12 and 299.12, i.e. calls land **0.5 s from the snare beats** on the beat that carries no snare. If the snare is the backbeat (2 and 4) the call is on 1 or 3, not "beat 2" as voice and feeling labelled it; if I label the snare beats 1 and 3 it is beat 2. Which is correct is a labelling question (I cannot see bar 1), but the objective statement is: **one call per bar, on a snare-free kick beat, opposite the backbeat**. That makes the voice a bar-marking accent. High for the geometry, low for the numbering.

**Lineage (is there a 16/32-bar super-structure?).** Fill times [R2] are 2:08, 2:24, 2:36, 2:48, 2:56: gaps 16, 12, 12, 8 s = 8, 6, 6, 4 bars. All whole bars (high), but not a regular 8/16/32 count. That suits a hand-built arrangement on a loop machine, where the arranger counts in 2-bar blocks and varies the run (4, 6, 8), more than a strict dance 16/32 lattice. I would drop my "8-bar default" wording; "multiples of 2 bars, mostly 6 or 8" is what the measurements support. Medium.

**Voice (speech not on the drum clock).** I accept it: the narration blocks have no bar phase, whereas the chops and the late call do. A free sample over a machine grid.

**Sound (single sample-like kick, identical each beat?)** I did not test the attack/decay shape. What I can say is that the kick onset phase is a constant 0.11-0.13 s from 1:28.6 to 5:00 [F3b], i.e. within a few ms, which fits a sequenced sample. Not tested: reverb/delay tails. The hat-delay test remains weak, as stated in [R2].

## 4. Connecting rhythm to the rest

- **Form.** The only true metric events are: grid start 0:28.1 (kick on the off-beat), the two stops (1:10.0-1:16.5; ~1:24-1:28.6) and the arrival at 1:28.6, where the kick moves a quaver onto the beat. Everything later is fills at 2-bar multiples and the final off-beat stop.
- **Feeling.** The release at 1:28.6 is a change from a leaning, off-beat kick (every hit lands "late") to an upright one. That is physically what "arriving" feels like, with no speed change. The stop before it removes the pulse for about 9 beats, so the return feels both expected and slightly "somewhere new".
- **Sound.** The kick is level and tightly timed; what grows is the top band of "other" (sound specialist), so the later excitement is timbral and not rhythmic.
- **Harmony.** The kick shift of 0.25 s matches the chord-arrival delay harmony reports, which is a reason to treat both as one re-barring event, with low-medium confidence.

## 5. Settled conclusions

- **Tempo: 120.0 BPM, 4/4, constant from 0:28 to the end.** The "160" in the tracker is the 0.375 s hat cross-rhythm, and D&B is excluded by the snare on alternate beats. High.
- **1:28.6 is a pattern change, not a tempo drop:** kick from mostly off-beat quavers to every beat, snare on alternate beats, grid unchanged. The kick moves by exactly one quaver (0.25 s). The preceding ~4.6 s silence is not a whole number of bars; it carries the shift. High for the measurement, medium for "re-barring".
- **Machine feel:** kick phase is steady to a few ms over 3.5 minutes, so the drums are sequenced or looped. High; sound identity unknown.
- **Voice and rhythm:** speech is free of the grid; the chops and the final 4:46-5:00 calls are on it, one per bar on the snare-free kick beat. The numbering (beat 1 or 2) is not determinable. Medium.
- **Structure and ending:** fills fall at 2-bar multiples (8, 6, 6, 4 bars), not a strict 16/32 plan. The final stop (5:00.86) and the last figure (5:02.34, 5:02.60, 5:02.85) are off-beat quavers, "and, beat, and". Medium.
