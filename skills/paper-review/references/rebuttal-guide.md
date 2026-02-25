# Rebuttal Guide

## Overview

A rebuttal is your opportunity to address reviewer concerns and clarify misunderstandings. A well-crafted rebuttal can change the outcome of a paper review.

---

## Step 1: Analyze Reviews

Before writing, carefully analyze each review:

### Categorize Concerns

For each reviewer concern, categorize it:

| Category | Response Strategy |
|----------|-----------------|
| **Misunderstanding** | Clarify with specific references to the paper |
| **Missing experiment** | Provide the experiment (if feasible within rebuttal period) |
| **Missing baseline** | Add comparison or explain why the baseline is not applicable |
| **Writing clarity** | Acknowledge and provide revised text |
| **Fundamental concern** | Address directly with technical arguments or additional evidence |
| **Minor issue** | Thank the reviewer and confirm you will fix it |

### Identify Common Themes

If multiple reviewers raise the same concern, prioritize it — it's likely a real weakness.

### Distinguish Actionable vs. Subjective

- **Actionable**: "Missing comparison with Method X" → You can address this
- **Subjective**: "The novelty is limited" → Harder to address, but can be reframed

---

## Step 2: Structure the Rebuttal

### General Template

```
We thank the reviewers for their constructive feedback. We address each
concern below and highlight the key changes in the revised paper.

## Common Concerns

[Address concerns raised by multiple reviewers first]

## Response to Reviewer 1

**Q1: [Paraphrase the concern]**

[Your response]

**Q2: [Paraphrase the concern]**

[Your response]

## Response to Reviewer 2
...
```

### Response Structure per Concern

For each concern:
1. **Acknowledge**: Show you understand the concern
2. **Respond**: Provide your answer (evidence, clarification, new experiments)
3. **Action**: State what you changed or will change in the revision

---

## Step 3: Writing Effective Responses

### For "Missing Experiments" Concerns

- If feasible, **run the experiment** and include results in the rebuttal
- If not feasible, explain why and offer alternatives:
  - "We agree this would strengthen the paper. We will include this in the revision."
  - "This comparison is not directly applicable because [reason], but we provide [alternative evidence]."

### For "Novelty is Limited" Concerns

- Restate the core insight that makes the work novel
- Highlight what existing methods cannot do that yours can
- Point to specific experimental evidence that demonstrates the advantage
- Avoid being defensive; be factual and specific

### For "Writing is Unclear" Concerns

- Thank the reviewer for identifying the issue
- Provide the revised text inline
- Explain what was changed and why

### For "Method Doesn't Work Well" Concerns

- If the concern is valid, acknowledge it honestly
- Provide additional evidence or analysis
- Discuss when/why the method works well and its limitations
- Adding failure analysis actually builds credibility

---

## Step 4: Tone and Strategy

### Do

- Be **respectful and professional** at all times
- **Acknowledge valid concerns** — reviewers appreciate honesty
- **Provide concrete evidence** — numbers, figures, and specific references
- **Be concise** — reviewers have limited time
- Thank reviewers for their time and effort

### Do Not

- Be defensive or dismissive
- Argue that the reviewer is wrong (even if they are — reframe instead)
- Ignore any concern (address everything, even minor issues)
- Promise changes you cannot deliver
- Exceed the word/page limit

---

## Pre-Submission Defense Strategy

The best rebuttal strategy is **prevention**. Before submitting:

1. **Self-review with the 5-aspect checklist** (see SKILL.md)
2. **Ask**: "What would a critical reviewer say about this paper?"
3. **Address weaknesses proactively**: Add experiments, clarify writing, discuss limitations
4. **Have others review**: Fresh eyes catch issues you've become blind to

See the `paper-review` SKILL.md "The Perfectionist Approach" section for the full self-review philosophy.

---

## Common Reviewer Concerns and Prepared Responses

Plan responses for these common concerns before submission:

| Common Concern | Preparation |
|---------------|-------------|
| "Limited novelty" | Clearly articulate the insight; show what others can't do |
| "Marginal improvement" | Emphasize other advantages; add challenging test cases |
| "Missing ablations" | Run all ablations before submission |
| "Missing baselines" | Include all relevant recent methods |
| "Not reproducible" | Add implementation details; plan code release |
| "Limited evaluation" | Use diverse datasets and multiple metrics |
| "No limitation discussed" | Always include a Limitation section |
| "Overclaimed results" | Ensure every claim has experimental support |
