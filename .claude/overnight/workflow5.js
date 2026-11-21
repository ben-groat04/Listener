// Workflow 5: re-examine the assumptions and arbitrary numbers in the existing models and the evaluation, whether tuning them helps, and whether the set of folds is also arbitrary.
// MAIN-SESSION NOTES (not for agents):
// - Never message/stop/restart a running workflow; the user's latest message is auto-forwarded to every agent, so launch only right after a neutral message ("go").
// - Pre-launch Sonnet audit must check every item in .claude/workflow-notes.md, every paraphrase of user input against its verbatim source, and the GATES list below.
// - Recreate the ~5 min status cron + Monitor on journal.jsonl. The overnight hook override is gone: the Workflow tool asks for approval at launch (3 Opus lead agents: plan, review, final).
// - Not in this workflow: sealed prep/run, candidate-song search.
//
// GATES (each is flag-only: nothing retries or blocks an agent; flags are passed to the leads, who judge):
//  G1 builder wall-clock cap: flagged if self-reported duration > 1.25 x cap. No floor. Finishing early legitimately costs nothing.
//  G2 builder checklist: every mandatory id must appear with status + evidence; missing ids / 'impossible' without a real explanation are flagged. Claiming 'done' falsely is caught by the devil's advocate re-check rows, not by the script.
//  G3 devil's advocate coverage: one verdict per numbered builder headline claim, every checklist id re-checked, evalkit and predictor code files listed, null control re-run reported. Gaps are flagged. No duration check of any kind.
//  G4 conditional steps: round-2 engineer runs iff the lead's evaluation_changes is non-empty; prep runs iff shared_prep is non-empty (and writes a NEW versioned directory, so nothing depends on a file the script cannot change); round 2 runs iff the lead's tasks is non-empty. The lead can set each, and can set prep_after_engineer so prep starts after the engineer instead of in parallel. Lead fields that are empty or just 'none'/'n/a'/'no change' count as empty. Task ids are sanitised and de-duplicated in the script.
//  G5 failed (null) agents are logged and passed on as '(failed)'; no automatic retry.
export const meta = {
  name: 'taste-workflow-5',
  description: 'Workflow 5: inventory of assumptions and arbitrary numbers in the existing models and evaluation, Opus research lead plans, engineer + shared prep + builders + devil\'s advocates, lead review, optional round 2, final report',
  phases: [
    { title: 'Inventory', detail: '5 inventory agents + coverage critic (Sonnet)', model: 'sonnet' },
    { title: 'Plan', detail: 'research lead (Opus)', model: 'opus' },
    { title: 'Round 1', detail: 'engineer + shared prep, then builders + 2 devil\'s advocates each', model: 'sonnet' },
    { title: 'Lead review', detail: 'research lead (Opus)', model: 'opus' },
    { title: 'Round 2', detail: 'engineer + shared prep, then builders + 2 devil\'s advocates each', model: 'sonnet' },
    { title: 'Final', detail: 'research lead (Opus) final report', model: 'opus' },
  ],
}

const ROOT = '/home/user/Listener'
const PROJ = ROOT + '/taste-model'
const SCRATCH = '/tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf5'
const DOCS = SCRATCH + '/docs'          // one report file per agent: DOCS/<label>.md
const S = 'sonnet', O = 'opus'
// Sanitised copies of the Workflow 4 documents (user-attributed method ideas and next-step recommendations removed); the Workflow 3 copies are also sanitised.
const W4_DIR = PROJ + '/reports/w4-sanitised'
const W3_DIR = PROJ + '/reports/w3-sanitised'

// Process limits (wall-clock minutes), one place only.
const PREP_MAX = 120
const R1_BUILDER_MAX = 120, R2_BUILDER_MAX = 90
const LATE_CAP = 2

// Single source of truth for folder and path names. Briefs written by the lead must not name folders; these win on any conflict.
const scratchOf = (label) => SCRATCH + '/' + label
const docOf = (label) => DOCS + '/' + label + '.md'
const predOf = (round, id) => PROJ + '/predictors/w5r' + round + '-' + id
const sharedOf = (round) => PROJ + '/.cache/shared-w5r' + round
const OLD_SHARED = PROJ + '/.cache/shared'   // Workflow 4's shared inputs: read-only for everyone

// Lead-output normalisation: empty-ish text fields count as empty; task ids are sanitised and de-duplicated.
const EMPTYISH = /^\s*(none|n\/?a|no changes?)\.?\s*$/i
const cleanText = (x) => (typeof x !== 'string' || !x.trim() || EMPTYISH.test(x)) ? '' : x
const normPlan = (plan) => {
  if (!plan) return plan
  plan.evaluation_changes = cleanText(plan.evaluation_changes)
  plan.shared_prep = cleanText(plan.shared_prep)
  plan.prep_after_engineer = plan.prep_after_engineer === true
  const seen = new Set()
  plan.tasks = (Array.isArray(plan.tasks) ? plan.tasks : []).filter(t => t && typeof t.brief === 'string' && t.brief.trim()).slice(0, 3).map(t => {
    let id = String(t.id || '').toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, '') || 'task'
    const base = id
    for (let k = 2; seen.has(id); k++) id = base + '-' + k
    if (id !== t.id) log(`task id "${t.id}" renamed to "${id}"`)
    seen.add(id)
    return { ...t, id }
  })
  return plan
}
// Shared inputs: list of { round, dir, doc } for every directory the prep agents were asked to build.
const sharedBlock = (shared) => shared.length
  ? shared.map(x => `- ${x.dir}/ (round ${x.round}; MANIFEST.txt inside) built by the shared-prep agent whose report is ${x.doc}`).join('\n') + `\nUse a shared directory only if its DONE file exists; if DONE is missing, treat that directory as unusable (it was not finished) and say so in your report. ${OLD_SHARED}/ (Workflow 4) remains readable.`
  : '(no shared artefacts this workflow; only the read-only Workflow 4 inputs in ' + OLD_SHARED + '/)'

