# video1: SOUND specialist, round 2 (debate)

Evidence keys: [lv] per_second_levels.json; [img NNNN] music_views/window_NNNNs.png; [R1-x] another specialist's round-1 file; [R2-h] harmony round 2; [s2] v1/scripts/agents/sound_r2.py and sound_r2b.py (new this round, on htdemucs stems at 22.05 kHz); [s1] my round-1 scripts. I cannot hear; all is inferred from measurement. Times m:ss. Demucs stems are proxies: leakage between stems is possible and no number below is an "instrument" measurement.

## 1. What changed since round 1
1. The 42.6 Hz sub is **not a perfectly steady tone**: it starts 3 to 6 Hz sharp and settles within about 0.3 s. A designed, synthesised impact is now medium-high, not just medium (section 2.1).
2. The "other" stem is **not one wall**. It has four distinct timbral states (low-D drone, mid wall, thin high fifths, bright wide wall). This answers Feeling and Form (section 2.2).
3. Drum sound: kick and hat peak levels vary only modestly, which does not prove a machine and does not prove a human (section 2.4). I withdraw nothing, but I tighten my wording.
4. I accept Harmony's finding that the sub is 42 cents under F1 and constant, and the correction that my "D/E" remark was label leakage. I also accept that my "F1 or a little flat" was a rounding of a number that deserved to be quoted exactly.

## 2. Answers to questions put to me

### 2.1 Harmony: does the sub show a glide, click or noise burst; is it a designed impact? (medium)
FFT peak (16x padded, 0.2 s window slid at 0.1 s) of the bass stem after each drop [s2]:
- Frequency track, first 0.4 s: 2:01 48.1, 44.2, 43.6 Hz; 2:07 45.8, 44.1, 43.3; 2:13 49.2, 44.7, 43.6; 2:19 46.4, 43.8, 43.4; 2:25 48.9, 45.0, 43.6; 2:31 47.2, 43.9, 43.4. After about 0.4 s every drop sits at 42.2 to 42.8 Hz for the remaining 1.2 s.
- So each hit starts 3 to 6 Hz (about 120 to 200 cents) above its resting pitch and falls to 42.6 Hz within about 0.3 s. That is the classic fall-to-pitch of a kick-drum or 808-style sub oscillator. Caveat: a 0.2 s window at 45 Hz is only about 9 cycles, so the exact numbers are blurred; the direction is the same at all six drops, which is why I trust it.
- Click or noise burst: energy above 300 Hz in the first 0.5 s is only 0.8 to 1.7% of the stem's amplitude at all six drops [s2]. No broadband click. The attack is a soft rise: 10 to 90% rise times of 20 to 110 ms (2:01 23 ms, 2:07 about 100 ms, 2:13 66 ms, 2:19 about 30 ms, 2:25 77 ms, 2:31 70 ms; the 2:19 value is the least reliable, peak amplitude only 0.03 against 0.12 to 0.19 for others). Plucked-bass attacks are generally faster and carry overtones; this one has neither.
- Reading: a synthesised sub with a short downward pitch drop and a rounded attack, tuned to a fixed 42.6 Hz and triggered, not played. Medium-high. The fact that the drop amplitude is irregular (peak 0.03 to 0.19) is partly separation, partly the drum stem masking it; I do not read it as velocity.
- Consequence for Harmony: because the resting pitch is fixed and the start is sharper, the listener hears "thump with a falling edge", a percussive event more than a pitched root. That supports Harmony's wording "weight, not a note".

### 2.2 Feeling: do the 2:00 to 2:14 wall and the 1:30 to 1:55 wall differ in timbre; guitar-heroic or machine-like? (medium on the difference, low on the labels)
`other` stem, mean spectrum [s2]:

| Time | Centroid | 85% roll-off | Strongest bins | Reading |
|---|---|---|---|---|
| 0:30 to 1:00 | 706 Hz | 1.6 kHz | 145, 151, 221, 291 | D3-centred wall, mid-weight |
| 1:30 to 1:49 | 650 Hz | 1.3 kHz | same | same wall, slightly darker |
| 1:50 to 1:59 | **333 Hz** | **452 Hz** | 145, 151, 156, 441 | very low, near-drone D3 only |
| 2:01 to 2:13 | **1480 Hz** | 2.3 kHz | 441, 587, 883, 1174 | A4, D5, A5, D6: high open fifths and octaves |
| 2:15 to 2:33 | 1010 Hz | 1.8 kHz | 221, 441, 657, 786 | mixed: A3, A4, E5, G5 |
| 2:40 to 3:00 | 861 Hz | 1.8 kHz | 140 to 156, 296 | back to the D3 wall |

