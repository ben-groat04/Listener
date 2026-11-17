# video1, RHYTHM specialist, round 1

Track: Public Service Broadcasting, "Elfstedentocht Part 1" (per context.md; this is a context claim, not something I measured). Duration 3:08.7 (188.66 s).
I cannot hear the audio. Everything below is from measurements. Evidence keys: [BT] audio_features/beat_times.json; [AFS] audio_features/summary.json; [LV] music_views/per_second_levels.json; [CH] chords.json; [WIN] my reading of win_*.md; [R1..R4] my scripts v1/scripts/agents/rhythm_r1.py, rhythm_r1b.py, rhythm_r1c.py, rhythm_r1d.py (drums stem stems_raw/htdemucs/song/drums.wav, librosa).

## 0. Verdict in five lines
1. The tracked pulse is a rock-solid **78 BPM** (period 0.766 s) for the whole track, no drift; the drums play a constant **0.19 s grid** (four per 78-BPM beat). High confidence on both numbers.
2. The octave question (78 with sixteenths, or 156 with eighths) cannot be settled by measurement. My best reading: **felt tempo about 156 BPM, 4/4, with a backbeat landing every 0.77 s**; the 78 BPM "beat" is the half-note/backbeat level, and also the harmonic rhythm. Medium confidence (about 60/40 over the 78-with-sixteenths reading).
3. The groove is a **continuous, gated, machine-tight hi-hat/snare comb with a syncopated, non-four-on-the-floor kick, repeating on a 3.07 s (one 78-BPM 4-beat bar) cycle**. Medium-high.
4. Nothing in the drums ever stops or fills until **one 0.4 s all-band cut at 2:47.8 to 2:48.2** and a ragged final-second cluster at about 3:06 to 3:08 before an abrupt end. High on the cut, medium on the fill.
5. All the energy variation is carried by the layers on top (bass, guitar-like "other", voice), not by the drum pattern, so the pulse reads as an engine that never changes gear. This is the main rhythmic "feeling" of the piece.

## 1. True tempo and the octave problem
**Measured facts**
- Beat tracker: 78.30 BPM global [AFS]; 218 beats from 0:00.95 to 2:47.97 [BT]. Inter-beat std 0.019 s; mean period per 30 s block 0.7686 to 0.7723 s (77.7 to 78.1 BPM) [R4]. Two tracker slips (a 0.93 s interval at 1:26.4 and 0.84 s at 2:47.1) are tracker noise, not tempo changes. No accelerations or ritardandi are measurable. High.
- The "local tempo percentiles" in [AFS] (10 %: 78, 50 %: 108, 90 %: 152) are not real tempo movement; they are the tracker/estimator hopping between octaves. The tempogram of the drum stem has two almost equal peaks, 78.3 (0.61) and 156.6 (0.58) [R2]. That is the textbook octave ambiguity.
- Drum-stem onset intervals: modes at 0.19 s (308 counts) and 0.17 s (243), then 0.37 to 0.39 s (about 160) [R3]. 0.19 s is exactly a quarter of 0.766 s. So the surface is 4 per beat at 78, or 2 per beat at 156.
- Per-20 s autocorrelation of drum onset strength: the strongest period is 0.766 s in every window from 0:20 onwards, and the 3.07 s (4-beat) lag stays 0.4 to 0.57 [R3]. In 0:00 to 0:20 the 1.53 s lag wins marginally (0.67 against 0.60 at 0.77 s), which fits a two-beat unit during the intro vamp. Medium.

