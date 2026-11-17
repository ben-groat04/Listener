# t_birdwalk: VOICE specialist, round 1

Scope: voice, words and samples across the whole track (188.15 s). I read all ten window notes (win_0000 to win_0180) and re-checked them against the stems, the images and new measurements. Helpers: `v1/scripts/agents/voice_r1.py`, `voice_r1b.py`, `voice_r1c.py`. Timestamps m:ss. Tags: measured / INFERRED / speculative, with confidence.

## 1. Summary

- The voice is the lead layer for the entire track. The vocal stem has a >=0.3 s pause (10 ms RMS below -50 dBFS) only three times between 0:01 and 2:47: at 1:27.2, 1:38.1 and 1:39.6 (voice_r1.py). It is then absent for 9.2 s (2:47.7 to 2:56.9), returns for about 2 s (2:57 to 3:00 as a glide), and is gone for the last 8 s. Measured, high.
- Delivery is rap and chant, not singing. Lead f0 mostly sits in 104-156 Hz (G#2-D#3) with brief excursions to D4 (about 294 Hz, 0:25-0:46) and sweeps (lead_notes.json, window images). INFERRED, high that it is spoken or rapped delivery.
- The hook words "that bird walk" and "watch me do that bird walk" are legible in both Whisper passes and match the file name. INFERRED, high. The verse (1:10 to 1:56) is a rapped boast; wording is medium-reliability.
- A recurring vocal gesture: a downward diagonal glide of harmonics in the vocal stem that arrives at a structural change. Found five times (section 5). INFERRED (treated voice), medium.
- The hook is re-voiced, not copy-pasted: nearest-neighbour matches of 3.2 s vocal chunks reach 0.8-0.9 correlation (random pairs mean 0.32, 95th percentile 0.45) but never above 0.91, so repeats are close but not bit-exact. Medium.

## 2. Words (what is, and is not, recovered)

Sources: `lyrics/whisper_medium_vocals_auto_transcribe.txt` (covers 1:00 to 1:56 and 2:28 to 2:39 only) and `..._mix_...txt` (covers 0:00 to 2:45). They differ on several words, so I tag words by agreement.

| Time | Text (best reading) | Agreement | Tag |
|---|---|---|---|
| 0:00.8 to ~0:08 | "Aye, man, we got this new dance, man ... watch me do that bird walk" | mix pass only | hook phrase INFERRED medium-high; opening words medium-low |
| 0:08 to 0:28 | "that bird walk, do that bird walk"; the following "3-2-1 cider with goalie, man" | mix pass only | the first half legible; the "cider with goalie" tail is a misrecognition (win_0000.md), low |
| 0:28 to 0:46 | "we don't out-dance no more, we just bird dance at home / the club get crunk / I can do it all night / Imma show you how it go, do that bird walk, man" (twice) | mix pass only | medium for "show you how it go, do that bird walk"; low for the rest |
| 0:46 to 0:59 | "do that bird walk, ey, that bird walk / watch me do that bird walk" repeated | mix pass | medium-high |
| 1:00 to 1:10 | "that bird walk, watch me do that bird walk" x several | both passes agree | high |
| 1:10 to 1:56 | verse: "I step up in the pub / club, all white ones, looking so fresh, looking like some bums / I don't really care what you haters gotta say / I got that money, money, money in the back / bank / I always get cake ... like it's my birthday / today you hate, so it's your worst day / birthday / tomorrow's my best, tomorrow's your worst / today is my best / you lookin' dummy/gummy, lookin' so bummy / all white nuttin's, nutty buddies on your feet / show you what it do, show you how it go / when I'm in the club, you know we comin' through / so icy, so nice, so whitey" | two passes agree on structure and most words; differ on pub/club, back/bank, worst day/birthday, dummy/gummy | words medium; verse structure high |
| 1:56 to 2:28 | no reliable text. The mix pass has "whitey" x ~60 in one 28 s segment, a decoder loop | rejected | the vocal stem is active at -18 to -23 dBFS/s, so there is voice here; words not recovered (high) |
| 2:19 to 2:45 | "watch me do that bird walk" (mix); "that burr-wop, watch me do that burr-wop" (vocals pass, 2:28.8 to 2:39.3) | disagree on last word | phrase INFERRED medium-high; exact syllables low. The file name and the earlier 1:00 section favour "bird walk" |

Note on "whitey": the whole-mix pass has the word repeated, and the vocals-stem pass has "so whitey" once at 1:56. I take "so icy, so nice, so whitey" as a heard line (two passes, medium) and the repetition as a decoder artefact (medium).

The verse contains strong language ("I fuck with the best", 1:32 to 1:35, both passes agree). It is a braggadocio rap (money, white trainers, "you hate, so it's your worst day"). Interpretation of tone is in section 7.

Beyond the words, the semantic role is simple: the verse is the only passage that is "about" something; everything else is the hook phrase used as rhythm.

## 3. How the voice is placed (measured)

Level, from `per_second_levels.json` and the vocal stem:

| Section | Vocal stem level (dBFS/s) | Vocal stereo side/mid (vocals.wav) | Notes |
|---|---|---|---|
| 0:01 to 0:12 | -18 to -25 | 0.43 | loudest layer; no bass, one hit per 1.56 s; mix -17 to -22 dBFS |
| 0:12 to 0:47 | -14 to -21 | 0.25 | bass (-13 to -15 dBFS) is now louder than voice; voice centred (mix width 0.04-0.10 from 0:24) |
| 0:47 to 0:59 | -18 to -22 | 0.55 | bass stem gone (-72 dB), mix falls about 7-8 dB (win_0040.md); voice widens |
| 1:00 to 1:56 (hook then verse) | -17 to -25 | 0.27 | voice 3-5 dB quieter in the verse, other stem up 5-8 dB (win_0060.md) |
| 1:56 to 2:47 | -17.6 to -23 | 0.51 to 0.54 | in 2:24 to 2:35 the mix level is only about 1.5 dB above the vocal stem, i.e. the mix is nearly voice alone (win_0140.md) |
| 2:47.7 to 2:56.9 | -58 to -71 | n/a | voice removed for 9.2 s |
| 2:57 to 3:00 | glide | | then <= -70 dB to the end |

Caution: the stereo-width differences come from the demucs vocal stem; some of the width may be separation leakage from the "other" stem. The mix-level width (per_second_levels) does confirm a widening in 0:47 to 0:58 (0.37 to 0.71 against 0.06 to 0.18 before), so that one is real. Measured, medium.

Spectral character: vocal-stem spectral centroid about 1.2-1.3 kHz in the opening, 1.67 kHz at 0:25 to 0:40 (the higher chant), 1.2 kHz in the 0:47 recitation, 1.5 kHz in the verse (1:20 to 1:40). The vocal stem is empty above roughly 6 kHz in every image, like the rest of the mix (win_0020.md measured a hard cut at 6 kHz across all stems). So the voice is as band-limited as everything else; there is no separate lo-fi voice layer.

Dryness: the vocal panels show short decay between syllables (dark gaps between vertical bursts, e.g. window_0120s.png), so the voice is close-miked or dry. No audible tail can be measured; reverb itself is not recoverable from separated stems (low).

Pitch behaviour (lead_notes.json, window images):
- 0:01 to 0:12: E3-D3-C#3, narrow, hovering; spoken contour.
- 0:12 to 0:23: G#2 to A3 (a quick leap to B3/A3 at 0:17.5), low rap register.
- 0:24 to 0:46: voice jumps about 17 semitones (G#2 to C#4/D#4 at 0:23.9) and sits on D4 / C#4 (277 to 294 Hz), a two-note chant of about 4 semitones range. This reads as hook as riff.
- 0:47 to 0:59: back down to G#2-D#3, flat recitation.
- 1:10 to 1:56: verse mostly G3 to A#3 per win_0080/0100 notes; 2:00 onwards G#2 to D#3 again.

(Octave caveat: tracker jumps such as C5 at 0:40.5 and 0:44.3 are probably octave errors; the 0:25 to 0:40 chant at D4 is stable and visible in the image, so I trust that.)

## 4. Voice and rhythm

Grid for all statistics below: the tracker beat grid from `audio_features/beat_times.json` (median beat interval 0.394 s, 152 BPM). Check against kick spacing: kick onsets (drum stem, 40-150 Hz band) have a median inter-onset interval of 0.788 s in 1:00 to 2:47, i.e. exactly two beat intervals (0.77-0.79 s). So the beat grid and the kick agree; in the 0:12 to 0:47 window the kick IOI median is 1.79 s (kick sparse, 15 onsets, not a result), and in the intro one hit per 1.56 s = one 4-beat bar.

Vocal onsets (vocal stem onset detection, 10 ms hop) against that grid, mean resultant length R (0 = uniform, 1 = locked), by beat and by eighth-note:

| Span | n onsets | R (beat) | R (8th) | onsets per second |
|---|---|---|---|---|
| 0:01 to 0:12 | 19 | 0.65 | 0.47 | 3.3 |
| 0:13 to 0:47 | 41 | 0.50 | 0.68 | 3.0 |
| 0:47 to 0:59 | 28 | 0.65 | 0.85 | 3.75 |
| 1:00 to 1:50 | 103 | 0.44 | 0.69 | 3.7 (4.35 in 1:20-1:40) |
| 1:50 to 2:47 | 116 | 0.63 | 0.77 | 3.75 |
| 2:08 to 2:20 | 23 | 0.66 | 0.77 | |
| 2:20 to 2:26 | 14 | 0.73 | 0.85 | 4.3 |

Reading: syllables lock to the 8th-note subdivision (0.197 s) much more than chance (chance R is about 0.27 for n=20-30; R 0.68-0.85 is clearly above), most strongly in the stripped sections (0:47 to 0:59, 2:20 s). So the voice is on the grid, and in the stripped passages it carries the pulse. The median vocal onset gap in 2:24 to 2:35 is 0.404 s against a 0.394 s beat (measured): about one syllable per beat on the mid-beat accents plus 8th-note fillers. Measured, high. The intro (R 0.47 at 8th) is looser, consistent with the free "announcement" feel noted in win_0000.md, but n=19, so low confidence.

The earlier claim in `voice_as_music.txt` (circular mean phase of whole segments, R 0.125) refers to phrase starts only (n=14), a different statistic; it does not contradict this table.

Vocal-bass-drum interplay: the voice is never ducked by the beat in any measurable way. voice_as_music.txt: accompaniment -16.2 dB during voiced against -15.1 elsewhere (-1.1 dB). That is a "no ducking" result because the voice is nearly continuous.

## 5. Treated voice: the recurring downward glide

In the vocal-stem panels there is a diagonal bundle of harmonics falling in frequency (an instantaneous pitch fall of an octave or more over 2-3 s). It appears at:

| Glide (approx.) | Window image | What happens straight after |
|---|---|---|
| 0:09.3 to 0:12.5 | window_0000s.png | 0:12.1: bass enters (+50 dB in the bass stem), mix +4.9 dB, denser drums |
| 0:43.5 to 0:46.7 | window_0040s.png (vocal panel x = 3.5 to 6.7) | 0:47: bass stem out (about -60 dB), mix -7 to -8 dB |
| 2:08.5 to 2:11.3 | window_0120s.png (vocals and mix, x = 8.5 to 11.3) | 2:11.4: bass and dense drums enter (bass panel x = 11.4) |
| 2:45 to 2:47.3 | window_0160s.png (vocal panel x = 5 to 7.3) | 2:47.3: voice leaves for 9.2 s; drum-led passage |
| 2:57 to 3:00 | window_0160s.png, window_0180 notes (pyin 880 Hz at 2:57.9 falling to about 108 Hz in about 2.3 s) | 3:00.4 to 3:08: fade-out, voice gone |

Evidence quality: the first and third are visible in both the vocal and the mix panels; the second and fourth in the vocal panel with weaker mix trace; the fifth is the cleanest (my pyin trace plus the lead pitch panel). In the 2:08 to 2:11 case the "other" stem has no matching streak, so it is in the vocal stem, not stem leakage from the other layer. Measured (visible), high. That it is the same treatment each time, and that it works as a "riser / transition" marker, is INFERRED, medium. Whether it is a pitch-shifted vocal, a tape-stop, a vocal glide by the performer, or a sample, cannot be told (see the final list).

Not every transition has one: the 0:59.4 re-entry (bass +53 dB, mix +11 to +14 dB within 0.2 s) has no visible glide in window_0040s.png (the vocal panel shows ordinary bursts). So the voice "announces" four of the five big events and the end, not all.

## 6. Repetition, sampling and chops

- Hook re-use (new measurement, voice_r1b.py): log-mel normalised cross-correlation of 3.2 s vocal chunks against the whole vocal stem. Best matches: 1:00.3 with 2:36.6 = 0.83; 1:03.5 with 2:39.8 = 0.77; 2:00 region (2:08) with 0:57.6 = 0.8; 2:32 with 2:07.6 = 0.91. Verse chunks (1:10 to 1:50) best-match only 0.53 to 0.64: no verse line is repeated. The control (300 random pairs) averages 0.32, 95th percentile 0.45.
  Interpretation: the hook sections are close repeats of one delivery pattern, with the same words and rhythm, but not bit-exact copies (a copy under identical processing would give >0.95). So either the hook was re-performed or the same recording sits under different surrounding mix content. INFERRED, medium-low. I cannot distinguish a re-performance from a copy that stem separation has smeared differently.
- Window 0140's own check (vocal bar-to-bar similarity 0.78-0.96, same as control sections) agrees: no loop signature.
- Chops: the win_0160 note counts 25 gated vocal chops in 7 s (2:40 to 2:47) with a median pitch of 112 Hz. In window_0160s.png the vocal panel at 0 to 7 s is a run of discrete vertical bursts of harmonic ladders separated by dark gaps, on the same grid as the drum hits (the drums panel shows matching vertical stripes). I confirm the stuttered, gated look. INFERRED, medium: a gated or chopped treatment of a spoken line, as opposed to ordinary rap pacing. Syllabic rap at about 4.3 onsets per second has about the same appearance, so low-medium.
- Voice removal 2:47.7 to 2:56.9: the vocal stem is at -58 to -71 dB for 9.2 s while drums and bass continue at full level (window_0160s.png, drums and bass panels). The mix level drop is about 0 dB as the drum/bass groove replaces it (mix -12 to -14 dB before and after per win_0160). This is a vocal dropout, not a silence; the rhythm section carries on. Measured, high.

## 7. How words and music answer each other

1. Introduction as announcement (0:01 to 0:12). Voice with one hit per bar and no bass. Words "we got this new dance ... watch me do that bird walk" literally introduce a dance, so the words explain the context. The musical state (sparse, loose, voice forward, 3.3 onsets per second against 152 BPM) equals "someone speaking at the front of the room". INFERRED, medium.
2. Hook as riff (0:24 to 0:46). The words are less important than the shape: a two-note chant on D4/C#4 with stabs. The words become a rhythmic motif. High that the hook is used as an instrument; the tone (playful, cocky) is INFERRED, medium; CLAP "playful" 0.5-1.0 is weak support only.
3. Stripped recitation (0:47 to 0:59). Voice drops about two octaves, widens (side/mid 0.55 against 0.25), the bass leaves. The same four words repeat every 1.5 to 3 s. This is the "slow-motion show-off", words repeated until they stop meaning anything. Interpretation tag: INFERRED, low-medium; the measured facts are the register fall, widening, bass removal, and syllables locked to 8ths (R 0.85).
3b. In 0:59.4 the groove returns with the hook ("that bird walk, watch me do that bird walk" at 1:00 to 1:10) and then the verse starts at 1:10.4. The words move from the move (hook) to the boast (verse): "all white ones", "money", "cake", "you hate", "you so bummy". The lyric content is self-regard against haters. The music supports it: the verse sits lower in the mix (-3 to -5 dB, other stem +5 to 8 dB), so the voice is part of a texture rather than the sole lead.
4. 1:56 to 2:46. The words are not recoverable (Whisper loop), but the voice is continuous and, in 2:24 to 2:35, almost alone with the sparse hits (mix about 1.5 dB above the vocal). The rap is the music here. CLAP's "no vocals 1.0" at 2:20 to 3:05 is wrong against the stem levels (-17.6 to -23 dBFS/s), so I discount the CLAP voice tag entirely (consistent with win_0120/0140/0160).
5. Ending (2:57 to 3:08). The voice turns from words to a falling glide, then vanishes while the groove continues for about 1.5 s, then fades over about 6.5 s (win_0180). The last word-like content is the 2:46 hook; the last voice sound is the glide ending about 3:00.1 and the stem never rises above -72 dB after 3:00.5.

Where lyric content and music disagree: a boastful lyric ("tomorrow's my best, tomorrow's your worst") sits on a harmonically static A pedal with narrow-range delivery. There is no melodic payoff; the emotional lift comes from the mix changes (register jump 0:24, bass drop 0:12/0:59/2:11). So the words do not carry the emotional contour; the arrangement does. INFERRED, medium.

## 8. Production-era cues (voice side)

- Peak: sample peak 1.0 (0 dBFS) in the whole file and in every window measured (win_0000, 0020, 0040); mix RMS -11 to -13 dBFS at the loud sections, crest 11-12 dB. Taken together this reads as a modern, limited master. INFERRED, medium-high.
- Band limit: the whole mix, voice and drums included, is empty above about 6 kHz (win_0000: -23 dB at 6 kHz, -35 at 7 kHz; win_0020: 6 kHz step). Because it covers the voice stem as well, the voice is not an old narrow-band sample sitting inside a full-range modern mix. It is a band-limited rendering of the whole track (encode/resample or deliberate lo-fi). INFERRED, medium-low.
- Voice vs archive material: none of my measurements indicate that the voice is archive speech. It sits at the same band limit as the beats; its stereo spread varies with sections (0.25 to 0.55 side/mid); the syllables lock to the 152 BPM 8th grid (R 0.68-0.85), a pattern that fits a modern rapped vocal performed over or with a beat. INFERRED, medium-high that this is a contemporary rap vocal, not a period archive sample.
- Kick spread (for the beat the voice sits on): intro hits one per 1.56 s with SD about 30 ms (win_0000); the 0:47 to 0:59 hits sit on a 1.557 s line with residuals up to 44 ms (win_0040, RMS about 33 ms). Looser than a quantised DAW grid, but consistent with a drum-stem separation or loose sampled one-shots; not a conclusive loop sign.

## 9. End of track (voice and mix)

From `audio/song.wav` and the four stems, 10 ms RMS envelope, last 3 s (duration 188.15 s): the mix peaks at -22.8 dB (around 185.0 to 185.3 s) and ends at -65.1 dBFS; the last point above -60 dB is 188.01 s (3:08.0), and the mix sits -60 to -68 dB for the last 0.14 s. Stems: vocals max -72.1 dB, last -72.4 dB, never above -60 dB in the final 3 s; drums last above -60 dB at 187.73 s; bass at 187.84 s; other at 186.91 s. Count of final hits in the 10 ms mix envelope (peaks in the last 3 s): five, at 185.25, 186.02, 186.43, 187.23 and 187.62 s (per win_0180.md; consistent with my drums-stem kick spacing of 0.4 to 0.8 s, i.e. the beat grid continues while fading). No voice, no final event. High.

## 10. Questions for fellow specialists

1. Rhythm specialist: for the hook-riff passages (0:24 to 0:46), do the bass stabs and the voice's D4/C#4 onsets share an exact grid or are the voice onsets about an 8th-note off the bass? My table shows only the voice side on the 152 BPM tracker grid; can you check the bass-to-voice offset against the same grid and the 0.788 s kick spacing?
2. Form specialist: I find a falling vocal glide arriving at 0:12.1, 0:47, 2:11.4, 2:47.3 and 3:00. Does the form reading (A / B / C sections) treat these as boundaries or as part of the next section, and does the missing glide before 0:59.4 mean 0:59.4 is a different kind of boundary?
3. Sound specialist: can you tell from the stems whether the glide is a pitch-shifted vocal (formants move with pitch), a tape-stop, or a synth riser blended into the vocal stem? And is there any measurable reverb tail on the voice at the 0:47 to 0:59 stripped section, where the voice is widest (side/mid 0.55)?

(For the lineage and feeling specialists: the genre cues here are a rap vocal on a fast 152 BPM, half-time-feeling, bass-and-hit groove; I would like lineage to say whether this delivery style belongs to a known regional rap dance-hook tradition, and feeling to say whether the 0:47 recitation reads as menace or comedy.)

## 11. Not recoverable by measurement

- Exact words in 0:00 to 0:46 and in 1:56 to 2:28: Whisper on rap with dense beats is unreliable (misrecognitions like "cider with goalie", the "whitey" loop); there is no clean vocal pass for the first minute.
- Who is rapping, whether the voice is one person or a double, and whether the same performer sings the hook and the verse: pitch and timbre statistics do not identify a person.
- Whether the hook is a sample (copy) or a re-performance: the best match 0.91 is not bit-exact, but separation smearing could explain it.
- What the downward glide is (pitch-shift effect, tape-stop, sample, performer slide): the stems show harmonics falling but not the cause.
- Whether the chops at 2:40 to 2:47 are an edit or ordinary rap pacing: both give gated bursts at about 4 onsets per second.
- Intent, irony and tone of the lyrics (comic, aggressive, affectionate): measurements give delivery shape, not attitude.
- Recording date or origin of any voice material: nothing in the measurements dates it; the band limit and peak level apply to the whole mix.
- Reverb or room: separated stems cannot confirm a room tail.
