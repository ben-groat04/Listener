# video1 (PSB, "Elfstedentocht Part 1"): the music, as a listener hears it

Written from the ten window notes (`win_0000` to `win_0180`) and all three rounds of the seven specialist files (form, harmony, rhythm, sound, voice, feeling, lineage). Where rounds conflict, the latest, best-measured statement is used and the conflict is listed in section 9. I cannot hear audio. Every claim rests on measurements and each carries a confidence tag: **H** high, **M** medium, **L** low.

Evidence shorthand: [lv] `per_second_levels.json`; [ch] `chords.json`; [ln] `lead_notes.json`; [clap] `clap_tags.json`; [img NNNN] `music_views/window_NNNNs.png`; [ab] `audio_features/`; [lyr] `lyrics/` (Whisper); [Rn-x] specialist x, round n; [win NNNN] window note. CLAP is a noisy zero-shot model and is used only as weak support. Times are m:ss. The track is 3:08.7 long (the official length is 3:09, per `context.md`).

---

## 1. The track in a paragraph

This is a loud, relentless, instrumental-rock groove built around one note, D, with a Dutch archive narrator talking over it. It is about 78 BPM at the slow beat, with a fast flutter of drums over it. The drums run for the whole piece, and it has no verse, chorus or tune. The drama comes from three things being switched on and off on a regular bar grid: the bass, the dense distorted "wall" layer (probably guitars, unproven), and the spoken voice. The result feels like "disciplined urgency": a heavy step with a fast heartbeat [R3-feeling, M]. It opens with a short swell and a hit, builds layer by layer, floats on a bass-less lift (1:15 to 1:40), lands hard when the bass returns (1:40), pulls down to a thin, high, hollow block with six slow sub-bass thumps (about 2:00 to 2:38), re-ignites with the narrator reading out a list of Frisian towns, then ends with the narrator's last line, a half-second hole (2:47.8), and a bright, wide, loud run to a short taper-out at 3:08.4 [R3-form, R3-rhythm, R3-feeling]. The harmony stays on a D pedal throughout, with a missing or ambiguous third, so it sounds stern and driven rather than sad or triumphant [R3-harmony, M].

---

## 2. Song map

Boundaries are high confidence (from stem on/off events [lv], [img], and the bar grid [R2-form]). Section names are mine. The feel column is interpretation, each tied to a measured cause.

