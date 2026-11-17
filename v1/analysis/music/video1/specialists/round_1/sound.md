# video1: SOUND specialist, round 1 (sound design and production)

Evidence keys: [lv] per_second_levels.json; [img NNNN] music_views/window_NNNNs.png; [stems] stems/stems.png and stem_rms_per_second.json; [af] audio_features/summary.json; [clap] clap_tags.json; [win] the ten window notes; [mine] v1/scripts/agents/sound_r1.py and sound_r1b.py (song.wav and demucs stems). I cannot hear; everything is inferred from measurements. British spelling; times m:ss. Sections follow [af] sections_auto, merged where they are the same sonic state.

## 0. One-paragraph verdict

A very loud, dense, heavily compressed modern-rock mix of a four-piece-style band (drums, bass, two-plus wide distorted guitar/synth layers) over archive speech. The production idea is not "a guitar band with a sample on top" but a *gated, layered* arrangement: the drums never stop, while bass, the "other" wall, the speech and the stereo width are switched on and off as the main dynamics, because the overall level barely moves (mean -11.1 dBFS, 5th to 95th percentile -16.1 to -10.6 [lv; mine]). The signature sound-design moment is a near-pure sub-bass sine at about 43 Hz that punches in every 6 s from 2:01 to 2:33. Confidence in the broad picture: high. Confidence in the specific instrument identities: low to medium (stems separation is a proxy; see section 9).

## 1. Loudness and dynamics (high confidence)

- Whole-track RMS -11.1 dBFS, sample peak 0 dBFS, with only 1 sample at or above 0.999 and 2 above 0.98 of 16.6 million [mine]. So it is peak-limited right to full scale but *not* audibly clipped sample by sample; this is brickwall-limiter behaviour (mastered to the ceiling), not digital clipping. (The file may also be a re-encoded video track; see section 9.)
- Crest factor (peak minus RMS) by section [mine]: 13.1 dB for 0:00-0:15, 11.0 for 0:15-1:06, 9.6 for 1:06-1:16, 9.7 to 10.1 for the dense blocks (1:28-1:49, 2:39-3:09), but 13.6 to 14.1 for the sparse blocks (1:16-1:28, 1:59-2:14). Low crest = squashed; the thin sections are *more* dynamic and the full ones are limited harder. This is typical of a master limited on the full band.
- 400 ms short-term level spread (P10 to P90) is only about 2 to 3 dB in the dense sections (e.g. -13.5/-10.6 at 1:28-1:49; -12.5/-10.5 at 2:39-3:09) and about 6 dB in the 2:00 block (-18.1/-12.1) because of the bass hits [mine]. Loudness range is therefore tiny. The structure is carried by timbre, density and width, not level.
- Contrast levels [lv]: the loudest sustained stretches are 1:06-1:16 (-9.8 RMS), 1:28-1:49 (-10.3), 1:49-1:59 and 2:39-3:09 (-9.9). Quiet states: 0:00-0:15 (-13.5), 1:16-1:28 (-13.9, bass absent), 1:59-2:14 (-14.5 to -16, the thinned "bass drop" passage). Loudest second by [af] is 1:52 (112 s), consistent with the 109-119 section at -9.9.
- Level drops of about 4 to 5 dB at 1:15 and 1:58 are both bass-stem removals, not fader dips: the bass stem goes to -66 dBFS (true silence in the separation, so the part was really absent, not merely masked) [lv; mine]. Bass gate, from [lv] with threshold -35 dB: on 0:08-0:12, 0:14-1:15, 1:40-1:55; then isolated hits at 2:01, 2:07, 2:13, 2:19-2:21, 2:25-2:27, 2:31-2:33; on again 2:38-3:07. Drums never drop below -40 dB at any second [lv].
- Ending: RMS about -10 to -13 until 3:07.7, then -16/-19 at 3:08.0-3:08.2 and -40 to -66 by 3:08.4 (win_0180 own measurement; I checked the stems view [stems] where all stems fall together at 3:08-3:09). A cut or a very short decay, not a fade. A 0.4 s dip to about -22 dB at 2:48 is a deliberate stop-time hit (win_0160).

## 2. Frequency balance (high confidence on numbers)

Share of mix energy by band, mono sum [mine]:

