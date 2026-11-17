# t_dl_mirror: VOICE specialist, round 3 (blind, measurements only)

Read: all seven round-2 files, plus round-3 harmony and sound (rhythm round 3 is empty). New script `v1/scripts/agents/voice_r3_tdl.py` (vocal-stem onsets, kick-grid test per hook, pitch around step starts). Times m:ss. Stems are demucs estimates; no context.md, research or web.

## 1. Answers to questions put to me

**Rhythm Q2: do hook syllables fall on the eighth grid, and can you list first-syllable onsets of three hook lines?**
Onsets (librosa onset detector on the vocal stem, 2.9 ms hop, seconds after the hook start, hook starts 0:10.4, 1:11.3, 2:12.0, 3:13.1). Line 2 ("In my ___ in the morning", +3.4 to +5.5 s):
- hook 2: 4.11, 4.24, 4.36, 4.71, 4.84, 4.97
- hook 4: 4.10, 4.29, 4.52, 4.86, 5.01, 5.14
- hook 3: 3.61, 3.77, 3.99, 4.45, 4.70, 5.04, 5.15
- hook 1: 4.14, 4.41, 4.75, 4.89, 5.03
Line 3 start (+13.3 to +15.0 s): 14.49, 14.85 (hooks 1 and 2, identical to 10 ms, 14.49 and 14.85 in both); 13.57, 13.92 (hook 3); 14.07, 14.68 (hook 4). Hooks 1 and 2 agree to 10 ms at two onsets; the others agree to 0.1 to 0.3 s, so syllable timing is the same pattern with small shifts (measured, medium; this softens my round-2 "same phrase" claim only in that exact onset times are not identical).
Grid test: against the kick-fitted eighth grid at 94.0 BPM (0.319 s), the voice onset concentration R is 0.15, 0.31, 0.25, 0.27 for hooks 1 to 4 (random 0.12 to 0.13, n 45 to 54); at 94.5 BPM (the form specialist's bass-loop clock) 0.29, 0.35, 0.38, 0.34. So hook syllables lean weakly towards an eighth grid, more at 94.5 than 94.0 (offset within -15 to +13 ms). But the kick's own R on that grid is only 0.06 to 0.16 (it is loosely defined; the phase is borrowed from it), and the sixteenth grid is no better (voice R 0.15 to 0.35). Reading: a weak pull to the eighth, below the 0.30 level that would be clearly non-random for n of 50 (low confidence); the within-line inter-onset intervals of 0.12 to 0.15 s (for example 4.11, 4.24, 4.36) are faster than a sixteenth (0.160 s), so rapid hook syllables are not grid steps (measured, medium). This is a statistic on the kick grid at 94.0 and the clock at 94.5, both named; it is not a sync result.

**Harmony Q2: does the voice change pitch or processing at the step starts, and is each hook line copied or re-sung?**
Pitch (pyin, median F0, windows before the step, around it, after it): at +5.7 s from hook start 394 to 397 Hz before, 392 to 397 around, 433 to 436 after in all four hooks; at +15.6 s 394 to 400, 390 to 393, 437 to 440 after. So in every hook the sung line sits on G4 (392 Hz) and moves up to A4 (about 435 to 440 Hz, 15 to 20 cents flat of A440) 1 to 2 s after the step starts, consistent with harmony's "voice leads or sits against the bass step" picture and with the three-note melody (G4, A4, F4); the voice does not jump at the step start itself (INFERRED, medium; windows are coarse). Processing: nothing measured changes (level, crest and gap pattern are the same in the four hooks, round 2), so no effect or compression change at the steps (low; dry mono stem). Copy or re-sung: phrasing and gaps repeat to about 0.5 s, pitch contours to 1 semitone, waveform not identical (round 2, r 0.24 to 0.46) and onset times shift by 0.1 to 0.3 s between hooks 3 and 4 against hooks 1 and 2. I keep: same performed pattern, not shown to be one pasted recording (INFERRED, medium-low).

**Sound: hook gated (active 72 to 78 % against 92 %), not more compressed.** Agreed; it matches my 35 to 50 dB gaps and the hook crest of 17.7 to 18.0 dB.

**Form (hook as 8-bar unit with inner events) and lineage (statement, answer):** my gap and step data fit form's plan: hole 1 (+0.2 to +0.8 s), step 1 (+5.4 to +6.5), long hole (+12.9 to +13.4), step 2 (+15.2 to +16.8), hole at +17.5. The voice is silent for about 1.1 s at +13 and again at +17.5, so the second half of the hook is a more broken delivery than the first. That is a statement and answer shape (INFERRED, low; no words are certain).

## 2. Corrections

- I keep my round-2 hook start times; the onset listing above confirms the first sung onset after hole 1 at +1.0 to +2.2 s, which is why the "hook starts" in the form file (2:14.0, 3:15.09) were hole exits (accepted by form).
- Round 2 said the voice leaves at 3:34.7 to 3:35.3. Form measured the thinning from 3:34.0 and the voice tail to 3:35.1 (-58 dB at 3:35.2); sound says phrase-wise thinning with no tail. I accept 3:33.5 for the last phrase edge and about 3:35.1 for the last audible voice (stem -58 dB), tag medium-high. My earlier "-51 dB at 3:35" is the same event.
- Tempo: my 24-bar spacing (60.9 s) sat between 94.0 and 95.7; form's bass loop gives 94.5. The grid test above is also slightly better at 94.5 than 94.0 (R 0.29 to 0.38 against 0.15 to 0.31). I now carry 94.5 as the arrangement clock and 94.0 as the kick-window figure, medium-low, and still reject 95.7.
- Feeling's "voice leaves, bass the only layer that moves, aftermath": agreed with my data (voice floor -66 to -74 dB from 3:35.3).

## 3. Connections (words and music answering each other)

- **Voice and harmony:** the missing-word line "In my ___ in the morning" holds the sung G4 while the bass walks (G, F, C, D); the voice then rises to A4 as the bass resolves back to the D pedal. The words are about a repeated morning and a mirror-like swap ("You I see, I see you" in the transcript), and the harmony is a thirdless D+A drone that only bends under that line (INFERRED, low-medium; word identity is not recoverable).
- **Voice and rhythm:** verse onsets 5.0 to 5.2 per second against 6.3 sixteenths per second, hook onsets about 2.2 to 2.7 per second on this detector, so verse rapping is dense and loosely locked to the kick grid (R 0.24) while the hook is sparse, gated and a little more eighth-aligned (R 0.25 to 0.38). Speech-like free flow versus a rehearsed refrain, which matches the form file's register jump (voice down 7 to 9 dB and up in pitch at hook entries).
- **Voice and sound:** dry, no tail, no side-chain; the voice cuts by 35 to 50 dB in 0.1 to 0.15 s, edges that sound calls hard digital cuts. The jolt is a mute, not an effect.
- **Voice and form:** voice defines the section edges (+4 to +5 dB into verses, -7 to -9 dB into hooks 2 and 4), bass is the offset clock; the fixed 24-bar vocal pattern (same gaps within 0.5 s) is the strongest repetition evidence in the track.
- **Production era (rule 1):** vocal stem peak -1.2 to -3.2 dBFS, verse crest 14.6 to 15.1 dB, mix peak 0.0 dBFS; hook holes repeated to 0.5 s but waveforms not identical (r 0.24 to 0.46), kick spread 20 ms SD on 94.0 BPM. Judgement: modern DAW-style arrangement and limited master, performed vocal on top; no narrow-band older layer separable from the common 8 kHz wall. INFERRED, medium.
- **End (rule 4):** last audible mix sound 3:56.45 at -60 dBFS, digital zero from 3:56.70 (10 ms envelope; form and sound agree). Last voice about 3:35.1, so the track ends on the bed with no voice.
- **Boundary table (voice view, other stems from colleagues, marked c):**

| boundary | drums | bass | vocals (mine) | other | carried by |
|---|---|---|---|---|---|
| 0:10.4 entry | +1.8 dB (c) | +29.9 dB (c) | -68 to -25 dB, +43.5 | +4.9 (c) | vocals, with bass |
| hook first holes | little (c) | on, except hook 4 (c) | to about -55 dB median | steady (c) | vocals only (hook 4: with bass) |
| 3:34.0 to 3:35.3 | -2.5 (c) | -12.4 (c) | -21 to -58 | -0.6 (c) | voice and bass together |

No silence: the mix stays above -22 dB in every hole (form).

## 4. Settled conclusions (5 bullets)
- **The voice is a dry, mono, gated vocal: rapped verses (about 5 onsets per second, speech pitch near A#3) and a sung or chanted three-note hook (G4, A4, F4), with 35 to 50 dB mutes in 0.1 to 0.15 s (measured, high; sung-versus-chanted INFERRED, medium).**
- **The four hooks are one performed pattern: gaps repeat within 0.5 s every 24 bars (hook starts 0:10.4, 1:11.3, 2:12.0, 3:13.1), contours agree to 1 semitone, waveforms do not match, so not shown to be a pasted copy (measured high on the timing; INFERRED, medium-low on re-sung).**
- **Hook 4 is not louder or higher (RMS -19.3 to -20.2 dB, F0 median 401 to 410 Hz); the final arrival is an arrangement event shared by all hooks, so the feeling of an ending comes from position and the voiceless outro (measured, high).**
- **Words and music answer in one place: the "In my ___ in the morning" line carries the bass walk, and the sung note moves G4 to A4 around it; syllables are only weakly tied to an eighth grid at 94.0 or 94.5 BPM and are too fast (0.12 to 0.15 s) for sixteenth steps (INFERRED low-medium).**
- **The voice ends by phrase-wise thinning at 3:33.5 to 3:35.1 with no tail, the last audible sound of the track is the bed at 3:56.45 (-60 dBFS), then 2.77 s of digital zero (measured, medium-high).**

## Not recoverable by measurement
- The missing hook word and the true lyrics: Whisper disagrees pass by pass, and a measurement gives timing and pitch, not words.
- Whether the hook was re-sung, chopped from one take, or pasted: stem bleed hides waveform identity.
- Whether the mutes are drawn, gated or performed: the edge shows the event, not the hand.
- Double-tracking, autotune, reverb, compression settings: mono, limited, 8 kHz-limited separated stem.
- Performer, intent, irony, whether it is autobiographical: only pitch, level and timing are measured.
- Real tempo (94.0, 94.5 or 95.7): three baselines give three figures.
- Source and age of the bed and any sample: the shared 8 kHz wall is the file chain, not a date.
