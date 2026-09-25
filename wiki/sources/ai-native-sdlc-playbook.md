---
type: Source Summary
title: The AI-Native SDLC Playbook (summary)
description: Summary of Anthropic's 2026-08-21 playbook that redesigns software delivery as a loop of versioned artifacts with human approval gates.
tags: [sdlc, agents, governance]
sources:
  - id: ai-native-sdlc-playbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-sdlc-playbook/README.md
    title: The AI-Native SDLC Playbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T16:05:00Z }
status: draft
---

A note in this repository, `Claude/ai-native-sdlc-playbook/README.md`, summarizing *The AI-Native SDLC playbook* by Louis Claxton, published by Anthropic on 2026-08-21. The note points out that it is an Anthropic-authored model built around Claude products, so its product choices are not vendor-neutral evidence.[^ai-native-sdlc-playbook]

## Takeaways

- Each delivery stage leaves a committed artifact (`intent.md`, `spec.md`, `plan.md`, results, PR, incident record) and production evidence loops back as new intent. See [AI-native SDLC](../engineering/ai-engineering/ai-native-sdlc.md#stages-and-practices).
- Autonomy grows in steps, with the production gate kept human. See [Risk-based autonomy](../engineering/ai-engineering/ai-native-sdlc.md#risk-based-autonomy).
- Deterministic checks enforce; agents judge and diagnose.[^ai-native-sdlc-playbook] See [Least-privilege tool access](../engineering/claude-code/subagents.md#least-privilege-tool-access).

[^ai-native-sdlc-playbook]: The AI-Native SDLC Playbook, [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-sdlc-playbook/README.md)
