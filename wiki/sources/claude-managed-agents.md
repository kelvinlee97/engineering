---
type: Source Summary
title: Claude Managed Agents (summary of the official overview)
description: Summary of Anthropic's Claude Managed Agents overview documentation, reviewed on 2026-09-15 while the product was in beta.
tags: [claude-api, managed-agents]
sources:
  - id: claude-managed-agents
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/managed-agents/README.md
    title: Claude Managed Agents
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:40:00Z }
status: draft
---

A note in this repository, `Claude/managed-agents/README.md`, summarizing Anthropic's *Claude Managed Agents overview* documentation, reviewed on 2026-09-15. The product was in beta and every request needed the `managed-agents-2026-04-01` header.[^claude-managed-agents]

## Takeaways

- Managed Agents is a hosted agent harness: Anthropic runs the loop, sandbox, and tool execution, and you send events.[^claude-managed-agents] See [Claude Managed Agents](../engineering/claude-code/claude-managed-agents.md).
- It trades the Messages API's control over every model call for managed infrastructure.[^claude-managed-agents]
- Being stateful, it was not eligible for Zero Data Retention or HIPAA BAA coverage at review time.[^claude-managed-agents]

[^claude-managed-agents]: Claude Managed Agents
