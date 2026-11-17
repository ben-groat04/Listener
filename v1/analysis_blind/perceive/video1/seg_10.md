# video1, segment 10: 3:00-3:09 (the final seconds; the video ends at 3:08.66)

Blind mode: only extracted data used (contact sheet 10, 7 keyframes, 1 fps frames f_0183, f_0184, f_0186, f_0187, f_0188, f_0189, shots.json, whisper, audio/visual/stem features). Timestamps are from the contact-sheet burn-in. Frame f_NNNN is second NNNN-1.

## 1. Shot-by-shot description

OBSERVATION. All black-and-white, grainy, soft, damaged-looking film (specks, scratches, blur). Saturation is 0.0 throughout, so no colour at all. Shots are very short (0.5-3 s) and handheld. Nothing is stable.

| Time | Shot (shots.json) | What we see |
|---|---|---|
| 3:00-3:01.4 | 46 (179.04-181.40) | Very close, tilted, motion-blurred view over the shoulder or back of a person in dark clothing. A white bib or cloth with a hand-painted number is crammed into the left of frame. It reads "S7/" on the contact sheet and "15?/" in the keyframe, so the number is partly cropped and not reliable. A dark, streaky, slightly sloping surface (perhaps ice or a path) fills the right. Camera is moving with the person (a following or "on the shoulder" shot). |
| 3:01 (second 181) | boundary area | Wide, rather soft shot of a dense crowd of people in winter coats and hats, some looking at or towards the camera. Several raise hands. Pale, overexposed sky above. It is unclear which detected shot this belongs to (see open questions). |
| 3:02-3:03 | 47 (181.40-184.44), first half | A lone figure in a dark woollen hat with a pale headband, dark jacket and trousers, caught mid-stride, leaning forward and swinging an arm. A white shape at the foot looks like a blade or boot. A pale textured band above (ice edge, snow or water) and a bare twig at the top. Strong forward lean suggests speed. The camera is high and looking down at a slant. Figure is in motion blur. I would call this a skater from the posture, but I cannot see the skate clearly (inference). |
| 3:03-3:04 | 47, second half | Violent whip-pan: horizontal smears of dark and light, with the horizon and buildings stretching out. A keyframe of the same shot (182.92 s) shows a crowd, a woman in a pale headscarf and dark glasses at left, hats and shoulders, and blurred houses on the skyline. The cut does not appear on a beat (see section 3). |
| 3:04-3:05 | 48 (184.44-185.04, only 0.6 s) | Almost white, hazy sky with a tall, slightly blurred pole or flag-staff, and a thin line of heads along the bottom. At left a man in a brimmed hat and a younger person stand out. Very overexposed. |
| 3:05-3:06.5 | 49 (185.04-186.56) | Close among the crowd, mostly seen from behind: a big bulky coat, a knitted cap, a man in a peaked cap who looks like uniform headgear (a police or official cap, inference), another dark back at right. Strong white glare or flare blooms on the right (3:05 frame). Shot feels like pushing through a crowd. |
| 3:06 | shot not separately listed | Stable, sharp, centred close shot of a road sign: a dark rectangular sign reading **DOKKUM** with a white triangle (give-way sign) below and a round speed-limit sign "50 km". Behind: a low house, bare trees and snow-covered ground, grey sky. This is the only calm, composed image in the segment. It appears in frame f_0187 (second 186). Shots.json puts the cut at 186.56, so the sign shot either was missed by cut detection or the timing is off by about half a second. |
| 3:06.5-3:07.4 | 50 (186.56-187.36) | Keyframe: a black sign with large pale capitals "**FRANEKER**" over "**FRJENTSJER**" in front of snow, a tyre or wheel arc below. Close, a bit tilted. See section 2. |
| 3:07-3:08 | 51 (187.36-188.08) | A white banner above a crowd, hand-lettered in two styles. Top line in script, partly cut off: "...uitvoerige Reportage" (frame 3:07 shows "uitvoerige Reportage"). Below in clear capitals: "**ELFSTEDENTOCHT**", and under it a script line that looks like "op de pasteur" or "op de parterre" (unclear). Under the banner small cards or flags hang, with dark scribbles (perhaps numbers or letters, unreadable). Heads and hats in the foreground, a white hat bottom centre. A vertical post at right. The camera is slightly shaky, tight on the banner. |
| 3:08-3:08.66 | 52 (188.08-188.60) | Pure black. The film ends here (frame f_0189 is entirely black). |

