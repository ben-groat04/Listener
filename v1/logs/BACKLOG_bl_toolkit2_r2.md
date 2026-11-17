# Backlog bl_toolkit2_r2 (triage lead, toolkit and docs only)

Checked first (files, not logs): already done: D2 voice_f0/lead_riff split and deprecated lead_notes alias (07), D3 chord templates, D8 14_mix_meters.py, E2 root preflight in 8 workflows, VID mandatory in 01/02/05/08/09/09b/_common, E6 partial (WHISPER_BLACKLIST env in 03), lint_human.py, TOOLKIT/README/CLAUDE human-listening wiring. Still missing: tempo_resolved/form recurrence/modal scores in 04; no bass-root or kick-grid detection script; no voice-as-music script; perceive/listen/interpret/report prompts do not mention FACTS/LISTENING or PROPOSAL 4.4-4.7.

## Selected (6 tasks, no shared files)
| ID | Files | Change | Source/tag |
|----|-------|--------|-----------|
| T1 | v1/scripts/04_audio_features.py | D4 tempo_resolved (kick-grid candidate, backbeat test, downbeat guess, confidence), D6 modal scores + third/seventh evidence, D7 stem-activity novelty + loop length (form.json) | D4/D6/D7 high/medium, all measurement (OBS) |
| T2 | new v1/scripts/11_bass_roots.py | D1 bass-root track and kick-grid autodetect that prints 09b_kick_grid.py args | D1 high |
| T3 | new v1/scripts/12_voice_as_music.py | D5 voice-as-music routine (VAD with bleed rule, f0 vs tonic, phase vs grid, ducking test, logprob filter) | D5 medium |
| T4 | v1/workflows/report.js | PROPOSAL 4.7: FACTS/LISTENING-first inputs, mandatory 'What it is like to listen', 'Where it sits' only from lineage/reception (INFERRED when blind), reception rule A5, compare section A4, context-fact source tags C5, frames-opened N C8 | A1 A3 A4 A5 C5 C8 |
| T5 | v1/workflows/listen.js | PROPOSAL 4.5: groove and body specialist, 'taught before' check in boundary rule 3, music_reading.md as sidecar, reception rule A5 | 4.5, A5, D10 |
| T6 | v1/scripts/check_outputs.py | C6 --chain tag-diff mode, B8 DO_NOT_CLAIM lint of dossier/interpretation, PROPOSAL 4.7.5 body checks for human pieces (tags, 'I felt', 'depends on', word budget) | C6 B8 4.7.5 |

## Remaining
- perceive.js (4.4 forward-only viewer, one-thing line) and interpret.js (4.6 where listeners split, devil's advocate, FACTS/LISTENING first): left for next round, one file each.
- TOOLKIT.md: add 11/12 steps once T2/T3 land.
- 07 per-stem boundary table (L11), D9 per-stem CLAP, D10 banned-noun lint in workflows, E6 generic multilingual blacklist file, 08 CLAP subject-neutral labels.
- make_index.py F1/F2 per-video definitive reading column; agents/ README and move to legacy (outside allowed paths).
- Outside focus: video1 REPORT B1-B13, video2 REPORT, diptych C7.
