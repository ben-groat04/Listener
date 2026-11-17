# video1: FORM and dynamics specialist, round 1 (blind, measurements only)

Evidence key: LV = music_views/per_second_levels.json (dBFS, width, per-stem dB); MV0xx = music_views/window_0xx0s.png; OV = audio_features/overview.png (loudness, centroid, chroma, auto-sections); CH = chords.json; LY = lyrics/whisper_medium_mix_nl_*; WIN = the ten win_*.md notes. My own helper: v1/scripts/agents/video1_form_sections.py (per-section averages from LV). Timestamps m:ss. File length 3:08.66, tempo about 78 BPM (beat gap 0.77 s), tonic D (D major 0.76 vs D minor 0.756, summary.json).

## 0. Headline

This is not a verse/chorus song. It is a **continuous, never-stopping 78 BPM drum stream (16th-note comb, about 4-5 hits/s, drums stem -14 to -21 dB the whole way, no drum stop anywhere) with a D drone on top, shaped almost entirely by layers entering and leaving**: bass in/out, the "other" (guitar/synth-like) wall in/out, stereo width opening/closing, and a spoken (not sung) announcer voice that comes and goes. The drama is built by *subtraction and re-entry*, not by tempo, key change or melody. I read it as a **sectional, additive/subtractive "build-and-strip" form with three bass-less "hollow" passages (1:15-1:40, 1:56-2:13, and the partial 2:13-2:38 gated-bass zone) and a final locked-in wide wall (2:48-3:08)**. Confidence in the broad map: high. Confidence in the exact interpretation of causes (what the instruments are): low.

## 1. Song map (with the numbers that define each section)

Averages are from my script over LV (mix dBFS, stereo width 0-1, "other" dB, bass_on = share of seconds with bass stem above -40 dB, voice_on likewise).

