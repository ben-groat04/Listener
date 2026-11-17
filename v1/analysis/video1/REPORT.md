# Elfstedentocht Part 1: a cold dawn, a heavy step, and a bass that comes back

Checked against: v1/data/video1/music_views/per_second_levels.json, v1/data/video1/music_views/chords.json, v1/data/video1/music_views/summary.json, v1/data/video1/stems/stem_rms_per_second.json, v1/data/video1/lyrics/ (Whisper Dutch and translate transcripts), v1/data/video1/sync/sync.json, v1/data/video1/frames_1fps/f_0024.jpg, f_0121.jpg, f_0168.jpg and f_0170.jpg (opened full size), dense 12 fps frames cut from videos/video1.mp4 at 2:45 to 2:50 and 2:58 to 3:08 (viewed as a contact sheet; scratch, not stored), v1/logs/ERRORS.md, 2026-11-17, status: checked (accuracy pass T1)

*Public Service Broadcasting, "Elfstedentocht Part 1" (3:09). Black-and-white archive film of the Frisian ice race of 18 January 1963, scored by a loud, relentless instrumental rock track.*

## The short version

A calm Dutch voice gives the date, says it is half past five in the morning and mentions a distance of about two hundred (the noun is unclear) for those strong enough, and sixteen degrees below zero follows. Underneath, a heavy, grinding step that never relaxes. For about a minute and a half the band builds; then at 1:15 the bass vanishes, and for about 25 seconds the music floats with no floor under it (bar one faint blip near 1:28). When the bass slams back at 1:40, it is the track's cathartic hit. It lands harder than its loudness suggests precisely because it was withheld. Everything after is a long run towards a bright, loud, cymbal-driven sprint that ends, at 3:08, with the effort still going. In the frames sampled (and in dense 12 fps frames around 2:45 to 2:50 and 2:58 to 3:08) I see no skater cross a line; at about 2:49 the frame shows a man in a flat dark cap seen from behind, a man in a peaked cap at his left, others around them and someone holding a camera-like object; no skater or bib is clear (f_0170 opened). The music tells you to arrive; the picture shows you cold, crowds, paperwork and tea.

## How to read this report

I cannot hear audio or watch film as you do. The music was "heard" through measurements: separated instrument stems, spectrograms, chord and pitch tracking, loudness curves. The picture was read from sampled frames, about one a second. Feelings below are reasoned inferences from those measurements, not listener data. Where something is uncertain I say so in plain words, once.

## The music