const CONTEXT = `
## Goal of this workflow
- Consider the huge amount of assumptions and arbitrary numbers used in the existing models, and whether tuning them helps.
- A follow-up question: is the set of folds also arbitrary?
- Decision threshold for dev results: about 80% intervals are enough; 95% is not required. This is the project owner's risk preference. Use it for dev decisions and for how results are described. Pass criteria for any sealed run are not part of this workflow.

## The user's words on this project (verbatim)
- "I want a workflow set up to attempt to analyse my music taste and do as well as possible on predicting new songs I haven't listened to. I guess you can create training sets based on say my listening up to a certain date and see how well it gets some of my favourite tracks after that. DO NOT STEER THE WORKFLOW IN ANY WAY it will decide on the best way to do it itself with research etc. It needs to analyse the music deeply, not just by artist etc. you'll need a devils advocate in there because otherwise it'll default to assuming artist etc is a good way of predicting."
- "Use all the music there then."
- On the Last.fm API key (offered as an option): "Id skip it because this is exactly the type of oversimplified analysis I warned about"
- "End goal should be to find candidate songs but don't do this until it is proven to work VERY WELL"
- Answers to earlier questions:
  1. On the success bar: "The bar is just keep pushing as good as you can. BE UNREASONABLY AMBITIOUS."
  2. On building an open-catalogue test: "I will not answer this, it's for the agent to decide. No steering."
  3. On allowing models that need trust_remote_code: "Yes that's fine."
  4. On which parts of songs: "It varies. Again, I will not steer."
  5. On the "Best Songs" playlist as a signal: "That is the better subset but the strictness of the bar to get in there is not consistent over time."
- Later, on the gate before finding candidate songs: "there is no set "bar" as such"
- After Workflow 2: "Is the score calculation good? In the next workflow a lot of things you've been treating as fixed need to be re-investigated. Because with the current scoring system let's be honest with the subjectivity you won't be going super super high"
## Unvetted ideas raised in discussion
These came up in chat. They are not from an expert, they may well not be the best way to work, and they carry no more weight than any other hypothesis. Test them on the evidence like anything else, and drop them if the data says so.
- How people listen to and discover music may be worth thinking about.
- The data is very noisy, so it may be necessary to act more on loose trends and correlation; expecting a clear result may be foolish.
- One view is that the project may have settled into habits.
- Listening frequency and statistics may be the most reliable indicator of taste at any given time.
- Many liked songs may be liked for specific parts of the music.
- The "loved" definition may be arbitrary but probably does a good job; like everything of this kind, it can be varied if performance plateaus.
- Taste changed a lot early on, so the oldest music may be of limited use; analysis will tell.

## Facts
- Data came from the user's stats.fm profile. Full listening history 2020-2026: ${ROOT}/spotify-liked-songs/.cache/streams.jsonl (147,256 JSON lines, newest first). The only other file you may read from ${ROOT}/spotify-liked-songs/ and its .cache/ is whatever the evalkit loader and README name as their inputs (top_tracks.json only through evalkit.data.load_meta).
- Evaluation harness: ${PROJ}/evalkit/ (read its README; currently v4.1). It was built by earlier agents and everything about it is open to change.
- Earlier work: ${PROJ}/predictors/ (Workflow 3 and 4 predictors; w4-shared-prep holds the Workflow 4 feature-preparation code) and ${PROJ}/.cache/ (caches). Workflow 4's shared inputs are in ${OLD_SHARED}/ (read-only; its MANIFEST.txt is stale for one harness cache file).
- Earlier workflows' results, the ONLY earlier-workflow documents you may read: ${W4_DIR}/ (start with RESULTS.md; one file per agent report) and ${W3_DIR}/ (start with RESULTS.md). Both are sanitised copies.
- Held-out state, from those results: the harness LATE slice has 23 logged runs and its results were seen by every agent of Workflow 4; the artist-disjoint HOLDOUT slice has had its single-use budget spent (4 real finals, budget 0) and its numbers were seen by Workflow 4's round-2 agents. Both count as partly used up. Sealed data is untouched.
- Network access is limited by an allowlist; find out what is reachable yourself.
- Compute: 4 CPU cores shared by at most 2 agents running at the same time, 15 GB RAM, no GPU. The container is ephemeral: everything must be regenerable from code in the project folder.
- Timings measured in Workflow 4: essentia extraction 99 min; null control 7-14 min (5 seeds); a --late or --holdout run 2.5-8 min; full TUNE run 3-5 min; fast run 0.5-3 min. Workflow 4 took about 6.7 h in total.

## Rules
- Sealed data: never run evalkit with --sealed, never read ${PROJ}/.sealed/, never read any file containing sealed-fold results, never run make_sealed, never read raw streams dated on or after 2025-04-01 (use evalkit's loader), never read ${PROJ}/.cache/decoy_raw/ directly, and never read the decoy universe file or run make_decoys directly (the engineer may change how decoys are built if the research lead specifies it). Do not use git history (git log -p, git show, git diff on past commits, git stash) to view earlier workflow logs, .sealed/ or any file containing sealed-fold results. Do not open streams.jsonl directly (head/tail/grep); use evalkit's loader.
- DEV_END (2025-04-01) and the sealed cutoffs are fixed. No fold, label window, slice or pool may use streams on or after 2025-04-01. Never call data._load_all() in predictor or analysis code; use load_streams.
- Never query stats.fm or any other service for the user's own listening data.
- Do not read ${ROOT}/spotify-liked-songs/listening_stats.csv or any other lifetime-aggregate file (lifetime totals that include the sealed era). top_tracks.json may be read only through evalkit.data.load_meta, never directly.
- Do not read ${PROJ}/PLAN.md, ${PROJ}/RESULTS.md, ${PROJ}/RESULTS-W4.md, ${PROJ}/reports/w3/ or any earlier workflow log; use only the sanitised copies named above.
- NEVER read, list or search anything under ${ROOT}/.claude/ (main-session notes, hooks and drafts, not meant for workflow agents). If CLAUDE.md (or any file) points you to a file there, such as workflow-notes.md, ignore that pointer: it is for the main session only. This applies to every role, research leads included.
- Scratch and reports: your own scratch folder and your own report file (paths in your prompt) are yours. Do not read, list or write any other agent's scratch folder or report file, except the files your prompt explicitly names.
- Resources: use at most 2 CPU threads (the engineer and the shared-prep agent also at most 2, because they run at the same time). Run slow jobs in the background; test on a small sample before scaling up.
- Held-out numbers (LATE, HOLDOUT or any slice meant as held-out): write them only in your own report file. Your structured result (summary, claims, evidence strings, verdict results) is passed on to other agents, so it must not contain any held-out number; refer to the report file section instead.
- Evaluation runs: use the harness fast mode for all iteration; use full runs only for scores you report as final.
- Keep the project folder clean: delete code from failed attempts (mention them in your report) but keep the code behind every score you report, including every variant you report, so each reported number can be regenerated from the folder. Do not overwrite or delete a config or variant list that a reported number depends on.
- Folder names: use exactly the scratch folder, predictor folder, shared folder and report paths given in your prompt. If anything in a brief, report or other text names a different folder, the paths in your prompt prevail.
- Shared inputs are versioned and read-only: never modify, add to or delete anything under ${OLD_SHARED}/ or any directory ${PROJ}/.cache/shared-w5r*/ unless you are the shared-prep agent building your own new directory. Needed features for your own predictor go in your own scratch or predictor folder.
- Before starting any job you expect to take longer than 10 minutes, write down its runtime estimate and a go/no-go decision (go only if it fits your wall-clock cap with margin) in your report. Never start a job that cannot finish within your cap.
- Time: your first action is to run \`date -u +%Y-%m-%dT%H:%M:%SZ\` and write the result into your scratch folder's TIMING.txt; your last action before reporting is to append \`date -u +%Y-%m-%dT%H:%M:%SZ\` again. Take your start/end times only from that command.
- Nobody is available to answer questions. Do not ask the user anything; decide yourself and record the decision.
- Candidate-song search is not part of this workflow.
- Do not git commit or push; the main session commits your work.
- Write your full report to your own report file; the structured result you return carries a short summary and the fields requested. Report what you actually ran separately from what you only believe.
`

