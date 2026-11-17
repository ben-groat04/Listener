# t_dl_mirror: FORM specialist, round 1 (blind, measurements only)

Evidence: all 12 `win_*.md` notes, `audio_features/summary.json` (tempo 95.70 BPM, key D minor 0.69, auto sections), `music_views/` images, and my own runs on `audio/song.wav` and the four demucs stems (`v1/scripts/agents/form_r1_tdl.py`, `_b.py`, `_c.py`; `_d.py` was written but its output was lost, see the last section). Times m:ss. Stem levels are dBFS RMS (my 5 s table, 0.1 s envelopes). Duration 239.44 s (3:59.44).

## 1. Song map (shape: intro, then hook/verse cycle x3, instrumental outro, fade)

Bar = 4 beats at 95.7 BPM = 2.51 s (tracker tempo, `summary.json`; the kick-grid figure is in section 6). Section lengths come out as whole bars, which supports the grid. I name sections by function; "hook" = the shorter, higher-register, sung-sounding section, "verse" = the longer, lower, denser, rapped-sounding one (vocal-stem pitch and level, win_0060, win_0080, win_0180).

| # | Section | Time | Length (bars) | Evidence for the section | Confidence |
|---|---|---|---|---|---|
| 1 | Intro, voiceless | 0:00-0:10.4 | ~4 | vocals stem -74 / -70.5 dB (my 5 s table); drums -18.4, other -26.5, bass gated (-16 dB on, 0:06-0:10.4 out at -55 dB) | high |
| 2 | Hook-like opening / first lift | 0:10.4-0:30 | ~8 | vocal enters +46 dB in one 0.25 s step at 0:10.4 (win_0000); vocal level -19 to -22 dB, lower than the verses' -16; auto section split at 0:15.5 (harmony turn) | medium (function) / high (entry) |
| 3 | Verse 1 | 0:30-1:11 | ~16 | vocal steady -16 to -17 dB; bass gated in blocks | medium-high |
| 4 | Hook 1 | 1:11.3-1:31.4 | ~8 | lead leaps to A4/D5 at 1:11.4 (win_0060); vocal -19 to -22 dB; auto section B 1:11.9-1:32.9; at 1:31.4 pitch drops about ten semitones (win_0080) | high |
| 5 | Verse 2 | 1:31.4-2:12 | ~16 | vocal -16 dB again (1:35-2:10); "other" steps down about 5 dB from 1:32 | high |
| 6 | Hook 2 | 2:14.0-~2:34 | ~8 | vocal returns at 2:14.0 after a gap (win_0120); auto B 2:12.9-2:31.9; vocal -18 to -21 dB through 2:15-2:35 | medium (end point) |
| 7 | Verse 3 | ~2:34-3:15 | ~16 | vocal back to -16 dB by 2:35 (my table); bass long exit 2:38, then 2:42-2:59 bass pulses | medium |
| 8 | Hook 3 (final) | 3:15.09-3:35.3 | ~8 | voice returns at a higher register after a 1.3 s hole; mix rises +11.1 dB at 3:15.09, the largest step in the song (win_0180); vocal -19 to -22 dB; auto B 3:14.5-3:34.8 | high |
| 9 | Instrumental outro (drums + drone bed + bass returning) | 3:35.3-3:49 | ~5 | vocals -51.5 then -74 dB (my 5 s table: voice gone for good at 3:35.3); drums -18.5, other -26 to -29 | high |
| 10 | Dissolve / fade | 3:49-3:56.5 | ~3 | mix -10 to -14 dB until 3:49, -23.9 dB (3:50 slot), -47.1 dB (3:55 slot) | high |
| 11 | Digital silence | 3:56.7-3:59.44 | n/a | exact zero from 3:56.70 (my sample test) | high |

Hooks are each about 20 s (20.1, 20.2 s) and verses 40-41 s; hook start to hook start is about 61-63 s (1:11.3, 2:14.0, 3:15.09: 62.7 s and 61.1 s), roughly 24 bars (16+8), which is a regular, loop-built architecture (INFERRED, medium; the cycle is consistent with DAW arrangement, not proof of it). The first 4-bar intro plus an 8-bar opener means the song begins one hook-length ahead of the cycle.

The window notes disagree on a few edges (hook 2 end and verse 3 start are not marked in any note); I took the 2:34 edge from the vocal level only, so treat it as medium.