- So the 2:00 block is a *different sound*, not the same wall turned down: high, thin, in octaves and fifths (A and D) rather than the D3 mid-register chug. It is 12 to 15 dB quieter [lv] and the stereo width collapses at the same time (0.29). It reads as a small, bright, hollow figure sitting on top of the sub, not a wall.
- The 1:50 to 1:59 stretch is the opposite: the `other` stem loses almost everything above 450 Hz. This is exactly Form's "roll-off of the wall's top end from about 1:49.5" (centroid 1.45 to 0.96 kHz in Form's measure; mine, with a different stem normalisation, 650 to 333 Hz). It is a real darkening of the guitar layer for about 10 s, ending at the drop at 1:59 to 2:00. Caution: when the bass has partial stem leakage into `other` in a sparse moment, low bins can be inflated. The bass stem is present at 1:49 to 1:58 [lv], so I give this medium confidence.
- Heroic versus machine: I cannot tell guitar from synth. What I can say is that the 1:30 to 1:50 wall has the dense, noise-like partials of high-gain distortion (round 1, [img 0100]) and the 2:00 block has cleaner, widely spaced octave-and-fifth peaks. The first leans "guitar-rock", the second leans "synth or clean-ish picked octaves". If a listener hears a human band in the wall and a machine in the middle, the contrast is real, but the labels are my reading, not measurement. Low.

### 2.3 Form: which form events are timbral gestures? (medium)
- **0:00.1 to 0:00.7 swell.** Broadband RMS in 20 ms frames [s2]: about -58 dB at 0:00.0, creeping to -48 dB by 0:00.45, then -43, -41, -39, -33 by 0:00.65, then a hit at about -9 dB. A rise of about 25 dB over 0.6 s into a hit is a reverse-cymbal or noise-riser gesture (the stem plots show it as a rising sweep). Evidence is the envelope only; I cannot identify a reversed sound. Medium.
- **1:49.5 roll-off**: see table above; a darkening of the `other` layer by about 300 Hz in centroid.
- **2:48 stop and return**: drum stem after the stop is brighter. Drum centroid is 395 Hz at 2:30 to 2:45 and 1189 Hz at 2:50 to 3:00, 1083 Hz at 3:00 to 3:08; the share of drum energy above 5 kHz goes from 3.3% to 12.4% and 11.6% [s2]. So after the stop the hat/crash share is about four times larger: Form's "cymbal-led, bright" is confirmed. It also matches my round-1 finding of the brightest centroid (2.6 to 2.8 kHz mix) at 3:00 to 3:08. The 2:48 stop is therefore both a gap (0.4 s) and a change of drum voicing, which is the strongest timbral reset in the piece.
- **Sub drops 2:01 to 2:33**: timbral gesture in the low end (section 2.1).
- **Bass gating** (1:15, 1:58, 2:38): level and spectrum events rather than melodic ones.

### 2.4 Rhythm: gated acoustic, drum machine or sample loop; velocity variation; kick synthetic? (low to medium)
Tests on the drum stem, 0:20 to 1:00 [s2]:
- Peak amplitude variation (coefficient of variation) of detected onsets in a band: kick 40 to 120 Hz, 119 events, CV 0.18; hats 6 to 10 kHz, 64 events, CV 0.27; snare/mid 1.5 to 4 kHz, 60 events, CV 0.27. 
- Reading: kick levels are fairly even (CV 0.18), hats and snare vary somewhat more. A drum machine with no variation would be near 0 (plus separation noise); a human kit in a loud rock mix commonly shows 0.1 to 0.3 on the kick and more on hats. Both a lightly humanised sample kit and a limited real kit fit. **I cannot separate them.** My honest position: not clearly a machine and not clearly a human; the 110 ms median decay (round 1) means it is either gated, heavily damped or sample-based.
- Per-16th hat grid CV of 1.2 is not informative (rests and accents dominate), so I did not use it.
- Kick synthetic or real: I did not measure kick spectral decay or pitch glide; this remains open. The only designed low sound I can show is the sub in 2.1.