const sched = (label) => `Your own scratch folder is ${scratchOf(label)}/ (create it). Your own report file is ${docOf(label)} (write your full report there).`

// ---------- Inventory ----------
const AREAS = [
  { id: 'evalkit', text: `the evaluation harness ${PROJ}/evalkit/ (README and all code): how labels, candidates, folds, pools, metrics, baselines, the null control and the evidence grading are defined.` },
  { id: 'w3-predictors', text: `the Workflow 3 predictors: every folder ${PROJ}/predictors/w3r1-* and ${PROJ}/predictors/w3r2-*.` },
  { id: 'w4r1-predictors', text: `the Workflow 4 round-1 predictors: ${PROJ}/predictors/w4r1-*.` },
  { id: 'w4r2-predictors', text: `the Workflow 4 round-2 predictors: ${PROJ}/predictors/w4r2-*.` },
  { id: 'features', text: `the feature and data preparation behind the models: ${PROJ}/predictors/w4-shared-prep/, the earlier feature-extraction code reachable from the predictors, and the data-loading and fetching code in ${PROJ}/evalkit/ as far as it shapes the model inputs.` },
]

const INV_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: 'At most 300 words: what you found, the biggest groups of items, and anything you could not cover' },
    n_items: { type: 'integer', description: 'Number of rows in your inventory table' },
    n_reason_found: { type: 'integer', description: 'Number of rows for which a reason or evidence for the value was found' },
    n_variation_found: { type: 'integer', description: 'Number of rows for which a variation or test of the value was found somewhere' },
    files_read: { type: 'array', items: { type: 'string' }, description: 'Code and doc files you read' },
  },
  required: ['summary', 'n_items', 'n_reason_found', 'n_variation_found', 'files_read'],
}

const inventoryPrompt = (a) => `You are an INVENTORY AGENT (${a.id}). You do not build or tune anything. You list, with evidence, every assumption and every chosen number in this part of the project: ${a.text}
${CONTEXT}
${sched('inventory-' + a.id)}
Task: read the code and the documents in your area and produce a complete inventory table in your report file, one row per item, where an item is an assumption made, or a number that was chosen (by hand, by convention or by a quick trial) rather than derived from data. For each row give: id; file and line; what it is; its value; kind (assumption, number, or both); the reason or evidence for the value that you found in the code, the README or the sanitised reports (or "none found"); whether any variation or test of it was found anywhere (cite where, or "none found"); whether the choice feeds the final scores directly. Be exhaustive within your area: go file by file and function by function and do not stop at the obvious ones. Do not judge or recommend; report facts. You may run tiny dev-only checks to confirm a value, but do not run experiments.
Return the structured result: its counts must match your table.`

const CRITIC_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: 'At most 300 words' },
    n_missing: { type: 'integer', description: 'Number of items found that the inventories lack' },
    n_checked: { type: 'integer', description: 'Number of code locations you checked against the inventories' },
  },
  required: ['summary', 'n_missing', 'n_checked'],
}

const criticPrompt = (invs) => `You are the INVENTORY COVERAGE CRITIC. Five inventory agents each listed the assumptions and chosen numbers in one area of the project. Find what they missed.
${CONTEXT}
${sched('inventory-critic')}
Inventory reports (read all of them; each is a table in its own file):
${AREAS.map((a, i) => `- ${a.id}: ${docOf('inventory-' + a.id)}${invs[i] ? ` (${invs[i].n_items} rows; summary: ${invs[i].summary})` : ' (FAILED, no report)'}`).join('\n')}
Method: independently go through the code in ${PROJ}/evalkit/ and ${PROJ}/predictors/ (all folders), find assumptions and chosen numbers, and check each against the inventories. Sample at least every file once; do not stop at the first misses. Write every item that is missing from the inventories into your report file in the same table format as theirs (including any area for which an inventory agent failed). Facts only; do not judge or recommend.`

