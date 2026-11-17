# video1: master dossier (blind mode)

Built from the checked music reading (`v1/analysis_blind/music/video1/music_reading.md`), the ten segment notes `seg_01` to `seg_10`, `music.md` and `words.md` in `v1/analysis_blind/perceive/video1/`, `sync/sync.json`, and frames I opened myself. Duration 3:08.66. No context file, no research notes, no web. Times are m:ss; frame `f_NNNN` is second NNNN-1.

Labels used: **SEEN** (I saw it in a frame or it is on-screen text), **HEARD-DATA** (from transcripts, stems or measurements; nobody here can listen), **INTERP** (interpretation), **UNVERIFIED** (hearsay from a note, not checked).

Frames I opened to settle questions: f_0013, f_0025, f_0035, f_0058, f_0059, f_0114, f_0117, f_0125, f_0136, f_0139, f_0153, f_0155, f_0168, f_0169, f_0160, f_0178, f_0187, f_0188.

---

## 1. Overview

A 3:08 black-and-white archive-style film about a mass winter ice-skating event in the Dutch/Frisian countryside, set to a loud, dry, relentlessly steady instrumental track at 78 BPM (possibly felt as 156), built on a D drone with no melody and no cadence. The only "lead" is a flat, old-sounding Dutch spoken voice that gives facts (SEEN/HEARD-DATA: "18 januari 1963", "16 graden beneden nul", "ruim 200 kilometer", "575 wedstrijdrijders, rond 9500 toerrijders", a roll-call of Frisian towns, and twice "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht"). The film runs from a dark, blurred pre-dawn crowd and newspaper headlines ("zwaar, zwaar, zwaar") through registration, the wind-blown ice, tea and exhausted faces, a sign-by-sign route list and a crowd at a FINISH banner, and ends on a rapid montage, a sign "DOKKUM" and a banner reading "ELFSTEDENTOCHT", then black at about 3:08.2. The music moves by subtraction and slam (bass out at 1:15, bass slam at 1:40, hush at 1:55-2:13, a 0.4 s breath at 2:47.8, a wide wall to 3:08, then a hard cut). The picture is not locked to the beat (7.8% of 51 detected cuts within 80 ms of a beat, against 19.7% expected by chance); it follows the narration and the music's sections instead. The overall feeling (INTERP): collective endurance, cold, anonymity, awe and distance, with warmth only in the tea sequence, and an unresolved stop.

---

## 2. Timeline

Picture times come from contact sheets and frames and are good to about +/-1 s unless a frame is cited; `shots.json` badly under-detects cuts in this film (a 30 s "shot" at 0:12-0:42, one at 1:27-1:48, and so on), so I trust frames and sheets. Words use large-v3 on the vocals stem (`words.md`) where available, with Dutch corrected from the transcripts; the English is mine. Whisper's "Bedankt voor het kijken" (3:07) and "MUZIEK" (1:42) are not speech. Music events follow `music_reading.md`.

