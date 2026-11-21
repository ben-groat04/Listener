// Workflow 4 (overnight): full review of the whole project so far, then work chosen by the agents, then final report.
// NOTE: do NOT message running workflow agents from the main session (the user's latest message is auto-forwarded; extra messages steer them).
// DRAFT: fill the W3_* paths below (see workflow4-notes.md) before launch; launch only right after a neutral message ("go").
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
// FILL once Workflow 3 has finished (must contain no sealed-fold results):
const W3_RESULTS = PROJ + '/RESULTS.md'
const W3_REPORTS = 'FILL: paths of Workflow 3 round reports (engineer/builder/devil\'s-advocate/lead), one per line'

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
- Scratch: use only your own folder under ${SCRATCH}/; do not read or list anything else outside it.
- Do not read anything under ${ROOT}/.claude/ (main-session notes and drafts, not meant for workflow agents), even though CLAUDE.md mentions workflow-notes.md: that instruction is for the main session only.
- Resources: use at most 2 CPU threads while another agent may be running. Run slow jobs in the background; test on a small sample before scaling up.
- Evaluation runs: use the harness fast mode for all iteration; use full runs only for scores you report as final.
- Keep the project folder clean: delete code from failed attempts (mention them in your report) but keep the code behind every score you report.
- Do not git commit or push; the main session commits your work.
- Report what you actually ran separately from what you only believe.
`

const EXTRA = `
## Further facts for this workflow
- Workflow 3 took many hours, largely because of long-running data and embedding jobs. The overnight window is limited, and about 2 more workflows should follow this one. Plan your work to fit; state in your report how long each job actually took.
- Nobody is available to answer questions. Do not ask the user anything; decide yourself and record the decision.
- Candidate-song search is not part of this workflow.
- Workflow 3's final report: ${W3_RESULTS}. Its round reports: ${W3_REPORTS}. These are the only earlier-workflow documents you may read.
- Earlier-review evaluation facts (UNVERIFIED, from before Workflow 3; some may already have been addressed in it): some feature transforms were fitted on all dev embeddings including decoys and future tracks (transductive); below-chance results were dropped instead of investigated.
`

const folder = (label) => `Your own scratch folder is ${SCRATCH}/${label}/ (create it). Do not read, list or write other agents' scratch folders or their predictor folders.`

const LEAD_SCHEMA = {
  type: 'object',
  properties: {
    assessment: { type: 'string', description: 'Your assessment of the whole project so far and of where it stands' },
    evaluation_changes: { type: 'string', description: 'Precise spec of changes to the evaluation/harness for the engineer to implement, or empty string if none' },
    shared_prep: { type: 'string', description: 'Precise spec of shared artefacts to build once and publish to all builders (in ' + PROJ + '/.cache/shared/), or empty string if none' },
    tasks: {
      type: 'array', maxItems: 2,
      items: { type: 'object', properties: { id: { type: 'string', description: 'short slug' }, brief: { type: 'string', description: 'self-contained task brief for one independent builder' } }, required: ['id', 'brief'] },
    },
  },
  required: ['assessment', 'evaluation_changes', 'shared_prep', 'tasks'],
}

const REVIEWERS = [
  { id: 'code', text: 'Review all the code in the project: evalkit, predictors, data loading, caches and their regeneration from code. Find bugs, leakage, inconsistencies, dead or unused code, and anything that does not do what its documentation says. Check claims by running small dev-only checks.' },
  { id: 'results', text: 'Review all the results: Workflow 3\'s final report and round reports, and every score reported in them. Check each against the code and output files that produced it, and against what the evaluation does and does not measure. Report which claims hold, which do not, and which are unverified.' },
]

const reviewerPrompt = (r) => `You are a PROJECT REVIEWER (${r.id}). This is a full review of the whole project so far. You do not build anything; you report facts and your own judgment, with evidence.
${CONTEXT}
${EXTRA}
${folder('reviewer-' + r.id)}
${r.text}
Report what you actually ran separately from what you only believe. Keep the report under 2500 words.`

