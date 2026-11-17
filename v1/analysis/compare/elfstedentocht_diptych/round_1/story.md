# Elfstedentocht, Parts 1 and 2: the story across the pair (round 1, story reader)

Scope: what each part covers, the arc between them, why it may be split this way, and what the pair says that one part does not. Music first, picture second. Nobody has heard the audio; every sound statement rests on the music readings and measurements. Timestamps are `<video> m:ss`. Tags: **OBS** measured or seen, **INT** interpretation, **SPEC** speculation; **H/M/L** confidence. "My check" marks something I ran or read in the raw data myself, not just in the analysis files.

Read: both `music_reading.md`, both `interpretation.md`, both `context.md`, `research/part_mapping.md`, `research/elfstedentocht_1963.md`, the Whisper passes in `data/video*/lyrics/`, and the vocals stems.

---

## 0. The mapping, verified

video1 = Part 1, video2 = Part 2 holds (H).
- My check: files are 188.66 s and 305.95 s (ffprobe) against MusicBrainz 3:09 and 5:04 (`part_mapping.md`). video2 is about 1.9 s long, which `part_mapping.md` puts down to a fade tail; I did not re-fetch MusicBrainz.
- Genre and picture agree: video1 is b/w, loud, D-pedal rock; video2 opens on the title board "De winter van 1963 in Friesland" and is colour, loop-built electronic.
- New from my check: the narration is the same script in both (section 2). That is the strongest content link that the pair belong together.

---

## 1. What each part covers

