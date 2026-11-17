# t_birdwalk: FORM and DYNAMICS specialist, round 1 (blind, measurements only)

Evidence key: [LVL] music_views/per_second_levels.json; [W0..W180] music_views/window_NNNNs.png; [OV] audio_features/overview.png; [EDGE] my script v1/scripts/agents/form_edges.py (0.1 s RMS on-off edges of each demucs stem; thresholds -45 dB, drums -50 dB); [MAP] v1/scripts/agents/form_map.py (per-second table); [SIM] my mel-spectrogram correlation checks between stem segments (inline Python, not saved); [WIN] the ten window notes. British spelling; times m:ss. Duration 3:08 (188.15 s); tempo estimate about 152 BPM (audio_features/summary.json), but see rhythm caveat in section 7.

## 1. The one-paragraph answer

This is not a verse/chorus song. It is a **loop-and-subtract arrangement**: a very loud, flat, dry, near-mono groove (about -12 to -14 dBFS all the way through [LVL]) is repeatedly **taken away and put back**. The tension and release are made almost entirely by removing and returning **the bass**, secondarily the drums, the "other" layer and the voice, and by the stereo image snapping wide (about 0.5-0.7) whenever the bass leaves and narrow (about 0.05-0.3) whenever it returns [LVL]. The key never leaves A; the tune does not develop. Form is therefore a **layer map**, and the best way to read the song is as three 12-second "floor-drops" (0:47, 1:59, 2:23) cut into a 3-minute groove, plus a 12-second intro and a voice-less final stretch that fades out.

## 2. Song map (with evidence)

Bass on/off edges [EDGE] define the skeleton; everything else hangs from them. "Wid" is stereo width, "mix" is mean dBFS from [LVL] over the section.

| Time | Section (my label) | Bass | Drums | Voice | Other | mix / wid | Evidence |
|---|---|---|---|---|---|---|---|
| 0:00-0:12.4 | **Intro / call** | off | one hit per bar (about 1.55 s apart: 0:00.3, 2.2, 3.7, 5.3, 6.9, 8.5, 10.1, 11.6) | in at 0:00.9 | present, quiet | -19 / 0.46 | [EDGE] drums; [W0]; [WIN 0000] |
| 0:12.4-0:47.2 | **Groove A (first drop)** | on (35 s) | busier, then thinning to sparse cracks | continuous | stabs | -12.4 / 0.16 | [EDGE] bass on@0:12.4; [LVL] bass -69 to -19 dB, mix -18 to -13 |
| 0:47.2-0:59.3 | **Floor-drop 1 (break)** | off 12.1 s | one hit per bar again | continuous | wide-band bursts, wider image | -18.2 / 0.53 | [EDGE] bass off@0:47.2 on@0:59.3; [W40] |
| 0:59.3-1:59.2 | **Groove B (the long stretch, 60 s)** | on, with internal gaps (below) | dense | continuous | stabs, one 10 s gap | -13.0 / 0.16 | [EDGE] |
| 1:59.2-2:11.3 | **Floor-drop 2 (repeat of drop 1)** | off 12.1 s | one hit per bar | continuous | bursts | -18.2 / 0.53 | [EDGE]; [SIM] below |
| 2:11.3-2:23.5 | **Short re-entry (12 s)** | on (A1 about 55 Hz) | clusters, then kick/snare | continuous | stabs | -12.9 / 0.30 | [WIN 0120] YIN 55 Hz; [EDGE] |
| 2:23.5-2:35.7 | **Floor-drop 3 (the deepest)** | off 12.2 s | **none at all** (drums off 2:23.2-2:36.1) | continuous, exposed | stabs with dips | -18.4 / 0.54 | [EDGE]; [W140] drums/bass panels black 3.5-15.7 s |
| 2:35.7-2:47.5 | **Final groove, voiced** | on | sparse, mid/high | chopped syllables, stops 2:47.5 | quiet, then jumps | -12.8 / 0.28 | [EDGE]; [WIN 0160] |
| 2:47.5-2:57.1 | **Voice-free drum-and-bass block** | on | louder (about -16 dB), kick-like low line | **absent (9.6 s)** | loud (-23 dB), stuttering gaps | -14 / 0.16 | [EDGE] vocals off@2:47.7 on@2:57.1; [LVL] |
| 2:57.1-3:01 | **Last vocal glide, last push** | on | on | falling glissando 2:58.5-2:59.9 | peak -23 dB | -11.5 to -14 | [WIN 0160/0180]; [LVL] vocals -38 at 2:58 |
| 3:01-3:08 | **Fade-out** | cut 3:03.3, ragged tail | thins, off about 3:07 | none | falls fastest | -14 to -44 dBFS | [LVL] 3:01 to 3:07; [EDGE] |

