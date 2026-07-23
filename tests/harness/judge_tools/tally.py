#!/usr/bin/env python3
"""Tally graph base-vs-skill blind pairwise verdicts (UNSEALS mapping.json).

Run only after all verdict.json files are in. Win rule (same as the k3
protocol): a pair produces a winner only if both position-swapped rounds
name the same arm; position-inconsistent = tie. Also aggregates the
per-dimension calls (taxonomy/edges/selection/utility) mapped back to arms.
"""
import json
import os
import pathlib

# Lives in tests/harness/judge_tools/ (versioned); workspaces stay under the
# gitignored runs/ tree. JUDGE_WS env selects the workspace generation (default
# judge_ws; v2 = enriched per-run prefetch digests). Keeps v1 verdicts/tally
# untouched by later passes.
JW = (pathlib.Path(__file__).resolve().parents[1] / "runs/graph-pilot-judge"
      / (os.environ.get("JUDGE_WS") or "judge_ws"))


def main():
    table, missing = {}, []
    dim_agg = {}  # dim -> {"base": n, "skill": n, "tie": n}
    agg = {"base": 0, "skill": 0, "tie": 0}
    for pdir in sorted(JW.iterdir()):
        if not pdir.is_dir():
            continue
        mapping = json.loads((pdir / "mapping.json").read_text())
        rounds = []
        for rnd, ab in sorted(mapping.items()):
            vp = pdir / rnd / "verdict.json"
            if not vp.exists():
                missing.append(f"{pdir.name}/{rnd}")
                continue
            v = json.loads(vp.read_text())
            w = v.get("winner")
            tag = ab.get(w, "tie") if w in ("A", "B") else "tie"
            dims = {}
            for dim, call in (v.get("dimensions") or {}).items():
                dtag = ab.get(call, "tie") if call in ("A", "B") else "tie"
                dims[dim] = dtag
                dim_agg.setdefault(dim, {"base": 0, "skill": 0, "tie": 0})[dtag] += 1
            rounds.append({"round": rnd, "winner_arm": tag, "margin": v.get("margin"),
                           "reason": v.get("reason"),
                           "decisive_factor": v.get("decisive_factor"),
                           "dimensions_arm": dims, "raw_winner": w})
        tags = [r["winner_arm"] for r in rounds]
        final = tags[0] if len(tags) == 2 and tags[0] == tags[1] else "tie"
        consistent = len(tags) == 2 and tags[0] == tags[1]
        agg[final] += 1
        table[pdir.name] = {"final": final, "consistent": consistent, "rounds": rounds}

    out = {"aggregate_pair_wins": agg,
           "dimension_round_calls": dim_agg,
           "pairs": table, "missing_verdicts": missing,
           "note": "mapping unsealed by this tally; win requires both swapped rounds to agree; "
                   "glm pairs are a control (neither GLM arm executed the skill pipeline)"}
    (JW / "tally.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
