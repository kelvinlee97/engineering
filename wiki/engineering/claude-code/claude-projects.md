---
type: Tool
title: Claude Projects
description: In the September 2026 redesign, a Claude project is one long-running conversation whose coordinator splits a goal into parallel threads sharing memory and a library.
tags: [claude-code, projects, agents]
sources:
  - id: claude-projects
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/projects/README.md
    title: Claude Projects, Redesigned
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: claude-cloud-sessions
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/cloud-sessions/README.md
    title: Claude Code Cloud Sessions
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:40:00Z }
status: draft
---

In the redesign announced on 2026-09-17, a Claude project stops being a folder of instructions and files and becomes one long-running conversation. You state a goal; Claude splits it into threads, runs them as parallel cloud sessions, and assembles the results.[^claude-projects] The source was reconstructed from secondary coverage; see the [source summary](../../sources/claude-projects.md).

## What changed

| | Old Projects | Redesigned Projects |
| --- | --- | --- |
| Shape | A folder of files and custom instructions | One ongoing conversation |
| Who splits the work | You, across separate chats | Claude scopes and delegates |
| Where work runs | The chat you are in | Parallel [cloud sessions](cloud-session.md), one per thread |
| Context between units | You re-paste it | Shared project memory |
| Outputs | Scattered across chats | Collected in the project library |
| After you close the laptop | Nothing runs | Threads keep running |

As described in the announcement.[^claude-projects]

## The pieces

- **Coordinator:** Claude in the project conversation. It scopes the request, decides what becomes a thread, delegates, reviews outputs, and assembles the result.[^claude-projects]
- **Threads:** each runs as a separate cloud session, in parallel, and keeps going after you disconnect.[^claude-projects] Each repository a thread clones needs the [Claude GitHub App](claude-github-app.md).[^claude-cloud-sessions]
- **Memory:** shared across threads; every thread reads and writes it. It also holds your working style, such as how often to check in and how detailed updates should be.[^claude-projects]
- **Library:** the files you add and the artifacts Claude produces, so later work starts from earlier work.[^claude-projects]

## Availability at announcement

Beta from 2026-09-17: Pro or Max, Claude Code (desktop and web) only, cloud sessions required, and only for accounts without existing projects on web or desktop. Announced rollout order: more Claude Code users, then the rest of Claude, then Team and Enterprise.[^claude-projects]

## Analysis from the source

The note's author argues that shared memory is what makes delegation cheap, since a thread no longer starts from what you pasted; that review risk moves into the assembled result, where the seams between threads are hidden; and that the check-in and verbosity settings are the only throttle on an unattended system.[^claude-projects] Compare [subagents](subagent.md), which delegate within a single session.[^claude-projects]

## Related

- [Claude Managed Agents](claude-managed-agents.md): the API-side option for long-running asynchronous work.
- Source: [Claude Projects, Redesigned](../../sources/claude-projects.md)

[^claude-projects]: Claude Projects, Redesigned
[^claude-cloud-sessions]: Claude Code Cloud Sessions
