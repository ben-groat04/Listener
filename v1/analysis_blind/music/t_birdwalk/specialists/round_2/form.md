# t_birdwalk: FORM and DYNAMICS specialist, round 2 (blind, measurements only)

Evidence key: [F1] my round-1 form.md; [EDGE] form_edges.py stem on/off edges; [LVL] per_second_levels.json; [R2f] new this round: v1/scripts/agents/form_r2_birdwalk.py (6 s vocal/other mel-pattern correlation against the same material 11-13 s earlier) and form_r2b_birdwalk.py (12 s vocal block from 2:11.3 slid across the whole track, 0.25 s steps); [R2g] inline RMS check of bass and drums stems around 0:10-0:14 (0.05 s hop). Other keys: R1 files by specialist name; R2 files for rhythm, sound and harmony (feeling, lineage and voice round 2 were not yet on disk). Timestamps m:ss. I cannot hear; all of this is level, timing and pattern-similarity inference.

## 1. What I now think (changes in bold)

- The song is still a **layer map on a frozen A** (high). Harmony round 2 confirms no chord change anywhere that the bass shows [H2], and sound round 2 confirms that bass and drums are mono and the wide "other" bed decides the stereo width [S2]. So the form is a pure arrangement: loudness, width and layer presence move together.
- **New: the song runs on a steady 12.0 s loop grid, and it can be written as a count of loops.** Intro 1 | groove 3 | break 1 | groove 5 | break 1 | groove 1 | break 1 | groove 2 (then fade). The loop arithmetic is rhythm's finding [R2 rhythm, section 1]: 0:47.2 to 1:59.2 is exactly 72.0 s, six loops. I adopt it.
- **New: the bass drops and returns are anticipated by about one second.** See section 2.
- **Corrected: break 3 is not "new vocal material".** Only the drums differ. See section 3.
- **Withdrawn: "the song accelerates its own cycle" (round 1, section 6).** The grid did not move; only the edit density rose. See section 4.

## 2. Answer to RHYTHM: is the first groove (0:12.4-0:47.2, 34.8 s) 1.2 s short of three loops?

Yes in bass-edge terms, but the shortfall is a phase effect, not a trim, in my reading (medium). Two phases are in play.
- **Bass-edge phase.** Every later bass edge sits near the line 11.2 + 12.0 k: 0:47.2 (exact), 0:59.3 (0.1 s late), 1:59.2 (exact), 2:11.3 (0.1 s late), 2:23.5 (0.3 s late), 2:35.7 (0.5 s late) [EDGE]. The first drop (0:12.4) is 1.2 s *after* that line.
- **Vocal-block phase.** The break material starts about 1.2 s after the bass edge: the vocal block that repeats at 0:48.5 and 2:00.5 [F1, section 5; S2 gives r = 0.96] begins 1.3 s after the bass leaves (0:47.2 and 1:59.2). My new slide [R2f/b] puts the 12 s hook block at 0:12.25 (r = 0.85 against the 2:11.3 block), 0:59.25 (0.80), 2:02.25 (0.81) and 2:11.25 (self). The hook-loop line is therefore about 12.4 + 12.0 k (0:12.4, 0:48.4, 1:00.4, 2:00.4, 2:12.4), and the **bass leaves and returns about 1.0-1.3 s before the loop line** (one and a bit beats at 0.75 s). That is a pickup or anticipation, the way a band cuts out just before the bar. Only the first bass entry (0:12.4) lands exactly on the line.
- On that reading the first groove is exactly three loops (0:12.4 to 0:48.4) with the bass leaving 1.2 s early, so nothing was trimmed. Counter-evidence: the 2:23.5 and 2:35.7 edges are only 0.5-0.8 s early, so "one constant anticipation" is loose. The evidence is fitted to my own choice of line, so I give it medium-low.
- [R2g] adds one fact: the intro's last drum hit at 0:11.6 is big (-22 dBFS against -55 to -65 dB for the intro's other hits, which were already single hits) and the bass enters 0.8 s later at 0:12.4, jumping from -71 to -21 dB in one 0.05 s frame, then a second bass slam at 0:13.4 (-24 to -11 dB). So the first drop is announced by a pickup hit one beat before it. Confidence high on the timings (single-frame edges), medium on "pickup" as a label.

