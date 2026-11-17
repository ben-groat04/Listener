# video2: SOUND specialist, round 2 (debate round 1)

I cannot hear; everything is from measurements. Confidence H/M/L. Timestamps m:ss. New helpers: `v1/scripts/agents/v2_sound_r2.py` (onset-envelope autocorrelation per stem, HPSS, bass spectrum and stab shapes, voice-burst bandwidth/width/flatness, other-stem at transitions) and `v2_sound_r2b.py` (other-stem band energy per 20 s, 1:56 lift, bass holes 4:20-4:50). Stems: `stems_raw/htdemucs/song/*.wav`, resampled to 22.05 kHz. I read all seven round-1 files and harmony's round-2 file.

## 0. What changed since round 1

1. **The "other" layer's brightening is a spectral-tilt change, not just gain** (section 2). Over 3:00-4:20 it gains +3 dB at 250 Hz-1 kHz, +9 dB at 1-2 kHz, +15 dB at 2-4 kHz and +24 dB at 4-8 kHz. Same rhythm, same pitch classes (harmony). H on the numbers, L-M on the mechanism.
2. **The bass gating is a mute/gate, not a sidechain** (section 3). M.
3. **The 4:38.5 "wideband voice burst" is almost certainly not voice** (section 4). It is 17-30 times flatter (noisier) than any real voice burst and coincides with a 0.4 s hole in the bass. M.
4. **Correction to my round 1, narrator brightness.** I compared 1:05-1:20 (95 % roll-off 2.5 kHz) with 3:45-4:25 (3.8-4.1 kHz) and called it "later narration is brighter". Re-measured on the loudest 30 % of frames: 1:05-1:20 = 2.54 kHz, 2:25-2:36 = 3.27 kHz, 3:24-3:40 = 3.97 kHz, 4:00-4:20 = 3.81 kHz, 4:40-4:59 = 3.12 kHz. So the first phrases are the darkest; the 2:25 narration (a real spoken passage per voice) already sits at 3.3 kHz. That points to **different excerpts or take, not a steady processing trend** (M). I withdraw "brighter and brighter" for the voice.
5. **Correction to my round 1 stem-width story.** I wrote that the narrator was "wider at 3:40-4:20 (-1.6 dB) than at 1:40-2:20 (-9.9 dB)". The full series is -8.8 dB (1:05-1:20), -10.2 (2:25-2:36), -2.3 (3:24-3:40), -1.6 (4:00-4:20), **+1.1 dB (4:40-4:59)**. It widens in two steps, at the 3:24 return and again towards the end, so the late bursts are either stereo-processed or contaminated by the wide "other" layer. See section 4. M.

## 1. Answers to questions put to me

**Rhythm Q3a: is the 3+3+4+3+3 bass a pitched bass guitar, a synth or something doubled in "other"?**
- Pitched, one note per chord slot (harmony: one root per 4 s, so a repeated note, no riff). The bass stem spectrum, averaged over 2:00-2:30 (v2_sound_r2.py section D): 60-120 Hz 55.6 dB, 120-250 Hz 46.5, 250-500 Hz 27.7, 500 Hz-1 kHz 16.8, above 1 kHz 11.8, i.e. the fundamental region leads the next octave by 9 dB and everything above 250 Hz is 28 dB or more down. The roots (B1 61.7 Hz, A1 55 Hz, D2 73 Hz, E2 82 Hz, G2 98 Hz) all fall inside the 60-120 Hz band. That is a **low-passed or sine-dominated bass tone**. A DI'd bass guitar, a sampled bass and a filtered synth bass would all give this; I cannot separate them (L).
- Later (4:30-4:45) the same stem gains upper content: 500 Hz-1 kHz is +10 dB and above 1 kHz +6 dB relative to 2:00-2:30 (23.9 and 17.6 dB). Either the bass gets brighter (filter, drive) as the track peaks, or the separator lets more of the bright "other" layer into the bass stem. I do not know which (L).
- Does "other" carry the 3-sixteenth cross-rhythm? **Partly, and that corrects the picture of "other" as pure sixteenths.** Onset-envelope autocorrelation of "other" at 1:44-3:20: 0.125 s 0.67, 0.25 s 0.63, **0.375 s 0.70**, 0.5 s 0.72, 0.75 s 0.61, 1.0 s 0.67, 2.0 s 0.81. At 3:40-4:30: 0.125 s 0.47, 0.25 s 0.51, **0.375 s 0.61**, 0.5 s 0.56, 0.75 s 0.53, 2.0 s 0.76. At 4:45-5:00: 0.375 s 0.62 against 0.5 s 0.55. In 3:40+ the 3-sixteenth lag is the strongest short lag, above the beat (0.5 s), and in the same sections the drums' strongest short lag is 0.5 s (0.41) and the bass's is 0.375 s (0.23-0.34). So "other" is a mix of a sixteenth grid and a 3-sixteenth figure (M). The 2.0 s lag is 0.68-0.81 in "other": a bar-length repeat, a looped pattern.
- Is the bass "gated by a sidechain or played stabs"? See section 3.

