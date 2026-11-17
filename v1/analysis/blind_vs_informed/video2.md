# video2: blind versus informed

Comparison of two independent analyses of video2 ("Elfstedentocht Part 2", PSB; the blind run was not told this).

- **Blind:** `v1/analysis_blind/music/video2/music_reading.md`, `v1/analysis_blind/video2/interpretation.md`, `dossier.md`, `perceive/`, panel rounds. No `context.md`, no research, no web.
- **Informed:** `v1/analysis/music/video2/music_reading.md`, `v1/analysis/video2/interpretation.md`. (`REPORT.md` does not exist for video2.)
- **Raw checks made for this note:** `data/video2/music_views/per_second_levels.json`, the audio (`audio/song.wav`, last 3 s), `lyrics/*`, frames f_0089, f_0090, f_0157, f_0158, f_0269, f_0270, f_0286 to f_0291, f_0293, f_0300, f_0305.

**Caveat on independence.** Both runs sit on the same measurement pipeline (same stems, Whisper passes, shot detector, specialist agents, six-persona panel). Where they agree on a measurement, that is the same data read twice, not two experiments. The only real difference in input is `context.md` and the research files. So this comparison tests what outside knowledge changed, not whether the measurements are right.

---

## 1. What the blind run worked out on its own

| Item | Blind result | How it inferred it | Verdict |
|---|---|---|---|
| Subject | A mass long-distance skating event on frozen waterways, with numbered entrants, cleared lanes and thousands of tourers | Bibs (201, 529, 504 and others), narration figures "200 km", "16 below", "575 wedstrijdrijders", "9500 toerrijders", "schaatsmarathon", a tractor scraping the ice, spectators at bridge railings | Correct. Matches the informed run and `context.md`. |
| Date | Winter 1963; the narrated date is 18 January 1963 | Title board "DE WINTER VAN 1963 IN FRIESLAND" (frame f_0001) and the Whisper Dutch pass ("18 januari 1963", three passes agree) | Correct. |
| Place | Friesland, the Netherlands | Board; Dutch narration; lorry lettering ending "-SNEEK" (read as a Frisian place name) | Correct. |
| Language | Narration probably Dutch | The forced-Dutch pass is coherent while auto-detect gave Welsh (p 0.57) and English (p 0.60) | Correct, and a good call to prefer the forced pass over auto-detect. |
| Medium | Grainy, scratched colour cine film, gauge unknown | Frames: grain, rounded corners, tint drift, light leaks, burn holes | Correct, and the final version stopped short of claiming 8 mm or 16 mm or an amateur maker. |
| Soundtrack | A programmed loop-machine track fitted to the film; cuts follow its form, so assembly was deliberate; date unknown | 120 BPM kick grid (inter-onset 499.99 ms), hard stop, 0 dBFS peaks, cut times against section edges | Correct in kind (the piece is a modern score on archive footage); under-committed on date (see section 2). |
| Emotion | Hush, then trudge, held breath, relief at 1:28.6, pressure, then an unresolved withdrawal; ending left for the viewer to finish | Timestamped cause-and-effect table in `interpretation.md` section 2 | Same arc as the informed run; see section 5. |
| Structure | Hush 0:00, groove 0:28, narration 0:42, hole 1:24 to 1:28.6, drop, long middle, voiceless bloom 2:36.6, pack, pull-back 4:36.6, thaw 4:49, hard stop 5:00.86, fade | Stems, per-second levels, shot list, frames | Matches the informed song map to within about 0.2 s throughout. |
| Edit logic | Picture cut to the music's large form, not its pulse | Cut-to-kick-grid test (36% against 32%, p about 0.09) and joints at 0:28.1, 1:28.6, 1:40.6, 2:36.6, 3:28.6 | Agrees with the informed run, which found the same. |
| What the film omits | No winner and no finish line shown | Frame review | Correct as a statement about this edit. |
| The race name | Not stated as fact | See section 2 | Over-cautious. |

The blind result is strong on everything the picture, the title board and the narration contain. That is most of the film.

---

## 2. What the blind run got wrong, invented, or threw away

