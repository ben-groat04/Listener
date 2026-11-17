# video2: VOICE specialist, round 1 (blind, measurements only)

Evidence keys: [LV] per_second_levels.json (vocals column); [IMG nnnn] music_views/window_nnnns.png; [LY] lyrics/ (whisper_small_mix, medium_mix_nl_translate, medium_vocals_auto); [LN] lead_notes.json; [CH] chords.json; [CLAP] clap_tags.json; [PY] my runs: scripts/agents/voice_r1_video2.py and voice_r1_pitch.py (pYIN on vocals.wav, onset-to-beat offsets); [WIN] the 16 window notes (read in full for the voice sections and cross-checked).

## 1. The big picture

The voice in this track is two different things, and the join between them is the most important fact about it.

**Part A, 0:42 to 2:36: a spoken, male, narration-like sample.** Plain speech, not singing. It is placed as discrete blocks (about 1 to 6 s) over a band that never stops for it, and it carries meaning.

**Part B, 3:28 to 5:00: wordless, chopped, higher-pitched vocal material.** It is hard-edged, gated bursts, repeated, quieter in the mix, and treated as a rhythmic or textural instrument. No words can be recovered.

Between them (2:36 to 3:28, 52 s) the vocals stem is silent (about -72 to -77 dB [LV]). The voice is therefore absent for the entire first 41 s, the whole 2:00-2:25 stretch, and 2:36-3:28. About 38% of the track has real voice (my sum of the segments from [LV] with level above -40 dB).

## 2. Presence map (vocals-stem level, [LV], cross-checked on [IMG])

| Time | Level (dB, mean / max) | What |
|---|---|---|
| 0:00-0:41 | -80 and below | none. Whisper nothing. CLAP "no vocals" 1.0. Demucs smears in the vocals panel are bleed (high) |
| 0:42-0:46 | -27.5 / -23.6 | speech block 1 |
| 0:51-0:54 | -22.9 / -20.5 | block 2 (loudest of the early ones) |
| 0:59-1:01 | -22.9 / -20 | block 3, tail runs into the next |
| 1:04-1:10 | -19.5 / -15.4 | block 4, the longest and loudest early block (6 s) |
| 1:20-1:22.5, 1:24.4-1:28.5 | -25 / -19 | block 5, with a 2 s gap; ends 0.1 s before the drop at 1:28.6 |
| 1:49-1:52.3, 1:53.3-1:56.2 | -19 / -17 | blocks 6 and 7, near the loudest speech levels in the track |
| 2:25-2:28.7, 2:29-2:32.3, 2:32.8-2:35.8 | -19 / -17.3 | blocks 8 to 10: three phrases |
| 2:36-3:28 | -72 to -77 | silent |
| 3:28.5-3:40 | about -53 mean then rising | first chops (3:28.5, 3:32.5, 3:36-3:39) |
| 3:40-4:20 | -31 / -24 | densest chop passage: bursts of 0.5 to 1.5 s every 1 to 3 s |
| 4:20-4:40 | near silent, one burst at 4:38.5 | release |
| 4:44-5:00 | -34 to -28 | chops return, strikingly regular (see section 5) |
| 5:00-5:06 | none | the voice stops before the band does |

Level contrast: speech sits at about -17 to -20 dB, roughly level with the drums, and 5 to 8 dB above the "other" bed. The chops sit at -25 to -35 dB, 10 to 20 dB under the drums and bass. So the speech is a foreground figure; the chops are a background texture.

## 3. Part A: the spoken sample

**Is it speech? High confidence.** pYIN on the stem gives a median f0 of about 118 Hz (10th to 90th percentile 92 to 138 Hz) at 1:05-1:10, about 128 Hz at 1:50-1:56 and about 142 Hz at 2:30-2:35, voiced fractions only 0.1 to 0.3 [PY]. A sung line would have long steady voiced stretches. Lead notes in these windows are fragments in B2 to E3 [LN], the intonation of a low male speaker. The window notes agree (win_0040, 0060, 0080, 0100).