| Section | 20-60 Hz | 60-250 | 250-1k | 1-4k | 4-8k | >8k |
|---|---|---|---|---|---|---|
| 0:00-0:15 | 8.1% | 68.9 | 13.6 | 7.5 | 1.7 | 0.2 |
| 0:15-1:06 | 8.0 | 58.7 | 21.2 | 10.3 | 1.4 | 0.3 |
| 1:06-1:16 | 6.2 | 52.9 | 23.3 | 13.6 | 3.1 | 0.8 |
| 1:16-1:28 (no bass) | 9.9 | 47.2 | 25.1 | 14.1 | 2.6 | 1.0 |
| 1:28-1:49 | 6.0 | 50.0 | 29.4 | 13.0 | 1.1 | 0.4 |
| 1:49-1:59 | 6.5 | 73.4 | 15.8 | 3.5 | 0.6 | 0.2 |
| 1:59-2:14 | **38.1** | 41.6 | 9.7 | 7.5 | 2.0 | 0.9 |
| 2:14-2:39 | 14.8 | 30.8 | 31.3 | 19.9 | 2.4 | 0.9 |
| 2:39-3:09 | 6.3 | 66.1 | 14.5 | 9.5 | 3.0 | 0.6 |

- Low-end heavy: roughly 55 to 75% of energy under 250 Hz in the dense blocks, as is normal for rock energy statistics but note that this includes kick, bass guitar/synth and guitar low-mids. Treat as "bass-heavy balance" not as "boomy".
- The 2:00 block is the exception: 38% of energy sits at 20-60 Hz, entirely because of the 43 Hz sub hits (section 4). The 2:14-2:39 block has the most 250 Hz to 4 kHz (51%): the guitars/speech-forward, least bass-dominated part.
- Top end: energy above 8 kHz is under 1% in every section, and the long-term spectrum falls from +39 dB (50 Hz) to +6 dB at 8 kHz to about -5 dB at 15 kHz, and drops off a cliff at about 20 kHz (-52 dB at 20 kHz vs -12 dB at 19 kHz) [mine]. A 19-20 kHz lowpass is a codec/encoding signature (typical of lossy audio in a video file), not a creative filter. [img] spectrograms show "energy to 8 kHz+" which agrees; the window notes that say "bright" mean "full, noisy mid-high", not extended air.
- Spectral centroid of the mix [af]: about 1.5 to 1.9 kHz in the quiet openings, 2.6 to 2.8 kHz in 1:06-1:14 and at 3:00-3:08. The brighter peaks are where hi-hat/cymbal and the guitar fizz rise and the bass is absent or low in the mix (win_0060, win_0180). Drum-stem energy above 6 kHz as a share of drum energy is highest at 1:06-1:16 (-10.8 dB) versus -14 to -16 dB elsewhere [mine]: that is the cymbal/hat wash that makes the 1:06 build feel suddenly airy.

## 3. Instrumentation, with evidence (medium to low confidence on identity)

1. **Drums, acoustic or acoustic-sampled rock kit, always present** (high). Drum stem is continuous from 0:00 to the end, no second below -40 dB [lv]. [img] drums panels show vertical transients and a low band; median -20 dB decay time of drum hits is only 110 ms (P10 84, P90 142 ms) [mine]: very tight, damped, gated or close-miked, not a big roomy kit. Drum-stem band energy: 95% below 4.9 kHz, 99% below 10 kHz, so cymbal content exists but is not dominant [mine]. About 4 onsets per beat at 78 bpm [rhythm/windows]: driving sixteenth-note energy; this is the rhythm specialist's territory.
2. **Bass: two different bass sounds** (medium).
   a. A *playing* bass (0:14-1:15, 1:40-1:55, 2:38-3:07). Its stem is 95% below 151 Hz and 99% below 226 Hz [mine], i.e. a clean low fundamental with very little overtone content that separation can find; level -19 to -20 dB mean when active [lv]. The narrow band means either a clean DI/sub-heavy bass or a low synth; distortion on the bass cannot be established. The spectrogram [img 0120] bass panel shows only thin harmonic upper content at the note onsets.
   b. A **sub-bass sine "boom"** at 2:01, 2:07, 2:13, 2:19, 2:25, 2:31 (about every 6 s, a bar of 8 beats at 78 bpm = 6.1 s; that is the bass entering at the downbeat of a 2-bar phrase). [mine] I measured the stem's spectral peak at 42.6, 42.7, 42.7 and 42.9 Hz for the first four, with the second harmonic 39 to 50 dB below the fundamental: effectively a pure sine, about F1 (43.65 Hz) or a little flat, nearer 42.7 Hz (about F1 minus 40 cents; or the project's chroma reads it as E, [img 0120] chroma panel, depending on tuning). It decays only about 6 to 10 dB over 1.3 to 1.7 s. A near-pure, long-sustaining 43 Hz tone is a **synthesised sub (808/sub-oscillator style)**, not a bass guitar. High confidence it is sine-like; high confidence it is not a plucked string; medium that it is intentionally an electronic layer. Level: the stem hits about -14 dB, higher than the playing bass at -20 dB [lv].
