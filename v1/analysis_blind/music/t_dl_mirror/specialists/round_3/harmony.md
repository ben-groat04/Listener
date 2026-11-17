# t_dl_mirror: HARMONY specialist, round 3 (blind, final)

Read: all seven round-2 files. New run: `v1/scripts/agents/harmony_r3_tdl.py` (FFT peak at partial positions in the other stem, pyin at about 50 ms on the vocal stem around the hook-4 walks, bass-stem peak frequency at 0.25 s, band shares). Times m:ss. Stems are demucs estimates; all chroma and pyin figures are crude. Tuning offset of +0.0081 (13-14 cents) applied to the bed positions.

## 1. Answers to questions put to me

**Sound Q: does the F5 position (698 Hz) carry energy in the bed, and does the D/Dm flip track it? (measured, medium)**
Levels re the D5 partial (587 Hz) in the other stem, same-window FFT, so window length cancels:

| window | F5 698 re D5 | F#5 740 re D5 |
|---|---|---|
| verse 0:40-1:10 | -26 dB | -14 dB |
| verse 2:40-3:10 | -23 dB | -5 dB |
| hook 1 non-walk 0:20-0:25 | -24 dB | -17 dB |
| hook 4 non-walk 3:14.5-3:18.5 | -28 dB | -17 dB |
| walk 3:19.1-3:22.3 | -19 dB | -21 dB |
| walk 3:28.8-3:31.9 | -20 dB | -33 dB |

F5 in the drone is 23-28 dB under D5 in verses and in hook non-walk stretches: effectively absent. It rises only inside the walks (5-8 dB more), where F is a bass and bed note. So the drone itself carries no minor third; "D minor" is a statement about the voice's F and the walk's F, not about the bed. The labeller's Dm flicker is not supported by a real 698 Hz component. I accept sound's partial-series reading and drop "the F# over F in the bed" as a clue either way. Tag: drone thirdless, INFERRED, medium-high.

**Voice Q1: does the walk start on "in my" or on "morning"? (measured to 0.25-0.5 s, low-medium)**
Hook 4, first walk: the sung line begins at about 3:18.0 (pyin voiced from 3:17.9, on G4). The bass stem's peak frequency drops from D-region to about 50 Hz (G1, with a sharp offset) at **3:18.75** (earlier than my 0.63 s chroma grid gave: 3:19.13). Then about 3:20.0-3:20.25 it moves to 84-96 Hz (G2/F2 region), about 3:21.75 to 66-68 Hz (C2), 3:22.25 to 73-75 Hz (D2). Second walk: G1 from 3:29.0, 100 Hz (G2) at 3:29.75, 78-101 then 89 Hz (F2) from 3:30.5-3:31.5, C2 66 Hz at 3:31.75, D2 74 Hz at 3:32.25. So the first bass step starts about 0.75-1.0 s after the voiced line begins, i.e. within the first words, well before "morning" (which falls near the end of the walk). The step is on the line, not tied to the last word (INFERRED, low-medium; ASR word times not used; octave labels are folding-prone).

