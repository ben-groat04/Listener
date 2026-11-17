# t_birdwalk: HARMONY specialist, round 2 (blind, measurements only)

Evidence key: R1 = round_1 specialist files; CH, LN, LV, WIN as in my round 1; MY2 = new measurements, scripts v1/scripts/agents/harmony_birdwalk_r2.py and harmony_birdwalk_r2b.py (pYIN on bass.wav in chosen spans; peak-frequency and chroma on other.wav). Timestamps m:ss. I did not read context.md, research or non-blind files.

## 1. What I now think (changes from round 1 in bold)

- Key centre A, unchanged (high). Bass is A1 throughout (MY2 below).
- **The "other" stab layer looks like a single repeated pitch, A, moved between octaves, not a riff and not chords (medium).** New measurement. This answers SOUND's question about whether "other" plays a figure against the pedal.
- **No chord change exists anywhere that the bass confirms (medium-high).** Every candidate cadence point named by RHYTHM and FORM was checked in the bass stem and none moves (section 3).
- Mode remains undecidable. I withdraw nothing, but I add one piece of evidence for a minor lean in the voice (section 4).

## 2. New measurement: the "other" layer is an A, in two registers

MY2, other.wav, peak-frequency pitch class of the strongest bin (150 to 2000 Hz) in the loudest 40 per cent of frames:
- 0:40-0:47: A in 63 per cent of frames, nearly all at about 883 Hz (A5, 880 Hz). B 18, C 14 per cent. Median A-peak 883 Hz. This is the "plucked tone at 0.8-1 kHz" SOUND saw in W0040 [sound.md, section on "Other" layer]: it is an A5.
- 1:00-1:20, 2:00-2:10, 2:45-2:50: A in 76 to 85 per cent of frames, now at about 226 Hz (A3, 220 Hz; the 6 Hz offset is one FFT bin, 5.4 Hz, not a tuning fact).
- Other pitch classes never exceed 20 per cent (D 17 per cent at 2:00-2:10; C 19 per cent at 2:35-2:45; B 14 to 18 per cent). No third or fifth is dominant at any time (E is 0 to 1 per cent of peaks).
Reading: the stab is a note-A sample or synth tone, jumped between A3 and A5, with a few off-A flickers that coincide with the sweeps. Together with the A1 sub, the instrumental layers sit on A in three octaves (A1, A3, A5). Medium confidence: one method, peak-picking can lock onto a strong partial, so A5 could be the second harmonic of an A4 or the fourth of A3. That does not change "all A".
The averaged chroma of "other" (MY2) is flat apart from A (C 0.36-0.56, C# 0.34-0.62, E 0.40-0.74, all within 0.01 to 0.2 of each other), as in round 1: stab noise and sweeps, no chord. In the final 10 s (2:47-3:00) G rises to 0.51 to 0.62 and G# to 0.60, the highest non-A values anywhere. That is where the stutter and falling sweeps sit, so I read it as sweep smear, but it is consistent with the b7 glow in WIN 0160.

## 3. Answers to questions put to me

**RHYTHM, Q1: does the bass move off A at 1:40-1:46, 2:50, or the 3:04 ending, and do chord changes line up with a 3.0 s bar?**
MY2 pYIN on bass.wav: 1:40-1:47 A 0.47 and A# 0.34 (median MIDI 33.3); 1:47-1:52 A 0.54, A# 0.19, G 0.09; 2:30-2:50 A 0.60, A# 0.28; 2:50-2:56 A 0.73; 2:56-3:00 A 0.66, G 0.11; 3:04-3:07 A 0.85, A# 0.14. So: no, the bass never leaves A, including the 1:41-1:46 hole (the notes that remain are A1), and the end is A. A# is the pitch-drop start of each note, as in round 1. There are therefore no chord changes to line up with a bar. The only G in bass is 0.09 to 0.11 of frames (1:47-1:52 and 2:56-3:00), tiny and unconfirmed. Where RHYTHM sees a "step down and shift in the sub" at 2:50 (win_0160), my pitch tracker sees no pitch step; if there is a shift it is timbre or level, not pitch (medium).

**FORM, Q2: is there any true harmonic change that could mark sections, e.g. 1:46-1:57 or 3:00-3:08?**
No true change marks sections. The G (b7) moments at 1:22, 1:47, 1:58, 2:47 and 2:58 (my round 1) are in the voice and in "other", never in the bass, so they are colour above a fixed floor, not cadences. They do, however, sit at the ends of transitions FORM identified: 1:22 just before the "other" layer is removed (1:23), 1:47 at the bass return after the hole, 1:58 at the cut into drop 2 (1:59.2), 2:58 at the last vocal glide. I cannot tell whether that is design or coincidence, but G-lean as a "something is about to change" marker is a fair hypothesis (low-medium; five instances, voice-pitch based).
For the ending: MY2 chroma of "other" at 2:56-3:00 has A 1.00, G 0.51, G# 0.60, A# 0.55, B 0.41, i.e. a fade on A with b7/leading-note colour, not F#m. FORM's "drains, not arrives" is right harmonically too.

**SOUND, Q2: is "other" a riff against the A pedal or a single repeated pitch?** Single repeated pitch A, octave-moved (section 2). I find no pitch figure. If a riff exists it is rhythmic (the stab pattern), not melodic. Whether the sub and the stab lock into one pattern is a rhythm matter, not a pitch one.

**VOICE and LINEAGE (C versus C#, D4):** accepted. VOICE's count (C3 and A2 about 60 per cent of hook notes; C#3 only 8 of 102 [voice.md]) beats my round 1 "both heard". Because the hook is a pasted loop (voice.md, FORM's 0.94 correlation), the C is a property of one take. I correct myself: the voice leans to a **minor third (C) over A** in the hook, giving a mild minor-ish colour (medium-low, speech pitch, one take). The "C versus C# sourness" I described in round 1 came mostly from verse material and the other stem's smear, not from the hook. VOICE's note that verse 2 sits on G3/G#3 matches my G (b7) reading; I agree it is a delivery move, not a harmonic one.

## 4. Corrections to others, and to myself

- FORM, section 6 and WIN 0180 "harmony drifts to F#m": withdrawn for good; the bass is A (3:04-3:07, A 0.85) and the other-stem chroma is A-led. CH's F#m is residue (medium).
- RHYTHM's "bass often lands 3 grid beats apart" and 2+3 cell: harmony has no objection; the bass content is all rhythm on one pitch. The A# in the bass is a pitch-drop on note onset, so a faster glide would add a pitched "boing" to each hit; SOUND found envelope shapes consistent with that. No disagreement.
- SOUND's sub histogram (280 at 55 Hz, 373 at 57.5 Hz): 57.5 Hz is 0.9 semitone above A1, i.e. the A#1 start of the glide, which matches my 1.2-semitone figure. Two independent trackers now agree (medium-high).
- Round 1 error of mine: I said CH D at 1:23 supported a G/D stab "chord change". MY2 other-stem peak data show A, not G or D, dominating 1:00-1:20 and the stab; I now rate the 1:22 G as a single passing b7 in voice and chroma, not a chord (low-medium).

## 5. Connections to other areas

- Form: with harmony frozen, the arrangement is the whole architecture, as FORM says. The drops are "harmonic" only in the sense that the sub (A1) leaves, so the A-floor goes from sounding to implied. In breaks the A is still carried by the A3/A5 stab and the voice, which is why the chroma stays on A when bass is absent (round 1, section 3) rather than a hidden chord.
- Rhythm: single-pitch bass and single-pitch stab mean pitch gives no pulse cues; the pulse is entirely the 1.57 s hits, 1.1-1.2 s bass cell and 0.19 s syllables. A listener cannot hear a "bar" harmonically, which fits RHYTHM's admission that the downbeat is inferred only.
- Sound: three-octave A (A1, A3, A5) plus a voice at D4 or A2-C3 is a very bare spectrum; this is why chord detection fails (47.6 per cent "N") and why the noise-like sweeps dominate chroma. The bare, repeated tonic is what makes the track hypnotic and chant-like.
- Feeling: lack of any harmonic motion makes the minor/major question almost moot to a listener: the drive is the bass dropping out and returning, with a faint minor lean from the voice's C and the sideways G leans.
- Lineage: one-note tonic, 808-style sub on A, chanted voice, stabs, and break-driven form match a crunk/club-chant model; harmony offers no counter-evidence.

## 6. Confidence summary

Key A: high. Bass A1 constant, no chord movement: high (two trackers, round 1 and MY2). "Other" = repeated A in octaves: medium. No functional chord progression: medium-high. Mode: undecidable; faint minor lean in the hook voice: medium-low. G (b7) as sectional "lean" marker: low-medium.

## 7. Cannot tell

Instrument identity; whether the stab is truly one note or a chord whose third and fifth are masked (the C/C# parity and weak E still allow a masked power chord); whether G moments are performance or coincidence; pYIN octave and formant errors on speech; demucs bleed (37 per cent of "other" below 150 Hz per sound.md).

## 8. Two new questions

1. **To SOUND:** the "other" stab is an A at A5 (883 Hz) in 0:40-0:47 but A3 (about 226 Hz) in 1:00-1:20, 2:00-2:10 and 2:45-2:50. Is that a different sample/patch in each section (look at the spectral envelope, attack and decay of the stab before and after 0:47), or the same sound pitched an octave or two? Which does the harmonic ladder of each look like: a plucked string, a square wave, a vocal sample?
2. **To FORM (with VOICE):** my five G (b7) lean moments (1:22, 1:47, 1:58, 2:47, 2:58) all fall within a few seconds before a layer change you mapped (1:23 other-out, 1:47 bass return, 1:59 drop, 2:47.5 voice-out, 2:57 voice return). Do you count them on the same bar grid (about 3.0 s multiples from the 0:12.4 drop) and do any of the transitions lack a G lean? If the pattern holds, it is a deliberate "signal before a change"; if not, it is voice-pitch noise.
