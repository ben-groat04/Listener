# video1: FORM and dynamics specialist, round 3 (blind, measurements only)

Evidence key: LV = per_second_levels.json; MVxxx = music_views windows; CH = chords.json. Scripts: `v1/scripts/agents/video1_form_r2.py` (edge timing, 256-sample RMS), `v1/scripts/agents/form_r3.py` (kick-band onset grid fit, run this round). Read: all seven round-2 files. Round-3 files from the others were mostly unfinished when I looked (rhythm.md empty), so I answer round-2 questions only.

## 1. Questions put to me

**Rhythm: do you accept bar spacings of 3, 4, 7, 3, 5, 8, 3, or are the true edges a beat out? Is the 1:48-1:55 swell a fill or a section?**
- Partly accepted. My own edge times (bass and "other" RMS, not the tracker) give gaps in beats (0.769 s each): 1:15.1 to 1:26.7 = 15.1; 1:26.7 to 1:40.0 = 17.3; 1:40.0 to 2:13.5 = 43.6; 2:13.5 to 2:38.5 = 32.5. In bars: 3.8, 4.3, 10.9, 8.1. So the 4 + 4 pair and the 8-bar 2:13-2:38 span agree with yours (high), and the long stretch 1:40-2:13 is about 11 bars, which is your 7 + 3 + 5 folded together by the 1:49 and 1:59 edges (those two are weak edges; see below).
- The odd counts (3, 5, 7) come from the weak edges, not from true 3-bar blocks. 1:49.4 and 1:58.7 are changes of drums and "other", not of bass or voice, and they are the ones I rank lowest. I therefore read the odd spacings as tracker edges being placed on "something changed" rather than "a block began" (medium). The one clean odd block that survives is 2:38.5 to 2:47.0 (about 3 bars), which both of us measure (medium-high).
- Phase: I tested the grid myself. Fitting a 16-slot cycle to kick-band onsets (0:30-2:45, residual 0.045 slot) gives a clean grid, but the kick counts per slot are almost flat across the four beats (41, 40, 45, 39) so the drums alone **do not reveal which beat is bar-one**. Section edges against that grid land at beat-in-bar 0.2-1.2, a spread of about 1 beat (1:15.3 = 0.91, 1:27.4 = 0.64, 1:40.0 = 1.02, 2:13.4 = 0.43, 2:38.4 = 0.93, 2:47.8 = 1.15). So edges are beat-locked (all within about a beat of a common phase) but not tightly bar-locked on my timings; your tighter 2.0 +/- 0.1 uses tracker times and I cannot confirm that precision (medium). Overall: **whole-beat construction, high; four- and eight-bar units where edges are strong, medium; true downbeat, unknown.**
- 1:48-1:55: drums rise from about -20 to -14 dB (LV drums 1:48 to 1:54), the mix peaks at -9.5 dB (1:52), then the bass drops out at 1:55 (-20 to -62 dB by 1:56) and "other" falls 12 dB by 1:58. It is a **swell that ends the peak**, a build into a strip, so I call it a fill-like "lift and drop" inside the peak section rather than a section of its own (medium). It is only about 7 s (3 bars), too short to be a block, but it is the only place the drums add energy of their own.

**Sound: nothing put to me directly.** I accept Sound's 2:13 "body added" versus 1:27 "top added" split, and now use it in the map below.

**Feeling (to Form, round 2): is the 1:52 peak more tense than the final plateau?** Level says the peak is louder (mix -9.5 dB at 1:52 against about -11.7 at 2:50) but the finale is wider (0.7+ against 0.4-0.6). Harmony finds D5 with b7 shadow in both pedals, no extra tension in the 1:40 peak. So the peak is *heavier*, the finale is *bigger and open*: not rest after tension but a second, different kind of climax (medium).

## 2. Corrections

- **Withdrawn**: round 2's claim of "whole bars" was too strong for my own timings; it is whole beats, and bars only at the strong edges (see above).
- **Accepted from Harmony**: 2:38 is also a tonal event (pitched D2 bass replaces the unpitched sub); the sub at 42.6 Hz is not a sounded chord tone, so my "heartbeat with no pitch change" wording stays.
- **Accepted from Voice**: 2:48 is an edit point and the closing gesture breaks, not ends. Harmony adds that the stop at 3:08.7 is not a cadence (tonic still strongest): the track ends mid-pedal.
- **Corrected**: 1:40-2:13 is one stretch of about 11 bars with a lift and a strip inside it, not three sections.

## 3. Connections

- Rhythm serves form by never changing: identical drum cell across the bass-less 1:15-1:48 (similarity 0.85), so subtraction is done only by bass, "other", width and the voice.
- Harmony serves form by standing still: the pedal gives bass and spectrum the whole job.
- Voice marks the form: speech only in low-energy states; exits at 0:32, 1:27, 2:48 each followed by a gain.
- Sound gives the felt kinds of edge: removal (1:15), opening (1:27), impact (1:40), filling-out (2:13), re-lock (2:38).

## 4. Final map (high on order, medium on bar counts, edges about +/-1 s)

0:00-0:09 intro build; 0:09-0:32 spoken statement; 0:32-1:15 voice-free plateau and slow build (peak at 0:58, mix -10.3); 1:15-1:27 collapse, bass out (4 bars); 1:27-1:40 bright bassless wall (4 bars); 1:40-1:55 bass slam and peak (bass +35 dB in about 1 s; loudest second 1:52); 1:55-2:13 thin trough with gated sub; 2:13-2:38 narration, moving chords (8 bars); 2:38-2:47 re-lock and last words (about 3 bars); 2:47-2:48 one-bar breath; 2:48-3:08 wide wall to a hard stop.

## 5. Settled conclusions

- **Built by layers, not by drums or harmony:** the drum cell and the D pedal barely move, so bass, "other" spectrum, width and voice make every edge; strong edges are 1:15, 1:27, 1:40, 2:13, 2:48 (high).
- **Subtract-then-slam is the engine:** bass out at 1:15, brightness in at 1:27, bass back at 1:40 is the biggest step (bass +35 dB); weight and brightness are never both on until 2:48 (high).
- **Two climaxes of different kinds:** 1:40-1:55 is the loudest and heaviest; 2:48-3:08 is the widest, brightest and longest, voice-free (medium).
- **Timing is whole-beat; bar units appear where edges are strong** (4 + 4 and 8 bars); odd 3/5/7 counts mostly reflect weak edges; true downbeat cannot be set from the drums (medium).
- **The ending is two gestures:** a one-bar breath (2:47.0-2:48.2) that resets, and a hard stop at 3:08.7 with no cadence, so it lands as abrupt and unresolved (medium-high).

## 6. Limits

No self-similarity test of note-level repeats; stem names are demucs labels; bar grid assumes 4/4 from Rhythm; I could not read Rhythm's round-3 file.
