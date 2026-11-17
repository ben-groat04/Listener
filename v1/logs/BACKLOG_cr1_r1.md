# Backlog from cold-read 1, round 1 (triaged)

Status: triaged from ~55 raw findings. Duplicates merged; each item keeps reader and severity.
Verified by the triage lead: v1/analysis/video2 has no REPORT.md; v1/scripts/00_setup.sh loops over "video1 video2" only; all six workflows hard-code `R = '/home/user/Listener'`; v1/scripts/agents/ holds 168 files; v1/analysis/compare does not exist.

Raw-finding claims about numbers (stem onsets, bass roots, tempo) were not re-verified by the triage lead; the task owner must re-check them against v1/data/<video>/ before editing text.

## A. Documentation, entry points and state (editor / engineer)
| ID | Item | Reader | Severity |
|----|------|--------|----------|
| A1 | No single entry point: TOOLKIT.md not linked from CLAUDE.md, README, RESUME; README layout table omits TOOLKIT, RESUME, logs, analysis_blind, REPORT.md. Add "Start here" block. | engineer/editor/human | high |
| A2 | PROGRESS.md is an append-only diary, stale (last entry 02:40); add a "Current state" block at top (done / in progress / not started per video, test videos, blind outputs). Move usage-% and restart noise to logs. | editor | high |
| A3 | No analysis/INDEX (video x REPORT/interpretation/music_reading/blind) with done/partial/missing; per-video INDEX.md listing the four locations; mark final vs working material (REPORT > interpretation > music_reading; rounds are working). | editor | high |
| A4 | TOOLKIT.md / RESUME.md / README overlap; make TOOLKIT the single manual, RESUME reduced to "after a reset"; mark unproduced outputs (comparison.md, BACKLOG_*) as "produced when run". | editor | medium |
| A5 | Empty file v1/analysis/music/video1/specialists/round_2/rhythm.md (0 bytes): re-run or delete and note in method line. | editor | medium |
| A6 | ERRORS.md: split into process incidents (chronological, with lessons) and claim corrections by document; add 10-line "Rules distilled" block; fix ordering (23:58 after 00:08); add video2 interpretation check section or note pending. | editor | medium |
| A7 | Start.txt unexplained; INSTRUCTIONS rule 3 says videos/video.mp4 (add dated note, do not rewrite user text); research part-mapping repeated in several files (make context.md the single home). | editor | low |
| A8 | Generic usage policy in TOOLKIT (stop new workflows at N percent), mark evergreen vs run-specific INSTRUCTIONS items; helper to print window percentage. | engineer | low |

## B. Deliverables missing (human / editor)
| ID | Item | Reader | Severity |
|----|------|--------|----------|
| B1 | video2 (main video) has no REPORT.md; run interpret/report workflows for video2. | human/editor | high |
| B2 | No cross-video diptych comparison (analysis/compare/); Part 1 vs Part 2 piece. | human | high |
| B3 | Blind vs informed comparison not delivered (analysis_blind/COMPARISON.md); diff claims on time/count (ending, loop A form, hole length, voice entry); finish a blind test-video report (t_birdwalk); record real blind run times; leak check in blind_chain.js. | human/musician/auditor | medium |
| B4 | Human-feeling layer: first-person listener narrative (tagged INT) separate from evidence; physical-sensation section; limitation stated once in toolkit docs not every file. | human | high |
| B5 | Two-tier output: plain-language main text with few numbers, evidence appendix; style rule in report/interpret prompts (no unit in main text unless it changes the feel). | human | high |
| B6 | Lineage and cultural context section (post-rock, krautrock/motorik, documentary tradition, Hel van 63, archive-voice nostalgia/hauntology), using lineage.md and cultural_context.md; tagged interpretation. | human | medium |
| B7 | Words/narration: "two audiences" paragraph (Dutch-understanding vs not), translated lines as reading list, delivery claims flagged as inferred; do not call voice "unperformed". | human | low |
| B8 | Process noise in deliverables (retraction history inline in interpretation s8, agent counts); keep deliverables free of process narrative. | human | low |

## C. Factual corrections to video1 REPORT.md and related (auditor) - all in one file set
| ID | Item | Reader | Severity |
|----|------|--------|----------|
| C1 | REPORT repeats refuted claims: "four or five syllables a second"; 2:48-3:08 "loudest" (level with 1:07 peak; 1:40 stretch louder by mean dBFS); bass "creeping in from 0:03" (a step of ~22 dB in 1 s); "for 24 seconds" (about 25 s, faint blip at 1:28); "one chord, D"/"built on one note"; run a fact-check pass and add "Checked against" header. | auditor/editor | high |
| C2 | Voice "held back when the band is at full weight" contradicts transcript (speaks 0:10-0:32 over full band); silent at both extremes. Replace with measured statement. | auditor | medium |
| C3 | "Quietest passage" 1:55-2:38 unsupported; limit to 1:55-2:13 and say one of two thinnest. | auditor | medium |
| C4 | "Nobody ever crosses a finish line"/"nobody smiles" rest on 1 fps sampling; extract 12-24 fps frames around 2:45-2:50 or soften to "in the sampled frames"; "hand-lettered" unsupported; absence claims need dense-frame verification. | auditor/human | medium |
| C5 | Town-list sync overstated ("each name"); seven of eleven signs; use 2:16 consistently. | auditor | medium |
| C6 | Picture/sound correlation overread (r about 0.27, picture leading by seconds); soften PROGRESS "phase-locked". | auditor | low |
| C7 | CLAP misreported (PROGRESS says triumphant/aggressive; actual nostalgic 0.34, triumphant 0.27, aggressive 0.19); context.md lists CLAP under "Confirmed". Add softmax-relative note to README. | auditor | medium |
| C8 | Open items treated as settled across files: sync result vs "rebuild cut list"; tempo 78 vs 78/156 open. | editor | medium |

