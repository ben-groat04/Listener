# video2: the music (blind read, "the ears")

Method: I cannot hear the audio. Everything below comes from measurements on `audio/song.wav` (stereo, 306 s): spectrogram, HPSS, band energies, stereo mid/side, chord and lead-note tracks, the source-separated stems (spectrograms in `music_views/window_*.png`), CLAP tags and the Whisper transcripts. Scripts: `v1/scripts/agents/v2_music_extra.py`; numbers: `v1/data/video2/audio_features/extra/v2_extra.json`. Confidence labels: HIGH / MED / LOW. Observation (O) is kept apart from interpretation (I).

## 1. One-paragraph summary

A 5-minute electronic-led instrumental piece in B minor that starts as a quiet, crackly archive-style ambient bed, brings in sampled spoken Dutch narration over a slowly pulsing bass, goes silent for about a second at 1:25, then launches into a huge, bass-heavy, driving groove at 1:28. From there it builds in loudness and brightness almost without letting go until it ends abruptly at about 5:01. Voices after the narration are fragments of chopped/sampled singing or shouting, not a lead singer. The mood is nostalgic and solemn-then-exhilarated: documentary memory turned into momentum.

## 2. Genre and instrumentation (with evidence)

- **Genre: electronic / synth-led post-rock-ish instrumental with sampled spoken word** (MED). Evidence: CLAP averages synth-pop 0.35, electronic 0.23, krautrock 0.16, post-rock 0.06; the 0:30-1:25 windows read as "electronic" at 0.99. Chords are minor-key with a repeating loop feel (Bm dominates: 136 s of 306 s, then D 44 s, Em 22 s, G 20 s). Krautrock/motorik is plausible for the late sections (steady driving pulse); the label is a model guess, not proof.
- **Drum machine or tightly programmed drums** (MED). O: the drums stem shows very regular, narrow vertical transients; between 3:20 and 3:40 they hit steadily with a hard kick-and-snare look. CLAP: "drum machine" 0.63 on average, 0.99-1.0 from 1:30. I: could equally be a sampled live kit; I cannot tell. Caution: the stem-separation drums curve is nearly flat during 1:40-2:25 although the track is loud, so the separator apparently put the kick into "bass". Do not read the stem chart as "no drums" there.
- **Sub-bass / bass synth is the main body** (HIGH). O: from 1:28 to 4:50 about 70-80% of spectral energy lies below 250 Hz (sub <80 Hz 33-45%; 80-250 Hz 37-48% in sections 1:29-3:37). Bass stem peaks at 135 s. Pitch tracking puts the lowest notes near B1-B2 and the lead-note range as C#2 to A#5.
- **Pad / organ / synth chords** (MED). The "other" stem has a smooth harmonic floor that grows from 0.04 to about 0.20 (peak around 3:50-4:30), eventually exceeding the bass; CLAP says organ 0.18, and "organ" >0.96 at 0:30-1:00. I: held synth pads or organ-like layers; guitars are possible (CLAP gives electric guitar 0.9 at 4:30) but unproven.
- **Bell-like / tuned percussive tones and crackle** (MED). CLAP "bells" 0.85-0.99 early and "vinyl crackle" ~1.0 from 3:00 on. The crackle label is a noise-texture guess; broad hiss in the top octaves exists (air band 5-11 kHz rises from near zero before 1:28 to ~1-1.5% after, and the spectrogram shows a bright wall from 1:28).
- **Sampled voices** (HIGH for presence, MED for nature). See section 5.
- **Not heard**: no evidence of a conventional lead vocal, strings, or acoustic drum-kit cymbal wash (air band is tiny throughout; 2-5 kHz presence band is only 1-6%). The sound is dark and low-weighted, not shiny.

## 3. Tempo, pulse, key

- Beat tracker: 161.5 bpm (grid starts at 0:42.7, 0.372 s between beats). Autocorrelation on 1:30-2:30 gives 161.5 or its half, 60-80 (octave ambiguity); on 3:00-4:00 it gives 161.5 firmly. Local-tempo plot shows ~117-123 bpm in the whole opening, i.e. the slow pulse before 1:10 is felt at about 118. HIGH that the groove from 1:28 sits on a 161 pulse; MED on whether a listener claps it at 161 or 80. I would call it "fast, driving" (161) with a half-time heavy feel in places (the drum stem hits about every 0.23-0.26 s at 1:50 and 3:20, double-time subdivisions).
- Anomaly: 4:10-5:00 the tempo tracker flips to ~96 bpm. That is 161 x 0.6, i.e. a tracker artefact or a slower accent pattern, not a real slowdown (LOW-MED); loudness stays level.
- **Key: B minor** (HIGH: whole-song 0.88; 0:00-0:30 = 0.94 B minor). Relative D major is the second candidate (0.73). Middle sections wander through E minor / G major (0:30-2:30) and return to B minor / D from 2:30 to the end. Loop shape in 1:41-2:15 (chord track): Em-G-D-Bm, then B, E, Em, G, D, Bm (about 4-8 s per chord), then in the later sections mostly Bm with D (i-bIII), occasional A, F#m. The B major / E major wobble at the very end is chroma noise (LOW).
- O: the opening (0:00-0:42) is a single sustained Bm drone for 42 s (chord track: one chord).