Confidence: boundaries within 0.2 s, high (hard stem edges in [EDGE], matched by [OV] section lines and the window notes). The *labels* are mine; the measurements show layer presence, not "verse" or "chorus".

### 2.1 Smaller structural events inside the grooves

- **1:23.0-1:33.2, "other" layer removed (10 s)** [EDGE]: bass, drums and voice stay, mix stays at -13 dBFS, but width collapses to 0.00-0.05 [LVL, MAP]. This is a **thinning that does not lower the level**: the opposite of a floor-drop. The sound becomes a mono beam. The layer returns at 1:33.2 with a rising sweep [WIN 0080]. Medium-high confidence.
- **1:34-1:54, drum-led section**: drums rise to -15 to -20 dB (loudest of the song, against -26 average in groove B) and are continuous (about 4 onsets per second [WIN 0100]).
- **1:41.4-1:46, bass hole (about 4-5 s)** [EDGE]: bass drops from -25 to about -66 dB, with a short blip at 1:42.1-1:42.4 and a ragged return 1:44.9-1:46.0, then full by 1:47. Drums and voice continue. A *mini* floor-drop, at a bar scale, not a section.
- **1:51.2-1:53.2**: two bass blips off/on [EDGE]; drums lighten from 1:52 (-22 to -28 dB) [LVL]; a sweep at about 1:55-1:57 [W100]; voice pauses 1:54.0-1:57.6 [EDGE]; vocal peak and mix maximum at 1:58 (-10.4 dBFS, the loudest second of the track [LVL]). This is a **run-up to drop 2**: lighten, sweep, shout, cut.
- **2:32.5-2:35.5 riser**: diagonal sweep across the spectrum in mix and voice [W140, x = 12.5-15.5 s]; bass and drums return at 2:35.7 [EDGE]. Textbook pre-drop riser (high confidence on the sweep, which is plainly visible in W140).
- **2:42-2:57 stutter**: short RMS dips of 14-31 dB at about 2:42.75, 2:44.7, 2:45.8, 2:48.6, 2:50.3, 2:51.4, 2:53.3, 2:54.5, 2:56.4, 2:57.4 [WIN 0160]; the later ones spaced 1.1 s / 1.9 s alternately. I have not re-measured these; I adopt them as medium confidence.

## 3. Tension and release: how it is engineered

