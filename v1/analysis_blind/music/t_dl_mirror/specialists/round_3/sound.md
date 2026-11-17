# t_dl_mirror: SOUND specialist, round 3 (blind, final)

Read: all seven round-2 files and harmony's round 3. New run: `v1/scripts/agents/sound_r3_tdl.py` (100 ms and 50 ms stem envelopes, onset-aligned averages, Welch of the bass stem, 60-120 s). Stems are demucs estimates of a limited mix; times m:ss. Tags: measured, INFERRED, speculative; high/medium/low.

## 1. Answers to questions put to me

**Feeling Q2: does the limiter or a sidechain make the hooks' equal vocal level, and does the bed duck under the voice? (measured, medium)**
- The bed does not duck. Other-stem level on onset-aligned averages (9 vocal entries after at least 1 s of silence, 0:10-3:40, 100 ms frames) stays within about -2.3 to +2.1 dB of its pre-onset level from 0.5 s before to 1.0 s after the voice enters. Mean other-stem level with voice active -28.7 dB, inactive -27.3 dB: 1.4 dB, in the wrong direction for ducking (quieter with voice, but inside the scatter).
- The mix steps up, not down, at a vocal entry: median +7 to +9 dB from 0.5 s after onset. That is the bass entering with the voice (bass stem +23 to +36 dB re pre-onset; drums +/-8 dB scatter), not the voice. Bass mean with voice active -38.6 dB, inactive -32.3 dB is the opposite sign only because the bass is dropped in verses and the voice is present there; the entry-aligned figure is the reliable one. So the entry gesture is "voice and bass arrive together", as round 2 found, and I see no gain-reduction dip in the bed.
- Whole-file 1 s correlation of vocal level with bed level: -0.41; with mix level: +0.43 (0:10-3:35). Weak, and both come from section structure rather than pumping.
- Therefore the near-equal hook vocal RMS (within 0.8 dB) is not shown to be limiter-made: the limiter would have to pump the bed, and the bed moves by about 1-2 dB. More likely a level-matched repeated phrase (or the same sample), possibly compressed before the master (INFERRED, low-medium; a clip-limiter with a fast release on a dual-mono file could hide some of it). Cannot be separated further.

**Form Q: is the 3:34.0 to 3:35.3 vocal fall a fader, tail or gate? (measured, medium-low)**
Vocal stem, 50 ms RMS: about -19 to -21 dB through 3:33.5-3:34.0; dips to -29/-40 at 3:34.1-3:34.2; back to -21 to -26 until 3:34.6; then -32 to -48 by 3:34.7-3:34.9; -34 to -42 to 3:35.2; -54 to -61 from 3:35.2 to 3:35.4; -61 to -73 afterwards (3:35.5-3:36.5). Slope 3:33.5-3:34.5 is -9.2 dB/s, 3:34.5-3:35.1 -6.3 dB/s. This is not a smooth fader (it moves up and down within the fall), not a repeating tail (no repeats at 0.635 s spacing; levels after 3:35.5 are -61 to -73 dB, flat), and not a single gate edge. It looks like phrase-by-phrase thinning with the last words falling away, with a floor around -65 to -70 dB that is stem residue. For form: call 3:35.1-3:35.3 the end of the voice (the last vocal activity above -50 dB is about 3:35.2), with no effect tail (INFERRED, medium-low). Extra: the other stem has a 100 ms hole of about -52 to -55 dB at about 3:36.1-3:36.2 against about -27 dB around it: a short bed dropout, not a mix mute (not checked in the mix, so I do not call it silence).

