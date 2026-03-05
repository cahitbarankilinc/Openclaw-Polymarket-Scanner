#!/bin/zsh
set -euo pipefail

# Ministral-3-Baran: two-stage local pipeline
# 1) frob/ministral-3:8b-thinking-q8_0 -> planning
# 2) ministral-3:8b -> final answer/code generation

THINK_MODEL="frob/ministral-3:8b-thinking-q8_0"
FINAL_MODEL="ministral-3:8b"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 '<task>' [output_file]"
  exit 1
fi

TASK="$1"
OUT_FILE="${2:-}"

PLAN_PROMPT=$(cat <<'EOF'
You are a planning model.
Think deeply, then output ONLY the content between these tags:
<PLAN>
...
</PLAN>
Rules:
- No code.
- Max 12 bullet points.
- Include algorithm choice, edge cases, and common pitfalls.
EOF
)

RAW_PLAN=$(ollama run "$THINK_MODEL" "$PLAN_PROMPT

TASK:
$TASK")

# Extract the section between <PLAN> and </PLAN>, fallback to raw text
PLAN=$(python3 - <<'PY'
import re,sys
text=sys.stdin.read()
m=re.search(r"<PLAN>\s*(.*?)\s*</PLAN>", text, re.S)
print((m.group(1) if m else text).strip())
PY
<<< "$RAW_PLAN")

FINAL_PROMPT=$(cat <<EOF
You are the final model.
Use the planner notes below, but DO NOT output analysis.
Return only the final answer.
If the task is coding: output only valid code.

Planner notes:
$PLAN

Task:
$TASK
EOF
)

FINAL_OUTPUT=$(ollama run "$FINAL_MODEL" "$FINAL_PROMPT")

if [[ -n "$OUT_FILE" ]]; then
  print -r -- "$FINAL_OUTPUT" > "$OUT_FILE"
  echo "Saved final output to: $OUT_FILE"
else
  print -r -- "$FINAL_OUTPUT"
fi
