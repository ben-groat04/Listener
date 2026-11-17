# video2 ("Elfstedentocht Part 2"), VOICE specialist, round 1

Evidence tags: [LVL] music_views/per_second_levels.json (vocals-stem dBFS); [IMG nnnn] music_views/window_nnnns.png; [LN] lead_notes.json; [LYR] lyrics/ passes (medium Dutch mix, small mix, vocals-stem pass which auto-detected Welsh and is therefore hallucinated); [CLAP]; [S1] scripts/agents/voice_v2_bursts.py (vocals.wav RMS bursts, 50 ms hop, threshold -52 dB); [S2] scripts/agents/voice_v2_repeat.py (mel similarity between bursts). I cannot hear the audio; everything is read from measurements. I have read all sixteen win_*.md notes and re-checked their voice claims.

## 1. Headline
There is no singing anywhere in this track (high). Every "voice" event is either (a) a spoken Dutch archive narration, 0:42-2:36, or (b) from 3:24 to the end, short bursts of vocal-stem energy that are not intelligible and read as chopped, looped or heavily treated voice or crowd-like sample used as a rhythmic instrument (medium). The track therefore has a two-part voice design: **a story told in sentences (first half), then the same voice material turned into percussion (second half)**. The lead-pitch tracker on the vocal stem produces only speech-contour scatter (e.g. D3-F#2-A#2 at 1:04-1:09 [LN], G4 to A#4 chatter at 3:42-3:58, A5/G#5 pairs at 4:30-4:35), so no melody can be claimed (high).

## 2. Map of voice presence (measured, [S1] and [LVL])
| Time | Event | Evidence |
|---|---|---|
| 0:00-0:41 | No voice. Vocal stem -80 to -86 dBFS (bleed) | LVL, IMG 0000/0020 |
| 0:42.6-0:46.1, 0:51.2-0:54.0, 0:59.1-1:01.2 | Narration phrases 1-3 (peak -18, -16, -14 dB) | S1, LVL |
| 1:04.5-1:10.5 | Longest single phrase (6 s, the loudest, -12 dB) | S1 |
| 1:20.0-1:22.7, 1:24.5-1:28.7 | Phrases 5 and 6, the second over a stripped bed | S1, IMG 0080 |
| 1:28.7-1:49.2 | Voice absent for 20 s (full groove, first voiceless band section) | LVL, win_0080 |
| 1:49.2-1:52.2, 1:53.4-1:56.4 | Phrases 7 and 8 (temperature, "monster" ride) | S1, LYR |
| 1:56.4-2:25.4 | Absent ~29 s | LVL |
| 2:25.4-2:28.5, 2:29.0-2:31.9, 2:32.5-2:36.2 | Three ~3 s phrases, the participant list | S1, IMG 0140 |
| 2:36-3:24 | Absent 48 s, the longest silence of the voice | LVL, win_0160/0180 |
| 3:24.8-3:29.6, 3:32.4-3:34, 3:36.4-3:39.6 | First "fragment" bursts, 1-1.7 s each, peak -16 to -20 dB | S1, IMG 0200 |
| 3:40.5-4:22 | Dense run of bursts (0.8-3.5 s, one 7.6 s block 3:54-4:01.8), peaks -18 to -26 | S1, IMG 0220/0240 |
| 4:23-4:31, then sparse to 4:35 | Last long blocks (8 s block 4:23-4:31), then thin (peaks -39 to -46) | S1, win_0260 |
| 4:38.4-4:59.5 | Regular ~2.0 s pulse of bursts (4:40.6, 4:42.5 ... 4:58.7), 0.6-1.7 s long | S1, IMG 0280 |
| 5:00-5:05 | Voice stops; the track ends on the band/bed | LVL |

Roughly 43 s of speech in the first half (0:42-2:36) against about 100 s of burst material in the second half (3:24-5:00). The narration is the lead voice of the first half only.

## 3. The narration (0:42-2:36)
**Content.** The best words come from the medium Dutch passes [LYR]: "18 januari 1963" (0:41.7-0:45.8; the same date twice in the translate pass at 0:42.5 and 0:45.5, suggesting either a repeated title card read or ASR duplication, low-medium); "...marathon" (0:50.6-0:54; translated as "The Marathon without rain" / schaatsmarathon, medium on "skating marathon"); the 1:04-1:10 phrase gives "200 kilometer ... Friesland" and, in the translate pass, "6.30 in the morning" (the small pass reads "1.5-6 in the afternoon": the passes disagree, so the clock time is low); "de twaalfde elfsteen / waar iedereen zich voor opmaakt, dat is de Elfstedentocht" (1:19.7-1:28.5, medium on "Elfstedentocht-like" meaning, low on wording); "temperatuur 16 graden beneden (nul) ... een monsterrit van ruim 200 kilometer" (1:49.4-1:56.1, medium); "575 wedstrijdrijders, rond 9500 toerrijders, ... Zweden, Zwitsers en Belgen" (2:25.8-2:36.1, medium on figures, low on the country order). Both independent passes agree on 575 and 9500. The vocals-stem pass is Welsh-hallucinated, but it does independently catch "18 Januari 1963", "575" and "200 kilopetri o'r Ffriesland" as digits and proper nouns (low value, but not contradictory). Confidence on the gist (date, distance, cold, entrants, nationalities): medium; on any exact sentence: low. Fact checks are in v1/data/video2/context.md and research; I have not re-verified the figures.

**Narrative arc told by the sentences**: date (0:42) -> the event name (0:51) -> distance/place (1:04) -> "the Elfstedentocht" named as the thing everyone prepares for (1:20-1:28) -> weather and scale (1:49) -> the participant census (2:25). It is a classic newsreel build from context to numbers, which then stops. The narration never describes the race itself being run, or the winner: the second half has no recognisable words. Interpretation: the track lets the announcer set the stage, then lets the music "go out onto the ice" without him (medium; this is reading, not measurement).

**Treatment (medium-high).** Placed dry, centred and upfront: stereo width falls to 0.55-0.65 when the voice is on against 0.9-1.0 in instrumental gaps (win_0060, LVL), and the vocal panel cuts off abruptly at phrase ends with little smear (IMG 0060, 0080). Spectrum is band-limited with a hard edge near 4-5 kHz in the stem panels, consistent with an old optical or tape recording (inference; separation artefacts also limit the top end). It is the loudest single layer when present (stem about -12 to -20 dB, versus other/bass around -24 in the same bars). No pitch-shift, loop or chop is detectable in this half: the phrases are natural-length and separated by silences of sentence size. Per-phrase mel patterns are only 0.45-0.62 similar to each other [S2 baseline], as expected for different words.

**How the band answers the voice (high for the first two, medium for the rest).**
- Drum pickup: at 1:04.1 the kick re-enters 0.3 s before the 1:04.4 voice entry after a drum stop at 1:01-1:03 (win_0060); the band sets up the sentence.
- Space-making: for the 1:24.5-1:28.7 phrase the bass and drums fall to -76/-80 dB and only the "other" pad remains; the mix drops to about -20 to -22 dBFS (win_0080). When the voice ends at 1:28.7 the whole band re-enters on one downbeat (drum stem -75 to -21 dB, +6 dB in the mix). So the voice is the "gate" that holds the groove back, and its end is the release.
- Harmonic timing: win_0140 shows the first list-phrase starting at the Bm-Em change (2:24.7-2:25.3) and phrase ends within about 0.3-0.5 s of the Em-G (2:28.7), G-D (2:32.2) and D-Bm (2:36.8) boundaries (chord detector precision about 0.5 s, so medium). It suggests the narration was edited to fit the chord loop, or the loop was built around it. I could not tell which.
- Voice as groove-neutral: at 0:42.6 onwards the drums keep their pattern throughout (win_0040: "nothing leaves"). So the first narration is laid over a running band, while at 1:04 and 1:24 the band makes room. Two treatments of the same material.
- Loudness: 2:30-2:36 (voice on) is -10.7 to -12.7 dBFS; 2:37-2:43 (voice off) falls to -13 to -14.5 (win_0160). The voice adds 2-3 dB of perceived push and the biggest brightness bloom (centroid ~1.9-2.1 kHz on voice phrases, 1.4-2.1 elsewhere).

**Gaps are structural.** Gap lengths between phrase groups: 0:36 (intro bed, 0:00-0:42), 29 s (1:56-2:25), 48 s (2:36-3:24). The voice reappears after progressively longer silences, which behaves like an entrance cue: the 2:25 list arrives after a build-less plateau, and the 3:24 return comes after the longest absence and is changed in character.

## 4. The second half: from words to rhythm (3:24-5:00)
**Observation.** From 3:24 the vocal stem wakes with fragments: 3:24.8 blip (-47 dB), 3:28.6-3:29.6 (-18, centroid 3.3 kHz, a bright clipped sound), 3:32.4, 3:36.4, 3:38.6, then runs of bursts every 1-3 s to 4:22. [S1] bursts are 0.8-3.5 s here, but IMG 0220 shows them as blobs 0.5-1 s long repeating at ~0.3-0.6 Hz with 200-1000 Hz harmonic stripes, i.e. voiced material, not noise. They sit 8-25 dB under the other stems (levels -23 to -43), far below the first half's -12 to -20: **the voice has moved from foreground to texture** (high on level, medium on role).

**Whisper "words" are not reliable.** The small mix pass lists "Stuck", "End of the road", "Climbing up" (3:32-3:59); the medium Dutch pass lists "Stief", "Eerst", "Slop", "Stapen", "In de lopen", "Vrijdiger" for the same instants. The two passes disagree entirely and neither resembles the other, which is exactly what ASR does on music-covered non-speech; the vocals-stem pass adds "Fafn." at 4:05-4:17 (Welsh pass, nonsense). Verdict: treat all of 3:24-5:00 as unintelligible (high). The earlier worry in the context that "Stuck/End of the road" are real words is best dropped; the context already flags it as low-confidence ASR and I agree.

**Is it chopped or looped?** Two partial tests.
1. Regular timing at 4:40-4:59 [S1/win_0280]: bursts start at 4:40.6, 4:42.5, 4:44.5, 4:46.6, 4:48.6, 4:50.6, 4:52.6, 4:54.6, 4:56.6, 4:58.65, i.e. every 2.0 s (high, matches IMG 0280, ten near-identical blocks). The beat tracker's grid is 0.372 s (161 bpm), so 2.0 s is 5.4 grid beats and the starts drift -0.18 to +0.13 s against that grid ([S2]); against a 120 bpm reading (0.5 s beat, 4 beats = 2.0 s, which win_0040/0240 also proposed for the drums) it is exactly one bar. So the voice bursts are one-per-bar at 120 bpm (medium), supporting the half-time/120 bpm bar count over the 161 bpm tracker value.
2. Mel-shape similarity [S2]: for the ten 4:40-4:59 bursts the mean pairwise correlation is about 0.72 (range 0.40-0.94, 4:52.6 versus 4:54.6 = 0.94, 4:50.6 versus 4:56.6 = 0.88), against 0.45-0.62 between the five different spoken phrases of the first half. Higher similarity is consistent with the same or a similar sample being retriggered, but a 0.8-s mel correlation is a crude test and loud-envelope shape alone would raise it (medium-low). Not proof of a literal loop; "looped/re-triggered voice fragment" is the safer wording.

**Shape of the second half.** 3:24-3:40 fragments appear (call-and-response with drums, per win_0200/0220); 3:40-4:22 a dense, repetitive run with a long 7.6 s block 3:54-4:01.8 (the vowel-like sustained stretch where lead tracker chatters at G4); 4:23-4:31 the last long block; 4:31-4:38 thinning to -39 to -46 dB with a conspicuous gap that coincides with the "bass leaves" moment of win_0260; 4:38.5 a single loud wideband burst (-26 dB, centroid 2.7 kHz, a bright exclamation-like transient at the bass gap, medium); then the 2-s pulse until the end. At 4:48.5 the bass is removed and replaced by sparse stabs (win_0280); the voice pulse and the drums then become the rhythm. The voice thus ends the piece as a metronome, and the last bar-level event is 4:58.7.

**Treatment of burst material (low-medium).** Short smeared tails at 1-4 kHz (small reverb or separation bleed; win_0280), bursts begin abruptly and end abruptly (gated), spectral centroid about 1.1-1.9 kHz (lower than the narration's ~2 kHz, suggesting lower-pitched or filtered material). I cannot say whether the source is the same narrator, a crowd, a commentary, or a synthesised choir. CLAP gives "choir" 0.98 near 0:45 and "no vocals" elsewhere; both are weak and in the first case probably triggered by sustained organ-like bed (win_0040).

## 5. Words and music answering each other
- **Voice speaks, band holds a loop**: the Bm-Em-G-D (A) cycle under the speech (0:42-1:28, 2:25-2:36) is the same one that carries the rest of the track (chord time shares: Bm 136 s, D 44 s, Em 22 s, G 20 s of 306 s, summary.json). The words ride on top of a pre-existing groove; harmony does not follow the voice.
- **Content mirrors form**: sentences about size, cold and numbers are given over a sparse then increasingly driven groove (drum stop at 1:01-1:03, drums out 1:23-1:28, full re-entry 1:28.5). The voice is used as the "gate" in time: phrase on -> band thin; phrase off -> band full. This is a feeling-level reading (medium): the narrator is the cold, remote statement, and the band is the physical effort that returns when he stops.
- **Silences as music**: the 20 s, 29 s and 48 s voice-free stretches are where the track feels most like a pure PSB band piece; the voice returns as an event.
- **Arc of meaning**: words in the first half, rhythm in the second. Semantically the track goes from "being told about the race" to "being in it", which is where intelligibility is lost (interpretation, medium-low).

## 6. Honest limits
- Demucs "vocals" on a spoken, band-limited sample is partly leakage of snare/hat and the "other" stem; the burst intensities at -40 to -50 dB near 4:31-4:35 are partly bleed.
- Whisper cannot hear the narration in the second half; I have not shown the second-half material is speech at all, only that it is voiced (harmonic ladders, 200-1000 Hz stripes) and gated. A processed instrument (vocoded synth, choir patch) cannot be excluded.
- Narrator identity, source film and exact Dutch wording remain unconfirmed (see context.md).
- Pitch tracker output on this stem is speech contour, not tune.

## 7. Where the window notes need care
- win_0040 and win_0060 say the narration is "not chopped, looped or pitch-shifted": I agree for the first half; do not extend that to 3:24 onward.
- win_0200 treats 3:24-3:29 as "fragments"; [S1] confirms they are 1-1.7 s each and louder than most later bursts (-16 to -18 dB), so the later material is quieter, not louder, than the entry.
- win_0220 reads Whisper "Stuck/End of the road" at 3:32-3:59 as words; I recommend the final write-up drop them.
- The 2.0 s burst period in win_0280 is correct; a "regular 161 bpm" framing would misplace it; 120 bpm one-per-bar fits better.

## 8. Three questions for fellow specialists
1. **Rhythm**: does a 120 bpm (0.5 s beat, 2.0 s bar) grid on the drum stem fit better than the 161 bpm tracker value for 3:24-5:00, and do the voice bursts at 4:40.6, 4:42.5 ... 4:58.7 land on beat 1 of each bar or on a fixed off-beat? Does the voice ever stay out of phase with the kick (the burst offsets scatter -0.18 to +0.13 s against the 161 bpm grid)?
2. **Sound**: can you tell from the "other" stem and the spectral top-end whether the 3:24+ bursts share the narrator's band-limited character (hard edge 4-5 kHz, dry) or are a different sound source (choir patch, vocoded synth, crowd)? Is the loud 4:38.5 wideband burst a voice or a drum/noise hit leaking into the vocal stem?
3. **Form**: is the 2:36-3:24 voice-free stretch (48 s) a conventional "verse-to-chorus" gap in the piece, and does it mark the section boundary where "words" become "rhythm" (3:24)? Where do you place the section boundary, and does it match the 1:28.7 and 2:25 voice-gated re-entries?
