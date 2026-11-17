# video2: the music, as a listener would hear it (blind reading, measurements only)

**Mode.** Blind: no context.md, no research, no web. I cannot hear; every statement is inferred from the measurements and from the window notes and specialist files (rounds 1 to 3: form, harmony, rhythm, sound, voice, feeling, lineage). Evidence keys: [IMG] music_views/window_NNNNs.png; [LVL] per_second_levels.json; [CH] chords.json; [AF] audio_features; [LY] lyrics/ (Whisper passes); [CLAP] clap_tags.json (weak); [WIN] window notes win_NNNN.md; [R1/R2/R3-x] specialist round files; [P] specialists' probe scripts in v1/scripts/agents/. Times are m:ss. Confidence is given as high, medium or low. Where I give a figure, I re-checked it against [LVL] unless I say otherwise.

---

## 1. The track in a paragraph

A single, instrumental-except-for-voices piece of about five minutes (5:00.9 of music, three last hits, a decaying tail, digital zero from about 5:04.2), in **B minor (Aeolian), at a constant 120 BPM in 4/4**, built like a loop machine rather than a song: no chorus, no key change, no tempo change, no cadence [R3-harmony, R3-rhythm, R3-form]. It opens with 28 seconds of wide, hazy, drumless pad and five long, ringing low strikes (0:00, 0:08, 0:12, 0:20, 0:24), then settles into a dry, centred, programmed stomp under a wide, tonal "wall" of sound, with a low, flat, spoken voice laid freely over it (0:42 to 2:36). At 1:28.6 a silence gives way to a drop where the kick moves onto every beat; at 1:40.6 the bass thickens. After a 52 s stretch with no voice the "other" stem slowly gets brighter (about +22 dB at 4 to 10 kHz between 3:00 and 3:50 on that stem; only about +3 to +8 dB on the full mix) while the chords do not change, a higher, gated, voice-like layer with no intelligible words recovered returns (3:28 onwards; voice or sample is unresolved), and the whole thing crests in a long plateau (3:36 to 4:36). It thins out into a ticking one-stab-and-one-call-per-bar mechanism, stops dead at 5:00.9, lands three off-beat hits, and goes to digital silence. It feels **serious, yearning and unresolved, then hypnotic**: gravity and distance at first, pressure and trance in the middle, "heat rising over a machine" at the top, and a closed door at the end, not a fade [R3-feeling, R3-sound]. The escalation is made of brightness and subtraction, not of louder drums or a changing tune.

---

## 2. Song map

Bar counts use a 2.000 s bar (120 BPM). Two lattices: bar 0 at 0:28.14 for the first half, bar 0 at 1:28.61 from the drop to the end [R2-form, R3-rhythm]. Section names are my interpretation; the times and levels are measured (high on times, medium on labels).

