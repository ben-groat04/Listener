# t_dl_mirror: the music, read as a listener (blind, measurements only)

Basis: 12 window notes (`win_0000.md` to `win_0220.md`) and all 21 specialist files (rounds 1 to 3: feeling, form, harmony, lineage, rhythm, sound, voice), cross-checked against `data/t_dl_mirror/` (stems, lyrics, audio_features). I did not read context.md, research or non-blind analysis, and used no web. One re-measurement of my own, on `audio/song.wav`, for the ending and peak (section 11). Times m:ss; levels dBFS; bars 2.54 s. Stems are demucs estimates and bleed. Tags: measured / INFERRED; high / medium / low. Where a colleague's tag is carried it is unchanged unless a reason is given.

---

## 1. The track in a paragraph

A 3:59 loop-based beat track at about 94.6 BPM (94.4 to 94.8) in 4/4, with a tonic of D. A drum loop with straight sixteenth hats and a low, off-beat kick feel runs unchanged from the first frame to the last decay. Over it sit a sustained, thirdless D+A drone and a bass that is switched on and off in 4-bar blocks. A dry, mono voice alternates between 41 s rapped verses (fast, near-monotone, about 5 onsets per second around A#3) and 20 s sung or chanted hooks on three notes (G4, A4, F4) built around the repeated line "You, you I see ... In my ___ in the morning ... I see you". The mix sits at about -10.4 dB RMS against a 0.0 dBFS ceiling the whole way through, so the drama is subtraction and return (bass and voice leaving and coming back), never a louder build. It feels like a locked, hypnotic, forward-leaning, close and slightly claustrophobic groove, hollow and open rather than plainly sad. It ends by stepped withdrawal and a fade into a cut, with no cadence. Tags: structure measured, high; feeling INFERRED, medium.

---

## 2. Song map

Edges good to about 0.2 s. Hook starts are the voice's phrase starts (0:10.4, 1:11.3, 2:12.0, 3:13.1), 24 bars apart.

| m:ss range | Section | What is playing | What it feels like |
|---|---|---|---|
| 0:00-0:10.4 (4.1 bars) | Voiceless intro | Drums running (-18.3 dB), sustained D+A bed (-27 dB), one bass burst 0:02.5-0:05.9 then none to 0:10.4 (bass-on 25 %); vocal stem at residue (-68 dB); mix -11.8 dB, -13.1 dB while bass is out. No fade-in | Dropped into a groove already running; expectant, slightly tense. INFERRED, medium |
| 0:10.4-0:30.4 | Hook 1 | Voice and bass arrive together (voice +43.5 dB, bass +29.9 dB, mix +2.5 dB, stems at 1.5 s windows). Sung G4-A4-F4 over D+A; first hole in the voice at +0.5 to +1.9 s (0:10.9-0:12.3); bass walk G-F-C-D at about 0:16 and 0:26; long vocal gap near +13 s; bass-on 84 % | First release: a voice arrives into a held pulse, then a jolt; lifted, open, chant-like. INFERRED, medium |
| 0:30.4-1:11.3 | Verse 1 | Voice steps up +4.4 dB, rapped, 5.0-5.2 onsets/s, active 97 % of the time; bass on 27-29 % in a 10.16 s on/off loop; no harmonic move | Grim, pressing forward, hypnotic. INFERRED, medium |
| 1:11.3-1:31.4 | Hook 2 | As hook 1; bass back (+13.7 dB), voice down 8.8 dB and up in register; first hole 1:11.9-1:13.0 | Familiar return; relief at the low end. INFERRED, medium |
| 1:31.4-2:12.0 | Verse 2 | As verse 1 (voice +5.1 dB, bass-on 28 %) | Same pressing groove |
| 2:12.0-2:32.4 | Hook 3 | As before; bass +20.3 dB; hole 2:12.8-2:13.9 | Anticipated by now |
| 2:32.4-3:13.1 | Verse 3 | As before (voice +4.1 dB, bass-on 27 %); hard digital cut at about 2:57.5 next to a clipped run | A jolt in the middle of the verse. INFERRED, low-medium |
| 3:13.1-3:33.5 | Hook 4 | Same pattern as hooks 1 to 3; bass absent 3:09.6-3:13.2 and returns inside the first hole (bass +29.5 dB); walks at about 3:18.75 and 3:29.0; voice -19.3 to -20.2 dB like the others | The last of four equal hooks; a familiar return with slightly fresher low end. INFERRED, medium |
| 3:33.5-3:35.8 | Dissolve | Voice, bass and drums thin together over about 1.3 s (voice -6.4 dB, bass -12.4 dB, drums -2.5 dB, mix -3.6 dB at 3:34.0); last voice activity above -50 dB about 3:35.2, no tail | The song lets go; a clean stop of the voice. INFERRED, medium |
| 3:35.8-3:49.0 | Voiceless outro | Bass back (+10 dB at 3:35.8), drums -20.5 dB, bed -29 dB; bass-on 25 %; no voice | Calm aftermath: the groove without the narrator. INFERRED, medium |
| 3:49.0-3:56.5 | Fade | Bass out at 3:49.0 (-38.4 dB) and for good at 3:54.5; mix -13.9 to -54.8 dB | Fading away, no resolution. INFERRED, medium |
| 3:56.67-3:59.44 | Digital zero | Exact zero for 2.77 s | A click-off. INFERRED, medium |

Form in bars: 4 + 8 + 16 + 8 + 16 + 8 + 16 + 8 + about 9. Voice-derived edges land within 0.1 bar of a 94.5 BPM grid at 12 of 12 edges (form; measured, high on edges, medium-high on the tempo). There is no bridge, no key change and no build.

---

## 3. Harmony and melody

- **Tonic D (high).** The bed is a thirdless D+A drone: D and A chroma are solid, and the F5 partial (698 Hz) sits 23 to 28 dB under D5 in verses and hook non-walk stretches (harmony round 3, FFT of the other stem). The labeller's Dm/D flicker (for example Dm/D alternation 0:00.28-0:15.46) is therefore a detector wobble over a missing third, not real alternation (INFERRED, medium-high). Whole-song key estimate D minor 0.69 (`audio_features/summary.json`).
- **Mode: D minor or Dorian-flavoured, low-medium.** The minor third comes only from the voice's F4 (15 to 17 % of hook frames) and the walk's F, not from the bed. A listener hears "hollow and open" more than "sad" (INFERRED, low-medium).
- **The only chord movement is the hook bass walk G - F - C - D** (iv, bIII, bVII, i over a D pedal), twice per hook (about +5 and +15 s into the hook, 10.2 s apart, one 4-bar loop), eight times in the song, about 3 s long, absent in verses (high on shape, medium on pitch classes). Octave is not safe (see section 10). The walk is irregular in time (steps about 2 to 2.5 beats, with a short D arrival), not one chord per beat (harmony round 3; low-medium). The chord quality of G (major or minor) is undetermined (lowered to low in round 3 with stated reason).
- **Voice melody:** a three-note hook G4 (392 Hz), A4 (about 435 to 440 Hz, 15 to 20 cents flat of A440), F4, contour G, A, F, A, F, the same in all four hooks to about 1 semitone (INFERRED, medium). G4 sits over the G bass (root), A4 over F (third of the chord), F4 over C (a fourth) and A4 then F4 over D (fifth, then minor third). The voice starts its line about 0.75 to 1.0 s before the bass steps (INFERRED, medium-low). Verse pitch is near-monotone speech around A#3.
- **Tuning (measured, medium-low):** the bed sits about 13 to 14 cents sharp of equal temperament (fundamental 147.9 Hz against D3), bass peak 74.7 Hz is +25 to +35 cents sharp of D2, and the voice sits about A440. Cause (speed, tuning, tracker error) is unknowable from the figures.
- The track ends on the D+A drone with no cadence (chroma D 1.00, A 0.96 over 3:45-3:55; measured, high).

---

## 4. Rhythm and groove

- **Tempo about 94.6 BPM (94.4-94.8), 4/4, bar about 2.54 s** (INFERRED, medium-high). Three independent long-baseline measures agree: drum-stem envelope repeat lags 60.79, 121.67, 182.46 s (rhythm, 24 bars per 60.82 s = 94.73); low-frequency kick-pattern lags 61.06, 122.25, 183.31 s (form, r 0.70-0.74 = 94.5); bass-loop fit 10.158 s per 4 bars (form, residual 0.10 s over 183 s = 94.50). The beat tracker's 95.7 (`summary.json`) is about 1 % fast and the earlier 94.0 came from short windows and an invalid kick-onset fit, which rhythm withdrew (kick bar-level phase concentration R 0.03-0.06 is chance). I do not choose between 94.5 and 94.7; the count of 24 bars per cycle is inherited from form.
- **One 4-bar drum loop (10.14-10.16 s) runs under every section** and keeps its phase through the hard cuts at 0:10.62 and 2:57.54 (offset change at most 0.05 s; rhythm round 3, medium). Drums move at most 1.8 dB at any hook/verse edge (form, high). The pulse is the floor; the low end is the variable.
- **Feel:** straight (unswung) sixteenth hats, a kick that sits off the beat in a 3-2-3-2 style, which is a head-nod, break-style feel rather than a trap roll (INFERRED, medium for "head-nod, not trap" by hats and no roll evidence; the "3-2-3-2 cell" is INFERRED, low-medium after the kick detector was found unreliable). Half-time (about 47 BPM) is an equally available way to feel it.
- **Bass is the offset clock:** a 10.16 s loop of about 3.4 s on and 6.7 s off in verses (bass-on 27-29 %), nearly continuous in hooks (84-88 %). Bass blocks start on or just before the hook start and run 5.5 to 5.8 s past the hook's end (loop phase 0.33).
- **Voice rhythm:** verse onsets 5.0 to 5.2 per second against 6.3 sixteenths per second at about 94.7 BPM, so free speech rhythm over a 16-step bar; hook syllables 0.12-0.15 s apart in places, faster than a sixteenth (0.158 s). Weak pull of hook onsets to an eighth grid (R 0.29-0.38 at 94.5, below the 0.30 clear level for most hooks; low).
- **Sync honesty:** no gap edge, cut or entry is shown to sit on a kick grid (gate edges 66-87 ms against 80 ms chance). Section edges are within 0.1 bar of the named 94.5 BPM arrangement grid (bass loop, hook spacing and kick-pattern lag all at 94.5). Voice re-entries after the first hole (1:13.15, 2:14.0, 3:15.09) fall 3.05, 3.09, 3.52 beats after the hook start on the drum-aligned 0.6335 s beat: two near a beat, one on an off-beat eighth (INFERRED, low).

---

## 5. Sound and production

- **Band-limited, mono, dry.** The file is dual-mono (identical channels). Every stem hits a steep wall at 8.03 kHz (about 79 dB deep; sound; measured, high); the likely cause is a 16 kHz-sampled stage (INFERRED, low-medium). Result: close, flat, dry; no width, no air, no audible reverb tail. Median 10 ms level about -11 dB with 3 to 5 dB movement.
- **Loud and limited.** Sample peak 1.0; I count 21,079 samples at or above 0.999 (matches the colleagues), 10,317 at full scale; RMS -10.0 to -10.9 dBFS; crest about 10.5 dB; a clipped run (3,354 samples, 80 ms) at 2:57.44-2:57.52 followed by a 20 ms mute to about -94 dBFS, and a 10 ms mute to about -69 dB at 0:10.62 (sound, rhythm; measured, medium-high). A 5 ms envelope does not resolve the 2:57.54 mute (resolution limit).
- **Layers (identities not recoverable):** (a) a sustained mid-range bed, fundamental 147.9 Hz, strongest third partial; (b) a gated bass centred at 60-90 Hz with a harmonic skirt (not a pure sub-sine: energy at 130-400 Hz about -9 to -11 dB per band); (c) a falling-pitch low kick (about 65 to 40 Hz) and flat 3-8 kHz hat energy; (d) a dry, close voice, hook gated (active 72-78 % of 50 ms frames, verses 92-97 %).
- **No ducking, no pumping.** The bed stays within -2.3 to +2.1 dB across nine vocal entries; vocal-to-bed correlation -0.41 comes from section structure (sound; measured, medium). The mix steps up +7 to +9 dB when bass and voice enter together at 0:10.4 and at the end of the track, but at hooks 2 to 4 the voice falls 7 to 9 dB while the bass rises 14 to 30 dB so the mix is nearly level (+2.5, -1.7, -0.5, -0.6 dB; form). I adopt form's reading; sound's "+7 to +9 at every entry" is too broad.
- **The vocal gaps** are mutes on the voice channel: 35 to 50 dB deep, 90 to 155 ms edges, no tail, while drums and bed continue (voice; measured, medium-high). A gate, a drawn mute or a re-triggered chop all fit.
- **Spectral change late on:** centroid 842 to 386 Hz and share above 4 kHz 10.5 % to 4.3 % over the outro (win_0220): duller and more distant.

---

## 6. Voice, words and samples

- **Two voice jobs.** Verses: rapped, dense, near-monotone (A#3, onsets 5.0-5.2 per second, vocal +4 to +5 dB into verses). Hooks: sung or chanted on pitch, G4-A4-F4, sparser (2.2-2.7 onsets per second; one hook line 3.6-4.9 per second on another detector), with a hole at +0.5 to +1.9 s, a second statement and a more broken second half (gaps near +13 s and +17.5 s, about 1.1 s each). Sung-versus-chanted INFERRED, medium (high that it is not speech pitch); "rapped verses" measured high.
- **Hook phrasing repeats, the waveform does not.** Aligned envelope r 0.90-0.96 and pitch contour r 0.89-0.94 (hooks 2 to 4) with the same gaps within about 0.5 s every 24 bars, but 1 s waveform r only 0.24-0.46 (voice). Reading: a performed or re-sung pattern, not shown to be one pasted recording (INFERRED, medium-low). Hook 1's pitch contour agrees poorly (r about 0.5; low).
- **Words (Whisper, unstable, so low confidence on content).** A legible, repeated hook transcript across passes: "You, you I see" (0:10.88-0:13.98, 0:20.50-0:23.96, 3:14.38), "In my ___ in the morning" (the missing word appears as "carry", "theory", "period", "hair" in different passes; not recoverable), and "I see you" / "You see in me, I see you" (3:32-3:34.7). This is a near-certain identification of the refrain's frame: a first-person, mirror-like "you I see / I see you" swap around a morning line (INFERRED, high that the lines repeat as stated; the missing word low). Verse text is unreliable (Whisper no_speech_prob 0.66-0.90 in verses), but the mix pass gives at 0:56-1:11 a legible run about a fiancée on her way up the steps, hiding someone in a closet, running to the sink and looking in the mirror (INFERRED, low-medium; ASR only), and the vocals-stem pass at 3:00-3:13 gives lines about "the street hotter than california", a "lawyer phone call" and "my face gone" (low). Voice-stem and mix passes disagree on wording, so I use them for subject matter only.
- **Words and music meet in one place.** The "In my ___ in the morning" line carries the bass walk both times per hook (checked hooks 3 and 4 against Whisper timestamps +/-0.5 s; walk starts +5.0 and +15.3 s into hook 4; INFERRED, low-medium on the link).
- **Samples:** no separate older or band-limited vocal or sample layer is visible: every stem shares the same 8.03 kHz wall. No claim that any layer is sampled (see section 13).

---

## 7. The emotional journey and its musical causes

All feelings are INFERRED from the measured cause; no measurement reads a listener.

1. **0:00-0:10.4, dropped in.** Cause: no fade-in, drums at -18 dB, bed at -27 dB, one low burst then nothing, no voice (vocal stem -68 dB). Feeling: expectant, slightly tense (medium).
2. **0:10.4, first release.** Cause: voice +43.5 dB and bass +29.9 dB land in the same 0.25 s step (a hard mute edge at 0:10.62 follows). Feeling: a voice arrives into a held pulse, then a small jolt (medium).
3. **Hook 1, 0:10.4-0:30.4.** Cause: sung G4-A4-F4 over D+A, a hole at +0.5-1.9 s, stutter, the bass walk. Feeling: lifted, open, chant-like with nervy stutters; by hook 3 it is familiar (medium).
4. **Each verse (41 s).** Cause: fast monotone rap, bass mostly off, no harmonic move, hat comb about 6 per second, off-beat kicks. Feeling: grim, hypnotic, pressing forward with no downbeat to rest on (medium-high cause, medium feeling).
5. **Each return to a hook.** Cause: bass returns +14 to +30 dB, voice falls 7 to 9 dB and rises in register, mix moves under 2.5 dB. Feeling: relief of low end, not a louder voice (high cause, medium-high feeling).
6. **The walk, eight times.** Cause: bass G-F-C-D under the line while the voice goes G4 to A4 to F4. Feeling: a single glance sideways off the drone; comforting after the first (low-medium).
7. **2:57.5, mid-verse jolt.** Cause: clipped run then a 20 ms mute. Feeling: a digital jolt (low-medium).
8. **3:13-3:15, hook 4.** Cause: the same hole as hooks 1 to 3 (mix minima -21.4 to -22.3 dB in all four), with the bass returning inside it. Feeling: a familiar return; any sense of a "last peak" comes from position, not loudness (INFERRED, low as a climax).
9. **3:33.5-3:35.2, letting go.** Cause: voice, bass and drums thin together; no tail. Feeling: a clean stop of the narrator (medium).
10. **3:35.8-3:49.0, aftermath.** Cause: no voice, bass +10 dB, drums -20.5 dB. Feeling: calm, the groove without the narrator (medium).
11. **3:49.0-3:56.5, fade, then 2.77 s of zero.** Cause: bass out at 3:49.0 and 3:54.5, mix to -54.8 dB, last sound 3:56.45, exact zero after. Feeling: fading away without resolution, then an abrupt click-off (high on figures, medium on feeling). CLAP "sad 0.91" and "tense 0.87" at 3:50-3:55 agree only weakly; CLAP is a noisy model.

Chain of causes: (a) a floor that never moves (drums within about 1.6 dB), so the body is locked in; (b) all drama is subtraction and return under a hard ceiling (mix 10 s RMS -10.1 to -10.5 dB); (c) the voice switches job (narrator against refrain); (d) dry, mono, 8 kHz-roofed sound keeps it close and claustrophobic; (e) eight identical walks and four identical hole patterns teach the form, so the first is a surprise and the rest are anticipated.

---

## 8. The five moments a listener remembers, and why

1. **0:10.4, the voice and bass arrive together** after ten voiceless seconds: +43.5 dB voice, +29.9 dB bass, with a 10 ms mute at 0:10.62 right after. It is the first and strongest contrast in the track (measured, high; memorability INFERRED, medium).
2. **The stutter hole in every hook** (voice mute of 1.0-1.3 s at +0.5 to +1.9 s, a second at +13 s): 35 to 50 dB deep, 0.1 s edges, the rest of the groove running. A hole this sharp repeated four times is what makes the hook recognisable (measured, high; INFERRED, medium).
3. **"In my ___ in the morning" with the bass walk**, the single harmonic excursion, G4 to A4 over G-F-C-D, eight times. It is the only moment the harmony changes at all (measured, high on shape; INFERRED, medium).
4. **The bass returning into each hook** (+13.7, +20.3, +29.5 dB), most noticeably at 3:13 after a 3.6 s absence. The release is low-end density, not loudness (measured, high; INFERRED, medium).
5. **The ending: the voice letting go at 3:33.5-3:35.2, the voiceless outro, and the cut to zero at 3:56.5.** Position and withdrawal make it read as an ending although no cadence or final hit exists (measured, high; INFERRED, medium).

Honourable mention: the hard clip-and-mute at 2:57.5 in verse 3 (INFERRED, low-medium that a listener notices it).

---

## 9. Where the specialists disagreed, and the best-supported view

| Question | Positions | Best-supported view |
|---|---|---|
| Tempo | tracker 95.7; rhythm R1/R2 94.0; form 94.5; rhythm R3 94.73 | About 94.6 (94.4-94.8): three long-baseline measures agree; 94.0 rested on an invalid kick-onset fit and short windows; 95.7 excluded (24 bars would be 60.2 s against 60.8-61.1 s measured). Medium-high |
| Is hook 4 the climax? | form/feeling R1: biggest return (+11 dB at 3:15.09) | No. Same first-hole minima (-21.4 to -22.3 dB), bass-on 84-87 %, voice -19.3 to -20.2 dB in all hooks; the +11 dB claim was withdrawn (a hole exit, not a hook start). Any climax feeling is position. INFERRED, low as a climax |
| Hook start times | form R1 2:14.0, 3:15.09 | 2:12.0 and 3:13.1; the earlier times were hole exits. Measured, high |
| G chord major or minor | harmony R2 major (medium-low); R3 undetermined | Undetermined (low): B appears only as a one-frame blip |
| Mode | minor / Dorian / bare drone | D tonic, drone thirdless, minor colour only from voice F4 and walk F; minor or Dorian, low-medium |
| Kick "3-2-3-2" cell and kick-spread figure | lineage R2 medium; rhythm withdrawn | Kick detector at chance (R 0.03-0.06), so no spread figure is quoted; the cell is INFERRED, low-medium; head-nod feel INFERRED, medium |
| Bass octave and sub-sine | lineage R2 octave labels; sound/harmony R3 harmonic skirt | Octave labels withdrawn; a tone centred 60-90 Hz with a harmonic skirt; pitch-class path G-F-C-D medium |
| Hook copy or re-sung | "same phrase" vs pasted | Same performed pattern; waveform r 0.24-0.46; not shown to be pasted (medium-low) |
| Does the mix step +7 to +9 dB at every voice entry? | sound yes; form no | Only at 0:10.4 and the end of track; at hooks 2 to 4 the mix moves under 2 dB. Low-confidence disagreement settled for form's figures |
| Limiter makes the equal hook level | feeling R2 worried; sound no | No ducking found; repeated phrase more likely; either way four hooks of equal weight (INFERRED, low-medium) |
| Voice end | 3:34.7-3:35.3 vs fade tail vs gate | Phrase-wise thinning from 3:33.5, last audible about 3:35.2, no tail (medium-high; medium-low on the mechanism) |
| Ending hit count | about six; 11; 15-20; none distinct | No distinct closing hit; a decaying cluster of 15-20 sub-peaks over about 1 s (3:55.5-3:56.5, prominence-dependent), and 1 peak in the last 3 s on my 3 dB prominence (section 11). Medium on count, high on shape |
| Intro: hook-first single convention | lineage R2 | Demoted to speculative: intro is verse-density with no voice |
| Outro label | form "verse slot" vs feeling "aftermath" | One block, 3:35.8-3:49.0; both labels kept (arrangement / felt) |
| Voice entries on the beat | feeling R2 inconsistent; form on-bar | Hook starts on the bar (within 0.1 bar at 94.5); hole exits not demonstrably quantised |

---

## 10. Uncertainties and what the measurements could not settle

- True tempo to better than about 0.3 BPM (94.4 to 94.8), and whether hook starts are bar-one downbeats (bar origin is arbitrary).
- Bass octave (D1 or D2, G1 or G2) and whether the bass is a synth or a re-pitched sample; the fundamental is weak (-19 dB in the 30-45 Hz band) and the 74.7 Hz peak could be a second harmonic.
- G chord quality and the real mode.
- The 13 to 14 cent sharp bed against a voice near A440; cause unknown.
- Hook words, especially the missing word; verse content beyond subject matter.
- Whether holes, stutters and the 3:34 thinning are performed, gated or edited.
- Whether the 2.77 s digital zero belongs to the master or is a file artefact.
- Stem bleed: voice-hole depths (stem floor -57 to -78 dB) and stem-level claims are estimates; the 3:36.1 other-stem dropout (about 100 ms to -52/-55 dB) was not checked in the mix.
- The Dm/D, F/F# readings in chroma are crude; my claims rest on the FFT partial figures where available.

---

## 11. Section-boundary evidence table and the measured end

Levels: 10 ms RMS, mean over 1.5 s before then after (dB), change in brackets. Source: form round 2 (own re-measurement of all four stems), harmony and voice round 3 for the walk and hole rows. Measured, high unless stated.

| Boundary | Drums | Bass | Vocals | Other | Mix | Which stem carries it |
|---|---|---|---|---|---|---|
| 0:10.4 intro to hook 1 | -17.0 to -15.2 (+1.8) | -51.7 to -21.8 (+29.9) | -68.4 to -24.8 (+43.5) | -27.8 to -23.0 (+4.9) | -11.8 to -9.3 (+2.5) | vocals, with bass; all four move |
| 0:30.4 hook 1 to verse 1 | -18.0 to -19.4 (-1.4) | -14.3 to -18.9 (-4.6) | -21.5 to -17.1 (+4.4) | -22.4 to -20.9 (+1.5) | -9.3 to -10.5 (-1.1) | vocals (level up into rap) |
| 1:11.3 verse 1 to hook 2 | -17.7 to -18.8 (-1.1) | -32.4 to -18.8 (+13.7) | -15.4 to -24.2 (-8.8) | -29.9 to -25.0 (+4.9) | -9.9 to -11.6 (-1.7) | vocals (down, register up) with bass entering |
| 1:31.4 hook 2 to verse 2 | -18.2 to -20.0 (-1.8) | -14.6 to -18.4 (-3.8) | -21.0 to -15.9 (+5.1) | -22.6 to -21.5 (+1.1) | -9.4 to -10.0 (-0.6) | vocals |
| 2:12.0 verse 2 to hook 3 | -17.8 to -19.2 (-1.5) | -37.5 to -17.2 (+20.3) | -19.4 to -22.0 (-2.6) | -28.7 to -27.1 (+1.6) | -11.2 to -11.7 (-0.5) | bass re-entry and vocal register |
| 2:32.4 hook 3 to verse 3 | -17.9 to -18.8 (-0.9) | -14.5 to -19.8 (-5.3) | -20.7 to -16.6 (+4.1) | -23.1 to -22.4 (+0.7) | -9.3 to -10.2 (-0.9) | vocals |
| 3:13.1 verse 3 to hook 4 | -17.7 to -18.0 (-0.3) | -49.4 to -19.9 (+29.5) | -17.3 to -24.4 (-7.1) | -28.5 to -23.4 (+5.1) | -10.6 to -11.3 (-0.6) | bass (back after 3.6 s) and vocals |
| 3:18.75 walk 1 (hook 4), step | about +0.9 to unchanged | D-region to about 50 Hz (G) | on G4 since 3:18.0, no step | G enters, D stays | under 0.7 dB | bass pitch (pitch event, not a level event); medium |
| 3:29.0 walk 2 (hook 4), step | small | G then 100 Hz, 66, 74 Hz in sequence | G4 since 3:28.1 | G, C, F rows | under 0.7 dB | bass pitch; medium |
| 3:34.0 hook 4 thins | -16.7 to -19.2 (-2.5) | -15.1 to -27.5 (-12.4) | -20.9 to -27.3 (-6.4) | -24.7 to -25.3 (-0.6) | -9.4 to -13.0 (-3.6) | bass and voice together, drums partly |
| 3:35.3 voice gone | -18.9 to -17.9 (+1.0) | -23.9 to -15.8 (+8.1) | -25.9 to -66.5 (-40.6) | -25.2 to -27.3 (-2.2) | -12.7 to -10.8 (+1.9) | vocals out; bass returns (+10 dB at 3:35.8) |
| 3:49.0 fade starts | -22.0 to -26.3 (-4.3) | -17.0 to -55.4 (-38.4) | floor (-74 to -76) | -28.5 to -34.5 (-6.1) | -13.9 to -20.9 (-7.0) | bass leaves; drums and bed fall with it |
| 3:54.5 steep drop | -32.8 to -45.1 (-12.3), 0.8 s windows | -30.9 to -76.8 (-45.9) | floor | -44.7 to -51.3 (-6.6) | -26.4 to -39.6 (-13.2) | bass out; drums and mix fall |

Hook first holes (50 ms means; vocals-only mutes): hook 1 0:10.94-0:12.29, hook 2 1:11.89-1:13.0, hook 3 2:12.81-2:13.91, hook 4 3:13.33-3:14.65. Voice drops from about -16 to -27 dB before to -40 to -51 dB in the hole (stem floor about -57 to -65), while drums (-18.7 to -20.2 dB) and bed (-23 to -25 dB) continue. Hook 4 is distinguished only by the bass being absent just before and returning inside the hole; the mix falls to -22.3 dB there. A second hole sits at +17.4 to +17.6 s (0:27.9, 1:28.65, 2:29.65, 3:30.55), and a long hole at +12.9 to +13.4 s (0:23.56, 1:24.38, 2:25.35, 3:26.04): vocals only.

**Reading.** Verse/hook edges are carried by the vocal stem (+4.1 to +5.1 dB into verses, -7 to -9 dB into hooks 2 and 4); drums move at most 1.8 dB at any hook/verse edge; bass changes 13 to 30 dB at hook entries but on its own 10.16 s clock; the mix moves at most 2.5 dB at any edge until 3:34.0. **No silence** occurs before the final zero: the mix stays above -22.3 dB in every hole, so every hole is a vocal mute (or, in hook 4, vocal plus bass) with the rest running, not a silence. The only true silence is the end.

**Measured end of track (rule 4).** My re-run on `audio/song.wav` (239.444 s, 10,559,488 frames at 44.1 kHz), 10 ms RMS envelope over the last 3 s (236.44-239.44 s):
- The window starts at -57.0 dBFS (3:56.44); one local peak at 3:56.47 (-60.2 dB, 3 dB prominence); last frame above -90 dB at 3:56.57; exact digital zero from about 3:56.70 to the end.
- **Last audible sound about 3:56.45; level at the end -57 to -60 dBFS, then -90 dB or less within 0.15 s and zero for 2.77 s.** Colleagues' round 2 and 3 figures (-60 dB at 3:56.47, -67 dB at 3:56.51, zero after 3:56.70) agree.
- **Hits from the waveform:** no distinct final hit. In the last 3 s the 10 ms envelope has 1 peak at 3 dB prominence (2 local peaks at 1 dB). The decaying run 3:55.5-3:56.5 has 15 to 20 sub-peaks (-37 to -60 dB), the count depending on prominence (form; medium on the count, high on the shape). Per stem maxima over the last 3 s: mix -57.0, drums -65.5, bass -69.5, other -76.4, vocals -78.3 dB (floor about -78).
- The ending is a 7.5 s decline from 3:49.0 (mix -13.9 dB to -54.8 dB), drums last (to about 3:56.37), then a cut. Whether the cut is a master fade or a file artefact is open.

---

## 12. Production-era judgement

**Judgement: a modern, loudness-maximised, DAW-style production (a looped arrangement mastered under a limiter), with no measured older or narrow-band layer sitting under a full-band mix. INFERRED.** Confidence: medium-high for "modern limiting" (sound, harmony and feeling carried medium-high; form, lineage, rhythm and voice carried medium; I adopt medium-high for the limiting because the figures are unambiguous and I re-measured the peak and clipping count, and keep medium for "DAW-style arrangement"). Figures:

- **Peak against 0 dBFS:** sample peak 1.0; 21,079 samples at or above 0.999 (my count); 10,317 at full scale; a 3,354-sample clipped run (80 ms) at 2:57.44. RMS -10.0 to -10.9 dBFS, crest about 10.5 dB.
- **Loop regularity:** 4-bar loops repeat with waveform r 0.75-0.85 and drum-envelope r 0.63-0.75 across hooks at 60.8 s lags, a bass loop that holds a line over 183 s with residual 0.10 s, and four hooks with identical hole patterns to about 0.5 s. This is loop-machine or DAW regularity but not bit-copy.
- **Kick onset spread:** withdrawn as a figure (the kick-onset detector's bar-level phase concentration is at chance, R 0.03-0.06), so it neither supports nor contradicts a grid-locked sequencer. Tempo steadiness over 183 s (no measurable drift, lag error 0.02-0.06 s per cycle) is the usable cue: a machine or DAW clock (INFERRED, medium).
- **Band-limited layer against a full-band mix:** none can be compared; every stem is dual-mono and stops at the same 8.03 kHz wall, no hiss or crackle floor in the fade (5-7.5 kHz about 37 dB under 100-1000 Hz). So the mix is one chain; whether the bed or the break is older source material cannot be seen (INFERRED, medium; "modern production over archive material" is not shown, and is not excluded).
- **Digital edits:** a 10 ms mute (about -69 dB) at 0:10.62 and a 20 ms mute (about -94 dB) at 2:57.54, and an exact-zero tail, all sample-accurate cuts.

I do not give a decade.

---

## 13. Not recoverable by measurement

- **Instrument identity** of bed, bass and drums (synth, sample, organ, guitar, played or sequenced): the measurements give partials, bands and envelopes, not sources.
- **Whether the bass is a synth or a re-pitched sample, and its octave:** weak fundamental and harmonic ambiguity.
- **Whether any layer is a sample of older music, and the real source or age of the bed or drum loop:** a sample processed with the rest shows no separate band-limited layer.
- **Whether the drums are sequenced or played:** the kick detector is at chance level.
- **Performer, recording date, studio, scene, region:** not in the signal; resemblance to loop-based hip-hop is similarity of sound, not provenance.
- **Intent:** whether holes, mutes, the 3:34 thinning and the ending are arrangement, gating, performance or edits; the waveform shows the event, not the hand.
- **The words and what they mean:** only unstable ASR transcripts exist; the missing hook word and the verse content beyond subject matter are not settled, and neither is irony, autobiography or tone.
- **Whether the hook is a copy, a chop or re-sung:** stem bleed hides waveform identity.
- **Reverb, double-tracking, autotune, compression settings:** mono, limited, 8 kHz-limited, separated stems hide them.
- **The cause of the 13-30 cent sharp tuning of bed and bass:** speed, tuning or tracker error cannot be separated by a pitch figure.
- **Whether the 8.03 kHz wall is a source property or a delivery stage, and whether the 2.77 s digital zero belongs to the released track.**
- **How any real listener feels:** the feelings above are responses the structure invites, not measured ones; a listener who follows the words, or hears half-time, may feel it as slower, heavier, darker or more narrative.
- **Whether a given section feels like a chorus, bridge or climax:** the labels are functional (voice register, level, bass density).
