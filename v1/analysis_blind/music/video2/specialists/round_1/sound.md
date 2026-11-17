# video2: SOUND specialist, round 1 (blind, measurements only)

Scope: sound design and production: instrumentation, timbre, distortion, space, stereo image, mix balance, loudness curve, era and style. I read all sixteen window notes (win_0000 to win_0300) and checked them against the images (window_0120s.png opened in full) and my own measurements (v1/scripts/agents/video2_sound_probe.py: per-20 s level table, band shares, crest factor, L/R correlation, stem band shares, final-hit decay).

Evidence key: [LV] per_second_levels.json; [IMG nnn] music_views/window_nnns.png; [AF] audio_features; [CH] chords.json; [CLAP] clap_tags.json; [LY] lyrics/; [P] my probe. Times m:ss. The file runs about 5:06 (305.9 s [P]); the music ends at about 5:04.

## 1. Headline

The track is a two-world production. Roughly the first 1:40 is a quiet, wide, dark, reverberant "film-score" bed with sparse low strikes and a sampled narrator. After the groove locks in (full band at 1:28.6, bass swell by 1:41), the second world is a loud, narrow, centred, dry-sounding, compressed rock/electronic band: punchy gated-sounding bass, very steady programmed-sounding drums, a dense saturated "other" layer, and chopped or cut speech samples sitting level with the instruments rather than above them. Loudness climbs about 16 dB from the opening to about 3:40-4:20, and the width falls from above 1.2 to about 0.3-0.5. The ending is a sudden stop on a dry bass-and-drum hit after a wide reverb tail.

## 2. Instrumentation (with evidence and honesty)

Stems are demucs separations, so the stem levels are real evidence of what is present, but stem contents are not labelled and bleed is real (for example the "vocals" and "bass" panels in the intro show leakage, with level near -80 to -90 dB [LV]).

- **Sustained pad/"other" layer, present from 0:00 to the end** (high confidence on presence). From 0:00 the "other" stem sits at -27 to -32 dB and is a stack of steady horizontal harmonic bands from about 100 Hz to 2-3 kHz with no rhythmic articulation [IMG 0000s]. Identity: the measurements cannot say organ, choir pad, strings or synth. CLAP says "choir/organ" 0.8-1.0 and "bells" [CLAP], which fits sustained-organ-or-pad-with-a-bell-like-top; weak evidence (CLAP fires "organ" and "bells" in almost every window, so it is not discriminative). Later (from 1:28.6) the same stem shows vertical stripes up to 8 kHz+ in sync with the drums [IMG 0080s], i.e. rhythmic attacks, and from 2:00 it is a dense horizontal-harmonic wall from about 100 Hz to 8 kHz [IMG 0120s, which I opened]. That looks like a layered, saturated chordal instrument (distorted guitar or a driven synth stack; the data cannot choose). Its level climbs from about -26 dB (1:20-1:40) to -22 dB (2:00-2:20) and then to -15 to -19 dB in 3:00-4:40 [P table], a total of about 10 dB. In my reading that makes the "other" layer the main driver of the late loudness rise (medium-high).
- **Low strikes (0:00-0:28)**: single events at 0:00, 0:08, 0:12, about 0:20 and 0:24, each decaying about 20 dB in 1 s and about 50 dB in 3 s [LV drums], centred near 65 Hz, 99% of energy below 150 Hz in 0:20-0:28 [win_0020 band measure]. I read this as a deep boomy tom, timpani-like or processed kick with a long tail; cannot tell which. Medium confidence that it is percussive rather than a bass note.
- **Drums from 0:28 (sparse pattern) and from 1:28.6 (full kit pattern)**: broadband vertical strikes reaching 8 kHz+ plus low kicks [IMG 0080s, 0120s]. Drum stem is a steady -18 to -19 dB for 1:40-4:50 [P table: -18.0 to -19.3 every 20 s]. That is extremely flat: the drum stem moves less than 1.5 dB in three minutes. Combined with the metronomic onset cell (repeating 1.0-1.5 s patterns of onsets at x.12, x.50, x.63..., with 0.12-0.14 s flams [win_0120, win_0160 onset runs]) and the clean black gaps between hits in the drum panel [IMG 0120s], this sounds programmed, sampled or very heavily gated/quantised. The drums panel at 2:00 (which I viewed) shows hits cut cleanly, no wash. CLAP "drum machine" 0.7-1.0 agrees weakly. I cannot rule out a real kit played to a click and sample-reinforced. Medium confidence for "programmed or sample-based".
- **Bass**: absent until 0:28 (-85 to -90 dB), then -22 dB. Two distinct characters: at 0:28-1:00 a mid-weight line with upper harmonics to 2-4 kHz (87% below 150 Hz, rich harmonics [win_0020]); from 1:41 a louder (-12 to -16 dB), tighter line: low sub (40-60 Hz) plus short, punchy articulations with upper partials to 3-4 kHz [IMG 0120s bass panel: a continuous low line, plus vertical short bursts]. Band shares of the bass stem at 2:00 (my probe): about 40% of the energy in 20-60 Hz at 40-60 s windows, but at 110-130 s window 90% in 60-150 Hz, so the weight sits around 60-150 Hz with a sub component on long notes. Plucked or driven electric bass versus synth bass: cannot say. The upper harmonic spread suggests overdrive or saturation (medium-low).
- **Voice**: a spoken-word sample (Dutch announcer-like per [LY]; I do not use the words here). It enters 0:42, 0:51, 0:59, 1:04-1:10, 1:20-1:28, 1:49-1:56, 2:25-2:36, then from 3:28 in many short cut blocks and from about 3:40-4:20 as chopped syllables, and again as a looped chop every about 2 s in 4:40-5:00 [win notes; LV]. Treatment and mix level matter for sound (section 6).
- **Possible high lead or trill**: the lead tracker shows an A5/G#5 alternation at 4:29.9-4:35.6 [win_0260, lead_notes]. It is the only plausible tune-like top line in the track. Source unknown (synth, guitar harmonic, sample); medium-low. It is worth a harmony specialist's view.

