export const meta = {
  name: 'v1-coldread',
  description: 'Cold-read improvement loop: fresh readers with different lenses audit the analysis/toolkit, a triage agent builds a backlog, workers fix the top items, verifiers check the fixes; repeat',
  phases: [{ title: 'Cold read' }, { title: 'Triage' }, { title: 'Fix' }, { title: 'Verify' }],
}
// args: { root: optional repo root, scope: 'analysis' | 'toolkit' | 'all', videos: ['video1','video2'], rounds: 1, fixes_per_round: 6, tag: 'cr1' }
// Root: args.root, else two directories up from this script (v1/workflows), else the working directory.
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs (__dirname/process undefined); pass args.root for another checkout
const TAG = args.tag || 'cr'
const SCOPE = args.scope || 'all'
const F = { type: 'object', properties: { findings: { type: 'array', items: { type: 'object', properties: { title: { type: 'string' }, where: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' }, severity: { type: 'string', enum: ['high', 'medium', 'low'] } }, required: ['title', 'where', 'problem', 'fix', 'severity'] } } }, required: ['findings'] }
const T = { type: 'object', properties: { tasks: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, task: { type: 'string' }, files: { type: 'string' }, done_when: { type: 'string' } }, required: ['id', 'task', 'files', 'done_when'] } } }, required: ['tasks'] }
const SUM = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const V = { type: 'object', properties: { ok: { type: 'boolean' }, notes: { type: 'string' } }, required: ['ok', 'notes'] }

const intro = `You are a COLD READER: you have never seen this project. Repo ${R}. Read CLAUDE.md, v1/INSTRUCTIONS.md (the user's rules and goal), v1/README.md, v1/PROGRESS.md, v1/logs/ERRORS.md first.
Scope: ${SCOPE === 'toolkit' ? 'the toolkit (v1/scripts, v1/workflows, docs) as something a fresh Claude session must run on a new video' : SCOPE === 'analysis' ? `the analysis outputs for ${(args.videos || []).map(v => (typeof v === 'string' ? v : v.vid)).join(', ')} under v1/analysis/ and v1/analysis_blind/` : 'both the analysis outputs (v1/analysis/, v1/analysis_blind/) and the toolkit (v1/scripts, v1/workflows, docs)'}.
Raw data for checking: v1/data/<video>/. Be specific: file, section, timestamp. British English.`
const READERS = [
  ['human', 'the user: someone who wants to understand how a perceptive human would FEEL and interpret this music and video. What is missing, shallow, robotic, over-technical, or unconvincing? What would a real fan or critic say that is absent?'],
  ['musician', 'a professional musician/producer: is the MUSIC analysis right and deep enough (structure, harmony, rhythm, sound, the samples as vocals)? What is wrong or missing? Check claims against v1/data/<video>/music_views and stems.'],
  ['auditor', 'an accuracy auditor: pick at least 15 specific factual claims across the outputs and check each against frames, measurements, transcripts or sources. Report every error or unsupported claim.'],
  ['engineer', 'a fresh Claude session asked to run this toolkit on a brand-new video: could you do it from the docs alone? What breaks, is undocumented, hard-coded to these videos, or fragile (container restarts, missing outputs, slow steps)?'],
  ['editor', 'an editor: organisation, duplication, contradictions between files, unclear final deliverables, whether a reader can find the definitive reading quickly.'],
]
for (let round = 1; round <= (args.rounds || 1); round++) {
  phase('Cold read')
  const reads = await parallel(READERS.map(([k, who]) => () => agent(`${intro}\n\nYour lens: ${who}\nReturn concrete findings with fixes (most severe first).`, { label: `cold:${k}:r${round}`, phase: 'Cold read', model: 'sonnet', schema: F })))
  const findings = reads.filter(Boolean).flatMap((r, i) => r.findings.map(f => ({ ...f, reader: READERS[i][0] })))
  log(`round ${round}: ${findings.length} findings`)
  if (!findings.length) break
  phase('Triage')
  const tri = await agent(`${intro}\n\nYou are the triage lead. Here are cold-read findings: ${JSON.stringify(findings)}\nDeduplicate, drop wrong or trivial ones, and write the backlog to v1/logs/BACKLOG_${TAG}_r${round}.md (all items, with reader and severity). Return the top ${args.fixes_per_round || 6} independent, high-value tasks that a single agent can complete in one go (no two tasks may edit the same file). Each task must be self-contained and say exactly which files to change and how to know it is done.`, { label: `triage:r${round}`, phase: 'Triage', model: 'sonnet', schema: T })
  if (!tri || !tri.tasks.length) break
  phase('Fix')
  const done = await pipeline(tri.tasks,
    t => agent(`${intro}\n\nYOUR TASK (${t.id}): ${t.task}\nFiles: ${t.files}\nDone when: ${t.done_when}\nDo the work carefully; verify facts against the data. NOTE: v1/workflows/*.js are Workflow-tool scripts: plain JavaScript with NO Node APIs (no require, process, __dirname, fs, Date.now, Math.random); keep \`export const meta\` a pure literal. Append one line to v1/PROGRESS.md describing what you changed. Return a summary.`, { label: `fix:${t.id}`, phase: 'Fix', model: 'sonnet', schema: SUM }),
    (s, t) => agent(`${intro}\n\nVerify that this task was done properly and did not introduce errors: TASK ${t.task}\nDONE WHEN: ${t.done_when}\nWORKER SAID: ${s ? s.summary : 'nothing'}\nInspect the files. If not ok, fix small issues yourself; otherwise explain.`, { label: `verify:${t.id}`, phase: 'Verify', model: 'sonnet', schema: V }).then(v => ({ id: t.id, ok: v ? v.ok : false, notes: v ? v.notes : 'verifier failed' })))
  log(`round ${round}: ${done.filter(d => d && d.ok).length}/${done.length} fixes verified`)
}
return 'done'
