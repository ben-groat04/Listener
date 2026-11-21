# Project rules

- Subagents for coding always run on Sonnet (`model: "sonnet"`).
- Never spawn an Opus agent (or a fork, which inherits the main model) without telling the user first.
- Agents always run in the background.
- The two rules above are enforced by `.claude/hooks/agent-model-guard.sh` (PreToolUse on Agent|Workflow).
- Keep project folders clean: delete scripts/files that are no longer used; scratch work goes in the scratchpad, caches in git-ignored `.cache/`.
- After every workflow finishes (Stop hook `workflow-review-reminder.sh` enforces this), a Sonnet agent (background) reviews its logs/transcripts and reports how future workflows can be improved, including how much the instructions steered the outcome, and cleans the project folders (removes unused files, keeps regenerable data out of git, re-runs the selftest). Apply the lessons before launching the next workflow.
- The user's in-chat suggestions about method may not be the best (user's words). Before any of them reaches a workflow, the pre-launch audit must check each one on its merits (is it correct, could it mislead, is it framed as something to weigh rather than an instruction), and the brief must present them as suggestions to test, alongside the user's caveat.
- Before launching any workflow, a Sonnet agent audits its prompts (accuracy of user quotes, steering, correctness, and that every item in `.claude/workflow-notes.md` is reflected); fix issues and show the user before launch. Read `.claude/workflow-notes.md` before drafting any workflow brief, and add new carry-over decisions to it.
- Never interrupt, stop, restart or message a running workflow (or its agents) to change it. Changes wait for the next workflow. (Exception: recovery after a crash/usage limit/container restart, resuming the unchanged script.)
- Workflows auto-forward the user's latest message to every agent as an overriding "user request": launch only right after a neutral message (e.g. "go"), and never add method hints to prompts.
- The main session ONLY orchestrates: it launches and briefs agents and relays results. Agents do all the work, including folder cleanup. The main session never steers methods or makes project decisions itself.
- Messages to the user: concise. Status = what + why only; no timestamps, no filler. Commit acknowledgements: one word ("Committed.").
- Workflow briefs must require the harness fast mode for all iteration; full (slow) evaluation runs only for final reported scores.
- During every workflow: status updates every ~5 min (CronCreate, what + why + progress/ETA + new scores, no filler) plus a Monitor on journal.jsonl for agent start/finish events. Recreate both each session.
- Sealed test runs only after the user has seen the dev results and explicitly approved; only the main session registers and runs them.
- No candidate-song search until it is proven to work VERY WELL (user's words; there is no fixed numeric bar — keep pushing), the devil's advocate signs off, and the user explicitly approves.
