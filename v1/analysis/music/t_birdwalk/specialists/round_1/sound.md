# t_birdwalk: SOUND specialist, round 1 (sound design and production)

Scope: instrumentation, timbre, distortion, space, stereo image, mix balance, loudness curve, production era. Evidence: all ten `win_*.md` notes (read in full for sections 1, 4, 6, 7, skimmed for the rest), `music_views/window_0040s.png` and `audio_features/overview.png` (opened), `audio/song.wav` (44.1 kHz stereo, 188.15 s) and `stems_raw/htdemucs/song/*.wav`. My own scripts: `v1/scripts/agents/sound_r1_t_birdwalk.py`, `sound_r1b_`, `sound_r1c_`, `sound_r1d_t_birdwalk.py`. Context.md holds no facts for this video, so nothing here depends on outside knowledge. All stem figures are demucs outputs, not the master, and stems leak into each other. Timestamps m:ss.

## 0. Verdict in six lines

1. **One band-limited path.** The whole mix and every stem except bass sit behind a brick-wall low-pass at about 5.75-6 kHz, from first to last second (measured, high). Several window notes quote 10-16 kHz limits; those are wrong, see 4.1.
2. **Modern, bass-led, hip-hop-shaped production.** A near-pure sine-like sub on A1 (about 55 Hz, constant pitch), a bright clap/snare-type hit, a stereo-wide mid-range plucked/sampled layer near 0.9-1 kHz, and a dry, close, rapped/chanted voice. INFERRED, medium-high.
3. **Production era: modern production, no archive layer found.** The band limit applies to everything (including the sub-free stripped passages), so there is no narrow-band layer sitting under a full-range mix. INFERRED, medium. The 6 kHz ceiling is a property of the delivered file, not evidence of old material (INFERRED, medium-low on its cause).
4. **Two loudness plateaus.** Full-band groove sections sit at -12.1 to -13.9 dBFS RMS; stripped sections sit at -18.5 to -18.7 dBFS RMS in four separate passages. Step about 5.5-6.5 dB (measured, high).
5. **Mono centre vs wide sample layer.** Sub and drums are near-mono; the "other" layer is as wide as it is centred (side/mid about 0 dB). The mix width is largely a function of which layers are in (measured, high).
6. **The ending is a fade-out, not a final hit.** Last sound above -60 dBFS at 3:08.03; the file ends at 3:08.15 on a steady -67 to -68 dBFS floor (measured, high).

## 1. Instrumentation (with evidence; identity is INFERRED only)