**Voice Q2a: do the 3:24+ bursts share the narrator's band-limited character, or are they a different source?** Same bandwidth, different spatial treatment (v2_sound_r2.py section E, loudest 30 % of frames):

| Segment | 95 % roll-off | 99 % roll-off | Centroid | Flatness | Stem S/M |
|---|---|---|---|---|---|
| 1:05-1:20 narration | 2.54 kHz | 3.34 kHz | 704 Hz | 0.0008 | -8.8 dB |
| 2:25-2:36 narration | 3.27 kHz | 4.16 kHz | 1355 Hz | 0.0010 | -10.2 |
| 3:24-3:40 bursts | 3.97 kHz | 4.79 kHz | 1342 Hz | 0.0014 | -2.3 |
| 4:00-4:20 bursts | 3.81 kHz | 4.25 kHz | 1150 Hz | 0.0007 | -1.6 |
| 4:40-4:59 bursts | 3.12 kHz | 4.20 kHz | 1244 Hz | 0.0027 | +1.1 |

The hard edge near 4-5 kHz, the centroid at about 1.2-1.4 kHz and the low flatness are the same as the 2:25 narration, so the bursts have **a voiced, band-limited spectrum like the narrator's** (M-H); I see no extra bandwidth that would mark a choir patch or a vocoder. What differs is **width** (the stem S/M rises 10 dB) and, at 4:40-4:59, flatness (0.0027, about 2-4 times the others). A voice sample that has been stereo-widened or sent to a stereo delay/reverb would show exactly that; so would leakage of the wide, noisy "other" layer into the vocal stem as the mix gets dense (M for either; I cannot choose). So the "voice has become texture" reading is supported by the sound as well as by level.

**Voice Q2b: is the loud 4:38.5 wideband burst a voice or a drum/noise hit leaking?** Almost certainly not a voice (M). Evidence (v2_sound_r2.py, 0.25 s steps from 4:37):
- Vocal stem: -38, -26, -39 dB at 4:38.5-4:39.0, silent (-62 to -70) either side. A single 0.4-0.5 s event, not a run.
- Spectral flatness 0.024 and centroid 2378 Hz, against 0.0007-0.0027 and 1150-1355 Hz for real bursts: **10-30 times flatter, twice as bright**. Voiced speech has harmonic structure; this has none.
- The bass stem drops to -65 to -68 dB for exactly 4:38.50-4:38.75 (bass-hole list: 4:38.38 -45, 4:38.50 -65, 4:38.62 -65, 4:38.75 -68) while the drums are at -22 dB (no louder than their neighbours). A simultaneous bass dropout and broadband noise burst is the signature of a **transition effect** (noise hit, reversed or struck cymbal, impact) rather than a sung or spoken sample. The first real regular burst follows at 4:40.7 (-26 dB) and the bass has a one-frame hole at 4:40.25.
- This is also the first gap in the bass before the 4:48.5 gating, i.e. a **precursor**: the low end is nicked at 4:38.5, again at 4:42.75-4:43.5, 4:46.75, then removed at 4:48.5. That supports Form's reading of gradual subtraction from 4:36 rather than one cut (M-H), and is a small correction to "bass gated at 4:48 only".