## 2. How the energy is engineered (tension and release)

The mix level is almost flat. Mean 5 s mix level sits between -9.5 and -11.3 dBFS from 0:10 to 3:35 (my table), with the drums at -18 to -19.6 dB for the whole of that span. This is not a song that builds by getting louder. Tension and release come from three subtractive devices:

1. **Bass gating (the main device).** The bass stem is the one that comes and goes. From my 0.1 s envelope (>-40 dB, gaps under 0.8 s merged, spans of 2 s or more), bass is on 10.4-36.3, 42.9-46.4, 53.1-56.6, 61.0-66.8, 70.0-97.2, 103.8-107.2, 114.0-117.6, 124.2-127.6, 131.0-158.2, 164.8-168.4, 175.0-178.6, 185.2-188.8, 193.2-219.0 and 225.5-229.1. Inside verses the bass appears as 3.4-3.6 s blocks every 10.2 s (42.9, 53.1; 103.8, 114.0, 124.2; 164.8, 175.0, 185.2), which is four bars (4 x 2.51 = 10.0 s). So in verses the low end plays a bar and a half in every four, a withheld-and-released pattern; in hooks and in the stretches 1:10-1:37, 2:11-2:38 and 3:13-3:39 the bass is continuous. Hooks therefore also feel like "the floor returns". Measured, high. When bass is off it is -55 to -68 dB (about 45-50 dB below its on level), yet the full mix drops only 0-4 dB (win_0060: 1:06.6-1:10.6, mix -10.3 to -12.2), because drums and the "other" bed carry the mix: so bass dropouts are felt as lightening, not as silence.
2. **Vocal register and level.** Verse to hook is a register leap, with the rapped voice at -16 dB and the hook voice 3-6 dB lower but higher in pitch (A4/D5, win_0060). The hook is thus a lift in pitch rather than in loudness. Measured, high.
3. **Short gap-edits before returns.** Before each hook or big return the arrangement thins or stutters: 1:12.15-1:13.1 vocal hole (mix -4.2 to -4.5 dB), 2:12.0 a 0.25 s all-stem dip (mix about -9 dB), 2:13.3-2:13.95 vocal gap (mix -12 dB), 2:23 and 2:35.2 further dips (about -5 dB), and the largest, 3:13.8-3:15.09 (mix down to -22.5 dB at 3:14.75, then +11.1 dB at 3:15.09). Hook 3 is thus engineered as the biggest "return", the only one preceded by a 1.3 s near-void in voice and bass with drums only partly present (win_0180). Measured, high.

**Peak.** The loudest 5 s slots are the first hook region (0:15-0:20 at -9.5 dB) and 2:55 (-9.6 dB), 2:30 (-9.8) and 1:30 (-9.9); all differences are under 2 dB, so the song has no single dynamic peak in level terms. The "peak" is a density peak: final hook (3:15-3:35: bass continuous, voice high, "other" brighter, bed +10 dB in 4-10 kHz at 3:12-3:13). Interpretation (INFERRED, medium): the last hook is the climax because it is the last time voice, bass and drums are all present together and because of the +11 dB return step.

**Release.** After the voice leaves at 3:35.3 the mix actually rises 10 dB for a moment (bass returns, win_0200), then drops: bed dips at 3:36.0 (-9 dB mix), bass exits at 3:38.9 (-9.2 dB), returns at 3:43.0 (+47 dB in the bass stem), a 3:49.0 fade begins (mix -13.3 to -19.3 dB). That is a stepwise thinning, not a gradual fade: the outro is a long release made of bass and bed removals, drums last (win_0220).

## 3. Boundary evidence table (re-measured: stem levels from my 5 s table and 0.1 s spans, plus the window notes' 0.25 s windows)

I re-measured boundary times against my own stem envelopes for the voice and bass (spans above). For drums and "other" I used my 5 s table (drums stay within -18.1 to -19.6 dB until 3:45, other within -23.4 to -30 dB) and the window notes' per-boundary numbers, which I checked for consistency but did not re-derive to 0.25 s. Where I am quoting a window note, it is marked (w).

