# Correction (2026-11-17): the picture does cut on the 1:28.6 drop

The round_1 to round_3 transcripts are left unedited as a record. Later rounds, the cold-read passes and some backlog passes say the picture does not cut on the drop: one static road shot 1:22.1 to 1:30.3, with the cut to the bridge crowd 1.7 s later. That is wrong.

- Frame at 88.3 s: snowy road, a few figures, round sign. Frame at 88.7 s: blurred bridge rail and crowd (checked with `python3 v1/scripts/frame_at.py video2 88.3` and `88.7`). The cut is at about 1:28.5.
- Drums go from about -75 dB (87 s bin) to about -21 dB (88 s bin) in `per_second_levels.json`: the sound returns in the same second.
- `shots.json` shows one shot 82.12 to 90.28 s because PySceneDetect missed the blurred whip. 90.28 s is only an angle change on the bridge.

So: cut on the drop, within about 0.1 s (observed, high confidence); designed by the editor or not, unknown. Where a panel member's round 2 point ("the hold over the drop was the cleverest decision") or round 3 retraction depends on a 1.7 s lag or a hold to 1:30.3, treat it as resting on a wrong fact. Current statements: `v1/analysis/video2/FACTS.md` (section A), `interpretation.md`, `REPORT.md`.
