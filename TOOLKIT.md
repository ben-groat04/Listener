# Listener toolkit: understand a music video like a human (the single manual)

Give a fresh Claude Code session this repo and a video. It should end with a checked, human-style reading of the **music first**, then the picture, then the whole. This page is the one manual for running the toolkit; the map of results and layout is [v1/README.md](v1/README.md), and what to do after a container reset is [v1/RESUME.md](v1/RESUME.md).

## For the person
1. Put the video in `videos/` as `<name>.mp4` (or attach it in chat and ask Claude to add it).
2. Start a Claude session on this repo and say: **"Run the Listener toolkit on videos/<name>.mp4."** Add "blind" for a run with no web research, or "blind first" for the blind-then-informed route (below).
3. Results appear in `v1/analysis/` (informed) or `v1/analysis_blind/` (blind). Start with `v1/analysis/<name>/REPORT.md`; [v1/analysis/INDEX.md](v1/analysis/INDEX.md) lists what exists.

## For Claude: stages in order
Convention: `VID` is the bare video name (no extension, no folder); `VIDEO_DIR` is the folder holding `<VID>.mp4` (default `videos`; `testvideos` for the test folder). Long steps (extraction, stems, transcription, CLAP) always go under `nohup ... &` with output in `v1/logs/`; poll with `tail`, never `cat` noisy logs. Put `cd` on its own line before backgrounding.

0. **Read the rules**: `CLAUDE.md`, `v1/INSTRUCTIONS.md`, `v1/logs/ERRORS.md`, [v1/DO_NOT_CLAIM.md](v1/DO_NOT_CLAIM.md) (readings the frames cannot support). Check usage and log it (see Usage policy).
1. **Setup** (idempotent, safe after a restart): `bash v1/scripts/00_setup.sh`
2. **Extract** (CPU only, no usage; roughly 15-30 min per 5-minute video on 4 cores, mostly stems and transcription):
   ```bash
   cd /home/user/Listener
   export VID=<name> VIDEO_DIR=videos
   nohup bash v1/scripts/extract_all.sh $VID > v1/logs/${VID}_extract.log 2>&1 &
   tail -n 20 v1/logs/${VID}_extract.log
   python3 v1/scripts/check_outputs.py $VID      # must print OK before any agent runs
   ```
   `extract_all.sh` skips what is done: frames and contact sheets, shot cuts, music features, visual features, transcripts (original + English), demucs stems (+ vocal-only transcript), music views (chords, melody, levels, per-window stem spectrograms), CLAP tags, then `check_outputs.py`. **Do not launch agents until it prints OK.**
3. **Context** (informed runs only; skip when blind): research the artist, song and subject with citations into `v1/analysis/research/`, and put verified facts in `v1/data/<name>/context.md`.
4. **Workflows** (Workflow tool, `scriptPath`, each takes `args`). Independent ones can run side by side, but each runs only about two agents at once on a 4-CPU machine.

   | Order | Workflow | args example | Output (produced when run) |
   |---|---|---|---|
   | a | `v1/workflows/listen.js` (music first) | `{"videos":[{"vid":"<name>","dur":<seconds>}]}` | `analysis/music/<name>/music_reading.md` |
   | a | `v1/workflows/perceive.js` (picture) | same | `analysis/perceive/<name>/seg_NN.md`, `music.md`, `words.md` |
   | b | `v1/workflows/interpret.js` (conversing panel) | `{"videos":["<name>"]}` | `analysis/<name>/interpretation.md` |
   | c | `v1/workflows/compare.js` (related videos; optional) | `{"videos":["a","b"],"name":"set","relation":"..."}` | `analysis/compare/<set>/comparison.md` |
   | d | `v1/workflows/coldread.js` (improve) | `{"scope":"all","videos":["<name>"],"tag":"cr1"}` | fixes and `logs/BACKLOG_*.md` |
   | e | `v1/workflows/report.js` (readable final piece) | `{"videos":["<name>"],"compare":"<set>"}` | `analysis/<name>/REPORT.md` |
   | last | `v1/workflows/blindcmp.js` (default final step once a blind and an informed run both exist) | `{"videos":["<name>"]}` | `analysis/blind_vs_informed/<name>.md`, `LESSONS.md` |
   | alt | `v1/workflows/blind_chain.js` (whole blind route) | `{"videos":[{"vid":"<name>"}],"video_dir":"videos"}` | `analysis_blind/...` |
   | helper | `v1/workflows/backlog.js` (triage, fix, verify the backlog files) | see its header | fixes and updated `logs/BACKLOG_*.md` |

   Add `"blind": true, "out": "analysis_blind"` to any of a-e for a no-context run.
5. **Choose a route.**
   - **Informed** (default when there is material online): stage 3, then workflows a, b, (c), d, e, then blindcmp if a blind run exists.
   - **Blind only** (obscure video, or a test of the toolkit): `blind_chain.js`, with no stage 3.
   - **Blind first, then informed** (recommended when both are wanted): run the blind route first and freeze its claims, then the informed extension, then blindcmp. `blind_chain.js` does this with `"blind_first": true, "compare_after": true`; or run the blind chain, do stage 3, then the informed workflows by hand. Doing blind first keeps the context file from priming the blind reading.
6. **Close out**: run `blindcmp.js` when both kinds of analysis exist, then regenerate the index with `python3 v1/scripts/make_index.py --write` (stdlib only; scans `v1/analysis`, `v1/analysis_blind` and `v1/data`, flags missing and 0-byte files, and rewrites only `v1/analysis/INDEX.md`). Add a line to `v1/PROGRESS.md`.
7. **Commit and push after every workflow.** Log mistakes in `v1/logs/ERRORS.md`.

## Usage policy (any video)
- Before launching a workflow, check usage (`list_events`, kind `rate_limit_event`) and append a line to `v1/logs/USAGE.md` (time, 5-hour %, 7-day %, note).
- **Stop starting new workflows at 85% of the 5-hour window** (or of the weekly one); let running ones finish, leave a committed, finished state, and note it in `v1/PROGRESS.md`. Never edge the limit. After the window resets, carry on.
- Use Sonnet agents where possible. Prefer helper steps that cost no usage (extraction scripts, `check_outputs.py`, `make_index.py`) and run only the workflows that fit comfortably.
- Workflows skip units whose output already exists, so a cut-off run resumes by running it again.

## What the agents can and cannot perceive
- **Picture:** they look at real frames (1 per second, plus a keyframe per shot), so visual claims can be checked. Sub-second timing and fine print are not readable; see [v1/DO_NOT_CLAIM.md](v1/DO_NOT_CLAIM.md).
- **Music:** hearing by measurement only. Agents cannot hear; they "listen" through stem separation, spectrograms, chords, melody contour, loudness and stereo, beat and tempo, CLAP tags and transcripts. Workflows force every music claim to cite a measurement and a confidence level, and what cannot be recovered by measurement (timbre as heard, groove, goosebumps) is stated as such, not guessed.
- **Words:** faster-whisper transcripts, including a pass on the isolated vocal stem. Names and non-English speech need checking.

See also: [v1/README.md](v1/README.md) (entry page and layout), [v1/RESUME.md](v1/RESUME.md) (after a reset), [v1/analysis/INDEX.md](v1/analysis/INDEX.md) (status of every deliverable).
