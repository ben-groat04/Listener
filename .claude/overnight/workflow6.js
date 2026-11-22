// Workflow 6: assemble a model or groundwork capable of answering "what new songs should I listen to?", fix the final evaluation, and prepare (not run) the single-use sealed test.
// MAIN-SESSION NOTES (not for agents):
// - Never message/stop/restart a running workflow. The user's latest message is auto-forwarded to every agent, so launch only right after a neutral message ("go").
// - Pre-launch Sonnet audit must check every item in .claude/workflow-notes.md, every paraphrase against its verbatim source, and the GATES list below. Show the audited brief to the user before launch.
// - Tell the user about the 3 Opus agents (plan, review, final lead) before launch (CLAUDE.md); the Workflow tool also asks approval for them.
// - Manual launch check (scripts cannot test files): taste-model/reports/w5-sanitised/ exists with README.md, RESULTS.md, lead-r1/lead-r2/lead-final.md, builder-*, devils-advocate-*, engineer-*, inventory-*, prep-r1.md (it does as of drafting).
// - Recreate the ~5 min status cron + Monitor on journal.jsonl. Not in this workflow: sealed prep/run (main session only, after the user approves), candidate-song search, committing.
//
// GATES (all flag-only: nothing retries or blocks an agent; flags go to the leads, who judge):
//  G1 soft wall-clock caps (builders, devil's advocates, leads, package auditor): every agent is told its cap; the script only logs a FLAG if self-reported duration > 1.25 x cap. Never a floor, never a retry, never a failure for finishing early.
//  G2 builder checklist: every id needs status + evidence; null-control line and declaration ids must be filled. Falsely claiming 'done' is caught by the devil's advocate re-check, not by the script.
//  G3 devil's advocate coverage: one verdict per numbered claim, every checklist id re-checked, evalkit + predictor code listed, null control re-run, declaration time vs first scored run checked. No duration check of any kind. A claim that neither of the pair re-ran is flagged.
//  G4 conditional steps (each can be satisfied by the lead's own output): engineer addendum iff the plan's evaluation_changes is non-empty (round 1 only; the harness is frozen before any builder starts and stays frozen for round 2); shared prep iff shared_prep is non-empty (new versioned directory); round 2 iff the review lead returns tasks. 'none'/'n/a'/'no change' count as empty. Task ids are sanitised and de-duplicated.
//  G5 failed (null) agents are logged and passed on as '(failed)'; no automatic retry.
//  G6 scout self-reports (sources reachable, DONE written) are flags for the lead. The standing harness pass is the one hard stop: if engineer-r0 fails or reports selftest/default-output/declaration_hashing/plain_80_rule not satisfied, the script returns an error before any Opus agent runs (no retry; the main session decides).
//  G7 held-out leak flag: builder, devil's advocate and lead structured text matching a LATE/HOLDOUT word near a decimal number is logged (and shown to the leads); it blocks nothing.
export const meta = {
  name: 'taste-workflow-6',
  description: 'Workflow 6: harness pass + catalogue scout, Opus research lead plans, optional engineer addendum + shared prep, builders with two devil\'s advocates each, lead review, optional round 2, final report with a sealed-test package (not run), package check',
  phases: [
    { title: 'Foundations', detail: 'harness engineer + catalogue scout in parallel (Sonnet)', model: 'sonnet' },
    { title: 'Plan', detail: 'research lead (Opus)', model: 'opus' },
    { title: 'Round 1', detail: 'optional engineer addendum + shared prep, then up to 2 builders + 2 devil\'s advocates each (Sonnet)', model: 'sonnet' },
    { title: 'Lead review', detail: 'research lead (Opus)', model: 'opus' },
    { title: 'Round 2', detail: 'optional shared prep, then up to 2 builders + 2 devil\'s advocates each (Sonnet)', model: 'sonnet' },
    { title: 'Final', detail: 'research lead (Opus): report + sealed-test package', model: 'opus' },
    { title: 'Package check', detail: 'package auditor (Sonnet)', model: 'sonnet' },
  ],
}

const ROOT = '/home/user/Listener'
const PROJ = ROOT + '/taste-model'
const SCRATCH = '/tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf6'
const DOCS = SCRATCH + '/docs'          // one report file per agent: DOCS/<label>.md
const S = 'sonnet', O = 'opus'
const W3_DIR = PROJ + '/reports/w3-sanitised'
const W4_DIR = PROJ + '/reports/w4-sanitised'
const W5_DIR = PROJ + '/reports/w5-sanitised'

// Soft process caps (wall-clock minutes), one place only. Agents are told each cap; the script only logs a flag on overrun. No floors, no retries.
const ENG0_MAX = 60, SCOUT_MAX = 60, ENG1_MAX = 45, PREP_MAX = 90
const R1_BUILDER_MAX = 90, R2_BUILDER_MAX = 60
const DA_MAX = 60, LEAD_MAX = 45, FINAL_MAX = 60, AUDIT_MAX = 30
const softCap = (n) => `Soft wall-clock cap ${n} minutes from your first action (there is no minimum; finish when everything asked is covered with evidence). At about 80% of the cap stop starting new work and report what you have, labelling any gap.`
const LATE_CAP = 2
const MAX_TASKS = 2   // the Workflow tool runs at most 2 agents at once on this box

// Single source of truth for folder and path names; these win on any conflict.
const scratchOf = (label) => SCRATCH + '/' + label
const docOf = (label) => DOCS + '/' + label + '.md'
const predOf = (round, id) => PROJ + '/predictors/w6r' + round + '-' + id
const sharedOf = (round) => PROJ + '/.cache/shared-w6r' + round   // round 0 = the catalogue scout's directory
const CAT_CODE = PROJ + '/catalogue'
const PKG = PROJ + '/prereg-w6'
const FROZEN_SHARED = [PROJ + '/.cache/shared', PROJ + '/.cache/shared-w5r1']   // Workflow 4 and 5 shared inputs: read-only for everyone

// Lead-output normalisation: empty-ish text fields count as empty; task ids are sanitised and de-duplicated.
const EMPTYISH = /^\s*(none|n\/?a|no changes?)\.?\s*$/i
const cleanText = (x) => (typeof x !== 'string' || !x.trim() || EMPTYISH.test(x)) ? '' : x
const normPlan = (plan) => {
  if (!plan) return plan
  plan.evaluation_design = cleanText(plan.evaluation_design)
  plan.evaluation_changes = cleanText(plan.evaluation_changes)
  plan.shared_prep = cleanText(plan.shared_prep)
  plan.prep_after_engineer = plan.prep_after_engineer === true
  const seen = new Set()
  plan.tasks = (Array.isArray(plan.tasks) ? plan.tasks : []).filter(t => t && typeof t.brief === 'string' && t.brief.trim()).slice(0, MAX_TASKS).map(t => {
    let id = String(t.id || '').toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, '') || 'task'
    const base = id
    for (let k = 2; seen.has(id); k++) id = base + '-' + k
    if (id !== t.id) log(`task id "${t.id}" renamed to "${id}"`)
    seen.add(id)
    const could_change = cleanText(t.could_change)
    if (!could_change) log(`FLAG: task ${id} states no decision or conclusion it could change`)
    return { ...t, id, could_change: could_change || '(the lead stated none)' }
  })
  return plan
}
const sharedBlock = (shared) => (shared.length ? shared.map(x => `- ${x.dir}/ (round ${x.round}; README/MANIFEST.txt inside) built by the agent whose report is ${x.doc}`).join('\n') : '(none)') +
  `\nUse a shared directory only if its DONE file exists; if DONE is missing treat the directory as unusable and say so in your report. Read-only older inputs: ${FROZEN_SHARED.join(', ')}.`

