// Workflow 4 (overnight): full review of the whole project so far, then work chosen by the agents, then final report.
// NOTE: do NOT message running workflow agents from the main session (the user's latest message is auto-forwarded; extra messages steer them).
// Launch only right after a neutral message ("go"). Pre-launch audit must check every item in .claude/workflow-notes.md is reflected.
// Concurrency: the Workflow runtime runs at most 2 agents at once on this 4-core box, so builders (and their devil's advocates) are queued, not truly parallel beyond 2.
export const meta = {
  name: 'taste-workflow-4',
  description: 'Workflow 4: whole-project review by reviewers, Opus research lead decides direction, engineer + 2 builders + 2 devil\'s advocates, lead reviews, round 2, final report',
  phases: [
    { title: 'Review', detail: '2 reviewers (Sonnet) + research lead (Opus)', model: 'opus' },
    { title: 'Round 1', detail: 'engineer + builders + 2 devil\'s advocates', model: 'sonnet' },
    { title: 'Lead review', detail: 'research lead (Opus)', model: 'opus' },
    { title: 'Round 2', detail: 'engineer + builders + 2 devil\'s advocates', model: 'sonnet' },
    { title: 'Final', detail: 'research lead (Opus) final report', model: 'opus' },
  ],
}

const ROOT = '/home/user/Listener'
const PROJ = ROOT + '/taste-model'
const SCRATCH = '/tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf4'
const S = 'sonnet', O = 'opus'
// Workflow 3 documents (checked: contain no sealed-fold results; exported verbatim from the W3 journal, engineer-r1 from the W3 script):
const W3_RESULTS = PROJ + '/RESULTS.md'
const W3_DIR = PROJ + '/reports/w3'
const W3_REPORTS = ['engineer-r1', 'engineer-r2', 'builder-r1-content-audio', 'builder-r1-song-content-beyond-audio', 'builder-r1-training-signal', 'builder-r2-audio-taste', 'builder-r2-integrated', 'devils-advocate-r1-works', 'devils-advocate-r1-dismissed', 'devils-advocate-r2-works', 'devils-advocate-r2-dismissed', 'research-lead-plan', 'research-lead-review', 'research-lead-final'].map(n => W3_DIR + '/' + n + '.md').join('\n  ')

// Process limits (wall-clock minutes). One place only; prompts and the lead schema read these.
const SHARED = PROJ + '/.cache/shared'
const PREP_MAX = 120          // shared prep step hard cap
const R1_BUILDER_MAX = 120, R2_BUILDER_MAX = 90
const BUILDER_MIN = 40        // floor for every builder (both rounds), see checklist
const DA_MIN = 20, DA_MAX = 60
const LATE_CAP = 2            // max --late runs per predictor hash, enforced in run.py by the engineer

// Single source of truth for folder and path names. Briefs written by the lead must not name folders; these win on any conflict.
const scratchOf = (label) => SCRATCH + '/' + label
const predOf = (round, id) => PROJ + '/predictors/w4r' + round + '-' + id