**2.1 It threw away the race's name.** This is the largest loss. The blind `perceive/words.md` had "Waar iedereen zich voor opmaakt, dat is de Elfstedentocht" at 1:24 to 1:28 rated "high for first half, medium for last word, repeated identically across mix and stem runs", and "de twaalfde Elfstedentocht" at 1:20 rated low-medium. The raw Whisper output reads "Elfsteenpast", "twaalfde elfsteen", "Elfstegendpachter". These strings are garbled, but together with 200 km, Friesland, a skating marathon and 1963 they converge on one famous event. The blind insider panellist even said so ("my own cultural knowledge applied to the clues") but the moderator's `interpretation.md` section 6 reduced it to "the race's name rests on garbled transcript strings and is not used as a fact". The informed run's confirmation of the name, the 12th tour, the 1963 outcome and the Dutch cultural weight is the single biggest thing context added. A blind run is allowed its own world knowledge; it should have written "almost certainly the Elfstedentocht (the Eleven Cities Tour), tagged INFERRED". Why it happened: confidence was lost between perceive, dossier and synthesis (see lessons 1 and 2).

**2.2 Under-commitment on the date of the music.** The blind reading found a programmed loop machine, constant 120 BPM, near 0 dBFS from 1:20, a narrator band-limited and gated to fit, and concluded "date unknown". Those cues, plus a mix on 1963 footage, support "a modern (digital-era, probably 2000s or later) production laid over archive film" at medium-high confidence. It stopped at the edit being deliberate. It also did not state the obvious corollary: the narration is almost certainly archival and the music is not.

**2.3 Residual errors in the final text.**
- *Key rated high.* The blind reading gives "B minor Aeolian (high)". Its own evidence is a whole-song estimate (B minor 0.88, D major and G major next) and a bass loop (E, G, D) whose tonic is withheld. The informed run's "B minor for the pad (M-H), first loop equally E minor or G major over a B pedal" is better calibrated.
- *The 2:47 to 2:50 "rise".* The blind reading says the wall "rises 8 to 10 dB at about 2:47 to 2:50 with unchanged spectrum". The raw "other" stem shows a dip of about 6 dB at 2:37 (-23.5 to -28 dBFS) and a recovery by about 2:49 (to -21). So the "rise" is mostly a recovery from the partial mute at the loop change. The informed run has this right.
- *Missed gap at 1:01 to 1:04.* The blind music reading puts the first drum "stop" at 1:10 to 1:20. The raw drums stem is near silent at 1:01 to 1:03 (-73 to -75 dBFS) as well, and sparse (-56 to -68) at 1:10 to 1:16 with single hits. The informed run lists both. (The blind interpretation correctly softened 1:10 to a thinning.)
- *Flag at 4:45 to 4:48.* The blind text says a flag with "red and white bands and a dark lower band". Frames f_0286 to f_0289 show a red cloth with a white panel, then red alone as it hangs, beside a dark telegraph pole. The dark lower band is the pole. The informed wording ("a red and white flag or cloth") is safer.
- *Light-weight speculation kept as reading:* "possibly amateur, possibly commissioned", "ordinary people" (about 94 per cent tourers), "the footage presumably had no such arc". Each is tagged [READING] or [SPEC], so honest, but the "presumably no arc" claim is stated as consensus and has no support in the data. The informed run, with the research notes, says the film mixes race-week pictures and probably other reels, which makes an arc made in the edit more likely.

**2.4 Errors in the first synthesis, caught by the fact-check (26 corrections, listed in the blind log).** These show where the data misled a blind run:
- *Wrong BPM grid.* The tracker's 161 BPM (the hi-hat cross-rhythm) gave a bogus sync statistic (37% against 43%). Corrected to the 120 BPM kick grid.
- *Shot detector.* It missed the real hard cut at 1:28.55, invented a cut at 69.2 s (a dissolve at about 1:13), over-split colour-cycling shots and under-split fast pack shots. This produced wrong shot-length and lattice claims.
- *1 fps frames.* A "dark frame" at 3:36 was an interpolation; the real cut is hard, onto an orange flare. The "no people from 4:49" claim missed a person's legs at 4:49 to 4:51 (confirmed in f_0290, f_0291, which show trousers, boots and a blade).
- *ASR.* The "time of day" differs between passes (6.30 morning, afternoon), "Friesland" was read as clean narration when only the board is certain, and the 3:32 to 3:58 words ("Stuck", "End of the road") are noise on a music-only stretch.
- *Stem bleed.* A "wordless" late phrase and "exactly one call per bar" were read off demucs stems that bleed.
- *Absence read as silence.* "Silence" at 1:24.6 to 1:28.6 was really a rhythm-section dropout, with the narrator and pad playing on and the mix only 2 to 3 dB down (raw: -19 to -22 dBFS in those seconds, against -18 to -20 before).
- *Gloss as fact.* "Hand-lettered", "family or club cine enthusiast", "uniformed helpers steadying", "panting", "fur", "male" narrator and "flat Dutch" were all interpretation. All were softened in the final text.