const CONTEXT = `
## Goal of this workflow
- "Next workflow simply needs to assemble a model or groundwork capable of answering the question: what new songs should I listen to?"
- This workflow fixes the final model(s) and the final evaluation design. They are then tested once on sealed data; that run is done later by the main session after the owner approves, never by you.
- Decision rule (the owner's risk preference): a difference counts as decided when the lower end of its 80% interval is above zero. There is no extra margin. 95% intervals are informational. On the decision rule: "I want the best set of recommendations possible, that's it."

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
- After Workflow 2: "Ah ok. Is the score calculation good? In the next workflow a lot of things you've been treating as fixed need to be re-investigated. Because with the current scoring system let's be honest with the subjectivity you won't be going super super high"
- "Ok after W5 I think w6 needs to be looking through everything to make the best test. Then testing it on sealed"
- "Best test was supposed to be final yes"
- On the sealed run: "Yes the sealed run is the data backed way of testing the output before it suggesting to me. When I get new suggestions I expect the project to transition into me giving more detailed feedback and conversing about how this should feed into improvements"

## Unvetted ideas raised in discussion
These came up in chat. They are not from an expert, they may well not be the best way to work, and they carry no more weight than any other hypothesis. Test them on the evidence like anything else, and drop them if the data says so.
- Questions might be settled by reasoning and logic where that is possible, instead of being left labelled as unresolved.
- It might be better for this workflow to be faster than earlier ones; whether and how testing and procedures could be sped up is open.
- How people listen to and discover music may be worth thinking about.
- The data is very noisy, so it may be necessary to act more on loose trends and correlation; expecting a clear result may be foolish.
- One view is that the project may have settled into habits.
- Listening frequency and statistics may be the most reliable indicator of taste at any given time.
- Many liked songs may be liked for specific parts of the music.
- The "loved" definition may be arbitrary but probably does a good job; like everything of this kind, it can be varied if performance plateaus.
- Taste changed a lot early on, so the oldest music may be of limited use; analysis will tell.
- There may be doubt that one score summarising everything captures everything.

## Facts
- Data came from the user's stats.fm profile. Full listening history 2020-2026: ${ROOT}/spotify-liked-songs/.cache/streams.jsonl (147,256 JSON lines). The only other file you may read from ${ROOT}/spotify-liked-songs/ and its .cache/ is whatever the evalkit loader and README name as their inputs (top_tracks.json only through evalkit.data.load_meta).
- Evaluation harness: ${PROJ}/evalkit/ (read its README; v5.1 at the start of this workflow). Everything about it is open to change by the harness engineer steps only.
- Earlier work: ${PROJ}/predictors/ and ${PROJ}/.cache/. Shared inputs of earlier workflows: ${FROZEN_SHARED.join(' and ')} (read-only).
- The ONLY earlier-workflow documents you may read are the sanitised copies: ${W5_DIR}/ (start with its README.md, which lists what was removed, then RESULTS.md; one file per agent report), ${W4_DIR}/ and ${W3_DIR}/ (start with RESULTS.md in each).
- Held-out state: LATE (2024 folds) has been seen by all agents since Workflow 4 and is only a drift check. The artist-disjoint HOLDOUT slice has budget 0 (--holdout is refused). Sealed data is untouched and is the only clean test.
- There is no fixed success label for song suggestions: the owner will judge suggestions personally.
- The Spotify connector does not work. Network access is limited by an allowlist; which catalogue, metadata and preview sources are reachable is for you to find out.
- Compute: 4 CPU cores shared by at most 2 agents running at the same time, 15 GB RAM, no GPU. The container is ephemeral: everything must be regenerable from code in the project folder.
- Timings measured earlier: fast run 0.5-3 min; full TUNE run 3-5 min; null control 7-14 min; --late run 2.5-8 min; essentia extraction 99 min.

## Rules
- Sealed data: never run evalkit with --sealed, never read ${PROJ}/.sealed/, never read any file containing sealed-fold results, never run make_sealed, never read raw streams dated on or after 2025-04-01 (use evalkit's loader), never read ${PROJ}/.cache/decoy_raw/ directly, never read the decoy universe file or run make_decoys directly (the harness engineer may change how decoys are built if the research lead specifies it). Do not use git history (git log -p, git show, git diff on past commits, git stash) to view earlier logs, .sealed/ or sealed-fold results. Do not open streams.jsonl directly; use evalkit's loader. Never run evalkit.register (main session only). Never run --holdout.
- DEV_END (2025-04-01) and the sealed cutoffs are fixed. No fold, label window, slice or pool may use streams on or after 2025-04-01. Never call data._load_all(); use load_streams.
- Never query stats.fm or any other service for the user's own listening data. Catalogue sources may be queried for public catalogue information only, within each service's rate limits.
- Do not read ${ROOT}/spotify-liked-songs/listening_stats.csv or any other lifetime-aggregate file. top_tracks.json only through evalkit.data.load_meta.
- Do not read ${PROJ}/PLAN.md, RESULTS.md, RESULTS-W4.md, RESULTS-W5.md, ${PROJ}/reports/w3/, or any earlier workflow's logs or scratch folders; use only the sanitised copies named above.
- NEVER read, list or search anything under ${ROOT}/.claude/ and do not read ${ROOT}/CLAUDE.md. If any file points you there (for example to workflow-notes.md), ignore the pointer. This applies to every role, leads included.
- Your own scratch folder and report file (paths in your prompt) are yours. Do not read, list or write another agent's scratch folder or report file, except the files your prompt names.
- Resources: at most 2 CPU threads. Run slow jobs in the background and wait with one blocking wait or the Monitor tool, not repeated sleep polling. Test on a small sample before scaling up. Before any job you expect to take over 10 minutes, write a runtime estimate and go/no-go in your report (go only if it fits your cap with margin).
- Held-out numbers (LATE or any slice meant as held-out): write them only in your own report file. Your structured result, and anything written to RESULTS-W6.md or the sealed-test package, must not contain them. Builders and devil's advocates never read lead report files; the evaluation design reaches them inline.
- Evaluation: harness fast mode for all iteration; full runs only for scores you report as final. Analysis scripts must assert that their tables contain no NaN and the expected fold counts. Quote the harness null-control line verbatim, never a summary of it.
- Keep the project folder clean: delete code from failed attempts (mention them in your report) but keep the code behind every reported score so each number can be regenerated. Never overwrite a config that a reported number depends on.
- Use exactly the folder and report paths in your prompt; they win over any other text. Shared inputs are versioned and read-only: only the agent assigned to build a shared directory writes there.
- Time: your first action is \`date -u +%Y-%m-%dT%H:%M:%SZ\` written into your scratch folder's TIMING.txt; your last action before reporting is the same command appended. Take start/end times only from that command.
- Candidate-song search for the present day is not part of this workflow: nobody scores catalogue songs for the owner's present-day taste or writes a list of suggested songs. Catalogue work is groundwork.
- Nobody is available to answer questions; decide yourself and record the decision. Do not git commit or push.
- Write your full report to your own report file; the structured result carries a short summary and the requested fields. Report what you ran separately from what you only believe.
`

