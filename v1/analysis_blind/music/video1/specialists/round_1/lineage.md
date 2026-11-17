# video1: lineage specialist, round 1 (blind, measurements only)

Evidence key: WN = window notes win_0000..win_0180.md; MV = music_views/window_NNNNs.png (I opened window_0140s.png); CL = clap_tags.json; BT = beat_times.json; SUM = audio_features/summary.json; LV = per_second_levels.json; own = my librosa passes on drums.wav (stems_raw/htdemucs/song), reported below. I cannot hear; all lineage statements are inference from structure and spectral shape.

## 1. Sonic facts the lineage argument rests on

1. **Very steady pulse, about 78 BPM (felt possibly 156).** BT: 218 beats, mean inter-beat 0.770 s, s.d. 0.019 s (own), SUM tempo 78.3. A 2.4% s.d. is tight, consistent with a sequenced or very disciplined drummer (medium). Drum-onset autocorrelation (own, 10-60 s) peaks at 0.197 s, 0.383 s, 0.766 s: sixteenth, eighth and beat lattice, strongest at the beat. High confidence on the pulse, medium on machine versus human.
2. **Drum stem is low-weighted and nearly hat-free.** Own band split of drums.wav: 58-78% of energy below 150 Hz, 20-26% at 150 Hz-1 kHz, only 1-5% above 5 kHz in most windows (12% only in 3:00-3:08). About 4.2-4.6 onsets/s throughout. In MV 0140s the drum panel is a regular comb of short broadband hits, with no sustained hat or ride wash. So a kick/tom-led, tight, dry pattern; a snare-like crack is present (broadband bursts), but cymbal sizzle is minimal (medium; demucs may leak hats into "other").
3. **A harmonic "wall" in the "other" stem.** Dense stacked partials 0-8 kHz, hard roll-off near 8 kHz, little gap between harmonics (WN 0020, 0040, 0180; MV 0140s "other" panel). Reads as overdriven or fuzz guitar and/or saturated synth. CL top instrument is "distorted guitar" in 16 of 33 windows and "drum machine" in 12. Weak evidence individually; the spectral density supports "saturated" (medium), not "guitar" specifically (low).
4. **Static, pedal-point harmony.** Key: D major 0.76 / D minor 0.756 / G major 0.51 (SUM), i.e. third ambiguous; chroma shows D almost constantly on (WN 0040, 0100). Bass low notes at about D2 (73 Hz) (WN 0020). Chord labels hover between Dm, Am, D, G, C, F (MV 0140s: Dm-Am-D-G-D-G-Dm; Em-D-Gm-Am-C; Am-D-G-Dm-F-C-D), which sit as a D-centred modal/aeolian-mixolydian mix with a Dm anchor every 8 beats (WN 0140). Medium (labels noisy).
5. **Arrangement by layering and subtraction, not by song form.** Drums alone at 0:00, "other" at 0:01.3, bass 0:03-0:08, voice 0:09 (WN 0000). Bass punctuated in 6 s blocks (one entry per two bars) at 2:01, 2:07, 2:13 (WN 0120; MV 0140s bass panel shows the blocks at about 0-1.5, 5.7-7.7, 12-13.7 s). Bass dropped abruptly at 1:15 and 1:58 (WN 0060, 0100). A 0.35 s total cut at 2:47.8 then re-entry (WN 0160). Ends with an abrupt cut to silence in 0.2-0.3 s at 3:08 (WN 0180: -19 dB, then -41, -57, -66, -81 dB).
6. **Spoken-word sample as lead, not sung.** Vocal stem shows speech formants, bursts of 1-3 s, then silence (MV 0140s vocals panel: bursts about every 1-2 s while a list of place names is read; WN 0000/0040/0140/0160). Whisper detects Dutch (p=1.0). CL voice tag: "radio announcer speech" near 1.0 over the speech windows (but CL says "rapping" 1.0 at 0:00: spurious, no speech there). No melody anywhere: lead_notes tracks speech or bleed (WN 0040, 0100, 0140, 0180).
7. **Loud, wide, compressed ending section.** Mix about -10 to -12 dBFS, width 0.62-0.86 at 3:00-3:07 versus 0.24 at the start (WN 0180, LV). Wide, driving texture rising in width across the track (0.35 at 0:20, 0.5 at 2:15, 0.7 at 3:05).
8. **CL genre vote:** "post-rock" top in 33 of 38 windows, krautrock 2, techno 1, synth-pop 1, rock 1 (own count of CL). CLAP's label set is a closed list I should not trust: "post-rock" scoring 1.0 mostly says "guitar-ish, instrumental, no sung vocals, builds".

