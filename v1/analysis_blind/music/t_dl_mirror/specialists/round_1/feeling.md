# t_dl_mirror: FEELING specialist, round 1 (blind, measurements only)

Role: the attentive listener's moment-by-moment journey, each feeling tied to a musical cause. Evidence: all twelve `win_*.md` notes and the five round-1 specialist files (form, voice, sound, harmony, rhythm) were read; I opened `music_views/window_0000s.png` and `window_0180s.png`; `lyrics/` transcripts; and I re-measured with `v1/scripts/agents/feeling_r1_tdl.py` (0.1 s stem envelopes, step sizes, end of file). Times m:ss. Stem levels are demucs estimates and can leak. Feelings are INFERRED from measured causes; I cannot hear. Tags: measured / INFERRED, with high/medium/low. No context.md, research or web used.

## 0. The track in one paragraph

A loud, flat-in-level, mono, hip-hop-pulse track (tracker tempo 95.7 BPM, D minor-ish, a D-A drone bed) that keeps one groove for 3:56 and gets all its drama from subtraction and return: the bass is switched off and on, the voice is chopped in the hook and continuous in the verse, and each hook lifts the voice up about ten semitones without getting louder. The feeling is a hypnotic, slightly cramped, dark-morning lean (verses), a brief rise into a half-sung refrain (hooks), one hard "floor back" arrival at 3:15, then a long, calm, stepwise unwinding to a clean stop. It does not build by volume; the listener feels it through the bass and the voice register. INFERRED, medium-high.

## 1. Moment-by-moment journey

