# t_dl_mirror: HARMONY specialist, round 2 (blind, measurements only)

Read: all seven round-1 files. New measurements this round: `v1/scripts/agents/harmony_r2_tdl.py`, `_r2b_tdl.py`, `_r2c_tdl.py` (stem chroma at 0.63 s steps, tuning estimate, pyin on the vocal stem, 10 ms end envelope). Times m:ss. Stems are demucs estimates; chroma is a crude pitch-class tool.

## 1. What changed in my reading (headline)

1. **The side-step is a real harmonic move, and the bass plays it.** Round 1 said the bass "plays the root only" and the bed does not move. Both are wrong for the side-steps. Stem chroma at 0.63 s steps shows the bass stem walking **G - F - C - D** in each side-step: 3:19.13-3:22.28 gives G#/G (to 3:20.4), F (3:20.4-3:21.65), C (3:21.65), then D from 3:22.3; 3:28.76-3:31.91 gives G (to 3:30.4), F (3:30.65-3:31.28), C-ish (3:31.28), D from 3:31.91. Same at 0:16.0-0:19.15 and 0:26.06-0:29.2. The "other" stem shows G (0.90-1.00) then C/F/E rows lit while D stays at 1.00 as a pedal (3:21.02: C 1.00, F 0.82). So: a bass walk G-F-C-D (iv - bIII - bVII - i if D is tonic) over a D pedal. Confidence: **high** that bass and bed move; **medium** on exact root names (bass chroma smears to G#/F# beside G; octave unknown).
2. **The "G" is more likely G major than G minor.** Round 1 favoured Gm (7.7 s Gm against 5.0 s G labels) and so natural minor. In the other stem B natural is 0.45-0.60 (0:16.0, 3:18.5, 0:26.06) against A# 0.27-0.36; Bb is never a top-3 class at any step. That reads as G major (IV) - F (bIII) - C (bVII), a Dorian-flavoured shape, not Aeolian. INFERRED, **medium-low**. I lower "natural minor favoured" from medium-low to **low**, reason: this step-by-step chroma contradicts the Gm labels (B may be leakage from the E-B-C stack at 0:18.5 and 3:31.3).
3. **The last chord of the run is ambiguous, not cleanly "Am" or "C".** At 0:18.52 and 3:31.28 the other stem shows B/E/C or C/F/E (3:31.28: C 1.00, F 0.95, E 0.86): E is strong and A is absent, so C/E rather than Am. INFERRED, low-medium. Neither is a dominant (no clear A major with C#).

## 2. Answers to questions put to me

**Form (do the side-steps sit at section boundaries; does the hook use a different chord loop from the verse?)**
- They sit **inside the hooks, never at a boundary**. Hook 1 (0:10.4-0:30): 0:16.0, 0:25.6. Hook 2 (1:11.7-1:32): 1:17.6, 1:26.5. Hook 3 (2:12-2:32): 2:17.4, 2:28.8. Hook 4 (3:14.4-3:34.7): 3:19.1, 3:28.8. Verses have **none**: other stem 2:40-2:50 is D 1.00, A 1.00, C 0.38 (pure drone), the same as 0:40-1:10 (D 1.00, A 0.97, C 0.37). So hook = same D+A bed plus a twice-repeated bass/bed walk; verse = bed alone (measured, high).
- Whole-hook other-stem chroma (3:14-3:35) has A 0.82 against 0.97-1.00 in verses: the walk takes energy from the A (INFERRED, medium).
- The `summary.json` split at 0:15.5 is the first step arriving: step chroma already shows G 0.90 and bass G#/G at 0:16.0. The chord labeller was 0.6-0.7 s late; I quote step times to a 0.63 s grid, so +/-0.6 s.

**Voice (same words each time? is the verse voice a semitone off the drone: clash or speech pitch?)**
- The step always starts under the line "In my carry/period/theory and (in) the morning" and runs through its end and the gap into "just seeing me / I see you". Offsets from the ASR line start (+/-0.5 s): hook 1 line 0:15.1 (mix pass), step 0:16.0 (+0.9); line 0:24.0, step 0:25.6 (+1.6); hook 2 line 2:16.8, step 2:17.4 (+0.6) and 2:26.6, 2:28.8 (+2.2); hook 4 line 3:18.0, step 3:19.1 (+1.1) and 3:28.1, 3:28.8 (+0.7). Same words, loose offset: the harmony is tied to the bar, not the syllable (INFERRED, medium; ASR segment starts are not syllable onsets). Hook 3 not aligned (ASR merges its lines).
- Verse voice against the drone (pyin on the vocal stem, tuned to the bed's +13 cent scale): verse 1 median 232.7 Hz, 53 % A#, 22 % A, 21 % B; verse 2 median 231.4 Hz, 43 % A#, 25 % A, 19 % B; verse 3 median 230.1 Hz, A# 27 %, B 24 %, wider. Centre A#3: a minor second above the bed's A, a minor sixth above D. It is near-monotone with a 3-5 semitone span, so **speech pitch, not a chosen melody** (INFERRED, high). I do not call it a deliberate clash.
- **New: the voice is not tuned with the bed.** Bed tuning is +13 cents sharp of A440 (`librosa.estimate_tuning` on the other stem; sound specialist +14, agreed). Hook 4: 65 % of tracked frames on A, median 439.4 Hz, which is about A440 and so about 14 cents under the bed's A (about 443.5 Hz). The verse medians sit about 13-15 cents under the bed grid too. INFERRED, **low-medium** (pyin on a processed voice; but three passages agree). Readings: separately sourced voice and bed; bed sped up about 0.8 %; tracker offset. Undecidable here.

**Sound (does the bed move in the side-steps; mono bed under a wider master?)**
- The bed moves: other stem G 1.00 at 3:19.13, C 1.00 at 3:21.02, A 1.00 and D 0.97 at 3:22.91. The 148 Hz stack is not one held note throughout; G/C/F/E rows are added for 3 s at each step (INFERRED, medium). I did not examine the partial series, so whether a second sound enters or the same sample is re-pitched is open.
- Width 0.0-0.024 (round 1) is mono: I cannot separate a mono source from a mono sum.

**Feeling (same chord shape at 0:15.5 and 3:18.7? tonic?)**
- Same shape, yes: the bass walk G, G(#), F, C then D in all four hooks, lasting 3.0-3.1 s each (0:16.0-19.15, 0:26.06-29.2, 3:19.13-22.28, 3:28.76-31.91), about 1.2 bars at 94-96 BPM (high on shape, medium on roots).
- Tonic: **D, high**. The bass returns to D after each walk and the bed holds D+A for about 84 % of the track. The hook voice centres on A (65 % in hook 4) with F and G. Major or minor stays open in the bed (F 0.17-0.27, F# 0.24-0.26) and is settled only by the voice (F 14 % in hook 4, about 17 % over all hooks; F# about 1 %) and the F in the walk: D minor (or Dorian), medium. The iv-bIII-bVII-i shape feels like a lift and release against a hypnotic drone (feeling claim, low).

**Rhythm (does anything change at the side-step starts?)**
- The **bass is the carrier**: bass stem chroma leaves D for G at 0:16.0, 0:25.6-26.06, 3:19.13, 3:28.76. The walks fall in the bass-dense blocks (rhythm: 0:20-0:40, 1:20-1:40, 2:20-2:40, 3:20-3:40). The 10.2 s chroma periodicity is therefore the bass-and-bed loop, not the bed alone (INFERRED, medium).

## 3. Corrections to others, with evidence
- **Lineage**: "bass root-only (harmony colleague)" came from my round 1 and is wrong for hooks: it is a walking G-F-C-D line there. "One-chord drone" holds for verses only.
- **Voice**: the walk is under the "In my ... morning" line, but its start varies 0.6-2.2 s from the line start (above).
- **Sound**: "no strong third in the bed" stands; the walk adds F, not a third of D.
- My own changes: natural-minor reading lowered to low (reason above); "root only bass" retracted; last chord Am/C downgraded to low-medium. Other round 1 tags kept unchanged.

## 4. Evidence rules
- **Production era (INFERRED, medium-high: modern limited master; the bed may be older material, low)**: sample peak 1.000 in the mix (stems: drums 0.985, vocals 0.99, bass 0.83, other 0.66), mix RMS about -10 dBFS in dense sections (round 1): limited, modern loudness. Cues pointing to an older or low-fi layer: bed mono at -25 dBFS under an 8 kHz-limited drum stem (sound, rhythm), bed 13 cents sharp while the voice sits at A440. Not decisive. Loop: 10.1-10.3 s chroma lag r about 0.92 (round 1), consistent with DAW or sampler, not decisive. Kick spread is held by rhythm (43-45 ms rms on a 16th grid).
- **End of track** (10 ms envelope, `audio/song.wav`, duration 239.44 s): last frame above -60 dBFS in the mix 3:56.44 at -57.0 dB; bass 3:56.36 (-59.5), drums 3:56.36 (-57.3), other 3:55.63 (-59.6), vocals 3:38.13. Levels at 3:50-3:52: mix -27.2, drums -34.0, other -37.9, bass -73.5, vocals -75.8 dB. Mix envelope per 0.5 s from 3:53.6: -30.5, -31.0, -43.7, -45.1, -51.5, -52.4 dB: a **gradual decay of about 3 s**, no single final hit. Peak-finding on the 10 ms envelope gives many small peaks (prominence 3 dB) that are drum and bed flutter, so I cannot give a hit count. Round 1 reported exact digital silence from 3:56.44 to 3:59.44; I did not re-measure that part. Chroma 3:45-3:55 is D 1.00, A 0.96: no cadence beyond held D+A.
- **Sync statistics**: none given. Step times are on a 0.63 s chroma grid, which is about one kick IOI at 94.5-95.7 BPM (rhythm), but alignment finer than 0.3 s is below my resolution.
- **Boundary evidence table** (side-step starts; levels from round 1, pitch from this round's step chroma):

| Boundary | drums | bass | vocals | other | carried by |
|---|---|---|---|---|---|
| 0:16.0 | -19.5>-17.0 dB | D to G/G#, walk starts | -19.1>-22.0 dB | G 0.90 enters, D stays 1.00 | bass pitch, then other |
| 3:19.1 | -19.8>-18.9 dB | D to G#/G, then F, C | -18.7>-23.8 dB | G 1.00, then C 1.00 | bass pitch; mix moves under 0.7 dB |
| 3:22.3 (return) | small | back to D | no change | A 1.00, D 0.97 | bass and other together |

  No silence is involved: the mix level moves under 0.7 dB.
- No unmeasured emotive sound nouns used; the bass walk is given as pitch classes only. Its octave is unmeasured (C1 is about 33 Hz: probable octave error, low confidence).

## 5. Two new questions
1. **To sound:** the bass stem chroma gives G#/G, F, C, D at about 0.63 s steps under each hook. Is that a pitched sub-bass line (sine or glide) or a re-pitched sample, and is its fundamental also +13 cents against A440 like the bed? That shows whether bed and bass share a source while the voice does not.
2. **To voice:** the hook voice sits about 14-15 cents below the bed's A. Does the voice change pitch or processing at the step starts (0:16.0, 3:19.1), and is each hook line repeated note for note (a copy) or re-sung (small pitch differences between hooks 1-4)?

## Not recoverable by measurement
- Which instrument or synth plays the D+A bed and the G-F-C-D bass walk: chroma gives pitch, not timbre.
- Whether the voice or the bed is the older material, or whether the 14-cent gap is a speed change, separate sourcing or tracker error.
- Whether the G chord is major or minor by intent: B against Bb evidence is thin and stem-separation dependent.
- Whether the A#3 verse pitch was chosen against the drone: speech pitch gives no intent.
- Octave of the bass notes: chroma folds octaves.
- Real chord names, recording or release date, and the source of any sample.
