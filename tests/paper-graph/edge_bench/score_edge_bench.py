#!/usr/bin/env python3
"""Score an audit_edge micro-benchmark run. usage: score_edge_bench.py <verdicts_dir>"""
import json
import pathlib
import sys
from collections import Counter

HERE = pathlib.Path(__file__).parent
out = pathlib.Path(sys.argv[1])
pairs = {p["pid"]: p for p in json.loads((HERE / "pairs.json").read_text())["pairs"]}

rows = []
for pid, pr in sorted(pairs.items()):
    vp = out / f"{pid}.json"
    verdict = json.loads(vp.read_text())["verdict"] if vp.exists() else "MISSING"
    ok = (verdict != "REJECT") if pr["label"] == "true" else (verdict == "REJECT")
    rows.append({**pr, "verdict": verdict, "ok": ok if verdict != "MISSING" else None})

done = [r for r in rows if r["verdict"] != "MISSING"]
t = [r for r in done if r["label"] == "true"]
f = [r for r in done if r["label"] == "false"]
print(f"scored {len(done)}/40  (true={len(t)}, false={len(f)})")
if t:
    print(f"true-pair survival (verdict != REJECT): {sum(r['ok'] for r in t)}/{len(t)}")
    print("  verdict dist:", dict(Counter(r["verdict"] for r in t)))
if f:
    print(f"false-pair rejection (verdict == REJECT): {sum(r['ok'] for r in f)}/{len(f)}")
    print("  verdict dist:", dict(Counter(r["verdict"] for r in f)))
    by_cat = {}
    for r in f:
        by_cat.setdefault(r.get("category", "?"), []).append(r["ok"])
    for c, oks in sorted(by_cat.items()):
        print(f"    {c}: {sum(oks)}/{len(oks)}")
miss = [r for r in done if not r["ok"]]
if miss:
    print("\nmisclassified:")
    for r in miss:
        print(f"  {r['pid']} [{r['label']}] {r['src']}->{r['dst']} verdict={r['verdict']}"
              + (f" ({r.get('category', '')})" if r["label"] == "false" else ""))
(out / "score_summary.json").write_text(json.dumps(rows, indent=1))
