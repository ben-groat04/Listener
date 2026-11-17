# Form specialist, round 1: t_cshells_cshore (blind, measurement-only)

Scripts: `v1/scripts/agents/form_r1.py` (10 ms envelopes of mix and four stems, peak, end of track), `v1/scripts/agents/form_r1b.py` (boundary table), plus inline autocorrelation of the drum-stem onset envelope. Sources: all 19 window notes (win_0000 to win_0360), per_second_levels.json, audio/song.wav, stems_raw/htdemucs/song/*.wav, chords.json, whisper transcripts, audio_features/summary.json. Tags: measured / INFERRED / speculative, with confidence. Timestamps m:ss. Stem levels below about -70 dB are the separator's floor and carry no information (checked: stems read -84 to -90 dB even in the exact-zero stretches).

## 1. One-paragraph shape

A 6:01 instrumental (duration 360.98 s) in an A-centred modal vamp, built as one long, slow accumulation and a long evaporation, not as verse/chorus. Digital silence (0:00-0:11.3) opens it; a noisy percussive prologue (0:11-0:24) gives way to a pitched A drone and strummed texture (0:24-1:04) that has no drums or bass; the rhythm section is then added in stages across a run of 4-second hit-and-decay blocks (1:04-1:53); a full-band groove holds from 1:53 to about 5:17 with the weight shifting between bass, drums and the "other" layer; drums leave at about 5:17-5:19, bass at 5:22.5-5:25, the harmonic layer fades from about 5:29 (about -15 dBFS) to about -63 dBFS, and the file cuts to exact zero at 5:42.84, followed by 18.14 s of digital silence. There is no sung lead vocal anywhere (vocals stem at the floor except a handful of short vocal-like events listed in section 5). Confidence: high on the arc, medium on where one "section" ends and the next begins, because most boundaries are gradual or are carried by one stem.

## 2. Song map

Mix level is per-second dBFS (per_second_levels.json) averaged over 4 s blocks, unless stated.

| # | time | name | what defines it | mix level | confidence |
|---|---|---|---|---|---|
| 0 | 0:00-0:11.30 | Digital silence | mix exactly zero (-240 dBFS floor); first non-zero sample at 0:11.299 | -240 | high (measured) |
| 1 | 0:11.30-0:24.4 | Noise/percussion prologue | full-band noisy "other" layer plus drum-stem bursts (about 8-9 onsets/s), no tonal centre (chords.json "N" 0:11.33-0:24.43), wide stereo (width up to 1.5) | -39 to -44 | high on facts, medium on role |
| 2 | 0:24.4-1:04.8 | Drone and strum, no rhythm section | near-mono (width 0.09-0.11), drums gone by about 0:30 (stem -87 dB from 0:32), bass and vocals at floor, A pedal; pulsed strokes at about 0.5 s (0:40-0:43.4), a 4-s dying low A (0:43.4-0:47.4), re-entry +16 dB at 0:47.4, near-stop at 0:55 | -33 to -45 | high |
| 3 | 1:04.8-1:53.4 | Staged build by 4-s blocks | hits at 1:00.9, 1:04.8, 1:08.8, 1:12.9, 1:16.8, 1:20.8, 1:24.9, 1:28.9, 1:33.0, 1:37.0 (hit IOI 3.9-4.1 s); drums enter 1:04.8, bass from about 1:06 (full by 1:16), other-stem dropout 1:44-1:49 | -33 rising to -19 | high |
| 3a | 1:04.8-1:20.8 | Add-the-band blocks | drums first, bass in over three blocks (bass -65 dB at 1:04 to -26 dB at 1:16) | -33 to -22 | high |
| 3b | 1:20.8-1:44 | Stab and sustain blocks | blocks alternate sustained and gated "other"; bass hole 1:33.8-1:36.6 | -19 to -27 | high |
| 3c | 1:44-1:53.4 | Thinned tension | "other" drops about 14 dB (1:45.2), then out again 1:47-1:49 (-50 dB); drums and bass keep ticking; return +20 dB in "other" at 1:49.3 and again 1:53.4 | -27 to -29 | high |
| 4 | 1:53.4-3:44 | Full-band groove plateau (the "A" part) | steady quaver bass (median IOI about 0.25 s), dense drums, "other" wash; mix -16.7 to -19.5, range only about 3 dB | -17 to -19 | high |
| 4a | 1:53.4-2:20 | Groove with a breather and a lift | "other" dropout 2:03-2:05.4 (rhythm section continues), lift at 2:07.5 (F#m/D colour, brighter drums) | -17 to -19 | high |
| 4b | 2:20-2:40 | Talky stretch | vocals stem rises to -25 dB at 2:22 (speech-like fragment, 2:21.5-2:26.5), quick chord churn 2:24.6-2:26.2 | -17 to -18 | medium |
| 4c | 2:40-3:07 | Locked plateau | no entries; drum highs taper at about 2:55; quarter-note bass (IOI about 0.49-0.51 s) 3:00-3:07 | -18 | high |
| 4d | 3:07-3:44 | Darkening and heaving | bass doubles to 8th/16th notes at 3:07; at 3:13 top end above 4 kHz falls away in mix and "other" while bass goes long and soft; "other" dip 3:18-3:19.5; bass thins from 3:24 (-29 dB) to -42 dB at 3:28; glide 3:27.5-3:28.5 (about 300-500 Hz up to about 1.1 kHz); sample peak 0 dBFS at 3:21.89 | -16 to -17 | medium |
| 5 | 3:44-4:11.5 | Bass-out peak (loudest) | bass stem falls 40 dB (-31 to -63 dB) over 3:43-3:44; "other" +6 dB and a sustained band near 1 kHz; two vocal-like bursts (3:44-3:45.5, 3:47.8-3:49.2); mix at its highest (-13.7 dBFS blocks, 3:44-3:59) | -14 to -16 | high |
| 6 | 4:11.5-4:36 | Bass returns, A-G swing | bass in at 4:12-4:13 (-61 to -27 dB), brief bass out 4:18.5-4:23, back 4:24-4:35; A/G alternation (chords.json) | -15 to -16 | high |
| 7 | 4:36-4:46.5 | Bass out again | bass -52 to -64 dB; held tones about 390 Hz and about 1 kHz (stops 4:42.3) | -15 | high |
| 8 | 4:46.5-5:17 | Bass re-entry and drum-led finale | bass +25 dB in about 2 s (4:46.5-4:48.5); drums dense (about 3 onsets/s, 0.12 s and 0.24 s spacings); two short vocal-like events at about 5:12.3-5:12.8 and 5:16.7-5:17.2 | -15 to -17 | high |
| 9 | 5:17-5:29 | Drums leave, drone | drum stem decays to floor by about 5:18.9 (last real onset 5:18.48); bass out 5:22.5-5:25; "other" holds about -15 dB | -15 to -17 | high |
| 10 | 5:29-5:42.84 | Fade with speech-like murmur | "other" fades about 3.7 dB/s (-15 dB at 5:29 to -63 dB at 5:42); vocals stem -50 to -67 dB intermittently from 5:30.5 | -18 to -63 | high on fade, low on voice |
| 11 | 5:42.84-6:00.98 | Digital silence | final non-zero sample at 342.835 s (amplitude -1.5e-05, one 16-bit LSB) | -240 | high (measured) |

Window-note disagreement resolved: the 0:20 note calls 0:22.3 a "gap"; I treat it as a 15 dB partial dip (mix about -50 dBFS, still audible), not a silence, consistent with that note's own table.

## 3. Tension and release

- **Largest single release/jolt: 0:11.30.** The mix steps from exactly zero to about -48 dB RMS in one frame with peaks near -22 dBFS (win_0000, my re-check: mix -240 to -39 dB over the 2.4 s before/after). This is the track's first event and works as a shock cut-in, not a build. INFERRED, high.
- **Slow-burn tension 0:24-1:04.** About 40 s with no bass and no drums (stems at floor, drum stem -87 dB, bass -86 dB) and a near-mono signal (width 0.09-0.11). Stasis is the tension: the harmonic layer swells and fades (0:43.4-0:47.4 dying low A at about -3.5 dB/s, then +16 dB re-entry 0:47.4 to 0:49) and stops down at 0:55 (mix -60.6 dBFS, 28 dB under its neighbours; not silence).
- **The 4-s block engine, 1:00-1:40.** Each block is a full-band hit then a 20-25 dB swell-and-fade (1:00 -30.1, 1:03 -53.4, next hit 1:04 -26.7, per win_0060). Rhythm section is added a layer per block (drums 1:04.8; bass 1:06 onward). That is an engineered build: the same hit-decay cycle repeats while the band thickens underneath, which is why it reads as accumulation. I checked the hit spacing: IOIs 4.0, 4.1, 3.9, 4.0, 4.1, 4.0, 4.1, 4.0 s (100 ms resolution), mean 4.03 s. That is 8 beats of a 0.50 s beat (120 BPM), not 8 beats of the tracker's 123.05 BPM (3.90 s). The drum stem at 1:05-1:15 also shows 0.50 s hit spacing (win_0060: 1:04.84, 1:05.35, 1:05.85). So the block grid is a 120 BPM-type grid; the tracker's 123 BPM is the song-level average (rule 5: grid named, checked against the drum/hit spacing). Confidence high that blocks are 4.0 s; medium that the local pulse is 120 BPM (my autocorrelation at 11.6 ms lag resolution gives 0.511 s at 1:04-1:40 and 0.499 s at 1:53-2:13; later 0.476 s, about 126 BPM at 3:50-5:00; coarse, low-medium confidence that tempo drifts 118-126 BPM).
- **Withheld-energy tension 1:44-1:53.** "Other" drops 14-24 dB (1:45.2, 1:47-1:49 at -50 dB) while drums and bass run on, mix about 14 dB down (win_0100: -33 to -23 dB at 1:49.3). The return at 1:49.3 (other -50 to -24, +26 dB) and again at 1:52.6-1:53.4 (other -40 to -20 dB, mix -25 to -18) is the major arrival of the track: from here the mix is about 5 to 8 dB louder than anything before it and stays within about 3 dB for the next 3 minutes. Confidence high.
- **Rhythm-section-only dropouts as micro-releases.** 1:33.8-1:36.6 (bass stem -50 to -79 dB, drums tick on), 2:03-2:05.4 ("other" out, drums and bass continue; mix about 3-10 dB lower on bare 0.25 s slices, win_0120), 3:18-3:19.5 ("other" -8 to -10 dB). None is a silence; in each the mix stays at or above about -27 dBFS.
- **Peak: 3:44-3:59.** The mix is at its highest sustained level (-13.7 to -14.2 dBFS 4 s blocks), reached not by adding but by removing the bass (bass -31 to -63 dB at 3:44) and letting the "other" layer rise 6 dB with a sustained band near 1 kHz. A peak made by subtraction plus mid-range emphasis. INFERRED, medium (the stem separator may be moving low synth between bass and "other").
- **Bass cycling 3:44-5:17 as the late-track pump.** Bass is out 3:44-4:11, in 4:12-4:18, out 4:18.5-4:23, in 4:24-4:35, out 4:36-4:46, in 4:47-5:17. Each return is a release; the 4:46.5-4:48.5 return (+25 dB in about 2 s) is the last big one. Drum stem never drops below about -35 dB through all of this.
- **Release by evaporation 5:17-5:42.84.** Drums out (5:17-5:19), bass out (5:22.5-5:25), then a fade (5:29 onward) of about 48 dB over 13 s, ending in a hard cut. No final cadence or climactic hit. See end-of-track section.

## 4. Boundary evidence table (re-measured separately, rule 3)

Levels are 10 ms-envelope energy averaged over 2.4 s before and after the boundary, in dB, from the Demucs stems and the full mix (form_r1b.py). Where a stem sits at about -75 dB or lower on both sides it is at the separator floor and counted as "no change".

| boundary | drums change | bass change | vocals change | other change | mix change | stem carrying it |
|---|---|---|---|---|---|---|
| 0:11.30 silence to sound | -84 to -41 (+43) | -84 to -73 (floor, small) | -84 to -74 (floor, small) | -86 to -50 (+36) | -240 to -39 | drums and other together; whole mix |
| 0:24.4 pitched drone enters | -59 to -52 (+7, tail) | none (floor) | none | -48 to -38 (+10) | -46 to -37 (+9) | other |
| 0:43.4 strokes stop, low A rings | none (floor) | none | none | -36 to -43 (-7; onsets stop, centroid 315 to 121 Hz per win_0040) | -35 to -43 (-8) | other |
| 0:47.4 re-entry | none | none | none | -47 to -33 (+14) | -46 to -33 (+13) | other |
| 1:04.8 drums enter, block build begins | -83 to -37 (+46) | -89 to -54 (+35) | -86 to -81 (floor, bleed) | -42 to -31 (+11) | -42 to -29 (+13) | drums, with bass following over 12 s |
| 1:20.8 block hit (block 6) | -43 to -38 (+5) | -26 to -27 (0) | none | -33 to -28 (+5) | -25 to -24 (+1; the hit is a 0.1 s transient of about +8 dB, win_0080) | other and drums on the transient only |
| 1:44.5-1:45.2 other thins | -48 to -47 (0) | -29 to -33 (-4) | none | -34 to -26 at 1:44.5, with a dip to -50 at 1:47-1:49 | -26 to -25; -33 at 1:47-1:49 | other (rhythm section carries on) |
| 1:49.3 return | -48 to -45 (+3) | -34 to -32 (+2) | none | -50 to -24 (+26) | -33 to -23 (+10) | other |
| 1:53.4 full band lock | -30 to -31 (0; centroid change) | -28 to -24 (+4; becomes quaver pulse) | -82 to -77 (floor) | -40 to -20 (+20) | -25 to -18 (+7) | other, then bass pulse |
| 2:03.0-2:05.4 other dropout | 0 (about -0.7) | +1 | floor | -5 then +12 (-33.5 to -21.4 per win_0120) | -2 then +3 | other only; rhythm section continues |
| 2:06.0-2:07.5 lift | -29 to -27 | -23 to -24 | floor | -27 to -21 (+6) | -20 to -18 (+2) | drums and other (timbre) |
| 3:13.0 darkening | -23 to -26 (-3; texture dense and noisy) | -23 to -24 (level same; partials lost per win_0180) | floor | -22 to -20 (level same; top end above 4 kHz lost per win_0180) | -17 to -16 (level same) | timbre change in other and bass, not level |
| 3:44.0 bass out | -26 to -27 | -31 to -63 (-32) | -76 to -47 (+29; two short bursts) | -20 to -14 (+6) | -17 to -14 (+3) | bass (down), other (up) |
| 4:11.5-4:13 bass returns | -26 to -28 | -61 to -27 (+34) | none | -18 to -19 | -16 to -16 | bass only |
| 4:18-4:19 bass thins | -27 to -25 | -26 to -33 then -46 | floor | -16 to -17 | -15 to -15 | bass only |
| 4:36.5 bass out | -27 to -25 | -30 to -64 (-34) | none | -17 to -17 | -15 to -16 | bass only |
| 4:46.5 bass re-enters | -24 to -28 | -42 to -23 (+19; +25 over 2 s per win_0280) | none | -18 to -19 (about -3 to -6 over the next 4 s per win_0280) | -16 to -16 | bass only |
| 5:17.1 drums leave | -29 to -37 then floor by about 5:18.9 | -24 to -24 | -45 to -77 (vocal-like event ends) | -19 to -17 | -17 to -16 | drums |
| 5:22.5 bass leaves | floor | -22 to -34, floor by 5:25 | -75 to -70 (floor) | -16 to -15 | -15 to -15 | bass |
| 5:29.0 fade begins | floor | floor | -70 to -65 (rising; speech-like from 5:30.5) | -15 to -18 and falling about 3.7 dB/s | -15 to -18 | other (fade); voice becomes relatively audible |
| 5:42.84 cut to zero | floor | floor | -78 to floor | -70 to -87 in the same instant | about -68 dB to exact zero in one sample step (win_0340; my env: -63 at 5:42.0, -121.6 at 5:42.5, -240 from 5:43.0) | whole mix (all stems at once) |

Which stem carries which boundary: the whole first 1:04 is carried by "other" (plus drums at 0:11.3). The block build 1:04-1:53 is carried by drums then bass then "other". From 1:53 on, boundaries are almost always one stem: bass (3:44, 4:11.5, 4:36.5, 4:46.5, 5:22.5), "other" (1:49, 2:03, 3:18, 5:29) or drums (5:17). That one-stem-at-a-time handling is the form's mechanism after 1:53.

Silence checks (rule 3): no rhythm-section-only silence exists. Every "quiet" point I checked (0:22.3, 0:55, 1:44-1:49, 2:03-2:05.4, 3:18-3:19.5, 5:17-5:42) has a mix above about -61 dBFS per second; the only true silences are 0:00-0:11.30 and 5:42.84 to the end (exact 0.0 samples). The deepest in-track dip is 0:55 (mix -60.6 dBFS, 28 dB under the neighbouring seconds).

## 5. Voice and sample events as form markers

No sung lead anywhere (vocals stem -71 to -85 dB except the events below). The Whisper vocals-stem pass returns Welsh-labelled text at language probability 0.49 on near-empty audio; I treat all of it as hallucination. Mix pass lists "You" (0:28.6), two English phrases (4:28.9-4:29.6: "This is the only way to get to the top of the mountain..." and a follow-on), and "Thank you." (5:59.64-5:59.94). The 5:59.64 line sits in digital zero (mix and stems at floor), so it is a hallucination (measured, high). The 0:28.6 "You" and 4:28.9 phrases fall where the vocals stem is at floor or only -51 dB at 4:27; I could not confirm speech there and rate them low confidence. Short vocal-like events with measurable stem energy (each 30-50 dB under the mix): 2:21.5-2:26.5 (to -25 dB at 2:22, the strongest), 3:44-3:45.5 and 3:47.8-3:49.2 (peak -42 dB), about 4:27 (-51 dB), 5:12.3-5:12.8 and 5:16.7-5:17.2, 5:30.5-5:42.7 (-50 to -67 dB). Their placement is form-relevant: they cluster at transitions (2:22 after the groove lock; 3:44 exactly at the bass-out peak; 5:12-5:17 just before drums leave; the murmur under the fade). Whether they are speech samples or processed instruments: not recoverable (below).

## 6. Measured end of the track (rule 4)

From a 10 ms envelope of song.wav (script form_r1.py):
- Whole-file length 360.977 s. Last non-zero sample at **342.835 s (5:42.84)**, amplitude -1.5e-05 (one 16-bit LSB, left channel only per win_0360). Exact 0.0 for the final 18.14 s; max |sample| in the last 3 s (357.98-360.98) = 0.0 for the mix.
- Level at the end: -240 dBFS floor (exact zero). Last audible sound: about 5:42.5; the envelope falls -63 dB (5:42.0) to -121.6 dB (5:42.5 half-second mean) to -240 (5:43.0). Audibly, the last content is about 5:42.4-5:42.6 at about -65 dB; it is inaudible at normal listening level well before that.
- Stems over the last 3 s: drums, bass, vocals, other all at or below 6.1e-05 peak (about -84 dB), which is separator noise; nothing real.
- Final hits: **none**. The 10 ms envelope over the final seconds of sound shows small fluctuations (peaks at 341.3, 341.57, 341.66, 341.78, 342.19, 342.59 with prominence over 3 dB) that belong to the speech-like murmur and the decaying drone, not to percussion hits (drums stem -90 dB, floor). Count of percussive final hits: 0. It ends by a decaying tone and murmur, then a one-step cut to exact zero. Confidence high.
- Fade shape: mix per-second: -14.8 (5:28), -25.5 (5:33), -36.7 (5:35), -48.8 (5:37), -54.5 (5:39), -63.1 (5:42). About 48 dB in 14 s (about 3.4 dB/s on win_0340's figures; 3.7 dB/s by my 5:29-5:42 estimate). Not a natural reverb tail (the fall is linear in dB and ends in a single-sample step), so a DAW fade-out plus trim or a cut. INFERRED, medium-high.

## 7. Production-era judgement (rule 1; INFERRED)

Reads as a modern DAW-era production with no clear evidence of archive material in its structure. Figures:
- Peak: 1.0 linear (0.0 dBFS sample peak) at 3:21.89 over the whole file; win_0160 measured 41 samples at or above 0.99 in 2:40-3:00 and a float decode of 1.036 (+0.3 dBFS), so the master is limited to the ceiling. Mix RMS -16.4 to -19.1 dBFS across 2:20-3:20 with only about 3 dB range, consistent with modern limiting. Confidence high that the master is modern.
- Exact digital zero for 11.3 s at the start and 18.14 s at the end, with the end a one-sample step after a fade: a DAW or editor timeline, not tape. Confidence medium-high.
- Loop regularity: the 4-s hit blocks repeat the pattern but IOIs vary 3.9-4.1 s (0.1 s resolution) and the drum fills differ block to block (win_0080), so no evidence of a rigid copy-paste loop; bass quaver IOIs show natural jitter (0.20-0.27 s, with 0.50 s gaps at 1:53.7, 1:57.2, 1:59.7; win_0100). Low-medium confidence: blocks are edited or played to a roughly 120 BPM grid; sample accuracy of my IOI figures is only about 0.05 s.
- Kick onset spread: the drum stem is dense and subdivided (about 3 onsets/s, 0.12 s and 0.24 s spacings, win_0300), the kick-band tracker locks to eighth-note subdivisions, not a clean kick grid; drum timing is more varied than a quantised drum-machine kick (low-medium).
- Band-limited layer under or inside a full-band mix: none found in the main body (95% rolloff 2.3 kHz at 0:30, 1.6 kHz at 1:10, 2.6 kHz at 3:00, 5.6 kHz at 5:00; energy above 10 kHz 0.00-1.2% of total). At the tail (5:38-5:42.5) the 95% rolloff is 5.2 kHz, about the same as 5:00 (5.6 kHz), but the share above 10 kHz falls from 1.2% (5:00) to 0.07% (5:38-5:42.5). That is a milder narrowing than win_0340 suggests ("narrow-band"), and I would not claim an archival layer from it: low confidence either way.
- Overall: modern production, medium-high. I cannot date the source of the noise or murmur material.

## 8. Notes on the window notes (checked against measurements)

- Confirmed: all level-based claims I re-measured (silence to 11.299 s; 1:04.8 drum entry; 1:49.3 and 1:53.4 returns; 3:44 bass out; 4:12, 4:36.5, 4:46.5 bass moves; 5:17-5:19 drums out; 5:22.5-5:25 bass out; 5:42.84 end; the 0:55 dip). The per-second table matches.
- Corrected/added: the 4-s block spacing is 4.0 s = 8 beats at 0.50 s, not 8 beats at 123 BPM (3.90 s); win_0080 describes the spacing as "8 beats at 123 BPM". I keep its measurement (about 4.0 s) and lower the tempo inference to "120 BPM-type local grid, medium".
- Tail band-limited claim lowered (see section 7).
- The win_0000 note mislabels 0:17-0:18 only as a drum burst; fine, but the 0:11-0:24 passage as a whole is "other" plus drums (mix -39 to -44 dB block means).
- Not independently re-verified (carried at their tags): 3:13 timbre change (timbre not level; level columns above show no change), the 3:27.5-3:28.5 glide, chord labels (the chord tracker is noisy; A/Am ambiguity; flickers are low-confidence).

## 9. What a listener would feel, form-wise (INFERRED, tied to cause)

- Disorientation at the start: 11.3 s of silence, then a sudden noisy burst (+about 200 dB step from the zero floor). Cause: measured.
- Waiting, stasis, mild dread through 0:24-1:04: no drums, no bass, mono, a held A with a dying tone and one near-stop at 0:55 (-60.6 dBFS).
- Gathering force from 1:04 to 1:53: block repeats every 4 s and band added piece by piece; a real lift at 1:49-1:53 when "other" returns +20 to +26 dB.
- Locked-in, trance-like drive from 1:53 to 5:17: level held within a few dB for over three minutes, pedal-like A and G/E harmony, with changes coming one stem at a time (low-end "pumping" in and out after 3:44). The song's drama is texture and low-end presence, not melody or words.
- A long unspooling and an abrupt, unresolved cut at 5:42.84, then 18 s of nothing: the quiet ending with faint speech-like murmur may feel unsettling or reflective; intention not recoverable.

## 10. Questions for fellow specialists

1. **Harmony:** the chord tracker flips between A and Am and shows rapid Em/Gm/F#m/Dm flickers (4:26.8-4:32, 2:24.6-2:26.2). From the chroma and the lead notes, is the real third present at all (A major, A minor, or an open fifth), and does the A-G swing at 4:00-4:40 and the F#m/D lift at 2:07.5 and 2:38 count as genuine harmonic sections or just passing colour? This decides whether I should label 4:00-4:40 a separate section.
2. **Rhythm:** I measured 4.0 s hit blocks (8 beats at 0.50 s) in 1:00-1:40 against a tracker tempo of 123.05 BPM, and autocorrelation hints at 0.50 s (1:13-2:13) and 0.476 s (3:50-5:00). Is there a real tempo change between about 1:53 and 3:44 versus 3:44 onward, and is the kick grid in the groove (1:53-3:44) on a fixed 0.50 s, 0.488 s or drifting spacing? Please measure the kick IOI on the drum stem and say which grid each part sits on.
3. **Voice:** the short vocal-like events (2:21.5-2:26.5, 3:44-3:45.5, 3:47.8-3:49.2, 5:12.3, 5:16.7, and the 5:30.5-5:42.7 murmur) fall at or near my structural boundaries. Can you tell from formants, pitch contour and bandwidth whether these are spoken, sung or a processed instrument, and whether the end murmur is the same material as the 2:22 event? A "yes" would let me call them recurring section markers.

(Also for **sound**: is the 3:44-3:59 peak "bass out, band near 1 kHz up" a real change of timbre, or did Demucs move low synth from the bass to the "other" stem?)

## Not recoverable by measurement

- What instruments or sources make the "other" layer, the drone, the glide at 3:27.5-3:28.5, and the sustained bands near 390 Hz and 1 kHz: the separator merges everything into "other" and the spectra are broadband.
- Whether the speech-like fragments and the end murmur are spoken samples, archive broadcasts, field recordings or processed instruments, and what is said: Whisper returns near-empty or hallucinated text (Welsh-labelled, probability 0.49); the stems are 30-50 dB under the mix.
- Whether the 11.3 s opening silence and 18.14 s tail are intended artistic silence or leftover padding in this particular file: only this file is measured.
- Whether the abrupt cut at 5:42.84 is a deliberate ending or a trim: the measurements show the cut, not the intent.
- The true tempo (120 vs 123 vs 126 BPM) and whether drift is deliberate: my envelope resolution and the noisy drum stem limit this.
- Real recording date or age of any layer: nothing measured is narrow-band enough to point to archive material; modern mastering is evidenced, the sources' ages are not.
- Whether the three-minute plateau feels "peak" or "trance" to a listener: level and density are measured, the feeling is inference.
