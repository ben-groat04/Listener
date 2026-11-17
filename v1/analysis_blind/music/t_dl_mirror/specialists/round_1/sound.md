# t_dl_mirror: SOUND specialist, round 1 (blind, measurements only)

Scope: sound design and production. I read all twelve `win_*.md` notes, then re-measured the whole file myself (helpers: `v1/scripts/agents/sound_r1_tdl.py`, `sound_r1_b.py`, `sound_r1_c.py`, `sound_r1_d.py`). I also looked at `music_views/window_0100s.png`. Times are m:ss. Stem levels are dBFS RMS from the demucs stems (estimates, they leak). Tags: measured / INFERRED, with high/medium/low.

## 0. One-paragraph verdict

A loud, hard-limited, mono, hip-hop-shaped mix: a punchy, dry, full-range-looking drum part, a short gated bass that comes and goes, a sustained harmonically ruled "bed" that holds a D-A fifth for the whole 3:56, and a dry, forward, close-sounding voice (rap verses, then a chanted or sung hook). The whole file has a hard ceiling at 8.0 kHz in every stem and the mix. That ceiling, the mono image and the clipping say the file was made or carried through a 16 kHz-class, mono, loudness-maximised stage. It does not read as one period recording. It reads as modern loudness handling on top of a narrow-band chain. Whether the bed is archive material is open (section 8).

## 1. Instrumentation, timbre (each with evidence)

| Layer | What the measurements show | Tag |
|---|---|---|
| Drums | Vertical, broadband transients with short decay across the drums panel (`window_0100s.png` panel 3). Stem rms about -19 dB all the way through (30 s blocks -18.4 to -20.6). 95% of drum-stem energy is below 6.3 kHz, 99% below 7.4 kHz. Kick-band (<150 Hz) onsets: 774 detected, modal inter-onset intervals 0.16 s, 0.14 s, 0.30-0.32 s, 0.64 s (about 94 BPM quarter, eighth and sixteenth subdivisions). Drum hits are re-used sounds: bar-to-next-bar mel correlation median 0.73, but the 10 ms placement varies (win_0020: envelope correlation about 0.3). Drum-machine versus live kit: not recoverable (section 9). | measured high; kit identity not recoverable |
| Bass | Short gated bursts, 0.5-1.2 s long, long gaps (up to about 4 s). 95% of bass energy below 221 Hz, 99% below 296 Hz, centroid 97 Hz, so a clean low sine-like or filtered tone with some harmonics to about 1-2 kHz at note onsets (bass panel). Stem rms -16 to -18 dB, the loudest layer under the voice. Peaks at -1.6 dB. Enters and leaves as a rhythm-section part, not as a continuous line. | measured high; "808-style" or synth versus electric bass is not recoverable |
| "Other" bed | Continuous for the whole track. Strongest partials at 148, 296, 444, 592, 740, 888, 1036, 1187 Hz and so on (3:40-3:48 spectrum), spaced at 148 Hz: a harmonic series on a 148 Hz fundamental (about D3, 146.8 Hz, cents-level differences not claimed). That fits a held D drone with its overtones and no strong third. Centroid 0.9 kHz, 95% of energy below 1.8 kHz, high-passed 3 kHz content is -43 dB (the mix is -20.8). Stem rms -25.7 to -28 dB, 8-10 dB under drums and bass. | measured high (harmonic series); identity (organ, synth, guitar, sample) not recoverable |
| Voice | Dry, forward, close. Band energy of the vocal stem over 0:40-3:20: 100-300 Hz -34.6 dB, 300 Hz-1 kHz -30.5, 1-4 kHz -33.6, 4-8 kHz -42.2. Formant ladders visible to 4 kHz, fricatives to the 8 kHz ceiling. Stem rms -16 to -23 dB (loudest stem in verses). Pitch about A3 in verses, up to A4 in the hook (win_0140, win_0080). | measured high |

