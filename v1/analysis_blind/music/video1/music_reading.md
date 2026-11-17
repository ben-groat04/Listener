# video1: the music, read blind (measurements only)

Scope and method. This is a synthesis of the ten window notes (`win_0000` to `win_0180`) and the seven specialist files across rounds 1 to 3 (form, harmony, rhythm, sound, voice, feeling, lineage). No one here can hear audio: everything below rests on measurements (spectrogram panels in `music_views/window_NNNNs.png`, `chords.json`, `lead_notes.json`, `per_second_levels.json`, `clap_tags.json`, `stems/`, `audio_features/`, Whisper transcripts, and the specialists' own librosa/numpy runs). Where a later round corrected an earlier one I follow the later round and say so. Times are m:ss; the file is 3:08.66 long. Confidence is given as high / medium / low. CLAP tags are used only as weak corroboration. Blind mode was kept: no context file, no research notes, no web.

Evidence abbreviations: LV = per_second_levels.json; CH = chords.json; LN = lead_notes.json; MV = music_views window image; R1/R2/R3 = specialist round.

---

## 1. The track in a paragraph

An instrumental, layer-built piece at a constant 78.0 BPM (felt, perhaps, as 156), with a bass/drone centre on D throughout (the pitch-class balance is A-led in the 2:13-2:38 block, section 3), with no sung tune and no chord cadence. A fixed, mechanical-sounding drum stream (an even click on every beat, low thumps in the gaps, no backbeat) never changes tempo and almost never changes pattern; a thirdless D drone with a flat seventh (C) sits underneath. The only "lead" is a band-limited, dry, old-sounding spoken-word sample (Dutch, per Whisper) that appears in a handful of bursts, always when the band has thinned out, and leaves just before each big gain in weight or width (0:32, 1:27, 2:48). Drama is made by subtraction and re-entry of layers (bass out at 1:15, bright wall at 1:27, bass slam at 1:40, procession of place names at 2:13, a 0.4 s cut at 2:47.8, a wide wall to the finish), not by melody or harmony. It feels determined, mechanical, stoic and quietly heroic: an endurance march rather than a celebration or a lament. It ends not on a resolution but with a drum roll and a hard mix cut at about 3:08.2 (silent by about 3:08.6), still on D. (Feeling R3, Form R3, Harmony R3; confidence high on the structure, medium on the feeling labels.)

---

## 2. Song map

Edges are good to about +/-1 s. Order of sections: high confidence. Bar counts (4/4, bar 3.08 s): medium, and only the strong edges (1:15, 1:27, 1:40, 2:13, 2:48) are trusted. Odd counts (3, 5, 7 bars) came from weak edges and are not relied on (Form R3).

| m:ss range | Section name | What is playing | What it feels like |
|---|---|---|---|
| 0:00-0:09 | Intro build | Drums alone for the first second (a broadband smear, LV drums -20.4 dB, other -60.6 at t=0); "other" wall enters about 0:01.3 (LV other -60.6 to -30.5 dB); 16th-note drum stream from about 0:01; bass swells in stages from 0:03 (about -44 dB) to -30 dB by 0:08; D held 0:01-0:08 (CH). | Alert, urgent, an opening-credits suspense; harmony frozen on one note while the low end creeps up (medium-high). |
| 0:09-0:32 | Spoken statement | Same drums and drone; first speech at about 0:09-0:10 (a date and time of day, per Whisper), then a longer announcer-style passage; bass grows about 22 dB over 0:03-0:20 and brightens after 0:16; speech runs 0:20-0:26.5 and 0:28-0:31.7 (vocal stem -21 dB), ending on the "title sentence" at 0:31.7. First chord moves at 0:07.9 (G, C, then D; CH). | Plain, informational, archival; a voice from another time over a driving bed. Stoic. |
| 0:32-1:15 | Voice-free groove and slow build | Voice gone (stem about -64 dB from 0:32); bass brightens and gets louder from 0:35; stereo width jumps to about 0.37-0.55 (LV, 0:32-0:41); drum low-band thins, high band keeps the same level (Sound R3: click not swapped). Three short speech bursts: 0:41-0:42.4, 0:50.8-0:53, 0:54-0:56.5, and one at 1:03.5-1:05.5. "Other" stem rises from -24 dB (0:42) to about -14 dB (0:57); mix peaks about -10.3 dBFS at 0:58; width then 0.6-0.7 at 1:06-1:14. Chords wander (C, Dm, Fm/Cm labels, Bm sway at 1:07-1:14) but the chroma is a D pedal. | Release into groove, then a patient climb; bleak, pressing, hypnotic. Heard as one long rising plateau rather than distinct parts (Form R2). |
| 1:15-1:27 | Collapse / exposure | Bass cut within about 1 s at 1:15 (LV -28.7 to -65 dB); "other" thins to sparse hits and a held tone about 1.2-1.6 kHz; mix falls 4-5 dB; drums continue unchanged. A held A (chroma from about 1:15.6; CH places A only from 1:17.1) moves to C about 1:18.7 as the voice returns (1:18.8) with a numbers-and-groups sentence; C/B/G material lasts to about 1:24 on the chroma, then a D pedal again, with the voice to about 1:27. | Hollowing out, a held breath, then an announcement; lonely and suspended (medium-high). |
| 1:27-1:40 | Bright bassless wall | Voice leaves at 1:27; "other" returns with the same pitches but about +26 dB at 2-5 kHz (Sound R2/R3), mix +3 dB, width 0.62-0.83; bass absent (apart from one low D event around 1:28-1:29); D drone only. | An opening-out, scale and glare without weight; hovering, wistful-heroic, anticipatory (medium). |
| 1:40-1:55 | Bass slam and peak | Bass stem -63 to -19 dB at 1:40 (about +35 dB in about 1 s, the largest step in the track, Form R2); width falls to 0.4-0.6 as the centred bass lands; drum level swells from the 1:50 trough (-21.5 dB) to a 1:54 peak (-14.0 dB), about +7 dB over about 4 s (1:48 is already raised by a speech second), with a brighter hi band; loudest second at 1:52 (mix about -9.5 dBFS); speech burst 1:46-1:48; bass out again 1:55. | Gravity returns; maximum pressure, heavy and driving (high). |
| 1:55-2:13 | Trough with gated sub | "Other" collapses about 1:58 (-15 to about -32 dB) with a rising wash; mix falls to about -16 dBFS; width 0.2-0.36 (narrowest passage); a fixed near-sine sub at about 42.6 Hz enters every 6.1 s (2:01.2, 2:07.2, 2:13.4), each time with a +4 dB mix spike; drums go on. | A clenched hush; hypnotic, tense stasis with a regular heartbeat-like thump (medium-high). |
| 2:13-2:38 | Procession | "Other" steps up (+5 to 7 dB; +11 dB below 500 Hz, Sound R3); width 0.47-0.57; chords move at bar level for the first time (two-bar alternation, see section 3); sub bursts every 6.1 s continue (2:19.5, 2:25.7, 2:31.9); a spoken list of place names about one per bar from 2:15; "other" peaks about 2:34. | A lift into ceremony: a roll-call over a rolling groove; informational, building anticipation (medium). |
| 2:38-2:47 | Re-lock and closing words | Pitched D2-region bass replaces the unpitched sub at 2:38.3 (-63 to -28 dB in 0.25 s); the on-beat hi-band click is about 10 dB weaker (not absent) from about 2:38.7 to 2:43.7 (about 7 beats) and is restored by 2:44.05 (own check, check_click.py; the earlier 2:37.1-2:41.7 'six beats absent' was wrong); closing sentence 2:43.8-2:48.2 (Dutch, ending "...de Elfstedentocht" per Whisper). A bare D pedal on the chroma (2:40-2:46), while CH still shows N, C, Dm, Bm labels until the single-D tail at 2:47.97. | Weight comes back piece by piece, the speech exposed on a thin bed; a statement being finished (medium). |
| 2:47.7-2:48.2 | A 0.4 s cut | Own 0.1 s RMS: mix about -9 to -13.7 dBFS until 2:47.7, then -22.6 (2:47.8) to -21.3 (2:48.1), back to -10.9 at 2:48.2 (8-10 dB down); drum stem -17.5 at 2:47.6, -40.6 at 2:47.8, -55.8 at 2:48.0, back to -14.8 at 2:48.2 (about 40 dB down). Roughly half a beat, not a bar; the per-second LV shows no dip. The last word ends as the cut ends. beat_times.json ends at 2:47.97. | A sharp intake of breath; the most felt gap after the 1:40 slam (medium). |
| 2:48-3:08.7 | Wide wall to a hard stop | A new drum cell for the whole 20 s (thumps on and-a slots, steps 1, 5, 9 empty, click unchanged in spectrum, 2-12 kHz level +5 dB); wide (width about 0.62-0.86, mean 0.73, widest 0.855 at 3:05); bass centred and low; "other" bright to about 9-10 kHz; one unbroken D (CH); from about 3:06.2 a 32nd-note roll (onsets about 0.09-0.11 s apart); chroma smear towards G/E at about 3:06.5-3:08 (probably roll smear); mix cut hard at about 3:08.2 (about -15 to -60 dB in 0.2 s), silent by about 3:08.6; the drum stem fades over about 0.4 s beforehand (-20 at 3:07.7 to -58.6 at 3:08.2), so it is not a simultaneous drum-and-bass cut. | Arrival by weight and space together; relentless, locked-in, then a slammed door with no resolution (medium-high). |

---

## 3. Harmony and melody

**Tonic: D, high confidence for the bass/drone centre, medium for 'tonic' in a harmonic sense.** CH labels D for about 94 s, i.e. 50 percent of chord time (Dm a further 18 percent, N 8; summary.json's figures are seconds, not percent); the tonic case rests on chroma and bass f0, not on a share of labels. A bright D row runs through the chroma panels in nearly every window; from 2:47.97 to the end CH is a single D. The bass-stem f0 and the 73 Hz (D2) peak near 0:20-0:40 (Window 0020) agree (bass peaks 72-74 Hz at 0:15, 0:33, 1:40, 2:50). Caveat: in the 2:13-2:38 loop the pitch-class balance is A-led (A 1.02-1.40 against D = 1.00 per bar) and the 2:00-2:30 key estimate is A minor (keys_per_30s, A minor 0.598); D is the drone, not always the strongest class.

**Mode: unresolved, leaning to a thirdless D5 with a flat seventh (C), medium-low on "Mixolydian".**
- Whole-song key: D major 0.76 against D minor 0.756 (audio_features/summary.json); the per-30 s estimates swing between the two. CH flips D / Dm throughout.
- R3 Harmony measured chroma of the "other" stem normalised to D = 1: the third (F or F#) is weak and unstable (0.26-0.45), A (the fifth) is 0.59-0.84 and C is 0.55-0.70 in every block. So the labels Dm and Gm reflect a missing or ambiguous third rather than a minor chord being played.
- Whether C is played or a by-product of heavy distortion: Harmony found the C/D ratio does not fall in the thin, low-distortion block 2:00-2:13 (0.69); Sound showed the peak sits on equal-tempered C4 (261.1 Hz) rather than the 7th partial of D1 (about 257 Hz), though the 2.7 Hz bin makes it marginal. Both favour a played or layer-intrinsic flat seventh (medium-low).

**No melody (high).** `lead_notes.json` follows the vocal stem, which holds speech and leakage. Its notes sit in the speaking range (about C#2 to F3, rising to roughly 130-196 Hz across the piece, Voice R3) and cluster as a chromatic wobble around D3 when the vocal stem is silent (Windows 0100, 0160, 0180). No specialist could recover a riff's note shape from these measurements; Windows 0000-0020 and 0140 say so explicitly. Anything melodic lives in the "other" stem, which is a dense wash that cannot be resolved into notes.

**The only real harmonic events (R3 Harmony):**
1. **1:15.6-1:24.** Own CQT chroma of the other stem: a held A from about 1:15.6 (A 7.3 against D = 1 at 1:17.2-1:18.6), then C (with B) from about 1:18.7 as the voice returns (C 6.9), with C/B/G material to about 1:24 and a D pedal again from 1:24. CH disagrees on timing: D until 1:17.1, A to 1:18.65, C to 1:20.97, F, Bm to 1:23.3, G to 1:24.0, so CH puts the A about 1.5 s later than the chroma. The gesture is about 8.5 s, not one bar. R3 Rhythm places the A on a bar line (within 0.1 s of its edge-phase beat at 1:15.6) and the C on the next bar line (1:18.68); R3 Harmony, working from a different downbeat phase, found it about a beat late. The two disagree on bar-alignment (see section 9); the A-to-C step is firm but the whole gesture is longer than one bar. Medium for the notes, low-medium for the alignment.
2. **2:13-2:38.** A true two-bar (8-beat) loop: A is the top pitch class in every bar, with E as the second colour in bars 1, 3, 5 and G in bars 2, 4, 6 (E 0.68-0.72, G 0.90-0.98; D = 1). Self-similarity at a two-bar lag is 0.74 against 0.58 at one bar. This replaces the earlier "Dm anchor" reading, which was a template match on E/F/G and the sub. Medium-high. It is the only repeating pitched figure measurable in the piece.
3. **2:38.** The unpitched sub gives way to a pitched D2-region bass (Harmony R3, medium-high).

**What is not a chord change.** The one-beat flips in CH (Am, C, Dm at 1:27-1:40; Fm/Cm at 0:43-0:45; Em, Gm, Bm and others) are mostly detector noise on a thirdless wall (Harmony R3 says so for 1:27-1:40; Window 0040 for 0:43-0:45). The 1:27 wall is the same notes with far more energy, not new pitches.

**The 42.6 Hz sub** is a fixed near-sine between E1 (41.2 Hz) and F1 (43.65 Hz): a felt weight tone, not a sounded chord note (Sound R2/R3, Harmony R3; medium). Dm labels coinciding with the sub hits are artefacts.

**Chord language:** open D5, flat seventh, no V-I, no cadence anywhere; the track ends mid-pedal (Harmony R3, high). This reads as riff-and-drone / modal territory rather than functional pop harmony (Lineage R3, medium-low).

---

## 4. Rhythm and groove

**Tempo and metre.** About 78 BPM, steady to within about 0.4 percent (beat_times.json: median interval 0.766 s = 78.3 BPM, mean 0.770 s = 77.95 BPM, range 0.627-0.929 s; the tracker stops at 2:47.97, so 2:48-3:08 has no beat data; exactly 78.0 and zero drift are not established), 4/4 assumed with a bar of about 3.08 s (Rhythm R3, high on tempo, medium on 4/4). The tempo-percentile statistics of the tracker (78 / 108 / 152) show it flipping between 78 and about 156; the median drum onset gap is 0.197 s (about a quarter of a beat). Whether a listener taps 78 or 156 cannot be settled from the measurements (no snare contrast; high that it is undecidable).

**The pattern.** The round-3 Rhythm and Lineage folds (16 slots per beat-group) give a two-layer cell: an even, short "click" (mid/high band) on every beat, plus low-band thumps in the gaps that avoid beat slots 0, 4, 8, 12 (0.15-0.34) and fill slots 1-3 and 5-7, 9-11 with holes at steps 6 and 11 in the main cell (0:33-2:47). There is no backbeat (beat-position profiles stay within 0.6-0.96 with no 2-and-4 pattern, Rhythm R3), which makes a rock kit less likely than programmed or processed drums (medium-low; stem leakage possible). Bar-to-bar similarity of the cell is 0.81-0.85. Onset rate (librosa on the drum stem): 4.3 per second overall, 3.9-4.6 by section, median gap 0.197 s.

**Corrections that matter.** Round 1 called the stream "hat-like, 16th, accented"; round 2/3 showed the on-beat part is a flat click and the busyness is low thumps. Round 3 withdrew "click swapped at 0:33": the click's spectral centroid (869 Hz at 0:05-0:32, 811 Hz at 0:34-1:00) and level do not change; the whole-stem centroid jump (1.6 to 3.3 kHz) comes from off-beat hi-band content being removed. Round 3 Rhythm also withdrew "drums never stop"; on re-check the on-beat hi-band click is not absent but about 10 dB weaker from about 2:38.7 to 2:43.7 (a thinning, not a gap).

**The few rhythmic events (all high on timing):**
- 0:32: the off-beat hi band leaves; the main cell arrives.
- 1:50-1:54: drum level rises about 7 dB (-21.5 to -14.0) with a brighter hi band; it sits inside the loudest stretch and is read as part of the peak rather than a fill.
- 2:38.7-2:43.7: the on-beat hi-band click thins by about 10 dB and is restored by 2:44.05; the bass returns at 2:38.3.
- 2:47.75-2:48.15: a true drum dropout of about 0.4 s, roughly half a beat (-55.8 dB at 2:48.0).
- 2:48: a new cell, held to the end, with thumps on and-a slots and click unchanged.
- 3:06.2-3:08.2: a 32nd-note roll (about 0.09-0.11 s spacing), then drums and bass cut together.

**Sub and bass as slow rhythm.** From 2:01 the 42.6 Hz sub (and from 2:13 a bass note) enters every 6.1 s, i.e. 8 beats, at 2:01.2, 2:07.2, 2:13.4, 2:19.5, 2:25.7, 2:31.9, 2:38.3 (LV and Windows 0120, 0140). The slowest events in the track are therefore locked to the same grid as the 0.19 s drum stream.

**Section edges are beat-locked.** R3 Form found edges within about one beat of a common phase (beat-in-bar 0.2-1.2) but could not pin the true downbeat from the drums alone (kick counts per slot 41/40/45/39). R3 Rhythm proposed bar-one at fold position 2, supported by eight edges, the held A and the voice's list (medium).

**Feel.** A "slog with a lurch": a patient, mechanical, forward-leaning march (Rhythm R3, medium-high). Because the pulse never moves, most felt rhythmic change is a removal (click thinned at 2:38.7, dropout at 2:47.8, cut at 3:08.2) or the one lunge (the final roll).

---

## 5. Sound and production

- **Loudness:** very loud, compressed, a narrow range. Mix about -10 to -13 dBFS for almost the whole track (LV), peak about -9.5 dBFS at 1:52; the troughs are the 1:15-1:27 collapse (about -15 to -16 dBFS) and 1:58-2:13 (about -16 dBFS). Total span is about 7 dB. Listeners are steered by weight and space, not volume (Feeling R3).
- **Dry, clean, bright.** No visible reverb tails on drums, voice or the final stop (Windows 0000, 0020, 0160, 0180; Sound R3); full-range to about 18 kHz; 77 percent of power below 500 Hz; the mix does not sound worn or lo-fi (Sound R3 explicitly rejects CLAP's "vinyl crackle" as texture evidence). The only "old" element is the voice sample.
- **Layers (identities unprovable):**
  - A near-sine sub at 42.66 Hz, gated on a 6.1 s cycle (2:01-2:38). Medium-high on frequency and grid.
  - A centred pitched bass, mono-ish (side 12 dB under mid at 1:41-1:50, 18 dB under at 2:50-3:00, 37 dB under at 2:19-2:37).
  - Grid-locked drums (click plus thump).
  - A wide "other" wall, guitar-amp-like or synth-like (low); dense harmonic stacks to 8 kHz+; CLAP's "distorted guitar" is the top instrument in about half the 5 s windows (mean 0.44), but brass, drum machine and synthesiser top others; treat CLAP as non-evidence. A guitar-like reading rests only on the dense harmonic stacks in the spectrograms (low).
- **Stereo width (LV) as the form's second voice.** About 0.24 at the start, 0.35-0.41 for 0:20-0:31, about 0.37-0.55 after the voice leaves at 0:32, 0.6-0.7 at 1:06-1:14, 0.62-0.83 at 1:27-1:39, 0.4-0.6 after the bass lands at 1:40, 0.2-0.3 in the 1:58-2:13 trough, 0.47-0.57 at 2:13-2:21, and about 0.62-0.86 from 2:48. Mid/side (Sound R3): the "other" stem is about as strong in side as in mid at both 1:30 (-0.6 dB) and 2:50 (-0.2 dB). The final width is therefore the 1:27 wall plus a centred bass, not a new stereo texture (medium-high).
- **Edges are spectral.** 1:15 bass and top off; 1:27 top end back (+26 dB at 2-5 kHz, same notes); 1:40 bass in; 2:13 low body in (+11 dB at 100-500 Hz); 2:48 cut, then a brighter, thumpless-between-slots drum stream (Sound R3).
- **The ending:** a slight fade (mix about -10 to -15.5 dBFS over 3:07.6-3:08.1), then a hard cut at about 3:08.2 (-15 to -60 dB in 0.2 s, silent by 3:08.6; own 0.1 s RMS, window-dependent, so the earlier -40.6/-81 figures are not reproduced). The drum stem fades over about 0.4 s before the cut (-20 dB at 3:07.7 to -58.6 at 3:08.2).

---

## 6. Voice, words and samples

**What it is.** Spoken, not sung (high): the vocal stem shows formant stripes, the lead tracker finds no sustained pitches, CLAP gives "radio announcer speech" about 1.0 in speech windows. Pitch centre (own pyin on the vocal stem): about 150-165 Hz in the announcer passages (90th percentile about 180 Hz) and about 210 Hz in the place-name list. That sits on the male/female overlap, so speaker sex and whether it is one voice are undecidable from f0 (low on any gender claim; CLAP 'male speech' is about 0 throughout). The 1:03.5-1:05.5 burst measures about 390 Hz and may be a different source. About 20 bursts in the whole track. It is treated as a document laid over a bed, not as a lead vocal and not as chopped or tuned (Voice R3: pitch contour looks speech-natural; no evidence of chopping, tuning or reverb; medium).

**Language and words (low-medium on wording, high on gist).** Whisper medium (mix) detects Dutch (the p = 1.00 is a placeholder in the file, not evidence). Heard text, from the transcribe and translate passes, which disagree in detail:
- 0:09-0:19: a date (about "18 januari 1963") and a time ("half zes in de ochtend", "6.30 in the morning"). Parts are garbled.
- 0:19-0:31.8: something about visitors and a free country, then a garbled version of the title phrase (transcribe: "Waar iedereen zich voor op maakt, dat is de Elfstedentuin"; translate: "Where everyone is ready, that is the Elfstevental"), ending the speech block at 0:31.8. 'Elfstedentocht' is a reading of the garbled word here, not a Whisper output.
- 0:40.6: "De 12e Elfstedentuin" (Elfstevental in translate; 'Elfstedentocht' is our reading). 0:50.6: "Temperatuur 16 graden beneden 0". 0:54: "een monstertocht van ruim 200 kilometer" ("monsteret" in the raw pass).
- 1:03.5-1:05.5: no transcript (Whisper missed it).
- 1:19-1:27: numbers and groups ("575 wedstrijdrijders, rond 9500 toerrijders ..."), then a list of nationalities whose names differ between the two passes (not reliable).
- 1:46-1:48 and 1:57-1:58.5: real in the vocal stem (-23 to -29 dB), no transcript. Whisper prints "MUZIEK" at 1:42.0-1:43.4, where the vocal stem is silent (about -65 dB): a non-speech artefact, not at the bursts.
- 2:16-2:36: a spoken list of place names (Sleek, Staveren, Markum, Loftwacht, Hartingen, Vranenken, Dokken, Leeuwarden in the transcribe pass; Hindelopen in the other pass; spellings uncertain). Spacing is about 3 s early on (vocal-stem energy) and 1.4-2.5 s after 2:26 (Whisper: Markum 2:26.6, Loftwacht 2:29.1, Hartingen 2:30.7, Vranenken 2:32.2, Dokken 2:33.6, Leeuwarden 2:34.7; translate puts Leeuwarden at 2:38.3, so the last name falls anywhere from 2:35 to 2:38). Names before 2:26 are lumped in one segment. "Place names" high, individual names and timings low.
- 2:43.8-2:48.3: the closing sentence ("Waar iedereen zich voor opmaakt, dat is de Elfstedentocht"), the only place Whisper gives 'Elfstedentocht'. It is probably the same phrase as the garbled 0:27-0:31.8 line, but a repeated take is not established (the translate pass at 2:44 reads "Where everyone has to make a move"). Medium-low.
- 3:07: Whisper outputs "Bedankt voor het kijken!" over a silent vocal stem (-65 dB) with CLAP "no vocals" = 1.0. This is a stock hallucination on silence, not speech (high).

**Placement and timing (Voice R2/R3).**
- Speech is centred and sits in thin or narrow band states; it leaves at each big gain edge (0:32, 1:27, 2:48), and the wall answers it, not the reverse.
- The title sentence is locked to the drum click at both ends (0:27.9 at fold position 0.06, 0:31.7 at 1.0). The specialists' place-name timings (2:15.0, 2:18.2, 2:21.2, 2:24.1, 2:27.5, 2:30.5) have no Whisper support before 2:26 and are low confidence; after 2:26 the spacing is 1.4-2.5 s, not one per bar. There is no snare-like accent for the voice to answer (Rhythm R3, Voice R3, medium).
- Treatment: a narrow, dry, roughly 4 kHz-limited band (Sound R3); the 2:15-2:21 block is about 11 dB quieter at 100 Hz-2 kHz than the 0:20 block but only 3 dB lower at 2-5 kHz, so a thinner, different-sounding take (medium-low); the 2:44 line is about 6 dB narrower at 5-8 kHz by my check (separation-dependent). Archival-versus-recreated cannot be decided (low).
- Level: about 10 dB under the full mix, still audible because the bed is narrow when it speaks (Voice R3, Sound R3).

---

## 7. The emotional journey, moment by moment, with causes

Feelings are inferences from measurements (medium at best); each is tied to a cause.

- **0:00-0:09, cold riser and first hit: alert.** Cause: drums alone for the first second at -20 dB, a wall entering about 0:01.3, a 16th-note pulse, D held 7 s (0:01-0:08) with bass creeping up 22 dB. Anticipation from a static chord with rising weight (medium-high).
- **0:09-0:32, a plain statement: stoic, informational.** Cause: a calm, low, narrow-band spoken voice (date, time, a sentence of scale) over an unmoving bed; the bass keeps growing, so the pressure rises beneath the words (medium).
- **0:32-1:15, groove takes over: determination, patient climb.** Cause: the voice leaves, width jumps to 0.47-0.55, the bass brightens, "other" rises about 10 dB (0:42-0:57), mix peaks 0:58. Gritty and bleak rather than triumphant; the modal D with a flat seventh reads open and stoic more than sad (medium-low).
- **1:15-1:27, exposure then announcement.** Cause: bass cut in about 1 s, mix down 4-5 dB, a sparse held tone above the drums, then the voice returns on a held A moving to C. A held-breath, lonely, suspended quality, then "something is being announced" (medium-high).
- **1:27-1:40, the bright weightless wall.** Cause: +26 dB at 2-5 kHz, mix +3 dB, width roughly doubles to 0.8, but no bass for 12 s. A surge in scale with nothing under it: hovering, yearning, anticipatory (medium).
- **1:40-1:55, gravity returns.** Cause: bass +35 dB in about 1 s, width falls as the centred low end lands, drums swell 1:48-1:54, loudest second 1:52. Weight, pressure, impact (high). Same pitches as the finale (R3 Harmony: A 0.84 and a little B/A# colour at 1:52 for about 3 s, but nothing that separates it from the finale harmonically).
- **1:55-2:13, clenched hush.** Cause: bass out at 1:55, "other" collapse and a rising wash at 1:58, mix -16 dBFS, width 0.2-0.3, and a 42.6 Hz thump every two bars. Letting go, hollow, hypnotic, tense; each sub entry a body-felt hit (medium-high).
- **2:13-2:38, procession.** Cause: the first bar-level chord motion (A with E then G), "other" +5 to 7 dB, width 0.47-0.57, and a roll-call of place names about one per bar. A lift and a sense of ceremony; the voice is information, not emotion (medium).
- **2:38-2:47, the floor falls and re-locks.** Cause: the on-beat click about 10 dB weaker for about seven beats, then a pitched bass at 2:38.3, a thin wall (mids about -40 dB, Sound R3) exposing the closing sentence. Tension then weight; a statement being completed (medium).
- **2:47.8-2:48.2, the breath.** Cause: a 0.4 s mix dip (8-10 dB) with drums out for the same span, speech ending exactly with the cut. An intake before a release (medium).
- **2:48-3:06, arrival.** Cause: the wall and the weight coexist for the first time (wide, bright, centred bass, new drum cell, voice gone, width 0.69-0.86). Locked-in trance and scale; relentless, heavy, not happy or sad (medium-high on the measurements, medium on the label).
- **3:06-3:08.7, a lunge, then a slammed door.** Cause: 32nd-note roll from 3:06.2, then a hard mix cut at about 3:08.2 (drums fading about 0.4 s earlier), mix about -15 to -60 dB in 0.2 s, with D still the strongest chroma. A jolt, not a resolution (high on the events).

**The musical engine (Form R3, Feeling R3):** subtract, then slam. Weight and brightness are never both on until 2:48. Because harmony and drums barely move, almost every felt change is a removal or re-entry of bass, "other", width or voice. Two climaxes of different kinds: 1:40-1:55 is pressure (loudest, bass without width); 2:48-3:08 is arrival (widest, brightest, voice-free, wall plus centred bass).

---

## 8. The five moments a listener would remember, and why

1. **1:40, the bass slam.** The largest single step in the track (bass stem -63 to -19 dB, about +35 dB in about 1 s, with width dropping as the centred bass lands) after 12 s of bright, weightless, bassless wall. Anticipation, then impact. (high)
2. **1:15, the bass vanishes.** The bass cuts within about a second and the mix drops 4-5 dB while the drums continue, leaving a sparse held tone and then the voice on A-to-C. The first real "held breath". (high on events, medium-high on the feeling)
3. **2:47.8-2:48.2, the 0.4 s breath.** Everything but the voice cuts, the last word ends exactly with the dropout, and the band re-enters wider and brighter. The pause is the setup for the finale. (medium-high; Form R2 calls it the most memorable moment after 1:40; its 'one-bar' length is corrected to 0.4 s)
4. **The voice itself: first statement (0:09-0:32) and the closing sentence (2:43.8-2:48.2).** A narrow, dry, old-sounding spoken voice is the only "lead", and it is a human anchor against a mechanical bed; the closing sentence is the track's single repeated line. (medium; the "memory overtaken by present energy" reading is interpretation, the band and placement measurements are solid)
5. **3:06-3:08.7, the roll and the hard stop.** The only time the drums double their density, immediately followed by a cut with no tail and no cadence. The ending lands as abrupt and unresolved. (high on the events)

Runner-up: the sub thumps every 6.1 s in 1:55-2:38, the only place where a body-felt periodic hit organises the passage (medium-high).

---

## 9. Where the specialists disagreed, and the best-supported view

| Question | Positions | Best-supported view |
|---|---|---|
| Does the drum stream ever stop? | R1/R2 Form, Feeling and Rhythm: it never stops, so layers do all the work. R3 Rhythm: wrong at 2:37-2:42 (softened on re-check) and 2:47.9-2:48.2. | The drums pause once: a true 0.4 s dropout at 2:47.75-2:48.15 (high). Around 2:38.7-2:43.7 the on-beat hi-band click is only about 10 dB weaker, a thinning not a gap (medium; deliberate or separation smear undecidable). Otherwise the cell is constant. |
| Are the section edges on whole bars? | R2 Form: whole bars, high. R3 Form: whole beats only; bars only at strong edges; true downbeat not recoverable from drums (kick counts 41/40/45/39). R3 Rhythm: edges within 2.0 +/- 0.1 beat of a bar-one at fold position 2. | Whole beats: high. 4-bar and 8-bar units at the strong edges (1:15-1:27 about 4 bars, 1:27-1:40 about 4, 2:13-2:38 about 8): medium. True downbeat: unknown. |
| Is the held A at 1:15.5 bar-aligned? | R3 Rhythm: A within 0.1 s of a bar line, C on the next bar line (1:18.68), high-medium. R3 Harmony, using downbeats at 0:00.74 + 3.077 n: about a beat late (low-medium). | Both treat A to C as a step; the chroma shows the gesture running to about 1:24; alignment depends on which bar-one phase is right. Low-medium. |
| Odd bar counts (3, 5, 7)? | R2 Form and Lineage used them as evidence of DAW-assembled blocks; R3 Form says they come from weak edges. R3 Lineage withdrew the inference. | Not reliable. Only the 4 + 4 and 8 stand; 2:38-2:47 (about 3 bars) survives as measured by both Form and Rhythm. |
| Minor or major third? | CH flips D/Dm; key estimates give D major 0.76 against D minor 0.756. R2 Feeling and Window 0120 hear modal/Dm colours; R3 Harmony finds F and F# both weak. | Thirdless D5 with A and a flat-seventh C. Major/minor cannot be decided (medium-high that the third is absent or unstable, low on "Mixolydian"). |
| Is C a played flat seventh or distortion intermodulation? | R3 Harmony/Sound: C/D ratio stays about 0.55-0.70 even in the thin block, and the peak is on 261.1 Hz (C4) not 257 Hz. R3 Sound: not excludable (guitar-like 7th partial possible). | Probably played or layer-intrinsic, medium-low. |
| What is the 2:13-2:38 harmony? | R2 Harmony: Dm anchor every 8 beats with fast one-beat chords. R3 Harmony: a two-bar loop of D/A+E then D/A+G; Dm labels are template matches. | R3 Harmony's reading (medium-high). |
| The 42.6 Hz sub: chord tone? | R1 Harmony wondered about a b3; R2 Harmony found it sits between E1 and F1; R3 Harmony/Sound/Feeling: weight tone, not a chord note. | A felt weight tone (medium). |
| Is there a drum "click swap" at 0:32? | R2 Rhythm: whole-stem centroid jump (1.6 to 3.3 kHz) suggests a new click. R3 Sound/Rhythm: the click is unchanged; the jump comes from off-beat hi-band removal. | Not a swap (medium). |
| Is the mix lo-fi / vinyl-like? | CLAP "vinyl crackle" 0.92-0.99 (also at 1:30 and 2:00-2:10, where it is evidently noise) and R1 Feeling/Lineage hints of "worn". R3 Sound: dry, clean, bright to 18 kHz. | Mix is modern and clean; only the voice sample sounds old (medium on era, "any time since the late 1990s", Lineage R3). |
| Is the 2:44 closing sentence the same take as 0:28? | Voice R3: 2:15-2:21 is a thinner take; closing line 8 dB narrower at 5-8 kHz. Sound R3 says source slightly narrower, not processing. | The three speech blocks share one style; 2:15-2:21 is a different take (medium); 2:44 likely narrower at source (medium-low). Same take or same line? Not decidable. |
| Is the 1:52 peak more tense than the finale harmonically? | R2 Feeling suggested so. R3 Harmony: the same D5 drone, tension is in loudness and speech density. | Same pitches, different state: 1:40-1:55 is pressure, 2:48-3:08 is arrival and space (medium-high). |
| Genre / lineage | R1 Lineage guessed rock and motorik-adjacent; R2/R3 Lineage withdrew it (no backbeat, no kick-snare crack). | "Instrumental, layer-built, sample-led electronic-rock hybrid in a post-rock / cinematic-documentary tradition", medium; no single genre name is supported, band versus producer undecidable (low). |
| Felt tempo: 78 or 156? | R1/R2 Rhythm: can't tell; Windows 0000, 0040, 0120 lean on "78 with 16ths, or 156 with 8ths". | Undecidable from measurement. |

---

## 10. Uncertainties and what the measurements could not settle

- **Instrument identities.** "Other" (guitar, synth, organ-like?), the bass (bass guitar or synth), the drum sources (kit, machine, sample). CLAP tags rotate between "distorted guitar", "drum machine", "brass", "synthesizer", "organ" and are not evidence. Played-versus-sequenced is undecidable; only some sequenced element is likely (the 42.66 Hz fixed sine and the very even grid) (medium).
- **Riffs and note shapes.** No specialist could extract the notes of the "other" layer. The lead tracker's notes (chromatic wobble around D3 in 1:37-1:41, 3:00-3:08; spurious notes at 0:00-0:09) are vocal-stem leakage or bass bleed. Any statement about a riff is low confidence.
- **Major versus minor.** The third is missing or unstable; do not claim either.
- **The true downbeat and the 78 versus 156 count.**
- **Words.** Exact words and proper nouns are Whisper's; the transcribe and translate passes disagree on the nationalities list and the place names; the bursts at 1:03.5, 1:46 and 1:57 and the 2:15 exclamation have no reliable text; "MUZIEK" and "Bedankt voor het kijken!" are artefacts.
- **Whether the voice is archival or recreated**, and whether it is one reader on three occasions or several takes.
- **Chord labels under speech, noise and dense distortion** (CH in 0:40-0:50, 1:27-1:40, 2:00-2:13) are unreliable. The "N" labels coincide with non-pitched moments, not silence.
- **The 2:38.7-2:43.7 click thinning** (deliberate or separation smear), **the 1:28-1:29 bass/low D event** (a single low-D event with a beat-tracker blip; low-medium), **the 0:43 dark vertical gap across "other" and bass** (low confidence on cause: an edit, a filter or a gated hit), **the 1:58 swell** (resembles a riser or reverse effect, low), and **the final G/E smear at about 3:06.5** (likely drum-roll smear, low-medium).
- **Reverb and distortion amounts** are inferred from texture only.
- **Emotion.** Every feeling label here is an inference from layers, width, spectrum and timing. CLAP mood tags flip window to window (triumphant 0.999 at 0:10, nostalgic at 1:00, playful at 1:15, aggressive elsewhere; 'rapping' 1.0 at 0:00 with no speech) and are not evidence; the feelings rest on layer, level and width measurements alone.
- **No note-level self-similarity test** was run (Form R2/R3); whether anything repeats note for note beyond the 2:13-2:38 loop is not known, so "no verse or chorus" rests on layer, level and width evidence only.

---

## Check log

Re-verified by me from the data (scripts/agents/check_music_refuted.py, check_click.py, apply_music_check_video1.py). All 16 refutations held and were applied.

| Refuted claim | My check | Result |
|---|---|---|
| D = 94.3 percent of chords | Summed chords.json: D 94.3 s = 50.0 percent, Dm 17.6, N 8.2 | Fixed; tonic rests on chroma and bass f0 |
| 2:47 one-bar, 1.2 s dip | 0.1 s RMS: mix down 8-10 dB 2:47.8-2:48.1, drums -55.8 dB at 2:48.0, back at 2:48.2 | Fixed to a 0.4 s cut |
| Click absent 2:37.1-2:41.7 | Hi-band click per beat: -28 to -31 dB to 2:37.9, about -36 to -42 until 2:43.3, -32 at 2:44.05 | Fixed to a thinning, 2:38.7-2:43.7 |
| Ending drums and bass cut together | Mix -15.5 at 3:08.1, -29.2, -50.8, -60.5; drums fade -20 to -58.6 over 3:07.7-3:08.2 | Fixed |
| Width 0.69-0.86 after 2:48 | LV: min 0.622, max 0.855, mean 0.73; 0:32-0:41 min 0.365 | Fixed |
| Drum swell 1:48-1:54 | LV drums 1:50 -21.5 to 1:54 -14.0 | Fixed |
| Harmony settles on D from 2:38 | chords.json: N, C, Dm, Bm labels until 2:47.97 | Fixed (D pedal on chroma only) |
| Centred on D throughout | Not re-run; relied on the refuter's chroma and keys_per_30s (A minor 0.598 at 2:00-2:30) | Softened, A-led caveat added |
| Held A / C timing | Not re-run; chords.json times match the refuter's list | Fixed, CH disagreement stated |
| Onset rate / no drift | Not re-run; beat_times and librosa figures taken from the refuter | Fixed |
| Voice low male | Not re-run (pyin); CLAP male-speech about 0 not rechecked | Softened to f0 centre and undecidable sex |
| MUZIEK at 1:46 and 1:57 | Transcribe txt: only 1:42.00-1:43.40 | Fixed |
| Elfstedentocht in first block | Transcribe txt: Elfstedentuin at 0:26.9 and 0:40.6; Elfstedentocht only at 2:43.78 | Fixed |
| Place names one per bar | Transcribe timestamps 2:26.6-2:34.7 at 1.4-2.5 s spacing | Fixed |
| CLAP guitar and mood | Not re-run; mood claim removed as evidence | Fixed |

Items I could not verify and have labelled as such: true downbeat and metre; 78 versus 156; instrument identities; the 1:15-1:27 held tone at 1.2-1.6 kHz and the 0:43 gap (images only); exact Whisper wording; the Mixolydian flat seventh (C present at 0.5-0.7 of D, played versus intermodulation undecidable); archival versus recreated voice; the band-limited voice (about 4 kHz) could come from separation or the source; dry/no-reverb texture is a spectrogram inference on demucs output; the 1:58 riser; whether the 1:03.5, 1:46 and 1:57 bursts are speech; no pitch recovered for the 2:35-2:38 and 2:44-2:48 speech; digits (1963, 575, 9500, 16 graden, 200 km) and language ID are the only reasonably solid Whisper content. Emotional labels and lineage are inference only.