## 3. Timbre and spectrum

- Opening (0:00-0:28): dark and warm. My probe shows 78% of the mix energy below 500 Hz, none above 6 kHz; spectral centroid about 710 Hz [P; AF 600-760 Hz]. Brightness dips on each low strike.
- 0:28-0:42: darker still, centroid about 516 Hz [P], because the bass fills 25-150 Hz (64% of the energy in 20-150 Hz [P]).
- 1:00-1:20: centroid about 970 Hz [P]; the first bright air appears with the narrator (to 6-8 kHz).
- From 1:40: centroid 1.6-2.3 kHz [P: 1772, 1575, 1735, 1958, 2296 Hz]. The mix is "weighted low but with a lit-up top": 60-150 Hz is the largest band at about 35-66% of linear power, and a persistent 2-8 kHz+ haze from hats and from "other" [IMG 0120s]. No content above about 10 kHz in the plot, so the ceiling is soft (consistent with a mastered-for-streaming or lossy source; cannot tell which).
- Distortion: not directly measurable. Evidence for saturation: dense harmonic ladders in "other" up to 8 kHz with noise-like fill [IMG 0120s]; bass harmonic spread; CLAP "aggressive" 0.97-0.99 at 2:25-2:35. I rate saturation or overdrive on "other" as medium confidence and on the bass as medium-low. I treat CLAP "vinyl crackle = 1.0" from 3:00 onwards (it saturates in every window) as a model artefact, not evidence of a vinyl or lo-fi treatment.

## 4. Space and reverb

