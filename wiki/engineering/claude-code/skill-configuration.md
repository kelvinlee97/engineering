---
type: Configuration
title: Skill configuration
description: The SKILL.md frontmatter fields and directory layout that define a Claude Code agent skill.
tags: [claude-code, skills, configuration]
sources:
  - id: claude-agent-skills-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/agent-skills/README.md
    title: Introduction to Claude Code Agent Skills (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:20:00Z }
status: draft
---
An [agent skill](agent-skill.md) is a directory named after the skill containing `SKILL.md`: YAML frontmatter, then the instructions Claude follows once the skill is loaded.[^claude-agent-skills-course]

## Fields

| Field | Required | Guidance |
| --- | --- | --- |
| `name` | Yes | Lowercase letters, numbers, hyphens; at most 64 characters; same as the directory name |
| `description` | Yes | At most 1,024 characters; what the skill does and when to use it, in words users actually say |
| `allowed-tools` | No | Restricts tools for read-only or sensitive workflows (see [Least-privilege tool access](least-privilege-tool-access.md)) |
| `model` | No | Selects a model for the skill |

[^claude-agent-skills-course] `name` identifies the skill, `description` decides when it matches, and the body says what to do.[^claude-agent-skills-course]

## Layout

```text
my-skill/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

Why the supporting folders exist is on [Progressive disclosure](progressive-disclosure.md).

## Example

```markdown
---
name: pr-description
description: Writes pull request descriptions. Use when creating or summarizing a pull request.
---

When writing a PR description:

1. Inspect the complete branch diff.
2. Explain what changed and why.
3. List the concrete changes and any renamed or deleted files.
```

## Related

- [Subagent configuration file](subagent-configuration.md): the parallel format for subagents, which can list skills to preload.
- Source: [Introduction to Claude Code Agent Skills](../../sources/claude-agent-skills-course.md)

[^claude-agent-skills-course]: Introduction to Claude Code Agent Skills (study guide)