| Time | What we see (SEEN) | What we hear (HEARD-DATA) | Craft and feeling (INTERP) |
|---|---|---|---|
| 0:00-0:01 | Blurred horizontal smear, dark band over pale mottled grey; nothing identifiable | Cold start: hard hit at about 0:00.7, level jumps from silence to about -15 dB; drums alone, wide-band tail | No fade-in; the viewer is dropped into the film. Disorientation |
| 0:01-0:04 | Night street, packed crowd silhouettes along a brick building with lit windows; faces black; handheld, grainy | Drums at 16th-note rate; "other" wall enters about 0:01.3; D held; bass creeps up from about 0:03-0:04 | Alert, urgent suspense. Murk before explanation |
| 0:04-0:06 | Close, tilted newspaper: LEEUWARDER COURANT, "ELFSTEDENTOCHT OP VRIJDAG", sub-deck partly legible ("Twaalfde tocht wordt zwaarste uit historie", faint); a ghost figure dissolved over it | No voice; same bed | Print supplies the reason for the dread. First newspaper. Double exposure suggests memory |
| 0:07-0:08 | Black night; lit sign "POSTHUMA" (cut at right edge), bare tree, tiny lights | Same | Light points in darkness (motif) |
| 0:09-0:11 | Second newspaper: FRIESE KOERIER, "Elfstedentocht bovenmenselijk zwaar", boxed "Chaos aan de finish"; photo of a lone skater in mist; skates and boots dissolve over it | Voice enters: "18 januari 1963." (0:09.8-0:12.0), the first speech | Voice and page arrive together; the date anchors the film in 1963 |
| 0:12-0:13 | Hard cut. Extreme close-up on black: a blown-out pale oval at top, two round glowing discs below, each with a dark curved rim and a pinpoint highlight (f_0013) | "Een schaatsmarathon zonder weerga" (0:13.6-0:15.6; "zonder weerga" is a correction, the garble may also be read "without a winner") | The most abstract image in the film; reads as eyes or lenses. What it is: unresolved (see section 5) |
| 0:14 | Wide misty night: one very bright lamp or flare, crowd in silhouette along the horizon with tiny lights, two small figures on a pale surface | Same | Dream-like haze |
| 0:15-0:17 | Crowd in caps, scarves and heavy coats; a young round-faced person with a pale cap looks towards the camera; a fur muff; jostling handheld. At 0:17 low angle on boots on a snowy wooden step | "Half zes in de ochtend" (0:16.7-0:18.2) | Pre-dawn dark of the shots fits the words. Note: Dutch "half zes" is 5:30; the English translate pass said 6.30, which I take to be wrong (my Dutch, not tested elsewhere) |
| 0:18-0:20 | Backs of dark leather jackets with white bib patches ("12" at 0:18; a second patch illegible); dark crowd faces | Voice, 0:19.0-0:23.8: "Tweehonderd kilometer door een Friesland waartegen alleen de allersterksten zijn opgewassen" (wording M; the two Whisper runs garbled "opgewassen") | Competitors introduced as numbered backs, not faces |
| 0:20-0:22 | Night crowd, extremely underexposed; fur-trimmed hat bowed; a small pale card or paper in a hand; bright blobs at top; very shaky | Speech continues | Claustrophobic, cold |
| 0:22.5-0:27 | Tilted newspaper page, held still: LEEUWARDER COURA[NT], "Elfstedentocht: zwaar, zwaar, zwaar", "Tal van uitvallers en vele gewonden", right column "Cracks staken wedstrijd" (read in f_0025); a dark photo of trees or a skater; ends on a brighter flash | 0:24.5-0:26.6: "[unclear opening word] voor de twaalfde Elfstedentocht" (opening word L; the rest H) | Three-times repetition of "zwaar" like a tolling beat. The headline ("many dropouts and injured") undercuts the heroic reading |
| 0:27-0:31 | Close, lunging skaters on a rough snowy path in the dark: one in a frost-coated furry jacket, mouth open, arm swinging; a skater on one leg in a deep crouch with a white glove; a distant skater between rows of spectators; one running or stomping at the camera, panting, in a pale pointed cap | 0:27.7-0:31.5: "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht." Bass keeps growing. Chords D, G, C, Dm early on; D drone dominates | First live skating, framed as strain and breath, not elegance. The refrain line is spoken first here |
| 0:32-0:37 | Hard change. Soft grey dawn or dusk; at left a dark wooden building with a railed platform on stilts (f_0035; earlier notes called it a curved silhouette, windmill or sail, which I do not see); telegraph pole and wires, a small white light low right, flat land, two or three tiny figures | Voice stops at 0:32; drums and bass carry on; stereo width jumps; off-beat hi band leaves, main drum cell arrives | The narrator falls silent exactly as the picture goes quiet. First calm shot: held breath |
| 0:37.5-0:41 | Bright, wide snowfield; a row of about eight silhouetted skaters in the same crouch, hands behind the back, evenly spaced; film flicker, specks | Drums briefly almost absent about 0:40, then back at 0:41 | A formation reads as ritual: individuals become a pattern |
| 0:41-0:42 | Cut to a sharper, higher-contrast single skater on rough ice beside snow banks, a hut behind | 0:41.0-0:42.4: "De twaalfde Elfstedentocht." Drums return at about 0:41 | Spoken like a title card |
| 0:42-0:44 | Two linked skaters bend double, camera lunging; then very dark silhouettes mid-stride | Gap in speech | A stumble or hard effort: the cost |
| 0:44-0:48 | Over-exposed snowfield; three skaters in a close column tracking with the camera (near-identical frames) | Bed builds; "other" stem rising | Hypnotic, nearly still image against a pushing pulse |
| 0:49-0:56 | Lower view over rough snow; four figures; then wind-blown ice with two skaters, glare streak; at 0:55 a swing down to legs and a flashing blade; 0:56 near-whiteout of empty ice | 0:50.9-0:53.1: "Temperatuur: 16 graden beneden nul." 0:53.9-0:56.0: "Een monsterrit van ruim 200 kilometer." | Words and picture agree: cold, blowing snow, emptiness as distance. Strongest literal match in the first minute |
| 0:57-0:58 | Low angle: a large black bellows camera and a man in a white-peaked cap against bright sky (f_0058) | Mix peaks about -10.3 dBFS at 0:58; cutting speeds up | First shot of the film acknowledging its own making |
| 0:58-1:00 | Dark close profile of an older man in a black balaclava, mouth open, speaking into a gooseneck microphone, crowd round him (f_0059) | The vocals stem is silent here, so nothing of him is recoverable | A commentator, as far as the frame shows; do not attribute any transcript to him |
| 1:00-1:05 | Skaters bent in profile with a man filming on a tripod camera; a row of about 15 onlookers, some children, then the cameraman in side view; at 1:05 extreme close-up behind a skater, bib "170" | Brief vocal-stem blip about 1:03.5-1:05.5 (about 390 Hz, no transcript, may be a different source) | Documentary self-reflection: someone filming, someone being watched |
| 1:06-1:13 | Fast montage of 0.7-3 s shots: a skater in a striped jumper rounding a bend before a wall of spectators; bibs "245" and "460"; blurred legs and boot at ice level (1:09); a lone skater far down a strip of ice; a crush of skaters; three skaters toward a bridge and houses | Stereo widest so far, brighter (centroid about 2.7 kHz), loudest steady stretch; chords wander but D pedal | Peak of the first build. Solitude (1:10) and mass (1:11) alternate |
| 1:13-1:15 | Dark silhouette of a skater from behind, arm raised; another mid-stride | Same | Light falls as the music is about to drop |
| 1:15-1:17 | Static, steadier wide shot of a low wooden hut with open windows; skaters with bibs and men in hats jostle against its front | At 1:15.6 the bass cuts within about 1 s, mix falls 4-5 dB, drums continue, a sparse held tone, then a held A | Picture slows (shot length about 1.5 s to about 11 s) as the music hollows. A checkpoint, a held breath |
| 1:18-1:20 | Low tilted view across a rough wooden counter: a ringed hand with a pen writes in a notebook; a man leans chin on hand; flag and banner behind; a child's face under the counter | Voice returns about 1:18.8 on A moving to C | Record-keeping as ritual |
| 1:20-1:26 | Fast, high-contrast close-ups: bib "157" on a skater in a white knitted hat while a man in a tweed coat leans in; gloved hands pushing papers; black masses against white paper (f_0087 nearly abstract) | 1:19-1:27: "575 wedstrijdrijders, rond 9500 toerrijders, een aantal Zweden, Canadezen, Zwitsers en [Belgen?]" (numbers consistent across runs; last nationality uncertain; "Dalmatians" is a hallucination). Placement: stem energy at about 1:04 and 1:17-1:24, VAD merged the segment | The only place the music clearly clears for the words. Individuals counted into a mass |
| 1:27-1:29 | First calm, wide daylit shot: snowy street, wooden houses, church spire, humpbacked bridge, old cars, five or six skaters with bibs bunched on skates | Voice ends at 1:27; the bright bassless wall arrives (+26 dB at 2-5 kHz, +3 dB mix, wider) | Release. Loudness up while the picture gets wider, quieter and paler |
| 1:30-1:33 | Extreme long shot: a file of about eight tiny dark skaters on a white void, no horizon | Wall continues, no bass, D drone | Smallness before nature |
| 1:34-1:36 | Frosted reed clump; two then three skaters pass behind and in front in the long low stride, panning with them | Same | Weather and wind texture |
| 1:37-1:39 | One small hunched figure beyond evenly spaced posts on a flat snowfield; a speck high in the sky (bird or damage, unclear); vertical film scratches | Same | Loneliness and endurance |
| 1:39-1:40 | Rough snow or ice ridges, no people, travelling along a bank, brightening | Same | Last quiet before the slam |
| 1:40-1:43 | Blizzard along a frozen channel: washed-white frame, two small figures leaning into wind (one possibly a dog; not resolved) | 1:40: bass stem rises about 35 dB in about 1 s, the largest step in the track; width narrows as the centred bass lands | Picture is calm and white; the sound lands with weight. Sound and picture do not hit together |
| 1:43-1:45 | High-angle aerial over a snowy village: pitched roofs along a curving road or canal | Heavy, loud bed | A map-like community view |
| 1:46-1:48 | Crowd on a bank behind a fence at a canal-side wooden stair; a bibbed skater in a light jumper climbs down and bends over his skates | Vocal-stem burst about 1:46-1:48 (no transcript; not "MUZIEK" which Whisper placed at 1:42-1:43.4 where the stem is silent) | The start of a skater's journey |
| 1:49-1:54 | Rapid cutting: blurred fur-hatted person with long scarf (1:49); ice-level legs and a long shadow across cracked ice (1:50); crowd-lined course with a silo, skaters passing (1:51-1:52); a muddy, grassy bank where men in dark kit, one with a striped headband and a chest patch, scramble over land with skates (1:53, f_0114); a lunging skater (1:54) | Loudest second of the track at 1:52 (about -9.5 dBFS); drums swell about 7 dB from 1:50 to 1:54; sound darkened (centroid about 1 kHz) | Visual energy equals audio energy: the most chaotic cutting under the heaviest sound |
| 1:55-1:57 | Interior, high angle: patterned oilcloth, a dark kettle pouring into a cup on a saucer, more cups, a knife, a slab of dark bread or cake (f_0117) | Bass leaves about 1:55; at about 1:58 "other" collapses and mix falls to about -16 dBFS; small vocal burst about 1:57-1:58 | Cut to warmth arrives about 3 s before the full collapse; the bass goes at the cut |
| 1:58-2:00 | Four or five young people in knit hats and anoraks drinking from white cups, one holding a saucer; a young person at right looks near the camera, calm and weary (f_0120) | The hush: width 0.2-0.3, narrowest in the track; drums go on | Care, relief, a human face meeting the lens |
| 2:00-2:04 | Close on a weathered older man in a patterned jumper and frosted fur-trimmed hat; another hunched figure in a snowy hat; then (f_0125) a dark vehicle with a white disc and black cross, snow, frosted branch | 42.6 Hz sub notes at 2:01.2, 2:07.2, 2:13.4 (every 6.1 s, 8 beats); no voice | The ambulance adds danger beside the care |
| 2:05-2:10 | A man in a frosted fur hat with a white bottle; a man in a patterned cap drinking from a white cup (2:07); a figure in white shorts kneels, rises and stumbles on bright snow (2:08-2:10) | Sub notes; sparse | Refuelling and collapse. Whether the stumbler falls: not resolved |
| 2:11-2:14 | A man slumped against a long trestle table in a hut, rows of white cups; a man in a woollen V-neck and frosted hat (2:13); an extreme close-up of a frost-encrusted profile (2:14) | Bass note and drop-in at about 2:13.4; at about 2:13-2:14 "other" steps up about 5-7 dB; the picture goes dark and motion peaks | Exhaustion; the music's procession starts |
| 2:15-2:17 | Wooden booth with the sign "...CONTROLE" at top (f_0136): a blurred skater runs past, a man in an overcoat with a paper beside him, seated officials behind the counter, a crowd behind a rope; then two men in fur-trimmed hats bent over a counter | Voice begins the town list about 2:15-2:16 (a Whisper block "Sleek, eerst, slotten, staveren..."; probably Sneek, IJlst, Sloten, Stavoren but those four are UNVERIFIED by sign) | Route as a series of checkpoints |
| 2:18 | Close on a frosted square sign with raised letters, reading "ULST" (f_0139) | Names continue | The sign may be a town name with a hidden letter (IJlst would fit: INTERP, unverified) |
| 2:19-2:20 | Wide, hazy: a small high-wing light aeroplane flying low; a woman in a pale coat carrying a camera, other spectators walking away | Sub every 6.1 s continues (2:19.5) | Observers from above; first big tonal change to pale |
| 2:21-2:23 | A village street in deep snow, dense crowd, bicycles, a van, gabled houses, flags; then a still, empty bank with bare reeds and a dark low object on the horizon, held about 2 s | Names | Public occasion, then a pause |
| 2:24-2:25 | Tilted close on an inn front with Gothic lettering "...Vrouwe van Stavore[n]" (reading uncertain), a round enamel sign, "VOLLEDIGE VERGUNNING E. HOLK" | "Stavoren" at about 2:24.4 | A name spoken and a sign shown together |
| 2:26 | Helicopter low above bare trees, a line of onlookers on a snowy road | "Hindeloopen" at about 2:25.8 (UNVERIFIED; nothing on screen identifies it); Whisper's "Markum" at 2:26.6 | Aerial watchers again |
| 2:27-2:28 | Frosted branches frame a hand-painted sign "WELKOM IN WORKUM"; a figure in a cap from behind, snow roofs, a boat | "Workum" at about 2:27 | Strong word-image match. Drums dip 2:26-2:29 |
| 2:29 | Extreme close on "BOLSWARD / BOALSERT" | "Bolsward" at about 2:29 (Whisper "Loftwacht/Noltswacht") | Dutch and Frisian names side by side |
| 2:30-2:31 | Wide gabled brick town, church tower; street workers shovelling snow, children watching | "Harlingen" at about 2:30.7 (Whisper "Hartingen"); the picture cannot confirm the town | The route unrolls as a litany |
| 2:32-2:33 | Close, rotated: "FRANEKER / FRJENTSJER" (f_0153) | "Franeker" at about 2:32 | |
| 2:34 | "DOKKUM" with a "50 km" speed-limit roundel and a give-way triangle; low houses behind (f_0155) | "Dokkum" at about 2:33.6 | This exact shot returns at 3:06 |
| 2:35-2:36 | A weathered signpost: "FRIESCHE / BIRDAARD / DOKKUM" over "IJSBOND / [smudged] / LEEUWARDEN"; a hut and a small car | "Leeuwarden" between 2:34.7 and 2:38.3 (the two Whisper passes disagree) | The route signs and names arrive together |
| 2:37 | Low backlit view of a frozen waterway; a hooded person in foreground silhouette, a few figures along the ice path in low light with long shadows | Brightness of "other" falling; centroid steps down at 2:38 | Dawn or dusk feel; threshold |
| 2:38-2:40 | A row of about a dozen figures in dark clothing stands bent forward in a line facing right on ice under a white sky, long shadow bands (f_0160); then a crowd on a snowy bank, men holding a long pale cloth or rope in a loop | 2:38.3: a pitched D2-region bass replaces the sub; the on-beat hi-band click is about 10 dB weaker to 2:43.7; mids thin | Start line or watchers at a rope: the pose is ambiguous (see section 5). Tension |
| 2:41-2:47 | Jostling handheld crowd: a man in a trilby, fur hats, an older woman with spectacles looking up at an officer whose back is to us (2:44), uniformed police or soldiers (2:45), a metal barrier (2:46), then a violent sideways blur and a person in a striped hood with dark glasses and a raised hand (2:47, f_0168) | 2:43.8-2:48.3: "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht." (second statement of the refrain) | "Everyone" literally shown as a crowd. The only sustained look at faces other than the tea sequence |
| 2:47.8-2:48.2 | Whip-pan smear into the banner | A true 0.4 s drop-out of drums and most of the mix (drums about 40 dB down), the last word ends with it | An intake of breath before release |
| 2:48-2:49 | Static banner "FINISH" held in front of a packed crowd (f_0169) | New drum cell for the whole rest; wide (0.62-0.86), bright to 9-10 kHz, bass centred, voice gone; centroid jumps from about 1.7 to about 3 kHz | The film's hinge: arrival. Detector puts the banner shot at 2:48.8 but f_0169 already shows it at the 2:48 sample, so the banner lands within a second of the gap (exact frame offset UNVERIFIED) |
| 2:49-2:52 | Dark chaos at the line: an officer's back, a hand reaching in, a smeared whip-pan; at 2:52 the back of a hooded skater with bib "342" | Same wall | Fast, underexposed, breathless |
| 2:53-2:54 | A skater in a chunky patterned jumper bends sharply; then a near-blank over-exposed white frame, tiny shapes, a farm line | Same | White flash as a visual pulse |
| 2:55-2:59 | A bunch of skaters from behind with numbers; two or three with hands clasped behind their backs; an extreme close-up of the newspaper again, "...edentocht: zwaar, zwaar, zw..." and a sub-line ending "...onden" (f_0178), apparently the same page as at 0:23-0:26; a diagonal crack through wet dark ice with a boot; an out-of-focus skater bent double against distant farm and trees | Same | The film folds back onto its own opening headline. Ice as stage and as threat |
| 3:00-3:01 | Very close tilted over-the-shoulder shot of a person in dark clothes with a hand-painted bib (reads "S7/" or "15?/", cropped); then a wide soft shot of a dense crowd, hands raised, some looking at the camera | Wall continues; one-second dip in bass and drums at about 3:02-3:03 with "other" at its peak | Breathless |
| 3:02-3:04 | A lone figure in a dark woollen hat with a pale band, mid-stride, leaning, arm swinging, white shape at the foot; then a violent whip-pan smear; a crowd with a woman in a pale headscarf and dark glasses | Same | Probably a skater (not seen clearly). The shot detector treats 3:02-3:04 as one shot but it contains two scenes |
| 3:04-3:06 | Near-white hazy sky, a tall pole, a line of heads (3:04); close among the crowd from behind: bulky coat, knitted cap, man in a peaked cap, flare on the right (3:05) | Centroid dips to about 2.5 kHz at 3:06 | Pushing through the crowd |
| 3:06 | The sharp "DOKKUM / 50 km" sign, identical to the 2:34 shot (f_0187) | A 32nd-note drum roll begins about 3:06.2 | Recap of the route list in picture only; the first clear, composed image in 10 s |
| 3:06.5-3:07.4 | "FRANEKER / FRJENTSJER" sign in snow (very likely the same footage as 2:32; I did not compare the frames) | Roll | The 2:32 and 2:34 order is reversed here (Dokkum then Franeker) |
| 3:07-3:08 | A white hand-lettered banner above a crowd: top line in script, partly cut ("...uitvoerige Reportage"), then capitals "ELFSTEDENTOCHT", then a script line (apparently "op de parterre"; I could not read it) with small hanging cards (f_0188) | Mix still loud (about -10 dB); drums fade over about 0.4 s before the cut | The title word appears as the last text. Cut-rate has risen (shots 0.5-1.5 s) while the level stays flat |
| 3:08.0-3:08.66 | Black (f_0189 entirely black) | Hard mix cut at about 3:08.2 (about -15 to -60 dB in 0.2 s), silent by about 3:08.6, D still in the chroma; no tail, no cadence | An abrupt, unresolved door-slam |

