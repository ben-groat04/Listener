# video1 (PSB, "Elfstedentocht Part 1"): the feeling specialist, round 1

Role: a moment-by-moment emotional journey, as an attentive ordinary listener would live it, tied to measured causes. I cannot hear; every "feeling" below is my interpretation of a measurement, and I say which. Timestamps m:ss. British spelling.

Evidence keys: LV = music_views/per_second_levels.json (dBFS, width, per-stem dB); CH = chords.json; LN = lead_notes.json; CL = clap_tags.json (weak); AF = audio_features/summary.json and beat_times.json; LY = lyrics/whisper_medium_mix_nl_translate; IMG = music_views/window_NNNNs.png; WIN = analysis/music/video1/win_*.md; MY = my script v1/scripts/agents/feeling_check.py (drum-stem onsets, autocorrelation, ending RMS).

## 0. The one-paragraph version
This is a 3:09 engine of a track: a distorted-sounding wall and constant semiquaver drums on a single D drone, almost never changing chord, with a documentary voice dropping facts on top. Nothing builds by harmony. The whole emotional story is told by **subtraction and addition of the bass**, by **stereo width**, by **the voice entering and leaving**, and by one extended "stop-start" passage (2:00 to 2:34) before a last statement and a hard cut. A listener would feel: punch (0:01), stern authority (0:10), a release when the voice leaves (0:32), swelling grandeur (0:57), floor-drop and lightness (1:15), a sudden widening lift (1:27), bass slam-back (1:40), a held breath (1:55), a coiled-spring middle (2:00), setting-off (2:15), a gasp (2:48), then a relentless sprint that is cut off rather than resolved (3:08.4). Overall register: determined, stoic, wistful-heroic rather than aggressive.

## 1. What I re-measured (checks on the window notes)
All window notes agree with the data on the facts that matter for feeling. My independent checks:

1. **Bass presence map (LV, bass > -40 dB), high confidence.** Bass on: 0:06 to 1:15; 1:40 to 1:55; short sub notes 2:01 to 2:02, 2:07, 2:13 to 2:15, 2:19 to 2:21, 2:25 to 2:27, 2:31 to 2:33, 2:31 to 2:33, then continuous from 2:38 to the end (LV seconds 158 to 187). Bass off: 0:00 to 0:05, 1:16 to 1:39 (nearly 24 s, the longest absence), 1:56 to 2:00 and the gaps between the 2:00 to 2:37 sub-notes. The bass pulses in 2:00 to 2:37 recur every about 6.15 s (autocorrelation lag 6.153 s, ac 0.68, MY) which is 8 beats at 0.767 s. The window notes are right about this, and also right that the 1:55 drop is not the same as the 1:15 drop (1:15 is a clean exit with a lightening; 1:55 is a collapse into the next section).
2. **Drum grid (MY), high.** 796 drum onsets in 188 s; inter-onset histogram is dominated by 0.15 to 0.20 s (581 of about 790) and 0.35 to 0.40 s (166); autocorrelation peaks at 0.197, 0.383, 0.766 s. So the drums run at about four hits per 0.767 s beat (semiquavers at 78 bpm, or quavers at about 156), with the 0.38 s gaps being rests in that grid. This confirms every window note. Tempo ambiguity (78 vs 156) is real (AF local tempo percentiles 78 / 108 / 152); a listener would most likely clap the slower 78 for the bass pulses and bar-length thuds, and feel 156 in the drums. Medium confidence on which one a person "taps".
3. **The ending (MY, LV), high.** RMS is about -11 dBFS to 3:07, -15.7 at 3:08.0, -53.9 at 3:08.3, -77 at 3:08.5. It is a cut within about 0.3 s, not a fade. The window 0180 note is right; the sentence in context.md that the video2 file has a "trailing fade" is not a statement about this one.
4. **Loudness (LV).** Quietest "full" stretch 2:00 to 2:14 (-16 to -17 dBFS); loudest 1:52 to 1:54 (about -9.7) and the 1:02 to 1:12 plateau (-10.6 to -11.2). AF names 1:52 as the loudest moment (112.15 s, which is 1:52). Overall the track sits in a narrow band, -10 to -16 dBFS, so feeling comes from texture, not dynamics.
5. **Chords (CH summary.json).** D 94 s, Dm 33 s, N (unlabelled) 16 s, G 13, C 11, Am 6, Bm 5.5. 143 changes in 189 s sounds like movement but most is D/Dm/N flicker on a pedal; I trust "D pedal, third ambiguous" (as every window note says) and not the minor/major labels.

