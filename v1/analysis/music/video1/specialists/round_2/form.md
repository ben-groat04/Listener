# video1 (Elfstedentocht Part 1): FORM specialist, round 2 (debate)

Evidence keys: [R1-x] a specialist's round-1 file; [R2-x] a round-2 file (harmony and sound exist; rhythm's round-2 file was empty when I read, so I answer its round-1 questions); [lv] per_second_levels.json; [ab] audio_features/summary.json and beat_times.json; [mine] new scripts this round, all in v1/scripts/agents/: `form_r2.py` (event-to-bar grid), `form_r2b.py` (K-weighted loudness, vocal edges), `form_r2c.py` (drum sixteenth-grid phase before/after the stop); one inline 50 ms stem envelope around 2:47.4-2:48.6. I cannot hear; everything is read from measurements. Times m:ss. British spelling.

## 1. What changed since round 1 (short)
1. **The form sits on a bar grid.** Counting 4-beat bars (3.077 s) from the first tracked beat (0:00.97), the big events fall on bar lines: bass out 1:15 = bar 24, wall 1:27 = bar 28, bass in 1:40 = bar 32, then 2-bar stab cycles, bar 43 re-ignition, bar 51 return, bar 54 stop. Round 1 said "2-, 4-, 8-bar blocks, medium-low"; the test below raises that to **medium-high**. (Answers Lineage and Rhythm.)
2. **Loudness correction (mine, R1 section 2 and item 11).** In K-weighted short-term loudness the loudest stretches are 1:07-1:15 and 2:48-3:08, **not** 1:40-1:55. The 1:40 "bass slam" adds about 0.1 LU: it is a change of weight and width, not of loudness. The loudness return after the bass-less passage is at **1:27**, with the wall. (Answers Feeling.)
3. **The 2:48 stop is not "all stems black" (mine, R1 item 19).** The drums and bass go out for about 0.5 s; the `other` layer keeps sounding at -23 to -27 dB through the hole and the narrator's last syllable decays inside it. It is a rhythm-section stop under a held guitar, not silence. (Corrects my round 1 and my reading of [img 0160].)
4. **No grid shift at the stop.** The drum sixteenth-grid phase is 0.80-0.83 of a sixteenth before and 0.81 after (R = 0.8 to 0.96). The loop kept running under the hole; the hole is a mute of about two sixteenths. (Corrects the speculation in [R1-rhythm] section 4, "after 2:48", which they rated low-medium.)

## 2. New measurements

### 2.1 The bar grid (high on the clustering; medium on "bar one")
Linear fit of the 218 tracked beats: period 0.7693 s, first beat 0.973 s, residual std 0.017 s [mine, form_r2]. Each event as beats after the fitted beat 0, then modulo 4:

| Event (time) | Beats | Bar count (beats/4) | Beat position in bar (mod 4) |
|---|---|---|---|
| 0:32 voice A ends | 40.1 | 10.0 | 0.07 |
| 0:41 voice B starts | 52.0 | 13.0 | 0.03 |
| 1:15.3 bass out | 96.6 | 24.2 | 0.62 |
| 1:27.4 wall arrives | 112.4 | 28.1 | 0.35 |
| 1:40.0 bass in | 128.7 | 32.2 | 0.73 |
| 1:55 bass out (threshold crossing 1:54.9) | 148.2 | 37.0 | 0.15 |
| 2:01.1 / 2:07.2 / 2:13.3 sub stabs | 156.2 / 164.1 / 172.0 | 39.0 / 41.0 / 43.0 | 0.16 / 0.09 / 0.02 |
| 2:38.4 bass in | 204.6 | 51.2 | 0.64 |
| 2:47.8 stop (drums out) | 216.9 | 54.2 | 0.86 |
| 3:08.06 end | 243.2 | 60.8 | 3.2 |

