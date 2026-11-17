# video1: the words (blind mode)

Sources compared: whisper medium on the mix (Dutch transcribe and Dutch-to-English translate, in `lyrics/`), plus my own faster-whisper **large-v3** run (language forced to nl; auto-detect on the medium run already gave nl, p=1.00) on the separated vocals stem `stems_raw/htdemucs/song/vocals.wav` (VAD on, three windows 0-60, 60-120, 120-189 s). On-screen text was read from contact sheets and used to check names. I cannot hear the audio; confidence is inferred from agreement between runs, log-probabilities (large-v3 about -0.18 to -0.40) and on-screen evidence.

## Language and speaker
- **Language: Dutch.** Both runs agree; the on-screen signs (Leeuwarder Courant, Friese Koerier, "Welkom in Workum", "Franeker / Frjentsjer", "Bolsward / Boalsert", "Dokkum") are Dutch and Frisian.
- **Speaker: a single voiceover narrator** (OBSERVATION: one continuous register of speech with no visible speaking person on screen during it; INTERPRETATION: formal newsreel-style commentary). Gender not established from the data. No singing: the transcripts contain only spoken prose and a list of place names. No sync-sound speech is transcribed.
- **A man speaks into a handheld microphone on screen at 0:58-1:00** (a reporter or commentator in a hat, in a crowd). The vocals stem is silent there (about 0.001 loudness), so nothing is recoverable from his speech. Do not attribute any transcript line to him.
- **Era and quality (INTERPRETATION, supported by the spoken date "18 januari 1963" and black-and-white, grainy footage):** early-1960s Dutch newsreel or documentary. The commentary is clean and close-miked, probably recorded separately in a studio and laid over the film. The vocals stem is loud only in short bursts, with silent gaps between phrases (see below). The mixed music is not part of this task.

## Transcript
Time is in m:ss (from large-v3 on the vocals stem unless noted). Confidence: H = both runs agree and the sense is clear; M = sense clear but wording differs between runs; L = guess.

| Time | Original (Dutch, best reading) | English | Conf. | Notes |
|---|---|---|---|---|
| 0:09.8-0:12.0 | "18 januari 1963." | "18 January 1963." | H | Date; first speech in the film. Medium: "18 januari 1963". |
| 0:13.6-0:15.6 | "Een schaatsmarathon zonder weerga." | "A skating marathon without equal." | M | Large-v3 wrote "zonder weer"; medium "Het staatsmarathon zonder lieveren". "Zonder weerga" (unequalled) is my correction; medium-translate "without a winner" is wrong. |
| 0:16.7-0:18.2 | "Half zes in de ochtend." | "Half past five in the morning." | H | Dutch "half zes" = 5:30. Medium-translate "6.30" is a mistranslation. Matches the dark, floodlit opening shots. |
| 0:19.0-0:23.8 | "Tweehonderd kilometer door een Friesland waartegen alleen de allersterksten zijn opgewassen." | "Two hundred kilometres through a Friesland that only the very strongest are a match for." | M | Large-v3 "200 kilometer ... zijn opgevassen"; medium "Tweehonderd bezoekers" (wrong, "kilometer" fits the later "ruim 200 kilometer"). "opgevassen/opgepast" are mishearings of "opgewassen". |
| 0:24.5-0:26.6 | "[Klaar/Gestart?] voor de twaalfde Elfstedentocht." | "[Ready/Starting?] for the twelfth Elfstedentocht." | L (opening words), H (rest) | Large-v3 "Standzijd", medium "Stad zijn". First word(s) unclear; I will not choose one with certainty. "Twaalfde Elfstedentocht" is clear in all runs. |
| 0:27.7-0:31.5 | "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht." | "What everyone is preparing for: that is the Elfstedentocht." | H | Medium "Elfstedentuin" is a mishearing; "tocht" = tour/ride. This line is repeated near the end. |
| 0:41.0-0:42.4 | "De twaalfde Elfstedentocht." | "The twelfth Elfstedentocht." | H | Short, isolated, almost like a title card spoken. |
| 0:50.9-0:53.1 | "Temperatuur: 16 graden beneden nul." | "Temperature: 16 degrees below zero." | H | Large-v3 "beneden door" is a mishearing; medium "beneden 0" agrees. |
| 0:53.9-0:56.0 | "Een monsterrit van ruim 200 kilometer." | "A monster ride of well over 200 kilometres." | H | Large-v3 and medium-translate agree. |
| 1:03.7-1:27 (stem active about 1:04-1:05 and 1:17-1:24) | "575 wedstrijdrijders, rond 9500 toerrijders, een aantal Zweden, Canadezen, Zwitsers en Belgen." | "575 competition skaters, about 9,500 tour skaters, a number of Swedes, Canadians, Swiss and Belgians." | M | Large-v3 gives a single segment 1:03.7-1:27.0 (VAD merged it; the vocals loudness suggests the number-phrase lands around 1:04 and the rest around 1:17-1:24). Medium put the whole sentence at 1:19.7-1:26.9; I trust the stem energy and medium for placement. "Dalmatians" in medium is a clear hallucination; "Belgen" fits translate. Numbers are consistent across runs. "Rond/ruim" for 9,500 uncertain. |
| 1:34.8-2:32.4 (see place list) | place names | place names | M | See next block. |
| 2:43.8-2:48.3 | "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht." | "What everyone is preparing for: that is the Elfstedentocht." | H | Final line, repeating the 0:27 line. Large-v3 garbled it ("Je reet zich bijvoorbeeld maakt"); medium has it correctly. Large-v3 times (2:32.9-2:48) are a merged segment; medium's 2:43.8-2:48.3 is the likelier placement. |

