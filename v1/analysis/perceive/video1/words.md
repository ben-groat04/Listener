# video1 — the words (Public Service Broadcasting, "Elfstedentocht Part 1", 2013; per context.md, unverified from audio alone)

## Method and limits
- Sources compared: the existing whisper-medium NL transcribe and translate passes on the full mix (`lyrics/`), plus my own faster-whisper medium re-runs on windows (5-40 s, 46-62 s, 72-100 s, 100-135 s, 135-170 s, 170-188 s) with `language=nl`, with and without an initial_prompt of Frisian place names. These passes ran on the full mix, so each hears voice plus loud music (a demucs vocals stem exists at `v1/data/video1/stems_raw/htdemucs/song/vocals.wav` but this pass did not use it). Only "medium" was available offline; large-v3 was not.
- **Provenance:** the only raw outputs committed to the repository are `v1/data/video1/lyrics/whisper_medium_mix_nl_transcribe.{txt,json}` and `whisper_medium_mix_nl_translate.{txt,json}`. My windowed re-runs (with and without initial prompt) were scratch runs, not committed; anything resting only on them is marked "scratch run not committed" and rated no higher than Medium.
- I cannot hear the audio. All text is ASR output corrected by judgement. Timings are whisper segment times, good to roughly +/-1 s (segments are coarse, and the first pass starts a few seconds later than the windowed re-run, e.g. 0:09 vs 0:05 window start).
- Caution on the place-name list: my prompt contained the town names, so a prompted pass could echo them. I therefore rely on (a) the un-prompted first pass, which independently produced garbled versions in the same order, and (b) the frames, where the signs on screen match (OBSERVATION: IJlst sign 2:18, "De Vrouwe van Stavoren" inn 2:24, "Welkom in Workum" 2:27, Bolsward/Boalsert 2:29, Franeker/Frjentsjer 2:32, Dokkum 2:34, Leeuwarden on a signpost 2:35-2:36; sheets 07-08).

## Who is speaking, era, quality
- Only one voice type is evident: a male-sounding Dutch newsreel/documentary NARRATOR (voice-over) reading short factual statements in the clipped, formal style of 1960s Dutch cinema newsreels. INFERENCE from the text register; I cannot hear timbre. No interviewee, no reporter on the ice, no singing detected. Whisper found no sung lyrics: the band's parts appear instrumental (spectrogram-based, medium confidence).
- Era: the 1963 race itself; the commentary was probably recorded or re-used from period film (Fries Film Archief, per context.md). Quality: likely narrow-band, noisy archival mono, which explains the many ASR errors. The 2013 band mixes it over loud music (RMS about 0.2-0.3 almost throughout, dips to about 0.14-0.18 at 1:15-1:26 and 1:58-2:13, which are the places where speech is most audible).
- Structure: speech is sparse and comes in three blocks: the opening facts (0:09-0:32), a temperature/distance pair (0:50-0:56) and entrant numbers (1:16-1:27), then a spoken list of the eleven towns (2:16-2:35), and a reprise of the opening refrain (2:43-2:48).

## Transcript table
Confidence: H = high, used only where a committed file is named in the row (the two committed medium passes agree and the text fits known facts); M = medium (includes anything resting on scratch runs not committed); L = low/guess.

