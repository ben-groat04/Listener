# video1, RHYTHM specialist, round 2 (reconstructed note)

The original round-2 file was empty (0 bytes; the session ended before writing). This short note was written afterwards from a fresh measurement and does not reproduce the lost round-2 reasoning. For the full argument see `../round_1/rhythm.md` and `../round_3/rhythm.md` (round 3 states that it answers the round-2 questions too).

Measured here (librosa 1.0.1, `data/video1/stems_raw/htdemucs/song/drums.wav`, sr 22050, hop 256, default `onset_detect`; beat list from `data/video1/audio_features/beat_times.json`; script in the session scratchpad, not committed):
- Beat tracker: 218 beats from 0.95 s to 167.97 s; median inter-beat interval 0.766 s, i.e. 78.3 BPM; inter-beat standard deviation 0.019 s.
- Drum-stem onsets: 796 in total. Most common onset-to-onset interval in 5-35 s: 0.18-0.20 s (79 of the counted intervals in the two top 0.02 s bins), then 0.38 s. That is a grid of about 0.19 s, four per 78-BPM beat, as rounds 1 and 3 report.
- Onset density (this detector): 4.57 per second at 5-35 s, 4.07 at 60-90 s, 4.14 at 121-158 s, 3.94 at 170-186 s. Roughly constant; the absolute values are lower than round 3's 5.2-5.3 per second because the detectors differ, so do not compare the two directly.
- Drum-stem RMS between 167 and 169 s has its minimum at 168.15 s (0.0011, against a whole-track median of 0.108): the all-band cut near 2:48 that round 1 reports.

Interpretation (INFERRED, not measured here): the octave question (78 BPM with sixteenths versus 156 with eighths) cannot be settled from these numbers; see round 3 section 2.
