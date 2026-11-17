# t_birdwalk: HARMONY specialist, round 1

Scope: key centre, chords and loops, modal colour, motifs, melodic contour. Sources: the ten `win_*.md` notes (read, then re-checked), `music_views/window_0000s.png` and `window_0060s.png` (opened), `chords.json`, `lead_notes.json`, `bass_roots.json`, `per_second_levels.json`, `audio_features/summary.json`, vocals transcript, and my own runs on `audio/song.wav` and `stems_raw/htdemucs/song/*.wav` (CQT chroma per stem and section, FFT peaks of the "other" stem, self-similarity, bass onset and kick IOIs, 10 ms envelopes). Track 188.15 s. Tags: measured / INFERRED, with high/medium/low.

## 1. Headline
The harmony is one pitch: **A**. It is a pedal or drone on A with almost no chord movement; the song is a rapped trap/hip-hop piece (transcript: "bird walk", "watch me do that bird walk"; "money, money"; "so icy, so nice"), not a chord-progression song.
- A is the tonic in every measurement (high). Whole-song key A minor 0.502 vs A major 0.465 (`summary.json`, `key_ambiguous: true`). Per-30 s blocks agree (A minor about 0.44 to 0.54, A major 0.41 to 0.51).
- The mode is undecided, and my chroma shows why: in the mix over 1:00 to 1:40, the minor third C = 0.25 and the major third C# = 0.23 (A = 1.00, relative to the strongest bin); over 2:35 to 3:00, C = 0.28, C# = 0.24. They are the same size, so there is no third. Mode label: unrecoverable from chroma (measured, high). Calling it "A minor" is a convention, not a finding.
- The "Am" 40.0 % and "A" 20.3 % chord shares in `summary.json` (N 47.6 %) are the chord detector choosing between two near-equal templates on an A-plus-fifth sound. Do not read them as minor-major alternation (INFERRED, high).

