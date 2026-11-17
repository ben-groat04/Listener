# video2: HARMONY specialist, round 3 (final, blind, measurements only)

Evidence keys: [CH] chords.json; [P3]/[P4] my round-2 probes (`v1/scripts/agents/v2_harmony_r2.py`, `v2_harmony_r2b.py`); **[P5]** new `v1/scripts/agents/v2_harmony_r3.py` (bass level and pYIN around the pickup notes; bass and "other" chroma at 4:10-4:49); [R2-x] another specialist's round-2 file. I cannot hear; every label is a pitch-class measurement. Times m:ss.

## 1. Answers to questions put to me in round 2

**Sound Q1: are the pickup notes (A before D, E before B) a different, shorter, more percussive note, and is there a glide?** [P5], bass stem:
- **No glide.** pYIN on the bass stem before the 1:48 / 2:04 / 2:16 / 2:32 D arrivals reads G2 (about 98 Hz), then A2 (about 110 Hz), then D2 (about 73 Hz), with no intermediate pitches. Before the loop-B B arrivals (2:48.1 to 4:36.1) it reads D2 (73 Hz), E2 (82 Hz), then B1 (62 Hz), again as steps. Discrete notes, not slides (medium-high).
- **Level: the pickup is not quieter or different in kind.** In 0.1 s RMS the bass sits at about -11 to -14 dBFS on held roots and on the pickup, and drops to -22 to -32 dB for about 0.2-0.4 s at the note boundary (e.g. around 3:00.1: -12, then -28, then -18). That dip is a re-articulation gap present at every change, not a special "ghost" level. So the pickup is a **short sustained note (0.5-0.9 s) with a gap each side**, not a percussive stab (medium-low; 0.1 s frames are coarse and stem separation smears attacks).
- Before 1:40 (1:15.4 and 1:35.7) the bass is much quieter (-21 to -30 dB) yet the same A-then-D step occurs, so the pickup figure predates the loud bass (medium).

**Rhythm Q2: did the whole band shift by a quaver after 1:28.6, or only the bass?** [P5] cannot settle it. I have: chord arrivals about 0.25 s later against the 0:00.14 grid in the second half (low-medium, R only 0.3-0.5 [P4]); [R2-form] counts bars from 0:28.14 first half and 1:28.61 second half, the same statement as "the lattice moved at the drop"; and the 1:24.5-1:28.0 stop is two bars at 120 BPM, so bar 1 lands on the returning hit. Simplest reading: the **bar was re-counted at the drop and the bass follows the new bar**; it is not off-beat against the kick in one half. Medium-low; Rhythm's drum fold would decide it.

**Voice Q: do bass or "other" contain a G# at 4:29-4:49 to justify the voice's G#?** [P5] chroma (normalised to the strongest pc):
- Bass: G# 0.15 (4:10-4:18), 0.20 (4:29-4:36), 0.29 (4:36-4:44), 0.18 (4:44-4:49); G 0.12, 0.11, 0.20, 0.11.
- "Other": G# 0.37, 0.40, 0.20, 0.21 against G 0.39, 0.39, 0.25, 0.30.
- G# is **not** a stable chord tone: bass G# stays under 0.3, and "other" has G and G# about equal and well below B, F#, D, A (0.5-1.0). The bass roots stay B-A-D on schedule. So the voice supplies its own G#/A inflections over an unmoving Bm; **any Dorian colour belongs to the voice alone** (medium-low; the voice is 16% voiced there and the pitch tracker may slide). The bass A# 0.57 at 4:36-4:44 is the same overtone/leakage issue as the earlier D#, not a chord note.

## 2. Corrections after reading round 2

- **Form (4:40):** I adopt Form's 4:36.6 (outro start) and 4:48.6 (one stab per bar). My "bass out at 4:40" was loose: A (4:40.9) and D (4:44.7) are the last full B-A-D cycle.
- **Form (bar counts):** loop A is 14 bars (28 s) and loop B 6 bars (12 s), consistent with [R2-form] counted from 0:28.14 and 1:28.61.
- **Rhythm:** accepted that the hat 3+3+3 is a programmed cross-rhythm and that the grid is one stable 0.5 s pulse. My "second cycle (3.4 + 0.5 s)" is a bass-phrase unit only, not a competing pulse.
- **Sound:** accepted that D# is plausibly a harmonic of a moderately saturated bass ([R2-sound]); I keep "overtone, not a played major third" at medium.
- **Voice:** I withdraw "rising inflection of a sample" for 4:10-4:15: [R2-voice] shows real voiced pitch at 4:29-4:36 (voiced fraction 0.67). It is a real voice, simply untied from the chord grid.
- **Lineage:** I make no guitar-versus-synth claim; the harmony is a Bm triad wall either way.

## 3. Connections to the other specialists

- **Form:** the harmonic map is the section map. Loop A withholds the tonic; from 2:36.6 B-A-D returns it every 12 s; the 3:36.6-3:48.6 ramp changes brightness, not notes. After 2:36 form is carried by register, voice and layers, not harmony.
- **Rhythm:** a jitter-free four-on-the-floor grid under roots held two bars: pitch moves slowly, drums repeat constantly. The beat-4 pickups are the only anticipation against that grid.
- **Sound:** the 2:47 lift is an octave move onto a clean Bm triad ([P3]); the later swell (C5-C7 share 0.20 to 0.44) is brightness. The bass is the only harmonic mover.
- **Voice:** speech is not pitched to the chords; chops float (3:28-4:22) then lock to beat 2 of each bar (4:44-5:00 [R2-voice]), matching the bass thinning to one stab per bar at 4:48.6.
- **Feeling:** yearning without arrival comes from a withheld tonic, the minor-sixth colour, no leading tone and no cadence; the plateau/trance feel after 1:40 from a fixed floor and slow loops ([R2-feeling]).
- **Lineage:** pitch set B D E F# A plus G suits an Aeolian rock vamp or cinematic post-rock; harmony cannot separate them.

## 4. Settled conclusions

- **Key and mode (high):** B minor, Aeolian (b6 G present; no sustained G#, A#, D# or F#), a B-minor-pentatonic palette with G as the single added colour. No real dominant and no cadence, even in the last 25 s.
- **Two bass loops (high on notes, medium on pickups):** loop A (0:28-2:36, 28 s repeat, loud from 1:40) is E-G-[A]-D, E-G-[A]-D, B in two-bar blocks; loop B (2:36.6-4:36.6, 12 s repeat) is B-A-D-[E]. The bracketed A and E are 0.5-0.9 s stepped (not slid) pickups on the last beat. Loop B is the simpler, more tonic-heavy cousin (B 13% of bass frames in A, 34% in B).
- **Upper layer (medium-high):** "other" holds a Bm-centred triad wall throughout; the 2:47-2:50 lift is an octave move onto a clean Bm triad, and later growth is height and brightness, not new notes.
- **Voice versus harmony (medium-low):** speech is not pitched to the chords; chops wander G4/G#4/A4 irrespective of chord; G# is absent from bass and "other" chroma, so Dorian colour at 4:29-4:49 belongs to the voice alone.
- **Feeling (medium):** the harmony holds rather than resolves: tonic withheld, minor-sixth colour, no leading tone, slow roots every 4 s, a final thinning to B and F# with no close. Still pitch material against a constant machine grid gives the yearning-yet-trance feel.

## 5. Limits
Chord thirds, instrument identity, whether pickups are played or sequenced, and whether A#/D# traces are overtones cannot be measured here. Bass-root snapping is about +-0.15 s; vocal pitch rests on 11-67% voiced frames. Nothing here is a heard chord.
