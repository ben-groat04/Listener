# Backlog: analysis-only triage, round 2

Sources: logs/BACKLOG_cr1_r1.md, analysis/blind_vs_informed/{LESSONS,video1,video2}.md, logs/BACKLOG_bl_analysis_r1.md. Scope: v1/analysis/** and v1/data/<video>/ derived outputs; helpers only in scripts/agents/.
Round 1 (T1-T7) fixed REPORT/interpretation/music_reading, added sync re-run, harmony, voice_as_music. Triage checks now: blind_vs_informed/video2.md still says "REPORT.md does not exist"; video1 dossier line 15 still has "one pedal note, D"; perceive/video1/seg_02.md still has "R. Paping op kop"; perceive/video1/seg_10.md and video2 seg_01/seg_10 still say "hand-lettered"; video2 dossier line 11 and panel files carry "one hit"; specialists/round_2/rhythm.md (video1) is 0 bytes; no tempo-candidate or per-section loudness outputs exist.

## Selected (7 tasks, disjoint files)
| ID | Task | Files |
|----|------|-------|
| U1 | D5 reconcile blind vs informed for video2 from stems (hole length, loop A form, drum stop times, first voice fragment); update stale status lines | analysis/blind_vs_informed/video2.md, new scripts/agents/reconcile_video2.py, data/video2/sync/reconcile.json |
| U2 | Same for video1 plus status notes that the raised fist and Paping errors are fixed in deliverables | analysis/blind_vs_informed/video1.md, new scripts/agents/reconcile_video1.py, data/video1/sync/reconcile.json |
| U3 | Working-material cleanup: priming and absence claims (Paping, raised fist, hand-lettered, one pedal note, one hit) with correction notes | analysis/video1/dossier.md, analysis/video2/dossier.md, analysis/perceive/video1/seg_02.md, seg_10.md, analysis/perceive/video2/seg_01.md, seg_10.md |
| U4 | D6 tempo candidates (drum-stem, half/double-time, downbeat) for both videos | new scripts/agents/tempo_candidates.py, data/video{1,2}/audio_features/tempo_candidates.json, analysis/music/tempo_candidates.md |
| U5 | D8 per-section LUFS, phase correlation, RT60 probe | new scripts/agents/section_levels.py, data/video{1,2}/audio_features/section_levels.json, analysis/music/section_levels.md |
| U6 | A5 empty rhythm.md and F1 words.md provenance and confidence downgrade | analysis/music/video1/specialists/round_2/rhythm.md, analysis/perceive/video1/words.md, analysis/perceive/video2/words.md |
| U7 | B6/B7 lineage and cultural context plus "two audiences" narration note, tagged interpretation, as new files | new analysis/video1/lineage_and_words.md, analysis/video2/lineage_and_words.md |

## Remaining
- B4/B5 two-tier plain-language rewrite and first-person listener narrative of REPORT.md (needs REPORT owner after U-round).
- Panel round files carrying "one hit" (working material, low value).
- Cross-video comparison.md refresh after U1/U2.
- All toolkit/workflow/script engineering (E1-E11, L1-L17) is out of focus.
