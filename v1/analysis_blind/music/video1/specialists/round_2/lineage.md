# video1: LINEAGE specialist, round 2 (blind, measurements only)

Evidence keys as round 1 (WN, MV, CL, BT, LV). I read all seven round-1 files and the round-2 files already written (harmony, rhythm, sound, voice). New run: `v1/scripts/agents/lineage_r2.py` (drums.wav, 16-step fold on rhythm's grid, period 0.7692 s, phase 0.164 s; low 30-150 Hz, mid 150-2500 Hz, hi 5-10 kHz; values normalised per band). I cannot hear. Times m:ss.

## 1. Questions put to me, answered

**Rhythm Q: backbeat (snare on 2 and 4 at 156) or half-time at 78?** Neither; rhythm's round-2 finding agrees with mine. My own fold of 0:33-1:48 over 16 slots (slot 0 = a click beat):
- mid band: 0.93 0.46 0.41 0.47 | 0.87 0.57 0.02 0.42 | 0.99 0.44 0.48 0.07 | 1.00 0.48 0.49 0.16. The click is strongest on slots 0, 4, 8, 12, i.e. every beat, with no weighting of beats 2 and 4 over 1 and 3.
- low band: 0.22 0.85 0.58 0.93 | 0.28 0.99 0.07 1.00 | 0.20 0.88 1.00 0.15 | 0.19 0.83 1.00 0.19. The low thumps avoid the beat slots (0.19-0.28) and fall on the off-sixteenths (slots 1, 3, 5, 7, 9, 10, 13, 14).
So there is no rock backbeat. The pattern is an even click on every beat with low thumps in the gaps. This is the opposite of a rock or motorik kit, where the kick sits on the beat and the snare answers on 2 and 4. High-medium confidence on the shape, which relies on demucs separation and on slot 0 being a true beat (rhythm's grid, which agrees with beat_times.json).

**Rhythm Q (loop or human?)** Rhythm says loop-like (bar similarity 0.81-0.85, no drift), and my fold is consistent. I raise one caution: demucs leakage between stems could fake some of the "gap" thumps, so "programmed" stays medium, not high.

**Sound Q: guitar or synth? Is the roll-off a filter?** Sound corrected itself: the roll-off varies by block (6.5-13 kHz), so it is not a fixed brick-wall. I withdraw my round-1 use of the "8 kHz hard roll-off" as evidence for a band-limited or production-filtered source. Sound leaves guitar versus synth open, leaning guitar-amp-like (low). I accept that. My lineage claim shrinks accordingly: "post-rock grammar" rests on the build-and-subtract gesture, not on a proven guitar.

**Harmony Q: modal vamp or functional?** Harmony says modal, Mixolydian-leaning D drone with a b7 (C) as the strongest non-tonic after the fifth (1:27-1:40 and 2:48-3:06: C 0.61-0.69, thirds 0.35-0.40). I take this as the best new lineage evidence. A D drone with a flat seventh and an open fifth, no third, no V-I, is the harmonic language of drone and riff music (post-rock, krautrock, and also stoner/sludge and some electronic), not of pop or blues-rock (which would give a stated third and a V). It also bears on "stadium rock": that needs a stated major third and cadences, which are absent. Medium. Harmony's own caveat stands: distortion intermodulation on a D5 power chord can fake a C (see question 1 below).

**Form Q: do my section edges match?** Rhythm shows eight edges (1:06.4 to 2:47.8) all within 0.11 beat of the same beat of the bar. A band playing loosely would not land that cleanly; this strengthens the "sequenced or DAW-arranged" reading in my hypothesis C (medium-high that the arrangement was assembled on a grid; unproven whether the instruments were played).

## 2. Corrections to my round 1

1. **Withdrawn: "drum stem is kick/tom-led, a snare-like crack present".** The fold shows no backbeat crack. The click is a flat every-beat tick, low thump in the gaps. I now describe the kit as "even click plus syncopated low thump", not rock kit.
2. **Weakened: motorik (hypothesis B).** Motorik is defined by a kick on the beat with a snare on 2 and 4 and steady hat. Here the low thumps avoid the beat and no backbeat exists. What survives is the hypnotic fixed groove and the long layering, not the beat. Downgrade to low-medium for "motorik beat", medium for "krautrock-adjacent repetition".
3. **Withdrawn: the 8 kHz roll-off as era or source evidence** (see Sound above).
4. **Rejected by Sound's measurement: "vinyl/tape/lo-fi" as a lineage trait.** The mix reaches 18 kHz, dry and clean; the old-sounding element is the voice only. The tape-collage flavour belongs to the sample, not to the production.

## 3. What this does to the lineage verdict

- The strongest lineage features, in order: (1) instrumental, non-sung, build and subtract arrangement (high); (2) fixed-grid loop with even click and low off-beat thumps, which fits programmed or heavily processed drums more than a rock kit (medium); (3) D drone with b7 and open fifth, modal, no cadence (medium); (4) archival-style spoken-word sample as the "lead" (high on the device; the voice specialist's bar-paced place-name list at 2:15-2:36 is a collage-lineage detail); (5) loud modern dry master with a pure 42.66 Hz sine sub (medium-low for "2010s on", Sound's own caveat is "any time from the late 1990s").
- Net: an **electronic-rock hybrid in the post-rock/cinematic tradition**, closer to "sequenced drums plus saturated riff layer plus sample" than to a conventional band. I have not got evidence for any single genre name; the nearest family is sample-led instrumental electronic rock. Confidence: medium that it is hybrid; low on which side (rock band or producer) did the playing.
- The final section (2:48-3:08) behaves differently in my fold: low band 0.18 0.02 1.00 0.96 | 0.19 0.03 0.82 0.75 | 0.22 0.11 0.81 0.83 | 0.33 1.00 0.14 1.00, and the click is no longer isolated on the beat (hi band 0.5-1.0 on most slots). Drum, bass and "other" coincide there (feeling's note on a 0.186 s median gap). So the pulse moves from "click on the beat, thumps between" to "dense, clustered thumps", a pattern change that suits the climax role form and feeling give this passage. (Window is only 20 s, medium-low.)

## 4. Connections to other specialists

- **To rhythm and form:** the even-click-plus-gap-thump pattern means the music has no backbeat to cue the bar. The listener's bar sense therefore comes from the bass entries (every 8 beats) and layer changes landing on one bar position. That fits the observation that structure, not the drum groove, carries the form.
- **To feeling:** the mechanical, backbeat-free pulse supports "urgent, cold, trance-like, endurance" far better than a rock groove would. A modal D drone with b7 and no third gives "open and neutral with an edge", agreeing with harmony: the human warmth, if any, comes from the voice and from the absence of resolution (tradition: documentary score).
- **To voice:** archive-style speech over a loop is a documentary-score device; the sparse speech bursts leave the drone unresolved, as in drone/post-rock pieces that use spoken samples for narrative.
- **To sound:** the fixed-pitch sub and grid-locked drums argue for at least one sequenced element, which is where I put "hybrid". I cannot tell whether the "other" layer is played or sequenced.

## 5. Not measurable

Instrument identity (guitar, synth, kit, machine), era, whether the voice is archive, whether the production was performed live or built in a DAW, and any artist or scene. I give resemblances only.

## 6. Two new questions

1. **Sound:** harmony asks whether C (0.6-0.7) in the "other" stem is a played flat seventh or intermodulation from distortion on the D-A fifth. Can you test that from the harmonic spacing, e.g. whether C appears at the same level in the thin, low-distortion blocks (1:15-1:27, 2:00-2:13) as in the dense ones? It decides whether I call the harmony "Mixolydian drone music" or just "distorted power chords".
2. **Rhythm:** in my fold the low thumps sit off the beat while the click sits on it. Is that a stable two-layer pattern (click layer, thump layer) that you can separate in the onset data, with the thumps sometimes on slots 2 or 10 (0.58, 1.00) instead of the others? And does the 2:48 pattern change (thumps at slots 2, 3, 6, 7, 10, 11, 13, 15) also hold in 2:48-3:07 beyond my 20 s fold? That decides whether the climax is a new drum pattern or the same one with the "other" layer thickening it.
