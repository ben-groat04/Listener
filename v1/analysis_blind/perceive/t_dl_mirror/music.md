# t_dl_mirror: the music (blind, ears-only reading)

Sources used: audio_features/summary.json, beat_times.json, stems (RMS and mp3s), music_views (chords, CLAP tags, 20 s windows), lyrics (whisper), sync.json, plus my own measurements (`v1/scripts/agents/music_extra.py`, `music_stems_extra.py`; outputs in `v1/data/t_dl_mirror/audio_features/extra/`). I cannot play audio. Everything is inferred from numbers and spectrogram images. No frames were opened for this file, so there are no 'literal/reading' picture notes and no 'unread' print list. I did not read context.md or analysis/.

Tags: OBSERVED = measured or read directly in the data; INFERRED = follows from observations (named); SPECULATED = a guess. Confidence in brackets.

## 1. At a glance

| Item | Finding | Tag, confidence |
|---|---|---|
| Length | 239.4 s (3:59). Music ends in a fade over about 3:50-3:59 | OBSERVED, high |
| Tempo | about 95.7 BPM (beat interval median 0.627 s). Tempogram also peaks near 92 and 185-199 BPM (double time) | OBSERVED for numbers; INFERRED that the felt pulse is about 96 (or a half-time feel of about 192), medium |
| Key | D minor (whole-song score 0.69; D minor top in every 30 s block). Chord labels flip between "D" and "Dm" | OBSERVED; INFERRED D minor tonal centre, medium-high. The D/Dm flip probably means the third is weak or ambiguous (sparse bass and loop), SPECULATED |
| Genre | Hip-hop (rap over a sampled, loop-based beat with a sung hook) | INFERRED from rap-style vocal delivery in the transcript, drum-machine-like percussion, heavy sub-bass; high |
| Stereo | Effectively mono: side-to-mid ratio about -109 dB over most of the song | OBSERVED, high. (One-off sample differences exist, so not bit-identical, cause unknown) |
| Loudness | Very even: RMS median about 0.30 across 10-225 s; crest factor and per-second rms show almost no dynamic movement | OBSERVED, high |

## 2. Instrumentation (with evidence)

