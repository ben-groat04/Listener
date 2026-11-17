export const meta = {
  name: 'v1-blind-chain',
  description: 'Blind end-to-end run (no context, no research, no web): perceive -> listen -> interpret, output to v1/analysis_blind/, then a leak check against context.md terms',
  phases: [{ title: 'Blind perceive' }, { title: 'Blind listen' }, { title: 'Blind interpret' }, { title: 'Leak check' }],
}
// args: { root: optional repo root, videos: ['video1'] or [{vid, dur}] (dur auto-read when omitted), video_dir: 'videos' }
// Root: args.root, else two directories up from this script (v1/workflows), else the working directory.
const R = (args && args.root) || (typeof __dirname !== 'undefined' ? __dirname.replace(/\/v1\/workflows$/, '') : (typeof process !== 'undefined' && process.cwd ? process.cwd() : '.'))  // runtime may lack Node APIs: falls back to '.' (agent cwd = repo root)
const W = `${R}/v1/workflows`
const common = { blind: true, out: 'analysis_blind', video_dir: args.video_dir || 'videos', root: R }
const VID_NAMES = (args.videos || []).map(v => (typeof v === 'string' ? v : v.vid))
phase('Blind perceive')
await workflow({ scriptPath: `${W}/perceive.js` }, { ...common, videos: args.videos })
phase('Blind listen')
await workflow({ scriptPath: `${W}/listen.js` }, { ...common, videos: args.videos, rounds: 2 })
phase('Blind interpret')
const r = await workflow({ scriptPath: `${W}/interpret.js` }, { ...common, videos: VID_NAMES, rounds: 3 })

// Leak check: blind outputs must not contain facts that only context.md knows (artist, commission, MusicBrainz, part number).
phase('Leak check')
const LEAK = { type: 'object', properties: { terms: { type: 'array', items: { type: 'string' } }, hits: { type: 'array', items: { type: 'object', properties: { file: { type: 'string' }, line: { type: 'integer' }, term: { type: 'string' }, text: { type: 'string' } }, required: ['file', 'term', 'text'] } } }, required: ['terms', 'hits'] }
const leaks = await parallel(VID_NAMES.map(vid => () => agent(`Leak check for ${vid} (repo ${R}). You are the only agent allowed to read v1/data/${vid}/context.md in this blind run, and only to extract terms.
1. Read v1/data/${vid}/context.md and list the context-only terms: the artist/band name and member names, the track title, the commissioning body/festival/event, the archive source, plus always 'MusicBrainz' and 'Part 1' / 'Part One' / 'Part 2' / 'Part Two' (case-insensitive).
2. grep -rniF for each term in ${R}/v1/analysis_blind/ (all files for ${vid}: perceive/${vid}, music/${vid}, ${vid}/, and compare/ if present; skip leak_check files).
3. Write ${R}/v1/analysis_blind/leak_check_${vid}.md listing terms searched and every hit (file:line, term, the line), or "no hits".
Return the terms and hits. Do NOT edit any blind output.`, { label: `leak:${vid}`, phase: 'Leak check', model: 'sonnet', effort: 'low', schema: LEAK })))
const hits = leaks.filter(Boolean).flatMap(l => l.hits)
log(`leak check: ${hits.length} hit(s) in blind outputs${hits.length ? ' - see v1/analysis_blind/leak_check_<video>.md' : ''}`)
return { interpret: r, leak_hits: hits, leak_checked: leaks.filter(Boolean).length + '/' + VID_NAMES.length }
