# t_cshells_cshore: VOICE specialist, round 1 (blind, measurement-only)

Role: voice, words and samples. Inputs read: all 19 `win_*.md` notes; `lyrics/*` (mix and vocals-stem Whisper medium, plus the doubtful list); `music_views/per_second_levels.json`, `lead_notes.json`, `clap_tags.json`; `window_0140s.png`, `window_0320s.png` (opened and read); `stems_raw/htdemucs/song/vocals.wav`, `other.wav`, `audio/song.wav`. My scripts: `v1/scripts/agents/voice_r1_cshells.py` (per-segment stem statistics), `voice_r1_f0.py` (pyin f0, modulation rate), `voice_r1_end.py` (10 ms envelopes, end of track). British English; times m:ss.

## 0. Headline
**This is an instrumental track with almost no voice. The voice that exists is a handful of short, quiet, heavily buried fragments, used as texture, with one clear exception: a roughly 5 s spoken-or-vocal-like fragment at 2:21.5-2:26 (vocal stem peak -12.7 dBFS) and a slow-fading speech-like murmur at about 5:30-5:43.** There are no sung lyrics and no legible sentence. Every transcript line is either a hallucination on silence or on noise (shown in section 1). Confidence high that there are no lyrics; medium that the fragments in section 2 are human-voice-like rather than instrument leakage.

## 1. What the transcripts really say (checked, not trusted)
| Transcript line | Where | Evidence it is not speech | Verdict |
|---|---|---|---|
| mix pass "You" 0:28.58-0:29.98 | 0:28.6 | no_speech_prob 0.74; word p 0.025; vocal stem -85 to -86 dB (separator floor) at 0:28; mix is a held A2 drone with no transient (win_0020 note, FFT 109.5 Hz) | hallucination, high |
| mix pass "This is the only way to get to the top of the mountain. / We're going to have to go all the way up to the top." 4:28.94-4:29.64 | 4:29 | no_speech_prob 0.93; word probs 0.002-0.67 (median about 0.2); the second sentence is crammed into a 0.02 s segment; vocal stem in 4:10-4:18 is -76 dB and at 4:28-4:30 -75 dB (my measure, 268.5-270 s: rms -75.2, spectral flatness 0.07, noise-like) | not speech; the sentence reads as a Whisper stock phrase, high |
| mix pass "Thank you." 5:59.64-5:59.94 | 5:59.6 | the mix is exact digital zero from 5:42.84 (section 6), so there is nothing to hear | hallucination on silence, certain |
| vocals-stem pass, Welsh-labelled strings (1:16-1:21, 2:21.7-2:24.3, 3:37-3:45, 5:15.8-5:44) | various | language ID "cy" p=0.49 for the whole file; no_speech_prob 0.35-0.94; avg_logprob -0.85 to -1.92; a single 20 s "segment" 5:15.8-5:36.0 where the stem is at -74 to -78 dB for most of the span; repeated clauses ("Mae'r ffyrdd yn dda" twice, "Mae unrhyw ddyn ... ystod hynny" twice) are decoder loops | not words, high |
So **no sentence or phrase is legible, and none repeats as a real repeated lyric** (rule 2: nothing clearly audible is being withheld; the repeats that exist are decoder loops, not heard repeats). I have no near-certain identification to state beyond "no lyrics".

## 2. The vocal-stem events that are real (measured)
Seconds where the vocal stem rises above -65 dB (per_second_levels.json; floor is -71 to -90). Full list: 1:04, 2:21-2:26, 2:31-2:32, 3:26, 3:44-3:45, 3:48-3:49, 4:27, 4:56-4:57, 5:12, 5:16, 5:30-5:41. Table of what each is:

