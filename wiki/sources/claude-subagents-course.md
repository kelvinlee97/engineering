---
type: Source Summary
title: Introduction to Claude Code Subagents (course study guide)
description: Study guide covering all four lessons of Anthropic Academy's Introduction to subagents course.
tags: [claude-code, subagents, course]
sources:
  - id: claude-subagents-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/subagents/README.md
    title: Introduction to Claude Code Subagents (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:10:00Z }
status: draft
---
A study guide to Anthropic Academy's four-lesson *Introduction to subagents* course, written in this repository as `Claude/subagents/README.md`. It is an original summary, not a transcript.[^claude-subagents-course]

## Scope and coverage

| Lesson | Coverage in the guide |
| --- | --- |
| What are subagents? | Article and video subtitles read in full |
| Creating a subagent | Article read in full; the video was blocked by a copyright claim on 2026-08-05, so no transcript was used |
| Designing effective subagents | Article and video subtitles read in full |
| Using subagents effectively | Article and video subtitles read in full |

All course material was read on 2026-08-05.[^claude-subagents-course] Upstream sources are the four course articles on anthropic.skilljar.com and their YouTube videos; this wiki cites the study guide, not the course directly.

## Takeaways

- A subagent trades visibility for a clean main context: its investigation stays isolated and only a summary returns. See [Subagent](../engineering/claude-code/subagents.md#what-a-subagent-is) and [Context isolation](../engineering/claude-code/subagents.md#context-isolation).
- The course calls a defined output format the most important design improvement, because it gives the subagent a stopping condition. See [Delegation contract](../engineering/claude-code/subagents.md#delegation-contract).
- The single deciding question is whether the intermediate work matters to the main thread. See [When to delegate](../engineering/claude-code/subagents.md#when-to-delegate).
- Tools should be the minimum the role needs. See [Least-privilege tool access](../engineering/claude-code/subagents.md#least-privilege-tool-access).
- Custom subagents are Markdown files with YAML frontmatter, created with `/agents`.[^claude-subagents-course] See [Subagent configuration file](../engineering/claude-code/subagents.md#subagent-configuration-file).

[^claude-subagents-course]: Introduction to Claude Code Subagents (study guide), [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/Claude/subagents/README.md)
