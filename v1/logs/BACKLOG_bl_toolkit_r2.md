# Backlog bl_toolkit_r2 (triage lead, toolkit and docs only)

Checked first: round 1 (T1-T6) is done: prompt rules (L2-L6, L14, L15, L17, L1, L3, L16) are in perceive/listen/report/interpret/coldread/blind_chain, make_index.py and docs exist. Still missing: frame_at.py, 10_onscreen_text.py, whisper reliability flags, check_outputs lint, 00_setup.sh fixes, 04 production-era features, compare.js/backlog.js input checks.

## Selected this round (6 tasks, no shared files)
| ID | Files | Change |
|----|-------|--------|
| T1 | new v1/scripts/frame_at.py, new v1/scripts/10_onscreen_text.py | L7 frame at time with PTS; L9 on-screen text crops with legibility tags |
| T2 | v1/scripts/03_whisper.py | L10/E8 forced-language pass, vocal-stem energy mask, hallucination blacklist, per-segment reliable flag |
| T3 | v1/scripts/check_outputs.py | L2/L14/E4 tag-diff between stages, emotive-noun lint, template context.md must fail, .done markers |
| T4 | v1/scripts/00_setup.sh, v1/scripts/extract_all.sh | E1/E3 import smoke test, ffmpeg check, no hidden pip failure, bare names, print ready args JSON with dur |
| T5 | v1/scripts/04_audio_features.py | L12/D6/D7 production-era features, drum-stem tempo candidates with half/double warning, ambiguous key flag, VID mandatory in this script |
| T6 | v1/workflows/compare.js, v1/workflows/backlog.js | E10 input existence checks, tag carry-through, output exists after writer, dur from summary.json |

## Remaining (next round)
- 02_scenes.py detector (L8) then re-run 09_sync.py/09b_kick_grid.py (D4).
- VID mandatory in 01,02,05,07,08,09,09b (E2); autocommit.sh (E7); 06_stem_one.sh.
- 07_audio_views.py per-stem boundary table (L11).
- Data layout identity.md/reception.md (L6, data).
- Deliverables outside focus: video2 REPORT, video1 corrections C1-C3, diptych, empty rhythm.md.