---

## 3. What the informed run got wrong that the blind run got right

Context did not mislead the informed run often, but it did in these places.

1. **The last hit.** The informed interpretation says "one last full-level hit at 5:02.3" (sections 2 and 4E) while its own music reading lists two drum onsets and three bass onsets about a quaver apart. Raw audio (3 s of `song.wav`) shows a hit at 5:02.34 (about -4 dB), a second at 5:02.58 (about -9 dB) and decay after. The blind reading's "three off-beat hits at about 5:02.34, 5:02.60, 5:02.85" matches the raw data. The informed summary compressed it into a neat symbolic gesture ("one more footfall", "last heartbeat") and the panel then debated a thing that was really a short tag.
2. **The plateau's start at 3:36.6.** The informed text says there is "no step at 3:36" and treats the plateau as beginning at 3:24.8. The level claim is right (the mix rises about 1 dB there), but the vocal stem changes character. Between 3:00 and 3:28 no second exceeds -45 dBFS. From 3:36.6 to 4:37, 50 of 60 seconds do. The blind reading's "dense chops begin at 3:36.6 after a pickup at 3:28.6" is a better description of what a listener hears, and it lines up with the picture's hard cut to the orange flare at 3:36.7.
3. **Priors steering the emotional frame.** The informed text leans on 127 finishers, the cancelled 2012 tour, "inheritance" and a "voice from before the day". Its own panel rated "mourning" L-M, and the sceptic noted there is no Dutch reception evidence, so "Dutch viewers hear hindsight" is a hypothesis. The note that "the grief is in the gap between channels", which depends on what the viewer already knows, is context-led. The blind run's cooler "withdrawal, suspension, a door then a dimmer" stayed closer to what is on screen and in the signal. Neither is wrong; the informed one is more at risk of reading history into a piece whose picture and sound carry little of it.
4. **Single-source facts used as framing.** The informed opening paragraph states the 50th-anniversary commission as fact; `context.md` itself marks it as a single source (writteninmusic.com). The same goes for "the 12th tour" and the 575 and 9,500 matching published figures. They are probably right, but they sit in the first sentence at higher confidence than the evidence.
5. **Archive provenance.** The informed run calls it "colour amateur or regional-archive film". `context.md` dropped "amateur reel" as unconfirmed. The blind run's "gauge, maker and purpose unknown" is closer to the evidence.

Points where the informed run was better (for balance): the mixed-reel observation, the correct 2:36.8 partial mute, the 1:01 to 1:04 drum gap, the flag wording, the key calibration, the ability to name the race, the 1963 facts and the Dutch cultural frame.

---

## 4. Music: do the two readings agree?

**Largely yes.** They share the same stems and per-second data, so this is expected.

