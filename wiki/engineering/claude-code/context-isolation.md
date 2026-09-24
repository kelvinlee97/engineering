---
type: Concept
title: Context isolation
description: Keeping an agent's intermediate work out of the main context window, at the cost of losing whatever the summary leaves out.
tags: [claude-code, context-engineering, agents]
sources:
  - id: claude-subagents-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/subagents/README.md
    title: Introduction to Claude Code Subagents (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T16:10:00Z }
status: draft
---
Context isolation means running noisy intermediate work (file reads, searches, tool output) somewhere other than the main conversation, so only the conclusion comes back. In Claude Code, a [subagent](subagent.md) is the mechanism.

## What it protects

Every exchange and tool result uses up the main context window (the finite amount of text the model can hold at once). A large investigation can fill it with material that is no longer useful; moving that exploration into a separate context keeps the main one clear.[^claude-subagents-course]

## What it costs

The parent loses visibility into how the conclusion was reached and into anything discovered but left out of the summary.[^claude-subagents-course] Two consequences follow in the course:

- The result must be specified in advance, including obstacles, or the main thread has to rediscover them. See [Delegation contract](delegation-contract.md).[^claude-subagents-course]
- Chains of dependent steps lose information at each handoff, so they belong in one context. See [When to delegate](when-to-delegate.md).[^claude-subagents-course]

## A side benefit: fresh context

A reviewer subagent starts without the conversation history that produced the code, so it can review more critically than the main conversation that helped write it.[^claude-subagents-course]

## Related

- [Progressive disclosure](progressive-disclosure.md): saving context by not loading material until needed.
- Source: [Introduction to Claude Code Subagents](../../sources/claude-subagents-course.md)

[^claude-subagents-course]: Introduction to Claude Code Subagents (study guide)
