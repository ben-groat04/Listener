# video1: SOUND specialist, round 3 (blind, measurements only)

Evidence keys as before: LV per_second_levels.json; MV window PNGs; ST stem RMS. New run: `v1/scripts/agents/sound_round3.py` (Welch spectra, 16384-point, and mid/side split on stems_raw/htdemucs/song/*.wav). Bin width 2.7 Hz. I read all seven round-2 files and the round-3 harmony file. Times m:ss. I cannot hear.

## 1. Questions put to me

**Harmony/Form/Lineage: is C in the "other" stem a played flat seventh or distortion intermodulation?**
Two tests.
- *Arithmetic.* Intermodulation between a D (73.4 Hz) and A (110 Hz) fifth gives sums and differences of their harmonics: D, A, E, F#, and a ladder on the D1 grid (36.7 Hz multiples). It does not give C at the lowest orders. C appears only as the 7th partial of D1 (about 257 Hz, 31 cents flat of equal-tempered C4). So heavy distortion could in principle put a flat-seventh-ish partial there, but not a strong C by the first-order products.
- *Measurement.* Peak in the 245-275 Hz region of the other stem: 261.1 Hz (-39 dB) at 1:30-1:40, 261.1 Hz (-63 dB) in the thin block 2:00-2:13, 263.8 Hz at 0:40-0:55. Those sit on equal-tempered C4 (261.6), not on the 256.9 Hz partial, though 2.7 Hz bins make this marginal. In the final plateau (2:50-3:05) the peak in that region moves to 250.3 Hz (-36 dB), i.e. smeared. Relative to the D3 peak (about 147 Hz) the C level is 2-6 dB under in dense blocks and 4 dB under in the thin block, in line with Harmony's ratio that does not fall in light blocks.
Settled: C is more likely a real or intrinsic-to-the-layer note than an intermodulation product (medium-low). I cannot exclude that a guitar-like power chord's own 7th partial supplies it, so "Mixolydian-leaning" stays at the confidence Harmony gives it, no higher.

**Feeling: is the final width carried by the "other" layer alone, or has the bass widened? (mid/side, side level relative to mid)**
- Other stem: 1:30-1:39 -0.6 dB, 1:41-1:50 -3.0, 2:19-2:37 -4.1, 2:50-3:00 -0.2. So the other layer is nearly as strong in side as in mid in both 1:30 and the finale.
- Bass stem: absent at 1:30-1:39 (mid -64 dB); side is 12 dB under mid at 1:41-1:50, 18 dB under at 2:50-3:00, 37 dB under at 2:19-2:37 (the pitched bass in the roll-call section is almost pure mono).
So the width is the other layer's, and the bass is centred and narrower still at the end. The finale is the 1:27 wall (same side/mid balance) plus a centred bass, not a new texture in the stereo sense. The width drop at 1:40 (0.3 lower in LV) is consistent with the bass landing in the centre and the other layer slipping 2.4 dB narrower (high-medium). Final width 0.73 is therefore wall-width with the bass diluting it very little. What is new at 2:48 is the drum shape and the extra top end, not the stereo field.

**Rhythm/Form: after 2:48 is the drum sound different, or only the pattern? Was the click swapped at 0:32?**
Drum stem, 2-12 kHz centroid and level (low band below 150 Hz in brackets): 0:05-0:30 5.5 kHz, -36.7 dB (-21.7); 0:34-1:00 6.2 kHz, -35.3 (-24.7); 1:40-1:55 6.2 kHz, -37.0 (-23.8); 2:05-2:20 6.4 kHz, -35.5 (-23.8); 2:30-2:47 6.3 kHz, -35.3 (-22.8); 2:50-3:06 6.3 kHz, -30.3 (-26.0). So:
- At 0:32 the high-band click keeps the same level and shape (-36.7 to -35.3 dB, centroid within 0.7 kHz); the low band drops about 3 dB. Rhythm's whole-stem centroid doubling (1.6 to 3.3 kHz) therefore comes mostly from the thumps thinning, with the click unchanged. Not a swap (medium).
- At 2:48 the 2-12 kHz level rises 5 dB and the low band falls 3 dB: same spectral shape of the click, more of it, with fewer thumps. That is a re-balance (a new pattern at slightly different gain, or the open-hat and cymbal wash of the wall leaking into the drum stem), not a new drum sound (medium; stem leakage cannot be ruled out).

**Voice: is the closing line's narrowness a low-pass or separator loss?**
Vocal stem, 5-8 kHz power: 0:20-0:26 -44.0 dB, 2:15-2:21 -47.0, 2:44-2:47.5 -52.4 (8 dB narrower than the first line). The "other" stem in the closing line is low (500 Hz to 2 kHz -40, 2-5 kHz -44 dB, 12 to 24 dB below its level at 0:20-0:26), so there is little wall to mask the voice's upper band and cause separator loss. That points to the source (take or recording) being slightly narrower at 2:44, not processing or masking (medium-low). No moving EQ is visible; the difference is 8 dB in a band that is already 15 dB down.

**Voice: 2:15-2:21 level.** Vocal stem is 11-12 dB lower in 100 Hz to 2 kHz than at 0:20 (-42/-41 against -31/-29) but only 3 dB lower at 2-5 kHz, with the other stem 3-5 dB louder at the same time. That is a quieter, thinner-sounding recording, consistent with a different take or a different source; the 2:44 line returns to full level (-32/-30), so it matches the first. It is the middle block that differs (medium).

## 2. Corrections
- Mine, round 2: "width is a function of the other layer's tightness" is now sharper: side-to-mid ratio of the other stem is the same (about 0 dB) at 1:30 and 2:50, yet LV width differs only by bass dilution. The bass is the only layer that is reliably central (high).
- Mine, round 2: I called the 2:48 rise "drum centroid 4.7 kHz after the cut". It is better stated as a 5 dB rise in the 2-12 kHz band of the drum stem with an unchanged centroid in that band.
- Harmony: I accept your replacement of "Dm at the sub hits" and the E/G alternation at 2:13. My 2:13 "body on" (+11 dB at 100-500 Hz) is the audible face of that alternation: the added body is the E and G tones appearing under the D/A drone, not louder D.
- Harmony: 1:27-1:40 Am/C/Dm labels: confirmed as untrustworthy; the other layer returns with the same notes but 26 dB more in the 2-5 kHz band.
- Feeling: nothing in my measurements supports "lo-fi/worn" texture. The mix is dry, clean and bright to 18 kHz; the worn quality is in the voice sample only.

## 3. Connections
- **To rhythm and form:** drum click unchanged at 0:32, thumps thinned, so the drum stem does not mark the 0:32 section edge by timbre; the edge is carried by the voice leaving and the bass bite. At 2:48 the drum stem does change, so 2:48 is the only edge where drums, other and width all move together.
- **To harmony:** the pitched events (A/C at 1:15, E/G at 2:13) are quiet, thin-layer events; the dense wall hides pitch change under distortion. So the form's loud peaks are harmonically still and its harmonic movement lives in the thin passages.
- **To voice:** the voice has a quiet, narrow centred lane and the wall is wide; where the wall opens, the voice has gone. The one exception is 2:44-2:47, where the wall is momentarily thin (-40 dB in the mids) and the closing line is exposed.
- **To feeling:** weight comes from a centred bass and sub; vastness from a wide, side-equal other layer. Both are present at the end, which is why it reads as arrival by weight, not by volume.

## 4. Settled conclusions
- **Production:** dry, loud, clean-bright to 18 kHz, 77 % of power below 500 Hz, no reverb tail; the only old-sounding item is the narrow voice sample (high on dryness and band; medium on era: any time since the late 1990s).
- **Layers:** a fixed 42.66 Hz near-sine sub (gated, 6.1 s cycle, locked to the 8-beat grid), a centred pitched bass, a grid-locked drum stream (every-beat click, low thumps between), and a wide "other" wall that is guitar-amp-like or synth-like, identity unprovable (low).
- **Stereo:** the other stem is as strong in side as in mid at 1:30 and at 2:50; bass is centred (12 to 37 dB side under mid); the finale's width is the 1:27 wall plus a centred bass, not a new texture.
- **Section edges are spectral:** 1:15 bass and top off; 1:27 top end back (+26 dB at 2-5 kHz, same notes); 1:40 bass in; 2:13 low body in (+11 dB, the E/G alternation); 2:48 cut then brighter, thumpless drum stream. Loudness barely moves (-9.5 to -16.5 dBFS).
- **C and the "Mixolydian" colour:** C is probably a played or layer-intrinsic flat seventh rather than intermodulation (medium-low), the sub at 42.66 Hz is a felt weight tone and not a chord note (medium), and the voice sample's three blocks are one style with 2:15-2:21 a thinner take (medium).
