# video2: sound specialist, round 1

Scope: sound design and production (instrumentation, timbre, distortion, space, stereo, balance, loudness, era). I cannot hear; everything is inferred from measurements. Helpers: `v1/scripts/agents/v2_sound.py`, `v2_sound2.py`, `v2_sound3.py`. Images opened: music_views window_0000s, window_0040s, window_0240s (others via the window notes and numbers). All win_*.md notes were read; sound-relevant claims checked below. Timestamps m:ss.

## 1. Headline

A **tightly programmed, modern electronic production** (machine-locked grid per the rhythm specialist) in which the sound world is **staged by bandwidth and width**: a dark, narrow-band, very wide intro (0:00-0:41) is "opened up" at about 0:42 exactly when the first narration arrives, and the track then settles into a loud, dense, centre-weighted, mastered-to-the-ceiling groove (1:28-5:04) that gets brighter and denser to the end. The sound moves from "archive/memory" to "present machine". Confidence: high on the measured facts, medium on the interpretation.

## 2. Loudness curve (per_second_levels.json; my section medians/means)

| Section | Mix mean dBFS | Notes |
|---|---|---|
| 0:00-0:28 | -25.5 | quiet pad plus a drum thud every 4 s; drums stem about -68 median |
| 0:28-1:00 | -18.3 | bass (-23) and drums (-32) enter at 0:28 |
| 1:00-1:28 | -18.2 | breaks and stops (1:24-1:27 hole) |
| 1:28-1:44 | -14.7 | drums jump to about -19 at 1:28.5 |
| 1:44-3:20 | -11.8 / -12.6 | plateau; bass raised to -14.8 at 1:44-2:30 |
| 3:20-4:30 | about -11 | |
| 3:36-4:30 | -10.5 (loudest) | "other" rises to -15 as vocals samples return |
| 4:30-4:48 | -11.4 | |
| 4:48-5:00 | -12.9 | bass gated to stabs (-45 median) |
| 5:00-5:04 | to -88 by 5:04, digital zero (-180 dB) from 5:04.3 | |

- Whole-file mean RMS about -12.9 dBFS; 3 s short-term RMS percentiles 10/50/90 = -20.1 / -12.4 / -10.4. Sample peak reaches 1.0 and 675 samples (0.0025 %) exceed 0.99: limiter-ceiling mastering, but no audible-grade clipping evidence in this count. Crest factor of the mix drops from about 17 dB (intro) to 10.4-12.3 dB (groove): from dynamic to compressed. High.
- The total rise is about 15 dB from intro to peak. Most of it arrives in three steps (0:28, 1:28.5, 3:36), not gradually. High.
- Drum stem is almost flat at -18 to -19 dBFS from 1:28 to 5:00 (the drums are the constant loudness anchor); the changes in mix loudness come from "other" (-25 to -15) and bass. High.

## 3. Bandwidth and timbre (spectral roll-off, HF energy; v2_sound2.py)

- **0:00-0:41: hard-band-limited.** 99 % roll-off is only 1.2-1.5 kHz; energy above 4 kHz is about -67 dB relative to the total. In window_0000s the mix has a visible ceiling near 2-3 kHz with horizontal harmonic lines below. Whatever it is, it is dark, "behind glass", like a low-pass-filtered synth pad / drone with a muffled thud. HF is flat at -70 dB from 0:34 to 0:41 (noise floor), then jumps about 26 dB in one second at **0:42**. High.
- **0:42:** the full mix (including "other") brightens to a roll-off near 3 kHz at the same instant the narrator's first phrase begins (window_0040s: vocal stem energy to about 6 kHz from 0:42.5). The filter is therefore either opened by the producer in time with the voice, or the "other" layer changes. Medium on the mechanism, high on the timing.
- **Narrator timbre:** in speech windows the vocal stem's 95 % roll-off is 2.5 kHz at 1:05-1:20, 3.8 kHz at 3:45-4:00, 4.1 kHz at 4:10-4:25; centroid rises from 706 Hz to 1570 Hz. So later narration is brighter than earlier, or is a different excerpt/recording. The harmonic-formant striping in window_0040s (vowel formants, aspirated bursts) says real speech, not a vocoder. Spectral width up to 4-5 kHz fits an old optical/magnetic film soundtrack or telephone-like mastering more than a modern studio voice, but I cannot prove the era from this. Low-medium.
- **Groove-section brightness:** mix roll-off climbs from about 3 kHz (0:42-1:20) to 3.8-4.4 kHz (2:20-4:30) to 5.6-5.7 kHz (4:40-5:00); >4 kHz share rises from -26 dB to -20 dB and then -17 dB. Spectral centroid rises 2136 Hz (1:40-2:20) to 2893 Hz (4:30-4:58). The track gets brighter and brighter. High.
- **"Other" stem** (guitar/synth layer): centroid 570 Hz at the start, about 700-760 Hz at 1:00-2:00, dips to about 450-470 Hz at 2:40-3:20 (darker, possibly a held pad/chord layer), then surges to 830, 1000 and 1080 Hz at 3:40-5:00, with >2 kHz share rising from -37 dB to -8.6 dB. That is a timbral transformation: a low pad becomes an upfront, bright, hi-hat-adjacent sparkle layer; at 4:40-5:00 it falls back to 412 Hz centroid with the stab section. High on the numbers; instrument identity unknown (see section 7).

