# t_cshells_cshore: VOICE specialist, round 2 (blind, measurement-only)

Read: all seven round_1 files and the two round_2 files already present (harmony, rhythm). New scripts: `v1/scripts/agents/voice_r2_cshells.py` (band statistics of vocals, other and mix per event; long-term-spectrum correlations; 4:27-4:31 levels; Whisper segment fields) and `v1/scripts/agents/voice_r2b.py` (harmonic peaks and a 10 ms pulse count for the 2:22 event). Tags: measured / INFERRED with confidence. British English, times m:ss.

## 1. Answers to questions put to me

**Sound Q2, Feeling Q3, Lineage (4:28.9 "spoken sample"): is the Whisper text at 4:28.9 supported by the vocals-stem energy?** No. Measured, high.
- Vocal stem at 4:27.0 is -48 dB; from 4:27.5 to 4:30.5 it is -71 to -78 dB in every 0.5 s block (the separator floor), while the mix sits at -15 to -17 dBFS. The single bump at about 4:27 is 1.9 s before the claimed text.
- The two "sentences" occupy 4:28.94-4:29.62 (0.68 s) and 4:29.62-4:29.64 (0.02 s), sharing no_speech_prob 0.928 and avg_logprob -0.99. The first is 12 words in 0.68 s (about 18 words per second; ordinary speech is about 2-4), the second 13 words in 0.02 s. Neither is physically speakable. The text is a decoder artefact on non-speech.
- So I contest Lineage's round-1 line "near-certain speech sample, INFERRED high" (lineage.md section 6, point 4). Rule 2 (blind honesty) asks for well-evidenced identifications; here the measured evidence points the other way: text is legible only in the transcript, not in the audio, and it is not repeated anywhere. I rate "speech sample at 4:29": not supported; INFERRED, high that it is a hallucination. Sound, Form and Feeling were right to rate it low or sceptical; Lineage should lower it. This also lowers the premise of any "archive or broadcast speech sample" reading built on it.

**Lineage Q3 / Sound Q2: are the voice-like fragments band-limited (broadcast-like) or full-band?** I correct myself here. In round 1 I called the 5:30-5:43 layer "band-limited, rolloff 2.5 kHz, a cue for older or lo-fi source". New measurement, same-method comparison on the full mix:
| Span | Layer | Centroid | 85% rolloff | 95% rolloff | Share above 5 kHz |
|---|---|---|---|---|---|
| 5:30.5-5:42.8 | vocals stem | 2.59 kHz | 2.47 kHz | 3.44 kHz | 0.017 |
| 5:30.5-5:42.8 | mix (equal to "other": both -27.3 dBFS) | 1.76 kHz | 0.45 kHz | 1.53 kHz | 0.001 |
| 5:20-5:28 (loud music) | mix | 2.19 kHz | 2.30 kHz | 3.30 kHz | 0.006 |
| 2:30-2:40 (loud music) | mix | 2.53 kHz | 0.89 kHz | 3.07 kHz | 0.017 |
The whole mix has its 95% rolloff at about 3.1-3.5 kHz and under 3 % of energy above 5 kHz throughout the loud body, so the voice layer is no narrower than the band it sits in. My round-1 "narrow-band layer under a full-range mix" cue is withdrawn: it compared the voice with the opening noise layer, not with the music. The band-limited-sample cue for era is therefore not evidenced for any fragment. What the figures do show: at 5:30.5-5:42.8 the voice layer extends higher (95% rolloff 3.4 kHz) than the fading music (1.5 kHz), so in the fade it occupies a region the music has vacated. That is a real measured fact (it is why the murmur can be heard at all); Sound's centroid of 3.5 kHz for the same span is the 95% rolloff, not the centroid, as far as I can reconcile it (my centroid 2.6 kHz). Era judgement for the voice: unchanged on the track (modern mastering: sample peak 0.0 dBFS, high), no era evidence for the voice itself (low).

