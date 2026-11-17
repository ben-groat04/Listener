# video1: harmony and melody specialist, round 1

Evidence keys: [ch] chords.json; [ln] lead_notes.json; [af] audio_features/summary.json; [img NNNN] music_views/window_NNNNs.png; [win] the ten window notes (win_0000 to win_0180); [mine] v1/scripts/agents/harmony_r1.py (CQT chroma of the `other` and `bass` stems per section, and pyin on the bass stem). I cannot hear; everything is inferred from measurements. Times m:ss. Tempo 78.3 bpm, beat 0.77 s, a "bar" of four beats is 3.07 s, an 8-beat cycle is 6.1 s [af].

## 1. Headline (what a listener gets harmonically)
A three-minute **D pedal**. One tonic, D, from 0:01 to 3:08, with almost no true modulation. Harmony is texture and colour, not journey: a power-chord (root plus fifth) wall that sits on D, flavoured by a flat seventh (C natural) and decorated by neighbouring chords (G, C, Bm, Am, F) that come and go. The major or minor third is never settled. The only distinctive harmonic event is a **low F sub-bass "drop" cycle at 1:56 to 2:40**. There is no sung melody anywhere; the "lead" is spoken narration. Confidence: high for D tonic and no sung tune; medium for the modal colour; low for any particular chord label.