---

## 3. Recurring motifs and where they occur

1. **The press and the written word.** Newspapers at 0:04 (Leeuwarder Courant, "Elfstedentocht op vrijdag"), 0:09 (Friese Koerier, "bovenmenselijk zwaar", "Chaos aan de finish"), 0:23-0:26 ("zwaar, zwaar, zwaar"), and again at 2:57 (apparently the same "zwaar, zwaar, zwaar" page). Signs and lettering as a second voice: POSTHUMA (0:07), "...CONTROLE" (2:15), ULST (2:18), the Stavoren inn (2:24), Workum (2:27), Bolsward (2:29), Franeker (2:32), Dokkum (2:34, 3:06), the IJsbond/Leeuwarden signpost (2:35), FINISH (2:48), the "Reportage / ELFSTEDENTOCHT" banner (3:07). The film mostly speaks through found text, not overlaid titles.
2. **Recording and witnessing.** A bellows camera (0:57), a microphone man (0:58), a tripod camera and its operator (1:00-1:04), a ringed hand writing in a notebook (1:18-1:20), registration papers (1:22-1:26, 2:17), a control booth (2:15), a woman with a camera (2:19), a helicopter and a plane (2:19, 2:26), the "Reportage" banner (3:07). Possibly the two glowing discs at 0:12 belong here (a lens?): unresolved.
3. **Numbers.** The date (1963), the hour, -16 degrees, 200 km, 575 and 9,500, the twelfth edition; bibs 12 (0:18), 170 (1:05), 245 and 460 (1:07-1:11), 157 (1:21), about 24 (1:28), 342 (2:52), a cropped one at 3:00. People are named by number, not by name.
4. **Crowd versus lone figure.** Dark crowd masses (0:01, 0:14, 0:20, 1:02, 1:07, 1:46, 2:21, 2:41, 3:01) against lone skaters or tiny files in white space (0:34 area, 1:10, 1:30-1:39, 1:41, 2:37, 3:02). Faces are rare; the film is mostly backs, hoods and silhouettes. The clearest faces: 0:15, 0:31 (panting skater), 0:58 (microphone), 1:59 (young person looking out), 2:01-2:14 (tired men), 2:44 (older woman).
5. **The skating posture.** Deep crouch with hands behind the back: 0:29, 0:38-0:41, 0:45, 1:34, 2:56, and perhaps the standing line at 2:39.
6. **White-out and black-out.** Dark frames (0:02, 0:07, 0:18, 1:14, 2:50) alternate with blown-white frames (0:56, 1:40, 2:08, 2:54, 3:04); the film begins in murk and ends in a white haze (3:04) and then black.
7. **Light points in darkness.** Windows and lamps (0:01, 0:07, 0:12, 0:14), a small white light at 0:34, the glare streak at 0:52-0:56.
8. **Cold to warm.** Ice and wind throughout; cups, kettle and bread at 1:55-2:12 are the only warmth. The white cups echo the snow.
9. **Mud and thaw-like texture.** Muddy grass bank at 1:53; cracked wet ice at 2:58; both undercut the clean-white image.
10. **Recycled footage.** The DOKKUM sign at 2:34 and 3:06 is the same shot (frames compared). The newspaper page at 0:23-0:26 appears to return at 2:57. The FRANEKER sign appears at 2:32 and 3:06.5. This repetition is deliberate or economical; I cannot say which.
11. **Aerial and map views.** Village from above (1:43), aeroplane (2:19), helicopter (2:26), the route list itself.
12. **The refrain.** "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht" at 0:27.7 and at 2:43.8: the opening and closing statements of the voice.

