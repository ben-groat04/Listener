# t_birdwalk: VOICE specialist, round 1 (blind, measurements only)

British English; times m:ss. I cannot hear. Everything below comes from stems, spectrograms, pitch tracks, transcripts and my own measurements. I did not read context.md, research notes or non-blind analysis, and used no web.

Evidence key
- [WN] = the ten window notes `win_0000.md` to `win_0180.md`
- [Wnnnn] = `music_views/window_nnnns.png` (I opened W0, W140, W160 myself)
- [LVL] = `per_second_levels.json`; [LN] = `lead_notes.json`
- [TR-mix] / [TR-voc] / [TR-tr] = Whisper medium on the mix, on the vocals stem, and the "translate" pass
- [V1]-[V5] = my scripts `v1/scripts/agents/voice_birdwalk.py`, `voice_birdwalk2.py`, `voice_birdwalk3.py`, `voice_birdwalk4.py`, `voice_birdwalk5.py` (all on `stems_raw/htdemucs/song/vocals.wav`)

## 1. Headline

1. **The voice is the lead instrument and almost never stops.** Between 0:01 and 2:47 the vocal stem is active (above -45 dB) for 83-100 per cent of every section. The only real gaps are 2:47.7-2:56.9 (9 s, stem at about -65 dB, i.e. bleed) and 2:59.9 to the end [V1]. Confidence high.
2. **There are two kinds of vocal material, and they behave differently on every measurement I tried.**
   - **Hook chant** ("Watch me do that bird walk"): a **short loop of about 12.1 s that is pasted back again and again, as audio, not re-performed**. It is stereo-wide, sits in a low A2-C3 band, and is the part that the bass and drums are taken away from and put back under.
   - **Verses** (0:24-0:47 and 1:10-1:58): **freshly performed, never repeated, and dead-centre mono**.
   Confidence high for repetition and mono-versus-wide; medium for the "pasted loop" reading (see section 4).
3. **Voice and drums are locked.** Vocal onsets land within 50 ms of drum hits 83-100 per cent of the time in sparse sections, against about 40 per cent expected by chance [V5]. The voice is the rhythm part as much as the drums are.
4. **Falling vocal sweeps** (short descending chirps, about 3 kHz down to 1.5 kHz in 0.7-0.8 s) are the voice's only "effect" material. They mark transitions: before the first drop (0:09-0:12), before the hook returns (2:32-2:35), at the end of the hook (2:44-2:47) and as the last thing the voice does (2:56-3:00) [W0, W140, W160, V4].
5. **No sung melody.** Pitch is speech intonation around a few semitones; the pitch tracker's "notes" are formant and register evidence, not tune.

## 2. Voice map (what the voice is doing, section by section)

