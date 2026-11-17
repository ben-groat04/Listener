# t_dl_mirror: RHYTHM specialist, round 3 (blind, measurements only)

Read all seven round-2 files. New scripts: `v1/scripts/agents/rhythm_r3_tdl.py`, `rhythm_r3_b.py`, `rhythm_r3_c.py`. Times m:ss. Tags: measured, INFERRED, speculative; confidence high/medium/low. Stems are demucs estimates.

## 1. Main correction: the tempo is about 94.7 BPM, not 94.0

Form (94.5 from the bass loop, 183 s baseline) asked me to re-measure on the longest baseline. I did, with the drum stem, and I concede.

- **Method (independent of any kick detector):** 10 ms drum-stem level in dB, 18 s windows, Pearson r, shift searched in 10 ms steps. Hook 1 (0:10.4) against hooks 2, 3 and 4: refined lags 60.79, 121.67, 182.46 s (r 0.63, 0.69, 0.67). Verse windows: 60.81, 60.85 and 121.66 s (r 0.67-0.75). So the repeat cycle is 60.82 s (60.79-60.85), with no accumulating error over three cycles (60.79, 60.84, 60.82 per cycle). Measured, high.
- **Converting to tempo:** 24 bars per cycle gives 2.534 s per bar = **94.73 BPM** (beat 0.6335 s, sixteenth 0.1584 s). The 4-bar loop is 10.137 s; the three hook lags are within 0.02 loops of 6, 12 and 18 loops. At 94.0 the cycle would be 61.3 s, and at 95.7 it would be 60.2 s: both are excluded by lags that the correlation resolves to about 0.05 s. The count of 24 bars is inherited from form; 23 or 25 bars would give about 98 or 90 BPM, which no beat evidence supports (tracker beat 0.627 s, round 1 beat 0.638 s). Medium-high, tolerance 94.4-94.8.
- **Why my round 1 and 2 said 94.0:** short-window (20 s) bar-lag autocorrelation and a kick-drift fit. The 4-bar lag inside verse 1 (35-70 s) comes out at 10.17 s (94.4 BPM), so short windows scatter by 0.3-0.5 per cent. More importantly, a fresh kick-band onset detector (35-130 Hz, 955 onsets between 0:30 and 3:35, inter-onset intervals 0.08-0.31 s, so it double-counts hats and bass) gives a bar-level phase concentration R of only 0.03-0.06 at every bar period from 2.48 to 2.62 s, which is chance. A kick-drift fit built on such a detector is not evidence. **I withdraw "94.0, high" and the 78 ms against 828 ms drift figure, and the "kick intervals held to 20 ms" statement.** Straight (unswung) sixteenths were measured from mid-band peak position in round 1 and are unaffected (medium).
- **Consequence for others:** use bar = 2.534 s. Form's 94.5 is inside my tolerance. The tracker's 0.627 s beat (95.7) is about 1 per cent fast. The kick-grid sync statistics anyone quotes should be named on this grid, and the kick detector's chance-level phase means no sync result against it is credible.

## 2. Answers to questions put to me

**Sound Q1: does the loop keep its phase across the 0:10.62 and 2:57.54 mutes, or does the cut remove time?** Method: drum-stem envelope in 3 s windows before the mute, just after, and 3.5 s after, each aligned to the same material one 4-bar loop (10.137 s) away. At 2:57.54, offsets against the loop reference: +0.02 s (before), -0.03 s (after), -0.06 s (3.5 s later), r 0.77-0.88; against two loops -0.03 and -0.05 s. At 0:10.62 (reference one loop later): -0.11 s before, -0.11 s after, -0.06 s later; two loops -0.09 and -0.11 s. The change across each mute is 0.05 s and 0.00 s, below the 0.1 s I would call a jump (a sixteenth is 0.158 s). **The loop runs on through both mutes: the cut silences the signal and does not remove time.** Measured, medium-high. The mix at 0:10.62 reaches about -69 dB for two 5 ms frames (about 10 ms) between neighbours at -12 and -5 dBFS; at 2:57.54 no frame of my 5 ms envelope falls below -12 dB, so the 20 ms mute sound reports is not visible at that resolution (resolution limit, not a contradiction).

**Form Q1: 94.0 or 94.5, and does the pattern restart at each hook start?** Section 1: 94.7 on the long baseline. The drum pattern repeats at integer loop multiples (6, 12 and 18 loops), so the pattern is in the same loop phase at each hook start (measured, medium-high). Whether a hook start is a bar-one downbeat I cannot say: my bar origin is arbitrary and the kick detector cannot fix the 3-2-3-2 phase.

**Voice Q2: is the 0.3-0.4 s per 24 bars a real tempo difference?** Yes; it was my bias: 60.82 s against my old 61.3 s. Form's 60.95 s and my 60.82 s differ by 0.13 s, inside the +/-0.2 s uncertainty of voice-derived hook starts.

