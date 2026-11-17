# t_dl_mirror: LINEAGE specialist, round 1 (blind, measurements only)

Scope: genre and lineage inferred from the sound alone: what the track resembles, which traditions it draws on, and what in the measurements says so. I read all twelve `win_*.md` notes, then re-measured the points below myself. I also read the four round-1 colleague files (harmony, rhythm, sound, voice) and carry their figures with their tags, marked "(colleague)". Images opened: `music_views/window_0060s.png`. Other files used: `chords.json`, `lead_notes.json`, `clap_tags.json`, `audio_features/summary.json`, `lyrics/` (mix and vocals-stem Whisper passes, including the doubtful files). Scripts: `v1/scripts/agents/lineage_r1_tdl.py`, `lineage_r1_b.py`, `lineage_r1_c.py`, `lineage_r1_d.py`. Times m:ss. Stems are demucs estimates and leak into each other. No context.md, research or web was used. Names of artists or scenes below are "resembles the tradition of", never an identification of this track.

## 1. Verdict

A rapped-verse and sung-hook **hip-hop track in a "loop-and-mute" beat-tape manner**: one fixed 94 BPM drum loop, a one-chord D-and-A drone bed, a sparse sub-bass that is switched on and off in four-bar blocks, a close dry voice that raps three narrative verses in a near-monotone and chants a four-times-repeated hook. It sits at the **crossing of three traditions**, none of which it follows cleanly:

1. **Boom-bap-era tempo and storytelling rap** (94 BPM, syncopated kick, verse as first-person narrative with dense internal rhyme). INFERRED, confidence medium-high.
2. **DAW or drum-machine production** (grid-locked tempo, pitched sub-bass, mute-based arrangement), not sample-chop boom-bap. INFERRED, medium.
3. **Dark minor-drone cinematic rap** (static D-A bed, no real chord changes, a rare Gm-F side-step). INFERRED, medium-low.

It reads as modern production on a bandwidth-limited, mono, loudness-maximised delivery chain. It does not read as archive material or as a period recording. INFERRED, confidence medium (section 4).

## 2. Evidence for the hip-hop core