## 2. The bass: A1 with a flat-second neighbour
`bass_roots.json` (pYIN on the bass stem, 753 windows, 543 voiced, 0 octave-flag windows):
| Pitch class | Voiced seconds | Share |
|---|---|---|
| A (about 55.0 Hz, A1) | 109.75 | 80.7 % |
| A# (about 56 to 59 Hz) | 19.0 | 14.0 % |
| G (49 Hz) | 5.5 | 4.0 % |
| G# | 1.0 | 0.7 % |
| B | 0.75 | 0.6 % |
- Per section, A1/A#1 counts: 12 to 47 s 80/50; 59 to 70 s 28/15; 70 to 100 s 89/25; 100 to 130 s 47/8; 130 to 150 s 42/4; 150 to 180 s 68/26. A#1 is largest early (12 to 47 s, 38 % of voiced windows) and again in the finale; it is rare around 2:10 to 2:30. G1 appears only in short bursts (for example 23.75 to 24.25 s).
- Reading: the note a semitone above A is a **flat second (b2, Phrygian-type colour)** over the A root, or equally an upward pitch-bend or glide on a sustained 808-type note starting from A (the median frequencies of the "A#" segments are 56 to 58 Hz, between A1 at 55.0 and A#1 at 58.3 Hz, so a bend is at least as likely as a discrete note). INFERRED, medium; the stem and a pYIN tracker cannot separate a stepped note from a glide on a sub-bass.
- Tuning: A1 reads 55.0 to 55.3 Hz, which is concert pitch (A440). The "other" stem has clear peaks at 110.4, 440.1 and 881.5 Hz (A2, A4, A5), so the sampled layer is also at A440 (measured, high; librosa tuning estimate +0.01 semitone for "other", -0.24 for the bass, the latter noisier because of the sub-bass). It does not look pitch-shifted by a fractional amount.
- Unexplained: a strong "other" peak at 224.8 Hz (57.4 in MIDI, not on any A440 note, 37 cents above A3). It is not 2x 110.4 (220.8). Source unknown (could be a vocal-chop formant or a detuned sample partial); I make no claim.

## 3. Chord track and what it can support
- `chords.json`: 155 changes, but most are Am/A/N flicker lasting 0.4 to 1.2 s. Section shares (my sums of `chords.json`): 0 to 12 s A 5.8 s / Am 3.6 s; 12 to 47 s N 10.9 / Am 7.9 / F#m 2.4 / F 1.2 / D 0.4; 47 to 59 s A 3.4 / N 3.9; 59 to 70 s Am 4.0 / N 3.9 / F 0.7; 70 to 100 s Am 9.3 / N 6.6 / A 1.9 / F#m 1.3 / F 1.1; 100 to 130 s N 7.2 / Am 4.3 / A 2.7 / F 1.3 / F#m 1.2; 150 to 188 s N 11.1 / Am 8.9 / F#m 4.5 / A 2.4 / F 0.8.
- The side labels F#m, F, D, Gm are each under 10 % and come in short bursts. F#m is read from A + E + F# energy, not from a bass F#: the bass never goes to F# (bass set at at least 3 % is only G, A, A#). F is likewise not supported by the bass. They are upper-layer colour or detector noise (INFERRED, medium). The window notes that call F#m "relative-minor colour" (3:06 to 3:08, last 2 s) are speculation over a fading sub-bass; I lower that to low confidence (reason: bass stem there is a bare A1 at 54.8 to 55.2 Hz at 3:05 to 3:06, measured, so the harmony at the end is A alone).
- In the stripped middles (no bass), the chroma lights C, D, E, G together in vertical stripes (window 2:20 note, `window_0140s.png`): this is voice and short stabs over an A tone, not a new chord (INFERRED, medium).
- Verdict on "progression": none is measurable. There is no I-IV-V or i-VI-VII cycle. The closest to harmonic motion is the A to A#(b2) bass wobble and the occasional G (b7) step below A in the bass. Confidence high that this is a static-harmony, one-chord piece.

## 4. The sampled layer ("other" stem): the only melodic/harmonic content
- CQT chroma of "other" is A-dominant in every section (A = 0.14 to 0.19 of chroma mass; A# next at 0.08 to 0.11 in most sections; E and G# also high). The mix chroma over 0 to 12 s is nearly flat (C 0.75, C# 0.70, D 0.65, E 0.72, A 1.00 relative), meaning a broad, many-pitched or noisy texture around A (it is also the voice-only opening; chroma is smeared by speech).
- Spectral peaks of "other" (FFT of whole stem sections): 881.5 Hz (A5) is present at every section; near it 870.7 and 890.9 Hz and a cluster at 940 to 1060 Hz (about B5 to C6 range). Short stabs at 0.5 to 2 kHz appear in `window_0000s.png` and `window_0060s.png` "other" panels as repeated horizontal dashes. I read this as a chopped or stabbed sample with a strong A (880 Hz) component, with pitch clustering about a semitone on either side (A#, G#), the same "A with b2/b7 neighbours" colour as the bass (INFERRED, medium; I cannot tell a vocal chop from a plucked or string sample).
- **Loop regularity** (rule 1): self-similarity of a mel representation of the "other" stem against lag: for 59.5 to 100 s the best repeat is at 2.91 s (correlation 0.44); 24 to 36 s 2.86 s (0.33); 0.5 to 12 s 3.06 s (0.43); and a longer repeat near 11.6 s (0.31) in the finale and 11.56 s (0.20) in 12.5 to 47 s. For the bass: 2.90 s (0.34) in 12.5 to 47 s and 2.95 s (0.38) at 59.5 to 100 s. A 2.9 s repeat is about four of the 0.735 s kick-grid periods or 7.4 of the 0.394 s tracker beats. Correlations of 0.2 to 0.44 are far from the near-1 values a bar-exact copy-paste loop would give once a rapped voice is on top; it is a repeating cycle that is not sample-identical (stem separation leakage from the voice lowers the figure; I cannot separate that from true variation). Judgement: a repeating one-bar-ish (about 2.9 s) and four-bar (about 11.5 s) pattern, consistent with a DAW or sampler pattern with live-mixed variation. INFERRED, medium to low.
- **Production era** (harmony-relevant part): sample peak 0.0 dBFS (clipping-level mastering) and mix RMS -13.8 dBFS (mono sum of `song.wav`); a pure-pitch A1 sub-bass at 55 Hz that is steady on every note, and bass stem about -14 dB against vocals -19 to -22 dB. This reads as **modern production** (limited master, 808-style sub). I did not find a band-limited or noisy older layer under the full-band mix in the chroma or the "other" stem (high-frequency content in "other" reaches the stem spectrogram top; `window_0000s.png`). INFERRED, medium; I did not measure the kick-onset spread (rhythm specialist).

## 5. The voice as melody (rap, so weakly pitched)
`lead_notes.json` (pYIN-style tracker on the vocal stem). Median MIDI by section (A3 = 57, A2 = 45):
| Section | Notes | Median | Range | Most common degrees above A |
|---|---|---|---|---|
| 0 to 12 s | 29 | 49 (C#3) | 44 to 54 | F (6), B (3), D (5) |
| 12 to 47 s | 79 | 60 | 44 to 73 | F (23), E (16), D# (12), A (10) |
| 47 to 59 s | 26 | 46 | 44 to 51 | A (10), C (7) |
| 59 to 70 s (hook) | 15 | 45 (A2) | 44 to 48 | A (6), C (5) |
| 70 to 100 s (verse) | 60 | 55 (G3) | 45 to 57 | G (27), G# (13) |
| 100 to 130 s | 67 | 54 | 44 to 70 | A (16), G# (15), G (10) |
| 130 to 150 s | 44 | 46 | 44 to 51 | A (16), C (10) |
| 150 to 188 s | 52 | 45 | 37 to 72 | A (13), E (13), C (9) |
- The hook (1:00 to 1:10, "that bird walk") sits on **A2 and C3** (about 110 and 130 Hz): a root and a minor third above it, with a short move up to C (3 semitones) in the pattern. The chanted hook is essentially a two-note figure, root and minor third, about 3 semitones (measured, medium; pYIN on rap is unreliable).
- At 1:10.4 the rapped verse starts and the median voice pitch rises from A2 (45) to G3 (55), about 10 semitones (win_0060 note says "about nine"; my section medians give 10; the tracker range 45 to 57 is wide). Mostly G and G# above the A root: the voice sits a semitone or two below the root octave, rather than on chord tones. The pooled chord-tone share in `voice_as_music.txt` is 0.342 against 0.25 chance, and the median note is on a chord tone in 0/4 listed segments (measured): the rap is only loosely tied to the harmony. Interval histogram of segment medians peaks at 9 and 10 semitones (4 each), I read this as a pitch register change, not a melody (INFERRED, medium).
- A descending vocal glide from about 880 Hz (A5) at 2:57.9 to about 108 Hz by 3:00.1 (`win_0180.md`, my reading of its pYIN figures, checked against the 3:00 tracker notes C5, D#4, C#4, B3 which agree), ends the vocal. This is the only clear melodic gesture in the track: a falling sweep over about 3 octaves, ending on a note near A2 (about 110 Hz, A) i.e. back to the tonic. Tag: measured contour, interpretation (sigh-like or siren-like effect) not claimed.
- The vocals stem is at the floor (not detected above -60 dB) in the last 3 s, so the last 8 s are bass, drums, and a thin other layer on A.

## 6. Boundary evidence table (harmony-relevant boundaries, 10 ms-scale RMS in dB, 1.4 s before to 1.4 s after; computed by me with an inline script, not saved to the repo)
| Boundary | Drums | Bass | Vocals | Other | Mix | Carried by |
|---|---|---|---|---|---|---|
| 0:12.3 | -33.6 to -22.9 | -69.1 to -15.4 | -19.6 to -21.4 | -32.2 to -32.9 | -18.1 to -12.4 (+5.7) | bass (and drums) enter |
| 0:47.0 | -34.3 to -30.8 | -12.8 to -70.7 | -19.2 to -21.0 | -32.8 to -31.8 | -11.7 to -19.4 (-7.7) | bass out; voice and other continue (rhythm-section dropout, not silence) |
| 0:59.4 | -32.5 to -26.5 | -70.7 to -15.3 | -19.2 to -21.0 | -31.2 to -33.8 | -17.9 to -13.2 (+4.7) | bass returns, drums step up |
| 1:10.4 | -28.1 to -26.7 | -14.5 to -13.3 | -17.7 to -22.6 | -34.3 to -28.0 | -12.1 to -11.8 | vocal register jump (about +10 st median) and other louder +6 dB; rhythm section unchanged |
| 1:59.0 | -23.3 to -30.8 | -14.2 to -71.2 | -17.1 to -21.6 | -30.2 to -32.0 | -11.0 to -19.9 (-8.9) | bass out (the bass leaves at 1:58 to 2:00 in the stem; I used 1:59.0 from the 1:59 to 2:11 note) |
| 2:11.4 | -32.2 to -29.9 | -68.5 to -14.4 | -19.4 to -21.2 | -32.0 to -31.6 | -18.0 to -13.1 (+4.9) | bass returns |
| 2:23.4 | -34.8 to -58.1 | -13.2 to -73.8 | -19.4 to -21.1 | -29.3 to -31.9 | -11.6 to -20.0 (-8.4) | drums and bass out together; voice and other continue |
| 2:35.7 | -68.6 to -29.0 | -72.3 to -14.0 | -18.8 to -21.4 | -32.8 to -32.5 | -17.9 to -12.9 (+5.0) | bass then drums return |
In every case the vocals and "other" stems stay within about 3 dB across the boundary (the 1:10.4 "other" +6 dB is the exception), so the harmonic layer does not change at the boundaries; only the sub-bass and drums switch. The "silences" in these places are not silences: mix drops 7.7 to 8.9 dB, not to a floor, with voice and other continuing.

## 7. Form from the harmonic side
Bass on/off pattern (from the table above and `per_second_levels.json` bass > -45 dB): intro voice-only 0:00 to 0:12.3; groove 0:12.3 to 0:47; stripped 0:47 to 0:59.4; groove from 0:59.4 (hook then verse) to about 1:58 to 1:59; stripped to 2:11.4; groove to 2:23.4; stripped to 2:35.7; groove to the fade. The tonic never changes. Harmonic variety comes only from (a) the bass b2 colour, which comes and goes (heavier in 12 to 47 s and 150 to 180 s), (b) the vocal register (A2 to G3 at 1:10), (c) filtered/stabbed "other". "Release then drop" is built by subtracting the bass, not by changing chords.

## 8. End of track (rule 4)
10 ms envelope over the last 3 s (computed on the stems and `song.wav` mono, 44.1 kHz): the last audible sound above -60 dBFS: mix 188.01 s (end level about -64.6 dB, a fade), bass 187.84 s, drums 187.73 s, other 186.91 s; vocals never exceed -60 dB in the last 3 s (end level -72.4). Final mix peaks in the 10 ms envelope: 185.22 s (-22.8 dB), 186.02 s (-32.9), 186.47 s (-29.8), 187.22 s (-36.8): at least four hits inside a decay, descending in level (peak counts from a prominence-6 dB detector; drum stem alone shows more small peaks at -30 to -57 dB). Bass pitch at 3:05 to 3:06 stays at 54.8 to 55.2 Hz (A1). The ending is an unresolved fade on the tonic A. Harmonically it simply stops on the root, not on a cadence (measured, high for pitch; the count of "hits" is medium because of the fade).

## 9. What the window notes got right and what I changed
- Right: A centre, no riff, pedal, "stripped island then drop", voice step at 1:10.4, descending glide at 2:57.
- Changed: (a) "F#m relative minor at the end" lowered to low (bass is a bare A1); (b) Am/A labels are not a mode claim; (c) A# in the bass is read as a b2 or an upward bend, not a chord root; (d) voice step up is 10 semitones by section median (notes say about 9); (e) the "other" stem's A5 at 881 Hz is a stable, repeated component not mentioned earlier.
- Tempo conflict I noticed (not my remit): `summary.json` tempo 152 BPM (beat 0.394 s) vs `bass_roots.json` kick grid period 0.7348 s (81.66 BPM), ratio 1.865, not a clean 2:1. My kick IOI percentiles (low-band drum onsets) in 59.4 to 103 s are 10 %/25 %/50 %/75 %/90 % = 0.157, 0.200, 0.389, 0.681, 0.907 s, so a tracker-beat (about 0.39 s) spacing fits the median; anything using the 0.735 s grid would need a check (rule 5).

## 10. Questions for fellow specialists
1. **Rhythm:** the tracker says 152 BPM (0.394 s beat) but the kick grid in `bass_roots.json` is 81.66 BPM (0.7348 s). Which one is the felt pulse (152, or half-time about 76 BPM), and how many beats is the roughly 2.9 s repeat I measured in the bass and "other" stems (bar or two beats)?
2. **Sound:** is the 881 Hz component and the cluster of 870 to 1060 Hz in the "other" stem a sampled vocal chop, a plucked string or a synth lead? And is the A# note in the bass a stepped note or an upward 808 glide (look at the attack of the 56 to 59 Hz segments)?
3. **Voice and Lineage:** is the 1:10 rise in vocal register (A2 to G3) a change from chant to rap flow (voice), and does a hook on a root and minor third over a one-note sub-bass belong to a known trap or southern hip-hop template (lineage)?
(Also for form: does the bass-out/bass-in cycle of about 12 s (0:47, 1:59, 2:23) line up with the lyric structure?)

## Not recoverable by measurement
- Major or minor mode: the third (C vs C#) is equally weak in chroma (0.25 vs 0.23), so no mode is measurable.
- Exact instrument identity of the "other" layer (sample vs synth vs vocal chop): stem separation gives spectra only.
- Whether the A# bass is a b2 note or a glide: pYIN on sub-bass cannot separate them.
- The source and date of any sample: no band-limited or older layer was measured, but a clean modern sample cannot be ruled out as a re-use of old material.
- The intended meaning of the descending vocal glide at 2:58 and of the stripped passages: measurement gives contour and level, not intent.
- Sung pitch of the rap: tracked pitch on rapped speech is prosody, so the interval figures are approximate.
