# W5 sanitised reports

Sanitised copy of Workflow 5's outputs for the next workflow's agents, following the pattern of w4-sanitised/ (same file layout: reports copied verbatim except for the removals below). Sources: taste-model/RESULTS-W5.md (saved here as RESULTS.md) and the W5 agent reports in the session scratchpad (wf5/docs/). Nothing under .sealed/, no sealed results and no decoy_universe.csv.gz were read.

Sanitisation rules applied:
1. Every held-out number (LATE, HOLDOUT, and pooled TUNE+LATE/ALL-slice grades) removed. Held-out outcomes remain only as the wording already used in RESULTS.md section 5 and brief word-only mentions in agent reports. Removed sections keep their heading with a "[REMOVED ...]" marker.
2. Lead "Next steps" and recommendation sections removed (RESULTS "Next steps"; builder sections "Recommended frame for the next workflow" and "Recommended pre-registrable decision rule"; lead-r1 section 3.4 mapping of method ideas). Builders' in-line conclusions about their own results (e.g. "keep the default recipe") were left in.
3. Attribution to the user/owner removed ("owner's preference/rule/follow-up question" rewritten as the project's decision threshold or plain 80% rule). Facts left in.
4. Kept: all measured TUNE results, methods, caveats, devil's advocate verdicts, inventories, engineer and prep reports. Note: absolute scratchpad paths and held-out log/table file names still appear in some reports as process facts; the numbers in them were removed.

| File | Source | What was removed |
|---|---|---|
| RESULTS.md | taste-model/RESULTS-W5.md | 'Next steps' section removed; 'owner's' phrasing neutralised (project decision threshold / plain 80% rule); pointer to lead section 6 replaced by a note; one 'recommended' wording turned into 'proposed by the round-2 builder'. Held-out outcomes remain only in words, as in the source. |
| builder-r1-eval-frame-folds.md | scratchpad/wf5/docs/builder-r1-eval-frame-folds.md | LATE and HOLDOUT section (8) numbers; 'Recommended frame for the next workflow' (11) |
| builder-r1-tune-content-numbers.md | scratchpad/wf5/docs/builder-r1-tune-content-numbers.md | Section 9 held-out confirmation (LATE/HOLDOUT numbers) |
| builder-r1-tune-signal-numbers.md | scratchpad/wf5/docs/builder-r1-tune-signal-numbers.md | Section 3 held-out confirmation; LATE/HOLDOUT figures in 'strongest case' item 1 |
| builder-r2-music-recipe-numbers.md | scratchpad/wf5/docs/builder-r2-music-recipe-numbers.md | LATE confirmation section; one LATE baseline value |
| builder-r2-score-calculation.md | scratchpad/wf5/docs/builder-r2-score-calculation.md | Section 10 LATE confirmation; 'Recommended pre-registrable decision rule' (8) |
| builder-r2-signal-fresh-and-averaging.md | scratchpad/wf5/docs/builder-r2-signal-fresh-and-averaging.md | Section 8 --late confirmation numbers |
| devils-advocate-r1-eval-frame-folds-dismissed.md | scratchpad/wf5/docs/devils-advocate-r1-eval-frame-folds-dismissed.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
| devils-advocate-r1-eval-frame-folds-works.md | scratchpad/wf5/docs/devils-advocate-r1-eval-frame-folds-works.md | Held-out slices section; LATE grade detail |
| devils-advocate-r1-tune-content-numbers-dismissed.md | scratchpad/wf5/docs/devils-advocate-r1-tune-content-numbers-dismissed.md | LATE/HOLDOUT figures in claim 15 (kept in words); 'owner' phrase neutralised |
| devils-advocate-r1-tune-content-numbers-works.md | scratchpad/wf5/docs/devils-advocate-r1-tune-content-numbers-works.md | Held-out figures section |
| devils-advocate-r1-tune-signal-numbers-dismissed.md | scratchpad/wf5/docs/devils-advocate-r1-tune-signal-numbers-dismissed.md | Section 3 held-out numbers; harness LATE/ALL grade references |
| devils-advocate-r1-tune-signal-numbers-works.md | scratchpad/wf5/docs/devils-advocate-r1-tune-signal-numbers-works.md | Harness ALL-slice (TUNE+LATE) grade and LATE/HOLDOUT deltas |
| devils-advocate-r2-music-recipe-numbers-dismissed.md | scratchpad/wf5/docs/devils-advocate-r2-music-recipe-numbers-dismissed.md | 'project owner's 80% threshold' neutralised |
| devils-advocate-r2-music-recipe-numbers-works.md | scratchpad/wf5/docs/devils-advocate-r2-music-recipe-numbers-works.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
| devils-advocate-r2-score-calculation-dismissed.md | scratchpad/wf5/docs/devils-advocate-r2-score-calculation-dismissed.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
| devils-advocate-r2-score-calculation-works.md | scratchpad/wf5/docs/devils-advocate-r2-score-calculation-works.md | LATE sauc and artist_recent LATE values (claims 15 and below-chance bullet) |
| devils-advocate-r2-signal-fresh-and-averaging-dismissed.md | scratchpad/wf5/docs/devils-advocate-r2-signal-fresh-and-averaging-dismissed.md | LATE table values in claim 13; 'owner' phrase neutralised |
| devils-advocate-r2-signal-fresh-and-averaging-works.md | scratchpad/wf5/docs/devils-advocate-r2-signal-fresh-and-averaging-works.md | 'owner's 80% rule' neutralised |
| engineer-r1.md | scratchpad/wf5/docs/engineer-r1.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
| engineer-r2.md | scratchpad/wf5/docs/engineer-r2.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
| inventory-critic.md | scratchpad/wf5/docs/inventory-critic.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
| inventory-evalkit.md | scratchpad/wf5/docs/inventory-evalkit.md | 'owner/earlier design' changed to 'earlier design' |
| inventory-features.md | scratchpad/wf5/docs/inventory-features.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
| inventory-w3-predictors.md | scratchpad/wf5/docs/inventory-w3-predictors.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
| inventory-w4r1-predictors.md | scratchpad/wf5/docs/inventory-w4r1-predictors.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
| inventory-w4r2-predictors.md | scratchpad/wf5/docs/inventory-w4r2-predictors.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
| lead-final.md | scratchpad/wf5/docs/lead-final.md | Section 6 held-out numbers removed; header sentence updated; 'owner' phrasing neutralised; pointer to 'Next steps' removed |
| lead-r1.md | scratchpad/wf5/docs/lead-r1.md | Section 3.4 (mapping of unvetted method ideas to tasks) removed; 'owner' phrase neutralised |
| lead-r2.md | scratchpad/wf5/docs/lead-r2.md | Section 6 held-out numbers removed |
| prep-r1.md | scratchpad/wf5/docs/prep-r1.md | none (copied unchanged; no held-out numbers, user attribution or recommendation sections found) |
