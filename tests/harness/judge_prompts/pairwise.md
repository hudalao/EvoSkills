You are an ICLR Area Chair. A paper received the reviews in `input/reviews.json` (paper text in `input/paper.md`). Two candidate author rebuttals were written independently: `rebuttal_A.md` and `rebuttal_B.md` (in this workspace root).

Question: which rebuttal is more likely to move reviewer scores upward / secure acceptance in the discussion phase?

Evaluate ONLY:
1. Does it resolve the concerns that actually drive the low scores (not just the easy ones)?
2. Is evidence specific and grounded in the paper (vs generic promises)?
3. Does it give the positive reviewer(s) concrete, quotable material to argue with?
4. Honesty: are claimed numbers real (spot-check suspicious ones against input/paper.md)?

Do NOT reward length, formatting polish, or politeness boilerplate.

Respond with ONLY a JSON object, no code fences:
{"winner": "A|B|tie", "margin": "clear|slight", "reason": "<3 sentences max>", "decisive_factor": "<one phrase>"}
