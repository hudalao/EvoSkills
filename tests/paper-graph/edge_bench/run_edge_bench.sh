#!/bin/bash
# Run the audit_edge micro-benchmark: 40 one-shot LLM calls with the skill's own template.
# usage: run_edge_bench.sh <model> [out_dir]     (resumable: skips existing verdicts)
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
MODEL=${1:?model required, e.g. zhipu-coding/glm-5.2}
OUT=${2:-$HERE/verdicts-$(echo "$MODEL" | tr '/' '_')}
mkdir -p "$OUT"

n=0
for f in "$HERE"/prompts/*.txt; do
  pid=$(basename "$f" .txt)
  [ -s "$OUT/$pid.json" ] && continue
  n=$((n + 1))
  raw=$(claude -p "$(cat "$f")" --model "$MODEL" --max-turns 1 --output-format json 2>"$OUT/$pid.err") || {
    echo "FAIL $pid (see $OUT/$pid.err)"; continue; }
  echo "$raw" | python3 -c "
import json, re, sys
payload = json.load(sys.stdin)
text = re.sub(r'^\`\`\`(json)?|\`\`\`$', '', payload.get('result', '').strip(), flags=re.M).strip()
v = json.loads(text)
assert v.get('verdict') in ('SUPPORTED_BY_ABSTRACT','SUPPORTED_BY_SECTION','INFERRED','REJECT'), v
print(json.dumps(v))
" > "$OUT/$pid.json" 2>"$OUT/$pid.parse_err" || { echo "PARSE-FAIL $pid"; rm -f "$OUT/$pid.json"; }
  echo "done $pid: $(cat "$OUT/$pid.json" 2>/dev/null | head -c 60)"
done
echo "ran $n new calls -> $OUT"
python3 "$HERE/score_edge_bench.py" "$OUT"