const CONTEXT = `
## The user's words on this project (verbatim)
- "I want a workflow set up to attempt to analyse my music taste and do as well as possible on predicting new songs I haven't listened to. I guess you can create training sets based on say my listening up to a certain date and see how well it gets some of my favourite tracks after that. DO NOT STEER THE WORKFLOW IN ANY WAY it will decide on the best way to do it itself with research etc. It needs to analyse the music deeply, not just by artist etc. you'll need a devils advocate in there because otherwise it'll default to assuming artist etc is a good way of predicting."
- "A lot of songs I like for specific parts of the music. This is something you'll have to work out. Again, DO NOT USE THIS TO STEER."
- "Use all the music there then. Ofc taste changed a lot early on so idk how useful the proper old stuff will be, but analysis will tell."
- "Liked songs was only a proxy of what I listened to. And I thought playlists were on there?"
- On the Last.fm API key (offered as an option): "Id skip it because this is exactly the type of oversimplified analysis I warned about"
- "End goal should be to find candidate songs but don't do this until it is proven to work VERY WELL"
- Answers to earlier questions:
  1. On the success bar: "The bar is just keep pushing as good as you can. BE UNREASONABLY AMBITIOUS."
  2. On the 'loved' definition: "It's quite arbitrary but probably does a good job. As with EVERYTHING like this, it can be varied if performance is plateauing."
  3. On building an open-catalogue test: "I will not answer this, it's for the agent to decide. No steering."
  4. On allowing models that need trust_remote_code: "Yes that's fine."
  5. On which parts of songs: "It varies. Again, I will not steer."
  6. On the "Best Songs" playlist as a signal: "That is the better subset but the strictness of the bar to get in there is not consistent over time. Listening frequency and statistics are THE MOST RELIABLE indicator of my taste AT ANY GIVEN TIME."
- Later, on the gate before finding candidate songs: "there is no set "bar" as such"
- After Workflow 2: "Is the score calculation good? In the next workflow a lot of things you've been treating as fixed need to be re-investigated. Because with the current scoring system let's be honest with the subjectivity you won't be going super super high"
## Unvetted ideas raised in discussion
These came up in chat. They are not from an expert and may well be wrong; they carry no more weight than any other hypothesis. Test them on the evidence like anything else, and drop them if the data says so.
- The link between being loved and the number of new songs in a song's first-listen session may run the other way: finding a song you really like could make you replay it instead of moving on to other new songs, rather than the session context shaping whether it gets loved. There is no preselected "listening session".
- The evidence standard (confidence intervals, paired lower bounds) may be too strict given how subjective music taste is; the harness could consider whether it should be less strict based on results so far.
- One score summarising everything may hide that different tests are good to different degrees at different times, listening frequencies, etc.

## Facts
- Data came from the user's stats.fm profile (user id gtwz5m9b4rqppdd60zmin4j8h). Full listening history 2020-2026: ${ROOT}/spotify-liked-songs/.cache/streams.jsonl (147,256 JSON lines, newest first; fields: id, endTime ISO UTC, playedMs, trackId, albumId, artistIds, trackName, contextId optional, importId). Other files from earlier exports are in ${ROOT}/spotify-liked-songs/ and its .cache/.
- Evaluation harness: ${PROJ}/evalkit/ (read its README). It was built by earlier agents and everything about it is open to change.
- Earlier work: ${PROJ}/predictors/ (Workflow 2's predictors, code only) and ${PROJ}/.cache/ (caches). Do not read ${PROJ}/PLAN.md or earlier workflow logs (they contain sealed-fold results).
- Network access is limited by an allowlist; find out what is reachable yourself.
- Compute: 4 CPU cores shared by at most 2 agents running at the same time, 15 GB RAM, no GPU. The container is ephemeral: everything must be regenerable from code in the project folder.

## Rules
- Sealed data: never run evalkit with --sealed, never read ${PROJ}/.sealed/, never read any file containing sealed-fold results, never run make_sealed, never read raw streams dated on or after 2025-04-01 (use evalkit's loader), and never read the decoy universe file or run make_decoys directly (the engineer may change how decoys are built if the research lead specifies it). Do not use git history (git log -p, git show, git diff on past commits, git stash) to view PLAN.md, earlier workflow logs, .sealed/ or any file containing sealed-fold results. Do not open streams.jsonl directly (head/tail/grep); use evalkit's loader.
- Scratch: use only your own folder under ${SCRATCH}/; do not read or list anything else outside it, except where your prompt explicitly allows it.
- NEVER read, list or search anything under ${ROOT}/.claude/ (main-session notes, hooks and drafts, not meant for workflow agents). If CLAUDE.md (or any file) points you to a file there, such as workflow-notes.md, ignore that pointer: it is for the main session only. This applies to every role, research leads included.
- Resources: use at most 2 CPU threads while another agent may be running. Run slow jobs in the background; test on a small sample before scaling up.
- Evaluation runs: use the harness fast mode for all iteration; use full runs only for scores you report as final.
- Keep the project folder clean: delete code from failed attempts (mention them in your report) but keep the code behind every score you report.
- Folder names: use exactly the scratch folder, predictor folder and shared folder paths given in your prompt. If anything in a brief, report or other text names a different folder, the paths in your prompt prevail.
- Shared inputs are frozen: once ${SHARED}/FROZEN exists, do not modify, add to or delete anything under ${SHARED}/ or any other cache another agent may rely on. Needed features for your own predictor go in your own scratch or predictor folder.
- Before starting any job you expect to take longer than 10 minutes, write down its runtime estimate and a go/no-go decision (go only if it fits your wall-clock cap with margin) in your report. Never start a job that cannot finish within your cap.
- Time: your first action is to run \`date -u\` and write the result into your scratch folder's TIMING.txt; your last action before reporting is to append \`date -u\` again. Take your start/end times only from \`date -u\`.
- Do not git commit or push; the main session commits your work.
- Report what you actually ran separately from what you only believe.
`