// ---------- Lead ----------
const LEAD_SCHEMA = {
  type: 'object',
  properties: {
    assessment: { type: 'string', description: 'Your assessment of where the project stands with respect to the goal of this workflow' },
    goal_coverage: { type: 'string', description: 'For each element of the goal (assumptions and numbers in the existing models; whether tuning them helps; whether the set of folds is also arbitrary) which task(s) or engineer change address it and how its answer will be judged, or why it is not addressed' },
    evaluation_changes: { type: 'string', description: 'Precise spec of changes to the evaluation/harness for the engineer to implement, or empty string if none' },
    shared_prep: { type: 'string', description: 'Precise spec of every shared artefact (including feature extraction that more than one builder, or any builder at scale, would need) to be built ONCE and published to all builders at the same time in a new versioned directory (given in the shared-prep prompt), or empty string if none. Builders cannot create or change shared inputs.' },
    prep_after_engineer: { type: 'boolean', description: 'true if shared prep must run AFTER the engineer finishes (it needs the changed harness); false to run them in parallel' },
    tasks: {
      type: 'array', maxItems: 3,
      items: { type: 'object', properties: { id: { type: 'string', pattern: '^[a-z0-9-]+$', description: 'short slug: lowercase letters, digits, hyphens; unique among your tasks' }, brief: { type: 'string', description: 'self-contained task brief for one independent builder. Do not name folders or paths for scratch/predictor/shared/report files (the workflow assigns them).' } }, required: ['id', 'brief'] },
    },
    checklist: {
      type: 'array',
      description: 'One entry per document or check in your coverage list',
      items: { type: 'object', properties: { item: { type: 'string' }, status: { type: 'string', enum: ['done', 'impossible', 'not_done'] }, evidence: { type: 'string' } }, required: ['item', 'status', 'evidence'] },
    },
  },
  required: ['assessment', 'goal_coverage', 'evaluation_changes', 'shared_prep', 'prep_after_engineer', 'tasks', 'checklist'],
}

const leadPlanPrompt = (round, history, coverage) => `You are the RESEARCH LEAD. You own the experiment design and the direction of this workflow. You do not build predictors yourself.
${CONTEXT}
${sched('lead-r' + round)}
${history}
Process facts for sizing the work: the workflow runs, in order, an engineer (harness changes) and a shared-prep step (at the same time by default; one after the other if you set prep_after_engineer; shared prep cap ${PREP_MAX} min), then the builders, each followed by two devil's advocates as soon as that builder finishes. At most 2 agents run at once, so builders and devil's advocates queue. Each builder has a wall-clock cap of ${round === 1 ? R1_BUILDER_MAX : R2_BUILDER_MAX} min and a mandatory checklist (no time floor). Builders cannot create or change shared inputs, so anything heavy that builders need (feature extraction, downloads, pool changes) must be in shared_prep, which is built into a new versioned directory. The harness caps --late runs at ${LATE_CAP} per predictor bundle. Folder and report names are assigned by the workflow; do not specify them in briefs.
In Workflow 4 each builder scored 30-95 variants on TUNE. Held-out state is in the facts above.
Decide, for yourself and with reasons:
1. How the goal of this workflow is to be addressed, using the inventories and anything you are permitted to read; whether and how the evaluation should change (anything about it may change, including how held-out evidence is obtained given the state above).
2. Any shared artefacts to be built once (versioned; published to all builders at the same time).
3. Up to 3 independent builder tasks for round ${round}. Each brief must be self-contained (builders see the shared context above, their own brief and the engineer's report file). Builders work independently and must not depend on each other. Write briefs in your own words; do not paste reviewer, builder or devil's-advocate text into them, and do not put any score from a slice meant as held-out into a brief. Size each task to fit its wall-clock cap.
Every builder will be required to: use the harness fast mode for all iteration; run a null control on its final predictor; give paired comparisons against every harness baseline (including artist_recent) and, as a diagnostic that is not a harness baseline, pool_artist_siblings; report held-out slices separately from the slice it iterated on; investigate, not drop, below-chance results; count every variant it scored; and state the strongest case against its own result. Whether held-out evidence is obtained, and which, is your decision (the builders' held_out_slices_reported_separately item is satisfied by 'none available' with harness evidence). Specify in evaluation_changes anything else the harness must provide.
Verify claims you rely on by reading code or running quick dev-only checks.
Coverage list (fill the checklist, one entry per line, with evidence; flags below are passed to you by the script and are facts, not verdicts):
${coverage}`

// ---------- Engineer / prep ----------
const engineerPrompt = (round, plan) => `You are the ENGINEER (round ${round}). Implement exactly the research lead's specification below, plus the standing harness-hygiene requirements, no more. A shared-prep agent works on feature inputs (at the same time as you, or after you if the plan says so); do not touch its directory, and it does not touch evalkit.
${CONTEXT}
${sched('engineer-r' + round)}
## Evaluation changes to implement (research lead)
${plan.evaluation_changes || '(none)'}
## Standing harness-hygiene requirements (every round)
- DEV_END (2025-04-01) and the sealed cutoffs are fixed: no fold, label window, slice or pool you build may use streams on or after 2025-04-01. Never call data._load_all() in harness, predictor or analysis code; use load_streams.
- Version the harness: only bump its version if code changed (if nothing changed, say so and leave the version alone); when you bump it, add a changelog entry to the README, and state which earlier numbers remain comparable. Any change that alters existing numbers must be selectable (flag or version) so the previous version's numbers can still be regenerated; label every table the harness prints with the harness version.
- Fit/feature cache keys must include the random seed and any relabelled or shuffled label identities. The selftest must assert that 3 null-control seeds give different results and must fail otherwise.
- Keep the --late cap (${LATE_CAP} per predictor bundle), logging, and read-only per-run output tables. Do not add or reset any held-out budget unless the specification asks for it; any counter or state file you add must be regenerable from code or documented in the README.
- Harness caches go under ${PROJ}/.cache/evalkit-cache/, never in any shared directory.
- A --holdout (and --late) run must print only the held-out slice's numbers, never pooled DEV or pooled dev+held-out numbers.
- Run the selftest and all baselines (dev only) after your changes.
Report facts only: what you changed, how to use it, current dev baseline scores with the harness version, whether earlier scores remain comparable, how long each job took, and anything in the spec you could not do and why. Do not build shared artefacts.`