| Time | Stem level (peak / rms) | Mix level at the time | Measured character | My reading | Confidence |
|---|---|---|---|---|---|
| 2:21.5-2:26.5 | peak -12.7 dBFS, rms -30.8 to -32.6 dB; 2:22 second -25.2, then -36.0, -46.3, -57.0 (slow decay over about 4 s) | -15 to -17 dBFS | window_0140s.png vocals panel: bursts of energy 200-1500 Hz in the window from about 1.5 to 5 s (2:21.5-2:25), each with clustered bands; clicks above; pyin voiced fraction 0.52, f0 median 216 Hz (10th-90th percentile 166-337 Hz); lead_notes there: G#5, E4 x3, G#3, G#5, E3 (0:2:21.5-2:26.7), alternating, so octave-jumpy, not a melody; stem centroid 363 Hz (rms-weighted) | the clearest voice-like event in the file: a short vocal or voice-sample fragment with a long decaying tail (reverb or release), then pieces of it trail off to 2:30. Pitch jumps by octaves are tracker confusion, not a sung line. Level: about 15 dB below the mix RMS in the stem peak second, so it is audible but not prominent. | medium that it is voice-like; INFERRED |
| 3:44-3:45.5, 3:47.8-3:49.2 | -43 to -50 dB per second (stem rms -46.6 / -46.3) | -13.9 | formant-like bands 1-2.5 kHz, centroid 1.4 kHz, lead_notes F5 x6 (224.5-229.4 s) at about 700 Hz; pyin mostly unvoiced (0.04, 0.26) so the F5 notes are not a clean voiced pitch | brief buried interjections 30 dB under the mix; a high whistle-like or voice-like tone. Could be a lead synth leaking into the vocal stem. | low-medium |
| 4:56-4:58 | -63.7, -50.1 | -15 to -16 | 200-700 Hz blob; pyin voiced 0.78, f0 median 165 Hz (136-186); lead_notes E3, C#3, D#3, F3, F#3, F3, A2 (semitone steps, falling and rising) | low, pitched, wobbling; the most voice-like pitch behaviour after 2:22 (stable voiced frames) but 35 dB under the mix; "male voice or bowed low instrument" cannot be told apart | low |
| 5:12.3-5:12.8 and 5:16.7-5:17.2 | 5:12 second -31.0 (peak -17.8), 5:16 -41.5 | -15 | two 0.5 s flashes below about 1.5 kHz; centroid 1.39 and 1.33 kHz; lead F#5, E5 | punctuation inside the drum roll, then just before the drums stop. Could be a clipped syllable, a vocal hit, or a drum or synth leak. | low-medium |
| 5:30.5-5:42.8 | per-second -49.8 to -62 dB; rms -55.0; peak -32.6 | mix falls -17.9 to -57.8 dBFS (a fade) | window_0320s.png vocals panel: from about 10.5 s into the window (5:30.5) a dense bright field appears with vertical bursts 0.1-0.4 s wide and horizontal bands (formant-like); onset rate about 16-19 per 6 s; syllable-like modulation at about 1.6-2.0 Hz; pyin f0 median 233-251 Hz but voiced fraction only 0.11-0.35; 85% rolloff 2.5 kHz (win_0320 note); CLAP 5:30-5:45 "male speech" 0.75-0.77, "male singing" 0.99 at 5:35 (weak) | a speech-like or crowd-like murmur as the music fades; the one place where syllable structure shows. Its mid-1 to 2.5 kHz band and the bursts fit speech, or a vocal sample with a band-limited telephone or radio treatment (INFERRED). | medium that it is speech-like; low on its content |
The window_0320 image gives one concrete observation: the vocal-stem field becomes dense at about 5:30.5 **exactly where the mix panel loses its bass and drops in level** (the lower 512 Hz bands thin), so the separator may be hearing the residue of a decaying band as "vocals". Separator bleed cannot be excluded: the vocal-stem rms is about 24-30 dB under the mix there.

Envelope-correlation check (stem against "other", 50 ms frames): 2:21.5-2:26.5 r=0.35; 3:44 r=0.23; 3:47.8 r=-0.10; 4:56-4:58 r=0.34; 5:12 r=0.49; 5:15.5-5:17 r=0.24; 5:30-5:43 r=-0.08. A low or negative correlation (3:47.8, 5:30-5:43) argues the stem content is independent of the band texture, so it is more likely a genuinely separate layer; the 5:12 value (0.49) fits a leak from the drum-roll texture.

## 3. How voice is used (placement, chop, treatment)
- **Placement:** buried. Stem peak is -12.7 dBFS in the best case and -35 to -50 dB for the rest, i.e. 15 to 35 dB under the mix (compare mix -13 to -17 dBFS). It is never a lead. (measured; high)
- **Chopping and repetition:** the fragments are short (0.1-0.5 s bursts, onset rate about 2.5-3 per second inside the 5:30 region) and sparse (a few events in 6 minutes). I find no repeated sample: the 2:22, 3:44 and 5:12 fragments differ in level, centroid (363, 1463 and 1387 Hz) and pitch behaviour, so no near-identical repeat (loop regularity rule 1: none for voice). Medium confidence.
- **Treatment cues:** the 2:22 fragment's slow multi-second tail (-25 to -57 dB over 4 s) could mean reverb or a release left ringing; the 5:30 material is band-limited (rolloff 2.5 kHz) against the full-band mix, which is the "narrow-band layer under or inside a full-range mix" cue for an older or lo-fi source (rule 1). Figures: 85% rolloff 2.5 kHz for the voice layer against 95% rolloff of about 13 kHz for the opening noise layer; but the voice stem is 30 dB quieter so its top end may simply sit under the noise floor. INFERRED, low.
- **Words and music answer each other?** There are no words to answer. The nearest relationship is structural: the voice is most present at moments when the band material thins or stops: 2:22 (after the full-band burst, the song is in its heavy stretch, mix -15 dBFS, so here the voice sits over, not in a gap), 5:12 and 5:16 (end of the drum roll) and 5:30-5:43 (the fade). That makes the late voice an epilogue, a human trace left as the band leaves. (interpretation, low-medium)

