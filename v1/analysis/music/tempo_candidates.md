# Tempo and metre candidates (video1, video2)

Source: `v1/data/<video>/audio_features/tempo_candidates.json`, made by `v1/scripts/agents/tempo_candidates.py <video>` (librosa, onset-strength autocorrelation tempogram, deterministic: a re-run gives an identical file). Strength is autocorrelation relative to the strongest peak of the same source (1.0 = strongest). Rule used: two top candidates within 10 per cent strength are called **ambiguous**. Tags: [M] measured; [I] interpretation of how it would feel, not tested on listeners.

Limit of the method: autocorrelation of an onset envelope shows what repeats, not which repeat a listener counts as the beat. Candidates a factor of 2 apart are expected to score similarly.

## video1

| Source | Candidates (BPM : relative strength) | Top two |
|---|---|---|
| Drum stem | 78.3 : 1.00, 156.6 : 0.96, 103.4 : 0.72, 62.3 : 0.60, 52.2 : 0.58 | 78.3 vs 156.6, 4 per cent apart: **ambiguous** (exactly a factor of 2) |
| Full mix | 156.6 : 1.00, 78.3 : 0.91, 103.4 : 0.86, 62.3 : 0.71, 52.2 : 0.63 | 156.6 vs 78.3, 9 per cent apart: **ambiguous** (exactly a factor of 2) |

- Kick (40 to 120 Hz flux, 131 onsets): median inter-onset interval 0.58 s (103 BPM), quartiles 0.38 s and 0.77 s, histogram mode 0.38 s (158 BPM) [M]. The median matches no beat level; it sits between 0.38 s and 0.77 s because kicks fall on both. It is not evidence for 103 BPM (103.4 is a weak third candidate, 0.72 and 0.86, and only 36 per cent of kicks sit on a 104 BPM grid).
- Kicks on the grid (period refined within 3 per cent): 156 BPM grid 76 per cent of kicks (99 of 131); 78 BPM grid 52 per cent (68 of 131). A 78 grid has half as many lines, so the higher figure for 156 is partly expected and not proof of 156 [M].
- Bar phase (beat with most low-band kick weight): on the 156 grid, index 2 (0-based) with 43 per cent of the weight, 1.70 times the next beat; on the 78 grid, index 3 with 33 per cent, only 1.12 times the next beat, which is no clear downbeat [M]. Counted from an arbitrary grid offset, so the bar line could be a beat away (assumption).
- Supported: **the 0.77 s pulse (78 BPM) and the 0.38 s pulse (156 BPM) are both present, and which one is "the beat" is not settled by the data.** The beat tracker's 78.3 BPM in `summary.json` is the same peak. Existing rhythm notes (hat every 0.385 s, kick on sixteenth positions) lean 55/45 to 78 as quarter note; this autocorrelation neither confirms nor overturns that (drum stem top = 78, full-mix top = 156, each by under 10 per cent).
- Half/double-time alternative: 156.6 BPM (double) if the hat pulse is counted; 78.3 BPM (half) if the kick-and-snare weight is counted.
- Still ambiguous: the octave (78 vs 156); the downbeat (low-band weight is spread over beats on the 78 grid; the 156 grid favours one beat in four, with 1.7 times the next).
- How a listener would feel it [I]: a heavy step at about 78 per minute over a fast hat flutter at 156 per minute. Counting slowly gives a 4-beat cycle of about 3.1 s (slow, weighty); counting the flutter gives a driving, urgent pulse with a bar of about 1.5 s. Most listeners would probably tap the heavy step and feel the 156 as the heartbeat underneath; this matches the "heavy step with a fast heartbeat" reading in `video1/music_reading.md`, and is a guess about listeners.

## video2

| Source | Candidates (BPM : relative strength) | Top two |
|---|---|---|
| Drum stem | 120.2 : 1.00, 60.1 : 0.86, 161.5 : 0.70, 95.7 : 0.61, 80.8 : 0.50 | 120.2 vs 60.1, 14 per cent apart: not ambiguous by the 10 per cent rule; 60.1 is the half-time alternative |
| Full mix | 161.5 : 1.00, 120.2 : 0.95, 79.5 : 0.85, 95.7 : 0.85, 60.1 : 0.76 | 161.5 vs 120.2, 5 per cent apart: **ambiguous** (not an octave pair) |

- Kick (247 onsets): median inter-onset interval 0.505 s (118.8 BPM), histogram mode 0.50 s (120 BPM), upper quartile 0.99 s where beats are skipped [M]. Same median and onset count as `v1/data/video2/sync/bar120_check.json` (0.505 s, 247 onsets).
- Kicks on the grid: 120 BPM grid (refined 119.95) 78 per cent (194 of 247); 60 BPM grid 43 per cent; 161.5 grid (refined 160.1) 32 per cent [M]. The 120 grid fits the kick clearly better than either alternative.
- Bar phase: on the 120 grid, beat index 1 (0-based) carries 41 per cent of the low-band kick weight, 1.75 times the next beat [M]. This agrees with `bar120_check.json`, which also picks beat index 1 (weights 5333, 9311, 4306, 3833 here against 6598, 11332, 5886, 5107 there, same ordering). The two beat offsets differ (0.034 s here against 0.107 s there) because this script fits a free period and the check uses a fixed 120.000 BPM; the bar offset is not comparable between them, only the weight pattern. Still an assumption that the heaviest beat is beat one.
- Supported: **120 BPM, 4/4 (bar 2.0 s)**, consistent with `bar120_check.json` (120 BPM, 2.0 s bar) and the 120 BPM stated in `video2/music_reading.md`.
- Half/double-time alternative: 60 BPM (half-time, strength 0.86 on the drum stem, only 43 per cent of kicks on that grid); 240 BPM is outside the strong candidates.
- The tracker's 161.5 BPM: strength 0.70 on the drums and 1.00 on the full mix, ratio to 120.2 is 1.344, close to 4/3 rather than 2 [M]. That fits a figure of three sixteenths (0.37 s) against the 0.5 s beat, which `video2/music_reading.md` attributes to the bass's dotted-quaver figure; this script does not test that cause [L].
- Still ambiguous: in the full mix, 161.5 and 120.2 are within 10 per cent, so the mix alone cannot say which is the beat; the drum stem and the kick grid settle it for 120. Which beat of the bar is "one" is an assumption.
- How a listener would feel it [I]: a steady four-on-the-floor walk at 120 (a brisk walking pace), counted in fours, with the 60 BPM half-time feel available as a slow nod on every second kick; the 161.5 figure would be felt as a restless cross-rhythm over the pulse, not as a faster beat. Not tested on listeners.
