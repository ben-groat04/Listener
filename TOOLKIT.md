# Listener toolkit: understand a music video like a human

Give a fresh Claude Code session this repo and a video. It should end with a checked, human-style reading of the **music first**, then the picture, then the whole.

## New video quickstart
```bash
cd /home/user/Listener
VID=<name>; VIDEO_DIR=videos          # use VIDEO_DIR=testvideos for the test folder; the file is $VIDEO_DIR/$VID.mp4
bash v1/scripts/00_setup.sh
nohup bash v1/scripts/extract_all.sh $VID > v1/logs/${VID}_extract.log 2>&1 &   # long: run with nohup
tail -n 20 v1/logs/${VID}_extract.log                                          # filter, do not cat noisy logs
python3 v1/scripts/check_outputs.py $VID                                       # must print OK before any agent runs
```
Then run the workflows in the table below and finish with `report.js`. Convention: `VID` is the bare video name (no extension, no folder); `VIDEO_DIR` is the folder holding `<VID>.mp4` (default `videos`). Long steps (extraction, stems, transcription, CLAP) always go under `nohup ... &` with their output in `v1/logs/`, and you poll with `tail`. Map of results and layout: [v1/README.md](v1/README.md) ("Start here").

**Usage policy (any video):** before launching a workflow, check usage (`list_events`, kind `rate_limit_event`) and log it in `v1/logs/USAGE.md`; use Sonnet agents where possible, run at most the workflows that fit comfortably, and never push the 5-hour or weekly limit; if close, stop at a finished, committed state and note it in `v1/PROGRESS.md`.

## For the person
1. Put the video in `videos/` as `<name>.mp4` (or attach it in chat and ask Claude to add it).
2. Start a Claude session on this repo and say: **"Run the Listener toolkit on videos/<name>.mp4."** Add "blind" if you want it done with no web research.
3. Results appear in `v1/analysis/` (or `v1/analysis_blind/`). Start with `v1/analysis/<name>/REPORT.md`; the page [v1/analysis/INDEX.md](v1/analysis/INDEX.md) lists what exists.

## For Claude (follow in order)
0. Read `CLAUDE.md`, `v1/INSTRUCTIONS.md`, `v1/logs/ERRORS.md`. Check usage (`list_events`, kind `rate_limit_event`) and log it in `v1/logs/USAGE.md`.
1. **Setup** (idempotent, safe after a container restart): `bash v1/scripts/00_setup.sh`
2. **Extract** (CPU only, no usage; about 15–30 min per 5-minute video on 4 cores, mostly stem separation and transcription):
   `v1/scripts/extract_all.sh <name>` (use `VIDEO_DIR=testvideos` for other folders). It runs, skipping anything already done:
   frames + contact sheets → shot cuts → music features → visual features → transcripts (original + English) → demucs stems (+ vocal-only transcript) → music views (chords, melody, levels, per-window stem spectrograms) → CLAP audio tags → `check_outputs.py`.
   **Do not launch agents until `check_outputs.py <name>` prints OK.**
3. **Context** (skip if blind): research the artist, song and subject (cited) into `v1/analysis/research/`, and put verified facts in `v1/data/<name>/context.md`.
4. **Workflows** (Workflow tool, `scriptPath`; each takes `args`). Run independent ones side by side, because each workflow only runs about two agents at once on a 4-CPU machine:
   | Order | Workflow | args example | Output |
   |---|---|---|---|
   | a | `v1/workflows/listen.js` (music first) | `{"videos":[{"vid":"<name>","dur":<seconds>}]}` | `analysis/music/<name>/music_reading.md` (produced when run) |
   | a | `v1/workflows/perceive.js` (picture) | same | `analysis/perceive/<name>/seg_NN.md`, `words.md` (produced when run) |
   | b | `v1/workflows/interpret.js` (conversing panel) | `{"videos":["<name>"]}` | `analysis/<name>/interpretation.md` (produced when run) |
   | c | `v1/workflows/compare.js` (related videos) | `{"videos":["a","b"],"name":"set","relation":"..."}` | `analysis/compare/<set>/comparison.md` (produced when run) |
   | d | `v1/workflows/coldread.js` (improve) | `{"scope":"all","videos":["<name>"],"tag":"cr1"}` | fixes + `logs/BACKLOG_*.md` (produced when run) |
   | e | `v1/workflows/report.js` (readable final piece; this is the report step) | `{"videos":["<name>"],"compare":"<set>"}` | `analysis/<name>/REPORT.md` (produced when run) |
   | any | `v1/workflows/blind_chain.js` | `{"videos":[{"vid":"<name>","dur":<s>}],"video_dir":"videos"}` | `analysis_blind/...` (produced when run) |
   Add `"blind": true, "out": "analysis_blind"` to any workflow for a no-context run.
5. Commit and push after every workflow. Log mistakes in `v1/logs/ERRORS.md`.

## What the agents can and cannot perceive
- **Picture:** they look at real frames (1 per second, plus a keyframe per shot), so visual claims can be checked.
- **Music:** they cannot hear. They "listen" through measurements: stem separation, spectrograms, chords, melody contour, loudness/stereo, beat/tempo, CLAP tags and transcripts. Workflows force every music claim to cite a measurement and give a confidence level.
- **Words:** faster-whisper transcripts, including a pass on the isolated vocal stem. Names and non-English speech need checking.

See also: [v1/README.md](v1/README.md) (entry page and layout), [v1/RESUME.md](v1/RESUME.md) (after a reset).
