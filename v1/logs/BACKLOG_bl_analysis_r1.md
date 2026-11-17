# Backlog: analysis-only triage, round 1

Sources: logs/BACKLOG_cr1_r1.md, analysis/blind_vs_informed/{LESSONS,video1,video2}.md. Scope: v1/analysis/** and v1/data/<video>/ derived outputs only (no workflows, scripts other than a new helper in scripts/agents/, root docs).
Triage checks (grep of current files): video2 REPORT.md exists but still says "one last hit at 5:02.3" (lines 65, 74) while line 34 gives the two-drum/three-bass tag; video1 REPORT.md still carries "built on one note", "One chord, D", "one unperformed voice", "Nobody ... smiles" (1 fps); video1 interpretation.md still carries the f_0168 "raised fist" (lines 9, 219) and "hand-lettered"; analysis/perceive/video1/seg_02.md and dossier.md line 38 still carry "R. Paping op kop" (not a task file: working material, flagged); comparison.md and video2 interpretation.md still say "one hit at 5:02.3"; data/video2/sync/grid_120bpm.json and sync_kickgrid.json exist, so D4 needs a verification re-run not a first run.

## Selected (7 independent tasks, disjoint files)
| ID | Task | Files |
|----|------|-------|
| T1 | video1 REPORT + interpretation accuracy (C1-C6, raised fist, R. Paping, absence claims with dense frames) | analysis/video1/REPORT.md, analysis/video1/interpretation.md |
| T2 | video2 REPORT final-hit fix, claim check, cold-read revision (D1, D9, B8) | analysis/video2/REPORT.md |
| T3 | video2 interpretation final hits + diptych comparison corrections | analysis/video2/interpretation.md, analysis/compare/elfstedentocht_diptych/comparison.md |
| T4 | music_reading corrections (one chord D, loudest, CLAP softmax, tempo open items, ending) | analysis/music/video1/music_reading.md, analysis/music/video2/music_reading.md |
| T5 | video2 sync on the 120 BPM bar grid and ending onsets (D1, D4, D5) via a new helper | scripts/agents/sync_bar120_video2.py, data/video2/sync/bar120_check.json |
| T6 | functional harmony layer with Roman numerals (D2, D7) | analysis/music/video1/harmony.md, analysis/music/video2/harmony.md, data/*/music_views/bass_roots.json |
| T7 | narrator as a musical voice (D3) | analysis/music/video1/voice_as_music.md, analysis/music/video2/voice_as_music.md |

## Remaining (not selected)
- Working material still carrying "R. Paping op kop": analysis/perceive/video1/seg_02.md, analysis/video1/dossier.md line 38 (frame-reading agents' files; fix after T1).
- Same fix to analysis/video2/dossier.md if it repeats the final-hit or sync claims.
- D5 blind/informed reconcile in blind_vs_informed/video2.md (hole length, loop A form), D6 tempo candidates, D8 per-section LUFS/RT60/phase, F1 words.md provenance, B1-B7 human-feel two-tier report, lineage section, cross-video comparison refresh after T2-T4.
- All toolkit/workflow/script items (E1-E11, L1-L17 changes) are out of this focus.
