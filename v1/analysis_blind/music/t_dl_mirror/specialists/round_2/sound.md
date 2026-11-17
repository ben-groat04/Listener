# t_dl_mirror: SOUND specialist, round 2 (blind, measurements only)

Read: all seven round-1 files (feeling, form, harmony, lineage, rhythm, sound, voice). New measurements in `v1/scripts/agents/sound_r2_tdl.py`, `sound_r2_b.py` to `sound_r2_g.py` (run on `audio/song.wav` and `stems_raw/htdemucs/song/*.wav`). I looked at no new images; I rely on round 1's `window_0100s.png`. Times m:ss. Tags: measured, INFERRED, speculative; high/medium/low. Stems are demucs estimates of a clipped, limited mix, so they cannot show pre-limiter levels.

One note on honesty: ffprobe printed the file's container title tag when I checked the sample format. I did not use it, and nothing below depends on it.

## 0. What changed since round 1

1. The bed's pitch classes (D, A, F#, C, E) are exactly the first harmonics of one tone near D3. That explains two things harmony found and weighed as colleagues' evidence (section 3). It matters for the minor/major question.
2. The 8 kHz wall is sharper and deeper than I said: about 79 dB down, with a transition under 100 Hz wide (section 5).
3. The kick is a pitch-falling sub thump, which answers rhythm's "double rise" question (section 2).
4. The 2:57.4 clipped run is an 80 ms drum-stem burst followed by a 20 ms near-total mute of the whole mix. That is an edit-like event, and the strongest modern-production cue I have beyond the limiter (section 4).
5. I withdraw my round-1 "loose clock, human-played" lean for the kick (section 7).

## 1. Answers to questions put to me

**Rhythm Q2: is the kick's double rise a second hit, a separation artefact, or a sample's room tail? Vinyl-era sample or modern machine?**
Measured (`sound_r2_b.py`, `sound_r2_e.py`). Using a Hilbert envelope of the 35-130 Hz band, 661 of 736 kicks in the drums stem (90 %) show a second envelope rise at a median 47 ms later (p10 37 ms, p90 167 ms), with a dip of median -12 dB between. The same is present in the full mix (854 of 908, median 52 ms), so it is not a demucs artefact. Caution: my round-1 2 ms RMS envelope gave similar numbers but was an artefact of the 70 Hz period (ripple), so I discarded it and use the Hilbert version.
Pitch tracking on the 47 kicks that have no other kick within 300 ms: the dominant frequency starts near 65 Hz (0-10 ms), falls to about 54 Hz at 40 ms, and about 38-43 Hz from 60 ms to 140 ms. The level holds within 10 dB of its peak to about 110 ms and falls 27 dB by 140 ms. So the "0.11 s" rhythm saw is the length of one kick body, and the thump is a falling-pitch sub tone (about 65 to 40 Hz), not a clean two-strike double. The second rise appears in the 35-60 Hz band (19 of 47) and 90-130 Hz band (35 of 47) but almost never in 60-90 Hz (2 of 47), which a simple sweep would not predict; I cannot say whether it is a second layer (click plus tone), beating between two components, or a sweep passing band edges. INFERRED, low-medium: one kick sound with a sustained falling-pitch body; not two separate hits. Whole-file kick-band dominant frequency median 57 Hz (p10 27, p90 188; spread includes non-kick events).
Vinyl-era versus machine: not decidable. Drum-stem energy by band (30-8000 Hz, power re total): 30-100 Hz -1.5 dB, 100-300 -10.2, 300-1k -15.3, 1-3k -17.1, 3-6k -11.7, 6-8k -12.3. That is bass-dominant with a lot of 3-8 kHz hat energy, flat to the 8 kHz wall. A drum break from an old record would usually fade in the top octave before a wall; here the hats and noise-like energy run flat to the wall (see section 5), so the drums as heard through the chain are full-range up to 8 kHz. That fits a machine or a recent sample, but a clean sample passed through an 8 kHz chain would look the same. Not recoverable.

