# Rebuttal Guide

## Overview

A rebuttal is your opportunity to address reviewer concerns and clarify misunderstandings. A well-crafted rebuttal can change the outcome of a paper review.

---

## Diagnose Before You Respond

Before writing a single word, answer one question: **"Why did this reviewer give this exact score?"** Not what they wrote — what drove the score. Most researchers skip this step and jump straight to answering every comment equally. That is a mistake.

### The Score Diagnosis Framework

For each reviewer, ask: **"What would move this reviewer from their current score to acceptance?"**

- A reviewer at 5 usually needs 1-2 concerns resolved to reach 7
- A reviewer at 3 usually has a fundamental objection that no amount of minor fixes will address
- A reviewer at 7+ is already your champion — your job is to arm them, not convince them

### Color-Code Your Review Analysis

Read through each review and mark every comment:

| Color | Meaning | Action |
|-------|---------|--------|
| **Green** | Positive comment or praise | Note for later — this is ammunition for your champion |
| **Red** | Critical threat — this concern drives the low score | Address first, with maximum effort and evidence |
| **Orange** | Addressable concern — can be resolved with effort | Address with concrete response or new data |
| **Gray** | Minor or cosmetic | Acknowledge briefly, confirm fix |

### Identify the Invisible Question

Behind every reviewer comment is an unspoken question. A comment like "The baselines are outdated" really asks: "Is this method actually competitive with current approaches?" Address the invisible question, not just the surface-level request.

**Counterintuitive insight**: Reviewers only firmly remember 1-2 key concerns when they enter the discussion phase. They may write 20 comments, but they forget most of them. Your rebuttal's success depends on nailing those 1-2 red-coded concerns, not addressing all 20 equally.

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

- **Actionable**: "Missing comparison with Method X" — You can address this
- **Subjective**: "The novelty is limited" — Harder to address, but can be reframed

---

## The Champion Strategy

**Your rebuttal's real audience is not the negative reviewer — it's the positive one.**

Most researchers write rebuttals aimed at convincing their harshest critic. This is wrong. Your rebuttal's primary job is to arm your champion with ammunition for the discussion phase.

### Why This Matters

- Without at least one champion, acceptance is nearly impossible regardless of rebuttal quality
- The champion argues on your behalf in the AC discussion — often using your exact words
- A neutral reviewer reading all reviews + your rebuttal should be able to tell whether concerns were addressed

### How to Write for Your Champion

1. **Make your key arguments copy-pasteable** — your champion will quote your rebuttal in the discussion
2. **Highlight where reviewers agree with each other** — consensus points strengthen the champion's position
3. **Flag contradictions between reviewers** — if R1 says "limited novelty" but R2 says "interesting approach," your champion can use this
4. **Lead with strengths before addressing weaknesses** — remind everyone (especially the AC) what your paper does well

### The Neutral Third-Party Test

Before submitting, have someone who hasn't read your paper read only the reviews and your rebuttal. Ask: "Can you tell whether the concerns were addressed?" If not, rewrite.

---

## Step 2: Structure the Rebuttal

### General Template

