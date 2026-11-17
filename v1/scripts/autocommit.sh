#!/bin/bash
# Every 2 minutes: commit and push whatever exists, so a container reset loses little.
# Optional env: AUTOCOMMIT_TRAILER = trailer lines appended to each commit message (e.g. "Co-Authored-By: ...<newline>Claude-Session: ...");
#   omitted when unset. Files modified in the last 20 s are skipped (may be half-written). Push errors go to v1/logs/autocommit.log.
cd "$(dirname "$0")/../.."
LOG=v1/logs/autocommit.log; mkdir -p v1/logs
log() { echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }
while true; do
  sleep 120
  NOW=$(date +%s); SKIP=()
  # untracked or modified files touched in the last 20 s are left out of this commit
  while IFS= read -r f; do
    [ -n "$f" ] && [ -e "$f" ] && [ $((NOW - $(stat -c %Y "$f"))) -lt 20 ] && SKIP+=("$f")
  done < <(git ls-files -m -o --exclude-standard)
  git add -A >/dev/null 2>>"$LOG"
  [ ${#SKIP[@]} -gt 0 ] && git reset -q -- "${SKIP[@]}" 2>>"$LOG"
  if ! git diff --cached --quiet; then
    MSG="v1: autosave $(date -u +%H:%M)"
    [ -n "${AUTOCOMMIT_TRAILER:-}" ] && MSG="$MSG

$AUTOCOMMIT_TRAILER"
    git commit -q -m "$MSG" 2>>"$LOG" || log "commit failed"
  fi
  B=$(git rev-parse --abbrev-ref HEAD); OK=""
  for i in 1 2 3; do
    if OUT=$(git push -q origin HEAD:$B 2>&1); then OK=1; break; fi
    log "push attempt $i failed: $OUT"
    OUT=$(git fetch -q origin $B 2>&1 && git merge -q --no-edit FETCH_HEAD 2>&1) || log "fetch/merge failed: $OUT"
    sleep 5
  done
  [ -n "$OK" ] || log "push gave up after 3 attempts"
done
