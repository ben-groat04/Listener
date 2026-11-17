# Progress

## Current state (verified by ls of v1/analysis and v1/analysis_blind)
Final pieces: REPORT > interpretation > music_reading (see [analysis/INDEX.md](analysis/INDEX.md)). done = file exists; partial = some units only; missing = not produced.

| Video | REPORT | interpretation | music_reading | blind equivalent | compare |
|---|---|---|---|---|---|
| video1 | done | done | done | done (interpretation, music_reading, perceive) | partial (diptych round_1 only) |
| video2 | missing | done | done | partial (music_reading and perceive done; interpretation only dossier + panel rounds 1-2) | partial (diptych round_1 only) |
| t_birdwalk | missing | missing | missing | partial (blind perceive only) | n/a |
| t_cshells_cshore | missing | missing | missing | missing (data extracted only) | n/a |
| t_dl_mirror | missing | missing | missing | missing (not extracted) | n/a |

Superseded/uncertain: the 02:00 sync entry below was computed on the tracker's beat grid (median beat interval 0.372 s for video2, with the 161/80 BPM ambiguity). A re-run on a 120 BPM kick grid (median interval 0.5 s; `data/video2/sync/grid_120bpm.json`, `sync_kickgrid.json`; `sync.json` is untouched) is the better basis, and the video2 kick-grid issue (which grid is right, and whether the 2.000 s bar period is a true lock) is still open. In both grids cut-on-beat share stays near chance (0.37 vs 0.43; 0.36 vs 0.32). Read `analysis/video2/interpretation.md` section 8 for what remains uncertain; do not rely on the 02:00 numbers.

The diary below is **history**, kept as written (apart from marked corrections); it can contradict the table above, and the table wins.

---

## Prep phase (before the 01:40 UTC usage reset; kept light on purpose)
- 23:38 Usage checked: 5-hour window 80% used, resets 01:40 UTC. Weekly 52%.
- Extracted video2: audio (wav), 306 frames at 1 fps, 16 contact sheets (20 s each, timestamped), 87 shots + keyframes, music features (tempo ~161/80 BPM ambiguity, key est. B minor / D major, 10 auto sections), spectrogram.
- First lyrics pass (whisper small, auto-language) shows the "vocals" are mostly **Dutch archival radio/TV-style narration about the Elfstedentocht of 18 January 1963** (-16 °C, ~200 km, "only the strongest"), plus a chant-like sung section at ~3:32–3:58 ("Stuck… End of the road… Climbing up").
- 23:42 User uploaded the **predecessor** video. Renamed original to `video2.mp4`, added `video1.mp4` (188.7 s).
- Running: video1 extraction, visual features for both, Dutch transcription + English translation (whisper medium) for both.

## Next (after reset)
- Multi-agent workflows: per-segment viewing agents (read contact sheets/keyframes like a viewer), music listeners (from features/spectrogram/lyrics), historical-context researchers, then conversing interpretation panels (debate rounds), synthesis, and cold-read critique loops.

## 23:50 Research done (pre-reset, Sonnet)
- **Artist identified:** Public Service Broadcasting, "Elfstedentocht Part 1" (video1) and "Part 2" (video2), 2013, commissioned by Explore the North (Leeuwarden) for the 50th anniversary; footage and voice-over from the Fries Film Archief. Files: `analysis/research/{artist_and_tracks,elfstedentocht_1963,cultural_context}.md`.
- Toolkit made video-agnostic: `scripts/extract_all.sh`, `workflows/perceive.js` (args: videos list), per-video `data/<video>/context.md`.
- 23:52 Launched perceive on video1 (10 segment viewers + music listener).

## 00:00 Pre-reset batch 2
- Container restarted at 23:58 (lost the music agent, stems and autosave; recovered via RESUME steps).
- video1: all 10 segment viewer notes done. Now running: video1 music + words, video2 segments 1-8.
- Wrote `workflows/interpret.js`: dossier -> 3-round conversing panel (first-timer, film critic, music critic, insider, symbolist, sceptic) -> moderator -> 3-lens adversarial fact-check -> fixes. Supports `blind: true`.

