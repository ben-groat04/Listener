# video1: the music (blind ears report)

Mode: BLIND. Only audio/feature data, stems, spectrograms and whisper transcripts were used. I cannot play audio, so everything about sound is inferred from measurements. Confidence is tagged H (high), M (medium), L (low). Times are m:ss. Duration 3:08.7.

Scripts: `v1/scripts/agents/blind_music_v1.py`, `blind_music_v2.py`, `blind_music_v3.py`. Outputs: `v1/data/video1/audio_features/extra/blind_music_v2_out.txt`, `blind_music_v3_out.txt`.

## 1. In one paragraph (interpretation, M)

A slow-pulsed, loud, guitar-and-drums-driven instrumental track in the post-rock / cinematic-rock family, built on a long D drone, with a deadpan spoken-word voice (Dutch, delivered like a news announcer or commentator) reading facts over the top. It is not a song with sung lyrics: the "vocal" stem is speech in short bursts. The arrangement works by subtraction and return. Full band, then the bass vanishes (1:16), full band again, then a hard collapse to drums plus a sub-bass drone (1:58), then a re-entry, a last narrated passage, a one-beat gap (2:48), a brightening finale and an abrupt cut-off (3:08). Loudness barely changes; the drama comes from what is removed and added.

## 2. Measured facts (observation)

- Pulse: beat tracker 78.3 BPM, beat period 0.766 s, and an onset-autocorrelation peak at 0.766 s in 10 of 11 sections (H for the pulse). Local-tempo plots jump between 78, 104 and 152 because of octave and subdivision ambiguity. See section 3.
- Key centre: D. D is the strongest pitch class in nearly every section (chroma D = 1.00 in 0:00-1:15, 1:28-1:58 and 2:48-3:08). Whole-song key estimate D major 0.76 vs D minor 0.756, i.e. a tie. Tuning offset +0.05 semitone, so standard A440 (H).
- Loudness is compressed and consistent. Whole-song RMS about -12 dB, short-term loudness 10th to 90th percentile only -15.2 to -10.9 dB, peak 1.009 (at full scale, so possible clipping or hard limiting), crest factor 10 to 14 dB (H). Loud sections are about -11 dB, the "empty" sections only about -15 to -17 dB.
- Mean per-section values (from `ears_sections`, my own re-measure in `blind_music_v2_out.txt`) are quoted below in the structure map.

## 3. Rhythm and tempo (M)

- The strongest, most stable periodicity is 0.766 s (78.3 BPM) and its double 1.533 s (one bar of 2 beats, or half a bar of 4). A 0.395 s peak (about 152 BPM) is also present nearly everywhere. 0.766 / 0.395 = 1.94, so the two are not a clean 2:1; I read 0.395 s as the busy off-beat hi-hat or 8th-note layer that is slightly irregular or swung, not as a separate tempo.
- Octave ambiguity: the music could be felt as a heavy 78 BPM half-time groove or a driving ~156 BPM rock beat. Evidence for the slow reading is that the sub-bass drone notes in the breakdown recur every 6.15 s, which is exactly 8 beats at 0.766 s (bass thumps at 2:01.2, 2:07.3, 2:13.5, ...), a phrase length that fits 78 as the beat. I would call it "78 BPM, felt busy". Confidence M.
- Drum density: onset rate 4.5 to 6.2 per second in most sections, about 3.5 events per beat, so hats or 16th-type patterns are constant. The drum stem is continuous almost the whole track, loudest per-second peaks in the stem plot at about 0.20 to 0.24, with a steady floor around 0.10 to 0.13. It never fully stops except at the cuts listed below (H).
- Cross-rhythm: from 2:39-2:52 the autocorrelation prefers 0.58 s (103.4 BPM), exactly 3/4 of the beat. This is the interval of a dotted-eighth echo or a 3-against-4 figure (L to M). It also shows at 1:06-1:15 (161 BPM, 0.372 s) and 1:49-1:58.
- Drums are "dry but bright" in two layers visible in the drum stem: kick/snare thumps in the bottom (under 200 Hz) plus a flat, broadband hi-hat/cymbal wash that rises above ~6 kHz in the 1:15-1:28 break, the 1:58 area and after 2:48 (spectrogram window images). CLAP labelled the instrument "drum machine" at the start with 0.975, but CLAP labels are unreliable here (it also says "rapping" for speech); I cannot say whether the kit is acoustic or programmed (L).
- The picture does not cut on the beat: only 7.8% of cuts land within 80 ms of a beat, against 19.7% expected by chance (`sync.json`). That is a fact about the edit, not the music, but it tells me the musical pulse is not being used as a cutting grid.