**Part 1 (video1, 3:08.7): the day as a document, from the night before to a sprint with no finish.**
- Picture is b/w archive: print (newspaper at 0:04, 0:23, again 2:57), a registration table, tea, a control hut, town signs, a FINISH banner, "Reportage ELFSTEDENTOCHT", then black (`video1/interpretation.md` sec 2, 3.2, 3.6; OBS, picture claims from the panel's frames).
- Sound is a 78 BPM D-pedal groove whose form is bass, "wall" and voice switched on and off (`music_reading` sec 1-2; H on measurement). Mode undecided (third missing, L).
- The voice gives only facts: date, hour, crowd, cold, distance, field size, then the eleven towns of the route read in order (2:16 to about 2:36), then the refrain sentence again at 2:44.
- It is told by place and procedure, not person: nobody is named, nobody crosses a line (INT, M).
- Ends at 3:08.4 on a cut-off taper, no cadence. Overall character: "disciplined urgency" (`music_reading`, M).

**Part 2 (video2, 5:06 file / 5:04 official): the winter, the endurance, and the leaving.**
- Picture is colour, starts on a broader title ("the winter of 1963 in Friesland") and spends its first 28 s on frost over a pad before any pulse (`video2/interpretation.md` sec 2).
- Sound is a 120 BPM electronic loop piece. Pad on B throughout; bass loop E-G-D, then B-A-D from 2:36.8 (`music_reading` sec 3; roots H, home centre M-L).
- Narration is sentences only until 2:36.1, then a long voiceless stretch with bar-locked fragments from about 3:28.6.
- Ends by subtraction: bright layer off at 4:36.8, bass gated at about 4:48.6, groove cut at 5:00.8, one last tag at 5:02.3, open water, fade (OBS, H).
- No finish, no winner, no named person, no credits.

One-line contrast (INT): Part 1 is the race as paperwork and pulse; Part 2 is the race as a landscape that people pass through and leave.

---

## 2. My main finding: the two parts re-tell the same narration

My check, from the Whisper medium Dutch passes of both parts, with the translate passes as a second opinion. This is ASR and its time stamps are loose by about 0.5 to 0.8 s (`music_reading` sec 6), so read order, not seconds.

| Line (as ASR heard it) | video1 | video2 |
|---|---|---|
| "18 januari 1963" | 0:09.1 | 0:41.7 |
| "schaatsmarathon zonder ..." (garbled both times; "zonder weerga" is SPEC) | 0:12.5 | 0:50.6 |
| time of day, then "200 km door een Friesland waar tegen alleen de allersterksten ..." | 0:16.6 to 0:24 | about 0:58.6 to 1:14 |
| "de twaalfde Elfstedentocht" | 0:24.2 | 1:19.7 |
| refrain "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht" | 0:26.9 to 0:31.8 | 1:24.0 to 1:28.5 |
| "Temperatuur 16 graden beneden" | 0:50.9 | 1:49.4 |
| "een monsterrit van ruim 200 kilometer" | 0:53.9 | 1:52.5 |
| "575 wedstrijdrijders, rond 9500 toerrijders, Zweden, Canadezen, Zwitsers, Belgen" | 1:19.7 to 1:26.9 | 2:25.8 to 2:36.1 |
| the towns, route order | 2:16 to about 2:36 | see section 3 |
| refrain again | 2:43.8 to 2:48.3 | not heard as speech |

- Same lines, same order (H on order: every pass agrees). Part 2 spaces them further apart. Date to end of the 575 line is about 78 s in Part 1 and about 114 s in Part 2.
- The refrain lasts about 4.9 s in Part 1 and 4.5 s in Part 2, so the sentences are not stretched; the gaps are (M, ASR durations loose).
- Weak voice check (L, my own): MFCC-DTW distances between vocals-stem excerpts (0:27, 0:51, 0:09 in Part 1 against 1:24, 1:49, 0:42 in Part 2) are lower for the same sentence across parts (2.6 to 3.5) than for different sentences (3.6 to 4.2), but the Part 1 refrain repeat at 2:44 scores worse (4.3) than the cross-part pair (3.2). Bleed in the stems makes this suggestive only. It does not prove one recording, but it is the same wording, and the better fit is one narration, used twice.
- It resolves two Part 2 doubts. The Part 2 time of day (passes: "6.30", "afternoon") sits at the same point in the script as Part 1's clearer "half zes in de ochtend" (0:16.6 to 0:18.0), so read it as the same line (M). Part 2's "Kaladezen" lines up with Part 1's "Canadezen" ("Canadians" in the Part 1 translate pass; M-H).

Consequence (INT, M): this is not one continuous account split in two. It is a single voice-over script, laid under two different films and two different pieces of music. Part 2 does not pick up where Part 1 stops; it goes back to "18 januari 1963".

---

## 3. A second finding, speculative: Part 2 may carry the town list as fragments

The Part 2 music reading treats the voice from 3:28.6 as probably wordless (L-M) and the Whisper words there as probably hallucinations. I set the two town-list passes side by side:

- Part 1, 2:16 to 2:35 (Dutch pass): Sleek, eerst, slotten, staveren, in de lopen, Markum, Loftwacht, Hartingen, Vranenken, Dokken, Leeuwarden. The route order is Sneek, IJlst, Sloten, Stavoren, Hindeloopen, Workum, Bolsward, Harlingen, Franeker, Dokkum, Leeuwarden (`elfstedentocht_1963.md`).
- Part 2, 3:25 to 3:48 (Dutch pass): Stief, Eerst, Slop, Stapen, In de lopen, In de banken, In de bonswacht, Vrijdiger.
- Same sequence of near-sounds: "eerst", "slotten/slop", "staveren/stapen", "in de lopen" twice, and "(Nolts/Lof)wacht" against "bonswacht" (OBS: the ASR strings; SPEC: that they are the same words).
- The Part 2 segments run at about 2 s intervals, which fits the bar-locked starts at the 2.000 s bar the music reading reports (Rayleigh p about 3e-6; `music_reading` sec 6).
- The English small pass hears "End of the road ... Climbing up" for the same stretch, so there is no stable reading. This is a hypothesis, not a finding (SPEC, L-M).
- If right: the route reading, a clear litany in Part 1, returns in Part 2 as a chopped, rhythmic texture from 3:28 on, and "the witness becomes a crowd/breath" is really "the place names become a pulse". It would make the pair a pair: the same list spoken, then sung without being sung. A listener who knows Dutch town names should be able to settle it (question 1).

---

## 4. The arc from one part to the next

OBS (structure), INT (meaning):

1. **Both parts hold the same sentence at the hinge.** In each, the refrain is followed by a break in the band and then a release.
   - Part 1: 2:44 to 2:48.2, hole at 2:47.8 (drums out about 0.4 s), then a bright sprint, 2:48 to 3:08.
   - Part 2: 1:24 to 1:28.5, bass and drums out about 3.6 to 4.3 s, then the full groove on one downbeat at 1:28.6.
   - In Part 1 this is the end of the piece; in Part 2 it is the start of the long body (about 29% of the way in). The same gesture closes one part and opens the next.
2. **Neither part gives a finish.** Part 1 ends on a banner and black while the sound is still at its loudest; Part 2 ends on water and fading. The finish that is present in Part 1 is a hand-lettered word (FINISH) and a sign; Part 2 has none. Both films leave out the winner, the 10:59, the 127 who finished (OBS, absence; `elfstedentocht_1963.md` has the facts that neither film uses).
3. **Energy shape.**
   - Part 1 builds toward release and stops at the loudest point (K-weighted -6.4 to -7.0 LUFS, 2:48 to 3:08).
   - Part 2 builds for four minutes (about 15 dB total, `music_reading` sec 5), then dismantles itself.
   - Put end to end, the pair rises, then falls: effort, then withdrawal (INT, M). Part 1 ends before the effort resolves and Part 2 spends its last 30 s on the aftermath.
4. **Voice.** Part 1 keeps the voice to the end (it ends in the refrain). Part 2 loses it at 2:36 and after that nobody explains. The explanation is front-loaded in both.
5. **Place.** Part 1 names places (towns, signs, "Reportage" banner). Part 2 shows a place without names: lanes, ice, open water (`video2/interpretation.md` sec 3.5). Naming then dissolving fits the arc.
6. **Tone, as the reception puts it.** Part 1 "loud and rock-oriented", Part 2 "calmer and more electronic" (`reception.md`, `part_mapping.md`). The music readings qualify "calm": Part 2 is calm in surface and gesture, not in energy (M).

Material the pair shares and does not share (OBS): same artist, same archive source (FFAA, films not identified, `context.md`), same wording, the same absence of a finish, no sung vocal in either. Not shared: tempo (78 against 120 BPM), centre (D against B/E), medium (b/w against colour), instrumentation as far as it is recoverable (a "wall" that reads as guitar in Part 1; Part 2 retires "guitar"), narration density.

---

## 5. Why split it like this? (INT / SPEC, held loosely)

- **A two-sided single.** MusicBrainz lists a release with these as A/B sides (`part_mapping.md`). That fits two pieces built to be played one after the other; it does not say why the A side is the shorter.
- **Two answers to one commission.** Both were commissioned for the 50th anniversary (`context.md`; single source for the commission). One reading: the festival got a version for the body (drive, 78 BPM groove, a roll-call of towns) and a version for the memory (the landscape, the loop, the leaving). The commission text found does not say so; this is my interpretation.
- **Cause and consequence, not chronology.** Since both parts restart from the date, the split is not "start, then finish". I read it as the same day as record (Part 1: print, counts, towns) and the same day as place (Part 2: the road, the light, what is left). Alternatives I cannot rule out: the pair was split for length, or by what footage the archive had (SPEC; no artist statement found, `music_reading` sec 10).
- **Same words, different weather.** Because the narrator's lines are identical, their weight is all in the setting. In Part 1 "575 racers, about 9,500 tour skaters" arrives into a bass-less float at 1:19.7 (`music_reading`: entry into cleared space); in Part 2 it ends the voice, at 2:36.1, with a clearing 0.7 s later. The same list reads as a census in one and as a last word in the other (INT, M).

---

## 6. What the whole says that a single part does not

1. **The Elfstedentocht is a script that can be told twice.** One sentence cycle is cut into two different formal worlds, and only hearing both shows that the voice never changes while everything around it does (INT, M; section 2 is the evidence).
2. **The refrain is the pivot, and the answer to it is always a break.** "That is the Elfstedentocht" is followed by a hole in the band in both parts (2:47.8; 1:24 to 1:28.6). Alone, either hole is a clever bit of arranging; together, they are a habit, the structural answer to naming the thing (INT, M-H on the parallel, M on the reading).
3. **Part 1 supplies the shape of an arrival that Part 2 declines.** Part 1's sprint (2:48 to 3:08) is the only place either film's sound arrives, and the picture does not follow it. Part 2 then builds a longer, quieter version and takes it apart. So the pair ask the listener to feel an arrival that neither shows (INT; the panels agree on the effect and split on intent, `video1/interpretation.md` 4.4).
4. **The effort is the subject, and the people stay anonymous.** One part counts, the other follows backs and bibs (OBS). The reading that the maker leaves "the name" for the viewer (`video2/interpretation.md` sec 3.4) gets stronger when it holds across two parts (INT, M-L). Dutch viewers may supply it from 1963 and the cancelled 2012 tour; no Dutch reception was found (`reception.md`).
5. **The route is told once and echoed.** If section 3 is right, the towns are the one thing the pair says twice, first as speech then as texture.

Limits: all of this rests on the same two sets of panels and the same dossiers; agreement among them is weaker evidence than it looks (`video2/interpretation.md` caveat). Hindsight, hauntology, "memory" and "grief" are viewer context, not shown properties of either film (both panels retracted these as findings).

---

## 7. Open points I could not settle

- Whether the narration is literally one recording used twice (L-M; voice distances above are suggestive only) and whether Part 2 spaces it deliberately.
- Whether Part 2's 3:28 to 3:48 fragments are the town names (section 3).
- Whether the footage in the two films overlaps (b/w against colour makes it hard to see; the panels did not compare).
- Whether the video1 black at 3:08.1 and the video2 title card at 0:00 were meant to meet; the official order is Part 1 then Part 2, but nothing found says they were played back to back.
- Why the A side is shorter; no artist statement.

---

## 8. Two questions for colleagues

1. **To the listener (and the music colleague if the listener has no Dutch):** play video2 at 3:25 to 3:50 beside video1 at 2:16 to 2:36. Do the video2 fragments sound like the same town names (Sneek, IJlst, Sloten, Stavoren, Hindeloopen, Workum, Bolsward) in route order, one per bar? If not, what do they sound like? A yes changes the music reading's "wordless" and the story of what the voice becomes in Part 2.
2. **To the picture colleague:** between video2 3:28 and 4:37, does any frame show a town sign, a route sign, or the same sign or paper that video1 shows (the Dokkum sign at 2:34 and 3:06.6, the newspaper page at 0:23 and 2:57)? And do any shots recur across the two films in b/w and colour? That tests whether the pair share footage and whether the names return in the picture too.