| # | Time | Label | Mix dB | Width | Other dB | Bass | Voice | Key evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:00-0:09 | **Intro, built in stages** | -14.7 | 0.31 | -30 | 33% on | none | Drums alone in second 0 (mix -19.9, other -60.6, bass -66.9: LV t=0), "other" wall arrives ~0:01.3 (+30 dB, MV000), bass creeps in -44 (0:04), -36 (0:06), -30 (0:08) |
| 2 | 0:09-0:32 | **Verse-like A: spoken statement** | -12.2 | 0.36 | -22 | on | 91% | Voice enters 0:09.5-0:10 (LV; whisper "18th of January 1963", LY 0:10); bass climbs to -19 by 0:20; speech blocks 0:20-0:26.5, 0:28-0:31.7 (MV020 vocals panel) |
| 3 | 0:32-0:50 | **Voice-free groove, first widening** | -12.4 | 0.50 | -22 | on | 11% | Voice gone 0:32 (LV -62.7), width jumps 0.38 -> 0.55 at 0:32, drum centroid ~1.6 -> ~3.3 kHz per WIN 0020, "other" dips to -25 at 0:36 then swells |
| 4 | 0:50-1:15 | **Build to first peak** | -11.2 | 0.54 | -16.5 | on | 36% | "Other" climbs -25 (0:40) -> -14.8 (0:58); mix hits -10.3 at 0:58; width reaches 0.67-0.71 at 1:06-1:10; two speech bursts 0:50.8-0:56.5 ("-16 degrees", LY) |
| 5 | 1:15-1:27 | **First collapse: thin, bass-less, spoken** | -15.2 | 0.46 | -23 | **8%** | 75% | Mix drops -11.1 -> -14.5 -> -16.4 across 1:14-1:16 (OV: loudness trough from ~1:16), bass to -65 at 1:16 (LV; MV060 bass panel cuts at 15 s), "other" -21 to -27, speech 1:18-1:27 (LY: 575 riders, 9,500 tourists) |
| 6 | 1:27-1:40 | **Wall without a floor** | -12.7 | **0.76** | -15.7 | **0%** | none | At 1:27 voice cut (-62.5), other jumps -27.5 -> -17.2, width 0.36 -> 0.62 -> 0.78-0.83 (LV), mix +3 dB; drums flat; bass stays at floor to 1:40 apart from a lone D hit at 1:28-1:29 (-43, -55 dB) |
| 7 | 1:40-1:55 | **Bass slam, second peak** | **-10.7** | 0.53 | -15.7 | on (-19 at 1:40, +46 dB from 1:39 -53.8) | 20% | Width collapses 0.8 -> 0.47 as the centred bass lands (LV 1:39-1:40); drums swell -16.2/-15.8/-14.0 at 1:52-1:54 (loudest drum passage, LV); mix peak -9.5 at 1:52 = the loudest point of the whole file in my table |
| 8 | 1:55-2:01 | **Drop-out and wash (the break)** | -14.1 | 0.50 -> 0.28 | -22 | off (-20.5 at 1:54, -33.5, -62.5 at 1:56) | brief | Bass leaves 1:55; "other" falls -13.4 (1:56) -> -25.9 (1:58) -> -30.9 (2:00); rising noise wash at ~1:57.8 (MV100 "other" panel at 17.8 s) then only <1 kHz; OV also marks a darkening, centroid falling to ~1 kHz at ~1:50-1:58 |
| 9 | 2:01-2:13 | **Stripped groove (gated sub pulses)** | -15.2 | **0.30** (narrowest passage after the intro) | -26 | 33% (single notes at ~2:01, 2:07, 2:13) | none | Bass appears for ~2 s every ~6 s (8 beats), each +4 dB in the mix (LV 2:01 -14.9 vs 2:04 -16.1; 121/127/133 s mix jumps +4.1, +4.2, +3.5); WIN 0120 measures this; chords static D / Dm |
| 10 | 2:13-2:38 | **Narration and place-names, harmony moves** | -12.6 | 0.50 | -17.5 | 48% (gated, 2-3 s blocks) | 56% | "Other" +6 dB at 2:13-2:14 (-26 -> -19), width 0.25 -> 0.48-0.55; voice 2:15-2:19, then the town list 2:21-2:39 (LY); chords wander Dm-Am-D-G-D, later Am/G/Dm/F/C (WIN 0120, 0140) |
| 11 | 2:38-2:48 | **Re-lock and the closing statement** | -11.6 | 0.49 | -20.5 | **continuous from 2:38** | 40% | Bass returns thick at 2:38 (LV -29 -> -17.7 at 2:40) and *stays*; voice 2:44-2:48 "that is the Elfstedentocht" (LY); drum level -13.7 to -14.8 at 2:44-2:46 (loud for this track) |
| 12 | 2:48-3:09 | **Coda: wide wordless wall, then stop** | -11.5 | **0.73** (0.85 at ~3:05) | -16.4 | continuous | none | 2:47.8-2:48.2 a 12 dB mix dip (256-sample RMS, WIN 0160); after it width 0.5 -> 0.7+, top shelf to ~9-10 kHz, chords a single D for 20.7 s (CH 2:47.97 to end); end: drums and bass stop first, tail silent by ~3:08.5 (WIN 0180) |

**Cross-check against OV auto-sections.** The automatic section labels (C 0:00; B 0:15; D 1:07; A 1:16; B 1:28; B 1:50; A 1:59; A 2:02; E 2:14; B 2:39) are consistent with my boundaries at 1:16 (collapse), 1:28 (wall), 1:50 (darkening before the break), 1:59-2:02 (stripped), 2:14 (lift), 2:39 (re-lock). The tool splits them on timbre, not on meaning, and its "B" repeats suggest that 0:15-1:07, 1:28-1:50 and 2:39-end share a "full band" sound; this agrees with my reading that there are really only **two states** the track alternates between: (F) full band with bass, or (H) hollow (bass out and/or "other" thinned). The local-tempo panel in OV flips between ~78, ~104-108 and ~152 and should be ignored: the beat is steady at 0.77 s (WIN 0000, 0080, 0180) and the flips are half/double-time tracking.