const prepPrompt = (round, plan) => `You are the SHARED-PREP agent (round ${round}). Build exactly the shared artefacts specified below, once, in a NEW directory, so that every builder starts from identical inputs. An engineer works on evalkit (at the same time as you, or before you if the plan says so); do not touch evalkit.
${CONTEXT}
${sched('prep-r' + round)}
## Shared artefacts to build and publish in ${sharedOf(round)}/ (research lead)
${plan.shared_prep}
Process:
1. Create ${sharedOf(round)}/ yourself. Never modify anything in ${OLD_SHARED}/ or in any other existing shared directory; read from them freely.
2. Before long jobs, estimate runtime and decide go/no-go; hard wall-clock cap for this whole step is ${PREP_MAX} min. If something cannot finish within the cap, build the complete subset, state exactly what coverage is missing, and do not leave half-written files.
3. Everything must be complete before you finish. Then write ${sharedOf(round)}/MANIFEST.txt (every file or directory, format, row/clip counts, coverage, sha256 of each non-bulk file) and finally an empty file ${sharedOf(round)}/DONE. Nothing in that directory may change afterwards; builders and devil's advocates will check the manifest.
4. Nothing outside the spec may be added.
Report facts only: where each artefact is (location and format only; do not name methods or models), coverage, how long each job took, and anything you could not do and why.`

// ---------- Builders ----------
const CHECK_IDS = ['fast_mode_for_iteration', 'full_run_final_scores', 'held_out_slices_reported_separately', 'null_control', 'paired_baselines_incl_artist_siblings_and_artist_recent', 'below_chance_investigated', 'variants_counted_and_selection_accounted', 'strongest_case_against', 'runtime_estimates_and_actuals', 'code_behind_every_reported_score_kept', 'ran_vs_believed_separated']

const BUILDER_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: 'At most 400 words: what you did and found, with the key dev numbers and the harness version they come from; no held-out numbers' },
    start_utc: { type: 'string', description: 'ISO start time from date -u +%Y-%m-%dT%H:%M:%SZ at your first action' },
    end_utc: { type: 'string', description: 'ISO end time from date -u +%Y-%m-%dT%H:%M:%SZ at your last action' },
    null_control_result: { type: 'string', description: 'The null-control verdict and numbers for your final predictor (or why impossible); no held-out numbers' },
    late_runs_used: { type: 'integer', description: 'Number of --late runs you made' },
    headline_claims: { type: 'array', items: { type: 'string' }, description: 'Every headline claim of your report, one per entry, each a single checkable sentence with its number; for claims about a held-out slice give no number (it is in the report file)' },
    checklist: {
      type: 'array',
      description: 'One entry for EACH of these ids: ' + CHECK_IDS.join(', '),
      items: { type: 'object', properties: { id: { type: 'string', enum: CHECK_IDS }, status: { type: 'string', enum: ['done', 'impossible', 'not_done'] }, evidence: { type: 'string', description: 'Where in your report or files it is, or why it was impossible' } }, required: ['id', 'status', 'evidence'] },
    },
  },
  required: ['summary', 'start_utc', 'end_utc', 'null_control_result', 'late_runs_used', 'headline_claims', 'checklist'],
}

const builderPrompt = (round, task, engDoc, shared, label) => `You are a BUILDER (round ${round}, task "${task.id}"). Other builders work independently; do not read or edit their folders, scratch or report files.
${CONTEXT}
${sched(label)}
Your predictor code folder is ${predOf(round, task.id)}/ (entry file the harness accepts). Use only these folders.
Files you may read in addition to the sanitised reports: the latest engineer's report ${engDoc || '(no engineer report)'} (when there is no engineer step this round it is the earlier round's report and the harness is unchanged), and every shared-input directory with its prep report:
${sharedBlock(shared)}
Read the reports before you start.
## Your task (from the research lead)
${task.brief}

Time: wall-clock cap ${round === 1 ? R1_BUILDER_MAX : R2_BUILDER_MAX} minutes from your first action; stop starting new work at about 80% of it and write your report. There is no minimum time: finish when the checklist below is complete and your task is answered. Heavy jobs: give a runtime estimate and go/no-go first; anything you need at scale that is not in the shared inputs must fit the cap or be dropped (you may not change shared inputs).
Evaluation: use the harness fast mode for ALL iteration; use full (slow) runs only for the scores you report as final. Use --late at most ${LATE_CAP} times in total for your final predictor. Write your final predictor and its declaration in your report BEFORE any --late or held-out run, and do not change the predictor afterwards (if you must, say so and report both).
Mandatory before you report; return one checklist entry per id, each with evidence, and put the matching content in your report file (a gap is flagged to the leads, so say plainly if something is impossible and why):
- fast_mode_for_iteration: all iteration used fast mode
- full_run_final_scores: final scores from a full harness run
- held_out_slices_reported_separately: whether held-out evidence is obtained at all is the research lead's decision in your brief (given the held-out state in the facts). If your brief calls for it, report each held-out slice the harness provides separately from the slice you iterated on. If no held-out evidence is available or your brief does not call for it, state 'none available' with harness evidence (README, logs, remaining budget); that satisfies this item. Evidence strings point to the report file; no held-out numbers in them
- null_control: the null control for your final predictor (also put its result in null_control_result)
- paired_baselines_incl_artist_siblings_and_artist_recent: paired comparisons against every harness baseline, including artist_recent, and against pool_artist_siblings as a diagnostic (it is not a harness baseline)
- below_chance_investigated: any score that comes out below chance is investigated, not dropped
- variants_counted_and_selection_accounted: every variant you scored is counted, and how much selection could have inflated your final score is stated with evidence
- strongest_case_against: the strongest case against your own result
- runtime_estimates_and_actuals: runtime estimates made and actual runtimes of each long job
- code_behind_every_reported_score_kept: the code and configs behind every reported number are in your folder and regenerate it
- ran_vs_believed_separated: what you actually ran is separate from what you only believe
Also list every headline claim of your report in headline_claims (the devil's advocates will verify each one).`