| Time | Voice | Evidence |
|---|---|---|
| 0:00-0:00.9 | Silence. Vocal stem blank, then -37 to -23 dB at 0:01. The first drum hit (0:00.81) and the first vocal onset (0:00.93) arrive together. | [W0]; [LVL]; [LN] first note 0:00.93 |
| 0:01-0:12 | Spoken talk-in, then the chant begins (about 0:07). Mid-register, E3-F#3 falling to D3 and B2-A2. L/R correlation 0.68 (wide-ish). Falling chirps at 0:09.4-0:12. | [W0] vocals panel; [LN]; [V4] |
| 0:12-0:24 | Chant over the first full drop (bass and drums enter at 0:12.2). Low: A2 (9 notes), C3 (5), G#2, C#3. Two high jumps (B3 0:17.5, A3 0:17.7). | [LN]; [W0] |
| 0:24-0:47 | **Verse 1**: near-monotone recitation on D4 (about 294 Hz; D4 21 notes, C#4 10, C4 6, D#4 4 out of 51). L/R correlation 0.99 (mono). Level the highest of the track (-17 dB RMS). Syllable rate fastest (median onset gap 0.157 s, 5.9 peaks/s). | [LN]; [V1] [V4] |
| 0:47-0:59 | **Hook, bass out**: chopped, clipped syllables locked to the sparse drum hits (1.4-1.5 s apart). Back low (A2, C3). Stereo-wide (L/R 0.55). | [WN win_0040]; [V4] [V5] |
| 0:59-1:10 | Hook with bass and drums back, "Yeah, that bird walk, watch me do that bird walk" x many. | [TR-voc] 1:00-1:10 |
| 1:10-1:58 | **Verse 2** ("I step up in the club/pub in my all white ones..."). Register moves up to G3-G#3 (G3 27, G#3 13 of 59). Mono (L/R 1.00 at 1:11-1:40, 0.98 at 1:41-1:59). Level about 3-4 dB lower than the hook (-21 dB). Only one gap over 0.35 s (1:27.2, 0.5 s). | [LN]; [TR-voc]; [V1] |
| 1:58-2:47 | **Hook, long**: low A2-C3 bounce (A2 36, C3 25, A#2 11, G#2 9 of 102 notes between 2:00 and 2:48). Wide (L/R 0.54-0.58). Contains the 12 s bass-out passages 2:00-2:11 and 2:23-2:35. | [LN]; [V4]; [WN win_0120, win_0140] |
| 2:40-2:47 | Voice chopped hardest: short formant-banded bursts every 0.2-0.4 s, then a falling chirp at about 2:44.5-2:47 as the voice leaves. | [W160] vocals panel x 0-7 s; [WN win_0160] |
| 2:47.7-2:56.9 | **No voice** (9 s). Drums brighten and get louder, bass shifts. | [V1] gap list; [LVL] vocals -58 to -70 dB |
| 2:56.5-3:00 | One falling glide (about 3 kHz to under 1 kHz), then a short falling phrase (C5, D#4, C#4, B3 at 2:58.5-2:59.9 per [LN]). The last vocal sound. | [W160] x 16.5-19.5; [LN]; [V4] |
| 3:00-3:08 | No voice. | [LVL] |

## 3. Words, and how far to trust them

The transcripts are weak evidence here. Whisper is working on fast, processed, partly masked speech, and the three passes disagree.

What the passes agree on:
- The title phrase **"Watch me do that bird walk" / "that bird walk"** is the hook. It appears in [TR-mix] at 0:00-0:15 and again 0:46-1:07, 2:19-2:45; in [TR-voc] at 1:00-1:10 and "that burr-wop, watch me do that burr-wop" at 2:28-2:39 (a mis-hearing of the same chant; confidence medium).
- The verse at 1:10-1:56 is read near-identically by all passes: boasting about white trainers ("I step up in the club/pub in my all white ones, looking so fresh..."), money, "today you hate, so it's your worst day / tomorrow's my best, tomorrow's your worst", then "show you what it do, show you how it go", "when I'm in the club, you know we comin' through, so icy, so nice, so whitey" [TR-voc, TR-mix]. Words are a swaggering boast. Confidence medium-high on the gist, low on exact words ("club" versus "pub", "bummy/gummy/dummy").
- Interjections: "ey", "yeah", "aye, man" appear as ad-libs between hook lines [TR-mix 0:46-0:55; TR-voc 1:00].

What they disagree on, so I will not quote it:
- 0:00-0:12: "What you doing?" [TR-tr] versus "Aye, man, we got this new dance, man, yea, man" [TR-mix]. Both read it as spoken, conversational banter before the chant. I would only say: **a short spoken, chatty address ("we got a new dance"-type) leading into the dance-name chant** (medium).
- 0:24-0:47 (verse 1): [TR-mix] "we don't out dance no more, we just bird dance at home / the club get crunk, I can do it all night / lean with it rock, move that move right"; [TR-tr] has different words in the same places ("Soulja unit in the club", "we get money"). Gist: club, dancing, stamina. Words not reliable.
- [TR-mix] 0:07-0:28 contains "3-2-1 cider with goalie, man" and 1:51-2:19 a runaway "whitey, whitey, whitey..." repetition. Both are typical Whisper hallucinations. [TR-voc] has **no text at all between 1:57 and 2:28 and between 2:40 and 2:56**, exactly where the hook loop and the chopped voice are densest. The hook's words in these passages are inferred from the waveform repeat in section 4 (they must be the same words as 0:47-0:59), not transcribed.

What this means: the lyrical content is a dance-craze chant plus a braggart verse. The meaning of the words is thin and repetitive; their sound (hard consonants "b", "d", "k", "w") matters more. Interpretation, not measurement.

## 4. The hook is a repeated audio loop (my main measurement)

Method [V2, V3]: for every 3 s block of the vocal stem (16 kHz mono), I searched the rest of the track (excluding the same 10 s) for the best-matching waveform by normalised cross-correlation.

Results:
- **Hook material matches itself at r = 0.7-0.9 across minutes.** Examples: 0:49 against 2:25.4 (r 0.88, lag +96.36 s); 2:31 against 0:54.6 (r 0.82, same lag); 2:25 against 0:48.6 (r 0.81, same lag); 2:40 against 2:27.9 (r 0.76, lag 12.08 s); 0:19 against 2:42.4 (r 0.75).
- **The lags are repeatable and close to multiples of 12.1 s**: 12.17, 24.39, 72.16, 84.17, 96.36, 108.58, 143.38 s, and a 47.0 s match between 0:14 and 1:01, i.e. the two bass-entry drops at 0:12.3 and 0:59.4 carry the same vocal start. The 12.1 s unit is also the length of the bass-out passage 0:47-0:59 and of each 2:11-2:23 / 2:23-2:35 block. A matching waveform at r 0.8-0.9 (not 1.0, because demucs bleed from drums and "other" differs from pass to pass) says the same recorded vocal take occurs at each location. Medium-high confidence that this is a copy, not a new performance; a human cannot repeat a 12 s rap to within a few milliseconds.
- **Verses do not match anything**: verse 1 (0:25-0:45) and verse 2 (1:13-1:55) show best-match r of 0.08-0.14, which is noise. They are single, unrepeated takes.
- The repeated unit is about eight drum-bar spacings long (12.1 s against the 1.5-1.6 s one-hit-per-bar spacing, about 7.8), so it is a bar-aligned loop in length, though the exact grid is a rhythm question.

Hook appearances, by this measurement: 0:12-0:24 (partial; r 0.4-0.75), 0:47-0:59, 1:00-1:10 (weaker, r about 0.4-0.5, plausibly because loud drums and bass mask the stem), 1:58-2:47 (about four repeats: 2:00, 2:11, 2:23, 2:35). So the hook is not one chorus but **a reusable vocal block that the producer lays over different backings**.

Consequence: the "variation" listeners feel inside the hook is almost all in the backing (bass on/off, drums sparse or dense, "other" bursts), not in what the voice says. The voice is the constant; the instruments are the variable. That is the opposite of a normal song, where the voice is the part that moves.

## 5. Placement, treatment, space

**Stereo image** [V4], vocals stem L/R correlation:
- Verses: 0.99 (0:25-0:47), 1.00 (1:11-1:40), 0.98 (1:41-1:59). Side-to-mid energy is -24 dB and -38 dB below mid [V1]. The voice is dead-centre, dry and close.
- Hook sections: 0.54-0.68 throughout (0:01-0:24, 0:48-1:10, 2:00-2:47), side energy only about 5-7 dB below mid [V1]. The voice is clearly wider: doubled, stereo-processed or stereo-reverbed, or partly mixed with stereo "other" material that demucs has put in the vocals stem. I cannot separate these. Confidence high that the difference exists, low on its cause.
- This agrees with the mix width in the window notes (narrow 0:24-0:45; wide 0:47-0:58, [WN win_0040] and [LVL]). The width of the whole mix therefore follows the voice treatment as much as it follows the bass.

**Level**: vocal stem about -17 dB (verse 1) to -21 dB (verse 2), -19 to -20 dB in the hooks [V1]. Verse 1 is the loudest voice of the track. It is typically 3-18 dB above "other" and, at 0:01-0:11, above everything [WN win_0000].

**Band and compression**: vocals show full harmonic stripes up to about 4 kHz, with consonant energy up to about 8 kHz and a hard roll-off near 10 kHz [W0, W140, W160]. The ridges are steady with little level movement, which is consistent with heavy compression, but I cannot prove it from a spectrogram. Low confidence.

**Falling chirps** [V4, W0, W140, W160]: ridge tracking shows repeated descents from about 3.2 kHz to 1.5 kHz in about 0.7-0.8 s (e.g. 9.41-10.2 s, 152.65-153.55 s, 164.84-165.5 s). In the spectrograms they look like a parallel ladder of falling lines, so a pitched, harmonic sound (a pitch-dropping voice sample, a "whoop", or a siren-like effect) rather than noise. They appear in the vocals panel and sometimes also in "other" (W160 x 17.5-19.5), so demucs may be splitting one sound. Occurrences: 0:09.4-0:12 (into the first drop), 2:32.5-2:35.5 (into the return of bass and drums at 2:35.7, [WN win_0140]), 2:44.5-2:47 (end of chant), 2:56.5-3:00 (final). Confidence high they exist and fall; low on identity.

## 6. How voice and music answer each other

1. **Voice carries the groove when the drums do not.** In the sparse sections the voice provides 4-5 syllables per second (median onset gap 0.19-0.20 s, about a sixteenth at the 152 BPM grid, 0.197 s) while the drums give one hit per 1.5 s. Voice onsets coincide with those drum hits in 83 per cent (0:01-0:12, 0:48-0:59) and 100 per cent (2:01-2:11) of cases within 50 ms [V5]. So the "one hit per bar" is a downbeat marker that the voice lands on, and the voice fills the bar's subdivisions. This answers the rhythm specialist's third question: **yes, the chant is about one syllable per sixteenth at the 152 grid** (syllable rate 4.4 per second against 5.1 for sixteenths; slightly slower because words have rests), and **the verses stay on the same grid** (peaks per second 4.0-4.9, median gap 0.19-0.20 s in 1:11-2:11), not floating. Verse 1 is faster (0.157 s median gap, 5.9 per second), which would suggest a triplet or double-time feel but may be jitter from the very strong D4 formant pulses. Medium confidence.
2. **Remove the voice's partners, not the voice.** At 0:47, 2:00 and 2:23 the bass goes and the voice stays; the voice is the thing the listener is left holding. When the voice itself leaves (2:47.7-2:56.9) the drums get louder and brighter and the bass shifts, so the rhythm section takes over. The voice is therefore **an alternate to the rhythm section**: the track alternates between "voice with sparse hits" and "rhythm section with no voice".
3. **Falling chirps are punctuation.** Each one sits immediately before a change in the backing (0:12 drop, 2:35.7 return) or at the final exit.
4. **Register tracks section.** High (D4, 0:24-0:47), low (A2-C3, hooks), middle (G3, verse 2). Verse 1 is a pitch above the chant; verse 2 is pitched a fifth-plus above A2 and sits on G3/G#3, i.e. close to the G colour that the harmony specialist reports at 1:23-1:47 [harmony.md]. The speaker's pitch rises into G while the rest of the sound stays on A. Speech intonation, so I would not call it a harmonic move; it is a delivery move.
5. **The hook's A2-C3 bounce** (A2 and C3 together carry about 60 per cent of the hook's notes; C#3 only 8 of 102 [LN]) is on the minor third (C) rather than the major third (C#). Because the hook is a pasted loop, the same recorded intonation recurs; it is a fixed feature of the take, not a development.

## 7. Cross-check of the window notes

Agreements: voice begins about 0:00.9 [win_0000]; verse 1 on D4, narrow, mono, 0:24-0:47 [win_0020, win_0040]; chant low A2-C3 in 0:47-0:59 and 1:00-1:10 [win_0040, win_0060]; rap switches at 1:10.4 [win_0060]; continuous rap 1:20-1:40 [win_0080]; voice gone 2:49-2:56 and falling glide at 2:57-2:59 [win_0160]; no vocal after 3:00 [win_0180]; chirp at 2:32.5-2:35.5 [win_0140].

Tightenings and corrections:
- [win_0000] and [win_0140] both call the falling lines "a pitched glide, siren or tape effect". I measure a **series of short descending chirps (3.2 to 1.5 kHz in 0.7-0.8 s)**, not one continuous glide, and they occur four times (0:09, 2:32, 2:44, 2:56), not once.
- [win_0040] says the chopping is "in time with drum hits". Measured: confirmed (83-100 per cent within 50 ms, chance about 40 per cent).
- [win_0160] says the voice is "chopped" 2:40-2:47. The measured syllable rate is the same as elsewhere (about 4.4 per second); what makes it feel chopped is the stem's short formant bursts with gaps, plus the loop structure. It is not a faster rate.
- [win_0160] reads the voice as "absent 2:49-2:55". Exactly: no voice from 2:47.7 to 2:56.9 [V1].
- No window note spotted the **12.1 s repeat** or the **mono verse / wide hook** split. These are new.
- [win_0100] and [win_0140] lean on Whisper for text where Whisper returned nothing (1:57-2:28 and 2:40-2:56 in [TR-voc]). I treat those words as inferred.
- CLAP says "no vocals" in several windows where the voice is plainly the loudest stem [WN win_0080]; I ignore CLAP's voice labels.

## 8. What the measurements cannot tell me

- Who is speaking, age, accent, how many voices. The "male register" reading rests on the 100-200 Hz notes (A2-G3) and is medium confidence only. Whether there is a second voice (a backing "ey" or a shouted response) is not separable; the stereo-wide hook might hide a doubled take.
- The words of the hook passages that Whisper did not transcribe, and the exact words of verse 1.
- Whether the hook loop is a sample from an existing record or the artist's own recording pasted. I can only say that it repeats exactly.
- Whether the falling chirps are a voice, a synthesiser or a sound effect.
- Whether the D4 verse is pitch-shifted or just a higher, more tense delivery. D4 (294 Hz) is high for a male chant that sits at A2-C3 elsewhere; verse 1 could be a different performer, a pitched-up vocal, or a different microphone distance. L/R correlation 0.99 shows it is centre-mono, consistent with a single close mic. Confidence low on cause.
- Actual loudness impression of consonants.

## 9. Feeling (my reading, labelled as interpretation)

A dance-craze chant. Part of the feeling is deliberate repetition: the same 12 s phrase hammered back under different backings, so the hook gets lodged by sheer recurrence. The verses give relief by being closer, flatter and more personal (mono, dry, centred), a swaggering boast delivered almost on one note (D4 recitation). The loud, wide, repeated hook against the narrow, plain verse creates a cheerful-aggressive alternation between "crowd" and "one man talking". The final sound the voice makes is a falling swoop that stops in mid-air, with the beat running on a few seconds without it: a deflation more than an ending. Medium confidence; mood claims cannot be measured.

## 10. Three questions for fellow specialists

1. **To FORM:** I find the hook loop (about 12.1 s, r 0.75-0.9) at 0:12, 0:47, 1:00, 2:00, 2:11, 2:23, 2:35 and verses that never repeat. Does your section map treat 0:12-0:24 as the first hook entry or as intro-extension? Is the 12.1 s unit a clean 8-bar block on your bar grid, and do the verse boundaries (0:24, 1:10, 1:58) sit on multiples of it?
2. **To SOUND:** vocals are stereo-wide in the hooks (L/R correlation 0.54-0.68) and mono in the verses (0.98-1.00). Does the "other" or mix stereo analysis show a stereo loop (a doubled vocal, or a stereo guitar/synth) that demucs may be putting into the vocals stem, and can you separate genuine vocal doubling or reverb from bleed? And are the falling chirps at 0:09, 2:32, 2:44 and 2:56 harmonic (a pitched sample) or noise-like?
3. **To LINEAGE:** the artefacts here (a pasted exact vocal loop, a one-note recitation over sub-bass, drums reduced to one hit per bar with the voice supplying the subdivisions, boast-style verse) are what sort of production practice, and does it read as a dance-craze single built for club use, such as a chant designed so that a crowd can join in? Is a voice that never leaves the foreground (measured gaps over 0.35 s before 2:47 total only about 1.4 s: 0:00-0:00.9 and 1:27.2) typical for that family?

(Also relevant to RHYTHM and HARMONY: the rhythm question about syllable-per-grid-beat is answered in section 6.1; the harmony question about C versus C# in the hook is answered in section 6.5: C is dominant, C# rare, and because the hook is a repeated recording this is a property of the take.)