## D. Music analysis (musician)
| ID | Item | Reader | Severity |
|----|------|--------|----------|
| D1 | video2 ending misstated as one hit; stems show 2 drum onsets (302.357, 302.613 s) and 3 bass onsets (302.357, 302.613, 302.845 s), matching the blind reading. Rewrite ending; add standing diff step for shared claims. (Re-verify onsets first.) | musician | high |
| D2 | No functional harmony layer: bass roots E-E-G-G-D-D / E-G-D (+B tag) loop A, B-B-A-A-D-D loop B from 2:36; Roman numerals in both B and E readings; pad vs bass roots; loop B change at 2:36.8 as real harmonic event. | musician | high |
| D3 | Narrator never analysed as a musical voice (f0, syllable rate, phrase-vs-bar alignment); fragment provenance test for 3:28-4:59; Whisper "MUZIEK" lines flagged as non-events; "twaalfde Elfsteen" plausibly the twelfth Elfstedentocht. | musician | high |
| D4 | video2 sync test used the tracker grid (161.5 BPM), not the 120 BPM / 2.0 s bar grid, and skips the first 42 s; re-run 09_sync.py with a grid override; until then mark "not rhythm-locked" as untested. | auditor | high |
| D5 | Blind and informed readings disagree (loop A form, hole 3.6/4.3 vs 4.6 s, drum stop times, first voice fragment); reconcile from stems. | musician | medium |
| D6 | Tempo/metre ambiguity in 04_audio_features.py (single beat_track); emit drum-stem tempo candidates, half/double-time warning, downbeat estimate; video1 "156 BPM half-time or 78 BPM". | musician | medium |
| D7 | Key detection/chords weak (KS on whole mix); add bass_roots.json step, modal-aware templates, "ambiguous" when top two within 0.05. | musician | medium |
| D8 | No true listening; document "not recoverable" list per report; per-section LUFS for all videos, RT60 probe, phase correlation. | musician | medium |
| D9 | Untested claims in video2 headline text (bar-lock 17 of 21 needs null test, fills, voiced share); tag as L in the song map. | musician | low |

## E. Toolkit engineering (engineer)
| ID | Item | Reader | Severity |
|----|------|--------|----------|
| E1 | 00_setup.sh hard-coded to video1/video2, misses torch/transformers/scipy/numpy, tesseract unused, `|| true` hides pip failure, no import smoke test, no ffmpeg check, no model pre-fetch. | engineer | high |
| E2 | Scripts 01-09 default VID=video2 silently; make VID mandatory; legacy 06_stems.sh and run_chain.sh (hard-coded names, forced `nl`) to scripts/legacy/; document 03_whisper.py args. | engineer | high |
| E3 | Workflows need `dur` by hand; read duration_s from audio_features/summary.json; accept bare names everywhere; extract_all prints ready args JSON. | engineer | high |
| E4 | Gate weak: template context.md passes check_outputs; no atomic writes/.done markers; no pipefail; half-run test videos (t_cshells_cshore, t_dl_mirror.mp4 with no data folder) undocumented. | engineer | high |
| E5 | Workflows hard-code `R = '/home/user/Listener'` (all six); blind mode relies on prompts, context.md sits in tree; helper scripts written to shared dirs. | engineer | medium |
| E6 | scripts/agents/ holds 168 per-video one-off scripts; move to evidence dir with INDEX, promote reusable probes to parametrised library. | engineer/editor | medium |
| E7 | autocommit.sh hard-coded branch and old trailer; commits 766 MB; interval inconsistent with RESUME; long steps need nohup/log-tail instructions. | engineer | medium |
| E8 | Whisper/CLAP: no VAD or no_speech filtering, translate on all videos, PSB-flavoured CLAP labels, language forced; gate on vocal stem, auto-detect language, document clap_extra_labels.txt. | engineer/musician | medium |
| E9 | No cost pre-flight or agent cap; windows fixed 20 s; non-mp4 and no-audio inputs unhandled. | engineer | medium |
| E10 | report.js should check inputs and that REPORT.md exists after writer; remove duplicate TOOLKIT step 5. | engineer | low |
| E11 | Experimental audio-LM script and 09_sync default VID in scripts/; priors leaking into observation sections of informed perceive notes. | auditor | low |

## F. Speech/ASR provenance (auditor)
| ID | Item | Reader | Severity |
|----|------|--------|----------|
| F1 | words.md rates readings "High" from unsaved scratchpad runs; commit stem-run JSONs or downgrade to Medium; drop language probability 1.00; mark "Elfstedentocht" as reconstructed. | auditor | medium |

## Dropped or merged
- Raw "Toolkit not fully video-agnostic" (musician and auditor versions) merged into E1, E2, E5, E8.
- Raw "No single definitive deliverable" merged into C1 and A3.
- Raw "REPORT.md repeats errors" (auditor and editor versions) merged into C1.
- "Process noise" kept low; D8 timbre-identity item downgraded from the raw "central limitation" framing: it is a documentation task, not a fixable one.