// ---------- Devil's advocates ----------
const DA_DIRECTIONS = [
  { id: 'works', text: 'Attack every claim that a change IMPROVES results or that something works: gains not real, selection among many variants, leakage, shortcuts, overfitting to the iteration folds, simple signals doing the work, noise, flaws in the evaluation that flatter results.' },
  { id: 'dismissed', text: 'Attack every claim that a change makes NO difference, that an assumption or number was checked and found fine, that something does not work, or that something was left fixed or never tried: insufficient effort, bugs, unfair or wrong evaluation, poor tuning ranges, results dropped or ignored without investigation, assumptions treated as fixed.' },
]

const DA_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: 'At most 300 words, including the overall verdict; no held-out numbers' },
    claim_verdicts: {
      type: 'array',
      description: 'EXACTLY one entry for each numbered builder headline claim (claim_no), plus any extra claims you assessed',
      items: { type: 'object', properties: { claim_no: { type: 'integer' }, verdict: { type: 'string', enum: ['holds', 'does_not_hold', 'unverified'] }, what_i_ran: { type: 'string' }, result: { type: 'string', description: 'no held-out numbers (those go in your report file)' } }, required: ['claim_no', 'verdict', 'what_i_ran', 'result'] },
    },
    checklist_rechecked: { type: 'array', items: { type: 'string', enum: CHECK_IDS }, description: 'The ids of the builder checklist items you checked against code and output files (all of them are expected)' },
    code_files_read: { type: 'array', items: { type: 'string' }, description: 'Paths of the builder code files and evalkit code files you actually read' },
    null_control_rerun: { type: 'string', description: 'The builder\'s null-control check as YOU re-ran it: command and result' },
    shared_inputs_unchanged: { type: 'string', description: 'Result of checking every shared directory the builder used against its MANIFEST.txt (name each directory), or why there are none' },
  },
  required: ['summary', 'claim_verdicts', 'checklist_rechecked', 'code_files_read', 'null_control_rerun', 'shared_inputs_unchanged'],
}

const daPrompt = (round, dir, task, b, bLabel, engDoc, shared, plan, label) => `You are a DEVIL'S ADVOCATE (round ${round}, direction: ${dir.id}) for the builder of task "${task.id}". Another devil's advocate covers the opposite direction for the same builder; other builders have their own.
${CONTEXT}
${sched(label)}
${dir.text}
Your work is judged on coverage, not on duration; there is no time floor, so finish when every item below is covered with evidence:
- one verdict per numbered builder headline claim below (and any further claim you find in the report), each from code and output files, not from the report's wording;
- read the builder's code in ${predOf(round, task.id)}/ and the evaluation code in ${PROJ}/evalkit/ (list the files in code_files_read), and check the engineer's changes against the research lead's specification;
- re-check every builder checklist item below against code and files (list the ids in checklist_rechecked), including any duration or effort it reports against file timestamps and its TIMING.txt in ${scratchOf(bLabel)}/ (read-only for you);
- re-run the builder's null-control check yourself and report the command and result;
- independently re-run every headline score on the iteration slice that you assess (full runs allowed for that). Do NOT run --late or --holdout yourself: verify those claims from the harness's read-only per-run tables and run logs, which you may only read;
- check every shared directory listed below that the builder used (and has a DONE file) against its MANIFEST.txt.
Write your full report, led by a per-claim verification table, to your report file.
## Research lead's specification
${JSON.stringify({ evaluation_changes: plan.evaluation_changes, shared_prep: plan.shared_prep }, null, 1)}
## Reports (read these files)
- Engineer: ${engDoc || '(none)'}
- Shared inputs and prep reports (use a directory only if its DONE file exists):
${sharedBlock(shared)}
- Builder: ${docOf(bLabel)}
## Builder's numbered headline claims
${(b.headline_claims || []).map((c, i) => `${i + 1}. ${c}`).join('\n') || '(none listed)'}
## Builder's checklist entries (to re-check)
${(b.checklist || []).map(c => `- ${c.id}: ${c.status}: ${c.evidence}`).join('\n')}
## Builder's null-control result
${b.null_control_result}`

// ---------- Flags (G1-G3): facts for the leads, never a gate ----------
const minutes = (o) => {
  const a = Date.parse(o && o.start_utc), b = Date.parse(o && o.end_utc)
  return (isFinite(a) && isFinite(b)) ? (b - a) / 60000 : null
}
const minStr = (o) => { const m = minutes(o); return m === null ? 'unparseable timestamps' : m.toFixed(1) + ' min' }
const builderFlags = (b, cap) => {
  const f = []
  if (!b) return ['builder failed (no result)']
  const m = minutes(b)
  if (m === null) f.push(`start_utc/end_utc unparseable (${b.start_utc} / ${b.end_utc}); duration unknown`)
  else if (m < 0) f.push(`end_utc is before start_utc (${b.start_utc} / ${b.end_utc})`)
  else if (m > cap * 1.25) f.push(`self-reported duration ${m.toFixed(1)} min exceeded the ${cap} min cap`)
  for (const id of CHECK_IDS) {
    const c = (b.checklist || []).find(x => x.id === id)
    if (!c) f.push(`checklist id missing: ${id}`)
    else if (c.status !== 'done' && (!c.evidence || c.evidence.length < 20)) f.push(`checklist ${id} is ${c.status} without a real explanation`)
    else if (c.status !== 'done') f.push(`checklist ${id} is ${c.status}: ${c.evidence}`)
  }
  if (!b.null_control_result || b.null_control_result.length < 10) f.push('no null-control result')
  if (!b.headline_claims || !b.headline_claims.length) f.push('no headline claims listed')
  return f
}
const daFlags = (d, b) => {
  const f = []
  if (!d) return ['devil\'s advocate failed (no result)']
  const n = (b && b.headline_claims || []).length
  const covered = new Set((d.claim_verdicts || []).map(v => v.claim_no))
  for (let i = 1; i <= n; i++) if (!covered.has(i)) f.push(`no verdict for builder claim ${i}`)
  const unv = (d.claim_verdicts || []).filter(v => v.verdict === 'unverified').map(v => v.claim_no)
  if (unv.length) f.push(`${unv.length} claim(s) left unverified: ${unv.join(', ')}`)
  const re = new Set(d.checklist_rechecked || [])
  const miss = CHECK_IDS.filter(id => !re.has(id))
  if (miss.length) f.push('checklist items not re-checked: ' + miss.join(', '))
  if (!(d.code_files_read || []).some(x => /evalkit/.test(x))) f.push('no evalkit code file listed as read')
  if (!(d.code_files_read || []).some(x => /predictors/.test(x))) f.push('no builder code file listed as read')
  if (!d.null_control_rerun || d.null_control_rerun.length < 10) f.push('builder null-control check not re-run')
  return f
}
const flagLine = (f) => f.length ? 'FLAGS: ' + f.join('; ') : 'flags: none'

