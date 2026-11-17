# video1 (PSB, "Elfstedentocht Part 1"): VOICE specialist, round 3 (final)

Evidence keys: [LV] per_second_levels.json; [LY] lyrics/whisper_medium_mix_nl_transcribe.json; [V3]/[V4] round-2 scripts; [V5] new `v1/scripts/agents/voice_r3.py` (vocal-stem envelope: syllable-like peaks per second, active fraction, pauses of 0.2 s or more, per speech passage); [R2-x]/[R3-x] other specialists' files. I cannot hear; all is inferred from measurement. Rhythm's round-2 file was empty, so I use only what the others quote from rhythm. Times m:ss. British spelling.

## 1. Answers to questions put to me

**Feeling's question: is the narrator's pace constant or does it quicken?** [V5], vocal stem, syllable-like envelope peaks per second (a rough speech-rate proxy):
| Passage | peaks/s | active fraction | pauses of 0.2 s or more |
|---|---|---|---|
| 0:10-0:18 (date, hour) | 4.3 | 0.66 | 2 |
| 0:19-0:31.7 (crowd, the sentence) | 5.1 | 0.77 | 3 |
| 0:51-0:56 (temperature, distance) | 5.4 | 0.80 | 1 |
| 1:19.7-1:27 (riders, nations) | 4.9 | 0.77 | 3 |
| 2:16-2:26.6 (first town run) | 2.7 | 0.51 | 6 |
| 2:26.6-2:36 (single towns) | 2.1 | 0.42 | 6 |
| 2:43.8-2:48.3 (closing sentence) | 4.2 | 0.68 | 2 |
Reading: the narrator speaks at a steady 4 to 5 syllable-peaks a second in every connected sentence from 0:10 to 2:48, with no quickening towards the end (the closing sentence is slightly slower than the middle ones). The town list is the one slow, spaced passage (2 to 3 peaks/s, many pauses): it is a list, not a rush. So Feeling's alternative holds: the music alone carries any build; the voice adds no rising excitement of its own. Confidence: medium-high on the numbers (proxy, not a syllable count); high on "no quickening".

**Sound's and Form's repeat question (is 2:44 the same take as 0:27?).** Unchanged and now reconciled across three tests: waveform cross-correlation 0.09 (Sound), envelope correlation 0.59-0.64 (not above speech-to-speech controls, mine), MFCC subsequence-DTW 0.278 against 0.40-0.54 for other speech (mine, round 2). The transcript gives the same words both times: 0:26.9-0:31.8 "Waar iedereen zich voor op maakt, dat is de Elfstedent[o]cht" and 2:43.8-2:48.3 "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht" [LY]. Same sentence: high. Same take or an edited loop: unresolved, low-medium; the sentence lengths differ (4.9 s against 4.5 s) and the first is preceded by two connected clauses, so it is more likely that the film's own commentary says the line twice, or that it was re-cut, than that a single clip was pasted. Production reading for lineage: a frame (first and last major statement), not a proven loop. The stop at 2:48 is therefore a callback to a line the listener already knows.

**Harmony's confirmations (1:57 and 1:46.6).** Accepted in full [R3-harmony]: the 150 Hz tone appears in all three stems, so 1:57 is the D pedal bleeding, and at 1:46.6-1:48.4 the guitars and bass hold D with a broad noise smear in the vocal stem (the "Cm" is a detector reaction). I therefore remove both from the voice map for good. Note the same applies to Whisper's "MUZIEK" at 1:42.0-1:43.4 [LY]: it is a typical hallucination on music-only audio, and my map has no speech there.

**Rhythm's open point (are the two voice exits at the same bar position?).** Form measured it [R2-form 2.4]: the first exit is on bar 9.99 (a bar line); the second ends at 2:48.1 = bar 54.3, i.e. displaced about 0.3 bar because the band is cut. So the edited-to-grid claim holds for the first exit only. Combined with my beat-phase scatter for the middle of the speech, I settle on: **narration is free in time; the arrangement places entries and exits next to its own section edges, not on beats.** Confidence medium.

## 2. New finding this round and a correction to myself