**Harmony Q3: is there an older, noisy, band-limited layer under the drone? Does a mono bed sit under a wider master?**
No on both, measured.
- Wider master: there is none. Whole file is dual-mono (round 1, 0.08 % of samples differ); the bed is not a mono layer under a wide master but part of an all-mono file.
- Noisy or crackly layer: in the fade (3:53-3:55.5) the other stem shows discrete partials (148, 296, 395, 444, 592, 740, 888, 1036, 1187 Hz) and the 5-7.5 kHz band sits 37 dB under the 100-1000 Hz band (-114 vs -77 dB, Welch). There is no hiss or crackle floor under the bed when everything else has gone. An archive-noise layer would show there (INFERRED, medium; negative evidence, since demucs can remove noise from the "other" stem). The CLAP "vinyl crackle" label stays rejected (lineage agrees).
- The extra peak at 395 Hz is within 1 cent of G4 at the same +14-cent offset as the bed (392.0 Hz x 1.0081 = 395.2 Hz). It is not on the 148 Hz series. Whether it is bleed, a G in the drone or voice residue, I cannot say (low); harmony may know whether a G sounds under the fade.

**Feeling / voice Q: is the 2:57.4 clipped 73 ms run a drum hit or a bass-plus-drum collision?** (`sound_r2_c.py`, 10 ms envelopes, section 4 table.) A drum-stem event: the drums stem jumps from about -22 to -27 dB up to -5 dB (about +17 to +20 dB) and stays flat at -5 to -7 dB for 8 frames (2:57.44-2:57.52). The bass does not join it: the bass stem falls from -11 dB to -20, -26, -28, -36, -38, -40, -43, -45 dB over the same 80 ms. So bass leaves as the hit arrives: not a collision (INFERRED, medium; a separation could mis-assign, but the mix is at 0 dBFS across the whole run, so something broadband is at full scale). The clipped samples are 3,354 in 2:57.4398-2:57.5196 (80 ms, left channel, at or above 0.999); round 1's "3,200 samples, about 73 ms" was an under-count at a stricter threshold.

**Voice Q: is the voice processed (compression, double-tracking)?** Partly answerable. The vocal-stem crest factor (50 ms frames, whole stem) is 14.6-15.2 dB in verses 1-2 and 18.2-20.4 dB in hooks 1-3. In the verses the voice is active (above -35 dB) in 92 % of 50 ms frames; in the hooks only 72-78 %, so the hook's phrases are gated or cut, and the higher crest comes from gaps and short notes, not from less compression. The level spread of active frames (p10 to p90) is 16-17 dB in verses and 13-14 dB in hooks. Evidence is consistent with a heavily limited, dry, close vocal in both parts. Double-tracking, pitch correction and compression ratio cannot be separated from the limiter on a mono, 8 kHz file. Dryness holds: gaps in the vocal stem go black within 0.25-0.5 s (round 1).

**Lineage Q2: is there any measurement that separates a 16 kHz-sampled origin from a low-pass added at mastering?** Partly (section 5). I could not find image or aliasing leakage that would tell them apart; I can bound the filter.

## 2. Instrumentation and timbre: additions

