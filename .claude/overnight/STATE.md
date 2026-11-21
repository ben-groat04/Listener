# Overnight run state (read this first after any restart / usage-limit pause)

Rules for tonight: .claude/workflow-notes.md ("Overnight run" section). CLAUDE.md still applies.
Hook override: .claude/hooks/.overnight-until (git-ignored; if missing after a container restart, recreate it with epoch 1795259433 (2026-11-21 11:10 UTC) only if before that time).

## Plan
1. Workflow 3 (scripts: .claude/overnight/workflow3.js) -> post-workflow Sonnet review + cleanup -> apply lessons.
2. ~3 more workflows (one = full review of the project so far), each: draft brief (agent-built) -> Sonnet pre-launch audit -> fix -> launch.
3. Optional ONE sealed run near the end, per the terms in workflow-notes.md.
4. Morning: report to user; delete the hourly recovery scheduled task; hook override expires by itself.

## Progress log (append; newest last)
- Workflow 3 launched: run wf_88069ba8-60d (journal under /root/.claude/projects/-home-user-Listener/<session>/subagents/workflows/wf_88069ba8-60d/).

## Recovery checklist
- Workflow task gone but journal exists and run unfinished -> Workflow({scriptPath, resumeFromRunId}) (usage-limit-refused and unfinished calls rerun; finished ones come from cache).
- Journal gone (container replaced) -> relaunch the script from .claude/overnight/ fresh; mention it in the log.
- Recreate the 5-min status CronCreate and the journal Monitor (both session-only).
- Commit and push agent work-in-progress (code only; caches/.sealed stay ignored).
- Engineer r1 finished but its report went to the main session (SendMessage to a workflow agent detaches it). Stopped wf_88069ba8-60d, injected the report verbatim as ENG_R1, resumed. Lesson: never SendMessage a running workflow agent.
- Workflow 4 (full project review + rounds) drafted: .claude/overnight/workflow4.js (+ workflow4-notes.md). Needs W3_REPORTS filled after W3 finishes, then Sonnet audit, then launch.
