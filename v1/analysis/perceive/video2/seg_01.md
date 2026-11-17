# video2, segment 1: 0:00-0:20 (eyes)

> Corrected after cold-read: signboard lettering method not claimed.

Method: contact sheet 01, four shot keyframes (shots 1-4), 1 fps frames f_0001, f_0003, f_0008, f_0009, f_0013, f_0016, f_0020, spectrogram, audio summary, transcripts. visual_features/ and stems were empty/absent for this video, so no brightness/motion numbers are used. Audio is inferred from features only; I cannot hear it.

## Shot-by-shot (observation)
Shot boundaries from shots.json: 0:00-0:01.7, 0:01.7-0:07.9, 0:07.9-0:12.2, 0:12.2-0:24.2 (the last runs past this segment).

1. 0:00-0:01.7 | Title card. A dark rectangular board, mounted on a pale, weathered wooden wall (peeling paint flecks at right), with white capital lettering: "DE WINTER VAN / 1963 / IN FRIESLAND". Static, locked-off, centred slightly left. Colour film but strongly desaturated: whitish wall, teal-green ledge below the board. Visible 16mm-style gate edge, slight vignetting, grain, small scratches/dust. Archival.
2. 0:01.7-0:07.9 | Close view of a hoar-frosted tree crown filling the frame, shot looking up against pale sky. Blue-violet cast. Near static with slight handheld drift/sway; the frame is a little uneven (black edge at left and a dark vertical strip upper right, as if the film is slightly mis-registered). Dense, lacy branching, almost abstract texture. Archival, colour (heavy blue grade/fade).
3. 0:07.9-0:12.2 | Camera moves (tilt/pan) down and to the right through frosted branches; a pale roof or house shape glimpsed behind the twigs (f_0009), out of focus. A broad black band at the right edge (about a fifth of the frame) from about 0:08 to 0:11, which looks like the film frame/edge or a masked area; I cannot tell which. Slightly more motion blur than shot 2. Bluer and darker than shot 4.
4. 0:12.2-(0:24.2) | Wider and brighter: a large frosted branch sweeps across the left; behind it, a snow-covered house with a stepped/gabled front and a small dormer window, lower right (f_0013, f_0016). The camera drifts slowly upward and rightward, so by 0:19 the house has dropped nearly out of the frame and only branches against a bright, almost white sky remain (f_0020). Exposure rises through the shot, ending washed out and pale cyan. Archival.

## People, places, objects, text
- People: none in 0:00-0:20.
- Place: a Frisian village or town street in deep frost, indicated by the sign and a gabled brick-style house under snow. The house shape is consistent with Dutch domestic architecture, but I cannot confirm the exact town.
- Objects: lettered/painted signboard (method unverified); frosted trees; one snow-roofed house.
- On-screen text: "DE WINTER VAN 1963 IN FRIESLAND" = "The winter of 1963 in Friesland". Dutch; "Friesland" is the Dutch name for the province also called Fryslan. Letters look like press-on/stick-on white capitals with slight mixed shapes (the "A" in "VAN" and "FRIESLAND" has an unusual form), so this is a homemade or amateur title board.
- This matches the context.md lead (Dutch archival footage of the 1963 winter/Elfstedentocht).

## Sound in this stretch
- Words: none transcribed. The first transcript line is "MUZIEK" at 0:28; narration begins at about 0:41 ("18 januari 1963"). So 0:00-0:20 has no speech (high confidence; consistent across whisper runs).
- Music (inferred from spectrogram/features, medium confidence): quiet, sparse and low. RMS about 0.03-0.07, mean for the track 0.20, so this is a fraction of the later loudness. Energy sits mostly below about 300 Hz plus a faint stack of harmonics around 400-2000 Hz; nothing above about 2 kHz until roughly 0:40. The spectrogram shows separate low-frequency pulses/gaps in the first ~27 s (vertical dark gaps near 0:03, 0:08, 0:12, 0:17-0:20), suggesting a slow, swelling or breathing drone/pad rather than a beat. Estimated key at the start is B minor (0.94), the strongest per-30s reading in the track. No beats are detected before 0:42 (beat_times starts at 42.68 s), so the stated track tempo (161 BPM) says nothing about this opening.
- Small RMS bumps at 0:00 (0.056), 0:08 (0.063), 0:12 (0.069), 0:19 (0.059). The 0:08 and 0:12 bumps fall within about 0.1-0.2 s of the cuts at 7.88 and 12.16 s (shot 3 and shot 4 starts), so the cuts may land on musical accents or a swell. The cut at 1.72 s has no matching bump (0:02 RMS is the minimum at 0.033). Treat the 0:08/0:12 link as tentative; with 1 s resolution it could be coincidence.
- Picture/sound relationship: the picture is slow, static and cold, and the sound is low and hushed, so they agree in mood. There are no words to echo images, and no cut-to-beat editing, since there is no beat yet.

## What a viewer feels (interpretation)
- Hush, cold and anticipation. A title board announces a historical document, and then the film dwells on frost rather than action, which reads as scene-setting and patience. The pale blue-violet cast, the lacy branch texture and the bright, overexposed sky give a feeling of fragile beauty, but also of a world coated and silenced.
- The old-film imperfections (grain, uneven frame edges, fading colour) signal "this is memory/record", so the viewer approaches it as heritage footage with some tenderness.
- The low, quiet music (if it is a drone, as the spectrogram suggests) would add weight and a sense of something large and slow approaching. Label: speculation about what the sound feels like.

## Motifs and visual rhymes to track
- Frost/hoar on branches: the first full image of winter; watch for it returning at the end as a bookend.
- Blue-violet cold colour grade vs. any warm colours later (e.g. skin, clothing, lamps).
- Bright, blown-out sky at 0:19: possibly a "white-out" that could cut to a new scene or lead to the 0:28 "MUZIEK" cue.
- Houses/roofs under snow: the human settlement behind the nature; the race will move through towns.
- Title card as a document frame: later text cards or the dated narration ("18 januari 1963") could rhyme with it.
- Tilting/drifting upward camera: a rising motion, perhaps echoed by the music swelling.

## Open questions for the team
1. Do the quiet pulses in the 0:00-0:27 spectrogram correspond to a drone or sampled wind/ice sounds? Stems (htdemucs in stems_raw) could check this.
2. Does the music's first beat/entry near 0:28 (the "MUZIEK" line) or 0:42 align with a visual change?
3. Is the black band at the right edge in shot 3 an original film-gate effect or a deliberate PSB edit/mask?
4. Is the title board footage from the Fries Film Archief (as context.md suggests), and is it the opening of an original amateur film? Research would help.
5. visual_features/ is empty for video2; the extraction step may need rerunning if numeric colour/motion values are wanted.
