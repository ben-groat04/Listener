# Video2 (Elfstedentocht Part 2): functional harmony

Written for task T6. Tags: **OBSERVED** (read straight off a file or stem, no interpretation), **HEARD(measured)** (a number measured from the audio stems by an algorithm; no listening), **INFERRED** (my reading of those numbers). Nothing here comes from listening. `music_reading.md` is untouched; where this file disagrees with it, see "Disagreements" below.

## Summary (plain language)

- The bass plays one note per two bars (4 s) and moves through a fixed loop. For the first two-and-a-bit minutes (loop A) the notes are E, G, D, E, G, D, then a short B, repeating every 28 s. From 2:36.6 the loop changes to B, A, D, repeating every 12 s (loop B), eleven times, until the bass is gated into stabs at about 4:50.
- The pad (the "other" stem) does not follow the bass. It sits on B (with F# and often D or G) nearly all the time. So the bass supplies the movement and the pad supplies a fixed colour.
- Which note is "home" is open. B is the pad's centre and the whole-song estimate (B minor 0.882 against D major 0.731, not ambiguous as a pair of candidates, but B minor and D major are relative keys sharing the notes). E is the bass's first root in loop A, though E, G and D each get equal time there (8 bars each before the hole, 10 each after). Both readings are given below.
- The change into loop B at 2:36.6 to 2:36.75 is a harmonic event: the bass stops visiting E, G and D and starts on the pad's own B.
- The bass is silent for 0 to 28 s (the pad and a few low thuds play alone), for about 3.5 s at 1:25 to 1:28.5 (the hole), and between stabs from about 4:48.5 to the end. No root claims are made for those stretches.
- What cannot be known from stems is listed at the bottom.

## Method and grid

- Bass roots: `pyin` (30 to 250 Hz) on `stems/bass.mp3`, one RMS- and voicing-weighted pitch-class histogram per 2.000 s bar; octave ignored; also one per 0.5 s quarter-bar (the `beat_roots` field). A bar with the bass more than 40 dB below its maximum, or no voiced frames, has no root (`root_claim: false`). Confidence = share of the weight on the top pitch class.
- Pad chroma: `chroma_cqt` mean per bar on `stems/other.mp3`, scaled so its largest class is 1.0.
- Bar grid: `data/video2/sync/grid_120bpm.json` (120 BPM, bar 2.000 s, downbeat anchor 88.6165 s from 246 kicks). It is a fit to the kicks of 1:28.6 to 5:00; bars before 1:28.6 are extrapolated backwards and are [L]. Bar times in the JSON are that grid.
- Data: `v1/data/video2/music_views/bass_roots.json` (152 bars, plus `events` and `loops`). Helper scripts (scratchpad, may be cleared; regenerate from the method above): `/tmp/claude-0/-home-user-Listener/cb832643-599e-5a16-8ae7-147fc9b20f96/scratchpad/bass_roots.py`, `post.py`, `probe.py`.
- Resolution: a pyin window is 0.5 s at best, with some detector latency, so a slot edge is good to about 0.25 s. Slots of 2 bars (4 s) are trusted; finer claims are marked.

## Loop structure with times

| Span (JSON bar starts, s) | Bass roots (bar pairs) | What | Tag |
|---|---|---|---|
| 0 to 28.0 | none | Bass silent (-77 to -83 dB re its maximum in every bar from 0.6 to 24.6; -60 dB in the bar at 26.6). Pad only. No root claim. | HEARD(measured) |
| 28.0 | E | Bass enters on E at -13 dB, 0.6 s before the extrapolated bar line at 28.62 (bar 15) [L, grid extrapolated]. | HEARD(measured) |
| 28.6 to 84.6 | E E, G G, D D, E E, G G, D D, B B | Loop A before the hole (bars 15 to 42): two 28 s cycles, 28.6 to 56.6 and 56.6 to 84.6. Each is E-G-D, E-G-D (6 bars, 12 s per cell) then a B slot (B at 52.6 to 56.6 and at 80.6 to 84.6). | HEARD(measured) |
| 84.9 to 88.5 | none | The hole: B fades out (-23 dB at 84.25, -39 at 84.75, floor from 85.0), bass silent about 3.5 s, E returns at 88.5. No root claim. | HEARD(measured) |
| 88.6 to 156.6 | E E, G G, D D, E E, G G, D D, B B (112.6 to 116.6); E-G-D x2 again to 140.6; B B (140.6 to 144.6); E E, G G, D D (144.6 to 156.6) | Loop A after the hole (bars 45 to 78): same cell. The third cycle has no B tag at its end; the next bass slot after 156.6 is the loop B's B. | HEARD(measured) |
| 156.6 to 276.6 | B B, A A, D D (x10) | Loop B (6 bars, 12 s each). First B is measured at 156.75 (D until 156.5), so the change falls between 156.6 (bar line) and 156.75. | HEARD(measured) |
| 276.6 to 288.6 | B B, A A, D D | 11th and last loop B cell (bars 139 to 144; cells 1 to 10 are the row above). Bass level falls about 7 to 10 dB (bars 139 and 140 at -18 and -19 dB re max against -7 to -9 before). | HEARD(measured) |
| 288.5 to 300.6 | stabs only | Gate: the last sustained note ends about 288.5; first stab at 290.25 (A at onset, B at 290.5), then 292.5 (B), 294.25 (A then B) and so on about every 2 s, floor (-55 to -65 dB) between. Stab pitch is mainly B with an A at some onsets; the bars are below the -40 dB rule, so no per-bar root is claimed. | HEARD(measured) |
| 300.5 to 304.2 | none, then tag | Last stab B at 300.5, floor from 301.0; end tag A at 302.25 then B at 302.5 and 302.75 (T2 onsets 302.34, 302.60, 302.84). Tag notes are three short hits, no root claim. | HEARD(measured) |

Loop A cell by itself: E-E-G-G-D-D (bars of 2 s each pair). The cell repeats; every second cell is followed by a B slot. Loop B cell: B-B-A-A-D-D. A short extra note appears in the last 0.5 s of some slots (`beat_roots`): in loop B all 10 D slots end with E there (for example the bar at 166.6, 0.72 weight on D for the whole bar); in loop A this E appears in only 2 of 20 D bars, and A in the last quarter of 5 of 18 G bars [HEARD(measured); reading them as passing notes or pickups is INFERRED].

## Roman numerals, both candidate tonics

Same seven-note set (B C# D E F# G A) in both columns, so the numerals only relabel.

| Loop | Bass root | B as tonic (B Aeolian / minor) | E as tonic (E Dorian or E minor) | Tag |
|---|---|---|---|---|
| A | E | iv | i | INFERRED |
| A | G | VI | III | INFERRED |
| A | D | III | bVII | INFERRED |
| A | B (tag) | i | v | INFERRED |
| B | B | i | v | INFERRED |
| B | A | VII | IV | INFERRED |
| B | D | III | bVII | INFERRED |

Loop A under B: iv - VI - III - iv - VI - III - i (28 s). Under E: i - III - bVII - i - III - bVII - v. Loop B under B: i - VII - III. Under E: v - IV - bVII. There is no leading tone (no A# or D#) and no V to I in either reading. With relative majors the same labels read G as I, E as vi, D as V and B as iii (loop A under G), or D as I, B as vi, A as V (loop B under D).

## Key candidates and ambiguity

| Measurement | Top two | Gap | Verdict | Tag |
|---|---|---|---|---|
| Whole-song, whole mix (`audio_features/summary.json`) | B minor 0.882, D major 0.731 | 0.151 | not ambiguous (but relative keys) | OBSERVED |
| Pad (other-stem) mean chroma, loop A (both halves) | B minor 0.982 / 0.962, D major 0.600 / 0.647 | 0.38 / 0.32 | B clear | HEARD(measured) |
| Pad mean chroma, loop B | B minor 0.919, D major 0.668 | 0.25 | B clear | HEARD(measured) |
| Bass-root bar counts, loop A pre-hole | G major 0.796, E minor 0.744 | 0.052 | just outside the 0.05 rule; G major and E minor are relative keys sharing every note, so the bass cannot separate them in practice | HEARD(measured) |
| Bass-root bar counts, loop A post-hole | G major 0.788, E minor 0.732 | 0.056 | as above | HEARD(measured) |
| Bass-root bar counts, loop B | D major 0.724, B minor 0.654 | 0.070 | outside 0.05, again a relative pair | HEARD(measured) |

The Krumhansl-Schmuckler scores on the bass use only three or four pitch classes (counts of bars), so they are crude and a pointer only. Overall the tonic is **ambiguous between E and B for loop A** (pad says B, bass says E), and **B-leaning for loop B** (pad B, bass returns to B every 12 s) [INFERRED]. Neither is shown by the data to be what a listener hears.

## Pad chroma against bass roots

| Span | Bars with a root | Pad's strongest class = bass root | Pad's strongest class is B | Mean pad chroma at the bass root | Tag |
|---|---|---|---|---|---|
| Loop A before the hole (28.6 to 84.6) | 28 | 6 | 21 | not separately computed | HEARD(measured) |
| Loop A after the hole (88.6 to 156.6) | 34 | 7 | 27 | not separately computed | HEARD(measured) |
| Loop A, both halves | 62 | 13 | 48 | 0.75 | HEARD(measured) |
| Loop B (156.6 to 276.6) | 60 | 34 | 45 | 0.94 | HEARD(measured) |

In loop A the pad's strongest class matches the bass root in only 13 of 62 bars (8 of them are B bars). The pad's strongest class is B in 48 of 62 loop A bars and in 45 of 60 loop B bars; the other 15 loop B bars have A or D on top (for example 172.6 to 178.6, 220.6 to 222.6, 232.6 to 236.6, 248.6 to 250.6 and 258.6 to 262.6); in 14 of those 15 the top class equals the bass root, so the pad's second colour sometimes moves with the bass, not a fixed B. The pad as a whole is a B pedal with a changing second colour [INFERRED]. Stacked, the bass plus pad notes read as E over B-D-F# (Em with the ninth and no third, or Bm/E), G over B-D-F# (Gmaj7), D over B-D-F# (D6 or Bm/D); in loop B Bm, Bm/A and Bm/D [INFERRED, voicings unknown].

## Harmonic events

- **28.0**: bass enters. HEARD(measured).
- **84.9 to 88.5**: bass-less hole, the pad's strongest class is E in bars 43 and 44 (84.6 to 88.6, pad chroma E 1.0, B 0.58 to 0.48), not B. HEARD(measured); reading it as the pad "answering" the missing bass is INFERRED and weak.
- **156.6 to 156.75: loop A to loop B.** The bass stops visiting E, G, D and sits on the pad's B at the start of each 12 s cell. Under B: iv-VI-III around a pedal becomes i-VII-III. Under E: a tonic bass becomes a dominant bass. Pad and pulse do not change at that moment. HEARD(measured) for roots, INFERRED for the label.
- **276.6**: bass level falls 7 to 10 dB over bars 139 and 140. HEARD(measured). (`music_reading.md` says the pad's D third fades about here; in the bar chroma, bars 139 and 140 have B first with D 0.51 and F# 0.55 as second classes; not re-tested beyond that.)
- **288.5 to 300.5**: bass reduced to stabs on B (A at some onsets). No loop B roots after 288.5. HEARD(measured).
- **302.25 to 302.75**: end tag A, B, B. HEARD(measured).

## Disagreements and refinements against earlier loop claims

1. Loop A bass roots E-E-G-G-D-D / E-G-D plus a B tag: **confirmed** (28 s cycle, two E-G-D cells then a B slot; the third post-hole cycle ends at 156.6 with E-G-D and no B tag).
2. Loop B B-B-A-A-D-D from about 2:36: **confirmed**, 11 cells of 12 s from 156.6 to 288.6.
3. Change at about 2:36.8: measured at **156.6 to 156.75** (first B at 156.75), within the 0.25 s resolution of the earlier figure; not a disagreement, but the 156.8 figure is not directly supported by this measurement.
4. `music_reading.md` places a B slot "at 1:20 to 1:28". Measured: B sounds 80.6 to about 84.9 (1:20.6 to 1:24.9) and the bass is **silent from 85.0 to 88.5**, so the last 3.5 s of that span are not B.
5. `music_reading.md` says the bass roots follow B-A-D "until about 4:48.5" and the gate begins at 4:48.55. Measured: the last sustained note ends at about 288.5 (4:48.5), but the **first stab is at 290.25**, with silence at the floor between 288.5 and 290.25. It does not contradict the gate time; it adds the 1.7 s of near-silence before the first stab.
6. Pad "B-F#-A" after 4:48.8: bar chroma for bars 145 to 150 (288.6 to 298.6) has B first and F# second (0.57 to 0.64); A is not in the top two, so "A" is not confirmed by this measurement.

## Cannot be known from stems

- Instrument identity (bass guitar, sampled bass or synth bass; the pad's source).
- Voicings, inversions and which notes are doubled; the pad chroma shows pitch classes, not stacks.
- Whether the listener hears E or B (or G, or D) as home; no listening was done.
- Octave of the bass roots (pyin jumps octaves; octaves ignored).
- Bass roots before 28.0 and between 85.0 and 88.5 (silent), and between stabs after 288.5 (gated).
- Whether the short extra note at the end of D and G slots is a passing note, a pickup or detector bleed.
- The grid before 1:28.6 is extrapolated; bar numbers before that are nominal.
