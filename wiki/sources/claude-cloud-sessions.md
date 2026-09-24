---
type: Source Summary
title: Claude Code Cloud Sessions (summary of the official docs)
description: Summary of Anthropic's Use Claude Code in the cloud documentation, reviewed on 2026-09-18.
tags: [claude-code, cloud-sessions]
sources:
  - id: claude-cloud-sessions
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/cloud-sessions/README.md
    title: Claude Code Cloud Sessions
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:30:00Z }
status: draft
---

A note in this repository, `Claude/cloud-sessions/README.md`, summarizing Anthropic's *Use Claude Code in the cloud* documentation page. It was reviewed on 2026-09-18, when cloud sessions were a research preview for Pro, Max, and Team users and for Enterprise users with premium or Chat + Claude Code seats.[^claude-cloud-sessions] Sections the note marks as analysis are its author's reading, not documentation claims; this wiki keeps that label.

## Takeaways

- A cloud session is an ordinary Claude Code session running on an Anthropic-managed VM that clones the repository from GitHub.[^claude-cloud-sessions] See [Cloud session](../engineering/claude-code/cloud-session.md).
- Network access, environment variables, and setup scripts come from a saved cloud environment.[^claude-cloud-sessions] See [Cloud environment](../engineering/claude-code/cloud-environment.md).
- Work moves terminal → cloud with `--cloud` and cloud → terminal with `--teleport`; the CLI cannot push a running session up.[^claude-cloud-sessions] See [Moving work between terminal and cloud](../engineering/claude-code/terminal-cloud-handoff.md).
- Auto-fix watches a pull request and responds to CI failures and review comments, but cannot see merge conflicts.[^claude-cloud-sessions] See [Pull request auto-fix](../engineering/claude-code/pr-auto-fix.md).
- The Claude GitHub App, not the sign-in method, is what enables auto-fix and project threads.[^claude-cloud-sessions] See [Claude GitHub App](../engineering/claude-code/claude-github-app.md).

[^claude-cloud-sessions]: Claude Code Cloud Sessions