3. **The "other" wall: distorted guitars plus possible synth/keys** (medium on guitar; low on anything else). Stem is wide (L/R correlation 0.22, side-to-mid -2.0 dB, the widest stem by far; vocals 0.76, drums 0.87, bass 0.92) [mine], 95% of energy below 2.6 kHz, centroid 1.7 kHz. [img] "other" panels show dense, noise-like partial stacks from 100 Hz to 8 kHz with no clear gaps, the visual signature of high-gain distortion. CLAP scores "distorted guitar" near 0.94 to 1.0 almost everywhere [clap] and context.md describes this track as guitar-riff rock; both are consistent but CLAP is weak evidence and I did not hear it. There are changes of *layer*: the extra layer at 2:13-2:14 is lower and fatter (centroid falls from about 2.3 kHz to 1.9 kHz, win_0120); at 1:15-1:20 discrete parallel harmonic lines at 1 to 2 kHz look more like sustained synth/organ or a clean sustained tone than distorted guitar (win_0060 [img 0060]). Whether guitars are doubled, quad-tracked or are a guitar plus synth cannot be determined from stems.
4. **Archive speech, not a performed vocal** (high). The "vocals" stem is 65 of 188 seconds above -40 dB [lv]. Band content [mine]: strong 150 Hz to 3 kHz, falling 25 dB by 5-8 kHz and 47 dB by 8-16 kHz, i.e. band-limited to about 5 kHz (95% below 4.2 kHz). That matches the sound of mid-20th-century film-optical or archive tape speech and the context.md identification of Fries Film Archief voice-over. Median level when present: about -23 dB vs -18 to -20 dB for the instruments [lv; mine], so the speech sits *under* the band: it is a texture riding in the mix, not featured. The singing/vocal-melody question (pyin "lead") is for the voice specialist.

Not established: guitar versus synth split in the "other" stem, whether there are keyboards/organ, bass identity at the playing sections, exact drum kit sound. These need ears.

## 4. Distortion and saturation (medium)

- No direct distortion measurement exists. Indirect evidence: "other" is noise-like and dense up to 8 kHz in every window image; 95% of its energy is below 2.6 kHz (typical of high-gain guitar through a speaker cabinet, which rolls off above about 5 kHz); the mix has a steep rolloff of +6 dB at 8 kHz vs +20 dB at 1 kHz [mine]. Probability that the "other" content includes heavy overdrive: high (about 85%).
- CLAP "vinyl crackle", "wind", "engine" and "bells" scores [clap] were repeatedly flagged by the window notes as probable misreadings of broadband distortion noise. I agree and do not use them; there is no measurement showing an archival noise bed (no steady hiss under the speech gaps in the vocals stem, which sits near -66 dBFS when silent [lv]).
- The drums are not obviously distorted; the bass sub is a clean sine (harmonic distortion at -39 to -50 dB). So the grit comes from the guitar layer, while the low end is clean and powerful.

## 5. Space, reverb, depth (medium; mostly "dry")

- Drum decay of 110 ms median to -20 dB [mine] and crisp vertical lines with dark gaps in every window image mean there is no long reverb on the kit. The stop at 2:48 and the end at 3:08 both fall to silence within about 0.3 s [lv; win_0160; win_0180], again a dry, gated production. Every window note that looked for tails found none.
- The speech is close and band-limited rather than roomy (vocal stem silent at -66 dBFS between phrases [lv], so no reverb tail was kept or separated). Depth is made by *level*, not by wetness: the speech is about 4 dB under the instruments.
- Caution: sustained notes in the other stem could be delay or sustain; separation cannot distinguish. Low confidence on any ambient/delay layer.

