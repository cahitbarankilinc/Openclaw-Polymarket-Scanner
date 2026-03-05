#!/bin/zsh
set -euo pipefail

# Ministral-3-Baran: chained local pipeline
# 1) thinking model produces reasoning notes (time-bounded)
# 2) non-thinking model receives:
#    - user prompt
#    - thinking model output
#    - system prompt (constructed for this pipeline)

THINK_MODEL="frob/ministral-3:8b-thinking-q8_0"
FINAL_MODEL="ministral-3:8b"
THINK_TIMEOUT="${THINK_TIMEOUT_SECONDS:-300}"   # default 5 min
FINAL_TIMEOUT="${FINAL_TIMEOUT_SECONDS:-300}"   # default 5 min

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 '<task>' [output_file]"
  echo "Env: THINK_TIMEOUT_SECONDS (default 300), FINAL_TIMEOUT_SECONDS (default 300)"
  exit 1
fi

TASK="$1"
OUT_FILE="${2:-}"

PLAN_PROMPT=$(cat <<'EOF'
You are a planning model.
Think deeply, then output concise planning notes.
Rules:
- Prefer bullets.
- Max 15 bullets.
- Include algorithm choice, edge cases, pitfalls, and test strategy.
- If task is coding, do NOT output final code, only plan/reasoning notes.
EOF
)

RAW_PLAN_FILE=$(mktemp)
FINAL_OUT_FILE=$(mktemp)

# ---- Stage 1: thinking model (time-bounded) ----
python3 - "$THINK_MODEL" "$PLAN_PROMPT" "$TASK" "$THINK_TIMEOUT" "$RAW_PLAN_FILE" <<'PY'
import subprocess, sys
model, plan_prompt, task, timeout_s, out_path = sys.argv[1:]
prompt = f"{plan_prompt}\n\nTASK:\n{task}\n"
try:
    p = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True,
        text=True,
        timeout=int(timeout_s),
        check=False,
    )
    content = p.stdout or ""
except subprocess.TimeoutExpired as e:
    content = e.stdout or ""
    if isinstance(content, bytes):
        content = content.decode("utf-8", errors="ignore")
    content = content.strip()
    if not content:
        content = "[TIMEOUT] Thinking model did not finish in time; continue with minimal plan."
if isinstance(content, bytes):
    content = content.decode("utf-8", errors="ignore")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)
PY

RAW_PLAN=$(cat "$RAW_PLAN_FILE")

# Basic cleanup for terminal noise/ANSI
PLAN=$(print -r -- "$RAW_PLAN" | perl -pe 's/\e\[[0-9;?]*[A-Za-z]//g' | tr -cd '\11\12\15\40-\176' )
if [[ -z "${PLAN// }" ]]; then
  PLAN="[EMPTY]"
fi

SYSTEM_PROMPT=$(cat <<'EOF'
You are the non-thinking executor model in a two-model pipeline.
Your job:
1) Read user prompt
2) Read thinking-model output as guidance
3) Produce final output only

Hard rules:
- No chain-of-thought, no explanations unless explicitly requested.
- If task is coding: output only valid code.
- Preserve exact constraints from user prompt (function names, test counts, output format).
- If thinking notes conflict with user prompt, user prompt wins.
EOF
)

FINAL_PROMPT=$(cat <<EOF
[USER_PROMPT]
$TASK

[THINKING_MODEL_OUTPUT]
$PLAN

[SYSTEM_PROMPT]
$SYSTEM_PROMPT

Now produce the final answer.
EOF
)

# ---- Stage 2: non-thinking model (time-bounded) ----
python3 - "$FINAL_MODEL" "$FINAL_PROMPT" "$FINAL_TIMEOUT" "$FINAL_OUT_FILE" <<'PY'
import subprocess, sys
model, prompt, timeout_s, out_path = sys.argv[1:]
try:
    p = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True,
        text=True,
        timeout=int(timeout_s),
        check=False,
    )
    content = p.stdout or ""
except subprocess.TimeoutExpired as e:
    content = e.stdout or ""
    if isinstance(content, bytes):
        content = content.decode("utf-8", errors="ignore")
    content = content.strip()
    if not content:
        content = "[TIMEOUT] Final model did not finish in time."
if isinstance(content, bytes):
    content = content.decode("utf-8", errors="ignore")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)
PY

FINAL_OUTPUT=$(cat "$FINAL_OUT_FILE")

if [[ -n "$OUT_FILE" ]]; then
  print -r -- "$FINAL_OUTPUT" > "$OUT_FILE"
  echo "Saved final output to: $OUT_FILE"
else
  print -r -- "$FINAL_OUTPUT"
fi

rm -f "$RAW_PLAN_FILE" "$FINAL_OUT_FILE"
