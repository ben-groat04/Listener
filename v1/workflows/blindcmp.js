export const meta = {
  name: 'v1-blindcmp',
  description: 'Final stage of a blind-first run: diff frozen blind claims against informed outputs (time and count claims especially), decide disagreements from raw data, report what blind got right, missed or invented; lessons for the toolkit',
  phases: [{ title: 'Compare' }, { title: 'Lessons' }],
}
// args: { videos: ['video1','video2'], root: optional }
// Documented default FINAL stage of the blind pipeline: blind_chain.js calls it when args.compare_after is true (set it for every
// blind-first run). It can also be run alone on any video that has blind and informed outputs.
// When v1/data/<vid>/blind_frozen.md exists, its claims are diffed against the informed outputs (and informed_extension.md);
// every disagreement on a time or count is decided from RAW DATA in v1/data/<vid>/, never from either analysis's say-so.
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs (__dirname/process undefined); pass args.root for another checkout
// Preflight: fail loudly before any agent is launched if the root is wrong (no fallback; default is the literal /home/user/Listener, pass args.root).
const ROOT_PROBE = `${R}/v1/scripts/check_outputs.py`
const ROOT_SCHEMA = { type: 'object', properties: { exists: { type: 'boolean' } }, required: ['exists'] }
const rootProbe = await agent(`Report whether this file exists (use ls or stat; do not read or edit it): ${ROOT_PROBE}`, { label: 'preflight:root', phase: 'Compare', model: 'sonnet', effort: 'low', schema: ROOT_SCHEMA })
if (!(rootProbe && rootProbe.exists)) throw new Error(`blindcmp.js: ${ROOT_PROBE} not found, so root "${R}" is wrong (pass args.root = the repo path)`)
const SUM = { type: 'object', properties: { summary: { type: 'string' }, lessons: { type: 'array', items: { type: 'string' } } }, required: ['summary', 'lessons'] }
phase('Compare')
const res = await parallel(args.videos.map(vid => () => agent(`Repo ${R}. Compare two independent analyses of ${vid}:
- BLIND (no context, no research, no web): v1/analysis_blind/music/${vid}/music_reading.md, v1/analysis_blind/${vid}/interpretation.md (and dossier.md, perceive/).
- FROZEN blind claims, if present: v1/data/${vid}/blind_frozen.md (read-only; never edit) and v1/data/${vid}/unknowns.md.
- INFORMED: v1/analysis/music/${vid}/music_reading.md, v1/analysis/${vid}/interpretation.md, v1/analysis/${vid}/REPORT.md if present, and v1/data/${vid}/informed_extension.md if present.
Step A, claim diff. If blind_frozen.md exists, list every frozen claim about a TIME (section starts/ends, moment positions) or a COUNT (number of shots, sections, people, repeats) and the matching informed claim. For each pair mark AGREE / DISAGREE / NOT COVERED. Decide every DISAGREE from raw data in v1/data/${vid}/ (scenes/shots.json, lyrics/ASR, audio_features, music_views, sync, frames), re-deriving the number from the file, and say which side the data supports, quoting the file and value. Raw data decides disagreements, not either analysis.
Step B, check other disputed points against the raw data in v1/data/${vid}/ (frames, music_views, lyrics) rather than trusting either side.
Write v1/analysis/blind_vs_informed/${vid}.md:
1. What the blind run worked out on its own (subject, era, place, emotion, structure), with how it inferred each; and whether the frozen identification named the event the data makes near-certain.
2. What it got wrong or invented, and why (which data misled it).
3. What the informed run got wrong that the blind run got right (context can bias too).
4. Frozen-claim diff table (time and count claims) with the raw-data verdict for each disagreement.
5. Music: do the two music readings agree on structure, instrumentation, peaks? Where they differ, which does the data support?
6. Human feel: which reads more like a person responding to the work?
7. Concrete lessons for the toolkit (prompts, tools, workflow steps) so blind runs on unknown videos get closer to the truth.
British English. Return a summary and the lessons.`, { label: `blindcmp:${vid}`, phase: 'Compare', model: 'sonnet', schema: SUM })))
phase('Lessons')
await agent(`Repo ${R}. Read v1/analysis/blind_vs_informed/*.md and these lessons: ${JSON.stringify(res.filter(Boolean).flatMap(r => r.lessons))}
Write v1/analysis/blind_vs_informed/LESSONS.md: deduplicated, prioritised lessons for making the toolkit work on unknown videos, each with the specific file/prompt/step to change. Do not edit the toolkit yourself. Add one line to v1/PROGRESS.md.`, { label: 'lessons', phase: 'Lessons', model: 'sonnet', schema: { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] } })
return res.filter(Boolean).map(r => r.summary)