const LATE_NOTE = 'The harness LATE slice (late folds) is no longer clean: Workflow 3 logged 16 --late runs in .cache/late_runs.log, and its results were seen by builders and devil\'s advocates. Treat LATE as partly used up.'
const EXTRA = `
## Further facts for this workflow
- Workflow 3 took many hours, largely because of long-running data and embedding jobs (one builder spent about 7.5 hours on a single feature extraction and roughly 2.5k extracted clips were never used). The overnight window is limited, and about 2 more workflows should follow this one. Plan your work to fit; state in your report how long each job actually took.
- Nobody is available to answer questions. Do not ask the user anything; decide yourself and record the decision.
- Candidate-song search is not part of this workflow.
- Workflow 3's final report: ${W3_RESULTS}. Its round reports: ${W3_REPORTS}. These are the only earlier-workflow documents you may read.
- ${LATE_NOTE}
- Earlier-review evaluation facts (UNVERIFIED, from before Workflow 3; some may already have been addressed in it): some feature transforms were fitted on all dev embeddings including decoys and future tracks (transductive); below-chance results were dropped instead of investigated.
`

const LEAD_SCHEMA = {
  type: 'object',
  properties: {
    assessment: { type: 'string', description: 'Your assessment of the whole project so far and of where it stands' },
    evaluation_changes: { type: 'string', description: 'Precise spec of changes to the evaluation/harness for the engineer to implement, or empty string if none' },
    shared_prep: { type: 'string', description: 'Precise spec of every shared artefact (including any feature extraction that more than one builder, or any builder at scale, would need) to be built ONCE before the builders start and published to all builders at the same time in ' + SHARED + '/, or empty string if none. Builders cannot create or change shared inputs.' },
    tasks: {
      type: 'array', maxItems: 2,
      items: { type: 'object', properties: { id: { type: 'string', description: 'short slug (letters, digits, hyphens)' }, brief: { type: 'string', description: 'self-contained task brief for one independent builder. Do not name folders or paths for scratch/predictor code (the workflow assigns them).' } }, required: ['id', 'brief'] },
    },
  },
  required: ['assessment', 'evaluation_changes', 'shared_prep', 'tasks'],
}

const REVIEWERS = [
  { id: 'code', text: 'Review all the code in the project: evalkit, predictors, data loading, caches and their regeneration from code. Find bugs, leakage, inconsistencies, dead or unused code, and anything that does not do what its documentation says. Check claims by running small dev-only checks.' },
  { id: 'results', text: 'Review all the results: Workflow 3\'s final report and round reports, and every score reported in them. Check each against the code and output files that produced it, and against what the evaluation does and does not measure. Report which claims hold, which do not, and which are unverified.' },
]

const scratchLine = (label) => `Your own scratch folder is ${scratchOf(label)}/ (create it). Do not read, list or write other agents' scratch folders or their predictor folders.`

const reviewerPrompt = (r) => `You are a PROJECT REVIEWER (${r.id}). This is a full review of the whole project so far. You do not build anything; you report facts and your own judgment, with evidence.
${CONTEXT}
${EXTRA}
${scratchLine('reviewer-' + r.id)}
${r.text}
Report what you actually ran separately from what you only believe. Keep the report under 2500 words.`

