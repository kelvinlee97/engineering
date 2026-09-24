---
type: Pattern
title: Progressive disclosure
description: Expose only a short summary up front and load detailed material into context only when the task needs it.
tags: [claude-code, skills, context-engineering]
sources:
  - id: claude-agent-skills-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/agent-skills/README.md
    title: Introduction to Claude Code Agent Skills (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:20:00Z }
status: draft
---
Progressive disclosure means showing the model a cheap summary first and loading detail only once the task justifies it. For [agent skills](agent-skill.md), discovery costs only a name and description; the full `SKILL.md`, and then any references or scripts, enter context later.[^claude-agent-skills-course]

```mermaid
flowchart TD
    accTitle: Skill discovery and loading
    accDescr: Claude sees only skill names and descriptions, matches the request against them, loads the chosen SKILL.md, and then reads a reference or runs a script only if the task needs one.
    B[Names and descriptions] --> M{Request matches?}
    M -->|No| N[Continue without the skill]
    M -->|Yes| S[Load SKILL.md]
    S --> R{More needed?}
    R -->|Detail| D[Read one reference file]
    R -->|Operation| X[Run a provided script]
    R -->|No| W[Follow the core workflow]
```

Each step down the chart costs more context, and each is taken only when the step above says so.

## Applying it to a skill

- Keep the essential workflow in `SKILL.md`; the course recommends under 500 lines.[^claude-agent-skills-course]
- Move conditional detail to `references/`, `scripts/`, or `assets/`, and say in `SKILL.md` when to read or run each.[^claude-agent-skills-course]
- Prefer scripts for operations: Claude runs a tested script and only its output enters context, not its source.[^claude-agent-skills-course]

## Related

- [Context isolation](context-isolation.md) saves context by moving work elsewhere; progressive disclosure saves it by not loading material until needed. (Analysis: this link is the wiki's own comparison, not a claim from either source.)
- Source: [Introduction to Claude Code Agent Skills](../../sources/claude-agent-skills-course.md)

[^claude-agent-skills-course]: Introduction to Claude Code Agent Skills (study guide)