Mix balance by 30 s block (stem rms): vocals -16 to -19, drums about -19, bass -16 to -18, other -26 to -27. Voice, drums and bass sit within about 3 dB of each other. The bed is a bed, 8-10 dB lower. Exception: 3:30-4:00 vocals fall to -30 dB (voice leaves at 3:35.3).

## 2. Stereo image (measured, high)

Dual-mono. The two channels are identical except for isolated samples: 8,666 of 10.56 million samples differ (0.08 %), grouped around 0:00, 0:08, 0:10, 0:11, 0:19, 1:09, 3:41, 3:44 and 3:46 (first at 0:00.27, a 0.355 vs -0.355 sample pair is an equal pair, so the difference is sample-level). Stem L-R rms: other -51 dB, drums -43 dB. The largest single L-R difference is 2.0 (one full-scale sign flip), consistent with a clipping or encoder glitch, not a stereo effect. The per-second `width` of 0.195 at 0:10 and 0.168 at 0:18 is the same few clip-adjacent samples (the hard-clipped runs at 0:10.7 and 0:18.4 are in the same seconds). There is no panning, no stereo reverb, no wide pad. Any impression of "space" comes from the sustained bed alone.

## 3. Space and reverb (INFERRED, medium)

Dry. Evidence: vocal-stem phrase gaps go black within 0.25-0.5 s (e.g. 0:11-0:12.2 at about -50 dB; 1:12.2-1:13.1 at -47 to -66 dB; 3:26.91-3:27.77 below -45 dB), so no tail bridges them. Drum hits show short decays in the panels. A mono file cannot carry stereo ambience; a short mono room tone cannot be excluded because stem separation would hide it. Limit: demucs may strip tails.

## 4. Distortion, clipping and limiting (measured high; cause INFERRED)

- Sample peak 0.0 dBFS. 21,079 samples (left channel count, at or above 0.999) in the file; 10,317 samples exactly at the maximum. 542 clipped runs, of which 313 are two or more samples long.
- Clipping is concentrated in two places, not spread evenly: 0:10-0:20 (3,886 samples in 0:10-0:15, 2,794 in 0:15-0:20) and 2:55-3:00 (3,377 in 2:55-3:00, with a 3,200-sample run, about 73 ms, at 2:57.45). Elsewhere it is 5-100 samples per 5 s. The longest runs at 0:10.66, 0:10.68, 0:18.44, 0:18.51 (1,000-1,158 samples, about 23-26 ms) coincide with the voice entry and crash hits. These are real flat-topped waveform stretches, i.e. the mix clips on its loudest events (voice plus bass plus crash arriving together at 0:10.4, and the 2:57.4 broadband hit).
- Otherwise the mix is limited: 10-s block RMS holds -10.0 to -10.9 dBFS from 0:10 to 3:40 and crest factor 10.0-10.9 dB (block 0:00-0:10: -11.9 dB RMS, crest 11.9). That plateau is flat to within 1 dB over three and a half minutes, which a limiter or heavy compression produces.
- Stem peaks: vocals -0.1, drums -0.1, bass -1.6, other -3.6 dBFS (stems are sums, so not additive evidence).
- Saturation inside the bed or bass cannot be separated from limiting. The bed's partial series is clean (evenly spaced, 12 or more partials seen). No guitar-style distortion is demonstrable (low).

## 5. Bandwidth: a hard ceiling at 8 kHz (measured, high)

Long-term Welch spectrum of the mix: -61.5 dB at 8.0 kHz, -75.7 dB at 8.5 kHz, -80 dB at 9-20 kHz and flat after that. In 250 Hz bins the step is between 7,750 and 8,000 Hz (-59.7 to -74.6 dB) and the floor beyond sits at -80 dB, which is the same on every band to 20 kHz. Voice, drums and bass stems are all down at 9 kHz (-110.6, -85.8, -118 dB against -69.4, -67.7, -110 dB at 7 kHz; the bass has nothing there anyway). `window_0100s.png` shows a black band above about 8.2 kHz in every panel, in all stems. This is a brickwall at 8 kHz, which is the Nyquist frequency of 16 kHz sampling.

