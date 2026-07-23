#!/usr/bin/env python3
"""Build sealed blind workspaces for graph base-vs-skill pairwise judging.

4 pairs (2 models x 2 cases), 2 position-swapped rounds each. Round-1 A/B
assignment is a hash of the pair name (not human-chosen); round 2 swaps.
mapping.json lives in the pair dir, OUTSIDE the round dirs the judges read,
and stays sealed until tally.py runs after all verdicts are in.
"""
import hashlib
import json
import os
import pathlib

# Lives in tests/harness/judge_tools/ (versioned); workspaces stay under the
# gitignored runs/ tree.
HERE = pathlib.Path(__file__).resolve()
RUNS = HERE.parents[1] / "runs"  # tests/harness/runs
TESTS = HERE.parents[2]          # tests/
# JUDGE_WS env selects the workspace generation (default judge_ws; v2 = enriched
# per-run prefetch digests). Same deterministic pair-name blinding either way.
JW = RUNS / "graph-pilot-judge" / (os.environ.get("JUDGE_WS") or "judge_ws")

PAIRS = {
    "s5-q2":  ("graph-pilot-sonnet5/q2-diffusion-sampling", "q2-diffusion-sampling"),
    "s5-q5":  ("graph-pilot-sonnet5/q5-seed-lora", "q5-seed-lora"),
    "glm-q2": ("graph-pilot/q2-diffusion-sampling", "q2-diffusion-sampling"),
    "glm-q5": ("graph-pilot/q5-seed-lora", "q5-seed-lora"),
    # full-matrix extension (2026-07-21): the 6 remaining sonnet-5 cases
    "s5-q1":  ("graph-pilot-sonnet5/q1-efficient-attention", "q1-efficient-attention"),
    "s5-q3":  ("graph-pilot-sonnet5/q3-rag", "q3-rag"),
    "s5-q4":  ("graph-pilot-sonnet5/q4-test-time-reasoning", "q4-test-time-reasoning"),
    "s5-q6":  ("graph-pilot-sonnet5/q6-seed-flashattention", "q6-seed-flashattention"),
    "s5-q7":  ("graph-pilot-sonnet5/q7-hybrid-prefopt", "q7-hybrid-prefopt"),
    "s5-q8":  ("graph-pilot-sonnet5/q8-hybrid-vlm", "q8-hybrid-vlm"),
}


def digest(qid):
    papers = json.loads((TESTS / "paper-graph/cases" / qid / "input/papers.json").read_text())
    lines = ["The frozen paper pool. Paper (N) below is what \"(N)\" refers to in both reports.", ""]
    for i, p in enumerate(papers, 1):
        ab = (p.get("abstract") or "(no abstract in pool record)").strip()
        if len(ab) > 900:
            ab = ab[:900] + " …"
        lines.append(f"({i}) **{p.get('title')}** ({p.get('year')})")
        lines.append(ab)
        lines.append("")
    return "\n".join(lines)


# --- per-run prefetch provenance (B-fix, 2026-07-21) -------------------------
# The skill's runbook step 7 (prefetch_sections) fetches conclusion/limitations
# text of POOL papers; judges previously saw only the abstract digest and
# penalized excerpt-grounded claims as unsupported in >=4 rounds. The digest now
# carries each run's OWN fetched excerpts, attributed to the round's A/B label.

# generous: real _conclusion_section runs 0.7-2.8k chars and truncation can cut the
# exact sentence a claim rests on (seen with q7 PEBS's P-GenRM line at offset 1561);
# the cap only guards against pathological extractions.
EXCERPT_CAP = 4000


def _norm(t):
    return "".join(c for c in (t or "").lower() if c.isalnum())


def _pool_index(rec, pool):
    """Map a pipeline papers.json record back to its 1-based pool index (N)."""
    for i, p in enumerate(pool, 1):
        if rec.get("paperId") and rec.get("paperId") == p.get("paperId"):
            return i
    ax = rec.get("arxiv_id") or (rec.get("externalIds") or {}).get("ArXiv")
    for i, p in enumerate(pool, 1):
        pax = p.get("arxiv_id") or (p.get("externalIds") or {}).get("ArXiv")
        if ax and pax and ax == pax:
            return i
    tn = _norm(rec.get("title"))
    for i, p in enumerate(pool, 1):
        if tn and tn == _norm(p.get("title")):
            return i
    return None