| Cue | Measurement | Reading | Tag |
|---|---|---|---|
| Tempo | Bar lag 2.554 s in every 20 s window, 0:20 to 3:50 = 93.96 to 94.01 BPM (rhythm colleague; the tracker's 95.7 in `audio_features/summary.json` is a coarse frame multiple) | the classic 85 to 100 BPM rap range; far steadier than a human drummer | measured, high for 94 |
| Kick placement | Kick IOIs after merging double triggers, in 16th steps at 94.0 BPM: 2 steps 72, 3 steps 107, 5 steps 36, 6 steps 37, 8 steps 33, one-beat (4 steps) only 3 of 298 (colleague, 0:30 to 3:35) | the kick avoids a four-on-the-floor or one-per-beat pulse; it moves in dotted-eighth steps (3+2+3+2), a tresillo-like cell | measured, medium; style reading INFERRED, medium |
| Kick sound | My measure on 408 kick-band peaks (30 to 150 Hz, 0:30 to 3:35): dominant frequency median about 70 Hz (p10 43 Hz), time to fall 20 dB median 0.18 s | a short, punchy kick, not a long 808 boom (808 kicks usually ring much longer) | measured, medium (the 0.08 s window gives only about 12 Hz resolution) |
| Hat or shaker comb | 851 onsets in 5 to 7.8 kHz over 0:30 to 3:35 (4.6 per second); IOI bins: under 0.06 s 34, 0.06 to 0.1 s 19, 0.13 to 0.2 s 436, 0.2 to 0.3 s 99, 0.3 to 0.5 s 189 | a steady sixteenth comb (0.16 s) with few fast rolls (about 6 per cent under 0.1 s). A trap hat part would show many triplet and 32nd rolls | measured, medium: not trap |
| Swing | Mid-band 16-step fold: even-eighth positions 0.46, on-beat 0.41, odd sixteenths 0.38 (relative units, `lineage_r1_b.py`); rhythm colleague gives off-beat eighth within 0.02 beat of straight | straight sixteenths, no 2:1 shuffle (not jazzy boom-bap swing, not a swung J Dilla-type feel) | measured, medium |
| Bass | pyin on bass stem 0:40 to 1:40: median 74 Hz, D2 (about 73 Hz) 60 per cent of voiced frames, D1 (37 Hz) 4 per cent, G1/G#1/D#2/F2 4 to 7 per cent each; 163 bass runs with median 0.12 s but p90 1.19 s and max 6.9 s; decay 0.6 s after peak: median -13 dB, quartiles -40 dB and -3.8 dB | two bass behaviours: short plucks and held flat notes. A clean low tone with its energy under 221 Hz (sound colleague, 95 per cent) | measured, medium; "808-style or synth" INFERRED, low-medium (instrument not recoverable) |
| Bass arrangement | Bass-on blocks restart every 10.0 to 10.3 s (colleague, 1:41.6, 1:51.8, 2:01.7, 2:11.9; 2:42.5, 2:52.8, 3:03.0, 3:13.2); at each drop only the bass stem falls (about -50 dB) while drums, voice and bed hold | arrangement by muting a loop track, a DAW or MPC-pad habit | measured, high; reading INFERRED, medium |
| Voice | Verse median 218 to 230 Hz (A#3), 94 to 98 per cent of voiced frames within 3 semitones of the median; hook median 403 to 410 Hz (G#4/A4) (voice colleague, my pyin agrees: verse 217 to 255 Hz p10 to p90) | near-monotone rap in the verses, a narrow chant in the hook: the standard rap-verse / sung-hook split | measured, high |
| CLAP | song-average genre: hip hop 0.78, country 0.08, R&B 0.06; instrument: drum machine 0.79, synthesizer 0.12 | agrees with all of the above, weak evidence on its own. The same file says "no vocals" 0.88 and "vinyl crackle" 0.80, which I reject: voices are plain in every stem, and I found no impulsive crackle (the file's floor above 8 kHz is a flat -80 dB with no spikes) | weak; flagged noise |

## 3. What the track is NOT (ruling out neighbouring lineages)

| Candidate | Why not, from the measurements | Tag |
|---|---|---|
| Sample-chop boom-bap (dusty-soul loop) | The bed has one root and fifth for 3:56 (D 118 s and Dm 82 s of 239 s in `chords.json`, 189 labels, colleague reading: unsettled third, third at about a quarter of the root strength). A chopped soul loop normally carries a chord progression. There is no separate narrow-band, crackly layer under a wider mix: every stem stops at the same ceiling near 8 kHz (colleague, `window_0100s.png`) | INFERRED, medium |
| Trap or drill | 94 BPM is outside the usual trap (about 130 to 150 or 65 to 75 half-time) and drill ranges; hat rolls are rare (above); bass is mostly short D2 plucks and flat holds, not long sliding 808 lines (a glide D2 to D3 is noted at 2:42 to 3:00 by the window note, a minor feature) | INFERRED, medium |
| G-funk or R&B-leaning | no melodic synth lead or sung harmony; hook is a thin chant on one fifth, CLAP R&B only 0.06 | INFERRED, medium-low |
| Live band or rock | Drums stay locked to 94.0 BPM within about 0.05 BPM across 23 windows (colleague); the whole track holds drums and bed with no change of feel. CLAP lists "country" 0.08 and "folk" 0.002: not evidence | INFERRED, medium |
| Old-school (early 1980s) rap | The mix is loud and limited (section 4), the voice is close and dry, the drum part is dense (about 6 onsets per second), the bass is a pitched sub | INFERRED, medium-low |

## 4. Production era (rule 1)

Judgement: **modern, home-style or independent production, delivered through a narrow-band mono chain; not an archive recording and not a modern track laid over old material.** INFERRED, confidence medium.

Figures:

- **Peak against 0 dBFS:** sample peak 1.0 (0.0 dBFS) measured on the mix (mine). The sound colleague counts 21,079 samples at or above 0.999 and 542 clipped runs, concentrated at 0:10 to 0:20 and 2:55 to 3:00 (colleague, measured high). Mix RMS holds -10.0 to -10.9 dBFS in 10 s blocks from 0:10 to 3:40 with crest factor about 10 to 11 dB (colleague). Hard peaks at 0 dBFS with a flat three-minute RMS plateau are what a modern limiter or loudness-maximised mixdown produces.
- **Loop regularity:** mel-spectrogram correlation at the bar lag (2.554 s) for the drums stem 0.85, at 5.1 s 0.85, at 10.2 s 0.84 (mine, 0 to 200 s). For the other (bed) stem 0.89 at the bar and 0.89 at 4 bars, and 0.94 at 61 s (about 24 bars). The bed is a near-static texture; the drums repeat strongly but not as a bit-exact copy (the rhythm colleague finds bar-to-bar envelope correlation median 0.72, with a repeat in waveform; carried as INFERRED, medium). A pure copy-paste loop would score nearer 0.99, so there is either variation in the pattern or in how the part is played or triggered.
- **Kick onset spread:** the kick chain fits a fixed 16th grid at 94.0 BPM with cumulative residual standard deviation 78 ms over about 185 s (a different tempo of 93.5 or 94.5 gives 282 to 307 ms; colleague, measured, high). The win_0000 note gives a 95 ms 8th-grid deviation for low-drum IOIs on the tracker's uncorrected phase, which is a phase-offset effect, not a spread figure I could confirm; I did not re-measure kick spread myself. So the hits are near-grid, like a sequencer with a small humanise offset, or played to a click. Not recoverable which.
- **Band-limit against full-band:** Welch spectrum of the mix (mine): -59.8 dB at 4 kHz, -55.3 at 6 kHz, -60.8 at 7.8 kHz, -61.5 at 8.0 kHz, -76.5 at 8.2 kHz, -80 dB at 9 kHz, -78.5 at 12 kHz, -83 at 16 kHz. A brick wall at 8 kHz, in the mix and in every stem. This is one ceiling over everything, so no layer is "older" than another; it is the delivery chain (INFERRED, medium; a 16 kHz-sampled or low-bitrate source is consistent, not proven).
- **Stereo:** L/R correlation 0.9988 on the whole file (mine); the sound colleague finds 8,666 of 10.56 million samples differing, i.e. dual mono. Mono delivery is common in old material and in downmixed uploads; here the loudness and clipping figures point to the second. Tag low for "downmix".
- **Pitch reference:** `librosa.estimate_tuning` gives +0.13 semitone (other stem) and +0.16 (mix), about 14 cents above A440 (A about 443.6 Hz). The bed's fundamental measures 148 Hz (sound colleague), against D3 146.8 Hz, which is +14 cents. A sampled source sped up a little, a detuned synth, or a loose tuning would all do this. Speculative, low.
- **Hook retuning:** in the three full hook passes 39 to 43 per cent of voiced frames lie within 15 cents of a semitone grid, and 33 to 35 per cent within 10 cents, against 28 to 32 and 19 to 22 per cent in the verses (uniform scatter would give 30 and 20). A hard retune effect would give above 80 per cent. So the sung hook is only slightly more pitch-stable than speech and **no hard auto-tune is measurable**. INFERRED, medium.

Net: peak and RMS figures say modern loudness handling; the near-grid kick says DAW or sequencer (or a click); no figure points to a period-consistent old recording.

## 5. Layer-by-layer lineage notes

**Drums.** Dense, dry, vertical hits; stem about -19 dB; 6 onsets per second. A kick-and-snare backbeat on 2 and 4 is the least certain part (rhythm colleague); the hat comb carries the sixteenth drive. Reads like a drum-machine or sampled-kit loop (CLAP drum machine 0.79, weak). Drum hit identity not recoverable.

**Bass.** Sub-bass on D, a root-only line (harmony colleague: no third). Bass is the loudest layer under the voice (-16 to -18 dB stem) and the main dynamic lever; its removal moves the mix by only 0 to 5 dB. That "bass in, bass out" device is a DAW arrangement habit and is also a mark of loop-based rap beats where a producer drops the 808 to open a hook or a verse.

**Bed.** A sustained harmonic stack on a 148 Hz fundamental with 12 or more evenly spaced partials (sound colleague), centroid 0.9 kHz, 95 per cent of energy under 1.8 kHz, flat level at -25 to -30 dB for the whole track. In `window_0060s.png` the "other" panel shows horizontal stripes between about 100 Hz and 1 kHz that never stop. It acts as a drone, the way a held organ, string or synth pad does in cinematic or "dark" rap beats, and the way a tanpura-like drone anchors modal music (metaphor for function, not an identification). The recurring Gm - G - F - (C or Am) - Dm side-step appears in pairs about 9 s apart, with the pairs about 60 s apart (colleague, 24 bars at 94 BPM): this is the one harmonic gesture and it keeps the track from being a pure one-chord vamp. D natural minor (F, C, Gm) is the best reading (colleague, INFERRED, medium-low).

**Voice, verses.** Near-monotone first-person narrative at 6.2 to 6.6 vocal-stem onsets per second, one four-beat line per bar, dense internal rhyme in the Whisper text ("daily / lady / blurry / hurry", 0:30 to 0:40), a comic-grotesque to darker arc across the three verses (hangover and a stranger in bed, road rage, street dealing; Whisper mix and vocals passes agree on the content, tag medium: the words are transcribed, not heard). This is the **storytelling-rap** tradition: the beat is a bed for a plot, the voice sits on top of the mix (verse vocal -16.4 to -16.7 dB against hook -20.4 to -21.1 dB). Resembles the tradition of narrative and comic-confessional rap more than of battle or braggadocio rap. INFERRED, medium; named scene or artist: not recoverable.

**Voice, hook.** A chanted, gated tune around A4 (the fifth of D) and G, F: a falling A-G-F cell, with a C#5 flick at the top of each pass (0:23, 1:24, 2:25, 3:26; harmony colleague). The hook is cut by 1.0 to 1.25 s vocal dropouts about 13 s in, with a 30 dB or greater fall in under 0.5 s (win_0000, win_0020 notes; voice colleague). The hook text, "You, you I see ... in my [carry/period/hair] and in the morning", is rendered three or four different ways by Whisper, so its precise words are uncertain; the repeated shape "you I see ... in the morning ... I see you" is legible (4 passes of about 20 s, low-medium). This is the pop-leaning **sung-hook-between-rap-verses** model (the "hip-pop" or rap-chorus tradition). The chopped, stuttered gaps resemble a DAW edit (gate, cut or mute), not a singer's breath. INFERRED, medium.

**Whole-song form.** Intro 0:00 to 0:10.4 (drums and bed, bass in gaps, no voice) / hook 0:10 to 0:30 / verse 0:30 to 1:11 / hook 1:11 to 1:31 / verse 1:31 to 2:12 / hook 2:12 to 2:32 / verse 2:32 to 3:13 / hook 3:13 to 3:35 / instrumental outro 3:35 to 3:56.4, then 2.8 s of digital zero. Hooks of 8 bars and verses of 16 bars at 94 BPM (voice and rhythm colleagues). This is the standard **verse-hook-verse pop-rap song form**, repeated without a bridge. No stop, no tempo change, no fill separable from the pattern (rhythm colleague).

## 6. Boundary evidence table (rule 3, mine, 1.4 s RMS windows before and after, dBFS)

| Boundary | Drums change | Bass change | Vocals change | Other change | Mix change | Which stem carries it |
|---|---|---|---|---|---|---|
| 0:10.4 hook 1 entry | -16.9 to -15.2 | -52.6 to -21.9 | -68.4 to -25.6 | -27.7 to -22.8 | -11.7 to -9.4 | vocals and bass together (the voice enters from residue); not a silence before it: drums and bed run from 0:00 |
| 0:30.4 verse 1 | -18.0 to -19.2 | -14.2 to -18.7 | -21.4 to -17.5 (register falls about 10 semitones) | -22.5 to -20.8 | -9.3 to -10.5 | vocals (register and level), not level of the rest |
| 1:11.3 hook 2 | -17.6 to -18.9 | -33.5 to -19.2 | -15.3 to -24.7 | -29.8 to -25.0 | -9.8 to -11.8 | vocals (register up, level down) with bass back in |
| 1:31.4 verse 2 | -18.1 to -19.9 | -14.6 to -18.3 | -21.0 to -16.0 | -22.6 to -21.4 | -9.3 to -10.0 | vocals |
| 2:12.0 hook 3 | -17.9 to -19.1 | -37.4 to -17.0 | -19.5 to -21.9 | -28.6 to -26.9 | -11.3 to -11.5 | bass (return) |
| 2:32.5 verse 3 | -17.8 to -18.8 | -15.0 to -19.8 | -20.7 to -17.2 | -23.3 to -22.1 | -9.4 to -10.5 | vocals (register) |
| 3:13.5 hook 4 | -17.2 to -19.5 | -26.7 to -25.0 | -16.9 to -31.4 | -27.5 to -25.2 | -10.1 to -13.3 | vocals (a line break, then the high register at 3:15.1 per colleague) |
| 3:35.3 voice leaves | -20.2 to -19.1 (3:35.5 grid) | -28.5 to -14.5 | -28.8 to -67.6 | -25.6 to -26.6 | -14.0 to -10.9 | vocals out, bass back in: a +3 dB lift, not a silence |
| 3:49.0 fade begins | -21.7 to -22.9 | -18.1 to -22.5 | -74.7 to -74.9 | -28.1 to -31.7 | -14.0 to -16.8 | bass and bed fall together |

Every boundary shows in one or two stems only; no boundary shows in all four. The rhythm section (drums plus bass) never drops out together. The only dips that I would call "gaps" are bass-only and, in the hook, vocals-only, each with drums running (details in colleague tables; mix falls of 0 to 5 dB).

## 7. End of track (rule 4)

From a 10 ms RMS envelope over the last 8 s of `audio/song.wav`: the mix stays around -15 to -20 dBFS in the 10 ms envelope until about 3:53.4, then falls to -44 dBFS at about 3:55.9 and -60 dBFS at 3:56.44; the last frame above -70 dB is 3:56.52, above -80 dB 3:56.56, above -90 dB 3:56.67. After that the envelope is -180 dBFS (digital zero) for the rest of the file (about 2.8 s). **Last audible sound: 3:56.44 (above -60 dBFS); level at the end: below -90 dBFS from 3:56.67 then zero.** The last 3 s of the audio (3:56.44 to 3:59.44) therefore hold only the final 0.2 s of a tail and then digital silence. Per-stem levels over the last 3 s: vocals max -78.3, drums max -66.6, bass max -69.0, other max -76.2 dBFS (stem-separation residue; the stems carry a constant floor to the file end, the mix does not). In the 10 ms envelope the final sounds are a diminishing series of low hits (peaks at 3:55.96 about -44 dB, 3:56.33 about -50.5 dB, 3:56.36 about -49.6 dB, 3:56.44 about -56.8 dB, 3:56.48 about -60 dB), counted on the envelope, not on the stems. This is a **fade-out of the whole loop over about 5 s**, not a final hit; whether the fade is the producer's or the delivery chain's is not recoverable.

## 8. What a listener might hear as lineage (and my confidence)

- "Boom-bap": tempo, kick spacing and narrative rap say yes; sample-chop texture says no. INFERRED, medium on tempo/vocal tradition, medium on no sample-chop.
- "Trap-influenced": sub-bass on D1/D2 and the muted-bass arrangement lean that way; hat rolls and tempo do not. Hybrid, low-medium.
- "Mixtape or internet-era DIY rap": mono, 8 kHz ceiling, hard clipping at the loudest events (voice, bass and crash arriving together at 0:10.4: runs of about 1,000 samples, 23 to 26 ms; colleague), uniformly loud mix. INFERRED, medium. A dating to a decade is not claimed.
- "Cinematic or horror-leaning dark rap": the minor D-A drone and the Gm-F side-step make it sound dark, but the tempo is mid and the voice is conversational, which pulls it toward comic storytelling. Low.
- "Pop-rap hook": the chanted A4 hook repeated four times, dry and chopped. Medium.

## 9. Disagreements and carried tags

- I carry the rhythm colleague's 94 BPM over the tracker's 95.7 (the tracker label stays in `audio_features/summary.json` and in several window notes). My own bass-run interval check (10.0 to 10.3 s per four bars) is consistent with 94 to 96; I did not re-derive the grid, so the 94 figure stays measured, high as tagged by the rhythm colleague.
- Sound colleague's "brick wall at 8 kHz" confirmed by my Welch figures (-61.5 dB at 8.0 kHz to -76.5 dB at 8.2 kHz). Their "dual mono" is consistent with my L/R correlation of 0.9988 (not 1.0, because of the isolated glitch samples).
- The hook-voice and chord tags are taken unchanged from the voice and harmony colleagues.
- CLAP "no vocals 0.875" and "vinyl crackle 0.80" are rejected for the reasons in section 2; CLAP "hip hop" and "drum machine" are kept as weak support.

## 10. Three questions for fellow specialists

1. **Rhythm:** the hat band shows only about 6 per cent of onsets under 0.1 s, but at 94 BPM a 16th comb can also read as a half-time 32nd grid. Can you say whether any section (for example the 2:55 to 3:00 clipped stretch) carries true rolls or triplets, so that I can rule trap hat technique in or out?
2. **Sound:** the 8 kHz wall and the +14 cent tuning offset (A about 443.6 Hz) could both come from the delivery chain or from a sped-up, low-sample-rate source. Is there any measurement (aliasing near 8 kHz, resampling images, pre-echo) that tells a 16 kHz-sampled origin from a lowpass added at mastering?
3. **Voice:** is the hook's chopped, gated delivery (30 dB or more falls in under 0.5 s at the same bar position each pass) a vocal edit, a gate, or a side-chained mute, and does the vocal phrase timing against the bar grid say anything about a producer's hand rather than a performer's breath?

## Not recoverable by measurement

- **Instrument identity** of the bed (synth, organ, guitar, strings, sample): only a 148 Hz harmonic series is visible.
- **Whether the drums are sampled, programmed or played:** near-grid timing and the bar-level repeat fit a sequencer, but cannot discriminate a click-tracked drummer or a looped sample.
- **Whether the bed or any layer is a sample from older music, and where it came from:** no band-limited or noisy older layer is separable, and a sample that was processed together with the rest would not show one.
- **Recording date, location or scene:** nothing in the audio fixes a year or a place; the lyric words are Whisper output, uncertain, and the transcript's "Thanks for watching!" at 3:56.26 is an obvious artefact over a silent tail.
- **Performer, intent, and whether the tuning offset (+14 cents) is deliberate:** a pitch figure cannot show a choice.
- **Whether the hook gaps and the bass mutes are edits or live performance:** the level drop shows, the cause does not.
- **The true meaning of the words, or how a listener "feels" the story:** only a transcript with unknown errors exists.