## 2. Lineage hypotheses, ranked

### A. Instrumental guitar-and-drums "post-rock" / "cinematic rock" with a sampled voice (high-medium)
Sonic evidence: no sung vocal; layered build and subtraction (fact 5); saturated guitar-like wall; D-pedal harmony with slow modal changes (fact 4); sustained, wide "other" with chug-like fast repeated onsets in the final section (WN 0180: 50 onsets, median gap 0.186 s, i.e. sixteenth-note repetition at 78 BPM); loudness swells (0:43-0:57 "other" +10 dB, WN 0040; "other" step +5-7 dB at 2:13, WN 0120). This is the classic post-rock and instrumental-rock grammar (crescendo, plateau, dropout, re-entry), plus the particular British-instrumental-rock habit of using archive speech in place of vocals. I cannot show it is guitar-based rather than synth-based (low confidence on instrument, medium-high on the gesture).

### B. Motorik / krautrock-derived drive (medium)
Evidence: relentless, unvarying pulse; repetition over a pedal; gradual layering with the groove never changing (fact 1, 5); static harmony. The drum density (4.5 onsets/s, fully steady across 3 minutes, own) fits a locked, trance-inducing pattern. Against it: the motorik signature is a straight 4/4 with an eighth-note hat and snare on 2 and 4 at 120-160 BPM. Here the hat band is nearly empty (fact 2) and I cannot confirm a snare-on-2-and-4 backbeat; the felt tempo may be 156, which would put it in motorik range (undecided; ask rhythm). CL gives krautrock only 2 top wins. Verdict: shares the hypnotic, locked-groove idea, not proven to share the beat.

### C. Electronic / drum-machine rock hybrid (medium)
Evidence: BT regularity (2.4% s.d.); CL "drum machine" top in 12 windows; dry, low-weighted drum stem with minimal cymbal wash; broadband hits repeated identically in MV 0140s (the comb looks near-identical bar to bar, though a looped sample or a very tight drummer would both do this). Suggests a programmed or sample-triggered drum part under a guitar band, the way electronic-leaning rock acts work. Also the sudden whole-mix cuts (2:47.8, 3:08) and drops that remove bass entirely are editing-like arrangement moves (stems silent, not just quiet) rather than a band stopping naturally, which is a production-led, sampler-and-DAW trait (medium-low: I only see stem silence, and demucs can zero a quiet stem).

### D. Documentary / archival sample-collage tradition (medium-high on the device)
Evidence: spoken announcer-style Dutch, factual content (date "18 januari 1963", temperature "16 degrees below zero", "more than 200 kilometres", Frisian place names, "that is the Elfstedentocht": WN 0000, 0040, 0140, 0160), placed on top of the mix without ducking, short clipped bursts, narrow-band speech with broadband 8 kHz energy (WN 0140). This is the same tradition as sound-collage and found-voice music (musique-concrete in spirit; spoken-word archive over rock). It is also a documentary-score tradition: the music accompanies a told story. Whether the recording is archival or newly recorded and filtered is not measurable (low). This hypothesis is about the voice device, and should not be read as a claim about identity or source.