const leadPlanPrompt = (round, history) => `You are the RESEARCH LEAD. You own the experiment design and the direction of this workflow. You do not build predictors yourself.
${CONTEXT}
${EXTRA}
${folder('lead-r' + round)}
${history}
Review the whole project so far, using the material above and anything you are permitted to read, and decide for yourself what direction is best and what to do about it. Decide:
1. Whether and how the evaluation should change. You may change anything about it.
2. Any shared artefacts to be built once and published to all builders at the same time.
3. Up to 2 independent builder tasks for round ${round}. Each brief must be self-contained (builders see the shared context above, their own brief and the engineer's report). Builders work in parallel (at most 2 agents run at once) and must not depend on each other. Write briefs in your own words; do not paste reviewer, builder or devil's-advocate text into them. Account for the timing facts above when sizing the work.
The evaluation must give builders a held-out dev slice (tune on early folds, report late folds separately) and a defined null control; specify these in evaluation_changes if the harness does not already provide them as you want them.
Verify claims you rely on by reading code or running quick checks (dev only).`

const engineerPrompt = (plan) => `You are the ENGINEER. Implement exactly the research lead's specification below, no more.
${CONTEXT}
${EXTRA}
${folder('engineer')}
## Evaluation changes to implement
${plan.evaluation_changes || '(none)'}
## Shared artefacts to build and publish in ${PROJ}/.cache/shared/
${plan.shared_prep || '(none)'}
Run the selftest and all baselines (dev only) after your changes. Report facts only: what you changed, how to use it, where shared artefacts are (describe them by location and format only; do not name methods or models), current dev baseline scores, whether earlier scores remain comparable, how long each job took, and anything in the spec you could not do and why.`

const builderPrompt = (round, task, eng) => `You are a BUILDER (round ${round}, task "${task.id}"). Another builder works independently in parallel; do not read or edit its folders or scratch.
${CONTEXT}
${EXTRA}
${folder('builder-r' + round + '-' + task.id)}
## Engineer's report (harness state and shared artefacts)
${eng || '(no engineer step this round)'}
## Your task (from the research lead)
${task.brief}

Put your code under ${PROJ}/predictors/w4r${round}-${task.id}/ with an entry file the harness accepts.
Mandatory before you report (each must appear in your report with numbers, or an explanation of why it is impossible):
- final scores from a full harness run, with the held-out slice reported separately (tune only on the early folds)
- the null control for your final predictor
- paired comparisons against every harness baseline (including pool_artist_siblings and artist_recent)
- any score that comes out below chance is investigated, not dropped
- the strongest case against your own result
Report dev scores, what you tried that failed, how long each job took, and the checklist above.`

const DA_DIRECTIONS = [
  { id: 'works', text: 'Attack every claim that something WORKS: gains not real, leakage, shortcuts, overfitting to the dev folds, simple signals doing the work, noise, flaws in the evaluation that flatter results.' },
  { id: 'dismissed', text: 'Attack every claim that something does NOT work or was dismissed or never tried: insufficient effort, bugs, unfair or wrong evaluation, poor tuning, results that were dropped or ignored without investigation, assumptions treated as fixed.' },
]

const daPrompt = (round, dir, reports, eng, plan) => `You are a DEVIL'S ADVOCATE (round ${round}, direction: ${dir.id}). Another devil's advocate covers the opposite direction.
${CONTEXT}
${EXTRA}
${folder('da-r' + round + '-' + dir.id)}
${dir.text}
Read the builders' code in ${PROJ}/predictors/w4r${round}-*/ and the evaluation code, and check the engineer's evaluation changes against the research lead's specification. Independently re-run every headline score you assess, and check builders' claims about what they ran against their code and output files. Produce a per-claim verification table: claim | what you ran | result | verdict (holds / doesn't hold / unverified). Read the builders' code, not only their reports. Check any duration or effort a builder reports against file timestamps and logs. Full runs are allowed for re-running reported final scores. Spend at least 20 minutes, and do not finish before every headline claim has a row.
## Research lead's specification
${JSON.stringify({evaluation_changes: plan.evaluation_changes, shared_prep: plan.shared_prep}, null, 2)}
## Engineer's report
${eng || '(none)'}
## Builder reports
${reports}`

