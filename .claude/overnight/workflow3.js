export const meta = {
  name: 'taste-workflow-3',
  description: 'Workflow 3: Opus research lead re-investigates evaluation and plans; engineer implements; 2 rounds of builders + two devil\'s advocates; lead judges',
  phases: [
    { title: 'Plan', detail: 'research lead (Opus) + engineer', model: 'opus' },
    { title: 'Round 1', detail: 'builders + 2 devil\'s advocates', model: 'sonnet' },
    { title: 'Review', detail: 'research lead (Opus) + engineer', model: 'opus' },
    { title: 'Round 2', detail: 'builders + 2 devil\'s advocates', model: 'sonnet' },
    { title: 'Final', detail: 'research lead (Opus) final report', model: 'opus' },
  ],
}

const ROOT = '/home/user/Listener'
const PROJ = ROOT + '/taste-model'
const SCRATCH = '/tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3'
const S = 'sonnet', O = 'opus'

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

## Facts
- Data came from the user's stats.fm profile (user id gtwz5m9b4rqppdd60zmin4j8h). Full listening history 2020-2026: ${ROOT}/spotify-liked-songs/.cache/streams.jsonl (147,256 JSON lines, newest first; fields: id, endTime ISO UTC, playedMs, trackId, albumId, artistIds, trackName, contextId optional, importId). Other files from earlier exports are in ${ROOT}/spotify-liked-songs/ and its .cache/.
- Evaluation harness: ${PROJ}/evalkit/ (read its README). It was built by earlier agents and everything about it is open to change.
- Earlier work: ${PROJ}/predictors/ (Workflow 2's predictors, code only) and ${PROJ}/.cache/ (caches). Do not read ${PROJ}/PLAN.md or earlier workflow logs (they contain sealed-fold results).
- Network access is limited by an allowlist; find out what is reachable yourself.
- Compute: 4 CPU cores shared by at most 2 agents running at the same time, 15 GB RAM, no GPU. The container is ephemeral: everything must be regenerable from code in the project folder.

## Rules
- Sealed data: never run evalkit with --sealed, never read ${PROJ}/.sealed/, never read any file containing sealed-fold results, never run make_sealed, never read raw streams dated on or after 2025-04-01 (use evalkit's loader), and never read the decoy universe file or run make_decoys directly (the engineer may change how decoys are built if the research lead specifies it). Do not use git history (git log -p, git show, git diff on past commits, git stash) to view PLAN.md, earlier workflow logs, .sealed/ or any file containing sealed-fold results. Do not open streams.jsonl directly (head/tail/grep); use evalkit's loader.
- Scratch: use only your own folder under ${SCRATCH}/; do not read or list anything else outside it.
- Resources: use at most 2 CPU threads while another agent may be running. Run slow jobs in the background; test on a small sample before scaling up.
- Evaluation runs: use the harness fast mode for all iteration; use full runs only for scores you report as final.
- Keep the project folder clean: delete code from failed attempts (mention them in your report) but keep the code behind every score you report.
- Do not git commit or push; the main session commits your work.
- Report what you actually ran separately from what you only believe.
`

const LEAD_SCHEMA = {
  type: 'object',
  properties: {
    assessment: { type: 'string', description: 'Your assessment of the work and evaluation so far' },
    evaluation_changes: { type: 'string', description: 'Precise spec of changes to the evaluation/harness for the engineer to implement, or empty string if none' },
    shared_prep: { type: 'string', description: 'Precise spec of shared artefacts to build once and publish to all builders (in ' + PROJ + '/.cache/shared/), or empty string if none' },
    tasks: {
      type: 'array', maxItems: 3,
      items: { type: 'object', properties: { id: { type: 'string', description: 'short slug' }, brief: { type: 'string', description: 'self-contained task brief for one independent builder' } }, required: ['id', 'brief'] },
    },
  },
  required: ['assessment', 'evaluation_changes', 'shared_prep', 'tasks'],
}

const leadPlanPrompt = (round, history) => `You are the RESEARCH LEAD. You own the experiment design for this round: what is evaluated and how, and what gets built. You do not build predictors yourself.
${CONTEXT}
${history ? '## This workflow so far\n' + history : ''}
Review everything relevant that you are permitted to read (code, reports, data) and decide:
1. Whether and how the evaluation should change. You may change anything about it.
2. Any shared artefacts that should be built once and published to all builders at the same time.
3. Up to 3 independent builder tasks for round ${round}. Each brief must be self-contained (builders see the shared context above, their own brief and the engineer's report). Builders work in parallel (at most 2 at a time) and must not depend on each other. Write briefs in your own words; do not paste builder or devil's-advocate text into them.
The evaluation must give builders a held-out dev slice (tune on early folds, report late folds separately) and a defined null control; specify these in evaluation_changes if the harness does not already provide them as you want them.
Verify claims you rely on by reading code or running quick checks (dev only).

## Known evaluation facts from earlier review (not verified by you; weigh them)
- Track duration alone scores ~0.578 on the tried pool; the harness has no metadata baselines.
- Songs without a preview get missing (NaN) audio features, a ~0.025 AUC shortcut.
- New-artist tie anomaly: artist-history baselines give identical, above-chance metrics on the zero-history new-artist subset; never checked.
- Some feature transforms were fitted on all dev embeddings including decoys and future tracks (transductive).
- The decoy universe was built from the user's lifetime top-300 artists including plays after the cutoff, plus related artists.
- Below-chance results (e.g. 0.37-0.45) were dropped instead of investigated.
- Any future sealed run needs sealed-era data/features prepared and sealed labels/manifest regenerated (candidate sets changed in evalkit v2.1); that is the main session's job, not this workflow's.`

const engineerPrompt = (plan) => `You are the ENGINEER. Implement exactly the research lead's specification below, no more.
${CONTEXT}
## Evaluation changes to implement
${plan.evaluation_changes || '(none)'}
## Shared artefacts to build and publish in ${PROJ}/.cache/shared/
${plan.shared_prep || '(none)'}
Run the selftest and all baselines (dev only) after your changes. Report facts only: what you changed, how to use it, where shared artefacts are (describe them by location and format only; do not name methods or models), current dev baseline scores, whether earlier scores remain comparable, and anything in the spec you could not do and why.`

const builderPrompt = (round, task, eng) => `You are a BUILDER (round ${round}, task "${task.id}"). Other builders work independently in parallel; do not read or edit their folders or scratch.
${CONTEXT}
## Engineer's report (harness state and shared artefacts)
${eng || '(no engineer step this round)'}
## Your task (from the research lead)
${task.brief}

Put your code under ${PROJ}/predictors/w3r${round}-${task.id}/ with an entry file the harness accepts.
Mandatory before you report (each must appear in your report with numbers, or an explanation of why it is impossible):
- final scores from a full harness run, with the held-out slice reported separately (tune only on the early folds)
- the null control for your final predictor
- paired comparisons against every harness baseline (including pool_artist_siblings and artist_recent)
- any score that comes out below chance is investigated, not dropped
- the strongest case against your own result
Report dev scores, what you tried that failed, and the checklist above.`

const DA_DIRECTIONS = [
  { id: 'works', text: 'Attack every claim that something WORKS: gains not real, leakage, shortcuts, overfitting to the dev folds, simple signals doing the work, noise, flaws in the evaluation that flatter results.' },
  { id: 'dismissed', text: 'Attack every claim that something does NOT work or was dismissed or never tried: insufficient effort, bugs, unfair or wrong evaluation, poor tuning, results that were dropped or ignored without investigation, assumptions treated as fixed.' },
]

const daPrompt = (round, dir, reports, eng, plan) => `You are a DEVIL'S ADVOCATE (round ${round}, direction: ${dir.id}). Another devil's advocate covers the opposite direction.
${CONTEXT}
${dir.text}
Read the builders' code in ${PROJ}/predictors/w3r${round}-*/ and the evaluation code, and check the engineer's evaluation changes against the research lead's specification. Independently re-run every headline score you assess, and check builders' claims about what they ran against their code and output files. Produce a table: claim | what you ran | result | verdict (holds / doesn't hold / unverified). Check any duration or effort a builder reports against what their files show. Full runs are allowed for re-running reported final scores. Spend at least 20 minutes, and do not finish before every headline claim has a row.
## Research lead's specification
${JSON.stringify({evaluation_changes: plan.evaluation_changes, shared_prep: plan.shared_prep}, null, 2)}
## Engineer's report
${eng || '(none)'}
## Builder reports
${reports}`

const runRound = async (round, plan, ph) => {
  let eng = null
  if (plan.evaluation_changes || plan.shared_prep) {
    eng = await agent(engineerPrompt(plan), { label: `engineer-r${round}`, phase: round === 1 ? 'Plan' : 'Review', model: S })
  }
  const tasks = plan.tasks || []
  if (!tasks.length) return { eng, reports: '(no builder tasks)', critique: '(none)' }
  const builds = await parallel(tasks.map(t => () => agent(builderPrompt(round, t, eng), { label: `builder-r${round}-${t.id}`, phase: ph, model: S })))
  const reports = tasks.map((t, i) => `### Task ${t.id}\nBrief: ${t.brief}\n\nReport:\n${builds[i] || '(failed)'}`).join('\n\n')
  const das = await parallel(DA_DIRECTIONS.map(d => () => agent(daPrompt(round, d, reports, eng, plan), { label: `devils-advocate-r${round}-${d.id}`, phase: ph, model: S })))
  const critique = DA_DIRECTIONS.map((d, i) => `### Devil's advocate (${d.id})\n${das[i] || '(failed)'}`).join('\n\n')
  return { eng, reports, critique }
}

phase('Plan')
const plan1 = await agent(leadPlanPrompt(1, null), { label: 'research-lead-plan', phase: 'Plan', schema: LEAD_SCHEMA, model: O })
if (!plan1) return { error: 'research lead failed' }
log(`Round 1: ${(plan1.tasks || []).length} task(s)`)
const r1 = await runRound(1, plan1, 'Round 1')

phase('Review')
const hist1 = `### Research lead plan (round 1)\n${JSON.stringify(plan1, null, 2)}\n\n### Engineer (round 1)\n${r1.eng || '(none)'}\n\n### Round 1 builder reports\n${r1.reports}\n\n### Round 1 devil's advocates\n${r1.critique}`
const plan2 = await agent(leadPlanPrompt(2, hist1), { label: 'research-lead-review', phase: 'Review', schema: LEAD_SCHEMA, model: O })
let r2 = null
if (plan2 && (plan2.tasks || []).length) {
  log(`Round 2: ${plan2.tasks.length} task(s)`)
  r2 = await runRound(2, plan2, 'Round 2')
}

phase('Final')
const hist2 = `${hist1}\n\n### Research lead plan (round 2)\n${JSON.stringify(plan2, null, 2)}\n\n${r2 ? `### Engineer (round 2)\n${r2.eng || '(none)'}\n\n### Round 2 builder reports\n${r2.reports}\n\n### Round 2 devil's advocates\n${r2.critique}` : '(no round 2)'}`
const final = await agent(`You are the RESEARCH LEAD writing the final report of this workflow for the user (a non-specialist).
${CONTEXT}
## This workflow
${hist2}
Write ${PROJ}/RESULTS.md: what was found, how the evaluation changed and why, the best results with their caveats and the devil's advocates' findings alongside them, what was tested and what the evidence does and does not support, and what you would do next. Plain English, concise. Return the full text.`, { label: 'research-lead-final', phase: 'Final', model: O })

return { plan1, round1: r1, plan2, round2: r2, final }
