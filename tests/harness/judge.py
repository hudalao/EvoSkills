#!/usr/bin/env python3
"""LLM-judge pass for rebuttal-eval runs. Backend: `claude -p` (uses your local CLI auth).

Modes:
  fab      — adjudicate fabrication candidates from metrics.json
             judge.py fab --case <case_dir> --run <run_dir> [--model M]
  quality  — grade responses to GT score-driving (high) concerns
             judge.py quality --case <case_dir> --run <run_dir> [--model M]
  pairwise — blind A/B between two runs' rebuttals, position-swapped x2
             judge.py pairwise --case <case_dir> --run-a <dir> --run-b <dir> [--model M]

Writes judge_<mode>.json into the run dir (pairwise: into run-a's dir).
Every quote in verdicts is machine-verified against the named file; failed quotes
flag the verdict with "quote_verified": false — treat those as void.
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HARNESS = pathlib.Path(__file__).parent
PROMPTS = HARNESS / "judge_prompts"


def call_claude(prompt, cwd, model, timeout=600):
    cmd = ["claude", "-p", prompt, "--model", model,
           "--allowedTools", "Read,Grep,Glob", "--output-format", "json"]
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"claude exited {r.returncode}: {r.stderr[-400:]}")
    payload = json.loads(r.stdout)
    text = payload.get("result", "")
    text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.M).strip()
    return json.loads(text), payload.get("total_cost_usd")


def verify_quotes(items, files):
    """items: list of dicts with evidence/response quote fields; files: {tag: text}."""
    for it in items:
        q = it.get("evidence_quote") or it.get("response_quote") or ""
        tag = it.get("evidence_file", "rebuttal")
        hay = files.get(tag, "") if isinstance(files, dict) else files
        it["quote_verified"] = bool(q) and (q in hay)
    return items


def mode_fab(args):
    run = pathlib.Path(args.run)
    metrics = json.loads((run / "metrics.json").read_text())
    cands = metrics.get("fabrication_candidates", [])
    if not cands:
        print(json.dumps({"mode": "fab", "n": 0, "verdicts": []}, indent=2))
        return
    prompt = (PROMPTS / "fab.md").read_text().replace(
        "{candidates}", json.dumps(cands, indent=1, ensure_ascii=False))
    verdicts, cost = call_claude(prompt, run / "ws", args.model)
    files = {
        "paper": (pathlib.Path(args.case) / "input/paper.md").read_text(),
        "rebuttal": (run / "ws/output/rebuttal.md").read_text(),
    }
    verify_quotes(verdicts, files)
    out = {"mode": "fab", "model": args.model, "cost_usd": cost,
           "n": len(verdicts), "verdicts": verdicts,
           "confirmed_fabricated": [v["num"] for v in verdicts
                                    if v.get("verdict") == "fabricated" and v.get("quote_verified")]}
    (run / "judge_fab.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


def mode_quality(args):
    case = pathlib.Path(args.case)
    run = pathlib.Path(args.run)
    gt = json.loads((case / "gt/score_driving.json").read_text())
    reviews = json.loads((case / "input/reviews.json").read_text())
    txt = {c["id"]: c["text"] for r in reviews["reviewers"] for c in r["comments"]}
    concerns = [{"id": i, "comment": txt[i]} for i in gt["high"]]
    prompt = (PROMPTS / "quality.md").read_text().replace(
        "{concerns}", json.dumps(concerns, indent=1, ensure_ascii=False))
    grades, cost = call_claude(prompt, run / "ws", args.model)
    verify_quotes(grades, (run / "ws/output/rebuttal.md").read_text())
    ok = [g for g in grades if g.get("quote_verified")]
    dist = {k: sum(1 for g in ok if g.get("grade") == k) for k in ("resolved", "partial", "evaded")}
    out = {"mode": "quality", "model": args.model, "cost_usd": cost,
           "n_graded": len(grades), "n_quote_verified": len(ok),
           "distribution": dist, "grades": grades}
    (run / "judge_quality.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


def mode_pairwise(args):
    case = pathlib.Path(args.case)
    ra, rb = pathlib.Path(args.run_a), pathlib.Path(args.run_b)
    prompt = (PROMPTS / "pairwise.md").read_text()
    results = []
    for swap in (False, True):
        first, second = (ra, rb) if not swap else (rb, ra)
        with tempfile.TemporaryDirectory() as td:
            ws = pathlib.Path(td)
            shutil.copytree(case / "input", ws / "input")
            shutil.copy(first / "ws/output/rebuttal.md", ws / "rebuttal_A.md")
            shutil.copy(second / "ws/output/rebuttal.md", ws / "rebuttal_B.md")
            verdict, cost = call_claude(prompt, ws, args.model)
        # map A/B back to run identities
        win = verdict.get("winner")
        ident = {"A": "run_a" if not swap else "run_b",
                 "B": "run_b" if not swap else "run_a"}.get(win, "tie")
        results.append({"swap": swap, "raw": verdict, "winner_run": ident, "cost_usd": cost})
    w1, w2 = results[0]["winner_run"], results[1]["winner_run"]
    final = w1 if w1 == w2 else "tie"
    out = {"mode": "pairwise", "model": args.model,
           "run_a": str(ra), "run_b": str(rb),
           "final": final, "consistent": w1 == w2, "rounds": results}
    (ra / "judge_pairwise.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


def mode_review_match(args):
    """Match planted defects (gt/defects.json) against a self-review's findings."""
    case = pathlib.Path(args.case)
    run = pathlib.Path(args.run)
    gt = json.loads((case / "gt/defects.json").read_text())
    defects = [{k: d[k] for k in ("uid", "type", "severity", "location_anchor", "detection_criteria")}
               for d in gt.get("defects", [])]
    if not defects:
        print(json.dumps({"mode": "review_match", "n": 0, "note": "clean control (V0) — nothing to match"}, indent=2))
        return
    prompt = (PROMPTS / "review_match.md").read_text().replace(
        "{defects}", json.dumps(defects, indent=1, ensure_ascii=False))
    if args.dry_run:
        print(prompt)
        return
    if getattr(args, "from_verdicts", None):
        verdicts, cost = json.loads(pathlib.Path(args.from_verdicts).read_text()), None
    else:
        verdicts, cost = call_claude(prompt, run / "ws", args.model)
    files_txt = ((run / "ws/output/findings.json").read_text(errors="replace") + "\n" +
                 (run / "ws/output/self_review.md").read_text(errors="replace"))
    for v in verdicts:
        q = v.get("evidence_quote") or ""
        v["quote_verified"] = (q in files_txt) if v.get("verdict") in ("HIT", "PARTIAL") else True
        if v.get("verdict") in ("HIT", "PARTIAL") and not v["quote_verified"]:
            v["verdict_voided_to"] = "MISS"
    def eff(v):
        return v.get("verdict_voided_to", v.get("verdict"))
    by_sev = {}
    for d in gt["defects"]:
        v = next((x for x in verdicts if x.get("uid") == d["uid"]), None)
        sev = d["severity"]
        by_sev.setdefault(sev, {"HIT": 0, "PARTIAL": 0, "MISS": 0, "n": 0})
        by_sev[sev]["n"] += 1
        by_sev[sev][eff(v) if v and eff(v) in ("HIT", "PARTIAL", "MISS") else "MISS"] += 1
    hits = sum(s["HIT"] for s in by_sev.values())
    out = {"mode": "review_match", "model": args.model, "cost_usd": cost,
           "n_defects": len(defects), "hits": hits,
           "recall_strict": round(hits / len(defects), 3),
           "recall_lenient": round((hits + sum(s["PARTIAL"] for s in by_sev.values())) / len(defects), 3),
           "by_severity": by_sev, "verdicts": verdicts}
    (run / "judge_review_match.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


def mode_review_fp(args):
    """Classify unmatched findings: legitimate / fabricated / subjective (FP audit)."""
    run = pathlib.Path(args.run)
    findings = json.loads(re.sub(r"^```(json)?|```$", "",
                                 (run / "ws/output/findings.json").read_text().strip(), flags=re.M))
    matched = set()
    rm = run / "judge_review_match.json"
    if rm.exists():
        for v in json.loads(rm.read_text()).get("verdicts", []):
            eff = v.get("verdict_voided_to", v.get("verdict"))
            if eff in ("HIT", "PARTIAL") and v.get("finding_id") not in (None, "memo"):
                matched.add(v["finding_id"])
    audit = [f for f in findings if isinstance(f, dict) and f.get("id") not in matched]
    if not audit:
        out = {"mode": "review_fp", "n_audited": 0, "note": "no unmatched findings"}
        (run / "judge_review_fp.json").write_text(json.dumps(out, indent=2))
        print(json.dumps(out, indent=2))
        return
    prompt = (PROMPTS / "review_fp.md").read_text().replace(
        "{findings}", json.dumps(audit, indent=1, ensure_ascii=False))
    if getattr(args, "dry_run", False):
        print(prompt)
        return
    if getattr(args, "from_verdicts", None):
        verdicts, cost = json.loads(pathlib.Path(args.from_verdicts).read_text()), None
    else:
        verdicts, cost = call_claude(prompt, run / "ws", args.model)
    paper = (run / "ws/input/main_flat.tex").read_text(errors="replace")
    sev = {f.get("id"): f.get("severity") for f in audit}
    for v in verdicts:
        q = v.get("evidence_quote") or ""
        if v.get("verdict") == "fabricated":
            v["quote_verified"] = q in paper
            if not v["quote_verified"]:
                v["verdict_voided_to"] = "subjective"
        else:
            v["quote_verified"] = (q == "ABSENCE") or (q in paper)
        v["severity"] = sev.get(v.get("id"))
    def eff(v):
        return v.get("verdict_voided_to", v.get("verdict"))
    counts = {k: sum(1 for v in verdicts if eff(v) == k) for k in ("legitimate", "fabricated", "subjective")}
    majors = [v for v in verdicts if v.get("severity") == "major"]
    out = {"mode": "review_fp", "model": args.model, "cost_usd": cost,
           "n_audited": len(audit), "counts": counts,
           "fabricated_major_n": sum(1 for v in majors if eff(v) == "fabricated"),
           "major_audited_n": len(majors),
           "fp_rate_major": round(sum(1 for v in majors if eff(v) == "fabricated") / len(majors), 3) if majors else None,
           "verdicts": verdicts}
    (run / "judge_review_fp.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


def _graph_gt(qid):
    gt_dir = HARNESS / "../paper-graph/gt"
    q = next(x for x in json.loads((gt_dir / "queries.json").read_text())["queries"] if x["qid"] == qid)
    return q


def mode_graph_taxonomy(args):
    case = pathlib.Path(args.case)
    run = pathlib.Path(args.run)
    q = _graph_gt(case.name)
    md = (run / "ws/output/report.md").read_text(errors="replace")
    m = re.search(r"## High-Level Taxonomy.*?(?=\n## )", md, re.S)
    section = m.group(0) if m else "(taxonomy section not found)"
    papers = json.loads((case / "input/papers.json").read_text())
    brief = "\n".join(f"({i+1}) {p.get('title')} ({p.get('year')})" for i, p in enumerate(papers))
    prompt = (PROMPTS / "graph_taxonomy.md").read_text()
    for k, v in (("{query}", q["query"]), ("{taxonomy_hint}", q.get("taxonomy_hint", "")),
                 ("{papers_brief}", brief), ("{taxonomy_section}", section[:6000])):
        prompt = prompt.replace(k, v)
    verdict, cost = call_claude(prompt, run / "ws", args.model)
    out = {"mode": "graph_taxonomy", "model": args.model, "cost_usd": cost,
           "scores": {k: verdict.get(k, {}).get("score") for k in
                      ("branch_coverage", "grouping_coherence", "granularity")},
           "detail": verdict,
           "note": "soft metric — anchored rubric, no mechanical quote verification"}
    (run / "judge_graph_taxonomy.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


def mode_graph_edges(args):
    case = pathlib.Path(args.case)
    run = pathlib.Path(args.run)
    metrics = json.loads((run / "metrics.json").read_text())
    edges = [e for e in metrics.get("edges", []) if e.get("src_arxiv") and e.get("dst_arxiv")]
    if not edges:
        out = {"mode": "graph_edges", "n": 0, "note": "no resolvable edges in report"}
        (run / "judge_graph_edges.json").write_text(json.dumps(out, indent=2))
        print(json.dumps(out, indent=2))
        return
    edges = sorted(edges, key=lambda e: (e["src_n"], e["dst_n"]))
    k = max(1, len(edges) // args.max_edges + (1 if len(edges) % args.max_edges else 0))
    sample = edges[::k][:args.max_edges]
    papers = json.loads((case / "input/papers.json").read_text())
    def mat(n):
        p = papers[n - 1]
        return {"title": p.get("title"), "abstract": (p.get("abstract") or "(no abstract)")[:1200]}
    payload = [{"edge": f"P{e['src_n']}->P{e['dst_n']}",
                "claimed_gap": e.get("gap", ""),
                "src": mat(e["src_n"]), "dst": mat(e["dst_n"])} for e in sample]
    prompt = (PROMPTS / "graph_edges.md").read_text().replace(
        "{edges}", json.dumps(payload, indent=1, ensure_ascii=False))
    verdicts, cost = call_claude(prompt, run / "ws", args.model)
    bytag = {p["edge"]: p for p in payload}
    for v in verdicts:
        p = bytag.get(v.get("edge"))
        q = v.get("killer_quote") or ""
        hay = ""
        if p:
            hay = p["src"]["abstract"] if v.get("quote_from") == "src" else p["dst"]["abstract"]
        v["quote_verified"] = bool(q) and q in hay
        if not v["quote_verified"] and v.get("answer") in ("holds", "refuted"):
            v["answer_voided_to"] = "undecidable"
    def eff(v):
        return v.get("answer_voided_to", v.get("answer"))
    counts = {k2: sum(1 for v in verdicts if eff(v) == k2) for k2 in ("holds", "refuted", "undecidable")}
    decided = counts["holds"] + counts["refuted"]
    out = {"mode": "graph_edges", "model": args.model, "cost_usd": cost,
           "n_sampled": len(sample), "n_total_edges": len(edges), "counts": counts,
           "refute_rate_decided": round(counts["refuted"] / decided, 3) if decided else None,
           "verdicts": verdicts}
    (run / "judge_graph_edges.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    for name in ("fab", "quality", "review-match", "review-fp", "graph-taxonomy", "graph-edges"):
        p = sub.add_parser(name)
        p.add_argument("--case", required=True)
        p.add_argument("--run", required=True)
        p.add_argument("--model", default="claude-opus-4-8")
        if name in ("review-match", "review-fp"):
            p.add_argument("--dry-run", action="store_true")
            p.add_argument("--from-verdicts", default=None)
        if name == "graph-edges":
            p.add_argument("--max-edges", type=int, default=10)
    p = sub.add_parser("pairwise")
    p.add_argument("--case", required=True)
    p.add_argument("--run-a", required=True)
    p.add_argument("--run-b", required=True)
    p.add_argument("--model", default="claude-opus-4-8")
    args = ap.parse_args()
    {"fab": mode_fab, "quality": mode_quality, "pairwise": mode_pairwise,
     "review-match": mode_review_match, "review-fp": mode_review_fp,
     "graph-taxonomy": mode_graph_taxonomy, "graph-edges": mode_graph_edges}[args.mode](args)


if __name__ == "__main__":
    main()