## 00:10 Music-first rebalance (user: focus more on the music)
- video2 segments 1-8 viewed; video1 music + words done (run without stems/visual data, see ERRORS 00:08).
- New CPU tools: `06_stem_one.sh` (demucs stems for any video), `07_audio_views.py` (per-20 s stem spectrogram windows, chords, lead melody, levels/stereo width), `08_clap_tags.py` (CLAP zero-shot genre/instrument/mood/voice/sound tags every 5 s), `check_outputs.py` (pipeline completeness gate). All wired into `extract_all.sh`.
- Fixed silent failure of visual features (OpenCV 5). Re-running for both videos.
- Next (after reset): music-first workflow (per-section listeners + specialist music panel), then interpret panel, cross-video comparison, blind runs, test videos, cold-read loops.
- 00:26 video2: all 16 segment notes + words.md done. A viewer questions whether video2 is really "Part 2" (context says Part 2 is calmer/electronic, but 3:20-4:00 is a loud dense plateau). **Must be verified** in the music/research phase.
- 00:45 Music tools complete for both videos (check_outputs OK). CLAP: video1 = post-rock, distorted guitar, announcer speech, mood nostalgic 0.34, triumphant 0.27, aggressive 0.19 (correction: earlier text said only "triumphant/aggressive"); video2 = synth-pop/electronic/krautrock, drum machine, "nostalgic/calm". Chords: video1 centred on D, video2 on B minor. Supports research's Part 1 (rock) / Part 2 (electronic) order. Launched video1 window listeners (listen.js, windows_only).
- 00:45 video1 music window notes done (10). Holding at 97% usage until reset.
### Plan from 01:42 (post-reset)
1. listen.js: video2 windows, then specialists + debate + reading + checks for both videos.
2. interpret.js on both (panel reads the music reading first).
3. Cross-video diptych comparison (Part 1 vs Part 2) incl. verifying which is which.
4. Blind runs (listen + interpret with blind=true, out=analysis_blind) on the PSB videos and the test videos; compare blind vs informed.
5. Cold-read improvement loops on the analysis and on the toolkit (can a fresh session run it from TOOLKIT docs?).
6. Toolkit entry doc + single command; final human-readable report per video.
- 01:52 Research wave 2: **Part mapping confirmed** (MusicBrainz: Part 1 = 3:09 = video1; Part 2 = 5:04 = video2). Archive = Fries Film (en Audio) Archief; specific films/narrator unidentified. Reception thin but positive (live highlights 2014). Applying corrections; launched blind chain for video1.
- 02:00 (SUPERSEDED/UNCERTAIN, see Current state) New `09_sync.py` (music-picture relationship). **Finding:** video1 cuts are phase-locked to the beat (Rayleigh p=0.006, mean phase 0.32 of a beat: tracker phase offset, cuts on the pulse); video2 cuts are not rhythm-locked (p=0.82). Cut rate rises with loudness in both (r~0.25). Wired into interpret/compare/perceive prompts and extract_all/check_outputs.
- 02:10 video1 music reading done (25 agents, 2.6M tokens; checks refuted 16 claims and flagged 16 unverifiable; fixes applied). Launched interpret on video1. Trying Qwen2.5-Omni-3B as a CPU audio-language 'second pair of ears' (scripts/10_audio_lm.py).
- 02:25 video2 music reading done (41 agents, 4.0M tokens; 14 refuted/14 unverifiable, fixes applied). Launched interpret video2 and blind chain on test video t_birdwalk (first blind test on an unknown video).
- 02:33 video1 interpretation done (24 agents; 16 refuted/36 unverifiable, fixed/softened). Added report.js (readable final piece + 2 cold reads + revision); running on video1.
- 02:40 video1 REPORT.md written (earlier writer step had produced no file; both cold reads failed on the missing file, so their valid music-reading style points were applied directly: felt lead, 1:40 catharsis, riff by feel, caveats once). Not independently re-reviewed.
- 02:40 T1: video1 REPORT.md fact-fixed against per_second_levels/transcripts/sync (voice syllable claim removed; 2:48-3:08 level with 1:07 peak; bass 0:03 step; ~25 s gap with 1:28 blip; measured speech/silence spans; quietest limited to 1:55-2:13; finish/smile/hand-lettered softened; seven of eleven towns, start 2:16; weak sync r 0.27; dB jargon trimmed; 'Checked against' header added).
- 02:42 T3: 09_sync.py now needs VID (no default), takes --grid/GRID_JSON, --bar-s, --out, and adds block/circular-shift permutation p for cut-rate vs loudness plus a first-42 s block; new 09b_kick_grid.py; video2 kick grid (v1/data/video2/sync/grid_120bpm.json) and sync_kickgrid.json written (sync.json untouched); 04_audio_features.py emits summary.json 'tempo_candidates' when a drums stem exists (not re-run on existing data).
- T2 (cold-read backlog D1, D2, D9): rewrote video2 ending as a multi-hit tag (re-measured onsets, blind agrees), added Functional harmony block (bass roots re-measured, B/E Roman numerals, pad vs bass), L-tagged untested items in music_reading.md; bar-lock re-test: Rayleigh p~3e-6 (n=27) at 2.000 s period but '17 of 21 before bar line' not reproduced.
- T5 (backlog E3/E5/E10): workflows no longer hard-code the repo path (root = args.root, else two dirs above __dirname, else cwd); bare video names accepted everywhere and dur auto-read from audio_features/summary.json; compare/report defaults generic; report.js preflights inputs and verifies/retries REPORT.md; blind_chain.js runs a context-term leak check (v1/analysis_blind/leak_check_<vid>.md). Syntax-checked only, not run.
- T4 toolkit hardening: 00_setup.sh loops all videos in videos/, testvideos/, $VIDEO_DIR (any of mp4/mkv/mov/webm), installs v1/requirements.txt (torch, transformers, scipy, numpy added), checks ffmpeg, ends with an import smoke test; extract_all.sh uses pipefail, .done markers, audio-stream check, BLIND=1 (no context.md) and prints workflow args JSON; check_outputs.py gained --blind, stems_raw/window/frame-count/template-context checks; VID mandatory in 01,02,03,05,06_stem_one,07,08 (new scripts/_common.py); 06_stems.sh and run_chain.sh moved to scripts/legacy/, audio-LM script to scripts/experimental/10_audio_lm.py; 03_whisper.py documented and writes *_doubtful.txt. 04 and 09 untouched. NOTE: check_outputs now flags t_birdwalk (summary duration 188.2 s vs file 201.4 s, 201 frames) and t_cshells_cshore (incomplete).
- T6 (backlog A1-A4, A7, C7, C8): entry docs rewritten (README 'Start here' + full layout, RESUME shortened with 2-minute autocommit, TOOLKIT quickstart), Current state table and INDEX.md added, CLAP figures corrected and moved under 'Weak model evidence' in both context.md files, CLAUDE.md links TOOLKIT.md, stray Start.txt (initial-commit placeholder 'start') deleted. No scripts or analysis prose changed.

