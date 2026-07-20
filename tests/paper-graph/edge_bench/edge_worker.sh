#!/bin/bash
# One-pid worker for run_edge_bench_parallel.sh.
# Invoked as: edge_worker.sh <pid>  with MODEL / OUT / HEREd exported in the environment.
# Per-call semantics are byte-identical to run_edge_bench.sh (same prompt, same claude flags,
# same parse + verdict assert, same resumable skip-if-exists).
set -uo pipefail
pid="${1:?pid required}"
f="$HERE/prompts/$pid.txt"
[ -s "$OUT/$pid.json" ] && { echo "skip $pid"; exit 0; }
raw=$(claude -p "$(cat "$f")" --model "$MODEL" --max-turns 1 --output-format json 2>"$OUT/$pid.err") || {
  echo "FAIL $pid (see $OUT/$pid.err)"; exit 0; }
echo "$raw" | python3 -c "
import json, re, sys
payload = json.load(sys.stdin)
text = re.sub(r'^\`\`\`(json)?|\`\`\`$', '', payload.get('result', '').strip(), flags=re.M).strip()
v = json.loads(text)
assert v.get('verdict') in ('SUPPORTED_BY_ABSTRACT','SUPPORTED_BY_SECTION','INFERRED','REJECT'), v
print(json.dumps(v))
" > "$OUT/$pid.json" 2>"$OUT/$pid.parse_err" || { echo "PARSE-FAIL $pid"; rm -f "$OUT/$pid.json"; exit 0; }
echo "done $pid: $(cat "$OUT/$pid.json" 2>/dev/null | head -c 60)"