- **Intro is a big, wet room.** The low strikes ring for 2-3 s [LV drums] and the end-of-window pad ends have long decays; width is 1.2-1.5 in 0:01-0:08 [LV]. My probe gives a L/R correlation of -0.22 at 0:05-0:10 and +0.21 at 0:30-0:38 [P], i.e. at the start the left and right channels are decorrelated to slightly out of phase. That is the numerical signature of a wide chorused, detuned or stereo-reverbed pad. It also warns that the opening might partly cancel in mono (medium confidence; I measured only 5-8 s clips).
- **Narration section (0:42-1:28):** the narrator is centred and dry with sharp onsets; the vocals-stem panels in win_0060 and win_0080 show clean edges, though win_0080 sees about 0.2-0.5 s tails on the 1:20-1:28 blocks. I read this as a dry-to-lightly-reverbed archival-style recording placed in the centre. Low-medium confidence.
- **Groove section (1:41-4:50):** the drums panel shows hits cut off cleanly with dark gaps [IMG 0120s], so the kit has almost no reverb tail; "other" is a continuous wall that could hide some. Overall: dry, tight, close. L/R correlation 0.76 at 1:50-1:58 and 0.56 at 3:20-3:30 [P], i.e. mostly mono-compatible.
- **Ending (5:00-5:04):** the "other" tail after the final chord decays slowly from -27 to -48 dB over 1.5 s with a bump at 5:01.8 and a width jump to 0.92 [win_0300; LV]; my probe confirms a gap of about -27 to -41 dB in 0:25 s bins from about 5:01 and then a dry hit at about -12 dB and the decay to -88 dB by about 5:04. Dry mono hit after a wide wet tail: a deliberate "gun-shot" ending (high confidence on the shape; the reverb-versus-sustain question for the tail is open).

## 5. Stereo image and loudness curve (measured)

Per-20 s means from [LV] via my probe (mix dBFS, width):

| time | mix | width | drums | bass | other | vocals |
|---|---|---|---|---|---|---|
| 0:00 | -26.4 | 1.2 | -65 | -89 | -28.6 | -83 |
| 0:20 | -20.6 | 0.9 | -41 | -48 | -26.1 | -81 |
| 0:40 | -18.1 | 0.8 | -32 | -23 | -25.4 | -55 |
| 1:00 | -17.7 | 0.8 | -50 | -23 | -23.8 | -54 |
| 1:20 | -17.0 | 0.5 | -34 | -33 | -25.8 | -56 |
| 1:40 | -12.0 | 0.3 | -19 | -16 | -25.1 | -56 |
| 2:00 | -11.6 | 0.3 | -19 | -14 | -21.8 | -76 |
| 2:20 | -12.0 | 0.3 | -19 | -16 | -23.2 | -46 |
| 2:40 | -13.1 | 0.3 | -19 | -18 | -23.9 | -75 |
| 3:00 | -12.2 | 0.5 | -19 | -19 | -18.8 | -74 |
| 3:20 | -11.5 | 0.5 | -19 | -18 | -17.4 | -53 |
| 3:40 | -10.8 | 0.5 | -19 | -18 | -15.8 | -32 |
| 4:00 | -10.3 | 0.5 | -19 | -18 | -14.8 | -37 |
| 4:20 | -10.2 | 0.5 | -19 | -17 | -15.2 | -43 |
| 4:40 | -12.7 | 0.5 | -18 | -35 | -19.3 | -35 |

(Means are in dB and include silent seconds, so the 0:00-0:28 drums/bass rows are depressed by silence. Per-second readings are in section 1 above.)

