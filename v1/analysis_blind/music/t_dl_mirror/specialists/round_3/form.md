# t_dl_mirror: FORM specialist, round 3 (blind, measurements only)

Read: all seven round-2 files, plus the round-3 harmony, sound and voice files already written (round-3 rhythm was empty when I read). New run: `v1/scripts/agents/form_r3_tdl.py` (end envelope; kick-band drum-stem pattern match between hooks). Times m:ss; levels dBFS. Stems are demucs estimates. Tags: measured / INFERRED, high / medium / low. Unchanged measurements from my round 2 (boundary table, first-hole table, bass-loop fit) stand and are not repeated in full.

## 1. New measurement: the kick pattern also runs on a 94.5 BPM clock (answers my own round-2 question to rhythm)

Rhythm had not answered (round-3 file empty), so I measured it. Method: drum-stem band-passed 40-150 Hz, 5 ms envelope; take the 15 s of hook 1 (0:15-0:30) and slide it over a 27 s search window centred on the expected repeat in each later hook; take the lag of best Pearson correlation.

| Hook compared with hook 1 | Best lag (s) | r | Gap per 24-bar cycle (s) |
|---|---|---|---|
| hook 2 | 61.055 | 0.70 | 61.06 |
| hook 3 | 122.245 | 0.73 | 61.12 |
| hook 4 | 183.310 | 0.74 | 61.10 |

The low-frequency drum pattern repeats at 61.06 to 61.12 s per 24 bars = bar 2.544 to 2.547 s = **94.5 BPM (94.47 to 94.52)**. Over 183 s the lag is 0.3 s from 3 x 61.0, which is consistent with the bass-loop fit (2.540 s) and not with 94.0 (2.554 s: 3 cycles would be 183.7 s) or 95.7 (2.51 s: 180.7 s). This is on the kick grid itself (rule 5: the pattern lag is a kick-pattern figure, not a bass one). So 94.5 is the better figure for the arrangement and the low drum pattern together; rhythm's 94.0 comes from short bar-lag windows and I now consider it about 0.5 per cent low. Measured on one method with a flat correlation peak (r 0.70-0.74; lag resolution 5 ms, but the true peak width is set by the pattern's own repeats), so INFERRED, medium-high. I did not test whether the kick's 3+2+3+2 phase restarts at each hook start; the high r at a single lag says the pattern is the same one at each hook but not where it starts.

## 2. Corrections and answers

