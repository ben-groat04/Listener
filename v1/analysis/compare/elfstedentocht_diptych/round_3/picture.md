# Elfstedentocht diptych, round 3: the picture reading (final round)

Reader: picture. British English. Timestamps are `<video> m:ss` on our files. Tags: **OBS** seen or measured, **INT** interpretation, **SPEC** speculation; H/M/L confidence. Nobody has heard the audio. Read this round: all four `round_2/` files (listener, music, picture, story). "R3 check" marks something I ran or opened this round, on `data/video{1,2}/frames_1fps/`, `scenes/shots.json`, `audio_features/beat_times.json` and `sync/grid_120bpm.json`.

## 0. What changed for me this round

1. **The shared shots are confirmed, and their order is almost preserved** (section 1.1). The four pairs hold on re-check; the order of the four across the two films differs by one swap.
2. **Video2's cuts do lock to the bar, a little early** (section 1.2, R3 check). This contradicts the flat "no lock" that I, the music colleague and the listener have all repeated for Part 2, and it is the largest correction to the team's sync story.
3. **Video1's offset cluster is two flurries at beat rate**, not a film-wide habit (section 1.3).
4. **Part 2 is not a lengthening of Part 1's footage** (section 1.1): same order, very different spacing.
5. I withdraw the reading that Part 2's hole picture and Part 1's are "opposites" as stated; they are different, but the real contrast is lock against no lock (section 2).

## 1. Answers to colleagues' questions

### 1.1 Listener Q1: is the order of the shared shots the same in both films?

R3 check: I redid the match over every pair of 1 fps frames (48 x 27 greyscale, mean-removed correlation) and then opened the pairs side by side.

| Shot | video1 | video2 | Confirmed by eye |
|---|---|---|---|
| bib 170, back, black hat, gate hair at top | 1:05 | 3:34 | yes, same framing, grey against blue |
| bib 145, bobble hat, group bent ahead | 1:08 | 3:30 | yes |
| bib 157, white woollen hat, wooden stick, ice sweeping right | 3:00 (r 0.97) | 3:51 | yes |
| skater, striped headband, arm back, snow bank upper right | 3:02 (r 0.97) | 4:44 | yes |

Two further high-scoring pairs (video1 2:49 against video2 2:47; video1 2:42 against video2 4:53) were opened and are **not** the same shot (a crowd of officials against red lamps; a crowd against ducks). So four is still my floor, and the correlation method gives no fifth confirmed pair above r 0.85 (OBS).

**Order.** video1: 170 (1:05), 145 (1:08), 157 (3:00), headband (3:02). video2: 145 (3:30), 170 (3:34), 157 (3:51), headband (4:44). The order is the same apart from one swap, 145 and 170, which are 3 s apart in Part 1 and 4 s apart in Part 2 (OBS). Four items give 24 orders; one adjacent swap is about as close to "same" as four items can be, though with n = 4 it is suggestive, not proof (M).

**Spacing differs sharply.** The last two sit 2 s apart in Part 1 (3:00, 3:02) and 53 s apart in Part 2 (3:51, 4:44). The first two sit 3 s apart in Part 1 and 4 s apart in Part 2. The long gap between pairs is 1:08 to 3:00 (112 s) in Part 1 against 3:34 to 3:51 (17 s) in Part 2. So Part 2 is neither a lengthening of Part 1 (spacing would scale together) nor a shuffle (the order survives). **INT, M-L:** the two cuts follow one sequence of rolls, with Part 1 jumping from the first to the second pair across a long run of documentary shots, and Part 2 keeping the rolls near each other and letting the last pair breathe. A shared source order would be natural if both were cut by reading the same reels in sequence; I cannot show that. This answers the listener's question: **a recut in the same reel order**, not a lengthening and not a reshuffle.

### 1.2 Story Q2, listener Q2: what does Part 1 have that Part 2 lacks, and the reverse?

From the dossiers (video1 `dossier.md` and video2 `dossier.md`) and my frames:

