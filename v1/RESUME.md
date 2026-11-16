# How to resume after a container reset

1. `bash v1/scripts/00_setup.sh` (reinstalls Python libs, regenerates the git-ignored WAV files).
2. Read `v1/INSTRUCTIONS.md` (rules), `v1/PROGRESS.md` (where things stand), `v1/logs/ERRORS.md` (don't repeat mistakes), `v1/logs/USAGE.md` (pacing).
3. Workflow scripts are in `v1/workflows/` (run with the Workflow tool via `scriptPath`). Agents write into `v1/analysis/`; an existing file means that unit is done, so prompts tell agents to skip finished work.
4. Check usage with `list_events` (kind `rate_limit_event`) on this session before launching large workflows.
5. Commit and push after every workflow (an auto-commit loop also runs every 10 minutes while the session is alive: `v1/scripts/autocommit.sh`).