Two small cautions on the window notes: (a) win_0100 says the full band "re-enters just after 2:00"; the stems and IMG 0120 show the bass does not return as a groove at 2:00, it returns only as single sub-notes (2:01 to 2:03, 2:07 to 2:09, 2:13 to 2:15, and so on), with the guitar-type layer also dropping at 2:00 to 2:01 then returning (IMG 0120 "other" panel). So 2:00 to 2:37 is a different mode, not a return. (b) the CLAP mood flicker (nostalgic / triumphant / aggressive / tense) is treated by some windows as support; I treat it only as "energetic, not which flavour".

## 2. The emotional journey, moment by moment

Format: time; what a listener feels; cause; confidence.

### 0:00 to 0:09: ignition (IMG 0000)
- **0:00 to 0:01: a click of silence-to-impact.** dBFS -19.9 at 0:00, -13.6 at 0:01 (LV). Feeling: no intro, a jump-cut into motion; the music is already running when you arrive. High.
- **0:01 to 0:09: an engine idling and building.** Drums constant from 0:00 (-14 to -16 dB), the "other" wall enters at about 0:01.3 (-30 to -25 dB), bass creeps from -66 (absent) to -36 by 0:06 and -30 by 0:12 (LV). Chords stay on D then start to move from 0:08 (CH, WIN 0000). Feeling: anticipation, "the race is about to start", pent-up energy. Cause: static harmony plus 16th-note surface plus slowly arriving low end. Medium-high.

### 0:09 to 0:32: the voice sets the scene (LV vocals -28 to -21 dB at 0:09 to 0:30; LY)
- **0:10 to 0:26: stern documentary authority.** The narrator (spoken, low male pitch, LN E3 to A2 area, a medium-confidence reading of a noisy tracker) says date and time: "18 January 1963 ... 6.30 in the morning" (LY, reliable; the rest of the transcript is mangled). The voice sits about 6 to 10 dB under the mix, not hidden, not singing. Feeling: the music acts as a score under a newsreel; facts first, mood second. Cause: unpitched-style speech over a fixed groove. High on structure, medium on "stern" (my reading).
- **0:20 to 0:32: gathering, cold, slightly grim heroism.** Bass rises to -18 dB by 0:21 (LV) and the mix to -11.4 (loudest stretch so far); harmony stays on D with a C flat-seven and Dm/Gm labels (CH, low-medium). Feeling: determined, a little icy. The icy part comes from a bright upper layer (IMG 0020 "other" panel, a bright saturated top). Medium.

### 0:32 to 0:40: first release, "the band takes over"
- Voice stops (vocals -64 dB from 0:33, LV) while width jumps 0.38 to 0.50 and drums brighten (LV, WIN 0020). **Feeling: relief and opening-out, the music steps forward as the human steps back.** This is the first of the track's three "voice-leaves, band-opens" moments (the others: 1:27 and 2:48 to 3:08). High on the measurement; medium on the feeling.

### 0:40 to 1:00: the engine room
- Width 0.55 (wide), drums at -19 to -20 (slightly lower than before), but "other" swells from -26 dB (0:39) to -14 dB (0:57), +11 dB (LV, WIN 0040). Voice appears only as short bursts (0:40, 0:50 to 0:56: "temperature 16 degrees below zero", "a monster ride of more than 200 km", LY). Feeling: gathering intensity, anthemic, a swelling that never peaks into a chord change. The "16 degrees below zero" line over a hot-loud band makes a cold-against-hot contrast. Medium-high (cause), medium (the contrast reading is mine). A small jolt at 0:42.9 (a gap in the wall, seen in IMG 0040 only; I did not check with a level slice, low).