const sched = (label) => `Your own scratch folder is ${scratchOf(label)}/ (create it). Your own report file is ${docOf(label)} (write your full report there).`

// ---------- Foundations: harness engineer ----------
const ENG_IDS = ['plain_80_rule', 'comparators_in_default_runs', 'single_model_file_deltas', 'fold_weight_sensitivity', 'declaration_hashing', 'output_sanity_helpers', 'null_control_line', 'default_output_unchanged']
const ENG0_SPEC = `Standing harness pass (everything below is required in this one pass; no further harness change happens after it unless the research lead specifies one before the builders start).
- plain_80_rule: a decision column that is POS when the lower end of the 80% interval of the paired sauc difference is above zero, NEG when the upper end is below zero, else UNDECIDED, with no extra margin, in every table that has a decision column. The existing margin column may stay but must be labelled as such and must not be the one the tables lead with.
- comparators_in_default_runs: one comparator set (a single setting, defaulting to artist_recent and ref_w4r1_listening until the research lead's evaluation design says otherwise), the same in every run whatever the fold set, whose paired comparison is printed in default and --fast runs as well, not only in --folds runs.
- single_model_file_deltas: the file-level paired-difference table prints rows for a file that holds only one model (it printed nothing before).
- fold_weight_sensitivity: beside every pooled paired difference vs the comparator set, print the same difference with inverse-variance fold weights, and the same difference with the heaviest folds left out; same decision labels.
- declaration_hashing: a command (python3 -m evalkit.declare NAME FILE...) that records the sha256 of the declared files and the UTC time in a new read-only file under .cache/declarations/ and refuses to overwrite one. Every scored run prints, and appends to a read-only run log with its UTC time, whether the predictor files match a declaration (declaration name and hash, or UNDECLARED).
- output_sanity_helpers: a small helper module that analysis scripts can call to assert no NaN in a table and the expected fold count.
- null_control_line: the null control prints, per model, one single-line machine-readable summary of the gated statistic, its band and the PASS/FLAG label, to be quoted verbatim.
- default_output_unchanged: a default run without new flags reproduces v5.1 numbers; the selftest asserts it (selftest --v52) and the selftest also runs all new checks.`

const engineerPrompt = (label, spec, priorDocs) => `You are the HARNESS ENGINEER (${label}). Implement exactly the specification below plus the standing hygiene requirements, no more.
${CONTEXT}
${sched(label)}
${priorDocs ? 'Earlier engineer report(s) of this workflow (the harness state you start from): ' + priorDocs + '\n' : ''}## Specification
${spec}
## Standing hygiene requirements
- Version the harness: bump the version only if code changed and add a changelog entry to the README stating which earlier numbers remain comparable. Anything that alters existing numbers must be selectable (flag or version) so earlier numbers can be regenerated; label every printed table with the harness version.
- Fit/feature cache keys include the random seed and relabelled identities; the selftest asserts that 3 null seeds give different results.
- Keep the LATE cap (${LATE_CAP} per predictor bundle) and the HOLDOUT closure (budget file untouched, --holdout refused). Never add held-out budget. A --holdout or --late run prints only that slice's numbers.
- DEV_END and the sealed cutoffs stay fixed; harness caches go under ${PROJ}/.cache/evalkit-cache/.
- Do not change make_sealed.py, sealed_manifest.json or the sealed code path. If a change you were given would require it, stop and report that instead. ${label === 'engineer-r0' ? 'FIRST action after the date: record sha256 of evalkit/make_sealed.py, evalkit/sealed_manifest.json and evalkit/register.py in your report (the package auditor compares them at the end).' : ''}
- Run the selftest and all baselines (dev only) after your changes.
- ${softCap(label === 'engineer-r0' ? ENG0_MAX : ENG1_MAX)}
Report facts only: what you changed, how to use it, the dev baseline scores with the harness version, which earlier numbers remain comparable, job runtimes, and anything you could not do and why. Do not build shared artefacts.`

const ENG_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: 'At most 250 words' },
    harness_version: { type: 'string' },
    selftest_passed: { type: 'boolean' },
    default_output_unchanged: { type: 'boolean', description: 'true only if you ran the check against the previous version and it matched (for an addendum: matched apart from the changes you were given)' },
    items: { type: 'array', description: 'One entry per specification item id (for the standing pass: ' + ENG_IDS.join(', ') + '; for an addendum: one per item you were given, with a short id)', items: { type: 'object', properties: { id: { type: 'string' }, status: { type: 'string', enum: ['done', 'partial', 'not_done'] }, evidence: { type: 'string', description: 'command run and what it showed, or why not done' } }, required: ['id', 'status', 'evidence'] } },
  },
  required: ['summary', 'harness_version', 'selftest_passed', 'default_output_unchanged', 'items'],
}
const engFlags = (e, ids, standing) => {
  if (!e) return ['engineer failed (no result)']
  const f = []
  if (!e.selftest_passed) f.push('selftest not reported as passed')
  if (standing && !e.default_output_unchanged) f.push('default output not reported as unchanged vs previous version')
  for (const id of ids) {
    const it = (e.items || []).find(x => x.id === id)
    if (!it) f.push('item missing: ' + id)
    else if (it.status !== 'done') f.push(`item ${id} is ${it.status}: ${it.evidence}`)
  }
  return f
}
const flagLine = (f) => f.length ? 'FLAGS: ' + f.join('; ') : 'flags: none'

// ---------- Foundations: catalogue scout ----------
const SCOUT_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: 'At most 300 words: what is reachable, what is not, what the tools and sample cover' },
    sources: { type: 'array', description: 'One entry per source you tried, reachable or not', items: { type: 'object', properties: { name: { type: 'string' }, reachable: { type: 'boolean' }, offers: { type: 'string', description: 'what can be listed or looked up, per-song fields, audio previews' }, limits: { type: 'string', description: 'rate, volume, coverage, terms you found' }, evidence: { type: 'string', description: 'the request or command and what came back' } }, required: ['name', 'reachable', 'offers', 'limits', 'evidence'] } },
    done_written: { type: 'boolean', description: 'true only if MANIFEST.txt and then the empty DONE file exist in the shared directory' },
  },
  required: ['summary', 'sources', 'done_written'],
}
const scoutPrompt = () => `You are the CATALOGUE SCOUT. Find out which catalogue, metadata and audio-preview sources are reachable from this container, and make them usable by later agents.
${CONTEXT}
${sched('catalogue-scout')}
Task: for every source you try, record whether it is reachable, what it offers (which songs can be listed or looked up, which per-song fields, whether audio previews exist), its limits (rate, volume, coverage, terms) and the evidence. Existing project code and caches may be read for ideas (the harness already fetched some catalogue data), but the existing caches stay untouched. Write small reproducible tools in ${CAT_CODE}/ and a small data sample in ${sharedOf(0)}/ (create it) so later agents can use whatever is reachable, and document usage in ${sharedOf(0)}/README.md. Finish by writing ${sharedOf(0)}/MANIFEST.txt (files, formats, counts, sha256 of non-bulk files) and then an empty file ${sharedOf(0)}/DONE; nothing in that directory changes afterwards. ${softCap(SCOUT_MAX)} If something cannot finish, leave a complete subset and state what is missing. This is groundwork only: do not score songs for the owner and do not write recommendations.`