Reading it:
- Total rise: about 16 dB (-26 to about -10). Steps: +5 dB at 0:28 (bass and drum pattern arrive), about +3 dB around 1:28-1:41 (groove then bass swell from -26 to -15 dB), then a slow +2 dB swell to 4:20 carried by "other".
- Crest factor (peak minus RMS, 20 s windows, [P]): 16.8 dB at 0:00-0:20, 16.4 at 0:40, 16.0 at 1:20, then 11.2 at 2:00, 12.8, 11.8, 10.3 at 4:00, 12.6 at 4:40. The drop from about 16 dB to about 10-12 dB shows the groove half is heavily compressed or limited (a loud, "everything-on" master), while the intro and narrator half keeps real dynamics. High confidence.
- Width (side/mid scalar in [LV]; I did not independently recompute it): falls from 1.2-1.5 (0:01-0:08) to 0.3 (1:42-2:40) and settles at 0.5. The two narrowest stretches (0.25-0.35 at 1:45-2:40) are where bass and kick are loudest relative to everything else and "other" is quietest. Widening to 0.5 from 3:00 happens exactly as "other" grows by 5 dB and starts to carry the top, so that layer has some stereo spread. Both facts together suggest: bass, kick, snare and narrator centre; "other" provides whatever width there is (high-medium).
- Narrow pulsing of width with the drum hits (0.53-0.65 on kicks, 0.9-1.05 between them at 0:40-1:00 [win_0040]) is the typical sound of a centred transient against a wide pad.
- Mix balance (stem dB, groove half): drums about -19, bass about -14 to -19, "other" about -15 to -25, vocal sample -17 to -25 when present (1:49-1:56: -17 to -20 dB; 2:25-2:36: -17 to -22 dB) and about -25 to -43 in the cut/chop sections later. Because stem levels are measured after separation, I read this as: drums and bass lead the balance; the narrator is level with the drums in 1:49-2:36 (a front-of-mix spoken part) but is pushed deeper (15-25 dB below the mix) once it becomes a chopped texture (3:40 onward).

## 6. How the voice is treated sonically

