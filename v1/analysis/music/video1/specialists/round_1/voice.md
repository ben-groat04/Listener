# video1 (Public Service Broadcasting, "Elfstedentocht Part 1"): VOICE specialist, round 1

Evidence keys: [LV] music_views/per_second_levels.json; [LN] lead_notes.json; [IMG nnnn] music_views/window_nnnns.png (vocals panel); [CLAP] clap_tags.json; [LY] lyrics/whisper_medium_mix_nl_*; [BT] audio_features/beat_times.json; [V1] my script v1/scripts/agents/voice_r1.py (vocals stem, 0.1 s RMS, threshold -42 dBFS); [V2] v1/scripts/agents/voice_r1b.py (band shares, pyin). I cannot hear; everything is inferred from measurements. Timestamps m:ss.

## 1. Headline
There is no singing anywhere. The only human voice is one archival Dutch newsreel narrator, plus (possibly) a few spliced numbers/place-names, used as a spoken sample laid over a loud D-centred rock band. It appears in 26 or so short bursts (about 2 s each) in four clusters, and is absent for the first 9 s, 0:57-1:03, 1:28-1:46, 2:00-2:14, and for good after 2:48 (about 2:20 of the 3:09 contains no voice). Confidence high on presence/absence times, medium on content, low on treatment details.

## 2. Map of the voice (vocals stem > -42 dBFS, [V1], cross-checked with [LV] and [LY])
| Time | Stem peak | What [LY] gives | Role |
|---|---|---|---|
| 0:09.9-0:12.3 | -18 | "18 januari 1963" | date stamp, first words |
| 0:13.6-0:15.8 | -18 | "het staatsmarathon zonder (winnaar)" ("the state marathon without a winner" in the translate pass) | scene-setting |
| 0:17.0-0:18.4 | -20 | "half zes in de ochtend" (6.30 am) | time stamp |
| 0:19.1-0:23.9 | -18 | "200 bezoekers door Friesland, waar alleen de allersterksten..." | longest unbroken sentence |
| 0:24.4-0:31.8 | -17 | "de twaalfde Elfstedentocht... waar iedereen zich voor opmaakt, dat is de Elfstedentocht" (garbled) | statement of the subject |
| 0:41.0-0:42.5 | -16 | "De 12e Elfstedentocht." | a lone repeat of the title phrase |
| 0:50.8-0:56.2 | -15 | "Temperatuur 16 graden beneden 0. Een monstertocht van ruim 200 km" | facts: cold, distance |
| 1:03.5-1:05.7 | -18 | nothing captured | unidentified burst, probably speech [IMG 0060] |
| 1:18.9-1:27.1 | -18 | "575 wedstrijdrijders, rond 9500 toerrijders, Zweden, Canadezen, Zwitsers..." | numbers and nationalities |
| 1:46.6-1:48.4 | -19 | nothing (Whisper only produced "MUZIEK" at 1:42, a hallucination) | interruption in the riff |
| 1:57.1-1:58.3 | -22 | nothing | cue as bass and guitars exit |
| 2:15.0-2:35.9 (about 12 bursts) | -16 to -20 | place-name list: Sloten, Stavoren, Hindeloopen, Workum/Markum, Laaxum, Harlingen, Franeker, Dokkum, Leeuwarden (translate and transcribe passes disagree on spellings) | the checkpoint litany |
| 2:44.3-2:48.2 | -16 | "waar iedereen zich voor opmaakt, dat is de Elfstedentocht" | reprise of the 0:24-0:31 line; last words |

Whisper's "Bedankt voor het kijken" at 3:07 has vocals at -66 dB and no_speech 0.90: a hallucination, ignore (high confidence). The "MUZIEK" at 1:42 is likewise not a voice.