## 02:55 Cold read cr1 done (18 agents). Backlog: `logs/BACKLOG_cr1_r1.md` (~55 findings triaged; 6 fixed+verified this round).
### Plan for the next window (after 06:40 reset)
1. **Accuracy first:** fix backlog C1-C8 (refuted claims leaking into REPORT; CLAP misreport; absence claims need dense frames) and D1, D4 (re-run 09_sync.py for video2 with the correct bar grid before claiming "not rhythm-locked").
2. **Music depth:** D2 functional harmony (bass-root loops, Roman numerals), D3 narrator as a musical voice (f0, syllable rate, phrase-vs-bar).
3. **Human layer:** B4/B5 two-tier reports (plain felt prose + evidence appendix), B6 lineage/culture section.
4. blindcmp.js on video1, video2, t_birdwalk; then LESSONS applied to prompts.
5. Remaining test videos (t_cshells_cshore, t_dl_mirror) blind chains once extraction finishes.
6. Docs: single entry point (A1-A4), current-state block, analysis INDEX.
7. v2 cold start: a fresh session/agent runs TOOLKIT.md end-to-end on a test video to prove the toolkit works cold.
- 02:50 Blind video1 chain done (71 agents; interpretation checks 26 refuted/33 unverifiable). Blind run identified subject from narration + printed headlines alone.
- 02:58 Blind video2 chain done (83 agents; 28 refuted/31 unverifiable). Launched blindcmp on video1+video2.