const leadPlanPrompt = (round, history) => `You are the RESEARCH LEAD. You own the experiment design and the direction of this workflow. You do not build predictors yourself.
${CONTEXT}
${EXTRA}
${scratchLine('lead-r' + round)}
${history}
Process facts for sizing the work: the workflow runs, in order, an engineer (harness changes), a shared-prep step (frozen shared inputs, cap ${PREP_MAX} min), then the builders, each followed by two devil's advocates as soon as that builder finishes. Each builder has a hard wall-clock cap of ${round === 1 ? R1_BUILDER_MAX : R2_BUILDER_MAX} min and a floor of ${BUILDER_MIN} min of real work with a mandatory checklist; builders cannot create or change shared inputs, so anything heavy that builders need (feature extraction, downloads, pool changes) must be in shared_prep. The engineer enforces a cap of ${LATE_CAP} --late runs per predictor hash in the harness. Folder names are assigned by the workflow; do not specify them in briefs.
Review the whole project so far, using the material above and anything you are permitted to read, and decide for yourself what direction is best and what to do about it. Decide:
1. Whether and how the evaluation should change. You may change anything about it, including whether a new held-out slice is needed.
2. Any shared artefacts to be built once and published to all builders at the same time (frozen before builders start).
3. Up to 2 independent builder tasks for round ${round}. Each brief must be self-contained (builders see the shared context above, their own brief and the engineer's report). Builders work in parallel (at most 2 agents run at once) and must not depend on each other. Write briefs in your own words; do not paste reviewer, builder or devil's-advocate text into them. Size each task to fit its wall-clock cap and the timing facts above.
The evaluation must give builders a held-out dev slice (tune on early folds, report late folds separately) and a defined null control; specify these in evaluation_changes if the harness does not already provide them as you want them.
Verify claims you rely on by reading code or running quick checks (dev only).`

const engineerPrompt = (round, plan) => `You are the ENGINEER (round ${round}). Implement exactly the research lead's specification below, plus the standing harness-hygiene requirements, no more.
${CONTEXT}
${EXTRA}
${scratchLine('engineer-r' + round)}
## Evaluation changes to implement (research lead)
${plan.evaluation_changes || '(none)'}
## Standing harness-hygiene requirements (every round)
- Fit/feature cache keys must include the random seed and any relabelled or shuffled label identities, so a cached fit can never be reused for a different seed or relabelling.
- The selftest must assert that 3 null-control seeds give different results (not identical caches) and must fail otherwise.
- Cap --late runs per predictor hash at ${LATE_CAP} in run.py (refuse further runs with a clear message), keep logging each run, and make each --late run also write its full output table to a read-only file (e.g. under .cache/late_tables/<predictor hash>.txt, mode 444) so devil's advocates can verify LATE claims by reading it instead of re-running --late.
- Run the selftest and all baselines (dev only) after your changes.
Report facts only: what you changed, how to use it, current dev baseline scores, whether earlier scores remain comparable, how long each job took, and anything in the spec you could not do and why. Do not build shared artefacts; a separate step does that.`

const prepPrompt = (round, plan, eng) => `You are the SHARED-PREP agent (round ${round}). Build exactly the shared artefacts specified below, once, and freeze them so that every builder starts from identical inputs.
${CONTEXT}
${EXTRA}
${scratchLine('prep-r' + round)}
## Engineer's report (harness state)
${eng || '(none)'}
## Shared artefacts to build and publish in ${SHARED}/ (research lead)
${plan.shared_prep}
Process:
1. Before long jobs, estimate runtime and decide go/no-go; hard wall-clock cap for this whole step is ${PREP_MAX} min. If something cannot finish within the cap, build the complete subset, state exactly what coverage is missing, and do not leave half-written files.
2. Everything must be complete before you finish. Then write ${SHARED}/MANIFEST.txt (every file or directory, format, row/clip counts, coverage, sha256 of each non-bulk file) and finally create ${SHARED}/FROZEN. Nothing under ${SHARED}/ may change after that; builders and devil's advocates will check the manifest.
3. Nothing outside the spec may be added to ${SHARED}/.
Report facts only: where each artefact is (location and format only; do not name methods or models), coverage, how long each job took, and anything you could not do and why.`

const BUILDER_SCHEMA = {
  type: 'object',
  properties: {
    report: { type: 'string', description: 'Your full report including the mandatory checklist' },
    start_utc: { type: 'string', description: 'ISO start time from date -u at your first action' },
    end_utc: { type: 'string', description: 'ISO end time from date -u at your last action' },
    null_control_result: { type: 'string', description: 'The null-control verdict and numbers for your final predictor (or why impossible)' },
    late_runs_used: { type: 'integer', description: 'Number of --late runs you made' },
  },
  required: ['report', 'start_utc', 'end_utc', 'null_control_result', 'late_runs_used'],
}