- 0:42-1:28: spoken narration, centred, band-limited at about 6-8 kHz with abrupt block starts and sharp ends, little or no reverb; strongly reads as an archival or radio-style recording dropped into the music. Consistent with a low-bit-rate or old-recording bandwidth; cannot prove a "vintage" filter.
- 1:49-2:36: the same sample style, now over a loud groove; each phrase is placed against chord changes (win_0140 section 5) and sits about 3-5 dB above the "other" bed. Mix level does not rise (-11 dBFS before and during), so it is mixed into the texture, not on top of it.
- 3:28 onward: blocks of 3-3.5 s gated phrases with 0.5 s gaps [win_0200], then 0.1-0.4 s clusters of chopped syllables clustered around G4 [win_0220, lead_notes], and at 4:40-5:00 a loop recurring every about 2 s [win_0280]. At that point the voice is a rhythmic or percussive instrument; its pitch tracker output (G4 clusters, A5/G#5) tells us the chops carry pitch, but that may be bleed from the lead synth line, not the voice (cannot tell).
- Whisper and CLAP are not reliable on this material (CLAP "no vocals = 1.0" while a speaker is talking), so I use only the stem levels.

## 7. Era and style of production

- The sound is a 2010s-onward hybrid: electronic/programmed drums (very steady stem level, tight gating, doubled 0.12-0.14 s hits), a loud heavily compressed master (crest 10-12 dB), centred sub-weighted bass, a dark film-score intro and sample-narration. This matches an "electronic-leaning rock / sample-collage" production (CLAP "synth-pop", "drum machine", "krautrock/post-rock" scattered) more than a 1960s-70s band recording. The recorded narrator, by contrast, has the narrow bandwidth of a mid-century broadcast, so the track juxtaposes an old recording with a modern loud master (medium confidence; spectral bandwidth and abrupt edges are the only evidence).
- I would not call the pad a vintage organ on this evidence alone. A modern synth pad or choir sample with chorus is equally consistent.
- The sudden stop (dry hit after a wet tail) and the 0:28 "drop" are arrangement/DJ-like production gestures rather than band gestures.

## 8. Moments where the sound itself tells a story

- 0:28: bass from -89 to -22 dB and a dense kit in one step, mix +5 dB, width 1.0-1.3 to 0.65-0.9, centroid 710 to 516 Hz.
- 1:25-1:28.6: both bass (-76 to -79 dB) and drums vanish and "other" falls to -30/-34 dB, leaving only the narrator and the tail of pad; then everything arrives at 1:28.6, mix +6 dB.
- 1:39-1:41: bass +11 dB (-26 to -15 dB), width 0.48 to 0.30: the "weight" arrival.
- 1:55.5-1:56.5 and 2:08 (about -10.8 dBFS, loudest second): short dense fills (snare band 50 to 54 dB).
- 2:36: drum fill (-15.2 dB), voice leaves, "other" drops 5-6 dB, mix -3 dB.
- 2:48-2:49: "other" up about 8 dB (-28/-30 to -20.5 dB) in a few seconds: either layers enter or a filter or distortion opens. The cause cannot be told from the stems.
- 4:36-4:40: bass goes to stabs then silence at 4:37.5, bass -17/-21 to about -35 dB, with a broadband burst at 4:38.5; from 4:40 the bass is pulsing stabs, then sparse accents every about 2 s from 4:48.4. The final 20 s is 2-3 dB quieter (-12 to -13 dB) and stripped.
- 5:00-5:04: the dry bass-and-drum hit after the wet tail.

## 9. What a listener feels because of the sound (interpretation, labelled)

- 0:00-0:28: hushed, spacious, hall-like, solemn: quiet (-26 dB), wide and phase-decorrelated pad, dark centroid (about 700 Hz), deep ringing strikes with 3 s decays. Confidence medium-high that this reads as "cavernous and ceremonial".
- 0:28 onward: physical forward push and a clamp-down in space: the step to -20 dB, mono bass and dry kick.
- 1:41-4:40: pressure and drive rather than space: narrow image, compressed (crest about 10-12 dB), kick-and-bass-first balance, bright hats on top. The spoken voice becomes a hard-edged rhythmic texture. Overall: "tight, dry, machine-like, relentless". The flatness of the drum stem (+/-1 dB over three minutes) means there is no dynamic breathing, which can feel either hypnotic or mechanical (interpretation).
- Late (3:00-4:20) fuller and more sheeny as "other" gains 5 dB and the image widens from 0.3 to 0.5: more "lift" with no new instrument measured.
- The ending: abrupt, almost violent after the soft wet tail; with 38 dB between the tail and the last hit it feels like a slammed door (interpretation).

## 10. Limits and disagreements with the window notes

- Per-20 s means in my table include silent seconds for stems, so the early drums/bass means look low; use the per-second readings in the window notes for events.
- The window notes use "width" from [LV], a single scalar of unknown formula; I trust its direction, not its absolute meaning. My L/R correlation numbers use only short clips, so they are indicative.
- The window notes' "organ/choir/bells" claims rest on CLAP and I do not rely on them. "Distortion" is inferred from spectral density only.
- CLAP "vinyl crackle = 1.0" from 3:00 is discarded.
- Window notes disagree slightly on the first narrator entry (0:41.5 versus 0:42.4); this does not change my analysis.
- The tempo debate (161 bpm versus a half-time or 1.0 s drum cell) belongs to the rhythm specialist.

## 11. Three questions for fellow specialists

1. **Rhythm:** The drum stem is within about 1.5 dB of -19 dBFS for three minutes and its onset cell repeats on a 1.0-1.5 s grid with 0.12-0.14 s doubled hits. Does the rhythm measurement support "programmed or quantised" (versus a human-played kit), and does the 1.0 s cell versus the 0.37 s tracked beat change what the drum sound is doing (for example kick on whole seconds)?
2. **Harmony:** At 2:48-2:49 the "other" stem jumps about 8 dB, and from 3:00 to 4:20 it keeps rising while the chords stay on a Bm pedal with D lifts. Is the harmonic content in "other" changing (new voicing or added octave and fifth layers) at 2:48, or is the lift only density? And what is the A5/G#5 line at 4:29.9-4:35.6 in harmonic terms (a pedal, a trill, a bell-like top)?
3. **Voice:** From 3:28 onward the narrator is cut into gated and chopped phrases with a pitch tracker cluster around G4. Are these chops being pitched or tuned to the chord, or is the pitch tracker reading the "other" layer? And does the voice's band-limited, abrupt-edged character read to you as an archival recording (a "found" sound) or as something produced for this track?

(Other specialists I would also like input from: **feeling** on whether the 16 dB loudness climb and the flat drum stem feel like escalation or like numbness, and **lineage** on whether the dark-pad-then-drop structure and spoken-sample use point to a known school.)
