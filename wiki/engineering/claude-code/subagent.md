---
type: Concept
title: Subagent
description: A worker agent that Claude Code hands a bounded task to, which runs in its own context and returns only a focused result.
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
A subagent is a specialized assistant that Claude Code delegates one task to. It works in a separate conversation, returns a short summary to the main conversation (the parent), and its own conversation is then discarded.[^claude-subagents-course]

## How it runs

A subagent receives two inputs: a system prompt from its [configuration file](subagent-configuration.md), which defines its role, and a task description the parent writes from the user's request.[^claude-subagents-course] Its file reads, searches, edits, and tool results stay in its own context; the parent keeps only the original request and the returned summary.[^claude-subagents-course] Why that matters, and what it costs, is on [Context isolation](context-isolation.md).

```mermaid
flowchart TD
    accTitle: Subagent delegation lifecycle
    accDescr: The parent defines a bounded task, the subagent investigates with its permitted tools and returns a focused result, and the parent verifies it. The subagent's detailed context is discarded.
    U[User request] --> P[Parent defines bounded task and expected output]
    P --> S[Subagent receives task and system prompt]
    S --> T[Investigates with permitted tools]
    T --> R[Returns focused result and obstacles]
    R --> V[Parent verifies and uses the result]
    S -.-> X[Detailed context discarded]
```

The parent only ever sees the result box, so the [delegation contract](delegation-contract.md) has to say what that result contains.

## Built-in and custom subagents

| Subagent | Purpose in the course |
| --- | --- |
| General purpose | Multi-step tasks that need both exploration and action |
| Explore | Fast searching and navigation of codebases |
| Plan | Codebase research and analysis during plan mode |

Claude Code also supports custom subagents with their own system prompts and tool access.[^claude-subagents-course]

## Example

To find which service handles refunds in an unfamiliar codebase, Claude might read around 15 files, run searches, and trace function calls. Done in the main conversation, all of that lands in its context although the wanted output is one fact; an Explore subagent keeps the investigation isolated and returns only the answer.[^claude-subagents-course]

## Related

- [When to delegate](when-to-delegate.md): the decision rule and the anti-patterns.
- [Least-privilege tool access](least-privilege-tool-access.md): which tools a subagent should get.
- Source: [Introduction to Claude Code Subagents](../../sources/claude-subagents-course.md)

[^claude-subagents-course]: Introduction to Claude Code Subagents (study guide)
