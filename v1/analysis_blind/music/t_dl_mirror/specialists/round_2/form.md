# t_dl_mirror: FORM specialist, round 2 (blind, measurements only)

Read: all seven round-1 files and the four round-2 files already written (harmony, rhythm, sound, voice). New runs: `v1/scripts/agents/form_r2_tdl.py` (per-stem 10 ms envelopes, boundary table, bass-on share per section), `form_r2_b_tdl.py` (bass-loop clock fit); other checks were short inline runs on `audio/song.wav` and `stems_raw/htdemucs/song/{drums,bass,vocals,other}.wav` (mono downmix; the file is dual-mono). Times m:ss. Levels are dBFS (RMS of 10 ms frames, then averaged as power over the window). Stems are demucs estimates. Tags: measured / INFERRED, confidence high / medium / low.

## 1. What changed in my reading (headline)

1. **Hook and verse edges move to the voice's grid.** My round-1 hook 3 and hook 4 starts (2:14.0, 3:15.09) were the end of the first vocal hole, not the start of the hook phrase. The voice file is right: hook starts are 0:10.4, 1:11.3, 2:12.0, 3:13.1 and the first hole sits 0.5 to 1.9 s after each. I re-checked with 50 ms envelopes of the four stems around all four first holes (section 4). Measured, high.
2. **The "largest step, +11.1 dB at 3:15.09, only hook preceded by a near-void" claim is withdrawn.** The 0.25 s minimum of the mix inside the first hole is -22.1 dB (hook 1, 0:11.9), -21.4 (hook 2, 1:12.15), -21.9 (hook 3, 2:13.8) and -22.3 dB (hook 4, 3:14.8); at 50 ms the minima are -24.8, -25.1, -25.2, -25.3 dB. Over the whole hole the mix averages -14.0, -14.2, -12.8 and -11.9 dB, so hook 4's hole is the shallowest of the four, not the deepest. Hook 4's return is the same event as the others. Measured, high. My round-1 reading "hook 3/4 engineered as the biggest return" was wrong (I compared one 0.25 s window with the ceiling and took a repeated gesture as a unique one).
3. **Peak/climax.** With (2) gone, nothing measured makes hook 4 louder, higher or denser than hooks 1 to 3: bass-on share 84, 87, 87, 87 per cent; mix 10 s RMS -10.1, -10.4, -10.5, -10.4 dB; voice RMS -19.3, -20.0, -19.9, -20.2 dB (voice file); clipped samples are not concentrated there (sound file: 0:10-0:20 and 2:55-3:00). I lower "the last hook is the climax by arrangement" from INFERRED medium to **INFERRED low**; what remains is position (it is the last hook, followed by the only voiceless section) and the feeling that goes with an ending.
4. **Tempo is neither 95.7 nor 94.0 on the long baseline: 94.5 BPM (bar 2.540 s).** See section 3. INFERRED, medium; this settles my round-1 question to rhythm only partly (rhythm's 94.0 comes from 20 s windows, mine from 180 s).
5. **The 3:34.0 to 3:35.3 stretch is a 1.3 s thinning of all of drums, bass and voice**, not a clean voice cut; and the voice's last phrase edge is 3:33.5 to 3:34.0, so the voice file's "voice leaves at 3:34.7 to 3:35.3" is the fade tail (section 5). Measured, high.

## 2. Song map (corrected), in bars of 2.540 s (94.5 BPM)

Bar numbers count from 0:00 (bar 0), bar n starts at about 2.540 n - 0.05 s (the -0.05 s is the fitted offset from the first bass burst at 0:02.49, section 3). Edges are good to about +/-0.2 s (+/-0.1 bar).

| # | Section | Time | Bars (start, length) | Evidence | Conf. |
|---|---|---|---|---|---|
| 1 | Intro, voiceless | 0:00-0:10.4 | 0, 4.1 | vocal stem -68 dB; bass-on 25 per cent (one burst 0:02.5-0:05.9, then gap); drums -18.3, other -26.8 | high |
| 2 | Hook 1 | 0:10.4-0:30.4 | 4.1, 7.9 | voice +43.5 dB at 0:10.4 (1.5 s windows); bass-on 84 per cent; voice -19.3 dB | high |
| 3 | Verse 1 | 0:30.4-1:11.3 | 12.0, 16.0 | vocal +4.4 dB at 0:30.4; bass-on 29 per cent; voice active 97 per cent | high |
| 4 | Hook 2 | 1:11.3-1:31.4 | 28.1, 7.9 | first hole 1:11.9-1:13.0; bass-on 87 per cent | high |
| 5 | Verse 2 | 1:31.4-2:12.0 | 36.0, 16.0 | vocal +5.1 dB at 1:31.4; bass-on 28 per cent | high |
| 6 | Hook 3 | 2:12.0-2:32.4 | 52.0, 8.0 | first hole 2:12.8-2:13.9; bass-on 87 per cent | high |
| 7 | Verse 3 | 2:32.4-3:13.1 | 60.0, 16.0 | vocal +4.1 dB at 2:32.4; bass-on 27 per cent | high |
| 8 | Hook 4 | 3:13.1-3:33.5 (voice tail to 3:35.1) | 76.0, 8.0 | first hole 3:13.3-3:14.65; bass-on 87 per cent | high |
| 9 | Dissolve into outro | 3:34.0-3:35.8 | 84.1 to 84.9 | all of drums, bass, voice fall (section 5) | high |
| 10 | Instrumental outro (verse-state rhythm section, no voice) | 3:35.8-3:49.0 | 85, ~5.2 | bass back +10 dB at 3:35.8; drums -20.5, other -29 dB; bass-on 25 per cent | high |
| 11 | Dissolve / fade | 3:49.0-3:56.5 | 90, ~3 | mix -13.9 to -20.9 dB (+7 dB drop at 3:49.0), -54.8 dB in 3:56-3:57 | high |
| 12 | Digital zero | 3:56.67-3:59.44 | 93.1 | exact zero (section 6) | high |

Hook lengths 20.0, 20.1, 20.4, 20.4 s (7.9 to 8.0 bars); verses 40.9, 40.6, 40.7 s (15.9 to 16.0 bars). Hook starts 60.9, 60.7, 61.1 s apart (voice file) = 24 bars of 2.538 s. Order of sections in bars: 4 + 8 + 16 + 8 + 16 + 8 + 16 + 8 + about 9 (dissolve plus outro plus fade to 3:56.5) = about 93.

## 3. The tempo clock from the bass loop (new measurement, answers the rhythm/harmony tempo question)

The bass stem is an on/off pattern: in verses it plays one short burst (about 3.4 s, of four sub-hits) every 10.16 s. I took the first sub-hit of ten bursts (0:02.49, 0:42.91, 0:52.98, 1:03.29, 1:43.85, 1:53.87, 2:04.27, 2:44.87, 2:55.02, 3:05.27; 10 ms envelope above -40 dBFS) and fitted a line against burst number (0, 4, 5, 6, 10, 11, 12, 16, 17, 18): **period 10.158 s = four bars of 2.540 s = 94.50 BPM; residual std 0.10 s, max 0.19 s over 183 s.** The hook start times (10.4, 71.3, 132.0, 193.1) all sit at loop phase 8.04, 8.09, 7.79, 7.94 s (spread 0.3 s), i.e. one fixed place in the bass loop, six loops (24 bars, 60.95 s) apart. The long bass block always ends at loop phase 0.33 of a loop (0:36.16, 1:37.03, 2:38.08, 3:39.0: 3.33, 9.32, 15.33, 21.33 loops), including after hook 4.

Check on a different grid (rule 5): this is a bass-loop and section-spacing clock, not the kick grid. The rhythm specialist's drum bar-lag gives 94.0 BPM (bar 2.554 s) and the tracker 95.7 (2.51 s). At 2.554 s the verse starts fall at bars 11.9, 35.8, 59.7, 83.6 and hook starts at 4.07, 27.9, 51.7, 75.6, so edges drift to 0.3 to 0.4 bar off integer by bar 84; at 2.540 s they land at 12.0, 36.0, 60.0, 84.1 and 4.1, 28.1, 52.0, 76.0 (within 0.1 bar). At 2.51 s the drift is the other way (bar 85 = 213.4 s). INFERRED, medium: the arrangement runs on a 94.5 BPM clock; the 0.5 per cent gap to rhythm's 94.0 could be a window-length bias in a 20 s autocorrelation. Rhythm's bar lag over three-and-a-half minutes is "constant to 0.05 BPM", which does not conflict (constant at 94.0 and constant at 94.5 are both "constant"). I cannot settle which of the two is the kick's true rate; I only say the arrangement edges fit 94.5 best.

## 4. Boundary evidence table (all four stems re-measured by me, 10 ms RMS, mean level over 1.5 s before and after the time, dB; change in brackets)

| Boundary | Drums | Bass | Vocals | Other | Mix | Carried by |
|---|---|---|---|---|---|---|
| 0:10.4 intro to hook 1 | -17.0 > -15.2 (+1.8) | -51.7 > -21.8 (+29.9) | -68.4 > -24.8 (+43.5) | -27.8 > -23.0 (+4.9) | -11.8 > -9.3 (+2.5) | vocals, with bass; all four move |
| 0:30.4 hook 1 to verse 1 | -18.0 > -19.4 (-1.4) | -14.3 > -18.9 (-4.6) | -21.5 > -17.1 (+4.4) | -22.4 > -20.9 (+1.5) | -9.3 > -10.5 (-1.1) | vocals (level step up into rap) |
| 1:11.3 verse 1 to hook 2 | -17.7 > -18.8 (-1.1) | -32.4 > -18.8 (+13.7) | -15.4 > -24.2 (-8.8) | -29.9 > -25.0 (+4.9) | -9.9 > -11.6 (-1.7) | vocals (down 8.8 dB, register up) with bass entering |
| 1:31.4 hook 2 to verse 2 | -18.2 > -20.0 (-1.8) | -14.6 > -18.4 (-3.8) | -21.0 > -15.9 (+5.1) | -22.6 > -21.5 (+1.1) | -9.4 > -10.0 (-0.6) | vocals |
| 2:12.0 verse 2 to hook 3 | -17.8 > -19.2 (-1.5) | -37.5 > -17.2 (+20.3) | -19.4 > -22.0 (-2.6) | -28.7 > -27.1 (+1.6) | -11.2 > -11.7 (-0.5) | bass (re-entry) and vocal register |
| 2:32.4 hook 3 to verse 3 | -17.9 > -18.8 (-0.9) | -14.5 > -19.8 (-5.3) | -20.7 > -16.6 (+4.1) | -23.1 > -22.4 (+0.7) | -9.3 > -10.2 (-0.9) | vocals |
| 3:13.1 verse 3 to hook 4 | -17.7 > -18.0 (-0.3) | -49.4 > -19.9 (+29.5) | -17.3 > -24.4 (-7.1) | -28.5 > -23.4 (+5.1) | -10.6 > -11.3 (-0.6) | bass (returns after a 3.6 s absence) and vocals |
| 3:34.0 hook 4 thins | -16.7 > -19.2 (-2.5) (1.0 s windows) | -15.1 > -27.5 (-12.4) | -20.9 > -27.3 (-6.4) | -24.7 > -25.3 (-0.6) | -9.4 > -13.0 (-3.6) | bass and voice together, drums partly |
| 3:35.3 voice gone | -18.9 > -17.9 (+1.0) | -23.9 > -15.8 (+8.1) | -25.9 > -66.5 (-40.6) | -25.2 > -27.3 (-2.2) | -12.7 > -10.8 (+1.9) | vocals out; bass returns (+10 dB at 3:35.8) |
| 3:49.0 fade starts | -22.0 > -26.3 (-4.3) | -17.0 > -55.4 (-38.4) | -74.3 > -75.8 (floor) | -28.5 > -34.5 (-6.1) | -13.9 > -20.9 (-7.0) | bass (leaves); bed and drums fall with it |
| 3:54.5 steep drop | -32.8 > -45.1 (-12.3) (0.8 s windows) | -30.9 > -76.8 (-45.9) | floor | -44.7 > -51.3 (-6.6) | -26.4 > -39.6 (-13.2) | bass out; drums and mix fall |

Reading the table: **the verse/hook edges are carried by the vocal stem almost alone** (voice +4.1 to +5.1 dB into every verse, -7 to -9 dB into hooks 2 and 4); the drum stem stays within -1.8 to +1.8 dB at every hook/verse edge (drums are not a boundary carrier); the bass changes are large at the hook entries (+13.7, +20.3, +29.5 dB) but that is the loop clock, not the edge (bass block starts are 0.0 to 1.4 s before or at the voice's hook start: 0:10.44, 1:10.63, 2:10.64, 3:13.24, mixed). No boundary shows in the mix by more than 2.5 dB until 3:34.0. **No silence** is claimed before the final digital zero: at each edge the mix level stays above -22.3 dB (the first-hole minima are rhythm-section-with-voice-out dropouts, with drums at -18.7 to -20.2 dB and the "other" bed at -23 to -25 dB inside the holes; 50 ms stems).

### First-hole table (new; shows hook 4 is the same gesture as hooks 1 to 3). Mean level in the hole, dB, 50 ms frames

| Hole | Time | Drums (before / in / after) | Bass | Vocals | Other | Mix |
|---|---|---|---|---|---|---|
| Hook 1 | 0:10.94-0:12.29 | -15.0 / -19.9 / -19.2 | -26.2 / -26.1 / -15.2 | -26.7 / -51.2 / -22.4 | -24.8 / -25.3 / -26.8 | -9.5 / -14.0 / -10.9 |
| Hook 2 | 1:11.89-1:13.0 | -17.4 / -20.2 / -20.3 | -20.8 / -26.5 / -14.6 | -16.1 / -46.4 / -20.0 | -28.1 / -25.0 / -26.1 | -9.6 / -14.2 / -10.6 |
| Hook 3 | 2:12.81-2:13.91 | -17.2 / -18.7 / -19.8 | -18.9 / -26.1 / -15.0 | -19.6 / -40.6 / -21.2 | -29.6 / -25.5 / -26.0 | -10.3 / -12.8 / -10.8 |
| Hook 4 | 3:13.33-3:14.65 | -18.5 / -18.7 / -19.7 | -49.8 / -19.9 / -16.0 | -16.8 / -28.5 / -22.0 | -29.3 / -23.3 / -26.6 | -11.0 / -11.9 / -11.1 |

The voice stem in hole 4 is shallower in these means (-28.5 against -40.6 to -51.2) only because it holds a stem-separation remnant; the voice file's per-hole depth (to -57 dB median) is the better figure. Hook 4's hole is distinguished only by the bass being absent just before it (3:09.6-3:13.2, the verse's loop gap) and returning inside the hole; in hooks 2 and 3 the bass block had already started. A second, deeper-in-the-voice hole sits at +17.4 to +17.6 s from every hook start (0:27.9, 1:28.65, 2:29.65, 3:30.55; vocal -27 to -39 dB, mix -10.0 to -11.1 dB, drums, bass, other steady): the voice file's pattern, confirmed on my side.

## 5. Answers to questions put to me

**Rhythm Q1: Is 0:10.4-0:30.4 a true hook, and is the opening a 12-bar unit that later cycles drop?** Yes to the first. It has the length (20.0 s, 7.9 bars), bass density (84 per cent against 87, 87, 87), voice level (-19.3 against -19.3 to -20.2) and the first-hole slot (0:10.94-0:12.29, +0.5 to +1.9 s after entry) of hooks 2 to 4; the voice file's cross-correlation of hook phrases (r 0.90 to 0.96) includes hook 1b. Hook 1 is therefore not a pre-verse. The opening is 4 bars of voiceless intro plus an 8-bar hook = 12 bars before the first verse; later cycles drop the 4-bar intro and are 24 bars (hook 8 + verse 16). The intro has the verse's bass density (25 per cent), so the 4 bars read as a verse-state rhythm section with no voice; the outro (25 per cent) is the same state. Measured, high. A second consequence for rhythm's wording "a section is a bass-density state": the bass block is not the section. The long bass block is 22 to 24.5 s long (0:12.29-0:34.50 and 0:35.0-0:36.2; 1:10.63-1:35.08 and to 1:37.03; 2:14.13-2:38.08; 3:15.08-3:37.27 and to 3:39.0), hook plus about 2.3 bars (5.5 to 5.8 s) into the verse, and that overshoot is constant on the bass-loop clock (loop phase 0.33). So the sections are defined by the voice (register and the +4 to +5 dB step); the bass state is a second, offset clock. INFERRED, medium-high.

**Voice Q3 and feeling: where does hook 3 end, is the 21 s voiceless block a fifth block or an extension of hook 4, and does the 3 s of digital zero count?**
- Hook 3 ends at **2:32.4** (8.0 bars after 2:12.0): the vocal stem steps +4.1 dB there and the verse level (-16.6) follows; the bass goes off at 2:38.08, 5.7 s later, not at the hook end. My round-1 "~2:34 edge" is corrected to 2:32.4 (the same step is at 0:30.4 +4.4 and 1:31.4 +5.1). Measured, high (edge to +/-0.25 s).
- The outro is **a voiceless block in the verse slot**, not an extension of hook 4. Evidence: (a) the bass block ends at loop phase 0.33 after hook 4 (3:39.0), exactly as after hooks 1 to 3 (section 3); (b) drums -20.5, bass-on 25 per cent (verse 27 to 29 per cent, hook 84 to 87), other -29.0 dB (verses -27.6 to -28.1, hooks -24.7 to -25.3), so the rhythm section and bed are in the verse state; (c) the bass returns at 3:35.8 = bar 85.0, a bar line of the 94.5 grid. The hook's voice edge at 3:33.5 (8.0 bars) is followed by 1.3 s in which bass (-15.1 to -27.5 dB), voice (-20.9 to -27.3, then -58 dB at 3:35.2) and drums (to -30 dB at 3:35.0) all thin together and the mix falls to -21.6 dB at 3:35.0; the voice tail runs to 3:35.1. It is not a voice-only cut and not a clean hook-end step as at hooks 1 to 3. INFERRED, medium (the verse-slot reading rests on the loop-phase match and the stem levels, not on a hearing of any change in role).
- Digital zero: 3:56.67 to 3:59.44 = 2.77 s of exact zero in the file. Whether it belongs to the "track" cannot be told from the file (it could be an encoder tail or a padding, section 7); I count the music as ending at 3:56.45 and list the file as 3:59.44 long. High on figures; open on status.

**Harmony Q (to form, round 1): do the Gm/G side-steps sit at boundaries?** Harmony's answer (inside hooks, never at a boundary) is confirmed from the form side: the steps are at +5.7 to +6.0 and +15.4 to +18.4 s from hook starts, away from every edge in my table. Form consequence: each hook has an internal plan of hole 1 (+0.5 to +1.9 s), walk 1 (about +6), hole 2 (about +17.5), walk 2 (about +16 to +19), end +20.4. The hook is a 8-bar unit with two sub-events at bars 2 and 6.9.

**Sound and voice on the 20 ms mutes (0:10.62, 2:57.4).** The 10 ms mix frame at 0:10.62 is -66.6 dB (my 10 ms scan, hook 1 hole) and sits 0.2 s after the voice entry, so the entry is a cut-in followed by a mute; for form this only says that the first hook's arrival is edit-stitched. INFERRED, low.

## 6. End of track (rule 4; 10 ms envelope of the last 3 s, 236.44-239.44 s; mix and stems)

- The file is 10,559,488 frames at 44.1 kHz = 239.444 s. The last 3 s start at 3:56.44 and contain only the last tail: mix above -60 dBFS only at 3:56.44 and 3:56.47 (-60), above -80 dB to 3:56.56, above -100 dB to 3:56.67. **Last audible sound 3:56.45 (-60 dBFS); level at the end -60 dB at 3:56.47, -67 dB at 3:56.51, then exact zero from 3:56.70.** The final 2.77 s are digital zero. Measured, high.
- Final hits (count from the waveform, 10 ms envelope peaks): within the last 3 s only 2 local peaks (3:56.47 at -60 dB and 3:56.51 at -67 dB) with 1 dB prominence, 1 with 3 dB. Over the decaying run from 3:55.5 to 3:56.5 the count depends on prominence (height above -65 dB: 20 peaks at 1 dB, 15 at 3 dB, first at 3:55.54, last at 3:56.48, -37 to -60 dB). I therefore say: a decaying cluster of 15 to 20 sub-peaks over about 1 s, no distinct closing hit (the earlier counts of 6 and 11 were at coarser prominence settings; I replace "about six" with this range). Medium on the count, high on the shape.
- Stem maxima over the last 3 s (10 ms): mix -57.0, drums -65.5, bass -69.5, other -76.4, vocals -78.3 dBFS (separation noise floor about -78). Last second before the cut: 3:56.0-3:57.0 mix level -54.8 dB; 3:55.0-3:56.0 -40.8; 3:54.0-3:55.0 -30.9 (1 s RMS). The ending is a 7.5 s decline (mix -13.3 dB per second slot at 3:48-3:49 to -54.8 at 3:56) that finishes at -60 dB and then cuts to zero: a fade or a stepped removal ending in a stop, not a ringing last chord (INFERRED, medium; whether the cut is a fade-out in the master is not recoverable).
- Step order in the decline (stems, 0.8 to 1.0 s windows): bass -38 dB at 3:49.0, bass out for good at 3:54.5 (-76.8 dB), drums -12 dB there, drums and bass last at 3:56.37-3:56.38 (sound file). Drums last, as I found in round 1.

## 7. Production era and sync (rules 1 and 5)

Figures: sample peak 0.0 dBFS (exact full scale), 10,317 samples at maximum and 21,079 at or above 0.999 (sound file); mix RMS -10.0 to -10.9 dBFS over 215 s, crest about 10.7 dB; four-bar bass clock with residual std 0.10 s over 183 s (section 3); hook starts 24 bars apart to within 0.4 s; kick-onset spread 20 ms IOI (rhythm), not used as a cue by sound. Verdict unchanged and tagged: modern, limited mastering on a looped, regularly arranged programme, not a single period-consistent recording, INFERRED, medium-high. Band-limited sample under a full-range mix: not available; the whole file is dual-mono and low-passed near 8 kHz (sound file), so a narrow-band layer cannot be separated from the master chain. I make no cut-to-beat statistic. The only sync figure is edge position against my own bass-loop/section grid (94.5 BPM): section edges are within 0.1 bar (0.25 s) of integer bars at 12 of 12 edges listed in section 2; that grid is a bass-and-voice arrangement grid, and its spacing differs from the kick IOI grid (94.0) by 0.5 per cent, so this is not a kick-grid sync result and I do not use it as one.

## 8. How the energy is engineered, restated after the corrections

- Level is flat: mix 10 s RMS stays within -10.1 and -10.5 dB across the hooks and verses; drums stay -18.3 to -19.2; there is no loudness build (sound file's loudness ceiling is the reason: every move is a subtraction).
- Verse to hook: the voice goes down 7 to 9 dB and up in pitch (voice file), the bass block opens (84 to 87 per cent on); hook to verse: the voice steps up 4 to 5 dB and the bass block runs on 5.6 to 5.8 s, then gaps.
- Each hook has the same four-event inner plan (hole 1, walk, hole 2, walk), so repeated returns are the main device; none is unique. The unique things are the 4-bar intro (voiceless) and the voiceless outro that replaces the fourth verse.
- Release: 1.3 s thinning (3:34.0-3:35.3), voice off, bass back at 3:35.8, bass out at 3:38.9-3:39.0 and back 3:43.0 (round 1) to 3:49.0, then bass out, drums and bed to the cut. A stepwise unwind; no cadence is measured.

## 9. Corrections to colleagues, with evidence

- **Rhythm:** "the sections are a bass-density plus register state" is half right: bass density differs by section, but the bass block is offset (starts 0 to 1.4 s before the hook; runs 5.5 to 5.8 s past its end), so the voice marks the edges. Rhythm's 61.3 s for 24 bars and my measured 60.95 s differ by 0.35 s over 24 bars; my bass-loop fit favours bar 2.540 s.
- **Voice:** accepted: hook starts (0:10.4, 1:11.3, 2:12.0, 3:13.1); my 2:14.0 and 3:15.09 were hole exits. Added: the voice tail after 3:33.5 is a fade running to 3:35.1, so "last vocal sound 3:34.7 to 3:35.3" is the fade tail (10 ms stem -58 dB by 3:35.2).
- **Sound:** accepted that the climax cannot be loudness (ceiling). My "+11 dB largest step" was a 0.25 s window artefact repeated in all hooks (their -21.4 to -22.3 dB minima).
- **Feeling (round 1, as I read it):** "final hook as the hardest arrival" has no measured support beyond position; I cannot confirm it.
- My own earlier tags: hook 1 "medium (function)" is raised to high on the function (hook), because the voice file's phrase correlations and my bass-on and length figures all match; the verse 3 edge "medium" is raised to high (vocal step +4.1 dB at 2:32.4). The "climax" tag is lowered (reason in section 1, point 3).

## 10. Not recoverable by measurement

- Whether the tempo is "really" 94.0, 94.5 or 95.7 BPM: three different baselines give three figures; only a project file or score settles it.
- Whether the arrangement was built in 4/8/16-bar blocks by design, and whether the holes, mutes, stutters and the 3:34.0 thinning are DAW edits, gates or performed gestures: the stems show the event, not the hand.
- Whether the digital zero after 3:56.7 is part of the released track or a file artefact.
- Whether any section "feels" like a chorus, bridge or climax to a given listener: my labels are functional (register, level, bass density).
- The real source and age of the drum loop, the bass and the drone bed; the performer; the recording date. Stem separation and a dual-mono, 8 kHz-limited file cannot show them.
- What the hole stems truly contain (demucs bleed makes the vocal floor about -57 to -78 dB).

## 11. Two new questions

1. **To rhythm:** the bass loop gives 94.50 BPM (10.158 s per four bars, residual 0.10 s over 183 s) and hook-to-hook spacing 60.95 s gives the same, while your drum bar lag gives 94.0 (2.554 s). Can you re-measure the drum-stem bar lag on the longest baseline you can (for example the lag that best aligns the 8-bar hook drums of 0:10.4-0:30.4 with 3:13.1-3:33.5, a 183 s gap, searching only 2.5 to 2.6 s per bar) and say whether the kick pattern follows 94.0 or 94.5, and whether the kick's 3+2+3+2 phase restarts at each hook start (bar 4, 28, 52, 76)?
2. **To sound:** across the 3:34.0 to 3:35.3 thinning the voice falls from -20.9 to -58 dB while bass and drums fall about 12 and 3 dB together. Does the vocal stem decay there look like a fader or fade (smooth fall in dB per second), a reverb or delay tail (a decay time you can state in ms, with repeats at a beat spacing of 0.635 s), or a gate? That decides whether I call 3:35.1 the "end of the voice" or 3:33.5 plus an effect tail.