### The list of towns (roughly 2:14-2:35, i.e. 134-155 s)
Both runs are poor on these names; medium gave better individual timestamps, matched to road signs shown on screen at the same moments. My corrected reading, which is an INTERPRETATION built from the signs I can see plus the garbled whispers:

| Time (m:ss) | Heard (whisper) | Corrected | On screen at that time (observation) |
|---|---|---|---|
| 2:16-2:26 | "Sleek, eerst, slotten, Staveren, in de lopen" (medium); "Sneek, Elst, Sloten, Staveren, Hindenlopen" (large-v3) | Sneek, IJlst, Sloten, Stavoren, Hindeloopen | Inn facade "...vrouwe van Stavoren" (2:24-2:25), helicopter (2:26), people on ice. Place names appear to be spoken as a quick run. |
| 2:26.6 | "Markum" / "Warkum" | Workum | Sign "Welkom in Workum" (2:27-2:28). Strong match. |
| 2:29.1 | "Loftwacht" / "Noltswacht" / "Walswat" | Bolsward | Sign "Bolsward / Boalsert" (2:29). Strong match. |
| 2:30.7 | "Hartingen" | Harlingen | Harbour-town skyline (2:30). |
| 2:32.2 | "Vranenken" / "Vranenkarren" | Franeker | Sign "Franeker / Frjentsjer" (2:32-2:33). Strong match. |
| 2:33.6 | "Dokken" | Dokkum | Sign "Dokkum" with 50 km/h (2:34). Strong match. |
| 2:34.7 | "Leeuwarden" | Leeuwarden | Signpost listing Dokkum and Leeuwarden (2:35-2:36). |

Large-v3 also output "Prager" after "Hardinger" (about 2:32), which I treat as a hallucination for "Franeker/Dokkum". The place names are spoken faster and quieter than the narration. I do not claim Hindeloopen/Sneek/IJlst/Sloten/Stavoren with high certainty: the Frisian town names are consistent with the Dutch eleven-city route as a pattern, but I only have written sign evidence for Workum, Bolsward, Franeker, Dokkum, Leeuwarden.

## Hallucinations to ignore
- Medium mix transcript 1:42 "MUZIEK" and 3:07 "Bedankt voor het kijken!" ("Thanks for watching"): there is no speech at those moments (vocals stem near zero), and the second is the standard whisper phantom phrase.
- Medium "Elfstedentuin", "Dalmatians", "Dalmatians/Zweden" confusion, "Tweehonderd bezoekers": errors, corrected above.
- The vocals stem shows small bursts at about 1:47-1:48, 1:56, 2:14, 2:20 and 2:24-2:27 (loudness 0.04-0.11) which no transcript captures as speech; they may be the town-name run, vocal-like music or noise leaking through separation. Not transcribed.

## Silence and pacing (OBSERVATION from the vocals stem)
Speech occurs in short bursts: 0:09-0:15, 0:17-0:23, 0:25-0:31, about 0:42, 0:51-0:56, about 1:04-1:05, 1:17-1:24, then sparse bursts to about 2:34, and a closing phrase near 2:43-2:48. Long silent stretches (0:32-0:40, 0:57-1:03, 1:25-1:45 and from 2:50 to the end at 3:08) leave room for music and picture.

## On-screen text that adds to the words (observation, read from frames)
- 0:04-0:06 newspaper "Leeuwarder Courant: Elfstedentocht op vrijdag"
- 0:09-0:11 newspaper "Friese Koerier: Elfstedentocht bovenmenselijk zwaar"
- 0:23-0:26 "Leeuwarder Courant... Elfstedentocht: zwaar, zwaar, zwaar. Tal van uitvallers en vele gewonden"
- about 2:57-2:58 headline fragment "zwaar, zwaar, zw..."
- about 2:48 banner "FINISH"; 3:07 banner reading roughly "...Reportage ELFSTEDENTOCHT" (partly cut off).
The newspapers state the same theme as the narration: the event is brutally hard. The date 18 January 1963 is stated only in speech.

## Phrases carrying emotional or thematic weight (INTERPRETATION)
1. "Een schaatsmarathon zonder weerga" (0:13) and "een monsterrit van ruim 200 kilometer" (0:54): scale and superlatives.
2. "Waar tegen alleen de allersterksten zijn opgewassen" (0:19): only the strongest survive; sets endurance and ordeal as the theme. Fits newspaper "zwaar, zwaar, zwaar... uitvallers en vele gewonden".
3. "Temperatuur 16 graden beneden nul" (0:51): bare statement of extremity, cold.
4. "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht" (0:27, 2:44): the repeated refrain; collective anticipation, the whole country preparing. It frames the film as a circle: it opens and closes on the same line.
5. The numbers (575, 9,500, nationalities): a sense of a mass, almost national event with international participants.
6. The run of town names (2:16-2:35): the route as a litany or journey, with the road signs supplying the places visually.

## Caveats
Whisper was run on CPU with machine load from other jobs; I did not re-run the town-name window at finer resolution. Corrections of Dutch words are from my own knowledge of Dutch and marked where uncertain. No context file or prior analysis was consulted.
