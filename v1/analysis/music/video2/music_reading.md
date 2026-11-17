# video2, "Elfstedentocht Part 2" (Public Service Broadcasting): the music, read as a listener

How to read this. I cannot hear audio. This reading is built from the window notes (`win_0000.md` to `win_0300.md`), all three rounds of the seven specialist files (form, harmony, rhythm, sound, voice, feeling, lineage), `v1/data/video2/` measurements, and window images I opened myself (`window_0080s.png`, `window_0280s.png`). Where the final-round specialists corrected earlier rounds I use the corrected version. Timestamps are m:ss on our file (305.9 s; the official track is 5:04, so absolute times may sit about 1.9 s off the release, intervals are unaffected). Confidence is H/M/L. Observation (measurement) and interpretation (felt reading) are kept apart: lines marked "Feels" are interpretation. Evidence keys: [LVL] per_second_levels.json, [CH] chords.json, [AF] audio_features, [IMG nnnn] window image, [W-nl] lyrics/whisper_medium_mix_nl_transcribe.txt, [CLAP] clap_tags.json, [R1/R2/R3-x] specialist round files. Identity of the track and the Dutch archive narration come from `context.md` and the Whisper passes; the narrator and source film are unconfirmed.

---

## 1. The track in a paragraph

A five-minute, loop-built electronic piece in B minor (B Aeolian) at 120 BPM in 4/4, with no sung vocal, no tune and no cadence [R3-harmony, R3-rhythm; H]. A dark, hushed pad and a few low thuds open it (0:00 to 0:28); a bass and a sparse drum pulse walk in underneath; then at 0:42 a dry, band-limited Dutch archive voice begins to speak about the 18 January 1963 Elfstedentocht [W-nl; H]. After a hole of about 3.6 s (bass) to 4.3 s (drums) at 1:24 in which bass and drums vanish while the narrator finishes "...dat is de Elfstedentocht", a full four-on-the-floor groove slams in at 1:28.6 and then never changes its pulse until the last bar [R3-rhythm; H]. Everything after that is made by one upper layer being muted, reopened and slowly brightened (about 24 to 28 dB more energy at 4 to 8 kHz between about 2:50 and 3:50; mechanism unrecoverable), by the voice turning from sentences into (probably wordless) bar-locked fragments (a very faint blip at 3:24.8, normal-level fragments from about 3:28.6), and finally by subtraction: the bright layer drops away at 4:36.8, the bass is gated into stabs at about 4:48.6, and the groove is cut at 5:00.8, followed by a pad ring-out and one last full-level kick-and-bass hit at 5:02.3 [R3-form, R3-sound; H]. It feels like a long, steady, determined walk or effort rather than a story or a celebration: calm on the surface (fixed pulse, no resolution), pressure underneath (growing brightness, density, loudness), and an ending that is withdrawal and a stop rather than arrival. That feeling is my reading of the measurements (M); the measurements themselves are solid.

---

## 2. Song map

Bars are 2.000 s at 120 BPM. "Cell" means a six-bar (12 s) loop unit.

