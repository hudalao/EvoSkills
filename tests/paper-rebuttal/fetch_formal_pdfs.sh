#!/bin/bash
# Fetch v1 PDFs for the formal-set roster (polite spacing; %PDF magic as validity check).
set -u
cd "$(dirname "$0")"
mkdir -p formal_pdfs
PAIRS="04:2505.11298 05:2509.10260 06:2503.11958 07:2507.12956 08:2509.04499 09:2509.23102 10:2505.12565"
for pair in $PAIRS; do
  n="${pair%%:*}"; id="${pair##*:}"
  f="formal_pdfs/${n}_${id}v1.pdf"
  if [ -s "$f" ] && head -c 4 "$f" | grep -q '%PDF'; then echo "SKIP $f"; continue; fi
  for attempt in 1 2 3; do
    curl -sL --max-time 240 "https://export.arxiv.org/pdf/${id}v1" -o "$f"
    if head -c 4 "$f" | grep -q '%PDF'; then echo "OK $f ($(wc -c < "$f" | tr -d ' ')B)"; break; fi
    echo "retry $id (attempt $attempt)"; sleep $((60 * attempt))
  done
  sleep 30
done
echo DONE