Numbers below come from my re-measurement (dB means of 0.1 s frames, so they sit a little under colleagues' RMS-over-span figures; steps agree with theirs).

| Time | What the listener meets (cause) | Feeling (INFERRED) | Conf. |
|---|---|---|---|
| 0:00-0:10.4 | Mix starts at full density with no fade-in; drums on a 16th-based break pattern (drums about -23 dB mean in my frames, -18 RMS per win_0000), a held D-A drone bed, and bass stabs that come and go (out 0:01-0:02.5, out again 0:06-0:10.4; `window_0000s.png` bass panel is black 0:06-0:10). No voice (vocals stem about -73 dB, residue). Effectively dual-mono here (L-R side/mid -92 dB per win_0000). | Thrown into a groove already running: restless, anticipating, a little claustrophobic (flat, centred, no air). The 4 s bass dropout leaves the top-heavy beat waiting for its floor. | high (causes) / medium (feeling) |
| 0:10.4 | Voice, bass and a broadband crash land together on a tracker beat: vocals stem -65 to -19 dB (+46 dB), mix about -18.7 to -7.3 dB over my 0.3 s frames, hard-clipped runs of about 1,000 samples (sound specialist). | The first and sharpest release: "now it starts". The punch is partly loudness, partly the clipping's crunch. | high |
| 0:10.4-0:30 | Hook voice, chopped: gaps at 0:11-0:12.2 (-50 dB), 0:14.5-0:15 and 0:17-0:17.9 each fall 30 dB or more in under 0.5 s; narrow melody about G4-A4; a short chord walk at 0:15.5-0:20 (D to G, F, Am, back to Dm per `chords.json`, chord labels noisy); a second crash at 0:18.45. | Stuttering, hesitant, chant-like: someone half-saying, half-singing, cut off mid-thought. The G-F-Am walk is the only real harmonic movement, so it feels like a small lift or a glance sideways, then home. | medium |
| 0:30-1:11 (verse 1) | Voice drops about ten semitones to a near-monotone around A#3 (median 230 Hz, voice stem about -16 to -18 dB, the loudest stem), one rhymed line per 2.5 s bar; bass in short blocks (on 0:30-0:36.3, off 0:36.3-0:42.9, then 3.4 s blocks about every 10 s; drums flat about -19 RMS). | Steady lean, conversational, a little grim: voice on top of the beat, no melody to hold on to, a floor that is repeatedly withdrawn so the track never relaxes. The words (Whisper, medium): a hungover morning, a stranger in bed, hiding things, "look in the mirror, but today I seem out of place". | medium-high (form) / medium (feeling) |
| 1:11-1:31 (hook 2) | Voice leaps to A4/D5 at 1:11.4; stays 3-6 dB lower than the verse voice (hook about -20 dB, verse about -16 dB); a vocal hole at 1:12.15-1:13.1 (mix -4 dB only); bass continuous (1:10-1:37). | A lift without extra loudness: the refrain feels "up and inside" the music rather than on top of it. The 1 s hole right after the entry makes the arrival feel interrupted, then resumed. | medium-high |
| 1:31-2:12 (verse 2) | Voice drops again (pitch down about ten semitones, +5 dB), "other" bed steps down about 5 dB from 1:32; bass out 1:37-1:41.4 (about -50 dB below its on level) then blocks. Words: a morning drive, road rage, a fight. | The same lean, harder: the story turns violent while the groove does not change, so it reads as more cold than angry (grooves that do not react to words). | medium |
| 2:12-2:34 (hook 3) | Short stutter at 2:12.0 (all stems dip about 0.25 s, mix about -9 dB), vocal gap 2:13.3-2:13.95, returns 2:14.0; more dips at 2:23 and 2:35.2. | A little "catch of breath" before each return (metaphor: it is a 0.25-0.65 s edit, not a breath). Familiarity now: the refrain is a comfort, the gaps are expected. | medium |
| 2:34-3:13.5 (verse 3) | Bass long exit at 2:38 then re-entering 2:42.5 and in pulses (D1 about 37 Hz then D2 about 74 Hz with rising glides, win_0160); a big accent at about 2:57.4: drums jump -24 to -14 dB over 1 s, mix at its loudest seconds (-7.4 dBFS), a 3,200-sample (about 73 ms) clipped run. Words: street dealing, arrest, a cell. | The most weight and the darkest content; the 2:57 hit is a jolt inside the lean. Feeling of tightening, being cornered. | medium |
| 3:13.8-3:15.09 | Voice and bass leave together; mix falls to about -22 dB (my frames: -22.2 before the return); the "other" bed brightens (3:12.5-3:15, +10 dB 4-10 kHz per colleagues). | A held breath, the longest and emptiest pause in the song (still not silence: drums partly present). | high |
| 3:15.09-3:35.3 (hook 4) | Mix +about 11 dB (my frames -22.2 to -11.4), the largest step in the song; voice returns at a higher register (about A4, lead notes reach D5 around 3:16 per `window_0180s.png`), bass continuous; Gm-G side-step at 3:18.7-3:20 in the chord track. | The hardest arrival: the floor slams back and the voice leaps up. It feels like release and climax, and also like the story's cell door shutting and the refrain ("You I see ... I see you", Whisper) turning back on the speaker. The reflective reading is interpretation only (low). | high (arrival) / low (meaning) |
| 3:35.3-3:49 | Voice gone (vocals stem -51 to -74 dB), mix briefly rises (bass returns), then thins: bed dips at 3:36.0, bass out 3:38.9, back 3:43.0; drums steady (about -22 in my frames through 3:49). | Aftermath, calm, a little hollow: the same groove without anyone telling the story. | medium-high |
| 3:49-3:56.5 | Stepwise fade: mix about -9 dB (3:50 block) to about -47 dB (3:55 slot) per form; drums last. | Letting go; a quiet, dimming, faintly sad finish (CLAP "sad" and "tense" about 0.9 at 3:50-3:55, weak evidence). | medium |
| 3:56.45-3:59.44 | Last audible sound 3:56.44 at -57 dBFS (my 10 ms envelope: last frame above -60 dB at 3:56.44); exact digital zero after (my mix frames 3:56-3:58 are -139 dB). | A clean click-off, then nearly 3 s of nothing: a stop, not a resolving chord (metaphor: lights out). | high |

## 2. What produces the feeling (causes ranked)

1. **Bass withdrawal and return (strongest, measured high).** The bass is on about -20 to -22 dB when playing and -48 to -60 dB when not (my section means: 36.3-43 s -59.8; 43-70 s -49.2 mean with blocks). It leaves for 4-7 s stretches (0:06-0:10.4, 0:36.3-0:42.9, 1:37-1:43.8, 2:38-2:42.5 and so on) while the full mix moves by only 0-4 dB, so the listener feels the floor withheld rather than the track getting quieter.
2. **Voice register (measured high).** Hook about 405-410 Hz, verse about 220-230 Hz (voice specialist), so the refrain is a lift of about ten semitones with no gain in loudness.
3. **Dryness and mono (measured high).** The vocal stops within 0.25-0.5 s with no tail, and the mix is dual-mono with a hard 8 kHz ceiling (sound specialist, -61.5 dB at 8.0 kHz and -80 dB beyond). Feeling: close, flat, boxed-in, urgent rather than spacious. INFERRED, medium.
4. **Drone harmony (measured high that the D-A fifth persists; mode INFERRED medium).** Chords sit on Dm/D with a weak third; the lack of harmonic change, apart from the 0:15.5 and 3:18.7 side-steps, gives hypnosis and unresolved gloom rather than progress.
5. **Even loudness (measured high).** Mix about -10 to -11 dBFS RMS from 0:10 to 3:40 with peaks at 0 dBFS; no crescendo, so no dynamic climax. The climax is the 3:15.09 return (+11 dB step), a density peak.

## 3. Evidence rules

**Production era (rule 1), INFERRED, medium-high.** Reads as modern production, not one period recording. Figures: sample peak 1.0 (0 dBFS), RMS -10.75 dBFS (my run; crest about 10.7 dB), 21,079 samples at or above 0.999 and clipped runs of up to about 73 ms (sound specialist); mono; mix steady to within about 1 dB over three and a half minutes. Drum onsets sit median about 11 ms from a 16th grid at about 94 BPM (win_0220, medium-low) and bar-to-bar mel correlation of the "other" bed is 0.83-0.93 (win_0220) or chroma 0.72-0.77 at bar lags (form): a looped or sequenced bed with variation, not a near-identical copy. An 8 kHz brickwall applies to every stem equally (sound), so I cannot show an older band-limited layer under a full-band mix; the source chain is narrow-band, not one layer. Whether the drone is sampled archive material is not settled.

**Section boundaries (rule 3).** I re-measured the four stems at the three boundaries that carry the feeling (0.1 s frame means, three frames either side; dB).

| Boundary | Drums | Bass | Vocals | Other | Mix | Carries it |
|---|---|---|---|---|---|---|
| 0:10.4 voice in | big hit, broadband (win_0000: -25 to -10) | -47 to -17 | -65 to -19 | -40 to -18 | -18.7 to -7.3 | vocals, with bass and crash together |
| 3:13.8-3:15.09 void | -7.6 (form/win_0180) | out | below -45 dB, min -71 | flat (bed brightens) | about -22 dB (my frames), not silence | vocals and bass; drums and bed continue |
| 3:15.09 hook 4 | +9 | +35 | +41 | +2 | -22.2 to -11.4 (my frames; +11.1 in form) | all three together; voice register jump |
| 3:35.3 voice out | +7 (win_0200, as quoted) | +22 | to -54/-66 | +2 | rises briefly | vocals (loudest layer removed) |

Last two rows are colleague figures I checked only for consistency of the mix step, and I keep their tags.

**End of track (rule 4), measured high.** 10 ms envelope over the last 3 s of the 44.1 kHz stereo file (239.444 s): last frame above -60 dBFS at 3:56.44 (-56.95 dBFS), exact digital zero from about 3:56.70 (form: sample test), so final 2.7-3.0 s is silent. Final hits: a decaying cluster of roughly six sub-hits at about 0.1 s spacing between 3:55.5 and 3:56.5 (-37 falling to -57 dBFS; form and win_0220 count six with a coarse pick, about ten with a fine one); I state "about six, medium". Drums are last; bass and other are below -78 dB there.

**Sync (rule 5).** No cut-to-beat statistic is made. Grids named in this note: tracker beat grid 0.627 s (95.7 BPM) and drum IOI about 0.157 s (a 16th of that), which agree; the vocal-event offset test in the voice note (mean absolute 0.15 s) is at chance level, so I claim no on-beat sync for the voice, only that single events (0:10.4 voice entry 0.07 s from a tracked beat) coincide.

**Emotive nouns (rule 6).** I use "held breath", "click-off", "lights out" and "catch of breath" strictly as metaphor, each beside the measured gap (1.3 s, about 22 dB mix; 0.25-0.65 s dips; -57 dBFS final cluster).

**Carried tags (rule 7).** Hook/verse labels and the 3:15 "climax" are INFERRED medium (form). Tempo 95.7 BPM (tracker) against 93.98 (a colleague's kick-grid) is unresolved; I use 95.7 and flag it. The hook word "mirror" is the voice note's low-medium candidate; I do not raise it. I did not carry the unverified Whisper slur in verse 3.

## 4. Where I might be wrong

- Feelings of "grim" and "cold" lean on Whisper wording that is itself unreliable in the verses (no_speech_prob 0.66-0.90, voice note); the groove-and-register part of the feeling is better supported than the story part.
- "Climax" at 3:15 is a density and step-size judgement. A listener who follows the words may place the peak elsewhere (2:57 accent, verse 3 arrest).
- Dm/D wobble may be chord-estimator noise; the "unresolved, sad" colouring rests on the missing third (INFERRED, medium) and on weak CLAP scores.

## 5. Questions for fellow specialists

1. **Harmony**: Does the 3:18.7-3:20 Gm-G side-step and the 0:15.5-0:20 G-F-Am walk share one chord shape, and is the hook's tonic really D minor (the hook voice sits on A, the fifth) or does the missing third leave it open between minor and major?
2. **Rhythm**: Do the vocal hole edges at 3:13.8, 3:15.09, 1:12.15 and 2:13.3 fall on bar lines at 2.51 s, and is the 4-bar bass block pattern (3.4 s on every 10.2 s) locked to the drum grid or drifting?
3. **Voice**: Is the hook voice in hook 4 higher or clearly more strained than in hooks 1-3 (lead notes reach D5 around 3:16), and does its delivery become louder than hook 2's -20 dB?

(Also for sound: is the 2:57.4 clipped 73 ms run a drum hit or a bass-plus-drum collision, and for form: where precisely does hook 3 end?)

## Not recoverable by measurement

- Intent, irony and tone of the voice (autobiographical, comic or bleak): stems give pitch, level and words, not delivery meaning.
- Exact instrument identity of the bed, the bass and the drum sounds (organ, synth, guitar; 808, sample or live): spectra show a 148 Hz harmonic series and a sub-bass at D, not sources.
- Whether the bed or any layer is archive or sampled material, and the recording date: an 8 kHz ceiling on every stem points to the file chain, not to a source.
- Whether the gaps and stutters (2:12.0, 3:13.8-3:15.09) are performed or DAW edits, and whether the ending is a fade or an edit.
- The actual word in the hook ("carry", "theory", "mirror" and so on): Whisper changes it per pass.
- How a particular human feels: my "feelings" are the response the structure invites, not a measurement of one.