const runRound = async (round, plan, ph) => {
  let eng = null
  if (plan.evaluation_changes || plan.shared_prep) {
    eng = await agent(engineerPrompt(plan), { label: `engineer-r${round}`, phase: ph, model: S })
  }
  const tasks = plan.tasks || []
  if (!tasks.length) return { eng, reports: '(no builder tasks)', critique: '(none)' }
  const builds = await parallel(tasks.map(t => () => agent(builderPrompt(round, t, eng), { label: `builder-r${round}-${t.id}`, phase: ph, model: S })))
  const reports = tasks.map((t, i) => `### Task ${t.id}\nBrief: ${t.brief}\n\nReport:\n${builds[i] || '(failed)'}`).join('\n\n')
  const das = await parallel(DA_DIRECTIONS.map(d => () => agent(daPrompt(round, d, reports, eng, plan), { label: `devils-advocate-r${round}-${d.id}`, phase: ph, model: S })))
  const critique = DA_DIRECTIONS.map((d, i) => `### Devil's advocate (${d.id})\n${das[i] || '(failed)'}`).join('\n\n')
  return { eng, reports, critique }
}

phase('Review')
const revs = await parallel(REVIEWERS.map(r => () => agent(reviewerPrompt(r), { label: `reviewer-${r.id}`, phase: 'Review', model: S })))
const revText = REVIEWERS.map((r, i) => `### Reviewer (${r.id})\n${revs[i] || '(failed)'}`).join('\n\n')
const plan1 = await agent(leadPlanPrompt(1, '## Project review reports\n' + revText), { label: 'research-lead-plan', phase: 'Review', schema: LEAD_SCHEMA, model: O })
if (!plan1) return { error: 'research lead failed', revText }
log(`Round 1: ${(plan1.tasks || []).length} task(s)`)
const r1 = await runRound(1, plan1, 'Round 1')

phase('Lead review')
const hist1 = `## Project review reports\n${revText}\n\n### Research lead plan (round 1)\n${JSON.stringify(plan1, null, 2)}\n\n### Engineer (round 1)\n${r1.eng || '(none)'}\n\n### Round 1 builder reports\n${r1.reports}\n\n### Round 1 devil's advocates\n${r1.critique}`
const plan2 = await agent(leadPlanPrompt(2, '## This workflow so far\n' + hist1), { label: 'research-lead-review', phase: 'Lead review', schema: LEAD_SCHEMA, model: O })
let r2 = null
if (plan2 && (plan2.tasks || []).length) {
  log(`Round 2: ${plan2.tasks.length} task(s)`)
  r2 = await runRound(2, plan2, 'Round 2')
}

phase('Final')
const hist2 = `${hist1}\n\n### Research lead plan (round 2)\n${JSON.stringify(plan2, null, 2)}\n\n${r2 ? `### Engineer (round 2)\n${r2.eng || '(none)'}\n\n### Round 2 builder reports\n${r2.reports}\n\n### Round 2 devil's advocates\n${r2.critique}` : '(no round 2)'}`
const final = await agent(`You are the RESEARCH LEAD writing the final report of this workflow for the user (a non-specialist).
${CONTEXT}
${EXTRA}
${folder('lead-final')}
## This workflow
${hist2}
Write ${PROJ}/RESULTS-W4.md: what the whole-project review found, what direction you chose and why, what was done, the best results with their caveats and the devil's advocates' findings alongside them, what was tested and what the evidence does and does not support, and what you would do next (including what the next workflow should know about timing). Plain English, concise. Return the full text.`, { label: 'research-lead-final', phase: 'Final', model: O })

return { revText, plan1, round1: r1, plan2, round2: r2, final }
