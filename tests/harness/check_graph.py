#!/usr/bin/env python3
"""Deterministic checker for one paper-graph report.

usage: check_graph.py --report <report.md> --qid <qid>
         [--gt-dir tests/paper-graph/gt] [--fixture <papers.json>]
         [--mmdc auto|off] [--no-s2]

Parses the report against the skill's own emission grammar
(outline: `S{m}_{n} --- P{c}_{i}["(N)"]`; detail: `X_P{src} -->|Gap...| X_P{dst}`,
inferred edges dotted; appendix entries `**({i}) [title](url)** — year`).
Citation consistency uses the fallback chain S2-by-ID -> title-match -> unverifiable
(never `fail` on resolver gaps alone).
"""
import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request


def norm_title(t):
    return re.sub(r"[^a-z0-9 ]", "", (t or "").lower().replace("-", " "))


def arxiv_of(paper):
    ex = paper.get("externalIds") or {}
    a = ex.get("ArXiv") or paper.get("arxivId") or paper.get("arxiv_id")
    if not a:
        m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", paper.get("url") or "")
        a = m.group(1) if m else None
    return re.sub(r"v\d+$", "", a) if a else None


def titles_match(a, b):
    """Guarded fuzzy title equality: containment only when lengths are comparable."""
    na, nb = norm_title(a), norm_title(b)
    if not na or not nb or min(len(na), len(nb)) < 16:
        return False
    if na == nb:
        return True
    shorter, longer = (na, nb) if len(na) <= len(nb) else (nb, na)
    return shorter in longer and len(shorter) / len(longer) >= 0.75


def mermaid_blocks(md):
    return re.findall(r"```mermaid\n(.*?)\n```", md, re.S)


def lint_block(b):
    issues = []
    first = next((ln for ln in b.splitlines() if ln.strip()), "")
    if not re.match(r"%%\{init|graph |flowchart ", first.strip()):
        issues.append("missing graph/init header")
    if b.count('"') % 2:
        issues.append("odd quote count")
    for br in "[]()":
        pass
    if b.count("[[") != b.count("]]"):
        issues.append("unbalanced [[ ]]")
    return issues


def mmdc_compile(block, timeout=90):
    mmdc = shutil.which("mmdc")
    cmd = [mmdc] if mmdc else ["npx", "-y", "@mermaid-js/mermaid-cli"]
    with tempfile.TemporaryDirectory() as td:
        src = pathlib.Path(td) / "b.mmd"
        out = pathlib.Path(td) / "b.svg"
        src.write_text(block)
        try:
            r = subprocess.run(cmd + ["-i", str(src), "-o", str(out), "--quiet"],
                               capture_output=True, text=True, timeout=timeout,
                               env={**os.environ, "PATH": os.environ.get("PATH", "") +
                                    ":" + os.path.expanduser("~/.nvm/versions/node/v24.18.0/bin")})
            return ("ok", "") if r.returncode == 0 and out.exists() else ("fail", r.stderr[-300:])
        except FileNotFoundError:
            return ("unavailable", "mmdc/npx not found")
        except subprocess.TimeoutExpired:
            return ("timeout", "")