## 4. Instrumentation, with evidence

| Element | Evidence | Confidence |
|---|---|---|
| Drum kit or drum-machine pattern, continuous | Drums stem has transients on almost every beat and subdivision across the whole track; `onset` 4.5 to 6.2 per second; high crest | H that drums are present, L on acoustic vs programmed |
| Sustained synth or processed-guitar bed ("other" stem) | Horizontal harmonic lines in the "other" stem and mix from 0:01.3 onward (window 0:00 image); it carries chord changes between D, G, C, Dm, Gm | M |
| Distorted electric guitar riff layers | CLAP picks "distorted guitar" at 0:30-0:50 and 1:45-2:00 with 0.6 to 0.85 confidence; spectral centroid 1.5 to 3 kHz, heavy mid-band 200 to 3000 Hz energy in 15-66 and 88-109 | L to M (the tagger is easily misled; the sound is guitar-like or synth-like) |
| Bass guitar or synth bass, around 60 to 200 Hz | Bass stem active from about 0:04, strongest (mean 0.113, 0.105) in 15-66 and 66-76; band energy 60-200 Hz is the loudest band in every section | H that a bass line exists |
| Pure sub-bass sine tone at about 43 Hz (about F1) | Four to six isolated ~2.4 s notes in 1:58-2:38; measured peak at 43.1 Hz at 2:01, 2:07 and 2:13 (bin resolution 2.7 Hz), no overtones, in the bass stem only | H that it exists, M on the note (F) |
| Spoken male-sounding voice (not singing) | Vocal stem shows formant bands in short, speech-length bursts with gaps (0:09-0:13, 0:14-0:16, 0:17-0:32 etc.), no sustained pitch, Dutch transcript of announcer-style statements | H that it is speech; M on "male" and "announcer style" (I only infer from register and cadence) |
| Brass | CLAP says brass at 0:15 and 2:45 (0.66 to 0.999). Lead-note tracker shows isolated mid notes (MIDI 55 to 72) with no sustained horn-like lines I could separate | L, probably a mislabel of bright guitar or synth |
| Sampled crowd or atmosphere | No evidence beyond the opening 0:00 to 0:01 | none |

Lead melody: the lead-note tracker finds only sparse, short notes (a few per ten seconds, MIDI 47 to 72, i.e. mid-to-low register). This music is riff-and-texture led, not tune-led (M). There is no evidence of a sung hook.

## 5. Harmony (L to M)

- Chord recognition over the whole track (time share): D 94 s, Dm 33 s, G 13 s, C 11 s, Am 6 s, Bm 5.5 s, Gm 3 s, F 2 s. The track lives on D with the neighbours G and C (a D mixolydian or "D with flat-seven" colouring: C natural beside a D chord, instead of C sharp).
- Third of D is ambiguous: F-sharp and F natural are both weak (about 0.4 to 0.5 relative) and the recogniser flips between D and Dm. Most likely open fifths or power-chord guitars and drones that leave the third unplayed or smeared (M for "the third is undefined"; this is a reason it feels neither plainly bright nor plainly sad).
- Section 2:14-2:38 pivots: chroma strongest at A, then F, B, G, local key estimate A minor (0.60, 120-150 s window) with F major second. A move from a D centre to an A / F area (a "lift" via the relative minor and subdominant side). Confidence L to M. The F sub-bass drone (43 Hz) before it hints at an F flat-sixth colour against D.
- Sections 1:16-1:28 and 1:58-2:14 have flat chroma (percussion and noise dominate, harmonic/percussive ratio of -2.3 dB and -1.1 dB vs +4.6 to +7.9 dB elsewhere): this is where tonal content is stripped to rhythm.

## 6. Structure map (my own, timestamps approximate to about +/-2 s unless noted)

Auto sections from the toolkit (C, B, D, A, B, B, A, A, E, B) were a starting point; I adjusted boundaries using the stems, loudness and spectrogram.