// ---------- Lead ----------
const TASK_ITEM = { type: 'object', properties: { id: { type: 'string', pattern: '^[a-z0-9-]+$', description: 'short slug, unique among your tasks' }, brief: { type: 'string', description: 'self-contained brief for one independent builder; do not name folders or paths (the workflow assigns them)' }, could_change: { type: 'string', description: 'the decision or earlier conclusion this task could change, and which result would change it' } }, required: ['id', 'brief', 'could_change'] }
const CHECKLIST_ITEM = { type: 'object', properties: { item: { type: 'string' }, status: { type: 'string', enum: ['done', 'impossible', 'not_done'] }, evidence: { type: 'string' } }, required: ['item', 'status', 'evidence'] }
const PLAN_SCHEMA = {
  type: 'object',
  properties: {
    assessment: { type: 'string', description: 'Where the project stands with respect to the goal' },
    goal_coverage: { type: 'string', description: 'For each element of the goal, which task or step addresses it and how its answer will be judged, or why it is not addressed' },
    evaluation_design: { type: 'string', description: 'The final evaluation design, fixed now before any builder runs: what is scored, against which comparators and baselines, how decisions are made, which secondary checks apply, how held-out evidence is obtained or not, and what the sealed test will need. It is passed inline to every builder and devil\'s advocate, who follow it, so it must contain no held-out number.' },
    evaluation_changes: { type: 'string', description: 'Further harness changes beyond the standing pass (engineer addendum, before the builders start), or empty string if none' },
    shared_prep: { type: 'string', description: 'Precise spec of every shared artefact that more than one builder, or any builder at scale, needs, to be built once in a new versioned directory, or empty string if none' },
    prep_after_engineer: { type: 'boolean', description: 'true if shared prep needs the addendum harness; false to run them in parallel' },
    tasks: { type: 'array', maxItems: MAX_TASKS, items: TASK_ITEM },
    checklist: { type: 'array', description: 'One entry per coverage item', items: CHECKLIST_ITEM },
    start_utc: { type: 'string' }, end_utc: { type: 'string' },
  },
  required: ['assessment', 'goal_coverage', 'evaluation_design', 'evaluation_changes', 'shared_prep', 'prep_after_engineer', 'tasks', 'checklist', 'start_utc', 'end_utc'],
}
const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    assessment: PLAN_SCHEMA.properties.assessment,
    goal_coverage: PLAN_SCHEMA.properties.goal_coverage,
    evaluation_design: { type: 'string', description: 'Additions to the evaluation design for round 2 (the plan\'s design stays in force and the harness is frozen), or empty string. Passed inline to round-2 builders and devil\'s advocates; no held-out number.' },
    shared_prep: PLAN_SCHEMA.properties.shared_prep,
    tasks: { type: 'array', maxItems: MAX_TASKS, items: TASK_ITEM, description: 'Round-2 tasks, or an empty list if the goal is answered as far as the data allows. could_change must name the specific round-1 conclusion (report file and claim) the task could overturn; do not repeat a round-1 design on another target unless you say why its answer could differ.' },
    checklist: PLAN_SCHEMA.properties.checklist,
    start_utc: { type: 'string' }, end_utc: { type: 'string' },
  },
  required: ['assessment', 'goal_coverage', 'evaluation_design', 'shared_prep', 'tasks', 'checklist', 'start_utc', 'end_utc'],
}

const leadRules = (round) => `Process facts: after you, ${round === 1 ? 'an optional engineer addendum and an optional shared-prep step (at the same time, or prep after the addendum if you set prep_after_engineer; soft prep cap ' + PREP_MAX + ' min), then' : 'an optional shared-prep step (soft cap ' + PREP_MAX + ' min), then'} up to ${MAX_TASKS} independent builders (soft wall-clock cap ${round === 1 ? R1_BUILDER_MAX : R2_BUILDER_MAX} min each, mandatory checklist, no time floor), each followed by two devil's advocates (soft cap ${DA_MAX} min each). At most 2 agents run at once. Builders cannot create shared inputs, so anything heavy they need must be in shared_prep. The harness caps --late at ${LATE_CAP} runs per predictor bundle; the HOLDOUT budget is 0. Folder and report names are assigned by the workflow; do not name them in briefs. Builders and devil's advocates do not read your report file: your evaluation_design field and the task briefs reach them inline, so neither may contain a held-out number. Write briefs in your own words; do not paste reviewer, builder or devil's-advocate text. Every builder must: use fast mode for iteration; declare its final predictor(s) with the harness declaration command before the first full scored run; run the null control; give paired comparisons against the comparators and baselines your evaluation design names; count every variant; investigate below-chance results; state the strongest case against its result. Whether held-out (LATE) evidence is looked at is your decision. Soft caps: ${round === 1 ? 'the plan lead' : 'the review lead'} ${LEAD_MAX} min, final lead ${FINAL_MAX} min, package auditor ${AUDIT_MAX} min (flag-only, no minimum). Script flags are facts for you to weigh, not verdicts.`

const leadPlanPrompt = (foundations, coverage) => `You are the RESEARCH LEAD. You own the experiment design and the direction of this workflow. You do not build predictors yourself.
${CONTEXT}
${sched('research-lead-plan')}
${foundations}
${leadRules(1)}
${softCap(LEAD_MAX)} Report start_utc and end_utc from the date command.
Decide, with reasons: (1) how the goal is to be addressed with what is known from all earlier workflows (read the sanitised reports; verify the claims you rely on), including which model(s) could be final; (2) the final evaluation design, which you fix now, before any builder runs; (3) whether the harness needs changes beyond the standing pass, and any shared artefacts; (4) up to ${MAX_TASKS} independent builder tasks, each stating the decision or conclusion it could change.
Coverage list (fill the checklist, one entry per line, with evidence; flags are facts from the script, not verdicts):
${coverage}`

// ---------- Prep ----------
const prepPrompt = (round, plan) => `You are the SHARED-PREP agent (round ${round}). Build exactly the shared artefacts specified below, once, in a NEW directory, so that every builder starts from identical inputs.
${CONTEXT}
${sched('prep-r' + round)}
## Artefacts to build in ${sharedOf(round)}/ (research lead)
${plan.shared_prep}
Process: create ${sharedOf(round)}/ yourself; never modify any other shared directory (read freely). Estimate runtime and decide go/no-go before long jobs; ${softCap(PREP_MAX)} If something cannot finish, build the complete subset and state exactly what is missing. Finish by writing ${sharedOf(round)}/MANIFEST.txt (every file, format, counts, coverage, sha256 of non-bulk files) and then an empty ${sharedOf(round)}/DONE; nothing changes afterwards. Nothing outside the spec is added. ${round === 1 && plan.evaluation_changes ? 'An engineer addendum changes evalkit at the same time or before you; do not touch evalkit.' : 'Do not touch evalkit.'}
Report facts only: where each artefact is (location and format), coverage, runtimes, anything you could not do and why.`