**Harmony Q (SOUND): in 0:00-0:28, which instrument carries the pad and the G4/E4 and G4/D5 pulses? What changes in "other" at 0:29 and 1:25-1:29?**
- Pad: I cannot name it. What the stem shows: harmonic-to-percussive ratio 14 dB at 0:05-0:25 (highest of any section; flatness 0.0000, an almost purely tonal signal), centroid 790-850 Hz, narrow bandwidth (0:00 window band energy: 250 Hz-1 kHz 30.4 dB, 2-4 kHz -6.8 dB, 4-8 kHz -30.8 dB), onsets at 4 per second on the quaver lattice (rhythm) so it is a slowly pulsing sustained timbre. A synth pad, organ or swelled/e-bowed guitar all fit. Parallel horizontal partials and stereo width (L/R correlation -0.2 in the "other" stem alone) make a chorused or ensemble-type sound likely (M for width, L for identity).
- At 0:29 (bass and drums enter): **nothing changes in "other"**. RMS -27.6 (0:28) / -26.9 / -27.2 / -25.2 dB, centroid 847 / 802 / 793 / 718 Hz, correlation -0.08 to -0.22. The layers enter underneath a pad that carries on unchanged (H). The 0:00-0:28 "intro" is the same pad that lives under the first groove; what changes at 0:28 is only the low end (levels per second, bass -85 to -22 dB).
- At 1:25-1:29: "other" dips from -24.8 to -33.2 dB at 1:26 (the break), then at 1:28 returns at -24.8 dB with the centroid higher (848 Hz at 1:26 to 1113-1140 Hz at 1:28-1:30) and correlation moving from -0.05 to +0.07-0.13. So the re-entry arrives with a **brighter "other" and a slightly narrower image**, not just the drums returning (M). Band table: 1-2 kHz and 2-4 kHz are already near +28 and +11 dB in the 1:00-1:20 window and keep rising slowly after; no step at 1:28 in the 20 s bins, so the brightening there is small (about 100-250 Hz of centroid) rather than a new layer.

**Lineage Q2: can "other" be split into a guitar-like and a synth-like layer, and is there a delayed repeat at 0.375 s?**
- Split: HPSS on "other" (harmonic/percussive energy, dB): 14.0 (0:05-0:25), 11.5 (0:30-1:00), 7.0 (1:00-1:25), 5.8 (1:40-2:20), 7.7 (2:40-3:20), 7.1 (3:20-3:36), 6.4 (4:00-4:40), 8.2-8.3 (4:40-5:00). It falls from 14 to 6 dB between 0:20 and 1:40 (more transient energy) and then stays 6-8 dB for the rest. So from about 1:00 "other" is a **sustained part plus a plucked/attacked part** in one stem; HPSS can separate them numerically but not name them as guitar versus synth (L). The attack content arrives gradually across 0:20-1:40, not at one entry.
- Delayed repeat: the 0.375 s autocorrelation lag exceeds the 0.5 s beat lag in the 3:40+ sections (0.61-0.62 against 0.55-0.56). That is what a dotted-quaver delay would add, **but it is also what a programmed 3-sixteenth pattern gives**, and 0.125 s multiples are all high. I did not measure a decaying echo of an isolated note (the "other" onsets are too dense); **I cannot confirm a delay effect (L)**. The bass shows the 0.375 lag at 0.23-0.34 in 1:44-3:20 and 3:40-4:30, but it is a root repeated by a sequencer and has no echo tail.

**Feeling Q2 and Form Q3: is the rise of "other" from -25 to -15 dB, the 1:56 lift, and the 2:50-4:30 brightening layering or opening up?**
- 1:56: "other" per second -27.1 (1:55) then -22.9 / -21.3 / -21.0 at 1:56-1:58 and about -21.4 to -22 after. A **+4.5 dB step within about 2 s and then flat** (H). The step lasts, so it is a level or part change on a bar line, not a swell.
- Band energy of "other" per 20 s (60-250 Hz / 250 Hz-1 kHz / 1-2 kHz / 2-4 kHz / 4-8 kHz, dB, v2_sound_r2b.py):

| Window | 60-250 | 250-1k | 1-2k | 2-4k | 4-8k |
|---|---|---|---|---|---|
| 0:00 | 4.7 | 30.4 | 17.5 | -6.8 | -30.8 |
| 1:00 | 28.8 | 32.7 | 28.3 | 11.4 | -13.1 |
| 2:00 | 28.1 | 35.8 | 28.3 | 18.7 | -1.1 |
| 2:40 | 28.8 | 34.9 | 25.1 | 13.3 | -5.7 |
| 3:00 | 33.6 | 38.7 | 29.0 | 19.4 | -0.6 |
| 3:20 | 34.5 | 39.9 | 32.1 | 25.6 | 8.5 |
| 3:40 | 34.9 | 40.8 | 36.6 | 31.5 | 18.6 |
| 4:00 | 34.1 | 41.5 | 38.3 | 34.5 | 21.8 |
| 4:20 | 33.4 | 40.9 | 38.4 | 35.1 | 22.9 |
| 4:40 | 36.6 | 36.2 | 27.6 | 18.4 | 11.8 |