**Voice Q1b: does the sung F4 sit on the G chord (clash) or the F chord (chord tone)? (measured pyin, medium-low)**
Voice notes against the bass step in hook 4 walk 1: G4 3:18.0-3:19.1 (and from 3:18.75 over the G bass: root); brief F4 at 3:18.5 and 3:19.2-3:19.35 (neighbour dips, over the G-bass start: a minor seventh, passing); A4 3:19.7-3:21.4 held about 1.7 s while the bass is on F (F2 from about 3:20.4-3:21.65): A is the major third of F, a chord tone; F4 at 3:21.5-3:21.9 as the bass reaches C: F over C is a fourth (suspension-like); then A4 again at 3:22.2-3:22.5 over D (the fifth) and F4 at 3:23.0-3:23.3 over D (the minor third, against the drone with no third). Second walk: G4 3:28.1-3:29.1, F4 3:28.7 brief, A4 3:29.9-3:30.5, F4 3:31.6-3:32.0, A4 and F4 again before the end. So the minor third F4 is not set over the G (it is a passing dip there); the long F notes land over C and D. The voice uses A, G and F as a three-note set that shifts its relation to the changing bass (root over G, third over F, fourth over C, fifth then third over D). The measured fact is the same contour in both walks: G, A, F, A, F (INFERRED, medium; pyin on a processed voice, octave and neighbour errors visible: stray B4, C#5, D#5 values are tracker artefacts, ignored).

**Lineage Q1: is the bass a sine-like sub? (partial, low)**
Bass-stem energy above 100 Hz is 5 dB higher than below 100 Hz over 3:14-3:30 (hook with walks). Either the stem is not a sine sub (harmonics, a mid-bass) or separation leaks drums/bed. I cannot tell which. The peak-frequency tracks in the 70-100 Hz range could be the second harmonic of the 37-50 Hz fundamental, so octave labels (D1 or D2, G1 or G2) are unsafe. Same-source with the bed is therefore still open.

**Lineage Q2 / Form: is a hook "statement, answer, answer without walk"? (measured on step times, medium)**
Walk starts in hook 4: 3:18.75 and 3:29.0 (+5.0 and +15.3 s from a hook start of 3:13.1 on the voice's pattern, form's start 3:14.4 gives +4.4 and +14.6). They are 10.25 s apart: the 10.2 s loop. A hook is about 20 s: two 10.2 s loops, each holding a walk at its start. So the hook is "walk, rest, walk, rest" on the 10.2 s loop rather than a statement-answer-answer. Verses carry no walk: the 10.2 s bass/bed loop only moves in hooks.

## 2. Corrections and connections

- **Retraction of G major as the better reading (my round 2).** The B-over-Bb argument rests on 0.45-0.60 against 0.27-0.36 in a smearing chroma. With bass G1 clean at the start of the step and the voice on G4 with no B in its stable notes (B4 appears once at 3:18.4 and 3:28.6 as a one-frame blip), the G chord's third is undetermined. I lower "G major, medium-low" to **low** and "natural minor" stays low. The mode of the whole piece: D tonic, minor third only from voice F and walk F, so **D minor or Dorian-flavoured, low-medium**; the G-F-C-D walk is iv, bIII, bVII, i regardless of the G's quality.
- **Form.** I agree the walk marks the 10.2 s loop and carries no boundary. New: the bass step is a better clock than the chroma labeller (about 0.4 s earlier). Use the bass-stem step times 3:18.75 and 3:29.0 for the loop start in hook 4.
- **Rhythm.** The walk's 3 s (1.2 bars at 94 BPM, 4.7 beats) with steps at 3:18.75, about 3:20.1, about 3:21.7, about 3:22.25 are not even beat multiples (beat 0.638 s: gaps 1.35, 1.6, 0.55 s are 2.1, 2.5, 0.9 beats). Rhythm's "one chord per beat" is therefore too regular; the walk is irregular, 2-2.5 beat chords and a short D arrival (low-medium; 0.25 s resolution).
- **Voice.** The voice leads the harmony by about 0.75-1.0 s each time, so the chord change is a bass-and-bed event under a sung phrase that already began. Voice's F4 fraction (15-17 %) is mostly over the C and D stages, not over the G.
- **Feeling.** Feeling's "single glance sideways" stands. Add the cause: the voice rises to A over the F chord and then dips to F over D, so the "lift" is melodic (the A-over-F third) as well as bass-led. Feeling should keep "comforting after the first" (low).
- **Sound.** Dual-mono bed, 8 kHz ceiling, and my +14 cent bed offset with the voice about 14 cents under it are still unexplained; I do not raise it above low-medium.

## 3. Evidence rules (carried and updated)
- **Production era (INFERRED, medium-high: modern limited master; bed origin unknown, low).** Sample peak 1.000, mix RMS about -10 dBFS, crest about 10.7 dB (round 1); 10.2 s chroma lag r about 0.92 and the exact same walk shape in all four hooks (loop-machine regularity); kick spread 43-45 ms rms on a 16th grid (rhythm); band-limited 8 kHz ceiling common to every stem (sound), so no layer reads as older than another. Tags carried unchanged.
- **End of track (carried from round 2, 10 ms envelope, `audio/song.wav`, 239.44 s).** Last frame above -60 dBFS at 3:56.44 (-57 dB); mix -27.2 dB at 3:50-3:52 decaying about 3 s from 3:53.6 (-30.5 dB) to -52 dB; digital zero after about 3:56.7. No single final hit and a hit count is not recoverable from the 10 ms peaks (many small 3 dB peaks are drum and bed flutter). Chroma from 3:45 to 3:55: D 1.00, A 0.96: the track ends on the D+A drone, no cadence.
- **Boundary table (new, step starts).**

| boundary | drums | bass | vocals | other | carried by |
|---|---|---|---|---|---|
| 3:18.75 (walk 1 start) | +0.9 dB to unchanged | D-region to about 50 Hz (G1) | on G4 since 3:18.0, no step | G enters, D stays | bass pitch |
| 3:29.0 (walk 2 start) | small | G1 then G2 | G4 since 3:28.1 | G, C, F rows | bass pitch |
| 3:22.25 (return to D) | small | to 74 Hz (D2) | A4 | A and D | bass and bed together |

  Mix level moves under 0.7 dB at each: not a silence, a pitch event.
- **Sync statistics:** none claimed. Step times are 0.25 s steps against the 10.2 s loop (about 94.5 BPM from the bass loop, form), not a kick-grid statistic.
- **Emotive nouns:** none used except as metaphor; "walk" is a pitch descriptor.

## 4. Settled conclusions (5 bullets)
- **Tonic and mode: D, high; minor or Dorian, low-medium.** The bed is a thirdless D+A drone (F5 23-28 dB under D5 in verses and in hook non-walk stretches, measured); the minor third appears only in the voice's F4 and in the walk's F (INFERRED, medium).
- **The only chord movement is the hook walk: bass G - F - C - D (iv, bIII, bVII, i) over a D pedal, twice per hook, eight times in the song,** starting at the head of each 10.2 s loop, about 3 s long, absent in verses (high on shape, medium on roots, octave unknown).
- **The voice is a three-note melody (G4, A4, F4, centre A4 at about A440) that shifts its relation to the changing bass (root, third, fourth, fifth/minor third) and leads the bass step by 0.75-1.0 s** (INFERRED, medium-low); verse voice is near-monotone speech pitch at A#3.
- **The walk is irregular in time (2-2.5 beat chords), not one chord per beat, and the voice runs ahead of it, so harmony is tied to the 10.2 s loop and the bar rather than the syllable** (INFERRED, low-medium).
- **The track ends on held D+A with a 3 s decay and no cadence; modern limited master (INFERRED, medium-high); the G chord's quality, the 14-cent offset between bed and voice, and the bass octave stay open.**

## Not recoverable by measurement
- Instrument or synth identity for bed and bass: chroma and pitch tracks give pitch, not timbre.
- Whether the G is major or minor: stem chroma and a few weak B/Bb readings do not settle it.
- Octave of the bass notes: the 37-50 Hz fundamentals and 74-100 Hz harmonics cannot be separated reliably.
- Whether the 14-cent gap (bed sharp of voice) is sourcing, speed or tracker offset.
- Performer's or producer's intent in the lyric-bass alignment; real chord names; recording date; the source of any sample.
