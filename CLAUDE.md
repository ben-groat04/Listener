# Listener: project rules (auto-loaded into every session and subagent)

**Goal:** a video-agnostic toolkit: upload any music video, send a Claude session at it, and get an understanding of the music and video **as a human would feel and interpret it**. Current attempt: `v1/` (two Public Service Broadcasting videos in `videos/`, extra test videos in `testvideos/`).

**Before acting, read** `v1/INSTRUCTIONS.md` (all user rules), `v1/logs/ERRORS.md` (mistakes not to repeat), and `v1/PROGRESS.md` (state). Resume steps: `v1/RESUME.md`.

Key rules (short form):
- **Music first**: weight analysis towards the music; read the video in relation to it.
- Accuracy first: never invent what you did not see or hear; separate observation from interpretation; verify claims.
- Use Sonnet for agents where possible; converse via workflows; use cold-read reviews to improve.
- Keep the toolkit video-agnostic; video-specific facts go in `v1/data/<video>/context.md`.
- Track usage (`v1/logs/USAGE.md`); never edge the limit.
- Log mistakes in `v1/logs/ERRORS.md`. Commit and push often (survive container resets).
- English with British spelling. Never stop on "waiting on…"; leave a finished, useful state.
- **Benchmark against reality early:** prototype the final output first and test it against real human examples, not AI judges alone.
- Shell: put `cd` on its own line before backgrounding jobs; filter noisy logs before reading.

**Entry points:** `TOOLKIT.md` (repo root) is the single manual for running the toolkit on a new video (stages, workflows, usage policy); `v1/README.md` ('Start here') is the map of results and layout; `v1/RESUME.md` is for after a container reset; `v1/DO_NOT_CLAIM.md` lists readings the frames cannot support; `python3 v1/scripts/make_index.py --write` regenerates `v1/analysis/INDEX.md`.

**Read in this order** (the rest is reference):
1. `TOOLKIT.md` (repo root): the single manual; follow it to run a video.
2. `v1/INSTRUCTIONS.md`: the user's rules, ending with the 'Resolved usage policy'.
3. `v1/logs/ERRORS.md`: mistakes not to repeat.
4. `v1/PROGRESS.md`: current state (table first, diary below).
5. `v1/README.md`: map of results and layout.

Reference only: `v1/RESUME.md` (after a container reset), `v1/DO_NOT_CLAIM.md`, `v1/analysis/INDEX.md`, `v1/logs/USAGE.md`.
