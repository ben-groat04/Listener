# Overnight plan: sealed test + first song suggestions (owner-approved 2026-11-22)

Owner's words: "you must run the sealed test too. I will wake up to new song suggestions."
The owner has seen the dev results; this message is the explicit go for the sealed run and for suggestions.
The proposed pass rule (PREREG.md section 5: S1 and S2 both decided positive) is applied as written.
Owner, verbatim, before sleeping: "To clarify so that you don't stop - I give my GO for the sealed test and anything else". This is standing approval for every stage below, including any owner go-ahead the PREREG asks for (e.g. a single fold under 90% coverage). Do not stop to ask; if the harness itself refuses (pooled coverage STOP), try the documented --retry, fix the cause if possible, and continue.

Each hourly firing of the scheduled task reads this file, finds the first unfinished stage (check the
STATE lines at the bottom), works on it, appends a STATE line, commits + pushes, and ends the turn while
long jobs run (background agents notify the session; the next firing continues). Never stop on a problem:
diagnose, fix (background Sonnet agents for code), continue. Status lines go in the STATE list, not chat.

## Stages

1. **Finish sealed feature build** (taste-model): resume `nohup python3 -W ignore -m evalkit.sealed_prep --main-session --threads 2 >> LOG 2>&1 &`
   (LOG = scratchpad/sealedprep/build.log, or taste-model/.cache/sealedprep_build.log if the scratchpad is gone). Resumable.
2. **Coverage gate** (PREREG.md section 3 step 5): `python3 -W ignore -m evalkit.sealed_prep --main-session --count`, `mert` column,
   groups tried and train. Pooled tried < 90% after one --retry = harness STOP: report to owner, do not run. A single fold < 90%
   with pooled >= 90%: owner pre-approved continuing (label results "coverage-limited").
3. **Sealed run (main session only, one look):** `sha256sum -c prereg-w6/FILES.sha256` all OK; then PREREG.md section 3 steps 6-7 exactly:
   `python3 -m evalkit.register predictors/w6r1-content-ranker-final/final_avg21_dev.py avg21_dev`;
   `python3 -W ignore -m evalkit.run --sealed predictors/w6r1-content-ranker-final/final_avg21_dev.py > SAVE.out 2> SAVE.err`
   (SAVE = taste-model/reports/sealed-w6/avg21_dev). Never run it twice; crash rule in PREREG.md. Extract S1-S4 + secondaries verbatim
   into taste-model/reports/sealed-w6/SEALED-RESULTS.md and apply the pass rule.
4. **Devil's advocate on the sealed result** (background Sonnet): may read SAVE.out/SEALED-RESULTS.md (sealed RESULTS only, never
   .sealed/labels.csv); checks the pass/fail reading against PREREG.md, coverage, crash/one-look rules. Signs off or not.
5. **Suggestions** (background Sonnet agent(s); after stage 3, the sealed period is no longer held out, so the model may now
   train on the full listening history up to today):
   - Model: avg21_dev if the sealed test passed; per PREREG.md, the incumbent ref_w4r1_listening if S3 came out decided negative;
     if S1 or S2 failed, still use avg21_dev but flag the list clearly as "model failed its sealed test".
   - Train on all history (streams.jsonl, all dates) with the same recipe; no retuning.
   - Candidates: Deezer related-artist walk (2 hops) from the owner's top ~50 artists of the last 12 months, plus Deezer genre charts of
     the owner's main genres (catalogue/ tools; previous walk produced 3,699 tracks). Exclude every track ever played (all history,
     match by normalised title + artist too). Aim for ~3,000 candidates with a preview; fetch with the catalogue client (Deezer is
     throttled at 4 req/s in catalogue.MIN_GAP; budget it), MERT via the same pipeline (~2.2 s/clip).
   - Score every candidate independently (independence check holds for avg21_dev).
   - Output taste-model/suggestions/SUGGESTIONS-1.md: top 30 overall, at most 2 per artist, split into "new artists" (never played)
     and "known artists"; each row: rank, title, artist, Deezer/Spotify link, preview source, score percentile. Also a CSV with all
     scored candidates.
   - Wait for jobs inside one blocking command (`timeout 590 bash -c 'until ...; do sleep 10; done'`); never end the turn while a job runs.
6. **Devil's advocate on the list** (background Sonnet): checks exclusion of already-played songs, artist cap, that scores come
   from the declared model trained as stated, no leakage, links valid. Fixes or flags.
7. **Final message to the owner** (end of the last firing; then disable the scheduled task with update_trigger enabled=false):
   sealed result in plain words (S1-S4, pass/fail), DA verdicts, and the suggestion list (top 30, new vs known artists), plus
   "tell me what you think of each" to start the feedback loop.

Rules kept: never read .sealed/labels.csv or other sealed inputs directly; only the main session registers/runs --sealed; no held-out
numbers outside reports/sealed-w6; commits end with the session's attribution lines; keep the owner's personal details out of external requests.

## STATE (append one line per stage change)
- 2026-11-22: stage 1 in progress (~2,850/5,056 MERT rows; tried + train done; ~2,200 decoy clips left).
- Owner, verbatim: "Including getting my stats.fm data if something goes wrong". If spotify-liked-songs/.cache/{streams.jsonl,top_tracks.json} are lost (container replaced), re-fetch them with `python3 spotify-liked-songs/statsfm_export.py` (owner-approved; the owner's own account). Caveat: a re-fetch can differ from the 2026-11-20 data (window, new plays), so re-run `evalkit.make_sealed` and check "matches manifest: True" before the sealed run; if it does not match, the sealed test is not valid as pre-registered — say so in the final message, skip stage 3, and still produce suggestions (stage 5) from avg21_dev trained on the re-fetched history, flagged "no valid sealed test".
- Owner, verbatim: "They will not match. You must provide me song suggestions regardless, trained on the old model if necessary. Even if the sealed test fails. I will be frustrated if I do not wake up to new music suggestions".
  OVERRIDING PRIORITY: a suggestion list (stage 5, checked by stage 6 if time allows) MUST exist by 07:00 UTC, whatever happens to stages 1-4.
  - Suggestions are produced in every case: sealed pass, sealed fail (flagged), no valid sealed test (flagged), data loss (flagged).
  - If the full-history data are unavailable or a re-fetch would not be ready in time, train on whatever history exists (the existing dev-era data / existing caches, i.e. "the old model") and say so.
  - Deadline rule: if at any firing after 03:00 UTC the sealed stages (1-4) are not finished, start stage 5 immediately in parallel (or instead), so the list is ready by 07:00 UTC; finish the sealed stages afterwards if possible.
  - If something blocks the full pipeline, fall back to the best model that can run in time (e.g. score candidates whose preview features can be computed in time; reduce the candidate count) and state the shortcut in the message. Never end the night without a list.
- 2026-11-22T22:42Z: stage 1 resumed (detached, pid 164; log scratchpad/sealedprep/build.log); data caches intact.
- Rule (owner concern): every long job started overnight gets a background watcher (Bash run_in_background, loop until the process exits or the log shows Traceback/error) so the session is woken immediately on finish or failure and moves to the next stage at once; the hourly firing is only a fallback. Agents are already notified on completion.