const fmtBuilder = (b, label, cap) => b ? `### Builder ${label}\nreport file: ${docOf(label)}\nself-reported duration ${minStr(b)} (cap ${cap}); late runs used: ${b.late_runs_used}\n${flagLine(builderFlags(b, cap))}\nNull control: ${b.null_control_result}\nSummary: ${b.summary}` : `### Builder ${label}\n(failed)`
const fmtDA = (d, label, b) => d ? `### Devil's advocate ${label}\nreport file: ${docOf(label)}\n${flagLine(daFlags(d, b))}\nverdicts: ${(d.claim_verdicts || []).map(v => `${v.claim_no}:${v.verdict}`).join(' ')}\nshared inputs: ${d.shared_inputs_unchanged}\nSummary: ${d.summary}` : `### Devil's advocate ${label}\n(failed)`

const runRound = async (round, plan, prev) => {
  const ph = round === 1 ? 'Round 1' : 'Round 2'
  const engLabel = 'engineer-r' + round, prepLabel = 'prep-r' + round
  const doEng = round === 1 || !!plan.evaluation_changes
  const doPrep = !!plan.shared_prep
  const runEng = () => doEng ? agent(engineerPrompt(round, plan), { label: engLabel, phase: ph, model: S }) : Promise.resolve(null)
  const runPrep = () => doPrep ? agent(prepPrompt(round, plan), { label: prepLabel, phase: ph, model: S }) : Promise.resolve(null)
  let eng, prep
  if (plan.prep_after_engineer && doEng && doPrep) {
    // the lead asked for prep to see the engineer's finished harness
    eng = await runEng()
    prep = await runPrep()
  } else {
    // engineer and shared prep run at the same time (they touch different folders)
    ;[eng, prep] = await parallel([runEng, runPrep])
  }
  if (doEng && !eng) log(`WARNING: ${engLabel} failed; builders proceed without an engineer report`)
  if (doPrep && !prep) log(`WARNING: ${prepLabel} failed; builders are told its report is (failed) and may use its directory only if DONE exists`)
  const engDoc = doEng ? (eng ? docOf(engLabel) : '(failed)') : (prev ? prev.engDoc : null)
  const shared = (prev ? prev.shared : []).slice()
  if (doPrep) shared.push({ round, dir: sharedOf(round), doc: prep ? docOf(prepLabel) : '(failed)' })
  const tasks = plan.tasks || []
  if (!tasks.length) return { eng, prep, engDoc, shared, builders: '(no builder tasks)', das: '(none)' }
  const cap = round === 1 ? R1_BUILDER_MAX : R2_BUILDER_MAX
  // each builder, then its two devil's advocates as soon as it finishes (no barrier across builders); no retries
  const out = await pipeline(
    tasks,
    (t) => agent(builderPrompt(round, t, engDoc, shared, 'builder-r' + round + '-' + t.id), { label: 'builder-r' + round + '-' + t.id, phase: ph, model: S, schema: BUILDER_SCHEMA }),
    async (b, t) => {
      if (!b) { log(`WARNING: builder-r${round}-${t.id} failed; no devil's advocates for it`); return { b: null, das: [] } }
      const bLabel = 'builder-r' + round + '-' + t.id
      const flags = builderFlags(b, cap)
      if (flags.length) log(`builder ${bLabel} flags: ${flags.join('; ')}`)
      const das = await parallel(DA_DIRECTIONS.map(d => () => agent(daPrompt(round, d, t, b, bLabel, engDoc, shared, plan, 'devils-advocate-r' + round + '-' + t.id + '-' + d.id), { label: 'devils-advocate-r' + round + '-' + t.id + '-' + d.id, phase: ph, model: S, schema: DA_SCHEMA })))
      das.forEach((d, j) => { const f = daFlags(d, b); if (f.length) log(`devil's advocate r${round}-${t.id}-${DA_DIRECTIONS[j].id} flags: ${f.join('; ')}`) })
      return { b, das }
    },
  )
  const builders = tasks.map((t, i) => `Task ${t.id}\nBrief: ${t.brief}\n${fmtBuilder(out[i] && out[i].b, 'builder-r' + round + '-' + t.id, cap)}`).join('\n\n')
  const das = tasks.map((t, i) => DA_DIRECTIONS.map((d, j) => fmtDA(out[i] && out[i].das[j], 'devils-advocate-r' + round + '-' + t.id + '-' + d.id, out[i] && out[i].b)).join('\n\n')).join('\n\n')
  return { eng, prep, engDoc, shared, builders, das }
}