---

## 4. The song's structure aligned with the picture

Music sections follow `music_reading.md` (edges good to about +/-1 s). The engine is "subtract, then slam": weight and brightness are never both on until 2:48.

| Music section | Picture during it | How they relate |
|---|---|---|
| 0:00-0:09 Intro build: drums, then a wall at 0:01.3, bass creeping up, D held | Smear, dark crowd, newspaper, POSTHUMA sign | Murky, slow-dissolve picture under a nervy pulse: tension without hurry |
| 0:09-0:32 Spoken statement: the voice gives date, hour, distance, the refrain | Newspapers, discs, pre-dawn crowd, strained night skaters | Picture and words travel together (date with the Koerier page; "half zes" with the dark crowd; "strongest" with the "zwaar" page) |
| 0:32-1:15 Voice-free groove and slow build; peak about 0:58; widest 1:06-1:14 | A grey quiet landscape, a skater formation, the white open ice, the camera and the microphone, then a fast 0.7-3 s montage of bibs and bunched skaters | Narration returns only in three short bursts (0:41, 0:51-0:56, 1:03.5) over the ice; cutting speeds up with the rising weight |
| 1:15-1:27 Collapse and exposure: bass cut, held A to C, the numbers read out | Hut, notebook, bibs and papers | Picture slows to long takes and close hands as the sound empties; the only place the music clears for words (4-6 dB quieter) |
| 1:27-1:40 Bright bassless wall | First wide calm street, white void with tiny skaters, reeds, a lone figure, snow ridges | Louder and wider sound with paler, emptier pictures; the voice leaves just before |
| 1:40-1:55 Bass slam and peak (loudest at 1:52) | Blizzard, aerial village, stair, fast scramble of fur, ice, mud, a lunge | The sound lands at 1:40 over a calm white shot (no match); the loudest passage then matches the fastest cutting (1:49-1:54) |
| 1:55-2:13 Trough with gated 42.6 Hz sub every 6.1 s | Tea, cups, young faces, weathered exhausted men, ambulance, a stumbling skater | Cut to the kettle at about 1:55 as the bass leaves; the hush runs a few seconds later. Quiet music and quiet people |
| 2:13-2:38 Procession: A-led two-bar loop, a roll-call of towns | Control booth, ULST, plane, signs and towns, helicopter, empty bank | Words and signs are paired within about a second at 2:24-2:36; cuts follow the names, not the beat |
| 2:38-2:47 Re-lock and closing words; click thinned about 10 dB to 2:43.7 | The standing line, crowd on the bank, the crowd crush | The refrain closes over the crowd it describes |
| 2:47.8-2:48.2 The 0.4 s breath | Whip-pan blur into FINISH | The hinge of the film in both channels |
| 2:48-3:08.7 Wide wall to a hard stop; 32nd-note roll from 3:06.2 | Fast chaos at the finish, bibs, newspaper, ice crack, crowd, signs, the "ELFSTEDENTOCHT" banner, black | The sound stays level; the picture alone accelerates (shot lengths 4.2, 2.4, 3.0, 0.6, 1.5, 0.8, 0.7, 0.5 s in 3:00-3:08). The last text is the event's name, then a cut with no tail |

