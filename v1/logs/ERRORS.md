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

- 02:46 · A cold-read fixer made report.js derive the repo root from __dirname/process, which do not exist in workflow scripts (it would fall back to '.'). · Replaced with args.root or the absolute default. · Tell fixer agents that workflow scripts are plain JS with no Node APIs.
- 02:48 · **Rules check-in 1 (02:45).** Compliant: Sonnet everywhere; conversing panels (interpret, listen debate, compare); adversarial checks on every reading; cold-read loop running; music-first; blind chains on video1, video2, t_birdwalk; usage logged (75%, not edging); commits every 2 min. **Drift found:** (a) only 1 of 3 test videos has reached analysis because CPU extraction (demucs) is the bottleneck; (b) no blind-vs-informed comparison yet; (c) cold-read fixers edited all workflows using Node APIs (fixed); (d) autosave hard-coded the branch name (now uses the current branch). **Course:** queue the blind-vs-informed comparison as soon as blind chains finish; start the remaining test videos as their extraction completes; brief fixer agents that workflow scripts are plain JS.

## Fact-check: video1 interpretation


Visual refutations were re-checked by me against the frames and the mp4 (f_0001, f_0008, f_0029, f_0107, and ffmpeg extractions at 186.0-187.6 s, plus ffprobe); all held. Audio and statistical refutations rest on the checker's own stem measurements, which I did not re-run; they are specific and internally consistent, so I applied them.

Changed (REFUTED):
1. 3:06-3:08 recap: now a four-sign recap (ULST, DOKKUM, BOLSWARD, FRANEKER at about 0.4 s each from 3:06.2), banner at 3:07.4, black at 3:08.1; DOKKUM no longer "on the roll at 3:06.5"; "reverse order" claim removed (re-checked: strip of frames at 186.0, 186.3, 186.7, 187.1, 187.6 shows ULST, DOKKUM, BOLSWARD, FRANEKER, banner). Also fixed the FRANEKER time in section 5 and the "DOKKUM on the roll" wording in 3.2.
2. 1fps labels: added a timing caution (up to about 0.5 s out).
3. 0:07: now a lit POSTHUMA sign (re-checked f_0008), not "a black sign".
4. 0:00-0:09: now a grey streaked blur with a dark band above (re-checked f_0001).
5. First live skating: now figures running or walking at 0:27-0:31, first clear skating 0:38 (re-checked f_0029: no skates visible).
6. 0:32 scene: mill-like tower, then a wooden platform on stilts, not a "building on stilts".
7. Sceptic's test: corrected shot-length claims; listed the real cuts; said ties are more than one but statistically modest (p about 0.06). I kept the note that the 1:40 slam lands in a shot that began at 1:39.40.
8. "Lacing skates at 1:46": now a bibbed skater stepping down a ramp (re-checked f_0107: no lacing).
9. Ambulance moved to 2:04.
10. Tea sequence extended to about 2:14.8; ceremony begins visually about 2:15.
11. "Mostly backs..." softened with face-led passages named.
12. Framing: 5:4 (600x480), checked with ffprobe.
13. "Weight and brightness never both on until 2:48": replaced by the corrected statement in sections 2 and 3.6.
14. Sub entries: six (2:01 to 2:32), 2:38.3 is a pitched D2 bass, in sections 2, 5 and 8.
15. "tweehonderd kilometer" at 0:16-0:23: now "half zes" at 0:16.6, a garbled line at 0:19-0:24, 200 km at 0:54.
16. "Voice-free groove 0:32-1:15": now mostly voice-free with four bursts; "three voice exits" now "three big voice exits".
17. "Only place the music clears for the words": softened as in section 2.
18. 0:00-0:09 bass "creep of 22 dB": now enters about 0:04, about -28 dB by 0:07, growing to about 0:20.
19. 1:27 wall "+26 dB": now about +20 dB against the trough, and not brighter than the 1:06 wall.
20. Elfstedentocht "spoken twice": now printed repeatedly, heard clearly once; Whisper hears three mentions, two garbled (sections 1, 2, 5).
21. Refrain time: about 2:44.0-2:48.3.
22. Bass cut: about 1:15.0-1:15.4; held A from about 1:15.6.
23. 1:40 bass step: about -64 to -22 dB within about 0.2 s.
24. 18 januari 1963: no longer "matched" with the newspaper page (re-checked f_0010 and the sheet: only the headline "Elfstedentocht bovenmenselijk zwaar" and "Chaos aan de finish" are legible).

Softened or marked (UNVERIFIABLE): crowd "cheering" at FINISH; "bellows camera"; "bread"; the skater row count and hands; ULST/IJLST; "Stavoren inn"; "minus 16" unit; the Frisian-audience claim; the voice "(measurements only)"; the "only repeating pitched figure" claim; the stereo-width ranking (metric-dependent); loudness figure caveat; the 575/9,500 figures; "sound and picture from different eras". Left unchanged because the checkers could not settle them either: "half zes" as 5:30 (already hedged in section 8), the 3:07 banner last line (already medium confidence), the cut-phase statistics (confirmed against sync.json), the roll length and the 3:08.2 cut (already listed as open in section 8).


