---
type: Tool
title: Claude Code GitHub Actions
description: "The anthropics/claude-code-action workflow step that runs Claude Code inside a GitHub Actions job, triggered by @claude mentions or a fixed prompt."
tags: [claude-code, github-actions, github, ci]
sources:
  - id: claude-github-actions
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-actions/README.md
    title: Claude Code GitHub Actions
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:50:00Z }
status: draft
---

Claude Code GitHub Actions runs Claude Code as a step in a GitHub Actions job (`anthropics/claude-code-action@v1`). An event starts the run, actor checks decide whether it may continue, and GitHub and Claude tool permissions limit what it can do.[^claude-github-actions] Typical uses: turning an issue into a pull request, fixing a bug asked for in a comment, answering questions, reviewing with a skill, and scheduled reports.[^claude-github-actions]

## Two modes

The presence of the `prompt` input picks the mode; v1 has no `mode` input.[^claude-github-actions]

| Mode | When | Behaviour |
| --- | --- | --- |
| Interactive | No `prompt` | Waits for the trigger phrase (default `@claude`) in comments, reviews, or a new issue, and replies there |
| Automation | `prompt` set | Runs on the configured event, such as a pull request or schedule, and writes to the workflow log by default |

[^claude-github-actions]

Before Claude starts, the actor must have write access (unless listed in `allowed_non_write_users` with a custom `github_token`), and bots are rejected unless listed in `allowed_bots`. A scheduled run is attributed to an actor, often whoever last edited the cron line.[^claude-github-actions]

## Permissions

What a run can do is the intersection of three layers: who may start it (actor checks), what GitHub accepts (the job's `permissions`), and what Claude may invoke (`--allowedTools`, `permissions.allow` in settings, or a skill's `allowed-tools`). A plain automation prompt has no shell or GitHub API tools until the workflow grants them.[^claude-github-actions] More on this pattern: [Least-privilege tool access](least-privilege-tool-access.md).

## Setup and authentication

Both setup paths need repository admin. Quick setup runs `/install-github-app` in Claude Code (github.com only), which installs the app, stores a secret, and prepares a workflow pull request; manual setup installs the [Claude GitHub App](claude-github-app.md), adds a secret, and copies `examples/claude.yml`.[^claude-github-actions]

| Authentication | Secret or config | Fits |
| --- | --- | --- |
| Claude API | `ANTHROPIC_API_KEY` | API billing and shared automation |
| Subscription | `CLAUDE_CODE_OAUTH_TOKEN` | Tied to the token creator's plan; a poor shared credential |
| Workload identity federation | No long-lived key; `id-token: write` | Organization deployments |
| Cloud provider | Provider OIDC; `use_bedrock`, `use_vertex`, `use_foundry` | Inference through Bedrock, Google Cloud, or Foundry |

[^claude-github-actions]

## Operating it

- Keep credentials in GitHub Secrets; deleting a secret does not revoke the key, so revoke it at the issuer.[^claude-github-actions]
- Treat issue and comment text as untrusted ([prompt injection](prompt-injection.md)), and require human review before merging generated changes.[^claude-github-actions]
- Bound cost with specific requests, a concise `CLAUDE.md`, `--max-turns`, workflow timeouts, and concurrency controls.[^claude-github-actions]
- If CI does not run after Claude pushes, do not force the default `GITHUB_TOKEN` when app authentication is intended, and make sure CI listens to the resulting event. Public-repository fork workflows do not get secrets.[^claude-github-actions]
- Migrating from `@beta`: switch to `@v1`, drop `mode`, rename `direct_prompt` to `prompt`, and move options into `claude_args` (`custom_instructions` becomes `--append-system-prompt`).[^claude-github-actions]

## Related

- [Pull request auto-fix](pr-auto-fix.md): the cloud-session way to respond to PR activity.
- Source: [Claude Code GitHub Actions](../../sources/claude-github-actions.md)

[^claude-github-actions]: Claude Code GitHub Actions
