#!/bin/bash
# Parallel sibling of run_edge_bench.sh: bounded concurrency via a standalone worker script
# (no export -f). Same per-call semantics (byte-identical worker), resumable (skips existing
# non-empty verdicts), scores once at the end.
# usage: run_edge_bench_parallel.sh <model> [out_dir] [concurrency]
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
MODEL=${1:?model required, e.g. zhipu-coding/glm-5.2}
OUT=${2:-$HERE/verdicts-$(echo "$MODEL" | tr '/' '_')}
CONC=${3:-8}
mkdir -p "$OUT"
export HERE MODEL OUT

TODO=()
for f in "$HERE"/prompts/*.txt; do
  pid=$(basename "$f" .txt)
  [ -s "$OUT/$pid.json" ] && continue
  TODO+=("$pid")
done
echo "concurrency=$CONC todo=${#TODO[@]}/40 -> $OUT"
if [ ${#TODO[@]} -gt 0 ]; then
  printf '%s\n' "${TODO[@]}" | xargs -P "$CONC" -I{} "$HERE/edge_worker.sh" {}
fi
echo "--- scoring ---"
python3 "$HERE/score_edge_bench.py" "$OUT"
