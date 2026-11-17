# Errors and mistakes log

Format: time (UTC) · what went wrong · how it was handled · lesson.

- 23:32 · (pre-v1) First Google Drive download returned a sign-in page because the file was private. · Asked the user to share it; re-downloaded. · Check `file`/content type of any download before trusting it.
- 23:47 · `cd X && (jobs) & pip ...` backgrounded the whole `cd && ...` list, so the following `pip` ran in the old cwd and its log path didn't exist. · Re-ran pip from the right directory. · Put `cd` on its own line before backgrounding jobs.
- 23:55 · Printed a full warning-spammed log (DeprecationWarning x87) into context, wasting usage. · Will always pipe logs through `grep -v Warning | tail`. · Filter noisy logs before reading.
- 23:55 · faster-whisper crashed: installed PyAV version rejects `metadata_errors` kwarg. · Fix by pinning a compatible `av` or feeding numpy audio. · Smoke-test new libraries on a 5 s clip before long runs.
- 00:00 · Committed a ~54 MB WAV (regenerable) and GitHub warned about large files. · Added `.gitignore` for `*.wav`, amended my own unmerged commit and force-pushed (with lease) to my session branch so history stays small. · Ignore regenerable binaries before the first commit.
- 00:05 · REPEATED the 23:47 mistake: `cd X && nohup ... &` backgrounds the cd too, so the next commands ran in the old cwd. · Noticed from 'No such file' errors. · Rule: always put `cd` on its own line (or use absolute paths) when a command backgrounds anything.
- 00:08 · Wikimedia Commons returned HTTP 429 for every media download (shared egress IP). · Switched to Internet Archive CC-licensed music videos. · Have a fallback source for test media.
- 23:58 · Container restarted: killed the video1 music agent, demucs stems, the queued test-video extraction and the autosave loop. · Re-ran 00_setup.sh and restarted the CPU jobs and autosave; music agent to be re-run after the reset. · Background jobs don't survive restarts: after any restart, run the RESUME steps and re-launch jobs.
- 00:05 · Drift: the first workflow gave video 16 viewers but music only 1 agent, against the spirit of a music-understanding goal (user flagged it). · Rebalancing: new audio perception tools and a music-first workflow. · Check the agent allocation against the goal before launching.
- 00:08 · **Visual features silently failed for both videos** (OpenCV 5 dropped `CascadeClassifier`; two OpenCV packages installed). The chain logged the traceback but carried on, and 20 viewer agents ran without colour/motion/cut-beat data. · Pinned `opencv-python-headless<5`, made face detection optional, re-running. · **Verify each pipeline output exists and is non-empty (add a check step) before launching agents on it.**
- 00:38 · CLAP script written against the old transformers API (get_*_features returned tensors; v5 returns ModelOutput) and wasn't smoke-tested before queuing. · Patched with a tensor shim. · Same lesson as 23:55: smoke-test on a short clip before long runs.
- 01:43 · Second container restart (between 00:49 and 01:42) killed autosave and the test-video extraction. · Restored via RESUME steps. · Expect restarts; keep everything idempotent and re-launch on every wake.