## 4. Structure map (timestamps measured; labels interpretive)

| time | what the data shows | what I think it is | conf. |
|---|---|---|---|
| 0:00-0:28 | quiet (RMS -25 dB), mid-band only (76% 250 Hz-2 kHz), wide stereo (side/mid 1.07), low-pass-like dark top, sustained Bm tones with sparse low blips at ~0:08 and ~0:12 (drum-stem transients) | an archive-feel ambient intro: drone, crackle, maybe bells. Reads as a "found recording" opening | MED |
| 0:28-0:41 | sub-bass and bass enter abruptly (sub+bass = 76%), loudness +6 dB; whisper hears "MUZIEK" at 0:28.6 (a spoken word or caption-like phrase) | a slow, pulsing bass-drone bed begins; the piece "switches on" | MED |
| 0:41-1:25 | narration bursts (vocal stem active 0:43-0:45, 0:52-0:53, 1:00, 1:05-1:10, 1:20-1:22, 1:25-1:28) over ticking percussion at roughly 3 hits/s, chords Bm-Em-G-D-A-B, brighter transients at 0:44, 0:52, 1:00, 1:08 (the voice) | spoken narration sections over a gently moving pad-and-bass progression. The beat grid locks from 0:42.7 | HIGH |
| 1:25-1:28 | loudness dips (per-second RMS ~0.05-0.07 at 1:28-1:29, section boundary 1:24.96-1:28.65), then from 1:28 the full band enters; further big rises follow at 1:41 (+0.05) and 1:45 (+0.08) | a held breath / silence before the drop | HIGH (the dip), MED (that it is deliberate) |
| 1:28-1:41 | "A" section: full-band entry, percussive fraction 65% (highest), bass+sub 83%; stereo narrows (0.45) | the first full groove: drums and bass arrive at once | HIGH |
| 1:41-2:37 | very loud, compressed (crest factor 3.7), very mono-centred (side/mid 0.33), bass stem peaks at 1:45, 2:00-2:05, 2:15 (0.30-0.37). Narration returns at 1:49-1:56 and 2:25-2:36 (vocal stem 1:50-1:55 and 2:26-2:35, but pulses so tightly with bass the separator is unsure) | main groove, bass-led, with spoken lines riding on top | HIGH |
| 2:37-2:57 | slight lull (RMS -13 dB), tempo tracker steady at 161 | a mid-song breather within the groove | LOW-MED |
| 2:57-3:37 | bass and kick still dominant; "other" climbs; vocal bursts begin about 3:29 and become frequent; stereo opens (0.48) | build: pads rise, the vocal chops appear | MED |
| 3:37-4:37 | loudest and most layered stretch: "other" stem ~0.20, mid band rises (43%), 2-5 kHz presence at its maximum (6%); chords mostly Bm with D, A, Em; vocal chops every ~2 s | the peak plateau; lushest, most anthem-like | HIGH on loudness, MED on the interpretation |
| 4:37-5:01 | brief drop in level then re-brightening (air band 1.5%, percussive fraction 46%), more transients and pulsing vocal fragments | final push / last chorus feel | MED |
| ~5:01 | sudden cut: RMS falls 0.20 to 0.03 in about 0.5 s, 5:02 a short hit, 5:03-5:05 silence, trailing tick ~5:06 | abrupt stop, not a fade. A listener would hear the music "slammed shut" | HIGH |

Overall loudness: quietest sections open the piece (-25 dB), loudest is 4:48 (global max at 288 s), average 1:41-4:37 around -10 to -13 dB. Dynamics shrink as the piece proceeds (crest factor 7.2 intro, 3.3 in the peak), so the song is "squeezed" tighter and tighter.

## 5. The voices and how the music frames them