## 2. Tension and release: how it is engineered

Everything here is read from level, width, spectrum and bass presence; I cannot hear it, and a human's felt response is an inference.

1. **The loudness range is small, so the contrast is made with timbre and weight.** Per-second mix level sits in -9.5 to -16.5 dBFS the whole song (LV). The loudest vs quietest sustained passages differ by about 5-6 dB (e.g. 1:52 at -9.5 vs 1:16-1:26 at about -15 to -16.5). Hence the track relies on *what* is present rather than *how loud*. Heavily compressed, wall-like (WIN 0160 "very loud and compressed"). High confidence.
2. **Bass is the main tension valve.** Two long bass-absences (1:16-1:40: 24 s; 1:56-2:38 mostly off with brief gated notes: ~42 s) end each time with a sudden, large re-entry (1:40 is a roughly +35 dB jump in the bass stem from -53.8 at 1:39 to -19 at 1:40 per LV, +46 dB from the floor; 2:38 climbs -64 -> -29 -> -17.7 in 2 s). Removing the low end for a long stretch and then putting it back is the strongest release device in the file. The bass is absent for 1:16-1:40 and 2:01-2:38 (mostly), i.e. it is *off* for about 64 s of 188 s. High confidence on the numbers, medium on "felt as release".
3. **Width is the second valve and it moves opposite to bass.** Width goes wide when bass is out and the "other" layer carries a sustained wall (0.76-0.83 at 1:27-1:39) and collapses when the centred bass lands (0.78 -> 0.47 at 1:40; LV). It then ends the track at its widest (0.73-0.85 for the final 20 s). So the *final* section is wide AND bass-on, which is a new combination in the song: the arrival is "everything at once" for the first time (check: sections 6 and 7 each have only one of those two; section 12 has both). That is my main structural reading of the ending as a climax and I rate it medium-high.
4. **Speech is the narrative engine; it is placed in the lower-energy states.** Voice-on share is highest in sections 2, 5 and 10 (91%, 75%, 56%), i.e. in the thinner or developing passages; the biggest instrumental peaks (4 -> 1:27-1:55, 12) are mostly voice-free, plus the loudest of all is voice-free. The voice stops at the moment of the biggest instrumental gain (1:27, other +10 dB, width doubles). Pattern: **talk, then the band answers.** Medium-high confidence; the speech content is only what Whisper gives (Dutch, translated), so I treat the words as secondary.
5. **Hold-then-hit mechanics** (the specific "big moments"):
   - **0:01.3, wall arrives.** One second of drums only, then "other" jumps by about +30 dB in one step (LV t=0 to 1, other -60.6 -> -30.5) and the mix by +6.3 dB (largest single-second mix jump in the file). A cold-open that announces the sound-world immediately. High.
   - **1:15-1:16, the floor falls out.** Bass cut (-19.4 -> -28.7 -> -65.2) and mix -11 -> -16 within 2 s, with a long sustained A (chroma, ~1:15-1:18, WIN 0060) over a D-based loop. A suspended, unsupported feeling. Medium.
   - **1:27, the "big wall".** Voice stops, "other" fills 100 Hz-8 kHz, width doubles (MV080 at x=7.2 s). The 13 s that follow have no bass, long sustained D-pedal tones (D, Am, C, Dm per WIN 0080), so energy is high but weight is missing, which holds tension unresolved for 13 s.
   - **1:40, the release.** Bass from -64 to -19 dB; mix +1-2 dB; width collapses; it is the payoff to the 1:27-1:40 suspense. This is the best-engineered "drop" in the track (preparation 13 s, then a big step). High on the mechanism.
   - **1:52-1:54 drum swell, 1:55 bass out, 1:58 wall out.** A *staggered exit*: drums get louder (+4-6 dB), then bass goes (1:55), then "other" collapses over 1:57.8-2:00 (mix -9.5 -> -16.5, a roughly 7 dB fall) with a rising noise sweep at about 1:57.8 just before it (MV100 other panel). A classic "build, pull out layers one by one, leave the groove exposed". Medium-high.
   - **2:01-2:13, gated sub pulses.** A three-times-repeated 8-beat cycle: bass note +4 dB in the mix every ~6 s (LV mix jumps at 2:01, 2:07, 2:13). Tension through repetition with a minimal event. Medium on the 4/4 assumption behind "8 beats".
   - **2:13, the second lift.** "Other" +6-7 dB and width 0.3 -> 0.5; first real chord motion (Dm-Am-D-G-D-Dm 2:15-2:19, CH). Opens the narration part. Medium-high.
   - **2:38 re-lock and 2:47.8 micro-stop.** Bass back for good at 2:38; a ~0.35 s dip of about 12 dB across the mix and all stems at 2:47.8-2:48.2 (WIN 0160 256-sample RMS; it is a deep dip, not digital silence), exactly at the end of the closing speech. After it: wider (0.69-0.79), brighter (shelf to ~9-10 kHz), voiceless, single-chord D. A "held breath then open air" device. High on the dip, medium on the width and brightness interpretation. (Note: I would call it a 12 dB dip, because the stems read as silent but the mix RMS does not.)