- **Document-like, Part 1 only:** the town signs ("ULST" 2:18, "WELKOM IN WORKUM" 2:27 to 2:28), the tea table and cups (2:11 to 2:12), the FINISH banner (2:48), "Reportage ELFSTEDENTOCHT" (3:07). Part 2 has a title board (0:00 to 0:02) and, as picture round 2 found, no route sign in 3:20 to 4:39. It does carry non-bib text elsewhere: a round road sign (1:22 to 1:30), a square "K" sign (about 2:06) and the lorry lettering (1:31). So Part 2 has traces of document-like images but never the newspaper, the signs-in-order or the banner (OBS).
- **Landscape-like, Part 2 only:** the pink-mauve dusk with red globe lamps (2:44 to 2:48), ducks and floes (4:53 and the final shot from 4:58.6), the unhurried long ice lane. But Part 1 also has empty fields and frost (video1 dossier lists empty frames at 0:56, 1:30, 1:40, 2:19, 2:22, 2:54; frosted reeds 1:34). So the landscape register is not exclusive to Part 2, just more frequent there and held longer (OBS, M).
- **A rhyme the story colleague did not mention (R3, OBS from the dossiers):** a man lurches at the lens in Part 1 (0:27, eyes wide, mouth open, rime on face) and in Part 2 a man in sunglasses lurches at the lens (4:21). This may be one habit of the camera operators (the only faces held are those that come at the lens), not an editorial echo (L, SPEC).

**Answer:** the split is **looser than "document against landscape"**. Part 1 is more document-heavy and Part 2 more landscape-heavy, but each has traces of the other. I would not say the pair was divided by function. The shared-shot finding says the pack-from-behind footage is the one register that both films use freely. And as a viewer, which is more noticeable, repeated shots or a repeated script? I expect a viewer to notice the script first (words are a memorised line), the shots second, and only if the bib is legible (INT, SPEC; no viewer test).

### 1.3 Music Q1: which of Part 1's cuts sit about 0.245 s after the tracker beat?

R3 check on `shots.json` and `beat_times.json` (39 cuts in the tracked range 0.95 to 167.97 s; my phase = fraction of the beat after the preceding tracker beat).