Transcripts (Whisper, language detection on the full mix said Dutch, p=1.00; vocals-only run guessed Welsh at p=0.57, which is wrong and should be ignored):
- **Corrected reading of the Dutch narration** (MED; names uncertain, judged from the Dutch and English runs): "18 januari 1963" (0:41-0:46); "Het schaatsmarathon zonder weerga" or similar, "the skating marathon without equal" (0:51-0:54); then something like "in the morning, half past six, 200 km through Friesland, where only the strongest are left" (0:58-1:14); then at 1:19-1:28 a line about "the twelfth Elfstedentocht... where everyone is getting ready for the Elfstedentocht" (whisper garbles "Elfstedentocht" as "elfsteen vluit/Elfstegendpachter"; I judge it to be the eleven-cities skating race, based on the repeated "Elf-" word, 200 km, ice, cold). At 1:49-1:56 "temperature 16 degrees below (zero), a monster ride of more than 200 km"; at 2:25-2:36 "575 (competition riders), about 9500 touring riders, from Sweden, Switzerland, Belgium...". Numbers repeat in both transcripts and are fairly reliable; country list is MED.
- The delivery is documentary newsreel narration: measured, declarative, the facts of a big public event. The data cannot give the speaker's emotion, only that the cadence is in 3-8 second statements.
- **What the music does around it**: O: during the narration in the first half (0:41-1:25) the bass and pad are steady, drum-stem ticks fill the spaces between phrases, and the voice starts exactly at bar-like points (0:42.7 = first beat of the grid). Level of the music does not duck dramatically; the voice sits as a bright burst (2-8 kHz) above a dark bed. I: the music behaves like a bed under a news report: still, pulsing, a bit ominous (minor key, sub-bass).
- **After the narration ends (~2:36)** the only "voice" is short fragments: the vocal stem at 3:28-3:40 shows formant-rich shouts, 5-8 per 20 s (window 3:20), then pulses roughly every 2 s from 3:29 to 5:00 (vocal-stem times 209, 213, 217, 219 ... 299 s). Whisper small invents "Stuck... End of the road... Climbing up" for 3:32-3:58 and "Fafn / Ymwneud" for others; these are most likely hallucinations over chopped vocal samples (LOW). I: vocal chops, chants or crowd-like shouts used as rhythmic hooks, giving a communal, "crowd on the ice" feel without any single singer. Pure speculation: they may be crowd sounds from the original footage.
- No sung lead melody is detectable; lead-note tracking is noisy and mostly picks up bass and pad.

## 6. Emotional arc (my interpretation, from sound alone)

1. **0:00-0:28, hush**: quiet, crackly, cold-sounding (dark top end, drone). Feels like opening an old record or archive.
2. **0:28-1:25, solemn gathering**: bass pulse beneath a calm announcer reciting date, place, distance. Anticipation, a sense of an event about to happen; minor key keeps it serious.
3. **1:25-1:28, intake of breath**: the near-silence is the biggest dramatic moment of the first half.
4. **1:28-3:30, drive**: crushing bass and relentless groove; excitement and physical momentum, with the spoken stats occasionally breaking through like reminders of scale (temperature, distance, riders).
5. **3:30-5:00, ascent / release**: more harmonic layers, brighter top, communal vocal hooks. Anthem-like exhilaration, still minor but triumphant in energy. CLAP mood tags stay "nostalgic" (0.58 on average); "hopeful" appears at ~1:00 and "aggressive" at ~2:30.
6. **5:01, end**: the cut-off leaves tension unresolved, as if the film ended while the race was still going.

Confidence: HIGH on the loudness/energy shape, MED on the emotional labels (they are my reading of the minor key, dark spectrum and build, not something I heard).

## 7. Moments a listener would remember

- **0:28**: the sudden arrival of deep bass out of near-silence (MED).
- **0:42-0:46**: first spoken "18 januari 1963" over the drone, which sets the story (HIGH).
- **1:25-1:28**: the dropout, then the full-band entry at 1:28 (HIGH). This is the clear "drop" of the song.
- **1:45-2:15**: the biggest bass swells (RMS peaks, bass stem up to 0.37 at 2:15) (HIGH).
- **1:49-1:56 and 2:25-2:36**: narrator returns with numbers (temperature, 200 km, 575 riders) in the middle of the groove (MED).
- **3:28-3:40**: first prominent chopped vocal shouts (MED).
- **~4:00-4:37**: the fullest, most layered plateau (MED).
- **4:48**: global loudness peak (HIGH).
- **5:01**: the sudden stop (HIGH).

## 8. Uncertainties and cautions

- The Dutch narration is reconstructed from imperfect ASR; treat exact wording and place names as approximate.
- Stem separation mislabels kick drums as bass in the loud sections; I based drum claims on the mix HPSS and spectrogram rather than the stems alone (the percussive fraction is 0.26-0.40 in the loud sections but this includes bass transients).
- Section 2:37-2:57 and the "chorus" naming are loose; the song is through-composed with gradual build more than it has verses and choruses, but a human might still hear repeated bass-lines as a "chorus".
- Tempo octave: 161 (fast) vs 80 (half-time) cannot be settled without hearing; the visual cut rate in `sync.json` shows cuts match beats at about chance level (37% within 80 ms vs 43% chance), so the edit does not clearly follow the pulse.
