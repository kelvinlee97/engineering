---
type: Source Summary
title: How Claude Code Auto Mode Works (video summary)
description: Summary of Claude's 2026-08-04 video explaining how Auto Mode reviews higher-risk actions with a separate classifier.
tags: [claude-code, auto-mode, security]
sources:
  - id: claude-auto-mode
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/auto-mode/README.md
    title: How Claude Code Auto Mode Works
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:50:00Z }
status: draft
---

A note in this repository, `Claude/auto-mode/README.md`, summarizing the 5:41 video *How auto mode works with Claude Code*, published by Claude on 2026-08-04, from its complete auto-generated English transcript.[^claude-auto-mode]

## Takeaways

- Claude does not approve its own actions in Auto Mode; a separate classifier reviews higher-risk ones. See [Auto Mode](../engineering/claude-code/auto-mode.md#how-auto-mode-works).
- Permission rules stay the hard enforcement layer; classifier guidance is not deterministic. See [Least-privilege tool access](../engineering/claude-code/subagents.md#least-privilege-tool-access).
- A server-side probe plus the classifier form two layers against prompt injection.[^claude-auto-mode] See [Prompt injection](../engineering/claude-code/auto-mode.md#prompt-injection).

[^claude-auto-mode]: How Claude Code Auto Mode Works, [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/Claude/auto-mode/README.md)
