# Form specialist, round 2 (blind, measurement-only): t_cshells_cshore

New script: `v1/scripts/agents/form_r2_novelty.py` (4 fps mel-spectrum novelty, 2.4 s before against 2.4 s after, on the mix and the Demucs stems) plus an inline check of drum and bass stem RMS and onset rate at 2:40-3:45. Round-1 measurements (10 ms envelopes, end of track, silence checks, 4-s block IOIs) are unchanged and not repeated. I read all six round-1 files and the round-2 files already written by harmony, rhythm, sound and voice. Tags: measured / INFERRED / speculative with high/medium/low. Timestamps m:ss.

## 1. Answers to questions put to me

**Harmony Q3: does the A/G vamp (4:00-4:40) mark a section distinct from the A-pedal section before it, and do the rising-chroma gestures line up with my boundaries?**
- Accepted: harmony's round-2 finding that the bass root, not the chord label, changes (G on the bass about 4.7 times as often as A at 4:12-4:40, A-led before and after). That fits my bass-stem boundaries exactly: bass returns 4:11.5 (bass stem +11.3 dB mean mel, novelty 15.5 on the bass, 2.9 on the mix), bass out 4:36.5 (bass -12.0 dB, novelty 15.6). So the G-centred stretch is **4:11.5-4:36.5**, bounded by two bass-stem edges. I therefore redraw my sections 6-7 as one "G-centred bass-on block" (4:11.5-4:36.5) followed by a bass-out stretch (4:36.5-4:46.5). Not 4:00-4:40: no stem changes at 4:00 or 4:08 (mix novelty 4.4 at 4:08, drums 7.2, bass 5.3, none a boundary). Confidence medium-high. Measured (stem edges) plus harmony's bass-pitch counts.
- The F#m/D "lifts" at 2:07.5 and 2:38 are harmony-demoted to passing colour. I accept that for harmony. At 2:07.5 there is still a **timbre/energy** edge (drums +10.0 dB mean mel, other +11.1, novelty on mix 7.5, "other" 12.5), so I keep 2:07.5 as a minor sub-section edge on drums and "other", not on harmony. At 2:38-2:42 the stems show nothing (2:43 mix novelty 3.0), so it is not a boundary. Measured, medium.