- **Drums**: see section 1. Kick: falling sub tone, 65 to about 40 Hz, body about 110-140 ms, fall -20 dB at a median 140 ms in the drums stem (lineage measured 0.18 s; both are short for the long boom of a typical sub-bass kick, which agrees with lineage's "not a long 808 boom", medium).
- **Bed** (`sound_r2_g.py`): fundamental measured at 147.9 Hz (partials 2, 4, 8 give 148.2, 147.8, 148.3 Hz), which is +12 to +14 cents against D3 = 146.83 Hz. That agrees with lineage's +14 cents from `estimate_tuning` (A about 443.6 Hz); it is not new evidence for a cause (speculative, low: sped-up sample, detuned synth or loose tuning). Partial levels relative to partial 1, in three stretches (0:36-0:46, 1:40-2:00, 3:40-3:48):
  2 (D): +5 to +6 dB; **3 (A): +12 to +16**; 4 (D): +4 to +9; **5 (F#): -5 to -10**; 6 (A): +4 to +6; **7 (C, about 30 cents flat of equal-tempered C): +7 to +9**; 8 (D): 0 to -4; 9 (E): -8 to -12; 10 (F#): -15 to -20; 11: -8 to -15; 12 (A): -19 to -20.
  So the strongest component is the 3rd partial (A near 444 Hz), not the fundamental; the spectral envelope peaks around 440-1000 Hz, which is why the bed is "mid-range" with centroid 0.9 kHz (round 1). Even and odd partials are both present. That is a sustained single timbre with a strong mid-range emphasis; the instrument is not recoverable (organ, synth, reed, string sample, all fit).
- **Bass**: unchanged from round 1 (95 % under 221 Hz; stem -16 to -18 dB).
- **Voice**: unchanged (dry, close; forward at -16 to -23 dB).

## 3. Connection to harmony: the third in the bed is mostly the overtone series (INFERRED, medium-high)

Harmony found the bed's chroma has F# (0.24-0.26) stronger than F (0.17-0.19), and C natural (0.37-0.41) a little stronger than C# (0.29-0.33), and read the F#-over-F result as "thirdless drone, the labeller's Dm/D flicker is noise".
My partial table gives a simple reason. A tone on D has its 5th partial on F# (above) and its 7th partial about 30 cents under C. Measured: F# partial at -5 to -10 dB re the fundamental, C partial at +7 to +9 dB. So the chroma "F#" and "C natural" need no chord tone: they are what one sustained D-based timbre gives. F natural has no partial position, so its 0.17-0.19 chroma must come from elsewhere (voice bleed, the side-step chords, hat noise in the "other" stem). Consequences:
- Do not read a major third (F#) or a natural-minor seventh (C) from the bed. Neither is a note; both are timbre. This supports harmony's "thirdless drone" and removes the apparent F#-over-F clue, in agreement with harmony's lean toward the voice for the minor third (F = 17 % of hook time).
- It also weakens harmony's argument for natural minor over Dorian that rests on the C in the bed. The Gm labels (7.7 s Gm vs 5.0 s G) remain the evidence; I do not add to it.
- Tag: INFERRED, medium-high (the arithmetic of the series is exact; whether the real source is one tone or a stack I cannot show).

## 4. Distortion, clipping, edits: the 2:57.4 event and one more

Boundary evidence table (rule 3), 10 ms envelopes (dB), 2:57.40 to 2:57.60, plus the 0:10.6 event for comparison. "Mix" is the full mix.

| Boundary | drums | bass | vocals | other | mix | carried by |
|---|---|---|---|---|---|---|
| 2:57.44 big hit starts | -22 to -27 -> -5 (+17 to +20) | -11 -> -20 -> -45 over 80 ms (leaves) | -26, flat (-26 to -30) | -25 -> -24 (flat) | -8 -> -1 -> 0 dBFS; clipped run 2:57.44-2:57.52 (3,354 samples) | drums stem; bass leaves as it arrives |
| 2:57.52-2:57.56 mute | -5 -> -24, -30, -46, -45, then -31, -16 | -45 -> -54 to -56, back to -13 at 2:57.56 | -28 -> -44 to -52, back to -38 | -24 -> -34 to -41, back to -28 | 0 -> -18, -24, -75, -94 dB, then -12 at 2:57.56 | all four stems and the mix together: a full-mix mute |
| 0:10.6 (voice, bass, crash enter) | -17 -> -14.5 (round 1) | -52.8 -> -20.2 (round 1) | -67.1 -> -23.0 (round 1) | -28.6 -> -22.0 (round 1) | one 10 ms frame at -67 dB at 0:10.62-0:10.63, then clipped runs 0:10.66-0:10.68 | the mix itself |

The mix has only six clusters of 10 ms frames below -40 dBFS between 0:05 and 3:48 (`sound_r2_f.py`): 7.84-7.87 s (-43), 8.14-8.16 (-41), 10.62-10.63 (-67), 177.54-177.56 (-94), 220.96-220.99 (-46), 226.35-226.39 (-42). Two are deep: 0:10.62 (-67 dB, 10 ms) and 2:57.54-2:57.56 (-94 dB, 20 ms). Both sit immediately next to a hard-clipped run. A mix level of -94 dBFS for 20 ms in a track whose 10 ms envelope median is -11.0 dB (p5 -22.4, p95 -6.6) is not what drums, bed and bass produce; it is a sample-accurate mute or a cut (INFERRED, medium-high: an edit, gate or a clipper/limiter reset; I cannot tell which). This is the strongest evidence beyond the limiter that the file was assembled or finished in a DAW-style environment. Interpretation for the feeling specialist: the "dropout" gestures at 2:57.5 and 0:10.6 are not tape-era breath-drops (metaphor); they are hard digital edges, felt as a jolt.
The other vocal and bass dropouts (1:12.15, 2:13.3, 3:13.8, 3:34.2 and so on) do not mute the mix: drums and bed continue and the mix falls only 3-12 dB (round 1 and rhythm tables). Not silence.
Clipping elsewhere remains as in round 1: 21,079 samples at or above 0.999, 542 runs, concentrated at 0:10-0:20 and 2:55-3:00. Hook 3 is not louder than the other hooks (10 s mix RMS -10.1 to -10.7 dBFS in 3:15-3:35, round 1 blocks), so the "largest step" form found at 3:15.09 (+11.1 dB) is a recovery from the hole at 3:13.8-3:15.09 (mix -22.5 dB) to the ceiling, not a new level. The limiter leaves no headroom for a final-hook lift: the climax is built by density and register, not by loudness (agrees with form, measured).

## 5. Bandwidth: the 8 kHz wall in more detail (measured, high; cause INFERRED, low-medium)

- Edge position and slope (median Welch, 16,384-point, 2.7 Hz bins): flat at about -62 dB from 7.0 to 7.975 kHz, -65 at 8.0, -71 at 8.025, -73 at 8.05, then -82 to -100 dB by 8.075-8.2 kHz. The step centre is near 8.03 kHz and the transition is under about 100 Hz wide. There is no roll-off below the wall: content is full to the edge.
- Depth: the per-second energy above 9.5 kHz is a median -78.6 dB (p10 -82.7, p90 -74.9) against the 0.1-8 kHz band (STFT, `sound_r2_c.py`). That is the same in seconds with zero clipped samples (-78.6) and in clipped seconds (-75.7), so it is not mainly clip splatter, and not a high-contrast anomaly either. It sits about 8 dB above pure 16-bit rounding noise (absolute STFT frame power -96 vs -105 dB), so it is a low floor of unknown origin (limiter, rounding without a clean dither, or the encode).
- Image test: I correlated the log spectrum above the wall (8.3-12 kHz) with its mirror about 8 kHz (4-7.7 kHz): median frame correlation -0.02 (p90 0.24, 1,016 frames); the control mirror about 10 kHz is -0.39 (tilt, not images). So there are no visible resampling images leaking past the wall, and no way to read the origin from them.
- Reading: a steep stop-band of about 79 dB placed at 8.03 kHz, i.e. at the Nyquist frequency of 16 kHz sampling within a few tens of Hz, is what a good sample-rate converter or sinc filter gives. A cheap analogue band-limit or a typical low-bitrate encoder low-pass would be more likely to sit away from exactly 8 kHz and to leave spectral holes below it (not tested for holes). INFERRED, low-medium: the file passed through a 16 kHz-sampled stage (source or delivery), then was upsampled to 44.1 kHz. It cannot say whether that stage was the original source or a later copy, nor whether the source was a lo-fi recording or a modern track downsampled. The one thing it does say: no layer is older or more band-limited than another (all stems stop at the same frequency).
- Answer to lineage: no measurement I can make separates a 16 kHz source from a mastering low-pass; the exact 8 kHz position favours a sample-rate stage over an arbitrary filter, at low-medium confidence only.

## 6. Loudness curve and end of track (carried, with cross-check)

Round-1 figures carried unchanged, tags kept: 10 s mix RMS -10.0 to -10.9 dBFS from 0:10 to 3:40 (first block -11.9), sample peak 0.0 dBFS in every block to 3:50; 3:40-3:50 -13.2, 3:50-4:00 -26.6 (the fade). New in this round: the 10 ms envelope over 0:10-3:30 has median -11.0, p5 -22.4, p95 -6.6.
End of track (rule 4), from my round-1 10 ms envelope of the last 3 s of the mix and each stem: last audible sound 3:56.45 (10 ms mix envelope -60 dBFS); level at the end -57 dB at 3:56.44; last nonzero sample 3:56.70; exact digital zero to 3:59.44. Drums and bass to 3:56.37-3:56.38, the bed to 3:55.65, vocals none. Final hits from the 10 ms envelope peaks: about eleven small peaks (3:56.01 to 3:56.44, -45 to -57 dB) at 3 dB prominence, a decaying run, not a closing hit. Form (about six sub-hits at coarser peak-picking, -37 to -57 dB) and rhythm (no distinct final hit, bumps at -57 to -60 dB) agree on the shape, and differ only in the count, which depends on prominence; I keep "about eleven at 3 dB prominence, six at coarser picking". Not a clean stop: a fade of the bed and gated bass followed by a cut at about -57 dB, then 2.74 s of digital zero.

## 7. Corrections to my own round 1 and to colleagues

1. **Kick spread (rule 1, rule 5).** In round 1 I measured absolute phase on a rigid 16th grid fitted at 93.6-95.8 BPM and found no lock (R = 0.03-0.06; rms 43.6-44.8 ms against 45-46 ms random) and wrote "loose clock, human-played or loosely tempo-mapped". That test is invalid for a grid whose tempo is uncertain by 1 BPM: over a 185 s file a 0.2 BPM error moves the grid by hundreds of ms, which hides lock. Rhythm's inter-onset test (IOI deviation 20.2 ms std on the 16th step of 94.0 BPM, 0.1596 s; cumulative drift fit at 94.0 BPM 78 ms std, bar-lag 93.96-94.01 BPM) is on the kick's own grid, as rule 5 asks, and is the right figure. I withdraw my "loose clock" reading. Even so, a 20 ms IOI spread from a 57 Hz sub kick is not informative about quantisation: low-band onsets from a thump with 10-20 ms rise are hard to place to better than about 10-15 ms (my estimate of detector jitter; I did not measure it separately), so 20 ms is neither "machine-exact" nor "human-loose". Tag: the kick-spread cue is **uninformative (low)**; it does not support or oppose a DAW loop. Rhythm's tag of INFERRED medium for a looped pattern rests on waveform repeats (r up to 0.85 at four bars), which I accept.
2. **Rhythm, 94.0 versus 95.7 BPM.** I used the tracker's 95.7 for fits and for "pulse 0.64 s". I accept rhythm's 94.0 (drift fit, 2.554 s bar lag steady to 0.05 BPM). My round-1 statement of "tempo wanders" followed from the bad test above and is withdrawn.
3. **Form, "mix peak at 3:15.09" and the climax.** Agreed as a density climax; added that loudness cannot rise (section 4).
4. **Round 1 count of the 2:57.4 clipped run** (3,200 samples, 73 ms) was low by a few samples against a looser threshold: 3,354 samples, 80 ms. Minor.
5. **Voice's "voice -50.5 dB side/mid"**: consistent with my dual-mono finding (a few differing samples), no conflict.
6. **Rhythm's "snare crack and tom region 1.5-5 kHz"**: not testable from sound alone; the drum stem has 3-6 kHz and 6-8 kHz at -11.7 and -12.3 dB re total, so the high mid-band is strong; no instrument naming from me.

## 8. Production-era judgement (INFERRED; confidence medium; carried with new figures)

Modern loudness-maximised production, delivered through a narrow-band, dual-mono chain; not a period recording; an archive layer is not shown. Figures: sample peak 0.0 dBFS and 10,317 samples exactly at maximum; mix RMS -10.0 to -10.9 dBFS for 3:30 min (crest 10-11 dB); clipped runs up to 3,354 samples (80 ms) at 2:57.4; a 20 ms near-total mute at -94 dB right after it and a 10 ms -67 dB frame at 0:10.62 (both edit-like, new this round); four-bar bed and bass cycles, waveform repeats r up to 0.85 (rhythm); 8.03 kHz wall about 79 dB deep, dual-mono. Kick spread: uninformative (withdrawn as a cue, section 7). Band-limited layer against a full-band mix: not available, because nothing in the file is full-band (all stems stop at the wall), so neither supported nor excluded; no hiss or crackle floor under the bed in the fade. Net: "modern mastering on top of archive material" is not supported by the measurements; "modern or DAW-style handling of whatever source went in" is. Only the loudness and edit cues show the modern stage; the narrow-band and mono properties could equally be an old source or a modern lo-fi delivery.

## 9. How the sound serves the other areas (connections)

- **To rhythm and form.** The mix has a loudness ceiling, so every arrangement move is a subtraction: bass out takes 1-4 dB off the mix (the drums and bed carry it), voice-and-bass out 6-12 dB. The sub-bass is the only energy below about 100 Hz that comes and goes, and the kick (65 to 40 Hz) sits right on top of it: when the bass is gated out the kick's falling thump is the only sub-bass left, which is why the low end reads as "thinned", not removed.
- **To feeling.** The felt "closeness" is measurable: dry vocal (gaps black within 0.25-0.5 s), dual-mono, nothing above 8 kHz, a flat -11 dB median envelope with only 3-5 dB of movement. The jolt at 0:10.6 and 2:57.5 is the clipping plus a hard mute, not a tail or swell. The pulse-like quality of the hat comb sits in the 3-8 kHz region, where the drums stem is flat to the wall.
- **To harmony.** The bed's pitch classes are an overtone series: D, A, F#, C, E. The third and the seventh you hear in it are timbre, not chords (section 3).
- **To voice.** The hook is gated (active 72-78 % of frames against 92 % in the verses), not more compressed.

## 10. Two new questions

1. **To rhythm:** The 20 ms full-mix mute at 2:57.54 and the 10 ms dip at 0:10.62 each follow a hard-clipped run. Does the kick or bar grid (94.0 BPM, 16th = 0.1596 s) keep its phase across each mute (the cut mutes time but the loop runs on) or does it jump (the cut removes time)? Please measure the kick IOI across 2:57.5 and 0:10.6 on the drums stem.
2. **To harmony:** If the bed's F# and C are partials 5 and 7 of one D tone (F# -5 to -10 dB, C +7 to +9 dB re f0, A the strongest at +12 to +16), does the labeller's D versus Dm flip track the level of the 740 Hz partial (F#5) against the 698 Hz position (F5), and is there any energy at 698 Hz in the bed at all in the stretches where the label says Dm? If not, the whole minor-third case rests on the voice's F (17 % of hook time) and the side-step chords, and the label "D minor" is a statement about the voice, not the drone.

## Not recoverable by measurement

- Instrument identity of the bed, bass and drums (organ, synth or sample; machine or break; synth or electric bass): spectra and envelopes show partials, decay and band energy, not a source. The bed's partial pattern fits several instruments.
- Whether the kick's second rise is a second layer, beating or a sweep through band edges: the isolated-kick sample is only 47 and the stems are estimates.
- Whether the file passed through a 16 kHz stage in the source or in the delivery, and why: the wall is sharp and well placed but is not a date stamp.
- Whether the 2:57.5 and 0:10.6 mutes are performance gestures, DAW edits, a gate or limiter behaviour: the signal shows the event, not who made it.
- Whether any real reverb, delay or double-tracking exists inside the mix: mono summing, a limiter and stem separation could remove the traces.
- Recording or release date, performer, studio: not in the signal.
- Why the bed is 12-14 cents sharp of D3 (sped-up source, synth tuning, or tape drift): a pitch figure cannot show the cause.
- Whether the clipping was deliberate and whether the final fade is a performance or a master fade.