- Between 3:00 and 4:20: +2.8 dB at 250 Hz-1 kHz but **+23.5 dB at 4-8 kHz** (and +15 dB at 2-4 kHz). This is a large tilt, so "the same part compressed and widened" would not produce it. At the same time the onset rate stays 7.2-7.9 per second and HPSS ratio 6-8 dB (no new rhythmic figure appears) and harmony reports the same pitch classes. So the layer is the **same rhythmic and harmonic material getting much brighter**: consistent with a filter opening, an added drive/saturation stage (which adds upper harmonics), or a doubled octave-up layer playing the same rhythm. I cannot separate these (L-M). I lean towards "opening/drive" as the simplest account, because the 250 Hz-1 kHz body grows by only 3 dB.
- Steps are not smooth: the 60-1k bands jump 4-6 dB at the 2:40 to 3:00 window (the loop B switch at 2:36.8, which harmony places), and the top band jumps in 3:20 (+9 dB) and 3:40 (+10 dB), then flattens at 4:00-4:20; at 4:40 the top falls 11 dB while 60-250 Hz rises, so the layer returns to a low pad (412 Hz centroid) with the stabs. Timing of steps is only as exact as the 20 s windows; the 3:36 step in round 1 was found at 1 s resolution. Mapping to cycle starts (3:24.8, 3:36.8) is a question for form.
- Hat leakage check (6-10 kHz): "other" HF level is -71.5 dB (1:40-3:20) and -65 dB (4:45-5:00), against drums at -41 to -43 dB, so leakage of hats into "other" is at least 22 dB down. But at 3:40-4:30 "other" is at -52 dB in that band (against the drums' -41 dB) and its 6-10 kHz envelope correlates **negatively** with the drums' (-0.17); so the 3:40+ top end in "other" is not a copy of the hi-hat envelope; it belongs to that layer (M). This also answers my round-1 worry that the sparkle might be hats mis-assigned.

**Form Q3 (sound side): is 0:42 and 3:36 an arrangement or a production change?** 0:42 (round 1): the bandwidth opens by 26 dB at 4 kHz+ in one second; "other" is unchanged at 0:40-1:00 compared with 0:20-0:40 in the 250 Hz-1 kHz band (32.7 vs 32.3 dB) and the top band is +4 dB in 2-4 kHz and +5 dB at 4-8 kHz. So the mix-level jump comes from the voice plus a small brightening of "other", not from a new instrument (M). 3:36: see tilt above; production-type (brightness) change on an unchanged part.

## 2. The bass gate, answered (Rhythm Q3b, Form claim "sidechain or gate")

- If the bass were sidechained to the kick, its envelope would dip on every kick (four per bar, 0.5 s). Folded onto the 0.5 s beat (v2_sound_r2.py section D), the bass envelope over 3:40-4:40 is **flat to within 1.2 dB** across the beat (-19.7 to -17.7 dB), so there is no sidechain pumping in the main groove. At 1:50-2:20 it varies by 4.6 dB over the beat (-18.3 at the kick to -13.7), which could be a gentle sidechain or just the note shape; M for "light ducking" there, H for "none" in the later groove.
- The final stabs (4:50.3, 4:52.6, 4:54.3, 4:56.6, 4:58.3) all peak at -14 to -16 dB, the same level as the running bass (-14.8 median), with decay to -20 dB in 139-522 ms. A sidechain would hit the pattern on the beat; these hits follow the 9+7 pattern from rhythm and are **not** on the kick lattice. So the bass is **muted by gating or played as short notes in a sequence** (M). That agrees with rhythm's "played stabs" and not with Form's "sidechain or gate" ambiguity: the evidence is for gate/sequence.
- The attack times I got (46-372 ms) are dominated by my threshold (-45 dB), so I do not trust them as "soft" or "hard" attacks.

## 3. Connecting sound to the other specialists

- **Rhythm and form:** the sound steps and the groove steps match. The three mix-loudness steps I reported (0:28, 1:28.5, 3:36) are drums and bass entries (0:28, 1:28.5) and an "other" brightness step (3:36). The drum stem sits flat at -18 to -19 dBFS from 1:28 on, so the **drums fix the loudness floor and the "other" and bass layers move the ceiling**. With a mono centred kick, mono bass and wide "other" (round 1 stem S/M table), the song has a fixed rhythmic skeleton and a wide, changing upper layer. The form's engineering of tension is therefore carried by the upper layer's tilt (3:00-4:20) and by subtraction (4:38.5 onwards), not by changing the rhythm.
- **Harmony:** pitch content is unchanged when the "other" layer brightens 3:40-4:20 (harmony round 2), so it is a timbre development. The one place the sound shows new harmony is the third dropping out in the last minute (harmony: D only 0.08), which fits my 412 Hz "other" centroid at 4:40-5:00: a low open-fifth pad (B-F#-A) under the stabs.
- **Voice:** my measurements add one fact to your "voice becomes rhythm": the 4:40-4:59 bursts occur at 2.0 s intervals (voice) over a bass with holes at 4:42.75-4:43.5 and 4:46.75, and one ten-bar run of identical-looking blocks; the burst bandwidth is the narrator's but the stereo width is wide (+1 dB S/M), so the bursts have been **moved into the instrument layer's space** (stereo-processed or leaking), which is the sound-design counterpart of "foreground voice to texture".
- **Feeling:** the production path is "narrow, dark, wide-phase intro (corr near zero for the pad alone, -0.2) to a mono-centred, loud, increasingly bright wall". Feeling's "no air" at 1:40-2:30 (mix width 0.30-0.35) agrees with my S/M and correlation numbers (drums -22 dB, bass -17 dB S/M). The late sparkle (4-8 kHz +24 dB in "other") is what a listener would hear as **"opening up, more urgent"** while the low end stays fixed. Interpretation M; numbers H.
- **Lineage:** I find no evidence of a faded, hissy, "vinyl" texture (round 1: 4 kHz+ at -70 dB in 0:34-0:41, no noise floor), and the late spectrum is clean and bright, so the sound lineage is modern electronic/post-rock production using archive speech as content, not archive fidelity as a texture (supports Lineage: "method not sound"; M). The dotted-quaver echo-guitar idea stays unconfirmed (L).

## 4. Limits

- Demucs stems carry bleed. Widths, flatness and per-stem spectra are indicative. The 4:38.5 event may still contain a short voice component; the flatness figure says it is dominated by noise-like content.
- 20 s bands hide the exact moment of each step in "other"; round-1 1 s data place the biggest at 3:36.
- Instrument identity remains unknown for pad, bass, "other" and drums. I report band-limit, harmonic ratio and envelope only.
- The autocorrelation at 0.375 s cannot distinguish a 3-sixteenth pattern from a dotted-quaver delay.

## 5. Two new questions

1. **To Rhythm:** the bass has holes at 4:38.38-4:38.8 (about 0.4 s), 4:40.25, 4:42.75-4:43.5 and 4:46.75, before the full gating at 4:48.5, and a noise-like event (flatness 0.024) sits at 4:38.5-4:39.0. On your 2.0 s bar grid, do these land on a bar start, a beat, or an off-sixteenth, and do similar one-beat bass holes or noise hits occur at other section changes (1:24-1:28.5, 2:36.8, 3:36.8)? That decides whether it is a repeated transition device (an "impact plus bass cut") or a one-off.
2. **To Form (with Harmony):** the "other" layer's top band (4-8 kHz) climbs 9 dB in the 3:20 window and 10 dB in the 3:40 window, and its 250 Hz-1 kHz body steps at the 2:40-3:00 window. Loop B cycles start at 2:36.8, 2:48.8, 3:00.8, 3:12.8, 3:24.8, 3:36.8, 3:48.8. Do you place the brightening steps on 3:24.8 and 3:36.8 (cycle starts), or at the 3:20-3:24 section marker in the audio features? If on cycle starts, can we say the brightening is a bar-aligned part or filter change, and name the four-step order (low body 2:36.8, mid 3:00, bright 3:24.8, brightest 3:36.8) as the form's real "build"?