**Resolving the octave (honest reasoning, not proof)**
- For 78 BPM as the quarter note: the drums would be playing constant sixteenth notes with a hat/snare accent on every quarter, at a slow ballad-like pace. The window notes lean this way ("sixteenths over a slow beat") [WIN 0000, 0020, 0100].
- For 156 BPM as the quarter note: the 0.19 s grid is eighth notes (the normal rock hat pattern); the strong hat/snare accents every 0.766 s are the **backbeat on 2 and 4**; the 4-beat 3.07 s cycle becomes two bars of 4/4 (or one bar of 8/8 with a 2-bar riff). Harmonic changes every 0.77 or 1.53 s [CH] become one chord per two beats / per bar, which is normal rock harmonic rhythm. A track at 156 with 2-beat chord changes is much more usual than a 78 BPM track with sixteenth-note drumming and a chord change on every sixteenth-quartet.
- Evidence of the accent hierarchy from my phase analysis [R1]: onsets in the snare (150 to 2500 Hz) and hat (6 to 11 kHz) bands cluster in four peaks per tracked beat, with the single strongest peak at the same position every 0.766 s (counts 206/185/139/127 for the four sixteenth positions in the mid band; 174/92/53/44 in the hat band) and the middle (eighth-note) position at about 0.5 relative strength. A strong every-0.77 s accent, medium at the 0.38 s, weak at the 0.19 s is the hierarchy of beats at 0.38 s with a backbeat every second beat. That favours 156.
- What a listener would clap or tap: probably either the 0.77 s accent (foot tapping the backbeat, "slow heavy") or the 0.38 s eighth. I would say a person who knows rock taps the 0.77 s as the "2 and 4", and walks to the 0.38 s. Confidence **medium**; I will call it "78 BPM pulse, felt as a 156 BPM rock drive" and ask the form specialist to look at bar counts.
- Cannot be decided: whether the sound designer meant a slow stately pulse (a 1963 winter march, heavy) or a rock sprint. The music does both at once, and that duality is part of the character.

## 2. Metre
- 4 beats at 78 BPM = 3.07 s is the strongest repeat unit in the drum-onset autocorrelation (value 0.59 for kick, 0.66 mid, 0.64 hat bands over the whole track) [R1]. So the cycle is 4/4. Nothing in the data suggests 3/4, 6/8, 5/4 or 7/8; no beat-interval disruption (all intervals 0.63 to 0.93 s, outliers are the two tracker slips) [R4]. High on duple metre; medium on whether the written bar is 3.07 s or 1.53 s.
- Triplet or swung feel: the phase histogram shows four evenly spaced peaks per beat at about 0.15, 0.40, 0.65, 0.90 of the tracked beat [R1] with no peak at 1/3 or 2/3 positions. The grid is straight, not shuffled. A note in win_0140 calls it a "driving shuffle"; I do not find evidence for swing. Medium-high.
- Note: the tracker's beat times sit about 0.15 of a beat (about 0.11 s) away from the drum-hit grid [R1], so [BT] is a good period estimate but its absolute alignment is not the downbeat. Do not use [BT] times as downbeat times to the nearest 0.1 s.

## 3. The drum pattern (what can and cannot be said)
**Constant layer: gated hat/snare comb.** Drums are never absent after 0:00.7 [R3: only 0:00.0 to 0:00.68 is below the stem median minus 14 dB]. Onset density per 10 s window is 3.4 to 5.0 per second, mostly 4.1 to 4.8 [R2]. Hat-band (6 to 11 kHz) energy relative to the low band changes by section (see section 4). High.

**Gated, dry feel.** Between hits, the drum stem and often the whole mix dips below -20 dB for 30 to 60 ms in a dense sequence, e.g. 1:15.7 to 1:26.7 and 1:58 to 2:13 [R3 first run]. Tight silences between hits mean the drums are short and dry or heavily gated/gated-reverb-free. A reverberant kit would not do this. I cannot say whether live or programmed. CLAP says "drum machine" at 0.9 to 1.0 for many windows [WIN] but that is a weak model; the regularity of the 0.19 s grid (0.17 to 0.21 s modal range) is the better indicator of machine-like or sequenced playing. Medium.

**Kick: syncopated, not four-on-the-floor.** Kick (40 to 120 Hz onset) profile over 16 sixteenth-note slots in a 4-beat cycle, aligned to the tracker (normalised): [0.93, 0.06, 1.0, 0.06, 0.84, 0.59, 0.06, 0.36, 0.99, 0.51, 0.21, 0.36, 0.85, 0.38, 0.64, 0.06] [R2]. Strong kicks on slots 0, 2, 4, 8, 12, weaker on 5, 9, 14, none on slots 1, 3, 6, 15. That is a pattern with clusters ("boom-boom, rest, boom, ..."), not an even four. The window note "mostly one kick per beat with extras" (win_0060) agrees. The slot numbering is relative to the tracker, so absolute bar position (which one is "1") is a **guess**: low confidence.

**Snare/hat: constant 16th comb, accent on the pulse.** Snare-region and hat-region profiles are almost identical to each other: peaks at slots 3, 7, 11, 15 (1.0, 0.9, 0.97 and 0.85 in the 1.5 to 5 kHz band) and 0.5 at the in-between eighths, 0.2 to 0.3 on the other sixteenths [R2]. With the tracker offset (section 2) slot 3 is essentially the beat itself. So the dominant accent is on every beat of the 78 grid, and the snare and hat cannot be told apart by this method (demucs places both in "drums"). Low-medium on "snare on every beat" (that would be unusual; more likely a backbeat on alternate beats plus bleed from hat and snare tails at the others: I cannot separate them).

