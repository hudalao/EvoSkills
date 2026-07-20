Meta Review of Submission4402 by Area Chair 8XBu (decision: Reject; scores 8,4,2,2)

Summary: The submission polarized the reviewers. Empirical results are strong on reported metrics; the method substantially reduces common spatial artifacts (collisions/penetrations, out-of-bound placements) and offers a valuable new dataset. Reviewer gk1H strongly championed the paper for its "core insight" regarding image-based representations.

However, several reviewers (notably qXFA and v9NZ, with overlap in emkT's concerns) questioned whether the technical novelty meets the ICLR bar. The method can be viewed as a cascade of an image diffusion generator and a detector-based parser — perceived as system-level integration. The reliance on a vision-based detector to reverse-engineer the scene graph from pixels was viewed as an engineering workaround rather than a learning advance. Unresolved concerns about baselines/positioning and perceived engineering emphasis contributed to doubts about novelty/insight level. Could be a strong fit for venues emphasizing applied scene synthesis systems and dataset contributions.

Successfully addressed in rebuttal: dataset clarifications/labeling (Chinese room names → English on release; scope = layout geometry); missing dining-room evaluation (CHOrD beats DiffuScene there); 'autoregressive' terminology (hierarchical across levels, not sibling objects); 'house-scale' definition; YOLOv8-OBB details + accuracy; EchoScene baseline added, MMGDreamer reproducibility documented.

Reviewer Scores (AC prediction): qXFA would maintain 2 (novelty disagreement fundamental); emkT likely maintain as well.
