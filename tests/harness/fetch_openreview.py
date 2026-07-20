#!/usr/bin/env python3
"""Fetch ICLR candidate pool from OpenReview (API v2, anonymous) for rebuttal-eval case selection.

Emits candidates.jsonl: one line per submission with review stats, decision, metareview presence.
Usage: .venv/bin/python fetch_openreview.py --venue ICLR.cc/2025/Conference --max 800 --out pool/candidates.jsonl
"""
import argparse
import json
import re
import sys
import warnings

warnings.filterwarnings("ignore")

import openreview


def parse_rating(value):
    """Ratings come as '6', 6, or '6: marginally above ...'. Return int or None."""
    if value is None:
        return None
    if isinstance(value, int):
        return value
    m = re.match(r"\s*(\d+)", str(value))
    return int(m.group(1)) if m else None


def get(content, key):
    v = content.get(key)
    if isinstance(v, dict):
        return v.get("value")
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--venue", default="ICLR.cc/2025/Conference")
    ap.add_argument("--max", type=int, default=800, help="max submissions to scan")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    client = openreview.api.OpenReviewClient(baseurl="https://api2.openreview.net")

    n_scanned, n_written = 0, 0
    with open(args.out, "w") as fout:
        offset = 0
        page = 1000
        while n_scanned < args.max:
            notes = client.get_notes(
                invitation=f"{args.venue}/-/Submission",
                details="replies",
                sort="number:asc",
                limit=min(page, args.max - n_scanned),
                offset=offset,
            )
            if not notes:
                break
            offset += len(notes)
            for note in notes:
                n_scanned += 1
                content = note.content or {}
                replies = (note.details or {}).get("replies", [])

                reviews, decision, meta, author_replies = [], None, None, 0
                for r in replies:
                    invs = r.get("invitations", [])
                    inv_str = " ".join(invs)
                    rc = r.get("content", {})
                    if "/Official_Review" in inv_str:
                        reviews.append(
                            {
                                "id": r["id"],
                                "rating": parse_rating(get(rc, "rating")),
                                "confidence": parse_rating(get(rc, "confidence")),
                                "signature": (r.get("signatures") or [""])[0],
                            }
                        )
                    elif "/Decision" in inv_str:
                        decision = get(rc, "decision")
                    elif "/Meta_Review" in inv_str:
                        meta = get(rc, "metareview") or get(rc, "recommendation") or ""
                    elif "/Official_Comment" in inv_str or "/Rebuttal" in inv_str:
                        sig = " ".join(r.get("signatures") or [])
                        if "Authors" in sig:
                            author_replies += 1

                ratings = sorted([r["rating"] for r in reviews if r["rating"] is not None])
                if len(ratings) < 3 or decision is None:
                    continue  # need full review cycle
                rec = {
                    "forum": note.forum,
                    "number": note.number,
                    "title": get(content, "title"),
                    "n_reviews": len(reviews),
                    "ratings": ratings,
                    "spread": ratings[-1] - ratings[0],
                    "decision": decision,
                    "has_meta": bool(meta),
                    "meta_len": len(meta or ""),
                    "author_replies": author_replies,
                    "has_pdf": bool(get(content, "pdf")),
                }
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n_written += 1
            print(f"scanned={n_scanned} kept={n_written}", file=sys.stderr)
            if len(notes) < page:
                break
    print(f"done: scanned={n_scanned} kept={n_written} -> {args.out}")


if __name__ == "__main__":
    main()
