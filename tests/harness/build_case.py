#!/usr/bin/env python3
"""Build one paper-rebuttal eval case directory from the ICLR 2026 dump + arXiv PDF.

Usage: build_case.py <forum_id> <arxiv_id_with_version> <case_dir>
Produces: input/paper.md, input/reviews.json (draft segmentation), prompt.txt,
          gt/outcome.json, gt/champion.json (prefilled), gt/consensus.json + gt/score_driving.json (templates),
          case_meta.json
Segmentation of weaknesses into numbered comments is a DRAFT — hand-verify before use.
"""
import json
import pathlib
import re
import sys
import urllib.request

FORUM, ARXIV, CASE_DIR = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])

HARNESS = pathlib.Path(__file__).parent

BULLET = re.compile(r"^\s*(?:[-*••]|\(?\d{1,2}[.)\]]|W\d+[:.)]|\[W\d+\])\s+")


def segment(text):
    """Split a weaknesses blob into discrete comments: bullet/numbered items first, paragraphs as fallback."""
    lines = text.replace("\r", "").split("\n")
    items, cur = [], []
    any_bullet = any(BULLET.match(l) for l in lines)
    if any_bullet:
        for l in lines:
            if BULLET.match(l):
                if cur:
                    items.append("\n".join(cur).strip())
                cur = [BULLET.sub("", l, count=1)]
            else:
                cur.append(l)
        if cur:
            items.append("\n".join(cur).strip())
    else:
        items = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    # merge fragments <120 chars into the previous item (they're usually continuations)
    merged = []
    for it in items:
        if merged and len(it) < 120:
            merged[-1] = merged[-1] + "\n" + it
        else:
            merged.append(it)
    return [m for m in merged if m.strip()]


def main():
    dh = json.load(open(HARNESS / "pool/iclr2026.json"))
    pc = {p["id"]: p for p in json.load(open(HARNESS / "pool/pc_iclr2026.json"))}
    paper = next(x for x in dh if x["url"].endswith(FORUM))
    status = pc[FORUM].get("status")

    inp = CASE_DIR / "input"
    gt = CASE_DIR / "gt"
    inp.mkdir(parents=True, exist_ok=True)
    gt.mkdir(parents=True, exist_ok=True)

    # 1) PDF -> paper.md
    pdf_path = CASE_DIR / "input" / "paper.pdf"
    if not pdf_path.exists():
        url = f"https://export.arxiv.org/pdf/{ARXIV}"
        print(f"downloading {url}")
        urllib.request.urlretrieve(url, pdf_path)
    import pymupdf4llm

    md = pymupdf4llm.to_markdown(str(pdf_path))
    (inp / "paper.md").write_text(md)
    print(f"paper.md: {len(md)} chars")

    # 2) reviews.json with draft segmentation, reviewers ordered as in dump
    reviewers = []
    revs = [r for r in paper["reviews"] if r.get("rating") is not None]
    for i, r in enumerate(revs, 1):
        rid = f"R{i}"
        comments = [
            {"id": f"{rid}.W{j}", "text": t}
            for j, t in enumerate(segment(r.get("weaknesses") or ""), 1)
        ]
        reviewers.append(
            {
                "rid": rid,
                "rating": r["rating"],
                "confidence": r.get("confidence"),
                "summary": (r.get("summary") or "").strip(),
                "strengths": (r.get("strengths") or "").strip(),
                "comments": comments,
            }
        )
    reviews = {
        "source": {
            "forum": FORUM,
            "venue": "ICLR 2026",
            "ratings_state": "pre-discussion snapshot (2025-11)",
            "note": "weaknesses only; 'questions' field not captured by upstream dump",
        },
        "scale": "ratings 1-10, higher is better",
        "reviewers": reviewers,
    }
    (inp / "reviews.json").write_text(json.dumps(reviews, indent=2, ensure_ascii=False))
    n_comments = sum(len(r["comments"]) for r in reviewers)
    print(f"reviews.json: {len(reviewers)} reviewers, {n_comments} comments")

    # 3) prompt.txt (arm-neutral)
    (CASE_DIR / "prompt.txt").write_text(
        (HARNESS / "templates/rebuttal_prompt.txt").read_text()
    )

    # 4) GT skeletons
    ratings = [r["rating"] for r in reviewers]
    top = max(ratings)
    champs = [r["rid"] for r in reviewers if r["rating"] == top]
    (gt / "outcome.json").write_text(
        json.dumps(
            {
                "decision": status,
                "initial_ratings": {r["rid"]: r["rating"] for r in reviewers},
                "final_ratings": "unavailable (public dumps are pre-rebuttal snapshots)",
                "source": "papercopilot status + davidheineman Nov-2025 snapshot",
                "HIDDEN_FROM_SUT": True,
            },
            indent=2,
        )
    )
    (gt / "champion.json").write_text(
        json.dumps(
            {"reviewer": champs[0] if len(champs) == 1 else None, "candidates": champs,
             "rule": "highest initial rating; tie broken by hand using review positivity",
             "needs_manual": len(champs) > 1},
            indent=2,
        )
    )
    for name in ("consensus.json", "score_driving.json"):
        p = gt / name
        if not p.exists():
            p.write_text(json.dumps({"TODO": "hand-label", "items": []}, indent=2))

    (CASE_DIR / "case_meta.json").write_text(
        json.dumps(
            {"forum": FORUM, "arxiv": ARXIV, "title": paper.get("title"),
             "decision": status, "initial_ratings": ratings,
             "paper_version_note": f"arXiv {ARXIV} (latest pre-review-release version)"},
            indent=2,
        )
    )
    print(f"case built at {CASE_DIR}")


if __name__ == "__main__":
    main()
