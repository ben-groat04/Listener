# Rhythm specialist, round 2 (blind, measurement only): t_cshells_cshore

Scripts: `v1/scripts/agents/rhythm_r2.py`, `rhythm_r2b.py` (drum and bass stems, stems_raw/htdemucs/song). I read all six round-1 files. Tags are carried from round 1 unless stated.

## 1. New measurements this round
**A. Independent tempo curve from the bass stem (not the tracker).** Median IOI of bass-onset pairs lying between 0.42 and 0.58 s (quarter notes), per 20 s:
| start (s) | 100 | 120 | 140 | 160 | 180 |
|---|---|---|---|---|---|
| quarter IOI (n) | 0.506 (10) | 0.504 (35) | 0.499 (31) | 0.494 (32) | 0.484 (13) |
| BPM | 118.5 | 119.1 | 120.3 | 121.5 | 124.0 |
After 200 s the bass is mostly out or not quarter-note (fewer than 5 pairs per window), so no bass tempo is claimable there. This confirms my round-1 drift (about 117.5 to 119 BPM at 1:40 to 2:00 rising to about 121 to 124 BPM by 3:00 to 3:20) by a method that does not use the tracker or the 4 s blocks. Measured, now medium-to-high confidence for 1:40 to 3:20.
**B. Drum-stem beat lag (onset-strength autocorrelation, broadband drum stem).** 120 to 200 s: beat lag 0.494 s (121.5 BPM, AC 0.35), bar lag 1.971 s. 200 to 260 s: 0.484 s (124.0 BPM, AC 0.22), bar 1.956 s. 260 to 317 s: 0.479 s (125.3 BPM, AC 0.26), bar 1.936 s. So the drums speed up by about 3 percent from 2:00 to 5:17, in step with the bass. Measured, medium.
**C. No 2-bar or 4-bar drum loop.** Drum-stem AC at the 4-bar lag (3.9 s): 0.01 (120 to 200 s), 0.11 (200 to 260 s), 0.07 (260 to 317 s); at 8 bars (7.8 s) -0.02 to 0.10. Beat and bar lags carry the periodicity, but nothing repeats at phrase length: the drum stem is varied or played, not copy-pasted. Measured, medium.
**D. A retraction (kick).** I re-ran a kick-band detector (35 to 110 Hz, drum stem, 5 ms hop, strict delta). It fires 1.3 to 1.9 per second with IOIs mostly 0.1 to 0.3 s (histogram, 120 to 160 s: 52 under 0.1 s, 73 at 0.1 to 0.2, 56 at 0.2 to 0.3, only 11 above 0.4 s), and its phase over a 4-beat bar folded on the bass quarter grid is flat (16 sixteenth-bins, 120 to 160 s: 9,15,15,11,14,10,10,10,15,15,12,15,16,13,16,12; 260 to 300 s similar). Within 30 ms of a bass-onset only 4 to 26 percent. A flat histogram means this detector is not finding a kick pattern; it is finding low-band noise, tom and bass leakage. I therefore withdraw my round-1 reading "syncopated or offbeat low hits" (section 6 of round 1, INFERRED low-to-medium): it was not supported by a measurement with this much structure. New status: kick position and count are not recoverable from the demucs drum stem (see list). This also answers the kick IOI check (rule 5): no valid kick grid can be named, so I make no kick-based sync claim.