| Boundary | Drums | Bass | Vocals | Other | Carried by |
|---|---|---|---|---|---|
| 0:10.4 voice in | -25 to -10 hit, broadband crash (w) | -47 to -17 (w) | -65 to -19 (+46 dB) (w); my 5 s: -70.5 to -22.6 | -40 to -18 hit (w) | vocals (largest) with bass; all four move |
| 0:15.5 harmony turn | little (w) | -40 to -15 (w) | sustained | small lift (w) | other/bass (chroma carries it) |
| 0:36-0:43 bass out | flat (-19 to -19.5, my table) | off 36.3-42.9 (my spans) | flat (-16 dB) | flat | bass only |
| 1:11.3 hook entry | slight increase (w) | stabs (w) | leaps to A4/D5, -18 to -26 (w) | +3.7 dB (w) | vocals (register) and other (level) |
| 1:12.15-1:13.1 vocal hole | continues -19.2 (w) | stabs -28.6 (w) | out, -48.9 (w) | continues | vocals only; mix -4.2 to -4.5 dB: dropout, not silence |
| 1:31.4 hook to verse | none (w) | none (w) | +5 dB, pitch down about ten semitones (w) | peak -19.3 then falls (w) | vocals |
| 1:37.0-1:41.4 bass out | flat (-17 to -22.7) (w) | -38.9 then -67 (about -50 dB) (w); my spans: off 97.2-103.8 | continues | already low | bass only |
| 2:12.0 stutter | -26 (from -15) (w) | -26 (from -23) (w) | -28.5 (from -18.8) (w) | -42 (from -30.5) (w) | all stems; mix about -9 dB for 0.25 s |
| 2:14.0 hook 2 | -24 normal (w) | -23 to -13 (w) | -37 then -20 (w) | -27 (w) | vocals |
| 2:38.09 bass long exit | -5.7 (w) | -44 (out) (w); my 5 s: 2:40 bass -21.7, 2:50 -23.0 | +9.3 louder (w) | -3.1 (w) | bass |
| 3:13.8 voice + bass leave | -7.6 (w) | -9.4 then out (w) | -25 (below -45 dB) (w) | flat (w) | vocals with bass; mix to -22.5 dB: not silence |
| 3:15.09 hook 3 | +9.0 (w) | +35.5 (w) | +41 and register jump (w) | +1.9 (w) | vocals, bass, drums together; mix +11.1 dB |
| 3:35.3 voice leaves | +7.4 (w) | +22.2 (w) | -54 to -66 (exit); my 5 s: -22.4 (3:30) to -51.5 (3:35) to -74.4 (3:40) | +2.2 (w) | vocals (loudest layer removed) |
| 3:38.9 bass out | -7.3 (w) | -20 to -65 (w) | none (floor) | -3.5 (w) | bass; mix -9.2 dB |
| 3:49.0 fade starts | -2 (w) | about -32 (w) | none | -6.4 (w) | bass and other; mix -6.0 dB |
| 3:54.5 steep drop | -17 (w) | to -76.9 (w) | none | -4 (w) | drums and bass; mix -16.7 dB |

No "silence" is claimed before 3:56.5: every thinning above keeps drums or bed running; the full-mix floor in 0.1 s steps stays above about -23 dB until the 3:50-3:55 fade (min mix 5 s slot -47 dB at 3:55).

## 4. End of track (10 ms envelope, rule 4)

- Native file: 44.1 kHz stereo, 10 559 488 frames, 239.444 s. Last 10 ms mix frame above -60 dBFS: 3:56.45. Last above -80 dBFS: 3:56.57. Exact digital zero from 3:56.70 (sample test). So the last audible sound is at about 3:56.5, and the final 3.0 s (3:56.70-3:59.44) is digital silence. Measured, high.
- Level at the end: -57.0 dBFS at 3:56.44, -60.4 at 3:56.48, -66.8 at 3:56.51, then zero.
- Final hits: the 10 ms envelope between 3:55.5 and 3:56.5 is a decaying cluster, -37 dBFS at 3:55.68 falling to -57 dBFS at 3:56.44, with local maxima every 0.03-0.15 s. A coarse peak-pick (as in win_0220: six peaks at about 0.10 s spacing, -43.6 to -57.1 dBFS at 3:55.95-3:56.44) gives six; a 1.5 dB prominence pick gives about ten. I therefore say "a small cluster of about six sub-hits decaying over about 0.8 s", not a precise count. Medium.
- Stems, max 10 ms level over 3:55.5-3:57.0: drums -42.2, bass -48.3, other -58.8 dBFS; vocals -78 (stem noise floor). Drums last (-83 dB at 3:56.55 tail), bass and other below -78 dB. High for ordering, medium for tails (separation noise floor about -78 dB).
- Shape: the track ends by a 7 s dissolve (-10 dB at 3:49 to -47 dB at 3:55) and then a stop. The drop 3:54.5 to the stop is a cut at low level, not a ringing tail. INFERRED, medium: the final drop is an edit or fade-out in the master (a fade-out would be smooth; a cluster of local maxima points to the last drum/bass notes dying out under it).

