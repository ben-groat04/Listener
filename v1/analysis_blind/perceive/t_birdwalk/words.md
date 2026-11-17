# t_birdwalk: the words (blind mode)

Method: three stored Whisper medium passes (mix transcribe, mix translate, vocals-stem transcribe) compared, plus my own re-run of faster-whisper medium (cpu, int8, language forced "en", word timestamps) on seven windows of the Demucs vocals stem (0-30, 28-58, 56-72, 110-135, 132-152, 150-172, 170-188 s). Language: English (stored pass p=0.92 mix, 0.95 vocals), American hip-hop/club-rap idiom. No non-English speech heard by any pass. I cannot hear the audio; times are Whisper's and drift by about 0.5 to 1 s. Duration 3:08 (188 s), tempo estimate about 152 BPM (probably a half-time 76 feel, speculation).

## Who speaks
- Voice 1 (0:00 to about 0:27): a male rapper/MC addressing the listener ("Aye man, we got this new dance"). Spoken, conversational, announcing a dance: an intro spoken to the crowd, not a narrator or interviewee.
- Voice 1 (0:28 to 1:07 and 1:10 to 1:57): the same rapper in rhymed bars, with ad-libs ("ey", "man", "ow"). Possibly one lead plus a doubled/chorus layer on the hook (SPECULATION; the stem cannot separate them).
- No reporter, narrator or interviewee. Wordless/ad-lib material after about 1:57 (see below).

## Era and quality
Modern (2000s to 2010s) club rap, studio-produced and clean; the vocal stem is loud and continuous (about -15 to -25 dB) from 0:01 to 2:47, so the vocal is dry and forward. No tape hiss or archival sound inferred. Era is judged from vocabulary ("crunk", "club", "haters", "money in the bank") and polished sound. Confidence: medium.

## Transcript (best reconstruction)
Confidence: H = at least two passes agree and phrase is clear; M = plausible, passes differ on a word; L = guess.

