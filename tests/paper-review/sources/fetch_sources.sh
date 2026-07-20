#!/bin/bash
# Politely fetch arXiv e-print sources; gzip-integrity as the re-fetch criterion; 90s backoff x4.
set -u
cd "$(dirname "$0")"
IDS="2505.06120v1 2510.13786v1 2502.08524v1 2510.19811v1 2510.03194v1"

valid() { # src.bin exists, is gzip/tar, and decompresses cleanly
  f="$1/src.bin"
  [ -s "$f" ] || return 1
  if file -b "$f" | grep -qi gzip; then gzip -t "$f" 2>/dev/null; return $?; fi
  file -b "$f" | grep -qi "POSIX tar"
}

for id in $IDS; do
  mkdir -p "$id"
  if ! valid "$id"; then
    # clean stale junk from earlier failed attempts
    find "$id" -type f ! -name src.bin -delete 2>/dev/null
    for attempt in 1 2 3 4; do
      echo "fetch $id (attempt $attempt)"
      curl -sL --max-time 300 "https://export.arxiv.org/e-print/$id" -o "$id/src.bin"
      valid "$id" && break
      sleep $((90 * attempt))
    done
  fi
  if valid "$id"; then
    f="$id/src.bin"
    if tar tzf "$f" >/dev/null 2>&1; then (cd "$id" && tar xzf src.bin)
    elif file -b "$f" | grep -qi gzip; then gunzip -c "$f" > "$id/main.tex"
    else (cd "$id" && tar xf src.bin); fi
    main=$(grep -rl 'begin{document}' "$id" --include='*.tex' 2>/dev/null | head -1)
    echo "OK $id | tex=$(find "$id" -name '*.tex' | wc -l | tr -d ' ') | main=${main:-NONE}"
  else
    echo "FAIL $id (still invalid after retries)"
  fi
  sleep 30
done
echo DONE
