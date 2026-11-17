# t_dl_mirror: VOICE specialist, round 1 (blind, measurements only)

Role: voice, words and samples. Times m:ss. Evidence: the twelve window notes `win_0000.md` to `win_0220.md` (all read); `lyrics/whisper_medium_{mix,vocals}_auto_transcribe*.txt/json`; `music_views/window_0020s.png` (viewed; others consulted via the window notes); `stems_raw/htdemucs/song/*.wav`; `beat_times.json`; my scripts `v1/scripts/agents/voice_r1.py`, `voice_r1b.py`, `voice_r1c.py`, `voice_r1d.py`. Stem levels are dBFS RMS from the demucs vocals stem, which can leak. No context.md, research or web used.

## 1. One-paragraph picture

This is a vocal-led hip-hop song built as hook, verse, hook, verse, hook, verse, hook, then an instrumental outro. The voice has two different jobs. In the hook (about 20 s, four times) it sings or chants a narrow tune around G#4 to A4 (median 403-410 Hz), cut into short gated phrases. In the verses (about 40 s, three times) it drops about ten semitones to a near-monotone rap around A3/A#3 (median 218-230 Hz), one line per 4-beat bar, and becomes the loudest stem. The words are a first-person story that gets darker verse by verse (a hangover and a stranger in bed; road rage and a fight; street dealing and arrest), and the hook is the one fixed, almost reflective phrase between them: "You, you I see ... in my [?] in the morning ... just seein' me, I see". Confidence: structure high; hook wording medium; verse wording medium; story reading medium.

## 2. Placement and form of the voice (measured)

Vocal-stem activity map (stem above -40 dB, gaps merged under 0.5 s; `voice_r1.py`):

| Section | Vocal span | Length | What the voice does |
|---|---|---|---|
| Intro | none to 0:10.2 | 10.2 s | stem -70 to -74 dB (residue) |
| Hook 1 | 0:10.2 to about 0:30 | about 20 s | gated sung/chanted hook |
| Verse 1 | 0:30.4 to about 1:11 | about 41 s | rap, 16 lines |
| Hook 2 | about 1:12 to 1:31 | about 20 s | hook, twice through |
| Verse 2 | 1:31.4 to 2:12 | about 41 s | rap |
| Hook 3 | 2:12 to 2:34 | about 22 s | hook, twice |
| Verse 3 | 2:34 to 3:13.5 | about 39 s | rap |
| Hook 4 | 3:13.5 to about 3:35 | about 21 s | hook; last vocal at about 3:35 |
| Outro | 3:35 to 3:56.4 | 21 s | no voice (stem -70 to -78 dB) |

Verse and hook lengths are about 8 bars of 2.508 s (4 beats at 95.7 BPM, tracker beat interval 0.627 s) for each hook and 16 for each verse. High for the layout (vocal stem, three independent hook starts and three verse starts); medium for the exact bar counts, because Whisper timestamps are coarse (about 0.2 s).

Gaps inside the vocal. Every hook has a 1.0 to 1.25 s vocal dropout about 13 s in (0:23.8 to 0:24.8; 1:12 to 1:13 and 1:24.5 to 1:25.8; 2:13.2 to 2:14 and 2:25.8 to 2:26.8; 3:13.8 to 3:15 and 3:26.5 to 3:27.8), and a second shorter one (0:11 to 0:12.2 and 0:13.5 to 0:14.5 in the first hook). The verse blocks (0:24.8 to 1:12, 1:28.8 to 2:13, 2:29.8 to 3:13.8) run unbroken: 44 to 47 s with no gap over 0.5 s. So the hook is chopped and the verse is continuous. This confirms win_0000 and win_0020 (hook gaps with 30 dB or more drops in under 0.5 s). Measured, high.

Treatment. The vocal looks dry: broad harmonic ladders to about 4 kHz and fricatives to about 8 kHz in `window_0020s.png`, with hard cut-offs rather than tails (vocal panel at 4.8 s and 8 s into that window: the voice stops within a frame, no visible reverb decay). It is also near-mono: vocal-stem side/mid over the whole file is -50.5 dB (`voice_r1.py`). That means the width the mix shows at 0:10 and 0:18 comes from other layers, not the voice. Medium for "dry" (I looked at spectrograms only), high for "centred".

Level. Hook voice about -20.4 to -21.1 dB RMS against a mix at -10.4 to -10.7 dB (about 10 dB below the mix). Verse voice about -16.4 to -16.7 dB (about 6 dB below the mix) and the loudest stem in the verses (drums -19, other -28 to -30 per win_0020 and win_0040). In the hook the "other" bed is as loud as or louder than the voice. Measured (`voice_r1b.py`), high. Consequence: the hook sits inside the music, the verse sits on top of it.