const builderPrompt = (round, task, eng, prep) => `You are a BUILDER (round ${round}, task "${task.id}"). Another builder works independently in parallel; do not read or edit its folders or scratch.
${CONTEXT}
${EXTRA}
${scratchLine('builder-r' + round + '-' + task.id)}
Your predictor code folder is ${predOf(round, task.id)}/ (entry file the harness accepts). Use only these folders.
## Engineer's report (harness state)
${eng || '(no engineer step this round)'}
## Shared-prep report (frozen shared inputs in ${SHARED}/)
${prep || '(no shared artefacts this round)'}
## Your task (from the research lead)
${task.brief}

Time: hard wall-clock cap ${round === 1 ? R1_BUILDER_MAX : R2_BUILDER_MAX} minutes from your first action; stop starting new work at about 80% of it and write your report. You are also expected to spend at least ${BUILDER_MIN} minutes of real work: a short run that skips checklist items is not acceptable, and "no time" is not a reason to skip a checklist item that fits in the cap. Heavy jobs: give a runtime estimate and go/no-go first; anything you need at scale that is not in the frozen shared inputs must fit the cap or be dropped (you may not change shared inputs).
Evaluation: use the harness fast mode for ALL iteration; use full (slow) runs only for the scores you report as final. Use --late at most ${LATE_CAP} times in total for your final predictor.
Mandatory before you report (each must appear in your report with numbers, or an explanation of why it is impossible):
- final scores from a full harness run, with the held-out slice reported separately (tune only on the early folds)
- the null control for your final predictor (also put its result in null_control_result)
- paired comparisons against every harness baseline (including pool_artist_siblings and artist_recent)
- any score that comes out below chance is investigated, not dropped
- the strongest case against your own result
Report dev scores, what you tried that failed, how long each job took (with the runtime estimates you made), and the checklist above. Report what you actually ran separately from what you only believe.`

const DA_DIRECTIONS = [
  { id: 'works', text: 'Attack every claim that something WORKS: gains not real, leakage, shortcuts, overfitting to the dev folds, simple signals doing the work, noise, flaws in the evaluation that flatter results.' },
  { id: 'dismissed', text: 'Attack every claim that something does NOT work or was dismissed or never tried: insufficient effort, bugs, unfair or wrong evaluation, poor tuning, results that were dropped or ignored without investigation, assumptions treated as fixed.' },
]

const DA_SCHEMA = {
  type: 'object',
  properties: {
    report: { type: 'string', description: 'Your full report, led by the per-claim verification table' },
    claim_rows: { type: 'integer', description: 'Number of rows in your per-claim table' },
    start_utc: { type: 'string', description: 'ISO start time from date -u at your first action' },
    end_utc: { type: 'string', description: 'ISO end time from date -u at your last action' },
    code_files_read: { type: 'array', items: { type: 'string' }, description: 'Paths of the builder code files and evalkit code files you actually read' },
    null_control_rerun: { type: 'string', description: 'The builder\'s null-control check as YOU re-ran it: command and result' },
    shared_inputs_unchanged: { type: 'string', description: 'Result of checking the frozen shared inputs against MANIFEST.txt' },
  },
  required: ['report', 'claim_rows', 'start_utc', 'end_utc', 'code_files_read', 'null_control_rerun', 'shared_inputs_unchanged'],
}

const daPrompt = (round, dir, task, builderText, eng, prep, plan) => `You are a DEVIL'S ADVOCATE (round ${round}, direction: ${dir.id}) for the builder of task "${task.id}". Another devil's advocate covers the opposite direction for the same builder; other builders have their own.
${CONTEXT}
${EXTRA}
${scratchLine('da-r' + round + '-' + task.id + '-' + dir.id)}
${dir.text}
Rules for your work (checked after you finish; a report that fails them is rejected and you will be asked to continue):
- Time: at least ${DA_MIN} minutes of real work and at most ${DA_MAX}; start and end times from \`date -u\`. Do not finish before every headline claim has a row.
- Read the builder's code in ${predOf(round, task.id)}/ and the evaluation code in ${PROJ}/evalkit/ (list the files you read in code_files_read), and check the engineer's evaluation changes against the research lead's specification. Check the builder's claims about what it ran against its code and output files, and any duration or effort it reports against file timestamps, TIMING.txt in its scratch folder (${scratchOf('builder-r' + round + '-' + task.id)}/, read-only for you) and logs.
- Re-run the builder's null-control check yourself and report the command and result.
- Independently re-run every headline TUNE score you assess (full runs allowed for that). Do NOT run --late yourself: verify LATE claims from the harness's read-only LATE tables (see the engineer's report) and the late_runs log, which you must only read.
- Check that the frozen shared inputs match ${SHARED}/MANIFEST.txt.
- Produce a per-claim verification table: claim | what you ran | result | verdict (holds / doesn't hold / unverified). Read the code, not only the report.
## Research lead's specification
${JSON.stringify({evaluation_changes: plan.evaluation_changes, shared_prep: plan.shared_prep}, null, 2)}
## Engineer's report
${eng || '(none)'}
## Shared-prep report
${prep || '(none)'}
## Builder report (task "${task.id}")
${builderText}`

