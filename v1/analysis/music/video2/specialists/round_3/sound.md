# video2: SOUND specialist, round 3 (final)

I cannot hear; all of this is measurement. Confidence H/M/L. Timestamps m:ss. New helper: `v1/scripts/agents/v2_sound_r3.py` (stem "other" band energy at loop-cell starts, tilt curve, vocal/other onset cross-correlation, 4:37 band drop). Stems: `stems_raw/htdemucs/song/*.wav`. Earlier numbers (round 2 sound.md) are reused, not repeated.

## 1. Answers put to me

**Form: is the "other" change a filter, or instruments entering and leaving? Is 2:36.8-2:48.8 a mute?**
Per-6 s band energy of "other" (dB; 250 Hz-1 kHz / 1-2 kHz / 2-4 kHz / 4-8 kHz):
- 2:30: 35.1 / 27.1 / 18.1 / 2.8. 2:36.8: 26.0 / 21.8 / 13.4 / -7.0. 2:42: 27.7 / 21.0 / 13.0 / -8.1. 2:48.8: 37.1 / 26.4 / 13.2 / -7.6.
- At 2:36.8 every band drops together (-9 dB body, -6 dB 1-2 kHz, -5 dB 2-4 kHz, -10 dB top), so it is a **level or part reduction, not a low-pass sweep** (a filter would drop the top far more than the body). It is a partial mute: the layer is not silent (body still 26-28 dB). At 2:48.8 only the body returns (+10 dB), while the top stays at -7.6 dB. So the layer returns in two stages: a low body first, then brightness. H on the numbers, M on "partial mute plus re-entry" (a fader or gate on one layer fits; a filter alone does not).
- From 3:00.8 the top then climbs: tilt (4-8 kHz minus 250 Hz-1 kHz) is -42 (2:54), -38 (3:10), -35 (3:26), -29 (3:34), -26 (3:42), -21 (3:50), -20 (3:58), then flat at about -19 to -17 to 4:30. That is a **ramp with a faster section 3:26-3:50 (about +14 dB in 24 s), then a plateau**, not a clean four-step staircase. The cell-start values (2:36.8, 3:00.8, 3:24.8, 3:36.8) do each show a rise, so a bar-aligned change is plausible, but with 4 s resolution I cannot tell a stepped filter from an automated sweep (L-M). I prefer "one layer being opened gradually, with cells where the movement is audible" over "new instruments".
- Layer test: the band-shape stays proportional (body +5 dB, 1-2 kHz +12, 2-4 kHz +15, 4-8 kHz +30 from 2:54 to 4:24). Added harmonics rising together with the same pitch classes (harmony) is what a **filter opening plus drive** produces; a new instrument would add a distinct onset pattern, and none appears (onset rate stays 7.2-7.9 per s, round 2). M.

**Feeling: is 4:37 a filter or fader move, or a layer stopping at a loop boundary? Did a layer enter at 2:48 and 3:24?**
- 4:36.8 (cell start): the whole layer falls together. 6 s windows: 4:30 41.5 / 39.1 / 36.0 / 24.2 to 4:36.8 30.7... 36.9 / 30.7 / 23.8 / 10.9, then 4:42 36.5 / 28.7 / 18.6 / 8.9. Per second, 4:34 to 4:38: top band 24.3, 22.2, 9.5, 15.6 and 1-4 kHz 40.5 to 33.4 to 31.8. Top falls most (-13 dB), 1-4 kHz less (-7), body 250 Hz-1 kHz about -4. The 60-250 Hz band **rises** (32 to 36 dB). So the bright layer is removed or filtered while the low pad stays, which a layer stopping explains as well as a filter. I cannot separate them (L). It is on a loop-cell start, so arranged, not accidental (M-H, harmony's cycle).
- 2:48 and 3:24: at 2:48.8 the body re-enters (+10 dB, above); there is no new onset figure, so I call it a **re-entry of the same layer, not a new one** (M). At 3:24.8 the top band rises about 6 dB (5.7 vs -2.0 at 3:00.8 and 0.5 at 3:12.8) with no new rhythm: brightening, not layering (M).

**Voice: do the 4:40-4:59 bursts lead in the vocal stem or the "other" stem?**
Onset-strength cross-correlation of the vocal stem against "other" over 4:40-4:59 peaks at only 0.18 at about -186 ms and is -0.12 at zero lag. That is **inconclusive**: "other" onsets are too dense (about 7.5 per s) for a 2.0 s burst rhythm to stand out, so the correlation is dominated by noise. Round 2's width result (+1 dB S/M) stays as the only evidence: the bursts sit in the wide instrument space. I cannot say whether they are leakage or a processed voice sample (L).

## 2. Corrections
- Round 2 said "bass gated, not sidechained" and the late brightening as "opening/drive"; both stand. I now soften "drive" to "filter opening and/or drive" (the numbers cannot choose).
- I withdraw any reading of 2:36.8 as a filter dip; the all-band drop says part reduction.
- Voice's cross-correlation test, which I accepted as decisive in round 2, is not decisive; I should have said so.
- Rhythm and form's loudness steps stay as stated (drums flat -18 to -19 dBFS from 1:28; mix steps at 0:28, 1:28.5, 3:36).

## 3. Connections
- **Form:** sound's best contribution to the form is the "other" layer's cell-aligned movement: mute-ish at 2:36.8, body back at 2:48.8, ramp 3:00-3:50, plateau to 4:36.8, removal at 4:36.8. The rhythm and pitch classes stay fixed, so form is carried by timbre and level.
- **Rhythm:** a fixed drum/bass skeleton under a moving upper layer; the 3-sixteenth lag in "other" is a pattern, not a confirmed delay.
- **Feeling:** the audible arc is narrow and dark, then loud and centred, then bright and urgent (top +20 dB over 3:00-4:24), then a sudden hollowing at 4:37 with the low pad left.
- **Lineage:** clean, bright modern electronic production; archive material as content, not fidelity.

## 4. Settled conclusions
1. **Sound design is modern, clean and bright, with no vinyl or tape noise floor** (4 kHz+ at about -70 dB early, bright late); the archive speech is band-limited (hard edge near 4-5 kHz) but sits in a clean mix. High on numbers, M on era.
2. **The mix is a fixed skeleton plus a moving upper layer**: mono-centred drums (flat -18/-19 dBFS from 1:28) and a low-passed, pitched bass (fundamental 60-120 Hz, 28 dB or more down above 250 Hz; bass guitar, sample or synth indistinguishable), under a wide "other" layer. H.
3. **The build is timbral**: "other" gains +24 dB at 4-8 kHz between 3:00 and 4:24 with unchanged rhythm and pitch, a ramp fastest at 3:26-3:50; this looks like filter opening and/or drive on one layer, not new instruments. M on mechanism, H on numbers.
4. **Transitions are subtractive**: 2:36.8 a partial mute (all bands -5 to -10 dB), 4:36.8 the bright layer removed with the low pad kept, 4:38.5 a noise-like transition hit (flatness 0.024) with a bass hole, and the bass gated (not sidechained) from 4:48.5. M-H.
5. **Instrument identity is not recoverable**; the late voice bursts are band-limited like the narrator but stereo-wide (+1 dB S/M), and I could not settle whether this is processing or stem leakage. L.
