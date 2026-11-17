# video2: LINEAGE specialist, round 1 (blind, measurements only)

Evidence keys: [WIN] the 16 window notes win_0000..0300; [AF] audio_features/summary.json, beat_times.json; [CH] chords.json and music_views/summary.json chord shares; [LV] per_second_levels.json; [IMG] music_views/window_*.png; [CLAP] clap_tags.json (weak); [LY] lyrics/ (Whisper passes); [R1] fellow round-1 notes (rhythm, sound, voice, harmony), used only as cross-checks; [P] my own probe, v1/scripts/agents/video2_lineage_probe.py (drum/bass/other stems, 2:00-4:40 unless stated). Times m:ss. I cannot hear. Lineage below is inference from structure and spectral behaviour; it names resemblances, not facts of the artist's influences.

## 1. Headline

The track sounds like **instrumental, loop-based electronic-rock in the "post-rock / krautrock-motorik / electronic dance" overlap, with a cinematic-documentary frame and a found-speech (sampled narration) device.** Three traditions are audible in the structure:
1. **Film-score / ambient drone opening** (0:00-1:28): wide, quiet, reverberant sustained bed, sparse low strikes, no pulse.
2. **Motorik / four-on-the-floor driving groove** (1:28.6 to the end): relentless steady kick, a fixed tempo, static one-or-two-chord harmony, slow build by layering and loudness.
3. **Sampled-voice-as-text**, a "found sound" narrator in the first half and chopped vocal fragments as rhythmic texture in the second. That is the tradition of sample-led electronic/art-rock where archival speech carries the story and the band does the feeling.

Confidence: high that it belongs to the electronic-leaning, riff/loop-driven, instrumental-band family; medium on the motorik and post-rock affinities; low on any narrower label (see section 6).

## 2. Sonic evidence, as it bears on lineage

**Pulse and groove (high).** My autocorrelation of the drum stem over 2:00-4:40 gives lag peaks at 0.5 s (0.48), 1.0 s (0.61) and 2.0 s (0.65), with only 0.22 at 0.375 s and 0.16 at 0.75 s [P]. That agrees with [R1 rhythm]: the felt grid is 120 BPM, 4/4, and the tracker's 161.5 BPM [AF] is a 4:3 reading of a dotted-quaver hat layer. Folded on the 2 s bar, the kick band (30-120 Hz) has equal peaks at beats 1, 2, 3 and 4 (about 0.19-0.20 each) plus a pick-up on the last semiquaver before beat 4 (0.12) [P]. So: **four-on-the-floor kick with a syncopated push into beat 4.** The 150 Hz-2 kHz band peaks on beats 1 and 3 of the folded bar (0.24, 0.23) with ghosts around them [P]; the phase of "beat 1" is not recoverable, so backbeat placement is unknown (low). The hi-hat band shows a 3-3-3 dotted pattern plus 2 s accents [R1 rhythm, WIN 0100]. Lineage reading: four-on-the-floor kick plus constant stiff tempo is the grammar of disco, house, techno and the German motorik beat; a dotted-quaver hat cross-rhythm over it is a hallmark of delay-driven guitar-band and electronic production (the "dotted-eighth echo" feel, though I cannot prove a delay is present).

**Tempo steadiness (high).** Beat-phase constant to about 30 ms across 1:30-5:00 [R1 rhythm]; drum-stem level flat within 1.5 dB over three minutes [R1 sound, LV]; black gaps between hits in the drum panel [IMG 0120s]. This is machine-like: a drum machine, sample sequencing, or heavy quantising. A live drummer would show drift and dynamic variation. That favours the electronic side of the family over, say, a live post-rock kit (medium; a very tight live-plus-click band cannot be excluded).

