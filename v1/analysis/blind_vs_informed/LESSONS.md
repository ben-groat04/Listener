# Lessons from blind versus informed runs (video1, video2)

Source: `video1.md`, `video2.md` in this folder, plus 23 lessons drawn from them. Merged and deduplicated into 14 changes below. Nothing in the toolkit has been edited yet; each item names where to change it. Paths are under `v1/` unless stated. File and prompt names are the likely targets and should be checked on implementation (prompts live inside `workflows/*.js` and `scripts/agents/`).

Priority: P1 = fixes errors both runs made or shapes every video; P2 = measurable gain; P3 = polish.

## P1: process and honesty rules

### L1. Blind first, informed extends; freeze the blind claims (P1)
- Blind lane is the standard first pass. Informed lane tests and extends it, never rewrites it. Lanes stay independent.
- Before research starts, write `data/<video>/blind_frozen.md`: subject, date, place, structure times, top moments, each with its confidence tag.
- Blind-versus-informed becomes the standard last step on every video; raw data, not the run with more context, settles disagreements. The diff feeds prompt fixes.
- Change: `workflows/blind_chain.js` (emit the frozen file), `workflows/blindcmp.js` (make it a default final stage), `TOOLKIT.md` (stage order).

### L2. Confidence tags carried through every stage (P1)
- Tags: OBSERVED, HEARD high/med/low, INFERRED high/med/low, SPECULATED.
- Synthesis may not lower a tag without a stated reason (the Elfstedentocht sentence was rated high in perceive and dropped in synthesis).
- Change: prompts in `workflows/perceive.js`, `interpret.js`, `report.js`; add a tag-preservation check (script that diffs tagged claims between stages) to `scripts/check_outputs.py`.

### L3. Named inference in blind mode: identification step (P1)
- New step after perceive: top three candidate identifications (event, era, kind of production), converging clues, confidence, kept as INFERRED. Failing to name a near-certain event is a defect, not caution.
- ASR convergence rule: when several passes give near-spellings of one proper noun and place, number, distance and year agree, treat the name as INFERRED high; match garbled strings against candidates derived from the other clues.
- Change: new stage in `workflows/blind_chain.js`; wording in the perceive prompt.

### L4. Unreadable print is never resolved from research (P1)
- Quote only what is legible at full size; list the rest as "unread". Never complete a name from research (the "R. Paping" case).
- Change: prompt rule in every agent that reads frames (`workflows/perceive.js`, `blind_chain.js`); `TOOLKIT.md` do-not-do list.

### L5. Open the frame at full size before interpreting it (P1)
- Pivotal frames (raised fist, look to camera, banner): record the literal description first, then the reading (the 2:47 "raised fist", the 3:07 indoor banner).
- Any colour, text or gesture claim in the final synthesis must cite a frame the author opened.
- Keep a standing do-not-claim list: fur, hand-lettering, sex of a person at 1 fps, role of men in caps, a pole read as a flag band.
- Change: perceive and report prompts (two-field "literal / reading" format); `workflows/coldread.js` to check citations; new `v1/DO_NOT_CLAIM.md` referenced from the prompts.

### L6. Guard the informed pass against its own priors (P1)
- Split `data/<video>/context.md` into `identity.md` (facts safe for reading pictures) and `reception.md` (interpretation, not for viewers), so research does not bias what the eyes report.
- Contextual claims in the opening paragraph must carry source and confidence from context; the sceptic must be asked which feelings come from the film and which from what the team was told.
- Change: `data/*/context.md` layout and the viewer-agent file lists in `workflows/interpret.js`, `compare.js`; sceptic prompt in `coldread.js`.

## P1: measurement tooling

### L7. Sub-second frame extraction from the mp4 (P1)
- `frames_1fps` labels can be about 0.5 s out. New script `scripts/frame_at.py <video> <t>` pulls a frame at a given time and records its PTS. All sub-second picture events come from it.
- Change: add the script; point agent prompts at it instead of frames_1fps for timing claims.

