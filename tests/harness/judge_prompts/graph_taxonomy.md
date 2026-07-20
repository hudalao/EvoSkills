You are grading the taxonomy of a research-lineage report against a reference sketch. Inputs below: the research query, the reference branch sketch (what a sound taxonomy of this field should roughly cover — a guide, not the only correct answer), the paper pool the report was built from, and the report's taxonomy section.

Grade THREE dimensions, each 1-5, using these anchors:

`branch_coverage` — does the taxonomy cover the substantive branches of the field that are actually representable with the given paper pool?
- 5: every reference branch representable from the pool appears (possibly under different names); no major representable branch missing
- 3: about half the representable branches appear; or branches exist but are so broad they merge distinct lines
- 1: taxonomy bears little relation to the field's actual structure

`grouping_coherence` — are papers placed under challenges/solutions where they belong?
- 5: every placement defensible; derivative/application papers not presented as lineage trunk
- 3: 1-2 clear misplacements, or noise papers mixed into core branches without distinction
- 1: placements look arbitrary; derivative noise dominates trunk positions

`granularity` — is the challenge/solution split at a useful altitude?
- 5: challenges are real technical tensions; solutions are distinct approaches, neither single-paper shells nor catch-alls
- 3: some single-paper solutions or one catch-all bucket
- 1: structure is degenerate (one challenge holding everything, or one solution per paper)

Rules:
- Judge ONLY against the given paper pool: do not penalize the report for branches that no pool paper could support (the pool may be noisy — that is a known input condition).
- For every score cite `evidence`: the specific branch names / paper numbers that justify it.
- Do not reward verbosity or mermaid styling.

Query: {query}

Reference branch sketch: {taxonomy_hint}

Paper pool (numbered): {papers_brief}

Report taxonomy section:
{taxonomy_section}

Respond with ONLY a JSON object, no code fences:
{"branch_coverage": {"score": 1-5, "evidence": "..."}, "grouping_coherence": {"score": 1-5, "evidence": "..."}, "granularity": {"score": 1-5, "evidence": "..."}, "overall_note": "<two sentences max>"}