## 2. Answers to questions put to me
- **Form, Q2** (is there a tempo change between 1:53 and 3:44 versus 3:44 onward, and is the groove on fixed 0.50, 0.488 or drifting spacing?): drifting, not fixed. Bass quarters 0.506 s at 1:40 shorten to 0.484 s by 3:00 to 3:20; drum beat lag 0.494 s (2:00 to 3:20) to 0.484 s (3:20 to 4:20) to 0.479 s (4:20 to 5:17). The beat is therefore about 0.50 s early on and about 0.48 s late; 0.488 s (the tracker constant) is the mid-point, correct only near 3:20 to 3:45. There is no step change at 3:44: the tempo glides about 1 percent per minute. Confidence medium. Form's 0.50 s (1:13 to 2:13) and 0.476 s (3:50 to 5:00) readings are both right, for their own spans.
- **Sound, Q1** (is the 4 s cycle on a different pulse from the 123 BPM tracker?): yes in the sense that the 4 s block is 8 beats of the local tempo, about 120 BPM at 1:00 to 1:40 (4.0 s), not of 123 BPM (3.90 s). The block spacing (4.00, 4.02, 4.02 s, my round 1; 4.013, 4.005, 4.037, 3.884 s, sound) is the same pulse as the later groove, merely slower; the tracker constant is an average. Where does the kick lock to the beat? I cannot say (section 1D); the bass is the only element that sits on the beat in my data.
- **Harmony, Q2** (does the bass pulse after 1:53 lock to the kick grid; do the stabs sit on a bar grid or drift?): the bass at 1:53 to 2:00 is in eighths (IOI 0.20 to 0.27 s; eighth is 0.25 s at 119 BPM, 0.244 s at 123 BPM); no kick grid is measurable, so I cannot say it locks to the kick. The bass quarters later (0.494 to 0.499 s) are themselves the best available grid. Stabs: a bar is 2.0 s at 120 BPM, so 4.0 s = 2 bars exactly at 120 BPM and 8 beats; the spread of 3.88 to 4.04 s (about 4 percent) is a played or hand-edited spread, not machine regular. My round-1 statement stands (medium to low).
- **Feeling, Q2** (does kick IOI median 0.24 to 0.26 s with 40 to 64 percent on beat multiples show syncopation or a loose live feel; is the 4 s clock exactly 8 beats at 123 BPM?): neither is proven. The 0.25 s median is the detector's noise floor on eighths and leakage (section 1D), not a kick rhythm, so syncopation is unsupported and I do not offer it. The 4 s clock is 8 beats at about 120 BPM, not at 123 BPM. I do support a loose-to-fairly-quantised feel from the all-drum measure of round 1 (median 9 to 11 ms from the sixteenth grid, tracker offset removed), medium.
- **Lineage, Q1** (is the kick loose or is the tracker phase off by an eighth or sixteenth; does the pattern repeat at 2 or 4 bars?): I cannot separate kick looseness from tracker phase with this stem. What I can say: a tracker offset of about 35 ms between the drum-onset detector and the tracker beat is a latency, and the bass-quarter grid is a better phase reference (bass onsets and drum envelope lag both give 0.48 to 0.50 s). The pattern does not repeat at 4 bars: drum AC 0.01 to 0.11 at 3.9 s (section 1C). 3+3+2 grouping: no evidence either way.
- **Lineage claim of motorik quarter-note kicks (kick IOI 0.48 to 0.52 s):** lineage measured kick IOI in five spans; my kick detector shows only 10 to 15 percent of IOIs above 0.4 s. The two cannot both be trusted; I tag "quarter-note kicks" low. A steady quarter-note bass (0.484 to 0.506 s) is measured and does give the motorik-like regularity; I assign the regularity to the bass, not the kick.

## 3. Corrections of colleagues
- **Feeling, "123 BPM held to a 16 ms beat spread (win_0240) ... machine-like trance":** the beat is not held at 123: bass and drum lags both slide 118.5 to 125 BPM. A local 16 ms spread inside a 20 s window is consistent with a smoothly gliding tempo, which sounds steady locally. "Machine-like" should be softened to "locally very steady, globally drifting" (measured, medium).
- **Form, hit blocks "8 beats at 0.50 s":** correct for 1:00 to 1:40 (matches bass quarter 0.506 to 0.504 s). The tracker 123.05 BPM overstates the early tempo by 3 to 4 percent.
- **Sound, "the mix compensates; stems trade level" (3:45, 4:40, 5:17):** fits my round-1 observation that the drum exit at 5:17 changed the mix by 0 to 1 dB; no objection.
- **Voice, drums last at 5:38.05 (stem at -85 to -88 dB):** that is the separator floor, not a hit; my round-1 figure (last real drum energy 5:18.86, about -70 dB, 10 ms drum max) stands. Not a conflict about audible content, only about threshold.
- **Own correction:** in round 1 I called the opening unlocked and the tracker 123.0 at 30 to 60 s a texture follower; this stands. My round-1 offbeat-kick claim is retracted (1D).

