# v1: a human-style reading of music videos (entry page)

The toolkit takes a music video and produces a checked reading of the **music first**, then the picture, then the whole. Current subjects: two Public Service Broadcasting videos (`videos/video1.mp4`, 188.7 s, "Elfstedentocht Part 1"; `videos/video2.mp4`, 305.9 s, "Elfstedentocht Part 2") and three test videos in `testvideos/`.

## Start here
| I want to... | Open |
|---|---|
| Read the definitive human reading of video1 | [analysis/video1/LISTENING.md](analysis/video1/LISTENING.md); verified fact sheet [FACTS.md](analysis/video1/FACTS.md); plain-register pieces [VOICES.md](analysis/video1/VOICES.md); evidence report [REPORT.md](analysis/video1/REPORT.md) |
| Read the definitive human reading of video2 | [analysis/video2/LISTENING.md](analysis/video2/LISTENING.md); verified fact sheet [FACTS.md](analysis/video2/FACTS.md); plain-register pieces [VOICES.md](analysis/video2/VOICES.md); evidence report [REPORT.md](analysis/video2/REPORT.md) |
| See how human-sounding output was tested (and that it is not yet passed) | [analysis/human_listening/](analysis/human_listening/): `STYLE.md`, `TURING.md`, `VERDICT.md`, `PROPOSAL.md`, `corpus/` (see below) |
| See the toolkit on an unknown video (example only) | [analysis_blind/t_birdwalk/REPORT.md](analysis_blind/t_birdwalk/REPORT.md) (blind run, no context file; working material, not a final piece) |
| See every deliverable and its status | [analysis/INDEX.md](analysis/INDEX.md) |
| Run the toolkit on a new video | [../TOOLKIT.md](../TOOLKIT.md) (stages and usage policy) |
| Recover after a container reset | [RESUME.md](RESUME.md) |
| See the current state, then the history | [PROGRESS.md](PROGRESS.md) (state table at the top, diary below) |
| Check the rules and past mistakes | [INSTRUCTIONS.md](INSTRUCTIONS.md), [logs/ERRORS.md](logs/ERRORS.md), [logs/](logs/) (also USAGE.md, BACKLOG_*.md) |

## Human output and the acceptance test
`FACTS.md` (verified sheet) feeds `workflows/listening.js` and `workflows/plainvoice.js`, which write `LISTENING.md` and `VOICES.md`; this is the main human output. `REPORT.md` and the measurements are the checking layer behind it. The **acceptance test is the Turing test against real human writing** (`analysis/human_listening/TURING.md`), and it is **currently NOT passed**: ours flagged as AI 83%, 92%, 50% (rounds 1 to 3) versus real writing flagged 0%, 0%, 2%. In round 3 the short, casual pieces pass, while the reviews and the video1 forum post are still flagged. `VERDICT.md` (six AI judges: the human piece beat the old report 6 of 6 on "more human" and "would rather read"; the old report stayed more accurate on video2) is an AI-judge result, not a human one, so it does not replace the Turing test. `PROPOSAL.md` holds the proposed fixes; `corpus/` holds the real human texts used as the benchmark.

## analysis versus analysis_blind
- `analysis/` is the **informed** run: agents may use `data/<video>/context.md` (artist, commission, archive facts, researched in `analysis/research/`).
- `analysis_blind/` is the **blind** run: the same workflows with no web research and no context file, to see what the data alone supports. It exists to compare against the informed run and to test the toolkit on unknown videos. Treat it as working material, never as the final piece.
- Final versus working: `REPORT.md` > `interpretation.md` > `music_reading.md` are the readable deliverables; everything else (window notes, specialist rounds, panels, dossiers, segment notes) is working material that backs them.

## Layout
| Path | What |
|---|---|
| `INSTRUCTIONS.md` | The user's core rules for this attempt (logged). |
| `PROGRESS.md` | Current-state table, then the dated diary (history). |
| `RESUME.md` | Short after-reset steps. |
| `DO_NOT_CLAIM.md` | Standing list of readings that frames and print do not support (referenced by the workflow prompts). |
| `../TOOLKIT.md` | The single manual: stages, workflows, usage policy (repo root). |
| `README.md` | This page. |
| `requirements.txt` | Python libraries installed by `scripts/00_setup.sh`. |
| `logs/` | `ERRORS.md` (mistakes), `USAGE.md` (usage pacing), `BACKLOG_*.md` (cold-read findings), plus extraction and run logs. |
| `scripts/` | Video-agnostic toolkit: numbered steps `00`-`09b`, `_common.py`, `extract_all.sh` (all steps for one video), `check_outputs.py` (completeness gate), `frame_at.py` (single frame at a time), `10_onscreen_text.py` (on-screen text), `make_index.py` (regenerates `analysis/INDEX.md`; `--write`), `autocommit.sh`, `fetch_archive.sh`, `fetch_commons.py`. Steps take `VID=<name>` (and `VIDEO_DIR=<folder>` if not `videos/`). |
| `scripts/legacy/` | Superseded scripts that hard-code video1/video2; reference only. |
| `scripts/agents/` | Per-video one-off measurement scripts written by agents during checks and specialist rounds (names such as `harmony_r2_video2.py`). Evidence trail, not part of the pipeline. |
| `scripts/experimental/` | `10_audio_lm.py` (Qwen2.5-Omni on CPU); failed, not in the pipeline. |
| `workflows/` | Video-agnostic Workflow scripts: `listen`, `perceive`, `interpret`, `compare`, `coldread`, `report`, `blind_chain`, `blindcmp`, `backlog`, `human`, `listening`, `plainvoice`, `musicvoice`. |
| `data/<video>/` | Machine-extracted raw material (git-ignored parts: audio WAVs): audio, 1 fps frames, contact sheets, shots, lyrics, audio/visual features, stems, music views, sync, and `context.md` (verified per-video facts). |
| `analysis/` | Informed analysis: `INDEX.md` (generated status), `<video>/` (REPORT, interpretation, dossier, panel), `music/<video>/` (music_reading, windows, specialists), `perceive/<video>/` (segment notes, words), `compare/`, `blind_vs_informed/`, `human_listening/` (style, Turing test, verdict, proposal, corpus), `research/` (cited background). |
| `analysis_blind/` | Blind analysis with the same shape (no `research/`). |

Videos: `../videos/` (video1, video2), `../testvideos/` (t_birdwalk, t_cshells_cshore, t_dl_mirror; see `SOURCES.md`).