- **Drum-machine or sampled drums, steady, hard-edged.** OBSERVED: the drums stem is nearly constant at about 0.10 RMS from start to the fade; spectrogram shows vertical broadband strikes on a grid from 0:00. INFERRED: programmed or sampled hip-hop drums, not a live kit (no kit-like decay variation visible; the pattern is the same every bar). Medium-high. The CLAP model labels 'drum machine' about 1.0 in most windows, but see caveat in section 8.
- **Heavy sub-bass / 808-style low end.** OBSERVED: energy below 80 Hz is the largest band by power in every 10 s block (about 24,000-36,000 units vs 3,000-24,000 for mids). The bass stem shows sharp attacks followed by decay and silence (spectrogram window 0-20 s, bass panel). The bass's tracked pitch is mostly D2 (about 73 Hz), with D#2 and F2 as neighbours and G1/G#1 in the hook. INFERRED: a plucked or 808-type bass line centred on D. Medium. Caveat: the chroma over the whole file is dominated by F and E (about 0.9), which is almost certainly sub-bass partials or tuning artefacts of the bass, not the key. So I trust the D-minor key estimate from the chord and key detector, with medium confidence.
- **Sample/loop layer in the mids ("other" stem).** OBSERVED: harmonic stripes in 250-2000 Hz repeating exactly bar to bar (0-10 s window, "other" panel), with a hard stop at about 3.2 s and about 8 s where the whole loop cuts out for a beat. INFERRED: a looped sample (keys/guitar/strings-type) rather than a played part. SPECULATED that it is a chopped soul-type sample; there is no direct evidence of source. Low confidence on timbre; high on 'looped'.
- **Vocals: two modes.** OBSERVED: (a) verses: sustained spoken-rhythmic delivery, median fundamental about 231 Hz (roughly A#3), onset rate about 5.3 per second while rapping (about 3.3 per beat, close to sixteenth-note density); (b) hooks: pitch-tracked notes mostly A4, G4, F4 (about 350-440 Hz), i.e. a sung or half-sung melody. INFERRED: rapped verses with a sung/chanted hook. High for rap, medium for sung.
- **No clear live guitar, piano or orchestral content evident.** INFERRED from absence of sustained harmonic content other than the loop; medium. CLAP labels 'piano', 'synthesizer' and 'glockenspiel' in odd windows; I treat these as unreliable (section 8).
- **Possible vinyl-crackle texture.** OBSERVED: CLAP labels 'vinyl crackle' near 1.0 for most windows. Unverified by me; SPECULATED, low confidence.

## 3. Structure map

Boundaries: auto-sections (summary.json), the vocal stem (vocals present 10-215 s in one span), whisper segment times and my 10 s band blocks. Section lengths fit about 95.7 BPM in 4/4 (one bar about 2.51 s): 8 bars about 20 s, 16 bars about 40 s. INFERRED (bar counts), medium-high.

| Time | Section | Evidence | Tag, confidence |
|---|---|---|---|
| 0:00-0:10 | Intro: beat and loop only, no vocal | vocals stem at floor until about 10.4 s; bass hits sparse (bass silent about 74% of tenths); loop breaks at about 3.2 s and about 8 s | OBSERVED, high |
| 0:10-0:30 | Hook 1 (about 8 bars). Vocal enters about 10.4 s with a sudden loud burst, melody from about 12.3 s | the loudest moment is 10.7 s; mid and air bands jump (mid 4k to 12k, air 3k to 10k); bass is present 79% of the time; chords include G/Gm and F, so more harmonic movement than elsewhere | OBSERVED; INFERRED 'hook' because lines repeat later, high |
| 0:30-1:11 | Verse 1 (about 16 bars). Starts about 0:28-0:30 with a one-bar lead-in ("still seein' me, I see you" per whisper, doubtful) | vocals steadier; mids 21-23k; bass silent about 69% of the time (so the bass is gated or sparse); chords almost only D/Dm | OBSERVED, high |
| 1:11-1:32 | Hook 2 | same signature as hook 1: bass back (84% present), mids fall to about 10-13k, chords Dm/Gm/F | OBSERVED, high |
| 1:32-2:13 | Verse 2 | as verse 1; whisper starts a new verse at 1:31 | OBSERVED, high |
| 2:13-2:32 | Hook 3 | auto-section boundary at 2:13 (132.9 s) and 2:32 (151.9 s) | OBSERVED, high |
| 2:32-3:14 | Verse 3 | whisper: new verse at 2:32; auto-section A to 194.5 s | OBSERVED, high |
| 3:14-3:35 | Hook 4 (final hook) | vocal stem active to about 215 s; last vocal line ends about 3:34-3:35 | OBSERVED, high |
| 3:35-3:50 | Outro: instrumental, beat and loop, bass returns to verse-like sparseness | vocal stem at zero after about 215 s; bass silent 69%; auto-section "D" 3:35-3:50 | OBSERVED, high |
| 3:50-3:59 | Fade out | rms falls to near zero, sub energy collapses (1,164 vs 24,000 in prior block) | OBSERVED, high |

Section pattern: Intro / Hook / Verse / Hook / Verse / Hook / Verse / Hook / Outro. INFERRED: the form is verse-hook alternation with the hook always the same length, so the song is built as three stories bracketed by a refrain. Because the hooks fit exactly in 8-bar blocks and every verse is 16 bars, the structure is rigidly regular. High.

Fine-grained note: the whisper timestamps put a short lead-in ("Still seein' me, I see you") before each verse, so the hook seems to run about 1-2 s past the auto boundary on the vocal track. OBSERVED timing, INFERRED reading, low-medium (whisper timing is a fraction of a second off at best).

## 4. Texture shifts: the one musical device that matters

The song has almost no dynamic movement, so the main change is in texture between the two states. Measured per 10 s block (units are STFT power):

- **Hook state** (0:10-0:30, 1:10-1:30, 2:10-2:30, 3:10-3:40): mid band about 8,000-13,000, bass present about 80%, bass stem mean about 0.125-0.129, percussive share lower (about 0.31-0.34), chords move (Gm, G, F appear).
- **Verse state** (0:30-1:10, 1:30-2:10, 2:30-3:10): mid band about 21,000-24,000 (the rapped voice), bass present only about 30%, bass stem mean about 0.055, percussive share higher (about 0.40-0.45), chords almost entirely D/Dm.

OBSERVED, high. INFERRED: the bass drops out under the rap and returns under the hook, giving the hook a warmer, fuller low end each time it comes back, while the verse leaves room for the words. Medium-high; alternative explanation is stem-separation leakage (the rapped voice masking the bass), so SPECULATED that the bass really stops rather than being masked, low-medium.

## 5. Rhythm and groove

- OBSERVED: tempo about 95.7 BPM, with a spread (10th to 90th percentile of local tempo 92-123 BPM) that reflects detector wobble rather than real change; the median beat interval is steady at 0.627 s.
- INFERRED: a mid-tempo, head-nodding groove; rap at this tempo reads as unhurried but the vocal density (about 3 syllable-onsets per beat) makes the verses feel fast on top. Medium.
- Beat grid check: my attempt to find where kicks and snares fall within the bar gave flat histograms (counts near-equal across all 16 sixteenth-steps). I treat this as a failed measurement (the beat tracker has no bar-start anchor and the 1 s resolution of drum onsets is noisy), so I make no claim about kick/snare pattern or swing. Tag: not measured.
- Picture relationship from sync.json (for the other agents): cuts land within 80 ms of a beat 29% of the time vs 25% by chance; so cuts are only weakly beat-locked. Cut rate correlates with loudness at r about 0.31-0.35. Section boundaries have a cut within 0.5 s in 6 of 9 cases. OBSERVED.

## 6. Emotional arc (how it would feel to a listener)

All INFERRED unless stated; medium confidence for the arc, low for fine feelings.

- 0:00-0:10, **Cold open.** A dry, repeated groove with stops: a loop that breaks for a beat twice, as if setting a scene. Slightly uneasy (CLAP: 'calm/eerie/tense', unreliable). Minor key.
- 0:10-0:30, **Jolt, then refrain.** At 10.4 s a sudden loud vocal burst (the loudest second of the file, 10.7 s) breaks the intro, then a sung, circling refrain over a fuller bass. Sounds like a chant: repeated phrases ("you, you I see" per whisper; the rest of the words are unclear).
- 0:30-3:14, **Three stretches of continuous rap.** With the bass thinned out and the mid-range filled by the voice, this is the driving, insistent part. The whisper text is the only evidence of content: the verse lyrics (doubtful, no_speech_prob 0.66-0.90) seem to tell three separate episodes. Verse 1 (from about 0:30): waking up next to a stranger after drinking, hiding her as a fiancee approaches. Verse 2 (from about 1:31): a car journey ending in a road-rage fight. Verse 3 (from about 2:32): street-level selling of drugs and arrest. These are the whisper transcript's words, which may be wrong in details (names, brand names, some slurs and numbers are doubtful). I report the gist only. INFERRED: a narrator whose situations get darker verse by verse. Medium; the verse 1 gist is the most reliable because whisper (mix) and the translate pass agree.
- 3:14-3:35, **Closing refrain.** The same chant, now after the heaviest story, so the repeated line carries more weight. INFERRED. The words "I see you / in my [?] in the morning" suggest looking at oneself or at someone (mirror motif; the file name hints at 'mirror' but that is from the filename only, not from audio). SPECULATED.
- 3:35-3:59, **Wind-down.** Voice stops at about 3:35; the loop continues alone for about 15 s and then fades. Quiet exit rather than a final hit.

Overall: not a build-and-release arc. Loudness is flat, so the emotional movement comes from the story told in the words and from the alternation of refrain (fuller, more melodic) and verse (barer, more insistent). INFERRED, medium-high.

## 7. How the music frames the words

- **Verses leave the low end open and put the voice at the centre.** The bass thins when rapping starts (measured, section 4) and the mids belong to the voice, so every word is audible against a minimal beat. INFERRED: the music is arranged as a stage for the story. Medium-high.
- **Metre.** Verse lengths of 16 bars and hooks of 8 bars sit exactly on the 4-bar grid, so the stories are told in fixed bar-sized instalments; each verse ends and the same refrain returns. INFERRED, medium-high.
- **The refrain repeats while the story changes.** The same sung lines come after three different episodes, which lets the refrain recolour as the stories darken. INFERRED, medium; the whisper wording of the refrain varies from pass to pass ("in my carry", "in my period", "in my ear") so the exact words are UNCLEAR. I do not choose one.
- **Chord movement is saved for the hooks.** G/Gm and F chords appear mainly in hooks; verses sit on D/Dm. OBSERVED; INFERRED: the hook is where the harmony opens up. Medium.
- **The voice is the only changing element in a locked groove.** The beat does not react to the story (flat loudness, same loop). INFERRED: this gives a deadpan, matter-of-fact telling even when the content is violent or sad. SPECULATED as a listener impression, low-medium.

## 8. Caveats and measurement problems

- **CLAP tags are unreliable here.** They report 'no vocals' (about 1.0) for most windows from 0:30 to 3:35, although whisper and the vocals stem show rapping there; they report 'rapping' only in the intro-adjacent windows (0-10 s, where the vocals stem is silent) and in the outro (215-235 s, where it is silent too). So the voice-type tags are inverted or unusable. The instrument tags (drum machine, synthesizer, piano) are zero-shot guesses; I use them only as weak support. OBSERVED contradiction, high.
- **Whisper on the mix is poor in this file.** Verse text is flagged doubtful; names, numbers and slurs may be wrong; the hook wording varies from run to run; 'Thanks for watching!' at 3:56 is a hallucination over a vocal-free fade. I use only the gist, with medium confidence.
- **Tempo octave.** I could not separate 96 vs 192 BPM from the data alone. 96 is chosen because the beat tracker and the median beat interval agree and because rap at this speed has about 3 syllables per beat. Medium.
- **Chords**: the chroma-based labels (D vs Dm) are noisy and the sub-bass skews the chroma. Key: medium-high; individual chords: low.
- **No bar-level drum pattern was measured** (see section 5).
- **Not done**: swing ratio, true downbeat alignment, exact kick/snare/hat pattern, sample identification.

## 9. Moments a listener would remember

1. **0:10 (10.4-10.7 s): the vocal burst.** The first voice arrives suddenly after ten seconds of beat; this is the loudest second in the file. OBSERVED loudness; INFERRED 'jolt'. High.
2. **0:03 and 0:08: the loop stops for a beat.** Two short holes in the intro loop that set up the groove. OBSERVED, medium-high (read from the spectrogram window).
3. **The refrain's return at 1:11, 2:13 and 3:14.** Each time the bass comes back fuller and the voice turns melodic after about 40 s of rap. OBSERVED, high.
4. **The turn into verse 3 at 2:32.** Subject matter (per whisper) shifts to street dealing and ends with an arrest-like scenario, and the last refrain follows at 3:14. INFERRED, medium; content wording uncertain.
5. **3:35: the voice stops** and the loop runs alone, then fades by 3:59. OBSERVED, high.

## 10. Confidence summary

- High: runtime, form (intro/hook/verse x 3/outro) and section times to about 1-2 s, mono image, flat dynamics, vocals present 10-215 s, rap in verses vs sung hook, sub-bass-heavy balance, fade-out.
- Medium-high: D-minor centre, about 96 BPM, drum-machine/loop-based production, hook-vs-verse bass difference.
- Medium: genre label detail, emotional arc, story gist of the verses, the harmonic opening in the hooks.
- Low: sample/loop timbre and source, vinyl crackle, individual chord labels, exact hook words, any claim about kick/snare patterns.
