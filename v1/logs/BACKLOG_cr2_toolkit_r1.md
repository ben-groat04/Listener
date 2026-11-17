# Backlog: cold-read round 2, toolkit (r1)

Triage of ~55 cold-read findings, deduplicated into themed items. Format: ID | severity | reader | item | files.
Dropped as trivial or duplicate: stray zero-byte rhythm.md (merged into B7), duplicate PROGRESS diary lines (merged into E4), CLAP timbre descriptors (kept low as M9), 'tag chain' and 'frame manifest' merged into S3.

## A. Report quality (human reader)
- A1 | high | human | Finished informed reports lack the first-person 'What it is like to listen' layer (only t_birdwalk has it). Re-run report.js on video1/video2; gate in check_outputs.py. | analysis/video{1,2}/REPORT.md, workflows/report.js, scripts/check_outputs.py
- A2 | high | human | Tier 1 is over-technical and over-hedged (Hz, %, p=, r=); move stats to the appendix; lint Tier 1 for number+unit; limitation statement at the end. | report.js, check_outputs.py, REPORT.md files
- A3 | medium | human | No genre/lineage 'Where it sits' paragraph; lineage specialist output is not surfaced. Take only from the specialist round or research; label INFERRED for blind. | report.js
- A4 | medium | human | Reports do not read as halves of one work; make compare section mandatory when a comparison exists, with reciprocal links. | report.js, README/make_index.py
- A5 | medium | human | 'Listeners feel...' claims lack reception evidence; rule: cite reception, state a musical mechanism, or label 'my reading'. | listen.js, interpret.js, report.js prompts
- A6 | low | human | README should list t_birdwalk REPORT as the unknown-video example; finish reports for t_cshells_cshore and t_dl_mirror. | README.md, analysis_blind/*

## B. Factual accuracy of video1 deliverables (auditor)
- B1 | high | auditor | REPORT ending lists IJlst/Bolsward/Franeker signs in the sprint; only DOKKUM (3:06, reused) is shown. | video1/REPORT.md
- B2 | high | auditor | 2:49 'bibbed skater held among officials' not in frame f_0170 (peaked-cap man from behind, camera-like object). | video1/REPORT.md
- B3 | medium | auditor | Sync wording: on-beat share 7.8% vs 19.7% chance; only single-beat Rayleigh p=0.0055 (n=39); r=0.27 untested; busiest cutting 1:06-1:16 and 2:58-3:08. | video1/REPORT.md
- B4 | medium | auditor | Tempo: tracker local range 78-152 BPM, median beat interval 0.766 s; 'never changes speed' is inferred from stems. | video1/REPORT.md
- B5 | medium | auditor | 575 / 9,500 from one unchecked Whisper pass (official 568 / 9,294); write 'transcribed as ... (ASR, unconfirmed)'; run Whisper on vocals stem. | video1/REPORT.md, data/video1/lyrics
- B6 | medium | auditor | 'A crowd is gathering' is not in the transcript; translate pass mis-renders 'half zes' as 6.30. | video1/REPORT.md, context note
- B7 | medium | auditor | Town word-to-picture match overstated (IJlst unconfirmed, Hindeloopen unshown, ASR timing spread up to 3 s). | video1/REPORT.md
- B8 | medium | auditor | Dossier breaks DO_NOT_CLAIM 1-4 (fur, middle-aged woman, policeman, hand-painted); add lint. | video1/dossier.md, check_outputs.py
- B9 | low | auditor | 'Two of five' tea-table viewers look at the lens: only one clearly does (f_0121). | video1/REPORT.md
- B10 | low | auditor | 'Widest and brightest' sprint and loudest-stretch wording (loudest 1:40-1:55, peak ~-9.5 dBFS at 1:52). | video1/REPORT.md
- B11 | low | auditor | 'Seven specialist notes' includes empty round_2/rhythm.md; 'no editing tricks measurable' unsupported. | video1/REPORT.md, specialists/round_2/rhythm.md
- B12 | high | sceptic | Known frame misreadings still stand (f_0188 hall banner 'parterre', 'raising a fist', Paping unreadable, FINISH vs start, 0.5 s label offset). | video1/dossier.md, interpretation.md, REPORT.md
- B13 | medium | sceptic | REPORT silently changes dossier observations without [changed: reason]. | REPORT.md

## C. Provenance, priming, tags (sceptic)
- C1 | high | sceptic | context.md 'Listening priors' hand informed agents the expected feeling; move to priors.md read only post hoc. | data/video*/context.md, perceive.js, interpret.js, report.js
- C2 | high | sceptic | video1 REPORT has no tags or Tier 2 appendix; regenerate; tag gate. | REPORT.md, report.js
- C3 | high | sceptic | Frame-evidence citations missing (video2 REPORT cites none; dense 12 fps frames not stored). | REPORT.md files, report.js
- C4 | high | sceptic | Anti-priming guard is honour-system; freeze literal frame notes with hash before context release; cold viewer should read blind music reading. | perceive.js, interpret.js, blindcmp.js
- C5 | medium | sceptic | Context facts in openers lack source/confidence markers. | report.js
- C6 | medium | sceptic | Tag lowering/hardening not checked across stages; add --chain mode. | check_outputs.py
- C7 | medium | sceptic | Diptych comparison lacks evidence-class column. | compare/elfstedentocht_diptych/comparison.md
- C8 | low | sceptic | Absence claims: record frames opened (N) per claim. | report.js, frame_at.py

