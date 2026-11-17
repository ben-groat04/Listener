# video1 music: "Elfstedentocht Part 1" (Public Service Broadcasting), ears report

Written by the music agent. I cannot play audio; everything below is inferred from signal measurements (librosa on `audio/song.wav`, 44.1 kHz stereo, 3:08.66), the auto features, beat times and Whisper transcripts. Confidence tags: [H] high, [M] medium, [L] low. OBS = measured/observed; INT = interpretation.

Scripts: `v1/scripts/agents/music_v1_ears.py` (new), `music_extra*.py` (earlier). Outputs: `v1/data/video1/audio_features/extra/` (`ears_sections.json`, `ears_run.txt`, `extra3_run.txt`, `music_extra.json`, `chroma_sections.json`). I did not view the spectrogram images; section boundaries come from numbers.

## 1. Genre and identity
- Context (verified elsewhere, not by me): PSB, "Elfstedentocht Part 1", 2013, described by press as loud guitar-riff rock. My measurements are consistent with that: [M].
- INT: instrumental rock / post-rock-adjacent with archive-film voice-over used as a sample "vocal". There is no sung vocal; the only voice is Dutch newsreel-style narration (see section 5). [M-H] no sung vocal (the transcripts contain only spoken material and place names; the loudness never shows a lead-vocal-like pattern, though without stems I cannot rule out a wordless one).

## 2. Tempo and metre
- OBS: beat tracker gives a constant 78.3 BPM (beat interval 0.766 s, identical in every 20 s window, so it is probably a locked grid, not a performance of drifting tempo). Onset autocorrelation peaks at 0.766 s, 0.383 s (eighths), 1.533 s and 3.07 s (= 4 beats, one bar). Alternative tempo candidates from the tempogram: 152 and 103. [H] for a steady pulse of 0.766 s; a bar of 3.07 s.
- Octave ambiguity: 78 BPM vs 156 BPM (152 is near double). INT: it will likely FEEL like a slow, heavy, plodding 78 with a half-time backbeat, or a driving 156 depending on the listener; the riff note spacing (strong low-band repeats at 0.77 s) favours the slow, heavy reading. [M-L]. Cut/beat alignment is not used here (see visual agent).
- Metre 4/4 [M]. Kick/snare/hat positions within the bar are only weakly resolved (kick-ish energy most on beat 1; offbeat hat-like energy on the "&"s) [L].

## 3. Instrumentation (evidence, not hearing)
- Distorted electric guitar riff, doubled by bass: [M]. Evidence: in the rock sections energy is dominated by 80-250 Hz and sub-80 Hz (62-68 dB band levels), with a broad 250 Hz-6 kHz body, high harmonic sustain (percussive/harmonic ratio about -5 dB, i.e. harmonic-dominated), a pitch centre fixed on D with chromatic neighbours C, C#, D# (a riff that leans on semitones, a hard-rock/metal-ish colour), and strong low-band repeats on the 0.77 s grid.
- Live-sounding or programmed drum kit: [M-L]. Evidence: onset density about 4.5-5 per second throughout, cymbal/air-band energy (6 kHz+) 30-35 dB in loud sections, hat-like offbeat energy. I cannot separate kit from guitar stabs.
- Sub-bass / synth or processed bass thumps: [M]. Evidence: in the 1:58-2:34 break the sub-80 Hz band holds 65 dB while everything above drops, and discrete thumps at about 1.4-1.5 s spacing appear (118.1, 119.0, 121.2, 122.9 ... measured peaks, irregular so partly guesswork) [L for the exact pattern].
- Archive voice-over sampled over the mix (300-3400 Hz speech region). [H] it exists (transcripts); mid-band energy shows no obvious ducking around it, so the narration sits inside the band rather than the band stepping aside. [L]
- Stereo: overall L/R correlation 0.55, S/M about -5 dB, widening as the track builds (see table). Guitars/other layers appear panned or doubled wide in the loud sections. [M]

## 4. Structure map
Section boundaries from auto-segmentation (`summary.json`) refined by my per-second loudness and band measurements. Levels are RMS dB (full-scale), P/H is percussive-minus-harmonic dB (higher = less sustained harmonic body), width is L/R correlation (lower = wider).

