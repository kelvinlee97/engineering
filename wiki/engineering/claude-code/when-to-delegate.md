---
type: Pattern
title: When to delegate
description: Delegate when only the result matters to the main thread; keep work in one context when its intermediate steps matter.
tags: [claude-code, subagents, agents]
sources:
  - id: claude-subagents-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/subagents/README.md
    title: Introduction to Claude Code Subagents (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:10:00Z }
status: draft
---
The course reduces the choice to one question: **does the intermediate work matter to the main thread?** If only the final result matters, delegate to a [subagent](subagent.md); if the main thread must see or react to what is found along the way, keep the work there.[^claude-subagents-course]

## Where delegation works

| Use case | Why it fits |
| --- | --- |
| Research and exploration, such as locating JWT validation in an unfamiliar codebase | Many files searched, one location and explanation returned[^claude-subagents-course] |
| Code review | Fresh context without the creation history; the system prompt can encode project review standards[^claude-subagents-course] |
| Tasks that need a different system prompt: copywriting (audience, tone, voice), styling (design-system files loaded first) | The difference comes from the instructions and context, which the main conversation lacks[^claude-subagents-course] |

## Anti-patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Empty expert personas ("Python expert") | The main conversation already has that knowledge; isolation helps only with a real difference such as a custom prompt, focused context, or controlled tools[^claude-subagents-course] |
| Sequential pipelines of dependent steps (reproduce → debug → fix) | Each handoff compresses away discoveries the next step needs; pipelines suit only independent tasks[^claude-subagents-course] |
| Test-runner subagents | Diagnosis needs full failure output, and a summary like "tests failed" hides it; the course reports this pattern performed worse among the configurations tested[^claude-subagents-course] |

All three are cases of [context isolation](context-isolation.md) costing more than it saves.

## Related

- [Delegation contract](delegation-contract.md): how to specify the task once you decide to delegate.
- Source: [Introduction to Claude Code Subagents](../../sources/claude-subagents-course.md)

[^claude-subagents-course]: Introduction to Claude Code Subagents (study guide)
