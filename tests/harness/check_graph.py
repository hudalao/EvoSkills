#!/usr/bin/env python3
"""Deterministic checker for one paper-graph report.

usage: check_graph.py --report <report.md> --qid <qid>
         [--gt-dir tests/paper-graph/gt] [--fixture <papers.json>]
         [--mmdc auto|off] [--no-s2]

Parses the report against the skill's own emission grammar
(outline: `S{m}_{n} --- P{c}_{i}["(N)"]`; detail: `X_P{src} -->|Gap...| X_P{dst}`,
inferred edges dotted; appendix entries `**({i}) [title](url)** — year`).

Citation consistency: refs_cache -> live S2 by arXiv id or S2 paperId (keyless
requests allowed; x-api-key attached when S2_API_KEY is set) -> title match
inside the reference list -> unverifiable (never `fail` on resolver gaps alone).
Pool-external papers named in the appendix are existence-checked (S2 id lookup
-> arXiv API fallback -> S2 title search) and edges touching them run through
the same citation chain. anchor_recall / gt_edge_recall carry explicit
frozen-pool ceilings so an at-ceiling run reads as such, not as a low ratio.
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
import urllib.parse
import urllib.request

S2 = "https://api.semanticscholar.org/graph/v1"
ARXIV_RE = re.compile(r"^\d{4}\.\d{4,5}$")


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


# --- network layer (all lookups cache-first; caches live under gt/) ---

def _save(cache_path, cache):
    if cache_path:
        cache_path.write_text(json.dumps(cache))


def http_json(url, key, timeout=30):
    """GET with retries. Returns (status, parsed) with status in ok|404|error."""
    headers = {"x-api-key": key} if key else {}
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(3):
        try:
            body = urllib.request.urlopen(req, timeout=timeout).read()
            time.sleep(1.1 if key else 3.1)  # keyless hits the shared rate pool
            return "ok", json.loads(body)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "404", None
            time.sleep(3 + 3 * attempt)
        except Exception:
            time.sleep(3 + 3 * attempt)
    return "error", None


def s2_refs(idref, cache, cache_path, key, net=True):
    """Reference list of a paper; idref is a bare arXiv id or an S2 paperId.
    Returns [[arxiv_id|None, title], ...] | None (no S2 record) | NO_NET | FETCH_FAILED."""
    idref = str(idref)
    if idref in cache:
        return cache[idref]
    if not net:
        return "NO_NET"
    path = f"arXiv:{idref}" if ARXIV_RE.match(idref) else idref
    status, data = http_json(f"{S2}/paper/{path}/references?fields=title,externalIds&limit=1000", key)
    if status == "error":
        return "FETCH_FAILED"
    if status == "404":
        cache[idref] = None
        _save(cache_path, cache)
        return None
    out = [[((r.get("citedPaper") or {}).get("externalIds") or {}).get("ArXiv"),
            (r.get("citedPaper") or {}).get("title")] for r in (data.get("data") or [])]
    cache[idref] = out
    _save(cache_path, cache)
    return out


def s2_paper(idref, meta, meta_path, key, net=True):
    """Existence lookup. Returns {title, arxiv, paperId} | None (404) | NO_NET | FETCH_FAILED."""
    ck = f"paper:{idref}"
    if ck in meta:
        return meta[ck]
    if not net:
        return "NO_NET"
    path = f"arXiv:{idref}" if ARXIV_RE.match(str(idref)) else str(idref)
    status, data = http_json(f"{S2}/paper/{path}?fields=title,externalIds", key)
    if status == "error":
        return "FETCH_FAILED"
    rec = None if status == "404" else {
        "title": data.get("title"),
        "arxiv": (data.get("externalIds") or {}).get("ArXiv"),
        "paperId": data.get("paperId"),
    }
    meta[ck] = rec
    _save(meta_path, meta)
    return rec


def s2_title_search(title, meta, meta_path, key, net=True):
    """Top-5 S2 title search; first titles_match hit. Same return shape as s2_paper."""
    ck = f"search:{norm_title(title)[:120]}"
    if ck in meta:
        return meta[ck]
    if not net:
        return "NO_NET"
    q = urllib.parse.quote(title[:200])
    status, data = http_json(f"{S2}/paper/search?query={q}&fields=title,externalIds&limit=5", key)
    if status == "error":
        return "FETCH_FAILED"
    rec = None
    for it in ((data or {}).get("data") or []):
        if titles_match(title, it.get("title")):
            rec = {"title": it.get("title"),
                   "arxiv": (it.get("externalIds") or {}).get("ArXiv"),
                   "paperId": it.get("paperId")}
            break
    meta[ck] = rec
    _save(meta_path, meta)
    return rec


def arxiv_api_title(aid, meta, meta_path, net=True):
    """arXiv API existence fallback for ids S2 hasn't indexed. Returns title | None | NO_NET | FETCH_FAILED."""
    ck = f"arxiv-title:{aid}"
    if ck in meta:
        return meta[ck]
    if not net:
        return "NO_NET"
    url = f"https://export.arxiv.org/api/query?id_list={aid}&max_results=1"
    try:
        body = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "replace")
        time.sleep(1.0)
    except Exception:
        return "FETCH_FAILED"
    m = re.search(r"<entry>.*?<title>(.*?)</title>", body, re.S)
    title = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
    if title and title.lower() == "error":
        title = None
    meta[ck] = title
    _save(meta_path, meta)
    return title


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--qid", required=True)
    ap.add_argument("--gt-dir", default=str(pathlib.Path(__file__).parent / "../paper-graph/gt"))
    ap.add_argument("--fixture", default=None)
    ap.add_argument("--mmdc", choices=["auto", "off"], default="auto")
    ap.add_argument("--no-s2", action="store_true",
                    help="fully offline: no S2/arXiv calls, cache-only verdicts")
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
    # citation-lookup id per pool index: arXiv id, else the S2 paperId the
    # fixture record carries (pools come from S2 search, so paperId is ~always there)
    idx2ref = {i + 1: (idx2arxiv[i + 1] or papers[i].get("paperId")) for i in range(len(papers))}
    pool_ids = {a for a in idx2arxiv.values() if a}

    net = not args.no_s2
    key = os.environ.get("S2_API_KEY") or None
    cache_path = gt_dir / "refs_cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    meta_path = gt_dir / "paper_meta_cache.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}

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

    # --- appendix entries: pool-slot relabels + pool-external existence checks ---
    app_entries = {}
    for m in re.finditer(r"^\*\*\((\d+)\)\s*\[([^\]]*)\]\(([^)]*)\)", md, re.M):
        n = int(m.group(1))
        url = m.group(3)
        am = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", url)
        app_entries[n] = {"title": m.group(2).strip(), "url": url,
                          "arxiv": am.group(1) if am else None}

    relabeled = []
    externals = []
    ext_ref = {}    # appendix index -> resolved citation-lookup id
    ext_title = {}  # appendix index -> report title (for title-fallback in citation check)
    for n, ent in sorted(app_entries.items()):
        if n in idx2arxiv:
            pt = idx2title.get(n)
            if pt and ent["title"] and len(norm_title(ent["title"])) >= 16 \
                    and not titles_match(pt, ent["title"]):
                relabeled.append({"n": n, "pool_title": pt, "report_title": ent["title"]})
            continue
        # pool-external paper: verify it exists at all, and pin an id for edge checks
        ext_title[n] = ent["title"]
        verdict, resolved = "unverifiable(no-id-no-title)", None
        loose = len(norm_title(ent["title"])) < 16  # too short to title-compare safely
        if ent["arxiv"]:
            rec = s2_paper(ent["arxiv"], meta, meta_path, key, net)
            if rec in ("NO_NET", "FETCH_FAILED"):
                verdict = f"unverifiable({rec})"
            elif rec:
                ok = loose or not ent["title"] or titles_match(rec.get("title"), ent["title"])
                verdict, resolved = ("exists-s2" if ok else "id-title-mismatch"), ent["arxiv"]
            else:  # S2 has no record for the id -> raw arXiv API
                at = arxiv_api_title(ent["arxiv"], meta, meta_path, net)
                if at in ("NO_NET", "FETCH_FAILED"):
                    verdict = f"unverifiable({at})"
                elif at:
                    ok = loose or not ent["title"] or titles_match(at, ent["title"])
                    verdict, resolved = ("exists-arxiv" if ok else "id-title-mismatch"), ent["arxiv"]
                else:
                    verdict = "not-found"
        elif ent["title"]:
            rec = s2_title_search(ent["title"], meta, meta_path, key, net)
            if rec in ("NO_NET", "FETCH_FAILED"):
                verdict = f"unverifiable({rec})"
            elif rec:
                verdict, resolved = "exists-s2", (rec.get("arxiv") or rec.get("paperId"))
            else:
                verdict = "not-found"
        if resolved:
            ext_ref[n] = resolved
        externals.append({"n": n, "title": ent["title"], "arxiv": ent["arxiv"],
                          "exists": verdict})
    out["external_papers"] = {
        "n": len(externals),
        "exists": sum(1 for e in externals if e["exists"].startswith("exists")),
        "not_found": sum(1 for e in externals if e["exists"] == "not-found"),
        "id_title_mismatch": sum(1 for e in externals if e["exists"] == "id-title-mismatch"),
        "unverifiable": sum(1 for e in externals if e["exists"].startswith("unverifiable")),
        "entries": externals,
    }
    out["relabeled_pool_slots"] = relabeled

    # --- anchor recall (report level, with frozen-pool ceiling) ---
    present_ids = {idx2arxiv[i] for i in appendix_nums if idx2arxiv.get(i)}
    anchors_hit, anchors_miss = [], []
    titles_gt = json.loads((gt_dir / "id_titles_s2.json").read_text())
    titles_gt.setdefault("2202.00512", "Progressive Distillation for Fast Sampling of Diffusion Models")

    def anchor_in_pool(a):
        if a["arxiv"] in pool_ids:
            return True
        t = titles_gt.get(a["arxiv"], "")
        return bool(t) and any(titles_match(t, idx2title[i]) for i in idx2title)

    pool_anchors = [a["arxiv"] for a in gt["anchors"] if anchor_in_pool(a)]
    for a in gt["anchors"]:
        gt_title = titles_gt.get(a["arxiv"], "")
        hit = a["arxiv"] in present_ids or any(
            titles_match(gt_title, idx2title[i]) for i in appendix_nums if i in idx2title)
        (anchors_hit if hit else anchors_miss).append(a["arxiv"])
    out["anchor_recall"] = {
        "hit": anchors_hit, "miss": anchors_miss,
        "ratio": round(len(anchors_hit) / len(gt["anchors"]), 3),
        "ceiling": len(pool_anchors), "pool_present": pool_anchors,
        "note": "ceiling = anchors present in the frozen input pool; misses beyond it belong to the retrieval layer, not the SUT",
    }

    # --- edges ---
    # src id may carry an inline node label — `ODE_P2("(2) DPM-Solver (2022)") -->|Gap...|` —
    # which is valid mermaid and model-idiom dependent; without this tolerance the
    # extraction silently undercounts edges for models that declare labels inline.
    raw_edges = re.findall(
        r"_P(\d+)\s*(?:\(\"[^\"]*\"\)|\[\"[^\"]*\"\])?\s*(-->|-\.->)\s*\|Gap([^|]*)\|\s*\w+_P(\d+)",
        md)

    def arxiv_for(n):
        r = idx2ref.get(n) or ext_ref.get(n)
        return r if (r and ARXIV_RE.match(str(r))) else None

    edges = []
    for src_n, arrow, gap, dst_n in raw_edges:
        s, d = int(src_n), int(dst_n)
        e = {"src_n": s, "dst_n": d,
             "src_arxiv": arxiv_for(s), "dst_arxiv": arxiv_for(d),
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

    # --- citation consistency (cache -> live S2 by id/paperId -> title -> unverifiable) ---
    for e in edges:
        sref = idx2ref.get(e["src_n"]) or ext_ref.get(e["src_n"])
        dref = idx2ref.get(e["dst_n"]) or ext_ref.get(e["dst_n"])
        if not (sref and dref):
            e["cited"] = "unverifiable(no-id)"
            continue
        refs = s2_refs(dref, cache, cache_path, key, net)
        if refs is None or refs in ("NO_NET", "FETCH_FAILED"):
            e["cited"] = f"unverifiable({'no-s2-record' if refs is None else refs})"
            continue
        ids = {r[0] for r in refs if r[0]}
        if e["src_arxiv"] and e["src_arxiv"] in ids:
            e["cited"] = "verified"
            continue
        stitle = idx2title.get(e["src_n"]) or ext_title.get(e["src_n"]) or ""
        tn = norm_title(stitle)
        hit = tn and any(len(norm_title(r[1])) > 15 and
                         (tn in norm_title(r[1]) or norm_title(r[1]) in tn)
                         for r in refs if r[1])
        e["cited"] = "verified-by-title" if hit else "not-found"

    # --- GT edge recall (with frozen-pool ceiling) ---
    report_pairs = {(e["src_arxiv"], e["dst_arxiv"]) for e in edges
                    if e["src_arxiv"] and e["dst_arxiv"]}
    gt_hit = [f"{s}->{d}" for s, d in gt["edges"] if (s, d) in report_pairs]
    reachable = [f"{s}->{d}" for s, d in gt["edges"] if s in pool_ids and d in pool_ids]
    out["gt_edge_recall"] = {
        "hit": gt_hit,
        "ratio": round(len(gt_hit) / len(gt["edges"]), 3),
        "total_gt": len(gt["edges"]),
        "ceiling": len(reachable), "reachable": reachable,
        "note": "ceiling = GT edges with BOTH endpoints in the frozen pool; 0 means this column cannot move on this case",
    }

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