def prefetch_excerpts(run_ws, pool):
    """{N: excerpt} this run's pipeline actually fetched — workdir papers.json
    records carrying a non-empty `_conclusion_section`. Empty dict when the run
    never ran prefetch (base arms, GLM runs, skipped-step runs)."""
    best = {}
    if not run_ws.exists():
        return best
    for pj in run_ws.glob("**/papers.json"):
        rel_parts = pj.relative_to(run_ws).parts
        if rel_parts[:1] == ("input",) or rel_parts[:1] == (".claude",):
            continue  # frozen pool copy / mounted skill source, not pipeline state
        try:
            recs = json.loads(pj.read_text())
        except Exception:
            continue
        if not isinstance(recs, list):
            continue
        found = {}
        for r in recs:
            if not isinstance(r, dict):
                continue
            sec = (r.get("_conclusion_section") or "").strip()
            if not sec:
                continue
            n = _pool_index(r, pool)
            if n:
                found[n] = sec
        if len(found) > len(best):
            best = found
    return best


def excerpt_section(ab, exc_by_arm):
    """Digest appendix for one round: excerpts attributed per A/B label, with
    the grounding rule stated. Empty string when neither side fetched anything."""
    blocks = []
    for label in ("A", "B"):
        exc = exc_by_arm.get(ab[label]) or {}
        if not exc:
            continue
        blocks += [f"### Excerpts fetched by Report {label}'s build", ""]
        for n in sorted(exc):
            t = " ".join(exc[n].split())
            if len(t) > EXCERPT_CAP:
                t = t[:EXCERPT_CAP] + " …"
            blocks.append(f"({n}) {t}")
            blocks.append("")
    if not blocks:
        return ""
    head = [
        "", "---", "",
        "## Fetched full-text excerpts (per-report provenance)", "",
        "While being built, a report's pipeline may have fetched conclusion/limitations",
        "excerpts of POOL papers — verbatim text from the papers themselves, beyond the",
        "abstracts above. The blocks below show exactly what each report's build fetched.",
        "Judging rule: for a report listed below, claims traceable to its excerpts COUNT",
        "AS GROUNDED. A report with no block below never saw this material — do not",
        "penalize it for not using it, and do not treat the excerpts as pool knowledge",
        "it should have had.", "",
    ]
    return "\n".join(head + blocks)


def main():
    for pair, (rel, qid) in PAIRS.items():
        pdir = JW / pair
        if pdir.exists():
            print(f"{pair}: already built, skipped (existing verdicts preserved)")
            continue
        arms = {"base": RUNS / f"{rel}-base/ws/output/report.md",
                "skill": RUNS / f"{rel}-skill/ws/output/report.md"}
        for a, p in arms.items():
            if not p.exists():
                raise SystemExit(f"missing report: {p}")
        # deterministic, not-human-chosen round-1 assignment
        flip = int(hashlib.md5(pair.encode()).hexdigest(), 16) % 2
        r1 = {"A": "skill" if flip else "base", "B": "base" if flip else "skill"}
        r2 = {"A": r1["B"], "B": r1["A"]}
        mapping = {"bs_round1": r1, "bs_round2": r2}
        dg = digest(qid)
        pool = json.loads((TESTS / "paper-graph/cases" / qid / "input/papers.json").read_text())
        exc_by_arm = {a: prefetch_excerpts(RUNS / f"{rel}-{a}/ws", pool)
                      for a in ("base", "skill")}
        query = (TESTS / "paper-graph/cases" / qid / "input/query.txt").read_text()
        for rnd, ab in mapping.items():
            rd = pdir / rnd
            rd.mkdir(parents=True)
            (rd / "query.txt").write_text(query)
            # digest is per-round: excerpt attribution follows this round's A/B mapping
            (rd / "papers_digest.md").write_text(dg + excerpt_section(ab, exc_by_arm))
            (rd / "report_A.md").write_text(arms[ab["A"]].read_text())
            (rd / "report_B.md").write_text(arms[ab["B"]].read_text())
        (pdir / "mapping.json").write_text(json.dumps(mapping, indent=1))
        print(f"{pair}: 2 rounds built (mapping sealed)")


if __name__ == "__main__":
    main()