## 4. Instrumentation (evidence, not names)

- **Drums**: stem shows sharp broadband vertical lines in every groove section (window_0240s), kick energy below 150 Hz plus noise-like hi-hat/snare content to over 8 kHz in 3:40-4:40; hit-to-hit regularity per the rhythm specialist (constant phase over 200 s) says sequenced or sampled, not human. The sparse intro thud (window_0000s) is a low, decaying "boom" below 500 Hz with a narrow lower tail, like a kick or timpani with long decay. The ending's last hit has a long, wide, low decay. High that drums are programmed or sample-based; low on kit type.
- **Bass**: stem sits below about 300 Hz in most windows (window_0240s: nearly all energy under 512 Hz with a bright line at the bottom). Dotted-quaver ostinato per the rhythm specialist. Sub-40 Hz energy is -39.5 dBFS in the intro and -27.9 dBFS in the groove. Demucs "bass" level is -14.8 dB median at 1:44-2:30 and drops to -18 elsewhere; in 4:48-5:00 it is gated to stabs. Likely a synth or sampled bass; a sine-like sub plus a harmonic is consistent with the narrow stem spectrum, but not proved. Low-medium.
- **"Other"**: sustained harmonic lines (window_0000s, parallel horizontal harmonic partials up to about 2.5 kHz) = pad-like or sustained electric guitar/synth; later (window_0240s) busy broadband with fine vertical texture = plucked or arpeggiated sixteenth layer plus hats leaking from the drum separation. Context.md says: verify instruments from stems, do not assume banjo; I find nothing in the spectra that supports a banjo, and nothing that excludes a clean electric guitar. Low.
- **Narrator**: speech sample, see section 3. Lead pitch contour (window_0240s lead track) shows short, disconnected "notes" at 65-81 MIDI: those are speech intonation fragments, not a singer.
- **CLAP (weak evidence)**: synth-pop/electronic and drum machine tags agree with the above; I give them no more than a tie-break weight.

## 5. Space and reverb

- Intro and sparse sections: windows show smooth, slowly decaying tails after each thud (window_0000s: drum energy decays over 2-4 s below 500 Hz), i.e. a long, dark, low-frequency ring. Measurable but I cannot say whether it is true reverb or a long-decay synthetic kick.
- Ending (v2_sound3.py, 0.5 s frames): groove ends about 5:00.8; at 5:02.0-5:03.0 two hits sit at about -14 dBFS with the stereo side/mid ratio at -23 to -25 dB (near mono), then a tail at 5:03.0-5:04.0 falls -51.6, -64, -88 dB, with width opening (S/M about 0 dB: wide, decorrelated ring). So the last hit is a centred strike followed by a wide, quick (about 1.5 s) tail; digital silence from 5:04.3. High on measurement; whether the tail is reverb or a plug-in is unknowable here.
- Narration seems dry in the stem (no long smears visible between words in window_0040s, vocal stem returns to the noise floor within about 1 s). So the voice is up front and not heavily reverbed. Medium.

## 6. Stereo image

- Whole-mix width (per_second_levels `width`, L/R correlation, S/M):
  - 0:05-0:25: corr -0.07, S/M +0.6 dB: very wide, slightly out-of-phase character. Width mean 1.14. This is a "hyper-wide" pad that would feel spacious and slightly unmoored on headphones; mono-sum would lose material. High on the numbers; the cause (chorus/ensemble, stereo reverb, phase-shifted layers) not separable.
  - 0:30-0:60: corr 0.26, width 0.8.
  - 1:00-1:28: width 0.74 (the voice sits in the middle, so the voice does not add width).
  - 1:28-2:30: width falls to 0.34-0.43: centred and mono-compatible (corr 0.80 at 1:40-2:20).
  - 3:40-4:20 and 4:30-5:00: corr 0.58-0.61, S/M -6 dB.