### 1:00 to 1:15: locked, heaving forward
- Plateau -10.6 to -11.2 dBFS, all stems on, width rises to 0.67 by 1:06 (LV). Hats brighten from about 1:05 (WIN 0060, medium). Feeling: weight, momentum, locked into a march; the "peak of groove" of the first half. Cause: loud, bright, wide, nothing missing. High.

### 1:15 to 1:27: floor drops, lightness, news-reader mode
- **1:15: bass exits.** -33 dB at 1:15, off from 1:16 (LV). Mix falls 4 to 5 dB (-10.6 to -14.5/-15.5) while drums stay constant. Feeling: the floor falling away, then buoyancy: lighter, airy, a bit exposed. I would call it a release by subtraction, and it feels hopeful because the remaining layer is bright and clean and the chords move upward (D to A to C, CH, medium). The voice returns at 1:19 ("575 competitors... about 9,500 skaters", LY).
- Voice list of numbers over a lilting groove: informational, buoyant, restless. Medium. CLAP "playful 0.998" at 1:20 agrees but is weak.

### 1:27 to 1:40: the long bass-less glide (bass off 1:16 to 1:39, about 24 s)
- At 1:27 loudness +2.5 to 3 dB, width 0.36 to 0.78 in two seconds (LV), voice gone. Feeling: a sudden lift, wide and bright, "soaring". Chords alternate Am and D then C, Dm (CH, labels low-medium) over a D pedal. Because the bass is missing the music has no floor, so it feels suspended and yearning, as if floating above a beat that won't land. **This is the "suspended / yearning" centre of the track** and the cause is absence, not harmony. Medium-high.
- Nostalgic-warm is plausible (CL "nostalgic" 0.95 to 1.0, weak).

### 1:40 to 1:55: bass slams back
- Bass from -53.8 (1:39) to -17.1 (1:42) (LV, WIN 0100: about +34 dB in a second), width narrows 0.78 to 0.44. **Feeling: the biggest physical event in the track so far: impact, arrival, the low end hitting your chest**, and the loudness climbs towards its maximum (-9.7 dBFS at 1:54). Cause: 24 s of absence makes the return land. High. Voice "intrudes" at 1:46 to 1:49 as a wide-band, announcer-timbre burst (LV vocals -29 at 1:48), a voice from the past, brief and dry (medium).

### 1:55 to 2:00: held breath
- Bass -33 to -62 dB by 1:56 (LV), guitars fall 10 to 17 dB, mix falls about 5 dB, width collapses to about 0.24 while drums continue (WIN 0100; my table shows dBFS -12.3 at 1:57, -16.2 at 2:00). Feeling: tension, exposure, leaning in, a coiled stillness; the drum-only texture is felt as "everything has gone but the heartbeat". High on cause, medium on feeling.

### 2:00 to 2:34: the stop-start passage ("coiled spring")
- Quietest full-band stretch (-16 to -17 dBFS; width 0.28 to 0.36 at 2:00 to 2:12; LV). The wall ("other") is at -25 to -31 dB, lower than the 1:30 to 1:55 wall (-15 to -16) (LV). Every 6.15 s a single held sub-bass note hits (2:01, 2:07, 2:13.5, 2:19.5; IMG 0120 bass panel shows bright low bars that last about 2 s then stop dead) with a chroma E-ish bar under the D (IMG 0120 chroma; the E is probably the sub-note; low-medium).
- **Feeling: a thud-and-breath cycle, like a held pulse or a heavy footstep every eight beats; tension that gets released only in small doses.** The cause is the metronomic 8-beat bass hit followed by dead silence in the low end, over an unchanged D (open fifth, no clear third, IMG 0120 chroma). The ear waits for a resolution that the harmony refuses. High on the structure, medium-high on the feeling.
- **2:13 to 2:15: setting off.** "Other" gains about 6 dB, width 0.30 to 0.55, voice re-enters at 2:15 (IMG 0120 vocals panel shows strong broadband bursts at 2:15 to 2:17.5 and 2:18.5), chords finally travel Am, D, G, D, Dm over 2:15.6 to 2:20 (CH, medium). Feeling: purposeful excitement, "they are off" or "the list begins". Medium-high.
- **2:21 to 2:39: place names as a checklist** (LY: Staveren, Hindeloopen, Workum, Nolswacht?/Hartwerd?, Harlingen?, Franeker?, Dokkum, Leeuwarden; the Whisper spelling is poor, so only "a list of Frisian town names, ending with Leeuwarden at about 2:38", medium). Feeling: an itinerary being ticked off, a sense of covering distance, anticipation and growing stakes, with the 8-beat sub-notes as mile markers. Weak evidence for "mile markers"; it is my interpretation of the 6 s regularity against the place-name rhythm.
- Mild unease: minor-ish colour and quick chord walks (CH, medium-low). The sub-bass holds feel "grand and heavy" (a medium-high reading).