1. **Release is a loss, tension is a return.** The usual pop pattern (build to a loud chorus) is inverted. The groove is the "home" state at constant loudness; the **floor-drops are the contrast** (mix falls 6-8 dB: 0:47 -11.3 to -18.7; 1:58 -10.4 to -18.5; 2:23 about -11.7 to -20.7 [LVL]) and the **re-entries are the payoff** (+5 to +6 dB: 0:11/0:12 -17 to -13; 0:59 -19 to -13; 2:10/2:11 -19 to -13; 2:35 -17 to -13.5 [LVL]). The "bang" is the bass coming back, not a new instrument.
2. **A level drop that is mostly bass.** Bass falls by 50-55 dB at each edge (e.g. -14 dB to -72 dB at 0:47, -15 to -71 at 1:59, -17 to -75 at 2:23 [LVL]). Everything else is roughly constant. Since the bass carries most of the energy under 150 Hz (low-end share 0.77-0.93 in the final groove [WIN 0160]), its removal is felt as weightlessness.
3. **Space as the second axis.** Width goes up to 0.5-0.7 in every break and down to 0.0-0.3 in every groove [LVL]. The break is therefore wider, lighter, more exposed and the groove is a tight centre-panned wall. Plausible cause: the bass and kick are mono-centred and dominate the side-over-mid ratio when present (my inference, not verified by stem width).
4. **The voice is the constant.** The vocal stem stays at -17 to -23 dB through the breaks [LVL], so during a floor-drop the voice is **exposed rather than interrupted**. The only real silence of the voice is 2:47.5-2:57.1, in a *groove* (bass on), the inverse of the breaks.
5. **Anticipation by a long hold.** The breaks last about 12 s (about 7.8 bars of 1.55 s, so roughly 8 bars). That is long enough to feel like waiting; the clearest build device is the riser at 2:32.5 before the third break ends. Breaks 1 and 2 have no visible riser on the full mix at the re-entry (I did not find one); a faller at about 0:09-0:12 [WIN 0000] precedes the first drop.
6. **Delayed gratification.** Drum density is deliberately low in the intro and breaks (one hit per bar) and the first groove thins to a sparse crack-per-bar rhythm; the *densest* drumming is held back to 1:34-1:54 (about 20 s). The song therefore saves its "busiest" for about the middle of the 60-second groove B.

## 4. The big moments, in my ranking

1. **0:12.4: the drop that starts the groove.** Bass enters from nothing, drums densify, mix +5 dB, width 0.46 to about 0.22 [LVL, EDGE]. First and best example of the song's device. High confidence.
2. **2:35.7: the return after the deepest break.** Drums and bass both absent for 12.2 s, riser, then both return together [EDGE, W140]. It is the most "complete" absence (no drums either), so the biggest relative release.
3. **0:59.3: the return after break 1**, +6 dB, with the voice carried through unchanged [LVL].
4. **1:58-1:59: the cut.** Loudest second (-10.4 dBFS), then everything but voice and "other" falls away [WIN 0100, LVL]. This is the sharpest *cut* in the song (-8 dB in one second, width 0.18 to 0.70).
5. **1:41-1:47: the bass hole inside groove B**, a miniature drop with a slam at 1:47 [WIN 0100].
6. **2:47.5-2:57: voice leaves**, leaving a drum/bass/other block, and then **2:57-3:00 the falling vocal glide** (C5 down to B3 in about 1.5 s [WIN 0160/0180, lead_notes]).
7. **3:01-3:08: the fade**: a 30 dB monotonic fade in which other falls first, then bass, then drums [WIN 0180, LVL]. Confidence high on the order.

## 5. A repeated-material finding (new, from my own checks)

[LVL] shows that the per-second profile for 0:48-0:59 and 2:00-2:11 is nearly identical (mean absolute difference of 0.61 dB over 12 s at lag 72 s; the next-best alignment was 2.6 dB). I checked the audio itself [SIM]: mel-spectrogram correlation between 0:48.5 and 2:00.5 is **0.94 on the vocals stem, 0.94 on "other", 0.87 on drums**. A correlation that high on a *voice* stem is hard to explain unless the two breaks reuse **the same recorded material** (a repeated take, a loop or a copy-paste). Window-wise vocal correlations elsewhere are 0.66-0.90, which is what a repeated chant phrase produces by itself, so the 0.94-0.95 at this one lag stands out. 6-second block matches: 0:48 matches 2:00.0 at 0.95; 0:54 matches 2:06.0 at 0.90; 2:00 matches 0:48.0 at 0.95 [SIM]. Medium-high confidence that breaks 1 and 2 are the same 12 s block; I cannot say whether it is looped or re-performed identically. Break 3 does **not** match (best vocal match 0.83 to 2:11.8, an ordinary chant-phrase match) and has no drums, so it is the one "new" break.