- **The final "Bedankt voor het kijken!" at 3:07-3:08.5 is a transcription artefact.** [V5]: vocal stem over 3:06.5-3:08.4 has median -65.9 dB, maximum -63.9 dB (the noise floor). Whisper produces this phrase (the sign-off of many web videos) on trailing audio. Nobody should treat it as content. High. It also means the voice-free closing stretch is 2:48.2 to the end of the track (about 20 s), confirmed.
- **My town-list reading, flagged as inference.** Whisper's rendering of the list is garbled ("Sleek, eerst, slotten, staveren", "Markum", "Loftwacht", "Hartingen", "Vranenken", "Dokken", "Leeuwarden"), but several are plausibly the Frisian towns Sneek, IJlst, Sloten, Stavoren, Workum, Harlingen, Franeker, Dokkum, Leeuwarden. If so, they follow the real route order and end at the start town (this is my knowledge of the route, not a measurement; low-medium). Rhythmically this is why the list has a different shape: a single long run of about 10 s (2:16-2:26.6, with Whisper unable to split it, which fits fast, continuous speech with few real gaps) then single names with 0.5-1.4 s gaps. That is a "counting off" structure: speed in the first half, a deliberate reading name by name in the second. This is a refinement of my round-2 "litany": the second half is slower and clearer, which matches Harmony's Am-D-G walk finally leading to the bass's return at 2:38.
- **Level wording stays** (median speech 4 to 5 dB under the band stems, peaks 3 to 8 dB under the mix), and the voice never makes the band duck.

## 3. How my area connects to the others (final)

- **To form and harmony:** voice entries occur into space made by subtraction (1:19 after the bass leaves at 1:15; 2:15 on the Am-D-G walk; 0:09.9 after the drums, wall and bass are in); exits sit at changes of state (0:31.7 on a bar line, 2:48 into the stop). The longest voice-free blocks coincide with the loudest and densest sections (1:27-2:15) and with the sub-stab block (2:01-2:14), so the story is told in the sparser passages and withheld when the band is fully on. Medium-high.
- **To sound:** a narrow-band, dry, centred, noise-free voice (95 % below about 3.7 kHz [R2-sound]) under a wide stereo band: a different time and place inside a modern sound. The cleanliness (no noise bed) means the sample has been cleaned or gated; I cannot say which.
- **To feeling:** the voice is the emotionally neutral layer (flat, falling intonation, steady rate, no performed pitch). Whatever the listener feels comes from the music; the voice supplies fact and context. The one exception is the last syllable inside the 0.4 s hole at 2:47.8: the voice ends, band and guitar hold, the band returns brighter at 2:48.2. Whether that reads as a held breath or a gasp is Feeling's judgement; the measurement is that the word is complete before the return (high).
- **To lineage:** the sample-as-narrator frame (opening statement, closing statement) is the lineage-relevant device. The audio supports "archival-style narration used as lead voice"; it cannot show who recorded it or when. Context for the wording ("waar iedereen zich voor opmaakt") comes from [LY], the language is Dutch, p = 1.00.
- **To rhythm:** no speech-to-grid lock to exploit; the list's chunk lengths (0.4-1.4 s, one 2.4 s) do not fit the 0.38 s or 0.77 s grid. So the voice does not settle the 78 versus 156 bpm question either way.

## 4. What I still cannot tell
One narrator or several; the untranscribed 1:03.5 burst's words; whether the second closing line is a separate take; LUFS; how much the stem separation altered the voice; the true place names (my reading is inference from garbled text).

## 5. Settled conclusions
- **Voice map (high):** speech only at 0:09.9-0:31.7, 0:40.6-0:43, 0:51-0:56, about 1:03.5, 1:19.7-1:27, 2:16-2:36, 2:43.8-2:48.3; the 1:46.6, 1:57, 1:42 "MUZIEK" and 3:07 "Bedankt voor het kijken!" events are not speech (leakage, band bleed or Whisper hallucination).
- **Delivery (medium-high):** one flat, falling, unperformed voice at a steady 4-5 syllable-peaks a second, no quickening, slower and spaced for the town list; free in time against the band and not beat-locked, 4-5 dB under the instruments, which never duck for it.
- **Treatment (high on measurement, medium on era):** dry, centred, band-limited (about 95 % below 3.7 kHz), no noise bed: a clean "archive" texture, not an effected or chopped sample; there is no chopping, pitch-shifting or looping that I can measure.
- **Frame (medium-high on the words, low-medium on the take):** the same sentence opens (0:27) and closes (2:44) the piece; whether it is the same recording is unproven; the first exit lands on a bar line, the last inside the 0.4 s stop.
- **Role (medium):** the voice carries the information and the structure of "what is happening" (date, crowd, cold, riders, route); the band carries all the emotion; entries follow subtractions and the voice is withheld when the band is at full weight.
