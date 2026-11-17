export const meta = {
  name: 'v1-blindcmp',
  description: 'Compare blind (no context) and informed analyses of the same video: what the blind run got right, missed, or invented; lessons for the toolkit',
  phases: [{ title: 'Compare' }, { title: 'Lessons' }],
}
// args: { videos: ['video1','video2'], root: optional }
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs (__dirname/process undefined); pass args.root for another checkout
const SUM = { type: 'object', properties: { summary: { type: 'string' }, lessons: { type: 'array', items: { type: 'string' } } }, required: ['summary', 'lessons'] }
phase('Compare')
const res = await parallel(args.videos.map(vid => () => agent(`Repo ${R}. Compare two independent analyses of ${vid}:
- BLIND (no context, no research, no web): v1/analysis_blind/music/${vid}/music_reading.md, v1/analysis_blind/${vid}/interpretation.md (and dossier.md, perceive/).
- INFORMED: v1/analysis/music/${vid}/music_reading.md, v1/analysis/${vid}/interpretation.md, v1/analysis/${vid}/REPORT.md if present.
Check disputed points against raw data in v1/data/${vid}/ (frames, music_views, lyrics) rather than trusting either side.
Write v1/analysis/blind_vs_informed/${vid}.md:
1. What the blind run worked out on its own (subject, era, place, emotion, structure), with how it inferred each.
2. What it got wrong or invented, and why (which data misled it).
3. What the informed run got wrong that the blind run got right (context can bias too).
4. Music: do the two music readings agree on structure, instrumentation, peaks? Where they differ, which does the data support?
5. Human feel: which reads more like a person responding to the work?
6. Concrete lessons for the toolkit (prompts, tools, workflow steps) so blind runs on unknown videos get closer to the truth.
British English. Return a summary and the lessons.`, { label: `blindcmp:${vid}`, phase: 'Compare', model: 'sonnet', schema: SUM })))
phase('Lessons')
await agent(`Repo ${R}. Read v1/analysis/blind_vs_informed/*.md and these lessons: ${JSON.stringify(res.filter(Boolean).flatMap(r => r.lessons))}
Write v1/analysis/blind_vs_informed/LESSONS.md: deduplicated, prioritised lessons for making the toolkit work on unknown videos, each with the specific file/prompt/step to change. Do not edit the toolkit yourself. Add one line to v1/PROGRESS.md.`, { label: 'lessons', phase: 'Lessons', model: 'sonnet', schema: { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] } })
return res.filter(Boolean).map(r => r.summary)