Consequence: no layer is "more band-limited than the rest". Every layer, including the drums, ends at the same frequency. That is a property of the file's source chain, not of one sample inside a wider mix (see section 8).

## 6. Loudness curve and dynamics (measured, high)

Mix RMS per 10 s: -11.9 (0:00-0:10), -10.0, -10.4, -10.4, -10.6, -10.4, -10.6, -10.4, -10.5, -10.2, -10.4, -10.5, -10.2, -10.9, -10.6, -10.1, -10.5, -10.1, -10.6, -10.7, -10.4 (3:20-3:30), -10.7 (3:30-3:40), then -13.2 (3:40-3:50, bass gaps) and -26.6 (3:50-4:00, the fade). Peaks sit at 0 dBFS in every block until 3:50. The track has essentially no loudness dynamics: the arrangement is shaped by subtraction (bass out, voice out) and moves the mix by 3-7 dB at most. Examples of that movement: voice and bass enter together at 0:10.4 (mix -11.8 to -8.4 dB, +3.4 dB; bass -52.8 to -20.2, vocals -67.1 to -23.0, drums -17.0 to -14.5, other -28.6 to -22.0); bass and voice leave at 3:34.3 (mix -12.2 to -11.5 at 3:34.7, but bass -18.1 to -37.8 and vocals -22.9 to -40.8) and the final bass leaves at 3:44.3 (mix -10.8 to -15.6, -4.8 dB).

## 7. Boundary evidence table (stems re-measured, 1 s before and after, dB)

I re-measured these boundaries myself. Others in the window notes carry their original tags.

