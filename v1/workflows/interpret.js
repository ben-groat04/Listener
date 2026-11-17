export const meta = {
  name: 'v1-interpret',
  description: 'Video-agnostic: dossier -> multi-round conversing panel of human perspectives -> moderated synthesis -> adversarial fact-check, per video',
  phases: [
    { title: 'Dossier', detail: 'merge perceive notes into one timeline per video' },
    { title: 'Panel', detail: 'personas read each other and respond over several rounds' },
    { title: 'Synthesis', detail: 'moderator writes the interpretation' },
    { title: 'Verify', detail: 'lens-specific fact-checkers try to refute claims; corrections applied' },
  ],
}
// args: { videos: ['video1','video2'], rounds: 3, blind: false, out: 'analysis' }
// blind=true: agents must NOT read context.md, v1/analysis/research/, or use the web; they rely on sight/sound data only.
const R = '/home/user/Listener'
const OUT = `${R}/v1/${args.out || 'analysis'}`
const ROUNDS = args.rounds || 3
const BLIND = !!args.blind
const SUM = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const VER = { type: 'object', properties: { checked: { type: 'integer' }, refuted: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' } }, required: ['claim', 'evidence', 'fix'] } }, unverifiable: { type: 'array', items: { type: 'string' } } }, required: ['checked', 'refuted', 'unverifiable'] }

const base = vid => `You are analysing videos/${vid}.mp4 (a music video) in repo ${R} as part of a team trying to understand it the way thoughtful humans do: feeling, meaning, craft, context.
Raw data: v1/data/${vid}/ (contact_sheets/sheet_NN.jpg = 1 frame/s grids with timestamps, sheet NN covers (NN-1)*20..NN*20-1 s; frames_1fps/f_NNNN.jpg = second NNNN-1; scenes/; lyrics/; audio_features/; visual_features/; stems/ if present).
THE MUSIC COMES FIRST: read ${OUT}/music/${vid}/music_reading.md (the checked music analysis) before anything else, and read the picture in relation to the music.
Per-segment viewer notes: ${OUT}/perceive/${vid}/ (seg_NN.md, music.md, words.md) — note: perceive notes always live in v1/analysis/perceive/${vid}/ unless ${OUT}/perceive exists.
${BLIND ? 'BLIND MODE: do NOT read any context.md, anything under v1/analysis/research/, or any non-blind analysis, and do NOT use the web. Judge only from what can be seen and heard in the data. If the perceive notes contain outside facts (artist names, historical facts), treat them as unverified hearsay.' : `Context: v1/data/${vid}/context.md and v1/analysis/research/*.md (web research, cited).`}
Rules: British English. Accuracy over eloquence: never assert something you did not see in the frames or find in the data/sources; open frames yourself (Read tool) to check anything important; mark speculation. Use timestamps (m:ss).`

const PERSONAS = [
  ['first_timer', 'a first-time viewer with no special expertise: honest gut reactions, what grabs you, what bores or moves you, what you would tell a friend'],
  ['film_critic', 'a film and editing critic: shot choice, montage, rhythm of cuts against music, archive handling, colour, narrative construction, how the director builds feeling'],
  ['music_critic', 'a music critic and producer: arrangement, instrumentation, dynamics, structure, production choices, how music and voice/samples interact, genre lineage'],
  ['insider', BLIND ? 'a cultural reader who infers the world shown purely from visual and audio clues (era, place, language, customs), stating evidence for each inference' : 'a cultural insider and historian of the subject: what the events, places, words and images mean to people who lived or inherited them'],
  ['symbolist', 'a poet and symbolist: motifs, metaphors, visual rhymes, the emotional and philosophical subtext, what the piece is really about beneath the surface'],
  ['sceptic', 'a rigorous sceptic: check the others\' claims against the frames and data, flag over-reading, demand evidence, and offer the most down-to-earth reading'],
]

async function doVideo(vid) {
  const D = `${OUT}/${vid}`
  await agent(`${base(vid)}

YOUR JOB: build the master dossier for ${vid}. Read every perceive note for this video and merge them into ${D}/dossier.md:
1. One-paragraph overview.
2. A continuous timeline table (m:ss range | what we see | what we hear: words + music | notable craft/feeling), resolving contradictions between segment notes by opening the frames yourself.
3. Recurring motifs and where they occur.
4. The song's structure aligned with the picture.
5. The open questions raised by the viewers, deduplicated.
Write the file, return a summary.`, { label: `dossier:${vid}`, phase: 'Dossier', model: 'sonnet', schema: SUM })

  for (let r = 1; r <= ROUNDS; r++) {
    await parallel(PERSONAS.map(([key, who]) => () => agent(`${base(vid)}

You are ${who}. You are on a panel discussing ${vid}. Read ${D}/dossier.md first and dip into the perceive notes and frames as needed.
${r === 1
  ? `ROUND 1: give your own reading. Cover: what this piece is about, how it makes you feel and exactly which moments do it (timestamps), what is clever or weak, and 3 questions you want the other panellists to answer.`
  : `ROUND ${r}: read ALL panellists' round ${r - 1} statements in ${D}/panel/round_${r - 1}/. Respond like a real discussion: answer the questions put to you, say where you agree, push back where you disagree (with evidence: open frames, quote data), concede points you got wrong, and develop the most interesting thread further. ${r === ROUNDS ? 'This is the final round: end with your settled reading in 5 sentences and the single moment that best captures the piece.' : 'End with 2 new questions for specific panellists.'}`}
Write ${D}/panel/round_${r}/${key}.md (start with a heading naming yourself), then return a one-paragraph summary.`, { label: `r${r}:${key}:${vid}`, phase: 'Panel', model: 'sonnet', schema: SUM })))
    log(`${vid}: panel round ${r}/${ROUNDS} done`)
  }

  await agent(`${base(vid)}

YOUR JOB: moderator. Read ${D}/dossier.md and every file in ${D}/panel/ (all rounds). Write ${D}/interpretation.md, the definitive human reading of ${vid}:
- The piece in one paragraph (what it is, what it does to you).
- Emotional journey through the video, timestamped, explaining which sound/image choices create each feeling.
- Meaning and themes (consensus), with the strongest evidence for each.
- Live disagreements: present each side fairly.
- Craft notes: editing, music, archive, structure.
- Context that changes the reading${BLIND ? ' (as inferred from clues only)' : ''}.
- The moments a human would remember.
- What remains uncertain.
Keep every claim traceable to the panel or data; do not add new facts. Return a summary.`, { label: `moderator:${vid}`, phase: 'Synthesis', model: 'sonnet', schema: SUM })

  const lenses = [
    ['visual', 'every claim about what is on screen (objects, people, text, colours, cuts, timings): open the cited frames and contact sheets and check'],
    ['audio', 'every claim about music, sound, words, lyrics, translations and their timing: check against lyrics/, audio_features/, stems/ and run librosa if needed'],
    ['facts', BLIND ? 'every inference about era, place, culture: check it is justified by visible/audible evidence and labelled as inference' : 'every historical, biographical or cultural fact: check against v1/analysis/research/ and the web (WebSearch via ToolSearch), citing sources'],
  ]
  const verdicts = await parallel(lenses.map(([k, what]) => () => agent(`${base(vid)}

YOUR JOB: adversarial fact-checker (${k} lens). Read ${D}/interpretation.md. Try to REFUTE ${what}. Default to suspicion: a claim survives only if you confirm it. Return refuted claims with evidence and a corrected wording, and list claims that cannot be verified.`, { label: `verify:${k}:${vid}`, phase: 'Verify', model: 'sonnet', schema: VER })))
  const refuted = verdicts.filter(Boolean).flatMap(v => v.refuted)
  const unver = verdicts.filter(Boolean).flatMap(v => v.unverifiable)
  log(`${vid}: ${refuted.length} claims refuted, ${unver.length} unverifiable`)
  if (refuted.length || unver.length) {
    await agent(`${base(vid)}

Apply fact-check results to ${D}/interpretation.md. For each REFUTED claim, re-check it yourself (open the frame/data); if the refutation holds, fix the text; if it does not, keep the original and note why. For UNVERIFIABLE claims, soften the wording or mark them as speculation. Append a "Fact-check log" section listing each change. Also append the same log to v1/logs/ERRORS.md under a heading "Fact-check: ${vid} interpretation" (only real errors).
REFUTED: ${JSON.stringify(refuted)}
UNVERIFIABLE: ${JSON.stringify(unver)}`, { label: `apply-fixes:${vid}`, phase: 'Verify', model: 'sonnet', schema: SUM })
  }
  return { vid, refuted: refuted.length, unverifiable: unver.length }
}

const res = await parallel(args.videos.map(v => () => doVideo(v)))
return res
