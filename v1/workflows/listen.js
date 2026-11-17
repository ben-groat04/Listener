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
// args: { videos: [{vid, dur}], rounds: 2, blind: false, out: 'analysis', skip_windows: ['video1:0040', ...], windows_only: false }
const R = '/home/user/Listener'
const OUT = `${R}/v1/${args.out || 'analysis'}`
const BLIND = !!args.blind
const ROUNDS = args.rounds || 2
const SUM = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const VER = { type: 'object', properties: { checked: { type: 'integer' }, refuted: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' } }, required: ['claim', 'evidence', 'fix'] } }, unverifiable: { type: 'array', items: { type: 'string' } } }, required: ['checked', 'refuted', 'unverifiable'] }
const pad4 = n => String(n).padStart(4, '0')
const mmss = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`

const base = vid => `You are a music listener on a team trying to understand the MUSIC of videos/${vid}.mp4 the way a perceptive human listener would: what is playing, how it is built, and how it makes you feel. The music matters more than the picture here.
You cannot hear audio directly. Your "ears" are measurements in ${R}/v1/data/${vid}/ — use them all and cross-check them:
- music_views/window_NNNNs.png: per 20 s window, stacked mel-spectrograms of the mix and the demucs stems (vocals, drums, bass, other), chroma with estimated chords, and the lead (vocal-stem) pitch contour. LOOK at these images.
- music_views/chords.json, lead_notes.json, per_second_levels.json (dBFS, stereo width, per-stem dB), clap_tags.json (CLAP zero-shot genre/instrument/mood/voice/sound scores per 5 s; a noisy model, treat as weak evidence), clap.png, summary.json.
- stems/stem_rms_per_second.json, stems/stems.png; audio_features/ (tempo, beats, key, sections, overview.png, spectrogram.png); lyrics/ (transcripts, incl. a vocals-stem pass if present).
- You may run Python (librosa, numpy, scipy) on audio/song.wav or stems_raw/htdemucs/song/{vocals,drums,bass,other}.wav for any extra measurement (onsets, hpss, spectral bands, tempo curves, intervals). Keep runs short; save helpers in v1/scripts/agents/.
${BLIND ? 'BLIND MODE: do NOT read context.md, v1/analysis/research/, or non-blind analysis; no web. Judge from the measurements only.' : `Context (verify, don't assume): v1/data/${vid}/context.md and v1/analysis/research/.`}
Rules: British English. Every claim must cite its evidence (which measurement, which image, which time). Give confidence (high/medium/low). Be honest about what measurements cannot tell you (e.g. exact instrument identity). Timestamps m:ss.`

const WIN = []
for (const { vid, dur } of args.videos) for (let w = 0; w < dur; w += 20) if (!(args.skip_windows || []).includes(`${vid}:${pad4(w)}`)) WIN.push({ vid, w, to: Math.min(w + 20, Math.ceil(dur)) })

const listenWindow = x => agent(`${base(x.vid)}

YOUR JOB: listen closely to ${x.vid} from ${mmss(x.w)} to ${mmss(x.to)}. Open music_views/window_${pad4(x.w)}s.png (and the neighbouring windows' images briefly, for continuity). Read the slices of chords/lead_notes/levels/clap/stems/lyrics for this range.
Write ${OUT}/music/${x.vid}/win_${pad4(x.w)}.md:
- What is playing: which layers are present, entering, leaving (bass, drums, guitars/synths/"other", voice/samples), with times.
- Harmony & melody: chords/key centre, movement, any riff or motif (describe its shape), the lead line's range.
- Rhythm: pulse, density, drum pattern changes, fills, stops, tempo feel.
- Sound: brightness, distortion, reverb/space, stereo width, loudness changes.
- Voice/words: what is said or sung, how it sits in the mix, whether it is treated like an instrument.
- How this window moves the song on from the previous one (build, release, contrast).
- What a human listener feels here and why (tie each feeling to a measurable cause).`, { label: `win:${x.vid}:${pad4(x.w)}`, phase: 'Windows', model: 'sonnet', schema: SUM })

const SPECS = [
  ['harmony', 'harmony and melody: key centres, chord progressions and loops, modal colour, riffs/motifs and how they develop, melodic contour of any lead line'],
  ['rhythm', 'rhythm, tempo and groove: true tempo (resolve octave errors), metre, drum patterns, syncopation, accelerations, stops, how the pulse drives the feeling'],
  ['sound', 'sound design and production: instrumentation (with evidence), timbre, distortion, space/reverb, stereo image, mix balance, loudness curve, era/style of production'],
  ['voice', 'voice, words and samples: how speech/singing/sampled audio is placed, chopped, repeated, treated, and how words and music answer each other'],
  ['form', 'form and dynamics: the song map (intro/build/peak/breakdown/outro etc.) with timestamps, tension and release, the big moments and how they are engineered'],
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
Do not add claims that are not supported by the notes or measurements.`, { label: `reading:${vid}`, phase: 'Reading', model: 'sonnet', schema: SUM })

  const lenses = [
    ['measure', 'every timing, chord, key, tempo, instrument-entry and loudness claim against the JSON measurements and images (run Python where needed)'],
    ['ears', 'every claim about instrumentation, timbre, voice and words: is it actually supported by stems, spectrograms, CLAP and transcripts, or is it guesswork dressed as fact?'],
  ]
  const verdicts = await parallel(lenses.map(([k, what]) => () => agent(`${base(vid)}

YOUR JOB: adversarial checker (${k}). Read ${D}/music_reading.md and try to REFUTE ${what}. A claim survives only if you confirm it. Return refuted claims (with evidence and corrected wording) and unverifiable ones.`, { label: `check:${k}:${vid}`, phase: 'Reading', model: 'sonnet', schema: VER })))
  const refuted = verdicts.filter(Boolean).flatMap(v => v.refuted), unver = verdicts.filter(Boolean).flatMap(v => v.unverifiable)
  log(`${vid}: music reading - ${refuted.length} refuted, ${unver.length} unverifiable`)
  if (refuted.length || unver.length) await agent(`${base(vid)}

Apply checks to ${D}/music_reading.md. Re-verify each refuted claim yourself; fix it if the refutation holds, keep it (with a note) if not. Soften or label unverifiable claims. Append a "Check log" section. Append real errors to v1/logs/ERRORS.md under "Music check: ${vid}".
REFUTED: ${JSON.stringify(refuted)}
UNVERIFIABLE: ${JSON.stringify(unver)}`, { label: `fix:${vid}`, phase: 'Reading', model: 'sonnet', schema: SUM })
  return { vid, refuted: refuted.length, unverifiable: unver.length }
}

// windows for every video run first (pipeline per video: its windows, then its specialists)
const byVid = args.videos.map(v => v.vid)
const res = await parallel(byVid.map(vid => async () => {
  await parallel(WIN.filter(x => x.vid === vid).map(x => () => listenWindow(x)))
  if (args.windows_only) return { vid, windows_only: true }
  return doVideo(vid)
}))
return res