**It is D-centred and static.** The track sits on a D drone at about 78 beats per minute (the tracker's local tempo ranges from 78 to 152 BPM; median beat interval 0.766 s), with a fast flutter of drums over it. That the pattern never changes speed is inferred from the stems, not proven. The chord detector labels D for about 94 s and Dm for about 33 s of the 189 s, but its 143 chord changes are partly reactions to distortion rather than real changes (doubt: moderate). What the stems and chords do support is a D-centred drone, an A, D, G walk from about 2:15 (chords.json labels Am, D, G from 2:15.6), and chromatic friction in the low figure of the final sprint. There is no verse, chorus or tune. The third of the chord is almost never played, so the mode is not settled (D major and D minor score almost equally): it sounds stern and driven, not sad and not triumphant.

**The drama is subtraction.** Three things are switched on and off: the bass, a dense, distorted "wall" layer (probably guitars, though the stems cannot tell guitar from synthesiser), and the narrator. The drums keep going for the whole track; their only break is a 0.4-second hole at 2:47.8. The composer here is, in effect, the mixer.

**The journey, in order:**

- **0:00 to 0:10, snap and gather.** A swell and a hit at 0:00.7, drums already running, the wall joining at about 0:01, the bass entering at about 0:03 as a step (quiet at first) and then rising over roughly 17 seconds to full weight. Layers arrive one by one on a fixed pulse: anticipation.
- **0:10 to 0:32, told a story.** The narrator gives the date ("18 januari 1963"), the hour ("half zes in de ochtend") and a distance of about two hundred ("tweehonderd", noun unclear) for those strong enough, ending on the sentence "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht". The band does not duck for him. A calm voice over an engine that never relaxes.
- **0:32 to 1:15, momentum.** The voice stops on what looks like a bar line and the band opens up, brighter and wider. Short bursts of narration ("16 degrees below zero", "a monster ride of more than 200 km"), the wall swelling markedly, the hi-hats opening from about 1:05, loudness climbing to a first peak around 1:07.
- **1:15 to 1:27, the floor falls away.** The bass cuts out at about 1:15, the mix gets noticeably quieter and the wall thins to bright upper lines. Light, suspended, slightly uneasy. The narrator comes in at about 1:19 to read out the numbers: 575 racers, about 9,500 tour skaters (transcribed as 575 and about 9,500: ASR, unconfirmed; research gives 568 and 9,294).
- **1:27 to 1:40, lift without ground.** The voice stops; the wall surges, the stereo picture doubles in width, loudness comes back, and a slow stepwise line floats over no bass at all. This is the track's one melody-like moment, and the nearest thing it has to yearning.
- **1:40, the landing.** The bass returns. This is the moment most listeners would point to. Loudness barely changes (about 0.2 to 0.5 LU on a later ebur128 measurement quoted in v1/analysis/video1/interpretation.md; the music reading's own K-weighting gives 0.1), but the bass itself leaps from almost nothing to full weight and the stereo image pulls into the centre. You feel weight and relief, not volume. It works because of the 25 seconds you waited.
- **1:55 to 2:38, held breath, then setting off.** The bass leaves again and the music empties to a thin, high, narrow block, one of the two thinnest passages of the piece (the other is the bass-less stretch at 1:15 to 1:27), and 1:55 to 2:13 is about as quiet as the bass-less 1:15 to 1:27 (within a fraction of a unit on the level meter). Into it fall six very low, identical thumps at 42.6 Hz, one every 6.15 seconds from 2:01 to 2:32, like a slow second clock over the unchanged flutter. On a phone speaker these largely disappear, and what you feel instead is the wall dropping. From about 2:13 the wall thickens, a walk through A, D and G begins, and the narrator reads the towns of the route one at a time.
- **2:38 to 2:48, weight resumes.** The bass comes back, the chords turn, and the opening sentence returns at about 2:44, so the line that began the piece comes back to frame it, and the band then answers it. Whether it is the same recording or a re-cut, the measurements cannot say. Then comes the hole: for about 0.4 seconds the drums and bass drop out while the narrator's last syllable decays and the guitar holds. A held breath that ends in release rather than shock.
- **2:48 to 3:08, the sprint.** A steady, bright and wide stretch (width 0.7 to 0.86), level in loudness with the first peak around 1:07 to 1:15 rather than louder than it. The loudest raw stretch of the track is 1:40 to 1:55 (peak about -9.5 dBFS at 1:52, per_second_levels.json). Mostly D by the chord detector, with a gritty, circling low figure (chromatic friction around D) and a cymbal-led kit. By feel it is the riff and the payoff: hard, grinding, relentless. The exact notes cannot be recovered from the recording, but the character is plain. It ends in a quick taper of about half a second, with no cadence, as if the effort carries on offscreen.

**The voice.** It sounds like one voice, band-limited and centred; whether the repeated line is a re-cut is unresolved. It supplies facts and nothing else; the band supplies the feeling. It enters into space the band has cleared by subtraction (1:19, 2:15) and leaves at changes of state. By the vocal stem, speech runs 0:09 to 0:32, 0:41 to 0:56, 1:19 to 1:27, 2:16 to 2:36 and 2:44 to 2:48; no speech is transcribed from 1:27 to 2:16 (the stem shows only brief, wordless blips near 1:03 to 1:05, 1:46 to 1:48 and 1:57 to 1:58) or from 2:48 to 3:08. The first long gap spans the band's return, the bass slam at 1:40 and the thin tea-table passage; the second is the sprint, so the last word goes to the band.

## How the picture works with it

The footage is made largely of print, paperwork, signs and crowds. Skaters are mostly anonymous bent figures seen from behind or at distance, in bibs. I saw no clear smile in the frames sampled, though most faces are small, dark or blurred. The cold is everywhere: rime on caps and sleeves, frosted reeds, a ground blizzard at about 0:51 to 0:56.

Some of the joins are plain to see:

- **The towns.** As the narrator reads the route from about 2:15, five or six of the eleven towns are heard and shown within about two seconds of each other (ASR timing varies by up to 3 s): IJlst is shown but its spoken name is unconfirmed; the others are the Vrouwe van Stavoren inn, "WELKOM IN WORKUM", BOLSWARD / BOALSERT, FRANEKER / FRJENTSJER, DOKKUM, then a signpost to Leeuwarden. Sneek, Sloten, Hindeloopen and Harlingen have no sign in the frames. This is the tightest word-to-picture match in the film. Language says where, the band says how hard, and the faces are left unlabelled.
- **The numbers.** The registration count at 1:19 to 1:27 plays over a registration table, writing hands and bib 157.
- **The tea tables.** At 1:55 to 2:14, under the thinnest music and the first thump, the picture goes indoors: a kettle, a row of young people drinking from white cups, one of the five looking at the lens (f_0121 opened; one or two others may), a frost-caked face, a van with a cross. This is the film's warmest and most exposed passage.
- **The ending.** At 2:47 a whip-pan and a "FINISH" banner arrive within about a second of the hole. Then the sprint, with bibs, skaters on the ice, blurred crowds, the newspaper page again (2:57), a reused DOKKUM sign at about 3:06, a banner reading "Reportage ELFSTEDENTOCHT", and black.

Whether the cuts follow the music by design is not settled. Only 7.8% of cuts fall within 80 ms of a beat against 19.7% expected by chance (sync.json), so cuts are not on the beat. Their phase within the beat does cluster (single-beat Rayleigh p=0.0055, n=39), but that depends on the beat tracker's phase being right, the cut list misses fast changes in snow, and the half-beat and bar tests are no better than chance (p=0.95, 0.56). The fair description is two well-made layers joined at the narrator, with the picture clearly following the narration, rather than a proven counterpoint. Broadly, though, picture and sound do get busier together, but only weakly (r=0.27 for cut rate against loudness, weak and untested for significance, with the picture leading the music by a few seconds): the busiest cutting is about 1:06 to 1:16 and 2:58 to 3:08, the first at the first loudness peak.

## What it means

**The band gives stakes; the picture gives content.** Drive, waiting, return and release come from the music. Faces, cups, cold and crowds come from the film. Put a cosy major-key bed under the tea scene and it would feel entirely different. Here it feels cold, effortful, collective and unglamorous.

**Collective effort, not heroics.** The film's units are places and documents: headlines, a registration table, tea, a control hut, town signs, the finish banner. No skater is named; the only print that could name a person is small newspaper print at 0:23, which I have not read (a name-like fragment sits beside the photograph, illegible at 1 fps and unreliable at full size). The narration reads out "575 racers, about 9,500 tour skaters" (ASR, unconfirmed; research gives 568 and 9,294), not a winner.

**The subject is the effort, not the result.** The sound has an arrival, the 2:48 sprint. In the sampled frames the picture never shows one; at 2:49 it shows a man in a flat dark cap seen from behind, a man in a peaked cap at his left, others around them and someone holding a camera-like object, and no skater or bib is clear. The panel agrees that viewers experience this; whether the makers intended it is undecidable. It is also only Part 1 of a two-part release, and archive cameras usually stood at control points, so the absence should not be over-read.

**Context.** The piece was commissioned by the Explore the North festival in Leeuwarden for the 50th anniversary of the 1963 race, "De Hel van '63". That year 9,862 started and 127 finished; Reinier Paping won in 10:59 (research context, not read from the film). The footage comes from the Fries Film Archief; which films were used, and who the narrator is, are not confirmed. The band's method is to let archive voices carry the story while the music frames them, and the archive hiss and grain are material, not flaws. Reception is thin but positive, centred on drive, physical effort and the fusion of image and sound. Readings of memory or ghostliness are the listener's, not demonstrated properties of the film.

## The moments that stay with you

1. **1:40, the bass slams back.** The strongest contrast in the track, made by absence.
2. **2:47 to 2:49.** The closing sentence, the half-second hole, the FINISH banner, then the sprint, in which no crossing of a line is seen in the frames sampled.
3. **1:55 to 2:14, the tea tables.** The thinnest music and the film's humanest scene.
4. **2:16 to 2:36, the town list**, with five or six of the eleven towns shown within about two seconds of being heard.
5. **1:15, the floor falling away**, and the six slow thumps, if your speakers can reproduce them.

If you only watch one minute, watch 1:55 to 2:48, and watch it loud, on good speakers or headphones.

## Caveats worth knowing

- The instrument identities (guitar versus synthesiser, played versus programmed) are inferred, not proven.
- The tempo could equally be felt at 156 BPM; the weight of the beat is the same either way.
- The Dutch transcription is reliable for the date, the hour and the key sentence, unconfirmed for the numbers (575 and about 9,500), and loose for place names over the loud band.
- Why the track ends in a half-second taper, studio choice or video edit, is unknown.

## Where to look next

- `v1/analysis/music/video1/music_reading.md`: the full music reading, with confidence tags, a song map and the specialists' disagreements.
- `v1/analysis/music/video1/specialists/`: the six specialist notes (round 2) behind it.
- `v1/analysis/video1/interpretation.md`: the panel's synthesis, with live disagreements and craft notes.
- `v1/analysis/video1/dossier.md`: the frame-by-frame picture evidence.
- `v1/data/video1/context.md` and `v1/data/video1/sync/sync.json`: the identification facts and the music-picture sync measurements.

## Corrections applied

1. Ending bullet: town-signs list replaced by the newspaper page again (2:57), a reused DOKKUM sign at about 3:06 and the "Reportage ELFSTEDENTOCHT" banner; IJlst, Bolsward and Franeker removed from the sprint.
2. 2:49 (short version): now a man in a flat dark cap from behind with a peaked-cap man at his left (checked against f_0170), others around, a camera-like object, no clear skater or bib (f_0170 opened). Also corrected in "The subject is the effort" below.
3. Sync: 7.8% of cuts on the beat against 19.7% by chance; single-beat Rayleigh p=0.0055 (n=39) with the tracker caveat; r=0.27 weak and untested; busiest cutting 1:06 to 1:16 and 2:58 to 3:08.
4. Tempo: local tempo 78 to 152 BPM, median beat interval 0.766 s; constant speed is inferred from stems.
5. Narration numbers marked ASR, unconfirmed (575, about 9,500); research gives 568 and 9,294.
6. Opening: date, half past five, about two hundred (noun unclear), replacing the crowd gathering.
7. Towns: five or six of eleven within about two seconds; IJlst's spoken name unconfirmed; ASR timing varies up to 3 s.
8. Tea tables: one of the five looks at the lens (f_0121 opened); one or two others may.
9. Sprint: steady, bright and wide (0.7 to 0.86); loudest stretch 1:40 to 1:55 (peak about -9.5 dBFS at 1:52); the "few tenths" figure now cited (0.2 to 0.5 LU, interpretation.md).
10. Specialist notes: six in round 2; the voice sounds like one voice, re-cut unresolved.