Verse boundaries (VOICE): 0:24, 1:10 and 1:58 fall about 0.8 s after, 1.2 s before and 1.2 s before a 12 s line respectively on the 11.2 line: they sit on the loop grid to about one second, which is as precise as a 6 s correlation window allows. I cannot say more.

## 3. Answer to FEELING and VOICE: is 0:12-0:24 a hook entry, and is the hook a pasted loop?

- **0:12-0:24 is the first hook entry, not intro-extension (medium-high).** The 12 s block from 2:11.3 correlates 0.85 with 0:12.25 [R2f/b]. 0:24-0:42 matches nothing at 11-13 s lag (r = 0.70-0.74, ordinary chant similarity; 6 s blocks) so I now label the first groove as **hook (0:12-0:24) then verse 1 (0:24-0:47)**, which is how VOICE heard it. This replaces my round-1 single "Groove A".
- **The hook block repeats at very high similarity three times in the last minute.** Lag-back correlation of 6 s vocal blocks at about 12.1 s: 2:12 r = 0.93, 2:18 0.87, 2:24 0.92, 2:30 0.85, 2:36 0.84, 2:42 0.75 [R2f]. That is the same vocal take pasted at 2:11.3, 2:23.4 and 2:35.5, so **break 3 (2:23.5-2:35.7) uses exactly the hook the groove had just played**; the drums were simply taken out as well as the bass. Round 1 called break 3 "the one new break"; that was wrong in the vocal sense. It is "new" only in having no drums.
- Earlier hook repeats are looser: 0:48 to 2:10 blocks match their 12 s predecessor at only 0.59-0.82, so the voice in the long middle (grooves B and the breaks) is **verse-like speech that does not loop**, except the 0:48 / 2:00 break block, which repeats itself at lag 72 s (0.94-0.96 [F1, S2]). So there are two pasted units: the **12 s break block (0:48 and 2:00)** and the **12 s hook (0:12, 0:59 or so, 2:11, 2:23, 2:35)**. Break-block vocals correlate 0.81 with the hook block, so they are the same chant type with different words or pitch contour (low confidence on what differs).
- Layer count in the last minute is therefore the cleanest instance of the form: same voice, same hook, the only things moving are bass and drums.

## 4. Correction: the song does not accelerate

Round 1 said the cycle "accelerates" (grooves of 35, 60, 12, 27 s). The loop grid is constant at 12.0 s throughout, and rhythm's arithmetic gives a steady count over 72 s [R2 rhythm, section 1]. The shortening of grooves is an editing pattern: the arrangement spends less time between subtractions late in the song (1 | 3 | 1 | 5 | 1 | 1 | 1 | 2 loops). I keep the felt consequence, that the last stretch is cut up more often (the breaks at 1:59, 2:23 follow only 12 s of groove), but not the word "accelerate". Confidence: high that the pulse did not change in the loop arithmetic, medium that the arrangement is "denser late".

## 5. Answer to HARMONY: do the G (b7) leans sit before layer changes on the same grid?

Harmony's five leans: 1:22, 1:47, 1:58, 2:47, 2:58. On the 12.0 s line I use (11.2 + 12 k, bass-edge phase) they fall at 1.2 s before, 0.2 s after, 1.2 s before, 0.2 s after, and 1.2 s before a line. All five are within 1.2 s of a line, but the vocal pitch estimates are only good to about plus or minus 0.5-1 s, and any time lies within 6 s of a line; so I cannot show this is more than chance (low). More useful: **transitions without a documented G lean** are the six bass edges at 0:47.2, 0:59.3, 2:11.3, 2:23.5, 2:35.7 and the first drop at 0:12.4, so the G-signal hypothesis would explain only the "late" cuts (the other-out at 1:23, the 1:47 return, 1:59, the voice-out at 2:47.5, the voice-in at 2:57). I accept it as a weak, voice-delivery marker, not as a form device. Harmony should check G in the vocal stem at 0:47, 2:11, 2:23 and 2:35; if it is missing there, drop the idea.

