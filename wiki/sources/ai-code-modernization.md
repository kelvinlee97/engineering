---
type: Source Summary
title: How to prepare for AI-driven code modernization projects (summary)
description: Summary of Anthropic's 2026-09-23 field note on the six steps an enterprise completes before and during an agent-driven code modernization.
tags: [modernization, agents, governance]
sources:
- id: ai-code-modernization
  resource: https://github.com/kelvinlee97/engineering/blob/main/raw/2026-09-25-ai-code-modernization.md
  title: How to prepare for AI-driven code modernization projects
  author: Jonah Ezekiel and Lexie Tonelli
  last_modified: 2026-09-23T00:00:00Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T13:00:00Z }
status: draft
---

A *Notes from the Field* post by two Anthropic forward deployed engineers, published 2026-09-23. It argues that once agents write the changes, the bottleneck of a modernization moves from producing changes to getting the organization to accept them, and lays out six preparation and execution steps. It is written by the vendor and names its own plugin and models, so treat product recommendations as vendor guidance. It gives no concrete cost figures; it points to other published modernization costs without quoting them.[^ai-code-modernization]

## Takeaways

- Pick the modernization type first (uplift, transform, reimagine); an unresolved choice returns later as arguments over whether a change is correct. See [Code modernization with agents](../engineering/ai-engineering/code-modernization.md#modernization-types).
- The certificate is a set of machine-checkable conditions every change must pass, written with the people who will approve the changes. See [The certificate](../engineering/ai-engineering/code-modernization.md#the-certificate).
- The promotion policy tiers human review by blast radius and agent confidence, agreed in advance and backed by leadership. See [The promotion policy](../engineering/ai-engineering/code-modernization.md#the-promotion-policy).
- Pilot end to end on a small partition, fix the workflow rather than individual changes, and extrapolate token cost from the pilot. See [Pilot, scale, and cost](../engineering/ai-engineering/code-modernization.md#pilot-scale-and-cost).
- Risk reduction, not cost reduction, is named as the usual driver.[^ai-code-modernization]

[^ai-code-modernization]: [How to prepare for AI-driven code modernization projects](ai-code-modernization.md), [original](https://github.com/kelvinlee97/engineering/blob/main/raw/2026-09-25-ai-code-modernization.md)
