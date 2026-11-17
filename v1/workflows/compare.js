export const meta = {
  name: 'v1-compare',
  description: 'Video-agnostic: compare a set of related videos (e.g. Part 1/Part 2) as a whole work, via a conversing panel, then synthesise and fact-check',
  phases: [{ title: 'Readings' }, { title: 'Debate' }, { title: 'Synthesis' }],
}
// args: { root: optional repo root, videos: ['video1','video2'], name: 'optional; default = videos joined with _', relation: 'optional, e.g. "video1 is Part 1, video2 is Part 2 (verify)"; default = derive from the context.md titles', blind: false, out: 'analysis', rounds: 2 }
// Root: args.root, else two directories up from this script (v1/workflows), else the working directory.
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs (__dirname/process undefined); pass args.root for another checkout
const OUT = `${R}/v1/${args.out || 'analysis'}`
const NAME = args.name || (args.videos || []).map(v => (typeof v === 'string' ? v : v.vid)).join('_')
const D = `${OUT}/compare/${NAME}`
const BLIND = !!args.blind
const SUM = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const VER = { type: 'object', properties: { refuted: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' } }, required: ['claim', 'evidence', 'fix'] } } }, required: ['refuted'] }
const vids = (args.videos || []).map(v => (typeof v === 'string' ? v : v.vid))
const base = `You are comparing related music videos as one body of work: ${vids.map(v => `videos/${v}.mp4`).join(', ')} in repo ${R}. Stated relation: ${args.relation || (BLIND ? 'unknown: infer it from the data' : 'not given: derive it from the track titles and notes in each v1/data/<video>/context.md')} (verify it).
For each video read, in this order: ${OUT}/music/<video>/music_reading.md (music comes first), ${OUT}/<video>/interpretation.md, ${OUT}/<video>/dossier.md; dip into raw data in v1/data/<video>/ (sync/sync.json = measured music-picture relationship; contact sheets, music_views images and JSON, lyrics) to check anything you claim.
${BLIND ? 'BLIND MODE: no context.md, no research, no web.' : 'Background: v1/data/<video>/context.md and v1/analysis/research/*.md.'}
Rules: British English; every claim traceable to data or the analysis files; mark speculation; timestamps as <video> m:ss.`

const LENSES = [
  ['music', 'the music: how the tracks relate (keys, tempi, instrumentation, motifs, energy, production), whether one answers the other, and what changes between them'],
  ['picture', 'the pictures: footage, colour vs b&w, editing styles, recurring images, how each video\'s visuals serve its track'],
  ['story', 'the story and meaning across the set: what each part covers, the arc from one to the next, why split it this way, what the whole says that a single part does not'],
  ['listener', 'the human experience of watching/hearing them in sequence: what you feel in each, what lingers, which works better and why'],
]
phase('Readings')
for (let r = 1; r <= (args.rounds || 2) + 1; r++) {
  await parallel(LENSES.map(([k, what]) => () => agent(`${base}

You focus on ${what}.
${r === 1 ? 'Write your comparative reading. End with 2 questions for named colleagues (music, picture, story, listener).' : `Round ${r}: read all colleagues' files in ${D}/round_${r - 1}/, answer their questions, challenge or build on their points with evidence. ${r === (args.rounds || 2) + 1 ? 'Final round: end with your settled view in 5 bullets.' : 'End with 1-2 new questions.'}`}
Write ${D}/round_${r}/${k}.md and return a summary.`, { label: `${k}:r${r}`, phase: r === 1 ? 'Readings' : 'Debate', model: 'sonnet', schema: SUM })))
  if (r === 1) phase('Debate')
}
phase('Synthesis')
await agent(`${base}

Read every file in ${D}/. Write ${D}/comparison.md: the set as one work (paragraph); side-by-side table (music, picture, words, mood, structure); how the parts talk to each other; the arc across the set; disagreements; what a human takes away. No new unsupported claims.`, { label: 'synthesis', phase: 'Synthesis', model: 'sonnet', schema: SUM })
const v = await agent(`${base}

Adversarially check ${D}/comparison.md: try to refute every factual claim (timings, keys, instruments, images, facts) against the data and source files. Return refuted claims with evidence and fixes.`, { label: 'check', phase: 'Synthesis', model: 'sonnet', schema: VER })
if (v && v.refuted.length) await agent(`${base}

Re-verify and apply these refutations to ${D}/comparison.md (fix where the refutation holds; append a "Check log"). Log real errors to v1/logs/ERRORS.md under "Compare check: ${NAME}". REFUTED: ${JSON.stringify(v.refuted)}`, { label: 'fix', phase: 'Synthesis', model: 'sonnet', schema: SUM })
return { refuted: v ? v.refuted.length : null }