### 2:38 to 2:48: bass locks on, the build to the statement
- Bass continuous from about 2:38 and then to the end (LV). Level climbs: -12.7 to -10.7 at 2:45 to 2:46. Width 0.42 to 0.46 (narrower: centred, ceremonial). Feeling: arrival, the long wait over, the engine fully on. High on cause.
- **2:44 to 2:48: the final statement.** "Where everyone has to make a move / that is the Elfstedentocht" (LY, 2:44 to 2:48). The voice is centred and the mix is slightly louder (WIN 0160 peak -10.6). Feeling: a ceremonial summing-up, the one line that tells you what this all is.

### 2:48: one-beat hole
- All four stems drop together, about 11 dB level drop for about 0.4 s (WIN 0160; I did not re-measure the 11 dB, but my table at 2:48 shows the mix falling from -10.7 at 2:45 to -12.4 at 2:48 which only partly shows because it is a short event in a per-second table; medium on the size). Feeling: a gasp, a held breath, then the release into the riff. Medium-high that it is a real dropout (two other windows and the image agree).

### 2:49 to 3:08: the sprint, hypnotic and dark-edged
- No more voice (vocals -65 dB, LV). Width 0.69 to 0.85 (the widest sustained stretch except 1:30 to 1:36). Bass -17 to -20, drums -17 to -19, "other" -16 to -17 (LV). A riff in a chromatic circle around D3 with C and D# neighbours (WIN 0180, medium-low: it comes from the lead tracker on a noisy stem). One chord (D) for the whole closing 20 s (CH: D held from 2:48 to the end).
- Feeling: a relentless, trance-like, determined sprint, loud and wide and bright; a "no turning back" finish with a dark rim (the chromatic neighbours make it grind, not soar). High on the relentless; medium on "dark rim".

### 3:08.4: the cut
- RMS -15.7 at 3:08.0, -53.9 at 3:08.3, -77 at 3:08.5 (MY). Not a fade, not a final chord; a gate-like cut. Feeling: abruptness; the listener feels it as a stop, not a resolution: the race is still going on when the record ends. That is a specific, measurable reason the piece feels "unfinished" or "continuing offscreen". High on measurement; medium on the interpretation.

## 3. The arc as a shape (feeling intensity, my reading)
Fast ignition (0:01) -> stern setup (0:10 to 0:32) -> first release (0:32) -> swelling engine (0:40 to 1:15) -> **lightening by subtraction (1:15)** -> suspended glide (1:27 to 1:40) -> **impact (1:40)** -> peak loudness (1:52 to 1:54) -> **collapse to drums (1:55)** -> coiled stop-start (2:00 to 2:34) -> setting off (2:13 to 2:21) -> itinerary (2:21 to 2:39) -> lock-on (2:38) -> statement (2:44 to 2:48) -> gasp (2:48) -> sprint (2:49 to 3:08) -> cut (3:08.4).
Features of this arc: the emotional peaks are **not marked by pitch or chord** but by low-end events, and the track is essentially a one-chord piece, so a listener's emotion is driven by **"what is missing"** more than "what is played". Energy is not a rising line; it is a series of drops and returns.

