# Listener toolkit: understand a music video like a human (the single manual)

Give a fresh Claude Code session this repo and a video. It should end with a checked, human-style reading of the **music first**, then the picture, then the whole. This page is the one manual for running the toolkit; the map of results and layout is [v1/README.md](v1/README.md), and what to do after a container reset is [v1/RESUME.md](v1/RESUME.md).

## For the person
1. Put the video in `videos/` as `<name>.mp4` (or attach it in chat and ask Claude to add it).
2. Start a Claude session on this repo and say: **"Run the Listener toolkit on videos/<name>.mp4."** Add "blind" for a run with no web research, or "blind first" for the blind-then-informed route (below).
3. Results appear in `v1/analysis/` (informed) or `v1/analysis_blind/` (blind). Start with the human piece, `v1/analysis/<name>/LISTENING.md` (one listener's account) and/or `v1/analysis/<name>/VOICES.md` (plain registers from `plainvoice.js`), once they exist; `v1/analysis/<name>/REPORT.md` is the evidence report behind them. [v1/analysis/INDEX.md](v1/analysis/INDEX.md) lists what exists.

## Product order: what the toolkit makes, and in what order
The product is a **human reading of the music and video**, not an audit. The order is fixed (sources: `v1/analysis/human_listening/VERDICT.md`, `PROPOSAL.md` sections 4.8-4.10, `TURING.md`):

1. **Measurement stack and reading workflows** (extraction, `listen.js`, `perceive.js`, `interpret.js`, and optionally `compare.js`, `coldread.js`) produce the checked notes.
2. **Verified fact sheet** `v1/analysis/<vid>/FACTS.md`: key moments, what the voice can and cannot be said to be, the overall shape in plain words, and a 'do not say' list of refuted or withdrawn claims. It is built, and verified line by line against the raw data, inside `listening.js`.
3. **THE main human output**, written only from the verified `FACTS.md`: `listening.js` (verified FACTS.md -> one listener's account, `LISTENING.md`) and/or `plainvoice.js` (plain registers in the style of real people, `VOICES.md`, Turing-tested against real writing).
4. **Evidence report and sidecar**: `report.js` makes `REPORT.md`. It is the evidence behind the human piece, kept at a separate path and out of the human file. It is not the main reading. (`listening.js` reads `REPORT.md` as a private note if it exists, so running `report.js` first helps.)

**Measurement is the checking layer, not the voice** (`PROPOSAL.md` 4.8). Nothing in the measurement stack is deleted; it (a) licenses each human sentence, (b) refutes a human sentence that is wrong, and (c) suggests new things for a human to say. If a sentence's licence fails, fix the sentence; do not defend it.

**Acceptance test for the human output: the Turing test against real human writing** (real excerpts are in `v1/analysis/human_listening/corpus/`; history in [TURING.md](v1/analysis/human_listening/TURING.md)). Judges label a shuffled pool of our pieces and real excerpts as human or AI. So far, over 3 rounds, ours were flagged AI 83%, 92% and 50% of the time against 0%, 0% and 2% for real writing: **not yet passed**. The short texts and one forum post now pass; the reviews and the longer, more structured pieces are still caught. The only true human data is a real listener's answer to 'what stayed with you, and which sentence rang falsest?' (`PROPOSAL.md` 4.7 item 6 plans `v1/analysis/human_listening/real_listener/<video>.md`; none has been collected yet). The scores in `VERDICT.md` come from AI judges (a panel of six), not human readers, so read them as a guide, not as proof. Keep the OBS/INT (observation/interpretation) distinction and the confidence tags in the evidence layer; the human piece commits to a felt account but adds no fact beyond `FACTS.md`.

## For Claude: stages in order
Convention: `VID` is the bare video name (no extension, no folder); `VIDEO_DIR` is the folder holding `<VID>.mp4` (default `videos`; `testvideos` for the test folder). Long steps (extraction, stems, transcription, CLAP) always go under `nohup ... &` with output in `v1/logs/`; poll with `tail`, never `cat` noisy logs. Put `cd` on its own line before backgrounding.

0. **Usage policy and rules** (do this first, any video).
   - Read `CLAUDE.md`, `v1/INSTRUCTIONS.md` (its 'Resolved usage policy' paragraph governs pacing), `v1/logs/ERRORS.md` and [v1/DO_NOT_CLAIM.md](v1/DO_NOT_CLAIM.md) (readings the frames cannot support).
   - Before launching a workflow, check usage (`list_events`, kind `rate_limit_event`) and append a line to `v1/logs/USAGE.md` (time, 5-hour %, 7-day %, note). If no `rate_limit_event` is available, write 'unknown' and run at most one workflow at a time.
   - **Stop starting new workflows at 85% of the 5-hour window** (or of the weekly one); let running ones finish, leave a committed, finished state, and note it in `v1/PROGRESS.md`. Never edge the limit. After the window resets, carry on.
   - Use Sonnet agents where possible. Prefer helper steps that cost no usage (extraction scripts, `check_outputs.py`, `make_index.py`) and run only the workflows that fit comfortably (see the cost table).
   - Workflows skip units whose output already exists, so a cut-off run resumes by running it again.
1. **Setup** (idempotent, safe after a restart; check the disk note first): `bash v1/scripts/00_setup.sh`
2. **Extract** (CPU only, no usage; roughly 15-30 min per 5-minute video on 4 cores, mostly stems and transcription). Add `BLIND=1` for a blind-first or blind-only run: it stops `extract_all.sh` creating `context.md` and runs the check with `--blind`.
   ```bash
   cd /home/user/Listener
   export VID=<name> VIDEO_DIR=videos
   BLIND=1 nohup bash v1/scripts/extract_all.sh $VID > v1/logs/${VID}_extract.log 2>&1 &    # drop BLIND=1 for an informed-only run
   tail -n 20 v1/logs/${VID}_extract.log
   BLIND=1 python3 v1/scripts/check_outputs.py $VID --blind   # must print OK before any agent runs (drop both for informed)
   ```
   `extract_all.sh` skips what is done: frames and contact sheets, shot cuts, music features, visual features, transcripts (original + English), demucs stems (+ vocal-only transcript), music views (chords, melody, levels, per-window stem spectrograms), CLAP tags, then `check_outputs.py`. It also prints the workflow `args` JSON with the duration. **Do not launch agents until the check prints OK.** Run one extraction at a time (see the model and network note).
3. **Choose a route.**
   - **Informed** (default when there is material online): stage 4, then workflows a, b, (c), d, e, f, (g), then blindcmp if a blind run exists.
   - **Blind only** (obscure video, or a test of the toolkit): `blind_chain.js`; stage 4 is just the 'no external sources found' note below.
   - **Blind first, then informed** (recommended when both are wanted): run the blind route first and freeze its claims, then the informed extension, then blindcmp. `blind_chain.js` does this with `"blind_first": true, "compare_after": true`; or run the blind chain, do stage 4, then the informed workflows by hand. Doing blind first keeps the context file from priming the blind reading.
4. **Context** (informed runs only). Research the artist, song and subject with citations into `v1/analysis/research/`, and put verified facts in `v1/data/<name>/context.md`.
   - **Blind-first:** do this only after the blind freeze (`v1/data/<name>/blind_frozen.md` exists and is read-only). Never before, or the context primes the blind reading.
   - **Blind only:** skip it; do not create `context.md`.
   - **Nothing found online:** still write `context.md`, saying 'no external sources found' and listing what was searched, so that `check_outputs.py` does not fail on the empty template and the informed lane knows the search was done.
5. **Workflows** (Workflow tool, `scriptPath`, each takes `args`; arguments are in the table below). Independent ones can run side by side, but each runs only about two agents at once on a 4-CPU machine.

   | Order | Workflow | args example | Output (produced when run) |
   |---|---|---|---|
   | a | `v1/workflows/listen.js` (music first) | `{"videos":[{"vid":"<name>","dur":<seconds>}]}` | `analysis/music/<name>/music_reading.md` |
   | a | `v1/workflows/perceive.js` (picture) | same | `analysis/perceive/<name>/seg_NN.md`, `music.md`, `words.md` |
   | b | `v1/workflows/interpret.js` (conversing panel) | `{"videos":["<name>"]}` | `analysis/<name>/interpretation.md` |
   | c | `v1/workflows/compare.js` (related videos; optional) | `{"videos":["a","b"],"name":"set","relation":"..."}` | `analysis/compare/<set>/comparison.md` |
   | d | `v1/workflows/coldread.js` (improve) | `{"scope":"all","videos":["<name>"],"tag":"cr1"}` | fixes and `logs/BACKLOG_*.md` |
   | e | `v1/workflows/report.js` (evidence report and sidecar; not the main reading) | `{"videos":["<name>"],"compare":"<set>"}` | `analysis/<name>/REPORT.md` |
   | f | `v1/workflows/listening.js` (THE human output: builds and verifies `FACTS.md`, then one listener's account, linted, fact-checked and judged) | `{"videos":["<name>"],"out":"analysis","max_iters":3,"blind":false}` | `analysis/<name>/FACTS.md`, `analysis/<name>/LISTENING.md` |
   | g | `v1/workflows/plainvoice.js` (plain registers: text to a mate, forum post, short review; Turing-tested against real excerpts) | `{"videos":["video2","video1"],"rounds":3,"seed":false}` (`seed: true` starts from the existing `VOICES.md`) | `analysis/<name>/VOICES.md`, `analysis/human_listening/STYLE.md`, `TURING.md`, `corpus/` |
   | last | `v1/workflows/blindcmp.js` (default final step once a blind and an informed run both exist) | `{"videos":["<name>"]}` | `analysis/blind_vs_informed/<name>.md`, `LESSONS.md` |
   | alt | `v1/workflows/blind_chain.js` (whole blind route) | `{"videos":[{"vid":"<name>"}],"video_dir":"videos"}` | `analysis_blind/...` |
   | once | `v1/workflows/human.js` (the debate that designed the human approach: panel, proposal, prototype, blind judging; already run, not part of a normal video run) | `{"videos":["video2","video1"],"rounds":3}` | `analysis/human_listening/round_N/`, `PROPOSAL.md`, `<video>_human.md`, `VERDICT.md` |
   | helper | `v1/workflows/backlog.js` (triage, fix, verify the backlog files) | `{"sources":["v1/logs/BACKLOG_x.md"]}` | fixes and updated `logs/BACKLOG_*.md` |

   `plainvoice.js` and `human.js` use their own defaults for `videos` (`['video2','video1']`) and, for `human.js`, `rounds` 3; pass the video you mean. `listening.js` needs `FACTS.md` to be buildable from the notes in `analysis/music/<name>/` and `analysis/<name>/`, so run a, b and (preferably) e first.

   Add `"blind": true, "out": "analysis_blind"` to any of a, b, c, e, f for a no-context run (`coldread.js` and `plainvoice.js` take no `blind` or `out`).

   **Writing the human piece** (the rules `listening.js` and `plainvoice.js` carry; from `VERDICT.md` 'Next changes'):
   - One voice, first person, as someone who has just watched and listened; no personas, no 'who hears what', no review-blurb opener, no survey ending.
   - Reaction first: state the felt response, then name only one or two moments, not a timeline. Comparisons to other music are allowed, offered as comparisons.
   - Landmarks, not clock times ('when the voice stops', 'the last third'); at most two clock times in a whole piece.
   - No craft or measurement jargon ('on the one', 'no fill', 'held sound', 'subtraction', 'the wall', dB, Hz, BPM, stems); lint for it.
   - Disclose once, in a page-level note, that this is built from analysis and nobody here heard it; then stop apologising and stop hedging every line.
   - Describe the voice as a sound and let facts land as feeling, not as decoding keys.
   - Withdrawn or refuted claims are deleted from the page, not only listed in the sidecar; check sync and count claims mechanically against `FACTS.md` before publishing.
   - Keep the sidecar (`REPORT.md`) at a separate path from the human file.

   **If the repo is not at /home/user/Listener pass "root": "<abs path>" to every workflow.** The workflow scripts cannot find their own location, so without `root` they use the literal `/home/user/Listener`.

   **Args (read from each script's header; defaults as coded):**

   | name | type | default | workflow |
   |---|---|---|---|
   | `root` | string, absolute path | `/home/user/Listener` | all |
   | `videos` | array of names, or `{vid, dur}` objects (required, except human and plainvoice, which default to `['video2','video1']`) | none | all except backlog |
   | `dur` (inside a `videos` object) | seconds | read from `data/<vid>/audio_features/summary.json` (`duration_s`) | listen, blind_chain, compare |
   | `blind` | boolean | `false` | listen, perceive, interpret, compare, report, listening |
   | `out` | string, folder under `v1/` | `analysis` (use `analysis_blind` with `blind`) | listen, perceive, interpret, compare, report, listening |
   | `video_dir` | string | `videos` | perceive, blind_chain |
   | `rounds` | integer | listen 2, interpret 3, compare 2, coldread 1, backlog 1; human 3; plainvoice 3 (as in its header example) | listen, interpret, compare, coldread, backlog, human, plainvoice |
   | `max_iters` | integer | 3 | listening |
   | `seed` | boolean | `false` (true starts from the existing `VOICES.md`) | plainvoice |
   | `skip_windows` | array like `"video1:0040"` | `[]` | listen |
   | `windows_only` | boolean | `false` | listen |
   | `skip_done` | array | `[]` | perceive |
   | `name` | string | the video names joined with `_` | compare |
   | `relation` | string | derived from the `context.md` titles (blind: infer from the data) | compare |
   | `compare` | string, name of a `compare/` folder | none (section skipped) | report |
   | `scope` | `analysis`, `toolkit` or `all` | `all` | coldread |
   | `tag` | string | coldread `cr`; backlog `bl` | coldread, backlog |
   | `fixes_per_round` | integer | 6 | coldread |
   | `blind_first` | boolean | `false` | blind_chain |
   | `compare_after` | boolean | `false` | blind_chain, blindcmp |
   | `informed_rounds` | integer | 3 | blind_chain |
   | `sources` | array of file paths (required) | none (the script throws) | backlog |
   | `focus` | string | highest value first, accuracy before style | backlog |
   | `per_round` | integer | 8 | backlog |

6. **Close out**: run `blindcmp.js` when both kinds of analysis exist, then regenerate the index with `python3 v1/scripts/make_index.py --write` (stdlib only; scans `v1/analysis`, `v1/analysis_blind` and `v1/data`, flags missing and 0-byte files, and rewrites only `v1/analysis/INDEX.md`). Add a line to `v1/PROGRESS.md`. **Commit and push after every workflow**, and log mistakes in `v1/logs/ERRORS.md`.

## Cost: agents and tokens (Sonnet agents)
Measured figures are from this repo's own logs (`v1/logs/USAGE.md`, `v1/PROGRESS.md`); a dash means no figure was logged, so do not guess one. Per-minute figures are the measured total divided by the video length.

| Workflow | Measured | Per minute of video |
|---|---|---|
| `listen.js` (music reading) | 3 min: 25 agents, 2.6M tokens; 5 min: 41 agents, 4.0M tokens | about 8 agents, 0.8-0.9M tokens |
| `perceive.js` (picture) | 3.1 min video1: 10 segment viewers, about 0.86M tokens (one viewer batch of 9: 0.79M) | about 3 agents, 0.3M tokens (plus a music and a words agent) |
| `blind_chain.js` (perceive, listen, identification, interpret, leak check) | video1 (3.1 min): 71 agents, 7.1M tokens; video2 (5.1 min): 83 agents, tokens not logged | about 16-23 agents, about 2.3M tokens (video1 only) |
| `interpret.js`, `compare.js`, `report.js`, `coldread.js`, `blindcmp.js` | no per-run figure logged | not measured |

Usage reference: in window 1 about four workflows in parallel burned roughly 1-1.4% of the 5-hour window per minute (`v1/logs/USAGE.md`, 02:22-02:33), and each full window cost about 13% of the weekly cap.

**Recommended maximum: about 6 minutes of video per run.** The longest fully measured run is video2 at 5.1 min (83 agents in the blind chain). Above 6 minutes, do not launch the whole chain on the full length: either cut the video into excerpts with `ffmpeg` and give each its own name, or run `listen.js` with `skip_windows`/`windows_only` and `perceive.js` with `skip_done` in several sittings across usage windows. Cost grows roughly linearly with length, so a 12-minute video is about two windows' worth of the blind chain; plan for it before starting.

## Disk, models and network
- **Disk.** Have about **2 GB free at minimum** before stage 1 or 2. Measured need per video is about 60 MB per minute of video in `v1/data/<vid>/` (video1, 3.1 min: 187 MB; video2, 5.1 min: 305 MB), of which `stems_raw/` is about 40 MB per minute and the WAVs in `audio/` about 12 MB per minute. Both are git-ignored and **deletable after extraction has passed `check_outputs.py`** (the mp3 stems in `stems/` stay; a rerun of the stem step would regenerate `stems_raw`). On 2026-11-17 this container's disk was at 100% with 87 MB free, with the pip cache at 3.3 GB and the Hugging Face cache at 18 GB. To free space: `python3 -m pip cache purge`, and delete the unused models in `~/.cache/huggingface/hub` (the pipeline needs only the three listed below; `faster-whisper-large-v3` and `faster-whisper-small` were also present and are not used by `extract_all.sh`).
- **Models (downloaded on first use).** faster-whisper `medium` (Hugging Face `Systran/faster-whisper-medium`, run on CPU in int8); CLAP `laion/larger_clap_music_and_speech`; HTDemucs (`htdemucs`, run through `python3 -m demucs`, weights from the `adefossez/HTDemucs` repo in the Hugging Face cache). The first extraction therefore needs outbound HTTPS to Hugging Face and the demucs weight host, plus PyPI for setup; a blocked host shows as a 403 from the proxy.
- **One extraction at a time.** Whisper, demucs and CLAP each use the 4 CPUs; two together swap and slow both. Run `extract_all.sh` for one video, wait for the check, then start the next.
- **Install with `python3 -m pip`**, so that pip belongs to the same Python the scripts use.

## Tools you may call mid-analysis
Both are video-agnostic and free of usage; call them when a claim needs a closer look than the 1 fps frames allow.
- `python3 v1/scripts/frame_at.py <video path or bare name> <t_seconds> [--out DIR]`: a full-resolution frame at time t straight from the mp4, with a `.json` giving the requested time, the actual presentation timestamp and the difference. Use it to settle a visual claim between two sampled frames.
- `VID=<name> python3 v1/scripts/10_onscreen_text.py [--step 1.0] [--max-crops 200]`: finds frames with on-screen print, saves crops and `v1/data/<VID>/text/index.json`, OCR by the `tesseract` command if installed. Each region is tagged legible, partial or unread; cite only the legible ones.

## Status of the proof
Honest status, from `v1/analysis/INDEX.md` and the files in `v1/data/` and `v1/analysis_blind/` (checked 2026-11-17):
- **No video has yet completed the full recommended route** (blind first, then informed extension, then blindcmp, all on the final prompts).
- **video1 and video2** (the two subjects) completed the full set of informed deliverables (REPORT, interpretation, music_reading, perceive, blindcmp) and a blind set (interpretation, music_reading, perceive). That was done before the later toolkit changes (anti-priming, blind-first freeze, two-tier reports), by the session building the toolkit, not by a fresh session following this page.
- **t_birdwalk** (test video, 188 s) is the furthest cold test: extraction, blind perceive, blind music_reading, blind interpretation, blind REPORT and a leak check exist in `analysis_blind/`. It has no informed run and no blindcmp. A fresh `check_outputs.py t_birdwalk` currently reports a frame-count mismatch (201 frames against 188.2 s) and an unfilled `context.md`; that was not investigated here.
- **t_cshells_cshore** (361 s, i.e. right at the 6-minute recommended maximum): data extracted; blind perceive (segments and `music.md`) and 12 blind music windows exist; no blind interpretation, no music_reading, nothing informed. Its blind chain was started and not finished.
- **t_dl_mirror** (239 s): data folders exist, but `analysis/INDEX.md` marks its extraction partial (no stems or music views were recorded then, although some files are now present), only a partial blind perceive exists (8 files), and there is no music_reading, interpretation or informed run.
- **Human output (Turing test):** it has had 3 Turing rounds against real human writing (`v1/analysis/human_listening/TURING.md`): ours flagged AI 83%, 92%, 50%; real writing flagged 0%, 0%, 2%. It is **not yet passing**: the short texts and the video2 forum post now pass (0/2), while the reviews of both videos and the video1 forum post are still flagged 2/2. No real listener has yet answered 'what stayed with you, which sentence rang falsest?'; the `VERDICT.md` scores are from AI judges.
- **Why unfinished:** the 5-hour limit was hit at 03:11 on 2026-11-17 and the weekly cap was nearing 70%; the test-video chains were cut off or deferred, and container restarts killed extraction jobs. The toolkit has therefore been shown to work end-to-end blind on one test video only; the informed and blind-first routes are proven on the two subject videos but not on an unknown video. Treat the first run on a new video as part of the proof, and log what breaks in `v1/logs/ERRORS.md`.

## What the agents can and cannot perceive
- **Picture:** they look at real frames (1 per second, plus a keyframe per shot), so visual claims can be checked. Sub-second timing and fine print are not readable; see [v1/DO_NOT_CLAIM.md](v1/DO_NOT_CLAIM.md).
- **Music:** hearing by measurement only. Agents cannot hear; they "listen" through stem separation, spectrograms, chords, melody contour, loudness and stereo, beat and tempo, CLAP tags and transcripts. Workflows force every music claim to cite a measurement and a confidence level, and what cannot be recovered by measurement (timbre as heard, groove, goosebumps) is stated as such, not guessed.
- **Words:** faster-whisper transcripts, including a pass on the isolated vocal stem. Names and non-English speech need checking.

See also: [v1/README.md](v1/README.md) (entry page and layout), [v1/RESUME.md](v1/RESUME.md) (after a reset), [v1/analysis/INDEX.md](v1/analysis/INDEX.md) (status of every deliverable).
