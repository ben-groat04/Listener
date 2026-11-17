#!/bin/bash
# Every 2 minutes: commit and push whatever exists, so a container reset loses little.
cd "$(dirname "$0")/../.."
while true; do
  sleep 120
  git add -A >/dev/null 2>&1
  git diff --cached --quiet || git commit -q -m "v1: autosave $(date -u +%H:%M)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DcM8jtvPtK2Am3XAi7g82X"
  for i in 1 2 3; do git push -q origin HEAD:ccr-1a19516b-5p6iyk 2>/dev/null && break; git fetch -q origin ccr-1a19516b-5p6iyk && git merge -q --no-edit FETCH_HEAD >/dev/null 2>&1; sleep 5; done
done