Camera and editing effects: no dissolves, no titles added by the editor in this stretch; all cuts are hard. The whip-pan blur (3:03) works as a transitional smear. Four of the seven shots are sign or banner shots or have text.

## 2. People, places, objects, on-screen text

PEOPLE (observation). All adults in thick dark winter clothing: coats, knitted or woollen caps, headscarves, one woman in dark glasses, a man in a brimmed hat, a man in a peaked cap. Mostly seen from behind or as part of a crowd. Only one detected face (second 183). Expressions are hard to read; the crowd members who are facing the camera look intent or cheerful (the woman in the headscarf appears to be smiling, low confidence). One lone moving figure (the skater, if that is what it is).

PLACES AND OBJECTS. Flat, open, snowy landscape, grey winter sky, low houses, bare trees. A road. A crowd gathered at a banner or booth. Number bib. Road signs.

ON-SCREEN TEXT (transcribed and translated):
- "DOKKUM" (road place-name sign; the name of a town) plus a round "50 km" speed limit sign.
- "FRANEKER / FRJENTSJER": Franeker is a town; "Frjentsjer" is the Frisian-language form. So the sign is bilingual, Dutch above, Frisian below (my knowledge of Frisian, not seen in the data).
- Banner: "...uitvoerige Reportage / ELFSTEDENTOCHT / op de (illegible)". "Uitvoerige reportage" is Dutch for "detailed/extensive report(age)". Tocht = tour/trip; Elfstedentocht = "Eleven Cities Tour". Probably a broadcaster's or newspaper's coverage stand; I cannot tell the exact wording of the last line.
- The bib number is mostly cropped: only "?57/" or "15?/" legible.

## 3. Sound in this stretch

WORDS. Whisper (Dutch run) gives one line, 3:07.06-3:08.46 "Bedankt voor het kijken!" ("Thanks for watching!"). This is very likely a whisper hallucination: this is a stock sign-off phrase that models produce on music or noise at the end of files, and the vocal stem is essentially zero for the whole range (about 0.001). I treat it as no real speech (confidence moderate-high). The earlier transcript contains genuine-looking narration (e.g. 2:43 "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht" = "What everyone is preparing for, that is the Elfstedentocht"), but nothing is audible as speech here.

MUSIC (inferred from features, not heard). The automatic section is B (158.69-188.66), mean RMS 0.259: one of the louder and more sustained sections. RMS per second is flat at about 0.26-0.28 (peak 0.282 at 3:02, 0.277 at 3:06, 0.272 at 3:07). Onset strength about 1.0 and steady. Spectral brightness about 2900-3050 Hz until 3:05, then drops to about 2500 Hz at 3:06-3:07 (a slight darkening of tone, perhaps a filter or an instrument leaving). Key estimate for 3:00-3:30 window: D minor (0.65), D major close behind (0.59), so a modal, minor-ish tonality with ambiguity. Global tempo ~78 bpm (beat about 0.77 s), local tempo not checked here. Stems: no vocals. Drums about 0.10-0.17 and bass about 0.09-0.12 for most seconds, so a full band texture; but at second 182 (3:02-3:03) the bass drops to 0.015 and drums to 0.06 while "other" (guitars, synths, keys?) jumps to its range peak of 0.26, suggesting a one-second break or a held chord/riser. At second 185 drums drop to 0.026 with bass still present. At the final second (188) drums 0.01 and bass 0.04: the music has essentially stopped by about 3:08.5.

Because the music has no fade-out in RMS through 3:07 (0.272) and the last second is the first quiet one, the ending is probably an abrupt or short stop, not a long fade (inference from one-second data; moderate confidence). The quietest moment is flagged at 188.66 (the very end).

