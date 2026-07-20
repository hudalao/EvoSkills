You are grading a paper self-review against a list of planted defects (this is an evaluation of the review, NOT of the paper). You are inside a workspace containing:
- `input/main_flat.tex` — the (defect-injected) paper source the reviewer saw
- `output/findings.json` — the self-review's findings list
- `output/self_review.md` — the self-review memo

Below are the planted defects. For EACH defect, decide whether the self-review caught it:

- `HIT` — some finding (or a memo passage) satisfies the defect's detection_criteria: it identifies the right problem at the right place. Different wording is fine; the criteria define the bar.
- `PARTIAL` — a finding touches the right location or the right problem type, but misses the substance the criteria require (e.g. flags the right table for a different reason, or names the issue but at the wrong location).
- `MISS` — nothing in findings.json or the memo satisfies the criteria even loosely.

Rules:
- Judge strictly by each defect's detection_criteria — do not improvise your own standard. The criteria's negative clauses (what does NOT count) are binding.
- For every HIT/PARTIAL verdict you MUST cite: `finding_id` (the "id" from findings.json, or "memo" if only the memo covers it) AND `evidence_quote` — a verbatim quote from findings.json or self_review.md showing the match. Quotes are machine-verified; a verdict whose quote does not appear verbatim in the named file is voided to MISS.
- One finding may hit multiple defects only if the criteria genuinely overlap; note it in reason when that happens.
- Work through defects one at a time; grep the findings for location keywords from the criteria before deciding MISS.

Planted defects:
{defects}

Respond with ONLY a JSON array, no code fences:
[{"uid": "V1-1", "verdict": "HIT|PARTIAL|MISS", "finding_id": "F3|memo|null", "evidence_quote": "<verbatim or empty for MISS>", "reason": "<one sentence>"}]