// ---------- Builders ----------
const CHECK_IDS = ['fast_mode_for_iteration', 'full_run_final_scores', 'held_out_state_respected', 'null_control_line_verbatim', 'paired_comparisons_per_evaluation_design', 'below_chance_investigated', 'variants_counted_and_selection_accounted', 'strongest_case_against', 'declaration_before_first_scored_run', 'output_sanity_asserted', 'runtimes_estimated_and_actual', 'code_behind_every_reported_score_kept', 'ran_vs_believed_separated']
const BUILDER_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: 'At most 400 words: what you did and found, key dev numbers with the harness version; no held-out numbers' },
    start_utc: { type: 'string' }, end_utc: { type: 'string' },
    null_control_line: { type: 'string', description: 'The harness null-control line for your final predictor(s), copied verbatim (or why impossible)' },
    declared: { type: 'array', items: { type: 'string' }, description: 'Names (as recorded by the harness declaration command) of every declaration you made, in order' },
    late_runs_used: { type: 'integer' },
    headline_claims: { type: 'array', items: { type: 'string' }, description: 'Every headline claim, one checkable sentence each with its number; no held-out numbers' },
    checklist: { type: 'array', description: 'One entry for EACH id: ' + CHECK_IDS.join(', '), items: { type: 'object', properties: { id: { type: 'string', enum: CHECK_IDS }, status: { type: 'string', enum: ['done', 'impossible', 'not_done'] }, evidence: { type: 'string' } }, required: ['id', 'status', 'evidence'] } },
  },
  required: ['summary', 'start_utc', 'end_utc', 'null_control_line', 'declared', 'late_runs_used', 'headline_claims', 'checklist'],
}
const contextFiles = (c) => `## Evaluation design (fixed by the research lead; follow it)
${c.design || '(the lead returned no evaluation design: follow your brief and state which comparators and decision rule you used)'}
Reports and inputs you may read in addition to the sanitised reports:
- Harness engineer report(s), in order: ${c.engDocs.join(', ') || '(none)'}. The harness is frozen; its version is in the last report.
- Shared inputs:
${sharedBlock(c.shared)}`

const builderPrompt = (round, task, c, label) => `You are a BUILDER (round ${round}, task "${task.id}"). Other builders work independently; do not read or edit their folders, scratch or report files.
${CONTEXT}
${sched(label)}
Your predictor code folder is ${predOf(round, task.id)}/ (entry file the harness accepts). Use only these folders.
${contextFiles(c)}
## Your task (from the research lead)
${task.brief}
Decision or conclusion this task could change: ${task.could_change}
Time: ${softCap(round === 1 ? R1_BUILDER_MAX : R2_BUILDER_MAX)} Use --late (if your brief calls for it) at most ${LATE_CAP} times, on the declared final predictor only.
Mandatory before you report (one checklist entry per id, with evidence; a gap is flagged to the leads, so say plainly if something is impossible):
- fast_mode_for_iteration; full_run_final_scores
- held_out_state_respected: no --holdout; --late only if your brief calls for it and within the cap; held-out numbers only in your report file
- null_control_line_verbatim: the harness null-control line for your final predictor(s), copied verbatim into null_control_line and your report
- paired_comparisons_per_evaluation_design: paired differences vs the comparators and baselines named in the evaluation design above, with the decision labels the harness prints
- below_chance_investigated; variants_counted_and_selection_accounted; strongest_case_against
- declaration_before_first_scored_run: your final predictor file(s) declared with the harness declaration command BEFORE the first full scored run of them; list the declaration names; do not edit a declared file afterwards (declare again and report both if you must)
- output_sanity_asserted: every analysis script asserts no NaN and the expected fold counts
- runtimes_estimated_and_actual; code_behind_every_reported_score_kept; ran_vs_believed_separated
List every headline claim in headline_claims; the devil's advocates verify each one.`

// ---------- Devil's advocates ----------
const DA_DIRECTIONS = [
  { id: 'works', text: 'Attack every claim that something IMPROVES results or works: gains not real, selection among many variants, leakage, shortcuts, overfitting to the iteration folds, simple signals doing the work, noise, evaluation flaws that flatter results.' },
  { id: 'dismissed', text: 'Attack every claim that something makes NO difference, was checked and is fine, does not work, or was left fixed or untried: too little effort, bugs, unfair evaluation, results dropped or ignored without investigation, assumptions treated as fixed.' },
]
const DA_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: 'At most 300 words including the overall verdict; no held-out numbers' },
    claim_verdicts: { type: 'array', description: 'EXACTLY one entry per numbered builder claim (claim_no), plus any extra claims you assessed', items: { type: 'object', properties: { claim_no: { type: 'integer' }, verdict: { type: 'string', enum: ['holds', 'does_not_hold', 'unverified'] }, what_i_ran: { type: 'string' }, result: { type: 'string' } }, required: ['claim_no', 'verdict', 'what_i_ran', 'result'] } },
    not_rerun_claims: { type: 'array', items: { type: 'integer' }, description: 'claim_no of every claim you judged from reading code or files without re-running it' },
    checklist_rechecked: { type: 'array', items: { type: 'string', enum: CHECK_IDS } },
    code_files_read: { type: 'array', items: { type: 'string' }, description: 'Builder and evalkit code files you actually read' },
    null_control_rerun: { type: 'string', description: 'The null-control check as YOU re-ran it: command and the verbatim harness line' },
    start_utc: { type: 'string' }, end_utc: { type: 'string' },
    declaration_check: { type: 'string', description: 'For each declaration the builder lists: declared hash vs the files now, and declaration time vs the first scored run in the harness run log' },
    shared_inputs_unchanged: { type: 'string', description: 'Each shared directory the builder used checked against its MANIFEST.txt, or why there are none' },
  },
  required: ['summary', 'claim_verdicts', 'not_rerun_claims', 'checklist_rechecked', 'code_files_read', 'null_control_rerun', 'declaration_check', 'shared_inputs_unchanged', 'start_utc', 'end_utc'],
}
const daPrompt = (round, dir, task, b, bLabel, c, label) => `You are a DEVIL'S ADVOCATE (round ${round}, direction: ${dir.id}) for the builder of task "${task.id}". Another devil's advocate covers the opposite direction for the same builder.
${CONTEXT}
${sched(label)}
${dir.text}
Judged on coverage, not duration. ${softCap(DA_MAX)} Finish when every item is covered with evidence:
- one verdict per numbered builder claim below, from code and output files, not from the report's wording; list in not_rerun_claims every claim you did not re-run (the other devil's advocate also assesses all claims);
- read the builder's code in ${predOf(round, task.id)}/ and the evaluation code in ${PROJ}/evalkit/ (list the files), and check the harness engineer's changes against their specification;
- re-check every builder checklist item below against code and files, including durations against its TIMING.txt in ${scratchOf(bLabel)}/ (read-only for you);
- re-run the null control yourself and give the command and the verbatim harness line; compare the builder's null_control_line with it;
- check each declaration against the files now and against the first scored run in the harness run log;
- re-run every headline score on the iteration slice that you assess. Do NOT run --late or --holdout; verify those claims from the harness's read-only tables and logs;
- check each shared directory used (with a DONE file) against its MANIFEST.txt.
Write your full report, led by a per-claim table, to your report file. Report start_utc and end_utc taken from the date command.
${contextFiles(c)}
- Builder report: ${docOf(bLabel)}
## Builder's numbered headline claims
${(b.headline_claims || []).map((x, i) => `${i + 1}. ${x}`).join('\n') || '(none listed)'}
## Builder's checklist entries
${(b.checklist || []).map(x => `- ${x.id}: ${x.status}: ${x.evidence}`).join('\n')}
## Builder's null-control line
${b.null_control_line}
## Builder's declarations
${(b.declared || []).join(', ') || '(none listed)'}`

