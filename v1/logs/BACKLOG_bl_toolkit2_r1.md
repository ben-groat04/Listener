# Backlog bl_toolkit2_r1 (triage lead, toolkit and docs only)

Checked first: cr2 items already fixed in files: D3 chord templates (07_audio_views.py QUAL), E7 autocommit.sh (env trailer, push log), E9 stem completeness check (06_stem_one.sh), E1/E5/F6/cost table in TOOLKIT.md, T1-T6 of bl_toolkit_r2 (frame_at, 10_onscreen_text, etc.). VERDICT.md/PROPOSAL.md lessons not yet in TOOLKIT.md/README/CLAUDE.md (plainvoice.js unmentioned; listening.js listed as 'f' after the others).

## Selected (6 tasks, no shared files)
| ID | Files | Change |
|----|-------|--------|
| T1 | TOOLKIT.md | Pipeline order: FACTS.md -> listening/plainvoice = main human output; measurement = checking layer; Turing test vs real human writing = acceptance test; add plainvoice/human.js; E2 root note |
| T2 | v1/README.md, CLAUDE.md | Same lessons in entry docs; definitive human reading per video; Turing history link |
| T3 | v1/workflows/{blind_chain,blindcmp,coldread,human,interpret,listen,perceive,compare}.js | E2 root preflight, fail loudly if R/v1/scripts missing |
| T4 | v1/scripts/02_scenes.py | L8 detector misses blurred whips (video2 88.3-88.7 s); fix, re-run, compare; 09_sync re-run to a separate --out |
| T5 | new v1/scripts/lint_human.py | Deterministic lint of a human piece (clock times, banned craft words, scaffolding, hedges) and stats vs the real-human corpus |
| T6 | new v1/scripts/14_mix_meters.py | D8 mix meters; settles B10 (loudest stretch, peak) for video1/video2 |

## Remaining
- D1 (bass roots/kick grid numbered steps, agents/ to legacy), D2 (voice_f0/lead_riff split), D4 (tempo_resolved), D5, D6, D7 (04_audio_features.py, 09_sync.py), D9, D10.
- VID mandatory in 01,02,05,08 (E2 scripts), E6 hallucination list genericity.
- listen.js/perceive.js/interpret.js/report.js: forward-only reading, FACTS-first wiring (PROPOSAL 4.4-4.7), A1-A6 report items; report.js gating on LISTENING.md.
- F1/F2/F4/F5/F7 doc tidy (PROGRESS split, INDEX per-video definitive reading, agents/ README).
- Outside focus: video1 REPORT corrections B1-B13, video2 REPORT, diptych C7.