Consequence for form: the song is closer to an **A B A' structure with a vamp** than to continuous development: break 1 is "heard again" at 2:00 and a different, emptier break arrives at 2:24.

## 6. What the form feels like (a human reading)

- **Nodding, looping, a little hypnotic:** the groove never develops harmonically (key A all the way; A minor 0.50 against A major 0.47 [summary.json]; chroma flat on A across [OV]). Interest comes from *what is missing*.
- **Playful and pushy rather than climactic:** nothing builds to a bigger version of the groove; the loudest second (1:58, -10.4) is a shout before a cut. Energy is dispensed in cycles of about 35 s on, 12 s off, 60 s on, 12 s off, 12 s on, 12 s off, 27 s on, then fade.
- **A gradual narrowing of the shape:** drops come at 0:47, 1:59, 2:23: the interval shrinks (72 s, 24 s), the groove spacing between breaks falls from 60 s to 12 s, so the song seems to **accelerate** its own cycle: more drops, shorter grooves, then the final 27 s run to the fade. This is my interpretation of the timestamps, medium confidence.
- **The ending is a draining, not an arrival:** no final chord or cadence is measured (WIN 0180 says the harmony drifts to F#m, low confidence). The fade is a volume ramp (-14 to -44 dBFS), dry, so it is more like the volume being turned down than a natural stop.

## 7. Caveats and things measurements cannot tell me

- Layer names (bass, drums, other, vocals) are demucs outputs; stems leak (voice bleeds into "other" [WIN 0000]), so a "silent" stem edge of -45 dB is safe but fine details such as 1:42.1-1:42.4 blips may be artefacts.
- The 8-bar block idea assumes a bar of about 1.55 s, from the intro's one-hit-per-bar drums [EDGE]. The beat tracker says 152 BPM (0.39 s) and swings between 80 and 162 in [OV]; the true metre is not established (rhythm specialist's job). Break lengths of 12.1-12.2 s are exact measurements; "8 bars" is not.
- I cannot say whether the drops are played, edited or sampled, nor what any instrument is.
- Fade-out end and ragged tail: the stems stop at about 3:07.5; I did not look at the last 0.5 s.
- I deliberately did not use CLAP tags for form: they are noisy and per-5-seconds.
- Disagreement with a window note: none material. WIN 0160 cites the drum jump at 2:49-2:50; my edge is 2:48.7-2:50.3 (consistent). WIN 0080 describes drums as "sparse" for most of that window; [MAP] shows them at -29 to -36 dB (sparse) until 1:34 then -20 to -15 (dense), consistent.

## 8. Three questions for fellow specialists

1. **Rhythm:** The breaks last 12.1-12.2 s and the intro 12.4 s, and the intro drums are one hit per 1.55 s [EDGE]. Do the bass pulse (about 0.75 s) and the voice's syllable rate support a bar of about 1.55 s (so 8-bar blocks) rather than the beat tracker's 152 BPM / 0.39 s beat, and is that 1.55 s hit a half-time backbeat or a once-per-bar marker?
2. **Harmony:** Chroma stays on A through every break and groove [OV], but chord labels vary (Am, A, F#m, F, D, Gm) and window notes disagree about minor against major. Is there any true harmonic change anywhere, for example at 1:46-1:57 (F, Gm, F#m) or the 3:00-3:08 end (F#m), that could serve as a cadence marking sections, or is the A pedal absolute and the other labels voice-pitch artefacts?
3. **Sound:** Do the stereo-width jumps (0.5-0.7 in breaks, 0.0-0.3 in grooves [LVL]) really come from the bass leaving, or is a separate wide layer (the "other" bursts) being revealed, and does the 0.94-correlated 12 s block at 0:48 and 2:00 look like a literal sample/loop repeat (same noise, same vocal formants) to you?