6. **The ending is a stop, not a fade.** Per WIN 0180, the last seconds are drums and bass stopping first, notes decaying by about 3:08.3, silence by about 3:08.5; the OV loudness panel shows a steep fall at the very end, not a long taper. The chroma moves D -> G -> E/F in the last ~2 s (about 3:06.5-3:08.6, WIN 0180; low confidence because the tail is blurred). A "stop on a gesture away from the tonic" would be unresolved; I rate that low and flag it for harmony.

## 3. The shape of the whole, in one picture

Energy (loudness x weight x width), my reading of LV:

```
0:00  low-mid  ramp (drums -> wall -> bass in stages)
0:09  mid      statement (speech, bass up to -19 by 0:20)
0:32  mid+     voice-free widening, "other" dips and builds
0:58  PEAK 1   (-10.3 mix, other -14.8, width 0.5-0.7)
1:16  LOW      collapse (bass out, thin) ........ speech
1:27  mid+     wall, no bass, widest (0.8) ....... unresolved
1:40  PEAK 2   bass slam (mix -10.9 to -9.5 by 1:52) 
1:56  LOW      pulled apart (bass, then wall out)
2:01  LOW      gated sub pulses, narrowest
2:13  mid      lift + narration + moving chords
2:38  mid+     bass re-lock, closing speech
2:48  PEAK 3   wide wordless wall to the stop (-11.5, width 0.73+)
3:08  end      hard stop
```

Three peaks (about 0:58, 1:52, 2:48-3:08), each preceded by a thinner passage, with peak 3 the only one that combines width and bass and the longest (20 s, no further contrast). That is a plausible long arc: **statement -> build -> collapse -> wall -> bass slam -> strip -> narration/lift -> final locked wall**. The periodicity is irregular (sections of 9, 23, 18, 25, 12, 13, 15, 6, 12, 25, 10, 21 s), so I do not hear a regular verse/chorus grid. A 2-bar unit (about 6.1 s at 78 BPM, 4/4 assumed) is visible only in sections 9-10 (bass at 2:01, 2:07, 2:13, 2:19.5).

## 4. Where the window notes need care (checks against my own measurements)