**Feeling Q1: where do the voice re-entries 1:13.15, 2:14.0, 3:15.09 sit on the beat grid?** Using drum-aligned hook starts (10.4 + 60.82 k = 71.22, 132.04, 192.86 s) and the 0.6335 s beat: 1:13.15 is 1.93 s after, 3.05 beats; 2:14.0 is 1.96 s after, 3.09 beats; 3:15.09 is 2.23 s after, 3.52 beats. Two of three land within about 0.1 beat of a beat position, one on an off-beat eighth. Uncertainty 0.1-0.15 s (0.15-0.25 beat), because the hook starts are voice edges. A lean towards beat-aligned for two of three (INFERRED, low). The bass entries after gaps cluster at a late-bar pickup (17 of 26, round 2; medium-low). I keep that the gate-edge statistic is at chance (66-87 ms against 80 ms).

**Harmony and voice (side-steps):** my round 2 numbers stand (drums +2.5 to +3 dB at three of four side-steps; bass +12 and +6 dB at two). The first side-step falls 5.4-6.5 s into the hook (2.1-2.6 bars), the second at 15.2-16.8 s (6.0-6.6 bars): roughly bars 2 and 6 of an 8-bar hook, uncertainty about 0.25 bar (INFERRED, low).

## 3. Connections

- **Form:** one 24-bar clock of 60.82 s; hook 8 bars, verse 16. The drums change about 1.6 dB at section edges (round 2), so sections are bass and voice states over a constant loop.
- **Sound:** under the limiter (peak 0.00 dBFS, 21,079 samples at or above 0.999), every arrangement move is a subtraction; rhythmically the loop is unchanged, so the felt release is low-end density, not pulse.
- **Voice:** verse onsets 5.0-5.2 per second against 6.31 sixteenths per second at 94.7: free speech rhythm over a 16-step bar.
- **Feeling:** a continuous sixteenth hat comb with off-beat kicks gives the lean; the bass cycle supplies withdrawal and return.
- **Harmony and lineage:** chord moves on beats (one per 0.6335 s); straight sixteenths, 3-2-3-2 kick feel, no roll evidence: a break-based hip-hop reading (INFERRED, medium), not a sample identification.
- **Production era (rule 1):** modern limiting on a looped, DAW-style rhythm. Figures: peak 0.00 dBFS; 0.2 per cent of samples at or above 0.999; RMS about -10.5 dB; crest about 10.5 dB; four-bar waveform repeat r 0.75-0.85; mono and band-limited near 8-9 kHz so no full-band layer to compare. Kick onset spread is withdrawn as a figure (section 1). Whether the break is older material is not measurable. INFERRED, medium.
- **End of track (rule 4):** from my round 1 10 ms envelope: last audible sound 3:56.44 at about -57 dBFS, digital zero after about 3:56.67, decay about 7 s from 3:49.0, no distinct final hit. Measured, high.

## 4. Settled conclusions (5 bullets)

1. **About 94.7 BPM (94.4-94.8), 4/4, bar 2.534 s**, from whole-envelope repeat lags of 60.79, 121.67 and 182.46 s (24 bars per 60.82 s). Medium-high. This replaces my 94.0; the kick-onset fit was not valid.
2. **One drum loop (four bars, 10.14 s) with straight sixteenth hats and a 3-2-3-2 kick feel runs the whole song and keeps its phase through the mutes at 0:10.62 and 2:57.54** (offset change at most 0.05 s). Medium.
3. **Form is a bass-and-voice state over that loop:** 8-bar hooks (bass on 84-88 per cent), 16-bar verses (27-29 per cent), drums moving only about 1.6 dB. High for the percentages, medium-high for the bar counts.
4. **Grid sync is not demonstrable:** vocal gate edges sit at chance (66-87 ms against 80 ms) and my kick phase is at chance at bar level (R 0.03-0.06). I claim no cut, gap or entry is quantised.
5. **The pulse is the floor and the low end is the variable:** a hot, limited, mono, band-limited loop with no drift, acceleration or stop until the closing decay; release and return are bass events.

## Not recoverable by measurement

- **Drum source and hit identity:** sample, machine or kit; I separated bands, not instruments.
- **Exact entered tempo:** 94.4-94.8 is a spread of methods, not a click, and rests on the 24-bar count.
- **Whether hook starts are bar-one downbeats:** my bar origin is arbitrary and my kick detector is unreliable.
- **Whether gaps are edits, gates or performance, and the intent:** timing is at chance level.
- **Whether a listener feels 94 or half-time 47:** both are available.
- **Whether the loop is archive material, and its age:** the limiting and band limit fit a modern lo-fi workflow as well as an old source.
- **Whether bass gating is arrangement or a stem artefact:** the stems are estimates.
