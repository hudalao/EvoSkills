#!/usr/bin/env python3
"""Mechanically prepare blinded judge workspaces + fully-substituted prompts.

The A/B mapping is written to mapping.json files which the orchestrator must NOT
read until all pairwise verdicts are collected. Assignment is deterministic
(crc32 of case name), round 2 is always the flip of round 1.

usage: blind_prep.py <runs_dir>
"""
import json
import pathlib
import shutil
import sys
import zlib

RUNS = pathlib.Path(sys.argv[1]).resolve()
HARNESS = pathlib.Path(__file__).parent.resolve()
CASES = (HARNESS / "../paper-rebuttal/cases").resolve()
PROMPTS = HARNESS / "judge_prompts"
JW = RUNS / "judge_ws"

PREAMBLE = """IMPORTANT EXECUTION RULES:
- Workspace root: {root}
  All relative paths in the instructions below resolve against this root.
- Never use web tools (no WebSearch/WebFetch). Never read files outside the workspace root.
- Your final message must be ONLY the requested JSON, no prose around it.

"""


def sub(template_name, root, mapping):
    t = (PROMPTS / template_name).read_text()
    for k, v in mapping.items():
        t = t.replace("{" + k + "}", v)
    return PREAMBLE.format(root=root) + t


def main():
    if JW.exists():
        shutil.rmtree(JW)
    made = []
    for case_dir in sorted(CASES.iterdir()):
        if not case_dir.is_dir():
            continue
        c = case_dir.name
        runs = {arm: RUNS / f"{c}-{arm}" for arm in ("base", "skill")}
        if not all((r / "ws/output/rebuttal.md").exists() for r in runs.values()):
            continue

        # --- per-run fab + quality prompts ---
        for arm, rdir in runs.items():
            ws = (rdir / "ws").resolve()
            metrics = json.loads((rdir / "metrics.json").read_text())
            cands = metrics.get("fabrication_candidates", [])
            outd = JW / "runs" / f"{c}-{arm}"
            outd.mkdir(parents=True, exist_ok=True)
            if cands:
                (outd / "fab_prompt.txt").write_text(
                    sub("fab.md", ws, {"candidates": json.dumps(cands, indent=1, ensure_ascii=False)}))
            gt = json.loads((case_dir / "gt/score_driving.json").read_text())
            reviews = json.loads((case_dir / "input/reviews.json").read_text())
            txt = {x["id"]: x["text"] for r in reviews["reviewers"] for x in r["comments"]}
            concerns = [{"id": i, "comment": txt[i]} for i in gt["high"]]
            (outd / "quality_prompt.txt").write_text(
                sub("quality.md", ws, {"concerns": json.dumps(concerns, indent=1, ensure_ascii=False)}))
            made.append(str(outd))

        # --- blinded pairwise workspaces, 2 position-swapped rounds ---
        base_is_A_r1 = (zlib.crc32(c.encode()) % 2) == 0
        mapping = {}
        for rnd in (1, 2):
            base_is_A = base_is_A_r1 if rnd == 1 else not base_is_A_r1
            d = JW / c / f"round{rnd}"
            d.mkdir(parents=True, exist_ok=True)
            shutil.copytree(case_dir / "input", d / "input")
            a_arm, b_arm = ("base", "skill") if base_is_A else ("skill", "base")
            shutil.copy(runs[a_arm] / "ws/output/rebuttal.md", d / "rebuttal_A.md")
            shutil.copy(runs[b_arm] / "ws/output/rebuttal.md", d / "rebuttal_B.md")
            (d / "pairwise_prompt.txt").write_text(sub("pairwise.md", d.resolve(), {}))
            mapping[f"round{rnd}"] = {"A": a_arm, "B": b_arm}
        (JW / c / "mapping.json").write_text(json.dumps(mapping, indent=1))
        made.append(str(JW / c))

    print(json.dumps({"prepared": made, "note": "mapping.json files are SEALED"}, indent=1))


if __name__ == "__main__":
    main()