- WIN 0160 headline "hard cut at about 2:48 (broad silence in all stems)" (said in WIN 0140 hand-off): the cut is real but is a 12 dB dip lasting ~0.35 s in the raw mix; the stems read near-zero. Same event, so I give the width of the dip as 12 dB, not silence.
- WIN 0100 says bass "returns at 2:01 then drops out again" and WIN 0120 says four gated entries; LV agrees (bass -19.9 at 2:02, -66 at 2:04, -18.5 at 2:08, -55 at 2:10, -17.4 at 2:14, -62/-63 at 2:16-2:18, -16.4 at 2:20). Between 2:13 and 2:38 the bass is on for ~48% of seconds, in short blocks; I classed it as "gated" rather than absent.
- WIN 0000 gives the bass as present from 0:03; LV agrees (-43.9 at 0:04) but it is only a faint low smear below about 250 Hz until ~0:05.5, so "bass enters" is gradual, 0:03-0:20 (-44 -> -19.5), a 17 s ramp, not an event. I treat the intro as a *long build*.
- Section 3 vs 4 boundary: WIN 0020 sees the voice exit at ~0:31.7 and a brighter bass entry ~0:34.8; WIN 0040 sees "other" rise from ~0:42. I put the true build start at ~0:40-0:42 (LV other -25 -> -17 by 0:50). Uncertainty of a few seconds either way.
- The OV local-tempo curve and WIN 0160's note that the pulse could be 78 or 156 BPM are an unresolved half/double-time question. It does not change the form map; it changes whether a listener feels bars of 3.1 s or 1.5 s (for rhythm).
- Whisper's text is unreliable (Dutch pass vs translation disagree on nationalities, WIN 0080). I use words only as markers of when a speech block starts and ends.
- CLAP tags (e.g. "triumphant" 0.9+ at 1:25, 2:10, 2:45) agree with my peaks only loosely; they were not used as evidence for any boundary.

## 5. What a listener would probably feel through the form (inference, medium)

- **0:00-0:20:** a quick, hard start and a slow thickening: curiosity, then locking in.
- **0:09-0:32:** informational, documentary: a voice stating facts over a groove.
- **0:32-0:58:** momentum building; "other" swelling, width opening (0.38 -> 0.55): rising anticipation.
- **1:16-1:27:** a sudden thinning, then facts again: a sense of exposure and scale ("numbers"), a hush in weight though not in pulse.
- **1:27-1:40:** a surge of scale without ground, "hovering heroic" (D drone, open fifths, no third settled): unresolved suspense.
- **1:40:** arrival, weight, punch.
- **1:56-2:13:** stripped, hypnotic, slightly cold; the pulse alone and the sub notes land like heartbeats.
- **2:13-2:38:** a procession: the list of names plus moving chords reads as travelling along a route.
- **2:48-3:08:** resolve and determination, then a sudden stop (no afterglow).

## 6. Limits

I cannot hear; "bass", "other", "wall" are stem labels from demucs, not instrument identities, and stem leakage means small level readings near the floor (below about -60 dB) are not literal silence. Section edges are good to about +-2 s. The major/minor third stays ambiguous throughout. I have not checked whether any segment repeats note-for-note (a loop-level repeat map would need a self-similarity pass, which I did not run); the claim "no verse/chorus grid" is based on timing and level only. Mix loudness figures are 1-second RMS values from LV, not LUFS.

## 7. Three questions for fellow specialists

1. **Rhythm:** Is the real felt pulse 78 BPM with a 16th-note comb, or 156 BPM with steady 8ths? And in 2:01-2:19, do the bass entries really fall every 8 beats of 4/4 (about 6.1 s), and is there any bar-level pattern (kick/snare placement) in the drum stem that changes between my "F" and "H" states, particularly the 1:51-1:54 swell and the brighter drums after 0:32?
2. **Harmony:** Over the long D drone, does the 1:15-1:18 held A, the 1:27-1:40 Am/C/Dm alternation and the 2:15-2:38 wandering (Dm-Am-D-G-F-C) amount to real tension relative to D, and does the final D section (2:48-3:08, one label) contain a third at all? What does the G -> E/F chroma motion in 3:06.5-3:08.6 do to the sense of ending (unresolved or just tail artefact)?
3. **Sound (with voice):** What changes at 1:27 (other +10 dB, 100 Hz-8 kHz, width 0.36 -> 0.8) and at 2:13 (other +6 dB, width doubled) in spectral terms: a new layer, a filter opening, or the same guitar-like layer simply louder and wider? And does the voice stem show any processing (band-limiting, radio filter) that differs between the 0:09-0:31 block and the 2:21-2:48 list that would explain why it feels like archive material or a performed announcer?
