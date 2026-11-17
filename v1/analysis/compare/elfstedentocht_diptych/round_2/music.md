# Elfstedentocht Parts 1 and 2: the music compared (round 2, music colleague)

British English. Timestamps are `<video> m:ss`. Tags: H/M/L confidence. "Measured" means I computed it from `v1/data/` this round. Speculation is marked **[speculation]**. Nobody on the team has heard the audio; all sound statements rest on measurements and the music readings.

Read: round_1 `listener.md`, `picture.md`, `story.md` and my own round-1 `music.md`. Raw data checked: `data/video{1,2}/sync/sync.json`, `sync_kickgrid.json`, `grid_120bpm.json`, `audio_features/beat_times.json`, `scenes/shots.json`, `stems/vocals.mp3`.

## 0. A correction to my own round 1 (important)

In round 1 I quoted video2's sync as "37.2% of cuts within 80 ms of a beat against 42.9% by chance". That figure is **not against the 120 BPM grid**. The default `sync.json` for video2 uses the tracker's `beat_times.json`, which I have now checked: 693 beats from 42.68 s with a median spacing of 0.372 s, that is the 161.5 BPM figure that follows the bass's three-sixteenth pattern, not the 0.500 s kick grid. The test against the real grid is `data/video2/sync/sync_kickgrid.json` (grid from `grid_120bpm.json`: period 0.49995 s, downbeat 88.6165 s, kick offset SD 9 ms, 246 kicks):

- cuts within 80 ms of a beat: 36.0% against 31.6% by chance; beat-phase Rayleigh p = 0.093; half-beat p = 0.83; bar p = 0.20 (measured/reported in that file);
- first 42 s only (n = 10 cuts): beat p = 0.056, **bar p = 0.014**, mean bar phase 0.645.

So the conclusion stands (no reliable cut-to-grid lock across Part 2), but the evidence that was cited by me and by `listener.md` and `picture.md` is the wrong grid. Anyone writing up Part 2's sync should cite `sync_kickgrid.json`. The weak early cluster (10 cuts, in the pad-only opening, before the drums are steady) is worth a look but is a small sample (L).

## 1. Answers to colleagues

### 1.1 To me, from picture: is video1's tracker grid less reliable than video2's, so that its weaker lock is an artefact?

I think the answer runs the other way. Measured:

- **Tempo stability.** Video1's tracker beats (218, 0.95 s to 167.97 s) have a median interval of 0.766 s and SD of only 0.019 s (5th to 95th percentile 0.744 to 0.790 s). It is a steady grid, not a wandering one. The reading's "bar one is tracker-derived" concerns which beat is the downbeat, not the beat spacing.
- **Coverage.** The tracker stops at 167.97 s, so about 20.7 s at the end (the 2:48 sprint) has no tracker beats. Only 39 of video1's 51 cuts fall inside the tracked range.
- **Phase lock.** Against this grid the 39 in-range cuts do cluster at a consistent beat phase: R = 0.365, Rayleigh p = 0.0055 (reported in `sync.json`; I reproduced R and p = 0.0055 and added a permutation test with random cut times over the same span: p = 0.0074). The mean phase is 0.32 of a beat, about 0.245 s after the tracker beat. Video1 is therefore the only one of the two with a statistically clear beat-phase cluster. That is why only 7.8% of cuts are "within 80 ms of a beat" (below the 19.7% chance): the cuts are not on the tracker's beats, they sit at a steady offset from them.
- **Interpretation (M-L).** Either the tracker's phase is offset from the felt beat (plausible: the kick takes sixteenth positions, `music_reading` section on rhythm, and the hat is on the even half-beat slots, so a tracker could lock to an off-slot), or the editor cut at a fixed delay after the beat. I cannot separate the two from this data. The cluster disappears at half-beat (p = 0.95) and bar (p = 0.56). Weak support for a real lock: with R = 0.365 on a beat period the half-beat statistic should shrink, which it does; this is not evidence against.
- **So:** for video1 the headline "7.8% on the beat" should be read as "offset, not absent". Video1 is arguably the more beat-aware edit (cuts clustered at one phase), and video2, whose three tight joints are at narration and section events, is the more event-aware one. This reverses the picture reading's expectation. It is still a modest effect: 39 cuts, one significant test, no multiple-testing correction (L-M).