**Words (medium for the gist, low for exact words).** Several independent passes agree on a Dutch-language newsreel-style narration:
- 0:41.5-0:46 "18 January 1963" (small-mix English; medium-nl-translate "18th of January, 1963"; vocals pass "18 Januari 1963") [LY]. Three passes agree, so this is the most secure line (high).
- 0:51-0:54 a title containing "marathon" ("The Marathon Without Rain" / "Schatmarathon without rain"); the translation is shaky on the first word (medium-low).
- 0:58-1:14 "(early) morning... 200 km through a (Friesland / free-slot) where only the strongest..." Whisper disagrees on details ("6.30 in the morning" vs "1.5-6 in the afternoon") (medium on "200 km", "only the strongest", low on the rest). The vocals pass wrote "200 kilopetri o'r Ffriesland ... unig", which supports "Friesland" with the Welsh-tagged text.
- 1:19.8-1:28.5 "The city is called the twelfth Elfsteden-(stone/hunter)... where everyone takes care of / stands up for..." This reads as the Elfstedentocht, the Dutch eleven-city skating race, but a blind listener should say only that Whisper hears "Elf-steden" (eleven-cities) words, medium-low.
- 1:49-1:56 "Temperature 16 degrees below zero, a monster ride of more than 200 km" (two passes agree on "16 degrees below zero" and "200 km", medium-high).
- 2:25-2:36 "575 ... riders, around 9500 ... riders, from Sweden/Norway... Switzerland and Belgium" (numbers agree across passes in 575 and 9500, medium; countries low).

Overall: an archival-sounding Dutch voice reading the facts of an event: date, title, distance, cold, numbers of participants. It is a progression, with each block adding detail (date, then title, then the setting, then the difficulty, then the field of competitors), like a documentary introduction. Whisper's language tag flips between Dutch, Welsh and English; the Welsh lines are hallucination, as the repeated nonsense ("ystafell ystafell...") shows. I treat only the English-forced and Dutch passes as evidence.

**Placement and treatment.**
- Entry and exit are hard-edged: blocks start abruptly with 8 kHz-wide consonants and end sharply (win_0040 on [IMG 0040], win_0100: "cut off sharply at 1:52.3 and 1:56.2"). The speech band reaches about 6 to 8 kHz and has little below 200 Hz. That fits a recording cut in, not a live singer. Whether it is band-limited archive audio or a clean modern read, the measurements cannot say (low).
- It is dry. Win_0100 saw no reverb tail on the 1:49 blocks; win_0080 saw a visible 0.2 to 0.5 s smear on the 1:20-1:28 blocks. I checked [IMG 0080]: that block does have a longer smear, but it is also a quiet section with a reverberant pad, so some of the "room" may belong to the whole sample. Medium-low.
- Centred: stereo width narrows with the speech and drum hits, then reopens (win_0040, 0.53-0.65 at voice moments).
- Speech is phrased by the harmony: entries land on chord changes (0:42.7 on E/Em/G, 0:51.3 on B, 0:59 on Em/E: win_0040), and the 1:49 phrases sit over D/Bm and Bm/B (win_0100). Phrases last 3 to 4 s, which is the 4 s chord pace; one speech phrase is about one chord (about 10 beats at 0.372 s). I checked the first of these in [CH] and it is consistent.

**How the band treats the voice (dialogue).**
- 1:20-1:28.5: the most considered placement in the track. Pad Em held, voice speaking, then at 1:25-1:28 the bass (-76 to -79 dB) and drums (-75 dB) both vanish while the voice finishes ([LV], [IMG 0080]). At 1:28.6 the full band comes in at once with +6 dB loudness. The words ("where everyone takes care of ... the Elfsteden...") are the last thing before the drop; the band answers the sentence. Strong, high confidence on the structure, medium on the words.
- 0:59-1:01: drums fall away (-56 to -73 dB) and the bass swells as the voice enters (win_0040), so the speech is given space.
- 1:49-1:56: the opposite approach: the bass ducks about 3 to 5 dB under the voice, drums keep going, and the "other" layer rises 5 dB at 1:56.5 as the voice leaves (win_0100). The voice is on top of a running groove and the band's lift is its release.
- 2:25-2:36: a drum build at 2:23-2:25 precedes the voice entry (win_0120, win_0140); the "other" layer drops 5-6 dB at 2:36-2:40 as the speech ends.
- Pattern: speech enters with the band thinning or building into it, and the band surges when the speech ends. Four of the five voice passages end and are followed within about 1 to 4 s by an upward lift or drop-in (1:28.6, 1:56.5, 2:36-2:40 followed by a change, 0:42 is the exception). The voice works as a section-opener and a gate for the band's energy.

## 4. The gap, and the change of voice at 3:28

