---
type: Tool
title: Claude Code on GitHub
description: The Claude GitHub App, the Claude Code GitHub Actions workflow, and PR auto-fix, and how they fit together.
tags:
- claude-code
- github
- ci
aliases:
- engineering/claude-code/claude-github-app
- engineering/claude-code/claude-code-github-actions
- engineering/claude-code/pr-auto-fix
sources:
- id: claude-cloud-sessions
  resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/cloud-sessions/README.md
  title: Claude Code Cloud Sessions
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: claude-github-actions
  resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-actions/README.md
  title: Claude Code GitHub Actions
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
Claude reaches GitHub in three connected ways: the Claude GitHub App grants repository access, Claude Code GitHub Actions runs Claude inside a workflow job, and PR auto-fix lets a cloud session answer CI failures and review comments. The app is the common gate; the other two depend on it.

## Claude GitHub App

The Claude GitHub App is how several Claude features get access to GitHub repositories. Which features you get depends on whether the app is installed on a repository, not only on how you signed in.[^claude-cloud-sessions]

### Two ways to connect cloud sessions

| Method | How | Reach |
| --- | --- | --- |
| GitHub App | Authorize it during web onboarding | Public repositories, plus private ones the app is installed on |
| `/web-setup` | Sends your local `gh` CLI token to your Claude account | Any repository your `gh` token can reach |

Features that need the app on the repository whichever method you used: [pull request auto-fix](#pull-request-auto-fix) and project threads. *Quick web setup*, the organization setting that exposes `/web-setup`, is off by default on Team and Enterprise; an Owner enables it under **Admin settings > Claude Code**.

The note's author reads this as the app being the real gate: connecting with `/web-setup` because it is faster quietly opts out of the automation features. (Analysis from the source.)[^claude-cloud-sessions]

### Permission scope

The app serves several Claude features, so its permissions are broader than [Claude Code GitHub Actions](#claude-code-github-actions) alone needs; the Action relies on read and write access to Contents, Issues, and Pull requests. An organization can create a custom GitHub App limited to those, but it does not replace the official app for Claude Code Review or web auto-fix.[^claude-github-actions]

## Claude Code GitHub Actions

Claude Code GitHub Actions runs Claude Code as a step in a GitHub Actions job (`anthropics/claude-code-action@v1`). An event starts the run, actor checks decide whether it may continue, and GitHub and Claude tool permissions limit what it can do. Typical uses: turning an issue into a pull request, fixing a bug asked for in a comment, answering questions, reviewing with a skill, and scheduled reports.[^claude-github-actions]

### Two modes

The presence of the `prompt` input picks the mode; v1 has no `mode` input.

| Mode | When | Behaviour |
| --- | --- | --- |
| Interactive | No `prompt` | Waits for the trigger phrase (default `@claude`) in comments, reviews, or a new issue, and replies there |
| Automation | `prompt` set | Runs on the configured event, such as a pull request or schedule, and writes to the workflow log by default |

Before Claude starts, the actor must have write access (unless listed in `allowed_non_write_users` with a custom `github_token`), and bots are rejected unless listed in `allowed_bots`. A scheduled run is attributed to an actor, often whoever last edited the cron line.[^claude-github-actions]

### Permissions

What a run can do is the intersection of three layers: who may start it (actor checks), what GitHub accepts (the job's `permissions`), and what Claude may invoke (`--allowedTools`, `permissions.allow` in settings, or a skill's `allowed-tools`). A plain automation prompt has no shell or GitHub API tools until the workflow grants them.[^claude-github-actions] More on this pattern: [Least-privilege tool access](subagents.md#least-privilege-tool-access).

### Setup and authentication

Both setup paths need repository admin. Quick setup runs `/install-github-app` in Claude Code (github.com only), which installs the app, stores a secret, and prepares a workflow pull request; manual setup installs the [Claude GitHub App](#claude-github-app), adds a secret, and copies `examples/claude.yml`.

| Authentication | Secret or config | Fits |
| --- | --- | --- |
| Claude API | `ANTHROPIC_API_KEY` | API billing and shared automation |
| Subscription | `CLAUDE_CODE_OAUTH_TOKEN` | Tied to the token creator's plan; a poor shared credential |
| Workload identity federation | No long-lived key; `id-token: write` | Organization deployments |
| Cloud provider | Provider OIDC; `use_bedrock`, `use_vertex`, `use_foundry` | Inference through Bedrock, Google Cloud, or Foundry |

*Source for this section.*[^claude-github-actions]

### Operating it

- Keep credentials in GitHub Secrets; deleting a secret does not revoke the key, so revoke it at the issuer.
- Treat issue and comment text as untrusted ([prompt injection](auto-mode.md#prompt-injection)), and require human review before merging generated changes.
- Bound cost with specific requests, a concise `CLAUDE.md`, `--max-turns`, workflow timeouts, and concurrency controls.
- If CI does not run after Claude pushes, do not force the default `GITHUB_TOKEN` when app authentication is intended, and make sure CI listens to the resulting event. Public-repository fork workflows do not get secrets.
- Migrating from `@beta`: switch to `@v1`, drop `mode`, rename `direct_prompt` to `prompt`, and move options into `claude_args` (`custom_instructions` becomes `--append-system-prompt`).[^claude-github-actions]

## Pull request auto-fix

Auto-fix lets Claude subscribe to activity on a pull request and respond to CI failures and review comments from a [cloud session](cloud-sessions.md#what-a-cloud-session-is). For each event Claude investigates, then pushes a fix when it is confident and the fix does not conflict with earlier instructions, asks you when the request is ambiguous or architecturally significant, or notes and skips duplicates.[^claude-cloud-sessions]

### Turning it on

- PR created in a cloud session: select **Auto-fix** in the session's CI status bar.
- From the terminal: `/autofix-pr` on the PR's branch spawns a cloud session and enables it.
- From mobile, or for any existing PR: ask Claude in words, or paste the PR URL into a session.

It is a per-PR toggle and requires the [Claude GitHub App](#claude-github-app) on the repository.[^claude-cloud-sessions]

### Caveats

1. **Merge conflicts are invisible to it.** GitHub sends no webhook when the base branch advances; open the session and ask Claude to rebase.
2. **Replies post under your GitHub account**, labelled as coming from Claude Code.
3. **Replies can trigger comment-driven automation** such as Atlantis, Terraform Cloud, or Actions on `issue_comment`. Review that automation first, and consider leaving auto-fix off where a comment can deploy infrastructure.[^claude-cloud-sessions]

## Related

- [Moving work between terminal and cloud](cloud-sessions.md#moving-work-between-terminal-and-cloud): without the app, `--cloud` uploads a bundle instead of cloning.

[^claude-cloud-sessions]: [Claude Code Cloud Sessions](../../sources/claude-cloud-sessions.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Claude/cloud-sessions/README.md)
[^claude-github-actions]: [Claude Code GitHub Actions](../../sources/claude-github-actions.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Claude/github-actions/README.md)