| Time | Original (best reconstruction) | English | Conf. | Notes |
|---|---|---|---|---|
| 0:09-0:12 | "18 januari 1963." | "18 January 1963." | H | Both committed passes agree (`lyrics/whisper_medium_mix_nl_transcribe.txt` 0:09.14, `..._translate.txt` 0:10.20); the word probability of "18" (0.14) is from a scratch run not committed. The date is also confirmed by the race records (see research). |
| 0:12-0:16 | "Het schaatsmarathon zonder weerga." (my reading) | "The skating marathon without equal." | M-L | Passes gave "Het staatsmarathon zonder lieveren" (nl) and "state marathon without a winner" (translate); the windowed re-run gave "schaatsmarathon zonder Leeuwarden". "Schaatsmarathon" is clearly right (skating marathon). "Zonder weerga" (= unequalled) is my guess from the sound pattern "zonder lie-/-weren"; speculation, not verified. Could alternatively be a place name. |
| 0:16-0:18 | "Half zes in de ochtend." | "Half past five in the morning." | M | Dutch "half zes" = 5:30 (not 6:30; the translate pass mis-rendered it as 6.30). Fits a pre-dawn start; word "half" had low probability. Not independently verified. |
| 0:18-0:24 | "Tweehonderd [zoekers / bezoekers / schaatsers?] door een Friesland waar tegen alleen de allersterkste zijn opgewassen." | "Two hundred (km?) ... through a Friesland against which only the very strongest are a match." | L-M | First pass: "bezoekers ... opgepast"; re-run: "zoekers ... opgepast". "Tweehonderd [kilometer] door een Friesland" (200 km through Friesland) is much more plausible than "200 visitors" since the route is about 200 km (research note). "Opgewassen tegen" (= up to the task of) is the idiom and fits "waar tegen alleen de allersterksten opgewassen zijn". Both are INFERENCE. |
| 0:24-0:28 | "[Elf] steden zijn voor de twaalfde Elfstedentocht." (garbled) | "Eleven cities... for the twelfth Elfstedentocht." | L-M | Committed pass: "Stad zijn voor de twaalfde elfste tegenwoord"; the windowed re-run "Stad zijn voor de twaalfde Elfstedentocht" (scratch run not committed). "Elfstedentocht" here is reconstructed from garbled strings plus context (INFERRED). Probably "Elf steden zijn ... voor de twaalfde Elfstedentocht", i.e. the twelfth official tour (1963 was the 12th by count; ties in with the repeated "twaalfde" at 0:40; unverified here). |
| 0:28-0:32 | "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht." | "What everyone is getting ready for: that is the Elfstedentocht." | M | The committed transcribe pass reads the Elfstedentocht word as "Elfstedentuin" here, so that word is reconstructed from garbled strings plus context (INFERRED); the clean reading is at 2:43 (`lyrics/whisper_medium_mix_nl_transcribe.txt`). Same sentence recurs at 2:43-2:48 and 2:44-2:48 (translate pass: "Where everyone has to make a move"; this is a mistranslation of "zich opmaken voor" = to prepare/gear up). The whole-people-waiting-for-it idea is the thematic refrain. |
| 0:40-0:42 | "De twaalfde Elfstedentocht." | "The twelfth Elfstedentocht." | M | First pass "De 12e Elfstedentuin"; re-run "De twaalfde afsteen"; translate "twelfth Elfstevental". The ending is garbled everywhere but "Elfstedentocht" is the only sensible word (reconstructed from garbled strings plus context, INFERRED; committed passes: "Elfstedentuin", "Elfstevental"). no_speech_prob 0.38, so partly masked by music. |
| 0:50-0:53 | "Temperatuur 16 graden beneden 0." | "Temperature 16 degrees below zero." | H | Committed transcribe and translate passes agree (`lyrics/whisper_medium_mix_nl_*.txt`, 0:50.9 and 0:50.6). Research note: later sources give about -18 C at the start, so this is "what the film says". |
| 0:53-0:56 | "Een monsterrit van ruim 200 kilometer." | "A monster ride of more than 200 kilometres." | M | Committed first pass "monsteret", translate "monster ride" (same files). The spelling "monsterrit" is my correction (INFERRED). "Monsterrit" is a real Dutch word (gruelling long trip). |
| 1:16-1:21 | "575 wedstrijdrijders ..." | "575 racing skaters ..." | H | Committed transcribe (1:19.74) and translate ("575 race drivers", 1:19.10) agree on the number (translate wrongly gives "race drivers", but "wedstrijdrijder" = racing skater; in speed skating terms, "rijder" means skater). |
| 1:21-1:27 | "... rond 9500 toerrijders, een aantal Zweden, Canadezen, Zwitsers en Belgen." | "... around 9,500 touring skaters, a number of Swedes, Canadians, Swiss and Belgians." | H (numbers: committed transcribe 1:19.74-1:26.90 and translate), M (nationalities) | The committed first pass gave "Dalmatians" for "Belgen" and the committed translate pass "Dutchmen" and "Belgians"; the windowed re-run (lp -0.29) gave "Belgen" (scratch run not committed). Numbers are consistent with research (about 10,000 starters). "Toerrijders" = recreational/touring skaters. |
| 1:42 | ("MUZIEK") | (nothing) | NON-EVENT (not speech) | The line exists in committed `lyrics/whisper_medium_mix_nl_transcribe.txt` (1:42.00-1:43.40); the no-speech probability 0.75 is from a scratch re-run not committed. This is a typical whisper artefact for music-only passages. Possibly the narration was a subtitle in the original film; do not count as lyric. |
| 2:16-2:21 | "[...] Sneek, [IJlst] ..." | "Sneek, IJlst ..." | L-M | First pass: "Sleek, eerst, slotten"; this fits Sneek, IJlst, Sloten. Timings from the first pass cover 2:16-2:26 as one blurred segment. On screen the IJlst sign appears at 2:18, so the voice (or the visual list) starts about there. |
| ~2:20-2:26 | "Sloten, Stavoren, Hindeloopen (heard: "in de lopen")" | same | M | Voice and frames line up: Stavoren inn at 2:24. |
| 2:26-2:28 | "Workum" (heard: "Markum") | "Workum" | M | "Welkom in Workum" sign at 2:27. |
| 2:29-2:30 | "Bolsward" (heard: "Loftwacht", "Noltswacht") | "Bolsward" | M | Sign "Bolsward/Boalsert" at 2:29. |
| 2:30-2:31 | "Harlingen" (heard: "Hartingen") | "Harlingen" | M | Town view at 2:30. |
| 2:32-2:33 | "Franeker" (heard: "Vranenken", "Vranenkarren") | "Franeker" | M | Franeker/Frjentsjer sign at 2:32. |
| 2:33-2:34 | "Dokkum" (heard: "Dokken") | "Dokkum" | M | Committed passes heard "Dokken"; Dokkum sign at 2:34. |
| 2:34-2:35 | "Leeuwarden" | "Leeuwarden" | H | Committed transcribe (2:34.72) and translate (2:38.32) both give "Leeuwarden". Completes the loop. |
| 2:43-2:48 | "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht." | "What everyone is getting ready for: that is the Elfstedentocht." | H | Committed transcribe 2:43.78-2:48.28 gives "Elfstedentocht" literally (`lyrics/whisper_medium_mix_nl_transcribe.txt`). Refrain from 0:28; second time it ends the film's spoken content. |
| 3:07 | ("Bedankt voor het kijken!") | ("Thanks for watching!") | NON-EVENT (hallucination) | Line in committed `lyrics/whisper_medium_mix_nl_transcribe.txt` (3:07.06); no_speech_prob 0.93-0.94 on 3 passes is from scratch runs not committed. This is a known whisper artefact from YouTube-trained data over quiet or music-only audio. Not in the video. Ignore. |