## 6. Stereo image (high on numbers, medium on causes)

[lv] width (project definition: side-to-mid ratio, higher = wider). Mean width by section [mine from lv]: 0:00-0:15 0.32; 0:15-1:06 0.45; 1:06-1:16 0.63; 1:16-1:28 0.46; 1:28-1:49 0.67; 1:49-1:59 0.57; 1:59-2:14 0.29; 2:14-2:39 0.51; 2:39-3:09 0.65.
- Wideness tracks the *"other" level*: correlation of width with other-stem dB is +0.61; with bass dB it is 0.01; with the voice dB it is -0.29 [mine from lv]. Interpretation: the width is the guitar/synth layer, panned left and right (doubled guitars hard panned is the classic rock method: L/R correlation of that stem is only 0.22), while kick, bass, snare, speech are centred (all stems other than "other" have correlation 0.76 to 0.92).
- Whole-mix L/R correlation by section [mine]: 0.82 in 0:00-0:15 and 0.84 in 2:00-2:14 (near-mono feel), falling to 0.39 to 0.42 in 1:06-1:16, 1:28-1:49, 2:39-3:09 (wide). The widest points are 3:00-3:07 (0.70 to 0.86) [lv].
- So the stereo field is itself a dynamic: *narrow and centred for the thin passages, wide and wrapping for the climaxes*. The 2:00 block is the narrowest of the track (0.24 to 0.28 at 1:58-2:00, 0.20 to 0.37 at 2:00-2:13 [lv; win_0120]) because the wall is thin and the only big events are the centred 43 Hz sine and kick.
- The width collapse at 1:40 when bass re-enters (win_0080) is a measurement artefact of the definition plus real centred bass energy.
- No evidence of phasey or out-of-phase content; mono compatibility of the mix is likely fine because correlation never goes negative at section level (lowest 0.39).

## 7. Mix balance (medium)

Median stem level when active [lv; mine]: other -18.8 dB, drums -18.4 dB, bass -20.5 dB, speech -23.4 dB. So guitars and drums are about level, bass 2 dB lower, speech 4 to 5 dB below the band. The drum stem is the most *continuous* element; the other stem is the most *tonally dominant*. In the stem-loudness plot [stems], the drums (orange) and other (red) are mutually high for most of the song, while bass (green) and speech (blue) are the two intermittent layers. That is the structural bones of the production: **drums + wall as a permanent bed; bass and speech as events.**

## 8. Era and style of production (medium; low on date)

- Heavily limited, bass-forward, guitar-wall rock with a gated sub-sine, sample-based archival speech and little reverb: contemporary alternative/post-rock production of the 2010s, consistent with the documented 2013 release (context.md; research part_mapping). The 43 Hz sine and the "stem on/off" arrangement are also the language of electronic and hip-hop-influenced production, which fits a band that mixes electronics with guitar riffs. I know the artist's wider style from research notes rather than from these measurements; the measurements alone only say "modern, loud, guitar-led, electronic sub".
- The speech reads as a vintage source treated as sample/texture (band-limited, dry, below the band). The contrast of narrow-band 1963 voice against the full-band modern wall is a production device in itself: the speech is audibly "from another time" simply because of its bandwidth.
- Sources of uncertainty on era: a loudness-war-style master was and is a feature of more than one decade; the 20 kHz cutoff is of the file, not the era.

## 9. What these measurements cannot tell (honest list)

- Instrument identity (guitar vs synth vs keys; bass guitar vs synth bass on the playing bass), tone settings (amp type, pedals), real vs programmed drums.
- Whether anything is "reverb" rather than sustain. Whether there is tape saturation or bus compression (only crest factor and level spread suggest it).
- Source-separation (htdemucs) leakage: transient hats can appear in "other" and vice versa; levels per stem are indicative, not exact. A stem at -66 dBFS means the separator found nothing, which I treat as true absence for the bass because the gating is regular and tied to musical grid.
- Video-file encoding: the 20 kHz lowpass and the loudness could differ from the commercial master.
- Loudness in LUFS (K-weighted) was not computed (pyloudnorm not installed); numbers here are plain RMS and sample peak dBFS.