**Rhythm Q3: does tempo creep (117.5 BPM at 1:40-2:00 to about 126 at 5:00) match my section boundaries (2:00, 3:00, 4:00, 4:46), and is 5:17-5:19 an outro start?**
- The glide is monotonic and slow (about 1 per cent per minute per rhythm), with no step at 3:44 or any boundary I list. So tempo does **not** mark sections; sections are marked by stem entries and exits. I withdraw my round-1 suggestion that tempo might differ "before and after 3:44": no step exists. Medium, accepting rhythm's two independent measures.
- One coincidence worth keeping (INFERRED, low): the slowest reading (about 117.5 BPM, 4.09 s block spacing at 1:40) falls inside my "thinned tension" stretch 1:44-1:53.4, and the acceleration begins at the 1:53.4 lock. A slight slackening into the arrival is a classic tension device, but the 20 s autocorrelation windows are too coarse to claim intent.
- 5:17: yes, an outro start. Drums leave 5:17.1 (last real onset 5:18.48 per rhythm's 10 ms envelope, floor by about 5:18.9), bass 5:22.5-5:25, then the pulseless tail. I now call the outro **5:17-5:42.84 in two parts: 5:17-5:29 (drone, "other" held about -15 dBFS, no pulse) and 5:29-5:42.84 (fade, about 3.7 dB/s)**. Rhythm's "pulseless from 5:19" fits. High.

**Voice Q2: do the voice events (2:21.5, 3:44, 4:56, 5:12, 5:30) sit on section boundaries or bar lines, and is the 5:30-5:43 murmur a coda or a separate fade?**
Grid: I name none for bar lines. The tempo glides 118.5 to 126 BPM (rhythm) and the drum stem has no clean kick grid, so a fixed-BPM bar-line test would be on a grid that does not match the kick spacing (rule 5). I make no bar-line claim. Against my stem-edge boundaries:

| event | nearest stem-edge boundary | offset | on a boundary? |
|---|---|---|---|
| 2:21.5-2:26.5 | none (2:21 mix novelty 2.5, the lowest of any candidate I tested) | n/a | no; it sits inside a plateau |
| 3:44-3:45.5 | bass out 3:43-3:44 | 0 to +1.5 s | yes |
| 4:56-4:58 | none (inside the bass-in, drum-led stretch 4:46.5-5:17) | n/a | no |
| 5:12.3-5:12.8, 5:16.7-5:17.2 | drums leave 5:17.1 | second event ends at the drum exit; first is 4.8 s earlier | one of two |
| 5:30.5- | fade start 5:29.0 | +1.5 s | roughly |

So 2 of 5 land on a boundary within about 1 s and a third touches it; the strongest, 2:22, lies on no boundary. This agrees with sound's and voice's refusal to use them as recurring markers. The one reading I keep (INFERRED, low-medium): voice shows 3:44 and 5:12 share a narrow-band 1.2-1.6 kHz sound; if that is one recurring tone, it is placed at "the bass leaves" (3:44) and "just before the drums leave" (5:12), i.e. at the two points where the rhythm section starts to come apart. That is an observation of placement, not a claim of design. On the coda: the murmur sits inside my 5:29-5:42.84 fade, which is the **second half of the outro**, not a separate section, because nothing structural changes at 5:30.5 (mix falls steadily, novelty at 5:30.5 17.6 is just the fade slope).

**Sound Q3: should form be described by rhythm-section layering rather than loudness, and where do the "re-balance" starts (2:07.5, 3:28, 3:45.2, 4:00, 4:40) go?**
Yes. Mix level inside 1:53-5:17 moves about 3 dB (round 1), mix-spectrum novelty at the late boundaries is small (mix 2.6-5.8 at 3:13, 3:28, 3:44, 4:11.5, 4:36.5, 4:46.5), while single-stem novelty is large (bass 11.5-21.3 at 3:28, 3:44, 4:11.5, 4:36.5, 4:46.5). The form is a layered one, carried by the bass stem. My ranking, from the measured novelty (mel RMS difference in dB, 2.4 s windows):

| tier | boundary | what carries it | novelty (mix / drums / bass / other) |
|---|---|---|---|
| 1 | 0:11.3 | whole mix from zero | 97.9 on the mix (4 s window) |
| 1 | 1:04.8 | drums then bass | 11.5 / 21.0 / 11.2 / 8.6 |
| 1 | 1:53.4 | "other" +28.7 dB mel mean | 13.2 / 6.4 / 9.9 / 30.3 |
| 1 | 5:17 outro | drums out | (round 1 table) |
| 2 | 2:07.5 | drums, "other" | 7.5 / 11.5 / 2.4 / 12.5 |
| 2 | 3:07 | drums, bass (see section 2) | 4.9 / 21.1 / 11.5 / 4.0 |
| 2 | 3:44 | bass out (-17.7 dB), "other" up | 5.8 / 3.7 / 21.3 / 9.8 |
| 2 | 4:46.5 | bass re-enters (+17.0 dB) with drum push | 5.1 / 13.4 / 19.1 / 3.4 |
| 3 | 3:13, 3:28, 4:11.5, 4:36.5 | one-stem changes | 2.6-4.9 on the mix |
| not a boundary | 4:00, 4:40 (sound's re-balance points) | no stem edge; 4:40 is sound's later reading of my 4:36.5 | 4:08 tested: 4.4 / 7.2 / 5.3 / 4.7 |

Sound's 3:45.2 and my 3:44.0 are the same event read 1.2 s apart (the bass fell over 3:43-3:44 in my 10 ms envelope; sound used a coarser window). Sound's own result (30-150 Hz -3.8 dB, 1-4 kHz +6.4 dB, mix level within 0-4 dB) means 3:44 is a colour and weight change, "lighter and brighter, not louder". Sound's question to me: is 3:44 a section start by itself? My answer: a **tier-2 sub-section start inside a 3:07-4:46 "bass-cycling" block**, not a main section, because mix novelty is only 5.8 against 11.5-13.2 at the tier-1 boundaries. High on the measurements, medium on the labelling (labelling is a judgement).

## 2. Corrections and additions (mine and others')

1. **New edge I missed in round 1: 3:07 is a drum lift, not only a bass change.** Drum-stem RMS (3 s windows): 2:40 -23.2, 2:50 -27.5, 3:00 -29.6, 3:03 -30.7, then 3:06 -27.8, 3:10 -23.3, 3:15 -26.2, 3:20 -23.9 dBFS. So the drums taper 7.5 dB from 2:40 to 3:03 (round 1's "drum highs taper at about 2:55" is the start of that), then return +7 dB by 3:10. Drum mel novelty at 3:07 is 21.1 (mean +20.8 dB, mostly high bands returning), bass +10.2 dB (consistent with my round-1 "bass doubles to 8th/16th notes at 3:07"). Drum onsets per second: 4.6 at 2:45-3:05 and 3.75 at 3:07-3:27 (librosa, so only a rough count), centroid 7163 Hz then 5671 Hz. The song-map items 4c and 4d are therefore split at **3:07 by a drum-and-bass lift**: 2:40-3:07 is the lull (drums at their lowest, -29 to -31 dB, mix still -18), 3:07 is the re-energising. Medium; the drum-stem balance may partly be separator behaviour on the hats.
2. **My "peak" wording was too strong.** Sound shows 3:44 brighter and lighter, not louder; my own 4 s blocks give -13.7 dBFS at 3:44-3:59 against -16 to -19 on the plateau, i.e. 2 to 5 dB. I now call 3:44-4:11 the **brightest and sparsest stretch with the highest short-term level**, not "the peak" as a dramatic climax. The peak I called "made by subtraction" stands as an observation (bass stem -17.7 dB mean mel, mix +4.5), and sound's mix-level Welch figures confirm the timbre change is real, not a Demucs reallocation (rule 7: I lower the "may be Demucs moving synth" doubt, with sound's mix-based evidence). Medium-high.
3. **Voice's rejection of the 4:28.9 speech phrase is right** (text legible only in the transcript, vocal stem -51 dB at 4:27). I had already rated it low; I now treat it as a hallucination for form purposes (INFERRED, high, from voice's evidence). Lineage should not build a section on it.
4. **Tempo.** I withdraw "0.476 s at 3:50-5:00, 118-126 BPM drift, low-medium" as a separate claim and defer to rhythm (drum beat lag 0.494 s at 2:00-3:20, 0.484 at 3:20-4:20, 0.479 at 4:20-5:17). Nothing contradicts it.
5. **Bass-cycling is a stem-edge series, not a rhythm change.** In round 1 I listed bass out 3:44, in 4:12, out 4:18.5-4:23, in 4:24, out 4:36.5, in 4:46.5. Re-measured on the 4 fps stem novelty, the three edges with bass novelty above 15 are 3:44, 4:11.5, 4:36.5 and 4:46.5 (21.3, 15.5, 15.6, 19.1); the 4:18.5-4:23 brief out is a 4.5 s hole inside the G-centred block (round 1, kept, not re-measured here).
6. **Production era** (rule 1): unchanged. Sound's new figures (true peak +0.50 dBTP, unvarying 17 kHz lowpass, no loop repeat: drum autocorrelation 0.01-0.11 at 3.9 s) support my round-1 "modern master, not a rigid loop build". I keep my tags: modern master medium-high; "played or hand-edited to a roughly 120 BPM grid" low-medium. The opening collage (0:11-0:24) and body share the same lowpass, so there is no band-limited archive layer, and the end-of-track fade is DAW-style (one-sample step after the linear-dB fade, round 1).

## 3. How the pieces connect (form, rhythm, harmony, sound, voice)

- **Rhythm serves form** by entering one layer at a time: drums 1:04.8, bass about 1:06, quaver bass 1:53.4, drum lift 3:07, bass cycling 3:44-4:47, drums out 5:17, bass out 5:22.5. Each is a stem edge; the drift of the tempo underneath is continuous and unmarked.
- **Harmony serves form** only through the bass root (A pedal 2:00-3:20, G-centred 4:12-4:36, A with E/G at 5:00-5:20), per harmony's round 2. The chord labeller adds nothing the stems do not.
- **Sound serves form** through colour: sound's bands show 3:44 moving weight from the low band to 1-4 kHz and a 1 kHz sustained band; it is a re-voicing at constant loudness.
- **Voice serves form weakly:** 2 of 5 events on a boundary, no repeated material proven.
- Revised song map (INFERRED labels; boundaries measured): 0:00-0:11.3 silence | 0:11.3-0:24.4 noise prologue | 0:24.4-1:04.8 drone with no rhythm section | 1:04.8-1:53.4 block build | 1:53.4-2:07.5 groove arrives | 2:07.5-3:07 groove, with lull from 2:40 | 3:07-3:44 lifted groove, darkening | 3:44-4:11.5 bass-out, bright | 4:11.5-4:36.5 G-centred bass block | 4:36.5-4:46.5 bass out | 4:46.5-5:17 drum-led finale | 5:17-5:29 drone | 5:29-5:42.84 fade | 5:42.84-6:00.98 silence.

## 4. Measured end of track (restated, rule 4; unchanged from round 1, no new measurement needed)

From the 10 ms envelope of song.wav: last non-zero sample at 342.835 s (5:42.84), amplitude one 16-bit LSB; final 18.14 s exact zero (max |sample| in the last 3 s = 0.0 on the mix; stems at or below -84 dB, separator floor). Last audible sound about 5:42.5 at about -65 dB. Percussive final hits counted from the envelope peaks: 0. Fade about 48 dB over about 14 s (about 3.4-3.7 dB/s), ending in a one-sample step: DAW fade plus trim (INFERRED, medium-high).

## 5. Boundary evidence table, round-2 additions (stem mean mel change, dB, 2.4 s before and after; rule 3)

| boundary | drums | bass | vocals | other | mix | carried by |
|---|---|---|---|---|---|---|
| 2:07.5 | +10.0 | +0.8 | floor | +11.1 | +7.0 | drums and other |
| 3:07 | +20.8 | +10.2 | floor | -3.1 | +2.3 | drums, then bass |
| 3:28 | -1.7 | -9.4 | floor | +4.5 | +1.9 | bass |
| 3:44 | +1.4 | -17.7 | burst, floor either side | +8.2 | +4.5 | bass down, other up |
| 4:11.5 | -4.9 | +11.3 | floor | +4.4 | +0.1 | bass |
| 4:36.5 | -0.4 | -12.0 | floor | -2.1 | -1.3 | bass |
| 4:46.5 | +3.1 | +17.0 | floor | -2.1 | +2.3 | bass |

(The round-1 table remains the reference for the other boundaries; vocals are at the separator floor except in the events listed in section 1.) No new silence claims: the table's mix levels never fall below the plateau by more than a few dB, so every "quiet" point is a stem dropout, not silence.

## 6. Two new questions

1. **To Rhythm:** the drum stem tapers about 7.5 dB (2:40 -23.2 to 3:03 -30.7 dBFS) and returns about 7 dB by 3:10, with bass going to 8th/16th figures at 3:07. Is that a real change of drum pattern (hats or ride opening, fill at 3:06-3:08, snare dropped out) or Demucs level behaviour, and does the bass-quarter against bass-eighth grid at 3:07 keep the same pulse (no tempo step)?
2. **To Sound and Voice:** is the narrow-band 1.2-1.6 kHz sound at 3:44 and 5:12 (voice's finding) the same thing as the sustained band near 1 kHz that sound measured across 3:44-4:11? If so it is a held tone, not a voice, and its recurrence at 3:44 and 5:12 could be a lead or whistle-like synth marking the two bass-out and drums-out moments; please check whether it is present at 4:36-4:46 (bass out again; round 1 saw held tones at about 390 Hz and 1 kHz there).

## Not recoverable by measurement

- Whether the sections are intended as the "A and B" sections a composer would name: only stem edges and levels are measured; the labels are my interpretation.
- Whether the 11.3 s and 18.14 s silences are artistic or file padding: only this file is measured.
- Whether the abrupt cut at 5:42.84 is a chosen ending: the cut is measured, intent is not.
- Instrument identity behind "other", the 1 kHz tone, the 3:27.5-3:28.5 glide: the separator merges sources.
- Whether voice-like events are speech, processed instruments or samples, and what, if anything, is said: stems 30-50 dB under the mix and Whisper output is unreliable.
- Whether the tempo glide is performed, tracked in real time or a drawn tempo map: autocorrelation shows the drift, not its cause.
- Whether a listener feels 3:44-4:11 as a climax or as a lull: level, brightness and sparseness are measured, the feeling is inference.