**Harmony and lineage Q: is the bass a sub-sine, does the 2nd harmonic carry it, is it at +13 cents? (measured, medium-low)**
Welch of the bass stem, 1:00-2:00, share of 20-2000 Hz power: 20-30 Hz -21.6 dB; 30-45 -19.0; 45-60 -12.0; **60-90 -1.7**; 90-130 -14.1; 130-200 -9.3; 200-400 -11.0; above 400 -29. Peaks: 74.7 Hz (the largest by 14 dB over any other peak, -24.7 dB), 90.2 Hz, 52.5 Hz, 43.1 Hz. So in this stem most of the power is at the D2 position (74.7 Hz; D2 equal-tempered 73.42, so about +30 cents, within a 0.7 Hz-bin resolution of 65,536 points it is +25 to +35 cents; coarser than pyin's +15). The 37 Hz fundamental (D1) is weak (-19 dB), so the pitch is carried by the second harmonic or the line is mostly on D2 in that minute. The bass is not a pure sub-sine: there is real energy at 130-400 Hz (-9 to -11 dB per band, together about as strong as the 90-130 band). Whether that is harmonics of a synth bass or stem bleed of the bed's 148 Hz partials I cannot say. Verdict: a low pitched tone with the energy centred on 60-90 Hz and a harmonic skirt; "sub-synth or re-pitched sample" is not decidable (INFERRED, low). Shares the bed's tuning: the peak at 74.7 Hz is sharp of equal temperament by about the bed's offset or more (+25 to +35 against +13 to +14 cents), consistent with lineage's +15 to +18 and the same direction; with the 0.7 Hz bin I would not claim it is the same figure. Medium-low that bass and bed share a tuning reference; voice does not (harmony round 2-3).

**Rhythm Q (my round-2 question: kick across the mutes)**: not answered in the files I read; rhythm's round-2 file did not reach it. I do not carry any claim from it.

## 2. Corrections and agreement

- I accept harmony's measurement that F5 (698 Hz) is 23-28 dB under D5 in the bed except in the walks. That supports my partial-series reading of F# and C as timbre; the drone carries no third. Tag INFERRED, medium-high carried.
- My round-2 "hook is gated" and "dry close vocal" stand. The hook vocal is active in 72-78 % of 50 ms frames, so the equal level across hooks follows from a repeated phrase, not a limiter effect (see above).
- Carried unchanged, with tags: end of track (last audible 3:56.45, -57 dB, about eleven 3 dB-prominence peaks, no clean closing hit, 2.74 s digital zero); clipping runs (3,354 samples, 80 ms at 2:57.44-2:57.52 followed by a -94 dB 20 ms full-mix mute); 8.03 kHz wall about 79 dB deep.
- Form's "3:35.1 end of voice": agreed on measure (last activity above -50 dB about 3:35.2).

## 3. How the sound serves the others (final connections)

- **Form**: the arrangement works by subtraction under a fixed ceiling. The mix steps +7 to +9 dB when bass and voice enter together (measured above) and falls by the same amount when they leave; nothing else changes, because the bed does not duck and does not swell.
- **Rhythm**: the kick (65 to 40 Hz) and the bass (centre about 75 Hz) overlap in the same sub region, which is why the gated bass leaves the low end thinner rather than empty.
- **Harmony**: drone thirdless (F5 absent), third and seventh are overtones; the voice's F carries the minor colour.
- **Feeling**: the effect is closeness and flatness: dry, mono, nothing above 8 kHz, a median 10 ms level -11 dB with 3-5 dB movement. The hard edges at 0:10.6 and 2:57.5 read as jolts because they are digital cuts (measured), not tails (metaphor).
- **Voice**: dry, thinned phrase by phrase at the end, no tail, no sidechain.

## 4. Production-era judgement (INFERRED, medium; carried)
Modern loudness-maximised, DAW-style production over a narrow-band dual-mono chain. Figures: sample peak 0.0 dBFS with 10,317 samples at full scale; mix RMS -10.0 to -10.9 dBFS for 3:30 min (crest 10-11 dB); clipped run of 80 ms plus a -94 dB 20 ms mute; four-bar loops (waveform repeat r up to 0.85, rhythm); 8.03 kHz wall about 79 dB deep. Kick spread (IOI 20 ms std on 94.0 BPM) uninformative (low). No older, narrower layer under a full-band mix, because everything stops at the wall; no hiss or crackle floor in the fade (37 dB between bands). "Modern mastering over archive material": not shown.

## 5. Settled conclusions
- **Production: modern limited master (INFERRED, medium-high), source of the bed unknown.** Peak 0.0 dBFS, RMS about -10.5 dBFS, 3,354-sample clipped run, a -94 dB 20 ms mute, four-bar repeats; no archive-noise floor or older band-limited layer.
- **Bandwidth and image: dual-mono and a steep 8.03 kHz wall (about 79 dB down) common to every stem (measured, high); the cause is a 16 kHz-sampled stage (INFERRED, low-medium).** The delivery is close, flat and dry, not wide or airy.
- **Instrumentation: a steady mid-range sustained bed (fundamental 147.9 Hz, +12-14 cents sharp of D3, strongest 3rd partial), a gated bass centred around 75 Hz with a harmonic skirt, a falling-pitch sub kick (65 to 40 Hz) and flat 3-8 kHz hat energy, a dry close voice.** Identities not recoverable (low).
- **Mix balance: no ducking, no pumping; moves come from bass and voice entering together (+7 to +9 dB) under a fixed ceiling, so the climax is density and register, not loudness (measured, medium-high).**
- **Edges and ending: the 0:10.6 and 2:57.5 jolts are hard digital cuts; the voice ends by phrase-wise thinning at about 3:35.2 with no tail; the track ends on a bed fade and a cut at about -57 dB at 3:56.45, with no closing hit (measured, medium-high).**

## Not recoverable by measurement
- Instrument identity of bed, bass, drums: spectra show partials and bands, not sources.
- Whether the bass is a synth or a re-pitched sample: the stem is an estimate and the fundamental is weak.
- Why bed and bass sit 13-30 cents sharp: speed, tuning or tracker offset cannot be separated by a pitch figure.
- Whether the 16 kHz stage was the source or the delivery: the wall is not a date stamp.
- Whether the mutes and the equal hook levels are performance, edit, gate or limiter: the signal shows the event, not who made it.
- Whether real reverb or double-tracking exists: mono summing, limiting and separation could hide it.
- Recording date, performer, studio, intent: not in the signal.