## 10. Section-by-section sonic map (confidence high unless marked)

| Time | Sonic state |
|---|---|
| 0:00-0:01 | Cold start: one drum-only burst (-20 dB drums, others near -60 to -67) then full level by 0:01 [lv]. |
| 0:01-0:14 | Drums plus guitar "other" at -13.5 RMS, mid-width 0.32, bass mostly absent except a brief 0:08-0:12. |
| 0:14-1:06 | Bass in, speech enters 0:19-0:31 (then 0:41, 0:50, 0:54), mix -11 RMS, width 0.45. Heavy and steady. |
| 1:06-1:16 | The "build": wider (0.63), brighter (centroid 2.6 to 2.8 kHz), loudest sustained (-9.8), crest 9.6 dB. |
| 1:15-1:28 | Bass cut (stem -66). Level -14, a sparse, tonal organ/synth-like texture; speech 1:18-1:26. |
| 1:28-1:49 | Wide, loud wall (width 0.67 to 0.84) without bass until 1:40, then bass returns and width narrows (centred bass). |
| 1:49-1:59 | Bass partly present, dense, loud; drop at 1:58. |
| 1:59-2:14 | Thin, narrow (0.29), near-mono; 43 Hz sine hits every 6 s dominate the spectrum (38% of energy under 60 Hz). Speech at 2:15. |
| 2:14-2:39 | Extra low-mid layer enters 2:13-2:14; guitars/speech forward; sub hits continue to 2:33; widest mid-range share. |
| 2:39-3:08 | Bass back for good, widest and brightest finale (width 0.7 to 0.86 at 3:00-3:07), stop-time hit at 2:48, abrupt cut at 3:08. |

## 11. Disagreements with / additions to the window notes

- win_0000 says the bass is largely absent at the start; confirmed (bass mean -41 dB for 0:00-0:15, on only 0:08-0:12 [lv]).
- Several window notes (0100, 0140, 0180) call the mix "bright"; my measurement says <1% of energy above 8 kHz and the centroid 2 to 3 kHz, so it is "full and gritty in the upper mids", not airy. Only 1:06-1:16 and 3:00-3:08 are noticeably brighter.
- win_0120 attributes the 2:00 "pumping" to bass drops and treats the lows as bass; I add that they are a single 42.7 Hz sine (not a bass-guitar note), which strongly shapes the feel and is an electronic production choice.
- win_0080/0100 interpret width collapse at the bass return as centred bass; my cross-correlation (width vs bass dB = 0.01 across the whole track) says the bass is not the main driver globally; the wide "other" layer is.
- The CLAP sound labels (wind, engine, vinyl crackle, bells) are not corroborated by any measurement, and I recommend dropping them from the synthesis.

## 12. Questions for fellow specialists

1. **To harmony:** the sub-sine at 42.7 Hz (stem measurement, not a bass-guitar note) is roughly F1, about 40 cents flat of equal temperament, while chroma and chord labels call the passage D/E. Is the sub a root (D would be 36.7 Hz or 73.4 Hz) or does it sit on the 7th/9th against the D pedal? What does a 43 Hz tone *do* harmonically against D and Dm in 2:00-2:35: is it tonal at all, or only a felt impact?
2. **To rhythm:** the bass gate repeats every 6 s from 2:01 (2:01, 2:07, 2:13, 2:19, 2:25, 2:31), while the drums continue unbroken. Does the 6.1 s spacing line up with an exact 8-beat bar at 78 bpm, or with 4 bars at a doubled tempo? Is the sub hit on the downbeat of the phrase, and what happens in the drums on that beat (fill, crash, kick) that could make it feel like a "drop"?
3. **To feeling:** the production gives almost no dynamic range (loudness P10 to P90 about 2 to 3 dB), yet your windows report strong build and release. Which of those shifts do you think a human actually feels as such: the width opening (0.29 to 0.65), the bass gating, or the band-limited speech entering? And does the dry, tightly gated sound (110 ms drum decay, 0.3 s cut-off ending) read as "controlled/mechanical" or "urgent" to you?