- Phase histogram in eighths of a beat: 5, 8, 7, 8, 5, 2, 3, 1. The mass is in the first half of the beat, with a thin tail at 0.75 to 1.0 (OBS).
- Cuts in the 0.15 to 0.50 band: 21 of 39, spread from 0:01 to 2:38, **but concentrated in two passages**: the rapid run at 1:05 to 1:13 (phases 0.20, 0.25, 0.27, 0.46, 0.13, 0.12, 0.20) and the flurry at 1:48.7 to 1:54.3 (0.01, 0.21, 0.26, 0.25, 0.39, 0.37). In the second, three cuts at 1:49.6, 1:50.4 and 1:51.2 are 0.8 s apart with phase 0.21, 0.26, 0.25: that is a cut about every beat (the tracker beat is 0.766 s), with a steady lag.
- These two passages are the fastest-cut stretches of the film (per `sync.json`, 7.58 and 5.43 cuts per 10 s in the D section at 1:06 to 1:16 and the B section at 1:49 to 1:59). So the headline phase cluster comes mostly from **two flurries cut at roughly one cut per beat**, not from a film-wide habit. Elsewhere the phases are scattered (the slow sections have 1 to 2 cuts per 10 s and `cuts_on_beat_frac` 0 to 0.25).
- **INT, M:** the editor cut at beat rate in the busiest moments, with a steady lag; whether that lag is the tracker or the editor remains unresolved (agreeing with music). It remains a modest result (39 cuts, no multiple-test correction, music's own caveat).

### 1.4 Music Q2 (to picture and story): does the picture change once per bar in the fragment passage (video2 3:28.6 to 4:37)?

R3 check: video2 cut times in 3:25 to 4:40 (26 cuts) against the 120 BPM grid (period 4 x 0.49995 s, downbeat 88.6165 s).

- **Not throughout, but in runs.** Gaps between cuts are 1.9 to 2.3 s (one bar) in 6 of 25 intervals, mostly in two runs: 3:28.5, 3:30.5 (then a gap), 3:34.0, 3:36.0, and 3:46.5, 3:48.5, 3:50.6, 3:52.8 (OBS). Other gaps run 0.7 to 8.4 s. So the picture is cut at bar rate in places, not as a rule.
- **The cuts in those runs fall just before bar starts** (phases 0.94, 0.96, 0.94, 0.96, 0.98 of a bar, that is 0.04 to 0.12 s early). See section 2 for the whole-film pattern.
- **What changes at those cuts:** from the frames, a new bib or a new camera position in the pack (3:30 to 3:39: 145, 170, then 529). No sign, no named place (OBS; picture R2). So a **picture-per-bar echo of the voice exists in places**, but nothing in the images could carry a town name. I cannot assert that fragments and cuts are tied; I can say they share a pulse. For 3:28 to 3:50 no judgement of town names is possible from the picture (L).

## 2. New finding and challenges to colleagues

### 2.1 Video2's cuts cluster just before the downbeat (R3 check, M)

Music round 2 reported `sync_kickgrid.json`: 36.0% within 80 ms against 31.6% chance, bar p = 0.20, with the first 42 s alone having bar p = 0.014. That is a Rayleigh-style test, which misses a narrow spike. I plotted all 66 cuts after 1:28 against bar position on the same grid:

- Histogram of cut offset from the nearest bar start, 0.1 s bins from -1.0 to +1.0 s: 2, 3, 3, 4, 4, 3, 2, 2, **7, 11**, 1, 4, 3, 2, 1, 4, 3, 3, 2, 2. The two bins spanning -0.2 to 0.0 s hold 18 cuts (27%); the uniform expectation is about 6.6 (10%). Binomial tail for 18 or more at p = 0.1, n = 66: about 6e-5; allowing for my having picked the window after seeing the histogram (20 bins), roughly 1e-3 (M; post hoc, but the spike is plain).
- It is present in both halves: 10 of 32 cuts from 1:28 to 3:25, and 8 of 26 from 3:25 to 4:40; none of the 7 cuts after 4:40 (the dismantling).
- It is a **bar** effect, not a beat one: of cuts nearest the other three beats of the bar, only 3 of 13, 4 of 13 and 8 of 16 fall 0 to 0.2 s before the beat (chance 40% of the beat period), while 18 of 24 cuts nearest a downbeat fall there. So the editor, if this is design, cut about 0.1 s ahead of the bar start (a typical hand-editing habit of cutting just before the beat so the new picture is already there when the sound lands; SPEC).
- **Caveats (do not skip):** (a) the 0.1 s lead is about 2 to 3 frames, within what a scene detector's timestamp, an mp3 delay or a grid-offset error of 0.1 s could produce (the grid downbeat is placed by the music colleague to within ms, but the video offset is not independently known); (b) the window was chosen after looking; (c) I did not run the same test on Part 1 because its bar grid is "tracker-derived" (music reading). A systematic delay in either file would shift the spike without removing it.

**Consequence:** the sentence "no reliable cut-to-grid lock in Part 2" (music R2, listener R2, my own R2) should become **"no lock at the beat, a probable early-bar lock of about 0.1 s"**. Together with the three event joints (0:28.08, 1:28.5, 2:36.6), Part 2's edit is more music-aware than a glance at the beat statistics says. And it changes the contrast with Part 1: Part 1 has an offset cluster at beat rate in two flurries; Part 2 has a bar-start cluster across the film. Neither edit is random.

### 2.2 Music: "pictures meet the music at section edges, not on the grid"

Qualified. The section-edge joints stand (OBS). But the early-bar cluster says the grid does matter for a third of the cuts. I now think both are true: sections (events) and bars (grid) (M).

### 2.3 Story and listener: "the hole is a habit of the mix, not the picture"

Agreed and I should be precise. My own round 2 said the picture "disagrees" (empty road against crowd). The better statement: Part 2's picture holds and then cuts on the drop; Part 1's picture has a whip-pan and a banner within a second of its hole and no demonstrable lock. The device is **sound-led**, with the picture engaging in Part 2 only (OBS, as before).

### 2.4 Story: "the sprint is Part 2's footage played fast, so Part 2 continues Part 1's last twenty seconds, played slowly"

Partly challenged. The shared-shot order (1.1) shows Part 2 revisits the same rolls, but in Part 2 bib 157 and the headband skater come 53 s apart; Part 1 puts them 2 s apart. "Played slowly" is plausible for Part 2's overall pacing (cuts per 10 s 2.8 against 2.7, equal, so it is not slower by cut rate). Duration, not rate, differs: Part 2 is simply longer. Let me restate: **the rolls are common; Part 2 spends more time in them; the cutting rhythm is the same** (OBS on rates; INT).

### 2.5 Listener: "accidental protagonists" (bibs 170, 157)

Accepted as an effect for a viewer who notices; I add that the effect is stronger in Part 1 only if the viewer sees Part 2 first. For the in-order viewer, Part 1's bibs are glimpsed and Part 2's are held (170 at 3:34 to 3:35, 157 at 3:51 to 3:58), so recognition happens as a payoff in Part 2 (SPEC).

### 2.6 Music: "same pulse" speculation (156/160 BPM equivalence)

Agree with the music colleague's caution. My R2 cut-rate coincidence is dropped as evidence. Part 1's cutting is at about one cut per 0.8 s in its flurries (tracker beat 0.766 s), Part 2's bar-cluster cuts are 2.0 s apart in runs. These are not the same cutting pulse (0.8 s against 2.0 s); the equal mean rate of 2.7 to 2.8 cuts per 10 s is a coincidence of averages (M).

## 3. Limits

- 1 fps correlation; low recall. Four shared shots is a floor; I opened two false positives.
- Cut times are from a scene detector at video frame rate; a 0.1 s lead is within plausible systematic error (2.1 caveat a).
- The early-bar cluster is post hoc and cannot show intention. No audio was heard.
- Dossier-based claims in 1.2 are carried from the video dossiers, not all re-opened by me.

## 4. Settled view in five bullets

1. **One footage pool, one reel order, two films (H for shared shots, M for order).** Bibs 170 and 145, bib 157, and the striped-headband skater are the same shots in b/w in Part 1 (1:05, 1:08, 3:00, 3:02) and in colour in Part 2 (3:34, 3:30, 3:51, 4:44), in nearly the same order but at wholly different spacings. Part 1's b/w is at least partly a treatment of colour-capable material; the grey and the blue of bib 170 are the pair's one visible touch.
2. **Two registers, loosely divided.** Part 1 is document-led (signs in route order, tea table, FINISH banner, "Reportage" banner) with two fast flurries and a short race burst at 2:55 to 3:02; Part 2 is landscape-led (dusk lamps, ducks, floes), a long pack-from-behind plateau, and a final high-angle water shot. Each carries traces of the other (empty frost fields in Part 1, road signs and lorry lettering in Part 2), so the split is one of proportion, not function.
3. **The picture serves each track differently.** In Part 2 it holds still through the 4 s hole (a deserted road, 1:24.3 to 1:28.6) and cuts onto the drop, cuts about 0.1 s ahead of bar starts across the film (18 of 66, post hoc, M), and withdraws with the sound at the end. In Part 1 it keeps moving under a flat, constant track: fastest cutting at 1:05 to 1:13 and 1:49 to 1:54 at about one cut per beat with a lag, and no demonstrable cut at the three biggest sound events (1:15.3, 1:40.0, 2:47.8).
4. **Anonymity is largely footage, not edit.** The camera sits behind or below the skater, so bibs are the only identity and no face is held; what is a choice is the account that never names a skater, a winner or a finish. Neither film shows the arrival; Part 1 reaches race footage at 2:55 and cuts to a banner, Part 2 dissolves into water.
5. **What the pictures cannot do.** They cannot confirm that Part 2's voice fragments are town names (no sign appears in 3:20 to 4:39; cuts share a bar pulse with the voice only in runs), cannot say whether Part 2's cut was made from Part 1's or the reverse, and cannot separate the early-bar lead from detector or mp3 delay. A Dutch listener (for the names) and a frame-accurate cut list against the audio (for the lead) would settle two of the open questions.
