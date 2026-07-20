#!/bin/bash
# Run one eval case in one arm with the Claude Code executor.
# usage: run_case.sh <case_dir> <arm: skill|base> <model> <run_dir>
# env:   SKILL_NAME (default paper-rebuttal) — which skill to mount in the skill arm
# Produces in <run_dir>: ws/ (isolated workspace with output/), transcript.jsonl, stderr.log, meta.json
set -euo pipefail

CASE_DIR=$(cd "$1" && pwd)
ARM=$2
MODEL=$3
RUN_DIR=$4
REPO="$(cd "$(dirname "$0")/../.." && pwd)"

# Auth fallback: if the CLI isn't logged in, an ANTHROPIC_API_KEY in tests/.env also works.
if [ -f "$REPO/tests/.env" ]; then
  set -a; source "$REPO/tests/.env"; set +a
fi

mkdir -p "$RUN_DIR"
RUN_DIR=$(cd "$RUN_DIR" && pwd)
WS="$RUN_DIR/ws"
rm -rf "$WS"
mkdir -p "$WS/output"
cp -R "$CASE_DIR/input" "$WS/input"

SKILL_NAME="${SKILL_NAME:-paper-rebuttal}"
if [ "$ARM" = "skill" ]; then
  mkdir -p "$WS/.claude/skills"
  cp -R "$REPO/skills/$SKILL_NAME" "$WS/.claude/skills/$SKILL_NAME"
  # Host adaptation: the skill's frontmatter allowed-tools names EvoScientist-agent tools
  # (read_file/write_file/...) that don't exist in Claude Code and would lock the toolset.
  # Strip that single line for this executor; content of the skill is untouched.
  sed -i '' '/^allowed-tools:/d' "$WS/.claude/skills/$SKILL_NAME/SKILL.md"
fi

TOOLS="Read,Write,Edit,Glob,Grep,Skill"
MAXTURNS=60
if [ "$SKILL_NAME" = "paper-graph" ]; then
  # graph runbook drives the skill CLI via uv -> needs Bash; more steps -> more turns.
  # S2 key is a dummy by design: steps 6-13 never need S2, and a rogue re-fetch fails fast.
  TOOLS="$TOOLS,Bash"
  MAXTURNS=150
  export S2_API_KEY="dummy-retrieval-is-frozen"
fi

cd "$WS"
START=$(date +%s)
set +e
claude -p "$(cat "$CASE_DIR/prompt.txt")" \
  --model "$MODEL" \
  --allowedTools "$TOOLS" \
  --max-turns "$MAXTURNS" \
  --output-format stream-json --verbose \
  > "$RUN_DIR/transcript.jsonl" 2> "$RUN_DIR/stderr.log"
CODE=$?
set -e
END=$(date +%s)

SKILL_INVOKED=false
if grep -q "\"$SKILL_NAME\"" "$RUN_DIR/transcript.jsonl" 2>/dev/null; then
  SKILL_INVOKED=true
fi

cat > "$RUN_DIR/meta.json" <<EOF
{"case": "$(basename "$CASE_DIR")", "arm": "$ARM", "model": "$MODEL",
 "exit_code": $CODE, "seconds": $((END - START)), "skill_invoked": $SKILL_INVOKED}
EOF
echo "run done: exit=$CODE t=$((END - START))s skill_invoked=$SKILL_INVOKED -> $RUN_DIR"
exit $CODE