- **All ten events before the end fall in the first beat after a bar line (0.0 to 0.9 beats).** If phase were free, a cluster that tight has a chance of well under 1 in 1000. Caveats: the bass thresholds are slow ramps, which explains the larger values (0.6 to 0.9) for the bass events; the tracker is about 0.15 beat (0.155 s) ahead of the drum hits (drum sixteenth phase 0.81, [mine form_r2c]; [R1-rhythm] section 2 gives about 0.11 s); some of my times are rounded to 0.1 s. Subtracting that offset puts every event within about 0.7 beat of the bar line. The events are not independent (bass in/out pairs were presumably placed by the same hand), so read this as "the arrangement is bar-locked", not as ten separate proofs.
- **Block lengths in bars:** 0:01-0:32 = 10; 0:32-0:41 = 3; 0:41-1:15 = 11; 1:15-1:27 = 4; 1:27-1:40 = 4; 1:40-1:55 = 5; 1:55-2:01 = 2; the three stabs 2 + 2 + 2; 2:13-2:38 = 8; 2:38-2:48 = 3; 2:48-3:08 = 6.5 (cut). The first half is square (24, 28, 32 = three four-bar steps, and bar 32 is exactly half of the ~61 bars). The second half is odd (5, 3, and a final run that stops at 6.5 bars, not 8). An 8-bar final run would have ended at about 3:11.8; the file ends about 3 s earlier. Whether that is a hard edit of the video (the official part is 3:09 per context.md, so within seconds) or the original ending, I cannot tell: low.
- **Which bar is "one"?** The data pick it: events cluster on tracker beats ≡ 0 mod 4 from 0:00.97, so bar 1 starts at 0:00.97 and the 0:00.7 hit with its swell is a one-beat pickup (the beat is 0.77 s, the swell 0.6 s). Under the 156 BPM reading ([R1-rhythm] section 1) the same grid is two 4/4 bars, so every event lands on beat 1 of every second bar, and the 4-bar blocks become 8 bars of 156. Either way the structure does not depend on the octave answer.

### 2.2 K-weighted loudness (BS.1770 filters, 3 s windows, my implementation, not a calibrated meter; medium-high)
Range -14.1 to -6.4 LUFS-short, i.e. 7.7 LU, about the same band as the dBFS trace, but the shape differs:

| Stretch | Short-term loudness |
|---|---|
| 0:05-0:31 | -9.9 mean (-12.0 rising to -8.3) |
| 0:35-1:15 | -8.2 mean, rising to **-6.6 at 1:07 and -6.8 at 1:13** |
| 1:17-1:25 (bass out) | **-12.7 to -11.2**, a 6 LU fall at 1:15 (R1 dBFS said 4 to 5) |
| 1:29-1:38 (wall, no bass) | -7.9 to -7.8: **the loudness comes back here, 11 s before the bass** |
| 1:41-1:53 (bass back, "peak") | -7.7 to -7.3: **no gain over 1:29-1:38** |
| 1:58-2:12 (pull-down, breakdown I) | -11.3, then -13.5 at 2:05: the trough, 6 LU under the rest |
| 2:15-2:37 | -10.0 rising to -7.7, then -8.0 |
| 2:45-3:06 | -8.1, then **-7.0 to -6.4**: the loudest sustained stretch of the track |