| Time | OBS | INT (label) | Conf. |
|---|---|---|---|
| 0:00-0:01 | Starts from digital silence (-44 dB) then jumps to -15 dB in 1 s | Track enters abruptly on the first beat; likely the clip was cut from the video, not a fade-in | [H] |
| 0:01-0:15 | -14 dB, narrow stereo (0.82), darker (centroid about 1.5-2.8 kHz), riff already present; first narration 0:09 | Intro: the riff states the theme at moderate weight while the date is spoken | [M] |
| 0:15-1:06 | Louder (-12 to -11.6 dB), wider (0.67 to 0.61), D pedal with C/C#, bands up about 6-8 dB vs intro | Verse/main-riff section A, the "engine room" of the track | [M] |
| 1:06-1:16 | Loudest plateau, -11.3 dB, much wider (corr 0.42, S/M -3.9 dB), less onset density (3.3/s), D major tendency (D, A, B, C) | Lift/pre-chorus: widening and a slightly more open harmony | [M] |
| 1:15 | Level drops 4 dB at 1:15; sub-bass, mid and air all lower | Hard cut to a stripped section | [H] |
| 1:16-1:28 | Quietest steady part (-15 to -17 dB), P/H positive (+2.3 dB, i.e. little sustained guitar), key centre shifts to C major / A minor (C, F#, A, F), narration at 1:19-1:27 (the numbers of riders) | Breakdown: guitars out, sparse texture, a harmonic step away from D | [M-H] on drop; [L] on key |
| 1:28-1:49 | Back to -13 to -10 dB, D minor, wide (0.40) | Riff returns, bigger and wider than before; second main block | [M] |
| 1:49-1:59 | Loudest section overall (peak per-second about -10 dB at 1:51-1:54), but darkest: air band falls from 30 to 25 dB, presence 39 to 31 dB, spectral centroid dips to about 1.1 kHz near 1:50, then recovers | A climb with a low-pass "closing" effect, or a thick low-end-only build; ends at the cut below | [M-L] on cause |
| 1:58-2:01 | Sudden -6 dB (to about -19/-21 dB) at 1:58 | Everything stops mid-phrase: the hinge of the whole track | [H] |
| 2:01-2:14 | Level jumps back +6 dB at 2:01 for one second, then -16 to -19 dB with repeated +5 dB returns at 2:07 (127 s) and 2:13 (133 s) | A quiet, sub-bass-led passage with full-band hits every 2 bars (6.1 s = 2 bars of 3.07 s) | [M-H] |
| 2:14-2:39 | -15 to -11 dB, centre moves to A minor / F, i.e. a new harmony; steady build 2:20-2:35 (-14 to -11 dB), highest harmonic content around A, G, E, F; narration with 11 place names from 2:18 to 2:39 | Second-half build: the riff returns in a different key area while the route is read out town by town | [M] on build; [L] on exact chords |
| 2:39-3:08 | Back to D minor, -11 to -12 dB, widest of the whole track (corr 0.31, S/M -2.8 dB), air band at its highest (35 dB) | Final statement: the main riff at full width and brightness, with the closing line of narration | [M] |
| 2:47.8 | Short dip to about 0.08 RMS (about -22 dB) for 0.5 s, immediately after the narration finishes saying "Elfstedentocht" | A one-beat break or stop-time hit, then the riff resumes | [M] |
| 3:07-3:08 | Final second falls to zero abruptly (last windows 0.31, 0.18, 0.11, 0.00) | Hard stop/short tail; probably the clip's own end rather than a fade | [M] |

(Whisper's "Bedankt voor het kijken" at 3:07 is a known hallucination on silence/noise; ignore it [H].)

Section-level measurements (from `ears_sections.json`): rms dB / P-H dB / low-band levels sub-bass, bass, low-mid, mid, presence, air (dB) / L-R corr.
- 0:00-0:10: -14.4 / -2.1 / 62 59 47 38 31 26 / 0.84
- 0:10-0:15: -13.3 / -2.7 / 59 57 47 39 33 22 / 0.80
- 0:15-0:40: -12.0 / -4.6 / 68 64 56 47 40 31 / 0.74
- 0:40-1:06: -11.6 / -4.9 / 68 65 57 48 41 32 / 0.61
- 1:06-1:16: -11.3 / -5.6 / 63 61 53 45 39 32 / 0.42
- 1:16-1:28: -14.9 / +2.3 / 60 58 51 42 35 28 / 0.63
- 1:28-1:49: -11.9 / -4.6 / 65 63 57 48 39 30 / 0.40
- 1:49-1:59: -11.1 / -7.2 / 64 63 51 42 31 25 / 0.52
- 1:59-2:14: -14.9 / +0.9 / 65 58 47 41 34 29 / 0.85
- 2:14-2:39: -12.4 / -2.3 / 66 62 57 50 42 33 / 0.60
- 2:39-2:52: -11.6 / -5.4 / 66 63 52 42 38 29 / 0.52
- 2:52-3:09: -11.5 / -5.1 / 65 64 54 45 43 35 / 0.31

## 5. Key and harmony
- Overall: D centre, major/minor undecided (D major 0.76 vs D minor 0.756 in the whole-song estimate). Per-section chroma mostly favours D minor in the riff sections, with D, C, C# prominent. INT: a D-rooted riff that includes C and C# against the D pedal makes the major/minor call unreliable; "D minor with chromatic colouring" is my best reading. [M-L]
- Excursions: 1:16-1:28 C major / A minor area [L-M]; 2:01-2:14 and 2:14-2:39 F / A minor area [L]. These are the two moments the track leaves D.
- No true key change in the sense of a modulation that stays; each excursion returns to D. [M]

## 6. Dynamics
- Highly compressed: short-term level 10th-90th percentile only -15.2 to -10.9 dB, mean -12.2 dB, sample peak near full scale (1.0). The contrast the ear hears therefore comes from texture, width and band balance more than from raw loudness (the two quiet sections are only 4-6 dB below the loud ones). [H]
- Loudest sustained moments: 1:49-1:55 and 1:06-1:15; the track gets wider rather than louder toward the end.

## 7. How the music frames the words
OBS: narration lines (corrected from the Dutch transcript; Whisper wrote "Elfstedentuin" and similar mistakes; the English translation is also unreliable, e.g. "575 race drivers" for wedstrijdrijders, "Tour riders" for toerrijders): 0:09 "18 januari 1963", 0:12 "Het staatsmarathon zonder winnaar" (my reading), 0:16 "half zes in de ochtend", 0:19-0:27 about 200 [sic: transcript says "tweehonderd"] visitors / "only the strongest", 0:27-0:32 "dat is de Elfstedentocht", 0:40 "de twaalfde Elfstedentocht", 0:51 "Temperatuur 16 graden onder nul", 0:53 "een monsterrit van ruim 200 kilometer", 1:19-1:27 rider numbers, 2:16-2:39 the eleven towns, 2:44-2:48 "waar iedereen zich voor opmaakt, dat is de Elfstedentocht".
INT:
- The opening date and "half past six in the morning" land over the riff while the band is still narrow and dark: the music is already moving as the voice sets the scene. [M]
- The numbers (riders, "ruim 200 kilometer") are delivered in the stripped breakdown at 1:16-1:28, where nothing competes with the voice. That is the one spot where the voice is clearly foregrounded by arrangement. [M]
- The place names (2:18-2:39) arrive during the build in a new harmonic area, so the list of towns reads as the field moving out across the course. [M-L]
- The closing "dat is de Elfstedentocht" at 2:46-2:48 is followed within a second by the short dip at 2:47.8 and then the widest, brightest version of the riff: the music answers the line with a full band statement. [M]
- Pattern: the narrator is a rhythmic element (separate phrases, spaced a beat or two apart) more than a lead. I have not measured the exact alignment of phrase onsets to the 0.766 s grid. [L]

## 8. Emotional arc (INT, listener view)
1. 0:00-1:06 Resolve and anticipation: a heavy, steady riff, slow like a crowd moving, not frantic. A sense of weight and cold. [M]
2. 1:06-1:16 Lift: wider, brighter harmony, a feeling of numbers swelling. [L-M]
3. 1:16-1:28 Hush: sudden thinning, the "stand and look" moment; the facts are read out. [M]
4. 1:28-1:58 Return and escalation to the darkest, heaviest, most compressed stretch, then a cut-off. [M]
5. 1:58-2:14 Emptiness or held breath: low pulse, sparse hits every 6 s. Probably the most "cold" and exposed part. [M-L]
6. 2:14-2:39 Setting off: a new harmony area and a steady build as the towns are named. [M]
7. 2:39-3:08 Arrival: the original riff at full width, ends abruptly rather than resolving. [M]
Overall the track is relentless more than climactic: loudness barely changes, so tension is handled by removal (1:15, 1:58) and by widening, and the end is a stop, not a resolution. [M]

## 9. Moments a listener would remember
1. 0:00-0:01: the instant start on the riff, no lead-in. [H]
2. 1:15: the floor drops out into the quiet breakdown. [H]
3. 1:19-1:27: the stripped passage where the numbers are read. [M]
4. 1:49-1:58: darkening climb and the sudden stop at 1:58. [H]
5. 2:01 and 2:07/2:13: single full-band hits in the quiet section, every 2 bars. [M-H]
6. 2:18-2:39: the town list over the build. [M]
7. 2:47.8: the half-second dip after "Elfstedentocht", then the wide final riff. [M]
8. 3:08: hard stop. [M]

## 10. Limits and open questions
- No stem separation exists for this video (`stems/` is absent), so I cannot tell guitar from bass from keys, or confirm there is no wordless vocal. A listening agent with stems would resolve this.
- Tempo octave (78 vs 156) is not decided by the numbers alone.
- Exact chord content is guesswork; chroma on distorted guitar is dominated by the root and semitone neighbours.
- Whisper times for speech are usable (+/- 1 s); text is not.
