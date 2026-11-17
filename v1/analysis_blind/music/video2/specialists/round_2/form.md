# video2: FORM specialist, round 2 (blind, measurements only)

Evidence keys: [R1-x] round-1 notes of specialist x; [R2-x] round-2 notes already written (harmony, rhythm, sound); [BAR] my new script v1/scripts/agents/form_r2b_video2.py (kick-band phase, bar arithmetic, "other" 4-10 kHz and vocal level per 4-8 s); [LVL] per_second_levels.json; [CH] chords.json. Times m:ss. I cannot hear; everything is inference from measurements.

## 1. What I changed my mind about, in one paragraph

Round 1 left the metre unsettled (I used the tracker's 0.372 s and was unsure whether 1:28.6 was a "tempo drop"). Rhythm and harmony have since shown 120 BPM, 2 s bars, one bass root per 2 bars. Counting in bars exposes a much tighter structure than I drew: **from the 1:28.6 drop onwards, every boundary I had marked falls on a whole bar of one lattice, and the sections are built from 6-bar (12 s) units.** The form is not a loose "slow burn"; it is a short, strict machine of repeated blocks, with the drama coming from what is added or taken out at block edges. Confidence: high on the arithmetic, medium on the labels I attach to it.

## 2. New measurement: the bar lattice [BAR]

- Kick-band beat phase (0.5 s grid) is 0.441 s in 0:30-1:00 (coherence only 0.28, a skipping kick) and **0.103-0.108 s in 1:30-2:30, 2:40-3:35, 3:40-4:35 and 4:40-4:58 (coherence 0.79-0.85)**. One lattice, 120.0 BPM, from the drop to the end. That confirms [R2-rhythm]: same pulse, different pattern, and a lattice offset between the first and second halves of 0.47 s (one beat, to within 0.03 s).
- Taking the post-drop lattice (bar 0 = 1:28.61), the events I had already chosen from level and layer data land as follows (bars after the drop):

| Event | Time | Bars after 1:28.61 |
|---|---|---|
| bass +10 dB step | 1:40.6 (my 1:40) | **6.0** (I measured the ramp at 1:39-1:41) |
| speech ends, "other" +5 dB | 1:56.5 | **14.0** |
| voice/other thin out, fill | 2:36.5 | **34.0** |
| "other" gear-change fill ends | 2:48.6 | **40.0** (fill 2:48.0-2:48.7) |
| voice returns (chops) | 3:28.7 | **60.0** |
| dense-voice / top of loop B | 3:36.6-3:37.2 | **64.0-64.2** |
| step-down, bass hole | 4:36.6-4:37.3 | **94.0-94.3** |
| bass goes sparse | 4:48.4 | **99.9 (100)** |
| stop of the rhythm section | 5:00.86 | 106.1 (a quaver after bar 106) |
| middle one of the three last hits | 5:02.60 | **107.0** |

  Nine of ten land within 0.3 bars, most within 0.05 bars (0.1 s). By chance one would expect a uniform spread, so this is strong. Before the drop, the old lattice (bar 0 = 0:28.14) fits too: 1:10.0 is bar 21 (21.0 - 0.0 exactly: 42 s after 0:28.0), and 1:24.5 is 28.25 bars. Both pre-drop stops sit on the first-half lattice.
- **The 1:24-1:28.6 hole is where the lattice shifts.** 0:28.1 to 1:24 = 56 s = 28 bars = two complete 14-bar passes of the E-G-D-E-G-D-B loop [R2-harmony: 28 s loop]; the hole (1:24.5-1:28.0 drums gone, bass gone) then runs 2 bars plus one beat to the new downbeat at 1:28.61. In other words **the hole is two bars of rest plus a one-beat "extra" that re-barres the whole piece by a beat** (the 0:28 start, 1:28.0 on the old lattice, is where drums and the mix first jump; the stable kick downbeat is 0.6 s later). This resolves rhythm's "re-phase" doubt [R2-rhythm 2.1]: it is a re-barring, but its seat is the hole, not the groove. Medium confidence (rests on phase estimates of a skipping vs a four-on-the-floor kick, as rhythm warns); I would not hang any big claim on it.

## 3. Revised song map in bars (replaces my round-1 table; times same, adds bar counts)

| Section | Time | Bars | Content |
|---|---|---|---|
| Intro | 0:00-0:28 | 14 | Pad and long tolls on a 2-bar clock (tolls at 8, 12, 20, 24 s [R1-rhythm]); G and Em colours in pad [R1-harmony] |
| Setup (narrated groove) | 0:28-1:28.6 | 30.2 | two 14-bar passes of the 7-chord loop, speech inside; drums stop 1:10-1:16.5 (3.25 bars) and 1:24.5-1:28 (the hole) |
| Drop stage 1 | 1:28.6-1:40.6 | **6** | full band, light bass |
| Drop stage 2 | 1:40.6-2:36.6 | **28** (bars 6-34) | bass +10 dB; speech 1:49-1:56 and 2:25-2:36; instrumental 1:57-2:25; loop A remainder |
| Loop-B "home" | 2:36.6-3:28.6 | **26** (bars 34-60) | B-A-D cycles, no voice; gear-change at 2:47-2:50; top band starts to rise |
| Voice returns / ramp | 3:28.6-3:36.6 | **4** | sparse chops, vocal stem -59 dB (3:28 8 s mean) |
| Peak plateau | 3:36.6-4:36.6 | **30** (= five 6-bar cycles) | dense chops (vocal stem -43 to -40 dB), brightness completed by 3:48 |
| Outro stage 1 | 4:36.6-4:48.6 | **6** | bass thins to a hole, mix -2 to -3 dB |
| Outro stage 2 | 4:48.6-5:00.6 | **6** | bass one stab per bar, chop one word per bar [R2-rhythm] |
| Stop and last hits | 5:00.6-5:03 | 1-2 | rest then three hits centred on bar 107 |

The outro is **exactly two 6-bar blocks (12 + 12 s = 24 s)** and the plateau exactly five of them. The 6-bar cycle (12 s: B, A, D bass blocks [R1-harmony]) is therefore the form's atom from 2:36.6 onwards. Drop stages 1 and 2 are 6 + 28 bars; the first is also one 6-bar block.

## 4. Answers to questions put to me

**Rhythm Q3: do my boundaries fall on whole bars from 0:00.14, and does the 16 s / 8 s fill spacing match my phrase map? (high on the bar arithmetic.)** Not from 0:00.14: the lattice after the drop is a beat away from the first-half lattice (section 2), so the whole bars I get are counted from **1:28.61** (second half) and **0:28.14** (first half). On that basis: yes. Fills at 2:08, 2:24, 2:36.5 sit at bars 19.7, 27.7 and 34.0 after the drop; the first two are on the *last beat* of a bar (x.7 = bar end), i.e. the fill occupies the final beats, as fills should. The gaps 16 s and 12 s (8 and 6 bars) fit my phrase map; 2:48.6 to 2:56.8 is 4 bars. The phrase default is 8 bars early (1:28.6 to 2:08 is 20 bars, with 1:56.5 at 14) and 6 bars late. I agree with the 8-bar working rule for the middle only as an approximation: the mixing unit is 6 bars (12 s) for the B-A-D loop and 14 bars (28 s) for E-G-D-E-G-D-B.

**Feeling Q (is 1:40 as important a boundary as 1:28.6; does 4:48 begin a distinct outro?).** On 1:40, partly: the bass stem step (+10 dB) is larger than any other stem step in the first half, but the mix step at 1:40 (3.5 dB) is smaller than at 1:28 (5 dB) and it happens exactly 6 bars after, i.e. it is the next 6-bar block of the **same** drop. So I demote it from "boundary" to "second stage of the drop" (as in my table): the listener hears an arrival at 1:28.6 and a thickening at 1:40.6. On 4:48: the outro really starts at **4:36.6** (the mix steps down 2-3 dB and the bass hole opens, [LVL]); 4:48.6 is its second stage, the point where the bass becomes one stab per bar. The outro is therefore 4:36.6-5:00.6, not 4:48-5:00. This amends round 1 (where I listed 4:37-4:48 "pull-back" and 4:40-5:00 "chop loop" as overlapping rows). High on levels.

**Voice Q3 (do 2:36 and 3:28 end and start sections; is 1:28.6 the first main drop the speech prepared?).** Yes to both ends of the 52 s silence: 2:36.6 is bar 34 (loop switch from E-G-D to B-A-D [R2-harmony] and the last speech block ends), and 3:28.6 is bar 60 (first chops). 3:28.6 sits mid-cycle of the 12-s B-A-D loop (cycles start 3:24 and 3:36 [R2-harmony: B at 3:24]) so it is a pickup, and **the real section edge is 3:36.6** when the loop restarts, voice becomes dense, and the mix reaches -10.9 dBFS. Whether the speech "prepares" 1:28.6: the last speech block before the drop is 1:20-1:28.5, the voice is cut at the same instant as the drums return (vocals -34 dB at 1:28, -74 at 1:29, [R1-form]); the same trick (speech ends, band moves) occurs at 1:56.5 (bar 14) and 2:36.5 (bar 34). So speech blocks end on **block edges of the drop** (bars 0, 14, 34), a form role independent of their words. Medium-high.

**Sound Q1 (should a section start at about 3:30; does the 8-bar grid say 3:32 or 3:36?).** My own measurement of the "other" 4-10 kHz band in 4 s means [BAR] gives -11 (2:50), -6 (3:02), -2.3 (3:18), +2.4 (3:22), +4 (3:30), +10 (3:38), +13 (3:46), **+18 (3:50), then flat +19 to +20 to 4:06**. So it is a continuous ramp of about 30 dB from 2:50 to 3:50 with its steepest part 3:22-3:50, finishing at **3:48.6 (bar 70, the sixth loop-B cycle start counting from 2:36.6)**. It does not step at 3:30. The section edge is 3:36.6 (voice density, loop restart); the brightness ramp then continues for two more 6-bar blocks (3:36.6-3:48.6 with voice, finishing as the plateau begins) and it is complete by 3:48.6. Neither 3:32 nor 3:36 on an 8-bar grid; on the 6-bar grid it is 3:36.6 (start) and 3:48.6 (completed). I accept your finding that the brightness ramp is the largest change of the late half; I place its **completion**, not its start, as the form event. This also tells the form: the peak is built over about 78 s (2:28 to 3:48) and is felt as arrival at 3:36-3:48.

**Lineage Q (do 4 s chord blocks and 8 s intro gaps support 8-bar phrases; is 5:04 a planned cut or a truncated loop?).** The intro tolls (8, 12, 20, 24 s) sit on the 2 s-bar clock but the intro (14 bars) is not eight or sixteen bars; the 28 s loop is 14 bars, the later cycle 6. **No 8-bar phrase is demanded by the data**; 14 and 6 are unusual numbers (14 = 2 x 7 chords of 2 bars). Ending: planned, not a loop truncation. The stop (5:00.6) is on bar 106 (within a quaver) and the central last hit (5:02.60) on bar 107, with the two flanking hits a quaver either side [R2-rhythm, BAR]; a truncated loop would not centre a hit on the lattice. The digital silence from 5:04.4 is a trim or fade after that (sound: digital zero [R2-sound]). High on "planned", medium on the arithmetic of the last hits (three onsets at 302.34, 302.60, 302.85 s).

**Harmony Q (check harmonic boundaries 0:28, 1:24-1:28, 2:36, 4:40 against form).** 0:28 agrees (bass in, loop A starts, bar 0 of the first lattice). 1:24-1:28 agrees and is the re-barring spot (section 2). 2:36 agrees to the second (bar 34 after the drop; the last E-G-D of loop A lasts 3 chords = 6 bars, 2:24-2:36.6). 4:40 is the weak one: bass A at 4:40 and D at 4:44 are simply the final B-A-D cycle after the outro start at 4:36.6, so harmony's "bass out at 4:40" is really "bass goes to one stab per bar at 4:48.6 (bar 100)". Minor: 4:36.6 is the B of the last full cycle, 4:48.6 is the next cycle start.

**Sound/feeling asked about "false ending, no key change".** Reconfirmed: no cadence, no modulation, no tempo change [R2-rhythm, R2-harmony]. High.

## 5. Corrections to my own round-1 note (and others')

1. **Tempo language.** My round-1 text used 0.372 s beats ("four beats at 0.372 s", "three beats at 161") and said that "120 vs 160 is a tracker switch". Correct reading: 120 BPM; the 1.5 s gap before the last hit is **three beats**, not four, and the form has no tempo element. (Agrees with [R2-rhythm].)
2. **Overlapping rows 14-15** (4:37-4:48 and 4:40-5:00): collapsed into two 6-bar outro stages (section 3).
3. **Loop A chords.** I had written "Em-G-A-D" as one 8 s half loop; [R2-harmony] shows A is a passing note before D (about 0.6 s), so the loop is E-G-[A]-D with 2-bar chords. I adopt that.
4. **"No true chorus."** Still true: nothing returns with new words/melody. But the bar counts add a **recurring "moment"**: a hole-then-return at the end of a block in 1:10-1:16.5, 1:24.5-1:28.6, 4:36.6-4:39.5 and 5:00.9-5:02.3. That is a form motif of removal followed by a hit, appearing four times (twice early, twice at the end), and it is the nearest thing to a refrain. Medium-low (four events, different sizes).
5. **Peak location.** Level peak (loudest seconds 4:12-4:24, [LVL]) is in the 30-bar plateau 3:36.6-4:36.6, where brightness has just completed (3:48.6). I stand by the broad crest, not a single peak.
6. [R1-harmony] reports the chord file wobbling to E at the start of 1:28; my lattice says the downbeat of the drop is 1:28.61 (E bass at 1:28.3 is a pickup). Consistent.

## 6. How the form serves the feeling and the sound

- **Feeling:** the "relief" at 1:28.6 [R1-feeling] is engineered from (a) 2 bars of silence plus a beat of re-barring, (b) speech cut at the exact instant the band returns, (c) the kick becoming four-on-the-floor [R2-rhythm]. The "gripping" is a second 6 bars later (1:40.6). For the long plateau, the feeling is a trance built from identical 6-bar cycles repeated 10 times (2:36.6 to 4:36.6) with a slow brightness ramp; numbness versus escalation depends on whether one hears the 22-30 dB top-band rise (escalation) or the flat drum stem and unchanged chords (stasis). Measurements show **both at once**, which is the engineered tension: harmonically static, spectrally escalating. Medium.
- **Sound:** every boundary has a mix signature [R2-sound]; adding bars: 0:28 (bass+drums in, bar 0 old lattice), 1:28.6 (bar 0), 1:40.6 (bar 6, bass), 2:36.6 (bar 34, voice/other out), 2:48.6 (bar 40, other lift), 3:36.6 (bar 64, voice dense), 3:48.6 (bar 70, top band done), 4:36.6 (bar 94, bass hole), 4:48.6 (bar 100, bass stab), 5:00.6 (bar 106, stop). Gaps between those in bars are 6, 28 (to 34), 6, 24 (to 64), 6, 24 (to 94), 6, 6. A long-short pattern of 6 and 24 (= 4 x 6), apart from the 28 (= 24 + 4). **Almost every interval is a multiple of 6 bars**, strongly suggesting one 6-bar cell and arrangement by moving along it in whole cells. (The exceptions are the 28-bar stretch, 34 = 6 x 5 + 4, and 3:28.6 pickup.) Medium-high.

## 7. Limits

I cannot say whether 6 bars is a designed unit or whether it comes from the 12 s bass-root loop (B-A-D, 4 s each) and was simply stacked; what the measurements show is that arrangement moves are made on its edges. I cannot say what the "extra beat" at the hole is (a dropped beat, a bar of 5, or a cut and re-barring). Bar phase, i.e. which beat is "1", is not in the stems [R2-rhythm]; the kick fold gives beat phase only (the 2 s bar coherence was 0.07-0.08, noise). I counted bars on the lattice anchored at the drop and have not verified individual bar downbeats. Stems leak; "vocal stem -59 / -43 dB" numbers are 8 s means and include bleed.

## 8. Two new questions

1. **Rhythm:** my arithmetic says the stop at 5:00.86 is a quaver *after* bar 106 and the three last hits are at bar 107 minus a quaver, on the downbeat, and plus a quaver (5:02.34, 5:02.60, 5:02.85). Is that a syncopated "and-of-4, 1, and-of-1" figure, and does the kick fold in the first-half lattice (0:28.14, kick skipping at bins 1,2,5,6,10,13) show a way to decide whether the hole at 1:24-1:28.6 contains a dropped beat or a bar of 5/4, so that the re-barring is explained?
2. **Voice:** the vocal-stem onsets in the 4:36.6-4:48.6 and 4:48.6-5:00.6 outro stages are said to be one word per bar from 4:46.65 (on the beat). Do the chops in the 3:36.6-4:36.6 plateau also fall on bar starts of the 1:28.61 lattice (e.g. a call every one or two bars, or at the start of each 6-bar cycle), and does the first dense chop at about 3:36 coincide with the first bar of a B-A-D cycle? That would settle whether the voice, as well as bass and "other", moves in 6-bar blocks.
