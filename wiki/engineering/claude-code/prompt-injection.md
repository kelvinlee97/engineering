---
type: Concept
title: Prompt injection
description: Instructions hidden in content an agent reads, such as web pages, files, or issue comments, that try to redirect it away from the user's request.
tags: [security, agents, claude-code]
sources:
  - id: claude-auto-mode
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/auto-mode/README.md
    title: How Claude Code Auto Mode Works
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: claude-github-actions
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-actions/README.md
    title: Claude Code GitHub Actions
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:50:00Z }
status: draft
---

Prompt injection is when content an agent reads (web pages, source files, tool results) carries hidden instructions meant to pull it away from the user's original request.[^claude-auto-mode] Any agent that reads text it did not write is exposed.

## Defenses described in the sources

| Setting | Defense |
| --- | --- |
| Claude Code [Auto Mode](auto-mode.md) | A server-side probe scans tool results and flags suspicious instructions, and the classifier checks that Claude's next action still matches the user's intent; an attack has to pass both.[^claude-auto-mode] |
| [Claude Code GitHub Actions](claude-code-github-actions.md) | Treat issue text, comments, and changed repository content as untrusted input; grant only the needed permissions and tools; require human review and branch protection before merging.[^claude-github-actions] |

Anthropic reports that prompt-injection attack success fell to zero in its evaluations with both the probe and Auto Mode on. The note stresses this is Anthropic's internal evaluation, not a guarantee for every environment.[^claude-auto-mode]

## Related

- [Least-privilege tool access](least-privilege-tool-access.md): limits what a successful injection can do.
- Source: [How Claude Code Auto Mode Works](../../sources/claude-auto-mode.md)
- Source: [Claude Code GitHub Actions](../../sources/claude-github-actions.md)

[^claude-auto-mode]: How Claude Code Auto Mode Works
[^claude-github-actions]: Claude Code GitHub Actions
