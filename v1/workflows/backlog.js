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
const done = []
for (let round = 1; round <= (args.rounds || 1); round++) {
  phase('Triage')
  const tri = await agent(`${intro}

You are the triage lead. Sources of work: ${(args.sources || []).join(', ')}. Focus: ${args.focus || 'highest value first, accuracy before style'}.
Already completed in earlier rounds of this run: ${JSON.stringify(done)}. Check the current files to see what is already fixed (other agents may have fixed items).
Pick up to ${args.per_round || 8} INDEPENDENT tasks (no two tasks may touch the same file), each completable by one agent in one go, each self-contained (exact files, exact change, how to verify). Prefer: factual corrections in deliverables, measurement re-runs that settle open claims, missing analysis layers, then docs. Record your selection and what remains in v1/logs/BACKLOG_${args.tag || 'bl'}_r${round}.md.`, { label: `triage:r${round}`, phase: 'Triage', model: 'sonnet', schema: T })
  if (!tri || !tri.tasks.length) break
  phase('Fix')
  const res = await pipeline(tri.tasks,
    t => agent(`${intro}\n\nYOUR TASK (${t.id}): ${t.task}\nFiles: ${t.files}\nDone when: ${t.done_when}\nVerify every fact against the data before writing it. Do not touch files outside your task's list. Append one line to v1/PROGRESS.md saying what changed.`, { label: `fix:${t.id}`, phase: 'Fix', model: 'sonnet', schema: SUM }),
    (s, t) => agent(`${intro}\n\nVerify this task was done properly and introduced no errors. TASK: ${t.task}\nDONE WHEN: ${t.done_when}\nWORKER SAID: ${s ? s.summary : 'nothing'}\nInspect the files and check facts against raw data. Fix small issues yourself; otherwise explain.`, { label: `verify:${t.id}`, phase: 'Verify', model: 'sonnet', schema: V }).then(v => ({ id: t.id, task: t.task.slice(0, 160), ok: v ? v.ok : false, notes: v ? v.notes.slice(0, 300) : 'verifier failed' })))
  res.filter(Boolean).forEach(r => done.push(r))
  log(`round ${round}: ${res.filter(r => r && r.ok).length}/${res.length} verified`)
}
return done
