export const meta = {
  name: 'v1-listen',
  description: 'Video-agnostic, music-first: per-window listeners -> specialist music panel that converses over rounds -> music reading -> adversarial audio fact-check',
  phases: [
    { title: 'Windows', detail: 'one Sonnet listener per 20 s window' },
    { title: 'Specialists', detail: 'harmony, rhythm, sound, voice, form, lineage, feeling' },
    { title: 'Debate', detail: 'specialists read and answer each other' },
    { title: 'Reading', detail: 'synthesis + refutation + fixes' },
  ],
}
// args: { root: optional repo root, videos: ['video1'] or [{vid, dur}] (dur auto-read from audio_features/summary.json), rounds: 2, blind: false, out: 'analysis', skip_windows: ['video1:0040', ...], windows_only: false }
// Root: no fallback. R is args.root, else the literal /home/user/Listener (not derived from the script location). Pass args.root for another checkout.
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs (__dirname/process undefined); pass args.root for another checkout
// Preflight: fail loudly before any agent is launched if the root is wrong (no fallback; default is the literal /home/user/Listener, pass args.root).
const ROOT_PROBE = `${R}/v1/scripts/check_outputs.py`
const ROOT_SCHEMA = { type: 'object', properties: { exists: { type: 'boolean' } }, required: ['exists'] }
const rootProbe = await agent(`Report whether this file exists (use ls or stat; do not read or edit it): ${ROOT_PROBE}`, { label: 'preflight:root', phase: 'Windows', model: 'sonnet', effort: 'low', schema: ROOT_SCHEMA })
if (!(rootProbe && rootProbe.exists)) throw new Error(`listen.js: ${ROOT_PROBE} not found, so root "${R}" is wrong (pass args.root = the repo path)`)
const OUT = `${R}/v1/${args.out || 'analysis'}`
const BLIND = !!args.blind
// Accept bare names or {vid, dur}; when dur is omitted an agent reads duration_s from v1/data/<vid>/audio_features/summary.json.
async function resolveVideos(list) {
  const vs = (list || []).map(v => (typeof v === 'string' ? { vid: v } : { ...v }))
  const need = vs.filter(v => !(v.dur > 0))
  if (need.length) {
    const got = await agent(`Read "duration_s" from ${R}/v1/data/<vid>/audio_features/summary.json for each of these videos: ${need.map(v => v.vid).join(', ')}. Return the numbers exactly as stored (do not invent any; omit a video whose file is missing).`, { label: 'durations', model: 'sonnet', effort: 'low', schema: { type: 'object', properties: { durations: { type: 'array', items: { type: 'object', properties: { vid: { type: 'string' }, dur: { type: 'number' } }, required: ['vid', 'dur'] } } }, required: ['durations'] } })
    for (const v of need) { const g = got && got.durations.find(d => d.vid === v.vid); if (g && g.dur > 0) v.dur = g.dur }
    const bad = need.filter(v => !(v.dur > 0)).map(v => v.vid)
    if (bad.length) throw new Error(`No duration for: ${bad.join(', ')} (pass {vid,dur} or run 04_audio_features.py first)`)
  }
  return vs
}
const VIDEOS = await resolveVideos(args.videos)
const ROUNDS = args.rounds || 2
const SUM = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const VER = { type: 'object', properties: { checked: { type: 'integer' }, refuted: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' } }, required: ['claim', 'evidence', 'fix'] } }, unverifiable: { type: 'array', items: { type: 'string' } } }, required: ['checked', 'refuted', 'unverifiable'] }
const pad4 = n => String(n).padStart(4, '0')
const mmss = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`

// Shared music-evidence rules (LESSONS L11, L12, L14 and the blind-honesty rule); appended to every listener, specialist, writer and checker prompt.
const MUSIC_RULES = `EVIDENCE RULES FOR MUSIC CLAIMS (all roles):
1. Production era. Judge whether the track reads as modern production laid over archive or older material, or as one period-consistent recording. Use measured cues only and name the figures you measured: peak level against 0 dBFS (true peaks or sample peaks near 0 dBFS suggest modern mastering or limiting), loop regularity (near-identical repeats of a bar or phrase suggest a loop machine or DAW), kick onset spread (how far kick onsets sit from a strict grid, measured from the drum stem), and band-limited sample against full-band mix (a narrow-band, noisy or low-fi layer sitting under or inside a full-range mix suggests older source material). Tag the judgement INFERRED with a confidence (high/medium/low). Never refuse to judge when the data clearly shows it: give the judgement, the figures and the confidence.
2. Blind honesty. A blind run must not refuse facts that are clearly heard or seen in the measurements or transcripts (a repeated, legible transcript phrase, an on-screen name, an unmistakable instrument range or tempo). A near-certain identification is a duty: state it, tag it INFERRED, confidence high, and give the evidence. Over-caution that withholds a well-evidenced fact counts as an error, just as an invented fact does.
3. Section boundaries. For every claimed section boundary or event, re-measure the four stems separately (drums, bass, vocals, other) around it and report a boundary evidence table: boundary time | drums change | bass change | vocals change | other change | which stem carries the boundary. A boundary may show in one stem only. A silence may be a rhythm-section dropout only (drums and bass out while voice or pad continue): check each stem and the full mix before using the word silence, and state the mix level drop in dB.
4. End of track. Measure the ending from a 10 ms envelope over the last 3 s of the audio (full mix and each stem), and count final hits from the waveform (peaks in the 10 ms envelope), not from per-second RMS or stem-separation passes. Give the time of the last audible sound and the level at the end.
5. Sync statistics. Any sync or alignment statistic (cuts or events against beats, kicks or bars) must name its grid (for example the kick grid, the tracker beat grid, or a fixed-tempo grid, with its BPM) and be checked against the kick inter-onset interval; a figure on a different grid from the kick spacing is not a sync result.
6. Emotive sound nouns. Do not use unmeasured emotive sound nouns such as heartbeat, bell, breath or sigh as descriptions of what is playing, unless a measured figure sits beside them (a rate in BPM or Hz, a frequency, a decay time) or they are explicitly labelled as metaphor (write: metaphor). Describe the sound by its measured properties first.
7. Confidence tags are carried, never lowered silently. If you take a claim from a colleague's file or an earlier round, keep its tag (measured, INFERRED, speculative, or high/medium/low); lower a tag only with a stated reason and the evidence for it. Do not raise one without new evidence either.
8. Not recoverable by measurement. (Every output carries a "not recoverable by measurement" list.) End your output with a short list headed "Not recoverable by measurement": things a listener may feel or assume that these measurements cannot settle (for example exact instrument identity, performer, recording date, intent, the real source of a sample), each with one line on why.`

const base = vid => `You are a music listener on a team trying to understand the MUSIC of videos/${vid}.mp4 the way a perceptive human listener would: what is playing, how it is built, and how it makes you feel. The music matters more than the picture here.
You cannot hear audio directly. Your "ears" are measurements in ${R}/v1/data/${vid}/ — use them all and cross-check them:
- music_views/window_NNNNs.png: per 20 s window, stacked mel-spectrograms of the mix and the demucs stems (vocals, drums, bass, other), chroma with estimated chords, and the lead (vocal-stem) pitch contour. LOOK at these images.
- music_views/chords.json, lead_notes.json, per_second_levels.json (dBFS, stereo width, per-stem dB), clap_tags.json (CLAP zero-shot genre/instrument/mood/voice/sound scores per 5 s; a noisy model, treat as weak evidence), clap.png, summary.json.
- stems/stem_rms_per_second.json, stems/stems.png; audio_features/ (tempo, beats, key, sections, overview.png, spectrogram.png); lyrics/ (transcripts, incl. a vocals-stem pass if present).
- You may run Python (librosa, numpy, scipy) on audio/song.wav or stems_raw/htdemucs/song/{vocals,drums,bass,other}.wav for any extra measurement (onsets, hpss, spectral bands, tempo curves, intervals). Keep runs short; save helpers in v1/scripts/agents/.
${BLIND ? 'BLIND MODE: do NOT read context.md, v1/analysis/research/, or non-blind analysis; no web. Judge from the measurements only.' : `Context (verify, don't assume): v1/data/${vid}/context.md and v1/analysis/research/.`}
Rules: British English. Every claim must cite its evidence (which measurement, which image, which time). Give confidence (high/medium/low). Be honest about what measurements cannot tell you (e.g. exact instrument identity). Timestamps m:ss.
${MUSIC_RULES}`

const WIN = []
for (const { vid, dur } of VIDEOS) for (let w = 0; w < dur; w += 20) if (!(args.skip_windows || []).includes(`${vid}:${pad4(w)}`)) WIN.push({ vid, w, to: Math.min(w + 20, Math.ceil(dur)) })

const listenWindow = x => agent(`${base(x.vid)}

YOUR JOB: listen closely to ${x.vid} from ${mmss(x.w)} to ${mmss(x.to)}. Open music_views/window_${pad4(x.w)}s.png (and the neighbouring windows' images briefly, for continuity). Read the slices of chords/lead_notes/levels/clap/stems/lyrics for this range.
Write ${OUT}/music/${x.vid}/win_${pad4(x.w)}.md:
- What is playing: which layers are present, entering, leaving (bass, drums, guitars/synths/"other", voice/samples), with times.
- Harmony & melody: chords/key centre, movement, any riff or motif (describe its shape), the lead line's range.
- Rhythm: pulse, density, drum pattern changes, fills, stops, tempo feel.
- Sound: brightness, distortion, reverb/space, stereo width, loudness changes.
- Voice/words: what is said or sung, how it sits in the mix, whether it is treated like an instrument.
- Per-stem boundary table for any change in this window (drums/bass/vocals/other, which stem carries it); if the window contains the end of the track, measure it as in rule 4.
- Production-era cues visible in this window (peak dBFS, loop regularity, kick onset spread, band-limited layers), tagged INFERRED with confidence.
- How this window moves the song on from the previous one (build, release, contrast).
- What a human listener feels here and why (tie each feeling to a measurable cause).
- End with "Not recoverable by measurement" (a short list for this window).`, { label: `win:${x.vid}:${pad4(x.w)}`, phase: 'Windows', model: 'sonnet', schema: SUM })

const SPECS = [
  ['harmony', 'harmony and melody: key centres, chord progressions and loops, modal colour, riffs/motifs and how they develop, melodic contour of any lead line'],
  ['rhythm', 'rhythm, tempo and groove: true tempo (resolve octave errors), metre, drum patterns, syncopation, accelerations, stops, how the pulse drives the feeling; any sync statistic must name its grid and be checked against the kick inter-onset interval'],
  ['sound', 'sound design and production: instrumentation (with evidence), timbre, distortion, space/reverb, stereo image, mix balance, loudness curve, and the production-era judgement (modern production over archive or older material, from measured cues, tagged INFERRED with confidence)'],
  ['voice', 'voice, words and samples: how speech/singing/sampled audio is placed, chopped, repeated, treated, and how words and music answer each other'],
  ['form', 'form and dynamics: the song map (intro/build/peak/breakdown/outro etc.) with timestamps, tension and release, the big moments and how they are engineered; include the per-stem section-boundary evidence table and the measured end of the track'],
  ['lineage', BLIND ? 'genre and lineage inferred purely from the sound: what it resembles, which traditions it draws on, with sonic evidence' : 'genre, lineage and the artist: where this sits in the artist\'s work and the wider genre, influences, what the artist was trying to do (cite sources)'],
  ['feeling', 'the feeling listener: a moment-by-moment emotional journey through the track as an ordinary attentive listener would experience it, tied to concrete musical causes'],
]

async function doVideo(vid) {
  const D = `${OUT}/music/${vid}`
  for (let r = 1; r <= ROUNDS + 1; r++) {
    await parallel(SPECS.map(([key, what]) => () => agent(`${base(vid)}

You are the ${key.toUpperCase()} specialist: ${what}.
${r === 1
  ? `Read ALL window notes in ${D}/win_*.md, then check them against the measurements yourself (open images, run Python). Write your full specialist analysis of the whole track. End with 3 questions for named fellow specialists (harmony, rhythm, sound, voice, form, lineage, feeling).`
  : `DEBATE ROUND ${r - 1}: read every specialist's previous file in ${D}/specialists/round_${r - 1}/. Answer questions put to you, correct mistakes (yours or theirs) with evidence, and connect your area to theirs (e.g. how the rhythm serves the form, how the sound creates the feeling). ${r === ROUNDS + 1 ? 'Final round: finish with your settled conclusions in 5 bullet points.' : 'End with 2 new questions for named specialists.'}`}
Write ${D}/specialists/round_${r}/${key}.md, then return a short summary.`, { label: `${key}:r${r}:${vid}`, phase: r === 1 ? 'Specialists' : 'Debate', model: 'sonnet', schema: SUM })))
    log(`${vid}: music specialists round ${r} done`)
  }

  await agent(`${base(vid)}

YOUR JOB: write the definitive human listening of ${vid}'s music: ${D}/music_reading.md. Read the window notes and every specialist file (all rounds). Sections:
1. The track in a paragraph (what it is, how it feels).
2. Song map table: m:ss range | section name | what's playing | what it feels like.
3. Harmony & melody. 4. Rhythm & groove. 5. Sound & production. 6. Voice, words & samples.
7. The emotional journey (moment by moment) and the musical causes.
8. The 5 moments a listener remembers, and why.
9. Where the specialists disagreed, and the best-supported view.
10. Uncertainties and what the measurements could not settle.
11. Section-boundary evidence table (per stem: drums, bass, vocals, other; what changes; which stem carries the boundary), and the measured end of the track (10 ms envelope, last 3 s, hits counted from the waveform).
12. Production-era judgement (modern production over archive/older material?) from measured cues, tagged INFERRED with confidence; blind runs state near-certain identifications as INFERRED high rather than refusing.
13. Not recoverable by measurement: a list of what a listener may feel or assume that these measurements cannot settle.
Carry every confidence tag from the notes unchanged unless you state a reason for lowering it. Do not use unmeasured emotive sound nouns (heartbeat, bell, breath) unless a figure sits beside them or they are labelled metaphor.
Do not add claims that are not supported by the notes or measurements.`, { label: `reading:${vid}`, phase: 'Reading', model: 'sonnet', schema: SUM })

  const lenses = [
    ['measure', 'every timing, chord, key, tempo, instrument-entry and loudness claim against the JSON measurements and images (run Python where needed)'],
    ['ears', 'every claim about instrumentation, timbre, voice and words: is it actually supported by stems, spectrograms, CLAP and transcripts, or is it guesswork dressed as fact?'],
  ]
  const verdicts = await parallel(lenses.map(([k, what]) => () => agent(`${base(vid)}

YOUR JOB: adversarial checker (${k}). Read ${D}/music_reading.md and try to REFUTE ${what}. A claim survives only if you confirm it. Also check against the EVIDENCE RULES: unmeasured emotive sound nouns (heartbeat, bell, breath), a sync statistic with no named grid, a silence that is really a rhythm-section dropout, an end-of-track claim not from a 10 ms envelope, a lowered confidence tag with no reason, an over-cautious refusal of a clearly evidenced fact, and a missing 'Not recoverable by measurement' list. Return refuted claims (with evidence and corrected wording) and unverifiable ones.`, { label: `check:${k}:${vid}`, phase: 'Reading', model: 'sonnet', schema: VER })))
  const refuted = verdicts.filter(Boolean).flatMap(v => v.refuted), unver = verdicts.filter(Boolean).flatMap(v => v.unverifiable)
  log(`${vid}: music reading - ${refuted.length} refuted, ${unver.length} unverifiable`)
  if (refuted.length || unver.length) await agent(`${base(vid)}

Apply checks to ${D}/music_reading.md. Re-verify each refuted claim yourself; fix it if the refutation holds, keep it (with a note) if not. Soften or label unverifiable claims. Append a "Check log" section. Append real errors to v1/logs/ERRORS.md under "Music check: ${vid}".
REFUTED: ${JSON.stringify(refuted)}
UNVERIFIABLE: ${JSON.stringify(unver)}`, { label: `fix:${vid}`, phase: 'Reading', model: 'sonnet', schema: SUM })
  return { vid, refuted: refuted.length, unverifiable: unver.length }
}

// windows for every video run first (pipeline per video: its windows, then its specialists)
const byVid = VIDEOS.map(v => v.vid)
const res = await parallel(byVid.map(vid => async () => {
  await parallel(WIN.filter(x => x.vid === vid).map(x => () => listenWindow(x)))
  if (args.windows_only) return { vid, windows_only: true }
  return doVideo(vid)
}))
return res