Sync measurements (`sync.json`): 51 detected cuts (under-counted), 7.8% within 80 ms of a beat (chance 19.7%), median offset 0.29 s; the correlations with loudness (cut rate r about 0.27, motion r about 0.32, brightness r about 0.26) are weak, and picture motion against music onsets is slightly negative (r about -0.32). So the match is by section and energy, not by beat. A fair statement (INTERP): the editing follows the words and the shape of the music in broad blocks.

---

## 5. Open questions (deduplicated)

**Picture**
1. What are the two glowing discs with dark rims and the blown-out oval at 0:12-0:13 (headlamps, a lens, eyes, a camera seen from the front)? Frame f_0013 gives no answer.
2. Is the 2:38-2:39 line of bent figures a skating start or spectators at a rope? Long shadows suggest low sun; the pose looks like both.
3. What happens at 1:53 on the muddy bank (changing skates, crossing land, helping someone)? Does the stumbler at 2:08-2:10 fall?
4. Is the second figure at 1:41-1:42 a skater, a person or a dog?
5. Is "ULST" at 2:18 a full word or a worn "IJLST"? What do the cropped Stavoren inn and "Dinneboom" signs fully say? What does the last banner line at 3:07 read ("op de parterre"?), and what is the "uitvoerige Reportage" banner (a broadcaster's stand)?
6. What is the dark speck at 1:37 (bird, damage)?
7. Is any footage newly made? Everything looks archival (grain, scratches, flicker, 4:3-like framing, clothing, cars); the newspaper close-ups may be filmed prop pages or real papers: undecidable from frames.
8. Is the 3:02 lone figure a skater (no blade visible)?
9. Whether the first or second use of recycled shots (DOKKUM, the "zwaar" page, FRANEKER) is original to the source footage or inserted by the editor.

**Words**
10. First words of the 0:24.5-0:26.6 line ("...voor de twaalfde Elfstedentocht"), and whether 0:13.6 is "zonder weerga" or "zonder winnaar".
11. The last nationality at 1:19-1:27 (Belgen? Dalmatians is a hallucination), and the exact placement of the numbers sentence (1:03.7 versus 1:17-1:24).
12. The first town names before 2:26 (Sneek, IJlst, Sloten, Stavoren, Hindeloopen) rest on garbled Whisper plus one sign; only Workum, Bolsward, Franeker, Dokkum and Leeuwarden have on-screen support.
13. Whether the 2:44 refrain is a repeated take of 0:28 or a re-read (the voice at 2:15-2:21 is also a thinner take); whether the voice is archival or recreated; speaker sex is undecidable from pitch.
14. What are the stem bursts at about 1:03.5, 1:46-1:48, 1:57-1:58, 2:14 and 2:20-2:27 that no transcript catches (speech, leakage, or a different source)?
15. The "6.30" from the translate pass against "half zes" (5:30): I read 5:30.

**Music**
16. True downbeat and metre; felt tempo 78 or 156; whether the drums are acoustic or programmed; whether the flat seventh C is played or intermodulation; major or minor third.
17. Whether the 1:15.6 A-to-C step is bar-aligned (the specialists disagree).
18. Whether the 2:38.7-2:43.7 thinning of the click is deliberate or a separation artefact.
19. Whether the 2:39 darkening and 2:48 gap are authored breaks or are, in part, separation artefacts; whether the ending is a hard cut at 3:08.2 or a very short fade.

**Meaning**
20. Why do the voice and the image so often fall silent or still together (0:32, 1:27, 2:48), and why is the voice absent in the two heaviest passages (1:27-1:58, 2:48-3:08)? (INTERP: the words are used as exposition and gates; the weight is left to music and picture.)
21. What is the effect of ending with a title banner, then black, on a still-loud, unresolved chord: an archive door slamming, or "to be continued"?

---

## 6. Contradictions between notes and how I resolved them

- **0:32-0:37 dark shape.** Earlier note: a curved silhouette, a windmill or sail. f_0035 shows a dark wooden building with a stilted railed platform; no curve. Resolved.
- **0:58 microphone man.** The `seg_03` note called him a commentator and the vocal stem is silent here; I keep "do not attribute speech".
- **Bass at 1:28 or 1:41.** `music.md` says the bass returns about 1:28; `seg_05` says it only appears at 1:41; `music_reading` says it is out from 1:15 and slams in at 1:40, with one low D event at 1:28-1:29. I follow `music_reading`.
- **Loudest second.** 1:52 in all notes.
- **Tea cut versus collapse.** Cut to tea at about 1:55 (confirmed f_0117 at 1:56); bass out at 1:55; "other" collapse at about 1:58.
- **FINISH banner time.** The detector says 2:48.8; the 2:48 sample already shows it. A within-one-second ambiguity.
- **"Cuts end at 3:10"** (a `seg_09` slip): the film ends at 3:08.66; fast cutting runs to the end.
- **Whisper's hallucinations.** "MUZIEK" (1:42) and "Bedankt voor het kijken" (3:07) are not in the film; the vocal stem is silent there.