// ---------- Flags ----------
const minutes = (o) => { const a = Date.parse(o && o.start_utc), b = Date.parse(o && o.end_utc); return (isFinite(a) && isFinite(b)) ? (b - a) / 60000 : null }
const minStr = (o) => { const m = minutes(o); return m === null ? 'unparseable timestamps' : m.toFixed(1) + ' min' }
const LEAK_RE = /(late|hold-?out)[^.\n]{0,40}\d*\.\d+|\d*\.\d+[^.\n]{0,40}(late|hold-?out)/i
const leakFlag = (o, what) => LEAK_RE.test(JSON.stringify(o || {}).replace(/\\n/g, ' ')) ? [`possible held-out number in the ${what} structured text (check, do not assume)`] : []
const capFlag = (o, cap) => { const m = minutes(o); return (m !== null && m > cap * 1.25) ? [`self-reported duration ${m.toFixed(1)} min exceeded the ${cap} min soft cap`] : [] }
const builderFlags = (b, cap) => {
  if (!b) return ['builder failed (no result)']
  const f = []
  const m = minutes(b)
  if (m === null) f.push(`start_utc/end_utc unparseable (${b.start_utc} / ${b.end_utc})`)
  else if (m < 0) f.push('end_utc is before start_utc')
  else if (m > cap * 1.25) f.push(`self-reported duration ${m.toFixed(1)} min exceeded the ${cap} min cap`)
  for (const id of CHECK_IDS) {
    const c = (b.checklist || []).find(x => x.id === id)
    if (!c) f.push('checklist id missing: ' + id)
    else if (c.status !== 'done' && (!c.evidence || c.evidence.length < 20)) f.push(`checklist ${id} is ${c.status} without a real explanation`)
    else if (c.status !== 'done') f.push(`checklist ${id} is ${c.status}: ${c.evidence}`)
  }
  if (!b.null_control_line || b.null_control_line.length < 10) f.push('no null-control line')
  if (!b.declared || !b.declared.length) f.push('no declaration listed')
  if (!b.headline_claims || !b.headline_claims.length) f.push('no headline claims listed')
  return f.concat(leakFlag(b, 'builder'))
}
const daFlags = (d, b) => {
  if (!d) return ["devil's advocate failed (no result)"]
  const f = []
  const n = (b && b.headline_claims || []).length
  const covered = new Set((d.claim_verdicts || []).map(v => v.claim_no))
  for (let i = 1; i <= n; i++) if (!covered.has(i)) f.push('no verdict for builder claim ' + i)
  const unv = (d.claim_verdicts || []).filter(v => v.verdict === 'unverified').map(v => v.claim_no)
  if (unv.length) f.push(`${unv.length} claim(s) left unverified: ${unv.join(', ')}`)
  const re = new Set(d.checklist_rechecked || [])
  const miss = CHECK_IDS.filter(id => !re.has(id))
  if (miss.length) f.push('checklist items not re-checked: ' + miss.join(', '))
  if (!(d.code_files_read || []).some(x => /evalkit/.test(x))) f.push('no evalkit code file listed as read')
  if (!(d.code_files_read || []).some(x => /predictors/.test(x))) f.push('no builder code file listed as read')
  if (!d.null_control_rerun || d.null_control_rerun.length < 10) f.push('null control not re-run')
  if (!d.declaration_check || d.declaration_check.length < 10) f.push('declaration check missing')
  return f.concat(capFlag(d, DA_MAX), leakFlag(d, "devil's advocate"))
}
// claims that neither devil's advocate of a pair re-ran
const pairFlags = (das) => {
  const ok = das.filter(Boolean)
  if (ok.length < 2) return []
  const [a, c] = ok.map(d => new Set(d.not_rerun_claims || []))
  const both = [...a].filter(x => c.has(x))
  return both.length ? [`claim(s) ${both.join(', ')} were not re-run by either devil's advocate`] : []
}

const fmtBuilder = (b, label, cap) => b ? `### Builder ${label}\nreport file: ${docOf(label)}\nself-reported duration ${minStr(b)} (cap ${cap}); late runs used: ${b.late_runs_used}; declarations: ${(b.declared || []).join(', ')}\n${flagLine(builderFlags(b, cap))}\nNull-control line: ${b.null_control_line}\nSummary: ${b.summary}` : `### Builder ${label}\n(failed)`
const fmtDA = (d, label, b) => d ? `### Devil's advocate ${label}\nreport file: ${docOf(label)}\n${flagLine(daFlags(d, b))}\nverdicts: ${(d.claim_verdicts || []).map(v => `${v.claim_no}:${v.verdict}`).join(' ')}\nnot re-run: ${(d.not_rerun_claims || []).join(',') || 'none'}\nshared inputs: ${d.shared_inputs_unchanged}\nSummary: ${d.summary}` : `### Devil's advocate ${label}\n(failed)`