| Layer | What the measurements show | Reading | Confidence |
|---|---|---|---|
| Voice (vocals stem) | Dense harmonic stripes to about 4 kHz in every `window_*.png` vocal panel (e.g. `window_0040s.png`). Level -17 to -25 dB per stem second, loudest stem in the stripped passages, below the bass stem in the groove. `lead_notes.json`: about G#2-F#3 (104-185 Hz) in the 0:01-0:23 rap register, then C4-D#4 (277-311 Hz) chant 0:25-0:40, per win_0020 | A rapped/chanted voice, close-miked and dry. Fundamentals 100-185 Hz in the low register sit in the adult male speaking range (INFERRED, medium); the C4-D4 chant is a high register. The words "bird walk" are legible in the mix transcript (see voice specialist) | high that it is a human voice; medium on register |
| Sub bass | Bass stem Welch peak 56.5 Hz (1:00-1:40). Harmonic ladder relative to the 55 Hz fundamental: 110 Hz -27 dB, 165 Hz -30 dB, 220 Hz -37 dB (my FFT, `sound_r1c`). Per-note FFT in win_0080/0120/0140/0160/0180 gives 52.5-56.5 Hz, i.e. one pitch (A1) on every note. Notes decay fast (about 0.27 s to -20 dB at 1:40) | A programmed, synthesised sub (808-style sine/low-harmonic tone), not a played bass guitar: constant pitch, near-pure sine, fast decay, no visible string-noise or fret harmonics. INFERRED. Mono: bass-stem side/mid -48 to -69 dB in every section where it plays (my measurement) | medium-high |
| Drum hit (the "snap") | Drum stem is broadband vertical bars to the 6 kHz ceiling; centroid of the first 100 ms of each hit 3.6-4.5 kHz (intro 4.0-4.5 kHz, 0:47-0:59 3.9-4.4 kHz, 2:01-2:11 3.6-4.3 kHz; `sound_r1c`). win_0020 found no separable kick in 40-120 Hz at 0:20-0:40. Hit-to-hit waveform correlation (peak of cross-correlation, 250 ms, drum stem): intro 7 hits mean 0.82 (min 0.69); 0:47-0:59 8 hits mean 0.67 (min 0.51); 2:01-2:11 7 hits mean 0.64 (min 0.52) | A clap/snare-type bright snap; the low weight belongs to the sub. The intro hits repeat closely (0.82) which fits one reused sample; later groups correlate less (0.64-0.67), which fits sample plus separation noise or a different layer. Not proven either way. INFERRED | medium on type, low-medium on sample reuse |
| Drum pattern (trap-like) | From 0:12.1, 1:33.4, 2:15 and 2:50.3 dense hits at 0.17-0.2 s spacing (win_0000, win_0080, win_0120, win_0160). 0.197 s is half the 0.395 s tracker beat of 152 BPM | Hi-hat/roll-style subdivision; roll fills of 0.2 s spacing at 0:22.4-0:24.15, 2:22.4-2:23.0 (win_0020, win_0140). Hat versus snare cannot be separated by the stem | medium |
| "Other" layer | Steady horizontal line near 0.9-1 kHz with short repeated stabs (`window_0040s.png`, "other" panel, 0:40-0:47 as dashes at about 900 Hz); broadband vertical stripes aligned to the hit times in 0:47-0:59. Stem side/mid about 0 dB (-1.5 to +1.0 dB across nine test spans; `sound_r1c`), i.e. side energy equal to mid | A plucked, chopped or sampled mid-range line, stereo-wide. Around 900 Hz sits near A5 (880 Hz) so it is probably on the tonic (INFERRED, low). CLAP labels (banjo, bells, brass, synth, "country") change window to window and are noise-level evidence; I do not use them | identity not recoverable; role medium |
| Edits/stutters | Whole-mix gaps of 0.08-0.11 s at 2:48.6, 3:00.2 (win_0160, win_0180): all four stems fall together by 25-30 dB within 10-30 ms and resume with a full-band hit | Sequenced gate or stutter edits, a modern DAW device. INFERRED, medium | medium |

## 2. Timbre and space

