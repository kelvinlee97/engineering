---
type: Service
title: Claude GitHub App
description: The GitHub App that gives Claude features repository access, and which features depend on it rather than on other sign-in methods.
tags: [claude-code, github, security]
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
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:50:00Z }
status: draft
---

The Claude GitHub App is how several Claude features get access to GitHub repositories. Which features you get depends on whether the app is installed on a repository, not only on how you signed in.[^claude-cloud-sessions]

## Two ways to connect cloud sessions

| Method | How | Reach |
| --- | --- | --- |
| GitHub App | Authorize it during web onboarding | Public repositories, plus private ones the app is installed on |
| `/web-setup` | Sends your local `gh` CLI token to your Claude account | Any repository your `gh` token can reach |

[^claude-cloud-sessions]

Features that need the app on the repository whichever method you used: [pull request auto-fix](pr-auto-fix.md) and project threads.[^claude-cloud-sessions] *Quick web setup*, the organization setting that exposes `/web-setup`, is off by default on Team and Enterprise; an Owner enables it under **Admin settings > Claude Code**.[^claude-cloud-sessions]

The note's author reads this as the app being the real gate: connecting with `/web-setup` because it is faster quietly opts out of the automation features. (Analysis from the source.)[^claude-cloud-sessions]

## Permission scope

The app serves several Claude features, so its permissions are broader than [Claude Code GitHub Actions](claude-code-github-actions.md) alone needs; the Action relies on read and write access to Contents, Issues, and Pull requests. An organization can create a custom GitHub App limited to those, but it does not replace the official app for Claude Code Review or web auto-fix.[^claude-github-actions]

## Related

- Source: [Claude Code GitHub Actions](../../sources/claude-github-actions.md)
- [Moving work between terminal and cloud](terminal-cloud-handoff.md): without the app, `--cloud` uploads a bundle instead of cloning.
- Source: [Claude Code Cloud Sessions](../../sources/claude-cloud-sessions.md)

[^claude-cloud-sessions]: Claude Code Cloud Sessions
[^claude-github-actions]: Claude Code GitHub Actions