## 4. How it would feel as a whole (and the paradoxes)
- **Stoic, not angry.** The distorted wall invites "aggressive", but the harmony is open (D with an open fifth) and CLAP "aggressive" is mostly near zero in the middle windows (WIN 0060, 0080, 0100). Result: determination and endurance. This agrees with the commissioned subject (an endurance race) and with documented reception (drive, physical effort; context.md), though I am not claiming the band intended it.
- **Hot band, cold subject.** Loud, wide, bright, driving music under a narrator reading "16 degrees below zero". The temperature word is read over a sound with no cold in it; the "cold" is only the stern spoken tone and bright top layer. That mismatch is interesting and probably deliberate, but I have no evidence about intent (low, interpretation).
- **Old voice, new machine.** A flat archival announcer over a machine-regular 16th grid (CLAP "drum machine" at 2:00 to 2:15, weak). It reads as human fact against a mechanical drive: "history carried by an engine". Interpretation, medium.
- **Memory without sentimentality.** Nostalgia comes from the voice and the scratchy-archive timbre, not from the harmony (no sad cadence, no soft piano, no sweeping strings that I can measure). The music itself is more "push" than "pine". Medium.
- **Repetition as a feeling.** D for 94 s as a labelled chord plus another 33 s as Dm: the pedal creates hypnosis. After 90 seconds the ear no longer registers the key; the drop/return of the bass becomes the "melody". High on structure; medium on the feeling.

## 5. What measurements cannot tell me
- Instruments: I cannot say guitar vs synth vs sample; "distorted wall" is spectral density. CLAP "distorted guitar" and "post-rock" are model tags, not proof.
- The actual melody/riff shape: LN is a vocal-stem tracker, and on loud sections it reads speech and leakage.
- Mode: the third is unresolved; D major vs D minor is a near tie (0.76 vs 0.756, AF). Any "minor-sounding" statement is conditional.
- Tone of voice in feeling terms (grave, matter-of-fact, warm): inferred from level, pitch and context, not from the Dutch content, which Whisper only partly recovers.
- The size of the 2:48 hole: seen as a stem dropout in images and the window note, not re-measured at sub-second resolution by me.
- The emotional effect on a particular human: all of the above is a reasoned estimate, not a listening test.

## 6. Questions for fellow specialists
1. **To the harmony specialist:** Across the whole track D is labelled for 94 s and Dm for 33 s, with a near tie in key (D major 0.76 vs D minor 0.756), and chroma shows no clear F or F sharp. Can you establish from the stems (bass.wav, other.wav pitch-class energy at F vs F-sharp, per section) whether the third is ever really present, and does it differ between the 0:20 to 0:40 stretch, the 1:27 to 1:40 bass-less glide and the 2:49 to 3:08 sprint? That would tell me whether the "yearning" at 1:27 and the "dark rim" at the end come from mode or only from texture.
2. **To the rhythm specialist:** The sub-bass notes between 2:00 and 2:38 recur every 6.15 s (8 beats at 0.767 s), while drums run 0.19 s semiquavers. Where do the bass hits fall on the bar (beat 1 of a 4/4 bar of 4 beats, or on a different downbeat from the drums' accents), is the drum pattern the same every bar, and which of 78 or 156 bpm would a person naturally tap? The answer changes whether I describe the pulse as heavy-and-slow or fast-and-driving.
3. **To the sound specialist:** Does the stem evidence (spectral roll-off, harmonic partials, transients, and the wall's sustain in other.wav) favour distorted guitar, synth, or a sampled/processed layer, and does the 2:00 to 2:14 wall (-25 to -31 dB) differ in timbre from the 1:30 to 1:55 wall (-15 to -16 dB)? I am relying on this to say whether the loudest moments feel "guitar-rock heroic" or "machine-like".

(Optional extra, for the form specialist: do you divide the piece at 1:15, 1:40, 2:00, 2:38 and 2:48 as I do, or do you see the AF sections 14.8, 66.4, 75.6, 87.9, 109.4 as more meaningful?)