const runRound = async (round, plan, prev) => {
  const ph = round === 1 ? 'Round 1' : 'Round 2'
  const engLabel = 'engineer-r1', prepLabel = 'prep-r' + round
  const doEng = round === 1 && !!plan.evaluation_changes
  const doPrep = !!plan.shared_prep
  const runEng = () => doEng ? agent(engineerPrompt(engLabel, plan.evaluation_changes, prev.engDocs.join(', ')), { label: engLabel, phase: ph, model: S, schema: ENG_SCHEMA }) : Promise.resolve(null)
  const runPrep = () => doPrep ? agent(prepPrompt(round, plan), { label: prepLabel, phase: ph, model: S }) : Promise.resolve(null)
  let eng, prep
  if (plan.prep_after_engineer && doEng && doPrep) { eng = await runEng(); prep = await runPrep() }
  else { [eng, prep] = await parallel([runEng, runPrep]) }
  if (doEng && !eng) log('WARNING: engineer-r1 failed; builders are told its report is (failed)')
  if (doEng && eng) { const f = engFlags(eng, (eng.items || []).map(x => x.id), false); if (f.length) log('engineer-r1 flags: ' + f.join('; ')) }
  if (doPrep && !prep) log(`WARNING: ${prepLabel} failed; builders may use its directory only if DONE exists`)
  const engDocs = prev.engDocs.slice()
  if (doEng) engDocs.push(eng ? docOf(engLabel) : docOf(engLabel) + ' (FAILED)')
  const shared = prev.shared.slice()
  if (doPrep) shared.push({ round, dir: sharedOf(round), doc: prep ? docOf(prepLabel) : docOf(prepLabel) + ' (FAILED)' })
  const design = round === 1 ? plan.evaluation_design : (prev.design + (plan.evaluation_design ? '\n\nAdditions for round 2 (the design above stays in force):\n' + plan.evaluation_design : ''))
  const c = { design, engDocs, shared }
  const tasks = plan.tasks || []
  if (!tasks.length) return { eng, prep, c, builders: '(no builder tasks)', das: '(none)' }
  const cap = round === 1 ? R1_BUILDER_MAX : R2_BUILDER_MAX
  const out = await pipeline(
    tasks,
    (t) => agent(builderPrompt(round, t, c, 'builder-r' + round + '-' + t.id), { label: 'builder-r' + round + '-' + t.id, phase: ph, model: S, schema: BUILDER_SCHEMA }),
    async (b, t) => {
      const bLabel = 'builder-r' + round + '-' + t.id
      if (!b) { log(`WARNING: ${bLabel} failed; no devil's advocates for it`); return { b: null, das: [] } }
      const bf = builderFlags(b, cap)
      if (bf.length) log(`builder ${bLabel} flags: ${bf.join('; ')}`)
      const das = await parallel(DA_DIRECTIONS.map(d => () => agent(daPrompt(round, d, t, b, bLabel, c, 'devils-advocate-r' + round + '-' + t.id + '-' + d.id), { label: 'devils-advocate-r' + round + '-' + t.id + '-' + d.id, phase: ph, model: S, schema: DA_SCHEMA })))
      das.forEach((d, j) => { const f = daFlags(d, b); if (f.length) log(`devil's advocate r${round}-${t.id}-${DA_DIRECTIONS[j].id} flags: ${f.join('; ')}`) })
      const pf = pairFlags(das); if (pf.length) log(`pair r${round}-${t.id}: ${pf.join('; ')}`)
      return { b, das }
    },
  )
  const builders = tasks.map((t, i) => `Task ${t.id}\nBrief: ${t.brief}\nCould change: ${t.could_change}\n${fmtBuilder(out[i] && out[i].b, 'builder-r' + round + '-' + t.id, cap)}`).join('\n\n')
  const das = tasks.map((t, i) => DA_DIRECTIONS.map((d, j) => fmtDA(out[i] && out[i].das[j], 'devils-advocate-r' + round + '-' + t.id + '-' + d.id, out[i] && out[i].b)).join('\n\n') + ((out[i] && out[i].das && pairFlags(out[i].das).length) ? '\nPAIR FLAGS: ' + pairFlags(out[i].das).join('; ') : '')).join('\n\n')
  return { eng, prep, c, builders, das }
}

// ===================== run =====================
phase('Foundations')
const [eng0, scout] = await parallel([
  () => agent(engineerPrompt('engineer-r0', ENG0_SPEC, ''), { label: 'engineer-r0', phase: 'Foundations', model: S, schema: ENG_SCHEMA }),
  () => agent(scoutPrompt(), { label: 'catalogue-scout', phase: 'Foundations', model: S, schema: SCOUT_SCHEMA }),
])
const eng0Flags = engFlags(eng0, ENG_IDS, true)
const scoutFlags = !scout ? ['scout failed (no result)'] : [].concat(scout.sources.some(s => s.reachable) ? [] : ['no source reported reachable'], scout.done_written ? [] : ['DONE file not reported written: treat the directory as unusable'])
if (eng0Flags.length) log('engineer-r0 flags: ' + eng0Flags.join('; '))
if (scoutFlags.length) log('scout flags: ' + scoutFlags.join('; '))
const foundations = `## Foundations (read both report files)\n### Harness engineer (standing pass)\nreport file: ${docOf('engineer-r0')}\n${eng0 ? `harness ${eng0.harness_version}; ${flagLine(eng0Flags)}\nSummary: ${eng0.summary}` : '(failed)'}\n### Catalogue scout\nreport file: ${docOf('catalogue-scout')}; shared directory ${sharedOf(0)}/ (usable only if DONE exists)\n${scout ? `${flagLine(scoutFlags)}\nSources: ${scout.sources.map(s => `${s.name}=${s.reachable ? 'reachable' : 'not reachable'}`).join(', ')}\nSummary: ${scout.summary}` : '(failed)'}`
const eng0Item = (id) => eng0 && (eng0.items || []).find(x => x.id === id)
if (!eng0 || !eng0.selftest_passed || !eng0.default_output_unchanged || !['declaration_hashing', 'plain_80_rule'].every(id => eng0Item(id) && eng0Item(id).status === 'done')) {
  log('STOP: the standing harness pass is not usable (' + eng0Flags.join('; ') + '); no Opus agent started')
  return { error: 'harness engineer pass failed or incomplete', foundations }
}
const shared0 = [{ round: 0, dir: sharedOf(0), doc: docOf('catalogue-scout') + (scout ? '' : ' (FAILED)') }]
const engDocs0 = [docOf('engineer-r0') + (eng0 ? '' : ' (FAILED)')]

phase('Plan')
const coverage1 = [
  `read ${W5_DIR}/README.md and RESULTS.md, ${W4_DIR}/RESULTS.md and ${W3_DIR}/RESULTS.md`,
  'list which per-agent reports in the sanitised folders you read (file names) and which claims from them you verified',
  'read the evalkit README and the fold, label, pool and decision-rule code',
  'read the engineer-r0 and catalogue-scout report files and weighed their flags',
  'verified at least one claim you rely on from an earlier workflow by reading its report or code, or by a quick dev-only check, or stated why not',
  'goal_coverage addresses every element of the goal and says how catalogue discovery is addressed; evaluation_design is complete enough that two readers would apply it identically and states the decision rule exactly as the owner set it',
].map(x => '- ' + x).join('\n')
const plan1 = normPlan(await agent(leadPlanPrompt(foundations, coverage1), { label: 'research-lead-plan', phase: 'Plan', schema: PLAN_SCHEMA, model: O }))
if (!plan1) return { error: 'research lead plan failed', foundations }
if (!plan1.evaluation_design) log('FLAG: the lead returned no evaluation_design; builders are told to state which comparators and decision rule they used')
{ const f = [].concat(leakFlag(plan1, 'plan lead'), capFlag(plan1, LEAD_MAX)); if (f.length) log('plan lead flags: ' + f.join('; ')) }
log(`Round 1: ${plan1.tasks.length} task(s); engineer addendum: ${plan1.evaluation_changes ? 'yes' : 'no'}; shared prep: ${plan1.shared_prep ? 'yes' : 'no'}`)

phase('Round 1')
const r1 = await runRound(1, plan1, { engDocs: engDocs0, shared: shared0, design: plan1.evaluation_design })