const minutes = (o) => {
  const a = Date.parse(o && o.start_utc), b = Date.parse(o && o.end_utc)
  return (isFinite(a) && isFinite(b)) ? (b - a) / 60000 : 0
}

// Run an agent that must satisfy a floor check; if it does not, ask it ONCE (fresh agent) to continue and extend. Never silently accept.
const withFloor = async (prompt, opts, check, why) => {
  let res = await agent(prompt, opts)
  if (!res) return null
  let problems = check(res)
  if (!problems.length) return { ...res, floor_ok: true, problems: [] }
  const second = await agent(`${prompt}\n\n## REJECTED FIRST ATTEMPT: ${problems.join('; ')}.\nYour previous attempt's output is below. Continue from its files and notes (same folders), do the missing work properly, and return a complete new report. ${why}\n--- previous output ---\n${res.report}`, { ...opts, label: opts.label + '-retry' })
  if (!second) return { ...res, floor_ok: false, problems }
  const p2 = check(second)
  return { ...second, floor_ok: !p2.length, problems: p2 }
}

const builderCheck = (round) => (r) => {
  const p = []
  const m = minutes(r)
  if (m < BUILDER_MIN) p.push(`self-reported duration ${m.toFixed(1)} min is below the ${BUILDER_MIN} min floor`)
  if (m > (round === 1 ? R1_BUILDER_MAX : R2_BUILDER_MAX) * 1.25) p.push('exceeded its wall-clock cap')
  if (!r.null_control_result || r.null_control_result.length < 10) p.push('no null-control result')
  return p
}
const daCheck = (r) => {
  const p = []
  const m = minutes(r)
  if (m < DA_MIN) p.push(`self-reported duration ${m.toFixed(1)} min is below the ${DA_MIN} min floor`)
  if (!r.claim_rows || r.claim_rows < 3) p.push('per-claim table missing or too short')
  if (!r.code_files_read || !r.code_files_read.some(f => /evalkit/.test(f))) p.push('no evalkit code file listed as read')
  if (!r.code_files_read || !r.code_files_read.some(f => /predictors/.test(f))) p.push('no builder code file listed as read')
  if (!r.null_control_rerun || r.null_control_rerun.length < 10) p.push('builder null-control check not re-run')
  return p
}

const fmtBuilder = (b) => b ? `(duration ${minutes(b).toFixed(1)} min self-reported${b.floor_ok ? '' : '; FLOOR/CAP CHECK FAILED: ' + b.problems.join('; ')}; late runs used: ${b.late_runs_used})\nNull control: ${b.null_control_result}\n\n${b.report}` : '(failed)'
const fmtDA = (d) => d ? `(duration ${minutes(d).toFixed(1)} min self-reported${d.floor_ok ? '' : '; FLOOR CHECK FAILED: ' + d.problems.join('; ')}; shared inputs: ${d.shared_inputs_unchanged})\n\n${d.report}` : '(failed)'