Other tokens never found: no other words were detected between 0:56 and 1:16, 1:27 and 2:16 (apart from "MUZIEK"), or 2:48 and the end. These stretches are probably music with perhaps quiet voice, which I cannot rule out given the loud mix; a vocal-stem pass would settle this.

## Corrections of the earlier transcripts
- "Het staatsmarathon zonder lieveren" -> "Het schaatsmarathon zonder [weerga?]" (low confidence on last word).
- "Tweehonderd bezoekers" -> probably "tweehonderd kilometer" or "zoekers" garble (inference).
- "Dalmatians" / "Dutchmen" -> "Belgen" (Belgians).
- "Dutch: Elfstedentuin / Elfstevental" -> Elfstedentocht.
- "race drivers" (translate pass) -> racing skaters.
- "6.30" (translate pass) -> "half zes" = 5:30.
- Garbled town names -> the eleven Frisian towns, matched against on-screen signs.
- "Bedankt voor het kijken", "MUZIEK" -> not speech.

## Phrases carrying emotional or thematic weight (INTERPRETATION)
1. "18 januari 1963": a date said like a title; a Dutch listener hears "de Hel van '63".
2. "Half zes in de ochtend", "Temperatuur 16 graden beneden 0": cold, dark, dread, set in the flat tone of a bulletin. The deadpan statistic is the emotional mechanism: the music has to supply the feeling.
3. "een monsterrit van ruim 200 kilometer": scale and cruelty in one word.
4. "575 wedstrijdrijders, rond 9500 toerrijders": the contrast of a few pros versus thousands of ordinary people; the sense of a mass undertaking.
5. "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht": the national waiting, repeated at 0:28 and 2:43 as a bookend/refrain (the only repeated line, so the nearest the piece has to a chorus).
6. The list of eleven towns (2:16-2:35), delivered like a litany and illustrated by town signs, mapping the route and ending on Leeuwarden, the start/finish. A Frisian viewer will hear a ritual roll-call; a foreigner hears a rhythm of strange names.

## Open items
- Run a vocal stem (demucs) or large-v3 on 0:05-0:35 and 2:15-2:50 to firm up "zonder weerga", "tweehonderd ...", and the town timings.
- Do not treat the narrator's figures as true; they are what the film says.
