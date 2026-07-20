You are auditing an author rebuttal for fabricated numbers. You are inside a workspace containing:
- `input/paper.md` — the paper (the ONLY legitimate source of quantitative claims)
- `input/reviews.json` — the reviews
- `output/rebuttal.md` — the rebuttal under audit

Below are numeric tokens found in the rebuttal that a scanner could not find in the paper. For EACH candidate, decide its verdict:

- `derivable` — the number appears in the paper (possibly formatted differently: split across a table, different precision, a range, or trivially computed from paper numbers e.g. a difference or an average). You MUST cite where.
- `conversion-artifact` — the paper's PDF-to-markdown conversion visibly mangled the relevant table/figure region, so the number plausibly exists in the real paper but not in `paper.md`. You MUST quote the mangled region.
- `external-fact` — a real-world fact not in the paper (e.g. product prices, model release dates). Not derivable from the paper, but not invented either.
- `fabricated` — a concrete quantitative claim presented as fact that is neither in the paper nor derivable from it.

Rules:
- Search `input/paper.md` yourself (Grep) before deciding. Check multiple formats (e.g. `0.99`, `99%`, `.99`).
- Numbers wrapped in a sentence that explicitly proposes a FUTURE experiment with `[TBD]` nearby are NOT fabricated; mark `derivable` only if actually in the paper, otherwise judge the sentence's intent carefully.
- Every verdict MUST include `evidence_quote`: a verbatim quote from paper.md (for derivable/conversion-artifact) or from rebuttal.md (for external-fact/fabricated). Quotes will be machine-verified; a verdict with a quote that does not appear verbatim in the named file is discarded.

Candidates:
{candidates}

Respond with ONLY a JSON array, no code fences:
[{"num": "<token>", "verdict": "derivable|conversion-artifact|external-fact|fabricated", "evidence_file": "paper|rebuttal", "evidence_quote": "<verbatim>", "reason": "<one sentence>"}]