So: the *level* peak is 1:07-1:15 (the build's end) and 2:48-3:08 (the final run, loudest, and very steady at about +/-0.3 LU); the *weight* peak is 1:40-1:55; the **deepest trough** is 2:02-2:13. K-weighting boosts the brighter hats and crash of the last section, which is why it gains about 1 LU over what dBFS RMS showed. This supports [R2-sound] "form is timbral" but nudges it: level does matter at the three ends of the arch (1:15 down, 1:27 up, 2:02 down, 2:14 up).

### 2.3 The 2:47.8 stop, stem by stem (50 ms envelope, high on timings)
- Drums: -22 at 2:47.72, -40 at 2:47.82, about -57 at 2:47.97 to 2:48.17, back to -14 at 2:48.22. Hole of about 0.45 s (0.58 beat, about two and a bit sixteenths).
- Bass: -45 at 2:47.52, about -65 from 2:47.62 to 2:48.12, back to -16 at 2:48.27. Out for about 0.6 s, so it goes out slightly before the drums and returns slightly after.
- `other`: -26 to -30 dB throughout 2:47.4 to 2:48.2, then -17 at 2:48.37. It never stops. It is the quiet bridge across the hole (medium: demucs leakage and sustain make this stem the least trustworthy; but the mix RMS of -21 dB during the hole has to be coming from somewhere).
- Vocals: last syllable peaks at -12 dB (2:47.72), decays through -32 at 2:47.82, -20 at 2:47.97, and ends at -38 by 2:48.12. **The narrator's last word sits inside the hole.** The band stops, the voice finishes, and then everything returns together at 2:48.22 as the voice has gone.
- Reading (interpretation): this is a deliberate rest on a bar grid, the one point where the rhythm section stops while a voice and a held guitar remain. It is smaller than R1's "full stop" and more theatrical: a held breath under the last word of the line.

### 2.4 Voice ends at bar lines (medium)
Vocal-stem edges [mine form_r2b]: the first sentence ends at 0:31.70 = bar 9.99 (a bar line to within 0.01 bar), and the band opens up at that point (0:32). The 2:44-2:48 line ends at 2:48.1, bar 54.3, inside the stop. So both "dat is de Elfstedentocht" endings are the **last event before a change of state**, and the first lands on a bar line (the second is displaced by about 0.3 bar because the band is cut around it). This is a structural use of speech even though the speech is not on the grid inside phrases ([R1-voice] section 3).

## 3. Answers to questions put to me

### 3.1 To me from Rhythm (R1 questions 3 and 1 in part): which boundary set; are blocks clean bar multiples; is 2:48 at a bar line? (medium)
- **Which set:** I trust the stem on/off set (1:15, 1:27, 1:40, 1:55, 2:01, 2:14, 2:38, 2:48) over the auto-sections [ab]: the stem set is on the bar grid, the auto set is not (1:06.4 is bar 21.6; 1:49.4 is bar 35.2; 2:39 is bar 51.4). Your hat-rest changes (0:33, 1:05, 1:15, 1:47-1:56, 2:34) are at 0:32.7 = bar 10.3, 1:05 = bar 20.8 (about 21), 1:47-1:56 = bars 34.5-37.4, 2:34 = bar 50; these sit within a beat of the bar line except 1:05, which is about 0.8 bar early. So your hat-rest changes are largely on the same grid; one outlier.
- **Counts:** above, section 2.1.
- **2:48:** the stop starts at bar 54.2 (0.86 beat after the bar line) and returns at 54.3 + 0.38 beat. Counted from the true drum-hit grid (tracker plus 0.155 s) it begins 0.7 beat after the bar line, i.e. on the **last sixteenth of beat 1 or the start of beat 2**, rests for about two sixteenths and returns on the next sixteenth-grid point. So the stop is **grid-aligned but not bar-aligned**: it falls at the end of bar 54's first beat, not on the one. I think this is why it feels like a catch rather than a full stop (interpretation). Medium.

### 3.2 To me from Feeling: do you divide at 1:15, 1:40, 2:00, 2:38 and 2:48 as I do, or at the auto points? Which should be the emotional peak? (medium)
- **Yes, with additions:** 1:15, 1:27 (not in your list: this is where loudness returns, 11 s before the bass; I think it is the true "lift"), 1:40, 1:55-2:01 (the pull-down as a 3-stage move: top-end roll-off from 1:49.5, bass out 1:55, collapse 1:58 to 2:01), 2:14, 2:38, 2:48. The auto-points [ab] 14.8, 66.4, 75.6, 87.9, 109.4 match 1:06, 1:16, 1:28 and miss 1:40, 1:55 and 2:48.
- **Emotional peak:** I would now name **2:48-3:08**, for three measured reasons: it is the loudest stretch (K-weighted -6.4 to -7.0), the brightest (drum share above 5 kHz 3.3% to 12%, [R2-sound] 2.3), and the widest sustained (0.62-0.8), and it follows the only rhythm-section stop. The 1:40 slam is the strongest *weight* event but adds no loudness. I would call 1:27-1:40 "lift" (wide, loud, tonic returning), 1:40 "landing", 2:01-2:13 "dread or held breath" (K-weighted trough, mono, thin high fifths), and 2:48 "release". These labels are interpretation; the measured basis is above.

### 3.3 To me from Voice: do the voice-free blocks line up with sections; is 2:44 a ternary closure of 0:27? (medium on blocks; low on ternary)
- **0:57-1:03:** inside the build, not a boundary (the voice just pauses).
- **1:28-1:46:** begins at the 1:27.4 wall (a boundary) and ends mid-peak (1:46), so the voice-free block is the wall plus the first six seconds of the peak.
- **2:00-2:14:** matches breakdown I (2:01-2:14) almost exactly, and the voice returns on the 2:14 re-ignition (bar 43.2).
- **2:48-3:09:** matches the final run exactly.
So two of four voice-free blocks are whole sections and a third starts at a boundary: the voice is a **section marker**, entering into space made by subtraction (as Voice says) and leaving at boundaries.
- **Ternary:** the text brackets the track (0:27 / 2:44), and in each case the line ends at the point where the band changes state (0:32 and 2:48). But the music on either side is not a reprise: the band after 0:32 is the D wall, after 2:48 it is bright and cymbal-led. So "framed by the same line" yes; "ternary form" no. Sound's envelope correlation of 0.64 with no waveform match [R2-sound 2.5] leaves open whether it is the same recording; the bar position of its end (9.99 vs 54.3) supports "built to the same function" more than "same take". Low.

### 3.4 To me from Lineage: is there a rule behind the layer entries and exits? (medium)
Yes: **every layer change from 1:15 to 2:48 falls within one beat of a bar line, and the lengths are 4, 4, 5, 2, 2, 2, 2, 8, 3 bars**. That is a loop-and-mute arrangement logic (mute or un-mute a layer on the bar), as in sequenced or DAW-built music, which supports Lineage's reading. It does not prove programming: a band can follow a click and a cue sheet, and the odd lengths (5, 3) show it is not a purely mechanical 8-bar template. I give "grid-locked arrangement, bar-based, probably built in a sequencer or to a click" medium, and "no live-band-in-a-room feel in the structure" low-medium.

### 3.5 To me from Harmony: do your boundaries agree; what does 2:48-3:08 do formally? (medium-high on agreement)
- Agree: 1:15, 1:40, 1:56 (mine 1:55-1:58), 2:12-2:14, 2:36-2:38, 2:48. Your 2:12 for the A-centred block is a few seconds before the full-band re-ignition at 2:14; a plausible reading is a 2-bar pickup (bar 42.2 vs 43.2). Your D return at about 1:24 is **one bar before the wall arrives at 1:27.4 (bar 27.1 vs 28.1)**. So the harmony prepares the wall by one bar: the tonic comes back at bar 27, the floor-less wall hits on bar 28. This is the nearest thing to a harmonic pickup in the piece.
- **2:48-3:08 formally:** neither a chorus nor a coda in the usual sense. It is a **reveal/release plateau** with the pedal D held for 6.5 bars, new timbre (cymbal-led, brighter), no voice, no bass change, no chord movement; it is the only stretch that is both loud and steady, and it is cut off before it completes an 8-bar phrase (section 2.1). It plays the role of a final chorus by loudness and brightness but not by melodic or harmonic content.

## 4. Corrections and agreements
- **Mine (R1 item 11, section 2):** "the loudest sustained stretch is 1:40-1:55" is true in dBFS RMS only. In K-weighting the final run is louder and the 1:40 stretch is level with 1:29-1:38. Replace with section 2.2 of this file.
- **Mine (R1 items 19 and 9):** "all stems black" at the stop is wrong; the guitar layer and the voice tail continue (section 2.3). "Drum energy above 5 kHz about 1% to 9-12%" in R1 vs [R2-sound] 3.3% to 12.4%: sound's before-figure is for 2:30-2:45 (a longer base), mine for 2:40-2:48 from [win 0160]; the after-figure agrees. Use the sound figure as the safer one.
- **Mine (R1 item 10):** "the peak is the landing of a long suspension" stands for weight, not loudness.
- **Accepted from Harmony:** the sub is a fixed 42.6 Hz tone, the bass pedal is D2, and the 1:15-1:23 passage has no D in the guitars. This sharpens my item 7 and 9: at 1:15 the floor goes *and* the tonic goes; at 1:24 the tonic returns; at 1:27 the wall. That is a three-step "return home" over three bars (24, 27, 28).
- **Accepted from Sound:** `other` has four timbral states, the 1:50-1:59 darkening is real (medium), and the 2:00-2:14 block is a different, high, thin sound rather than the wall turned down. That explains why this block is 6 LU down as well as narrow.
- **Rhythm R1 vs me:** "the 2:48 grid shifted by 1/8 beat" is not supported (section 1, point 4).

## 5. How the area connects to the others
- **Rhythm serves form** by not changing: the grid, the 2-bar hat-rest cycle and the sixteenth drum phase all continue through the stop. The only rhythmic event is the 0.45 s mute at bar 54. Everything else the listener hears as form is layering on a fixed ground, as Rhythm says.
- **Sound creates the feeling of the form events**: the loudness return at 1:27 is the wall (distorted, wide); the trough at 2:02 is a different (thin, high, mono) sound; the gesture at 2:48 is a bright drum voicing, and, with Harmony, the "weight, not a note" sub at 42.6 Hz makes the six-second pulses a body-level event under the breakdown.
- **Harmony follows form**: [R2-harmony] agrees that harmony changes at stem boundaries, and the extra fact here is the bar-before pickup (the D back at bar 27).
- **Voice marks the form**: voice-free blocks are whole sections, voice entries come after subtraction, the opening line ends on a bar line at 0:31.7.

## 6. What I still cannot say
Whether the K-weighted figures match a calibrated meter (I used standard BS.1770 coefficients at 48 kHz, 3 s windows, no gating and no relative threshold); whether the guitar layer in the 2:48 hole is truly continuing or is a separation artefact; whether the odd bar counts (5, 3, 6.5) are intentional or the result of editing the video; bar one relies on the tracker's phase plus my cluster test; whether the end cut is the original or an edit.

## 7. Two new questions
1. **To Rhythm:** the drum sixteenth phase is the same (0.81) before and after the 2:48 hole, so the hole is a mute of about two sixteenths with the loop continuing, and the stop starts about 0.7 beat after the bar line. Does the kick pattern in the 3.07 s cycle (your slots) have its strong kick on my bar line (tracker beat ≡ 0 mod 4 from 0:00.97), and does the hat-rest pair fall at the same bar positions in every block? If your kick "slot 0" and my bar line are the same instant, the bar grid is confirmed from the drum side.
2. **To Feeling:** in K-weighted terms the "lift" at 1:27 (+4 LU, wide, tonic back, no bass) and the "landing" at 1:40 (no LU change, weight and width collapse) are different kinds of event, and the trough at 2:02-2:13 is 6 LU down. Which of these does a listener feel as the climax, and does the 0.45 s stop at 2:48, with the narrator's last syllable inside it, read as a held breath or as a gasp? I propose 2:48-3:08 as the emotional peak (section 3.2); tell me if you would rank 1:27 or 1:40 higher and why.
