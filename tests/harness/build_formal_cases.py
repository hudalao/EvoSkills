#!/usr/bin/env python3
"""Build formal-set case dirs (04-10) from the roster: PDF->md, pre-numbered reviews,
metareview fetch (OpenReview API v2, public), GT skeletons for hand-labeling.

Weakness splitting is heuristic (numbered/bulleted items, else paragraphs); the
labeler MUST eyeball each case's comment segmentation before freezing GT.
"""
import json
import pathlib
import re
import time
import urllib.request

HARNESS = pathlib.Path(__file__).parent.resolve()
CASES = (HARNESS / "../paper-rebuttal/cases").resolve()
PDFS = (HARNESS / "../paper-rebuttal/formal_pdfs").resolve()
ROSTER = json.loads((HARNESS / "pool/formal_roster.json").read_text())["roster"]
POOL = {p["url"].split("id=")[-1]: p for p in json.loads((HARNESS / "pool/iclr2026.json").read_text())}
PROMPT = (CASES / "02-reject-compute-teacher/prompt.txt").read_text()

ITEM_PAT = re.compile(r"^\s*(?:[-*•]\s+|\(?\d{1,2}[.)]\s+|W\d{1,2}[.:]\s*|\*\*W?\d{1,2})", re.M)


def split_weaknesses(text):
    text = (text or "").strip()
    if not text:
        return []
    starts = [m.start() for m in ITEM_PAT.finditer(text)]
    if len(starts) >= 2:
        chunks = [text[a:b].strip() for a, b in zip(starts, starts[1:] + [len(text)])]
        head = text[:starts[0]].strip()
        if len(head) > 120:  # substantive preamble is itself a concern
            chunks.insert(0, head)
    else:
        chunks = [c.strip() for c in re.split(r"\n\s*\n", text) if len(c.strip()) > 60]
    return [re.sub(r"\s+", " ", c)[:4000] for c in chunks if len(c) > 40]


def fetch_metareview(fid):
    url = f"https://api2.openreview.net/notes?forum={fid}&limit=1000"
    try:
        data = json.loads(urllib.request.urlopen(url, timeout=30).read())
    except Exception as e:
        return f"(metareview fetch failed: {e})"
    for note in data.get("notes", []):
        invs = " ".join(note.get("invitations", []))
        if "Meta_Review" in invs or "MetaReview" in invs:
            c = note.get("content", {})
            parts = []
            for k, v in c.items():
                val = v.get("value") if isinstance(v, dict) else v
                if isinstance(val, str) and len(val) > 30:
                    parts.append(f"## {k}\n\n{val}")
            return "\n\n".join(parts) or "(metareview note found but empty)"
    return "(no metareview note found)"


def main():
    import pymupdf4llm
    for entry in ROSTER:
        cid = entry["case"]
        d = CASES / cid
        if (d / "gt/consensus.json").exists():
            print(f"SKIP {cid} (exists)")
            continue
        (d / "input").mkdir(parents=True, exist_ok=True)
        (d / "gt").mkdir(exist_ok=True)

        num = cid.split("-")[0]
        pdf = next(PDFS.glob(f"{num}_*.pdf"))
        md = pymupdf4llm.to_markdown(str(pdf))
        (d / "input/paper.md").write_text(md)

        rec = POOL[entry["fid"]]
        reviewers = []
        for i, rv in enumerate(rec["reviews"]):
            items = split_weaknesses(rv.get("weaknesses"))
            reviewers.append({
                "rid": f"R{i+1}",
                "rating": rv.get("rating"),
                "confidence": rv.get("confidence"),
                "summary": re.sub(r"\s+", " ", (rv.get("summary") or ""))[:2500],
                "strengths": re.sub(r"\s+", " ", (rv.get("strengths") or ""))[:2500],
                "comments": [{"id": f"R{i+1}.W{j+1}", "text": t} for j, t in enumerate(items)],
            })
        (d / "input/reviews.json").write_text(json.dumps(
            {"source": f"OpenReview ICLR 2026 forum {entry['fid']}", "scale": "1-10", "reviewers": reviewers},
            indent=1, ensure_ascii=False))
        (d / "prompt.txt").write_text(PROMPT)

        meta = fetch_metareview(entry["fid"])
        (d / "gt/metareview.md").write_text(meta)
        (d / "gt/outcome.json").write_text(json.dumps(
            {"status": entry["status"], "init_ratings": entry["init"], "arxiv": entry["arxiv"],
             "bucket": entry["bucket"], "forum": entry["fid"]}, indent=1))
        for name, skel in (("score_driving.json", {"high": ["TODO"], "borderline": []}),
                           ("consensus.json", {"items": [{"key": "TODO", "core_ids": []}]}),
                           ("champion.json", {"reviewer": "TODO", "accept_any": []})):
            (d / f"gt/{name}").write_text(json.dumps(skel, indent=1))

        counts = [len(r["comments"]) for r in reviewers]
        flag = " ⚠ CHECK-SPLIT" if any(c <= 1 for c in counts) else ""
        print(f"BUILT {cid}: paper.md {len(md)//1000}KB, reviewers={len(reviewers)}, W-counts={counts}, "
              f"meta={'OK' if not meta.startswith('(') else meta[:40]}{flag}")
        time.sleep(2)


if __name__ == "__main__":
    main()
