# Project rules

- Subagents for coding always run on Sonnet (`model: "sonnet"`).
- Never spawn an Opus agent (or a fork, which inherits the main model) without telling the user first.
- Agents always run in the background.
- The two rules above are enforced by `.claude/hooks/agent-model-guard.sh` (PreToolUse on Agent|Workflow).
- Keep project folders clean: delete scripts/files that are no longer used; scratch work goes in the scratchpad, caches in git-ignored `.cache/`.