def s2_refs(aid, cache, cache_path, key):
    if aid in cache:
        return cache[aid]
    if not key:
        return "NO_S2"
    url = (f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{aid}/references"
           f"?fields=title,externalIds&limit=1000")
    req = urllib.request.Request(url, headers={"x-api-key": key})
    for attempt in range(3):
        try:
            data = json.loads(urllib.request.urlopen(req, timeout=30).read())
            out = [[((r.get("citedPaper") or {}).get("externalIds") or {}).get("ArXiv"),
                    (r.get("citedPaper") or {}).get("title")] for r in data.get("data", [])]
            cache[aid] = out
            if cache_path:
                cache_path.write_text(json.dumps(cache))
            time.sleep(1.1)
            return out
        except urllib.error.HTTPError as e:
            if e.code == 404:
                cache[aid] = None
                if cache_path:
                    cache_path.write_text(json.dumps(cache))
                return None
            time.sleep(2 + 2 * attempt)
        except Exception:
            time.sleep(2 + 2 * attempt)
    return "FETCH_FAILED"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--qid", required=True)
    ap.add_argument("--gt-dir", default=str(pathlib.Path(__file__).parent / "../paper-graph/gt"))
    ap.add_argument("--fixture", default=None)
    ap.add_argument("--mmdc", choices=["auto", "off"], default="auto")
    ap.add_argument("--no-s2", action="store_true")
    args = ap.parse_args()

    gt_dir = pathlib.Path(args.gt_dir).resolve()
    gt = next(q for q in json.loads((gt_dir / "queries.json").read_text())["queries"]
              if q["qid"] == args.qid)
    fixture_p = pathlib.Path(args.fixture) if args.fixture else \
        gt_dir.parent / "fixtures" / args.qid / "papers.json"
    papers = json.loads(fixture_p.read_text())
    idx2arxiv = {i + 1: arxiv_of(p) for i, p in enumerate(papers)}
    idx2title = {i + 1: p.get("title") for i, p in enumerate(papers)}
    idx2year = {i + 1: p.get("year") for i, p in enumerate(papers)}

    md = pathlib.Path(args.report).read_text(errors="replace")
    out = {"qid": args.qid, "report": args.report}

    # --- structure ---
    blocks = mermaid_blocks(md)
    has_tax = "## High-Level Taxonomy" in md
    outline = blocks[0] if (has_tax and blocks) else ""
    n_challenges = len(set(re.findall(r"\bC(\d+)\b", outline)))
    n_solutions = len(set(re.findall(r"\bS(\d+)_(\d+)\b", outline)))
    out["structure"] = {
        "mermaid_blocks": len(blocks),
        "has_taxonomy": has_tax,
        "n_challenges": n_challenges,
        "n_solutions": n_solutions,
        "n_solution_sections": len(re.findall(r"^### Challenge \d+ · Solution", md, re.M)),
        "has_core_appendix": "## Paper Appendix (Core lineage)" in md,
        "structure_ok": has_tax and n_challenges >= 2 and n_solutions >= n_challenges
                        and "## Paper Appendix (Core lineage)" in md,
    }

    # --- mermaid validity ---
    mm = []
    for i, b in enumerate(blocks):
        lint = lint_block(b)
        entry = {"block": i, "lint_issues": lint}
        if args.mmdc == "auto":
            status, err = mmdc_compile(b)
            entry["compile"] = status
            if err:
                entry["compile_err"] = err
        mm.append(entry)
    out["mermaid"] = {
        "lint_clean": sum(1 for e in mm if not e["lint_issues"]),
        "compiled_ok": sum(1 for e in mm if e.get("compile") == "ok"),
        "compile_mode": args.mmdc if args.mmdc == "off" or
                        all(e.get("compile") != "unavailable" for e in mm) else "lint-only",
        "blocks": mm,
    }

    # --- numbers / hallucination ---
    appendix_nums = {int(n) for n in re.findall(r"^\*\*\((\d+)\) ", md, re.M)}
    graph_nums = {int(n) for n in re.findall(r'P\d+_\d+\["\((\d+)\)"\]', md)}
    graph_nums |= {int(n) for n in re.findall(r"_P(\d+)\(", md)}
    out["indices"] = {
        "appendix": sorted(appendix_nums),
        "in_graphs": sorted(graph_nums),
        "hallucinated_in_graphs": sorted(graph_nums - set(idx2arxiv)),
        "graph_not_in_appendix": sorted(graph_nums - appendix_nums),
    }

    # --- anchor recall (report level) ---
    present_ids = {idx2arxiv[i] for i in appendix_nums if idx2arxiv.get(i)}
    present_titles = [norm_title(idx2title[i]) for i in appendix_nums if i in idx2title]
    anchors_hit, anchors_miss = [], []
    titles_gt = json.loads((gt_dir / "id_titles_s2.json").read_text())
    titles_gt.setdefault("2202.00512", "Progressive Distillation for Fast Sampling of Diffusion Models")
    for a in gt["anchors"]:
        gt_title = titles_gt.get(a["arxiv"], "")
        hit = a["arxiv"] in present_ids or any(
            titles_match(gt_title, idx2title[i]) for i in appendix_nums if i in idx2title)
        (anchors_hit if hit else anchors_miss).append(a["arxiv"])
    out["anchor_recall"] = {"hit": anchors_hit, "miss": anchors_miss,
                            "ratio": round(len(anchors_hit) / len(gt["anchors"]), 3)}

    # --- edges ---
    raw_edges = re.findall(r"_P(\d+)\s*(-->|-\.->)\s*\|Gap([^|]*)\|\s*\w+_P(\d+)", md)
    edges = []
    for src_n, arrow, gap, dst_n in raw_edges:
        s, d = int(src_n), int(dst_n)
        e = {"src_n": s, "dst_n": d,
             "src_arxiv": idx2arxiv.get(s), "dst_arxiv": idx2arxiv.get(d),
             "gap": re.sub(r"^\s*(?:#40;inferred#41;|\(inferred\))?\s*:?\s*", "", gap).strip()[:400],
             "inferred": arrow == "-.->" or "inferred" in gap.lower()}
        # chronology: arXiv YYMM if both new-style, else fixture year
        sa, da = e["src_arxiv"], e["dst_arxiv"]
        if sa and da and re.match(r"^\d{4}\.", sa) and re.match(r"^\d{4}\.", da):
            e["chrono_ok"] = da[:4] >= sa[:4]
        else:
            sy, dy = idx2year.get(s), idx2year.get(d)
            e["chrono_ok"] = (dy >= sy) if (sy and dy) else None
        edges.append(e)

    # --- citation consistency (S2-ID -> title -> unverifiable) ---
    cache_path = gt_dir / "refs_cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    key = None if args.no_s2 else os.environ.get("S2_API_KEY")
    for e in edges:
        sa, da = e["src_arxiv"], e["dst_arxiv"]
        if not (sa and da):
            e["cited"] = "unverifiable(no-id)"
            continue
        refs = s2_refs(da, cache, cache_path, key)
        if refs in (None, "FETCH_FAILED", "NO_S2"):
            e["cited"] = f"unverifiable({refs})"
            continue
        ids = {r[0] for r in refs if r[0]}
        if sa in ids:
            e["cited"] = "verified"
        else:
            tn = norm_title(idx2title.get(e["src_n"], ""))
            hit = tn and any(len(norm_title(r[1])) > 15 and
                             (tn in norm_title(r[1]) or norm_title(r[1]) in tn)
                             for r in refs if r[1])
            e["cited"] = "verified-by-title" if hit else "not-found"

    # --- GT edge recall ---
    report_pairs = {(e["src_arxiv"], e["dst_arxiv"]) for e in edges
                    if e["src_arxiv"] and e["dst_arxiv"]}
    gt_hit = [f"{s}->{d}" for s, d in gt["edges"] if (s, d) in report_pairs]
    out["gt_edge_recall"] = {"hit": gt_hit,
                              "ratio": round(len(gt_hit) / len(gt["edges"]), 3),
                              "total_gt": len(gt["edges"])}

    # --- fabrication pressure ---
    anchor_ids = {a["arxiv"] for a in gt["anchors"]}
    noise_edges = [e for e in edges
                   if (e["src_arxiv"] not in anchor_ids) and (e["dst_arxiv"] not in anchor_ids)]
    unciteable = [e for e in edges if e["cited"] == "not-found"]
    out["edges_summary"] = {
        "n": len(edges),
        "inferred_n": sum(1 for e in edges if e["inferred"]),
        "cited_verified": sum(1 for e in edges if e["cited"].startswith("verified")),
        "cited_not_found": len(unciteable),
        "cited_unverifiable": sum(1 for e in edges if e["cited"].startswith("unverifiable")),
        "chrono_violations": sum(1 for e in edges if e["chrono_ok"] is False),
        "noise_noise_edges": len(noise_edges),
        "noise_noise_not_found": sum(1 for e in noise_edges if e["cited"] == "not-found"),
    }
    out["edges"] = edges

    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
