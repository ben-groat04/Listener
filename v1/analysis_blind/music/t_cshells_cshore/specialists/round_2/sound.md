# SOUND specialist, round 2 (blind, measurement-only): t_cshells_cshore

I read all six round-1 files and rhythm's round-2 file. New measurements: `v1/scripts/agents/sound_r2.py` (plus one inline 5:12 tone check, same stems). Tags carried from my round 1 unless stated. Timestamps m:ss. Welch/FFT on audio/song.wav and stems_raw/htdemucs/song/*.wav.

## 1. Answers to questions put to me

**Harmony Q1: is the final pad (5:20-5:42.8) an oscillator/organ-like tone or a processed sample, and does the flat tuning fit an old-source layer?**
- Measured on the "other" stem, zero-padded FFT of 8 s spans:
  - 5:22-5:30: partials at 218.6, 438.7, 659.0, 879.1 Hz (fundamental about 11 cents flat of 220), but the 3rd and 4th partials are the strongest (-7 and 0 dB re the peak) and the fundamental is 30 dB down.
  - 5:30-5:38: 217.0, 437.3, 657.7, 876.5 Hz; now the 2nd partial is the strongest and the fundamental is -20 dB.
- Correction to the "10-25 cents flat" figure I carried: that depends on which partial is read. From the fundamentals it is -11 then -24 cents. From the partial ratios (f4/4, f3/3) it is -3 to -7 cents (219.8, 219.7 Hz) and -7 to -10 cents (219.1, 219.2 Hz). Partials are in near-exact harmonic ratio (within 0.3 percent), so this is a harmonic tone, not noise. The pitch also moves about 1.5 Hz (about 12 cents) between the two spans while it fades. Measured, medium: flat by roughly 3 to 24 cents, and drifting.
- Evidence for "oscillator/organ-like versus sample": the exact harmonic ratios and the changing partial balance over 16 s (the spectrum's weight moves from partials 3-4 to partial 2) say a sustained harmonic source whose timbre evolves (a filter, a bow-like or reed-like swell, or a playing change). A looped sample would repeat its balance. I cannot choose between organ, synth, bowed or reed-like instrument. INFERRED, low-medium.
- Amplitude modulation: my envelope-detrend figures (peak modulation 0.33 and 0.50 Hz, depth 0.8-1.0) are contaminated by the 40 dB fade, so I withdraw them as a vibrato claim; no vibrato rate is established. The 0.5-1 Hz "ripple" at 3:44-4:00 from round 1 stays "visual only, low".
- Does flat tuning fit a tape/old-source layer? A fixed offset of 3-24 cents that wanders by 12 cents is as consistent with a played, hand-tuned or detuned-by-design instrument as with a tape source, and no band-limited or noisy layer accompanies it (section 5 below). I do not raise my round-1 "mild evidence" above low. Not a dating cue.

**Form Q (3:44-3:59 "bass out, band near 1 kHz up": real timbre change or Demucs moving low synth from bass to other?).** Real, and I checked it by the mix, not the stems. Welch dB on the mix, 3:30-3:43 against 3:47-4:00:
| band | before | after | change |
|---|---|---|---|
| 30-150 Hz | -26.8 | -30.6 | -3.8 dB |
| 150-1000 Hz | -23.3 | -22.3 | +1.0 dB |
| 1-4 kHz | -27.3 | -20.9 | +6.4 dB |
The "other" stem's 30-150 Hz band does not take over the bass (-29.4 to -33.0 dB, it also falls 3.6 dB), and the bass stem's own low band falls 17.5 dB (-38.2 to -55.7). So the low end really thins and the 1-4 kHz region really brightens in the mix itself: a real change of timbre balance (thinner floor, brighter body), not a separator transfer. Measured, medium-high. One caveat: the bass stem's low band was already 9 dB under "other"'s low band before 3:44 in this span, so the bass was not the dominant low-frequency source there; the thinning is by about 4 dB, not a collapse. That fits my round-1 observation that the mix level hardly moves (rises 4 dB) when the bass leaves.

**Lineage Q3 / Voice Q1: are the voice-like fragments band-limited, noisy, broadcast-like (archive) or full-band (studio)? Is there a telephone band-pass or dedicated reverb at 2:22 and 5:30-5:42?** I measured the four events, mix and vocals stem, in five bands (0-200 / 200-1k / 1-4k / 4-8k / 8-17k Hz, percent of power):
| event | vocals stem | mix in event | mix 6 s before |
|---|---|---|---|
| 2:21.5-2:26 | 0.2 / **99.7** / 0.2 / 0 / 0 ; 85% roll-off 334 Hz, 95% 845 Hz | 29 / 58 / 8 / 2.6 / 2.2 | 50 / 32 / 12 / 3.3 / 2.2 |
| 4:28.5-4:31 | 15 / 48 / 23 / 11 / 3 ; 85% 3.9 kHz | 22 / 51 / 21 / 4.4 / 1.6 | 26 / 46 / 22 / 4.6 / 1.7 |
| 5:12.0-5:13.2 | 100% in 1-4 kHz, 85-95% roll-off 1.5 kHz | 32 / 24 / 41 / 3.3 / 0.2 | 39 / 35 / 20 / 4.6 / 1.9 |
| 5:30.5-5:42.5 | 2 / 28 / 68 / 2 / 0.3 ; 85% 2.5 kHz, 95% 3.5 kHz | 1 / 91 / 8 / 0.1 / 0 | 2 / 64 / 32 / 2 / 0 |
Findings:
- 2:22: the stem energy is a low-mid murmur, 99.7% between 200 and 1000 Hz (peak -22 dB on the 50 ms envelope at 2:23.0). It is narrow-band, but the mix confirms a real event (200-1000 Hz share rises from 32% to 58%). Medium confidence that something low-mid-voiced is present; a telephone band-pass cannot be told from a low voice (a telephone band would start at about 300 Hz and run to 3.4 kHz; this has almost nothing above 1 kHz).
- Decay at 2:22 (50 ms envelope of the stem): -73 dB at 2:21.5, -22 at 2:23.0, -55 at 2:23.5, -37 at 2:24.0, -71 at 2:24.5. So the event is two bursts about 1 s apart, each falling about 30 dB in 0.5 s. That is a dry gate-like shape, **not** the 4 s decay voice quoted in round 1. A reverb tail would show an exponential fall over seconds; I measure none. I correct my own round-1 report of "decay about 4 s" as not applicable: the 4 s was the band's own fade, not the voice's. Medium.
- 4:29: the mix barely changes (200-1000 Hz share 51% against 46%; 1-4 kHz 21% against 22%) while the vocals stem is full-bandwidth (85% roll-off 3.9 kHz, 95% 7.3 kHz). A stem that is broader than the mix change it should have caused is separator bleed of the band, so the stem energy at 4:29 does not independently support a spoken phrase. Whisper's "top of a mountain" text has no acoustic support I can measure, and I rate the phrase unverified (low). This answers my own round-1 question to voice about 4:29.
- 5:12: the "voice" is, in the mix, **a steady tone at 1572 Hz** for the whole 1.2 s (FFT peak 1571-1574 Hz in every 0.2 s slice of the mix; the stem finds 1343-1499 Hz, i.e. bleed). A steady 1.57 kHz line is a pitched partial (it lies 4 cents above G6 at 1568 Hz, and is about 8.0 times 196 Hz, a G3 fundamental, which the A/G vamp would supply), not speech. Measured; interpretation (a partial of the band, or a whistle-like synth) INFERRED, low. I withdraw "speech-like" for 5:12.
- 5:30-5:42.5: the mix in this span is 91% between 200 and 1000 Hz and has almost nothing above 4 kHz (0.1%); the body 8 s earlier had 32% at 1-4 kHz. So the tail is narrower than the body, but this is mostly because the drums, bass and brighter layers have left, leaving the A pad; it is not a separate band-pass filter on the whole mix. The stem's 95% roll-off 3.5 kHz does mark the murmur as band-limited relative to the full-range body (its 4-8 kHz share is 2% against 3-5% in the body), but at -50 to -62 dB the high bands may simply be below the separator floor. Band-limited, **medium**; "archive sample" is not established, since a low-level, quiet, narrow-band voice and an old sample give the same figures.
- Summary for the lineage question: none of the four events is full-range. Two are low-level and narrow (2:22, 5:30), one (4:29) is probably band bleed, one (5:12) is a tone. This leans toward "a quiet, processed or sampled layer", not toward "studio-recorded full-band", but does not reach "archive", which needs a measured band-limit AND noise floor that I do not find. Low-medium.

**Rhythm Q2: is the 4 s stab decay a reverb or gate shape; is the pulse layer from 0:48.8-1:04.8 plucked, struck or sampled; is there a distinct low drum?**
- Stab decay (20 ms RMS of the "other" stem, every 0.5 s after each stab):
  - 1:00.83: -20.7, -21.9, -23.4, -26.6, -32.0, -42.4, -52.8, -59.2 dB (0.0 to 3.5 s).
  - 1:04.84: -24.3, -22.4, -24.6, -29.2, -35.1, -46.5, -57.9, -64.4 dB.
  - 1:08.85: -18.2, -20.7, -23.6, -28.0, -32.5, -40.3, -50.4, -62.3 dB.
  - 1:12.89 is different: stays at -22 to -24.4 dB for 3.5 s (the next sound overlaps).
  The shape is not an exponential reverb tail. It sustains for about 1 s (down only 2 to 5 dB), then falls at about 10 to 20 dB per second (from -23 at 1.0-1.5 s to -53 at 3.0 s). That is a held note with a late release (an envelope or gate, or a sustained source being stopped), not room decay. Measured, medium. It does not look like a single sampled loop either: the first-stab fall differs from the third by 4 to 5 dB at the same delay, and the fourth does not fall at all, which fits my round-1 cross-correlation 0.17-0.33. A played, repeated chord stab with a similar release fits best; plucked versus struck versus synthesised cannot be chosen (INFERRED, low).
- Low drum: in 120-160 s the **drums stem has only -48.6 dB in 45-90 Hz, 17.6 dB below the bass stem (-31.0)** and 12 dB below its own 90-300 Hz band (-36.2); its energy sits in 90 Hz-3 kHz (-36.2, -35.7), with 3-10 kHz at -39.6. In 260-300 s the same: 45-90 Hz -46.9 against 90-300 Hz -34.9. So the demucs drum stem has no strong sub-100 Hz thump. Either the kick is a low-weight, mid-weight (about 90-300 Hz) hit, or its low weight is credited to the bass stem, or the kit is toms-and-snare dominated. This supports rhythm's finding of a flat kick phase histogram: I cannot show a distinct low kick. Measured for the band shares, medium; the interpretation "no dedicated deep kick" is INFERRED, low-medium. (My attempt at a drum low-band envelope peak count returned nan because of an empty filter result; I do not report a peak rate from it.)

## 2. Corrections to colleagues (with evidence)
- **Voice, "dry or telephone"?** Answered above: no reverb tail at 2:22 (two bursts, each -30 dB in 0.5 s); no whole-mix band-pass at 5:30-5:42 (the mix narrows because layers leave).
- **Voice, 5:12 as a voice event:** it is a stable 1572 Hz tone in the mix, not speech (section 1).
- **Voice/Form/Feeling, "voice events recur as section markers":** four events with three different spectral characters (low-mid murmur, bleed, tone, quiet band-limited murmur) are not one repeating source. Using them as recurring markers is not supported by the sound.
- **Feeling, "the 22 dB fade" is the main cause of the ending's feeling:** I measure 48 dB in 14 s from 5:28 (round 1, about 3.4 dB/s), so the fade is about twice as large as stated. The murmur's mix share is about 0 dB relative; the cut is a hard 30 ms ramp. Of Voice's Q3 (how much human feeling is from murmur versus fade and cut) I can say that the fade is the larger measurable event; the murmur is at -50 to -62 dB.
- **Rhythm's retraction of kick syncopation:** I agree, and add that the drum stem has no strong low band (above), so a "kick" reading of low-band peaks was always weak. Rhythm's tempo glide (118.5 to 125 BPM) refines my round-1 check of 4 s spacing against 123 BPM: I accept the local tempo of about 120 BPM (4.0 s = 8 beats = 2 bars at 1:00-1:40). My round-1 comment "does not lock to the tracker beat" is explained.
- **Own corrections:** (1) the "10-25 cents flat" claim (above). (2) Round 1 said CLAP "vinyl crackle" is constant: unchanged. (3) I called the 5:30-5:42 layer "a mid-band speech/noise residue": the mix there is 91% in 200-1000 Hz, which is the pad's own partial series (217-877 Hz); the "centroid 3.5 kHz" in the vocal stem only describes the stem. I now say: pad plus a very quiet band-limited murmur.

## 3. Connections
- **Sound serves form:** at every rhythm-section change I listed in round 1 (3:45.2, 4:40, 5:17) the mix level stays within 0-4 dB, so the sections are heard as colour changes. At 3:44 the colour change is now quantified (30-150 Hz -3.8 dB, 1-4 kHz +6.4 dB): lighter and brighter, not louder.
- **Sound and rhythm:** rhythm's tempo glide of 118.5 to 125 BPM, together with the brightness peak at 3:44-4:00 (centroid 3.1-4.1 kHz, round 1) and the 20 dB loudness ramp, means the body accelerates and brightens together; the 4 s stabs release at 10-20 dB per second, so they breathe at the speed of two bars of about 120 BPM (a metaphor is avoided: this is the measured fall). Lack of a deep drum band (drum stem 17.6 dB under the bass in 45-90 Hz) means the pulse is carried by the bass quarters (rhythm: 0.484 to 0.506 s) and by mid-band hits, which fits the dense, mid-forward mix (1-4 kHz about 40% of magnitude at 4:00-4:20).
- **Sound and feeling:** the end sounds unresolved because of the measured mechanics: a pad of exact harmonics (217-877 Hz) fading 48 dB in 14 s with a 1.2 s-scale murmur beneath it, then a 30 ms ramp to zero. No decay tail, no final hit.
- **Sound and harmony:** the 1572 Hz line at 5:12 (G-family partial) and the pad's partial series on A (217-219 Hz) both agree with an A/G centre; I find nothing in the timbre that argues for major or minor (no third is isolated).

## 4. Production era (rule 1), updated INFERRED
**Judgement unchanged: modern loud master over material that was probably played, not a loop-machine DAW build; no measured archive layer. Confidence medium-high for modern master, medium for "no older source".** Figures: sample peak 0.0 dBFS and true peak +0.50 dBTP (round 1); median 1 s RMS -16.9 dBFS, 10 s crest 14-17 dB; an unvarying 17 kHz lowpass across all sections (so no band-limited layer separated from the full-band mix: the opening collage and loud body are alike); no loop repeat (rhythm's drum autocorrelation 0.01-0.11 at 3.9 s; my stab waveform cross-correlation 0.17-0.33; stab decays differ by 4-5 dB and one does not fall); tempo glide 118.5 to 125 BPM (rhythm, bass IOI); pad pitch 3-24 cents flat and wandering by 12 cents. New this round: no strong sub-100 Hz in the drum stem (45-90 Hz 17.6 dB under bass), so nothing suggests a modern sub-kick drum-machine build (low-medium). Kick onset spread from the grid: still not determinable (rhythm's flat phase histogram); I do not use it.

## 5. Boundary evidence, re-checked this round
| boundary | drums | bass | vocals | other | mix | carried by |
|---|---|---|---|---|---|---|
| 3:44-3:45 | continues | -17.5 dB in 30-150 Hz band (3:30-3:43 to 3:47-4:00) | none | 1-4 kHz up, low band -3.6 dB | 30-150 Hz -3.8 dB, 1-4 kHz +6.4 dB, 150-1000 +1.0 dB | bass leaves, "other" brightens |
| 2:21.5-2:26 | not re-measured | ducks (round 1) | two low-mid bursts, about -22 dB peaks, 200-1000 Hz | band continues | 200-1000 Hz share 32% to 58% | vocals stem and mix band shares |
| 5:12 | not re-measured | not re-measured | stem energy is bleed of a tone | tone at 1572 Hz | 1-4 kHz share 20% to 41% | other (tone) |
| 5:30-5:42.5 | out | out | murmur, 95% roll-off 3.5 kHz, about -50 to -62 dB | pad 217-877 Hz | 200-1000 Hz share 64% to 91% | other, then vocals/noise |
Silence is used only for the digital zero at 0:00-0:11.3 and from 5:42.9. End of track (round-1 figures, not re-measured): last non-zero sample 5:42.835, last 10 ms frames -70.6, -76.1, -93.8, -101 dB then exact zero; no final hits (the ten local maxima are -47.5 to -58.3 dB wobbles on the fade).

## 6. Two new questions
1. **Harmony:** the final pad's partial balance moves from the 3rd/4th partials (5:22-5:30, fundamental 30 dB down) to the 2nd (5:30-5:38, fundamental 20 dB down), with the fundamental 217-219 Hz. Does your chord tracker's A/Am call at 5:20-5:42 depend on the missing fundamental, and is there any third (C or C#, near 261/277 Hz) in the pad at all, or is it an open fifth (A and E at 329/659 Hz)? Also, does the 1572 Hz line at 5:12 sit inside your chord at that time (G-family: G, B, D)?
2. **Form (with voice):** given that the 2:22 event is two dry bursts about 1 s apart, the 5:12 event is a 1.2 s steady tone and the 5:30-5:42 layer is a quiet band-limited murmur, would you still treat "voice-like events" as one recurring structural device? And is the 3:44 change (low band -3.8 dB, 1-4 kHz +6.4 dB, bass stem -17.5 dB) strong enough, in your table, to be a section start by itself, or only a sub-section colour change within the 3:20-4:00 block?

## Not recoverable by measurement
- Exact instrument identity (guitar, organ, synth, bowed or reed-like source, sample): harmonic ladders and band shares do not separate these.
- Whether the voice-like events are spoken words, a sample or an instrument; what is said; and the real source of the 4:29 Whisper phrase (no acoustic support found).
- Whether the 3-24 cent flat tuning is tape, a detuned or hand-tuned instrument, or an artefact of stem separation and fade smearing: all give the same figures.
- Whether the drums are live, sampled or programmed, and whether a separate deep kick exists: the drum stem has no strong sub-100 Hz band, but separator behaviour hides the cause.
- Reverb time and room: the dry gate-like shapes measured (stab, 2:22 bursts) say the layers are not reverberant, but not what space, if any, they were recorded in.
- Recording date, performer, source film or broadcast: no measured marker survives a limited master and a 17 kHz lowpass.
- Whether the 11.3 s lead-in and 18.1 s trailing zero belong to the release or to this file.
- Intent behind the fade-and-cut ending: measurements show the 48 dB fade and the 30 ms ramp, not why.
