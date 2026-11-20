#!/usr/bin/env bash
# PreToolUse guard for Agent / Workflow tool calls.
#  - Agent with no model      -> forced to sonnet
#  - Agent with sonnet/haiku  -> allowed
#  - Agent with opus/other, or a fork (always inherits the main model) -> user must approve
#  - Workflow (spawns many agents, may use opus) -> user must approve
#  - Every allowed Agent call is forced to run_in_background: true
input=$(cat)
tool=$(jq -r '.tool_name // ""' <<<"$input")

ask() {
  jq -n --arg r "$1" '{systemMessage: $r,
    hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "ask", permissionDecisionReason: $r}}'
  exit 0
}

if [ "$tool" = "Workflow" ]; then
  ask "Workflow requested: it spawns multiple agents, possibly on Opus. Approve?"
fi

model=$(jq -r '.tool_input.model // "" | ascii_downcase' <<<"$input")
type=$(jq -r '.tool_input.subagent_type // "" | ascii_downcase' <<<"$input")
desc=$(jq -r '.tool_input.description // "agent"' <<<"$input")

if [ "$type" = "fork" ]; then
  ask "Fork agent \"$desc\" runs on the main (Opus) model. Approve spawning it?"
fi

allow_with() {  # $1 = model to set
  jq -n --argjson ti "$(jq '.tool_input' <<<"$input")" --arg m "$1" '{
    hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "allow",
      permissionDecisionReason: "Project hook: Sonnet/Haiku model, run in background",
      updatedInput: ($ti + {model: $m, run_in_background: true})}}'
  exit 0
}

case "$model" in
  "") allow_with sonnet ;;
  *sonnet*|*haiku*) allow_with "$model" ;;
  *) ask "Agent \"$desc\" requested on model \"$model\" (not Sonnet). Approve spawning it?" ;;
esac
