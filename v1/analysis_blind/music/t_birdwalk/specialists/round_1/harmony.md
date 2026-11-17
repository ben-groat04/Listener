# t_birdwalk: HARMONY specialist, round 1 (blind, measurements only)

Evidence key: WIN = music_views/window_NNNNs.png (opened 0080 myself); CH = chords.json; LN = lead_notes.json; LV = per_second_levels.json; SUM = audio_features/summary.json and music_views/summary.json; NOTES = the ten win_*.md notes; MY = my own measurements (scripts: v1/scripts/agents/harmony_birdwalk.py, harmony_birdwalk2.py, harmony_birdwalk3.py; pYIN on bass.wav and vocals.wav, CQT chroma on other.wav and the mix). Timestamps m:ss.

## 1. Bottom line

This is not a chord-progression song. It is a one-note piece: a sub-bass pedal on A1 (about 55 Hz), a rapped, near-chanted voice, and an "other" layer that gives stabbed texture rather than chords. Everything the chord labeller calls "movement" is, on my measurements, either the voice's inflections, bass or percussive smear, or a brief genuine colour move to G or F (flat seventh, flat sixth) over the unchanged A pedal. Tonic A: high confidence. Mode (minor or major): not determinable from the measurements; I would call the colour "A-based, third-less or third-ambiguous, with a bluesy minor-ish lean from the voice" (medium-low).

## 2. Key centre: A (high confidence)

- Whole-song key: A minor 0.502, A major 0.465, F# minor 0.214 (SUM). Per 30 s: A minor beats A major in every block by 0.02 to 0.06 (SUM, NOTES), which is a statistical tie, not a mode. F# minor is the relative minor of A major and scores a distant third (0.21; 0.275 at 3:00), so the estimator is not seeing a separate F# centre.
- Chroma: the A row is saturated in every window image (WIN 0000 to 0180; WIN 0080 chroma panel shows a solid A bar for the whole 20 s apart from the stab moment at 1:22 to 1:23). The mix chroma, normalised, has A at 1.00 in every segment I tested (80-83, 83-92, 93-100, 106-110, 131-144, 167-170, 184-188 s) (MY).
- Bass, measured directly (the lead tracker cannot see it; NOTES could only infer): pYIN on bass.wav gives A1 (MIDI 33) as the dominant bass pitch class in every 10 s block from 0:10 onward, 53 to 82 per cent of voiced frames (MY). Median pitch of the sustained part is 0.01 semitone from A1 at A=440, i.e. exactly in tune with concert pitch, so the bass is a tuned sub tone or sample, not a sloppy live bass (medium: one tracker). The only non-A bass pitches of any size are G1/G#1 (about 0.1 to 0.2 s of frames) and tracker octave jumps to A2-C#3 (low confidence, probably harmonics).
- So the bass never changes note across the track. When the chord labeller says F#m, F, D, Gm or Dm over the bass, those labels are not bass-rooted harmony.

## 3. Bass behaviour: a pitch-drop glide on every hit (medium)

In MY bass tracking, about 75 per cent of the 40 long bass runs begin on average about 1.2 semitones above their sustained pitch (start mean MIDI 34.2, sustain median 33.0), which shows as a large A#1 share (14 to 31 per cent of frames per block) next to A1. The simplest reading is an 808-style kick-bass whose pitch falls from about A#1 onto A1 at each hit. The alternative is tracker overshoot on a loud transient. WIN 0080 bass panel supports the first reading: each hit is a vertical click with a low tail. Consequence for harmony: the "A#" in chroma is probably this glide and should not be read as a b2 colour.

Bass on/off from LV (bass above -45 dB): present 0:12-0:47, 0:59-1:42, 1:45-1:59, 2:11-2:23, 2:35-3:06 (LV). Absent: 0:00-0:12 (bass about -70 dB, so the opening has no tonal floor), 0:47-0:59, 1:42-1:45, 2:00-2:11, 2:23-2:35. During every absence the chroma still shows A as the brightest row (NOTES win_0120 and win_0140 say the same). That means the A centre is carried by something other than the bass in those gaps, probably the "other" layer's sustained or repeating A, or the voice sitting on A, not by the bass alone.