| Aspect | Blind | Informed | What the data supports |
|---|---|---|---|
| Intro | 28 s drumless pad, five strikes (0:00, 0:08, 0:12, 0:20, 0:24), mix about -25 dBFS | Same, "thuds" | Both; per-second mix -25.3 dBFS over 0:05 to 0:25. |
| Groove entry | 0:28.1, loop A, kick on the off-beat | 0:28.13, mix +7 dB | Both. Bass stem from silence (-89) to -22 dBFS. |
| Narration | 0:42 to 2:35.8, free of the bar | 0:41.7 (Whisper) or 0:42.5 (stem) to 2:36.1 | Both. Vocal stem jumps at 42 s (-80 to -29). |
| The hole | Drums out about 1:24.0, bass out about 1:24.6 to 1:28.5 | Drums out 1:24.3, bass out 1:25.0, back at 1:28.6 | Raw drums: -41 (1:23), -66 (1:24), -76 (1:25). Raw bass: -30 (1:24), -76 (1:25). Informed times are slightly tighter; the difference is under half a second. |
| The drop | Kick on every beat, snare on alternate beats, mix up about 5 dB | Drums up about 50 dB, mix about +1 dB over pre-hole | Raw mix: -17.7 (60 to 80 s) to -15.4 (88 to 100 s), so +2 dB on the pre-hole average and about +5 dB on the hole seconds. The informed "+50 dB" is against silence and sounds bigger than it is; "+1 dB" is a little low. |
| 1:40.6 | Bass +10 dB, mix narrower, drier | Bass swell, mix +4 dB | Raw bass stem -25 to -15 dBFS; mix -15.4 to -11.8. Both. |
| 2:36.6 to 2:48.8 | "Wall rises 8 to 10 dB at 2:47 to 2:50" | Partial mute of the "other" layer at 2:36.8, body back at 2:48.8 | Informed (raw: "other" falls about 6 dB at 2:37, recovers by 2:49). |
| Plateau start | 3:36.6 (dense chops, pickup at 3:28.6) | 3:24.8 to 3:28.6 fragments begin; no step at 3:36 | Both partly. Voice stem: first burst 3:28.6; dense (50 of 60 s) from 3:36.6. Level: no step. |
| Peak | Loudest 12 s at 4:12 to 4:24; plateau about -10 to -11 | Loudest about 4:24 to 4:36 (12 s mean -9.9); per-second max -9.3 at 4:12 | Raw per-second maximum is -9.3 at 4:12, with -9.4 to -9.6 at 4:00 to 4:27; the plateau is broad, within 2 to 3 dB. Both agree there is no single peak; the blind "4:12 to 4:24" is closer to the per-second maximum, the informed 12 s mean peak is a smoothing choice. |
| 4:36.6 to 4:48.6 | Mix down 2 to 3 dB, bass chopped | Sag at 4:36.8: top band down 13 dB, bass 4 dB lighter | Compatible. |
| 4:48.6 to 5:00.8 | One bass stab and one voice-like call per bar | Same | Raw bass: -71.7 at 4:59, -22 at 5:00. |
| End | Stop at 5:00.86, three hits, zero at 5:04.24 | Stop at 5:00.8, "one" hit at 5:02.3, silence by 5:04 | Blind (raw audio: two clear hits and a third). |
| Key | B minor Aeolian (high) | B minor pad (M-H), first-loop bass ambiguous | Informed. |
| Tempo | 120 BPM; tracker's 161 is the hi-hat cross-rhythm (probable) | 120 BPM; 161 is the bass's three-sixteenth figure (H) | Both reject 161; the cause is unproved. |
| Voice | Late voice-like bursts, source unknown | Same; roughly half of about 29 fragments near the bar line | Same data, same uncertainty. |

**Where they differ, the data supports the informed run on the 2:36 to 2:50 passage, the 1:01 to 1:04 gap and the key calibration, and the blind run on the last hit and the 3:36.6 vocal-density change.** The disagreements are small (under half a second, or a few dB).

**Instrumentation.** Both say instrument identity is not recoverable (drum machine, bass loop, a wide pad, a voice-like layer). Neither invents a banjo, guitar or brass.

---

## 5. Which reads more like a person responding?

Honest answer: they are close, and both are written in the voice of a panel, not of a single viewer. Judged on the text:

- **Blind** reads more like a first response. It stays with what is on screen and in the sound: "a door opening onto people" at 1:28.6, "a trudge", "the loneliest moment" at 2:36.6, "a mechanism stopping is the only way a machine can grieve". The hedging ("if you go with it, hypnotic; if not, numb") is how an honest viewer talks. Its flaw is the flattening effect of over-caution. A person watching would just say "this is the Elfstedentocht", and the blind text never lets itself say so, which makes the piece feel more generic than it would to anyone who recognised it.
- **Informed** reads more like a prepared essay by someone who knows the history. It has more weight ("an inheritance: a dated blank into which each family writes a name"; "being left alone with a place after the people have gone") and a real account of how a Dutch viewer might feel. Some of that feeling comes from knowledge (127 finishers, 2012) rather than from the film, which the informed run's own sceptic noted.

Overall, the blind run is the closer match to a first-time viewer's felt response, and the informed run is the closer match to an informed viewer's. For the toolkit's stated goal (an understanding "as a human would feel and interpret it") the ideal is the blind run's grounded feeling plus the informed run's named subject, and neither alone is that.

---

## 6. Lessons for the toolkit

