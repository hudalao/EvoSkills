# Human eval — pairwise skill-version win rates

A durable ledger of blinded human A/B judgments over skill outputs, used to
decide whether a new skill version actually beats the old one. Complements the
LLM-judge tooling in `tests/harness/` (see `judge_tools/` on `tests-handover`):
same pairwise idea, but single-pass human judging and a persistent
cross-version record instead of per-run printouts.

中文操作手册（实习生向，含逐步命令与评审纪律）：[README.zh-CN.md](README.zh-CN.md).

## Flow

1. **Generate runs** for both arms with the usual harness: one runs dir with
   `{case}-{tag}` subdirs (e.g. `q1-efficient-attention-base` /
   `...-skill`), one generation per arm per case, SUT model pinned.

   `run_matrix.sh` always tags arms `base`/`skill`, so a version-vs-version
   pair (two runs dirs, both tagged `-skill`) needs a symlink merge dir first:

   ```
   mkdir -p ../harness/runs/graph-v010-vs-v011
   for d in ../harness/runs/<v010-runs>/*-skill; do
     c=$(basename "$d" -skill)
     ln -s "$(cd "$d" && pwd)" "../harness/runs/graph-v010-vs-v011/$c-v010"
   done    # same loop again for the v011 runs dir -> $c-v011
   ```

   then blind with `--baseline-tag v010 --baseline-ref v0.1.0
   --candidate-tag v011 --candidate-ref v0.1.1`.

2. **Blind** — build a judge workspace (positions balanced + deterministic,
   mapping sealed):

   ```
   python3 blind_prep.py --skill paper-graph \
     --runs ../harness/runs/graph-pilot-sonnet5 \
     --baseline-tag base --baseline-ref no-skill \
     --candidate-tag skill --candidate-ref v0.1.0 \
     --artifact ws/output/report.md --extra ws/input/query.txt \
     --sut claude-sonnet-5 --out judge_ws/graph-s5-base-vs-v010
   ```

   Artifact / judge-context paths per skill (`--extra` is repeatable):

   | skill | `--artifact` | `--extra` |
   |---|---|---|
   | paper-graph | `ws/output/report.md` | `ws/input/query.txt` |
   | paper-rebuttal | `ws/output/rebuttal.md` | `ws/input/paper.md`, `ws/input/reviews.json` |
   | paper-review | `ws/output/self_review.md` | `ws/input/main_flat.tex` |

3. **Judge** — for each case read `query.txt` + `report_A.md` / `report_B.md`,
   fill `verdicts.tsv` (winner `A|B|tie`, margin `clear|slight`, one-line
   reason). Keep real tabs — rows whose tabs an editor silently converted to
   spaces fail ingest validation. Do **not** open `.mapping.json`, the runs dir, or old tally
   reports until done.

4. **Ingest** — validates completeness, unseals, resolves, appends to
   `ledger.csv`, prints the pair summary:

   ```
   python3 tally.py ingest judge_ws/graph-s5-base-vs-v010 --judge WH
   ```

5. **Report** — win rates for everything recorded so far:

   ```
   python3 tally.py report [--skill paper-graph]
   ```

## Ledger schema (`ledger.csv`, machine-written by `tally.py`)

| column | meaning |
|---|---|
| `date` | day the judgment was ingested |
| `skill` | skill under test |
| `case` | frozen test-case id |
| `baseline_ref` / `candidate_ref` | version tag or commit of each arm (`no-skill` for base arms) |
| `sut_model` | model that executed the runs |
| `judge` / `judge_type` | judge id; `human` or `llm` |
| `candidate_position` | which blinded slot (A/B) held the candidate |
| `verdict` | `candidate` / `baseline` / `tie` (resolved) |
| `margin` | `clear` / `slight` (empty for ties) |
| `reason` | judge's one-line rationale |

One row per (case × judge). LLM-judge verdicts can be ingested into the same
ledger (`--judge <model> --judge-type llm` on a same-format workspace), which
makes the human–LLM agreement rate fall out of `tally.py report` for free.

## Protocol

- **Paired frozen cases, target ~20 per skill.** Sign-test detectability:
  15/20 wins ≈ p 0.04; at n=10 only 9/10 blowouts reach significance. Add a
  couple of fresh cases each round as a Goodhart guard.
- **Win rate** = candidate wins / (wins + losses); ties reported separately.
  `tally.py` also prints the exact two-sided sign test.
- **Blinding**: positions are balanced across cases and derived by hash, so
  reruns are reproducible and nothing about position is human-chosen. The
  mapping is honor-sealed — the workspace README states the rules.
- **Self-judging caveat**: if the judge authored the candidate version,
  blinding limits but does not remove bias; for judgments that gate a version
  bump, add a second judge on at least a subset.
- **Acceptance rule for a version bump**: to be settled — candidates are
  simple majority of non-ties, a fixed bar (e.g. ≥60% win rate), or p<0.05.
  Record the rule here once chosen.

`judge_ws/` is gitignored: workspaces are regenerable from runs; the ledger
is the durable record.
