# Elfstedentocht diptych, round 2: the story across the pair

Reader: story. British English. Timestamps are `<video> m:ss` on our files. Tags: **OBS** measured or seen, **INT** interpretation, **SPEC** speculation; H/M/L confidence. Nobody has heard the audio; sound claims rest on the music readings and on measurements in `data/`. "R2 check" marks something I ran or read in the raw data this round.

Read this round: `round_1/{story,music,listener,picture}.md` and `round_2/picture.md` (the only other round-2 file present when I wrote). `part_mapping.md` re-read. I did not re-read the per-video analysis files this round; claims about them are carried from round 1 and from my colleagues' quotations.

---

## 0. Headline changes to my round 1

1. **One script, one footage pool, two films.** Picture's R2 finding (round_2/picture.md sec 0: bibs 170, 145, 157 and a striped-headband skater recur between the films, b/w in Part 1, colour in Part 2) is the biggest change to the story. It joins my narration finding. The pair now share (a) a spoken script, (b) a footage pool, (c) a sound device (the hole under the title sentence), and differ in (d) tempo, key, texture, (e) colour treatment, (f) order and density of what is shown and said. I did not open the shot pairs myself. I accept them on picture's method (correlation 0.95 against next-best 0.59 and 0.72, then eyes on every pair); the reader should treat the list as a floor (H that some shots recur, M on direction).
2. **Withdrawn: "the better fit is one narration, used twice."** Music's DTW (title sentence across parts 0.49 to 0.57 against 0.50 within Part 1 and 0.74 to 0.89 for different words) and my own (2.6 to 3.5 against 3.6 to 4.2) use different scales but agree on the weak result: same words, not provably the same take. I now write "same script, same wording", not "same recording" (L-M that it is one recording).
3. **Corrected: Part 1 says "twelfth" twice.** R2 check on `video1/lyrics/whisper_medium_mix_nl_transcribe.json`: "...twaalfde Elfstedentocht" at 0:24.2 to 0:26.9, then the refrain at 0:26.9 to 0:31.8, then "De 12e Elfstedentocht" again at 0:40.6 to 0:42.9. Part 2 has it once (1:19.7 to 1:22.5), then the refrain (1:24.0 to 1:28.5). So my table's order stands (date, marathon, hour, 200 km, twelfth, refrain), and music's remark "V1 puts the title sentence before 'twelfth'" is explained by Part 1's repeat at 0:40.6, which Part 2 lacks. Part 2 is not simply a stretched copy of Part 1; Part 1 has one extra line (M; ASR only).

---

## 1. Answers to colleagues

### Music Q2 (second half): which beat of the race does each part's final minute cover, and does the story still need words?

My reading rests on the picture file's shot lists and my round-1 sources (OBS where a frame is named, INT otherwise).

- **Part 1's last minute (2:08 to 3:08)** moves from the tea table and control hut (1:55 to 2:14), to town signs in route order (2:16 to 2:36, voice reading the eleven names), to a crowd and hand-held FINISH banner (2:38 to 2:49), to race footage at speed from about 2:55 to 3:02 (picture R2, sec 0 item 2), to the "Reportage ELFSTEDENTOCHT" banner at 3:07 and black. So its final minute covers **organisation, route and a burst of racing**, as a list; it names the route and then shows a few seconds of the race.
- **Part 2's final minute (4:06 to 5:04)** is, per picture: the bridge crowd (4:01 to 4:09), a control point with officials (4:28 to 4:29), a stopped lorry (4:36 to 4:39), then open water and floes from 4:58.6 as the sound is taken apart (bright layer off 4:36.8, bass gated 4:48.6, groove cut 5:00.8). It covers **the end of the effort and what is left**, not a finish.
- **Neither final minute is "the finish of the race".** Part 1's sound arrives and its picture mostly gives a banner; Part 2's picture and sound both withdraw. The race beat that neither shows is the arrival (the 10:59 and the 127 finishers, which `elfstedentocht_1963.md` has and neither film uses; round 1 sec 4). INT, M-H on the absence, which is OBS.
- **Does Part 2's story still need words after 2:36.1? Partly, and the evidence now splits.** Picture R2 (sheets 11 to 14, all frames opened): no town sign, route sign or newspaper between 3:20 and 4:39, only bibs. So the picture carries no printed information in that window. A viewer who has had 2:36 of voice and the title board is in the position of someone told the rules before the game; the later two minutes need that frame (INT, M, agreeing with picture). But the voice itself may still be giving information, see sec 2.