## 4. Connections to other areas
- **Rhythm and form:** the 4 s block engine is two bars of about 120 BPM, and the rhythm section is the form: drums 1:04.8, bass about 1:06, fill 1:52.5 and bass quavers 1:53.4, then a groove whose tempo glides up about 6 percent to 5:17, then the drum decay 5:17 to 5:19 (my 10 ms drum envelope; -19 dBFS to -70 dB in 1.8 s), bass out about 5:24. I would draw the form's "outro" at 5:17, where the pulse stops, and call 5:19 to 5:42.8 free-time tail; this matches form's coda idea but the tail is pulseless, so voice's murmur is not on any beat grid (no claim).
- **Rhythm and sound:** brighter, louder drift to 3:44 to 4:00 (sound) coincides with the tempo's rise: the body gets faster and brighter together, which a listener reads as lift without naming either.
- **Rhythm and harmony:** harmonic rhythm of 1 to 2 bars (2 to 4 s) is the 4 s block halved or kept; at 120 BPM a bar is 2.0 s, so chord changes at 4.0 s are two bars. I cannot test whether chords sit on the stab attacks (that needs the harmony file's chord times against 60.8, 64.8, 68.8, 72.9, 76.8 s).
- **Rhythm and feeling:** the gliding accelerando is the one pulse-level cause of rising urgency that survives all the checks; the kick-syncopation story does not. Listeners feel a steady drive with an unnamed quickening (INFERRED, medium).
- **Era (rule 1):** I add the drum AC result: no phrase-length repetition (0.01 to 0.11 at 3.9 s), plus tempo glide of about 6 percent: against a rigid DAW loop. Peak 0.0 dBFS and digital-zero edges (round 1) still point to modern mastering. Net unchanged: modern master over a human-played or hand-tempo-mapped groove (medium).

## 5. Boundary table (re-checked, rhythm-relevant only)
| boundary | drums | bass | vocals | other | carries it |
|---|---|---|---|---|---|
| 1:04.8 | -81 to -35 dB | enters about 1:06 | none | steady | drums |
| 1:33.8 to 1:36.6 | continue | -50 to -79 dB | none | gapped, mix -20 to -40 dBFS | bass (not silence) |
| 3:30 to 4:00 | continue at -26 dB | about -50 dB | none | pad continues | bass out |
| 5:17 to 5:19 | -19 dBFS to -70 dB in 1.8 s | continues to about 5:24 | n/a | continues, mix stays about -15 dBFS | drums |
| 5:24 | -75 dB | to floor | n/a | continues | bass |
All values are carried from round 1 (10 s stem levels and 10 ms envelopes); I did not re-measure them this round. Silence is used only for 0:00 to 0:11.3 and from 5:42.9 (digital zero; last 3 s contain no peaks; last audible sound 5:42.8 at about -70 dB, from round 1; there are no final drum hits).

## 6. Two new questions
1. **Harmony:** in 1:00 to 1:40 the stabs fall at 60.8, 64.8, 68.8, 72.9, 76.8 s on a local grid of about 120 BPM (2 s bars). Please list the times of every chord change you measured in 1:00 to 2:00 and say whether each lands on a stab (a 2 or 4 s multiple from 60.8 s) or off it; and whether the 4 chord-changes-per-minute rate speeds up with the tempo rise (4.0 s down to 3.95 s by 2:40)?
2. **Sound:** the demucs drum stem yields no clean kick (flat phase histogram on 35 to 110 Hz). From the spectrograms or the stem images, is there a distinct low drum at all (a kick with a defined thump and decay in the 50 to 80 Hz band, not the bass line), or is the lowest layer only the bass and a pad, so that the groove is carried by mid-band hits (snare-like or tom-like) and hats?

## Not recoverable by measurement
- The kick pattern, or whether a kick exists as a separate drum: the demucs drum stem mixes tom, bass and leakage, and my 35 to 110 Hz detector gives a flat phase histogram.
- Whether the tempo glide of about 118.5 to 125 BPM is deliberate rubato or a tempo-mapped edit: only bass IOIs, drum autocorrelation and stems are measurable, and the glide is consistent with both.
- Live kit, sampled kit or drum machine: onset spacing alone cannot say.
- What the 4 s stabs and the opening noise layer are (instrument or sample), and whether they derive from older material: they show only as broadband attacks.
- Intent behind the opening 11.3 s and trailing 18.1 s of digital silence: they could belong to the release or to this file's export.
- Whether the pulseless tail from 5:19 is a performed ending or a fade-out edit: only level and spectrum are measurable.