### E. Classic rock / stadium rock, metal, techno, pop (low)
- **Not metal:** no double-kick density, no palm-muted low riffs identified, no tritone riffing; drum low-end heavy but sparse (4.5 onsets/s).
- **Not techno:** tempo about 78 or 156 and a heavy, saturated guitar-like wall do not suit it; CL "techno" top in one window only.
- **Not pop / song form:** no verse-chorus, no sung melody, no repeating hook found (WN passim). Chord loop of 8 beats repeats, but with no topline.
- **Not blues/funk/hip hop:** pedal and modal drone harmony, no swing or syncopated bass groove measured; the bass is held low notes, not a riff.
- **Hip hop:** CL "rapping" 1.0 at 0:00-0:05 is spurious (no vocal then). The speech-over-beat shape can resemble rap-adjacent sample use, but there is no flow-like rhythmic alignment (WN 0060: speech not rhythmically locked to the drums), so low.

## 3. Fit with the 20 s windows (timeline of the lineage story)
- 0:00-0:40: electronic-tinged, krautrock-like layering start: drums alone, then bed, then bass; archival voice announces date and time. Documentary frame, pulse not yet "rock".
- 0:40-1:15: build and plateau; "other" swells 10 dB, bass steady (WN 0040, 0060): post-rock crescendo grammar.
- 1:15-1:30: subtraction/breakdown (bass out, thin ringing tones) then spoken list of numbers: sampler-collage moment.
- 1:27-2:00: dense sustained wall, long held notes over drums, 1:58 "other" drops 10 to 15 dB with a rising wash (riser-like, WN 0100): produced, cinematic.
- 2:00-2:48: groove with punctuated bass and chord changes, spoken place names; the most song-like harmony (8-beat loop) in the track; the 2:48 stop is a hard edit-like cut after "that is the Elfstedentocht" (WN 0160).
- 2:48-3:08: wide, loud, driven; fast repeated onsets; wall; abrupt end. The closest to heavy "stadium/post-rock climax" and to repetitive chug.

## 4. What the measurements cannot tell me
- Instrument identities (guitar versus synth, kit versus machine) and therefore any claim of "rock band" versus "electronic production": unresolved.
- Whether the sound is vintage (tape/analogue) or digital: I only see roll-off near 8 kHz in "other" (WN 0180), which suggests a band-limited source or a low-pass in production; that is no era evidence.
- Whether the speech is archival (I only see narrow formants and no hiss: CL "tape hiss"/"vinyl crackle" were never dominant).
- Lineage cannot be fixed by one track: I give traditions it resembles, not a source.

## 5. Overall lineage verdict
An **instrumental, loop-based, drum-led rock/electronic hybrid**: post-rock structural grammar (layering, crescendo, subtraction, wall of saturated guitar-like sound, no sung vocal) built on a motorik-leaning locked pulse and a drone-like D pedal, with a documentary tradition of archival-style spoken Dutch narrating the content. Confidence: high on "instrumental, non-sung, build-and-subtract, spoken-sample device"; medium on "post-rock/cinematic rock" and "motorik-like pulse"; low-medium on "electronic/programmed drums"; low on any specific instrument.

## 6. Three questions for fellow specialists
1. **Rhythm:** is the drum pattern a backbeat (snare on beats 2 and 4 at 156 BPM, motorik-like) or a half-time feel at 78 BPM, and does the pattern vary bar to bar at all (a human would drift; a loop would not)? My drum band split shows a low-weighted, hat-poor pattern at 4.2-4.6 onsets/s.
2. **Sound:** can you tell from spectral shape (harmonic spacing, noise floor, attack) whether the "other" wall is a distorted guitar or a synth, and whether the 8 kHz hard roll-off is a source property or a production filter? That decides "rock band" versus "electronic".
3. **Harmony / form:** does the D-pedal Dm/D/Bm/Am/G/C/F loop (8-beat cycle with Dm anchor at 2:19, 2:25, 2:31) behave as a modal vamp (aeolian or mixolydian) or functional progression, and where does form (sections) actually change, as compared with my build/subtract map at 0:40, 1:15, 1:27, 1:58, 2:13, 2:48?