// ===================== run =====================
phase('Inventory')
const invs = await parallel(AREAS.map(a => () => agent(inventoryPrompt(a), { label: 'inventory-' + a.id, phase: 'Inventory', model: S, schema: INV_SCHEMA })))
invs.forEach((r, i) => { if (!r) log(`WARNING: inventory-${AREAS[i].id} failed`) })
const critic = await agent(criticPrompt(invs), { label: 'inventory-critic', phase: 'Inventory', model: S, schema: CRITIC_SCHEMA })
const invText = `## Inventories of assumptions and chosen numbers (read the files)\n` + AREAS.map((a, i) => `- ${a.id}: ${docOf('inventory-' + a.id)}${invs[i] ? ` | ${invs[i].n_items} rows, ${invs[i].n_reason_found} with a reason found, ${invs[i].n_variation_found} with a variation found | ${invs[i].summary}` : ' | FAILED'}`).join('\n') +
  `\n- coverage critic (items missing from the inventories): ${docOf('inventory-critic')}${critic ? ` | ${critic.n_missing} missing, ${critic.n_checked} locations checked | ${critic.summary}` : ' | FAILED'}`

phase('Plan')
const coverage1 = [
  'read every inventory file and the critic file (one entry each)',
  `read ${W4_DIR}/RESULTS.md and the ${W3_DIR}/RESULTS.md`,
  'read the evalkit README and the fold, label and pool code',
  'verified at least one claim you rely on by a quick dev-only check, or stated why not',
  'goal_coverage addresses every element of the goal',
].map(x => '- ' + x).join('\n')
const plan1 = normPlan(await agent(leadPlanPrompt(1, invText, coverage1), { label: 'research-lead-plan', phase: 'Plan', schema: LEAD_SCHEMA, model: O }))
if (!plan1) return { error: 'research lead failed', invText }
log(`Round 1: ${(plan1.tasks || []).length} task(s); engineer changes: ${plan1.evaluation_changes ? 'yes' : 'standing hygiene only'}; shared prep: ${plan1.shared_prep ? 'yes' : 'no'}`)

phase('Round 1')
const r1 = await runRound(1, plan1)

phase('Lead review')
const hist1 = `${invText}\n\n## Research lead plan (round 1)\n${JSON.stringify({ assessment: plan1.assessment, goal_coverage: plan1.goal_coverage, evaluation_changes: plan1.evaluation_changes, shared_prep: plan1.shared_prep, tasks: plan1.tasks }, null, 1)}\n\n## Engineer round 1\n${r1.eng ? 'report file: ' + docOf('engineer-r1') : '(none)'}\n\n## Shared prep round 1\n${r1.prep ? 'report file: ' + docOf('prep-r1') + ' (inputs in ' + sharedOf(1) + '/)' : '(none)'}\n\n## Round 1 builders\n${r1.builders}\n\n## Round 1 devil's advocates\n${r1.das}`
const coverage2 = [
  'read every builder report file and every devil\'s advocate report file of round 1 (one entry each)',
  'for each builder, re-ran or re-derived at least one headline score from its code and outputs, or stated why not',
  'weighed every flag listed above',
  'for each builder, spot-checked one of its devil\'s advocates\' re-runs (a verdict or its null-control rerun) against its files, or stated why not',
  'goal_coverage states for each element of the goal what the evidence so far does and does not support',
  'if you plan round 2: decided whether evaluation changes are needed, and if so wrote the spec so that numbers of both harness versions stay comparable',
].map(x => '- ' + x).join('\n')
const plan2 = normPlan(await agent(leadPlanPrompt(2, '## This workflow so far\n' + hist1 + '\n\nRound 2 may be empty (tasks = []) if the goal is answered as far as the data allows. Round-2 briefs must not contain any score from a slice meant as held-out.', coverage2), { label: 'research-lead-review', phase: 'Lead review', schema: LEAD_SCHEMA, model: O }))
let r2 = null
if (plan2 && (plan2.tasks || []).length) {
  log(`Round 2: ${plan2.tasks.length} task(s); builder cap ${R2_BUILDER_MAX} min`)
  phase('Round 2')
  r2 = await runRound(2, plan2, r1)
} else {
  log('No round 2 (lead returned no tasks or failed).')
}

phase('Final')
const hist2 = `${hist1}\n\n## Research lead plan (round 2)\n${plan2 ? JSON.stringify({ assessment: plan2.assessment, goal_coverage: plan2.goal_coverage, evaluation_changes: plan2.evaluation_changes, shared_prep: plan2.shared_prep, tasks: plan2.tasks }, null, 1) : '(failed)'}\n\n${r2 ? `## Engineer round 2\n${r2.eng ? 'report file: ' + docOf('engineer-r2') : '(none)'}\n\n## Shared prep round 2\n${r2.prep ? 'report file: ' + docOf('prep-r2') + ' (inputs in ' + sharedOf(2) + '/)' : '(none)'}\n\n## Round 2 builders\n${r2.builders}\n\n## Round 2 devil's advocates\n${r2.das}` : '(no round 2)'}`
const final = await agent(`You are the RESEARCH LEAD writing the final report of this workflow for the user (a non-specialist).
${CONTEXT}
${sched('lead-final')}
## This workflow
${hist2}
Coverage list (read every builder and devil's advocate report file of both rounds before writing; weigh every flag above):
- read every builder report file and every devil's advocate report file of both rounds (list them)
- re-derived several headline scores from code and outputs (list them), and spot-checked at least one devil's advocate re-run
- weighed each flag listed above and say how
- state in the report which files you read and which headline scores you re-derived.
Write ${PROJ}/RESULTS-W5.md in plain English, concise: what the inventories found (how many assumptions and chosen numbers, how many had a variation or test found and how many had none); the answer, with evidence and caveats, to each element of the goal (whether tuning the assumptions and numbers helps, with honest accounting of selection; whether the set of folds is arbitrary, and what that does to the conclusions); the best results with the devil's advocates' findings alongside them and the harness version every number comes from (note any flags above); the state of the held-out slices; what the evidence does and does not support; process problems (timing, caps, reproducibility). Put anything you would recommend doing next ONLY in a final section titled "Next steps (kept separate)". Return the full text.`, { label: 'research-lead-final', phase: 'Final', model: O })

return { invText, plan1, round1: r1, plan2, round2: r2, final }