## D. Music analysis tooling (musician)
- D1 | high | musician | Bass roots, kick grid, voice-as-music have no scripts in repo; promote to numbered, VID-parameterised steps (11-13), move agents/ probes to legacy/. | scripts/
- D2 | high | musician | lead_notes is the vocals-stem pitch track (speech on PSB); split voice_f0.json and lead_riff.json (other stem, basic-pitch). | 07_audio_views.py, listen.js
- D3 | high | musician | Chord detector triad-only; beat grid ends at 167.97 s giving a 20 s artefact; add power/sus/7 templates, extend grid, report root vs quality confidence. | 07_audio_views.py
- D4 | high | musician | Tempo/downbeat: re-run 04 on all videos; add tempo_resolved (kick grid, backbeat test, downbeat guess); 09_sync to use it. | 04_audio_features.py, 09_sync.py
- D5 | medium | musician | Voice-as-music routine (VAD with bleed rule, f0 vs tonic, phase vs grid, ducking test, Whisper logprob filter). | new script, listen.js voice prompt
- D6 | medium | musician | Modal reading (pitch-class histogram, per-mode scores, third/seventh evidence, key_ambiguous). | 04_audio_features.py
- D7 | medium | musician | Form: stem-activity novelty and recurrence/loop-length (form.json); auto-sections as secondary. | 04, listen.js form prompt
- D8 | medium | musician | Mix meters script (LUFS, true peak, crest, band energy per stem, L/R correlation, long-FFT sub peak). | new 14_mix_meters.py
- D9 | low | musician | CLAP weak for instruments; per-stem timbre descriptors; caveat once. | 08_clap_tags.py, sound prompt
- D10 | low | musician | 'heartbeat' etc. used in music_reading.md despite rule 6; deterministic banned-noun lint in workflows. | music_reading.md, listen.js, report.js

## E. Engineering robustness
- E1 | high | engineer | Disk 100% full (121M free); add free-space preflight (>=2 GB) to 00_setup.sh and extract_all.sh; document cache cleanup and per-minute disk need. | 00_setup.sh, extract_all.sh, TOOLKIT.md
- E2 | medium | engineer | Workflows default root to /home/user/Listener while comments claim a fallback; document args.root, fail loudly if R/v1/scripts missing; correct PROGRESS T5 claim. | workflows/*.js, TOOLKIT.md, RESUME.md
- E3 | medium | engineer | Usage policy contradictory (INSTRUCTIONS 4/11/23 vs TOOLKIT 85% vs CLAUDE); one resolved paragraph plus fallback if rate_limit_event unavailable. | INSTRUCTIONS.md, TOOLKIT.md
- E4 | medium | engineer | No cost guard; add per-minute agent/token table and quick/budget arg; max recommended duration. | TOOLKIT.md, listen.js, perceive.js
- E5 | medium | engineer | Model downloads/network needs undocumented; pre-download in setup; list hosts; Python version. | 00_setup.sh, TOOLKIT.md
- E6 | medium | engineer | Whisper hallucination blacklist is Dutch/English and video-specific; generic multilingual list + per-video file; instrumental case test. | 03_whisper.py, check_outputs.py
- E7 | medium | engineer | autocommit.sh hard-codes another session's attribution and commits heavy regenerable data; use env var; gitignore frames_1fps/contact_sheets/mp3 stems; surface push failures. | autocommit.sh, .gitignore, RESUME.md
- E8 | low | engineer | Context stage has no recipe (research.js), BLIND=1 undocumented in TOOLKIT, 'no external sources found' template. | TOOLKIT.md, extract_all.sh
- E9 | low | engineer | Restart fragility: demucs partial vocals.wav passes as complete; failed step log only in .raw; python3 -m pip; drawtext font check; one extraction at a time. | 06_stem_one.sh, extract_all.sh, 00_setup.sh
- E10 | low | engineer | frame_at.py, 10_onscreen_text.py missing from docs; CLAP sound labels subject-specific. | TOOLKIT.md, README.md, 08_clap_tags.py

## F. Docs and status (editor)
- F1 | high | editor | PROGRESS state table, INDEX and filesystem disagree; make make_index.py the only status source, add blind REPORT column, check stems and music_views separately. | PROGRESS.md, analysis/INDEX.md, scripts/make_index.py
- F2 | high | editor | Definitive reading per video not named (README 'if present' hedge); per-video table; mark working files; LESSONS.md status column. | README.md, INDEX.md, blind_vs_informed/LESSONS.md
- F3 | medium | editor | TOOLKIT.md stage order muddled; single args table; usage up front. | TOOLKIT.md
- F4 | medium | editor | Stray files (analysis_blind/video1 whisper/seg files), logs/ clutter, agents/ README. | analysis_blind/video1, logs/, scripts/agents/
- F5 | medium | editor | INSTRUCTIONS item 3 path stale; ERRORS.md needs distilled top rules and split of per-video logs; CLAUDE.md 'read in this order'. | INSTRUCTIONS.md, ERRORS.md, CLAUDE.md
- F6 | medium | editor | No record of the cold-start proof; 'Status of the proof' section; t_birdwalk duration mismatch. | TOOLKIT.md
- F7 | low | editor | PROGRESS diary: split into state plus DIARY.md, unique ids, remove duplicate. | PROGRESS.md, logs/DIARY.md