### L8. Replace the coarse shot detector (P1)
- Both runs retracted cut-rate and sync statistics because `shots.json` under-detects (missed the 1:28.55 hard cut, invented a dissolve, mis-split colour-cycling and fast shots).
- Build a lower-threshold pixel or histogram detector in `scripts/02_scenes.py`; verify manually at the main music edges; add a higher-frame-rate pass around every music-section boundary. Add a default "detector caveats" line to every report that uses shot counts.
- Dependency: `scripts/09_sync.py`, `09b_kick_grid.py` consume shot times and need re-running.

### L9. Text-on-screen extraction step (P1)
- New script (for example `scripts/10_onscreen_text.py`): find frames with print, save full-resolution crops to `data/<video>/text/` with legibility tags (legible / partial / unread). Headlines and signs are then read from this record, not argued by hand.

### L10. Treat Whisper as a hint (P1)
- Quote only digits, language ID and phrases that repeat across passes. Accept place names only with an on-screen sign. Flag known hallucinations ("MUZIEK", "Bedankt voor het kijken", "Dalmatians").
- Mask ASR output where the vocal stem is quiet or the content is music bleed ("Stuck", "End of the road", "Fafn"). Prefer a forced-language pass over auto-detect; mark time-of-day and other single-word items unreliable when passes disagree.
- Change: `scripts/03_whisper.py` (forced-language pass, vocal-stem energy mask, hallucination blacklist, per-segment `reliable` flag); lyric-reading prompts.

## P2: music reading

### L11. Per-stem evidence and exact end-of-track measurement (P2)
- Re-measure drums, bass, vocals and other separately around every claimed event: a "silence" can be a rhythm-section dropout and a boundary can show in one stem only (the 3:36.6 vocal density, the 2:37 dip and recovery). Output a section-boundary evidence table: each stem's change and which stem carries the boundary.
- End of a track: 10 ms envelope over the last 3 s; count hits from the waveform, not per-second RMS or stem passes.
- Any sync statistic names its grid (kick grid against tracker grid) and is checked against the kick inter-onset interval.
- Change: `scripts/07_audio_views.py`, `09_sync.py`, `09b_kick_grid.py`; the music prompt in `workflows/listen.js`.

### L12. Production-era check (P2)
- Add features: peaks near 0 dBFS, loop-machine regularity, sample-exact kick spread, band-limited sample against full-band mix. Lets a blind run say "modern production over older material" without outside data.
- Change: `scripts/04_audio_features.py` plus a line in the listen prompt.

### L13. Make music independence real (P2)
- Both lanes share the same stems and levels, so their agreement is weak. Give the blind lane a different feature view or a different analyst (for example CLAP tags and chroma only, or a different stem model).
- Change: `workflows/blind_chain.js` config; document in `TOOLKIT.md`.

### L14. Ban unmeasured emotive sound nouns (P2)
- No "heartbeat", "bell", "breath" unless a measured rate or figure sits beside it, or it is labelled metaphor. Add as a lint in `scripts/check_outputs.py` and in the listen and report prompts.

## P3: viewer and writing practice

### L15. Human-feel inputs (P3)
- Ask viewer agents for first-person attention and boredom notes and for changes of mind; these produced the most human-sounding blind material. Add a cold-viewer persona that sees only frames and the music reading, not the dossier (the six-persona panel on one dossier agrees weakly; the blind run listed this as unexamined).
- Change: persona list in `workflows/interpret.js`.

### L16. Research agenda from blind unknowns (P3)
- Auto-generate an "unknown / cannot determine" list from the blind run (source films, narrator, archival versus recreated voice) as the informed lane's research agenda. Change: final stage of `workflows/blind_chain.js` writes `data/<video>/unknowns.md`; research step reads it.

### L17. Opening paragraph last (P3)
- Write the opening paragraph after everything else: one plain "what this most probably is" sentence including INFERRED identifications, before hedged detail about gauge, lettering or stems. Change: `workflows/report.js` synthesis prompt.

## Suggested order
1. Prompt-only rules (L2 to L6, L14, L17): cheap, no new code.
2. Tools (L7, L9, L10, L8) then rerun sync scripts.
3. Workflow changes (L1, L3, L13, L15, L16) and music additions (L11, L12).
4. Cold-start test on a test video (`testvideos/`) with the revised toolkit.