| m:ss range | Section | What is playing (measured) | What it feels like (interpretation) |
|---|---|---|---|
| 0:00 to 0:28 | **Prelude: pad and thuds** | One sustained, band-limited, wide pad (the "other" stem, about -32 to -27 dBFS) alternating Bm (F# strongest) with D-rich spans (about 0:08 to 0:14 and 0:20 to 0:24) and G-coloured spans (0:04 to 0:08, 0:16 to 0:20), then turning to E at about 0:24 to 0:28 just before the bass enters (other-stem chroma in 2 s steps; chords.json gives only a single Bm for 0 to 42.7 s, so no support from it); isolated low drum thuds at 0:00, 0:08, 0:12, 0:20 (double at 0:19.9 and 0:20.15), 0:24; bass and voice stems silent (-80 to -90 dB). Roll-off only 1.2 to 1.5 kHz, almost nothing above 4 kHz. Mix about -25.5 dBFS. [win_0000, win_0020, LVL, R2-sound, R2-rhythm; H on layers, M-L on the D/G/E alternation] | Held breath; dim, "behind glass", slow, wide and quiet. A cold-morning stillness is a fair image (interpretation, M). |
| 0:28 to 0:42 | **Groove enters, no voice yet** | Bass (about -23 dBFS) and a sparse drum pattern enter on the 2 s grid under the unchanged pad (0:28.13 is beat 56 on the grid); mix steps up about 7 dB to about -18 dBFS. The "other" stem does not change at 0:28 [R2-sound; H]. The tempo tracker's grid starts only at 0:42.68 [win_0000, AF]. | The first footfalls: a stride begins, still muted and dark (M). |
| 0:42 to 1:24 | **Narrator and a restrained band (loop A)** | Dutch narration enters at 0:41.7 ("18 januari 1963"); 0:50.6 about the skating marathon; further phrases at about 1:00 to 1:14 (roughly "200 km through Friesland ... only the strongest ..."; three ASR passes agree, M; the time of day differs between passes, so it is not used), 1:19.7 and 1:24.0 [W-nl; H on date, M on rest]. The mix top band (4 to 8 kHz) jumps about 34 dB at 42.0 to 42.5 s, but the vocals stem makes the same jump (about -44 to +14 dB) and the mix follows it: it is the narrator's own sibilants and consonants entering. The "other" stem's top band rises only about +8 dB there [check, 0.5 s bands; H]. Bass plays one root per 4 s slot (E, G, D, with B tags); drums are intermittent: silent 1:01 to 1:03, burst at 1:04 and 1:08, near-silent 1:10 to 1:15, hits at 1:16, 1:19, 1:20 [win_0060, LVL; H]. Chord changes at 0:32.1, 0:36.5, 1:00.2, 1:04.4, 1:08.2, 1:12.2, 1:20.2 [R2-rhythm]. | Testimony over a held-back band; spacious, documentary, a little solemn. The voice leads and the music frames it (M). |
| 1:24 to 1:28.6 | **The hole** | Bass fades 1:24.5 to 1:25.0 and is silent about 3.6 s (1:25.0 to 1:28.6; stem at -76 to -79 dB); drums are silent about 4.3 s (1:24.3 to 1:28.6); only the pad and the narrator remain ("Waar iedereen zich voor opmaakt, dat is de Elfstedentocht", 1:24.0 to 1:28.5). Pad ("other") dips to about -33 dBFS at 1:26 [R2-sound; LVL; IMG 0080 confirms the black drum and bass panels between window seconds 4.5 and 8.5]. | Held breath, then a coiled spring (M). |
| 1:28.6 to 2:36.8 | **Body 1: the full groove** | Everything returns on one downbeat: drums jump from about -75 to about -18 dBFS within a second and stay flat at -18/-19 dBFS to 5:00; four-on-the-floor kick, strong hats, bass cross-rhythm; "other" returns at about -25 dBFS, slightly brighter and narrower. Mix about -14.7 then -11.8/-12.6 dBFS. Bass swells (up to +11 dB) around 1:40.6; fills at 1:44.4, 1:55.4. Narration interjects until 2:36.1 (16 degrees below, a 200 km "monster tour", the 575 racers and 9,500 tourists list) [R3-voice, R3-rhythm, LVL; H]. Harmony: E-G-D cycle (6 bars) with optional B tag. | Locked-in stride; dry, centred, low in air; a machine carrying a human voice. Drive (M). |
| 2:36.8 to 2:48.8 | **Clearing** | The narrator's last word is at 2:36.1; loop B (B-A-D) begins; the "other" layer partly mutes (all bands -5 to -10 dB; body about 26 to 28 dB, top about -7 dB) while drums and bass carry on [R3-sound; H on numbers, M on "partial mute"]. | A sudden clearing, space after the last human sentence (M). |
| 2:48.8 to 3:24.8 | **Trance** | Body of "other" returns (+10 dB at 2:48.8, top band still low); voice-free for 48 s; mix flat near -12 to -13 dBFS; loop B repeats every 12 s; width opens (0.33 to 0.5) [LVL, R3-sound, R2-feeling]. | Hypnotic; the loop is no longer tracked consciously (M). |
| 3:24.8 to 4:36.8 | **Plateau: pressure and the voice as rhythm** | A very faint vocal-stem blip (about -47 dBFS, L) sits at 3:24.8, 24 bars after 2:36.8; fragments at normal voice level start at about 3:28.6 and then recur on the bar (17 of 21 onsets within one beat before the bar line) and lengthen (mean 1.5 s, 2.2 s, 3.6 s by third) [R3-voice]. "Other" brightens in a ramp, fastest 3:26 to 3:50 (about +14 dB in 24 s), then flat; a sixteenth-hat change at 3:40 is not confirmed (drum-stem hat onset density above 6 kHz climbs only gradually, about 5 to 6 per s, with no step at 3:40); 12 s mean mix peaks at about -9.9 dBFS at 4:24 to 4:36 (per-second maximum -9.3 at 4:12) [R3-sound, R3-form, LVL]. | Rising pressure, "more intense and I don't know when" (M); documentary quality lost (H on shift, M on feeling). |
| 4:36.8 to 4:48.8 | **Sag** | Top band of "other" falls about 13 dB, 1 to 4 kHz about 7 dB, body about 4 dB, while 60 to 250 Hz rises; bass about 4 dB lighter but continuous; mix -9.8 to about -12 dBFS; noise-like hit with a 0.48 s bass dropout at 4:38.3 to 4:38.8 [R3-sound, R3-rhythm; H]. | The glitter goes and the energy drains while the machine continues (M). |
| 4:48.8 to 5:00.6 | **Stutter** | Bass gated from about 4:48.55 (-68 dB on alternate seconds against -18 to -22; stabs about 2 s apart); pad B-F#-A whose D third had already faded at the 4:36.8 sag (D 0.8 to 0.5 to 0.3 in other-stem chroma); one voice stab per bar, on beat 1, unpitched; width opens (0.38 to 0.48 up to 0.53 to 0.58) [LVL, R3-harmony, R3-voice; H]. | Brittle, hollow, lurching (M-L). |
| 5:00.6 to 5:04 | **Cut and ring-out** | The groove stops at about 5:00.8. The pad rings out about 2 s, decaying from -30 to -50 dB. One further full-level mono kick-and-bass hit lands at about 5:02.3 (about -14 dBFS per second; width 0.06), then silence by 5:04; digital zero from 5:04.3 [LVL, stems at 0.25 s; H] | A full stop, a fading pad, then one more hit as loud as the groove; it is not a quiet tap (interpretation, M). |

---

## 3. Harmony and melody

**Key and mode.** One key centre throughout: B minor (B Aeolian: B C# D E F# G A), no modulation [R3-harmony; M-H]. Whole-song key estimate: B minor 0.88 [AF]. The per-30 s labels that read E minor or G major (30 to 150 s) are the same pitch set weighted from other roots [R3-harmony], and the first window found Bm with a G colour from the pad's own peaks (369 to 377 Hz F#4, 493 to 498 Hz B4, 584 to 587 Hz D5, about 390 Hz G4) [win_0000; H on pitches].

**Loop A (0:28 to 2:36.8).** Bass roots E-G-D in 4 s slots (a 6-bar cell, 12 s), with a B tag on some passes (8-bar, 16 s cycles). Example roots: G to about 1:14.5, D 1:16.5 to 1:20, B 1:20.25 to 1:24.5, then E from 1:28.5 starting a fresh cycle [R3-harmony; H on roots, M on edges because of 0.2 to 0.8 s detector latency]. In loop A the lifts are E to G (minor third) and D to E (whole tone), with a G to D drop (bass-root yin in 4 s slots: E-G-D-E-G-D-B).

**Loop B (2:36.8 to 4:48.8).** A strict 6-bar B-A-D loop, 11 passes; it returns to B every 12 s [R3-harmony, R3-form; H]. Roots go B down to A (whole tone), up to D (perfect fourth) and back to B (minor third down). The pad's D third fades at the 4:36.8 sag (other-stem chroma D 0.8, 0.54 at 4:36, 0.33 at 4:39 to 4:48), so by 4:48.8 the pad is B-F#-A, an open fifth with a seventh; the bass roots still follow B-A-D until about 4:48.5 [M].

**No cadence and no tune.** No measured V-I, no clear major third on the B chord (B major labels in [CH] at 4:48.4 and 4:54.8 are best read as Bm losing its D in a thin texture [win_0280]); no lead melody. The "hook" is the bass-root contour and the voice; the lead tracker's notes in the vocals stem are speech or bleed [win_0000, win_0060, R3-harmony; H that there is no sung melody].

**Feels (M).** Elegiac with a lift: the minor-third rises are cancelled by a return to the B pedal every 12 to 16 s, so the effort does not accumulate into arrival [R2-feeling, R3-harmony]. Loop B is more anchored than loop A (home B every 12 s), which suits "settled but straining". The harmony never drives the build; timbre does.

---

## 4. Rhythm and groove

**Tempo.** 120 BPM, 4/4, bar 2.000 s, constant from 1:28.6 to 5:00 (kick fit period 0.49995 s, one constant phase) [R2-rhythm, R3-rhythm; H]. The automatic tracker reports 161.5 BPM with beats every 0.37 s [AF]; this follows the bass's dotted-quaver (3-sixteenth) figure, not the kick, and is explained under section 9.

**Kit and groove.** Kick on every beat (four-on-the-floor), plus an extra kick on the "a" of beat 2 (step 7) in the full groove from about 1:40 [R3-rhythm; H that it is present, M on drum identity]. Backbeat on 2 and 4 is weak at first and strong after about 3:20 (band 1.5 to 5 kHz, beats 2 and 4 are 1.2 to 3.6 times louder; M). A sixteenth-hat change at 3:40 is unverified: hat-band onset density in the drum stem climbs only gradually (about 5 to 6 per s) with no step at 3:40. Drums are flat at -18/-19 dBFS from 1:28.6 to 5:00 and mono-centred [R1-sound, LVL; H].

**Bass cross-rhythm.** The bass plays one pitch per 4 s slot on a 3-sixteenth grid (steps 2, 5, 8, 11, 14), so its first note of each bar is on the "and" of 1 and it lands with the kick only on beat 3 [R3-rhythm; M]. It never plays on beat 1. This is the groove's "lean": steady foot-tap with a slight limp (interpretation, M). The bass is gated, not sidechained (flat within 1.2 dB over the beat) [R2/R3-sound; M].

**The early groove (0:28 to 1:24)** is sparser and different: kick pattern strongest at steps 2, 3, 6, 7, 11, 14 with a weak step 0, so there is no four-on-the-floor yet [R3-rhythm; M]. The 4 s chord slots are the same.

**The grid event.** The drop at 1:28.62 is beat 176.99, 121 beats after the 0:28.13 groove entry (30 bars plus 1 beat); the kick fold changes from the sparse pattern to steps 0, 4, 8, 12 [R3-rhythm; H on the shift, M on how to describe it: a held B slot of 17 beats (two slots plus one beat) followed by 8 beats of bass silence].

**Constancy.** After 1:28.6 no fill, stop or gap longer than 0.32 s marks 2:36.8, 3:24.8, 3:36.8 or 4:36.8. The only pulse-level events are the hole (1:24 to 1:28.6) and the last bar [R3-rhythm, R3-form; H]. Fills exist (1:44.4, 1:55.4, 4:10.4 to 4:12.6) but are not consistently placed before downbeats (two of three end on or after the slot downbeat) [R3-rhythm; M].

**Feels (M-L).** Hypnotic, mechanical, not rock-like; not motorik. Drive in the first half; "propulsion with strain" late; "lurch" only in the stutter. Whether it feels "drive" or "lurch" is interpretation and not settled by measurement [R3-feeling].

---

## 5. Sound and production

**Overall character.** Modern, clean and bright, with no steady hiss floor in the intro (4 kHz and above at about -70 dB early; measured intro only). From about 2:45 CLAP scores "vinyl crackle" about 0.94 to 1.0 in nearly every 5 s window (song mean 0.46 hides this), coinciding with the bright "other" layer; I measured that band as more tonal than noisy (spectral flatness 0.09 at 4:10 to 4:30, against 0.45 at 0:05 to 0:25), so I treat the label as a model response to a bright, driven texture, not as evidence of vinyl; era and late-band cleanliness M-L [R3-sound; H on numbers, M on era]. Heavily limited near the ceiling (sample peak 1.0; 0.0025 % of samples above 0.99), crest factor falling from about 17 dB (intro) to 10.4 to 12.3 dB (groove) [R1-sound; H].

**Loudness arc (mix mean, dBFS).** Intro -25.5; 0:28 to 1:00 -18.3; 1:28 to 1:44 -14.7; 1:44 to 3:20 -11.8/-12.6; 3:36 to 4:30 about -10.5 (12 s mean peaks at -9.9 at 4:24 to 4:36; per-second maximum -9.3 at 4:12); 4:48 to 5:00 -12.9. About 15 dB total rise, mostly in steps at 0:28, 1:28.5 and 3:36 [R1-sound, R3-form; H].

**Layers.** (a) The "other" pad or layer: wide, sustained, present from 0:00. Its spectral tilt opens over 3:00 to 4:24 (body +3/+5 dB, 1 to 2 kHz +9/+12, 2 to 4 kHz +15, 4 to 8 kHz +24 to +30), with the same rhythm and pitch classes, which fits a filter opening and/or drive on one layer rather than new instruments [R2/R3-sound; H on numbers, M on mechanism]. Onset rate stays about 7.2 to 7.9 per s. HPSS energy ratio falls from 14 dB (0:05 to 0:25) to 6 to 8 dB after 1:00, so from 1:00 it contains a sustained part plus an attacked or plucked part [R2-sound; M]. (b) Bass: low-passed or sine-dominated (fundamental 60 to 120 Hz, about 25 dB down at 250 Hz to 1 kHz and about 35 dB down above 1 kHz, peak near 86 Hz); bass guitar, sampled bass and synth bass are indistinguishable [R2-sound; L on identity]. (c) Drums: mono-centred, broadband stripes in every groove window [IMG 0080, 0280; H].

**Width.** Intro is very wide and narrow-band; kick and voice centre the mix; instrumental gaps are wide (0.9 to 1.0 around 1:03 and 1:12, against 0.55 to 0.65 with voice and drums) [win_0060, LVL; H]. Width opens as the bass leaves (0.53 to 0.58 at 4:49 to 4:51) [R2-feeling; H].

**The narrator's sound.** Dry, centred (stem side-to-mid -8.8 to -10.2 dB), band-limited with a hard edge near 4 to 5 kHz; vowel-formant striping shows real speech, not a vocoder [win_0040, R2-sound; H]. The later fragments share that edge (95 % roll-off 3.0 to 5.4 kHz) but are wider (-2.3 to +1.1 dB) [R2-sound; M-H].

**Instruments.** Not recoverable. CLAP's drum machine (song mean 0.63), organ (0.18) and choir (0.11) and synth-pop/electronic/krautrock genre guesses (0.35/0.23/0.16) are weak evidence from a noisy model [CLAP]; Per-window CLAP is more structured than the means: choir 0.78 to 0.99 with bells at 0:05 to 0:25, organ 0.54 to 1.0 in about 14 of 17 windows from 0:30 to 1:20, then drum machine about 1.0 from 1:30. So CLAP consistently suggests a sustained organ- or choir-like pad with bell-like tones in the first 85 s (M-L on timbre) and a drum-machine groove. It also labels the late bright layer "electric guitar" (0.99 at 4:10, 0.90 at 4:30); that is weak and untestable, so guitar is neither asserted nor excluded for the late layer. No identification of banjo or guitar is supported.

**Feels.** Dark and muffled, then open; later hard-edged and bright; at the end hollow.

---

## 6. Voice, words and samples

**No singing anywhere.** The "voice" is Dutch archive narration, then chopped wordless fragments (CLAP misses the narration in most windows, "no vocals" about 1.0, with one speech hit at 1:50 ("radio announcer speech" 0.51) and dips at 1:15 (0.64) and 2:40 (0.67); weak but not blind [CLAP; H]). Dutch is established by content words and context, not by language detection: the Whisper medium pass was run with Dutch forced (lang_prob 1.0 is a placeholder), the small mix pass auto-detected English (p 0.60) and the vocals-stem pass chose Welsh (0.57) [W-nl].

**Words I trust.** There is only one Dutch pass (medium, forced Dutch), plus a small mix pass and a translation pass. Agreement is partial. Medium gives "18 januari 1963" (0:41.7), "Waar iedereen zich voor opmaakt, dat is de Elfsteenpast" (the race name is garbled and restored by me from context; passes give 'Elfsteenpast', 'elven stone', 'Elfstegendpachter'), "Temperatuur 16 graden beneden" (1:49.4; the translation pass says 'below zero'), "een monsteret van ruim 200 kilometer" (1:52.5), "575 ... rijders, rond 9500 toerrijders" (2:25.8 to 2:36.1; other passes 'motorway riders', 'Fettstreet Riders') and Zweden, Zwitsers, Belgen. The date, 16 degrees, 200 km and the 575 and 9,500 figures are supported by two or three passes (H); the restored word 'Elfstedentocht' and the nationalities are M [R3-voice; H on date and figures, M on the rest]. The Whisper lines at 0:50.6 (marathon on skates) and 1:19.7 (the twelfth Elfstedentocht, garbled) are lower-confidence. The vocals-stem auto-language pass chose Welsh and is used for timing only.

**Free timing, then grid.** Narration (0:42 to 2:36) is free-timed, dry and centred. From about 3:28.6 (a faint -47 dB blip at 3:24.8 is not a comparable event, L) the fragments are wordless in my reading (inference, L-M: the Dutch, small and Welsh passes give mutually incompatible words at the same times, which supports 'no reliable words', not 'no words'; Whisper's "eerst", "slop", "in de ..." at 3:25 to 3:48 are probably hallucinations; no word is trusted there; L) and bar-locked: 17 of 21 onsets fall 0.18 to 1.18 beats from the kick grid zero, about 0.1 to 0.2 s before the bar line; they are not beat-quantised or cell-quantised. Fragment length grows (1.5, 2.2, 3.6 s mean) and voiced share of seconds rises from 0.46 to 0.69, then at 4:40 to 4:59 collapses to short unpitched one-per-bar stabs on beat 1 [R3-voice; H on numbers].

**Source of the fragments.** Band-limited like the narrator, but wide; whether they are sliced archive speech, a vocal-like synth or stem leakage of the wide "other" layer cannot be decided [R3-voice, R3-sound; L-M]. The 4:38.5 event is a noise impact with a bass dropout, not a voice [R3-voice accepting R2-sound; M-H].

**The joints.** Three joints are within 0.1 to 0.6 s of a music change: the title sentence ends 1:28.3 and the full band lands about 0.3 s later (IMG 0080 shows the vocals ending at window second 8.5, 1:28.5, with the kick); the last figures end 2:36.1 and loop B starts 2:36.8; the faint blip at 3:24.8 is exactly 24 bars after that (arithmetic correct, event weak) [R3-voice, R3-harmony; H on times, M on intent, direction unprovable].

**Feels (M-L).** Witness to crowd to breath: the voice moves from outside the machine to inside it, and a human sentence is replaced by something nearer to a crowd noise, then a metronomic breath. This is a reading; the measured causes are the widening, the bar lock, the lengthening and the loss of words.

---

## 7. The emotional journey and its causes

Each line is the feeling (interpretation) followed by the measured cause.

- **0:00 to 0:28, held breath.** Single quiet pad, dark roll-off, sparse low thuds with long tails, no pulse [win_0000, LVL]. Cause: no rhythmic grid, narrow bandwidth, 4 s harmonic boundaries marked by thuds.
- **0:28, a stride begins.** Bass and drums arrive under an unchanged pad (+7 dB mix step) [R2-sound, R1-sound]. Cause: low end only.
- **0:42, a voice opens the window.** The mix top band jumps about 34 dB at 42.0 to 42.5 s as the narrator says the date; the vocals stem makes the same jump and the "other" layer rises only about +8 dB [0.5 s band check]. Cause: the narrator's own sibilants and consonants entering (timing and cause H). The earlier 'filter or layer opened with speech' mechanism is dropped. It tells the listener this is about a real day, 18 January 1963.
- **0:42 to 1:24, solemn testimony, spacious.** Sparse intermittent drums, bass roots in 4 s slots, wide instrumental gaps [win_0060, LVL]. Cause: low density, the voice at centre, wide beds in the gaps.
- **1:24 to 1:28.6, held breath, then a jolt: the biggest single event.** Rhythm section stops for about 3.6 to 4.3 s, the narrator names the race, then a hit on beat 1 with about 50 dB return and a brighter, narrower "other" [R3-form, R3-rhythm, R2-sound, LVL]. No fill prepares it; its force comes from the absence of anything leading to it (M).
- **1:28.6 to 2:36.8, a locked stride, dry and low in air.** Constant 120 BPM, flat drums at -18/-19 dBFS, bass lean, narration still free over the top [R3-rhythm]. Cause: pulse fixed, voice free. Drive (M).
- **2:36.8 to 2:48.8, a sudden clearing.** The last voice has just ended, loop B begins, the pad layer falls 5 to 10 dB [R3-sound, R3-harmony]. Three things stack on one cell start (voice out, loop change, layer mute): the best-engineered transition after the drop (M-H on engineering, M on felt effect).
- **2:48.8 to 3:24.8, trance.** Body returns, no new element for 47 s, mix flat, width opens [R2-feeling, LVL]. Cause: repetition without change.
- **3:24.8 to 4:36.8, mounting pressure that no single event announces.** Top band up about 24 to 28 dB, sixteenth hats, longer voice fragments, mix to -9.9 dBFS [R3-sound, R3-voice]. Cause: a slow ramp (fastest 3:26 to 3:50) over an unmoving pulse and a pedal-anchored loop, which sounds like "settled but straining" (M). Because it is a ramp, the listener perceives intensity rising without being able to say when.
- **4:36.8, the pressure leaves.** The bright layer falls 7 to 13 dB in about two seconds, the low pad stays, the mix drops 2 to 3 dB [R3-sound, R3-feeling]. The pulse continues, so it reads as "the energy has gone out" while the machine goes on (M-H on felt change, M on "exhaustion"; tempo never slows, so exhaustion is an image).
- **4:38.3, a stumble.** A one-beat bass dropout and a noise hit [R3-rhythm]. Minor accent, one-off (L as an intended cue).
- **4:48.8, the floor goes.** Bass gated, brittle and airy, one voice stab per bar over a thirdless pad [LVL, R3-harmony, R3-voice]. Cause: subtraction of the low end (the pad's third had already faded at 4:36.8). The kick survives, so it is "no longer a groove in the body" (M) while still a groove in the numbers (H).
- **5:00.8, stop.** A hard cut at 5:00.8, a pad ring-out, one more full-level kick-and-bass hit at 5:02.3, silence [LVL, stems]. A listener used to dance-music form will not expect resolution (M).

Overall the tempo and drum level never change; the emotion lives in layers, level and voice. That is the central finding [R3-form, R3-feeling; H].

---

## 8. The five moments a listener remembers

1. **1:24 to 1:28.6: the hole and the drop.** Every specialist rates it the largest event. It is the only point where the pulse itself disappears; the narrator's phrase naming the Elfstedentocht finishes as the kick lands; the drums return about 50 dB louder on beat 1 with no fill [R3-rhythm, R3-voice, LVL, IMG 0080]. Why it sticks: silence, a named subject, then force.
2. **0:42: the first words.** The top band jumps about 34 dB at the instant the narrator says "18 januari 1963", because the voice itself enters (vocals stem shows the same jump) [band check, W-nl]. Why: it turns a mood into a documented day; first human sound after 42 s of pad.
3. **2:36.8: the last sentence and the clearing.** The list of 575 riders, 9,500 tourists and nationalities ends, the loop changes and the layer thins [R3-voice, R3-sound]. Why: it is the last time a human voice speaks in sentences and the music has to carry the scale of the crowd.
4. **About 3:28.6 to 3:50: the voice breaks into fragments and the build accelerates.** A faint blip 24 bars after the loop change (3:24.8, L), normal-level fragments from about 3:28.6; top band rises about 14 dB in 24 s; fragments grow longer [R3-voice, R3-sound]. Why: change of kind (testimony to texture) plus an accelerating brightness ramp.
5. **4:36.8 to 5:00.8: the unmaking and the stop.** Brightness off, bass gated, one stab per bar, hard cut [R3-form, LVL]. Why: it is the reverse of a build; a track that has only added layers for four minutes takes them away and does not resolve.

Runner-up: 0:28, bass and drums entering.

---

## 9. Where the specialists disagreed, and the best-supported view

| Question | Positions | Best-supported view |
|---|---|---|
| Tempo | Tracker 161.5 BPM (0.37 s beats) [AF, win_0060]; window notes spoke of "81 BPM felt"; all specialists settled on 120 BPM. | **120 BPM**, kick period 0.49995 s, constant phase [R2-rhythm]. The 0.375 s pulse is the bass's 3-sixteenth grid (160 BPM equivalent). H. |
| Length and position of the break | R1 Form: "30.3 bars from 0:28"; R2 Rhythm: "9 beats long"; R3 Rhythm: "17-beat B slot, 8 beats of silence"; Harmony R2 said B bar 8 s. | Groove entry beat 56, drop beat 176.99, 121 beats = 30 bars plus 1 beat. B slot before the break is normal in length; bass is silent 4.0 s; the extra beat is absorbed in the held B (M-H). |
| Is 4:36.8 a gate? | R1 Form: "bass gate / sparkle collapse at 4:36.8"; R1 Sound: "bass gated -45 median"; R2 Feeling corrected. | Two events: **sag at 4:36.8** (top falls, bass -4 dB, still continuous) and **gate from 4:48.5/4:48.8** [R3-form, R2-feeling, LVL]. H. |
| 4:38.5 burst: voice or noise? | R1 Voice: voice-like (pyin C5); Sound: noise (flatness 0.024, bass hole). | Noise impact (flatness 10 to 30 times a voice burst, bass hole), Voice withdrew its claim (M-H). |
| 2:36.8: filter dip or mute? | R2 Form: body-led thinning; R2/R3 Sound: all bands drop together. | A partial mute of one layer, re-entering in two stages (body 2:48.8, top later) [R3-sound]. M-H. |
| Late build: new layers or filter/drive? | Round 1 notes spoke of the layer "surging"; R3 Sound: same pitch classes and onset rate, proportional tilt. | One layer opened gradually (filter opening and/or drive); mechanism unrecoverable (L-M); no new instruments appear in onset patterns (M). |
| Narrator getting brighter? | R1 Sound said later narration is brighter; R2 Sound re-measured on loudest frames (2.54 kHz at 1:05, 3.27 at 2:25, 3.97 at 3:24, 3.12 at 4:40). | Different excerpts, not a steady trend; claim withdrawn (M). |
| Late fragments: archive voice or synth or leakage? | Voice R2: chopped sample; R3 Voice and R3 Sound: undecided; Lineage cautioned. | Undecided. Band-limited like the narrator (M), wide (M-H) (L-M overall). |
| Stem-lead test (vocal vs "other" onset cross-correlation) | R2 Voice and Sound took it as decisive. | Inconclusive (0.18 at -186 ms, -0.12 at zero; other has about 7.5 onsets per s) [R3-sound]. |
| "Calm" in the press vs the numbers | Lineage R1 accepted "calm"; Feeling R2: pressure; mix rises about 15 dB. | Calm in surface and gesture, not in energy [R2-feeling, R2/R3-lineage]. M. |
| Hauntological sound? | Method: archive-as-material (M). CLAP: "vinyl crackle" 0.46 and "nostalgic" 0.58 [CLAP]. Sound: no vinyl floor (L-M era). | Method yes, timbre no. CLAP's vinyl-crackle score is about 1.0 from 2:45 but I measured that band as tonal (flatness 0.09), so it is a model response, not evidence of vinyl; the clean-band measurement covers the intro only. M-L. |
| Key/chord labels | [AF] E minor, G major, D major per 30 s; [CH] Bm 135.8 s, D 44.0, Em 21.9, G 20.1 s. | One key, B Aeolian; the others are the same pitch set from other roots [R3-harmony]. M-H. |
| Kick "extra" step | Lineage's step 11 vs Rhythm's step 7. | Same event (offset of 4 sixteenths): the "a" of beat 2 (H). |
| Fills before downbeats | R2 Rhythm: all three; R3 Rhythm: two of three. | Two of three (M). |
| Rock-song or post-rock form? | Lineage R1 raised it. | Refuted: no verse/chorus, no cadence, no modulation; DAW-style loop form (H on facts, M on label) [R3-lineage, R3-form]. |
| Drive or lurch | Rhythm/Feeling. | Interpretation; "drive" in half one, "strain" late, "lurch" only in the stutter (L-M). |

Process errors the final round corrected (so a reader should not reuse the earlier numbers): Form's 1.2-beat-late count; Harmony's "B bar 8 s"; Sound's 4:36.8 as gate; Voice's phrase-start beat clusters and the 4:38.5 "vocal-like"; Feeling's "never recovers" (the mix recovers partly then sits 1 to 3 dB below peak).

---

## 10. Uncertainties and what the measurements could not settle

- **Instrument identity.** Pad, "other" layer, bass and kit sources are unrecoverable. Spectra fit synthesised or processed sources; CLAP guesses are weak. I make no claim of banjo, guitar or specific synths (L).
- **How the build is made.** Filter, drive or layered parts on "other" cannot be separated at 4 s resolution (L-M).
- **Source of the chopped voice.** Sliced archive speech, a vocal-like synth or stem leakage (L). Demucs's vocal stem leaks hats and snare and widens.
- **Narrator and film.** Narrator identity, source film and whether the narration is newsreel, club film or sponsor film are unconfirmed [context.md].
- **Narration words.** Whisper is unreliable on band-limited speech; only the date, the title sentence, 16 degrees, 200 km and 575/9,500 are trusted. The narration at about 1:00 to 1:14 gives roughly "200 km through Friesland ... only the strongest ..." in three passes (M); the stated time of day (6.30 morning vs afternoon) is contradictory across passes and not used; the Dutch "half zes" error is logged in ERRORS.md for video1. The 3:32 to 3:58 "Stuck", "End of the road" words from context.md are low-confidence ASR.
- **Intro harmony and pad.** The first 28 s alternate Bm, G-coloured and D-rich spans and turn to E at about 0:24 to 0:28, read from other-stem chroma in 2 s steps (M-L); the specialists did not resolve the pad instrument, and the lead-pitch tracker there is artefactual [win_0000].
- **Timing precision.** Bass root times have 0.2 to 0.8 s latency; I trust whole 4 s slots only. Beat-of-bar labels depend on treating the chord change as beat 1 (plus or minus 1 beat for single events). Our file is 1.9 s longer than the official length, so absolute times may differ from the release.
- **Intent.** Why the 1:28 break is one beat long, whether the voice was cut to the music or the music to the voice, and whether "exhaustion", "walk" or "effort" is what PSB meant are interpretation. No artist statement about these tracks was found [R3-lineage].
- **Whether the felt tempo is 120.** I took 120 from the kick; a listener could feel the bass's faster 160-ish pulse (L).
- **Perception.** Nothing here was heard. Mood words are mine. The picture was not used for this reading.

Key helper scripts (all in `v1/scripts/agents/`): `v2_rhythm_r3.py`, `v2_rhythm_r3b.py`, `form_r3_video2.py`, `harmony_r3_video2.py`, `v2_sound_r3.py`, `v2_voice_r3.py`.

---

## Check log

Music check of this reading against measurements (re-run in `v1/scripts/agents/v2_check_music.py`: 0.5 s top-band energy per stem at 40.5 to 44 s, 0.25 s stem RMS for the 1:24 hole, the 3:24 vocals-stem blip and the ending). Each refuted claim was re-verified.

- 0:42 top-band jump: refutation holds. Mix 4 to 8 kHz goes -30 to +14 dB, vocals stem -23 to +14 dB, "other" only about -23 to -15 dB. Rewritten as the narrator's own sibilants; the mechanism M claim is dropped. The slow 2:48 to 4:24 "other" ramp is unaffected.
- Minor thirds (E-G, A-D): holds (A-D is a fourth, in loop B). Corrected from the refutation's root sequence (not re-derived).
- Intro harmony: accepted (from the refuting chroma; not re-run), downgraded to M-L; chords.json gives one Bm only.
- 3:24.75 first fragment: holds. My 0.25 s check shows only -44 to -51 dB at 3:24.5 to 3:27.2 and normal level (-20 to -25) from 3:28.5. Downgraded to L.
- 4:48.8 D third: accepted (chroma figures from the refutation, not re-run); the third fades at 4:36.8.
- Sixteenth hats at 3:40: kept as unverified, not confirmed.
- Hole timing: holds. Bass at floor from 1:25.0 to 1:28.5 (3.5 to 3.6 s), drums silent from about 1:24.3 (4.3 s). Loudness and gate-onset corrections accepted (-9.3 per-second, 4:48.55).
- Whisper "both Dutch passes agree" / p = 1.00: accepted; only one Dutch pass, language was forced.
- 1:04 to 1:10 narration: accepted; added as supported gist (M).
- Ending: holds. Drums and mix show a full-level hit at about 302.25 s (drums -15 dB, mix -12 dB at 0.25 s) after the groove stops at about 300.75. "Tap" removed.
- Vinyl crackle, CLAP instruments, CLAP "no vocals", bass 250 Hz figure: accepted and reworded; per-window CLAP and flatness numbers come from the refutation and were not re-run by me.
- Not tested and so unchanged, label as unverified: fill positions, kick step 7, backbeat ratios, bar-lock 17 of 21, fragment length growth, voiced share, source of fragments, bass gate vs sidechain, 4:38.5 noise, all "Feels" lines and timbre words.
