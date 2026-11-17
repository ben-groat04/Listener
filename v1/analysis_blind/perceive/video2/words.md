# video2: the words (blind mode)

Sources compared: whisper medium (mix, forced Dutch), medium translate, medium on isolated vocals (auto-detect, wrongly chose Welsh at p=0.57), small (mix, auto, wrongly chose English). I re-ran medium on the Demucs vocals stem and on the mix in short windows (Dutch forced, plus auto/English for the late section). Language is clearly **Dutch** (forced-Dutch runs on the vocals stem gave p=1.0 and coherent sentences). The Welsh and English output is hallucination from mis-detected language and should be ignored. I cannot hear the audio; this is transcription by model, corrected by judgement.

## Who speaks, when, and recording quality
- 0:41 to ~2:36: a single **male narrator** in the classic newsreel/documentary voice-over style (OBSERVATION: continuous clean declamatory speech with gaps, no overlapping voices; INTERPRETATION: a cinema newsreel commentary, mid-20th-century Dutch, because the content gives a date, 1963). Medium confidence on the era from the date given in the narration itself; speech style supports it.
- The narration comes in four bursts (stem loudness shows vocals at ~0:41-0:54, 0:58-1:09, 1:20-1:28, 1:49-1:56, 2:25-2:36), separated by music and archive footage with no speech.
- Quality: whisper reads the narration cleanly on the isolated vocals but the mix transcripts drop or garble parts, which fits a recording with limited bandwidth that has been laid over a modern score (INTERPRETATION: the narration looks like an old archive recording mixed into a newly made track). No interview, no reporter at the scene, no crowd speech was transcribed.
- From ~3:25 onward there is **no narration**. The short fragments are chopped vocal-like snippets inside the music (see below); the singer/voice identity is unknown.

## Table (time, original Dutch, English, confidence, notes)

| Time | Original (best reading) | English | Confidence | Notes |
|---|---|---|---|---|
| 0:28 | (MUZIEK, whisper tag only) | (music) | high | no words; music only |
| 0:41-0:45 | "18 januari 1963." | "18 January 1963." | high | all four transcripts agree; narration opens with the date. Sets the time and the event as a historical record |
| 0:50-0:54 | "Een schaatsmarathon zonder weerga" | "A skating marathon without equal" | medium | mix: "schaatsmarathon zonder weg(en)"; vocals: "zonder weer/wegen". "Weerga" (unmatched) is my reading as the most idiomatic fit; the exact last word is uncertain |
| 0:58-1:01 | "Half zes in de ochtend" | "Half past five in the morning" (Dutch "half zes" = 5:30) | low-medium | variants: "6.30 in the morning" (translate), "in de orde" (vocals), "afternoon" (small). "Ochtend" is a guess from "in de o..." plus dawn-start context; I did not verify against the picture |
| 1:04-1:10 | "Tweehonderd kilometer door een Friesland waar tegen alleen de allersterksten zijn opgewassen" | "Two hundred kilometres through a Friesland [province] against which only the very strongest are a match" | medium | stem transcript reads "allersterkste zijn opgepast"; "opgewassen" (up to the task) is the likely word. Translate model said "frieze" and "free-slot" in other runs; they are errors for "Friesland" |
| 1:20-1:22 | "Staat nu voor de twaalfde Elfstedentocht" (uncertain) | "[It] stands before the twelfth Elfstedentocht" (Eleven Cities Tour) | low-medium | mix: "Stort zijn voor de twaalfde elfsteen vluit"; vocals: "Stad zijn voor de twaalfde Elfstedelkort/Elfstedentort". Number "twaalfde" (twelfth) and "Elfsteden-" (eleven cities) are consistent; the verb phrase is not secure. "Elfstedentocht" is my correction of garbled "Elfsteenvluit/Elfstedentort" |
| 1:24-1:28 | "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht." | "What everyone is preparing for: that is the Elfstedentocht." | high for first half, medium for last word | repeated identically across mix and stem runs |
| 1:49-1:56 | "Temperatuur 16 graden beneden nul, een monsterrit van ruim 200 kilometer." | "Temperature 16 degrees below zero, a monster ride of well over 200 kilometres." | high | "monsteret" in the transcript is "monsterrit" (my reading); "beneden 0" appears in stem and small runs |
| 2:25-2:36 | "575 wedstrijdrijders, rond 9500 toerrijders, een aantal Zweden, Canadezen, Zwitsers en Belgen." | "575 competition skaters, around 9,500 tour skaters, a number of Swedes, Canadians, Swiss and Belgians." | medium-high | numbers consistent in all runs (575, 9500). Nationalities: mix says "Nato Zweden, Kaladezen"; stem says "een aantal Zweden, Canadiens, Zwitsers en Belgen". "Canadezen" is my correction. Sounds like a list of foreign participants |
| 3:25-3:50 | "Eerst ... slopen/stapelen ... in de lopen, in de banken, in de bonswacht, vrijdiger, vrijdiger" | no reliable English | very low | **Not narration.** Short isolated chops inside the music with weak vocal energy; every run gave different words (small: "Stuck / End of the road / Climbing up"; medium mix nl: the Dutch above; vocals auto: "fafn"). Probably unintelligible sung/sampled syllables or whisper hallucinating over instruments. Do not quote as lyrics |
| 4:16 and 4:58 | (MUZIEK) | (music) | n/a | whisper labels only |
| 4:35-5:00 | stray syllables ("Zeg", "Hebs", "Zeld", "Schouder", "Hitloof" ...) | none | none | clear hallucination pattern (isolated words every 2 s, an artefact of window length). Treat as no speech. Stem loudness shows small vocal-stem spikes 4:35-5:00, probably percussive bleed or vocal-like synth |

## Thematic and emotional weight
- **"18 januari 1963"**: the first words. The only thing here that anchors the film in a specific day; frames everything after as archive. 
- **"zonder weerga" (if correct) / "allersterksten"**: the register of heroic endurance: extreme distance, only the strongest survive. 
- **"Waar iedereen zich voor opmaakt, dat is de Elfstedentocht"**: the narrator sums up national anticipation; the one sentence about collective feeling, delivered after a pause and music.
- **"16 graden beneden nul ... monsterrit"**: hardship and scale. 
- **The numbers (575, 9500) and nationalities**: the scale of participation, a crowd-and-community theme; the foreigners add pride/curiosity.
- The narration is purely factual-announcing, with no first-person emotion. Emotion in this piece is carried by the music and picture, not by what is said. After 2:36 the work is wordless (OBSERVATION); I cannot confirm any lyrics at all.

## Overall confidence
Date, "Friesland", "twaalfde Elfstedentocht", temperature, distance and participant numbers: confident. Time of day, "zonder weerga", the start of the line at 1:20: tentative. Anything after 3:20: no usable words.