1. **Carry confidence forward, never down.** The blind perceive stage rated the Elfstedentocht sentence "high" and the final synthesis discarded it. Every stage (perceive, dossier, panel, synthesis) should keep an explicit tag (OBSERVED, HEARD high/med/low, INFERRED high/med/low, SPECULATED) and the synthesis prompt should forbid lowering a tag without a stated reason.
2. **Allow named inference in blind mode.** The blind rule "no research, no web" should still permit "I recognise this from my own knowledge". Add an "identification" step: list the top three candidate identifications (event, era, kind of production) with the clues that converge, give a confidence, and keep the identification as INFERRED instead of erasing it. Tell the synthesis agent that refusing to name a near-certain event is a defect, not caution.
3. **Add a convergence rule for ASR.** When several ASR passes give near-spellings of one proper noun, and other clues (place, number, distance, year) agree, treat the name as inferred high. Run a name-matching step against a short list of candidate proper nouns taken from the other clues (place plus year plus numbers), not just against the dictionary.
4. **Date the production from the signal.** Add a short "production era" check to the music reading: loudness (peaks near 0 dBFS), loop-machine regularity, sample-exact kick spread, stereo width, band-limited sample against a full-band mix. State "modern production over older material, medium-high" when they agree, and name the likely consequence (archive voice, new score). This closes the blind run's "date unknown" gap without any outside data.
5. **Separate the audio from the claims about the audio.** The 1 fps frames and the stems produced most of the fact-check's refutations. Rules for the toolkit:
   - Ask for per-second levels around every claimed event, and re-measure the drum stem, bass stem and full mix separately (a "silence" can be a rhythm-section dropout).
   - For the end of the track, always run a 10 ms envelope over the last 3 s, so hits are counted from the waveform and not from per-second RMS or from a stem pass.
   - Name the grid a statistic uses (kick-grid against tracker grid) in the output, and fail the check if the grid disagrees with the kick inter-onset interval.
6. **Make the shot detector's blind spots visible.** The detector missed a hard cut at 1:28.55, invented a dissolve cut, over-split colour-cycling shots and under-split fast shots. Add a second pass at higher frame rate around every music-section boundary, and have the dossier carry a "detector caveats" line by default. Any statistic that depends on shot lengths should carry the caveat.
7. **Do not read the ASR on instrumental stretches.** Whisper gave "Stuck", "End of the road" and "Fafn" over music. Mask ASR output where the vocal stem is quiet or where its content is non-speech (music bleed), and mark the rest "no usable words".
8. **Read the evidence for sections from the right stem.** The 3:36.6 boundary is invisible in the mix level and obvious in vocal-stem density; the 2:37 to 2:49 "rise" is a recovery from a dip. Add a "section-boundary evidence" table to the music reading that gives, per boundary, the change in each stem (level, density, brightness) and says which one carries it.
9. **Check pictures claims against the frame before the synthesis.** The flag's "dark lower band" was a pole; "hand-lettered" and "helpers steadying" were glosses. Add a rule that any colour, text or gesture claim in the final synthesis cites a frame number that the author opened, and keep a short "do not claim" list for common traps (fur, hand-lettering, a person's sex at 1 fps, the role of men in peaked caps).
10. **Run the informed pass second and diff it.** The most useful output of this comparison is the diff. Make the blind-versus-informed comparison a standard final step on every video, and use it to feed prompt fixes (as here). When informed and blind disagree on a measurement, the raw data decides, not the run that had more context.
11. **Guard the informed pass against its own priors.** Context raised the risk of reading history in (127 finishers, the 2012 cancellation, "50th anniversary" stated as fact). In informed mode, require every contextual claim in the opening paragraph to carry its source and its confidence from `context.md`, and ask the sceptic persona explicitly "which feeling here comes from the film, and which from what we were told?".
12. **Reduce the persona monoculture.** Both runs use the same six personas on the same dossier, so their agreement is weak evidence. For an unknown video, add one persona who has not seen the dossier (a "cold viewer" shown only frames and the music reading), which is the thing the blind interpretation itself lists as "not examined by anyone".
13. **Write the first paragraph last, in plain terms.** A blind synthesis should open with an "if I had to tell a friend" sentence that says what the thing most probably is (including inferred identifications), before any hedged detail. The blind video2 opening spends its words on gauge and lettering and never says "the Elfstedentocht, probably".
