# Elfstedentocht Parts 1 and 2: the music compared (round 3, final, music colleague)

British English. Timestamps are `<video> m:ss`. Tags H/M/L = confidence; **[speculation]** marks guesses. Nobody on the team has heard the audio; all sound statements rest on measurements and the music readings. Read this round: `round_2/{music,story,picture,listener}.md`, `round_1` earlier, the CLAUDE rules and `logs/ERRORS.md` (so I keep the checks narrow and quote only what I re-measured). New checks are marked "R3 check"; scripts read `data/video{1,2}/stems/*` only.

## 1. Answers to questions put to me

### 1.1 Story Q1: do Part 2's vocal bursts (3:26 to 3:48) repeat the eleven Part 1 name onsets?

R3 check: burst detection on `stems/vocals.mp3` of both videos (16 kHz, 10 ms hop, a burst is a run above 20 dB below that window's maximum, gaps under 0.25 s merged). The result depends on that threshold, so I use only the clear differences.

- **Part 1, 2:16 to 2:37:** the stem shows about 22 short bursts of 0.03 to 0.58 s; the larger ones (0.3 s or more) start at 2:16.0, 2:21.2, 2:24.1, 2:24.6, 2:25.9, 2:27.5, 2:29.0, 2:30.6, 2:32.0, 2:35.1. Spacing is irregular, about 1.1 to 1.8 s between main bursts, with several short sub-bursts (OBS, M). That agrees with an unmetred spoken list.
- **Part 2, 3:25 to 3:50:** the main bursts (0.4 s or more, and each often followed by a very short tail) start at 3:28.6, 3:32.5, 3:36.5, 3:38.6, 3:40.6, 3:42.3, 3:44.6, 3:46.2, 3:48.6: **nine**, not eleven. Their lengths are 0.4 to 1.0 s, longer than Part 1's name bursts (OBS). The first two gaps are 4 s (a bar skipped), then about 2 s (2.2, 2.0, 1.7, 2.3, 1.6, 2.4). The per-second vocal level agrees (stabs at 3:29, 3:33, 3:37, 3:39, 3:43, 3:45, 3:47 at -20 to -27 dB, between -42 and -74 dB).
- **Verdict:** no match in count (9 against about 11), duration or spacing (bar-quantised against free). It does not retire the town-name hypothesis, because a chopped voice would be re-timed by whoever chopped it, but it removes the one structural support I could have found. Story's Whisper chain (eerst, in de lopen, -wacht) remains the only evidence, and ASR on rhythmic material is the weak kind (ERRORS: Whisper times and words overstated before). **Status: unproven, leaning against; M-L.** Only a Dutch listener can settle it, as the listener says.
- Beyond 3:50 the stem has dozens of short events (3:50 to 4:31 about 50 starts, many under 0.1 s): these are artefacts of the separation plus the stabs, not countable "words".

### 1.2 Picture Q1 (same shots at comparable musical events?)

Story did the level table. I checked the stems at the four shared-shot times (R3 check, `stem_rms_per_second.json`, per-second linear RMS, so low resolution at these quiet values):
- video1 1:05 sits 10 s before the bass exit (bass about -21 to -23 dB at 1:10 to 1:13, then at about -64 dB from 1:16, back at about -25 to -20 dB from 1:40; confirms reading, 1:15.3 to 1:40.0). Vocal burst 1:03 to 1:05. A voiced passage with a bass line.
- video1 3:00 to 3:02 is inside the drum-led final sprint (drums about -13 to -16 dB at 2:45 to 2:47; the 3:00 sprint is the loudest stretch by the reading).
- video2 3:34, 3:51, 4:44 are inside the plateau and sag, under a bar-rate voice stab.

So the four shared shots meet **three different musical situations** in Part 1 (voiced band, sprint) and **one continuing groove** in Part 2. I agree with story: placement by musical event is not shown (M). I add one musical reason it is not a surprise: Part 2's plateau is a single 72 s state (3:24.8 to 4:36.8) in which any footage will land under the same groove, so a placement test has almost no power on the Part 2 side (H on the structure, M on the inference).

### 1.3 Listener: "relief or restart?" and the 0.4 s hole on laptop speakers

Already settled in round 2 as relief in level, restart in content; I confirm the figures (Part 2 opens about 15 dB under Part 1's end; B pedal against D). On the hole: the Part 1 hole is 0.4 s at 2:47.8 (drums fade about 0.4 s first); a first-time listener may not take it for a hole, as the listener says. I keep my own round-2 withdrawal: "same stage direction twice", **[speculation]** on intent.

## 2. Building on or challenging colleagues

- **Picture: shared footage (sec 0).** Accepted, and it is the finding that most changes the music question. Music alone could not have told us it: the two scores share no riff, melody or bass line (still none found, H on absence), no key (D then B pedal), no tempo (78 then 120 BPM). The footage pool and the narration script are the only objective bridges; the music is where the pair differs. So **the music is the variable and the script and footage are the constants** in this diptych. That is the clearest way to state what each film adds.
- **Picture, "equal cut rates are a roll-length artefact".** Agreed with the caution; I also withdraw my round-1 156/160 BPM "same pulse" speculation entirely.
- **Story, "pair rises then falls" and listener's "two loudness shapes".** Agreed. In levels: Part 1 sits at about -15 to -10.9 dBFS for 80% of its seconds; Part 2 climbs from about -25.5 to near -9.3 by 3:48 and is then taken apart, ending with a full-level hit at 5:02.3. Nothing links these as one arc except the order of release; I would not call it a staircase.
- **Story, "hole is a property of sound and script, not of the audiovisual work".** Agreed. It is a property of the sound only where the sentence "dat is de Elfstedentocht" is followed by a gap, and the sentence's own position differs (V1 2:44 against V2 1:24).
- **Listener, "Part 1's strongest agreement is its last 20 s".** Fits what the music does: Part 1 is the only track whose loudest, brightest run (centroid about 2.9 kHz) comes last. Fine. Note the tracker ends at 2:47.97, so sync statistics say nothing about those 20 s.
- **Picture's "Part 2's picture holds then cuts on the return".** I accept the 0.1 s figure with the caveat in my own ERRORS history: the drop is at 1:28.62 on the kick grid; a 1 fps frame check cannot confirm sub-second lock, so the claim is "cut within a second of the drop, and the shot list places it about 1:28.5" (M).

## 3. Does one answer the other? Final position

The music does not answer; it **re-sets**. Evidence: new tempo (78 to 120), pedal (D to B, same pitch-class set neighbourhood, no cadence between them), instrumentation (band-led riff and bass against loop-built electronic layers), texture and form (alternating events against a build and dismantling), and a restart of the narration at the date. The only sense of continuity is level: Part 1's end is the loudest part of the pair's first half; Part 2's opening is the quiet start of a longer climb. The one structural echo is the hole device, which I rate as habit, not signature.

## 4. Settled view (5 bullets)

- **Variation, not answer.** Same script, same footage pool, two scores that share no riff, key or tempo (D at 78 BPM; B at 120 BPM). Music is what differs; it re-sets rather than continues (H on the measurements, M on the reading).
- **Two shapes.** Part 1 is a flat, loud, event-by-event band piece (drums constant; events are bass exits at 1:15.3 to 1:40.0, the 0.4 s hole at 2:47.8, the sprint, a 3:08.2 stop). Part 2 is a build-and-unbuild loop piece (pad, bass at 0:28.1, hole at 1:24.3 to 1:28.6, loop B at 2:36.8, plateau, sag 4:36.8, gate 4:48.6, cut 5:00.8, hit 5:02.3). Only loudness spans both.
- **Shared device, shared words, not shown the same take.** The sentence "dat is de Elfstedentocht" and a hole around it appear in both, but cross-correlation is at control level and the hole's placement differs; "rehearsal" and "signature" stay as speculation.
- **Sync.** Neither film locks cuts to the beat grid (Part 2: 36.0% within 80 ms against 31.6%, p = 0.093, on `sync_kickgrid.json`, not the earlier 161.5 BPM figure; Part 1: offset cluster about 0.245 s after the tracker beat, p about 0.006, uncorrected). Joints sit at section changes (Part 2: 0:28.1, 1:28.5, 2:36.6). Moderate, small samples.
- **Open, and honest.** The Part 2 voice fragments as town names are unproven and my structural test leans against (9 bursts, not 11, longer, bar-quantised); nobody has heard the audio, and a Dutch listener plus a human ear on the two ends (relief or restart; whether the 0.4 s hole registers) is the test that would change this view.
