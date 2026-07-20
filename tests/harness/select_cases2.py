#!/usr/bin/env python3
"""Join davidheineman (initial reviews, Nov'25 snapshot) x papercopilot (final ratings + decisions)
and pick pilot rebuttal-eval cases with known outcomes."""
import json
import re
import statistics
from collections import Counter

dh = json.load(open("pool/iclr2026.json"))
pc = json.load(open("pool/pc_iclr2026.json"))

pc_by_id = {p["id"]: p for p in pc}

def parse_dist(s):
    """papercopilot rating strings like '4;6;6;8' or '4, 6' -> sorted ints"""
    if not s:
        return []
    return sorted(int(x) for x in re.findall(r"\d+", str(s)))

def num(v):
    """papercopilot numeric fields are sometimes lists like [count, avg]; take the last numeric."""
    if isinstance(v, list):
        v = v[-1] if v else 0
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0

def review_ok(r):
    text = (r.get("summary") or "") + (r.get("strengths") or "") + (r.get("weaknesses") or "")
    return r.get("rating") is not None and len(text) > 400

joined = []
for p in dh:
    fid = p["url"].split("id=")[-1]
    q = pc_by_id.get(fid)
    if not q:
        continue
    revs = [r for r in (p.get("reviews") or []) if review_ok(r)]
    if len(revs) < 3 or not p.get("pdf"):
        continue
    init = sorted(r["rating"] for r in revs)
    final = parse_dist(q.get("rating"))
    if not final or len(final) < len(init):
        continue
    rec = {
        "forum": fid,
        "title": p.get("title") or "",
        "status": q.get("status"),
        "init": init,
        "final": final,
        "init_mean": round(statistics.mean(init), 2),
        "final_mean": round(statistics.mean(final), 2),
        "delta": round(statistics.mean(final) - statistics.mean(init), 2),
        "spread": init[-1] - init[0],
        "n_rev": len(revs),
        "wc_rebuttal": int(num(q.get("wc_reply_authors_avg"))),
        "min_wlen": min(len(r.get("weaknesses") or "") for r in revs),
        "pdf": p.get("pdf"),
    }
    joined.append(rec)

print(f"joined usable: {len(joined)}")
print("status dist:", Counter(r["status"] for r in joined).most_common(6))
rebutted = [r for r in joined if r["wc_rebuttal"] > 200]
print(f"with substantive rebuttal (wc>200): {len(rebutted)}")

def show(name, rows, k=6):
    print(f"\n=== {name} ===")
    for c in rows[:k]:
        print(f"  {c['init']}->{c['final']} d={c['delta']:+.2f} {c['status']:>7} wcR={c['wc_rebuttal']:>5} minW={c['min_wlen']:>4} {c['forum']} {c['title'][:64]}")

# Score-change data is unavailable publicly (ratings are pre-rebuttal snapshots in both dumps),
# so buckets anchor on the final DECISION. A/B are a matched pair: same initial band, opposite outcome.
def good(r):
    return r["n_rev"] >= 3 and r["min_wlen"] >= 800

A = sorted([r for r in joined if good(r) and r["status"] in ("Poster", "Oral", "Spotlight")
            and 4.5 <= r["init_mean"] <= 5.6],
           key=lambda r: -r["min_wlen"])
B = sorted([r for r in joined if good(r) and r["status"] == "Reject"
            and 4.5 <= r["init_mean"] <= 5.6],
           key=lambda r: -r["min_wlen"])
C = sorted([r for r in joined if good(r) and r["spread"] >= 6 and r["init"][0] <= 2
            and r["status"] in ("Poster", "Oral", "Spotlight")],
           key=lambda r: -r["min_wlen"])

show("A: borderline ACCEPT (init 4.5-5.6)", A)
show("B: borderline REJECT (init 4.5-5.6, matched band)", B)
show("C: extreme split, outlier overridden (min<=2, spread>=6, accepted)", C)

json.dump({"A": A[:10], "B": B[:10], "C": C[:10]}, open("pool/shortlist.json", "w"), indent=1)
print("\nshortlist -> pool/shortlist.json")
