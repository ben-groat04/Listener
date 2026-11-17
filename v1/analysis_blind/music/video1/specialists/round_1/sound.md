# video1: SOUND specialist, round 1 (blind, measurements only)

Role: sound design and production (instrumentation, timbre, distortion, space, stereo image, mix balance, loudness curve, era/style).
Evidence key: LV = music_views/per_second_levels.json; MV = music_views/window_NNNNs.png; CL = clap_tags.json; ST = stems/stem_rms_per_second.json; WN = the ten window notes (win_0000 to win_0180); MY = my own runs, v1/scripts/agents/sound_round1.py and sound_round1b.py (librosa/numpy on audio/song.wav and stems_raw/htdemucs/song/*.wav). I read all ten window notes and re-checked their sound claims; I also opened window_0120s.png.
Confidence labels: high / medium / low. Timestamps m:ss. I cannot hear; everything is inferred from measurements.

## 0. One-paragraph picture

This is a loud, dense, dry, heavily saturated mid-tempo (about 78 BPM) track. Its sound world is four things stacked: (1) a machine-tight sixteenth-note drum pulse that is weighted towards low thump rather than bright hats; (2) a wide, broadband, distortion-like "other" layer (guitar-wall and/or synth; identity unproven) that does most of the harmonic work; (3) a bass that is a different animal in different sections, from a bright gritty line (0:35 to 1:15 and 1:40 to 1:58) through a pure sub-bass sine "boom" played in four-to-six second pulses (2:01 to 2:40), to a thick, drum-locked low line (2:38 to the end); (4) a lo-fi, narrow-band, centred spoken-word sample (Dutch announcer-style) that is treated as an archive voice placed on top, not as a sung lead. Loudness is almost constant, so the "drama" is carried by spectrum, stereo width and entries/exits of layers, not by level.

## 1. Instrumentation (layer by layer, with evidence)

### 1.1 Drums (high on presence and pulse, low on kit identity)
- Present from 0:00 to the end except for the cut at 2:47.8 to 2:48.2 (WN 0160; MV 0160 black band). Drum-stem level is the loudest stem for the first 40 s (LV drums -14 to -17 dB; the vocal stem at -21 dB is the loudest only when it speaks).
- Onset gaps about 0.19 s against a 0.77 s beat (beat_times.json; audio_features tempo 78.3). That is four per beat: a steady sixteenth pulse (WN 0000, 0020, 0140, 0160; I re-ran counts, agree: about 4.5 onsets/s). Evenness suggests programming or very tight playing (medium); the CLAP "drum machine" tag (0.97 at 0:00, 2:55 to 3:05) is weak evidence, but the regularity itself is real.
- Weighted low, not bright: MY band split of the drum stem shows 76 % of energy below 150 Hz at 0:10 to 0:30, 60 to 69 % through most of the middle, 50 % at 2:50 to 3:00; only 2 to 5 % above 5 kHz for most of the track, rising to 11 to 13 % at 1:10 and 2:50 to 3:00 (MY). So the drum stem is a heavy kick/tom thump with the snare and hats a smaller part of the energy; the stem is not hat-dominated, despite the dense fast onset count. A caution: the 0.19 s onsets may be tonal low thumps, not hats, so "hi-hat" in WN 0000 and 0020 is unproven.
- Brightening events: drum centroid jumps from about 1.6 kHz to 3.3 kHz at 0:32 (WN 0020) and again after the stop at 2:48.2 (WN 0160: 2.2 kHz before, about 4.7 kHz after). These read as a hat or cymbal layer opening up (medium).
- Very dry: hits are vertical lines with short decay in every drum panel (MV all windows). No visible reverb smear (medium-high; but see 4).

### 1.2 "Other" layer (high on presence and heavy saturation, low on instrument)
- Continuous from 0:01.3 to the end bar the 1:58 to 2:12 reduced passage and the bass-less stretches. Stacked horizontal harmonic lines to about 8 kHz, no empty gaps between partials (MV 0000, 0140, 0180).
- MY: the "other" stem's 99 % spectral roll-off averages 8.5 kHz and its flatness is the lowest of any stem (0.001 versus drums 0.018), meaning a dense, strongly tonal, thick-harmonic signal. The 8 kHz ceiling is a hard shelf in MV 0160 and 0180 (WN 0180: 17 % at 2 to 6 kHz, 0 % above 6 kHz). Consistent with distorted guitars, fuzz bass-guitar bleed, or a saturated synth saw (medium); a pure clean pad is unlikely because the stack is so dense.
- CLAP gives "distorted guitar" at 0.86 to 1.0 in many 5 s blocks (0:05, 0:45, 0:55, 1:00 to 1:15, 2:20, 2:40 to 3:05) and "brass" at 0:20 to 0:30 and 0:50, "drum machine" at others. Contradictory labels across blocks mean CLAP is reacting to texture, not naming a single instrument. I treat it as weak support for "gritty, guitar-like or fuzz-synth".
- Rhythmic: onset rate 4.3/s at 0:20 to 0:32 (WN 0020) and 50 onsets with median gap 0.186 s at 3:00 to 3:08 (WN 0180). The "other" layer is playing a fast repeated figure, so a chugging/picked riff or sequenced saturated synth (medium).
- Stereo: by far the widest stem (MY: L/R correlation 0.22, side/mid -2.0 dB; bass 0.92, -13.9 dB; drums 0.87, -11.3 dB). The track's width movements (section 3) are mostly this layer widening or narrowing.
- The few clear tonal peaks in the stem at 1:20 to 1:46 (MY FFT peaks: about 220 Hz (A3), 148 Hz (D3), 293 Hz (D4), 330 Hz (E4) at 1:30 to 1:46) show D and A fundamentals, a power-chord-like open fifth stack, again guitar- or synth-compatible (low-medium).

### 1.3 Bass (high on register; role shifts by section)
Four distinct bass identities, each evidenced:
1. 0:03 to 0:20: slow 22 dB swell from the floor to -19.5 dB, below 250 Hz at first, brightening after 0:16 (LV bass; WN 0000).
2. 0:35 to 1:15: "bite". Share of bass-stem energy above 300 Hz doubles from 15 % to 29 % at 0:32 to 0:35 and its centroid goes from about 260 Hz to 425 Hz (WN 0020). Bass level -15 to -16 dB. Either an overdriven bass guitar, a fuzz synth bass, or leakage of the guitar layer into the stem.
3. 2:01 to 2:40: the sub. MY (sound_round1b): FFT peak locked at 42.6 Hz in every burst (2:01.3, 2:07.3, 2:13.5, 2:19.7); the second and third harmonics are 38 to 48 dB below the fundamental. That is an almost pure sine. MV 0120 shows it as a flat, perfectly straight horizontal line below 100 Hz with a sharp onset, about 1.5 s long. The frequency does not glide (42.6 Hz flat within 0.1 Hz for about 1 s; only the first and last 0.25 s frames wander, which is windowing at attack and release). My envelope run: onset to -12 dB within 0.05 s, slow decay about 11 dB over 1.5 s, then a cut to the floor in 0.1 s, i.e. a gated or enveloped synth sub, not a plucked bass guitar (high on "sine-like, fixed pitch", medium on "synthesised"). 42.6 Hz sits roughly 40 cents under F1 (43.65 Hz), so it is likely a detuned, or tuned-to-another-reference, F; whichever, it is a low "b3"-ish pitch against D, or it is felt mostly as weight. The mix spikes by 3 to 4 dB at each hit (LV 121 s -12.1 dB; 127 s -12.3 dB; 133 s -12.3 dB).
4. 2:38 to 3:08: a broader low line: 97 % of the bass-stem energy below 150 Hz, centroid about 320 Hz, onsets within 20 ms of the drum onsets (WN 0180; the stem fine-FFT at 2:38 to 2:40 gives peaks at 65 to 74 Hz, C2 to D2). A "pumping", drum-locked line (medium).
- The 1:15 to 1:40 stretch has no bass at all (stem -65 dB at about 1:15; returns at 1:40 at -19 dB; WN 0060, 0080, 0100). MY mix measurements: M/S side level rises, correlation drops to 0.25 at 1:30 to 1:40.

### 1.4 Voice / sample (high on timbre, medium on origin)
- Spoken Dutch (Whisper NL transcript, language p = 1.0; the translate pass reads dates and a race name). Centred; narrow in band: MY shows 64 to 83 % of vocal-stem energy in 300 Hz to 3 kHz, 15 to 35 % in 3 to 8 kHz and 0 % above 8 kHz in every segment I tested (0:10, 0:20, 1:40, 2:15, 2:44). No low rumble (below 300 Hz 0 to 10 %). A band-limited, mid-forward, noisy transmission or archive-tape quality, as distinct from a modern close-miked vocal (medium).
- Level: -21 to -22 dB in the stem when speaking (LV 0:10, 0:20), on a par with or above the "other" layer, so the voice is a foreground narrator, not buried.
- No audible sung part: lead_notes.json lists only scattered short notes, and the vocal stem sits at the -65 dB floor except for spoken bursts (LV). Hence there is no "vocal sound" to speak of beyond a spoken sample, and that is the track's single human-textured element.
- No measurable reverb on it: bursts end sharply (MV 0120 vocals panel: 2:15 and 2:18 bursts with vertical edges). Dry placement, "voice on top of the bed".

### 1.5 Texture / noise layer (low confidence)
- CLAP "vinyl crackle" at 1:30 and 1:35 (0.99), 2:55 to 3:05 (0.92 to 0.98), "wind" 0.82 to 1.0 at 0:55 to 1:00 and 1:30, "engine" 0.9 at 0:40 and 0:45. These are not independent of the distortion wash. My MY measurement shows the mix carries energy to about 18 kHz and then drops off a cliff above 20 kHz (mean level -21 dB above 18 kHz, -68 dB above 20 kHz), which looks like a lossy-codec low-pass, not tape hiss. I would not claim vinyl or tape noise. At most: broadband high-frequency fizz from the distortion and cymbals, and a noisy archival voice.

## 2. Timbre, distortion, space

- Distortion: high-medium. Four independent hints agree: dense unbroken harmonic stack in "other" (MV 0000/0140/0180); the stem's lowest spectral flatness and 8 kHz shelf (MY); the bass-stem upper band growth at 0:35; CLAP "distorted guitar". Cannot say fuzz versus amp overdrive versus synth saturation.
- Compression: the mix is dense. MY: sample peak -0.0 to -0.5 dBFS throughout, short-term RMS about -11 to -14.8 dBFS, so crest factor about 11 to 14 dB across 10 s blocks (lowest 10.8 dB at 1:00 and 1:40, highest 14.3 dB at 2:00). By hot-modern standards that is loud but not brickwall; individual drum hits still stick out. Consistent with LV's very flat dbfs curve (-10 to -12 for most of the track). Peaks at about 0 dBFS suggest limiter or clipping (medium).
- Space: dry. No decay tails on drums, voice or bass bursts (WN 0020, 0140, 0160; MV 0120). The one exception is the very end (3:08.0 to 3:08.5, a short tail; 3:07.6 to 3:08.4 envelope in WN 0180 and my 10 ms RMS: about -15 dB to -20 dB then a cut). The "space" is therefore made by the stereo spread of the "other" layer (width), not by room or reverb. I cannot exclude short gated reverb.
- Spectral balance (MY on mono mix, whole song): 20 to 60 Hz 9.5 %; 60 to 150 Hz 37.6 %; 150 to 500 Hz 30.3 %; 500 Hz to 2 kHz 14.7 %; 2 to 6 kHz 6.8 %; 6 to 12 kHz 0.9 %; above 12 kHz 0.2 % of power. It is a low-heavy, bass-and-low-mid-dominated mix (about 77 % of power below 500 Hz), with only a modest presence band. Centroid moves between about 1.8 kHz (0:20 to 0:30, 1:40 to 1:50) and about 3.9 kHz (2:10 to 2:20), measured on the mono mix.

## 3. Stereo image

Per-second width (LV "width", the toolkit's own side/mid index) and my side-to-mid and correlation measurements agree on the shape:

| Span | Width (LV) | MY corr L/R | What changes |
|---|---|---|---|
| 0:00 to 0:30 | 0.24 to 0.40 | 0.84 to 0.78 | Narrow: drums, centred bass and voice dominate |
| 0:32 to 0:42 | 0.47 to 0.55 | 0.67 | Voice leaves; drums and "other" fill sides |
| 0:43 to 0:56 | 0.46 to 0.65 | 0.57 to 0.64 | Wide build |
| 0:57 to 0:59 | 0.33 to 0.39 | | Narrowest at the loudest moment (WN 0040) |
| 1:06 to 1:14 | 0.60 to 0.71 | 0.46 | Loop opens out |
| 1:27 to 1:39 | 0.62 to 0.83 | 0.25 | Widest early peak: bass-less "wash" |
| 1:40 | drops to 0.40 to 0.47 | 0.56 | Bass (centre) arrives |
| 2:00 to 2:12 | 0.20 to 0.36 | 0.86 (2:00 block) | Narrowest and most stripped; sub hits narrowest of all (0.20 to 0.22) |
| 2:13 | rises to 0.47 to 0.57 | 0.60 | "Other" steps up about 8 dB and widens |
| 2:48 to 3:08 | 0.69 to 0.86 | 0.27 to 0.33 | Widest part of the track after the 2:47.8 stop |

Interpretation (medium-high): width is mostly a function of which layers are present. Centred sources (voice, bass, sub) pull width down; the wide "other" layer pushes it up. The track therefore alternates between a narrow, focused "mono-ish" punch (opening, the 2:00 reduced passage, bass hits) and a wide, enveloping wash (1:27 to 1:39, the final minute).

## 4. Loudness curve and mix balance

- Mix level (LV dbfs): -19.9 at 0:00, -13.6 at 0:01, plateau -12 to -13 through 0:19, -11 to -12.9 for 0:20 to 0:40, loudest stretch about -10.3 at 0:57 to 0:58 (WN 0040) and -10.3 to -11.4 for 1:00 to 1:14; a 4 to 5 dB drop to about -14.5 to -16.4 at 1:15 to 1:26 (bass leaves); climbs to about -12 to -13 from 1:27 and -10 to -11 at 1:40; flat at -10.3 to -11.4 until 1:58; falls to about -16 at 2:00 to 2:12 (with +4 dB spikes at the sub hits); -12 to -14.6 from 2:13; about -11 to -12.6 to 3:07; stop at 3:08.
- MY 10 s blocks (RMS on mid): -14.4 (0:00), -11.0 (1:00 and 1:40), -14.8 (2:00), -11.4 (3:00). Overall dynamic range is narrow; section contrast is mostly 3 to 5 dB.
- Mix balance by stem (LV): drums -14 to -17 dB first, then "other" and bass at -15 to -21 dB; vocals -21 dB when present. Level order changes by section: opening drums > other > bass; 0:35 to 1:15 bass about equal with other; 1:20 to 1:40 "other" dominant (no bass); 2:01 to 2:12 drums dominant (other -25 to -31 dB); final minute "other" loudest (-14.6 to -17.6 dB; WN 0180), drums and bass underneath.
- The ending is an abrupt gate: about 20 dB drop from 3:07.5 to 3:08.1 (-40.6, -57, -66, -81 dB per 0.1 s in WN 0180), silence at 3:08.3. High confidence. Not a fade.

## 5. Section-by-section sonic map (what a listener would hear)

- 0:00 to 0:09: drums alone (a short noisy pick-up), then a dense saturated wash at 0:01.3, then bass creeping in; the voice at 0:09.
- 0:09 to 0:32: narrator over groove; mix is centred and narrow (width about 0.3 to 0.4).
- 0:32 to 0:41: voice leaves, bass bites, drums brighten, image opens. A "release into groove".
- 0:41 to 1:15: wide, loud, hard, gradually tightening; bass-rich; peak loudness at 0:57 to 0:58.
- 1:15 to 1:40: bass vanishes; thin low end, wide wash, held tones (WN 0060 notes a high shimmering tone with a possible bell-like CLAP tag at 1:15; weak). Loudness drops 4 to 5 dB then recovers by 1:40. The "exposed" part of the track.
- 1:40 to 1:58: bass returns, loud, dense, speech bursts at 1:46 and 1:57; at 1:58 the "other" layer falls 10 to 15 dB with a rising high-frequency wash (WN 0100) and width collapses to about 0.2.
- 2:00 to 2:12: stripped, narrow: drums, dry sub boom (42.6 Hz) every 6.1 s, thin "other" at -25 to -31 dB.
- 2:13 to 2:40: "other" steps up and widens; the sub continues in bursts; speech list reading in short bursts.
- 2:38 to 2:47.8: the sub is replaced by a drum-locked thicker low line; loud; drums darker.
- 2:47.8 to 2:48.2: a full-band cut (all stems), about 0.4 s of near-silence. Then the brightest, widest, most "hissy" section (shelf near 9 to 10 kHz, width 0.69 to 0.86).
- 3:00 to 3:08: continuous loud wall, no voice; abrupt end at 3:08.3.

## 6. Era and style of production (low-medium)

- Style-wise, the combination (programmed-sounding sixteenth drums, saturated guitar-like wall, synthesised sub boom, archive-voice sample on top, dry mix, narrow dynamics) is a hybrid of electronic and rock production with a spoken archival sample, in the lineage of sample-led post-rock/electronic rock of the 2000s to 2020s. I cannot name an artist from measurement.
- Sub-bass sine at 42.6 Hz with a gated envelope, and the dryness plus width-by-saturated-layers, are signatures of modern (2010s on) digital production (low-medium: a pure sine sub requires a synth or a sampler, which could be done at any time since the 1980s; but combined with the density and 0 dBFS peaks it points to a recent loud-era master).
- The sample voice itself is much older in character than the band (narrow, mid-forward, noisy), so the track mixes two eras on purpose: modern loud music with archive speech (medium).
- 20 kHz brick-wall low-pass in the mix (MY) tells us about the file's encoding, not the production era.

## 7. What a human would feel from the sound design

- Weight and menace from the low-heavy balance (77 % of power below 500 Hz) and from the pure sub boom: felt in the body, not heard as a note (high).
- Relentless, hypnotic drive from the constant 16th pulse and the never-moving loudness; no breathing room except at 1:15 and 2:00 (high).
- Dryness gives an unromantic, close, almost documentary feeling: no cathedral echo, the music is in the room with you (medium).
- The wide wash at 1:27 to 1:39 and 2:48 to 3:08 feels enveloping and slightly overwhelming; the narrow stretch at 2:00 to 2:12 feels clenched and stripped (medium).
- The scratchy, narrow announcer voice sets "archive / history" against the modern machine groove: an eerie, respectful distance (medium).
- The abrupt stop at 3:08 leaves a shock of silence rather than release (high on the stop; medium on the felt effect).

## 8. What the measurements cannot tell

- Guitar versus synth versus organ for the "other" stem; electric bass versus synth bass for the 0:35 to 1:15 bass; kit versus machine for the drums.
- True reverb or delay: absent in the stems I looked at, but short or gated reverb could be hidden by distortion.
- Whether the "vinyl crackle" and "wind" CLAP tags correspond to any real noise; my spectral evidence says no.
- Whether the sub's detune (about -40 cents from F1) is deliberate.
- Real bass versus guitar-bleed separation after 0:35: demucs stems are approximate, so "bass bite" may partly be leakage.

## 9. Three questions for fellow specialists

1. **Harmony:** the 42.6 Hz sine sub is fixed in pitch (no glide) and enters on the 8-beat grid in 2:01 to 2:40. Does your chord reading treat it as a sounded b3/F (so a Dm colour) or as a non-harmonic weight tone beneath D? Does the chroma "E/F" bar I saw in MV 0120 line up with each sub hit and nothing else?
2. **Rhythm:** my drum band split says the stem is 50 to 76 % below 150 Hz and only 2 to 5 % above 5 kHz for most of the track, so the 0.19 s onsets may be tonal low thumps, not hi-hats. Does your onset-by-band analysis show a separate kick/snare backbeat inside the sixteenth pulse, and does the pattern change at 0:32, 2:00 and 2:48?
3. **Form (with feeling):** width and loudness flip together at 0:32, 1:15, 1:27, 1:40, 1:58, 2:13, 2:38 and 2:48. Which of these do you call real section boundaries, and does the abrupt full-band gap at 2:47.8 to 2:48.2 mark the start of a final section, so that the widest and brightest minute is the climax?
