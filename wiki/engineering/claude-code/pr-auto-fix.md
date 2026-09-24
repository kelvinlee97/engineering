---
type: Tool
title: Pull request auto-fix
description: A Claude Code cloud feature that watches a pull request and responds to CI failures and review comments, with known blind spots.
tags: [claude-code, cloud-sessions, github]
sources:
  - id: claude-cloud-sessions
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/cloud-sessions/README.md
    title: Claude Code Cloud Sessions
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:30:00Z }
status: draft
---

Auto-fix lets Claude subscribe to activity on a pull request and respond to CI failures and review comments from a [cloud session](cloud-session.md).[^claude-cloud-sessions] For each event Claude investigates, then pushes a fix when it is confident and the fix does not conflict with earlier instructions, asks you when the request is ambiguous or architecturally significant, or notes and skips duplicates.[^claude-cloud-sessions]

## Turning it on

- PR created in a cloud session: select **Auto-fix** in the session's CI status bar.
- From the terminal: `/autofix-pr` on the PR's branch spawns a cloud session and enables it.
- From mobile, or for any existing PR: ask Claude in words, or paste the PR URL into a session.

[^claude-cloud-sessions] It is a per-PR toggle and requires the [Claude GitHub App](claude-github-app.md) on the repository.[^claude-cloud-sessions]

## Caveats

1. **Merge conflicts are invisible to it.** GitHub sends no webhook when the base branch advances; open the session and ask Claude to rebase.[^claude-cloud-sessions]
2. **Replies post under your GitHub account**, labelled as coming from Claude Code.[^claude-cloud-sessions]
3. **Replies can trigger comment-driven automation** such as Atlantis, Terraform Cloud, or Actions on `issue_comment`. Review that automation first, and consider leaving auto-fix off where a comment can deploy infrastructure.[^claude-cloud-sessions]

## Related

- Source: [Claude Code Cloud Sessions](../../sources/claude-cloud-sessions.md)

[^claude-cloud-sessions]: Claude Code Cloud Sessions
