# t_birdwalk: HARMONY specialist, round 3 (blind, measurements only, final)

Keys: H2 = my round 2; R2/S2/F2/V2/L2/FE2 = other specialists' round-2 files; MY3 = new script v1/scripts/agents/harmony_birdwalk_r3.py (frame-by-frame strongest-peak pitch class, 150-2000 Hz, of stems_raw other.wav, loudest 40 per cent of frames, n_fft 4096). Timestamps m:ss. Blind: no context.md, research or web.

## 1. Answer to SOUND (Q2): does "other" play a riff order (A to D to E) or a static chord?

MY3, time-resolved:
- 1:02-1:20: A 79 per cent of loud frames, C 6, D 6, B 6. Successive pitch-class changes: D to A nine times, A to C six times. No E.
- 1:40-2:00: A 81, D 8, B 2, C 2. Changes: D to A 15, A to D 9, A to B 4. No E.
- 1:20-1:24: A 92-94, D 6-8. No G, no change of peaks around 1:22.
- 2:56-3:00: A 91, D 9.
- 2:27-2:30: A 73, E 12, D 8, F# 8 (a short stretch, three seconds).
Reading: the layer is A with brief, repeated excursions to D (a fourth above the pedal, a plain 5-10 per cent of frames) and back. That is a tiny two-pitch figure, A with a D neighbour, not a three-note A-D-E riff and not a chord. SOUND's A-D-E averages (164, 293, 331 Hz) are compatible only if E appears in short places such as 2:27-2:30; per-frame data show it is rare (medium). I therefore refine H2: "single repeated pitch" becomes "A with an occasional D; the D visits are too rare and brief to be a melody" (medium). D could also be vocal-formant bleed, since VOICE puts verse 1 on D4 (0:24-0:45); but the visits occur in 1:02-1:20 and 1:40-2:00 too, where VOICE has the voice on G and A-C, so D is more likely the stab layer itself (low-medium).
Answer on the G at 1:22: it does not show in "other". The layer stays A and D through 1:20-1:24. So H2's G lean at 1:22 is vocal only (VOICE's verse 2 centre is G, V2) and I downgrade it again (low).

## 2. Answer to FORM (G leans versus the 12.0 s grid)

FORM computed that all five leans fall within 1.2 s of the grid, but with any time within 6 s of a line this is not evidence, and six real edges (0:12.4, 0:47.2, 0:59.3, 2:11.3, 2:23.5, 2:35.7) have no lean [F2 s5]. I accept that. Combined with section 1 (no G in "other"), I withdraw the "G as signal before a change" hypothesis: it was voice-pitch noise (high-medium that it is not a deliberate harmonic signal). Verse 2's G is simply where the speaker's pitch sat.

## 3. Other answers and corrections

- RHYTHM: no objection to the 12.0 s loop and the 80 BPM half-time grid. Harmony cannot count a bar, as I said; the A pedal gives no downbeat. The D neighbours in "other" (about 9 changes per 18 s at 1:02-1:20, i.e. every roughly 2 s) are the only pitched event I can offer, and they are too irregular to test against a 3.0 s bar by my method (low).
- LINEAGE: my "single note" wording made L2 drop any sample-loop idea. MY3 shows A plus D neighbour; that is still a very small cell, so L2's "one-note pluck, not a melodic loop" survives with the proviso of a D neighbour. CLAP "country" stays discarded.
- FEELING: agreed that harmony gives little emotion. Its "wry, bluesy lean" rests on the hook voice's C over A (VOICE: C about twice as common as C#) and is medium-low; the D neighbour adds a suspended, third-less open feel (fourth and fifth, no third in the instruments), which is neutral (low-medium).
- VOICE: accepted that verse 1 D4 is a natural reciting pitch, not a tuned note (+9 cents), and that the hook's -1 cent offset in all three passes suggests the same take pasted (F2 and V2), not three performances.
- SOUND: the A5 pluck cluster 883-1047 Hz (A5, B5, C6) in 0:40-0:47 re-measured here: A 63, B 18, C 14 per cent, so a short rising-colour cluster of A, B, C exists in the intro/break zone only. It is a 3-note neighbour set, not a progression (medium).
- My own earlier errors now settled: F#m (CH, F's WIN 0180) is residue; the G/D "chord change" at 1:23 does not exist; "A-D-E power chord" is not supported frame-by-frame.

## 4. Connections

- Form: with pitch frozen, the architecture is entirely arrangement (loops, drops, width). Harmony supplies no section signposts, which makes the 1.0-1.3 s bass anticipation and the 12 s loop the only structural cues.
- Rhythm: pitch gives no pulse, so the pulse is bass notes (about 1 s tail), hits (1.5 s) and 0.19 s syllables. The D to A flicker adds a small irregular ornament over the grid.
- Sound: three octaves of A (A1 sub, A3 and A5 stab) plus a D neighbour and a near-sine bass is a bare spectrum; chord detection returns "N" 47.6 per cent and "Am" only because of C in the voice.
- Voice/feeling: the only third in the track is in the voice (C), so the mood (playful, cheeky, dark-bottomed, not sad) is a delivery and timbre matter more than a harmonic one.

## 5. Settled conclusions

- **Key centre A, one tonic throughout (high).** Bass A1 on every pYIN span, with only an A# onset glide (~0.7-1.2 semitone); the ending is A (3:04-3:07 A 0.85).
- **No chord progression exists (medium-high).** No bass movement anywhere; F#m, F, D and Gm labels in chords.json are voice or sweep residue; 47.6 per cent of chord time is "N".
- **The stab layer is A at A3 and A5 with brief D neighbour visits (medium); no riff, no sounding third or fifth cell (medium-low).**
- **Mode is undecidable from instruments; the voice leans to C over A in the hook (medium-low), giving a faint minor, bluesy colour; verse pitches (D4, G3) are speech register, not harmony.**
- **The G (b7) "signal before change" idea is withdrawn (high-medium); structure comes from layers, not harmony. Cannot tell: instrument identity, whether a masked chord sits under the stab, pYIN octave/formant error, demucs bleed.**