Pitch. `voice_r1b.py` (pyin on the vocal stem, voiced frames only):

| Part | Median | p10 to p90 | Note |
|---|---|---|---|
| Hook 1 | 410 Hz | 225 to 505 Hz | wider because the first pass catches the entry notes |
| Hook 2 | 403 Hz | 349 to 445 Hz | F4 to A4 |
| Hook 3 | 405 Hz | 353 to 447 Hz | same |
| Hook 4 | 410 Hz | 351 to 445 Hz | same |
| Verse 1, 2, 3 | 230, 229, 218 Hz | 206 to 248, 209 to 252, 190 to 257 Hz | about G#3 to B3 |

The hook centres about 10 semitones above the verse (410/230 Hz). Correction to the win_0020 note, which describes the move as "about an octave and a half": it is about 10 to 11 semitones, just under an octave (410 Hz is about G#4/A4, 230 Hz about A#3). The D-A drone of the music puts the hook voice on the fifth (A) and the verse voice a semitone or so off the root's octave pitch class (A#/B against D-A), which the win_0040 note already calls tension. High for the figures.

Syllable rate (librosa onset count per second of the vocal stem, a rough proxy): verses 6.2 to 6.6 per second, hooks 3.6 to 4.9 per second. The earlier note says about 5/s from `stems_extra`; my count differs because it counts all vocal-stem onsets, so I treat it as "roughly 5 to 6.5 per second, fast speech-rhythm". Medium.

Sung or spoken? The hook is pitched (a stepwise contour F4 to A4, one leap to C#5 at 0:23.3 per win_0020) and is a singing-style tune. The verse is near-monotone and speech-like. INFERRED: hook sung/chanted, verse rapped. High. The CLAP "rapping 0.998" over the silent intro (win_0000) is not evidence for either (vocal stem -70 dB).

## 3. The words

Transcripts are Whisper medium passes (mix and vocals stem). Whisper flags the verse segments as "doubtful" (no_speech_prob 0.66 to 0.90) because rap over loud music reads as non-speech; but the lines are legible, rhyme, and the mix pass and the vocals-stem pass agree on 0:30 to 1:11 (checked line by line), so I use them. I do not reproduce a slur-like token that appears in the verse-3 mix pass (2:37 to 2:40, "my nigg..."); that line is a transcription I cannot settle and I leave it out.

Hook (high that it is a repeated fixed phrase; medium on the wording):
- Mix pass 0:10.9: "You, you I see"; 0:15.1: "In my carry in the morning"; later passes "in my hair and in the morning", "in my period in the morning", "in my ear and in the morning", vocals-stem pass 3:17.98 "In my theory and my morning"; closing "just seein' me, I see" / "I see you" / "You see in me, I see you".
- Safe reading: "You, you I see / In my ___ in the morning / [just] seein' me, I see (you)". The unknown word changes with each pass (carry, theory, hair, period, ear), which is the signature of an unclear word, not of a different word each time. Candidate: "mirror". It is two syllables, fits the stressed slot "in my ___ in the morning", and verse 1 ends on "look in the mirror, but today I seem out of place" (mix 1:06 to 1:11, vocals pass 1:06). INFERRED, low-medium. I base this on the verse-1 transcript only, not on the file name.
- Structure of the words: "You I see ... I see you" is a chiasmus (the same two words swapped): a reflected pair. Vocals pass 3:14 to 3:34 shows both orders ("You I see", "I see you"). Whether this is intended as a mirror image is interpretation (INFERRED, low); the swap itself is on the page.
- The hook is heard four times, always with the same words and the same sequence of gated phrases. Envelope correlation of the vocal stem between hook 2 and hook 4 sections is 0.75 and 0.88 at matched 10 s offsets (`voice_r1b.py`, hooks starting at about 1:12/1:22 and 3:14/3:24). Waveform cross-correlation between hook instances is only 0.05 to 0.29 with my rough alignment, so I cannot say they are sample-identical copies; they are the same phrasing, but whether a loop or a live repeat is not settled (low). I do not claim a loop machine from the voice.

Verses (medium; Whisper wording, I did not hear it):
- Verse 1 (0:30 to 1:11): wakes, stretches, sees "a strange lady" in bed, cannot recall her ("last night's blurry"), one shot to five, Henny on the rocks, bed bath and beyond, then the fiancé "on her way up the steps", hide the girl, pop tic tacs, hide the mimosa, run to the sink, "look in the mirror, but today I seem out of place". End rhymes daily / lady / blurry / hurry, one line per bar.
- Verse 2 (1:31 to 2:12): a morning drive in a 1995 Nissan, catching red lights, road rage, a gesture out of the window, a crash, "out of anger, jump out the car", a fight ("I put a crease in his cheeks ... I saw myself inside his blood").
- Verse 3 (2:34 to 3:13): street dealing ("baggies with the custom logo", "3 for 10 all day, that's my promo", selling to a minor who overdoses), then arrest and a cell ("can't ... lawyer, phone call", "life is living colour right now cause my time's up", "locked ... shiny aluminum toilet"). The mix and vocals-stem passes agree on the shape; individual words differ.
- Arc: the same morning-after-the-night frame gets more serious each time (embarrassment, violence, crime and custody), INFERRED, medium. The hook, which keeps the same words while the stories escalate, behaves like a refrain of self-regard. The "mirror" reading of the hook would tie hook and verse 1; that is low-medium.
- Quoting caution: the stems and Whisper give me words and rhythm, not delivery, tone of voice, irony or whether it is autobiographical. Not recoverable (below).

## 4. How words and music answer each other

1. Voice enters on the grid. The voice enters at 0:10.4 with a full-band hit, 0.07 s from the tracker beat at 10.47 s (46 dB jump in the vocal stem, bass -47 to -17 dB, per win_0000). Measured, high. It restarts at 0:12.3 (0.03 s from a beat). This is a point event, not a statistic.
2. Alignment statistic, honest version. For 13 vocal events (hook entries and gap edges, listed in `voice_r1c.py`) against the tracker beat grid (95.7 BPM, 0.627 s interval) the mean absolute offset is 0.15 s. A random point on that grid would average 0.157 s (a quarter of the interval), so this is no better than chance and I claim no vocal-on-beat sync result. Two reasons: my events are read from a 0.25 s envelope, and the gating edges may be set to a 16th grid I did not test. The drums are on a roughly 0.157 s sub-grid (win_0220 note, intervals at multiples of about 0.16 s, which is 0.627/4), so the beat-grid and kick-spacing grids agree; the voice edges just do not show a measurable preference with my resolution. Low confidence either way.
3. The verse sits on a 4-beat bar (one rhyming line per bar: line starts 30.38, 33.00, 35.54, 37.98, 40.56, a spacing of 2.44 to 2.62 s against a 2.508 s bar), same grid as the beat tracker. Medium.
4. Bass dropouts do not follow the words. I checked whether the bass-out gaps in the verse (win_0020's 36.0 to 40.2 s hole, bass out while voice and other continue) track the lyric ("blurry" memory lines). They do not: measured from each verse start the bass is out at about 6 to 10 s, 11 to 12.5 s, 16 to 20 s, 21 to 22.8 s, 26 to 30 s, 36 to 40 s in both verse 1 and verse 2 (`voice_r1d.py`), with different words. Verse 3 shows the same gaps shifted about 2 s (my start estimate for it is loose). So the bass cycle is a fixed loop under the voice, not a text-driven effect. I withdraw any "bass thins on 'blurry'" reading. High that the pattern repeats; this is a rhythm-section dropout only (mix drops about 4 dB, per win_0020's table), not silence.
5. Backing steps back for the rap. At 0:32 the "other" bed drops about 7 dB as the verse rises (win_0020), so the rap is made the foreground. Hook and verse are separated by level and register, not by a section of silence. Measured, high.
6. Hook as the harmonic moment. The only chord movement away from D is in the hook (G, F, C, Dm in 0:25.6 to 0:29.4 and G, F, Am at 0:16 to 0:19, per win_0000/0020), while verses sit on the D-A drone (win_0040). So the words that change are carried over a static bed and the one repeated phrase is carried over the moving harmony. High on the harmony (chroma, chords.json); the "refrain gets the colour" reading is interpretation.

## 5. Samples and production era (voice view)

- Is the voice a sample? Nothing in the vocal measurements says so: the verses are continuous 40+ s of new words (not looped), the lines rhyme, and the vocal stem has no repeated waveform. The hook words repeat, but I cannot tell sung-again from copied (cross-correlation 0.05 to 0.29, low). So no sampled voice is claimed. The 0:00 to 0:10 intro bed is the only candidate "sample", and it is not a voice.
- Era (INFERRED, medium): modern production: full-scale sample peaks at 0.0 dBFS (win_0000: 6,720 samples at or above 0.999 in the first 20 s), mix RMS -8 to -13 dB, voice centred (side/mid -50.5 dB) and 6 to 10 dB below the mix, verse rapped with gated hook; mono, band-limited bed under it (everything above about 9 kHz is missing, per win_0020 and win_0040). Whether the band limit is from an older source or from low-bitrate distribution is not separable because nothing full-range sits above it (win_0020 says this too). Kick onset spread was not measured here; win_0220 gives drum onset deviation 10.9 ms median from a 16th grid (about 23 ms frame limit), which says "tight" rather than "grid-perfect". Low-medium.

## 6. End of the track (10 ms envelope over the last 3 s, `voice_r1b.py`)

- The audio is 239.44 s long. In the last 3 s (3:56.44 to 3:59.44) the mix envelope is digital zero (about -180 dBFS, peak 0.002 over the whole 3 s, effectively nothing). The last audible sound is at 3:56.5 (last 10 ms frame above -70 dBFS), with level -50 dB or lower after 3:56.36.
- Not a hit ending: from 3:48 the mix falls (-15.3 dB in the 3:48 to 3:50 span, -25.1, -33.5, -57.8 at 3:56), the drums fall from about -19 to -68 dB, the other bed from -29.7 to -73 dB, bass in bursts. The five small 10 ms envelope peaks between 3:55.67 and 3:56.36 are -39 to -49 dBFS and sit on a decay, so I count them as the end of the fade, not as final hits. No voice (vocals stem -70 to -78 dB from 3:35.2). High.
- What this means for the voice: the song ends on the instrumental, not on a last word. The final vocal is the hook's closing line at about 3:34 ("I see you") and then 21 s of drone and drums fade. Measured, high.

## 7. What a listener is likely to feel (voice only, interpretation)

- 0:10 is an arrival: the first voice in the song comes in on a full-band hit, as the stem jumps 46 dB. INFERRED effect, medium.
- The chopped hook reads as hesitant, almost stuttering (metaphor), because of 1 s dropouts and 9 dB mix notches (win_0020 table). It sounds like someone catching themselves in the line "I see you / you I see".
- The verse arrives as a talking-pace stream: 6 or so syllables a second, one line a bar, the voice 6 to 10 dB louder than in the hook, in a lower register. It reads as a narrator who has taken over. The effect is pressure and momentum, helped by the voice never leaving for 40 s. INFERRED, medium.
- The ending (21 s of music alone, a slow fade, no last word) is an unresolved, open exit rather than a closed hook. INFERRED, low-medium.

## 8. Confidence summary

| Claim | Tag | Confidence |
|---|---|---|
| Hook/verse/hook... layout with spans above | measured | high |
| Hook sung/chanted, verse rapped | INFERRED | high |
| Hook pitch median about 405 to 410 Hz, verse about 218 to 230 Hz (about 10 semitones lower) | measured | high |
| Voice dry and centred | measured (side/mid) / INFERRED (dry) | high / medium |
| Hook words "You, you I see / In my ___ in the morning / just seein' me, I see" | INFERRED | medium |
| Missing hook word is "mirror" | INFERRED | low-medium |
| Verse stories (hangover, road rage, dealing/arrest) | INFERRED from Whisper | medium |
| Bass dropouts are a fixed loop, not text-driven | measured | high |
| No vocal-on-beat sync result | measured | low (resolution-limited) |
| Modern production | INFERRED | medium |
| Ending: instrumental fade, 3 s digital zero, last sound 3:56.5 | measured | high |

## Not recoverable by measurement
- Who is speaking or singing, or whether the story is autobiographical: stems show pitch and timing, not identity or intent.
- Exact words in the hook (carry/theory/hair/period/ear/mirror) and in the busiest verse lines: Whisper disagrees with itself; I cannot hear.
- Whether the hook voice is a sample, a loop or a fresh take each time: low waveform correlation is not proof either way.
- Tone: irony, humour, anger, regret: no measurement gives it; only register, level and rate.
- Whether the voice is processed (compression, autotune, reverb) beyond what the spectrograms show: demucs separation can add or remove such traces.
- Meaning of the bass and drum drop patterns for the performer: they repeat, but their intent is not measurable.
- The real source and age of the mono, band-limited bed: bandwidth does not give age.

## Questions for fellow specialists
1. To rhythm: are the 1.0 to 1.25 s vocal dropouts in each hook, and the chopped phrase edges, on the 16th grid (0.157 s) of the kick, measured on the drum stem with a 10 ms envelope? My 0.25 s resolution made the on-beat test no better than chance.
2. To harmony: does the hook's G-F-C-Dm / G-F-Am excursion fall on the same words each time ("In my ___ in the morning"), and does the D-A drone with the verse voice a semitone off (A#3/B3 against D/A) read as a deliberate clash or as speech pitch?
3. To form: the hooks are 20 to 22 s and the verses 39 to 41 s, always with the bass pattern repeating from each verse start; do you read the 21 s voiceless outro as a fifth block or as an extension of hook 4, and does the 3 s of digital zero after 3:56.5 count as part of the track?
