You are an ICLR Area Chair assessing whether an author rebuttal actually addresses specific reviewer concerns. You are inside a workspace containing:
- `input/paper.md` — the paper
- `input/reviews.json` — the reviews
- `output/rebuttal.md` — the rebuttal

For EACH concern listed below, read the reviewer's full comment (by its ID in reviews.json) and locate the rebuttal section(s) claiming to address it (look for `Addresses:` lines). Then grade:

- `resolved` — the response directly engages the underlying concern with specific evidence from the paper, a concrete committed change, or a decisive clarification. A reasonable reviewer would consider the point settled or clearly on track.
- `partial` — the response engages the concern but leaves the core question open (e.g. promises without specifics, addresses a weaker version of the point, or answers only part).
- `evaded` — the response restates, deflects, disputes without evidence, or answers a different question.

Rules:
- Judge ONLY whether the concern is addressed, not writing style.
- A promise of future work counts toward `resolved` only if it is specific (what experiment, what metric, feasible in a 2-week window) AND the concern is of a kind that a credible commitment can settle; fundamental soundness objections cannot be settled by promises alone.
- Every grade MUST include `response_quote`: a verbatim quote from rebuttal.md showing the load-bearing sentence of the response. Quotes are machine-verified.

Concerns to grade:
{concerns}

Respond with ONLY a JSON array, no code fences:
[{"id": "R1.W2", "grade": "resolved|partial|evaded", "response_quote": "<verbatim from rebuttal.md>", "reason": "<one sentence>"}]