### Picture Q1 (to music and story): did the maker place the shared shots at comparable musical events in the two forms?

R2 check on `music_views/per_second_levels.json` for the four pairs in picture sec 0.

| Pair (video1 / video2) | Level and voice at video1 | Level and voice at video2 |
|---|---|---|
| bib 170, 1:05 / 3:34 | -10.5 to -10.9 dBFS; vocals stem active at 1:03 to 1:05 (-24 to -30 dB), then quiet; bass about -18 dB; bass leaves at 1:15 | about -11.1 to -11.8 dBFS; bar-rate voice stabs (3:32 and 3:33 at -25 and -34 dB) |
| bib 145, 1:08 / 3:30 to 3:31 | about -10.9 dBFS, no voice | about -11 to -12 dBFS, voice stabs through the window |
| bib 157, 3:00 / 3:51 | -11.5 dBFS, no voice, inside the 2:48 to 3:08 sprint | -10.8 dBFS; the seconds just before, 3:48 (228 s), at -9.8 dBFS, are within 0.5 dB of the piece's maximum per-second level (-9.3, music sec 0) |
| striped headband, 3:02 / 4:44 | -11.5 dBFS, sprint | about -12 dBFS, after the bright layer goes off (4:36.8), bass still full, voice stabs |

What it shows:
- Three of four pairs fall on near-peak seconds in both films. That cannot be called a design signal, because video1 is flat (-15.0 to -10.9 dBFS for 80% of seconds, music sec 1), so "near its peak" is nearly everywhere in Part 1 (M that the test has no power on the video1 side).
- The pair that is distinctive is bib 157: in Part 1 it is the closing sprint, the only stretch where picture and track both go to effort (picture R2); in Part 2 it sits at the top of the brightening ramp (3:48 is the loudest second of the stretch). So the same shot meets the loudest thing the film has, in both films (INT, M-L; one pair).
- The other three pairs do not meet the same kind of event: 1:05 is a voiced passage ten seconds before Part 1's bass exit; 3:30 to 3:35 is mid-plateau with voice stabs; 4:44 is after the brightness is subtracted (INT, M).
- Answer: **not placement by musical event, apart from one pair; the sound structure and the footage pool look independent** (M). Combined with the weak sync (video1 7.8% against 19.7% chance; video2 37.2% against 42.9%), the likeliest picture is that the pack-from-behind material is a **filler register** that the editor uses wherever the music has no sign or narration to bind to (SPEC; supported by picture's equal cut rates being explained by roll shot-length).
- Not tested: which film's cut came first, and whether any stems or masters are shared.

### Picture's challenge: anonymity comes from camera position, not from the edit

I accept most of it. Same operator, same behind-the-skater position and recurring bibs make "no face held" an easy outcome of the footage. I adjust my round 1 point 4 (sec 6.4): the anonymity is **in the pool**; what is an editorial choice is what the pair adds on top: no name in the voice (the script gives numbers, places, a date, never a person), no winner, no finish. So the anonymity of the skaters is partly footage, but the anonymity of the **account** is a decision (INT, M; the script is a document, the pool is a fact about the archive). The pair's reading "the effort is the subject" survives, resting on the script rather than the framing.

### Picture on the hole device: the picture does not share it

Agreed and sharpened. Picture's table (Part 2 hole: a static empty road, then a hard cut to the first crowd about 0.1 s from the drop; Part 1 hole: a whip-pan to a hand-held banner in a crowd, no demonstrable lock) means the hole is **a property of the sound and the script**, not of the pair as audiovisual work. In my round 1 (sec 6.2) I called it a "habit"; I now say it is a habit of the **mix and arrangement** only. The picture's only sound-lock in the pair is in Part 2 (1:28.5), not Part 1 (INT, M-H; consistent with picture's OBS).

### Listener Q to the music colleague (relief or restart?), which I take because the story arc depends on it

After Part 1 ends on black at 3:08.4, Part 2 opens on a title board "De winter van 1963 in Friesland", 28 s of pad and frost, and then the narrator starts again from "18 januari 1963" at 0:41.7. With the footage pool shared and the script restarting, **restart** is better supported than relief (INT, M-H). The viewer meets the same date, same sentences and some of the same shots, so Part 2 is not a continuation but a second telling, slower to begin. This is the main support for "two tellings" over "part one, part two" (sec 3).

---

## 2. New evidence on my round-1 town-list hypothesis (the voice in Part 2, 3:25 to 3:48)

R2 check on `video2/lyrics/whisper_medium_mix_nl_transcribe.json`, and the vocal levels in `per_second_levels.json`.

Whisper segments (start, end): 3:25.9 to 3:27.3 "Stief"; 3:30.6 "Eerst"; 3:34.5 "Slop"; 3:35.9 "Stapen"; 3:38.3 "In de lopen"; 3:39.9 "In de banken"; 3:42.1 "In de bonswacht"; 3:44.3 to 3:48.1 "Vrijdiger" twice. Against the route (Sneek, IJlst, Sloten, Stavoren, Hindeloopen, Workum, Bolsward, Harlingen, Franeker, Dokkum, Leeuwarden):

| Whisper hears | Route | Fit |
|---|---|---|
| Stief | Sneek | initial S, one syllable, M-L |
| Eerst | IJlst | Part 1 also writes it "eerst" for IJlst (round 1) |
| Slop | Sloten | Part 1 "slotten" |
| Stapen | Stavoren | Part 1 "staveren" |
| In de lopen | Hindeloopen | Part 1 "in de lopen" (identical) |
| In de banken | Workum? | unclear: Part 1 hears "Markum" here, L |
| In de bonswacht | Bolsward | Part 1 "Loftwacht", the "-wacht" echo is shared, L-M |
| Vrijdiger | Harlingen? | unclear, L |

- **New OBS:** eight to nine Whisper fragments in about 22 s, with the first five in route order and three of them (eerst, in de lopen, -wacht) hearing the very same non-words that Whisper wrote for the clear Part 1 reading. That is stronger than the round 1 version, which only noted the sequence, though it remains the same ASR on a chopped voice (hallucination on rhythmic material can also produce chains of Dutch syllables; the Whisper small-model pass hears English in the same stretch).
- Timing: the fragments are about 2 s apart in places (3:34.5, 3:35.9, 3:38.3, 3:39.9, 3:42.1, 3:44.3) and the vocals stem peaks at even seconds from 3:36 onwards, consistent with the 2.000 s bar (music sec 6). In Part 1 the eleven names fill 2:16 to 2:36 (about 1.8 s each), so a 2 s bar per name is the same pace (OBS; the arithmetic is mine).
- Where it fails: the sequence stops after about 8 names at 3:48. The last three towns (Franeker, Dokkum, Leeuwarden, the best-known) are not heard, and the voice-stem activity continues to about 4:59 without Whisper words (the "MUZIEK" tags at 4:16 and 4:58 are not speech). If the list is there, it does not complete, or it recurs unrecognised (SPEC).
- **Picture R2 weighs against a link in the image, not the sound:** no sign appears in 3:20 to 4:39 (picture). So if the towns are being spoken, they are spoken over a pack that does not name them. That fits "the places become a pulse" better than "the places are shown" (INT, L-M).
- Status: **SPEC upgraded from L-M to M-L.** Question 1 below asks for the one test that would settle it.

---

## 3. The arc across the pair, revised

1. **Telling, then re-telling.** Both films begin from the date and run the same script in the same order. Part 1 tells it quickly, 78 s from the date to the end of the 575 line; Part 2 slowly, about 114 s (round 1, sec 2). The second part does not advance the story; it re-starts it in a different register. INT, M-H, from OBS.
2. **Document, then experience.** Picture: Part 1 sequences the pool as print, desk and signs with a short burst of race; Part 2 sequences the same pool as pack, crowd and landscape. Music: Part 1 never changes gear (drums constant, events are bass, wall and voice); Part 2 builds by a ramp and unbuilds. Together: Part 1 is a record, Part 2 an immersion (INT, M).
3. **Effort and withdrawal remain the sound arc.** Part 1 ends at its loudest; Part 2 reaches a comparable level (-9.8 to -9.3 dBFS) at 3:48 and dismantles itself. Picture's finding that Part 1's closing seconds already show the footage Part 2 spends two minutes on changes one thing: Part 2 is partly **the continuation of Part 1's last twenty seconds, played slowly**, not a different subject (INT, M).
4. **The hinge sentence sits at the end of the first and the start of the main body of the second** (round 1 sec 4.1). The sound shares that; the picture does not (see above). Keep it as an arranging fact (M-H) and not as a reading of the race.
5. **Endings answer each other only partly.** Part 1: print then black; Part 2: water, no people. The shared pool shows the choice of ending was free (picture), but nothing shows the two were designed as a pair (SPEC).

### Why split it this way? (updated; INT/SPEC)

- **Two tellings of one account, not two chapters.** The strongest case is now: one script, one pool, two cuts, two scores. A single piece with this material would have needed one cut; the maker made two and gave each a different job. The commission (50th anniversary; single source, `context.md`) does not say why. Candidate reasons, in order of how well the evidence fits:
  1. A two-sided single, an A and a B side (MusicBrainz via `part_mapping.md`; H that the release exists, SPEC on reasons). The shorter, louder, rock-oriented one as the A side, the longer, electronic one as the B side fits the usual single pattern; the press described them that way.
  2. **The same material for two functions**: a hard, short piece that tells the event as a list (Part 1), and a longer piece for living inside it (Part 2) (INT, M-L).
  3. The A/B format dictating the lengths with no story reason (SPEC, L).
- **What the pair says that one part does not (revised):**
  1. The same script and the same shots can carry two quite different meanings depending on tempo, key, and what is subtracted. Only the pair shows that the story is in the treatment, not in the content (INT, M; evidence: sec 0 and picture sec 0).
  2. A listener who sees both is shown the same skater twice, once grey and fast (bib 157 at video1 3:00, in the loudest stretch of Part 1), once in blue within the swelling plateau (video2 3:51). The pair lets the viewer see the footage as source material, not as an unrepeatable record (INT, M; viewer-side, no test).
  3. Neither part supplies an arrival; one tells it by counting and the other by dissolving. So the pair says the event is **unfinished as story**: its subject is the run-up and the aftermath of an effort, never its resolution (INT, M).
  4. If the town fragments are real, the pair says the route twice: once as a recitation and once as a pulse. That is the only content the music appears to carry in both parts (SPEC, M-L).

---

## 4. Limits and a challenge to my own earlier story

- The picture findings rest on 1 fps correlation, so the shared-shot list is a floor and its direction (colour source to b/w) is inferred.
- The level table is weak evidence for design; it is mainly a check that I could not find a counter-case.
- My claim "Part 2 does not pick up where Part 1 stops" now needs one qualification: it does, in the footage, at video1 2:55 to 3:02; it does not in the script. So the pair is **continuous in material, restarting in narration**.
- All four colleagues and I read the same dossiers; agreement is weaker evidence than it looks (carried caveat). Hindsight, memory and grief (the viewer's knowledge of later winters) are not shown properties of either film.
- I did not listen. No viewer test was done.

---

## 5. Two new questions

1. **To the music colleague (the one test that would settle sec 2):** take `video2/stems/` vocals from 3:25.9 to 3:50 and `video1/stems/` vocals from 2:16 to 2:36. Compare the number and spacing of syllable bursts with the eleven Part 1 name onsets (about 1.8 s apart): does Part 2 have eleven onsets in a block of about 22 s (3:26 to 3:48), with the same rise and fall shapes in the first eight, and do the vocal bursts after 3:48 (stabs at 3:56, 4:02, 4:06 and so on to 4:59, per the vocals level) repeat that block or use different material? A match in the first eight onsets against the Part 1 stem would turn sec 2 from SPEC into OBS; a mismatch would retire it.
2. **To the picture colleague and the listener:** since the pool is shared, does Part 1 contain any shot, in any colour state, that Part 2 plainly lacks (the newspaper, the registration table, the signs, the control hut), and does Part 2 contain a shot Part 1 lacks (the title-board "De winter van 1963", the frost, the final water)? If everything that is document-like appears only in Part 1 and everything landscape-like only in Part 2, the pair was divided by function, not by what the archive held; if either side contains the other's kind, the split is looser than the story I have told. And as a viewer: which is more noticeable, that the second film repeats shots, or that it repeats the script?