## Fact-check: video2 interpretation

Applied after the fact-check. Refutations re-checked by me where cheap: mean luma of f_0216 to f_0218 (3:35 to 3:37: 88, 127, 187, so no dark frame at 3:36), f_0290 to f_0306 (4:49 to 4:51: 135, 137, 126; 4:52: 167; 5:01 to 5:05: 124, 120, 79, 42, 12), and f_0291 opened (trouser legs, boots and a skate-like blade on scored ice). All three held. The audio, shot-list and transcript refutations rest on the checker's measurements and were applied as given (not independently re-run).

Changes:
1. 3:36 to 3:37: removed "dark frame"; now a hard cut at 3:36.7 from a red-hatted skater on a bright lane to an orange-yellow flare over bib 529 (sections 2, 7).
2. Ending fade (section 2, 4.2): dimming starts at about 5:02.5, two-thirds at 5:03, a third at the audio zero, near-black from 5:05, not fully black until about 5:06; "undimmed at the slam" and "full strength at 5:03" removed.
3. "No people" from 4:49: a person's legs and boots at 4:49 to 4:51; no people from 4:52 (sections 2, 3.5, 7).
4. "55 s of non-human ice": now about 12 s of nobody on screen (4:52 to 5:04), preceded by 3 s of legs (3.9, 7).
5. "No one until 0:53": now no people before 0:48, tiny distant walkers from 0:48, foreground from 0:53 (2, 3.5).
6. 3:28.5 cut: now a very close hunched cluster of three or more bibbed backs, a pair in the foreground by 3:29.
7. Shot lengths: 5.2 s holds for 1:28.6 to 2:36.6 (6.2 s for 1:40.6 to 2:36.6), detector-based; 3.0 s after 4:00 against 2.7 s before, so "about the same" only (2, 4.4, 4.8).
8. 1:24.6 to 1:28.6 is not silence: drums and bass dropout while the narrator and pad continue, mix only 2 to 3 dB down; "two silences" now "two rhythm-section dropouts"; the 1:10 event softened to a thinning of an already sparse drum stem (1, 2, 3.3, 5, 7).
9. 4:36.6 row: bass stabs per bar start at about 4:48.6; the voice-like calls from 4:46.6.
10. Sync statistics: replaced 37% against 43% (p 0.8, wrong 161 BPM grid) with the 120 BPM kick-grid figures (36% against 32%, p about 0.09 beat, 0.2 bar), plus the uncorrected early-clustering caveat (3.2).
11. 0:08 cut: meets its strike at 0.27 s early; the 0:12 and 0:24 cuts within 0.02 s; nothing meets 0:20.
12. Top-band brightening: about +22 dB on the other stem, about +3 dB on the full mix (the +8 upper figure dropped).
13. 4:29 to 4:36 phrase: now a quiet high (about G#5) phrase at about 4:31 to 4:35 after a louder mid-register phrase; "wordless" and prominence not shown.
14. "Friesland" removed from the clean narration items; certain only from the board. "schaatsmarathon" downgraded to moderately clear (2, 6, 8).
15. "Flat Dutch" and "male" narration: now a low (about 110 to 150 Hz), flat, dry voice, probably Dutch; sex not established.
16. Calls "exactly one per bar": now one principal hit per roughly 2.0 s bar (seven) with a smaller echo about 0.3 s later.
17. Drum accent before each 12 s cell: reduced to a weak claim (about 17% above other bars; not distinguishable at 4:12.6 and 4:48.6) (4.4, 5).
18. "Bass enters (about 65 dB above ...)": now about -22 dB from silence at 0:28; the 65 dB figure dropped.
19. "Small-gauge home-movie film" and "family or club cine enthusiast": now film of unknown gauge, maker and purpose [READING]/[SPEC] (1, 5, 6).
20. "Modern track fitted to the reel; no sign of a 1963 edit": now a soundtrack of unknown date; the cuts follow its form, so assembly was deliberate; whether a 1963 edit survives is unknowable (6).
21. Board lettering: "hand-lettered" replaced by white capitals on a dark board, manner undecided (1, 6).
22. "No winner and no finish line" as a fact about the event: now what this edit shows (3.4).
23. Banner at 4:45 to 4:48: now a flag with red and white bands and a dark lower band (possibly a tricolour; not confirmed), beside a telegraph post (2, 3.5, 5, 8).
24. 4:28 "uniformed helpers" and "steadying": now coated onlookers with at least one man in a peaked cap (role unclear); at 4:35 a red-hatted skater beside a man in a green jacket; no steadying claimed (2, 6).
25. Field arithmetic (575 and 9,500): stated as the narration's two labels, 94 per cent only if disjoint participants; "ordinary people" marked [SPEC] (3.4, 6).
26. "Establishes a mass long-distance skating event on natural ice": now board plus partly garbled narration plus pictures of mass skating on frozen waterways with cleared lanes [READING] (6).

UNVERIFIABLE items softened: helper steadying; "panting" (now "bent-forward faces"); "fur" collar (now uncertain); the 0:36 specks as people and the 4:36 lane colour in the rhymes list; the 3:24 vanishing-point timing (now 3:25 to 3:28); "legs and blades" at 4:50 (blade seen only at 4:51); the 2:57 skater's sex; the vocal-stem cut time at 1:28 (now stated on a 0.5 s grid); the 161 BPM hi-hat cause (plausible, unproved). Left unchanged because they were already tagged as unknown or speculative: edit causation, narration provenance, nationalities, period clues, flicker and burn source, 12 s lattice design, instrument identity, ending meaning.

## Compare check: elfstedentocht_diptych

Eight errors found in comparison.md and fixed (see its Check log): (1) claimed no town-like list in Part 2 Whisper although nine fragments exist at 3:25.9 to 3:48.1; (2) put the loudness peak at 3:48 instead of the 3:36 to 4:30 plateau (max 4:12); (3) said the picture cuts onto the drop, but one static shot runs through it; (4) listed 1:28.5 as a cut joint, but it is narration ending with no cut; (5) said no drums or bass for 28 s, ignoring low thuds; (6) said shared shots sit where narration is silent, ignoring voice fragments, and ignored the 4:28 road sign; (7) described 3:13 to 4:33 as a from-behind run, but it includes faces and a control point. Cause: summarising from colleague files without re-reading the raw lines. Lesson: re-read the source line before quoting a number or an absence.
- 03:02 · video2 REPORT.md was not saved: the writer subagent's Write call was refused ('Subagents should return findings as text, not write report files') and it complied. Report text was recovered from the journal and saved by hand; it has NOT had the cold-read/revise pass. · report.js now tells writers the file is a repo deliverable, returns the markdown in a field, and uses a saver agent as fallback. · Deliverable files written by subagents need explicit framing plus a returned-text fallback.
- 06:43 · Third container restart (during the limit pause). · RESUME steps; autosave and test-video extraction restarted. · (expected)
- 06:45 · **Rules check-in 2** (fired 04:01 during the limit; handled at 06:45). Compliant overall. Drift: video2 REPORT.md skipped its cold-read revision (writer blocked); reports still one-tier (evidence-heavy); toolkit prompts don't yet include the blind-vs-informed anti-priming lessons; weekly usage (67%) now a constraint the 5-hour plan ignored. Course: two backlog workflows (analysis accuracy/music depth; toolkit/docs/lessons) + resumed t_birdwalk; cap this window at ~80% weekly.

## Music check: t_birdwalk

Errors found in music_reading.md and fixed (see its Check log): (1) invented a bass exit at 2:54.5 (bass actually continues to the fade); (2) said loudness flat at -12 to -14 dBFS though three breaks sit about -18.5; (3) 'N' chord share given as 47.6 per cent (it is 47.6 s, 37 per cent); (4) D4 share 90 per cent (actually 82); (5) bass-hole floor -75 dB (actually about -66, flickering); (6) verse 1 width range too narrow; (7) pub/club listed as a Whisper disagreement though both passes say 'pub'; (8) 'male-sounding' and 'natural reciting pitch' asserted without evidence; (9) other-layer spike given as +12 dB (about +8, one second). Lesson: re-derive numbers from the JSON before quoting; check for sustained, not single-frame, events.

## Fact-check: t_birdwalk interpretation

Errors found in analysis_blind/t_birdwalk/interpretation.md and fixed (see its Fact-check log): (1) credit card said to stay to 3:18 (it ends about 3:15), undermining the length-mismatch argument; (2) hooded man "grinning and pointing at the lens" (raised finger, open mouth); (3) puppet tower "tumbles at 2:21.5" (standing at 2:22, tumbles 2:24-2:26); (4) 2:44 child given a beak not visible in frames; (5) children "flapping" inferred from 1 fps stills; (6) chequered floor claimed for all four dark clips (visible only at 0:12 and 2:36); (7) "bare-room" trio and "teenager" unsupported; (8) puppet beak paired with "we got this new dance" against Whisper word times; (9) verse 1 "drops" to D4 (it rises over an octave from about 113 to 286 Hz); (10) "nothing locks" omitted the weak off-beat clustering (Rayleigh p 0.04); (11) "at home" treated as a literal match despite the "that hoe" pass; (12) drums "densest" 1:34-2:00 (similar at 2:40-3:00); (13) sub-bass 47 per cent below 60 Hz (about 55 per cent of mix over 0:15-0:45); (14) "late-2000s" from MySpace/iTunes alone; (15) "US", pickup and palms over-read; (16) "Southern" club rap asserted without data; (17) puppet "resembles a well-known children's-TV character" (outside knowledge in blind mode); (18) "home-made production" account of the ending stated as explanation. Cause: carrying panel and perceive-note inferences into the synthesis as facts. Lesson: re-open the frame or data row before quoting a timing, a feature of an image, or a statistic, and keep inferences tagged.