| m:ss range | Section | What is playing | What it feels like |
|---|---|---|---|
| 0:00 to 0:01 | Swell and hit | A rising swell in the drum stem itself from 0:00.2 (-64 to -38 dB by 0:00.6), a hit at 0:00.7 (-14 dB). The other stem is silent until 0:01.3 [R1-form, lv, H]. | A snap to attention, not a cold slam. |
| 0:01 to 0:10 | Intro build | Drums from 0:00.8. The "other" wall enters at about 0:01.3 [lv, img 0000]. Bass enters at about 0:03 (-66 to -44 dB in one second), then rises to -36 dB at 0:06 and -19.5 dB at 0:20 [lv]. D chord from 0:01 to 0:08 [ch]. | Curious, leaning in. A pulse starts and layers join (M). |
| 0:10 to 0:31.7 | Narration over the band | Spoken Dutch: the date "18 januari 1963", the time (half past five in the morning; Whisper's Dutch pass has "half zes in de ochtend" at 0:16.6 to 0:18.0, and Dutch "half zes" means 5:30; M), the crowd, and the sentence "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht" [lyr]. Drums, bass and wall continuous. | Informed, steady, slightly detached. A calm voice over a pulse that never relaxes (M-H). |
| 0:31.7 to 0:41 | Band alone | Voice stops at 0:31.7, on a bar line. Drums brighten (centroid about 1.5 kHz to 3 kHz). Stereo width jumps 0.35 to 0.55. Bass gets rougher from about 0:35. | Relief, "now the band takes over" (M). |
| 0:41 to 1:15 | The build | Short narration bursts at 0:41, 0:51 to 0:56 ("16 degrees below zero", "a monster ride of more than 200 km") and a possible short vocal-stem burst at about 1:03.5 (not shown to be speech, L). The wall swells about 11 dB (-25 to -14 dB by 0:57). Hats open from about 1:05. Width climbs to 0.6 to 0.7. K-weighted loudness peaks at about -6.6 LUFS at 1:07 [R2-form]. | Determination, forward drive, accumulating weight (M-H). |
| 1:15 to 1:27 | Bass-less float | The bass leaves at about 1:15.3 (-28.7 dB at 1:15, -65 dB at 1:16) and returns at 1:40.0; a faint blip at 1:28 to 1:29 (-43 dB) is probably bleed. The mix drops 4 to 6 dB. The wall thins to bright upper lines. The tonic D is nearly absent from the wall for about 8 s [R2-harmony]. Narrator's list of riders and nations from about 1:18.9 (vocal-stem onset; Whisper says 1:19.7) to 1:27 ("575 wedstrijdrijders, rond 9500 toerrijders"). | Floor falls away: light, suspended, slightly uneasy (H on cause, M on the word). |
| 1:27 to 1:40 | The lift | The voice stops at 1:27. The wall jumps (-22 to -15 dB), loudness returns, width goes 0.36 to 0.78. Still no bass. A slow stepwise line (A, C, B, G, then D) runs across 1:15 to 1:36 [R2-harmony]. | Lifting, opening out, yearning, rising without ground (M-H). |
| 1:40 to 1:55 | Landing | The bass returns at 1:40 (-53.8 dB at 1:39 to -19.1 dB at 1:40). Width pulls into the centre (0.78 to 0.40). Dense, loud, voice-free. | Arrival: weight slams back after 24 s of absence. Emotional high point of the first half (M-H). |
| 1:55 to 2:14 | Pull-down and thin block | The bass leaves at about 1:55 and the wall sweeps into a broad wash at about 1:58, then collapses. The mix drops to about -13.5 LUFS at 2:05. Width falls to 0.2 to 0.3. The sub thumps start at 2:01.1. | Sudden emptying: held breath, exposed, hollow (M). |
| 2:00 to 2:38 | Sub thumps | Six identical 42.6 Hz sub hits at 2:01.1, 2:07.2, 2:13.4, 2:19.5, 2:25.7 and 2:31.9, with the bass otherwise silent. A seventh bass event follows at 2:38.4. | Slow, heavy, regular. Coiled, "waiting for something large" (M). |
| 2:14 to 2:38 | Re-ignition and town list | The wall thickens (+6 dB) at 2:13. Width goes 0.3 to 0.55. The narrator reads a town list from 2:16 to 2:36. The chord walk (A, D, G) starts 2.2 s after each thump. | Lift-off: "setting off", an itinerary being read (M). |
| 2:38 to 2:47.8 | Run-up | Bass returns (-64 dB to -19 dB by 2:39). Chords turn (F, C, D, C). The final line, "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht", starts about 2:44.4 (vocal-stem onset; Whisper 2:43.8) and ends about 2:48.2. | Weight returns; a resumed journey (M-H). |
| 2:47.83 to 2:48.21 | The hole | Drums out about 0.4 s (167.8 to 168.2 s), bass out about 0.65 s (167.55 to 168.2 s); timing against the beat grid is within 0.1 s, not exact. The guitar holds (instrument unproven). The narrator's last syllable decays inside it [R2-form 2.3, H on timing]. | Held breath, then release (M). |
| 2:48.2 to 3:08.4 | Bright release plateau | One chord, D. The drum energy above 5 kHz rises from about 1% to 9 to 12%. Width 0.7 to 0.86. Mix steadily about -11 dBFS. K-weighted loudness -7.0 to -6.4 LUFS, the loudest and steadiest stretch. No voice. | Hard, driven, grinding. The band takes over (M-H). |
| 3:06 to 3:08.4 | Close | Denser drum onsets from about 3:06. Chroma shifts toward G and E just before the end (L). Level -11 dB at 3:07, -15.5 dB at 3:08.0, below -60 dB by 3:08.4, -72 dB by 3:08.5. | A cut-off, as if the effort carries on offscreen (M). |

Block lengths on the 4-beat bar grid: 24, 28 and 32 bars to the three bass events at 1:15, 1:27 and 1:40, then odd blocks of 5, 2, 2, 2, 8 and 3 bars, and a final run of about 6.5 bars [R2-form, R3-form]. Bar one is tracker-derived. The drum kick band cannot confirm which beat is "one" [R3-form, M].

---

## 3. Harmony and melody

**Key and mode (H on D, L on mode).**
- D is the tonic everywhere. Whole-song key is D major 0.76 against D minor 0.756, effectively a tie [ab summary].
- Power chroma shows D 1.00 in every window, with the fifth A and the flat seven C always present [R3-harmony].
- The third (F or F sharp) never rises above about 0.16 in power, except one flicker (F 0.39 at 1:47) [R3-harmony]. So the sound is a bare D5 power-chord world. Dorian or Mixolydian by pitch content, undecided because the third is missing.
- "Stoic" and "stern" are texture and rhythm, not mode. "Sad" and "triumphant" by mode are unsupported [R3-feeling].

**Almost no progression (M-H).**
- [ch] logs 125 chord changes. Most are detector labels on a static D. The Cm at 1:48, the Fm and Cm at 0:43 to 0:45, and the 20 s "D" at the end are all examples [R3-harmony, R2-harmony].
- Across the track there is no 8-beat harmonic cycle and no V to I cadence. Resolution comes from the bass returning and the stop at 2:48, not from chords.

**The two places where pitch does move.**
1. **1:15 to 1:40, the one melody (M).** The `other` stem plays a slow stepwise line. The pyin contour (per 0.5 s, polyphonic and rough) reads A3 about 1:16 to 1:18.5, C4 to 1:21, B3 to 1:23, G3 to 1:24, D3/D4 from 1:24.5 to 1:27.5, then a D2 drone from 1:27.5 (source: pyin on the other stem, not lead_notes.json, which does not show this line). Against D that is fifth, flat seven, sixth, fourth, root. The tonic D is nearly absent from the wall from 1:15 to about 1:24 (D 0.08 to 0.26; other-stem chroma: C top at 1:18, B at 1:21, D back at 1:24) and the bass is also out. A slow attack (median 0.22 s to peak, L) suggests a sustained or swelled tone rather than a pluck [R3-sound]. This is the only candidate for the track's "yearning".
2. **2:00 to 2:40, an A-centred walk (M).** A is strongest in `other` from 2:00 and 2:12 to 2:33. Chord labels step A, D, G, D, G and then, at 2:34.8 to 2:39.5, D, G, Dm, F, C, D [ch]. The walk starts 2.2 s after each sub drop, one label per beat (0.77 s), and runs about 3.8 s to the next drop [R2-harmony, R3-rhythm]. It leans on the dominant side of D and does not establish a new key. The F at about 2:37 is the one place a third-like note appears clearly for about 3 s.

**The sub (M-H on measurement, L on perception).** The low thump is a fixed 42.6 Hz tone, 42 cents flat of F1 and 58 cents sharp of E1. It starts about 3 to 6 Hz sharp and falls within about 0.3 s, with a soft 20 to 110 ms rise and almost nothing above 300 Hz [R2-harmony, R3-sound]. It does not follow the chords. It adds weight without a clear note, and may be nearly inaudible on small speakers.

**The riff at the end (L-M).** From 2:48 the chroma is a D bar with short stabs on C, A, B and E at about one per beat. The pyin lead-notes [ln] 3:00 to 3:07 show a gritty low figure circling D3 (C, C sharp, D, D sharp, A sharp, B). This is a chromatic riff on a drone, not a cadence. The exact notes are not recoverable from chroma on distorted guitar.

**Where the harmony sits relative to the form.** Harmony changes at stem boundaries (1:15, 1:24, 1:40, 1:56, 2:12, 2:36 to 2:38, 2:48) and not on its own schedule [R2-harmony, R3-form].

---

## 4. Rhythm and groove

**Tempo (H on the number, L-M on the octave).**
- Beat tracker 78.0 to 78.3 BPM (0.769 s level; summary.json says 78.30), steady to 2:48 where beat_times ends (last beat 2:48.0). After 2:48 the beat file cannot show drift; a drum-onset autocorrelation still peaks at 0.766 s through 3:06 but weaker (0.62 against 0.72). Four-beat cycle about 3.077 s [R3-rhythm, [ab] beat_times]. The refit drum-slot period is 0.1923 s.
- Whether the "real" quarter note is 78 or 156 BPM is not settled. Rhythm moved to about 55/45 in favour of 78, because the hat plays every 0.385 s and the kick takes the sixteenth positions. This is structural, not proof [R3-rhythm]. Either way the felt weight is 0.77 s, the walking step is 0.38 s and the flutter is 0.19 s.

**Groove (M-H).**
- The 0.19 s "comb" seen in the windows is the sum of two interlocking layers, not a continuous sixteenth-note pattern [R3-rhythm].
  - The hat band (6 to 11 kHz) sits on the even slots, every 0.385 s, with the accent every 0.769 s.
  - The kick (40 to 120 Hz) sits mostly on the odd sixteenth slots (1, 5, 7, 9, 13, 15), and is nearly absent on 0, 4, 8, 12.
- From 2:01 to 2:38 the hat thins further to a fixed seven-slot pattern.
- No swing. About 5.3 drum onsets per second from 2:20 to 2:45 and 5.25 from 2:50 to 3:06, so no densification after the stop [R3-rhythm].
- It is syncopated and stiff. Motorik was withdrawn as a pattern claim. It is nearer funk, hip-hop or post-rock programming [R3-rhythm, R2-lineage].

**The drums never change gear (H).** All form events are bass, wall or voice moves. The only drum event in the whole track is the 0.38 s hole at 2:47.83 to 2:48.21 [R3-rhythm].

**The sub thumps (M).**
- The six drops (2:01.09, 2:07.24, 2:13.39, 2:19.55, 2:25.70, 2:31.85) all fall at slot 21 mod 32 of the drum grid, spaced 6.15 s (8 beats), within about 15 ms of the grid [R3-rhythm].
- Slot 21 is a sixteenth after a beat, off the hat accent, on a kick position. The block is therefore "heavy and metronomic but leaning" [R3-feeling, M].

**The stop at 2:47.8 (H on timing).**
- Duration about 0.38 to 0.45 s, exactly two grid slots. It starts on a beat and ends on the off-eighth, so it is a catch inside the bar, not a bar-line stop [R3-rhythm].
- The drum loop resumes on the same phase [R2-form, R3-rhythm].

**Voice versus band.** Speech is free in time against the grid, except at its two exits (0:31.7, which is on a bar line, and 2:47.8) [R3-voice, R3-rhythm].

---

## 5. Sound and production

**Overall (H on style, M on instrument labels).** A dense, high-gain, heavily limited alt/post-rock mix. Loudness is very flat: about 8 LU of K-weighted short-term range, mostly at the section ends [R3-sound]. Per-second dBFS mostly sits between -9.5 and -16.5 [lv].

**Layers.**
- **Drums:** dry, tight, with a short decay (median 110 ms). They are bright, with the hat band strong. Nothing shows a long reverb tail [R3-rhythm, img]. Kick amplitude CV is 0.18 and hat CV 0.27. That fits either a played kit or a sequenced one [R3-sound, L].
- **Bass:** a low line, with flat floors of about -65 dB when out (no ring-out, no room tone). That behaves like a muted stem or a gated synth, but demucs also gates quiet stems, so it is not proof [R3-sound, M-L]. The sub drops are the one clearly designed sound.
- **"Other" (the wall):** not one wall but four timbral states [R2-sound, M-H]:
  1. A low D drone with the narration (0:01 to 1:15);
  2. A mid wall;
  3. Thin high open fifths (2:00 to 2:14, centroid about 1.5 kHz, width 0.29);
  4. A bright wide wall from 2:48.
  CLAP gives "distorted guitar" as top label in only about a third of 5 s windows (song average 0.44) and flips between brass, drum machine, synthesizer and electric guitar, so it is weak, unstable support. The guitar reading rests mainly on `context.md` (guitar-riff rock), which itself says to verify instruments. The stems cannot separate guitar from synth. I call it "the wall" and treat "guitar" as an inference.

**Width.** The stereo width measure runs 0.20 to 0.86 [lv]. It is narrowest when the mix is thin and centred (about 0.2 to 0.36 at 1:58 to 2:13, mostly 0.2 to 0.3), widest in the bass-less lift (0.7 to 0.84 from 1:27 to 1:39) and the final run (0.62 to 0.86 over 2:49 to 3:07). When the bass returns at 1:40 the width pulls in from 0.78 to 0.40. That is consistent with centred bass energy re-entering (M), but a correlation of width with bass dB across the whole track is only 0.01 [R2-sound], so width is not simply a bass effect.

**Brightness.** Mix centroid is about 1.7 to 1.9 kHz at 1:00 to 1:05, about 2.6 to 2.8 kHz at 1:06 to 1:14, 1.6 to 1.9 kHz at 2:40 to 2:48, and 2.9 kHz from 2:48 [win 0060, win 0160]. The final run is brightest, driven by a cymbal-led kit (hat and crash share 3% to 12% [R2-sound]; drum centroid 2.1 to 2.9 kHz becomes 4.7 to 5.0 kHz [R2-form]).

**Loudness and weight are different axes (M-H).**
- Loudness (K-weighted) peaks at 1:07 to 1:15 (about -6.6 LUFS) and 2:48 to 3:08 (-6.4 to -7.0, steady within about 0.3 LU). It returns at 1:27, 11 s before the bass.
- Weight peaks at 1:40 to 1:55, where the bass adds only about 0.1 LU but about 40 dB in the bass stem.
- The trough is 2:02 to 2:13 (about -13.5 LUFS) [R2-form].

**Mix of the voice.** Mostly below about 4 kHz (95% roll-off 3.4 to 4.6 kHz depending on passage), dry, centred, no noise bed. The vocal stem sits roughly 0 to 10 dB under the other stems depending on passage, and about level with the wall and bass at 2:44 (demucs stem dB are not strictly comparable). The band does not duck for it [R3-sound, R3-voice]. That fits mid-century film or radio audio set against a modern band. The era is an inference.

**Ending.** The mix goes from -11 dB at 3:07 to -15.5 dB at 3:08.0, below -60 dB by 3:08.4 and -72 dB by 3:08.5 (track length 188.66 s). That is a taper or gate of about 0.4 s, not a hard cut and not a fade [R1-form, win 0180 timings].

**Playback dependence.** The 42.6 Hz sub largely vanishes on small speakers [R3-sound, R3-feeling]. On those, the felt event at each thump is the drop in the wall and the narrowing.

---

## 6. Voice, words and samples

**The voice map (M).** Whisper finds speech at these times [R3-voice]. The vocal stem also shows two short bursts, about 1:46.7 to 1:48.8 and 1:57 to 1:58.3, which could be leakage or non-lexical sound; not confirmed as speech. Whisper's "MUZIEK" segment at 1:42 to 1:43 is probably a hallucination. Whisper segment times are loose by about 0.5 to 0.8 s; vocal-stem onsets are given where measured.
- 0:09.9 to 0:31.7 (date, time, crowd, the sentence);
- about 0:41.1 to 0:42.4 (the twelfth Elfstedentocht; vocal-stem onset, Whisper says 0:40.6);
- 0:51 to 0:56 ("16 degrees below zero"; "a monster ride of more than 200 km");
- possible short vocal-stem burst at about 1:03.5: not shown to be speech, possibly cymbal or hat bleed like 1:46.6 (L); not counted as speech;
- about 1:18.9 to 1:27.0 (Whisper starts 1:19.7; 575 racers, about 9,500 tour skaters, nationalities garbled);
- 2:16 to 2:36 (town list);
- about 2:44.4 to 2:48.2 (the closing line; Whisper starts 2:43.8).

**Not speech (H after the round-3 checks).**
- 1:46.6 to 1:49 is a noise smear in the vocal stem with a D held in the guitar and bass underneath.
- 1:57 is a held D3 near 150 Hz present in all three stems, so the D pedal is bleeding into the vocal stem.
- Whisper's "MUZIEK" at 1:42 and "Bedankt voor het kijken!" at 3:07 are hallucinations (the stem is at -66 dB then) [R3-voice, R3-harmony].
- The window notes for 1:40 to 2:00 and 3:00 to 3:09 treated some of these as voice. That reading is overturned.

**The words.**
- Dutch, language probability 1.0 [lyr]. Whisper is unreliable over the loud band. Reliable: the date "18 januari 1963", the key sentence "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht", the numbers (575, about 9,500), and the temperature and distance lines. Place names in the town list are Whisper's garbles of the 1963 route. Whisper recovers Staveren, Hindelopen (translate pass, 2:25.8), Workum (as "Markum"), Harlingen ("Hartingen"), Dokkum and Leeuwarden with reasonable confidence; Sneek ("Sleek") and Sloten ("slotten") are loose garbles; IJlst and Franeker are inferred from the route, not heard. Leeuwarden is timed 2:34.7 (Dutch pass) but 2:38 (translate pass), so the end of the list is uncertain by about 2 s (L-M).
- The key sentence appears twice, at 0:27 to 0:31.7 and at 2:44 to 2:48 [R3-voice]. Same words (H). Same recording or a re-cut: unresolved (waveform correlation 0.09; MFCC DTW 0.278, above the speech controls) (L-M).

**How it is delivered (M-H).**
- One flat, falling, unperformed voice at a steady 4 to 5 syllable-peaks a second, with no quickening (4.3 at 0:10 to 0:18, 5.1 at 0:19 to 0:31.7, 5.4 at 0:51 to 0:56, 4.9 at 1:19.7 to 1:27, 4.2 at 2:43.8 to 2:48.3). The town list is slower and spaced (2 to 3 peaks per second with many pauses) [R3-voice].
- No chopping, pitch shifting or looping that I can measure. It is a clean, centred, band-limited sample [R3-voice].

**What the voice does (M).**
- It supplies facts (date, crowd, cold, distance, riders, route). The band supplies the emotion; the narrator adds no excitement of its own [R3-voice, R3-feeling].
- Entries come into space made by subtraction: 1:19.7 after the bass leaves at 1:15, and 2:15 on the A, D, G walk. Exits sit at changes of state (0:31.7 on a bar line, 2:48 into the hole) [R3-voice].
- The longest voice-free block (1:27 to 2:15) coincides with the loudest, densest sections and the thin block. The story is told in the sparse passages and held back when the band is at full weight (M-H).

**Not sung.** The lead-pitch tracker [ln] finds only speech inflection and instrument bleed. There is no sung melody anywhere (H).

---

## 7. The emotional journey and its musical causes

The feelings below are my interpretation of measured causes, not listener data (see section 10). The mechanism is the same throughout: a fixed pulse, a D pedal, and layers switched in and out [R3-feeling].

- **0:00 to 0:10, snap and gather.** A swell and a hit set a pulse; bass creeps up from silence; the wall enters at 0:01.3. Anticipation. Cause: layers entering one by one on a fixed pulse (M).
- **0:10 to 0:32, told a story.** A calm voice gives date, hour and crowd over a band that never relaxes. Documentary detachment against rock energy. Cause: a flat voice at constant speech rate over constant drums (M-H).
- **0:32, the voice finishes the sentence on a bar line and the band opens up.** The width jumps, the drums brighten. Relief, "now it's ours". Cause: voice exit, width 0.35 to 0.55, drum centroid 1.5 kHz to 3 kHz (M).
- **0:41 to 1:15, momentum.** Repetition, a wall swelling 11 dB, hats opening, width widening. A heave forward. Cause: accumulating layers plus a K-weighted ramp to -6.6 LUFS (M-H).
- **1:15, the floor falls away.** The bass vanishes, the mix drops 4 to 6 dB, and the wall turns thin and bright. Light, suspended, slightly uneasy. Cause: bass and the D in the wall both leave (H on cause).
- **1:27 to 1:40, lift without ground.** The wall surges, width doubles, loudness comes back, and a slow stepwise line floats over no bass. Opening-out, yearning. Cause: the line plus the missing floor (M-H).
- **1:40, arrival.** Bass returns after about 24 s, width narrows, and the mix thickens. Weight, release, the "thump" the ear was waiting for. This is the emotional high point of the first half. Cause: bass +40 dB, width -0.27, loudness only about +0.1 LU (M-H on cause).
- **1:55 to 2:14, held breath.** Bass out again, guitars swept to a wash then a thin high figure, width collapse, mix 6 LU down. Exposed, hollow, waiting. Cause: stripped, narrow, high (M).
- **2:01 to 2:38, slow thumps.** A heavy low note every 6.15 s over an unchanged fast flutter. Anticipation, tipping at most into mild dread. Cause: the 42.6 Hz designed thump, off the hat accent, and the fixed hat pattern (M).
- **2:15 to 2:36, the itinerary.** The wall thickens, width opens, the narrator reads towns one by one over an Am, D, G walk. Setting off, checkpoints being called. Cause: +6 dB wall, width 0.3 to 0.55, and moving chords (M).
- **2:38 to 2:47, weight resumes.** Bass back, chords turning F, C, D, C, the sentence returns. Resuming a journey (M-H).
- **2:47.8, the hole.** A 0.4 s rest with the narrator's last syllable inside it and the guitar holding. A held breath that ends in release, not a shock (M).
- **2:48 to 3:08, the sprint.** The loudest, steadiest, brightest, widest stretch. Hard, driven, grinding, with chromatic friction around D and a cymbal-led kit. Cause: one chord with a circling riff, hat and crash share up to 12%, width 0.7 to 0.86 (M-H).
- **3:08.4, the end.** A half-second taper to silence with no cadence. The effort seems to continue offscreen. Whether it is the studio ending or an edit of the video is unknown (M on the feel, L on the cause).

Overall character: "disciplined urgency, heavy step with a fast heartbeat" [R3-feeling, M].

---

## 8. The five moments a listener remembers

1. **1:40, the bass slams back after 24 s.** The strongest contrast in the track. Bass goes from -53.8 dB at 1:39 to -19.1 dB at 1:40, width narrows 0.78 to 0.40, and the wall and drums are already dense. It is felt as weight and relief rather than louder, since loudness rises only about 0.1 LU [lv, R3-sound, R3-feeling]. The anticipation was built across the long bass-less passage (M-H).
2. **2:47.8, the half-second hole after "dat is de Elfstedentocht".** The narrator's key sentence ends, the drums and bass drop out for about 0.4 s while the guitar holds, then the band returns brighter and wider. It is the track's only drum event and a callback to the 0:27 line [R2-form, R3-rhythm, R3-voice] (M-H).
3. **1:15 to 1:27, the floor falling away.** The bass cuts dead at 1:15.0, the mix drops about 6 LU and the wall turns thin. The listener feels the lightness and loss before the voice returns at 1:19.7 [lv, R2-form] (H on measurement, M on feeling).
4. **The 6.15 s sub thumps (2:01 to 2:31).** A slow, very low gesture repeated six times over an unchanged fast pulse, in the quietest, thinnest part. It is the clearest designed sound in the piece, though it is largely lost on small speakers [R3-sound, R3-rhythm] (M).
5. **The 2:48 to 3:08 bright finish and the cut.** After the hole the band is at its loudest, steadiest, widest and most cymbal-bright, with a circling riff on D. It then ends abruptly with no cadence [R3-form, R3-sound, win 0180] (M-H). The opening swell-and-hit at 0:00.7 is a minor candidate (M).

Two honourable mentions: the key sentence of narration at 0:27 to 0:31.7 landing on a bar line before the band opens up, and the narrator's list of towns at 2:16 to 2:36 (M).

---

## 9. Where the specialists disagreed, and the best-supported view

| Issue | Positions | Best-supported view |
|---|---|---|
| Climax: 1:27, 1:40 or 2:48? | Round 1: various (1:40 by dBFS; 2:48 by level). Feeling ranked 1:40 first, Form ranked 2:48 first. | Two peaks: emotional arrival at 1:40 (weight, width, relief), physical release at 2:48 to 3:08 (loudest, steadiest, brightest). 1:27 is a lift, not a peak [R3-form, R3-feeling, M-H]. |
| Loudness at 1:40 | Window notes said loudest around 1:40 (dBFS). Form's K-weighting: 1:07 to 1:15 and 2:48 to 3:08. | Accept K-weighting. 1:40 adds about 0.1 LU; loudness returns at 1:27 [R2-form, R3-sound, M-H]. |
| Bass jump size at 1:40 | Window note: about 34 dB. Feeling: +42.6 dB. | The 1 s bins in [lv] give -53.8 to -19.1 dB (about 35 dB). Feeling's +42.6 dB comes from its own before/after table (F2), whose windows I did not re-derive, so the gap is probably a difference in the averaging windows (my inference). Both agree on a very large step [lv, R3-feeling, H on size, L on the exact figure]. |
| Tempo octave | Round 1 rhythm: 60/40 for 156. Round 3: 55/45 for 78. | Unsettled. 78.0 BPM at 0.769 s is certain. Hat on 0.385 s with a kick on sixteenth offbeats mildly favours 78 as the quarter note. Felt weight is the same either way [R3-rhythm, L-M on octave]. |
| Drum pattern | Window notes: continuous sixteenth-note comb. Rhythm R3: hat on even slots, kick on odd. | Rhythm R3. The comb is the sum of two interlocking layers [R3-rhythm, M-H]. |
| The 2:48 stop | Window 0160: "all stems black", Form R1 "full stop". Form R2: drums and bass out about 0.45 s with the guitar and last syllable inside. | Form R2 and R3. Drums and bass out about 0.38 to 0.45 s, the guitar holds, the loop phase is unchanged [R2-form 2.3, R3-rhythm, H]. |
| Grid shift after the stop | Round 1 rhythm: possible 1/8 beat shift. Rhythm R3: retracted. | No shift. Phase creep is about 0.09 s over three minutes, nothing at the stop [R3-rhythm, H]. |
| Bar alignment of the stop | Form R2: 0.7 beat after the bar line. Rhythm R3: starts on beat 3 of the cycle. | Both agree it is grid-aligned and not clearly bar-aligned. A catch inside the bar [R3-form, R3-rhythm, M]. |
| Voice at 1:46.6 and 1:57 | Windows 0100 and 0120: a burst of voice at 1:46.5 to 1:49 and a second at 1:55 to 1:58. | Not speech. Noise smear plus held D bleed; the 150 Hz tone is in all three stems [R3-harmony, R3-voice, H]. |
| Voice at 3:07 ("Bedankt voor het kijken!") | Whisper transcript. | A hallucination; the vocal stem is at -66 dB [R3-voice, H]. |
| Chord labels (Cm at 1:48, Fm/Cm at 0:43, 20 s "D" at the end, Gm and Dm throughout) | Window notes read some as real chords. | Mostly detector reactions to a D pedal under distortion. The riff at the end is a figure over a drone [R3-harmony, M-H]. |
| 2:00 to 2:20 harmony | Window 0120: "Dm held". Harmony R2: A-centred, no third. | A-centred walk, no third [R2-harmony, M]. |
| 1:27 to 1:40 harmony | Window 0080: D5 wall with a bare fifth, "Am/D alternation" as artefacts. Harmony R2: a stepwise line from 1:15 to 1:36 with the tonic nearly absent for about 8 s. | The two are compatible. D returns at about 1:24 to 1:26 and the line runs through the D-pedal wall. The line is the only melody [R2-harmony, M]. |
| The sub pitch | Round 1 harmony: F1 sub. Round 2: 42.6 Hz, 42 cents flat of F1. | Quote 42.6 Hz and treat it as a designed, fixed, falling-edge thump; any chord colour is withdrawn as a perception claim [R3-harmony, M-H on measurement, L on perception]. |
| Does the sub fall on the accent? | Form R3: with the drum accent (guess). Rhythm R3: slot 21 mod 32, a sixteenth after a beat, off the hat accent. | Rhythm R3: "heavy but leaning" [R3-rhythm, R3-feeling, M]. |
| Opening and ending | Windows: "cold-start burst" and "abrupt loss in the last 0.3 s". Form R1: 0.7 s swell, and a 0.5 s taper. | Form R1: a 0.7 s swell then the hit; a taper of about 0.4 to 0.5 s [R1-form, H]. |
| Kit: live or programmed | Several windows lean "machine" from CLAP "drum machine". Sound R3: kick CV 0.18, waveform correlation 0.35. | Unresolved. Moderately consistent, not identical [R3-sound, L]. |
| Motorik | Lineage R1 resemblance. | Withdrawn as a pattern claim. Kept only as "a fixed ground" function [R3-rhythm, R2-lineage, M-H]. |
| Same take at 0:27 and 2:44? | Form and Lineage: "likely a deliberate edit". Voice and Sound: unproven. | Same words (H); same recording unproven. A frame, not a proven loop (L-M) [R3-voice, R3-lineage]. |
| Does the narrator speed up? | Feeling suggested a quickening build. | No. A steady 4 to 5 peaks per second, no quickening [R3-voice, M-H]. |
| Bass-stem silences | Sound R3: muted stems or a programmed bass. | Suggestive; demucs gating confounds it [R3-sound, M-L]. |
| Section blocks: strictly 2/4/8 bars? | Form R2: first half square (24, 28, 32). Lineage R3: not square (5, 3, 6.5). | Square in the first half, odd in the second; the 6.15 s sub cycle is exact [R3-form, R3-lineage, M]. |
| Mode | Windows lean major, minor or modal depending on the window. | Undecided. The third never exceeds about 0.16 in power chroma; stern, not sad [R3-harmony, L]. |

---

## 10. Uncertainties and what the measurements could not settle

**Cannot be known from stems and CLAP.**
- **Instrument identity (H that I cannot say).** Guitar versus synth in any state of the wall, and bass guitar versus synth bass. The wall is "distorted-sounding", and CLAP's "distorted guitar" and `context.md`'s "guitar riff" are supporting inferences. CLAP also gives "brass" at 0:50, 2:45 and elsewhere, which I reject.
- **Live versus programmed drums.** Kick and hat consistency fits either. Flat bass floors fit muted stems but are confounded by demucs gating.
- **Where beat 1 is.** The drum kick band cannot say. All structure statements are tied to the tracker grid, with the drum-slot count given where it matters [R3-form, R3-rhythm].
- **Octave of the tempo** (78 versus 156 as quarter note).
- **Major or minor.** The third is missing or flickers.
- **Riff notes.** The exact notes of the final riff and of the wall's rhythmic figure.
- **The final seconds.** Whether the end at 3:08.4 is the studio ending or an edit of the video. The beat tracker has no beats after 2:48; the drum-slot fit covers it [R3-rhythm]. The chroma shift toward G and E at 3:06.5 is not recorded in [ch] (L).

**Voice.**
- The words of the 1:03.5 burst; the identity and number of narrators; whether the closing line is the same take as 0:27.
- The place-name reading of the town list is inference.
- Whisper times drift by up to several seconds; the vocal-stem bursts are the better clock (about 0.3 s by eye) [win 0140].

**Feelings.**
- All emotion words are interpretations of measurements, not tested on listeners [R3-feeling]. Whether listeners hear the 1:15 to 1:40 line as melody at all is unknown (pyin on a polyphonic stem is rough).
- The 42.6 Hz sub's perceptual effect depends on playback.

**Measurement caveats.**
- K-weighted figures are the specialist's own implementation, not a calibrated meter.
- demucs stems leak (the vocal stem in particular carries D-pedal and cymbal bleed, and low "lead" notes after 2:50 are bass and guitar bleed, not a voice).
- The stereo-width figure depends on the project's definition (side-to-mid ratio).
- The window images were read by eye (timing error about 0.3 s) in places.

**Context kept at arm's length.** The artist, track, commission and archive credit are sourced in `context.md`. The identity of the narrator and source film, and any "newsreel" label, are not confirmed there. I have not used them to support any claim above.


## Check log

Cold-read check, music: video1. Refuted claims were re-verified against the measurements named in each refutation and fixed where the evidence held.

Fixed:
- Time of day: Whisper Dutch pass says "half zes" (0:16.6 to 0:18.0) = 5:30, not 6:30. Now medium confidence.
- Voice map: confidence lowered from H to M. Two further vocal-stem bursts (about 1:46.7 to 1:48.8, 1:57 to 1:58.3) noted as unconfirmed. Earlier "not speech" rulings elsewhere (noise smear, D bleed) stand as the likelier reading but are not proven.
- Speech onsets given from the vocal stem (0:41.1, 1:18.9, 2:44.4); Whisper segment times loose by about 0.5 to 0.8 s.
- 1:15 to 1:40 line timings moved 0.5 to 1 s earlier; source stated as pyin on the other stem.
- 2:36 to 2:39 chord walk corrected to D, G, Dm, F, C, D.
- Stereo width ranges corrected (0.20 to 0.86; 0.62 to 0.86 final run; thin block 0.2 to 0.36).
- Tempo wording: beat file ends at 2:48; no drift claim beyond it.
- Bass entry at about 0:03 (not a creep from 0:01); bass leaves about 1:15.3 with a faint 1:28 blip; intro swell is in the drum stem.
- Stop at 2:47.8: drums 0.4 s, bass about 0.65 s, grid alignment within 0.1 s.
- Ending levels corrected.
- CLAP "distorted guitar" claim replaced with the measured, weak picture.
- 1:03.5 burst downgraded to unconfirmed.
- Voice level and roll-off restated (about 4 kHz; 0 to 10 dB under the stems, level at 2:44).
- Town list restated with what Whisper actually recovers.

Left unverified (labelled as such, not changed): bar-one identity and block counts; 78 versus 156 BPM octave and hat/kick slot claims; drum onsets per second (detector-dependent, ratio holds); seven-slot hat pattern and slot period; instrument identity (guitar versus synth, played versus sequenced, bass type); sub-bass frequency, attack and glide figures; drum decay and CV figures; drum above-5 kHz share (direction agrees: checker got 1.4 to 3.3% rising to 13.5%); the four timbral states and the stepwise line (pyin on a polyphonic stem is rough); narrator identity and era; all feeling labels.