## 5. Dynamics and loudness figures

- Native sample peak 0.0 dBFS (exactly full scale), mix RMS -10.75 dBFS, so crest about 10.7 dB; stereo channel correlation 0.9988 (near mono). Peak at 0 dBFS with RMS about -11 dB reads as modern mastering with a limiter (INFERRED, medium-high; my 22 kHz resampled peak, +3.9 dBFS, is a resampling artefact and is not used).
- The mix stays within about 2 dB for 215 s: a compressed, even-loudness master, so "form" is carried by what is in the mix, not how loud it is.

## 6. Production-era read (rule 1) and sync (rule 5)

- Drum bar-to-bar regularity: a colleague's kick-onset figure of 14.5 ms RMS from a 16th grid at 93.98 BPM (win_0000) is carried here with its tag (INFERRED, medium, not a strong discriminator). My own kick-grid run failed (the band-pass detector picked up hat and snare bleed, giving 1399 onsets and a non-meaningful 646 BPM figure) and I do not use it. Tracker tempo 95.70 vs colleague 93.98 BPM is a mismatch I cannot settle here; I used 95.70 only for bar lengths, and with 93.98 BPM the bar would be 2.55 s, which changes the section bar counts by under 2 %.
- Chroma of the "other" stem repeats strongly at bar lags (mean frame correlation 0.716 at 2.51 s, 0.714 at 5.0 s, 0.77 at 10.0 s): a loop-like harmonic bed. The drum onset-envelope bar-to-bar correlation came out at only 0.08 (unreliable method, onset envelope too noisy), so no drum-loop claim from me.
- Verdict: modern, limiter-mastered production on a looped, regularly arranged bed (INFERRED, medium). I cannot show an older band-limited layer from form alone.
- No cut/beat sync statistic is claimed in this note.

## 7. What a listener feels along the map (metaphor labelled where used)

Intro: a drum-led, voiceless 10 s with a stabbing, gated bass is expectation without payoff; the +46 dB vocal entry at 0:10.4 is the first and sharpest release in the song. Verses 1-2-3 feel like a steady lean, with the bass held back for 6.7 s of every 10.2 s, so the floor keeps being denied and handed back. Each hook lifts in pitch while the floor stays down, and each return is stitched with a short stutter (2:12.0, 2:23, 2:35.2). The final hook is the single hardest arrival; the outro then takes the layers away one at a time, voice first, bass next, bed, drums, so the finish feels like a controlled unwinding rather than an ending with a final chord. Feeling claims are INFERRED (medium) from the engineered structure.

## 8. Not recoverable by measurement

- Lyrics' meaning and which sections a human would call "verse" or "chorus": the stems give register, level and pitch only; my hook/verse labels are functional.
- The exact bar count (tempo 95.70 vs 93.98 BPM disagree) and whether the song was written to a grid of 4/8/16 bars: only a score or project file could say.
- Whether the end is a manual fade, a mastering fade or an edit.
- Instrument identity of the drone bed, and whether it is sampled from older material.
- Whether the 3:13.8-3:15.09 void and the 2:12.0 stutters are performed gestures or DAW edits.
- The disk filled during this run, so the kick-grid and tempo-drift results were not obtained.

## 9. Questions for fellow specialists

1. **Rhythm**: Is the true tempo 95.70 BPM (tracker) or 93.98 BPM (win_0000 kick grid), and does the kick IOI stay on one grid through the 0.25 s stutters at 2:12.0, 2:23 and 2:35.2, or does the grid slip after them?
2. **Harmony**: Do the Gm-G-F side-steps (3:18.7-3:20 and 3:28.4) and the 0:15.5 chord turn sit at section boundaries, or only inside them? Does the hook use a different chord loop from the verse?
3. **Voice**: Is the hook voice really sung (the pitch contour A4/D5 against A3-C4 in the verse), and is the final hook's voice the same take as hook 1 and 2, or a different one?
