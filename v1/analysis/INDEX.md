# Analysis index: every video by deliverable

**Rule:** the final pieces are `REPORT.md` > `interpretation.md` > `music_reading.md` (best available first). Everything else (windows, specialists, panels, dossiers, segment notes, research) is working material. Status checked by `ls` of `v1/analysis` and `v1/analysis_blind`. Paths are relative to `v1/`. Back to [README](../README.md).

## Informed (`analysis/`)
| Video | REPORT | interpretation | music_reading | perceive | compare |
|---|---|---|---|---|---|
| video1 | done: `analysis/video1/REPORT.md` | done: `analysis/video1/interpretation.md` | done: `analysis/music/video1/music_reading.md` | done: `analysis/perceive/video1/` (10 segments, `music.md`, `words.md`) | partial: `analysis/compare/elfstedentocht_diptych/round_1/` (music.md, picture.md; no comparison.md) |
| video2 | missing | done: `analysis/video2/interpretation.md` (s8 lists open uncertainties) | done: `analysis/music/video2/music_reading.md` | done: `analysis/perceive/video2/` (16 segments, `words.md`) | partial: same diptych round_1 |
| t_birdwalk | missing | missing | missing | missing (blind only) | n/a |
| t_cshells_cshore | missing | missing | missing | missing | n/a |
| t_dl_mirror | missing (no extracted data yet) | missing | missing | missing | n/a |

## Blind (`analysis_blind/`, no context)
| Video | blind interpretation | blind music_reading | blind perceive | Note |
|---|---|---|---|---|
| video1 | done: `analysis_blind/video1/interpretation.md` | done: `analysis_blind/music/video1/music_reading.md` | done: `analysis_blind/perceive/video1/` | blind-vs-informed comparison not written |
| video2 | partial: only `dossier.md` and `panel/round_1`-`round_2` | done: `analysis_blind/music/video2/music_reading.md` | done: `analysis_blind/perceive/video2/` | blind interpretation unfinished |
| t_birdwalk | missing | missing | partial: `analysis_blind/perceive/t_birdwalk/` (10 segments, `music.md`; no `words.md`) | first blind test on an unknown video |
| t_cshells_cshore | missing | missing | missing | data extracted only (`data/t_cshells_cshore/`; no music_views or CLAP yet) |
| t_dl_mirror | missing | missing | missing | not extracted |

## Research and logs
- `analysis/research/`: `artist_and_tracks`, `cultural_context`, `elfstedentocht_1963`, `part_mapping`, `archive_sources`, `psb_method`, `reception`. Verified facts are in `data/<video>/context.md`.
- Cold-read findings: `logs/BACKLOG_cr1_r1.md`. Mistakes: `logs/ERRORS.md`.