## 2. Key centre and mode (checked)
- Whole-song key D major 0.760 vs D minor 0.756, G major 0.51 [af]: a tie, which itself says "third ambiguous". Per 30 s: 0:00 D maj, 0:30 D min (0.70 v 0.63), 1:00 D maj (0.73 v 0.58), 2:00 to 2:30 flips to A minor / F / C (0.60) [af, win_0120]. That flip is not a modulation: it follows from the Am-D-G fragments and the loud A in the guitar chroma at 2:15 (see 5).
- My CQT chroma of the `other` stem [mine]: D is the strongest pitch class in every section except 2:15 to 2:40, where A overtakes it (A 1.00, D 0.84). The fifth A is second in most sections (0.5 to 0.83). **C natural is consistently stronger than C sharp** (e.g. 0:40 to 1:00 C 0.70 vs C# 0.46; 1:15 to 1:40 C 0.82 vs 0.52; 2:48 to end 0.67 vs 0.48). So the seventh is **flat**: Mixolydian, Dorian or Aeolian colour, not Ionian. Confidence medium-high.
- The third: F natural (minor) and F sharp (major) both appear at low-to-moderate strength and neither dominates. F is 0.52 at 0:40 to 1:00 and 0.35 at 1:40 to 1:56; F# is 0.28 to 0.40 at 0:00 to 0:40, 0.52 at 1:56 to 2:15, 0.41 at 2:48 to end [mine]. This fits power chords (no third) with the third only brushed by passing notes or by the chord-tracker flicker D/Dm. Window notes agree (win_0040, win_0060, win_0080, win_0120). **Verdict: D5 modal pedal, third unspecified; the flat seventh makes it read Mixolydian or Dorian rather than major or natural minor.** Sixth: B natural 0.36 to 0.52 vs A sharp (B flat) mostly lower except 1:56 to 2:15 (A# 0.48), which weakly hints Dorian most of the time and Aeolian at the drop section. Low confidence.
- Do not call it "D minor": the label counts in [ch] show Dm and D alternating roughly equally, which is tracker wobble on an ambiguous third.

## 3. Chord content, loops and the progression
Chord track [ch] is a chroma-template guess on distorted material; treat Fm, Cm, Gm, Em, N as noise or passing notes. The stable reading is by section:

| Time | Harmony | Evidence / confidence |
|---|---|---|
| 0:01 to 0:08 | static D5 (one long bar group of ~9 beats) | [ch] D 0:00.95 to 0:07.89; chroma D 1.00, A 0.65 [mine]; high |
| 0:08 to 0:20 | D with G, C, Gm, Dm moving every beat: G - C - D - Gm - D - G - D - C - Dm - D | [ch], win_0000; medium (labels noisy). Pattern: a 1-beat "chord-stab" per 0.77 s over the D pedal |
| 0:20 to 0:40 | D home, neighbours G, Dm, Gm, C; returns to D every 1 to 2 chords | [ch], win_0020; medium. G and E chroma flashes recur about every 3.1 s (one bar) [win_0020, img0020] suggesting a repeated one-bar figure |
| 0:40 to 1:00 | clearest repeating pair **C then D** (flat-seven to tonic, every 2 to 3 s), then F, A, G passing | [ch]; medium. Fm/Cm at 0:43 to 0:45 are dubious (a "jolt" gap at 0:42.9, win_0040) |
| 1:00 to 1:15 | D / Dm with Bm every ~3 s (1:07.2, 1:10.2, 1:13.3) over a D+A pedal | [ch], win_0060; the Bm is probably the sixth (D6) or a riff note; medium-low |
| 1:15 to 1:20 | D to A to Am to C to F to Bm: harmony opens when the bass drops out | [ch]; low-medium (estimator unreliable with no bass) |
| 1:20 to 1:27 | F - Bm - G - D - G - D: the most "functional" move in the piece (C-F-G-D feel) | [ch] win_0080; low-medium |
| 1:27 to 1:40 | D pedal with bare fifth; labels Am/D alternate but chroma is D+A | [img0080], win_0080; medium |
| 1:40 to 1:57 | D with brief Cm, Bm lift at 1:48 to 1:51 under a vocal burst | [ch], win_0100; low |
| 1:57 to 2:15 | D/Dm held, **F sub-bass drops** (see 4) | [img0120] chroma, [mine]; high |
| 2:15 to 2:40 | 8-beat loop: **Dm held ~2 s (with the bass drop), then a quick walk Am - D - G - D - G**, then back; repeats at 2:21, 2:25.6, 2:31.7, 2:38 (period ~6.1 s) | [ch], win_0120/0140; medium (timing matches the bass-stem drops exactly) |
| 2:40 to 2:48 | C - Dm - D, Bm at 2:47 | [ch]; medium-low |
| 2:48 to 3:08 | **D held for 20 s** (one chord label) but chroma shows stabs on C, A, B, E roughly once per beat: a one-beat riff over a drone; last 2 s drift to G/E/F# (win_0180) | [ch], [img0160/0180], [mine] C 0.67, A 0.60, B 0.52; medium on drone and stabs, low on the ending |

**Structural loops.** (a) Two-bar (8-beat, 6.1 s) loop is the main harmonic unit in 0:00 to 0:20 and 2:15 to 2:40 [ch, beats]. (b) The progression family is I - bVII (D - C) with IV (G) and a lift to vi/II colours (Bm, Am); in Roman numerals relative to D Mixolydian: I, bVII, IV, vi, v/minor-v. None of these resolves by dominant: the V chord (A major) appears only as the A of power chords, and I see no A to D cadence. That absence of leading-note/dominant pull is why the track feels static and driving rather than resolving.

## 4. The F sub-bass drops (the one distinctive harmonic fact)
My pyin on the bass stem [mine]: in 2:00 to 2:40 the held bass note is **F1 (about 43.7 Hz)**: F1 count 97 of ~110 voiced frames at 2:00 to 2:15, 91 at 2:20 to 2:40. At 0:40 to 1:15 and 2:48 to 3:08 the bass is **D1 (36.7 Hz)** (173, 138, 167 counts), with C2/C1 and G1 as neighbours. The image [img0120] confirms it: bright F row in the chroma panel precisely at the bass drops (2:01.2, 2:07.2, 2:13.4, 2:19.6) and the bass panel shows a plain sustained low tone with a flat top and abrupt cut.
- Interpretation: in the middle of the song the bass moves from the D root to **F, the minor third, held as a pedal while the guitars sit on D5/Dm and then walk Am-D-G**. Harmonically that is Dm/F, or equivalently an F-major-ish sub tone under the D wall (bVI/relative-major colour, with the A chroma dominance at 2:15 to 2:40 suggesting an Am/F/C-area reading as the 30 s key block did). This is why [af] flips to A minor / F / C at 2:00 to 2:30. It is also why the third finally leans minor in that stretch (F is in the bass). Confidence: high that the bass pitch class is F; medium on how it combines with the guitars; low on octave (43.7 Hz is at the limit of pyin; D1/F1 are in the sub-bass where the tracker may be an octave off).
- Elsewhere the bass is a D pedal with C below it (bVII) and brief C#/B passing (1:15 to 1:40 is the bass-absent stretch, so those bass-chroma numbers are leakage). Bass-chroma for 0:01 to 0:08 is flat (the bass is near -66 dB then, so ignore).

## 5. Riffs and motifs (limits first)
No reliable melodic riff can be transcribed from stems alone; the window notes agree. What is measurable:
- **Rhythm of the guitar-like layer:** onsets every ~0.19 s (sixteenth notes) from 0:00.77 on the D pedal [win_0000 onsets]: a palm-muted ostinato on D. High on the rhythm, low on the notes.
- **One-bar figure at 0:20 to 0:40:** G/E chroma flashes about every 3 s [win_0020, img0020]: a repeated stab on the IV/ii colour against the D drone. Medium-low.
- **One-beat stabs at 2:48 to 3:08:** root D with excursions to C (down a tone, bVII), A and B (up), about once per beat [img0160, img0180, mine]. The vocals-stem lead notes after the narrator has gone (D3, C3, C#3, D#3, A#2, B2, G3, A#3 at 3:00 to 3:07, [ln]) are guitar/bass bleed, and show a low chromatic wobble around D: C - C# - D, down to A#/B, back to D, repeated at 3:01.6 to 3:03 (win_0180). That is a plausible description of the closing riff: a **semitone-neighbour figure circling D3**, i.e. gritty and chromatic, consistent with the flat-seven (C) plus occasional C#. Confidence medium-low.
- **Development:** the "motif" develops by layering, level and brightness (other stem -27 dB at 0:02 to -14 dB by 0:57; centroid 2.1 kHz at 2:30 to 2:50 vs 2.76 kHz at 3:00 to 3:08 [win_0180]) rather than by changing notes. I see no transposition, inversion or counter-melody. The sustained, pitched lines in the `other` stem at 1:21 to 1:25 and 1:33 to 1:38 (about 1.5 kHz and 1 kHz bars, [img0080], win_0080) are the nearest thing to a melodic line; the pitch of those partials was not identified. **Task for another round:** compute their f0 from the `other` stem to see if they are a held lead or just chord overtones.
- **Lead-note tracker [ln]:** every window note correctly calls it speech. Spoken pitch sits around G2 to B3 (about 100 to 250 Hz) with falling gestures (e.g. B3-A3-G3 at 2:16 to 2:17.5). Notes in silent-vocal stretches are leakage. There is **no sung melody** in the whole track (high).

## 6. Narration against the harmony
The sample is unpitched but its phrases end on chord boundaries (win_0020: last phrase at 0:31.6 lands on Gm-D; phrase gap at 0:26.4 on D-G). Harmony under the speech is mostly pedal; chord motion clusters in the instrumental gaps (0:08, 0:32 to 0:40, 1:20, 2:15). Medium.

## 7. How it feels (interpretation, flagged as such)
- **Relentless, trance-like, a train that does not stop** (high): one tonic for three minutes, sixteenth-note ostinato, no dominant pull.
- **Stern, cold, slightly grim grandeur** (medium): the flat seventh and ambiguous third give a modal, open, unsentimental power-chord sound, not a warm major key. Matches CLAP "triumphant/tense/nostalgic" only loosely (weak evidence).
- **Brief lift and hope** (medium-low): 1:20 to 1:27 (F-Bm-G-D, bass absent) and 2:15 to 2:20 (Am-D-G walk) feel like opening-out moments, because chords move for the first time after long stasis.
- **Weight at 2:00 to 2:40** (medium): the very low F under the D wall is felt as a body-level pulse, a "dread/anticipation" pedal, repeatedly released.

## 8. What the measurements cannot tell
Guitar vs synth identity; the actual riff notes; major vs minor third; whether F1 is an octave off; whether Bm/Am/Gm labels are real chords or passing tones; whether the final seconds (3:06.5 on) really leave D (chroma suggests G/E/F# but [ch] still says D).

## 9. Three questions for fellow specialists
1. **Sound specialist:** does the `other` stem's timbre (attack, distortion, spectral shape of the sustained 1 to 1.5 kHz lines at 1:21 to 1:38) look like electric guitar, an organ or a synth? That decides whether the held lines are a lead melody or chord overtones.
2. **Rhythm specialist:** are the F sub-bass drops (2:01.2, 2:07.2, 2:13.4, 2:19.6 ...; period 6.1 s = 8 beats) aligned to a bar downbeat, and do the kick or snare drop out or change at the same instants? That would show whether the F pedal is the "bar 1" of an 8-beat phrase.
3. **Form specialist:** my harmony splits the track at 1:15 (bass out, chords open), 1:40 (bass in, full band), 1:56 (guitar cut, F-drop section), 2:15 (Am-D-G walk with the narrator) and 2:48 (20 s D plateau). Do your section boundaries agree, and what does the 2:48 to 3:08 plateau do formally (a coda, a final chorus)?
