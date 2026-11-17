# t_birdwalk: the music (blind-mode ears report)

Method: inferred from audio_features, stems, spectrogram, music_views (chords, lead notes), whisper transcripts and my own librosa measurements (helper scripts `v1/scripts/agents/birdwalk_music_measure.py` and `..._measure2.py`; outputs in `v1/data/t_birdwalk/audio_features/extra/`). I cannot play audio. Confidence is marked High / Medium / Low. Context.md, other analyses and the web were not used.

## 1. Snapshot

- **Genre (Medium-High):** modern trap-flavoured hip-hop / club rap, dance-novelty record. Evidence: a long sub-bass at about 55 Hz (A1) carrying about 35-40% of spectral energy in "full" sections, sparse low-heavy drums with hi-hat energy above 5 kHz in some sections, rapped/chanted vocals with ad-libs ("Aye", "ey"), and lyrics about a dance, clubs, money and trainers. No automatic genre tagger was used.
- **Tempo (High for the number, Medium for the feel):** the beat tracker gives 152.0 BPM, with a beat interval median of 0.394 s and standard deviation 0.024 s (steady, not human-drifting, so almost certainly programmed). Autocorrelation of onsets also has a strong peak at 79.5 BPM, which is the half-time octave. Trap is usually felt at about 76 BPM half-time with hi-hats running at 152 or double, so I read it as "76 felt, 152 counted". The local-tempo plot jumping to 100-110 or 80 is octave/tracking noise, not real tempo changes (High).
- **Key (Medium):** A minor. Whole-song estimate A minor 0.50 vs A major 0.47. Chroma in every section is dominated by A, then A#/G#/B/G. The bass stem sits on A1 (55.0 Hz) with a secondary A#1 (58.3 Hz) throughout the song. Chord detector shares: Am 40%, A 20%, F#m 10%, F 5.5%, D 3.6%, "no chord" 48% of the time. The major/minor ambiguity is probably because the sub-bass note is a bare root with little third (Medium). A#1 next to A1 could be a flat-second (Phrygian) colour or a pitch glide on the 808 (Low); I cannot separate those.
- **Dynamics (High):** loud sections about 0.22-0.25 RMS, quiet sections about 0.11-0.12. Dynamic range (p95-p5 of per-second dB) is only 9 dB, so it is heavily compressed and "block-like", not gradual.
- **Duration:** 3:08 (188 s).

## 2. Instrumentation (with evidence)

