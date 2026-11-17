# t_birdwalk: SOUND specialist, round 3 (blind, final, measurements only)

Keys: S3 = my round-2 script sound_r2.py; S4 = new script v1/scripts/agents/sound_r3.py (side-channel coupling between the vocals and "other" stems; harmonic ladder, onset rate and 15 dB decay of the "other" stab in four spans). Other files cited as R2/F2/H2/H3/V2/L2/FE2 (round 2, and Harmony round 3). I did not read context.md, research or non-blind files. I cannot hear; "consistent with" is my strongest claim.

## 1. Answers to questions put to me

**VOICE (Q1): is the hook's stereo width (vocals-stem correlation 0.52-0.56) leakage from the "other" stem or a doubled/processed voice?** S4 compared the side channel (L minus R) of the two stems in 50 ms frames.
- Log-envelope correlation of vocal-side against other-side: 0.02 (0:30-0:58), -0.25 (2:15-2:23), -0.09 (2:32-2:38), -0.34 (2:45-2:50), 0.08 (1:35-2:00); sample-level correlation 0.04-0.13 throughout. If the stabs were leaking into the vocal side, the vocal side would pulse with the stab side. It does not (it is zero or negative).
- Vocal-side against vocal-mid envelope: 0.64, 0.58 and 0.97 in the three hook spans, but about 0 in the 0:14-0:40 verse. In the hooks the side signal rises and falls with the voice itself.
- Reading: the width belongs to the hook voice (a doubled, stereo-widened or double-tracked take, or a stereo-recorded sample), not to leakage from the stab layer. Side-to-mid is 0.50-0.55 in hooks and 0.16-0.29 in verses. The side spectra of vocals and "other" are similar in shape (0.71-0.86), but that is the generic shape of broad mid-range content, so I do not lean on it. **Medium** (up from my round-2 "low"). Cannot tell: a stereo reverb or chorus versus a true double; the earlier note of zero inter-channel delay (V2) fits a pan/width effect or a copy rather than a second performance.

**HARMONY (Q1): is the A5 stab (0:40-0:47) the same sound as the A3 stab (1:02-1:20, 2:00-2:10, 2:45-2:50)?** S4 on the mono "other" stem:
- 0:40-0:47: peak 883 Hz; harmonics fall away steadily (2nd -12, 3rd -19, 4th -23 dB). Onset rate 4.0 per second, median 15 dB decay 0.12 s, centroid about 2.5 kHz. A short, bright, plucked-like tone.
- 1:02-1:20: peak 226 Hz; 2nd -11, 3rd -18, then the 4th harmonic (near 904 Hz) only -4 dB; onset rate 2.7 per second, decay 0.26 s. 2:45-2:50 is the same (4th at -4 dB, decay 0.27 s). 2:00-2:10 is similar but without the strong 4th (-16 dB).
- Reading: not one tone pitched up and down (an octave shift would carry the whole ladder with it, and the decay time would not double). The A3 passages hold a body at about 226 Hz plus a bright component at about 900 Hz, which is the same register as the A5 stab, so the 0:40 sound looks like the top of the same palette with the low body removed. So it is one family of plucked sample with a different voicing, longer decay and slower rhythm in the groove (not octave transposition). **Medium-low.** Cannot say pluck, square or vocal sample: the ladder is falling, even harmonics are present, so it is not a clean square wave; beyond that identity is out of reach.

**RHYTHM (earlier Q1, 8-bar versus half-time):** R2's 80 BPM half-time reading matches the 0.26 s stab decay and 1.0-1.4 s bass tail I measured; I accept it. **FEELING (Q on the dip before bass entries):** a dip of 5-12 dB 0.7-0.9 s before each bass entry is, in sound terms, the drums and stab going quiet while the sub is absent, so the entry arrives as a return of weight and a stereo narrowing at once (S3); I can say that is mechanically what the dip does but not whether the producer meant a "pickup".

## 2. Corrections

1. My round-2 line that the A-D-E cluster in "other" implied a "power-chord" colour is superseded by H3: per-frame pitch gives A with brief D visits and E rare (5-10 per cent D, E mostly absent). My averaged-peak method over many seconds overweighted occasional events. Withdrawn as a "chord"; the layer is A plus a D neighbour. **Medium.**
2. My statement that "other" is "more than one repeated pitch" stands only in the sense of timbre (body plus 900 Hz bright part), not pitch.
3. I called the hook-voice width "low confidence leakage or double". The side-envelope test above now favours the voice's own width.
4. The "mono bus" reading is not needed: bass and drums are mono by nature (1.00 correlation, S3), and the collapse is an energy-ratio effect (unchanged).

## 3. Connections

- **Form:** the form is a stereo-and-layer map: centre (mono sub and drums, the weight) versus side (wide bed and wide hook voice, the space). Every bass cut opens the image; every return closes it. The pasted break (0.96 similarity, F2) is the one place the wide bed and wide voice are heard with the weight removed.
- **Rhythm:** the short plucked stab (0.12-0.27 s decay) sits at 2.7-4 onsets per second, finer than the 1.5 s drum hit; the falling sub fills the half-bar. So three time-scales are carried by three timbres: sub (1 s), drum hit (1.5 s), stab/syllable (0.2-0.4 s).
- **Harmony:** the sound world is nearly harmonic-free: near-sine sub, plucked A, noise sweeps. The bare spectrum is why chord detection returns "N" so often (47.6 per cent) and why mode is undecidable.
- **Voice:** the verse voice is mono and close; the hook voice is wide. The leap in width from the verse to the hook is the strongest "one man to the crowd" signal I can measure; it is an effect of treatment, not proof of several people.
- **Feeling/Lineage:** flat loudness (-12 to -14 dBFS) with changing width and sub makes the impact bodily, not a rise in level. Falling-glide sine sub, dry mono drums, wide plucked bed and a band-limited top (about 9-10 kHz) fit mid-2000s to 2010s Southern club production (low-medium).

## 4. Settled conclusions

- **The sub-bass is a near-mono (correlation 1.00), near-sine, falling-glide tone (about 0.7 semitone, 2nd harmonic -28 dB) on A1, ringing about 1 s and gated: a synthetic 808-like sub (medium-high), and it supplies about half the energy (47 per cent below 60 Hz), so most of the track's "weight" is physical, not tonal.**
- **The sound is a centre-versus-side design: mono bass and drums (high) against a wide, decorrelated "other" bed (correlation 0.0-0.15, high) and a wide hook voice (0.52-0.56). Width changes with the bass because of an energy ratio, not a mono-ing mastering stage (high); loudness stays flat at -12 to -14 dBFS (high).**
- **The "other" layer is a short plucked A-family sample (0.12-0.27 s decay, falling harmonic ladder, 0.9 kHz bright part), A5-bright in the 0:40 build and A3-bodied in the groove, not simply transposed (medium-low); the 0:48 and 2:00 break is a pasted copy (0.96 similarity, medium-high).**
- **The hook voice's width comes from its own treatment (vocal-side tracks vocal-mid, 0.6-0.97, and does not track the stab side, about 0), not from stem leakage (medium); the verse voice is mono, dry and close.**
- **Overall: dry, close, compact, band-limited (about 9-10 kHz ceiling), bass-heavy and minimal. It is warm and boxy, with space appearing only when the sub leaves. Era mid-2000s to 2010s club/crunk-snap style (low-medium). Unknowable from these measurements: exact instrument identity, whether the width is reverb, chorus or a double, and how much of the "other" stem is demucs bleed.**
