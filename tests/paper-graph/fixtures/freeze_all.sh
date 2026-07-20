#!/bin/bash
# Freeze the retrieval layer for all 8 queries: resolve seeds + fetch_papers via the
# skill's own CLI (S2-backed). Resumable; polite 15s spacing between queries.
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
CLI="$REPO/skills/paper-graph/scripts/cli.py"
set -a; source "$REPO/tests/.env"; set +a
UV=~/.local/bin/uv

for d in "$HERE"/q*/; do
  qid=$(basename "$d")
  cd "$d"
  if [ -s papers.json ]; then echo "SKIP $qid (papers.json exists)"; continue; fi
  echo "== $qid"
  $UV run --with httpx --with python-dotenv python "$CLI" resolve_seed_papers \
      --query-file query.txt --out seed.json || { echo "  seed FAIL"; continue; }
  $UV run --with httpx --with python-dotenv python "$CLI" fetch_papers \
      --parsed-query parsed_query.json --seed seed.json --n 10 --out papers.json \
      || { echo "  fetch FAIL"; continue; }
  python3 - <<'PY'
import json
ps = json.load(open('papers.json'))
ids = [((p.get('externalIds') or {}).get('ArXiv'), (p.get('title') or '')[:55]) for p in ps]
print(f"  fetched {len(ps)}:")
for a, t in ids:
    print(f"    {a}  {t}")
PY
  sleep 15
done
echo FREEZE-DONE
