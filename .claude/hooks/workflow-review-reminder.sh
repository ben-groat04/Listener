#!/usr/bin/env bash
# Stop hook: if a workflow run in this session has finished (every started agent has a result
# and the journal has been quiet for 2+ minutes) and has no review marker, block stopping and
# tell Claude to run the post-workflow review. The review agent creates <run dir>/.reviewed when done.
input=$(cat)
tp=$(jq -r '.transcript_path // ""' <<<"$input")
sid=$(jq -r '.session_id // ""' <<<"$input")
[ -n "$tp" ] && [ -n "$sid" ] || exit 0
wfdir="$(dirname "$tp")/$sid/subagents/workflows"
[ -d "$wfdir" ] || exit 0
now=$(date +%s); pending=()
for d in "$wfdir"/wf_*/; do
  j="$d/journal.jsonl"; [ -f "$j" ] && [ ! -f "$d/.reviewed" ] || continue
  started=$(grep -c '"type":"started"' "$j"); results=$(grep -c '"type":"result"' "$j")
  age=$(( now - $(stat -c %Y "$j") ))
  if [ "$started" -gt 0 ] && [ "$started" -eq "$results" ] && [ "$age" -ge 120 ]; then
    pending+=("$(basename "$d")")
  fi
done
[ ${#pending[@]} -eq 0 ] && exit 0
jq -n --arg r "Finished workflow run(s) not yet reviewed: ${pending[*]} (in $wfdir). Per project rules, spawn a background Sonnet agent to review the logs (how to improve future workflows, how steered it was) and clean the project folders; it must create .reviewed in each run dir when done." \
  '{decision: "block", reason: $r}'
