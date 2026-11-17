export const meta = {
  name: 'v1-report',
  description: 'Video-agnostic final step: turn the checked music reading + interpretation into a readable, human REPORT.md, then cold-read and revise it',
  phases: [{ title: 'Write' }, { title: 'Cold read' }, { title: 'Revise' }],
}
// args: { videos: ['video1'], out: 'analysis', compare: 'elfstedentocht_diptych' (optional) }
const R = '/home/user/Listener'
const OUT = `${R}/v1/${args.out || 'analysis'}`
const SUM = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const CR = { type: 'object', properties: { verdict: { type: 'string' }, problems: { type: 'array', items: { type: 'string' } } }, required: ['verdict', 'problems'] }
async function one(vid) {
  const F = `${OUT}/${vid}/REPORT.md`
  const src = `Sources (already fact-checked): ${OUT}/music/${vid}/music_reading.md (the music, primary), ${OUT}/${vid}/interpretation.md, ${OUT}/${vid}/dossier.md${args.compare ? `, ${OUT}/compare/${args.compare}/comparison.md` : ''}, v1/data/${vid}/context.md (unless blind), v1/data/${vid}/sync/sync.json. Repo ${R}.`
  await agent(`${src}

Write ${F}: the final, human report on ${vid}, for an intelligent reader who wants to understand how this music and video FEEL and what they MEAN, the way a perceptive critic or a moved listener would put it.
- Lead with the music. Then how the picture works with it. Then meaning and context. Then the moments that stay with you.
- Write flowing, vivid, precise prose (British English), not an evidence table. Keep timestamps (m:ss) so the reader can find moments.
- Every factual statement must come from the sources; do not add facts. Drop the H/M/L/OBS/INT tags in the prose, but keep honesty: where something is uncertain, say so in plain words ("probably", "the measurements suggest").
- Be clear that the music was "heard" through measurements (stems, spectrograms, chords, levels) and say once, briefly, what that means.
- End with "Where to look next": links to the detailed files.
- Length: 1,200-2,000 words.`, { label: `write:${vid}`, phase: 'Write', model: 'sonnet', schema: SUM })
  const crit = await parallel([
    ['feel', 'a music lover who has seen the video: does this capture how it actually feels? Where is it flat, robotic, over-hedged, or missing the obvious (the big riff, the emotional peak, the human story)?'],
    ['truth', 'a strict fact-checker: check 12 concrete claims against the source files and raw data (v1/data/' + vid + '/). List anything unsupported or wrong.'],
  ].map(([k, who]) => () => agent(`${src}\n\nYou are ${who}\nRead ${F}. Return a verdict and a list of concrete problems with suggested fixes.`, { label: `cold:${k}:${vid}`, phase: 'Cold read', model: 'sonnet', schema: CR })))
  await agent(`${src}\n\nRevise ${F} using these cold-read notes (verify each against the sources before acting; ignore notes that are wrong): ${JSON.stringify(crit.filter(Boolean))}\nKeep it readable and true. Append nothing about the revision to the report itself; add one line to v1/PROGRESS.md.`, { label: `revise:${vid}`, phase: 'Revise', model: 'sonnet', schema: SUM })
  return vid
}
return await parallel(args.videos.map(v => () => one(v)))