| Boundary | Drums | Bass | Vocals | Other | Mix | Carried by |
|---|---|---|---|---|---|---|
| 0:10.4 voice and bass enter | -17.0 to -14.5 | -52.8 to -20.2 | -67.1 to -23.0 | -28.6 to -22.0 | -11.8 to -8.4 | bass and vocals together (drums and bed steady-ish) |
| 2:32.5 sung hook to rap verse | -17.6 to -18.6 | -20.6 to -18.2 | -21.8 to -16.8 | -23.0 to -21.2 | -10.0 to -9.9 | vocals only (delivery and pitch, not level; win_0140 shows the pitch fall from A4 to F#3-B3) |
| 3:34.7 voice's last line ends | -20.0 to -17.0 | -18.1 to -37.8 | -22.9 to -40.8 | -24.8 to -26.7 | -12.2 to -11.5 | vocals and bass leave together (my 3:34.7 sample is the 1 s pair about the 3:34.7 mark). A rhythm-section-plus-voice dropout; drums and bed continue. Not a silence. |
| 3:44.3 last long bass leaves | -17.9 to -21.0 | -14.8 to -58.1 | -73.7 to -75.2 | -28.6 to -26.9 | -10.8 to -15.6 | bass |
| 3:49.0 fade begins | -22.6 to -24.7 | -15.4 to -47.3 | none (-75) | -27.6 to -34.0 | -13.3 to -19.3 | bass out, then the bed fades (win_0220: bed -26/-29 to -70 by 3:56) |
| 3:56.0 tail | -45.9 to -64.6 | -77.0 to -57.7 | none | -57.4 to -70.5 | -40.8 to -54.8 | drum and bass tails; the bed decays under |

No row is a silence of the full mix before the ending. In every dropout drums and bed continue, so the word silence is wrong for them: they are rhythm-section or voice dropouts of 3-7 dB in the mix.

## 8. Production-era judgement (INFERRED, medium; figures given)

Judgement: modern loudness production, not one period-consistent recording. Reasoning, by the four cues in the brief:

1. Peak against 0 dBFS: sample peak 0.0 dBFS, 10,317 samples exactly at maximum, runs up to 3,200 samples; mix RMS flat at -10.0 to -10.9 dBFS with 10-11 dB crest for 3:30 minutes. This is modern loudness-war limiting or clipping (high that the file went through it; INFERRED high). A tape-era or early-digital master does not sit here.
2. Loop regularity: bar-to-next-bar mel correlation median 0.855 (other), 0.73 (drums), 0.61 (bass). The bed repeats with near-identical spectra, the bass less so, the drums re-use sounds with varied placement (win_0020, win_0040: bed correlations 0.91 at 1, 2, 4 bars; win_0100: 4-bar cycle at r = 0.76 for bass; vocal phrase repeats at 10.0, 9.8, 10.4, 10.1 s, win_0100 and win_0120). Together: a four-bar arrangement cycle with a near-static bed. Fits a DAW or sampler; none of it is bit-identical (the drums stem fails exact repeats), so a loop machine with live or varied additions rather than a pure copy. INFERRED, medium.
3. Kick spread: against a rigid 16th grid fitted at 93.6-95.8 BPM, the whole-file kick onsets show phase concentration R = 0.03-0.06 and rms deviation 43.6-44.8 ms, against 45.2-46.0 ms for random onsets. So there is no rigid grid on the file-wide 16th grid: tempo wanders. Tracker beat intervals have a standard deviation of 17-30 ms in 40 s blocks (block tempos 94.35-94.97 BPM) and 5th to 95th percentile 0.603-0.651 s. Against the tracker's beat grid (95.7 BPM, the same pulse as the kick intervals 0.64 s / 0.32 s / 0.16 s), the kick-band onsets fall into four lumps per beat (bins 3, 7, 11, 15 of 16, with 269 and 97 in the last two bins: a consistent early lead of about one 16th bin, 0.03-0.06 of a beat, i.e. about 20-40 ms before the tracker beat) and the half-beat and quarter-beat positions are all populated. So the pattern is a 16th-based one, but the clock is loose by tens of ms. win_0100 reported 14.5 ms rms on a local 16th grid over 20 s. A quantised DAW kick would show a few ms. This points to a human-played or loosely tempo-mapped source, or a sample whose own timing wanders, rather than a rigid sequencer (INFERRED, low-medium). It is the weakest of my cues.
4. Band-limited layer against a full-band mix: this cue is negative. There is no full-band mix to contrast with. Everything is cut at 8.0 kHz. The bed is darker than the rest (95% of energy below 1.8 kHz, against 3.6 kHz for the vocal stem and 6.3 kHz for drums), but a dark synth or organ explains that as well as an old source. CLAP says "vinyl crackle" 0.95-1.0 for most 5 s blocks, and also "no vocals" while the voice is at -22 dB, so it is a bad witness (low). The 3 kHz high-passed energy in the bed is -43 dB against -20.8 for the mix, so no crackle or hiss floor is visible in the bed. Verdict on an archive layer: not shown, not excluded (INFERRED, low).

Extra cues I measured: the 8 kHz brickwall (section 5), mono (section 2), and a smooth tail to digital zero (section 10). The 8 kHz ceiling suggests a source or delivery at 16 kHz sampling, or a deliberate low-pass at 8 kHz, before the final upsample to 44.1 kHz (measured; the cause is INFERRED, medium). Combined with mono and clipping, it fits a lo-fi or compact-format delivery that was later loudness-maximised and re-encoded as a 44.1 kHz stereo file with identical channels. It does not fit "modern hi-fi stereo production". So "modern production over archive" is partly supported (modern limiting, DAW-like four-bar arrangement) and partly not (no full-band contrast, no stereo, no archive-noise evidence).

## 9. Not-heard-but-assumed risks I checked

- "Heartbeat/bell" nouns: none used.
- Vinyl crackle: not measured. The only evidence is CLAP at 1.0 in nearly every block (including blocks where CLAP also says "no vocals" and "ice skating"), so ignored.
- Reverb: not shown (section 3).

## 10. End of track (rule 4, 10 ms envelope over the last 3.5 s, measured, high)

Duration 239.44 s. The last nonzero sample is at 3:56.70 (236.698 s). The last time the 10 ms mix envelope exceeds -60 dBFS is 3:56.45 (236.453 s, level -60.0 dB). The final audible sound is therefore at about 3:56.45. Per stem (envelope above -60 dB): drums to 3:56.37, bass to 3:56.38, other to 3:55.65, vocals never in the last 4 s. Level at the end: mix 10 ms envelope -46 dB at 3:56.01, -50 dB at 3:56.3, -56.7 dB at 3:56.44, then under -60 dB to the last nonzero sample 3:56.70, then exact digital zero until 3:59.44 (2.74 s of digital silence from the last nonzero sample; the tail of the file is about 3.0 s counting from 3:56.44). Final hits counted from the 10 ms envelope peaks (prominence 3 dB, 10 ms spacing, 3:56.0-3:56.5): about eleven small envelope peaks at 3:56.01, .03, .07, .11, .17, .19, .23, .33, .37, .39, .44, all between -45 and -57 dB. That is a decaying run of small events (drum tail and ghost hits), not a single closing hit; it is not a clean stop. I do not count them as intentional final hits. Fade shape: the bed falls from -26 to -70 dB over 3:49-3:56 (win_0220), so the ending is a slow fade of the bed and gated bass bursts, then a cut.

## 11. Disagreements and corrections to colleagues' notes

- win_0000 gives 6,720 samples at 0.999 in 0:00-0:20; mine is 6,680 (3,886 + 2,794) in 0:10-0:20 on the left channel plus 15 from 0:00-0:10. The difference is counting threshold; same conclusion.
- Several notes (win_0040, win_0120) quote a side/mid ratio of about -26 dB (0.048), others "exactly 0" or correlation 1.0. My whole-file result is: identical channels except 8,666 isolated samples. The -26 dB figure came from a window containing a few differing samples or from a stem sum; I treat the file as dual-mono (high).
- win_0100 and win_0140 call a 14.5 ms or tight kick grid medium evidence of programming; my whole-file figure (rms 43.6-44.8 ms, no lock) disagrees on a 16th grid. I tag the kick-spread cue low-medium and not usable alone.

## 12. Not recoverable by measurement

- Exact instrument identity (organ, synth, guitar or sample for the bed; drum machine or live kit; synth bass or electric bass): stems and spectra show harmonic structure and envelopes, not instruments.
- Whether any layer is archive or sampled material: no full-band contrast exists and CLAP's "vinyl crackle" is not a measurement.
- Why the file stops at 8 kHz (16 kHz sample rate, low-pass, or a low-bitrate encode) and whether the mono image was intended: the file cannot say.
- Recording date, performer, studio or mixing engineer: not in the signal.
- Whether the clipping was deliberate: only that it exists and where.
- Real reverb or delay inside the mix: demucs and mono summing may strip tails.
- Whether the voice is processed (compression, saturation, pitch correction): the contour and levels do not separate it from the limiter.
- Whether the D/Dm flicker is a real third: that belongs to harmony.

## 13. Three questions for fellow specialists

1. Rhythm: kick onsets lock on a quarter-beat lattice about 20-40 ms ahead of the tracker beats but drift on a file-wide 16th grid at 43-45 ms rms (random level). Is that a swung, human-played feel, a wandering sample clock or just tracker lag, and is the drum part a loop or played?
2. Harmony: the bed is a 148 Hz-spaced harmonic series (about D3 and its overtones), no strong third, and the D/Dm labels flicker. Does the bed itself ever move, for example in the "side-steps" Gm-G-F-Am at 3:19-3:32 (win_0200), or is the third coming from the voice only?
3. Voice (and form): voice and bass enter together at 0:10.4 with a roughly 46 dB vocal jump, and both leave together at 3:34-3:35. Is the vocal entry a sample or cut-in, and does the hook (sung, A4) versus verse (rapped, A3) treatment differ in compression or double-tracking in a way my mono, 8 kHz-limited measurements cannot show?