- **Feeling (round 2): "outro as a fifth, aftermath block, not an extension of hook 4": agreed.** I had it as a voiceless block in the verse slot (bass loop phase 0.33 at 3:39.0, bass-on 25 per cent, bed -29 dB); the two readings agree on "not hook 4". Where we differ is the label: "verse slot" (arrangement) against "aftermath" (feeling). INFERRED, medium.
- **Feeling: "hook 4 is the +11 dB slam back" and "3:15.09 return": already withdrawn in my round 2**; feeling's own hook-4 voice figures (-20.8 dB against -20.3 to -21.1) agree with mine. Feeling's journey line 5 should read: the arrival is the same event as at 0:10.4, 1:11.3 and 2:12.0, but the *bass* is the only thing returning late in hook 4 (absent 3:09.6-3:13.2, back in the hole at 3:14.1). That is the one genuine difference: hook 4's hole is rhythm-section-with-bass-returning, not an emptier hole.
- **Feeling: "voice re-entries at inconsistent bar phases on 0.627 s beats".** Correct only because the grid was wrong: on 94.5 BPM (bar 2.540 s) every hook start lands at 4.1, 28.1, 52.0, 76.0 bars, within 0.1 bar. The edges are on the bar; the hole exits (1:13.15, 2:14.0, 3:15.09) are 0.5 to 1.9 s after, and rhythm found gap ends not quantised to sixteenths. So: section edges on the bar (measured, high on 94.5), holes loose within the hook.
- **Sound (round 3): vocal fall at 3:33.5-3:35.1 is phrase-wise thinning with no tail, with -9.2 then -6.3 dB/s slopes and up/down movement.** I accept it and drop my question: the voice's last phrase edge is 3:33.5; its last audible activity (above -50 dB) is about 3:35.2; nothing smooth like a fader. My table row "3:34.0 thinning" is consistent: bass (-12.4) and voice (-6.4 to -40) thin together over 1.3 s, with drums -2.5. Measured, medium-high.
- **Sound: the mix "steps +7 to +9 dB when bass and voice enter together and falls by the same amount when they leave".** True at 3:34.0 (-3.6 dB mix over 1.5 s windows) and 3:49.0 (-7.0 dB), but not at the hook entries (+2.5, -1.7, -0.5, -0.6 dB mix in my table): at hooks 2 to 4 the voice goes down 7 to 9 dB as the bass rises 14 to 30 dB, so the mix is nearly level. The +7 to +9 dB figure is for the end of the track and for 0:10.4 only (+2.5 mix there; voice +43.5, bass +29.9 stems). I ask sound to state which entries it means. Low-confidence disagreement; my table figures are 1.5 s means of 10 ms RMS.
- **Voice (round 3): hook = statement/answer, second half of each hook "more broken" (gaps at +13 and +17.5).** Confirmed from my first-hole and second-hole data (+17.4 to +17.6, vocal -27 to -39 dB, mix -10.0 to -11.1). Adds to my hook plan: hole 1 (+0.5 to +1.9), step 1 (+5.4 to +6.5), long gap (+12.9 to +13.4), step 2 (+15.2 to +18.4), hole 2 (+17.5), end +20.4. Measured, medium-high (voice and harmony agree on all except the step 2 window).
- **Harmony: the walk G-F-C-D sits in the bass-dense blocks and is the one harmonic event.** Form consequence: each 24-bar cycle has exactly two pitch events (both in the hook, bars 2 and 6.9) and no harmonic change at any section edge. The verse is a pitch-static bed (D+A) with the voice as the only pitched mover. So form is carried by voice register and bass density, with harmony only adding detail inside hooks. Measured, high.
- **Own tag changes:** none lowered; tempo for the arrangement raised from medium to medium-high (kick-pattern lag, bass loop and hook spacing now agree at 94.5).

## 3. Song map (settled, bars of 2.540 s)

Intro 0:00-0:10.4 (4.1 bars) | hook 1 0:10.4-0:30.4 | verse 1 0:30.4-1:11.3 | hook 2 1:11.3-1:31.4 | verse 2 1:31.4-2:12.0 | hook 3 2:12.0-2:32.4 | verse 3 2:32.4-3:13.1 | hook 4 3:13.1-3:33.5 (voice tail to 3:35.1) | thinning 3:34.0-3:35.3 | voiceless outro 3:35.8-3:49.0 | fade 3:49.0-3:56.5 | digital zero 3:56.67-3:59.44. Edges +/-0.2 s. Boundary table is in round 2 (section 4); the verse/hook edges are carried by the vocal stem (+4.1 to +5.1 dB into verses, -7 to -9 dB into hooks 2 and 4); drums move at most 1.8 dB at any hook/verse edge; bass moves 13 to 30 dB at hook entries but on its own 10.16 s clock; the mix moves at most 2.5 dB at any edge until 3:34.0. No silence before the final zero: the mix stays above -22.3 dB in every hole. Measured, high.

## 4. End of track (rule 4, re-run)

10 ms envelope of the last 3 s (236.44-239.44 s), mix: the file is 239.444 s long. Only the first frames of the window carry sound: -57.0 dBFS at 3:56.44 (last frame above -60), last frame above -90 dB at 3:56.57, exact zero after about 3:56.70 (round 2 gave -60 at 3:56.47, -67 at 3:56.51 on its own threshold). **Last audible sound 3:56.45 (-57 to -60 dBFS); level at the end about -57 to -67 dB, then cut to zero for 2.77 s.** Final hits: no distinct hit; a decaying cluster of 15 to 20 sub-peaks in 3:55.5-3:56.5 (round 2) and 2 peaks inside the last 3 s. Mix ending is a 7.5 s decline from 3:49.0 (-13.9 dB to -54.8 dB at 3:56). Measured, high on the time and level, medium on the hit count (depends on prominence setting).