### 2.5 Voice: is the voice band-limited like a 1960s optical track; does `other` carry matching hiss; is 2:44 the same recording as 0:27? (medium on band, low on repeat)
- Band limit: the vocal stem has 95% of energy below 3.7 kHz at 0:19 to 0:24, 3.5 kHz at 0:28 to 0:32 and 3.4 kHz at 2:44 to 2:48 [s2]; share above 5 kHz is 0.3 to 1.0% of the burst [s2]. That is narrower than Voice's "6 to 19% above 3 kHz" only if measured as a share above 5 kHz; the two agree on a falling top end. Consistent with a mid-century optical or radio source; not proof, since demucs and lossy encoding both reduce the top end. Medium.
- Hiss in `other`: the `other` stem has 0.0 to 0.1% of energy above 5 kHz during the speech bursts [s2], so it contains no bright hiss that could leak into the vocal stem. The 8 kHz noisy bursts that Voice saw in [img 0100, 0120] therefore come from cymbal/guitar fizz leaking into the vocal stem or from the speech's own sibilants, not from a film-hiss bed that `other` retains. This also fits my round-1 observation that the vocal stem is silent at about -66 dB between phrases: no constant noise floor. Medium.
- Same recording at 0:27 and 2:44? Waveform cross-correlation of the vocal stem is 0.09 (no exact copy found); amplitude-envelope correlation after best lag is 0.64 [s2]. A low waveform match through two different mixes proves little: demucs, mix level and the other instruments differ. Envelope similarity of 0.64 is moderate and consistent with a repeated phrase, not conclusive. Low. I defer to Voice and the lyrics transcripts.

## 3. Corrections
- **Mine, sub tone is a "pure constant sine"** (R1 3.2b): constant pitch at rest, yes; it has a short downward start. The R1 phrase "effectively a pure sine" stands for the resting tone only.
- **Mine, "other" as one wall** (R1 3.3): wrong in emphasis; there are four states.
- **Mine, "F1 or a little flat"**: use 42.6 Hz, per Harmony.
- **Mine, "bass is not the main width driver"**: correlation of width and bass dB of 0.01 across the whole track still stands, but the 2:00 narrowing is also because the `other` layer there is a thin high figure. Both effects coincide at 2:00; they can't be separated by correlation.
- **Harmony R2** says the stem is "identical at all six drops". Not exactly: pitch is identical at rest, but peak amplitude varies five-fold (0.03 to 0.19) and attack times between 23 and about 110 ms. I think the difference is due to masking and separation, but it is a measured difference.

## 4. Connections to other specialists
- **Sound and Harmony.** A rounded, glide-started 42.6 Hz thump under high open fifths is a production decision that removes the third entirely: the only low note available to the ear is not on a chord tone. "All weight, no third" is thus a mix property.
- **Sound and Rhythm.** The sub is gated on the 8-beat cycle while the drums never stop; the drum brightness change at 2:48 (more cymbal) is the only rhythmic-instrument timbre change. Rhythm's evidence that the track feels like a fixed engine fits the constant drum stem: the machine-like regularity is largely a mix-structure fact (drums never gated), not necessarily a machine-made sound.
- **Sound and Form.** All the strongest section boundaries are timbral: bass on/off (1:15, 1:40, 1:58, 2:38), `other` darkening (1:49.5), thin-fifths block (2:00 to 2:14), cymbal-led final (2:48). Level changes are small (round 1: P10 to P90 2 to 3 dB). Form is built from timbre, density and width.
- **Sound and Feeling.** Hot, loud, wide production with brief dry gaps (0.3 to 0.4 s stops) is a "controlled" rather than "mechanical" shape: strong constant energy, sharp stops. The thin 2:00 block feels small because the width falls to 0.29 and the wall rises into high fifths at lower level; the loud 1:28 to 1:49 stretch is wide (0.67) and dense. Which of the changes a human feels most is a listening question; the largest measured jumps are width (0.29 to 0.65) and the bass gate (4 to 5 dB), and the stop at 2:48 (-22 dB for 0.4 s).
- **Sound and Voice.** Speech at -23 dB under the band and narrow in bandwidth is "from another time" by spectrum alone, as in round 1. A narrow voice under a wide band is also a space decision: the voice is centred and close.
- **Sound and Lineage.** Gated sub, drums-as-bed, archive speech as texture: production language shared by electronic and post-rock band music of the 2010s. Still only a "fits", not a claim about this artist's practice.

## 5. What I still cannot say
Guitar or synth in any state of `other`; whether the thin 2:00 figure is picked or sustained; whether there is delay or reverb on the figure (the stems cannot separate sustain from tail); kick sample versus acoustic; the exact repeat identity of the speech; LUFS.

## 6. Two new questions
1. **To Rhythm:** at the six sub drops the sub starts with a 20 to 110 ms rise and a downward pitch fall of about 0.3 s. Is the kick drum or a drum accent coincident with the sub's onset to within 20 ms at every drop, or is the sub offset (before or after the grid beat)? If the sub is late by 30 to 100 ms, the "drop" would feel behind the beat; if it is on the kick, the two read as a single sound.
2. **To Voice:** the speech burst at 2:44 to 2:48 has a 0.64 amplitude-envelope correlation to the burst at 0:27 to 0:32 but no waveform match. Does the transcript show the same sentence (and, if so, is the second reading the same take, or a re-recorded or re-edited version)? That decides whether the stop at 2:48 is a "callback" production device on the same speech.