PICTURE VS SOUND.
- Cuts vs beat: over the whole film only 7.8% of cuts land within 80 ms of a beat, below the 19.7% expected by chance, with a median offset of 0.287 s. Here the cuts (179.04, 181.40, 184.44, 185.04, 186.56, 187.36, 188.08) are therefore not "on the beat" in any tight sense; I did not test each one against beat times. The edit is rhythmic in feel (faster, 6-7 cuts in this 10 s vs 0 to 3 in several earlier ten-second windows) rather than metrically locked.
- Cutting speed rises: shot lengths 4.2, 2.4, 3.0, 0.6, 1.5, 0.8, 0.7, 0.5 s. Acceleration of cuts into the end, while the music stays level in loudness. So the energy of the ending is carried by the picture, not by a swell in the sound.
- Picture echoes words: the earlier narration (listing towns at 2:26-2:35 including "Dokkum" and "Franeker/Vranenken") appears to be echoed visually here by town signs (DOKKUM, FRANEKER/FRJENTSJER) and by the title word "ELFSTEDENTOCHT" on the final banner, which is also the last phrase of the spoken narration at 2:43. Observation of the match; the interpretation (a recap or "roll call" of the route before the end) is mine.
- Contrast: the music stays steady and driving while the picture goes from motion blur and glare to a calm, crisp sign and then black.

## 4. What a viewer feels here and why (interpretation)

- Breathless urgency and crowd energy at 3:00-3:05: tilted handheld shots, whip-pan, glare and haze, with the lone leaning figure. The viewer is thrust into the event, being a participant jostled in the crowd rather than an observer.
- A moment of clarity and arrival at 3:06-3:07: the sharp, centred town signs and the banner give orientation and a sense of place and destination, and the title word is finally legible. A feeling of "this is what it was all for / this is where we are", a kind of resolution.
- A sudden, slightly abrupt ending at 3:08: the cut to black, with the music stopping, leaves an unresolved, wistful or stunned silence rather than a triumphant close. The cold, grainy greyness and the faceless backs of the crowd keep a documentary, distant, nostalgic tone (these are people from an earlier era, many with their backs turned: anonymous).
- Overall: collective effort, cold, endurance; the individual lost in the group.

## 5. Symbols, motifs, visual rhymes worth tracking

- Bib number close-up (3:00): numbered individuals vs anonymous crowd. Check whether numbers recur earlier (competitors, "575 wedstrijdrijders" in transcript at 1:19).
- Town signs as a motif of route and progress (DOKKUM, FRANEKER). Compare with the 2:26-2:35 town list; do earlier shots show other town signs, and in what order?
- Crowd from behind (3:05): the viewer stands with the spectators looking at something we cannot see. Compare with other crowd shots.
- The lone figure on a pale, icy ground (3:02): the central image of the whole film, probably; the same posture may recur from earlier.
- Text on screen is almost always hand-made or municipal sign lettering, not added titles: the "found text" aesthetic.
- Overexposure and whiteness (3:04-3:05 haze) vs the pure black ending: a white-out then black-out bookend.
- The end lands on the event's own name, "ELFSTEDENTOCHT", on a banner: title as final image.

## 6. Open questions for the team

1. Is the final image (banner 3:07) the same footage or the same banner as in earlier segments (e.g. around 0:09-0:31 where the date and event are announced)? Does the film begin with a matching text shot (a bookend)?
2. Which detected shot does the 3:01 crowd frame belong to, and is the DOKKUM shot (3:06) a missed cut? Shots.json lists 46 (179.04) and 47 (181.40) but the keyframe of 47 (182.92) shows a crowd while 3:02 shows the skater: the first-half and second-half of shot 47 look like different scenes, so there may be an undetected cut at about 182.5-183.
3. Does the music have a deliberate stop/hit at 3:02-3:03 (bass and drums dropping, "other" peaking) and is it matched to the whip-pan? A listening check at 182-183 s would settle it.
4. The final spoken line in Whisper ("Bedankt voor het kijken!") is probably spurious. Can someone with audio access confirm that there is no speech at 3:07?
5. Is the ending a hard stop or a decay? (The RMS series has no value after 187.)
6. The banner's third line ("op de pa(r)te(r)re"?) and the number on the bib need a closer look at the original resolution, if available.
7. Is the lone figure really a skater? Check the preceding 20 s and the rest of the film for ice and skates.