| m:ss range | Section | What is playing | What it feels like |
|---|---|---|---|
| 0:00-0:28 | Intro | Sustained, dense mid-range pad ("other" stem about -28 dB), wide stereo (width 1.1 to 1.5), mix about -25 dBFS. No bass (-85 to -90 dB), no voice. Isolated long-ringing strikes (drums stem) at 0:00, 0:08, 0:12, 0:20 and 0:24 (five; a smaller blip at 0:19; decay about 20 dB in 1 s), then the groove at 0:28. Harmony ('other' stem chroma, 4 s blocks): B-F# fifth with D (no G) 0:00-0:04; G+B+D 0:04-0:08; F#/D/B 0:08-0:16; G/B 0:16-0:20; D/F# 0:20-0:24; E/B/G 0:24-0:28 [WIN 0000, R3-feeling, LVL] | Wide, washy, hazy, wistful; "something large and old", a hopeful lift that sinks. No pulse; the strikes mark time |
| 0:28-0:42 | Groove arrives | Bass enters (about -23 dB mean over 0:28-1:10) and a skipping, programmed drum pattern; the kick mostly lands on the off-beat quaver [R3-rhythm]. Loop A begins (E-G-[A]-D, E-G-[A]-D, B in 2-bar blocks, 28 s repeat) [R3-harmony] | A trudge, a march with a limp; weight and distance |
| 0:42-1:28.6 | Narrated groove | Low spoken voice (f0 about 118-142 Hz; low-medium, lead_notes is sparse) in blocks: 0:42-0:48, 0:51-0:54, stem-measured 0:59-1:01 and 1:04.5-1:10.5 (Whisper gives 0:59-1:14, but the stem is silent after 1:10.5), 1:20-1:22, 1:24-1:28 [LY]. Two 14-bar passes of loop A. Drums stop twice: first stop 1:10 to about 1:20 (drums only; bass continues at -20 to -26 dB; sparse single hits at 1:16 and 1:19-1:20), second stop about 1:24.6-1:28.6 (drums and bass both absent, about 4 s) | Newsreel seriousness; the two stops make you count silently and wait |
| 1:28.6-1:40.6 | Drop, stage 1 (6 bars) | Kick now on every beat, snare on alternate beats, mix about +5 dB (-19 to -15 dBFS), speech cut off as the band lands | Relief, arrival, upright after the leaning kick; no tempo change |
| 1:40.6-2:36.6 | Drop, stage 2: locked groove (28 bars) | Bass +10 dB, narrower and drier mix (width 0.3), mix about -12 dBFS; speech 1:49-1:56 and 2:25-2:36; instrumental 1:57-2:25; fills at 2:08, 2:24 | Grip and pressure, hypnotic if you go with it. Loudness nearly flat from here on |
| 2:36.6-3:28.6 | Loop B "home", no voice (26 bars) | Bass loop B (B-A-D-[E], 12 s repeat); the tonic now returns every 12 s. The wall rises 8 to 10 dB at about 2:47-2:50 with unchanged spectrum, then its top end slowly brightens | Grounded, settled, warm; the human story has gone and the machine blooms |
| 3:28.6-3:36.6 | Voice returns | Sparse, gated voice-like bursts (vocal stem 50 ms peaks about -17 dB at 3:28-3:36; per-second -25 dB; 3:28.56 first, 3:32.4 next) over loop B | A pickup into the plateau; the stem shows bursts only a few dB under the other stem (stem bleed possible) |
| 3:36.6-4:36.6 | Plateau and crest (30 bars = five 6-bar cycles) | Dense chops (vocal stem 50 ms peaks about -16 dB; the earlier -43 to -40 dB was a median including gaps); brightness ramp (on the other stem) completes at 3:48.6; mix about -10 to -11 dBFS, loudest stretch 4:12-4:24; one longer high wordless phrase 4:29-4:36 | Heat rising over a machine; a broad top rather than a peak. Trance or sameness, depending on attention |
| 4:36.6-4:48.6 | Outro, stage 1 (6 bars) | Mix steps down 2 to 3 dB; at 4:37 the mix steps down about 2 dB and the bass is chopped by sub-0.3 s gaps (4:37.5-4:41.5), not a hole; last full B-A-D cycle runs 4:36.6-4:48.6 (D from 4:44.6) | Pressure leaves |
| 4:48.6-5:00.6 | Outro, stage 2 (6 bars) | Bass reduced to one stab per bar; one dry vocal call per bar (4:46.6 to 4:58.6, about -21 to -25 dB per call, about 4 dB spread) | A mechanism ticking on, absorbed |
| 5:00.9-5:04.4 | Hard stop and last hits | Rhythm section stops at 5:00.86; three off-beat hits about 5:02.34, 5:02.60, 5:02.85 (tail peak about -0.7 dBFS at 5:02.6, not the track's loudest sample); tail below -45 dBFS after 5:02.9; last non-zero sample 5:04.24 [LVL: 5:03 -57 dBFS, 5:04 -94 dBFS] | An abrupt, un-cadenced shut; a closed door, a small shock |

---

## 3. Harmony and melody

- **Key and mode (high):** B minor Aeolian. The whole-song key estimate puts B minor first (0.88), D major second, G major third [AF summary.json]; the flat sixth (G) is the single added colour over a B-minor-pentatonic palette, and there is no sustained G#, A# or D#; no real dominant and no cadence, even in the last 25 s [R3-harmony, CH].
- **Intro (medium):** the chord track shows only "Bm" for 0:00-0:42.7 [CH], which is the estimator's limit. Chroma shows more: a B-F# open fifth with D and no G at 0:00-0:04 (other-stem chroma), G+B+D at 0:04-0:08, F#/D/B at 0:08-0:16, G/B again at 0:16-0:20, a D/F#-led span 0:20-0:24 and a turn to E/B/G at 0:24-0:28 [WIN 0000; R3 harmony file; ERRORS.md notes the earlier mis-timings]. So: slow harmonic rhythm (blocks of about 4 to 8 s), a minor home with a dark flat-sixth shadow.
- **Two bass loops (high on notes, medium on the pickups):**
  - **Loop A (0:28-2:36.6, 28 s = 14 bars):** E-G-[A]-D, E-G-[A]-D, B, in two-bar blocks. The A is a short pickup before D.
  - **Loop B (2:36.6-4:36.6, 12 s = 6 bars):** B-A-D-[E]; the E is a pickup before the returning B. Loop B is more tonic-heavy [R3-harmony]; the specialists' pYIN shares (34% against 13%) did not reproduce in my CQT check (B about 13% in loop B), so I keep only the direction (B is 1 of 3 four-second blocks in loop B, 1 of 7 two-bar blocks in loop A).
  - The pickups are **stepped notes, not slides** (pYIN on the bass stem reads G2, A2, D2 with no intermediate pitches before D arrivals; D2, E2, B1 before B arrivals), each a short sustained note of 0.5 to 0.9 s with a 0.2 to 0.4 s re-articulation gap either side. Medium-high that they are steps; medium-low that they are "short, not percussive".
- **Upper layer ("other", medium-high):** holds a Bm-centred triad wall throughout. The lift at about 2:47-2:50 is an octave move onto a clean Bm triad, and the later growth (3:00-3:50) is height and brightness, not new notes [R3-harmony, R3-sound].
- **Melody:** there is no tune in the instrumental layers: no riff or repeating pitch shape in the intro pad [WIN 0000], and the only moving line is the bass loop. The voice supplies the only pitch gestures in the second half: chops wander G4, G#4, A4 irrespective of the chord; G# is **not** a chord tone in bass or "other" (bass G# under 0.3 of the strongest pitch class; "other" G and G# about equal and well below B, F#, D, A), so any Dorian colour (G# over Bm) belongs to the voice alone (medium-low; voiced fraction only 16 to 67%, octave errors possible) [R3-harmony, R2-voice].
- **Why it yearns (medium):** the tonic is withheld in loop A, the flat sixth is present, there is no leading tone and no cadence; the bass moves, the minor ground does not. Lifts are "weather changes, not hope that resolves" [R3-feeling].
- **What I cannot say:** that any chord's third is major or minor in a particular bar (the chord tracker is a pitch-class estimator), which note is "heard" as root where the bass is saturated, or whether D#/A# traces are overtones (I follow the specialists: overtones of a moderately saturated bass, medium).

---

## 4. Rhythm and groove

- **Tempo and metre (high):** 120.0 BPM, 4/4, constant from the first beat grid (about 0:28) to the end. The tracker's "161 BPM" [AF summary.json] is the 0.375 s hi-hat cross-rhythm, not the pulse; the snare on alternate beats and the grid make drum-and-bass at about 160 an unlikely reading [R3-rhythm].
- **Machine-exact (high on constancy, medium-high on "sample-like"):** kick inter-onset interval 499.99 ms (spread about 7 ms); level spread 0.6 dB; waveform correlation between kicks 0.79 (60 kicks, 2:00-2:30); kick phase stable to a few ms from 1:28.6 to 5:00 [R3-sound, R3-rhythm]. The drum stem stays near -19 dB from 1:40 to 4:50 [LVL: 100-156 s mean -19.0; 216-276 s mean -19.2].
- **The change at 1:28.6 (high for the numbers, medium for the reading):** before it, the kick mostly lands on the off-beat quaver (phase about 0.37 on the 0.5 s grid); from 1:28.61, on every beat (phase 0.11 to 0.13). The grid itself does not move; the kick shifts by **one quaver (0.25 s)**, and the snare takes alternate beats [R3-rhythm]. The preceding drum-and-bass silence lasts about 4 s (about 2 bars), not a whole number of bars, so the re-barring is built into the hole. Round 1 and 2 versions ("three semiquavers", "a beat", "5/4 bar") are withdrawn.
- **Hi-hat cross-rhythm (medium):** a 3+3+3 dotted-quaver accent spacing (0.375 s) is a programmed pattern, not a delay: the drum-stem hi-band autocorrelation has a bump at 0.375 s (0.25 against 0.06 to 0.14 for neighbours) but nothing at 0.75 s, so no decaying train of repeats [R3-sound]. I do not claim sixteenth hats from 3:40 (no step was measured; see ERRORS.md).
- **Syncopation:** the bass pickup on the last beat is the only anticipation against the grid, and the end figure "and, beat, and" repeats the early off-beat kick feeling [R3-harmony, R3-rhythm].
- **Fills and cell length (medium):** fills (elevated drums-stem onset counts in the bar ending) at about 1:56, 2:08, 2:24, 2:36, 2:48 and 3:00 (gaps 12, 16, 12, 12, 12 s); the 2:56 fill is not supported. My own onset counts depend on the detector (I reproduced elevated bars only roughly), so treat fill positions as medium-low; not a strict 8/16/32 plan. The working cell is 2 bars, with 6 bars (12 s) as the commonest unit and 14 bars for loop A [R3-form, R3-rhythm]. Hand-varied loop-machine logic, not a dance template.
- **Feel:** from 0:28 to 1:28 the pattern leans and skips; after 1:28.6 it stands upright. The only larger rhythmic events are the stops (1:10-1:16.5, about 1:24.5-1:28.6, the 5:00.9 stop). Everything else changes by layer and brightness, not by drum activity.

---

## 5. Sound and production

- **Intro space (medium on width, low on "hall"):** wide, decorrelated stereo (width 1.1 to 1.5 in 0:01-0:08; L/R correlation -0.22 at 0:05-0:10). That shows width, not a measured room; "hazy and washy", not "cathedral" [R3-sound]. Strikes are centred and long-ringing.
- **Groove section (high on levels):** a dry, centred kick and bass under a wide wall. Mix correlation rises from 0.32 to 0.79 at the drop because the centred bass and kick land on an unchanged wide layer, not because the wall narrows [R3-sound]. From 1:40 the mix width is about 0.3 to 0.5 [LVL].
- **The wall (medium on being one source; low on identity):** stem L/R correlation (other stem, re-measured) near 0 or negative in the intro (-0.24 / -0.21 / +0.10 for 100-400 / 400-1600 / 1.6-6k Hz at 0:05-0:25) but positive later (+0.25 / +0.26 / +0.07 at 2:00-2:30; +0.30 / +0.34 / +0.55 at 3:40-4:10), so the wall becomes more centre-weighted as it builds. Flatness 0.0004 and the P/H ratio are specialist figures I did not re-run. Instrument identity (guitar, synth, organ, choir) is undecidable: CLAP gives synth about 0 and guitar weak and intermittent, its stronger readings are drum machine, organ and choir, probably reading a sustained harmonic pad; no 50:50 figure is evidence-based (low) [R3-sound, R3-lineage, CLAP].
- **Build is brightness and automation, not density (medium):** 2:44-2:52: the 'other' stem rises 8 to 10 dB with an unchanged spectrum (about -28 to -21 dB per second on the stem); the full mix barely moves (-13.5 to -13.0 dBFS, under 1 dB): a bloom of the same stem material, not a loudness event. The 4 to 10 kHz band of the 'other' stem then rises about +22 dB across 3:00-3:50 (about +28 dB from 2:50), completing at **3:48.6**; there is no step at 3:30 [R2-form, R3-sound]. On the full mix the same band rises only about +3 to +8 dB, because drums dominate it, and on the stem it starts from a very low floor (20 dB or more under its 100-1000 Hz band). So it is a real but modest-in-the-mix brightening. Low-medium that it is a drive or filter opening rather than a hidden new layer. The 'centroid' wording in the specialist notes is ambiguous (about 1 kHz vs 300 Hz) and I did not re-run it.
- **Bass (medium):** fundamental-heavy, moderately saturated, re-attacked about once per bar, stepped pickups.
- **Levels (re-checked against [LVL]):** mix mean about -25.5 dBFS in the intro; about -18 in 0:28-1:10; about -15 at 1:28-1:40; about -12 from 1:40 to 3:28; about -10 to -11 at 3:36-4:36, with a 12 s mean peak near -10.0 around 4:12-4:24 (a mean, not a sample peak). The track reaches 0 dBFS (limiter or clipping; 374 samples above 0.999, the first at 1:32.1, every 20 s block from 1:20 at about 0 dBFS), so the last hit (tail peak about -0.7 dBFS at 5:02.6) is not the loudest sample.
- **Voice treatment (medium):** narration is band-limited, centred, gated and dry. Chops and calls fall 20 dB within 0.14 to 0.59 s, no long reverb or delay throw [R3-voice, R3-sound].
- **Ending (high):** a hard edit of drums and bass at 5:00.86, a brief tail, then digital zero.
- **Era or genre label:** layered, DAW-built production is a weak impression only; no measurement gives a date [R3-lineage].

---

## 6. Voice, words and samples

- **Two layers, two regimes (narration high; chops medium-low):** the narration (0:42-2:36) is a voice with high confidence (stem, transcripts and low pitch agree). The second-half layer is a vocal-stem-routed, voice-like layer, probably voice- or sample-derived; demucs can route a lead synth, guitar or processed sample to 'vocals', CLAP says 'no vocals' at 0.999 in every sampled window from 3:25 to 5:00 (it also says so over the narration, so it is no evidence either way), and the pitch tracker wanders (G4, A4, G#4, E4, A#4, F#3, D#3; G#5 and A5 at 4:00-4:36).
  1. **Narration, 0:42-2:35.8:** low (f0 118-142 Hz), flat, dry, free of the drum clock; the ten or eleven block onsets have no common bar phase [R2-voice]. It ends at the 2:36 loop change (bar 34) and is cut at the instant the band returns at 1:28.6 (vocal stem -34 dB at 1:28, -74 dB at 1:29) and again at 1:56.5.
  2. **Voice-like chops and calls, 3:28-5:00 (medium-low that this is a voice at all):** higher (pYIN mostly about 390-415 Hz, G4/G#4/A4, but also E4, A#4, G#5, A5 and D#3: a selective summary; octave uncertain), gated, over loop B. Loosely bar-anchored: about half of 36 bursts fall within 0.2 s before a bar start (chance is 10 to 20%), but they do not lock to the 6-bar cycle and are, if anything, off the beat in a 67-onset test (31% within 0.12 s of a beat against 48% by chance) [R3-voice, R3-form]. The final 4:46.6-4:58.6 calls fall one per 2.000 s bar at bar phase 0.00-0.03 on the kick-only beat (no snare), about -21 to -25 dB each (about 4 dB spread): triggered-sample-like behaviour (medium-low).
- **The words (low for sentences, medium for the numbers):** the narration is probably Dutch-like (the forced-Dutch pass, the English-translate pass and the small-mix pass agree on the date, '200 km', '16 degrees', '575', '9500', Sweden and Belgium; only the auto-language Welsh pass is nonsense, from a mis-detected language). The forced-Dutch translate pass yields: "18th of January, 1963" (0:42-0:48), "The Marathon Without Rain" (0:51-0:54), "In the morning, 6.30 in the morning, 200 km through a frieze ..." (0:59-1:14), "The city is called the twelfth elven stone" and "Where everyone stands up for themselves, that is the elven stone" (1:20-1:28), "Temperature 16 degrees below zero, a monster ride of more than 200 kilometers" (1:49-1:56), "575 motorway riders, around 9500 tour riders, Nato Zweden, Kaladezen, Zwitsers and Belgium" (2:25-2:36) [LY]. The vocals-stem auto-language pass labels it Welsh (p 0.57) and produces mostly nonsense words, apart from the digits "18 Januari 1963", "200 kilopetri", "575"; the language probability is a placeholder, and the passes differ on many other words. I can say with medium confidence that it is spoken, includes dates and numbers, and is probably Dutch-like narration of a factual, report-like kind (a date, a distance, a temperature, a head count); the rest of the sentence content is not reliable. I do not name a subject.
- **Second-half words (low):** no intelligible words recovered. Whisper returns inconsistent word-like strings (small-mix 'Stuck / End of the road / Climbing up' at 3:32-3:56; Dutch pass 'In de lopen', 'In de banken' at 3:38-3:48; vocals pass 'Fafn' x5 at 4:05-4:17), probably hallucinations on syllabic chops; whether the chops are wordless, syllabic or a processed sample is unknown.
- **Archival or produced, human or sample (low):** the speech is band-limited (energy to about 3.7 kHz at 95% roll-off), with abrupt edges, consistent with archival audio but also with stem estimation. The chops are not a simple repitch of the narrator (spectral centroids rose only 1.0 to 1.8 times, where a two-octave speed-up would raise them far more) [R2-voice]. The 4:29-4:36 high phrase has a 26-45 cent pitch wobble at 4 to 6 Hz (specialist figure, not re-measured), so it is not a rigid tuned synth line; it is human-like or LFO-modulated (low-medium).
- **Role (interpretation, medium):** the voice carries the human story first, then becomes texture, then a one-per-bar clock tick: words give way to rhythm as brightness rises.

---

## 7. The emotional journey, and its musical causes

All feeling is inferred from measured cause [R3-feeling]; levels are from [LVL].

| Time | What you would feel | Musical cause |
|---|---|---|
| 0:00-0:28 | Awe tinged with unease; looking at something large and old; a hopeful lift that sinks | Wide pad, no pulse, mix at -25 dBFS, slow chord blocks, flat-sixth colour; strikes at 0, 8, 12, 20 s mark time like tolls |
| 0:28-0:42 | Weight arriving, a limping march | Bass enters about 65 dB above the intro stem level (the intro bass stem is demucs noise floor, effectively absent); off-beat kick |
| 0:42-1:10 | Gravity, distance, a newsreel voice in front of a trudge | Low flat voice, dry; the kick leaning on the off-beat; loop A withholds the tonic |
| 1:10-1:16.5 and 1:24.5-1:28.6 | Suspense, counting in the silence | First stop: drums drop out (bass carries on, the voice ends at 1:10.5); second stop (about 1:24.6-1:28.6): drums and bass both removed, about 4 s, roughly 8 beats of near-silence |
| 1:28.6 | Relief, arrival, the floor under your feet | Kick moves onto every beat, mix +5 dB, speech cut at the same instant (a tension-by-subtraction payoff) |
| 1:40.6 | Grip, pressure | Bass +10 dB (largest single stem step of the first half), narrower, drier mix |
| 1:40-2:36.6 | Hypnotic pressure, or numbness | Loudness flat within about 2 dB; drums flat near -19 dB; the voice comes and goes over a fixed floor |
| 2:36.6-3:28.6 | Human absence; grounded, warm, rising; "something inhuman and swelling" | Narration ends; the tonic returns every 12 s; wall blooms 8 to 10 dB at 2:47-2:50 |
| 3:28.6-3:36.6 | A voice-like layer returns, in intermittent bursts | Gated bursts sitting a few dB under the other stem in the stem view (not shown to be quiet; demucs bleed could inflate the level) |
| 3:36.6-4:36.6 | Heat rising over a machine, a broad crest; trance or sameness | Top band (other stem) complete at 3:48.6, mix -10 to -11 dBFS, dense chops, a high phrase at 4:29-4:36 |
| 4:36.6-5:00.6 | Pressure leaving; the machine ticking on | Mix step-down and chopped bass at 4:37, then one stab and one call per bar |
| 5:00.9-5:04.4 | A little shock; suspension, not closure | Hard stop, off-beat three hits, digital zero, no cadence |

The core pattern (high on events, medium on feeling): **tension by subtraction** (the drum stop from 1:10 and the drum-and-bass stop before 1:28.6, the 5:00.9 stop; the 4:37 step-down is milder), **escalation by brightness** (not by tune or tempo), and a **slow pressure** of a unit change roughly every 12 s that holds attention without a clear melody.

---

## 8. The five moments a listener remembers, and why

1. **The drop at 1:28.6 (high).** About 4 s with no drums and no bass (1:24.6-1:28.6; the drums alone had dropped out from 1:10) after speech, then the kick lands on every beat, the speech is cut at that instant, and the mix rises about 5 dB. It is the biggest single change, and it comes as an arrival rather than as a new tempo.
2. **The bass thickening at 1:40.6 (medium-high).** +10 dB on the bass stem with a narrower, drier mix: a second, heavier landing 6 bars after the first.
3. **The wall blooming at 2:47-2:50 into the voice-free middle (medium).** The narration has gone (2:35.8), the tonic starts coming back every 12 s, and the same layer rises 8 to 10 dB: the music seems to grow without people.
4. **The long brightening, finishing about 3:48.6 and cresting by 4:12-4:24 (medium).** No new chord; the top band of the other stem climbs about 22 dB across 3:00-3:50 (about +3 dB on the mix). A listener may hear it as "brighter" more than "louder", but I have not shown by perceptual weighting that it is the main driver of the felt escalation (low-medium).
5. **The ending (high on events).** The step-down at 4:37, the one-per-bar calls, then the hard cut at 5:00.9 and three off-beat hits ending in digital silence. It is remembered because it does not resolve; honourable mentions are the high phrase at 4:29-4:36 (low-medium) and the date-and-numbers narration, which anchors the early part.

---

## 9. Where the specialists disagreed, and the best-supported view

| Issue | Positions | Best-supported view |
|---|---|---|
| Metre or tempo | Tracker 161.5 BPM; form and feeling used 0.372 s early; rhythm 120 BPM | **120 BPM** with a 0.375 s hat cross-rhythm; 160 is that cross-rhythm [R3-rhythm] (high) |
| What the 1:28.6 shift is | "three semiquavers" (R1), "a semiquaver" (R2), "a beat", "a 5/4 bar" | **A quaver (0.25 s) kick shift** inside a roughly 4 s gap; not a tempo change (high numbers, medium reading) |
| Did the whole band shift or only the kick | Harmony: maybe only bass; rhythm: kick | Kick measured; whole-band shift low-medium, chord tracker's 0.37 s hop is too coarse to settle it |
| Section structure | Regular 8/16/32-bar dance lattice (lineage R2) vs 2-bar-block, 6-bar cell | **No 8/16/32**: bars from the drop are 6, 28, 26, 4, 30, 6, 6; lineage withdrew it [R3] (medium) |
| Brightening start | 3:30 or 3:32 or 3:36 | A **ramp 2:50-3:50 completing at 3:48.6**; section edge at 3:36.6 (high on the ramp, medium on the edge) |
| 2:47-2:50 | A new layer joins vs a bloom of the same layer | **A bloom** (unchanged spectrum, 8 to 10 dB), low-medium |
| Voice on the grid | "floats", "6-bar blocks", "bar-anchored" | Narration has no bar phase; chops are loosely bar-anchored but not 6-bar-locked; calls from 4:44 are exactly one per bar (high for the end, medium-low for the middle) |
| Which beat the call falls on | "Beat 2" (R2) vs the bar's first kick beat (R3) | **One per bar on the kick-only beat, opposite the snare**; numbering undecidable (low) |
| Outro start | 4:37 vs 4:40 vs 4:48 | **4:36.6** (stage 1), 4:48.6 (stage 2) (high on levels) |
| Intro "hall" | R2 feeling: hall, awe | Only "wide and decorrelated" is measured (medium) |
| Guitar vs synth wall | 50:50 | Undecided (low) |
| Genre | "dance-rock", "post-rock", "cinematic electro" | Best fit: instrumental loop-built electro/dance-rock with a cinematic frame, second frame post-rock-style build (medium, with the caveat that lineage means resemblance only) |
| Vocal origin | Human vs sample | Open; calls behave like a triggered sample; the high phrase wobbles like a human or modulated source (low) |

---

## 10. Uncertainties and what the measurements could not settle

- **Instrument identity (guitar, synth, choir, bells, timpani) is not recoverable.** CLAP says "choir" and "bells" in the intro [WIN 0000], but CLAP is a noisy zero-shot model with strong time structure; it is a tie-break at most. The intro strikes are "low, long-ringing, percussive" (the 'centre about 65 Hz' is a specialist figure I did not re-measure; 'long-ringing' and 'percussive' fit a roughly 20 dB per second decay on the drums stem), nothing more.
- **Which beat is "1".** Bars are counted from phase estimates; I cannot say which beat the arranger would call the downbeat.
- **The words, language and speaker.** Transcripts disagree; the language probability is a placeholder; archival versus newly recorded cannot be told.
- **Whether the voice in the second half is sung, spoken, sampled or synthetic.** Only the final calls' behaviour (uniform, gated, on the grid) supports "triggered sample".
- **Whole-band or kick-only shift at 1:28.6.** Not settled; the chord tracker's hop is 0.37 s.
- **Chord thirds and the overtone question (D#, A#).** The chord tracker reports pitch classes only; I follow the overtone reading (medium).
- **Whether the brightening is a new layer or drive/filter on the old one.** Low-medium for the latter; stem separation could hide a layer.
- **Whether the 6-bar cell is design or a stacked 12 s loop.** Not recoverable.
- **Stem artefacts.** Demucs bleed, pYIN octave errors (voice above about 700 Hz), onset-picker misses (final hits corroborated only in timing) and 0.1 s RMS frames limit every fine-timing claim.
- **Feeling versus trance versus numbness.** The measurements show flat loudness and a changing top end; whether a listener finds that hypnotic or monotonous depends on attention and cannot be measured.
- **Known corrections from the project's own error log applied here:** the 0:42 top-band jump is the narrator entering; A to D is a perfect fourth; the D third of the pad fades at 4:36.8, not 4:48.8; the ending is a full-level hit at 5:02.3, not a quiet tap; the 3:24.8 vocal-stem blip is not a vocal fragment (real fragments begin about 3:28.6); and "both Dutch passes agree" is not claimed.


---

## Check log

Checks applied by a second pass that re-measured each refuted claim (scripts: v1/scripts/agents/check_music_refuted_v2b.py, check_music_refuted_v2c.py).

**Refutations that held and were fixed in the text**
- Peak level: audio/song.wav hits 0 dBFS from about 1:20 (374 samples above 0.999, first at 1:32.1); last-hit tail peaks about -0.7 dBFS. Not the loudest sample.
- Digital zero: last non-zero sample 5:04.24 (not 5:04.4).
- Intro strikes: drums stem decays at 0, 8, 12, 20, 24 s (-26.3, -28.0, -26.4, -24.7, -25.4 dB per second) plus a smaller blip at 19 s: five strikes.
- Drum stops: at 1:10-1:20 only drums drop (bass -20 to -26 dB); drums and bass are both gone only about 1:24.6-1:28.6 (bass -76 to -79 dB at 1:25-1:27). Section 7 and the "4.6 s hole" wording fixed.
- Narration 0:59-1:14: vocal stem -43 dB at 1:10 and below -75 dB from 1:11; Whisper's end time is not supported.
- 4:37 bass hole: bass stem -19 to -20 dB per second throughout 4:37-4:48, 0.1 s RMS shows only brief gaps; removed as a hole (a 2 dB mix step-down is what changes).
- Last B-A-D cycle: bass-stem pitch class B 4:36, A 4:40, D 4:44 (4-s blocks); bass falls away at about 4:48.5.
- Fills: partly held (bar onset counts are detector-dependent; I reproduced elevated bars only roughly), so fill times are softened and the 2:56 fill is dropped.
- Bass enters about 66 dB above the intro stem (-88.6 vs -22.9 dB mean); the intro value is noise floor.
- Intro chroma: re-measured in 4 s blocks; G is absent at 0:00-0:04 and G/B returns at 0:16, not 0:12.
- Brightening: 4-10 kHz at 3:30/3:40: mix -31.8 dB (3:30) rising to -29.8 (3:50) against the other stem -46.3 to -37.4, so the large figures are stem-only; text now says so.
- Wall L/R correlation: near 0 or negative only in the intro; +0.25 to +0.55 later.
- Outro calls: peaks -21 to -25 dB (my 50 ms peaks -22.3 to -25.4), not uniform to better than about 4 dB.
- Second-half voice level: vocals stem per second -23.6 to -28 dB at 3:28-4:00; 50 ms peaks about -17 and -15.6 dB. "Murmur" and "very quiet" removed.
- Wordless: replaced with "no intelligible words recovered" plus the Whisper strings (small-mix and vocals pass; I confirmed 'Fafn' and 'Climbing' exist in the transcript files).
- Human-voice confidence for the chops lowered to medium-low; CLAP "no vocals" noted as non-evidence in both directions.
- Guitar vs synth "50:50" removed; instrument identity undecidable.
- Dutch wording: agreement across passes acknowledged; the "contradict each other on most words" overstatement softened.

**Not re-run, left as specialist figures (labelled in the text)**
Hi-hat 0.375 s cross-rhythm, flatness, P/H ratio, 26-45 cent wobble, bass pickup shapes, pYIN bass shares (which did not reproduce), intro centre about 65 Hz, narration f0, chop pitch contour details, the 3:27.3 minor vocal-stem event, and all CLAP/lineage claims (weak evidence).

**Unverifiable from measurements:** instrument identity, words and speaker, kick-only versus whole-band shift at 1:28.6, chord thirds, sample versus performance.
