#!/usr/bin/env python3
"""Ingest blind verdicts into the human-eval ledger and report win rates.

ingest <workspace>: validates verdicts.tsv is complete, unseals .mapping.json,
resolves A/B back to baseline/candidate, appends rows to ledger.csv (refuses
duplicate (skill, case, pair, judge) rows unless --force, which replaces),
then prints the pair summary. Works for LLM judges too via --judge-type llm,
so both judge populations share one ledger and stay comparable.

report: aggregates the ledger per (skill, baseline_ref, candidate_ref,
judge_type): W/T/L, win rate excluding ties, exact two-sided sign test, and
per-case human-vs-llm agreement where both judge types covered a case.
"""
import argparse
import csv
import datetime
import json
import math
import pathlib
import sys

LEDGER = pathlib.Path(__file__).resolve().parent / "ledger.csv"
COLS = ["date", "skill", "case", "baseline_ref", "candidate_ref", "sut_model",
        "judge", "judge_type", "candidate_position", "verdict", "margin", "reason"]
KEY = ("skill", "case", "baseline_ref", "candidate_ref", "judge")


def read_ledger(path):
    if not path.exists():
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write_ledger(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)


def sign_test(wins, losses):
    """Exact two-sided binomial test against p=0.5, ties excluded."""
    n = wins + losses
    if n == 0:
        return None
    k = max(wins, losses)
    p = 2 * sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
    return min(1.0, p)


def summarize(rows):
    w = sum(1 for r in rows if r["verdict"] == "candidate")
    l = sum(1 for r in rows if r["verdict"] == "baseline")
    t = sum(1 for r in rows if r["verdict"] == "tie")
    wr = f"{w / (w + l):.0%}" if w + l else "n/a"
    p = sign_test(w, l)
    return (f"{w}W / {t}T / {l}L  ->  candidate win rate {wr} (excl. ties)"
            + (f", sign test p={p:.3f}" if p is not None else ""))


def cmd_ingest(a):
    ws = a.workspace
    mapping = json.loads((ws / ".mapping.json").read_text())
    meta, cases = mapping["meta"], mapping["cases"]

    with open(ws / "verdicts.tsv", newline="") as f:
        verdicts = {r["case"]: r for r in csv.DictReader(f, delimiter="\t")}

    problems = []
    for c in cases:
        v = verdicts.get(c)
        if v is None:
            problems.append(f"{c}: missing row")
            continue
        winner = (v.get("winner") or "").strip()
        margin = (v.get("margin") or "").strip()
        reason = (v.get("reason") or "").strip()
        if winner not in ("A", "B", "tie"):
            problems.append(f"{c}: winner must be A|B|tie, got {winner!r}")
        elif winner == "tie":
            if margin:
                problems.append(f"{c}: margin must be empty for a tie")
        else:
            if margin not in ("clear", "slight"):
                problems.append(f"{c}: margin must be clear|slight, got {margin!r}")
            if not reason:
                problems.append(f"{c}: reason required for a non-tie")
    for c in verdicts.keys() - cases.keys():
        problems.append(f"{c}: not in sealed mapping (row edited?)")
    if problems:
        sys.exit("verdicts incomplete, mapping stays sealed:\n  "
                 + "\n  ".join(sorted(problems)))

    today = datetime.date.today().isoformat()
    new = []
    for c in sorted(cases):
        v, pos = verdicts[c], cases[c]["candidate"]
        winner = v["winner"].strip()
        verdict = "tie" if winner == "tie" else (
            "candidate" if winner == pos else "baseline")
        new.append({
            "date": today, "skill": meta["skill"], "case": c,
            "baseline_ref": meta["baseline_ref"],
            "candidate_ref": meta["candidate_ref"],
            "sut_model": meta["sut_model"],
            "judge": a.judge, "judge_type": a.judge_type,
            "candidate_position": pos, "verdict": verdict,
            "margin": (v["margin"] or "").strip(),
            "reason": " ".join((v["reason"] or "").split()),
        })

    rows = read_ledger(a.ledger)
    keys = {tuple(r[k] for k in KEY) for r in new}
    dupes = [r for r in rows if tuple(r[k] for k in KEY) in keys]
    if dupes and not a.force:
        sys.exit(f"{len(dupes)} of these judgments already in {a.ledger} "
                 f"(same skill/case/pair/judge); use --force to replace")
    rows = [r for r in rows if tuple(r[k] for k in KEY) not in keys] + new
    write_ledger(a.ledger, rows)

    pair = f"{meta['candidate_ref']} vs {meta['baseline_ref']}"
    print(f"{len(new)} judgments -> {a.ledger}"
          + (f" (replaced {len(dupes)})" if dupes else ""))
    print(f"{meta['skill']}  {pair}  [{a.judge_type}:{a.judge}]  {summarize(new)}")


def cmd_report(a):
    rows = read_ledger(a.ledger)
    if a.skill:
        rows = [r for r in rows if r["skill"] == a.skill]
    if not rows:
        sys.exit(f"no rows in {a.ledger}" + (f" for skill {a.skill}" if a.skill else ""))

    groups = {}
    for r in rows:
        groups.setdefault(
            (r["skill"], r["baseline_ref"], r["candidate_ref"], r["judge_type"]),
            []).append(r)
    for (skill, bref, cref, jt), g in sorted(groups.items()):
        judges = ",".join(sorted({r["judge"] for r in g}))
        print(f"{skill}  {cref} vs {bref}  [{jt}: {judges}]  n={len(g)}  {summarize(g)}")

    # human-vs-llm agreement on cases both judged (unanimous within each type)
    pairs = {}
    for r in rows:
        pairs.setdefault((r["skill"], r["baseline_ref"], r["candidate_ref"]),
                         {}).setdefault(r["case"], {}).setdefault(
                             r["judge_type"], set()).add(r["verdict"])
    for (skill, bref, cref), by_case in sorted(pairs.items()):
        both = {c: t for c, t in by_case.items()
                if len(t.get("human", set())) == 1 and len(t.get("llm", set())) == 1}
        if both:
            agree = sum(1 for t in both.values() if t["human"] == t["llm"])
            print(f"{skill}  {cref} vs {bref}  human-llm agreement: "
                  f"{agree}/{len(both)} cases")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ing = sub.add_parser("ingest", help="unseal a judged workspace into the ledger")
    ing.add_argument("workspace", type=pathlib.Path)
    ing.add_argument("--judge", required=True, help="judge id (initials or model name)")
    ing.add_argument("--judge-type", choices=("human", "llm"), default="human")
    ing.add_argument("--ledger", type=pathlib.Path, default=LEDGER)
    ing.add_argument("--force", action="store_true",
                     help="replace existing rows for the same skill/case/pair/judge")
    ing.set_defaults(fn=cmd_ingest)
    rep = sub.add_parser("report", help="aggregate win rates from the ledger")
    rep.add_argument("--ledger", type=pathlib.Path, default=LEDGER)
    rep.add_argument("--skill")
    rep.set_defaults(fn=cmd_report)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
