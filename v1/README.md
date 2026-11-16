# v1: first attempt at a human-style analysis of the two music videos

- `../videos/video1.mp4`: the predecessor (188.7 s).
- `../videos/video2.mp4`: the main video (305.9 s).

## Layout
| Path | What |
|---|---|
| `INSTRUCTIONS.md` | The user's core instructions for this attempt (logged). |
| `PROGRESS.md` | Running log of what has been done and what's next. |
| `logs/ERRORS.md` | Mistakes and how they were handled. |
| `scripts/` | Video-agnostic toolkit. `extract_all.sh` processes every `videos/*.mp4`; individual steps take `VID=<name>`. |
| `workflows/` | Video-agnostic workflow templates (per-video facts come from `data/<video>/context.md`). |
| `data/<video>/` | Machine-extracted raw material: audio, 1 fps frames, contact sheets, shots, lyrics, audio/visual features. |
| `analysis/` | Human-style interpretation written by agents (the actual point). |
