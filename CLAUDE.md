# Project rules

- Subagents for coding always run on Sonnet (`model: "sonnet"`).
- Never spawn an Opus agent (or a fork, which inherits the main model) without telling the user first.
- Agents always run in the background.
- The two rules above are enforced by `.claude/hooks/agent-model-guard.sh` (PreToolUse on Agent|Workflow).
- Keep project folders clean: delete scripts/files that are no longer used; scratch work goes in the scratchpad, caches in git-ignored `.cache/`.
- After every workflow finishes (Stop hook `workflow-review-reminder.sh` enforces this), a Sonnet agent (background) reviews its logs/transcripts and reports how future workflows can be improved, including how much the instructions steered the outcome. Apply the lessons before launching the next workflow.
- Workflows auto-forward the user's latest message to every agent as an overriding "user request": launch only right after a neutral message (e.g. "go"), and never add method hints to prompts.
- The main session ONLY orchestrates: it launches and briefs agents and relays results. Agents do all the work, including folder cleanup. The main session never steers methods or makes project decisions itself.