## 6. Connecting my area to the others

- **Rhythm to form.** With a beat of about 0.75 s the loop is 16 beats, one bar at about 3.0 s being 4 beats. I now prefer rhythm's option (b): a 4-bar loop at about 80 BPM and a 1.55 s hit that falls on beats 1 and 3 (half-bar). So my "8 bars" in round 1 becomes **4 bars of about 3.0 s**; 12.0 s is the unit and bar numbers are a labelling choice. The sparse drum hit per 1.55 s in the intro and the breaks is half-time backbeat-like, and the sudden drum density at 1:34-1:54 [F1, section 2.1] is the groove filling in what the sparse sections leave out.
- **Sound to form.** The stereo width jump in breaks is an energy-ratio effect of mono bass and drums against a wide, decorrelated "other" bed [S2]. That means the width change cannot be a separate dynamic move; it is the same one as the bass leaving. I withdraw my round-1 phrase "space as the second axis" as an independent axis: it is the same axis seen through the stereo image. Confidence high.
- **Harmony to form.** With the pitch floor fixed on A (bass A1, other A3/A5 [H2]), the 50-55 dB bass fall at each edge is the loss of a *sounding* tonic, while the A stays implied by the stab and the voice. This is why the breaks feel light yet not unstable: there is no key change to resolve, only the floor to put back.
- **Voice to form.** The voice never rests, so the breaks work as exposure (voice -17 to -23 dB constant [LVL]) and the voice-free 2:47.5-2:57.1 block is the one place where the song removes its anchor while the groove is on. Because the last-minute hook is pasted exactly (section 3), that voice-free block is also the only passage where the loop is broken, and its end, a falling glide at 2:58.5-2:59.9, is the only non-loop gesture near the end.
- **Feeling to form.** The "release is a loss, tension is a return" pattern fits FEELING's account of a playful, pushing groove: the payoff is the bass coming back. The 1 s anticipation of each cut and return (section 2) is how that payoff is shaped: the bass hits before the bar line, which makes the return feel like a push (inference, not measured by me).

## 7. What I am not sure of

- The 1.2 s phase offset between bass edges and hook loop is fitted, not independently measured; I have not checked the drum-hit grid against it.
- 6 s correlations of chanted speech run 0.6-0.8 for any similar-sounding phrase, so only values of 0.9 and above mean "same take".
- Round-1 details I adopted without re-measuring remain medium confidence: the 2:42-2:57 stutter list and the 1:41-1:46 bass hole blips.
- The map says nothing about verse/chorus meaning, only layer presence and pasted repeats.

## 8. Two new questions

1. **To RHYTHM:** the intro's big drum hit at 0:11.6 (-22 dBFS) precedes the first bass entry (0:12.4) by 0.8 s, then a second bass slam lands at 0:13.4 (1.0 s later). In your beat grid are 0:11.6, 0:12.4 and 0:13.4 beat positions (one beat is 0.75 s, so 0.8 and 1.0 s would be 1.07 and 1.33 beats), and does the 1.0-1.3 s lead I measure on later bass cuts (0:47.2 against the hook line 0:48.4, 1:59.2 against 2:00.4) equal one beat plus a sixteenth or an eighth-note anticipation?
2. **To VOICE (with SOUND):** the three pasted hook blocks at 2:11, 2:23 and 2:35 correlate 0.84-0.93; the 0:48 and 2:00 block correlates 0.94-0.96 with itself. Can you tell, from pitch contour and syllable timing in lead_notes, whether the break block and the hook are the same words with different pitch, or different words, and does the break block begin its first syllable on the loop line (about 0:48.4) rather than at the bass cut (0:47.2)?