| Time | What happens (observation) | Role (interpretation) | Conf |
|---|---|---|---|
| 0:00-0:01 | First sound at 0:00.7: a hard hit with ringing wide-band tail, level jumps from -67 dB to about -15 dB in one second | Cold start; no fade-in | H |
| 0:01-0:09 | Drums and a harmonic bed (other stem enters at 0:01.3), bass creeps in about 0:04-0:06; D drone. Loudness -14 dB, narrow stereo (L/R correlation 0.82). No voice. | Intro and groove-establishing | H |
| 0:09-0:33 | Speech bursts: 0:09-0:13, 0:14-0:16, 0:17-0:32. Band reaches full weight (bass 0.11, loudness -12 dB). Chords D, G, C, Dm. | Verse-like first narration; the music is already full, the voice sits on top | H |
| 0:33-0:40 | Voice stops; the groove carries on, bass strong | Instrumental gap | H |
| 0:40-0:57 | Two short speech phrases (0:40-0:43 "twelfth Elfstedentocht", 0:50-0:56 "16 degrees below zero ... 200 km"). Loudness -13 to -12 dB. | Second narration block | H |
| 0:57-1:06 | No voice, "other" stem rising (0.12 vs 0.08 earlier), loudness -11 dB | Build | M |
| 1:06-1:16 | Stereo widest so far (corr 0.42), brightness up (centroid about 2.7 kHz vs 1.8 kHz), loudest steady stretch (-11 dB), beat tracker pulse breaks into faster 161 BPM subdivisions | Build to a peak | H |
| 1:15.6-1:28 | Sudden fall of about 4 to 6 dB (-11 to -17 dB). Bass stem is silent for the whole 12 s; drums continue; "other" becomes thin with long sustained high lines; chroma flat (percussive). Voice at 1:19-1:27 reads the entry figures ("575 ... 9500 ..."). | First drop / break; the music steps back so the numbers stand out | H on the drop, M on purpose |
| 1:28-1:49 | Return of the full band: bass returns (0.045 mean, partial), loudness -13 to -10 dB. Mostly no voice. Chord D. | Release; first "payoff" | H |
| 1:49-1:57 | Loudest stretch of the whole track (peak at 1:52, per-second maximum), but the spectral centroid sinks to about 1.0 kHz at 1:49-1:56: the sound is darkened or filtered down while still loud | Tension build by filtering (a "closing the filter" move) | M |
| 1:58-2:00 | Level collapse to -19/-21 dB. Three near-silent instants below -30 dB at 1:58.4, 1:59.2 and 2:00.0 | A hard stop | H |
| 2:00-2:14 | Drums with sparse hits; four repeating 43 Hz sub-bass notes at 2:01, 2:07, 2:13.5 (every 8 beats); stereo narrow again (corr 0.84); chroma flat then D/Dm/Am | Breakdown / sparse middle-eight | H |
| 2:14-2:38 | Bass and "other" return (loudness back to -12.4 dB), brighter (mean centroid up, 3-8 kHz bands rise). Speech from 2:16 to 2:35 is a list of short single words with pauses (place-name-like: transcribed as "Sloten, Staveren, Hindelopen, Markum/Workum, Loftwacht/Noltswacht, Hartingen, Vranenken, Dokken, Leeuwarden", the two transcripts disagreeing on several, so spellings are unreliable). Bass tonic moves toward A / F. | Second main section, brighter, with a rhythmic roll-call | H on the speech form, M on musical role |
| 2:38-2:48 | Sudden darkening (centroid falls to about 1.2-1.5 kHz, a clear step at 2:38) and then a final phrase 2:43.8-2:48.3 ("where everybody is getting ready, that is the Elfstedentocht"). The 0.58 s cross-pulse becomes dominant here. | Closing statement | H |
| 2:47.8-2:48.2 | A complete drop-out of drums, bass and everything for about 0.4 s (dark column in the spectrogram) right after the last word | A held breath before the finale | H |
| 2:48-3:08 | No voice, brightest, widest part of the track (S/M -2.8 dB, L/R correlation 0.31). Centroid rises steadily from about 1.7 kHz to 3 kHz+ at 3:00-3:07, i.e. a gradual opening of the sound. Loudness -11.5 dB. | Finale; the biggest, widest sound | H |
| 3:07.5-3:08.7 | Loud to silence in about a second, with a last-moment drop (-10 to -23 dB then -64 dB); the loudness at 3:07 is still -10 dB | Hard cut or very short fade, not a natural decay | H |

(A whisper "3:07 Bedankt voor het kijken" is a hallucination: the vocal stem is silent there. A "MUZIEK" line at 1:42 is likewise not speech: the vocal stem is near 0.00 at 1:40-1:45.)

## 7. Emotional arc (interpretation, M)

