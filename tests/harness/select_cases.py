#!/usr/bin/env python3
"""Select pilot rebuttal-eval cases from the ICLR 2026 dump (davidheineman/iclr-2026)."""
import json
import statistics
import sys
from collections import Counter

POOL = sys.argv[1] if len(sys.argv) > 1 else "pool/iclr2026.json"

with open(POOL) as f:
    papers = json.load(f)

print(f"total rows: {len(papers)}")
print("venue_type distribution:", Counter(p.get("venue_type") for p in papers).most_common(10))

def review_ok(r):
    text = (r.get("summary") or "") + (r.get("strengths") or "") + (r.get("weaknesses") or "") + (r.get("review") or "")
    return r.get("rating") is not None and len(text) > 400

candidates = []
for p in papers:
    revs = [r for r in (p.get("reviews") or []) if review_ok(r)]
    if len(revs) < 3 or not p.get("pdf"):
        continue
    ratings = sorted(r["rating"] for r in revs)
    wlens = [len(r.get("weaknesses") or "") for r in revs]
    candidates.append({
        "url": p["url"],
        "title": (p.get("title") or "")[:80],
        "venue_type": p.get("venue_type"),
        "n": len(revs),
        "ratings": ratings,
        "mean": round(statistics.mean(ratings), 2),
        "spread": ratings[-1] - ratings[0],
        "min_wlen": min(wlens),
        "abs_len": len(p.get("abstract") or ""),
    })

print(f"candidates with >=3 substantive reviews + pdf: {len(candidates)}")

def show(name, rows, k=8):
    print(f"\n=== {name} ===")
    for c in rows[:k]:
        print(f"  {c['ratings']} mean={c['mean']} {c['venue_type']:>9} minW={c['min_wlen']:>5} {c['url'][-14:]} {c['title']}")

accepted = {"poster", "spotlight", "oral"}
bucket_a = sorted([c for c in candidates if c["venue_type"] in accepted and 5.0 <= c["mean"] <= 6.0 and c["spread"] <= 4],
                  key=lambda c: -c["min_wlen"])
bucket_b = sorted([c for c in candidates if c["venue_type"] not in accepted and 4.0 <= c["mean"] <= 5.5 and c["spread"] >= 2],
                  key=lambda c: -c["min_wlen"])
bucket_c = sorted([c for c in candidates if c["spread"] >= 6], key=lambda c: -c["min_wlen"])

show("A: borderline-accept (arm-the-champion / resolve-fence-sitters)", bucket_a)
show("B: mixed-score reject (score-driving diagnosis)", bucket_b)
show("C: extreme split (3/8/8-type outlier dynamics)", bucket_c)
