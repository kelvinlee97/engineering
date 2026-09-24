---
type: Pattern
title: Least-privilege tool access
description: Grant an agent only the tools its job requires, starting from what it must do.
tags: [claude-code, agents, security]
sources:
  - id: claude-subagents-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/subagents/README.md
    title: Introduction to Claude Code Subagents (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:10:00Z }
status: draft
---
Least privilege means starting from what an agent must do and granting only the tools that job requires. For subagents, the course gives two reasons: fewer unintended side effects, and a clearer responsibility for each subagent.[^claude-subagents-course]

## Tools by role

| Subagent role | Course-recommended access |
| --- | --- |
| Research, read-only | `Glob`, `Grep`, `Read` |
| Code reviewer | Read tools plus `Bash` for commands such as `git diff`; no edit or write |
| Styling or code modification | Add edit and write, because modification is the job |

As described in the course.[^claude-subagents-course]

The `/agents` creation screen groups tools as read-only, edit, execution, MCP, and other. A reviewer normally needs to read, may still use execution to inspect pending changes, and should not get edit or write access.[^claude-subagents-course] The chosen list is stored in the `tools` field of the [subagent configuration file](subagent-configuration.md).

## Related

- [Delegation contract](delegation-contract.md): tool limits are one of the course's four characteristics of an effective subagent.
- Source: [Introduction to Claude Code Subagents](../../sources/claude-subagents-course.md)

[^claude-subagents-course]: Introduction to Claude Code Subagents (study guide)