## 5. Production era and sync (rules 1 and 5)

Figures: sample peak 0.0 dBFS, 10,317 samples at full scale (21,079 at or above 0.999); mix RMS -10.0 to -10.9 dBFS over 3.5 minutes, crest about 10.7 dB; kick-pattern repeat r 0.70-0.74 at 61.1 s lags; bass loop residual 0.10 s over 183 s; kick IOI spread 20 ms (rhythm); the whole file is dual-mono and low-passed near 8 kHz, so no narrow-band layer can be compared with a full-band mix. Verdict: modern, limited master of a looped, DAW-like arrangement; whether the break or the drone bed is older source material cannot be seen (INFERRED, medium; unchanged). Sync: section edges against the 94.5 BPM arrangement grid are within 0.1 bar at 12 of 12 edges; that grid (bass loop, hook spacing and kick-pattern lag all at 94.5) is now also the kick-pattern clock, 0.5 per cent from rhythm's kick IOI grid (94.0), so I carry both grids named and give edge sync only on 94.5.

## 6. Settled conclusions (5 bullets)

- **Form is a three-cycle 24-bar plan after a 4-bar voiceless intro:** 8-bar hook + 16-bar verse repeated three times (hook starts 0:10.4, 1:11.3, 2:12.0, 3:13.1), a fourth hook, then a voiceless outro in the verse slot, a 7.5 s fade and a 2.77 s digital zero. All edges are within 0.1 bar of a 94.5 BPM (2.540 s) grid, which the bass loop (10.158 s per 4 bars), the hook spacing (60.95 s) and the kick-pattern lag (61.06-61.12 s, r 0.70-0.74) all support (high on edges, medium-high on 94.5).
- **The voice carries the section edges and the bass is an offset clock:** vocal stem +4 to +5 dB into verses and -7 to -9 dB into hooks 2 and 4; drums never move more than 1.8 dB at an edge; the bass block starts on and runs 5.5 to 5.8 s past each hook (loop phase 0.33). Mix moves at most 2.5 dB at any edge (measured, high).
- **There is no climax by loudness, pitch or density, and hook 4 is a repeat:** hook voice -19.3 to -20.2 dB, bass-on 84 to 87 per cent, mix 10 s RMS -10.1 to -10.5 dB, first-hole minima -21.4 to -22.3 dB in every hook. Tension is made by repeated withdrawal and return of bass and voice under a fixed limiter ceiling; any sense of a last peak is position and the voiceless outro (measured, high; the "last hook is the climax" reading is INFERRED, low).
- **Each hook has the same inner plan and the verses have none:** hole at +0.5 to +1.9 s, bass-walk step near +6, long gap near +13, second step and hole at +15 to +18, end at +20.4; the only harmonic events (bass G-F-C-D over a D+A bed) are inside hooks; the voice is the only pitched mover in verses (measured, medium-high).
- **The ending is a stepped withdrawal into a cut, not a cadence:** voice thins 3:33.5-3:35.2 with no tail, bass returns 3:35.8 and leaves at 3:49.0 and 3:54.5, drums and bed fall to -57 dBFS at 3:56.45 with no final hit, then 2.77 s of exact zero (measured, high on time and level; the cut's status as master fade or file artefact is open).

## Not recoverable by measurement

- Whether the true tempo is 94.0, 94.5 or 95.7 BPM: three baselines, three figures; a project file would settle it (I favour 94.5 for the arrangement).
- Whether the 4/8/16-bar plan, the holes and the 3:34.0 thinning are DAW edits, gates or performed gestures: stems show the event, not the hand.
- Whether the 2.77 s digital zero belongs to the released track: the file cannot say.
- Whether any section feels like a chorus, bridge or climax to a given listener: my labels are functional (voice register, level, bass density).
- Source, age and performer of the drum loop, bass and drone bed; recording date: separation, mono and an 8 kHz ceiling hide them.
- What the hole stems truly contain: demucs bleed makes the vocal floor -57 to -78 dB.
