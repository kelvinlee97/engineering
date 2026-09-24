---
type: Service
title: Claude Managed Agents
description: An Anthropic-hosted agent harness that runs the agent loop, sandbox, and tools for long-running tasks, driven by events instead of your own runtime.
tags: [claude-api, managed-agents, agents]
sources:
  - id: claude-managed-agents
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/managed-agents/README.md
    title: Claude Managed Agents
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:40:00Z }
status: draft
---

Claude Managed Agents is a hosted agent harness: Anthropic runs the agent loop, the sandbox, and tool execution, and your application sends events into a running session instead of implementing its own runtime.[^claude-managed-agents] It was in beta at review time (2026-09-15); every request needs the `managed-agents-2026-04-01` header, which the SDK sets.[^claude-managed-agents]

## Building blocks

| Concept | What it is |
| --- | --- |
| Agent | Model, system prompt, tools, MCP servers, and [skills](agent-skill.md); created once and referenced by ID |
| Environment | Where sessions run: an Anthropic-managed cloud sandbox or a self-hosted one |
| Session | A running agent instance in an environment, doing one task |
| Events | Messages between your application and the agent: user turns, tool results, status updates |

As described in the documentation.[^claude-managed-agents] You create an agent and an environment, start a session, and send events; Claude runs tools on its own and streams results back over server-sent events. Event history is stored server-side, so a session survives pauses, and you can steer or interrupt it with further events.[^claude-managed-agents]

Built-in tools are Bash, file operations (read, write, edit, glob, grep), web search and fetch with optional domain allow or block lists, and MCP servers.[^claude-managed-agents]

## When it fits

Use it for long-running work (minutes or hours across many tool calls), managed or self-hosted sandboxes, stateful sessions with a persistent filesystem, and cron-scheduled runs. Stay on the Messages API when you need a custom agent loop or control over every model call.[^claude-managed-agents]

## Constraints at review time

- Access was on by default for API accounts; MCP tunnels and "dreaming" were a narrower research preview.[^claude-managed-agents]
- History, sandbox state, and outputs persist server-side, so it was not eligible for Zero Data Retention or HIPAA BAA coverage. Sessions and uploaded files can be deleted through the API.[^claude-managed-agents]
- Behaviour could still change between beta releases.[^claude-managed-agents]

## Related

- [Claude Projects](claude-projects.md): long-running, parallel work inside Claude Code rather than through the API.
- [Cloud environment](cloud-environment.md): the Claude Code counterpart for sandbox configuration.
- Source: [Claude Managed Agents](../../sources/claude-managed-agents.md)

[^claude-managed-agents]: Claude Managed Agents
