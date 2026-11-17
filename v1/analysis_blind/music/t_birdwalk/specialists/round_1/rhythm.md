# t_birdwalk: RHYTHM specialist, round 1 (blind, measurements only)

Evidence key: [BT] audio_features/beat_times.json + summary.json; [LVL] per_second_levels.json; [STEM] stems/stem_rms_per_second.json; [Wnnnn] music_views/window_nnnns.png (I opened W20 and W160 and checked the others via the window notes); [WN] the ten win_*.md notes; [R1-R6] my scripts in v1/scripts/agents/rhythm_birdwalk.py and rhythm2..6.py (librosa onsets on stems_raw drums/bass, onset-envelope autocorrelation and comb fits). Timestamps m:ss. I cannot hear: everything below is inferred from timing, level and spectra.

## 1. Headline

- **Felt tempo: about 76-80 BPM, half-time hip-hop, with the pulse grid tracked at 152-160 BPM (the double-time reading).** Confidence medium-high for the half-time feel, medium for the exact number. The tracker's 152 BPM [BT] is the sixteenth/eighth-level counting; a listener nods at about 76-80.
- **The tempo is not a rigid click.** My comb-fit of the onset envelope by section [R6] gives roughly: intro 0:00-0:12 152 BPM; 0:47-0:59 about 154; main groove 0:12-0:47 about 160; 1:00-1:23 about 163 (the tracker's 161.7 reading in the 60-80 s window agrees [BT]); 1:34-1:59 about 160; 2:12-2:23 about 156; 2:40-3:00 about 158. So the pulse speeds up by roughly 5 to 7 percent after the intro and stays between 156 and 163. The one-number "152" in summary.json is the intro tempo. Confidence medium: the combs are noisy and the beat tracker itself jitters (inter-beat gaps of 0.348, 0.325 and 0.441 s keep appearing [R3]), so I do not trust single beat positions, only section-level averages. The drum hits do not vary much from a steady spacing inside a section (see 2).
- **Metre: 4/4 at the half-time level, bar of roughly 3.0-3.15 s.** The evidence is a stack of consistent periods rather than a heard downbeat (medium confidence):
  - Intro drum hits recur at 1.53-1.61 s (0.80, 2.28, 3.81, 5.36, 6.93, 8.54, 10.12, 11.67 s [R2]). In 0:47-0:59 they are 1.58 s apart (50.85, 52.45, 53.95, 55.53, 57.11, 58.69) and again at 2:01-2:11 (2:01.3, 2:02.9, 2:04.5 per WN win_0120; my onsets 125.95, 127.55, 129.06, 130.65 s = 2:05.95, 2:07.55, 2:09.06, 2:10.65 [R2]). 1.57 s = 4 grid beats at 152, or 2 beats at 76. I read this as one hit per half-bar (beats 1 and 3, or kick then snare alternating), not a hit per bar, because the stutter gaps below give a 3.0 s repeat.
  - Stutter in 2:50-2:58 alternates 1.1 s and 1.9 s (WN win_0160, from mix-RMS dips: 170.30, 171.41, 173.34, ...). 1.1 + 1.9 = 3.0 s, which is 8 grid beats at 160 or one bar at 80 BPM. At the sixteenth level (about 0.19 s) that is a 6+10 split of 16 steps. Confidence medium; I did not re-derive those dip times myself.
  - Drum ioi histogram [R2] peaks at 0.1-0.2 s (hats/subdivision, 0.197 s is an eighth at 152 and a sixteenth at 76), then 0.3-0.4 s, then 1.4-1.6 s (the half-bar hits).
- Nothing in the measurements suggests 3/4 or 6/8. The bass often lands 3 grid beats apart (autocorrelation peak 1.10-1.15 s in most windows [R1]), but that is a syncopated pattern against a four-beat drum frame (see 3), not a triple metre. Low-medium confidence on that reading.

## 2. Drum patterns by section (drums.wav onsets [R1, R2], levels [STEM])

The drum stem is better thought of as a set of different "modes" than as one kit pattern.

1. **Sparse pulse mode (one broadband thump per half-bar, nothing between).** 0:00-0:12 (hits at 0.8, 2.28, 3.8, 5.4, 6.9, 8.5, 10.1, 11.7 s, drums about -34 to -38 dB [STEM], bass absent -70 dB); 0:47-0:59 (1.58 s spacing; hits are broadband, snare-like from the fold in [R4], some with low content); 2:00-2:11; and the return at 2:35.7-2:40 (WN win_0140: hits at about 2:35.4, 2:37.9, 2:39.3). This is the "empty room" mode. Confidence high that it is sparse and regular, medium that it is a snare/clap rather than a kick.
2. **Groove mode, mid-level (0:12-0:47, 1:00-1:33).** Drum stem sits at -30 to -35 dB, but the mix is full because the bass is at about -14 dB [LVL/STEM]. Onsets per 4 s are only 3 to 9 in 0:24-0:47 (vs 15-17 during busy parts [STEM table above]), so the groove is carried largely by the bass and the voice, with the drums as accents on a roughly 1.4-1.6 s frame plus short flurries. W20 shows this clearly: drum stem has a thump at about 5.0, 7.5, 9.2, 10.4, 12.5, 14.7 s of the window, i.e. 0:25, 0:27.5, ..., with irregular 1.1-2.5 s gaps, while the bass stem shows a stab about every 0.7-1.1 s. Medium confidence.
3. **Busy mode (0:12-0:24, 1:06-1:30, 1:34-1:59, 2:16-2:23, 2:44-3:06).** Hits at 0.15-0.4 s spacing, eighth/sixteenth density (onsets per 4 s 11-18). At 0:20-0:24 there is a burst of hi-frequency clicks every 0.15-0.2 s (hat roll, WN win_0020 and my onsets 20.03, 20.22, 20.41, 20.61, 20.79, 20.93 [R2]: spacing 0.19 s, i.e. a steady sixteenth-note roll at 76/152). The loudest drums are 1:38-1:50 (-15 to -17 dB) and 2:52 (-16 dB), where the kick/snare are well forward.
4. **Hit-by-hit: kick/snare identification.** A band-split fold [R4] gives kick (30-150 Hz) and snare (150 Hz-2.5 kHz) energy that is only weakly periodic over whole sections because of the tempo wander, so I cannot print a clean bar diagram. In the one tidy section (2:12-2:23, section 132-143 s in the fold) kicks sit on three of the four beat positions with the snare on the third: beat 1, "2", beat 3 (snare), beat 4 kick. Confidence low; treat as "a snare-type hit on beat 3 of the half-time bar, kicks around it".
5. **No reliable evidence for swing or triplets.** The IOI histogram shows steady 0.19-0.2 s spacing with no obvious long-short alternation. Rapid hat rolls look straight. Confidence low-medium, because the beat grid is not locked enough for a swing-ratio measurement.

## 3. Bass rhythm and the syncopation

- Bass onsets [R5, per-section IOIs in units of the 0.1965 s eighth]: most intervals cluster near 4 and near 6 (also 3 and 5): e.g. 0:12-0:30: 4.0 5.7 5.3 4.0 1.8 3.9 1.5 4.2 4.1 3.6 ... ; 0:30-0:47: 3.7 5.6 5.4 3.2 3.0 2.8 5.0 3.4 5.6 ... ; 2:11-2:23 (131-143 s): 4.7 3.8 6.0 6.0 ... ; 2:36-3:00: 4.2 4.0 6.0 5.2 4.1 5.8. Read at 152-160 BPM, that is notes 2 beats and 3 beats apart: a 2+3 (or 3+3+2, 4+6+6 in eighths) cell, i.e. a dotted/tresillo-feel bass line that cycles every 1.1-1.2 s (autocorrelation peaks of the bass onset envelope at 1.10-1.20 s in nearly every 20 s window [R1]) against drums on a four-beat (1.57 s) frame. The two never sit in a simple 1:1 relation, which produces a lopsided, rolling bounce.
- Short plucked/sub notes with fast decay (W20 bass panel, WN win_0060), so the rhythm is "stab - space - stab". At 0:20-0:47 the bass level never falls below -14.5 dB [STEM]: the bass, not the drums, is the primary pulse carrier. Confidence high on that point.
- Bass pitch is mostly a single pitch (A1, about 55 Hz in 2:40-2:49 per WN win_0160); so the rhythm of the bass, not its melody, is its content. (Harmony specialist, see question 2.)

## 4. Where the pulse stops, thins or lurches (the key rhythmic events)

All values from [STEM]/[LVL] unless noted; my own 4 s tables confirm them.

| Time | Event | Evidence |
|---|---|---|
| 0:00-0:12 | Bass absent, sparse hits every 1.55 s, with a falling filter-sweep-like gesture at about 0:09-0:12 (WN win_0000) | bass -70 dB; drums -34 to -38 dB |
| 0:12 | Re-entry by addition: bass +53 dB, drum onsets 3 -> 8 per 4 s; loudest broadband hit at 12.2 s | STEM; R1 |
| 0:20-0:24 | Hat/click roll at 0.19 s spacing, onsets 17 in 4 s | R2 |
| 0:47 | Bass drops out in one second (about -14 to -71 dB, -35.6 at 0:56-0:60 transitional), drums stay sparse; "other" also thins | STEM; WN win_0040 |
| 0:59 | Bass returns (+53 dB, mix +5 dB) | STEM |
| 1:23-1:33 | "Other" gone (-58 dB), bass hits only about every 3 s, drums sparse with near-total stop at about 1:25.5-1:27 and 1:29-1:30 (gaps in drum stem) | WN win_0080 (from images); STEM |
| 1:33-1:40 | Build: drums regular and heavy (-25 to -21 dB), "other" returns with a rising sweep | STEM |
| 1:40 | Bass steps from about -22/-25 to -41 dB in about 0.2 s and falls to -66 to -75 at 1:43-1:44; returns 1:45-1:47 | STEM; WN win_0100 |
| 1:59 | Hard stop of bass and most drums (mix 6-8 dB down); drums drop to one hit per 1.57 s; bass off to 2:11 | STEM; WN win_0100/0120 |
| 2:11.4 | Re-entry by addition (bass +55 dB, +6 dB mix), no fill before it, possible tom-like roll at 2:17-2:19 | STEM; WN win_0120 |
| 2:23.5-2:35.7 | **Clean stop of the whole rhythm section for about 12 s**: drums -65 to -70 dB, bass -71 to -73 dB; voice (-19 to -20 dB) and "other" carry on; drums fade to -53 at 2:23 and stop abruptly at about 2:23.5 | STEM table; WN win_0140 |
| 2:35.7 | Sparse hits and bass return with a block of low-frequency energy at about x=15.7 s of W140 | WN win_0140 |
| 2:47-2:50 | Voice stops entirely (vocal stem -57 to -70 dB); drums heavy and rising (-23 -> -16 dB), "other" +12 dB | STEM; W160 |
| 2:50-2:58 | **Stutter/gate**: dips of 14-31 dB in the mix at 1.1 s and 1.9 s alternately (3.0 s cycle) | WN win_0160 (mix RMS) |
| 2:58 | Falling sweep (vocal stem, W160 at about x=17-19 s) into last groove | W160 image |
| 3:00-3:08 | Fade: -14 dBFS to -44.5 dB in 7 s; drum gaps at about 3:00, 3:02, 3:03, 3:05-3:06 | WN win_0180; STEM |

Notes on the table. (1) Re-entries at 0:12, 0:59, 2:11 and 2:35 are always "by addition", not by drum fill: the ear gets a sudden floor, which is a recurring design device here, not a one-off. (2) The 0:47 and 1:59 breakdowns each strip the bass but keep the sparse 1.57 s pulse, so the pulse is never lost and the groove re-enters on the same grid. (3) The 2:23.5-2:35.7 stop is the only place the pulse is entirely carried by something other than bass and drums; I could look for the "other" stem's onsets (it is chopped and stabbed per WN win_0140), and I believe it keeps the grid, but I did not measure that.

## 5. Voice as rhythm

- Voice-stem onsets cluster on a 0.38-0.40 s period (autocorrelation peak in vocals at 0.372-0.395 s in all but one window [R1]) and a 1.46-1.60 s period, so the delivery is locked to the same 4-beat/half-bar frame as the drum hits. Confidence high on that numerical match.
- Syllable bursts at 0.2-0.4 s in 2:40-2:47 (WN win_0160) are the chopped-voice section; the lead-note tracker puts the pitch near E3-F#3 through the bursts (speech inflection, not melody).
- 0:47-0:59: the fragments "lock to the drum hits" (WN win_0040); in the table of hits (1.58 s) this means voice-and-drum are literally the same pulse.

## 6. What the pulse does to the feeling

1. **Swagger / strut** (medium-high): half-time at 76-80 with a 2+3 bass cell that never quite lines up with the 4-beat drum frame gives a lopsided, loping gait. "Bird walk" fits the gait, but I do not know the lyric context; a human would feel a head-nod pace with double-time hats on top.
2. **Tension by subtraction** (high): the 1.57 s sparse-hit passages (0:00, 0:47, 2:00, 2:35) are felt as held breath; then the drop by addition delivers weight (+50 dB of bass in a second). The 2:23.5-2:35.7 gap is a 12 s rhythm-section stop, the longest in the track and the biggest rhythmic gesture.
3. **Urgency and rush** (medium): tempo grows 152 -> 160 -> 163 over the first minute and a half (my combs), a slight push that a listener would hear as increasing drive; the 2:40-2:47 voice chops at 0.2-0.4 s add machine-gun energy.
4. **Hypnotic / trance-like** (medium): bass is on one pitch (A) and the rhythm cell repeats; with little harmony the groove carries all the interest.
5. **Jerky ending** (medium-low): the stutter at 2:50 and the ragged drum gaps in the 3:00 fade leave the pulse broken as it fades, so the ending feels like a hanging rather than a resolved landing.

## 7. Checks against the window notes (agreements and disagreements)

- All the ten window notes use 152 BPM as headline and suggest half-time; I agree on half-time and add that the speed varies 152-163 (they used the tracker's whole-song mean; win_0160 noted 161 BPM locally, consistent with my combs).
- win_0000 and win_0120 say the intro and 2:00-2:11 hits are "one per bar"; I think half-bar (two beats at 76) because of the 3.0 s bar suggested by the 2:50 stutter and the bass cell. Medium-low confidence; a 1.57 s bar (four beats at 152, one hit per bar) is the notes' reading and remains possible.
- win_0020: "drum stem shows only a few discrete clicks, not a hi-hat grid": agreed for 0:24-0:47; I found a hat roll at 0:20-0:24 and busy mode elsewhere. W20 image confirms.
- win_0100: "continuous drums at 4 onsets/s" matches the 11-18 per 4 s I counted; their "kicks almost every beat" (win_0120 on the previous window) is plausible for 1:38-1:50 where kick energy is at its highest.
- Disagreement risk: the notes label hits "kick/snare" by spectrum; demucs bleed means "drums" includes some hits triggered by other layers. Low confidence on all instrument labels.
- Not verified by me: bass at 1:23-1:33 "about every 3 s" (taken from win_0080 notes); stutter dip times (win_0160). I did not re-compute them.

## 8. What the measurements cannot tell me

- Whether the drum sound is a drum machine, a sample or played (CLAP says "drum machine" and "hip hop" at times but is noisy).
- Which half-bar hit is kick and which is snare in the sparse mode.
- The true bar line and count-in: all downbeat labels above are inferred from period arithmetic, not heard.
- Whether the tempo wander is deliberate (e.g. a sampled/live source with a tempo-mapped drum track) or an artefact of my comb fits and a jittery beat tracker. If the track was made on a grid, a flat 160 would be expected and my 163/152 numbers would be bias; but the intro at 152.3 is repeatable across three methods (tracker, drum autocorrelation 1.53-1.61 s / 4, onset comb).
- Whether the stops are edits or played breaks.

## 9. Questions for fellow specialists

1. **To harmony:** the bass is a stabbing single pitch (about A1, 55 Hz) on a 2+3-eighth cell that cycles every 1.1-1.2 s: does the chroma show any bass movement off A at the 1:40-1:46 bass dip, the 2:50 step "down and shift in the sub" (win_0160), or the 3:04 F#m ending, and do chord changes ever line up with the 3.0 s bar I infer?
2. **To form:** I find four "by addition" re-entries (0:12, 0:59, 2:11, 2:35) and a 12 s rhythm stop at 2:23.5-2:35.7; do your section boundaries (auto sections have 0:12.9, 0:47.5, 0:59.8, 1:23.4, 1:33.8, 1:59.5, 2:12, 2:23, 2:36) agree with these, and which ones sit on the same bar grid (3.0 s multiples) in your count?
3. **To voice:** the vocal onsets lock to 0.38-0.40 s and 1.5-1.6 s periods: is the chant at 2:40-2:47 a one-syllable-per-grid-beat delivery (about 0.19 s sixteenth, which would double the vocal rate), and does the rapped 1:23-1:33 verse stay on the same grid, or does it float over it?
