#!/usr/bin/env python3
"""Blinded single-pass judge workspaces for HUMAN pairwise skill comparisons.

Pairs per-case outputs of two arms from one runs dir ({case}-{tag} subdirs),
anonymizes each pair as A/B. Positions are deterministic and balanced: cases
are ordered by crc32("human|skill|case|baseline_ref|candidate_ref") and the
candidate alternates A/B along that order — reproducible, roughly 50/50, and
independent of the LLM-judge pair-name hashing, so prior tally reports leak
nothing. The judge fills verdicts.tsv; .mapping.json stays SEALED (do not
open it) until tally.py ingest unseals it after all verdicts are in.

usage:
  blind_prep.py --skill paper-graph \
    --runs tests/harness/runs/graph-pilot-sonnet5 \
    --baseline-tag base --baseline-ref no-skill \
    --candidate-tag skill --candidate-ref v0.1.0 \
    --artifact ws/output/report.md --extra ws/input/query.txt \
    --sut claude-sonnet-5 --out judge_ws/graph-s5-base-vs-v010
"""
import argparse
import csv
import datetime
import json
import pathlib
import shutil
import sys
import zlib

README = """# Blind pairwise judging — human protocol

Each case dir holds two anonymized outputs ({stem}_A{ext}, {stem}_B{ext})
plus any context files. Which arm is A varies per case; the mapping is sealed.

Rules while judging:
1. Do NOT open .mapping.json, the runs dir, or old judge/tally reports.
2. Judge every case in verdicts.tsv (tab-separated; keep it tab-separated):
   - winner: A | B | tie
   - margin: clear | slight   (leave empty for tie)
   - reason: one line, required for non-ties (free text, tabs -> spaces)
3. Judge the deliverable a user would receive: correctness, faithfulness to
   the query, structure, and usefulness — not formatting taste.

When every row is filled:

    python3 {tally} ingest {ws} --judge <your-initials>

That unseals the mapping, resolves A/B to arms, appends to the ledger, and
prints the win rate.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skill", required=True)
    ap.add_argument("--runs", required=True, type=pathlib.Path)
    ap.add_argument("--baseline-tag", required=True)
    ap.add_argument("--candidate-tag", required=True)
    ap.add_argument("--baseline-ref", required=True,
                    help="version tag/commit of the baseline arm (or 'no-skill')")
    ap.add_argument("--candidate-ref", required=True,
                    help="version tag/commit of the candidate arm")
    ap.add_argument("--artifact", required=True,
                    help="path of the judged output inside each run dir, e.g. ws/output/report.md")
    ap.add_argument("--extra", action="append", default=[],
                    help="extra per-case context file(s) to copy unblinded, e.g. ws/input/query.txt")
    ap.add_argument("--sut", required=True, help="model that executed the skill runs")
    ap.add_argument("--out", required=True, type=pathlib.Path)
    ap.add_argument("--fresh", action="store_true",
                    help="wipe an existing workspace (default: refuse to touch one)")
    a = ap.parse_args()

    if a.out.exists():
        if not a.fresh:
            sys.exit(f"refusing to touch existing workspace {a.out} (use --fresh to wipe)")
        shutil.rmtree(a.out)

    def cases_for(tag):
        suf = f"-{tag}"
        return {d.name[: -len(suf)]: d for d in a.runs.iterdir()
                if d.is_dir() and d.name.endswith(suf)}

    base, cand = cases_for(a.baseline_tag), cases_for(a.candidate_tag)
    cases = sorted(base.keys() & cand.keys())
    for c in sorted(base.keys() ^ cand.keys()):
        print(f"warning: case {c} present in only one arm, skipped", file=sys.stderr)
    if not cases:
        sys.exit(f"no paired cases under {a.runs} for tags "
                 f"{a.baseline_tag!r}/{a.candidate_tag!r}")

    def key(c):
        return zlib.crc32(f"human|{a.skill}|{c}|{a.baseline_ref}|{a.candidate_ref}".encode())

    # balanced deterministic positions: hash-order the cases, alternate A/B
    ordered = sorted(cases, key=key)
    cand_pos = {c: ("A" if i % 2 == 0 else "B") for i, c in enumerate(ordered)}

    art = pathlib.Path(a.artifact)
    stem, ext = art.stem, art.suffix
    missing = []
    for c in cases:
        cdir = a.out / c
        cdir.mkdir(parents=True)
        pos = cand_pos[c]
        arms = {pos: cand[c], ("B" if pos == "A" else "A"): base[c]}
        for label, run_dir in arms.items():
            src = run_dir / art
            if not src.exists():
                missing.append(str(src))
                continue
            shutil.copy(src, cdir / f"{stem}_{label}{ext}")
        for x in a.extra:
            src = cand[c] / x  # frozen inputs are identical across arms
            if src.exists():
                shutil.copy(src, cdir / pathlib.Path(x).name)
    if missing:
        sys.exit("missing artifacts, workspace incomplete:\n  " + "\n  ".join(missing))

    with open(a.out / "verdicts.tsv", "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["case", "winner", "margin", "reason"])
        for c in cases:
            w.writerow([c, "", "", ""])

    (a.out / ".mapping.json").write_text(json.dumps({
        "meta": {
            "skill": a.skill,
            "baseline_ref": a.baseline_ref,
            "candidate_ref": a.candidate_ref,
            "sut_model": a.sut,
            "runs_dir": str(a.runs),
            "artifact": a.artifact,
            "created": datetime.date.today().isoformat(),
        },
        "cases": {c: {"candidate": cand_pos[c]} for c in cases},
    }, indent=1) + "\n")

    tally = pathlib.Path(__file__).resolve().parent / "tally.py"
    (a.out / "README.md").write_text(
        README.format(stem=stem, ext=ext, tally=tally, ws=a.out.resolve()))
    print(f"{len(cases)} blinded cases -> {a.out}  "
          f"(candidate as A in {sum(1 for p in cand_pos.values() if p == 'A')}"
          f"/{len(cases)}; mapping sealed)")


if __name__ == "__main__":
    main()