## 4. Chords: what the labeller says versus what is there

CH shares of time (music_views/summary.json): N 47.6 per cent, Am 40.0, A 20.3 (these do not add to 100 because they are the top-10 list as given), F#m 9.7, F 5.5, D 3.6, Gm 0.9; 155 changes. Nearly half of the track gets "no chord", which is itself informative: the harmony is too thin and too masked for a template match.

Independent check on the "other" stem (the only pitched-ish accompaniment layer), energy-weighted chroma by section (MY):
- A is 1.00 in every section; the next pitch classes are all weak and flat: E 0.40 to 0.63, G# about 0.5, A# 0.4 to 0.6, C 0.36 to 0.47, C# 0.34 to 0.51. Crucially C (minor third) and C# (major third) are within 0.01 to 0.07 of each other in every section I measured (e.g. 0:12-0:47: C 0.44, C# 0.38; 1:00-1:23: C 0.36, C# 0.34; 1:40-2:11: C 0.37, C# 0.37). A stable triad of either quality would show one third clearly above the other. It does not. So either the third is absent (an "A5" power-fifth or A-only sample), or the stem is mostly broadband stab/percussive smear, or the voice is feeding both thirds. I cannot decide which; all three lead to the same conclusion: no clear minor or major chord is playing.
- The fifth (E) is only modest (0.4 to 0.6) so not even a strong power chord is measurable. Highest E values are at 0:47-1:00 (0.63) and 2:24-2:35 (0.61), the two breakdowns, where the bass is absent (MY, LV). That fits the fifth being supplied by the sample in the breakdowns when the sub is out.

Therefore the NOTES labels "Am" and "A" alternate for reasons of tracker noise (agrees with every window note that raised it). Confidence medium-high that no functional progression exists.

## 5. The real colour moves (small, localised)

These are the only places where measurement supports a harmonic event, as opposed to a labeller flicker:

1. 0:23.7-0:24.4: chroma briefly moves to G (win_0020 note, WIN 0020 chroma). Medium-low; one-beat step down a tone from A.
2. 1:20-1:23: a stab bed in "other" with G lit strongly at about 1:22.2 to 1:23.0 and a D label (WIN 0080 chroma panel, which I opened: bright G block at x about 2.2 to 3 s, flanked by A; CH D at 1:23). MY mix chroma for 1:20-1:23 gives A 1.00, A# 0.66, G# 0.53, G 0.50. Reading: A, then G (or G over A), back to A: a b7 gesture, i.e. A-G-A or "A / G/A" (medium-low). This is the one place in the first half that sounds, on paper, like a chord change.
3. 1:23-1:33: "other" is gone (LV other below -45 dB until about 1:33); only the A pedal, drums and voice remain (WIN 0080 "other" panel dark 3 to 15 s). Harmonically it is pure pedal. The Dm label at 1:26.6 is a 0.8 s blip with no support in chroma (low).
4. 1:33-1:40: a diagonal rising sweep in "other" at 1:35 to 1:38 (WIN 0080 other panel, diagonal streak from about 500 Hz to 4 kHz) plus F#m labels (1:35.3, 1:38.1) and F/B/C#/E lit in chroma. I read this as a riser with harmonic smear, not a real F#m (low-medium). The window notes' "F#m-Am turn" is plausible but cannot be separated from sweep noise.
5. 1:46-1:49: G lit in chroma and CH Gm at 1:47.6 under a high voice (A4 to A#4); 1:58-2:00 chroma turns G-led, then A at 1:59.8 (win_0100 note). The same flat-seventh step down and back to A at the end of a long verse block; medium-low.
6. F as a flat-sixth: CH F at 1:03.4 and 1:14.9, 2:21.2, 2:37.5; win_0060 reads this as an Am-F gesture about every 11 s. I cannot confirm: bass stays on A (MY), so F would have to be the "other" layer or the voice, not a bass move. Low confidence that it is more than a vocal inflection.
7. 2:47-2:48.3 and 2:57.5-2:59: G glow before the end (win_0160). Again b7 passing over A.
8. 3:05-3:08: CH reads D at 3:05.3 and F#m held 3:06.1-3:08.2 in the fade. The level is -36 to -45 dB (win_0180), so this is the tail of the loop decaying with the bass already gone (LV bass absent after 3:06 on my run list). My mix chroma for 3:04-3:08 has A 1.00, A# 0.36, B 0.19 only (MY, 184-188 s), i.e. mostly A with a hint of B, not a convincing F#m. I therefore doubt the "unresolved F#m ending" in NOTES: the ending is, on my numbers, an A-dominant fade-out, with D/F#m labels from low-level residue (medium-low).

Net: the harmonic vocabulary is A, with G (b7) as the main neighbour and possibly F (b6). This is Aeolian/blues-minor/mixolydian territory without any evidence that picks one. A mode claim would be an invention.

## 6. Lead line: speech melody, not a tune

LN is a vocal-stem tracker on a rapper, and I re-ran pYIN on vocals.wav (MY) to check the window notes:

- 0:00-0:12: median MIDI 48.6 (C3), spread across A, D, C#, C, B: no centre (low-register chatter).
- 0:12-0:24: median 45.6 (A2); pitch-class share A 0.36, A# 0.16, C 0.14. Voice sits on the tonic.
- 0:24-0:40: median 61.7 (C#4/D4); D 0.46, C# 0.25. This confirms win_0020's finding of an almost monotone recitation on D4 with C#/C/D# neighbours. D is the fourth above A, so the voice is chanting on scale degree 4 over an A1 pedal. Interval to the pedal: a perfect fourth (two octaves up and a bit); nothing in the stems resolves it.
- 0:40-0:47: median 60.3; C# 0.25, C 0.21, B 0.18: descending chromatic tail from C5 (win_0040 note).
- 0:47-1:23: median 48.4; A 0.21, G# 0.15, G 0.14, C 0.10: low chant around A with minor-third bounce (A-C-A) and leading-note neighbour (G#). This is the A-C-A cell that win_0040 and win_0120 call a motif.
- 1:23-1:40: median 54.3 (F#3/G3); G 0.35, E 0.15: a verse a fourth-ish above the pedal's octave, centred on G (b7). Interesting: the voice's centre here is G, the same b7 that shows in "other" chroma at 1:22; so b7 is the colour of this verse (medium-low, pYIN on speech is jittery).
- 1:40-2:11: median 53.4; A 0.20, G# 0.19, G 0.16; with the high A4 to A#4 excursions at 1:46-1:49 (win_0100).
- 2:11-2:35 and 2:35-2:48 (hook "that bird walk"): median 45.5 (A2); A 0.35, C 0.14 to 0.17, A# 0.14, G# 0.11 to 0.15. Narrow, tonic-centred, minor-third bounce. This is the same A-C-A figure as 0:47-1:23. So the hook and the second chant share one shape.

Chromatic wobble (G#, A#, C#, C, D#) in every verse means the tracker is following speech inflection, not scale degrees. Both C and C# are heard in the voice (win_0000: C3 and C#3 at 7 to 17 s; win_0120: C3 and C#3 repeated), which is the bluesy third-ambiguity, and it might be the main source of the mode flicker.

"Motif": the only repeating melodic shape is the voice's narrow A2-C3-A2 (a minor-third bounce) in the low chant sections, and the descending tail at 0:40-0:46. Nothing in the instrumental stems carries a tune (I found no repeated pitched figure in "other" or bass beyond the pedal). The "riff" is rhythmic: bass hits of A on a pitch-drop, stab bursts on A. Confidence medium; a different instrument layer (e.g. an "A" sample with pitch not visible in chroma) cannot be ruled out.

Development: no development of a melodic idea. Variation is by register and layering: low chant (0:12-0:24, 0:47-1:23, 2:11-2:48) versus high D4 recitation (0:24-0:47) versus G-centred verse (1:23-2:11), plus remove-and-return of bass and "other". The harmony itself is stationary; form is made by texture (see questions).

## 7. Cross-check of the window notes: agreements and corrections

Agreements: A centre in all ten; mode unresolved in all ten; chord labels over a pedal are noisy (win_0020, win_0040, win_0060, win_0140); D4 recitation 0:25-0:40; low A2-C3 chant in the 2:00-2:48 stretch.

Corrections or tightenings:
- win_0000 and win_0020 say bass pitch "cannot be read" or "probably A". Measured: A1, in tune, every block (MY).
- win_0060 reads "A-and-fifth power sound with no clear third (low)". My C versus C# test supports a third-less or thirdambiguous reading (not proof).
- win_0060 "slow Am-F gesture every 11 s" is not supported by the bass (it never leaves A). Treat F as colour in other or voice.
- win_0160 and win_0180: "F#m ending as hanging/unresolved" is weak. The final chroma is A-dominant with B and C/C# traces (MY), and bass is absent in the last seconds; F#m is a label on residue.
- win_0160 correctly says lead_notes near C#2 in 2:50-2:58 are sub-bass leaking into the vocal pass; I agree (MIDI 37 is C#2, 69 Hz: not A1 but a low harmonic-residual artefact, or a second bass tone; I cannot tell).
- win_0100 "A4 and A#4 lift at 1:46" may be an octave error; vocal stripes in that part of the vocal spectrogram do look higher, so medium.

## 8. How it feels (harmonic contribution)

- A single held tonic with a sub-bass under it is hypnotic and relentless: weight without direction. The listener is not led anywhere harmonically, so tension and release come from the bass arriving (0:12: bass from -70 dB to about -15 dB in one second, LV) and leaving (0:47, 1:42, 2:00, 2:23), not from chords. The A that remains in the gaps (chroma bar persists) is felt as a floor you are standing on after the lights go off.
- The flat-seventh visits (G at 0:24, 1:22, 1:47, 1:58, 2:47, 2:58) give a brief lift or "sideways" lean, like leaning off the tonic and coming back. They are the only moments the ear can hear "harmony".
- The ambiguity between C and C# in the voice and "other" gives a sour, cheeky, slightly menacing but playful feel (CLAP "playful" weak evidence in win_0020). I would not call it sad.
- The ending is a fade on an A-based loop with no cadence; harmonically it does not conclude, it just goes out of earshot. Confidence medium.

## 9. What measurements cannot tell me

- Instrument identity of the "other" layer (the NOTES offer synth, guitar, sample, banjo; CLAP disagrees with itself), so I cannot say whether a third is played and masked or absent.
- Whether the A# in bass chroma is a real glide or tracker overshoot (my reading is glide; one tracker).
- Whether any chord change is hidden under the loud voice and drums: chroma is smeared whenever the voice and drums are loud, and CH labels N for 48 per cent of the track.
- Mode (aeolian, mixolydian, blues-minor, or major): not decidable.
- Voice pitches are speech-contour estimates (pYIN may follow formants); octave errors likely at 1:46-1:49 and 2:58.

## 10. Three questions for fellow specialists

1. To SOUND (sound specialist): is the bass hit a pitch-dropping 808-type tone (my pYIN says the pitch starts about 1.2 semitones above A1 and settles on A1 for about 75 per cent of notes), and does the "other" stem look like a sample that has a fixed pitch (an A-only loop) or a chordal instrument? Anything in the harmonics of "other" at 800 to 1000 Hz (win_0000 note) that betrays a third or a fifth?
2. To FORM (form specialist): the harmony never changes, so form is built purely from bass and "other" entering and leaving (bass off 0:47-0:59, 1:42-1:45, 2:00-2:11, 2:23-2:35). Do these gaps line up with phrase or bar boundaries of the beat grid (152 BPM tracked, half-time probable), and does each return of the bass at 0:59, 1:45, 2:11 and 2:35 land on a downbeat? Do the G-colour moments (1:22, 1:47, 1:58, 2:47, 2:58) sit at the ends of eight- or sixteen-bar blocks?
3. To VOICE (voice specialist): in your reading, is the rapped delivery consciously pitched (D4 chant at 0:24-0:47; the A2-C3-A2 bounce in the hook at 2:11-2:48) or simply speech intonation? And does the voice's sitting on C versus C# (both present in the lead tracker) sound like a deliberate blue third, given the instrumental layer gives no third?