Starts abruptly and mechanically (0:00), settles into a steady, pushing, marching feel (0:09-1:15) where the voice recites facts. The build at 1:06-1:15 is the first lift. The sudden hollow at 1:16 is where the feeling changes from "marching" to "waiting": the bass has gone and the voice counts people (1:19-1:27). Release at 1:28, then the sound darkens and swells (1:49-1:57) and falls off a cliff (1:58). The breakdown (2:00-2:14) is the coldest part: narrow, sparse, a single low note repeating every eight beats, like a distant pulse (M, my image). The re-entry at 2:14 is brighter and carries the roll-call of names; the short darkening at 2:38 and the half-second hole at 2:48 make the finale feel earned. The last twenty seconds are the most open and widest, and the abrupt cut-off at 3:08 withholds a resolution (the listener is left mid-motion). Net mood: determined, cold-but-driving, with moments of awe; nostalgia or archival feel comes from the announcer-style voice and the narrow, dry opening, not from the harmony (M, interpretive).

CLAP mood tags, for what they are worth: hopeful then triumphant (0:00-0:30), nostalgic (0:45-1:50), tense at 2:00, triumphant 2:15-2:45, aggressive at 3:00. This broadly agrees with my arc but is a tagger, not evidence.

## 8. How the music frames the words

- The voice is never louder than the band, and there is no ducking: during speech 0:19-0:31 the mix level is -12 to -11 dB, the same as before and after (H). The music is not stepping aside for the voice; the voice sits in the 500 Hz to 3 kHz gap above the bass.
- Speech is placed around the form: three blocks in the first 60 s, one block in the thinned break (1:19-1:27: the only place where music is clearly cleared away for the words, 4 to 6 dB quieter, no bass), a roll-call over the re-entry (2:16-2:35), and a final line over the closing darkening (2:44-2:48). There is no voice at all in the two biggest stretches (1:28-1:58 and 2:48-3:08): the words fall silent when the band is at its biggest (H).
- Where the transcript is wrong: whisper's Dutch transcription is much better than its "translation". The statements are about a date (18 January 1963), a race beginning at "half past six in the morning" (0:16-0:18), about 200 participants and a "free"/"Friesland" setting, "16 degrees below zero" and "over 200 kilometres" (0:50-0:56), and "575 competitors, about 9,500 tour riders" from several countries (1:19-1:27). The sentence at 0:19-0:31 is garbled (the Dutch version says "Friesland where only the strongest are spared" and "the twelfth Elfstedentocht"). "Elfsteden-" is whisper's rendering of a single word; spoken repeatedly at 0:31, 0:40 and 2:48. The place-name list 2:21-2:39 is only partly reliable. I am judging these only from the transcription and sound, not from outside knowledge. Confidence on the gist is M, on exact words L.
- Voice character: flat, measured, newsreel cadence; short sentences with gaps; the first block (0:09-0:32) has six phrases of 2 to 5 seconds each.

## 9. Moments a listener would remember (ranked)

1. 1:58 collapse into near-silence and the low drone notes every ~6 s (H, the most dramatic change in the whole track).
2. 1:16 bass vanishing while drums carry on, with the figures being read (H).
3. 2:48 half-second total gap after "...Elfstedentocht", then the finale opening up (H).
4. The abrupt end at 3:08 (H).
5. The roll-call of single words over the returning band at 2:16-2:35 (M).
6. The cold start at 0:00.7 with no fade-in (H).
7. The darkening and then re-brightening of the sound (1:49-1:57, 2:38, 2:48-3:07), done as filter-like sweeps rather than level changes (M).

## 10. Stereo and mix (H)

L/R correlation: 0.82 (intro) -> 0.74 -> 0.61 -> 0.42 (1:06-1:16) -> 0.63 (break) -> 0.40 (1:28-1:49) -> 0.84 (breakdown, nearly mono) -> 0.60 -> 0.52 -> 0.31 (finale). The soundstage narrows when the music empties and opens as it fills, widest in the closing minute. Band balance: bass band (60-200 Hz) dominates every section at 46 to 53 dB, with the 3-8 kHz band lifting by about 4 dB and the 8 kHz+ air band by about 6 dB in the finale and in 1:06-1:16 (brighter, more cymbal and hiss energy).

## 11. Things I could not determine

Whether the drums are real or programmed; whether the lead is guitar, synth or something else; exact chord quality (D vs Dm); whether the voice is a recording of a historical announcer or a modern read (the sound is dry and narrow in the opening; I cannot tell). I did not identify the track or artist and did not look for them.
