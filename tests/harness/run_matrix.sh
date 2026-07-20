#!/bin/bash
# Run the full case x arm matrix with the Claude Code executor, then summarize.
# usage: run_matrix.sh [model] [out_root] [case_dir ...]
# env:   SKILL_NAME=paper-rebuttal|paper-review  (default paper-rebuttal)
#        selects the mounted skill, the default cases dir, and the checker
set -uo pipefail
HARNESS=$(cd "$(dirname "$0")" && pwd)
MODEL=${1:-claude-sonnet-5}
OUT=${2:-$HARNESS/runs/$(date +%Y%m%d-%H%M%S)}
shift 2 2>/dev/null || shift $# 2>/dev/null || true

export SKILL_NAME="${SKILL_NAME:-paper-rebuttal}"
case "$SKILL_NAME" in
  paper-rebuttal) CASES_DIR="$HARNESS/../paper-rebuttal/cases"; CHECKER="$HARNESS/check_rebuttal.py" ;;
  paper-review)   CASES_DIR="$HARNESS/../paper-review/cases";   CHECKER="$HARNESS/check_review.py" ;;
  paper-graph)    CASES_DIR="$HARNESS/../paper-graph/cases";    CHECKER="$HARNESS/check_graph_case.py" ;;
  *) echo "unknown SKILL_NAME: $SKILL_NAME" >&2; exit 1 ;;
esac

if [ $# -gt 0 ]; then
  CASES="$*"
else
  CASES=$(ls -d "$CASES_DIR"/*/)
fi

mkdir -p "$OUT"
for case in $CASES; do
  for arm in base skill; do
    name="$(basename "$case")-$arm"
    echo "=== $name ($MODEL, $SKILL_NAME)"
    "$HARNESS/run_case.sh" "$case" "$arm" "$MODEL" "$OUT/$name" || echo "RUN FAILED: $name"
    python3 "$CHECKER" "$case" "$OUT/$name/ws" --meta "$OUT/$name/meta.json" \
      > "$OUT/$name/metrics.json" 2> "$OUT/$name/checker.err" || echo "CHECK INCOMPLETE: $name"
  done
done
python3 "$HARNESS/summarize.py" "$OUT"