- **Brightness.** Dark. Mix spectral centroid 0.95-1.65 kHz per 5-10 s slice (win_0080, win_0100, win_0140), 95 % roll-off 0.2-2.3 kHz per 10 s (my Welch, section 4.1), 78-80 % of energy under 150 Hz in the groove sections, 0.0 % above 8 kHz. Stripped passages are mid-forward: 0:47-0:58 has 0.1 % below 60 Hz, 55 % in 200-800 Hz (win_0040).
- **Distortion.** No THD was measured by anyone. What can be said: only 223 samples are at or above 0.999 in the whole file (0.0017 % of samples), so the file is not flat-topped. Sample peak 1.000 at 0:19.83; 4x-oversampled true peak +0.10 dBFS (inter-sample overshoot, my `sound_r1`). Bass harmonics are 27 dB or more below the fundamental, so the sub is clean rather than saturated (high for that figure; whether it was saturated before the file's low-pass is not recoverable).
- **Space.** The voice and drum hits look dry in every window: gaps between syllables go dark, and cuts fall 20-30 dB inside 10-30 ms with no tail (win_0160, win_0180, win_0020). No decay time was measured on the voice by me or anyone; I state "dry, close, no visible tail" at medium confidence and make no reverb-time claim. The stereo width comes from the wide "other" layer and from stem leakage, not from reverb.
- **Stereo image.** Mix side/mid -12.2 dB overall (L/R correlation 0.886). Per section (win notes, measured): intro 0.4-0.6 width index; 0:24-0:46 nearly mono (0.04-0.10); stripped 0:47-0:58 0.37-0.71; 1:23-1:33 0.00-0.05 (the "other" layer is gated out); 2:24-2:35 side/mid -5.1 dB; finale -15.7 dB. By stem (my measurement, side/mid dB): other about 0 dB in all sections except 1:25-1:32 (-13); bass -48 to -69 dB where it plays; drums -14 to -28 dB; vocals either -5 to -7 dB (wide) or -43 to -44 dB (mono). The vocal stem is wide in the intro, 0:13-0:23, 0:48-0:58, 1:02-1:12, 2:00-2:10 and 2:25-2:35, and mono in 0:25-0:40 and 1:25-1:32. That tracks where the wide "other" layer is present, so the vocal-stem width is probably demucs leakage of the wide layer, not a stereo vocal effect (INFERRED, low-medium); the voice specialist should check it, see question 2.

## 3. Mix balance and loudness curve

1 s per-stem levels from `per_second_levels.json` as quoted in the window notes, plus my section RMS of the mono mix (`sound_r1c`):

| Section (auto A-E labels from `audio_features/overview.png`) | Mix RMS dBFS | Peak | What carries the balance |
|---|---|---|---|
| 0:01-0:11.9 intro | -18.7 | -0.6 | Voice about -18 to -25 dB; one drum hit per bar; no bass (bass stem -70 dB) |
| 0:13-0:47 groove | -12.1 | 0.0 | Bass -13 to -15 dB is the loudest stem; voice -14 to -21; drums -24 to -34; other -29 to -41 |
| 0:48-0:58 stripped | -18.6 | -0.6 | Bass absent; voice and "other" lead; one hit per bar |
| 1:00-1:58.7 groove | -12.8 | 0.0 | Bass steady -13 to -16 dB; drums continuous, loudest at 1:33-1:51 (-14 to -21 dB per second) |
| 2:00-2:11.3 sparse | -18.5 | 0.0 | Bass out; voice and stabs; one hit per bar |
| 2:11.4-2:23.3 groove | -12.8 | -0.4 | Bass back at A1 |
| 2:24-2:35.6 stop | -18.7 | -0.6 | Bass and drums out; voice continues |
| 2:35.7-3:01.4 finale groove | -13.9 | 0.0 | Bass -13 to -26 dB; drums -16 to -38; the voice is absent 2:47.3-2:56.4 |
| 3:01.5-3:08.15 fade | falls to -62 dBFS | -2.05 | See section 5 |

Whole file: RMS -13.8 dBFS, crest 13.8 dB (my measurement; `summary.json` quotes -13.5 and 13.5, consistent). The key figure for the curve is the **two-state loudness**: every stripped passage is -18.5 to -18.7 dBFS (four independent passages within 0.2 dB), every groove passage -12.1 to -13.9. A real rhythm-section return is therefore worth +5.0 to +5.8 dB at the mix (table in section 6), not more, because the voice and "other" layer are already loud in the stripped state. The mix level barely changes when a single stem comes or goes inside the groove (1:10.5, 1:41.3, 1:46.0, 2:15.0, 2:47.3 all within +-2.2 dB).

## 4. Production-era judgement (rule 1)

### 4.1 The band limit (corrects the window notes)

Measured on the full mix (Welch, 8192 points, mono mean): PSD is flat at -65 to -69 dB/Hz from 3 to 5.5 kHz, -76.6 at 5.75 kHz, -96.5 at 6.0 kHz, -103 at 6.25 kHz, -108 at 6.5 kHz, -111 at 7 kHz, -127 at 10 kHz, -135 at 16 kHz. So the edge is a steep drop of about 30 dB between 5.5 and 6.0 kHz and about 45 dB by 6.5 kHz; this is a brick-wall low-pass at about 5.75 kHz with essentially nothing above it. Per 10 s slice the share above 6 kHz is -55 to -65 dB relative to the total and above 10 kHz -72 to -75 dB, in every one of the 19 slices. Per stem: vocals PSD -71 dB at 5 kHz and -110 at 6 kHz; drums -71 to -97; other -83 to -114; bass is sub-only. `window_0040s.png` shows the black band above about 6-7 kHz in the mix and in every stem panel. win_0000 and win_0020 got this right (about 6 kHz); win_0080, win_0100 and win_0120 describe 10-16 kHz limits and win_0140 "7-8 kHz", which read the faint -110 to -127 dB residue, not the audible edge. Use 6 kHz.

A cut at about 5.75-6 kHz is what a source at a 12 kHz sample rate (Nyquist 6 kHz) would give after resampling to 44.1 kHz, or a very low-bitrate or deliberately low-pass chain. I cannot tell which from the measurements (INFERRED, medium-low on cause; the existence of the cut is measured, high).

### 4.2 The four measured cues

| Cue | Figure | What it says |
|---|---|---|
| Peak versus 0 dBFS | Sample peak 1.000 (0:19.83), true peak +0.10 dBFS, 223 samples at or above 0.999, crest 13.8 dB, RMS -13.8 dBFS | Peaks touch full scale on isolated transients (the stabs, the hits). With crest 13.8 dB and 0.0017 % of samples near full scale, this is peak-normalised or lightly limited, not a flat-topped "loudness-war" master. Several window notes say "hard limited, loudness-war"; I lower that to "peak-normalised or lightly limited, modern" because crest 13.8 dB is wide for a limited master (INFERRED, medium) |
| Loop regularity | Bass bars 1:00-1:16: log-mel bar correlation 0.78-0.90 (win_0060). Intro hit waveform correlation 0.82; later 0.64-0.67 (mine). Other-stem bars 0.23-0.74; vocals 0.87-0.92 (win_0140). Song-wide bar-chroma correlation 0.88 | Bass repeats closely (programmed pattern, INFERRED medium); drums and "other" do not repeat bar-for-bar. No sample-exact loop was demonstrated: INFERRED, low-medium |
| Hit-onset spread from a strict grid | One-per-bar drum hit, refined onset times (mine): intro IOI 1.487, 1.529, 1.554, 1.577, 1.600, 1.575 s (mean 1.554, SD 37 ms); 0:47-0:59 IOI 1.50-1.60 s (mean 1.556, SD 36 ms); 2:01-2:11 IOI 1.484-1.614 s (SD 50 ms). Kick-band spread: 96 ms around the tracker grid over 407 onsets (`summary.json`); only 3-9 kick-band onsets per window, so most windows cannot support a kick statistic. The 152 BPM bar is 1.579 s, so the IOI is one hit per bar | SD of 36-50 ms is far looser than a quantised DAW grid (which gives onset jitter of a few ms plus detector error of 10-20 ms). The intro IOI also grows monotonically from 1.487 to 1.600 s over six intervals, which no fixed-tempo grid would do. Reads as hand-placed or live-triggered or sampled-from-performance timing, not machine-quantised. INFERRED, medium. This is on the bar grid (4 beats at 152 BPM), which matches the hit IOI, so the statistic is valid |
| Band-limited sample against full-band mix | The mix has no full-band part: everything above 6 kHz is near zero in all stems and all sections, including the stripped passages with no sub | There is no narrow-band layer inside a full-range mix, so no evidence of older source material in the sense of rule 1. The whole file is band-limited. (A narrow-band source with the sub added on top would be indistinguishable here, because the sub is below the cut; so I cannot exclude it, but I cannot support it either) |

### 4.3 Judgement

**Modern production (sub-bass-led, trap/hip-hop-shaped, DAW-style edits and gate stutters), delivered through a 6 kHz band-limited path. No archive or older-recording layer is measurable.** INFERRED. Confidence: medium that it is modern production as opposed to a period-consistent older recording (the sub on A1 with fast decay, the 78 % of energy below 150 Hz and the 0.1-s all-stem stutters are modern-production cues; none is an archive cue); low that the "other" layer is not itself a sample of older material (separation cannot say; it is the only layer that could be, and it carries no separate band-limit signature: it is cut at the same 6 kHz as the voice). I explicitly do not date the recording.

## 5. End of track (rule 4)

Method: 10 ms moving-RMS envelope (441 samples) of the mix and the four demucs stems, last 3 s (`sound_r1b`). Duration 188.1513 s.

- Mix, 0.25 s means from 185.15 s: -27.8, -29.2, -33.9, -37.2, -46.7, -33.4, -38.0, -43.6, -41.2, -45.1, -52.2, -60.4 dBFS. Last time above -40 dBFS 187.31 s; above -50 dBFS 187.69 s; above -60 dBFS 188.03 s; last 0.5 s is a constant -67 to -68 dBFS to the final sample (188.15 s). The last sample is not zero (the last sample above 1e-4, -80 dBFS, is at the very end). So the **time of the last audible sound is about 188.0 s (3:08.0), and the level at the end is -67 to -68 dBFS**; the file stops on a quiet residual rather than digital silence (the clip is cut at the end, not faded to zero; win_0180 saw the same, "-62 dB at 3:08.0").
- Final hits: there is none. Envelope peaks with 3 dB prominence in the last 3 s are 185.23 s (-22.0 dBFS), 186.02 (-31.9), 186.34 (-56.5), 186.48 (-29.1), 186.55 (-32.2), 187.23 (-36.6), 187.40 (-40.7), 187.62 (-44.6): eight peaks, each lower than the one before (apart from 186.48), which is the fading drum stem (drum-stem peaks at 185.23 and 185.34, -22 and -26 dBFS). They are the groove ticking on while the level falls, not a last chord or a stinger.
- Stems at the end: vocals flat at -72.5 dBFS (separation floor, absent); drums -30.4 dB at 185.15, -47.6 at 187.5, -62.8 in the last 0.5 s; bass -43.6, -61.1 in the last 0.5 s; other -54.7 to -69.3. The order of leaving (win_0180): "other" first, then bass, then drums, with the drums the last to fade (drum stem still the loudest stem at 3:03-3:07).
- Stereo width does not change in the fade (side/mid -14.7 to -15.9 dB, win_0180).
- Confidence: high.

## 6. Boundary evidence table (rule 3, all re-measured by me, `sound_r1d`)

Each cell is the stem or mix RMS in dBFS over the 1.0 s before the boundary (with a 0.1 s guard) and over the 1.0 s after, with the change in dB. Stems are demucs outputs.

| Boundary | Drums | Bass | Vocals | Other | Mix | Stem that carries it |
|---|---|---|---|---|---|---|
| 0:00.8 | -42.9 to -54.9 (-12.0) | -72.1 to -71.8 (+0.3) | -72.6 to -23.2 (+49.5) | -27.2 to -28.1 (-0.9) | -27.0 to -21.0 (+6.0) | vocals (voice enters; the lead-in is the "other" layer alone) |
| 0:12.1 | -32.1 to -21.4 (+10.8) | -69.4 to -18.6 (+50.8) | -19.6 to -19.8 (-0.2) | -32.1 to -38.1 (-6.0) | -18.1 to -12.9 (+5.1) | bass, with drums |
| 0:23.9 | -25.3 to -34.7 (-9.4) | -13.6 to -13.5 (+0.1) | -18.1 to -18.5 (-0.4; lead jumps about 1.5 octaves) | -32.9 to -37.0 (-4.1) | -11.5 to -12.0 (-0.6) | vocals (pitch) and drums (roll ends); the mix does not move; width drops 0.24 to 0.07 |
| 0:46.9 | -32.9 to -29.3 (+3.6) | -12.3 to -29.8 (-17.5; then -72) | -19.5 to -20.5 (-0.9) | -34.1 to -45.2 (-11.1) | -11.3 to -18.7 (-7.5) | bass (out) and "other" thinning together; rhythm-section dropout, not silence |
| 0:59.4 | -31.0 to -25.0 (+6.0) | -70.7 to -18.0 (+52.7) | -19.7 to -22.5 (-2.8) | -29.8 to -36.4 (-6.7) | -18.1 to -14.7 (+3.4; +5.8 by 1:00) | bass |
| 1:10.5 | -28.4 to -27.0 (+1.3) | -13.0 to -12.8 (+0.2) | -17.5 to -22.4 (-4.9) | -32.7 to -26.7 (+6.0) | -11.1 to -11.2 (-0.1) | "other" (level and texture) with a vocal register jump; mix does not move |
| 1:23.0 | -25.3 to -30.0 (-4.7) | -12.5 to -15.9 (-3.4) | -22.1 to -23.5 (-1.4) | -27.7 to -59.1 (-31.4) | -11.4 to -14.9 (-3.5) | "other" (gated out); mix width collapses to mono |
| 1:33.1 | -38.8 to -25.7 (+13.1) | -14.7 to -15.8 (-1.1) | -21.6 to -21.0 (+0.6) | -58.7 to -33.8 (+24.9) | -13.7 to -13.2 (+0.5) | "other" returns, then drums go dense at 1:33.4 |
| 1:41.3 | -16.2 to -15.5 (+0.7) | -27.5 to -41.5 (-14.0; floor by 1:41.5) | -22.6 to -21.4 (+1.2) | -28.3 to -27.1 (+1.2) | -13.2 to -13.2 (-0.1) | bass only; the mix does not move |
| 1:46.0 | -15.3 to -14.7 (+0.6) | -35.3 to -20.7 (+14.6) | -22.6 to -20.7 (+1.9) | -28.6 to -26.0 (+2.6) | -13.3 to -11.1 (+2.2) | bass (returns) |
| 1:58.7 | -22.5 to -33.2 (-10.8) | -14.7 to -21.0 (-6.2) | -17.1 to -19.7 (-2.6) | -29.8 to -45.8 (-16.0) | -10.9 to -16.8 (-5.9; -19.5 within 1 s, 10 ms floor -31) | drums and bass together, "other" falls too; rhythm-section dropout, not silence |
| 2:11.4 | -30.8 to -28.5 (+2.3) | -68.2 to -14.7 (+53.5) | -20.4 to -24.4 (-4.0) | -30.7 to -30.4 (+0.3) | -18.7 to -13.7 (+5.0) | bass |
| 2:15.0 | -61.7 to -23.5 (+38.2) | -14.7 to -17.0 (-2.3) | -18.2 to -18.7 (-0.5) | -37.8 to -36.2 (+1.7) | -12.8 to -12.9 (-0.2) | drums (pattern changes; the 1 s "before" value is a gap second) |
| 2:23.4 | -33.6 to -56.8 (-23.1) | -12.3 to -74.2 (-62.0) | -19.9 to -21.2 (-1.2) | -27.9 to -46.8 (-18.9) | -10.9 to -20.4 (-9.5) | bass and drums (and the stab layer weakens); voice continues: a rhythm-section dropout; no silence in the mix |
| 2:35.7 | -68.1 to -27.6 (+40.5) | -72.4 to -14.6 (+57.8) | -19.1 to -22.6 (-3.5) | -31.3 to -32.5 (-1.2) | -18.1 to -13.4 (+4.6) | bass first (2:35.7), drums 0.7 s later (2:36.41) |
| 2:47.3 | -24.4 to -27.5 (-3.1) | -13.7 to -13.7 (-0.1) | -20.5 to -47.4 (-26.9; -70 by 2:49) | -28.2 to -28.3 (-0.1) | -11.8 to -13.1 (-1.3) | vocals (leave); mix hardly moves |
| 2:50.3 | -23.7 to -22.0 (+1.7; 10 ms: -64.9 to -16.8 at the hit) | -15.2 to -19.2 (-4.0) | -69.7 to -71.2 (-1.5) | -29.2 to -31.2 (-1.9) | -14.1 to -15.0 (-0.9) | drums (dense pattern launches after a 0.1 s all-stem stutter) |
| 2:56.5 | -20.6 to -20.0 (+0.6) | -19.6 to -18.6 (+1.0) | -70.5 to -35.7 (+34.9; sweep in) | -32.2 to -27.9 (+4.4) | -15.7 to -14.0 (+1.7) | vocals |
| 3:01.5 | -27.2 to -24.5 (+2.7) | -15.5 to -23.2 (-7.7) | -68.0 to -71.6 (-3.7) | -26.4 to -32.3 (-5.9) | -13.4 to -18.3 (-4.8) | bass and "other" (start of the fade) |

Reading: no boundary is a silence of the whole mix. The deepest mix drops are 2:23.4 (-9.5 dB across 1 s means) and 0:46.9 (-7.5 dB), both rhythm-section dropouts: voice and "other" continue, mix stays above -20.7 dBFS (per-second figures). The boundaries carried by bass alone (0:12.1, 0:59.4, 2:11.4, 2:35.7, 1:41.3, 1:46.0) show bass stems moving 14-58 dB while the mix moves 5.0-5.8 dB at a full return and 0 to 2.2 dB at the partial ones. Boundaries carried by "other" or voice alone (1:10.5, 1:23.0, 1:33.1, 2:47.3) leave the mix within 3.5 dB.

## 7. What the sound does to a listener (INFERRED; feeling is the feeling specialist's call)

- Weight: 78-80 % of energy below 150 Hz and a constant-pitch A1 sub make the groove sections physically heavy rather than bright; the 6 kHz ceiling removes cymbal and consonant air, so the sound is dull-edged, close and dense (measured cause; the felt effect is INFERRED).
- Section contrast comes from subtraction: each stripped passage (0:47, 2:00, 2:24) removes the mono sub and drums and lets the wide, mid-range "other" layer and the voice stand alone, 5.5-6 dB quieter. The returns at 2:11.4 and 2:35.7 are 5.0 and 4.6 dB louder than the passage they follow and the bass moves 54-58 dB; that is the loudest "event" the production has.
- Dry voice, no reverb tail, hard gate cuts: nothing blurs the words; gaps are abrupt (2:48.6, 3:00.2).

## 8. Questions for fellow specialists

1. **To rhythm:** The one-per-bar snap in the intro has IOIs 1.487, 1.529, 1.554, 1.577, 1.600, 1.575 s (SD 37 ms, rising monotonically over the first five) against a 1.579 s bar at 152 BPM. Is the intro really slowing by about 7 %, or is the hit placed by feel, and does the 1.44 s spacing of win_0020 (0:27-0:42) mean a different half-time grid (about 83 BPM) rather than a tempo change?
2. **To voice:** The vocal stem is wide (side/mid -5 to -7 dB) in the intro, 0:48-0:58, 2:00-2:10 and 2:25-2:35 and mono (-43 dB) in 0:25-0:40 and 1:25-1:32, exactly where the wide "other" layer is in or out. Can you tell from the vocal stem's phase and the words whether the voice is double-tracked or stereo-effected in the stripped sections, or is this stem leakage?
3. **To harmony:** The sub holds one pitch (A1, 52.5-56.5 Hz on every note I and the window notes measured) and the "other" line sits near 0.9 kHz (about A5). The chord labeller invents F, F#m, Gm and D (win_0020, win_0000). Is there any real harmonic motion above the A pedal, or is the colour only the voice's passing notes and the G row that lights at the stops (1:58-1:59.5, 2:23, 2:35)?

## Not recoverable by measurement

- **Exact instruments** (808 versus synth sub, clap versus snare, the plucked "other" line): demucs gives spectra, not sources; CLAP labels are inconsistent.
- **Real source of the "other" layer** (sampled older recording, library loop, played instrument): it is cut at the same 6 kHz as everything else, so no separate source signature exists in these data.
- **Cause of the 6 kHz ceiling** (12 kHz-rate source, codec, creative filter): the shape of the edge is measured, the reason is not.
- **Recording or release date, performer, intent**: no tags or credits in the data; the measurements do not date a recording.
- **Reverb, compression and distortion settings**: only dry-versus-wet appearance and level figures were measured; no decay time, no THD, no gain-reduction measurement.
- **Whether the groove was quantised in the DAW**: the 36-50 ms hit spread rules out a strict grid for the hits I measured, but it cannot show whether the beats were performed, sample-triggered by hand or deliberately off-grid.
- **True loudness in LUFS**: I measured unweighted RMS, not K-weighted loudness, so no LUFS figure is given.