From 2:36 to 3:28 there is nothing, and the first vocal event after it is of a different kind. Evidence for "different kind":
- Pitch: pYIN median f0 about 390 to 430 Hz (G4 to A4) at 3:32-3:34 (412-465 Hz), 4:10-4:16 (386-412 Hz), 4:44-4:49 (412 Hz median) [PY]. The earlier voice is about 118-142 Hz. That is about 1.5 to 2 octaves higher. The lead tracker agrees: win_0200 and win_0220 report notes at MIDI 64-75 and clusters around G4 (LN). Note that on [IMG 0220] the lead panel shows notes mostly between MIDI 63 and 70 (about D#4 to A#4), so a G4-ish centre is right. Either it is another speaker (a woman or a boy), a pitched-up male sample, or a vocal synth/choir. The measurements cannot choose (low).
- Delivery: not sentence-like, but short syllabic bursts of 0.1 to 0.4 s (LN) up to 1.5 s, in gated blocks with sharp on/off edges. Harmonic ladders in the lowest 1 kHz in the bursts [IMG 0220], so it is voiced and probably a human voice or a convincing imitation, but the ladders are brief.
- Words: nothing reliable. The small-mix pass gives "Stuck... End of the road... Climbing up... End of the road to me ... End of the exit" at 3:32-3:59, in fragments of 0.7 to 1.8 s that line up well with the stem's burst timing (win_0200). That is partial support for real English words. But the vocal-stem pass hears only Welsh-tagged nonsense ("I'n sgarfodol", "I'n edrych") and then "Fafn" repeated five times 4:05-4:17, and the 4:52-4:59 "ymwneud" loop. Whisper loops are a known hallucination on repetitive, non-lexical audio. A clean "End of the road" repeated is an unusual thing for Whisper to invent as English when the language-forced Dutch pass gives "MUZIEK" for the same stretch, which makes me suspect a real English phrase, but I rate it low (and could be Whisper reading drum-and-chop rhythm as syllables). The best honest summary: possibly a few short English words ("stuck", "end of the road"); mostly non-lexical.
- Level: -24 to -43 dB at 3:40-4:00, 15 to 25 dB under the mix [WIN 0220]; I confirm the average -31 dB.

## 5. Part B: chop behaviour and rhythm (new measurement)

I detected vocal-stem bursts (RMS above -48 dB, longer than 0.15 s) and compared their onsets to the beat grid (0.372 s period) [PY].
- 3:28-4:22: 36 bursts. Inter-onset intervals are irregular (0.24 to 4.0 s, many near 0.6-0.9, 1.1, 1.6, 1.9). Offsets to the nearest beat are spread from -0.17 to +0.17 s with no clustering at zero (about as spread as chance, since the maximum possible offset is 0.186 s). So the chops in this region are not locked to the beat grid; they float over it. They look like phrase fragments, not a drum-like pattern. Medium confidence (the stem is noisy; some bursts may be bleed).
- 4:44-5:00: the intervals become strikingly regular: onsets at 4:50.6, 4:52.6, 4:54.6, 4:56.6, 4:58.6 (IOIs 1.98-2.03 s, five in a row), plus 4:48.6 and 4:46.6 close to the same grid. That is a 2.0 s period, which is not an integer number of beats of 0.372 s (5.4 beats); it is also close to a 120 BPM pulse, or exactly half of the 4 s chord pace. So here the voice is a metronomic call every 2 s, running across the beat grid. It matches win_0280's "recurrence about every 2 s" reading. High confidence on the period (measured), medium on its meaning. A 2 s loop against a 0.372 s pulse produces a slow cross-rhythm (a repeating 5.4-beat figure) and is the kind of thing a producer sets as a loop, not a performance; it may be that the loop length is set against a half-time bar (4 beats of 0.5 s), which I leave to the rhythm specialist.
- 4:05-4:17: five "Fafn" bursts at 4:05.6, 4:08.1, 4:11.6, 4:12.8, 4:15.9 [LY], spaced 2.5, 3.5, 1.2, 3.1 s. The text is probably not "Fafn"; this is whatever one-syllable burst Whisper hears.
- Stem pitch in 4:10-4:16: median 391 Hz, almost all G4 to G#4 [PY]. The same note recurs at 4:44-4:49. A repeated G4 against the B minor harmony would be the minor third (G natural, the b6 of B minor is G, so it is the sixth degree, which the chord Em carries; against Bm it is the b6, a colour tone, and against G it is the root). I give this as harmony-specialist material, not a claim.

## 6. How words and music answer each other

1. **Scene-setting, then hand-over (1:20-1:28.6).** The stripped band is the clearest "spoken word, then answer" gesture: the sentence ends and a full drop arrives 0.1 s later. High confidence on timing [LV], interpretation mine.
2. **Spoken blocks as bars.** Each speech block is about one chord long and is bounded by the 4 s harmonic rhythm (win_0040, 0100, 0140). That gives the voice a metric role like a lyric line.
3. **Information accumulates while the music loops.** The harmony loops Em-G-D-Bm (win_0100, 0120), while the words move from date to title to course to cold to field of riders. The text grows in drama (cold, monster ride, 9500 riders) while the groove is steady, so the listener hears the story build against a constant engine. That is an interpretation; the transcripts supporting it are partly unreliable, so medium-low.
4. **Quiet bridge to chop.** The long silence 2:36-3:28 lets the groove carry the listener with only the "other" layer thickening (win_0160, 0180). When the voice returns it has lost its meaning (no sentences) and its register, and is used as colour: a shift from "narrating" to "singing/ chanting along".
5. **The ending.** The last voice cut is before 5:00 (vocal -33.7 dB at 4:59). The stray "You" at 5:02.6 is a hallucination on a drum hit (win_0300). The band outlives the voice; the final seconds are instrumental.

## 7. What a listener would feel from the voice

- 0:42-1:56: gravity and documentary distance. A low, flat, factual voice over minor chords feels like a newsreel or a radio report; the date as first word immediately says "this is history". (Interpretation, from [LY] and [CH]; medium.) The band's reaction at 1:28.6 turns that into a feeling of departure.
- 2:25-2:36: the numbers (575, 9500) give a sense of scale and crowd.
- 3:28-4:20: the voice becomes human and urgent but faceless: high, fragmentary and repeated. A chanting or yearning quality, like a crowd or a distant call. The change from the plain male report to a higher, broken voice is the emotional step of the second half (interpretation; medium-low because I cannot hear it).
- 4:44-5:00: a steady 2 s call over the groove, ritual or signal-like, then silence. It feels like a mechanical or ritual refrain rather than a person.

## 8. Contradictions and corrections to window notes

- win_0020 and 0000 treat CLAP "choir" at 0:05-0:20 as a possible vocal. [LV] shows the vocal stem at -80 dB, so I agree with their conclusion that it is not a voice; I would add that a choir-like pad being rated "choir" by CLAP could also mean the pad has vocal-like formants, which I cannot test.
- win_0200/0220 say the vocals "enter" at 3:28.5. [LV] has isolated vocal-level seconds at 3:28-3:29 near -25 dB (208-209 s), then a gap, so the first event at 3:28.5 is single and the proper entry is 3:32.5. Minor.
- win_0100 says the 1:49 speech is "dry"; win_0080 says 1:20-1:28 is reverberant. These are not necessarily in conflict (different blocks) but I would not generalise either.
- The "Welsh" transcript and the "Fafn" and "ymwneud" text should not be quoted as content; I found them driven by language mis-detection (p=0.57) and repeat loops.
- CLAP "no vocals" = 1.0 for 4:15-4:45 while the vocal stem shows bursts: CLAP cannot be used as a voice detector in this track at all, and it also reads the spoken sample (1:20-1:40) as "no vocals". Several window notes already say this; agreed.

## 9. Limits

I cannot hear: speaker identity, language (Dutch is Whisper's best guess), whether the sample is archival or newly recorded, whether Part B is a person, a pitched sample or a vocal synth, and the words of Part B. The vocal stem is a demucs estimate; drum and guitar bleed produce bursts, so some of the "chops" in 4:20-4:50 may not be voice (win_0260 says the same). Pitch figures come from pYIN on speech and are only reliable where the voiced fraction is high (3:32, 4:10, 4:44 yes; 4:50-5:00 returned no voiced frames, so those onsets are noise-like or unpitched).

## 10. Three questions for fellow specialists

1. **Rhythm:** The vocal onsets at 4:46-4:59 are on a 2.0 s grid (1.98-2.03 s, five in a row), which is 5.4 beats of the 161.5 BPM tracker pulse but exactly 4 beats at 120 BPM, while the true feel is uncertain (octave-doubling doubts in win_0000 and 0120). Do the drums and bass show a 120 BPM or half-time (about 80.7) reading in that stretch, and does the 2 s call line up with a bar of the drums or cross it?
2. **Harmony:** The higher voice repeatedly sits near G4 to G#4 (4:10-4:16 and 4:44-4:49 [PY]) over B minor and D chords. Is that note a chord tone of the chord sounding at those times (G is in Em and G, but the chart shows Bm/D), and does it ever resolve, or is it a held colour tone?
3. **Form:** Four of the five speech passages are followed within about 1 to 4 s by a band lift or drop (1:28.6, 1:56.5, 2:36-2:40; 0:42 is the exception), and the voice is silent for 2:36-3:28 and returns as chops at 3:28.5. Do the form boundaries from the sections analysis put 2:36 and 3:28 as the ends and starts of sections, and is 1:28.6 the first "main" drop that the speech has been preparing?
