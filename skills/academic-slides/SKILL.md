---
name: academic-slides
description: "Guides creation of academic presentation slides and research talks. Covers talk structure, slide design, visual hierarchy, delivery, Q&A preparation, and practical .pptx file creation with code examples. Use when the user wants to create presentation slides, prepare a research talk, design a slide deck, build a .pptx file, or practice an academic presentation."
allowed-tools: "write_file edit_file read_file think_tool execute"
metadata:
  author: EvoScientist
  version: '1.0.0'
  tags: [academic presentation, slides, research talk, conference]
---

# Academic Slides

A structured approach to creating academic presentation slides and preparing research talks. Covers narrative structure, slide design, visual hierarchy, delivery technique, and Q&A preparation.

## When to Use This Skill

- User wants to create presentation slides for a research talk
- User asks about structuring an academic presentation
- User needs to prepare for a conference talk, thesis defense, or lab meeting
- User wants to design a slide deck from a paper or research project
- User mentions "slides", "presentation", "talk", "defense", "poster talk"

---

## Before You Start: Three Questions

Before designing any slides, answer these questions clearly:

1. **What works are you presenting?**
   They must share a coherent research direction. If presenting multiple works, they should form a narrative arc — not a disconnected list.

2. **What problems do these works solve in that direction?**
   Each work should map to a specific problem. If you cannot articulate the problem in one sentence, you are not ready to present.

3. **How do you use related work to naturally introduce these problems?**
   Related work is not citation duty. It builds the motivation for YOUR problem. Each related work you mention should advance the audience toward understanding why your approach is needed.

---

## Core Workflow

```
Step 1: Define scope and audience
Step 2: Draft narrative arc (outline)
Step 3: Design slide structure (section breakdown)
Step 4: Create individual slides (one idea per slide)
Step 5: Add visual elements (figures, diagrams, animations)
Step 6: Rehearse and time
Step 7: Prepare backup / Q&A slides
```

### Step 1: Define Scope and Audience

| Audience | Adjust |
|----------|--------|
| Domain experts | Skip basics, go deep on method and results |
| Broad CS / engineering | Explain task context, moderate technical depth |
| Interdisciplinary | Start from the application, minimize jargon |
| Industry | Lead with impact and demo, light on theory |

**Rule of thumb**: Duration in minutes = approximate slide count. A 20-minute talk needs about 20 slides.

### Step 2: Draft Narrative Arc

Use the outline template at [assets/talk-outline-template.md](assets/talk-outline-template.md) to plan your talk before making any slides. The outline forces you to articulate your key takeaway and narrative arc.

### Step 3-5: Structure, Create, and Visualize

See [references/talk-structure.md](references/talk-structure.md) for two complete talk structures and a section-by-section guide.

See [references/slide-design.md](references/slide-design.md) for the 10 design rules and visual principles.

See [references/slide-creation.md](references/slide-creation.md) for the practical `.pptx` creation guide — color palettes, layout code examples, charts, tables, figures, icons, and QA workflow.

### Step 6: Rehearse and Time

See [references/delivery-and-qa.md](references/delivery-and-qa.md) for the rehearsal protocol, delivery principles, and Q&A preparation.

### Step 7: Prepare Backup Slides

Backup slides go after your "Thank You" slide. They are not part of the talk — they are your safety net for Q&A:

- Full quantitative comparison table
- Failure cases (shows honesty and preparation)
- Additional ablations or analysis
- Slides addressing anticipated tough questions

---

## Counterintuitive Presentation Rules

### 1. Your slides are not your paper

A talk is an advertisement, not a lecture. Your goal is to make the audience interested enough to read the paper. Cut 80% of your paper's content. If someone can reconstruct your paper from your slides alone, your slides have too much.

### 2. One idea per slide, one minute per slide

If you need 2 minutes to explain a slide, split it. Dense slides force you to rush or skip content — both are worse than having more slides with less content each.

### 3. Slide titles ARE the talk

A distracted audience member reading only your slide titles should understand your story. Use claim-style titles: "CTNND1 drives metastasis via cadherin switching" not "Results." If your title is a single noun ("Method", "Evaluation"), rewrite it.

### 4. Reading and listening compete

Text-heavy slides force the audience to choose between reading your slides and listening to you. They will read — and stop hearing you. When you put text on a slide, you are choosing to be ignored.

### 5. Enthusiasm > polish

A passionate speaker with rough slides beats a bored speaker with beautiful slides. The audience remembers your energy and clarity, not your color scheme. If you only have time to improve one thing, rehearse more — don't redesign slides.

### 6. Related work is not citation duty

Use related work to BUILD your problem motivation, not to show you have read papers. Each related work slide should advance the narrative: "This approach solved X, but Y remains open — which is exactly what we address."

---

## Reference Navigation

| Topic | Reference File | When to Use |
|-------|---------------|-------------|
| Talk structures | [talk-structure.md](references/talk-structure.md) | Organizing the narrative arc |
| Slide design | [slide-design.md](references/slide-design.md) | Visual design and layout rules |
| Slide creation | [slide-creation.md](references/slide-creation.md) | Building .pptx files with code |
| Delivery and Q&A | [delivery-and-qa.md](references/delivery-and-qa.md) | Rehearsal, timing, Q&A preparation |
| Talk outline template | [talk-outline-template.md](assets/talk-outline-template.md) | Starting a new presentation |
