export const meta = {
  name: 'v1-backlog',
  description: 'Work an existing backlog: triage lead picks independent tasks (no shared files) from backlog/lesson files, workers fix, verifiers check; repeat for N rounds',
  phases: [{ title: 'Triage' }, { title: 'Fix' }, { title: 'Verify' }],
}
// args: { sources: ['v1/logs/BACKLOG_cr1_r1.md', 'v1/analysis/blind_vs_informed/LESSONS.md'], focus: 'text', rounds: 2, per_round: 8, tag: 'bl1', root: optional }
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs
const T = { type: 'object', properties: { tasks: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, task: { type: 'string' }, files: { type: 'string' }, done_when: { type: 'string' } }, required: ['id', 'task', 'files', 'done_when'] } } }, required: ['tasks'] }
const SUM = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const V = { type: 'object', properties: { ok: { type: 'boolean' }, notes: { type: 'string' } }, required: ['ok', 'notes'] }
const intro = `Repo ${R}. Read CLAUDE.md, v1/INSTRUCTIONS.md, v1/logs/ERRORS.md first (rules: music first, accuracy first, video-agnostic toolkit, British English). Raw data per video: v1/data/<video>/. Workflow scripts (v1/workflows/*.js) are plain JavaScript run by a Workflow tool with NO Node APIs (no require/process/__dirname/fs/Date.now/Math.random) and \`export const meta\` must stay a pure literal. Files under v1/analysis*/<video>/REPORT.md are repository deliverables: you may write them.`
const CHK = { type: 'object', properties: { files: { type: 'array', items: { type: 'object', properties: { path: { type: 'string' }, exists: { type: 'boolean' }, bytes: { type: 'integer' } }, required: ['path', 'exists', 'bytes'] } } }, required: ['files'] }
async function exists(paths, label) {
  const r = await agent(`For each of these paths (repo ${R}; relative paths are relative to it), report whether the file exists and its size in bytes (use ls -l or stat; do not read or edit them): ${JSON.stringify(paths)}`, { label, phase: 'Triage', model: 'sonnet', effort: 'low', schema: CHK })
  return paths.map(p => { const f = r && r.files.find(x => x.path === p); return { path: p, ok: !!(f && f.exists && f.bytes > 0) } })
}
// Preflight: every source file must exist; fail clearly before any triage agent runs. (No per-video duration is used by this workflow.)
if (!(args.sources || []).length) throw new Error('backlog.js: args.sources is empty; pass e.g. { sources: ["v1/logs/BACKLOG_x.md"] }')
const pre = await exists(args.sources.map(s => (s.startsWith('/') ? s : `${R}/${s}`)), 'preflight')
const missing = pre.filter(x => !x.ok).map(x => x.path)
if (missing.length) throw new Error(`backlog.js: missing source files, nothing launched:\n${missing.join('\n')}`)
const done = []
for (let round = 1; round <= (args.rounds || 1); round++) {
  phase('Triage')
  const BL = `${R}/v1/logs/BACKLOG_${args.tag || 'bl'}_r${round}.md`
  const triage = note => agent(`${intro}

You are the triage lead. Sources of work: ${(args.sources || []).join(', ')}. Focus: ${args.focus || 'highest value first, accuracy before style'}.
Already completed in earlier rounds of this run: ${JSON.stringify(done)}. Check the current files to see what is already fixed (other agents may have fixed items).
Pick up to ${args.per_round || 8} INDEPENDENT tasks (no two tasks may touch the same file), each completable by one agent in one go, each self-contained (exact files, exact change, how to verify). Prefer: factual corrections in deliverables, measurement re-runs that settle open claims, missing analysis layers, then docs. Record your selection and what remains in v1/logs/BACKLOG_${args.tag || 'bl'}_r${round}.md. When a task rests on a tagged claim (H/M/L, OBS/INT, near-certain/probable/possible), carry the tag into the task text; never lower a tag without a stated reason.${note}`, { label: `triage:r${round}`, phase: 'Triage', model: 'sonnet', schema: T })
  const tri = await triage('')
  if (tri && tri.tasks.length && !(await exists([BL], `exists:r${round}`))[0].ok) { log(`${BL} missing after triage; retrying once`); await triage('\nA previous attempt did not write the backlog record. You MUST create the file with the Write tool at the exact path above.') }
  if (!tri || !tri.tasks.length) break
  phase('Fix')
  const res = await pipeline(tri.tasks,
    t => agent(`${intro}\n\nYOUR TASK (${t.id}): ${t.task}\nFiles: ${t.files}\nDone when: ${t.done_when}\nVerify every fact against the data before writing it. When you synthesise or edit text that carries confidence tags (H/M/L, OBS/INT), keep them: no lowering without a stated reason. Do not touch files outside your task's list. Append one line to v1/PROGRESS.md saying what changed.`, { label: `fix:${t.id}`, phase: 'Fix', model: 'sonnet', schema: SUM }),
    (s, t) => agent(`${intro}\n\nVerify this task was done properly and introduced no errors. TASK: ${t.task}\nDONE WHEN: ${t.done_when}\nWORKER SAID: ${s ? s.summary : 'nothing'}\nInspect the files and check facts against raw data. Fix small issues yourself; otherwise explain.`, { label: `verify:${t.id}`, phase: 'Verify', model: 'sonnet', schema: V }).then(v => ({ id: t.id, task: t.task.slice(0, 160), ok: v ? v.ok : false, notes: v ? v.notes.slice(0, 300) : 'verifier failed' })))
  res.filter(Boolean).forEach(r => done.push(r))
  log(`round ${round}: ${res.filter(r => r && r.ok).length}/${res.length} verified`)
}
return done
