#!/usr/bin/env python3
"""Aggregate metrics.json files from a run_matrix output dir into a compact table."""
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
rows = []
for mp in sorted(root.glob("*/metrics.json")):
    try:
        m = json.loads(mp.read_text())
    except Exception:
        continue
    meta = m.get("run_meta", {})
    if "gt_defect_n" in m:  # paper-review run
        f = m.get("findings", {}) or {}
        jm = {}
        jmp = mp.parent / "judge_review_match.json"
        if jmp.exists():
            jm = json.loads(jmp.read_text())
        jf = {}
        jfp = mp.parent / "judge_review_fp.json"
        if jfp.exists():
            jf = json.loads(jfp.read_text())
        rows.append({
            "run": mp.parent.name,
            "arm": meta.get("arm", "?"),
            "ok": "Y" if m.get("files_ok") and m.get("findings_parse") else "N",
            "champ": "-",
            "prioP": jm.get("recall_strict"),
            "prioR": jm.get("recall_lenient"),
            "cons": f"{f.get('major','-')}M/{f.get('minor','-')}m",
            "cov": jf.get("fp_rate_major"),
            "hi%": None,
            "fab": jf.get("counts", {}).get("fabricated"),
            "skill": "Y" if meta.get("skill_invoked") else "n",
            "sec": meta.get("seconds"),
        })
        continue
    if "edges_summary" in m:  # paper-graph run
        es, st = m["edges_summary"], m.get("structure", {})
        ar, ger = m.get("anchor_recall", {}), m.get("gt_edge_recall", {})
        ext = m.get("external_papers", {})
        # achieved/frozen-pool-ceiling when the checker provides ceilings
        # (old metrics.json fall back to the raw ratio)
        if "ceiling" in ar:
            prio_p = f"{len(ar.get('hit', []))}/{ar['ceiling']}"
            prio_p_ratio = (len(ar.get("hit", [])) / ar["ceiling"]) if ar["ceiling"] else None
        else:
            prio_p, prio_p_ratio = ar.get("ratio"), ar.get("ratio")
        if "ceiling" in ger:
            prio_r = f"{len(ger.get('hit', []))}/{ger['ceiling']}"
            prio_r_ratio = (len(ger.get("hit", [])) / ger["ceiling"]) if ger["ceiling"] else None
        else:
            prio_r, prio_r_ratio = ger.get("ratio"), ger.get("ratio")
        uv = es.get("cited_unverifiable", 0)
        rows.append({
            "run": mp.parent.name,
            "arm": meta.get("arm", "?"),
            "ok": "Y" if st.get("structure_ok") else "N",
            "champ": "-",
            "prioP": prio_p,
            "prioR": prio_r,
            "_prioP": prio_p_ratio,
            "_prioR": prio_r_ratio,
            "cons": f"{es.get('cited_verified',0)}/{es.get('n',0)}cite"
                    + (f"+{uv}uv" if uv else ""),
            "cov": es.get("chrono_violations"),
            "hi%": es.get("noise_noise_not_found"),
            "fab": len(m.get("indices", {}).get("hallucinated_in_graphs", [])),
            "ext": f"{ext.get('n',0)}:{ext.get('not_found',0)}!" if ext.get("n") else "-",
            "skill": "Y" if meta.get("skill_invoked") else "n",
            "sec": meta.get("seconds"),
        })
        continue
    pr = m.get("priority", {})
    cons = m.get("consensus", {})
    cov = m.get("coverage", {})
    bud = m.get("budget", {})
    rows.append({
        "run": mp.parent.name,
        "arm": meta.get("arm", "?"),
        "ok": "Y" if m.get("files_ok") else "N",
        "champ": {True: "Y", False: "N"}.get(m.get("champion_hit"), "-"),
        "prioP": pr.get("precision"),
        "prioR": pr.get("recall"),
        "cons": f"{cons.get('detected','-')}/{cons.get('total','-')}" if cons else "-",
        "cov": cov.get("ratio"),
        "hi%": bud.get("high_share"),
        "fab": m.get("fabrication_candidate_n"),
        "skill": "Y" if meta.get("skill_invoked") else "n",
        "sec": meta.get("seconds"),
    })

if not rows:
    print("no metrics found under", root)
    sys.exit(1)

cols = ["run", "ok", "champ", "prioP", "prioR", "cons", "cov", "hi%", "fab", "ext", "skill", "sec"]
if all(r.get("ext", "-") in ("-", "") for r in rows):
    cols.remove("ext")  # only graph runs carry the pool-external column
widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in cols}
print("  ".join(c.ljust(widths[c]) for c in cols))
for r in rows:
    print("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))

# arm-level means for numeric metrics
def mean(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    return round(sum(vals) / len(vals), 3) if vals else None

print("\narm means:")
for arm in ("base", "skill"):
    sub = [r for r in rows if r["arm"] == arm]
    if sub:
        # graph rows carry hidden vs-ceiling ratios (_prioP/_prioR); cases whose
        # frozen-pool ceiling is 0 are excluded from the mean rather than read as 0
        print(f"  {arm:>5}: prioP={mean(r.get('_prioP', r['prioP']) for r in sub)} "
              f"prioR={mean(r.get('_prioR', r['prioR']) for r in sub)} "
              f"cov={mean(r['cov'] for r in sub)} hi%={mean(r['hi%'] for r in sub)} "
              f"fab={mean(r['fab'] for r in sub)}")
