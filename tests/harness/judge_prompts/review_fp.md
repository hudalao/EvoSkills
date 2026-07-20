You are auditing a paper self-review for FALSE claims about the paper (this evaluates the review, not the paper). You are inside a workspace containing:
- `input/main_flat.tex` — the paper source the reviewer saw
- `output/findings.json` — the review's findings
- `output/self_review.md` — the review memo

Below is a subset of findings to audit (findings already matched to known issues are excluded). For EACH finding, verify its factual claims against the paper source and classify:

- `legitimate` — the criticism is factually grounded: what it says about the paper is true (the detail IS missing, the claim IS unsupported, the table DOES lack X), and a reasonable reviewer could raise it. It being subjective in *severity* is fine; the factual basis must hold.
- `fabricated` — the finding misstates the paper: it claims something is absent that is present, misquotes numbers or content, references a section/table/figure that does not exist, or attributes a claim the paper never makes.
- `subjective` — no falsifiable factual claim (pure style/taste/preference), so neither of the above applies.

Rules:
- Grep `input/main_flat.tex` yourself before deciding. For "X is missing" claims, search several plausible spellings/synonyms of X (including in the appendix) before accepting `legitimate`.
- Every verdict MUST carry `evidence_quote`: for `fabricated`, a verbatim quote from main_flat.tex CONTRADICTING the finding (e.g. the passage that does contain X); for `legitimate`, a verbatim quote consistent with the criticism, or `"ABSENCE"` when the evidence is that nothing matching exists (then list in `searched` the 3+ patterns you grepped). Quotes are machine-verified against the file; a `fabricated` verdict with a non-verifying quote is voided to `subjective`.
- Judge the finding's central factual claim, not incidental wording.

Findings to audit:
{findings}

Respond with ONLY a JSON array, no code fences:
[{"id": "F3", "verdict": "legitimate|fabricated|subjective", "evidence_quote": "<verbatim from main_flat.tex or ABSENCE>", "searched": ["<pattern1>", "..."], "reason": "<one sentence>"}]