phase('Lead review')
const hist1 = `${foundations}\n\n## Research lead plan (round 1)\n${JSON.stringify({ assessment: plan1.assessment, goal_coverage: plan1.goal_coverage, evaluation_design: plan1.evaluation_design, evaluation_changes: plan1.evaluation_changes, shared_prep: plan1.shared_prep, tasks: plan1.tasks }, null, 1)}\n\n## Engineer addendum\n${r1.eng ? 'report file: ' + docOf('engineer-r1') : '(none or failed)'}\n\n## Shared prep round 1\n${r1.prep ? 'report file: ' + docOf('prep-r1') + ' (inputs in ' + sharedOf(1) + '/)' : '(none or failed)'}\n\n## Round 1 builders\n${r1.builders}\n\n## Round 1 devil's advocates\n${r1.das}`
const coverage2 = [
  'read every builder and devil\'s advocate report file of round 1 (one entry each)',
  'for each builder, re-ran or re-derived at least one headline score from its code and outputs, or stated why not',
  'weighed every flag listed above; for every claim flagged as not re-run by either devil\'s advocate, re-ran or re-derived it yourself or said why not',
  'spot-checked one devil\'s advocate re-run per builder against its files, or stated why not',
  'goal_coverage says what the evidence so far does and does not support for each element of the goal, and which model(s) could be final',
  'for every round-2 task, could_change names a specific round-1 conclusion; if tasks is empty, said why the goal is answered as far as the data allows',
].map(x => '- ' + x).join('\n')
const review = normPlan(await agent(`You are the RESEARCH LEAD reviewing round 1 and deciding round 2. Round 2 may be empty. The evaluation design in your plan above stays in force and the harness is frozen. Final models can only be chosen later among predictors built, declared and evaluated in this workflow, so if combining or finishing models is needed it must be a round-2 task.
${CONTEXT}
${sched('research-lead-review')}
## This workflow so far
${hist1}
${leadRules(2)}
${softCap(LEAD_MAX)} Report start_utc and end_utc from the date command. Round-2 briefs must not contain any held-out score.
Coverage list:
${coverage2}`, { label: 'research-lead-review', phase: 'Lead review', schema: REVIEW_SCHEMA, model: O }))
let r2 = null
if (review) { const f = [].concat(leakFlag(review, 'review lead'), capFlag(review, LEAD_MAX)); if (f.length) log('review lead flags: ' + f.join('; ')) }
if (review && review.tasks.length) {
  log(`Round 2: ${review.tasks.length} task(s); builder cap ${R2_BUILDER_MAX} min`)
  phase('Round 2')
  r2 = await runRound(2, review, { engDocs: r1.c.engDocs, shared: r1.c.shared, design: r1.c.design })
} else {
  log(review ? 'No round 2 (review lead returned no tasks).' : 'WARNING: review lead failed; no round 2.')
}

phase('Final')
const hist2 = `${hist1}\n\n## Research lead review\n${review ? JSON.stringify({ assessment: review.assessment, goal_coverage: review.goal_coverage, evaluation_design: review.evaluation_design, shared_prep: review.shared_prep, tasks: review.tasks }, null, 1) : '(failed)'}\n\n${r2 ? `## Shared prep round 2\n${r2.prep ? 'report file: ' + docOf('prep-r2') + ' (inputs in ' + sharedOf(2) + '/)' : '(none or failed)'}\n\n## Round 2 builders\n${r2.builders}\n\n## Round 2 devil's advocates\n${r2.das}` : '(no round 2)'}`
const final = await agent(`You are the RESEARCH LEAD writing the final report and the sealed-test package. You do not build or change predictors: you may only select among predictors that were built, declared and evaluated in this workflow. ${softCap(FINAL_MAX)}
${CONTEXT}
${sched('research-lead-final')}
## This workflow
${hist2}
Coverage list (read every builder and devil's advocate report file of both rounds first; weigh every flag above):
- list the files you read and the headline scores you re-derived from code and outputs; spot-check at least one devil's advocate re-run
- say how you weighed each flag
## Deliverables
1. ${PROJ}/RESULTS-W6.md, plain English for a non-specialist, concise: what was assembled and what it can and cannot do toward "what new songs should I listen to?" (including what the catalogue scout found reachable); the final model(s) with dev results, devil's advocate findings and the harness version each number comes from; decisions by the owner's 80% rule; what the evidence does and does not support; state of the held-out slices in words only (no held-out numbers); process problems. Anything you would recommend doing next goes ONLY in a final section "Next steps (kept separate)".
2. The sealed-test package in ${PKG}/ (create it): PREREG.md plus FILES.sha256. PREREG.md fixes, before any sealed scoring: the exact final predictor file(s) and every file of their bundles with sha256; the comparators and baselines; the evaluation design and decision rule exactly as they would be applied; a proposed pass criterion for the owner to approve (nobody applies it until approved); every input the final model(s) need when scored on the sealed folds and how each is produced without looking at sealed labels or results; the expected runtime; what the sealed run will and will not tell the owner. Do not run --sealed, do not register anything, do not read .sealed/.
Write your own report file with everything you read and re-derived; held-out numbers may appear only there. Return the full text of RESULTS-W6.md.`, { label: 'research-lead-final', phase: 'Final', model: O })

phase('Package check')
const pkgCheck = final ? await agent(`You are the PACKAGE AUDITOR. A research lead produced ${PROJ}/RESULTS-W6.md and the sealed-test package ${PKG}/. The sealed test is single-use, so you check that the package is ready before the owner sees it. You change nothing except your own report. ${softCap(AUDIT_MAX)} Report start_utc and end_utc from the date command.
${CONTEXT}
${sched('package-check')}
Check, each with evidence (command and output):
- every file in the package exists and every sha256 in FILES.sha256 / PREREG.md matches the file now; the bundle listed equals what the final predictor(s) actually import or load (trace it)
- the final predictor code contains no access to .sealed/, the decoy universe, raw streams, _load_all, listening_stats.csv or top_tracks.json except as the rules allow (grep and read)
- the harness selftest passes; the final predictor(s) run in fast mode and reproduce the numbers reported in RESULTS-W6.md
- the decision rule and pass criterion in PREREG.md are unambiguous: write down every way two readers could reach different pass/fail answers
- the list of sealed-time inputs is complete: for each input the predictor needs, how it would be produced for the sealed folds from data allowed at that time; list any that cannot be
- RESULTS-W6.md and the package contain no held-out (LATE) number
- the harness budget file still shows HOLDOUT budget 0 and no registration or sealed log entry exists
- evalkit/make_sealed.py, sealed_manifest.json and register.py still match the sha256 recorded by ${docOf('engineer-r0')}, and no later engineer report or predictor code changed the sealed code path
Write your report file; return the structured result.`, { label: 'package-check', phase: 'Package check', model: S, schema: {
  type: 'object',
  properties: {
    ready: { type: 'boolean', description: 'true only if every check above passed with evidence' },
    issues: { type: 'array', items: { type: 'object', properties: { severity: { type: 'string', enum: ['blocking', 'minor'] }, text: { type: 'string' } }, required: ['severity', 'text'] } },
    checks_run: { type: 'array', items: { type: 'string' }, description: 'One line per check: command and outcome' },
    summary: { type: 'string', description: 'At most 250 words' },
    start_utc: { type: 'string' }, end_utc: { type: 'string' },
  },
  required: ['ready', 'issues', 'checks_run', 'summary', 'start_utc', 'end_utc'],
} }) : null
if (!final) log('WARNING: final lead failed; no package to check')
else if (!pkgCheck) log('WARNING: package check failed; the package is unchecked')
else { const f = capFlag(pkgCheck, AUDIT_MAX); if (f.length) log('package check flags: ' + f.join('; ')) }

return { foundations, plan1, round1: r1, review, round2: r2, final, packageCheck: pkgCheck }