## 4. Production-era cues for the voice layer (INFERRED)
- Peak: the whole song peaks at 0.0 dBFS (song.wav), consistent with modern limiting; the voice stem peaks at -12.7 dBFS, so the voice is not what sets the ceiling.
- Band limitation: 5:30-5:43 voice layer rolloff 2.5 kHz against a full-band mix: medium-low evidence of a lo-fi or broadcast-style source. The mix at 5:30-5:42 falls from -17.9 to -57.8 dBFS in about 12 s, then **exact digital zero**, which is a DAW edit (section 6).
- Loop/grid: no voice loop evidenced (section 3). Kick-onset spread is a rhythm matter; nothing in the voice stem sits on a grid I could test (stem rms near the floor), so no sync figure is claimed.
- Overall: modern production, with an unidentifiable voice-like source layered or sampled in. Source date cannot be set. Medium on modern mastering, low on the voice source.

## 5. Whisper's behaviour as evidence
Language ID flips to Welsh (p=0.49) on the vocals stem and English (p=0.39) on the mix, both low. Whisper medium tends to hallucinate stock phrases on non-speech audio; "Thank you.", "You", and long invented sentences are textbook examples. I therefore read the transcripts as a negative result: **nothing speech-like loud or clear enough to decode**. I did not run any new Whisper pass (cost and likely the same).

## 6. End of track (rule 4), from my own 10 ms envelopes
- Mix: last non-zero sample at 5:42.835 (342.835 s); the file runs to 6:00.977 (360.977 s), so the final **18.1 s is exact digital zero** (per-second dB -240). 10 ms envelope maxima per second of the mix: 5:38 -43.1 dB, 5:40 -47.5, 5:41 -52.4, 5:42 -57.6 (mean -92.4 over the second because the sound stops mid-second), then -240. So the last audible sound is at about 5:42.8, at about -58 dBFS (10 ms RMS), about 17 to 18 dB under the 5:20 level of -15 dBFS.
- Stems: vocals last > 1e-4 at 5:42.81 (envelope -59.5 dB max in 5:42, then floor -90.3); other 5:42.81 (-62.2 max); drums last at 5:38.05 and bass at 5:38.5 (both at floor, -85 to -88 dB, i.e. the rhythm section has already left by about 5:38). So the fade tail is carried by vocals and other together, in the last 5 s.
- Last 3 s of the audio (5:58-6:01): no signal at all in any stem. Final hit count from the waveform in the last 3 s: **zero peaks**. The fade has no hits to count: it is a decay, not a struck ending. "Thank you." at 5:59.6 sits in this silent stretch and is therefore a hallucination, certainly.
- So the voice is among the last audible things in the track (vocal stem alive at -59.5 dB at 5:42), alongside "other". It does not end the track alone: both stems cut together in the same 10 ms, which with a smooth multi-second decay before it suggests an edit or fade-out applied to the master (INFERRED, medium).

## 7. Boundary evidence table (voice-relevant boundaries; stems re-measured)
Per-second dB, from per_second_levels.json unless stated.

| Boundary | Drums | Bass | Vocals | Other | Mix drop or rise | Stem carrying it |
|---|---|---|---|---|---|---|
| 2:21.5 voice fragment enters | active (about -25 dB) | active | -60.0 (2:21) to -25.2 (2:22), +35 dB | -17 to -15 (flat) | -17.4 to -15.3 (+2 dB) | vocals only (mix barely moves: the voice is added over a loud band) |
| 3:44 and 3:48 interjections | active | active | floor -72 to -44.6 (+27 dB) | none | -13.9 flat | vocals only |
| 5:12.3 flash | drum roll in progress | low | -75 to -31.0 (+44 dB) | -15 flat | -15 flat | vocals only (could be separator leak) |
| 5:30.5 voice-like layer becomes dense | falls | -85 at floor after 5:30 | -60 to -50 (+10 dB) | -17.9 to -40.5 (5:30-5:36, falls 22 dB) | -17.9 to -40.5 | other falls; vocals rises relative to it. The vocal change is mainly one of share. |
| 5:42.84 end of sound | floor since 5:38 | floor since 5:38.5 | -59.5 to floor -90 | -62 to -88.9 | -57.6 to -240 dBFS (full-mix silence, not a rhythm-section dropout) | vocals and other together |