**A 3.07 s breathing cycle in 0:33 to 2:34.** The drum stem drops about 14 dB below its median for 0.15 to 0.22 s in a repeating pattern: for example 0:33.08, 0:33.78 (gap 0.70), 0:36.10, 0:36.92, 0:39.16, 0:39.94, 0:42.24, ... then 3.0 to 3.1 s between pairs [R3]. These are rests in the hat pattern: two per bar, spaced 0.77 to 0.82 s apart, bar-repeating every 3.07 s. They appear in 0:33 to 1:04, 1:16 to 1:47, 1:56 to 2:14 and (more sparsely) 2:14 to 2:34, and are absent in the intro (0:01 to 0:33), at 1:05 to 1:15, at about 1:47 to 1:56, and from 2:34 to the end. That is a bar-level groove signature: the drummer or programmer drops the hats on two of the beats of each bar. Confidence medium-high on the measurement; medium on interpretation.

**Hats open up at section changes.** Share of drum-stem energy above 5 kHz is 0.8 to 1.2 % at 2:40 to 2:48 and 9 to 12 % at 2:48.4 to 3:00 [WIN 0160]; the same kind of brightening happens at 0:32 (centroid 1.5 to 3.0 kHz [WIN 0020]) and about 1:05 (+6 dB 5 to 10 kHz [WIN 0060]). I accept those figures as read from the window notes; I did not independently remeasure them. Medium.

## 4. Time map of rhythmic events
(All from [R*] unless noted. "Pulse" means the 78 BPM beat.)

| time | event | evidence | confidence |
|---|---|---|---|
| 0:00.0 to 0:00.7 | Single drum-led broadband hit, then near-silence (mix -180 dB at the first 0.36 s, drums -56 dB) | R3, [LV] | high |
| 0:00.95 | Pulse begins; first beat; drums continuous from here; "other" at about 1:01.3 s (0:01.3) | [BT], [LV] | high |
| 0:01 to 0:33 | Intro/narration section: dense, no hat rests, autocorrelation strongest at 1.53 s | R3 | medium |
| 0:32 | Narration ends, drums brighten (centroid 1.5 to 3.0 kHz), stereo width 0.35 to 0.55 | [WIN 0020], [LV] | high |
| 0:33 to 1:04 | Bar-cycle rests appear (3.07 s cycle) | R3 | med-high |
| 1:05 to 1:15 | No rests; hat band louder from 1:05; bass drops out at 1:15 while drums unchanged | R3, [WIN 0060] | medium |
| 1:15 to 1:27 | Rests return; very gated; bass absent; voice list | R3 | medium |
| 1:27 to 1:40 | Wall of "other"; drums unchanged; no rests until 1:28.4 and then resume | R3, [WIN 0080] | medium |
| 1:55 to 2:00 | Bass and guitar drop; drums exposed (a "break" by subtraction, not by stopping) | [WIN 0100], [LV] | medium |
| 1:58 to 2:13 | Rests of 0.14 s pair every beat or so; very sparse-looking | R3 first run | medium |
| 2:14 to 2:34 | Rests at about 3.07 s intervals again | R3 | medium |
| 2:47.8 to 2:48.2 | **All-band cut of about 0.4 s** (mix to about -22 dB); drum stem to -57 dB at 2:48.0 to 2:48.2. Aligned with the end of the final narration | [WIN 0160], R3 (167.80 to 168.20 s) | high |
| after 2:48 | Tracker has no beats; my phase test of drum hits relative to the old grid shows the 16th grid shifted by about 1/8 of a beat (hist peaks at 0.375, 0.625, 0.875 against 0.0, 0.25, 0.5, 0.75 before) and the IOI mode is 0.18 s not 0.19 | R4 | low-medium. It could be a tiny speed-up, a shifted re-entry (the loop re-triggered on a different offset), or simply noise from the brighter cymbal-led kit; I do not know |
| 3:06 to 3:08 | Denser, brighter cluster of hits (fill or cymbal wash) | [WIN 0180] | medium |
| 3:08.06 to 3:08.68 | Abrupt end: mix to -180 dB; drums to -64 dB | R3 | high |