```
We thank the reviewers for their thoughtful feedback.

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

### Organizing Reviews Efficiently

Use a structured method to organize before writing:

- **Spreadsheet method**: One row per concern, columns for reviewer ID, category, priority (red/orange/gray), response status, and page limit budget
- **Group common concerns** across reviewers into a single consolidated response — this saves word count and demonstrates that the concern is well-understood
- **Mark key questions per reviewer**: Usually found in the "questions for authors" or "justification" section — these are what the reviewer actually cares about

### Response Structure per Concern

For each concern:
1. **Acknowledge**: Show you understand the concern
2. **Respond**: Provide your answer (evidence, clarification, new experiments)
3. **Action**: State what you changed in the revision

---

## 18 Tactical Rules

### Structure Rules

**1. Address biggest concerns first, not in reviewer order.**
The AC reads your rebuttal quickly. Put the most important answers at the top, not buried under minor issues.

**2. Consolidate shared concerns into a "Common Response" section.**
If two reviewers both question the baselines, write one strong response instead of two weaker ones. This also signals you understand the pattern.

**3. Quote the concern concisely, then answer directly.**
Lead with the answer. Put supporting details after. Reviewers skim — front-load the conclusion.

**4. Use resolution-oriented headers.**
Write "Clarifying statistical significance" not "Is the improvement significant?" Problem-oriented headers make your rebuttal feel defensive; resolution-oriented headers signal confidence.

### Content Rules

**5. Do, don't promise.**
Provide the experiment, explanation, or revised text inline. "We will add in the revision" is the weakest possible response. If you ran a new experiment, show the table now.

**6. If it's already in the paper, cite the exact location AND restate it.**
Never say "as discussed in Section 3.2" and leave it at that. The AC likely won't re-read Section 3.2. Quote or summarize the relevant content in the rebuttal itself.

**7. Use data over argumentation.**
One new experiment table beats three paragraphs of explanation. Reviewers trust numbers, not rhetoric.

**8. Stay self-contained.**
The AC may not re-read your paper during the discussion. Reintroduce acronyms, method names, and key setup details in the rebuttal.

**9. Address the underlying intent, not just the literal question.**
"Why didn't you compare with Method X?" often means "I'm not convinced your method is competitive." Answering the literal question (adding Method X) without addressing competitiveness misses the point.

**10. Never introduce new problems.**
Every new claim in a rebuttal is a new attack surface. If you mention a new capability, a reviewer may ask "where's the evidence?" Keep the scope tight.

### Tone Rules

**11. Start with genuine positives.**
A sentence like "We appreciate R2's recognition that our approach handles X well" reminds the AC of your paper's strengths before diving into defense.

**12. Write "We agree" not "We acknowledge."**
"Acknowledge" sounds reluctant, as if you're conceding under pressure. "Agree" sounds collaborative.

**13. Write "revised version" not "final version."**
"Final version" implies the paper is already accepted. "Revised version" respects the process.

**14. Be transparent about constraints.**
If you cannot run a requested experiment due to compute budget or venue page limits, say so honestly. Honesty builds trust; silence looks evasive.

**15. Thank reviewers for constructive additions.**
When a reviewer catches typos or suggests useful citations, a quick "Thank you — added" costs nothing and builds goodwill.

### Advanced Tactics

**16. Flag unreasonable reviews professionally.**
If a reviewer's concern contradicts the other reviewers, reference this factually: "We note that R1 and R3 both found the experimental evaluation comprehensive, which seems to address R2's concern about evaluation scope."

**17. Peer-check your critical responses.**
Have a colleague verify your 1-2 most important answers. A fresh pair of eyes catches logical gaps, unclear phrasing, and missing evidence.

**18. Save all reviews permanently.**
Patterns across submissions reveal your blind spots. If three different papers get "limited novelty" feedback, the issue is likely in how you frame contributions, not in the contributions themselves.

---

## Word Count Optimization

For venues with strict word limits (e.g., 500-1000 words):

- **Tables count as fewer words than equivalent prose** — present new results as compact tables instead of narrating them
- **Link to supplementary material** — "See Appendix A in the revised paper for the full ablation" saves word budget for critical responses
- **Merge related concerns** to avoid repeating context — if R1 and R3 both question robustness, address them together
- **Cut boilerplate to one line** — "We thank all reviewers for their feedback" is sufficient; no need for a full paragraph of gratitude
- **Use bullet points instead of paragraphs** — they're denser and easier to scan
- **Prioritize ruthlessly** — if you can only address 5 of 15 concerns well, pick the 5 that move scores; a shallow response to all 15 is worse than a thorough response to 5

---

## Counterintuitive Rebuttal Principles

### 1. Submit a rebuttal even with extreme scores

A paper with scores of 3/8/8 has better odds than you think. Reviewers read each other's reviews and sometimes revise their scores during discussion. The negative reviewer may realize they are an outlier. But this only works if you submit a rebuttal — without one, the AC has nothing to work with.

### 2. Concede something small, win something big

Acknowledging a minor weakness ("We agree that Table 2 could include dataset X for completeness") makes your defense of major points more credible. Pure defense with zero concession reads as unobjective.

### 3. One new experiment > three paragraphs of explanation

Reviewers are trained to be skeptical of arguments. They are not trained to be skeptical of data. A small new experiment that directly addresses a concern is worth more than any amount of reasoning.

### 4. The best rebuttal is written before submission

As you write your paper, draft responses to likely attacks. This is "prebuttal" — and it has two benefits: (1) you often realize the attack is valid and fix the paper, and (2) if the attack does come, you have a polished response ready.

### 5. Don't defend every point equally

Equal effort across all concerns signals that you don't know which points matter. Allocate 60% of your word budget to the 1-2 red-coded concerns, 30% to orange, and 10% to gray. Reviewers notice when you nail the big issues.

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
| "Unfair comparison / cherry-picked baselines" | Use standard evaluation protocols; include all commonly reported baselines, not just favorable ones |
| "Method is engineering, not research" | Clearly identify the scientific insight behind the engineering; explain why the design choice is non-obvious |
| "Evaluation metrics don't match the claim" | Align each claim with a specific metric; if the claim is about quality, don't only report speed |
| "Related work is incomplete" | Survey systematically; if a prominent paper is missing, adding it and explaining the relationship costs little but prevents a rejection trigger |

---

## Pre-Submission Defense Strategy

The best rebuttal strategy is **prevention**. Before submitting:

1. **Self-review with the 5-aspect checklist** (see SKILL.md)
2. **Ask**: "What would a critical reviewer say about this paper?"
3. **Address weaknesses proactively**: Add experiments, clarify writing, discuss limitations
4. **Have others review**: Fresh eyes catch issues you've become blind to
5. **Draft prebuttals**: For each likely criticism, write the response now — if you can't defend it, fix the paper

See the `paper-review` SKILL.md "The Perfectionist Approach" section for the full self-review philosophy.