## 8. Feeling and what the voice does for the listener
- 2:22: a human sound intrudes into a dense, loud stretch for about 4 s and decays; it reads as a brief human presence, "someone speaking from afar" (metaphor; measurement says only a 200-1500 Hz band burst with a 4 s decay and clicks). Effect: a small shock of the human against machine-like drums (stem drums -23 to -31 dB; kick-like bass pulses at about 0.5 s visible in window_0140s).
- 3:44-3:49: faint, high, formant-like interjections; they pull the ear towards a point, not a statement (interpretation, low).
- 5:30-5:43: voices in the fade read as the human world coming back as the noise and drums go: the strongest emotive use of voice in the track, and it ends in a cut to silence rather than a resolution (the 18 s of zero). The silence at the start (0:00-0:11.3, exact zero) and the silence at the end frame the track with two digital zeros: the opening is a jolt (+about 190 dB step), the ending an abrupt drop after a decay.
- Overall emotion carried by texture and level, not by words (CLAP "no vocals" about 1.0 across most windows; weak, but agreeing with the stems).

## 9. Where I disagree with, or tighten, colleagues' window notes
- win_0020 and win_0100 correctly dismiss "You" and the 4:28 lines. I add the no_speech_prob 0.93 and the 0.02 s segment as hard reasons.
- win_0140 calls the 2:21.5-2:26.5 fragment "processed spoken/sampled, not sung". I agree with "not sung" (the lead tracker gives octave-jumping notes G#5/E4/G#3, voiced fraction 0.52 only) but lower "processed" to INFERRED low: a long tail can equally be an instrument's release leaking into the stem.
- win_0320 says "speech-like voice (not singing)" from about 5:30.5 to 5:42.8. I keep medium, but note the CLAP "male singing 0.99" at 5:35 contradicts "not singing" and cannot be resolved; my pyin f0 voiced fraction (0.11-0.35) is low for sustained song, which supports speech or noise rather than singing.
- win_0300 says the 5:12 and 5:16 flashes are medium vocal-like. I lower to low-medium: stem envelope correlation with "other" is 0.49 at 5:12, a leak-like value.
- win_0220 says 3:44 bursts are "vocal-like melodic interjections" under F5: lowered to low-medium (voiced fraction 0.04).

## 10. Not recoverable by measurement
- Whether any voice fragment is speech, singing, chanting or a synth patch: the separator output is bleed-prone and the vocal stem is 15-35 dB under the mix.
- The language, words and speaker of any fragment: Whisper's output is hallucination; the audio is too quiet and too short.
- Whether the 5:30-5:43 layer is a sampled broadcast, an archive recording, a crowd or a performed vocal: no source marker is measurable (band-limitation alone is weak).
- Whether the voice is a deliberate theme: no repeat was found; intent is not measurable.
- The real source of any sample and its date: measurements show only level, band, and syllable-rate behaviour.
- Whether the two exact-zero silences are the artist's intent or an artefact of this file: only this file was measured.

## 11. Three questions for fellow specialists
1. **Sound specialist:** the vocal stem at 2:22 peaks at -12.7 dBFS with a 4 s decay and the 5:30-5:43 layer is band-limited (85% rolloff 2.5 kHz). Does your measurement of the full mix at those times show a dedicated reverb or telephone-style band-pass, or is it the same compression and room as the band layer?
2. **Form specialist:** the voice appears at 2:21.5, 3:44, 4:56, 5:12, 5:30. Do these sit on your section boundaries or on bar lines (name your grid and BPM; the tracker is 123.05 BPM, 0.488 s), and is the 5:30-5:43 murmur your "coda" or a separate fade-out section?
3. **Feeling specialist:** given that no word is legible and the voice is always buried, how much of the "human" feeling in the final 12 s comes from the speech-like murmur, and how much from the 22 dB fade and the cut to digital zero at 5:42.84? Please separate the two if your measurements allow.
