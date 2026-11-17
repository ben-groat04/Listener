# video1: SOUND specialist, round 3 (final)

Evidence keys: [lv] per_second_levels.json; [img NNNN] music_views windows; [s2] sound_r2*.py; [s3] v1/scripts/agents/sound_r3.py (new: kick-band waveform comparison, kick pitch and decay, sub-versus-kick timing at the six drops, onset rise of the 1:15 to 1:40 line, 50 ms stem floors around edits; htdemucs stems at 22.05 kHz); [R2-x] round-2 files (rhythm's was empty, so I answer its R1 points only where relevant). I cannot hear; all is inferred. Times m:ss. Stems are proxies and leak.

## 1. Answers to questions put to me

### 1.1 Lineage: sampled or programmed kit versus played kit? (low; open)
[s3], 96 kick events in 0:20 to 1:00 (40 to 120 Hz band, window -5 to +80 ms):
- Mean pairwise waveform correlation of the normalised kick snippets is **0.35**. Identical samples through a constant mix would give near 1 if the stem were clean, but the snippets include hat, snare and bass-stem bleed, so 0.35 is not a clean test. I cannot call it either way.
- Peak frequency in the first 60 ms: median 58 Hz, spread 12.6 Hz (a 60 ms window is about 3 cycles, so blurred). Decay from first 20 ms to 40-80 ms: median -6.7 dB, spread 2.7 dB (consistent with R1's short decay).
- Round-2 amplitude CV was 0.18. Net: kick hits are moderately consistent, not identical. This **does not support** "flat, copy-pasted machine hits", and does not support "played" either. The honest answer is that the stems cannot settle band-in-room versus loop-built. Only the sub (section 1.3) is demonstrably designed.

### 1.2 Lineage: do the wall's floor or decay change at edit points in a way that suggests muted stems rather than a band stopping? (medium-low)
[s3] min / median dB of 50 ms frames in a 2 s window around each edit:
| Edit | bass stem | drums | other |
|---|---|---|---|
| 1:15 | min -66, median -47 | min -42 | min -27 |
| 1:40 | min -65, median -33 | min -40 | min -19 |
| 1:55 | min -65, median -27 | min -32 | min -20 |
| 2:48 | min -66, median -31 | min -59 | min -30 |
- When the bass is out it falls to about -65 dB and stays flat there: no ring-out, no bleed, no room tone. A real bass amp or room does not drop to a flat floor this cleanly; a muted stem or a gated synth does. But demucs also gates quiet stems, so this is **suggestive of stem muting or a programmed bass, not proof** (medium-low).
- The `other` stem never goes below about -27 to -30 dB at any edit: the guitar layer keeps a floor, so it is continuous (agrees with Form's 2:48 finding).
- The drums stem goes to -59 only at 2:48 (a real hole); at other edits it keeps hat activity.
- Reading: the arrangement behaves like stems being muted and unmuted on a grid (bass in and out with flat floors), over a continuous guitar and drum bed. That is production language, not a band stopping. Medium-low, since bass-stem flat floors are also what a demucs gate would produce.

### 1.3 Harmony: attack of the 1:15 to 1:40 stepwise line (plucked, bowed, organ-like)? (low)
[s3] onset rise: for 119 detected onsets in `other` 200 to 600 Hz, the median time from onset to envelope peak is 0.22 s. That is slow for a pluck (tens of ms) and fits a sustained or swelled tone (bowed, organ-like, synth pad, or sustained guitar with reverb or e-bow-like envelope). But a median-filtered envelope and a distorted overlay smear everything, so this is **weak, low confidence**. It agrees with R2's description of it as a slow stepwise line; it does not name an instrument.

### 1.4 Rhythm (my R2 question): sub versus kick at the drops (low)
[s3] kick-band peak versus 50% point of the 35 to 55 Hz sub envelope at the six drops: offsets between about -0.4 s and +0.4 s with no pattern. My nominal drop times were rounded to the second and the sub's rise is slow, so this test is not precise enough; the kick-band energy at the drop may just be the sub itself leaking into the drum stem. I withdraw the question as unanswerable with these stems. What survives: the drums keep running under the drops (Form's phase result), so kick and sub are separate layers.

## 2. Corrections
- Mine, R2 2.4: I said both machine and human fit; [s3] adds that kick waveforms are only moderately alike, which slightly disfavours "identical samples" but is confounded. Net wording: unresolved.
- Mine: the R2 table of `other` centroids stands; I now add that the 1:15 to 1:40 line has a slow (0.22 s) attack, low confidence.
- Form's loudness correction (K-weighted: level peaks at 1:07 to 1:15 and 2:48 to 3:08, not 1:40 to 1:55) is accepted. My R1 "loudest around 1:40" claim based on dBFS is superseded: weight peaks at 1:40, loudness at the two ends.
- Feeling's note that the 42 Hz sub vanishes on small speakers is correct and I endorse it: it is the main playback-dependence of the whole piece.

## 3. Connections
- **Sound and Form:** every boundary is a stem mute/unmute on a bar grid (1:15, 1:27, 1:40, 1:55, 2:38, 2:48); bass floors of -65 dB in the gaps make the boundaries sharp. Form is built from timbre and density, plus loudness at the ends of the arch.
- **Sound and Harmony:** the fixed, falling-edge sub plus a high open-fifth figure at 2:00 means the mix itself withholds the third; the key feel is made by production.
- **Sound and Feeling:** the felt "arrival" at 1:40 is weight and width, not loudness (+0.1 LU). The 2:00 block feels small because it is high, thin and narrow; the final run feels hard because it is loudest, steady (+/-0.3 LU), and has a hat/crash share four times larger.
- **Sound and Voice:** narrow-band, dry, centred speech under a wide band, with a clean floor between phrases.

## 4. Settled conclusions (final)
1. **Contemporary alt/post-rock production, heavily limited:** a dense high-gain "wall" (probably guitars; the stems cannot prove it), dry gated-sounding drums that never stop, loudness flat across the piece (about 8 LU of short-term range, mostly at the section ends). High on the style, medium on the instrument labels.
2. **The one clearly designed sound is the sub:** fixed 42.6 Hz, starting 3 to 6 Hz sharp, falling within about 0.3 s, soft 20 to 110 ms attack, almost no content above 300 Hz; six triggered hits at 2:01 to 2:31. It is weight without a note, and nearly inaudible on small speakers. Medium-high.
3. **Form is made by timbre and mixing moves:** bass in/out with flat -65 dB floors, the `other` layer's four timbral states (D3 drone, mid wall, high fifths at 2:01 to 2:13, bright wall), width swings (0.29 to 0.73), and the cymbal-led final (hat and crash share 3% to 12%). Medium-high.
4. **The speech is a separate, clean, band-limited layer** (95% below about 3.7 kHz, no noise bed, centred, dry, 4 to 5 dB under the band), consistent with mid-century film or radio audio set against a modern band. High on the measurements, medium on the era.
5. **Honest limits:** I cannot say whether the drums are sampled or played, whether the wall is guitar or synth, whether any reverb or delay exists on the 2:00 figure, or true LUFS; the bass-stem silences hint at muted stems or a programmed bass but cannot prove it.
