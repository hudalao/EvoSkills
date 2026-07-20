#!/usr/bin/env python3
"""Deterministic checker for one rebuttal-eval run.

usage: check_rebuttal.py <case_dir> <ws_dir> [--meta <meta.json>]
Prints a JSON metrics object. Judge-dependent metrics (false positives, persuasiveness)
are NOT computed here; fabrication candidates are listed for the later judge pass.
"""
import argparse
import json
import pathlib
import re
import sys


def load(p):
    return json.loads(pathlib.Path(p).read_text())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case_dir")
    ap.add_argument("ws_dir")
    ap.add_argument("--meta", default=None)
    args = ap.parse_args()
    case = pathlib.Path(args.case_dir)
    ws = pathlib.Path(args.ws_dir)

    reviews = load(case / "input/reviews.json")
    all_ids = [c["id"] for r in reviews["reviewers"] for c in r["comments"]]
    gt_cons = load(case / "gt/consensus.json")
    gt_sd = load(case / "gt/score_driving.json")
    gt_champ = load(case / "gt/champion.json")

    out = {"case": case.name}

    # --- file presence / schema ---
    ana_p = ws / "output/analysis.json"
    reb_p = ws / "output/rebuttal.md"
    out["files_ok"] = ana_p.exists() and reb_p.exists()
    ana, reb = None, ""
    if ana_p.exists():
        try:
            ana = json.loads(re.sub(r"^```(json)?|```$", "", ana_p.read_text().strip(), flags=re.M))
        except Exception as e:
            out["analysis_parse_error"] = str(e)
    if reb_p.exists():
        reb = reb_p.read_text()
    out["analysis_parses"] = ana is not None

    # --- per_comment completeness ---
    if ana:
        pc_ids = [x.get("id") for x in ana.get("per_comment", [])]
        out["per_comment_missing"] = sorted(set(all_ids) - set(pc_ids))
        out["per_comment_extra"] = sorted(set(pc_ids) - set(all_ids))
        out["per_comment_complete"] = not out["per_comment_missing"] and not out["per_comment_extra"]

        # --- champion ---
        fav = ana.get("most_favorable_reviewer")
        accept = gt_champ.get("accept_any") or [gt_champ.get("reviewer")]
        out["champion_pick"] = fav
        out["champion_hit"] = fav in accept

        # --- priority vs GT score-driving ---
        high_gt = set(gt_sd["high"])
        border = set(gt_sd.get("borderline", []))
        sut_high = {x["id"] for x in ana.get("per_comment", []) if x.get("priority") == "high" and x.get("id") in all_ids}
        tp = len(sut_high & high_gt)
        fp = len(sut_high - high_gt - border)
        fn = len(high_gt - sut_high)
        out["priority"] = {
            "sut_high_n": len(sut_high),
            "precision": round(tp / (tp + fp), 3) if tp + fp else None,
            "recall": round(tp / (tp + fn), 3) if tp + fn else None,
            "missed_high": sorted(high_gt - sut_high),
            "extra_high": sorted(sut_high - high_gt - border),
        }

        # --- themes vs GT consensus ---
        sut_themes = ana.get("themes", []) or []
        matched = []
        for item in gt_cons["items"]:
            core = set(item["core_ids"])
            hit = any(len(core & set(t.get("comment_ids", []))) >= 2 for t in sut_themes)
            matched.append({"key": item["key"], "detected": hit})
        out["consensus"] = {
            "detected": sum(1 for m in matched if m["detected"]),
            "total": len(matched),
            "items": matched,
            "sut_theme_count": len(sut_themes),
        }

    # --- rebuttal coverage via Addresses: lines ---
    addr_ids = set()
    sections = []  # (tier_ids, wordcount)
    if reb:
        # tolerate leading markdown emphasis (*, **, _, ~, >) and spaces around the colon,
        # e.g. "*Addresses: R1.W1, R2.W3*" — otherwise coverage silently goes to 0.
        chunks = re.split(r"^\s*[*_~]*\s*(Addresses\s*:\s*.+)$", reb, flags=re.M)
        # chunks: [text, addr_line, text, addr_line, ..., tail]
        for i in range(1, len(chunks), 2):
            ids = set(re.findall(r"R\d+\.W\d+", chunks[i]))
            addr_ids |= ids
            words = len(chunks[i - 1].split())
            sections.append((ids, words))
        covered = addr_ids & set(all_ids)
        out["coverage"] = {
            "addressed": len(covered),
            "total": len(all_ids),
            "ratio": round(len(covered) / len(all_ids), 3),
            "unaddressed": sorted(set(all_ids) - addr_ids),
            "unknown_ids_in_addresses": sorted(addr_ids - set(all_ids)),
        }

        # --- word budget by GT tier ---
        high_gt = set(gt_sd["high"])
        border = set(gt_sd.get("borderline", []))
        buckets = {"high": 0, "borderline": 0, "low": 0}
        for ids, words in sections:
            if ids & high_gt:
                buckets["high"] += words
            elif ids & border:
                buckets["borderline"] += words
            elif ids:
                buckets["low"] += words
        tot = sum(buckets.values())
        out["budget"] = {
            "words": buckets,
            "high_share": round(buckets["high"] / tot, 3) if tot else None,
            "total_addressed_words": tot,
        }

        # --- fabrication candidates (for the judge pass) ---
        # normalize unicode dashes and thousands-commas so range/format quirks
        # (0.76–0.99, 1,234) don't create false mismatches against the corpus
        def norm(s):
            # `9 _._ 99` = pymupdf artifact for split decimal points; also unify dashes/commas
            s = re.sub(r"(\d)\s*_\._\s*(\d)", r"\1.\2", s)
            return s.replace("–", "-").replace("—", "-").replace(",", "")
        corpus = norm((case / "input/paper.md").read_text() + json.dumps(reviews))
        corpus_nums = set(re.findall(r"\d+(?:\.\d+)?", corpus))
        reb = norm(reb)
        cand = []
        for m in re.finditer(r"\d+(?:\.\d+)?", reb):
            tok = m.group(0)
            ctx = reb[max(0, m.start() - 60):m.end() + 20].replace("\n", " ")
            if tok in corpus_nums:
                continue
            if re.search(r"(Figure|Table|Section|Sec\.|Eq\.|page|R\d+\.W|20\d\d|19\d\d)\s*$", reb[max(0, m.start() - 12):m.start()]):
                continue
            if float(tok) <= 20 and "." not in tok:  # small enumeration ints
                continue
            cand.append({"num": tok, "context": ctx})
        out["fabrication_candidates"] = cand[:20]
        out["fabrication_candidate_n"] = len(cand)
        out["tbd_count"] = len(re.findall(r"\[TBD\]", reb))

    if args.meta and pathlib.Path(args.meta).exists():
        out["run_meta"] = load(args.meta)

    print(json.dumps(out, indent=2))
    # exit non-zero only on hard failure (no outputs at all)
    sys.exit(0 if out.get("files_ok") else 2)


if __name__ == "__main__":
    main()
