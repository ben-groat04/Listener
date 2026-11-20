# Project rules

- Subagents for coding always run on Sonnet (`model: "sonnet"`).
- Never spawn an Opus agent (or a fork, which inherits the main model) without telling the user first.
- Enforced by `.claude/hooks/agent-model-guard.sh` (PreToolUse on Agent|Workflow).