## 3. How it is placed
- **Laid over, not woven in.** Mean levels while the voice is present vs absent (after 0:09) [LV]: mix -12.5 vs -12.3 dBFS, drums -17.9 vs -18.5, other -20.1 vs -18.6, bass -33.8 vs -31.5. So the band does not duck for the speaker: the voice rides above a full-level mix (stem peak 3 to 8 dB below the mix level, [V1] "voc-mix" column; only at 1:19-1:27 is it within 2-3 dB because the mix is quieter there, about -15). Confidence medium-high; demucs stem levels are not a mixing-desk truth.
- **Almost always in the centre**: width falls slightly under speech (0.5 vs 0.6) but at 2:14-2:19 it jumps to about 0.55 as the "other" layer widens, so the voice sits in the middle of a widening picture (medium).
- **Free time against the beat.** I took each burst onset against the 78 bpm beat grid [BT]: phases are scattered (0.02, 0.29, 0.32, 0.42, 0.59, 0.85, 0.96 and so on; bar positions all over). In the final list (2:15-2:35) onsets land at a steady 0.2-0.4 beat phase, i.e. consistently a little after the beat but no more locked than that. Reading: the narrator speaks at newsreel pace, not to the grid; the band keeps the pulse. Low-medium (the 78 bpm grid may be half-time of a driving 156 bpm feel; the tracker's bar position is arbitrary).
- **Entry through gaps.** Several entries follow a subtraction: 1:18.9 right after the bass was cut at 1:15 (win_0060 notes), 2:15 just as an extra layer swells at 2:13 and the chords start moving (Am, D, G), 1:57 as the bass and guitars fall away. The arrangement seems to clear or open a room before the voice; my reading, medium.
- **Phrase length**: about 1.5-2.5 s phrases separated by 0.4-1 s gaps; the 0:19-0:24 and 0:24-0:31 sentences are the longest. In the list section the gaps (2:17, 2:19-2:21, 2:23, 2:26-2:27...) correspond to the pauses between town names.

## 4. Treatment and sound of the voice
- **Band-limited, noisy, archive-like.** Vocal-stem energy shares [V2]: 300 Hz-3 kHz carries 73-88 % in the later bursts (0:19-0:24 80 %; 0:28-0:32 84 %; 2:24-2:36 88 %), under 300 Hz only 4-9 %, above 3 kHz 6-19 %. That is the classic 1960s optical-soundtrack/radio shape (little low end, rolled-off top). Noisy sibilant bursts to about 8 kHz appear in the images [IMG 0100, 0120], but demucs smears band noise into this stem, so some "voice" energy is leakage of guitars/cymbals. High on narrowness, medium on "archival".
- **Pitch.** pyin on the stem gives a median f0 of about 160-195 Hz where voiced (0:19-0:24 160 Hz, 0:51-0:53 176 Hz, 1:19-1:27 163 Hz, 2:24-2:36 196 Hz), voiced fraction only 17-36 %; [LN] shows tiny wandering notes B3-A3-G3 (2:16-2:17.5) that fall at ends of phrases. That is speech intonation of a male speaker (an announcer's falling cadence), not a tune. High that it is not sung. [LN] values in non-speech passages (e.g. D3 repeats 1:51-1:58, 3:00-3:07) are guitar/bass leakage into the vocal stem: do not read them as melody.
- **No obvious effects.** No echo tails appear in the quiet vocal-stem floor: between bursts the stem returns to about -65 dB (only a handful of seconds sit at -41 to -54: 9, 66, 70, 109, 137, 140, 143, 153, 154 s, which are fringes of bursts or leakage). So no long reverb or delay on the voice (medium), no pitch-shifting evidence, no stutter or loop-chopping: each burst is a single contiguous sentence or word. The "chopping" is editorial: phrases are chosen and spaced, not granulated.
- **Repetition.** The one clearly repeated text is "waar iedereen zich voor opmaakt, dat is de Elfstedentocht" (about 0:27-0:32 and 2:44-2:48) and the title phrase "de 12e Elfstedentocht" (0:41). I have not verified that the 2:44 line is the same recording (not a re-cut) as 0:27; levels (-16.5 vs -15.7 peak) and durations (4 s vs 4 s) are similar. Question for sound/form below.

## 5. Words and music answering each other
- **Narrative arc written into the voice distribution.** Opening 0:10-0:56: context (date, hour, crowd, temperature, distance): dense, nearly continuous speech over the intro groove. 1:03-1:27: numbers of competitors (the field). 1:46-2:00: two wordless-to-me interruptions with the riff at its loudest (mix about -10 to -11 at 1:40, win_0100). 2:15-2:36: place names as checkpoints, the song's "journey" passage, which coincides with chord movement (Dm, Am, D, G, Gm, C, F) [win_0120/0140 notes]. 2:44-2:48: the thesis line again, then a stripped moment at about 2:48 and the band wins: the voice never returns, final 20 s instrumental (win_0160/0180 notes).
- **Words as rhythm.** The town list is a spoken ostinato of short, uneven chunks (0.3-1.5 s) that cut across a regular drum pattern; the cross-rhythm may be the most "musical" use of the voice (medium; only phrase times, not syllables, are measured).
- **Speech as lead instrument.** With no singer, the narrator occupies the lead role: stem peak 3-8 dB under the mix, centre, mid-band. The riff is not shaped around the words (chord changes are not locked to phrase starts except loosely at 1:48 Cm/D/Bm during a burst and 2:15). Medium-low.
- **Feeling (interpretation, not measurement).** A flat, factual, historical voice over a relentless guitar-driven groove creates a documentary-with-adrenaline feel: the narrator's calm against the band's urgency. The long absence of voice from 2:48 turns the story from told to felt; the last words restate the subject, then the music carries it alone. CLAP tags "radio announcer speech" (0.66-1.0) agree where speech exists but also fire wrongly at 2:40 (vocals -67 dB) and "no vocals" at 2:30 (speech present), so I give CLAP no weight [win_0140 notes].

## 6. Where I disagree with or tighten the window notes
- win_0000-0020 treat the 0:09-0:56 voice as a sample over the band; supported. I would add that the translate/transcribe passes agree on a clear text only in 0:09-0:56, 1:19-1:27 and the 2:44 line; the rest are guesses.
- win_0100 calls 1:57 "a more sustained, voiced phrase"; pyin cannot confirm (burst is 1.2 s, peak -22 dB, the weakest burst in the track), so I rate it as an unidentified speech or noise event, low confidence.
- win_0120 calls the 2:15 burst a list of towns "from the transcript at 2:21+". [LY] confirms the list from 2:18 (Sloten/Stavoren... ), which matches. 2:15-2:18 words are unverified.

## 7. What measurements cannot tell
Whether the narrator is one person or several; whether the 0:09 and 2:15+ passages come from the same film; whether sentences were edited together (splices are hidden under the band); the actual word content in the 1:03, 1:46 and 1:57 bursts; whether anything is sung at very low level in the "other" stem; how loud the voice feels to a listener (loudness, not stem dB, would need K-weighting).

## 8. Questions for fellow specialists
1. **Sound specialist:** is the 300 Hz-3 kHz concentration (73-88 % of voice-stem energy) plus rolled-off top consistent with a 1960s mono optical track, and does the "other" layer carry a matching band-limited sample (film hiss, crackle) that could be leaking into my vocal stem and exaggerating the 8 kHz noise in the bursts?
2. **Form specialist:** do the voice-free blocks (0:57-1:03, 1:28-1:46, 2:00-2:14, 2:48-3:09) line up with your section boundaries, and is the 2:44 reprise of "dat is de Elfstedentocht" the closing statement of a ternary shape (0:27 / 2:44), or only a coincidence of the film's own script?
3. **Rhythm specialist:** is the true tempo 78 or about 156 bpm, and in your reading do the town-name onsets (2:15-2:36) sit consistently about a quarter-beat after the beat, or is that an artefact of an arbitrary beat grid and my 0.1 s resolution?
