---
type: Configuration
title: Cloud environment
description: The saved configuration that sets network access, environment variables, and setup scripts for Claude Code cloud sessions.
tags: [claude-code, cloud-sessions, security]
sources:
  - id: claude-cloud-sessions
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/cloud-sessions/README.md
    title: Claude Code Cloud Sessions
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:30:00Z }
status: draft
---

A cloud environment is a saved configuration that every [cloud session](cloud-session.md) runs inside. It controls three things: network access, environment variables, and setup scripts.[^claude-cloud-sessions]

## Defaults

With no environment yet, onboarding sets up a **Default** environment with **Trusted** network access, creating it or prompting you depending on plan. The same environments apply to every surface, plus Claude Tag and routines; Claude Tag channel sessions use organization-level environments only.[^claude-cloud-sessions]

The network policy is the setting most likely to surprise: a blocked domain simply cannot be reached, and the failure shows up inside the session as a proxy `403` or an egress-blocked error, not as a configuration warning.[^claude-cloud-sessions]

## Anthropic-hosted versus self-hosted

Sessions can run in a self-hosted environment on your own infrastructure, which moves several guarantees to you:[^claude-cloud-sessions]

| Layer | Anthropic-hosted | Self-hosted |
| --- | --- | --- |
| Isolation | One Anthropic-managed VM per session | Your deployment's responsibility |
| Network | Limited by default, can be disabled; a default allowed-domain list applies | You restrict egress at your own boundary |
| Git credentials | Kept outside the sandbox; a proxy authenticates with scoped credentials | Supplied by your deployment |
| API credentials | On Pro and Max, keys stay outside the sandbox and are attached after requests leave it | Not available (nor yet on Team or Enterprise) |

Even with network access disabled, Claude Code can still reach the Anthropic API, which may allow data to leave the VM: disabled network is not an air gap.[^claude-cloud-sessions]

## Related

- [Least-privilege tool access](least-privilege-tool-access.md)
- Source: [Claude Code Cloud Sessions](../../sources/claude-cloud-sessions.md)

[^claude-cloud-sessions]: Claude Code Cloud Sessions
