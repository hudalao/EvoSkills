# Contributing to EvoSkills

Welcome! EvoSkills is the community-driven skill repository for [EvoScientist](https://github.com/EvoScientist/EvoScientist). There are two ways to contribute:

1. **Improve an existing skill** — fix content, update references, tune descriptions
2. **Add a new skill** — extend EvoScientist with new domain expertise

## Prerequisites

- **EvoScientist** installed (`pip install evoscientist` or `pip install -e ".[dev]"` from source) and configured (`EvoSci onboard`)
- **EvoSkills** cloned:
  ```bash
  git clone https://github.com/EvoScientist/EvoSkills.git
  cd EvoSkills
  ```
- An LLM API key configured

## Repository Layout

```
EvoSkills/
  skills/                    # 10 skills (edit in-place)
    paper-planning/
    paper-writing/
    research-ideation/
    ...
```

Each skill is a self-contained directory:

```
my-skill/
  SKILL.md          # required — frontmatter + body
  references/       # optional — docs loaded into agent context
  assets/           # optional — files used in agent output (templates, images)
```

## Skill Anatomy

### SKILL.md Frontmatter

```yaml
---
name: my-skill
description: "One-line summary. Key method/framework keywords. Use when: specific triggers."
allowed-tools: "write_file edit_file read_file think_tool"
metadata:
  author: YourName
  version: '1.0.0'
  tags: [relevant, keywords]
---
```

### Description Tips

The existing 10 skills use a common description pattern that works well for routing accuracy:

```
"[1-sentence summary]. [Core method/framework keywords].
 Use when: [specific triggers].
 Do NOT use for [scenarios that belong to other skills]."
```

The `Do NOT use for` clause helps the agent distinguish skills with overlapping domains — for example, `paper-planning` says `Do NOT use for actual writing (use paper-writing)`. This isn't required, but it's helpful when your skill shares keywords with others.

### Body

After the frontmatter, the body contains the skill's full instructions: workflow steps, rules, examples, and cross-references to `references/` files. Structure varies by skill type — see existing skills for patterns.

## Improving an Existing Skill

### Types of Changes

| Change | Example |
|--------|---------|
| Content fix | Correct a rule, add a missing example |
| Reference update | Update a guide in `references/` |
| Cross-skill consistency | Ensure related skills agree on shared terms or outputs |

### Workflow

1. Edit the skill files in `skills/<name>/`
2. Validate structure: the directory must contain `SKILL.md` with valid frontmatter
3. Manual test: install the skill and try it in EvoSci (`/install-skill path/to/EvoSkills/skills/<name>`)
4. If you changed the **description**, we recommend running eval with `skill-creator` (see [Testing & Evaluation](#testing--evaluation))

## Adding a New Skill

### 1. Bootstrap

You can ask EvoSci to create a skill for you using the built-in `skill-creator`:

```text
"Create a new skill called my-new-skill in path/to/EvoSkills/skills"
```

Or manually create `skills/my-new-skill/SKILL.md` following the frontmatter format above.

### 2. Write the Skill

- Write a clear `description` in the frontmatter — see [Description Tips](#description-tips) for the recommended pattern
- Write the body with workflow steps, rules, and examples
- Look at existing skills for inspiration

### 3. Test

Install and try the skill in a real EvoSci session:

```text
/install-skill path/to/EvoSkills/skills/my-new-skill
```

### 4. Update README

Add your skill to the table and description sections in `README.md`.

## Testing & Evaluation

There are two ways to validate your changes:

### Manual Testing

The simplest approach — install the skill and use it in real tasks:

1. Start an EvoSci session
2. Install your skill: `/install-skill path/to/EvoSkills/skills/<name>`
3. Try queries that should trigger the skill, and queries that should not
4. Verify the skill produces correct output when loaded

This is sufficient for most content changes.

### Automated Eval with `skill-creator` (Recommended for Description Changes)

EvoScientist ships with a built-in `skill-creator` skill that can systematically evaluate and optimize skill descriptions. To use it:

1. Start an EvoSci session (`skill-creator` is built-in, no extra install needed)
2. Ask it to evaluate or optimize your skill's description:
   ```text
   "Optimize the description for path/to/EvoSkills/skills/paper-planning"
   ```
3. `skill-creator` will:
   - Generate 20 trigger eval queries (10 should-trigger, 10 should-not-trigger)
   - Let you review and edit the queries
   - Run an automated eval + improvement loop (train/test split, iterative refinement)
   - Report the best description with scores

This is the same methodology used to optimize the existing 10 EvoSkills descriptions.

See the [`skill-creator` SKILL.md](https://github.com/EvoScientist/EvoScientist/tree/main/EvoScientist/skills/skill-creator) for full details on the eval workflow.

## Quality Checklist

Use the appropriate tier based on your change:

### Content Changes (no description edit)
- [ ] SKILL.md frontmatter is valid (name, description, allowed-tools)
- [ ] Cross-references to `references/` files are correct
- [ ] Manual test: install skill, run a sample query in EvoSci

### Description Changes
- [ ] All of the above, plus:
- [ ] Tested with `skill-creator` eval (recommended) or thorough manual testing

### New Skill
- [ ] All of the above, plus:
- [ ] README.md updated with skill entry

## Quick Reference

| Task | Command |
|------|---------|
| Install skill for testing | `/install-skill path/to/EvoSkills/skills/my-skill` (in EvoSci session) |
| Install all skills | `/install-skill path/to/EvoSkills/skills` (in EvoSci session) |
| Eval with skill-creator | Ask EvoSci: `"Optimize the description for path/to/skills/my-skill"` |
| Create a new skill | Ask EvoSci: `"Create a new skill called my-skill in path/to/EvoSkills/skills"` |

## Commit & PR Standards

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) with the skill name as scope:

```
feat(paper-planning): add fallback narrative section
fix(evo-memory): correct IVE trigger condition in memory-schema.md
docs(experiment-pipeline): add 20% regression threshold note
```

For new skills: `feat: add my-new-skill`

### Pull Requests

- Title: brief summary under 70 characters
- Body: describe what changed and why
- **Include eval scores** if description was optimized with `skill-creator`