1. **808-style sub-bass / bass drone (High that it exists, Medium on type).** The spectrogram shows a hard-edged bright band at roughly 40-64 Hz that switches on and off in blocks. In the bass stem, the notes are A1 (55 Hz), long and decaying, with sharp attack transients. Sub-20-60 Hz energy fraction jumps from 1-6% in "quiet" sections to 35-41% in "full" sections. Stereo side/mid ratio falls to 0.02-0.15 in those full sections (bass is centred and the mix narrows).
2. **Drums (High for presence, Medium for sound).** Drum stem onset rates by section: 0.8 per s (intro), 1.9 (0:13-0:47), 0.7, 2.8 (1:00-1:34), 3.9 (1:34-2:00), 0.8, 2.7, 0.1 (2:23-2:36), 3.3 (2:36-end). In 1:00-1:30 the drum stem is bright (15% of energy above 5 kHz), which suggests hi-hats/claps; in 1:38-1:58 and 2:12-2:22 it is 84-93% below 200 Hz, i.e. mostly the sub-kick/808 (the separation has put the sub into "drums" there). Sharp wideband transients in the 0:20-0:40 view (spaced at about the beat) read as claps/snares/hi-hat hits.
3. **Rap vocals (High).** The vocals stem has a clear voiced harmonic structure (formant-like bands in the music_views), loud from the start (0:03) to 2:47, then nothing (RMS 0.000 from 2:48; a small blip at 2:57-2:59). There is also a held, sliding vocal at about 0:27 (the "Wow" ad-lib in the transcript) and a downward glide near 1:55-1:59 in the vocal and "other" stems (Medium: this may be a vocal effect or a synth sweep).
4. **"Other" layer (Medium-Low):** mid-register content near 0.9-1 kHz plus short stabs, present in all sections at low level (RMS 0.01-0.1) and strongest in the build near 1:50 (up to about 0.10) and 2:50 area. I cannot identify the timbre (synth pluck / sample). The lead-note tracker is noisy (range C#2-C#5) so I do not trust it for melody. There is no sign of guitar or live drum kit: the sound is clean, low-heavy and grid-locked.
5. **Band limit:** nothing above about 5.5 kHz in the spectrogram (air band fraction about 0.0). This points to a lossy / low-bitrate source (e.g. MP3 or web-video audio at a cutoff) rather than the music being dull (Medium-High). Treat "brightness" features with this in mind.
6. **Stereo (Medium):** left/right correlation 0.89 overall; the mix is fairly narrow. Quiet sections are wider (side/mid 0.48-0.55) than loud ones (0.02-0.3), which means the intro/verse-lite sections have wider elements (samples, ad-libs) and the big sections are driven by centre sub-bass and vocal.

## 3. Structure map

Block pattern is set by the bass and sub: it is either "in" (full, loud) or "out" (thin, harmonic mid-range). Section boundaries (auto sections, snapped to the sub on/off in the spectrogram):

| Time | Section (my label) | Evidence | Conf. |
|---|---|---|---|
| 0:00-0:13 | **Intro**, no sub-bass; spoken/ad-libbed vocal, sparse drums | RMS 0.11; sub 1%; perc/harm 0.95; vocals from 0:03; mix transcript: "Aye, man, we got this new dance... watch me do that bird walk" | High |
| 0:13-0:47 | **Verse 1** with sub-bass in; the first beat drop at 0:13 | RMS 0.23-0.25, sub 35%; bass stem jumps from 0 to 0.15-0.2 at 0:13; vocals 0.1-0.2 | High |
| 0:47-1:00 | **Breakdown / hook, bass out** | RMS 0.11; sub 5%; vocals continue, drums sparse (0.7 onsets/s); bass stem drops to 0 at 0:48 | High |
| 1:00-1:10 | **Hook, bass back in** ("that bird walk" repeated) | whisper (vocals stem) 1:00-1:10 chant; bass stem returns at 1:00 at 0.17-0.23 | High |
| 1:10-1:34 | **Verse 2** ("I step up in the pub...") | RMS 0.23; hi-hat bright drums; vocals 0.07-0.12 | High |
| 1:34-1:59 | **Verse 2 continued / build: drums loud, bass stem thins and drums stem carries the sub** | drum stem rises to 0.15-0.21 at 1:39-1:52; the 1:40-2:00 view shows tight, dense kicks; the lines "show you what it do... so icy, so nice, so whitey" | Medium |
| 1:59-2:12 | **Breakdown 2, sub out** | RMS 0.11-0.12, sub 4%, vocals 0.09-0.12 | High |
| 2:12-2:23 | **Drop 3, short, sub back** | RMS 0.23, sub 39%; bass stem jumps at 2:12 | High |
| 2:23-2:36 | **Stripped section**: almost no drums (0.08 onsets/s), no sub | RMS 0.13; bass, drums stems near zero at 2:24-2:35; vocals continue at about 0.1; vocals-stem transcript has "burr-wop" (probably "bird walk") at 2:28-2:39 | High |
| 2:36-2:47 | **Final drop**, full band + vocals | RMS about 0.19, bass 0.19 steady; the vocal ends at 2:47 | High |
| 2:48-3:08 | **Outro**: instrumental, decaying | vocals 0; bass/drums/other decay to zero by about 3:07; loudness quietest at the end (fades). A brief rise in drums near 2:55-2:59 | High |

The "auto labels" in `summary.json` call 0:13-0:47, 1:00-1:23 and 1:34-1:59 type C, which agrees with my reading of them as the same "full" sound; my sub-bass on/off table matches the boundaries to within about 1 s (High). The sub-bass hard edges are at 0:13, 0:47, 1:00, 1:59, 2:12, 2:23, 2:36 (from the spectrogram band).

Caveat on 1:23-1:34 ("E" in auto labels): I see no clear change in the sub-bass there, only a slightly darker, vocal-forward texture (Low confidence that it is a separate section).

## 4. Emotional arc (INTERPRETATION)

- **0:00-0:13 casual introduction (Medium):** a friend's "Aye, man, we got this new dance" voice over a thin beat. It sets a playful, boasting tone. The sub is held back so that its entrance is a lift.
- **0:13 first lift (High as an event, Medium as feeling):** a sudden 2.2x rise in loudness and a bass the listener feels in the chest. Strongest "club" moment.
- **0:47 and 1:59 pull-outs (High as events):** the bass is deliberately removed in blocks for 12-13 s. Their function is to reset and make the return at 1:00 and 2:12 feel bigger. The energy never builds slowly; it alternates between two states, like a switch. This gives a bouncy, repetitive, trance-like loop rather than an emotional narrative.
- **1:34-1:59 peak intensity (Medium):** the highest drum activity (3.9 onsets/s) and the lyric "show you what it do... so icy, so nice" make this the most urgent stretch.
- **2:23-2:36 near-silence in the beat (High as event):** the hush before the last drop is the one real "breath" in the song.
- **2:48-3:08 comedown (Medium):** the voice leaves, the groove decays; it ends by fading, not on a hit.
- **Overall mood (Medium):** confident, cheeky, party-ready, with a minor-key undertone (A minor) that gives swagger rather than sadness. Nothing in the audio suggests melancholy.

## 5. How the music frames the words

- **The hook is a repeated chant (High):** "watch me do that bird walk" recurs at 0:00-0:07 (intro), about 0:42-1:07 (mix transcript), 1:00-1:10 (vocals stem) and 2:19-2:45. In the mix transcript it shows up at about 0:46-0:55 with "Imma show you how it go, do that bird walk" repeated, and in the final stretch it is the only line. Repeating one phrase against the changing bass state is the main way the song makes it stick.
- **The bass-out blocks are where the words are most exposed (High):** at 0:47-1:00 and 1:59-2:12 the vocal sits on a thin, mid-range bed, so the listener hears the voice and the hook without the weight underneath.
- **Verse delivery (Medium):** whisper timestamps put one line every about 3 s in 1:10-1:52; at 152 BPM a 4-beat bar is 1.58 s, so a line is about two bars (Medium), consistent with a half-time rap flow. Rhymes are playful and simple ("birthday / worst day", "bummy / gummy / dummy"). Lyrics are about fashion (white trainers, "nutty buddies on your feet"), money and a taunting of "haters". The mood is boastful and humorous (Interpretation).
- **Transcript caveats:** whisper on the mix and on the vocals stem disagree in places (e.g. "bank" vs "back", "worst day" vs "birthday", "dummy / gummy / bummy"). The mix transcript's run of "whitey, whitey, ..." from 1:51-2:19 is a Whisper repetition loop (hallucination) and should be ignored; the true content there is the "so icy, so nice, so whitey" line and probably the chanted hook. "3-2-1 cider with goalie" at 0:08-0:28 is unintelligible. "burr-wop" at 2:28 is likely "bird walk" (Medium; my correction by judgement). There is no vocals-stem transcript for 0:00-1:00 or 1:56-2:28, even though the vocal stem has plenty of energy, which means the voice is probably heavily processed, chopped or chanted there (Low).

## 6. Moments a listener would remember

1. **0:13**, the sub-bass hits and the whole record doubles in loudness (High).
2. **0:27-0:28**, the long sliding "Wow" ad-lib in the vocals stem, the only sustained pitched vocal moment in the verse (Medium).
3. **0:47-1:00**, the bass vanishes; the hook rides alone; then **1:00** the bass crashes back (High).
4. **1:39-1:58**, drum-heavy peak, "show you what it do", ends with a sliding sweep at about 1:56-1:59 (Medium) into the second bass-out at **1:59**.
5. **2:23-2:36**, near-bare beat, the song's quietest groove moment before the final drop at **2:36** (High).
6. **2:48**, the voice stops abruptly and the track decays over 20 s (High).

## 7. Relation to the picture (music's side only)

Sync data (not my analysis, quoted): 51 cuts; only 21.6% of cuts fall within 80 ms of a beat against about 42% expected by chance, so the editing is not beat-locked (High as a measurement). Loudness-cut-rate correlation is weak (r about 0.27). The big music events (0:13, 0:47, 1:00, 1:59, 2:12, 2:36) therefore are mostly not marked by cuts: a cut lands exactly on the 59.8 s boundary and within 0.5 s of 47.5 s, but others are 0.6-3 s away. Visual colour warmth rises with loudness (r 0.25-0.38), so loud sections might look warmer (Low). Check this in the picture reports.

## 8. Open uncertainties

- Whether the sub-bass pitch is a fixed A or glides to A# (stem shows A1 with A#1 secondary).
- Exact bar-level structure (I gave sections, not bars; beats are regular at 0.394 s so bars of 4 beats are 1.58 s).
- Vocal content in 0:00-1:00 and the 2:00-2:48 chant is only partly transcribed.
- The role of the 1:23-1:34 "E" auto section.
- Whether the 5.5 kHz band limit is in the source file or from extraction.