## Research corrections (wave 2)
Applied 2026-11-17 to research/{artist_and_tracks,elfstedentocht_1963,cultural_context}.md and data/video{1,2}/context.md. Lesson: do not state an inference (part order, source film, "amateur", "premiere") as fact before checking; tag M/L until sourced.
- Part mapping was "medium, inferred" and official lengths "not found". Corrected: MusicBrainz gives Part 1 3:09 / Part 2 5:04, so video1 = Part 1, video2 = Part 2 at high confidence (video2 file 1.9 s longer, trailing fade).
- Part 2 YouTube link was "not checked live". Corrected: youtu.be/vrPBTwwnpdc is titled "Elfstedentocht Part Two" (PSBHQ). Our video2.mp4 is not confirmed to be that exact upload.
- "Deluxe edition, due 11 Nov" conflated with the 11 Nov 2013 digital release of "Parts 1 & 2" (also described as a Record Store Day single; 7" followed Record Store Day 2014). Corrected wording: autumn 2013; formats are compatible.
- Polygoon/NTS newsreel hypothesis for the narration was too strong. Downgraded to low: PSB credit only the Fries Film Archief; the source films are unconfirmed.
- video2 called an "amateur reel" and video1 "newsreel" without evidence. Now unconfirmed; a sponsor/regional film ("Dit is Friesland", Esso) is also a candidate.
- Archive name: "Fries Film Archief" (2013) is now Fries Film en Audio Archief (FFAA).
- "Premiere" was assumed. Corrected: commissioned for, and booked to perform at, Explore the North, Leeuwarden, 23 Nov 2013; no premiere confirmed.
- Reception was implied to include hauntology/grief readings. Corrected: documented reception is thin and speaks of drive, physical effort and image-sound fusion; the rest is our interpretation.
- PSB tagline ("lessons of the past ... music of the future") unverified; do not cite as a Willgoose quote. "Mr B" visuals credit is for live shows only; no edit credit for these videos.

## Music check: video1
- Read Dutch "half zes" as 6:30; it means 5:30.
- Claimed speech "only" at Whisper times; the vocal stem has other bursts (1:46.7, 1:57) and a doubtful 1:03.5 one. Whisper segment starts used as onsets though vocal-stem onsets differ by 0.5 to 0.8 s.
- Misquoted figures: melody timings, chord order (F before C), width range, bass entry (0:03, not a creep), ending levels, tempo "no drift" beyond the end of beat_times (2:48), stop durations (bass 0.65 s).
- Overstated CLAP "distorted guitar" (0.6 to 1.0 throughout; real: top label in about a third of windows, mean 0.44).
- Town list filled from route knowledge; dropped Hindelopen which Whisper did transcribe.
- Voice spectral figures (3.7 kHz, 4 to 5 dB under band) stated without per-passage checking.
- 02:14 · Push rejected: agents and the autosave loop push concurrently, so the remote moved. · Fetched + merged, pushed; autosave now fetch-merges on rejection. · Concurrent writers need merge-on-reject.
- Video1 reading: summary.json chord_time_share_top10 is in seconds; I called D "94.3 percent" (it is 50 percent of chord time).
- Video1: called the 2:47.8 cut "one bar / 1.2 s" (it is 0.4 s) and the 2:37 click "absent for six beats" (it is about 10 dB weaker, 2:38.7-2:43.7); claimed drums and bass cut together at 3:08.2 (drums fade about 0.4 s first); quoted ending levels not reproducible at 0.1 s.
- Video1: "centred on D" ignored A-led pitch classes in 2:13-2:38; "settles on D" from 2:38 ignored CH noise labels; held A/C timing and 1:15-1:24 extent wrong versus chroma.
- Video1: width ranges, drum swell span, onset rate (4.3/s) and "no drift" (tracker ends 2:47.97) misquoted.
- Video1: treated "Elfstedentocht" as Whisper output in the first block (it is Elfstedentuin there), put MUZIEK at the wrong bursts (it is 1:42 on a silent stem), assumed one place name per bar, and stated "low male" voice from an f0 overlap range; leaned on CLAP guitar/mood tags as support.

## Music check: video2
- Attributed the 0:42 top-band jump (about 26 dB) to a filter or layer opening with speech; it is the narrator's voice entering (the vocals stem shows the same jump, the "other" layer rises only about 8 dB).
- Called A to D a minor third (it is a perfect fourth); quoted loop A lifts wrongly.
- Intro harmony: wrote a 4 s D tip with a return from window notes; chroma shows D-rich spans at 0:08 to 0:14 and 0:20 to 0:24, G spans elsewhere and a turn to E at 0:24 to 0:28.
- Called a -47 dB vocal-stem blip at 3:24.8 the first wordless fragment; real fragments start at about 3:28.6.
- Put the loss of the pad's D third at 4:48.8; it fades at 4:36.8.
- Asserted sixteenth hats from 3:40 without a measurement; no step is found.
- Small timing errors: hole bass silence 3.6 s not 4.0, drums 4.3 s; loudness peak -9.9 is a 12 s mean; gate onset 4:48.55.
- Wrote that "both Dutch passes" and a Dutch detection (p = 1.00) agree; there is one forced-Dutch pass and the language probability is a placeholder. Overstated agreement of words (Elfstedentocht never transcribed).
- Left out supported narration at 1:00 to 1:14 ("200 km through Friesland") and called it unclear; also called a "misread" what is contradictory across passes.
- Ending misread as a quiet "tap": it is a full-level kick-and-bass hit at 5:02.3 after a pad ring-out.
- Cited CLAP only as song means (vinyl crackle, instruments, no-vocals), hiding strong time structure; overstated "no vinyl" and bass "28 dB down".
- 02:30 · Audio-language model (Qwen2.5-Omni-3B on CPU) failed: audio not received (config/token mismatch) and ~15 min per window. Wasted ~25 min of CPU, no usage. · Abandoned; script kept as experimental_10_audio_lm.py with a warning; deleted its misleading output and the 8 GB model cache. · Budget a quick feasibility check (speed + a sanity answer) before building around a heavy local model.
- Check round 2 (video2 music reading): called the last hit the loudest sample (the track is at 0 dBFS from about 1:20); digital zero at 5:04.4 (it is 5:04.24); omitted the 0:24 strike (five strikes, not four).
- Described the 1:10-1:16.5 stop as drums and bass (only drums drop; both are absent only about 1:24.6-1:28.6, about 4 s); trusted Whisper's 1:14 narration end (vocal stem ends about 1:10.5).
- Called a 4:37 "bass hole" (bass stem is -19 to -20 dB there); placed the end of the last B-A-D cycle at 4:44.7 (it is 4:48.6); fill list included 2:56 and missed about 1:56 and 3:00.
- Quoted stem-only brightening (+22 dB at 4-10 kHz) as a property of the whole wall/mix (the mix gains about +3 to +8 dB); gave "L/R correlation about 0 in every band" (true only in the intro); intro chroma timings of G (G absent at 0:00-0:04, back at 0:16).
- Called the second-half voice "murmur / very quiet / wordless" and "high" confidence human voice: the vocal-stem bursts peak about -16 dB; no words recovered is not the same as wordless; CLAP "no vocals" contradicts; "guitar vs synth 50:50" had no evidence; "calls uniform about -21 dB" (spread about 4 dB); "bass 50 dB louder" (about 65 dB, from noise floor).

## Fact-check: video1 interpretation

- Overclaimed "the only direct look to the lens in the film"; several other people look at the lens (0:15, 0:27, 0:31, 2:43-2:44) and two of five at 1:58.
- Counted "eight town signs"; frames show six town/route signs (seven showings).
- Said "five dots at 1:32" (six or seven figures); "bibs the only light" (lamps, newsprint, faces too); newspaper dated 0:22 (it is 0:23-0:26); "bridge at 1:47" (a wooden ramp, no bridge); pack close-ups "from 1:06.6" (from about 1:05).
- "Drums never change gear" contradicted the document's own brightness claims: pattern and grid are fixed, timbre changes.
- Called 2:48-3:08 the loudest stretch (equal to 1:07-1:15 within 0.1 LU); said the 1:40 bass return adds 0.1 LU (ebur128 gives 0.2-0.5); called 1:40-1:55 "loudest" in raw dBFS only.
- Narrator "steady 4 to 5 per second, no quickening" (varies about 25%); Whisper gap at "Leeuwarden" 3.6 s not 3 s; chord changes placed with the bass return (they precede it by about 1 s); bass gap 24 s (about 25 s); town-list start given inconsistently (2:15 vs 2:16).
- Process: the fact-checker's frame filenames for 1:46-1:48 were off by 60 (f_NNNN is second NNNN-1); check the number against the timestamp.

## Fact-check: video2 interpretation

- Trusted the shot list: put the drop at 1:28.6 over a 1.7 s picture hold and an 8.2 s hold at 1:22; the cut is at about 1:28.5 (no cut at 1:22.1, which is a tint swing). Also took the 252 to 260 s shot as one 8.16 s hold (it has a hard cut at about 254.55 s) and counted long holds from a list that hides cuts.
- Frame-time slips: golden skater placed at 4:11 to 4:14 (face 4:10.3 in a separate shot, skater 4:10.5 to 4:12.0); bobble-hat at 0:59 to 1:01 (about 0:59.6 to 1:01.7); "empty road" listed for frames with people; curved mark given as 3:00 to 4:36 (2:49 to 4:46); "only modern footage" at 2:36.6 (cars at 2:04 to 2:12); "mostly inside the pack" after 2:36 (about 85 s of 150 s).
- Audio overstated: mix "steps" at 1:28.5 and 3:36 (second step about 1:40; none at 3:36); bright-layer ramp "by 2:45" (recovery from a mute; real rise from about 3:10); narration start 0:41 and "40 s of pad" (0:42.5; pad alone 28 s); "half zes" as H (p 0.49); "17 of 21" bar-locked fragments (about half of about 29); "thirdless" pad as H; width 0.9 to 1.0 at 1:13 to 1:24 (mostly 0.7 to 0.85); B Aeolian as H (bass E-G-D is ambiguous).
- Facts: 2012 cancellation reduced to "2 cm of ice"; 575 and 9,500 called "pre-race entry-style" and "close to 568" (sources give 568 or 577); "-16 to -18" attributed to sources (-16 is the narrator's); "a generation" gloss (22 years to 1985); spelled-out date and "wedstrijdrijders" presented as heard (Whisper gave digits; "wedstrijd-" is a restoration).
- Process: quote Whisper timestamps only after checking the vocal stem; check a shot-list cut against frames before building an argument on it.

