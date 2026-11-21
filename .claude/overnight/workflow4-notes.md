# Fill in before launching Workflow 4
1. In workflow4.js set W3_REPORTS (currently "FILL...") to the actual paths of Workflow 3's round reports (engineer, builders, devil's advocates, lead). Confirm none contain sealed-fold results; W3_RESULTS defaults to taste-model/RESULTS.md (confirm it exists).
2. Confirm Workflow 3 finished: no agents/jobs still running (CPU, background embedding jobs).
3. Pre-launch Sonnet audit of prompts (user quotes, steering, every item in .claude/workflow-notes.md); fix, then launch only right after a neutral message ("go").
4. Reviewers read RESULTS.md and round reports; check the "known evaluation facts" in EXTRA are still unresolved, else drop them.
5. Recreate the ~5 min status cron + Monitor on journal.jsonl. Main session must not message running workflow agents.
6. Hook override .claude/hooks/.overnight-until expires ~11:10 UTC.
7. Not in Workflow 4: sealed prep (isolated agent writing only to .sealed/, no scores) and the single sealed run (main session only, near the end, only if a dev result survives DAs and beats baselines); candidate-song search.
8. Post-workflow Sonnet review + folder cleanup (CLAUDE.md) after Workflow 4; commit after.