Also, `picture.md` says video1 has no cut at the biggest events (1:15.3, 1:40.0, 2:47.8); I agree, and note the 2:48 sprint falls outside tracked beats entirely.

### 1.2 To me, from story: do the Part 2 fragments (3:28.6 onward) sound like the town names, one per bar?

I cannot hear Dutch and have no audio ears; I can only test structure. What I measured on `video2/stems/vocals.mp3`, per 2.000 s bar on the kick grid, from 3:26 to 4:40:

- Of 37 bars, 28 have vocal energy starting within 0.05 s of the bar start (onset threshold 25% of the bar maximum). The few with later onsets are at the edges (3:26 to 3:30; 4:36 to 4:40). That agrees with the bar-lock the music reading reports (Rayleigh p about 3e-6).
- The stem is active (above 25% of bar maximum) for 10% to 63% of each bar, so a burst, not continuous speech. Consistent with "one short event per bar".
- **Count test.** The Part 1 list has 11 names (Sneek to Leeuwarden). Fragments run from about 3:28.6 to 4:37, about 34 bars. 34 is close to three passes of 11 (33). I looked for a repeat at an 11-bar lag: the mean correlation of bar-level MFCC means is 0.19 at lag 11 and 0.13 at lag 12, against 0.45 at lag 1 and 0.30 at lag 2 (continuity) and negative values at lags 5 to 8 (n about 37 bars, so about 26 pairs per lag). A faint bump, nothing a threshold would call a repeat. **Inconclusive (L).** It neither supports nor rules out the hypothesis, and 34 against 33 is a coincidence I would not lean on. I would need a person who knows the names to listen.
- Note a count problem for the hypothesis: Part 1's list takes 2:16 to 2:36, about 1.8 s per name (reported). A one-name-per-bar reading in Part 2 would be 2.0 s per name, plausible, but the Whisper segments you quote run at about 2 s because they are the bars, so the Whisper timing cannot discriminate between "names" and "any bar-locked fragment".

### 1.3 To me, from listener: was Part 1's 0.4 s hole a rehearsal of Part 2's 4 s one; is "dat is de Elfstedentocht" the same recording in both parts?

**Same recording.** I ran a normalised waveform cross-correlation of the vocals-stem excerpt against windows of the other occurrence (16 kHz, mp3 stems):

| Query | Searched in | Peak normalised correlation |
|---|---|---|
| V1 0:27 to 0:31.7 | V1 2:40 to 2:52 | 0.091 |
| V1 0:27 to 0:31.7 | V2 1:20 to 1:32 | 0.070 |
| V1 2:44 to 2:48.2 | V2 1:20 to 1:32 | 0.063 |
| control: V1 0:27 to 0:31.7 | V2 0:40 to 1:02 (different words) | 0.079 |

All are at control level, including the pair within Part 1. A sample-identical, unprocessed copy would give a clear high peak; the stems are separated and mp3-coded and each part is mixed with different processing, so the test would also miss a copy that was re-filtered, but it does rule out a plain reuse of the same audio clip. Together with my round-1 MFCC-DTW result and the story colleague's (cross-part distance lower for same words than for different words, but no better than the within-Part-1 pair) the evidence is: **same words, no evidence of the same take** (M that the words are shared, L on take).

**Rehearsal.** Not supported, and the facts are a little more awkward than I wrote in round 1. The sentence is heard three times (V1 0:27, V1 2:44, V2 1:24). The rhythm-section hole follows two of them (V1 2:47.8, V2 1:24.3 to 1:28.6) but not the first (V1 0:27 to 0:31.7, where the reading finds the band continuous, then widening). So the hole is not a fixture of the sentence. It is placed twice, once at 88% and once at 28% of the running time. "Rehearsal" requires Part 1's small hole to have been made with Part 2's in mind; no source documents the order of composition (`part_mapping.md`, `artist_and_tracks.md`) and a two-part release is documented, an authored arc is not. I withdraw "hole as signature" as stronger than "the same stage direction used twice" **[speculation on intent]**.

### 1.4 To me, from listener: after Part 1 does Part 2's 28 s of pad and thuds feel like relief or like a restart?

I cannot report feeling. What the data allows:

- **Relief in level.** Part 1 ends with its loudest, brightest run (centroid 2.9 kHz, width 0.62 to 0.86, 2:49 to 3:07); Part 2 opens at about -25.5 dBFS, roughly 15 dB lower, with no drums for 28 s. A drop of that size, from a bright and wide sound to a quiet pad, is the kind of change usually described as a release (interpretive, M).
- **Restart in content.** The story colleague's finding changes my round-1 reading. Part 2's narration begins again with "18 januari 1963" at 0:41.7, so Part 2 is a re-telling of the script from the date, not a continuation. Musically it is also a restart: new pedal (B against D), new tempo (120 against 78), new kit behaviour. My round-1 phrase "the answer in kind to Part 1's 3:08 of unbroken drive" is true of level only; of content it is a second version.
- **Therefore** I would now describe the pair as one script, two arrangements (Part 1 band-led, Part 2 an electronic build), with loudness as the only thing that reads like a continuous arc. Whether a listener hears relief or restart will depend on whether they take Part 2's start as a continuation of the preceding Part 1 or as a fresh track. That is a perceptual question for someone with ears.
- One pitch fact: Part 1's 3:08 end is on a D pedal, Part 2's pad is a B pedal, a minor third lower, in a set containing D (`music_reading` for both). I mention it only because it is the shared-pitch link; no cadence ties the two (L).

## 2. Building on and challenging colleagues

- **Picture's joint table (video2 0:28.08, 1:28.5, 2:36.6), accepted.** Each sits within 0.05 to 0.2 s of a measured music event, which fits `grid_120bpm.json` (bass entry 0:28.13; downbeat 1:28.62; loop change 2:36.8). I would add that these are all points where the **music** changes state, and where the narrator is silent or just ended (2:36.1). The pictures meet the music at section edges, not on the grid. That is what a hand editor who hears the track would do; it is also what any editor cutting at section changes would do (M, no way to tell).
- **Story's "one script, two films".** Strongly supported on the music side, as above. It weakens my round-1 "does one answer the other" section: the diptych is better described as variation than as answer. I keep the loudness staircase point only as a description.
- **Listener's ranking (Part 1 stand-alone, Part 2 as half of a pair).** I agree on the Part 1 event density; my numbers: bass below -50 dB for 52 s of 188 (28%) in Part 1 against 40 s of 305 (13%) in Part 2, and Part 2's quietest long stretch is the pad opening, not the middle. I would qualify "Part 2's long middle has no events": it has the bar-locked vocal fragments over 3:28.6 to 4:37, the brightening layer (24 to 28 dB at 4 to 8 kHz, about 3:00 to 4:24), and loop A to B at 2:36.8. These are slow rather than absent. Whether they hold a listener is a question about attention, not data.
- **Listener's caveat on "rock/guitar".** Agreed; I also would not cite CLAP "distorted guitar" for Part 1.
- **Not claimed.** I still find no shared melody, riff or bass line between the parts.

## 3. Open and revised points

1. The wrong-grid sync citation (section 0) should be fixed wherever it appears in the round-1 files.
2. Video1's cut-to-beat phase lock is real but offset by about 0.245 s from the tracker (p about 0.006); the cause (tracker phase against editorial delay) is unresolved.
3. Fragments in Part 2 as town names: untestable without a Dutch listener; my structural test is inconclusive.
4. Same take for the key sentence: no evidence for it; no evidence against it either, because of processing.
5. "Rehearsal" and "hole as signature": withdrawn to **[speculation]**.

## 4. New questions

1. **To picture:** Part 1's cuts cluster at about 0.245 s after the tracker's beat (39 cuts, p about 0.006). Which cuts are they, and are they spread through the film or concentrated in sections (the per-section table in `sync.json` has `cuts_on_beat_frac` and `cuts_per_10s`)? If they are all in, for instance, the 0:41 to 1:15 build, that tells us whether the offset is a habit of the edit or an artefact of one passage.
2. **To story and listener:** during the Part 2 fragment passage (3:28.6 to 4:37), the voice hits once per 2.000 s bar. Does the picture show a change per bar (a new person, place or sign) in any stretch of it, which would suggest that the fragments are tied to a visual list; or does it run independently of them? A listener who can hear Dutch should also say, for 3:28 to 3:50, whether any of the seven or eight sounds is a town name.
