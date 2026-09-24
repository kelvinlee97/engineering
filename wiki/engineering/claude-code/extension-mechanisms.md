---
type: Concept
title: Claude Code extension mechanisms
description: How CLAUDE.md, skills, subagents, hooks, and MCP servers differ, and which job each one owns.
tags: [claude-code, skills, subagents, hooks, mcp]
sources:
  - id: claude-agent-skills-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/agent-skills/README.md
    title: Introduction to Claude Code Agent Skills (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:20:00Z }
status: draft
---
Claude Code has five ways to add behaviour, and each is defined by when it applies. Picking by that behaviour avoids forcing one mechanism to carry every responsibility.[^claude-agent-skills-course]

| Mechanism | What distinguishes it | Use it for |
| --- | --- | --- |
| `CLAUDE.md` | Always loaded | Project-wide rules and constraints |
| [Skill](agent-skill.md) | Matched to the request, loaded on demand | Task-specific knowledge and procedures |
| [Subagent](subagent.md) | Separate execution context | Isolated delegated work or different tool access |
| Hook | Triggered by an event | Repeatable checks or side effects around tool actions |
| MCP server | Supplies external capabilities | Integrations, data sources, tools |

As described in the course.[^claude-agent-skills-course]

Skills extend the current conversation; subagents leave it, work independently, and return a result. Hooks react to events rather than to what a request means. MCP is a capability boundary, not an instruction format.[^claude-agent-skills-course] Slash commands differ from skills in needing explicit invocation, where skills activate from the intent of an ordinary request.[^claude-agent-skills-course]

The mechanisms combine: permanent rules in `CLAUDE.md`, review knowledge in a skill, automatic validation in a hook, an isolated review in a subagent, and external services through MCP.[^claude-agent-skills-course]

## Related

- [When to delegate](when-to-delegate.md): deciding whether work belongs in a subagent.
- Source: [Introduction to Claude Code Agent Skills](../../sources/claude-agent-skills-course.md)

[^claude-agent-skills-course]: Introduction to Claude Code Agent Skills (study guide)
