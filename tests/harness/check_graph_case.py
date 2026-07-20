#!/usr/bin/env python3
"""run_matrix-compatible adapter around check_graph.py.

usage: check_graph_case.py <case_dir> <ws_dir> [--meta <meta.json>]
Derives qid from the case dir name, locates ws/output/report.md, runs the
main checker, and attaches run_meta — same contract as the sibling checkers.
"""
import argparse
import json
import pathlib
import subprocess
import sys

HARNESS = pathlib.Path(__file__).parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case_dir")
    ap.add_argument("ws_dir")
    ap.add_argument("--meta", default=None)
    args = ap.parse_args()
    case = pathlib.Path(args.case_dir)
    ws = pathlib.Path(args.ws_dir)
    qid = case.name

    report = ws / "output/report.md"
    if not report.exists():
        out = {"qid": qid, "files_ok": False, "error": "output/report.md missing"}
        if args.meta and pathlib.Path(args.meta).exists():
            out["run_meta"] = json.loads(pathlib.Path(args.meta).read_text())
        print(json.dumps(out, indent=1))
        sys.exit(2)

    r = subprocess.run(
        [sys.executable, str(HARNESS / "check_graph.py"),
         "--report", str(report), "--qid", qid,
         "--fixture", str(case / "input/papers.json"), "--mmdc", "auto"],
        capture_output=True, text=True)
    if r.returncode != 0:
        out = {"qid": qid, "files_ok": True, "checker_error": r.stderr[-400:]}
    else:
        out = json.loads(r.stdout)
        out["files_ok"] = True
    if args.meta and pathlib.Path(args.meta).exists():
        out["run_meta"] = json.loads(pathlib.Path(args.meta).read_text())
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
