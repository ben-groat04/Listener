# video2: HARMONY specialist, round 1 (blind, measurements only)

Role: key centres, chord progressions and loops, modal colour, riffs/motifs, melodic contour. Music first.
Evidence keys: [WN] window notes `analysis_blind/music/video2/win_*.md`; [CH] `music_views/chords.json`; [AF] `audio_features/summary.json`; [IMG] `music_views/window_NNNNs.png`; [LN] `lead_notes.json`; [LV] `per_second_levels.json`; [P1] `v1/scripts/agents/v2_harmony_probe.py` (chroma of the bass and "other" stems per 4 s); [P2] `v1/scripts/agents/v2_harmony_probe2.py` (bass-root change times, tuning, drum autocorrelation, third of B, pitch tracking of the "other" stem). All times m:ss. I cannot hear anything; every label below is a pitch-class measurement, not a heard chord.

## 1. Headline findings (what I changed or confirmed against the window notes)

1. **The chord file understates the structure; the bass stem gives a far cleaner harmonic skeleton.** The window notes lean on [CH], which flips between Em/E/B/Bm/Am/F#m. The bass-stem chroma [P1] and bass-root change detection [P2] give one root per about 4.0 s with almost no ambiguity (the bass-stem chroma has the root at 1.00 and the next pitch class at only 0.2-0.4 whenever the bass is playing). This is the most reliable harmonic evidence in the dataset. High confidence for the roots, medium for chord quality.
2. **Tuning is A=440** (librosa tuning offset +0.02 semitone [P2]), so pitch names are not shifted. High confidence.
3. **Home key is B minor, Aeolian (natural minor), not Dorian and not major.** [AF] whole-song B minor 0.88. The raised sixth (G#) of Dorian does not appear in any top-five chroma of the "other" or bass stems [P1], while the lowered sixth (G) is strong (e.g. "other" 0:32 G 0.98; bass root G every cycle). The leading tone (A#) is absent as a real pitch; it appears only in the flat noise-floor chroma of the bass stem after 4:48 and at tracker junk. The lowered seventh (A) is the bass root of the late loop. So: B C# D E F# G A with C# rare (a weak 0.4-0.57 only at 1:16 and similar spots, [P1]). High confidence for "natural minor, no raised notes"; medium for the missing C# (the chord loops simply never need it).
4. **Static upper pedal, moving bass.** In the "other" stem, B is the strongest pitch class in nearly every 4-s slice from 0:40 to the end (value 1.00, with F# and D as the next two, [P1]). So the upper layer sits on a B-F#-D (Bm) pedal, and the bass walks under it (E, G, D, B, A). The chord labels Em/G/D/A in [CH] are therefore partly the bass root dragging the label, and partly genuine upper-layer movement (see section 3). Read the sound as "B minor held above, with the bass changing the colour": Bm over E (a suspended, open fourth), Bm over G (a Gmaj7-like warmth: G-B-D-F#), Bm over D (Bm/D, a settled first-inversion), Bm over A (a Bm7-like softness), Bm over B (home). This is an interpretation of two stems' chroma; confidence medium.
5. **The tracker's 161.5 BPM is a 4:3 misreading; the felt pulse is about 121 BPM** (161.5 x 3/4 = 121.1). Drum onset autocorrelation 3:00-3:40 [P2] peaks at 0.5108 s (r 0.40), 0.9985 s (r 0.62) and 1.9969 s (r 0.64), and only weakly at the tracker's 0.3715 s (r 0.21). So the beat is about 0.5 s, the bar about 2.0 s, and a bass note lasting about 4.0 s is **two bars (8 beats)**. This agrees with the rhythmic cell of 1.0 s noted in [WN win_0120] and removes the "about 11 beats per chord" oddity noted in several windows. Medium-high confidence (the 4 s root spacing sits at 8 beats of 0.5 s to within about 0.1 s over the whole track).

## 2. Bass-root map (the skeleton)

Root-change times [P2] with 4-s slice roots [P1]. Bass is silent before 0:28 and again at 1:25-1:28 [LV; WN win_0080].

| Time | Bass roots (each about 4 s = 2 bars) | Reading in B minor |
|---|---|---|
| 0:00-0:28 | no bass; "other" pad only | see section 3a |
| 0:28-0:56 | E, G, D, E, G, D, B (0:28, 0:32, 0:36, 0:40, 0:44, 0:48, 0:52) | iv, VI, III, iv, VI, III, i |
| 0:56-1:24 | E, G, D, E, G, D, B (0:56 ... 1:20; B held to 1:24) | same cycle, 2nd time |
| 1:24-1:28 | bass drops out; Em pad over speech [WN win_0080] | break, 2 bars |
| 1:28-1:56 | E, G, D, E, G, D, B | 3rd time |
| 1:56-2:24 | E, G, D, E, G, D, B | 4th time (2:08 fill, [WN win_0120]) |
| 2:24-2:36 | E, G, D | 5th time, cut short |
| 2:36-4:40 | B, A, D, B, A, D, ... (B 2:36, A 2:40, D 2:44; then every 12 s through 4:36; A at 4:40, D at 4:44) | i, VII, III, i, VII, III |
| 4:48-5:00 | bass chroma flat (A#, B, A, no clear root); chord track Bm | pedal on B, notes unresolved |
| 5:01-5:03 | final stab on B | i |

So there are **two harmonic loops**, a 28-second, seven-chord one (E G D E G D B) for 0:28-2:36 and a 12-second, three-chord one (B A D) for 2:36-4:40. The step from the first to the second is a simplification: the iv-VI-III machinery is dropped and the harmony settles on i-VII-III, the "rock" Aeolian cycle. The chord file's long "Bm / D" seesaw in 2:48-4:20 [CH; WN win_0180/0200] is this B-A-D loop with the A (bass) reported as Bm/D because the "other" stem keeps B+A+D lit [P1: 3:04 other B 1.00 A 0.78 D 0.77]. I correct the note in [WN win_0200] that reads it as "a two-chord seesaw Bm and D": the bass shows three chords per 12 s (B, A, D). Confidence high.

## 3. Section by section

### 3a. Intro, 0:00-0:28 (no bass, no drum pulse)
- [CH] gives one label, Bm, for 42 s. The "other" stem chroma per 4 s [P1] shows more: 0:00 F#+B; 0:04 B+G+D; 0:08 F#+D+B; 0:12 F#+B+D; 0:16 B+G+D; 0:20 F#+D+B; 0:24 E+B+G. So a Bm (B, D, F#) sonority, with **G entering as a second colour at 0:04-0:08 and 0:16-0:20** (G+B+D, a G-major or Bm-flat-six sound) and an **Em colour at 0:24** leading into the bass E at 0:28. Alternation of 4-s slices: Bm, G, Bm, Bm, G, Bm, Em. This agrees with [WN win_0000] ("Bm with flat-sixth G") and [WN win_0020] (E-dominant at 0:26-0:32). High confidence that G is present; medium for "chord change" vs "pad shimmer".
- The intro therefore previews the later vocabulary: i, VI (G) and iv (E) before the bass has even entered.
- The "lead" notes B2/G2 and B4/C5 in [LN] come from a vocal stem with no voice; ignore them as melody [WN win_0000]. Confirmed.

### 3b. Loop A, 0:28-2:36 (iv-VI-III-iv-VI-III-i)
- Cycle of 28 s. The listener hears: rock-solid E (open, suspended over the Bm pedal), a lift to G, a further lift to D (the brightest chord, the relative major), then the whole thing again, and finally B, a drop to the tonic that closes the 28-s sentence. Rising roots E, G (+3 semitones), then D (a step back down a fourth to the pivot) and B gives an "ascend and fall home" shape. Interpretation, medium.
- The "other" stem on the B-bass bars (0:52, 1:20, 1:52, 2:20) shows B plus F#, with D weak or absent on some [P1: 0:52 B 1.00, E 0.79, G 0.69, D 0.61; 1:20 E 0.75, G 0.54]. That explains the chord file's "B" labels. **I do not accept B major (a major third D#) as the harmony of these bars.** D# is elevated everywhere in the mix chroma (0.27 at 0:53, 0.45 at 3:00, 0.42 at 4:49 [P2]), including at clearly minor places where D is 0.49, so D# is most likely the fifth overtone (about +386 cents) of a loud, distorted B and not a chord tone. [WN win_0040]'s "B major dominant pull into Em" is therefore low confidence; what the data support is "B with a bare fifth (B-F#), third unstated" (power-chord colour), as suggested by [WN win_0100].
- Em at 1:22-1:29 for 7 s [CH; WN win_0080] and its pedal over speech is the bass-less 1:24-1:28 hole. The harmony there is the pad alone: E+B+G, an Em chord, as the "other" chroma shows (1:24 E 1.00, B 0.55, G 0.44 [P1]).
- At 2:08 there is a drum fill [WN win_0120] on the E bar (E bass at 2:08), marking the half-cycle (the second E-G-D group); it is also the point where the "other" stem chroma lights D+F#+B at 2:00-2:12 [P1], so the D chord region is wide and bright here. Medium.

### 3c. Loop B, 2:36-4:40 (i-VII-III, B-A-D)
- 12-s cycle repeated about 17 times. Bass roots B, A, D [P1, P2]. This is a very stable minor loop. Over it, the "other" stem is B-led (B 1.00 in every slice) with F#/D/A as the second voice; on the A bars the chroma shows A and B both lit (e.g. 3:04 A 0.78 and B 1.00; 4:04 A 0.88; 4:16 A 0.97, F# 0.97), meaning the upper layer does not follow the bass to A but keeps B, so the sound on the A bars is Bm with A below (Bm7/A, mild and suspended). On the D bars, the "other" shows D, F# lit with B (Bm/D; or D major with an added sixth). I could not separate "B-D-F# over D bass" (Bm/D) from "D-F#-A" (D major) in several slices (e.g. 2:52 D 1.00 F# 1.00 A 0.95 B 0.78 looks like D major; 3:44 B 1.00, D 0.93, F# 0.81 looks like Bm), so the D bar flips between D major and Bm/D. Medium-low on that.
- The brief extra labels in [CH] (Am, F#m, Em flashes at 2:41-2:46, 4:00, 4:12, 4:29-4:36, 4:42) are short chroma flickers of a few hundred ms each; none is supported by a bass root. The bass stays B-A-D. I treat them as passing tones or tracker wobble. Low-medium.
- A faint E on the "other" stem occurs in many B-bar slices (0.40-0.74, e.g. 4:16 E 0.71, 4:28 E 0.79 [P1]). A fourth (E) over B/F# gives a sus4 colour, consistent with the open fourth heard in loop A; interpretation, low-medium.
- Anything that sounds like movement across 2:36-4:40 therefore comes from rhythm, texture and the voice, not from new harmony; [WN win_0220] and [WN win_0240] say this too. Where they claim an A-B-D "open dyad" at 4:05-4:09 (chroma B and A, D absent), I agree with the observation (chroma: only B and A on "other" at 4:04: B 1.00 A 0.88 F# 0.85 D 0.73; the third is not absent in my slice, so I put this at low confidence).

### 3d. Ending, 4:40-5:03
- 4:40-4:48: bass A (4:40) then D (4:44), the last two clear roots, then flat bass chroma [P1]; chord track Bm 4:45-4:48 and a "B" flash at 4:48-4:49 [CH]. The "other" stem collapses onto B+F# with little else from 4:36 on (4:36 B 1.00, F# 0.55, D 0.52; 4:48 B 1.00, F# 0.63, D 0.31 [P1]), i.e. a bare B-F# drone, thinning from Bm toward an open fifth. High confidence that the harmony reduces to B (and F#) in the last 25 s; medium that this is an intentional winding-down.
- Final chord at 5:01-5:03: mix chroma B 1.00, F# 0.33-0.39, D 0.36 vs D# 0.32 at the last hit [P2] (D and D# are indistinguishable). The chord file says "B" (major). **The third cannot be resolved**; a bare B-F# power chord is the most economical reading. A Picardie (major) ending is not supported. [WN win_0300] is right to flag this as uncertain; I agree, low confidence for any claim of major.

## 4. Mode and key evidence (summary)
- B minor throughout; the song-level estimate B minor 0.88, D major 0.73, G major 0.64 [AF] is the relative-major-and-submediant family of the same seven notes. The per-30-s estimate wanders to E minor (30-60 s) and G major (60-150 s) [AF] because the bass spends most of loop A on E, G and D (iv, VI, III). That is bass movement over a B pedal, not a key change. I would rate "modulation to G or E minor" as unsupported (high confidence).
- Tonic strength: bass B appears only once per 28 s in loop A (so the tonic is "arrived at" rather than stated), and every 12 s in loop B. In loop A the home chord is therefore delayed, which gives that section its drifting, floating, "away from home" feel; interpretation, medium.
- Harmonic rhythm: one change every 2 bars (about 4 s) all the way through. Very slow, therefore the music is heard as a drone with colour changes rather than as a chord progression.

## 5. Melody, riffs and motifs
- **No sung or instrumental melody was found.** The vocal stem is speech/sample material for most of the file (see voice specialist; [WN] throughout). The lead tracker's "notes" [LN] are bass bleed (D2-B2), speech intonation (F#2-E3), or noise.
- I tested the "other" stem directly for a melodic top line in 4:28-4:38, where [WN win_0260] reads an A5/G#5 semitone "trill" motif from [LN]. pYIN on the "other" stem (200-1500 Hz) returns D4, F#4, E4, C#4, A3 in runs of 3-8 frames, i.e. chord tones and neighbours of Bm/D, and no A5/G#5 [P2]. The vocal stem is voiced only 28% of that stretch. **The A5/G#5 figure is therefore unconfirmed and probably a tracker artefact on a vocal chop**; the chromatic content (G#, A#, D#) the notes in [WN win_0240/0260] list is not diatonic to B minor, supporting this. Low confidence in any melodic motif; I recommend discarding it as a motif.
- What does repeat is **rhythmic-harmonic**: the bass note held for 2 bars with short bursts and upper-harmonic "picked" attacks about every 0.35-0.5 s [WN win_0160/0280]; this is an ostinato figure on a drone, not a tune. The "other" stem striping is consistent with repeated chord stabs or arpeggio on the Bm pedal [WN win_0160, 0220], but note-level shape cannot be extracted. Low confidence on arpeggio vs strummed chords.
- The nearest thing to a "melody" is the **bass-root contour**, E to G to D, and its rising-then-falling shape: +3 semitones (E to G), then down a fourth to D, repeated, then B. In loop B it is B to A to D: -2 semitones, then up a fourth. Both are plain, singable three-note shapes, and the E-G-D figure is very close to a rock "power-chord riff" root pattern. Medium (the contour is measured; calling it a riff is my interpretation).
- Chromatic climb G#4-A4-A#4 at 4:42.7-4:43.5 [LN; WN win_0280]: three semitone steps in under a second, probably a vocal glide or noise; one-off, low confidence.

## 6. How it feels (harmonic reasons)
- Intro: a B-minor pad with a G colour; dark but not grim, "wistful" (the flat sixth over a minor tonic). Medium.
- Loop A: yearning and rising. The bass E under a B-minor pedal is unresolved, G and D lift (the major-key relative) and B at the end drops back. A long-breathed, slowly unfolding sound. Medium.
- Loop B: heavier, more fixed, anthem-like, "locked". The three-chord i-VII-III is the classic modal-rock cycle; a short loop repeated for two minutes produces hypnotic, motorik momentum, with intensity coming from sound and rhythm, not harmony. Medium.
- Ending: harmony empties out to a bare B-F# drone and a hard stop on B: an unresolved, flat, sombre close, with no cadence (no V-i, no A# leading tone). Medium.

## 7. Limits and cautions
- Instrument identity (guitar, synth, organ) cannot be told. Chord quality (major vs minor third) is uncertain wherever the D/D# overtone ambiguity applies, which is wherever a loud distorted B-based tone sounds.
- Demucs "bass" may include kick and low synth; "other" contains everything else including the pad, so chroma of "other" mixes several parts.
- [CH] is a template-matching triad labeller; labels shorter than about 1 s should be disregarded.
- Bass-root detection after 4:48 is meaningless (flat chroma).
- Speech pitch is not melody.

## 8. Three questions for fellow specialists
1. **Rhythm:** I measure beat period about 0.50 s (autocorrelation peaks at 0.51, 1.00, 2.00 s) and read each bass note as 2 bars of 4/4 at about 121 BPM, rejecting the tracker's 161.5 BPM (0.37 s). Does your drum-onset grid confirm a 4/4 bar of 2.0 s with the snare/kick pattern, and where does bar 1 of each 2-bar chord fall (so I can say whether the chord change lands on the downbeat)? Also, what is the exact drum-fill/stop position near 2:08 and 1:24-1:28 relative to the bass cycle?
2. **Sound:** The "other" stem keeps B as a near-constant top pitch class while the bass moves. Does your timbre and spectral evidence support one sustained distorted layer (guitar/synth wall, with D# as a B overtone) or two layers (a pad plus a rhythmic stab layer)? And is the bass distorted/overdriven enough that its own harmonics explain the D#/third ambiguity I see?
3. **Voice:** Are the vocal-stem pitched events at 4:29.9-4:35.6 (A5/G#5 alternation in [LN]) and 4:42.7 (G#4-A4-A#4) real voiced material, such as a chopped sample or a sung "hook", or artefacts? If real, what pitch contour does your own pYIN give, and do the entries line up with the 4-s bass-root grid (B, A, D)?

(Further for form and feeling: the harmonic section boundaries are 0:28 [bass in], 1:24-1:28 [hole], 2:36 [loop A to loop B], 4:40 [bass out]. Please check these against your form map.)