- By stem (S/M in dB, 1:40-2:20 and 3:40-4:20): drums -22.5 / -23.2 (essentially mono), bass -16.8 / -15.1 (near mono), vocals -9.9 / -1.6, other -1.3 / -3.3. So **the foundations are mono and centred; all width lives in the "other" layer (and the late vocal samples)**: a classic modern mix design. At 3:40-4:20 the narrator's stem is wider (-1.6 dB) than at 1:40-2:20 (-9.9 dB): the later samples are either stereo recordings or are given stereo processing. Medium (the separator may mix other-layer bleed into "vocals").
- Result: width narrows as loudness rises: the intro is open and ambiguous, the groove is a centred "wall". High.

## 7. Mix balance and production era

- Balance in groove (median stem dBFS at 1:44-3:20): drums -19, bass -15 to -18, other -21 to -22, voice -75 (absent). With the voice (3:36-4:30): other rises to -15, vocals -32. So voice sits about 15-17 dB below the drums and bass in stem terms. Because the stem split is not a mix fader level, treat the voice level as a clue that it is meant as a texture or hook, not a foreground lead. Medium.
- Era: the combination of a sub-heavy mono low end, near-mono drums, wide synth/guitar layer, limiter-ceiling loudness and sixteenth hats at 120 BPM is characteristic of 2010s electronic/synth-pop and indie-dance production (the release is 2013 per context.md; consistent). The archival-voice-over-band method is PSB's trademark per context.md; I cannot confirm from audio. Confidence for "2010s electronic-pop mastering practice": medium. The opening dark filtered pad is also typical of modern production and need not imply a deliberate "old-media" treatment; but its pairing with the 0:42 opening makes the narrator-driven reading attractive.
- Distortion: no evidence of heavy overdrive. The HF content above 6 kHz is smooth in the groove, and the crest factor of 10-12 dB is moderate for a loud mix. A tape-hiss-like noise floor is not measurable under the music: at 0:34-0:41 the 4 kHz+ band is -70 dB, so no hiss in the intro. The "archive grain" that context.md mentions is therefore not a broadband noise layer I can see here; any grain is in the picture, or in the voice sample band-limiting. Medium-high.

## 8. Cross-check with the window notes

- Agree: intro described as a dark, narrow pad; wide stereo; strong loudness steps at 0:28, 1:28.5 and about 3:36; ending as a hard stop with a decaying ring; digital zero after 5:04.3.
- Correction/qualification: some notes call the stem "other" "guitar/synth" without evidence. I cannot split them. Also, notes that read CLAP genre (reggae etc.) as meaningful are weak evidence.
- Not independently verified: exact chord-instrument claims in notes (harmony specialist's area) and the "bass note bursts" level claims at 4:50-5:00 (I confirmed the bass median at -45 dB for 4:48-5:00 and the stab structure matches the rhythm note).

## 9. Limits

- Demucs stems are estimates with bleed; stem widths and levels are indicative, not absolute.
- I cannot identify instruments, only bandwidth, envelope, and spectral behaviour.
- Reverb versus long-decay synthesis cannot be told apart from these summaries.
- Phase-ambiguity in the intro (corr near zero) might come from a stereo-synthesis effect, not intent.

## 10. Three questions for fellow specialists

1. **Form:** Does your section map put a boundary at 0:41-0:42 (bandwidth opening, voice entry) and at 3:36 (vocal-sample return plus "other" brightening)? If so, are these arrangement changes or just production (filter automation) changes?
2. **Voice:** Is the narration's brightness change (95 % roll-off 2.5 kHz at 1:05-1:20 vs 4.1 kHz at 4:10-4:25) consistent with different source recordings or speakers, or with different processing? Does the voice stem's speech content match archive film audio (language, noise, bandwidth) or a re-recorded narrator?
3. **Harmony (or Lineage):** Does the dark, wide, drone-like opening pad (chroma B-D-G heavy, window_0000s) plausibly serve as a sustained hold of one chord (Bm / Gm-B ambiguity in the chroma), and does that ambiguity reflect the stereo phase issues I see in the intro (corr about 0), or is it the chord detector failing on the out-of-phase signal? Also lineage: which other PSB or 2010s synth-pop records use a muffled low-pass intro that opens on a sample entry?
