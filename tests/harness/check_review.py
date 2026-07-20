#!/usr/bin/env python3
"""Deterministic checker for one review-eval run (schema + stats only).

Defect hit-matching and false-positive assessment are judge-pass work
(judge.py review-match mode, later); this checker validates structure and
emits the numbers that don't need language understanding.

usage: check_review.py <case_dir> <ws_dir> [--meta <meta.json>]
"""
import argparse
import json
import pathlib
import re
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case_dir")
    ap.add_argument("ws_dir")
    ap.add_argument("--meta", default=None)
    args = ap.parse_args()
    case = pathlib.Path(args.case_dir)
    ws = pathlib.Path(args.ws_dir)

    gt = json.loads((case / "gt/defects.json").read_text())
    out = {"case": case.name, "variant": gt.get("variant"), "gt_defect_n": len(gt.get("defects", []))}

    f_p = ws / "output/findings.json"
    m_p = ws / "output/self_review.md"
    out["files_ok"] = f_p.exists() and m_p.exists()

    findings = None
    if f_p.exists():
        try:
            findings = json.loads(re.sub(r"^```(json)?|```$", "", f_p.read_text().strip(), flags=re.M))
            assert isinstance(findings, list)
        except Exception as e:
            out["findings_parse_error"] = str(e)
            findings = None
    out["findings_parse"] = findings is not None

    if findings is not None:
        req = {"id", "severity", "location", "description", "fix"}
        bad = [f.get("id", f"#{i}") for i, f in enumerate(findings)
               if not isinstance(f, dict) or not req.issubset(f.keys())]
        sev = {"major": 0, "minor": 0, "other": 0}
        for f in findings:
            if isinstance(f, dict):
                sev[f.get("severity") if f.get("severity") in ("major", "minor") else "other"] += 1
        out["findings"] = {
            "n": len(findings),
            "schema_violations": bad,
            "major": sev["major"], "minor": sev["minor"], "bad_severity": sev["other"],
            "empty_locations": sum(1 for f in findings
                                   if isinstance(f, dict) and not str(f.get("location", "")).strip()),
        }

    if m_p.exists():
        memo = m_p.read_text()
        out["memo_words"] = len(memo.split())

    if args.meta and pathlib.Path(args.meta).exists():
        out["run_meta"] = json.loads(pathlib.Path(args.meta).read_text())

    print(json.dumps(out, indent=2, ensure_ascii=False))
    sys.exit(0 if out.get("files_ok") else 2)


if __name__ == "__main__":
    main()
