---
type: Service
title: Cloud session
description: A Claude Code session that runs on an Anthropic-managed VM instead of your machine, cloning your repository from GitHub and running after you disconnect.
tags: [claude-code, cloud-sessions]
sources:
  - id: claude-cloud-sessions
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/cloud-sessions/README.md
    title: Claude Code Cloud Sessions
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: claude-projects
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/projects/README.md
    title: Claude Projects, Redesigned
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:40:00Z }
status: draft
---

A cloud session is an ordinary Claude Code session whose machine is not yours: an Anthropic-managed VM that clones your repository from GitHub, keeps running after you close the laptop, and can be picked up later from a browser, a phone, or your own terminal.[^claude-cloud-sessions] Because the machine is not yours, the code has to come from GitHub (see [Claude GitHub App](claude-github-app.md)) and network and secrets need their own policy (see [Cloud environment](cloud-environment.md)).[^claude-cloud-sessions]

## Where one can start

| Surface | How to start |
| --- | --- |
| Browser | claude.ai/code (Claude Code on the web) |
| Mobile | The **Code** tab in the Claude app |
| Desktop app | Choose **Cloud** instead of **Local** |
| Terminal | `claude --cloud "<task>"` |
| Routines | Each scheduled or triggered run is a cloud session |

The starting surface changes nothing about how the session runs.[^claude-cloud-sessions] A session running on your own machine and steered from a phone is Remote Control, a different feature; `--remote-control` does not create a cloud session.[^claude-cloud-sessions] Moving work in and out of the cloud is on [Moving work between terminal and cloud](terminal-cloud-handoff.md).

## Differences from a local session

- Commands that produce text work; terminal-only ones such as `/plugin` and `/resume` do not. Picker commands such as `/model` take their value as an argument (`/model sonnet`), which needs Claude Code v2.1.205+ in the environment.[^claude-cloud-sessions]
- `/compact` and `/context` work; `/clear` does not, so start a new session instead.[^claude-cloud-sessions]
- Cloud sessions set `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` themselves, and it overrides the same variable in your environment; to change compaction, set `CLAUDE_CODE_AUTO_COMPACT_WINDOW` instead.[^claude-cloud-sessions]
- [Subagents](subagent.md) work as they do locally, and `.claude/agents/` definitions are picked up. Agent teams are off unless `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set.[^claude-cloud-sessions]
- To change a setting, set an environment variable on the environment or commit it to `.claude/settings.json`; `/config` in the browser only opens the settings panel.[^claude-cloud-sessions]

## Lifecycle and sharing

A session expires after inactivity and the VM is reclaimed. Reopening it restores the history on a fresh VM, but background work such as subagents and shell commands is not restored.[^claude-cloud-sessions] A session also counts as inactive while it waits for you to approve an MCP tool call or sign in to an MCP server.[^claude-cloud-sessions]

Sharing differs by plan: Team and Enterprise choose Private or Team with repository access verification on by default; Pro and Max choose Private or Public (any logged-in claude.ai user) with verification off by default. Sessions can contain private code and credentials, so check before sharing.[^claude-cloud-sessions]

## Limits

- Rate limits are shared with all other Claude usage on the account; there is no separate VM charge.[^claude-cloud-sessions]
- Cloning and pull requests need GitHub. Other remotes can be sent as a bundle but results cannot be pushed back.[^claude-cloud-sessions]
- An organization IP allowlist makes Anthropic-hosted sessions fail with an authentication error, because they call the API from Anthropic's network.[^claude-cloud-sessions]
- Organizations with Zero Data Retention cannot use cloud sessions.[^claude-cloud-sessions]

## Related

- [Pull request auto-fix](pr-auto-fix.md)
- [Claude Projects](claude-projects.md): each project thread runs as a cloud session, and local-only workflows are not supported.[^claude-projects]
- Source: [Claude Projects, Redesigned](../../sources/claude-projects.md)
- Source: [Claude Code Cloud Sessions](../../sources/claude-cloud-sessions.md)

[^claude-cloud-sessions]: Claude Code Cloud Sessions
[^claude-projects]: Claude Projects, Redesigned
