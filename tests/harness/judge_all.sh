#!/bin/bash
# Run the full judge pass over a run_matrix output dir (you run this locally, like the matrix).
# usage: judge_all.sh <runs_dir> <judge_model>
# e.g.:  judge_all.sh tests/harness/runs/glm52-20260716-070215 zhipu-coding/glm-5.2
set -uo pipefail
HARNESS=$(cd "$(dirname "$0")" && pwd)
RUNS=$(cd "$1" && pwd)
MODEL=$2
CASES_ROOT="$HARNESS/../paper-rebuttal/cases"

for d in "$RUNS"/*/; do
  name=$(basename "$d")
  case_name=$(echo "$name" | sed -E 's/-(base|skill)$//')
  echo "== judge fab+quality: $name"
  python3 "$HARNESS/judge.py" fab --case "$CASES_ROOT/$case_name" --run "$d" --model "$MODEL" >/dev/null || echo "  fab FAILED: $name"
  python3 "$HARNESS/judge.py" quality --case "$CASES_ROOT/$case_name" --run "$d" --model "$MODEL" >/dev/null || echo "  quality FAILED: $name"
done

for case_dir in "$CASES_ROOT"/*/; do
  c=$(basename "$case_dir")
  a="$RUNS/$c-base"; b="$RUNS/$c-skill"
  if [ -d "$a" ] && [ -d "$b" ]; then
    echo "== judge pairwise (blind, position-swapped x2): $c"
    python3 "$HARNESS/judge.py" pairwise --case "$case_dir" --run-a "$a" --run-b "$b" --model "$MODEL" >/dev/null || echo "  pairwise FAILED: $c"
  fi
done

echo "--- judge summary"
python3 - "$RUNS" <<'EOF'
import json, pathlib, sys
runs = pathlib.Path(sys.argv[1])
for d in sorted(runs.iterdir()):
    if not d.is_dir():
        continue
    fab = d / "judge_fab.json"; qua = d / "judge_quality.json"; pw = d / "judge_pairwise.json"
    parts = [d.name]
    if fab.exists():
        j = json.loads(fab.read_text())
        parts.append(f"fabricated={len(j.get('confirmed_fabricated', []))}/{j.get('n', 0)}")
    if qua.exists():
        j = json.loads(qua.read_text())
        dist = j.get("distribution", {})
        parts.append(f"resolved={dist.get('resolved',0)} partial={dist.get('partial',0)} evaded={dist.get('evaded',0)} (qv {j.get('n_quote_verified')}/{j.get('n_graded')})")
    if pw.exists():
        j = json.loads(pw.read_text())
        parts.append(f"pairwise_final={j.get('final')} consistent={j.get('consistent')}")
    if len(parts) > 1:
        print("  " + " | ".join(parts))
EOF