**Form Q3: are these spoken, sung or processed, and is the end murmur the same material as 2:22?** Different material, with one cross-check I must also disown.
- 2:21.5-2:26 is **pitched with harmonic structure**: spectral peaks at 215, 433, 657 and 875 Hz in the first second (1:2:3:4 series, f0 about 219 Hz, which is A3 within 10 cents of 220 Hz), plus 328 Hz (E4, 329.6 Hz) and its third harmonic near 982 Hz. A and E are the track's tonic and fifth (Harmony round 2: A with an E fifth). Stem 85% and 95% rolloff are 334 and 355 Hz: nearly all the energy sits below 400 Hz in the stem. Measured, high that it is harmonic; medium on the pitches.
- It is **four near-equal pulses**, from a 10 ms envelope (1-3 ms smoothing at 441 samples) of the stem: peaks at 2:22.12, 2:22.53, 2:22.96, 2:23.36 (levels -26, -22, -16, -45 dB), spacing 0.41, 0.42, 0.40 s, then 0.54 s to 2:23.90. A spacing that regular (±0.01 s) is more like a played or gated sound than human speech. 0.41 s is not the beat: Rhythm measures the drum beat lag as 0.494 s at that time (2:00-3:20), so the ratio is 0.83 (about 5:6). Measured, medium (the stem is separation output).
- I therefore **lower my round-1 reading** of 2:22 from "voice-like, medium" to "pitched, rhythmically regular event, voice or synth/guitar harmonic leaking into the vocal stem: undecidable", INFERRED, low-medium that it is a human voice. This agrees with Harmony's view that the lead trackers read pad or bass pitch, and with the 0.35 envelope correlation to "other" in my round 1.
- 5:30.5-5:42.8: no harmonic series at the 5 s level (peaks 1776, 2005, 2468, 1965, 1860 Hz: close, unharmonic, noise-like), centroid 2.6 kHz, 85% of energy up to 2.5 kHz, modulation peak 2.5 Hz (the 1-12 Hz envelope spectrum), 83 % of energy in 300-3400 Hz. Speech-like in its 2-3 Hz syllable-rate envelope, but noise-like in spectrum. So it is not the same material as 2:22: pitched below 400 Hz against unpitched mid-band. Medium.
- Long-term spectrum correlation of the vocal stem (24 log bands 100 Hz-8 kHz): 2:22 against 5:30 is 0.73, but 2:22 against 4:27 is 0.73 and 4:27 against 4:56 is 0.76, and these are floor segments, so a correlation of 0.7 is simply the shared low-frequency tilt of the stem and does not mean "same source". The only low correlations are 3:44 against everything (0.05-0.19) except 5:12 (0.73): so 3:44 and 5:12 are the two events that resemble each other (both 1.2-1.6 kHz peaks, 1.5 kHz rolloff, 300-3400 Hz share 0.99-1.0, spectral peaks 1211-1585 Hz and 1343-1534 Hz). Those two look like one narrow-band high-mid sound (a squeal or lead tone) recurring, 224 s and 312 s, 88 s apart. Medium-low. I do not call them "section markers" (Form's suggestion): two points do not make a recurrence.
- Spoken, sung or processed at any time: not decidable; no event shows syllable structure plus voiced pitch together.

**Feeling Q (how much of the closing "human" feeling is the murmur, how much the fade and the cut):** measurable parts only. The murmur: vocal stem -54.8 dB rms, 27 dB under the fading mix (-27.3 dBFS over the span), but it sits at 1.5-3.4 kHz where the fading music has almost nothing (music 95% rolloff 1.5 kHz). The fade: mix falls from -17.9 to -57.8 dBFS in 12.3 s (40 dB, 3.2 dB per second), then exact digital zero at 5:42.84. The murmur is at best a faint texture on top of a 40 dB decay; the decay and the cut carry the closure. I cannot isolate "feeling"; but if a listener hears human presence at 5:30-5:43, it comes from a layer 27 dB under the music and mostly in a band the music has left. Low on the percentage, high on the levels.

**Sound Q1 / Form Q1 (my own earlier question to them) and Rhythm round 2, point D.** Rhythm says the drum stem gives no kick grid. For the voice: the 2:22 pulses (0.41 s) are on no grid I can name, and I make no sync claim (rule 5). The pulses are also not on the bass-quarter grid (0.50 s early, 0.484 s by 3:00), so they are an independent pulse, not part of the beat.

## 2. Corrections and ties to other specialists
- **To Lineage:** the "sample-collage prologue" in the opening is outside my voice measurements; I make no claim on it. I withdraw the "archive voice" thread: no fragment shows band-limitation relative to the mix.
- **To Harmony:** the 4:56-4:58 voiced low pitch (f0 165 Hz, E3 region) matches your E fifth, and 2:22 (219 Hz A3 plus 328 Hz E4) is the same A-E pair. Both are consistent with a tonic and fifth leaking into the vocal stem rather than a sung melody: I now lean towards "leak or doubled instrument line" for 2:22 and 4:56 (INFERRED, low-medium), keeping a possible human voice as open.
- **To Rhythm:** the track's tempo glides (0.506 to 0.479 s per beat), so no static grid fits; the voice events carry no audible lock to it. The 2:22 pulse (0.41 s) deserves a drum-stem look.
- **To Form:** voice events at 2:21.5, 3:44, 4:56, 5:12, 5:30 are not shown to fall on section boundaries (I have not re-measured Form's grid); the strongest link is that the **only voice-like layer which becomes the main band-free content is the 5:30.5 onwards fade**, where drums and bass have gone (drums last at 5:18.9 in Rhythm's 10 ms measure; my 5:38.05 was the separator floor, so I accept Rhythm's figure). Boundary table below is restated with that correction.
- **End of track:** unchanged from round 1: last non-zero sample 5:42.835; vocals and other end together; final 18 s exact zero; zero hits in the last 3 s (checked on the waveform envelope in round 1, not per-second RMS).

### Boundary evidence table (voice-relevant; stems per-second dB from per_second_levels.json)
| Boundary | Drums | Bass | Vocals | Other | Mix change | Stem carrying it |
|---|---|---|---|---|---|---|
| 2:21.5 pitched event | active, no change | active | -60 to -25 (+35 dB) | -17 to -15 | +2 dB | vocals stem only (could be leak) |
| 3:44 / 3:48 interjections | active | active | floor to -45 (+27 dB) | none | flat (-13.9) | vocals stem only |
| 5:12.3 flash | drum roll | low | -75 to -31 (+44 dB) | flat -15 | flat | vocals stem only; envelope correlation with other 0.49 (leak-like) |
| 5:30.5 murmur band | drums out (last 5:18.9, Rhythm) | at floor from about 5:30 | -60 to -50 (+10 dB) | -17.9 to -40.5 over 5:30-5:36 | -22 dB fall | other falls; the vocal change is one of share |
| 5:42.84 end | out | out | -59.5 to floor | -62 to -89 | -57.6 to -240 dBFS (full-mix silence, not a rhythm-section dropout) | vocals and other together |

## 3. How the voice serves the music (what I can still claim)
- Voice is texture and trace, never lead: stem peak -12.7 dBFS (1.6 s at most), most events 30-60 dB under the mix. Measured, high.
- No sung or spoken lyric exists; the transcripts are hallucination (no_speech_prob 0.74, 0.93, silence, and the Welsh labels). High.
- The 2:22 event, if it is a voice, would be a pitched A3 with an E4 above, answering the tonic-fifth drone of the band: a doubling, not an answer. Words never answer the music because there are none.
- The final minute's human trace is thin: murmur 27 dB under the fade; the track's closure is the 40 dB decay and the cut.

## 4. Not recoverable by measurement
- Whether any fragment is a human voice at all, or a pitched instrument, synth or tracker artefact in the vocals stem (2:22 is harmonic and rhythmically regular, which favours an instrument).
- The words, language or speaker of any fragment: the only text is hallucination.
- Whether 3:44 and 5:12 are the same sound by design: two similar events 88 s apart do not show intent.
- The source, date or provenance of any sample: no band-limit or noise cue separates a fragment from the band.
- Whether the 5:42.84 cut is the artist's choice or an edit of this file.

## 5. Two new questions
1. **Rhythm specialist:** the 2:22 event is four pulses at 0.41 s (±0.01) against a drum beat of 0.494 s (ratio 0.83, about 5:6). Does the drum or bass stem at 2:22-2:23.5 show a matching 0.41 s pulse (a polyrhythm or a gated delay), or does the 0.41 s sound live only in the vocal stem?
2. **Harmony specialist:** the 2:22 event has f0 219 Hz (A3) with E4 (328 Hz) and the 5:12 / 3:44 events peak at 1.2-1.6 kHz (about D6-G6). In the "other" stem at those moments, is there a matching A3/E4 pitch at 2:22 (a leak) and a sounding tone near 1.2-1.6 kHz at 3:44 and 5:12 (a lead line), or is the vocal stem the only place they appear?