**Harmony: static, modal, ostinato (high on facts, medium on reading).** Whole-track key B minor (0.88) [AF]; chord time share Bm 136 s, D 44 s, Em 22 s, G 20 s, B 12 s, E 10.5 s, A 6.6 s [CH summary.json]. My pYIN pass on the bass stem (2:00-3:20) counts B1 (829 frames), D2 (733), A1 (630), E2 (368), G1/G2 (about 180 each) [P]: a **B pedal with D, A and E** colour notes. In the groove sections (3:00-4:40) the chords just rock Bm and D, each about 4 s (2 bars) [CH, WIN 0180, 0200, 0240], with brief Em/A. That is an i - III vamp: modal, no dominant-to-tonic cadence (the V chord, F#, scarcely appears: F#m 2.6 s). The middle (1:30-2:40) moves through Em - G - D - Bm and Em - G - A - D [WIN 0100, 0120]: a minor-pentatonic-flavoured "rock" loop, and the A to D (VII to III in B minor, or V to I in D) is a plain rock-band lift. Lineage reading: a static modal vamp with the interest carried by texture and layering is the shared habit of krautrock, trance, post-rock and film-score minimalism; it is not typical of song-form pop or blues rock.

**The "other" stem: distortion-or-saturation layer that grows (medium on behaviour, low on identity).** In 0:00-1:28 it is horizontal harmonic bands below about 3-4 kHz, a drone or pad [IMG 0000s, 0060s]. From 1:28.6 it gains vertical stripes up to 8 kHz [IMG 0080s] and from 2:00 is a dense full-spectrum wall [IMG 0120s]. Its level rises about 10 dB, from about -26 dB (1:20-1:40) to -15/-19 dB (3:00-4:40) [R1 sound, LV], and spectral centroid of the whole mix goes from about 0.7 kHz (0:00-0:28) to 1.1 kHz (1:00-1:28) to 1.6 kHz (2:00-3:00) to 1.8 kHz (3:20-4:40) [P]. Its harmonic share in HPSS at 3:20-4:00 is only about 0.60 [P], so it is as much percussive/noisy as tonal. That mix of sustained tone, wide band and rhythmic attack is what a distorted, chorused or delay-washed guitar layer does, but also what a saturated synth stack does. **I cannot decide guitar versus synth**; CLAP's "electric guitar" 0.9 at 4:30-4:40 [WIN 0260, 0280] and "organ/choir/bells" in almost every window [CLAP] are non-discriminative (the window notes already caution this). Both branches lead to the same lineage zone: an instrumental band texture built by layering (the "wall of sound" habit of post-rock and shoegaze-adjacent builds) or synth-led electronic rock.

**Space and production era (medium-low).** Quiet intro is wide (stereo width above 1.2 at 0:01-0:03) and reverberant (long tails, 2 s decay on low strikes [WIN 0000, 0020]); the groove is narrow (0.28-0.40) and dry [WIN 0120; R1 sound]. A sudden width collapse at the beat entry, and a dense bass/kick-centred mix, is a modern, compressed production aesthetic (post-2000 in broad terms, by the dry, punchy, centred drum and bass sound; weak, since I am inferring era from mix habits only).

**Layered build rather than songwriting (high).** The arc is quiet drone (0:00-0:28), sparse low pulse (0:28-1:28), full groove (1:28.6), speech-led middle (to 2:36), voice-free drive (2:36-3:28), chopped-voice texture (3:28-4:20), release to instrumental wall (4:20-4:40), a continuing drive, and an abrupt stop at about 5:04 [WIN 0000-0300; R1 sound]. Loudness climbs about 16 dB over the track [R1 sound]. Instrumental-band "crescendo through repetition" is the post-rock method; "enter the beat, then add layers" is the electronic-dance method. This track does both.

## 3. Sampled speech: the strongest lineage clue (medium-high)

Several Whisper passes agree on Dutch speech: "18 January 1963", "The Marathon Without Rain" (title-like), "6.30 in the morning, 200 km...", "Temperature 16 degrees below zero, a monster ride of more than 200 kilometres", "575 motorway riders, around 9500 tour riders" [LY medium_mix_nl_translate; WIN 0040-0140; R1 voice]. pYIN f0 on the vocal stem is about 118-142 Hz with voiced fraction 0.1-0.3, so it is a low male speaker, not a singer [R1 voice]. The delivery is newsreel-like, in blocks of 1-6 s that the band does not stop for, and it carries the story (date, event, distance, conditions). The track then abandons words (3:28-5:00) and uses gated vocal bursts of 0.5-1.5 s every 1-3 s, 10-20 dB under the drums [R1 voice, WIN 0240].

Lineage: **archival-speech sampling over an instrumental band** is a recognisable tradition (documentary/"found voice" instrumental rock and electronic music, from tape-collage and sample-based electronica through to modern "sample-narrated" post-rock). The chop passage (3:28-4:20) turns the voice into a rhythmic instrument, which is the hip-hop/electronica sampling habit. The key sonic fact: the voice is **not the song's lead**; the lead pitch tracker finds no tune anywhere in the track except a possible A5/G#5 wobble at 4:30-4:36 [WIN 0260], and I would not trust that as a melody. This is an instrumental, not vocal, music tradition.

## 4. What it does not resemble (negative evidence, useful for ruling out)

- **Not song-form pop/rock:** no sung lead, no verse-chorus; voice absent 62% of the time and non-melodic when present [R1 voice].
- **Not breakbeat or drum and bass**, despite the CLAP "drum and bass" 0.93-0.99 at 4:45-4:55 [WIN 0280]: the kick is four-on-the-floor at 120 BPM [P]; the 161 reading comes from the dotted hat layer. Low confidence residual: a half-time D&B reading cannot be completely refuted, but there is no breakbeat snare displacement in the snare fold [P].
- **Not a classical or choral piece**, despite CLAP "choir/organ/bells": those labels fire in almost every window and the 0:00-1:28 pad has no articulated voice-leading [WIN 0020, 0060].
- **Not blues/funk/swing:** no swung feel; the semiquaver grid (0.125 s) is straight, and the dotted pattern is a 3:4 cross-rhythm rather than swing [R1 rhythm].
- **Not folk or acoustic:** the saturated, dense "other" wall and gated drums point away [WIN 0140, 0240].

## 5. Where each strand sits in time (for the form specialist)

| Time | Strand | Evidence |
|---|---|---|
| 0:00-0:28 | Film-score drone, free time, deep low strikes (8-12 s apart then every 4 s) | [WIN 0000, 0020; LV] |
| 0:28-1:28 | Sparse beat plus narration blocks over Bm-Em-G-D; "documentary" | [WIN 0020-0080; CH] |
| 1:28.6-2:36 | Motorik groove arrives; speech continues; Em-G-A-D rock loop | [WIN 0080-0140; CH] |
| 2:36-3:28 | Pure instrumental drive on Bm/D vamp; "other" lift at 2:48 | [WIN 0140, 0160, 0180; LV] |
| 3:28-4:20 | Chopped vocal texture over groove (rhythmic sampling) | [WIN 0200, 0220, 0240] |
| 4:20-5:04 | Release to wall of guitars/synths, A5/G#5 wobble, return of chops, abrupt stop | [WIN 0260-0300] |

## 6. Candidate lineages, ranked (all low-to-medium; CLAP is only a weak vote)

1. **Instrumental "post-rock with electronic pulse"** (medium): slow layered build, static modal chords, sampled voice, dense guitar-or-synth wall, cinematic quiet-start. CLAP "post-rock" 0.94 at 1:45 and 0.19 at 2:35 [WIN 0100, 0160] is a vote but a noisy one.
2. **Krautrock / motorik descendants** (medium): constant four-on-the-floor stomp, one or two chords for minutes, hypnotic repetition; CLAP "krautrock" 0.72-0.97 at 4:05-4:40 [WIN 0240, 0260]. My independent support: the kick fold and the harmonic share above [P]. Weakness: classic motorik is a snare-on-2-and-4 pattern with a driving hat, whereas this kick pattern plus a syncopated pick-up reads more like dance music; a real motorik drummer would show some drift.
3. **Synth-pop / electro-rock** (low-medium): CLAP "synth-pop" 0.72-1.0 for most of 1:40-3:00 [WIN 0100-0160]; the dotted-hat layer and drum-machine steadiness fit. But no sung hook or chorus.
4. **Dance/techno-adjacent build** (low-medium): the layer-adding arc and 120 BPM kick.
5. **Cinematic/ambient film score** (the frame only, 0:00-1:28).
6. **Industrial-rock / "aggressive" texture** (low): CLAP "aggressive" 0.86-0.99 at 1:50 and 2:25-2:30 [WIN 0100, 0140]; the saturated wall fits, the mood label is noisy.

## 7. Honest limits

- No instrument identification is possible from stems (guitar vs synth, machine vs live kit); every lineage statement therefore rests on rhythm, harmony, level and spectral shape, not timbre.
- CLAP is weak; I used it as a tie-breaker only, and "organ", "bells", "vinyl crackle" I disregarded.
- Whisper on archival Dutch speech is partly unreliable; I use only items that several passes agree on.
- "Era" and "regional tradition" cannot be read from audio alone; the Dutch speech is evidence of the speech source, not of the band's nationality.
- Demucs separation bleed (bass into vocals, drums into other) can inflate or hide features; kick/snare band folds are approximate.

## 8. Three questions for fellow specialists

1. **Rhythm:** Can you tell, from the snare-band fold or accent pattern, whether the beat is closer to the motorik snare-on-2-and-4 pattern or a pure four-on-the-floor dance beat, and does the dotted-quaver 0.375 s hat layer behave like a delay repeat (decaying copies, constant 3:4 lag from the kick) or like a programmed hat line? That would separate a guitar-band lineage from an electronic one.
2. **Sound:** Is there any measurable evidence (attack shapes in "other", harmonic share, odd/even harmonic balance, high-frequency noise bursts at note onsets, chorus-like modulation) that favours guitar-through-effects over synthesiser for the post-1:28 wall, and does the stereo width collapse at 1:28.6 look like a mix decision or a source change?
3. **Harmony:** Is the B-pedal/D-A-E bass pattern (B1 dominant, D2, A1, E2 [P]) better described as Aeolian/Dorian/pentatonic, and is there any real dominant (F# or F#m) approach before the Bm returns, or is the vamp strictly modal? This decides whether to call the idiom "rock riff" or "trance/ambient vamp".

(Also, for the form specialist: do the 4 s chord blocks and the 8-s gaps of the intro strikes support 8-bar phrases at 120 BPM, as the rhythm note suggests, and does the abrupt end at about 5:04 look like a planned cut or a loop truncation?)
