---
type: Configuration
title: Subagent configuration file
description: The Markdown file with YAML frontmatter that defines a custom Claude Code subagent, and how to create it with /agents.
tags: [claude-code, subagents, configuration]
sources:
  - id: claude-subagents-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/subagents/README.md
    title: Introduction to Claude Code Subagents (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: claude-agent-skills-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/agent-skills/README.md
    title: Introduction to Claude Code Agent Skills (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:20:00Z }
status: draft
---
A custom [subagent](subagent.md) is one Markdown file: YAML frontmatter for its settings, then a body that is its system prompt. Project-level subagents are typically stored at `.claude/agents/<name>.md`.[^claude-subagents-course]

## Creating one with /agents

1. Run `/agents` and choose **Create new agent**.
2. Choose a scope: project-level (this project only) or user-level (all projects on the machine).
3. Configure it by hand, or describe the behaviour and let Claude generate the name, description, and system prompt. The course recommends generating as the easier start.
4. Select tools, model, and UI colour.
5. Save the generated file.
6. Test on a representative task; if delegation does not trigger, refine the description.

As described in the course.[^claude-subagents-course]

## Fields

| Field | Role |
| --- | --- |
| `name` | Unique identifier; also usable as `@agent <name>` |
| `description` | Tells Claude when to delegate and shapes the delegated prompt; one line, with escaped `\n` for breaks |
| `tools` | The tools the subagent may use (see [Least-privilege tool access](least-privilege-tool-access.md)) |
| `model` | `haiku` (fast, light tasks), `sonnet` (middle ground), `opus` (complex analysis), or `inherit` (use the main conversation's model) |
| `color` | UI cue for which subagent is active |
| Body | The system prompt: focus, method, reporting |

As described in the course.[^claude-subagents-course]

A custom subagent can also take a `skills` field listing [skills](agent-skill.md) to load when it starts, for example `skills: accessibility-audit, performance-check`. The listed skills must already exist in an available skills directory; this suits isolated work that must apply a fixed, named set of standards.[^claude-agent-skills-course]

## Example

```markdown
---
name: code-quality-reviewer
description: Review specified code changes for quality and risk.
tools: Bash, Glob, Grep, Read
model: sonnet
color: purple
---

Review only the files named in the delegated task. Report findings by
severity and include enough evidence for the parent agent to verify them.
```

What to write in `description` and the body is covered on [Delegation contract](delegation-contract.md).

## Related

- [Skill configuration](skill-configuration.md): the matching format for skills.
- Source: [Introduction to Claude Code Agent Skills](../../sources/claude-agent-skills-course.md)
- Source: [Introduction to Claude Code Subagents](../../sources/claude-subagents-course.md)

[^claude-subagents-course]: Introduction to Claude Code Subagents (study guide)
[^claude-agent-skills-course]: Introduction to Claude Code Agent Skills (study guide)
