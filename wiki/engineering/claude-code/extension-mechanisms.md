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
  - id: ai-native-sdlc-playbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-sdlc-playbook/README.md
    title: The AI-Native SDLC Playbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: gh-600-study-notes
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-agentic-ai-developer/README.md
    title: "GitHub Certified: Agentic AI Developer (study notes)"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T16:05:00Z }
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

## Keeping them maintainable

The AI-native SDLC playbook recommends a short, reviewed `CLAUDE.md` holding build and test commands, conventions, architecture, and recurring mistakes, with reusable organization-wide policy in skills, and treats instructions, skills, hooks, and permission rules as reviewed, version-controlled code.[^ai-native-sdlc-playbook]

The GH-600 course describes hooks as policy enforcement that does not depend on the model's judgment: a pre-tool-use hook can block an unsafe command, a post-action hook can write an audit log, and an error hook can escalate.[^gh-600-study-notes] (Its example uses GitHub Copilot agents' `.github/hooks/`; Claude Code hooks fill the same role.)

## Related

- Source: [GitHub Certified: Agentic AI Developer](../../sources/gh-600-study-notes.md)
- Source: [The AI-Native SDLC Playbook](../../sources/ai-native-sdlc-playbook.md)
- [When to delegate](when-to-delegate.md): deciding whether work belongs in a subagent.
- Source: [Introduction to Claude Code Agent Skills](../../sources/claude-agent-skills-course.md)

[^claude-agent-skills-course]: Introduction to Claude Code Agent Skills (study guide)
[^ai-native-sdlc-playbook]: The AI-Native SDLC Playbook
[^gh-600-study-notes]: GitHub Certified: Agentic AI Developer (study notes)