| Time | Original (English) | Conf | Notes |
|---|---|---|---|
| 0:00-0:06 | "Aye man, we got this new dance, man ... it's called the bird walk, man." | M | Mix pass: "Aye, man, we got this new dance, man, yea, man"; vocals pass adds "it's called a bird walk". Translate pass gave "What you doing?", a poor guess. |
| 0:06-0:23 | "Watch me do that bird walk, watch me do that bird walk, that bird walk, do that bird walk" (repeated) | M | Hook chant under the intro. Whisper's stem output garbles it ("bird won't"). Exact repeat count unknown. |
| 0:23-0:27 | "Soulja unit in the club, we get money, ow" | L | Pass-specific: translate "Soulja unit in the club"; vocals "saltier unit"/"Soldier"; mix "3-2-1 cider with goalie" (hallucination, rejected). Sounds like a shout-out/tag ("Soulja unit"); I cannot say what it refers to without outside knowledge. |
| 0:28-0:32 | "We don't out-dance no more, we just bird-dance at home / that ho" | M | "out dance" is in all three passes. Last word differs: "at home" (mix, vocals) vs "that hoe" (translate). Unresolved. |
| 0:32-0:35 | "In the club, get crunk, I can do it all night" | H | Vocals pass says "get drunk"; "crunk" is the two-pass reading and fits the idiom. |
| 0:35-0:39 | "Lean with it, rock, move that, move right" | H | Echoes a familiar dance-chant formula (SPECULATION: a call-and-response dance instruction). |
| 0:39-0:42 | "Soulja unit in this ho, I'ma show you how it go" | M | Tag repeated. "in this hoe" (translate) vs "so chill you in the end zone" (mix, rejected). |
| 0:42-0:46.6 | "Do that bird walk, man, I'ma show you how it go" x2 | H | |
| 0:46.6-0:49 | "I'ma show you how it go, do that bird walk, ey, that bird walk" | H | |
| 0:49-0:58 | "Watch me do that bird walk, ey, watch me do that bird walk; that bird walk, ey, that bird walk; watch me do that bird walk" | H | Hook, about 9 s. |
| 0:58-1:10 | "Do that bird walk, ey, that bird walk; watch me do that bird walk (x2)" (repeating) | M | Translate pass lists these in 3 s blocks (0:58 to 1:10); the mix pass lists only one line over the span and my stem re-run of 56-72 returned nothing. Stem still shows vocal energy (-17 to -22 dB). The vocal stem pass heard "that bird walk, watch me do..." at 1:00 to 1:10. Present but uncertain in detail. |
| 1:10-1:14 | "I step up in the club in my all-white ones" | M | "club" (translate) vs "pub" (mix, vocals). Later "when I'm in the club" supports "club". "All-white ones" is probably white trainers (SPECULATION). |
| 1:14-1:17 | "Looking so fresh, looking like some bums" | H | Boast with a twist: fresh/bums. |
| 1:17-1:20 | "I don't really care what you haters gotta say" | H | |
| 1:20-1:23 | "'Cause I got that money, money, money in the bank" | M | "bank" (mix, translate) vs "back" (vocals). |
| 1:23-1:26 | "I always get cake, cake, like it's my birthday" | H | |
| 1:26-1:29 | "Today you hate, so it's your worst day" | M | Vocals pass: "your birthday" (probably a mishearing, but possibly a rhyming wordplay). Next lines support "worst". |
| 1:29-1:32 | "Tomorrow's my best, tomorrow's your worst" | H | |
| 1:32-1:35 | "Today is my best, I fuck with the best" | H | Explicit. |
| 1:35-1:38 | "You know I get that money, money, you looking dummy" | M | "dummy" (mix, translate) vs "gummy" (vocals). |
| 1:38-1:42 | "Looking so bummy, all-white nuttin's" | M | |
| 1:42-1:45 | "Nutty buddies on your feet, 'cause he's/you're so bummy" | M | "Nutty Buddies" is a snack name; here it seems to be a jibe at the target's white shoes (SPECULATION). "he's" (mix, translate) vs "you" (vocals). |
| 1:45-1:48 | "'Cause he's so bummy, bummy. Show you what it do" | M | |
| 1:48-1:51 | "Show you how it go, show you how I do" | H | |
| 1:51-1:54 | "When I'm in the club, you know we coming through" | H | |
| 1:54-1:57 | "So icy, so nice, so whitey, whitey ..." | M | "whitey" is repeated; the mix pass runs it for 28 s (1:51 to 2:19), which is a classic Whisper repetition loop, and the 110-135 s stem re-run did the same. Real count unknown; probably a few ad-libbed repeats, perhaps a chant. |
| 1:56-1:58 | "White tits that kill me, that's how I do" | L | Translate pass only; likely a misheard rhyme line. Treat as unverified. |
| 1:58-2:05 | "Do that bird walk, ey / that bird walk, ey / watch me do that bird walk, ey (x2)" | M | Translate pass, short 1.4 s segments, consistent with a hook return. |
| 2:07-2:39 | "Watch me do that bird walk" (repeated) | M | Mix pass says 2:19 to 2:45 "Watch me do that bird walk"; vocal-stem pass heard "burr-wop / bird walk" at 2:29 to 2:39; my 150 to 172 s re-run: one segment at 2:31 to 2:47 "Watch me do that bird walk" (x2). Loop-prone region. |
| 2:39-2:47 | "do that bird walk" (repeated) | L | Translate pass lists a long run to 3:04 that is a repetition loop. Stem is loud until about 2:47 (-19 to -21 dB), then collapses (2:48 -48 dB, 2:49 to 2:56 about -70 dB, silent). |
| 2:57-3:00 | wordless or one short ad-lib | L | Stem blips -36/-35 dB at 2:57 to 2:58, -46/-52 dB at 2:59 to 3:00; no transcript. Could be a reverb tail or a single "ey". |
| 3:00-3:08 | instrumental ending | M | Stem silent. |

## Phrases carrying weight
- "Bird walk" is the title and the hook (about 40 repetitions): an invitation to a dance, the song's only real "thesis".
- "Tomorrow's my best, tomorrow's your worst / Today is my best, I fuck with the best" (1:29 to 1:35): the one place where the lyric builds a contrast (my time versus yours) and the emotional peak of the boast.
- "I don't really care what you haters gotta say" (1:17): defiance.
- "So icy, so nice, so whitey" (1:54): style/status as the payoff line.
- "Show you how it go" / "I'ma show you how it go": the promise to teach the dance, which is the song's direct address.

## Interpretation (labelled)
Genre braggadocio plus a dance-craze song: the first minute is the "new dance" pitch, the second is status boasting about white trainers and money versus "bummy" rivals, and the end returns to the dance hook. Tone: playful, cocky, party. Ambiguous or crude phrases ("ho", "fuck with", "white ones") are only as certain as marked.

## Reliability notes
- Whisper's mix pass hallucinates "3-2-1 cider with goalie", "so chill you in the end zone" and the long "whitey"/"do that bird walk" loops; rejected or discounted.
- The translate pass is more detailed for the hook but is a transcription task in English too; its "that hoe" and "white tits" readings are single-source.
- Whisper no-speech probability is high (0.58 to 0.87) on stem windows because the stem is processed rap; do not read that as absence of speech.
- Names ("Soulja unit") are sound-alikes only.
