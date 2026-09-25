---
type: Source Summary
title: Claude Code GitHub Actions (summary of the official docs)
description: "Summary of Anthropic's Claude Code GitHub Actions documentation for anthropics/claude-code-action@v1, reviewed on 2026-09-15."
tags: [claude-code, github-actions, github]
sources:
  - id: claude-github-actions
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-actions/README.md
    title: Claude Code GitHub Actions
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:50:00Z }
status: draft
---

A note in this repository, `Claude/github-actions/README.md`, summarizing Anthropic's Claude Code GitHub Actions documentation for `anthropics/claude-code-action@v1`, reviewed on 2026-09-15. It covers setup, execution modes, permissions, authentication, security, cost, and troubleshooting.[^claude-github-actions]

## Takeaways

- The Action is a constrained agent inside a GitHub Actions job: an event starts it, actor checks gate it, and permissions limit it. See [Claude Code GitHub Actions](../engineering/claude-code/github-integration.md#claude-code-github-actions).
- Effective capability is the intersection of actor checks, job permissions, and allowed tools. See [Least-privilege tool access](../engineering/claude-code/subagents.md#least-privilege-tool-access).
- The official [Claude GitHub App](../engineering/claude-code/github-integration.md#claude-github-app) has broader permissions than the Action alone needs.[^claude-github-actions]

[^claude-github-actions]: Claude Code GitHub Actions, [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/Claude/github-actions/README.md)