## 5. How the pulse makes the music feel (interpretation, kept separate)
- **Relentlessness**: a 0.19 s grid that never rests for 3 minutes, level within about 2 dB, mix at -11 to -13 dBFS [LV, WIN]. The ear is given no breathing room. This is the "engine" feeling, also "sprint" and "marching in cold".
- **Duality of fast and slow**: the heavy 0.77 s accent (backbeat/pulse) over the rapid 0.19 s hat grid gives the sensation of a heavy walker with a pounding heart, or a skater whose strides (0.77 s) carry a fast cadence of poles and blades (0.19 s). That analogy is mine; no measurement establishes it, but it is consistent with the film subject (a 200 km skating race, per context.md).
- **Absence of change as drama**: because the drum pattern barely changes, listeners will read energy and emotion from the layers over it: bass swelling (0:03 to 0:20), bass vanishing (1:15 to 1:40, 1:55 to 2:00), the guitar wall at 1:27. The rhythm section is a fixed ground; the other layers breathe against it. Same logic as minimalist or motorik music.
- **The cut at 2:47.8 is the only real rest.** Half a beat of silence after a sample says "Elfstedentocht" ([WIN 0160]) is a theatrical gasp: the pulse has been unbroken for 2:47, so the hole is a shock; the return with a brighter hat gives a "second wind". The final cut at 3:08.06 is rawer: no decay, no ritardando.
- **No syncopation-induced swing**: the grid is straight; the syncopation is in the kick and in the guitar stabs [WIN 0020: repeating figure every 3 to 3.5 s], which lends a stiff, mechanical, determined character rather than a loose or groovy one. Mechanical, not dancing.

## 6. What the measurements cannot tell me
- Which of 78 or 156 a listener would call the tempo (section 1). Needs the harmony and feeling specialists' views of chord rate.
- Exact kick and snare positions, and which slot is beat 1. Demucs lumps hat and snare; the tracker is offset from the hits (about 0.11 s).
- Live vs programmed kit. The tight 0.19 s regularity and gating favour programmed or heavily edited, but a skilled drummer with a click and gating could produce the same.
- The tempo after 2:48 (tracker gives nothing; my IOI estimate 0.18 s is not reliable).
- Whether the shifted grid at 2:48 is real; I only have one 8-bin histogram on about 10 s of data.
- Window notes that say "the drums double at 1:50 to 1:55" or "more onsets at 5.1/s" are small differences (4.2 to 5.1 onsets/s). Onset counts are affected by bleed from other stems; I do not treat 10 % density shifts as a change in the pattern.

## 7. Corrections or disagreements with window notes
- Several windows describe the drum pattern as "sixteenth-note" without testing the octave; I argue (section 1) that eighths at 156 are at least as likely. Not a contradiction of the measurement, only of the label.
- win_0140 says "shuffle of eighths or sixteenths"; the phase test shows no swing.
- win_0100 says there are "no stops" and then calls the bass and guitar dropout a "break"; I agree it is a break by subtraction and not a drum stop. In my data the drums keep their gaps pattern.
- win_0180 says the tracker "lost the pulse once the pattern got busy". I suspect, rather, that the pattern re-aligned after the 2:48 cut and the new hat-led texture confused the beat tracker (section 4); I cannot prove it.

## 8. Questions for fellow specialists
1. **Harmony:** Chord changes in [CH] arrive on a 0.77 s or 1.53 s grid and the D pedal dominates. Do the chord changes cluster on every 4 beats (3.07 s, one bar of 78) or every 8 (6.1 s)? That would tell us whether the "bar" is 78-BPM or 156-BPM, which settles my octave problem. Do the guitar-like figures at 0:20 to 0:40 [WIN 0020, repeats every 3 to 3.5 s] land on the same 3.07 s cycle as the drum breathing pattern?
2. **Sound:** Can you tell whether the drum sound is a gated acoustic kit, a drum machine or a sample loop (e.g. from transient shape, tails, velocity variation in the drum stem)? In particular, does velocity vary between consecutive hats (human) or stay flat (machine)? And is the kick a synth or a real bass drum?
3. **Form:** Section boundaries from [AFS] (0:14.8, 1:06.4, 1:15.6, 1:27.9, 1:49.4, 1:58.7, 2:01.7, 2:14.1, 2:38.7) do not line up with the hat-rest cycle changes I found (0:33, 1:05, 1:15, 1:47 to 1:56, 2:34). Which boundary set do you trust, and can you count bars (in 3.07 s units) between your boundaries so we can see if the structure is a clean 4-, 8-, 16-bar phrase length? Is the 2:48 cut at a phrase boundary in bars?