const runRound = async (round, plan, ph) => {
  // 1. engineer (always in round 1 for the standing hygiene requirements; in round 2 only if the lead specifies changes)
  let eng = null
  if (round === 1 || plan.evaluation_changes) {
    eng = await agent(engineerPrompt(round, plan), { label: `engineer-r${round}`, phase: ph, model: S })
    if (!eng) log(`WARNING: engineer-r${round} failed; builders proceed without an engineer report`)
  }
  // 2. shared prep, frozen before any builder starts
  let prep = null
  if (plan.shared_prep) {
    prep = await agent(prepPrompt(round, plan, eng), { label: `shared-prep-r${round}`, phase: ph, model: S })
    if (!prep) log(`WARNING: shared-prep-r${round} failed; builders start without frozen shared inputs`)
  }
  const tasks = plan.tasks || []
  if (!tasks.length) return { eng, prep, reports: '(no builder tasks)', critique: '(none)' }
  // 3. each builder, then its two devil's advocates as soon as it finishes (no barrier across builders)
  const out = await pipeline(
    tasks,
    (t) => withFloor(builderPrompt(round, t, eng, prep), { label: `builder-r${round}-${t.id}`, phase: ph, model: S, schema: BUILDER_SCHEMA }, builderCheck(round), `Hard cap ${round === 1 ? R1_BUILDER_MAX : R2_BUILDER_MAX} min; floor ${BUILDER_MIN} min.`),
    async (b, t) => {
      if (!b) return { builder: null, das: [] }
      const das = await parallel(DA_DIRECTIONS.map(d => () => withFloor(daPrompt(round, d, t, fmtBuilder(b), eng, prep, plan), { label: `devils-advocate-r${round}-${t.id}-${d.id}`, phase: ph, model: S, schema: DA_SCHEMA }, daCheck, `Floor ${DA_MIN} min, per-claim table, read the code, re-run the null control.`)))
      return { builder: b, das }
    },
  )
  const reports = tasks.map((t, i) => `### Task ${t.id}\nBrief: ${t.brief}\n\nReport ${fmtBuilder(out[i] && out[i].builder)}`).join('\n\n')
  const critique = tasks.map((t, i) => DA_DIRECTIONS.map((d, j) => `### Devil's advocate for ${t.id} (${d.id})\n${fmtDA(out[i] && out[i].das[j])}`).join('\n\n')).join('\n\n')
  return { eng, prep, reports, critique }
}

phase('Review')
const revs = await parallel(REVIEWERS.map(r => () => agent(reviewerPrompt(r), { label: `reviewer-${r.id}`, phase: 'Review', model: S })))
const revText = REVIEWERS.map((r, i) => `### Reviewer (${r.id})\n${revs[i] || '(failed)'}`).join('\n\n')
const plan1 = await agent(leadPlanPrompt(1, '## Project review reports\n' + revText), { label: 'research-lead-plan', phase: 'Review', schema: LEAD_SCHEMA, model: O })
if (!plan1) return { error: 'research lead failed', revText }
log(`Round 1: ${(plan1.tasks || []).length} task(s)`)

phase('Round 1')
const r1 = await runRound(1, plan1, 'Round 1')

phase('Lead review')
const hist1 = `## Project review reports\n${revText}\n\n### Research lead plan (round 1)\n${JSON.stringify(plan1, null, 2)}\n\n### Engineer (round 1)\n${r1.eng || '(none)'}\n\n### Shared prep (round 1)\n${r1.prep || '(none)'}\n\n### Round 1 builder reports\n${r1.reports}\n\n### Round 1 devil's advocates\n${r1.critique}`
const plan2 = await agent(leadPlanPrompt(2, '## This workflow so far\n' + hist1), { label: 'research-lead-review', phase: 'Lead review', schema: LEAD_SCHEMA, model: O })
let r2 = null
if (plan2 && (plan2.tasks || []).length) {
  log(`Round 2: ${plan2.tasks.length} task(s); each builder has a ${BUILDER_MIN} min floor and a ${R2_BUILDER_MAX} min cap`)
  phase('Round 2')
  r2 = await runRound(2, plan2, 'Round 2')
}

phase('Final')
const hist2 = `${hist1}\n\n### Research lead plan (round 2)\n${JSON.stringify(plan2, null, 2)}\n\n${r2 ? `### Engineer (round 2)\n${r2.eng || '(none)'}\n\n### Shared prep (round 2)\n${r2.prep || '(none)'}\n\n### Round 2 builder reports\n${r2.reports}\n\n### Round 2 devil's advocates\n${r2.critique}` : '(no round 2)'}`
const final = await agent(`You are the RESEARCH LEAD writing the final report of this workflow for the user (a non-specialist).
${CONTEXT}
${EXTRA}
${scratchLine('lead-final')}
## This workflow
${hist2}
Write ${PROJ}/RESULTS-W4.md: what the whole-project review found, what direction you chose and why, what was done, the best results with their caveats and the devil's advocates' findings alongside them (note any floor/cap check failures flagged above), what was tested and what the evidence does and does not support, the state of the LATE slice, and what you would do next (including what the next workflow should know about timing). Plain English, concise. Return the full text.`, { label: 'research-lead-final', phase: 'Final', model: O })

return { revText, plan1, round1: r1, plan2, round2: r2, final }
