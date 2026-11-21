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

const ENG_R1 = "ENGINEER REPORT: evalkit v3 is implemented in /home/user/Listener/taste-model/evalkit/. The iTunes preview fallback (item 6) is built but NOT active; everything else in the spec is done.\n\nNothing is committed. I did not run --sealed, make_sealed, or any sealed cutoff. I did not read PLAN.md, .sealed/ or earlier logs, and I did not open streams.jsonl directly; all stream access went through evalkit's loader.\n\n## 1. The item that did not complete: iTunes preview fallback\n**What happened**\n- The iTunes Search API rate-limits this container to roughly 6-15 lookups per minute. The original 2355 lookups would have taken hours. I saw 403 responses, and a second concurrent client made the 403s worse. The main session also flagged the projected duration, so I cut the scope.\n- Scope now: preview-less user tracks that are tried songs in a dev fold, plus a seeded sample of 250 preview-less decoys. Other preview-less train-only user tracks are not looked up. This deviates from the spec's \"every user track\".\n- Even this reduced scope did not finish. At the time I stopped it, `.cache/itunes_fallback.csv` held about 270 rows (it grew a little after the final run because a stray process kept appending; I killed it).\n- `fetch_itunes.py` is resumable and writes `.cache/itunes_fallback.complete` once all its targets are resolved. `data.load_meta_all` fills previews, and decoy eligibility changes, only when that marker exists. A partial fill would make \"preview present\" mean different things for tried songs and decoys.\n\n**Consequence**\n- previewUrl is currently exactly what stats.fm provides. Coverage is about 82% of tried songs and 87% of decoys.\n- Missing previews stay NaN and must be handled explicitly by predictors.\n\n**Selftest numbers**\n- The selftest's metadata-shape shortcut classifier gets AUC 0.587 (AUC 0.595 when the release-age bucket is added), both under the 0.62 limit.\n- The release-age bucket is available for all tried songs (0% unknown).\n\n**To finish it:** run `python3 -m evalkit.fetch_itunes` repeatedly (about 15 per minute at best), then rebuild pools and rerun the selftest. The preview audio cache would then need a resumable `fetch_previews` top-up.\n\n## 2. What changed (all in evalkit/; README.md rewritten, selftest.py updated, passing)\n- **Folds.**\n  - 14 quarterly dev cutoffs, 2021-07 to 2024-10.\n  - TUNE is 10 folds, LATE is 4 folds, ALL is both.\n  - `--fast` is TUNE only, nboot 100, no independence check, no LATE.\n  - The default run is TUNE, nboot 300, with the independence check.\n  - `--late` prints separate TUNE, LATE and ALL tables and appends a JSON line to `.cache/late_runs.log`: UTC time, predictor paths, sha256 of each file, plus whether the run was `--null-control` and the `--window` setting.\n  - The log currently holds one line, from my final baseline-only `--late` run. I deleted the earlier test lines.\n- **Labels.** `share90` is added. Spearman of the score against days90, log1p(plays90) and share90 is reported.\n- **Baselines.**\n  - Kept: popularity, artist_plays, artist_recent, artist_love_rate.\n  - Added: `duration` (a one-feature gradient-boosting model), `meta_gbm` and `nonaudio_gbm`.\n  - `random` is removed as a scored model. Tie noise is removed everywhere.\n  - Point-in-time artist features are verified by a selftest that recomputes them from truncated history.\n  - Design choice to review: an unconstrained `nonaudio_gbm` learned the reversed direction on TUNE (sauc 0.46) because artist-history counts are confounded with calendar time. I added monotone constraints on the familiarity features and a 180-day recency weight on training songs, for all GBM baselines. I chose the 180-day half-life to match artist_recent and tested only a handful of variants, on TUNE only. They are constants at the top of `baselines.py`.\n- **Diagnostics.**\n  - They are computed inside the harness from pool columns, not through the predictor interface: pool_artist_siblings, pool_album_siblings, exposure_session, oracle_day1, oracle_7d.\n  - For exposure_session, decoys are scored below every tried song.\n  - Oracles are 0 for decoys.\n- **Metrics (rewritten in metrics.py).**\n  - Everything runs on one weighted engine: bootstrap weights come from artist-cluster resampling. The selftest checks it against brute force.\n  - Reported: sauc for all, new-artist and known-artist songs; wa_sauc, ww_sauc and ws_sauc; plift; p20; AP lift; CIs; paired lower-bound tables against every other model for sauc and wa (open-pool variants too, plus p20); permutation null band (200 permutations, cached); per-fold AUC with CI; the BELOW CHANCE flag.\n  - Tie-averaging for p10/p20/r20/hits is the exact expectation over random tie-breaks, which is the limit of the 20-seed average. The 20-seed average is used for AP, lift, r20 and macro AUC.\n- **Open pool.**\n  - Seeds are chosen per fold from pre-cutoff plays only (top 300 artists plus up to 6 related artists of each of the top 150). A selftest asserts that truncating history at the cutoff leaves the seeds unchanged.\n  - The decoy universe is now one file with `source_artists` per track. It has 84,875 tracks, built with `make_decoys.py` from the existing raw cache plus newly fetched artists.\n  - Exclusion of any song the user ever played stays as before, and is documented in the README.\n  - Draws are covariate-matched in two stages (draw 8 times the tried count, then 5 times).\n  - Release-age buckets use stats.fm album dates, cached in `.cache/album_release.json`, and are included in both the matching model and the selftest classifier.\n  - `open_wa_sauc` is implemented: loved tried songs against decoys by the same primary artist.\n- **VERDICT table.**\n  - It has no fixed thresholds. The diagnostic reference rows are printed at the top of each slice.\n  - Null control is PASS only if tried sauc and wa_sauc both lie inside the 95% permutation band.\n  - Label-variant consistency is reported, not gated.\n  - When a predictor file has no `PREDICTORS` dict, its model name is now the file stem instead of the full path.\n- **Cache hashes.** Pool and baseline cache hashes no longer depend on the partial iTunes csv; they depend only on its completion marker.\n- **Stale caches.** Deleted old pools, baseline pickles and null bands. Current ones are in `.cache/shared/` (one pools, one baseline-scores, one nullband file). The Workflow 2 feature caches (`clap-preview-emb`, `hand-audio-feat-v1`, `C-textemb-v1`) are untouched and are noted in the README as covering the old pools only. No failed-attempt code was left in the project.\n\n## 3. Shared artefact: preview audio cache\n- Location: `/home/user/Listener/taste-model/.cache/shared/previews/`\n- Contents: `audio/<md5(previewUrl)>.<ext>` holds the original downloaded bytes, unchanged. `manifest.csv` has columns md5, previewUrl, ext, bytes, duration_s, source, ok, error.\n- Size and status: 9220 distinct previewUrls, all 9220 ok, about 4 GB. All 14 dev cutoffs are included; no sealed cutoffs.\n- Script: `evalkit/fetch_previews.py` (resumable, at most 6 threads; `--report` prints coverage).\n- Coverage by fold, fraction of tried songs / decoys with ok audio:\n\n| Fold | Tried | Decoys |\n|---|---|---|\n| 2021-07 | 0.727 | 0.850 |\n| 2021-10 | 0.612 | 0.743 |\n| 2022-01 | 0.673 | 0.840 |\n| 2022-04 | 0.750 | 0.885 |\n| 2022-07 | 0.717 | 0.808 |\n| 2022-10 | 0.775 | 0.872 |\n| 2023-01 | 0.796 | 0.849 |\n| 2023-04 | 0.841 | 0.874 |\n| 2023-07 | 0.755 | 0.827 |\n| 2023-10 | 0.823 | 0.849 |\n| 2024-01 | 0.879 | 0.894 |\n| 2024-04 | 0.846 | 0.895 |\n| 2024-07 | 0.871 | 0.939 |\n| 2024-10 | 0.868 | 0.891 |\n\n- These URLs come from the pools before I made the iTunes fill inactive. The pools did not change (the fill was already inactive when they were built), so the scope still matches.\n- If the iTunes fill is later completed, the scope grows and `fetch_previews` needs a top-up run.\n\n## 4. Dev baseline scores (full run, `--late`, baselines only)\nFull output is in `/tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/final_run_baselines.log`.\n\nSelftest passes, with the same results as the final-state log in section 1. Chance is 0.5; the permutation band for TUNE sauc is (0.459, 0.537).\n\n**Tried pool, love label, all songs (sauc with 95% CI)**\n\n| Model | TUNE sauc | LATE sauc |\n|---|---|---|\n| popularity | 0.471 (0.435, 0.507) | 0.521 |\n| artist_plays | 0.619 (0.558, 0.652) | 0.454 |\n| artist_recent | 0.619 (0.550, 0.653) | 0.436 |\n| artist_love_rate | 0.550 (0.469, 0.630) | 0.493 |\n| duration | 0.559 (0.506, 0.606) | 0.564 |\n| meta_gbm | 0.524 (0.482, 0.570) | 0.558 |\n| nonaudio_gbm | 0.557 (0.512, 0.604) | 0.534 |\n| pool_artist_siblings (diag) | 0.630 | 0.546 |\n| exposure_session (diag) | 0.658 | 0.619 |\n| oracle_day1 (diag) | 0.766 | 0.821 |\n| oracle_7d (diag) | 0.880 | 0.906 |\n\n- The artist-based baselines are above chance on TUNE and not above it on LATE. artist_plays also trips the BELOW CHANCE flag on fold 2024-04.\n- Within-artist (`wa_sauc`) is 0.50 for all artist-only scores. This is by construction: same artist, same score.\n- On TUNE, nonaudio_gbm's `wa_sauc` is 0.540 and duration's is 0.607.\n\n**Open pool, TUNE (open sauc)**\n\n| Model | Open sauc |\n|---|---|\n| artist_recent | 0.749 |\n| artist_plays | 0.728 |\n| nonaudio_gbm | 0.600 |\n| popularity | 0.511 |\n\n- For exposure_session and the oracles, the open-pool numbers are high by construction: decoys sit below every tried song and the oracles give them 0.\n\n**Null control check**\n- `--null-control` run on a mock predictor (artist_recent plus popularity) returned FAIL (sauc 0.60 on TUNE, outside the band).\n- The identity shuffle preserves the number of songs per artist, which is itself a familiarity signal, so the check is strict for artist-based scores.\n- I did not run null control on the real baselines.\n\n## 5. Comparability and usage\n- **Comparability.** Earlier scores are not comparable. The folds, decoys (re-seeded per fold), baselines (tie noise removed, GBMs added), CIs and bar all changed. The README says so.\n- **Sealed cutoffs.** The code paths exist but I did not run them. Before any sealed run the main session must:\n  1. run `python3 -m evalkit.make_decoys --sealed` (fetches the extra seed artists);\n  2. optionally run `python3 -m evalkit.fetch_itunes --sealed` and finish the dev lookups;\n  3. run `make_sealed --write-manifest`.\n- **Early folds.** The first folds are tiny (2021-07 has 44 tried songs, a love rate near 65%) and noisy.\n- **Environment.** About 2 threads were used throughout. The early `fetch_itunes` process briefly exceeded that while building its decoy target list, before I applied thread limits."

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
  if (round === 1) {
    eng = ENG_R1  // round-1 engineer finished but its report was delivered outside the workflow; injected verbatim
  } else if (plan.evaluation_changes || plan.shared_prep) {
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
