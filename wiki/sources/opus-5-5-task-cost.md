---
type: Source Summary
title: What a task costs on Opus 5.5 (summary)
description: Summary of Addy Osmani's 2026-09-25 claude.dev post pricing Claude Code tasks on Opus 5.5 against Opus 5, and the settings that move the bill.
tags: [claude-code, cost, models]
sources:
  - id: opus-5-5-task-cost
    resource: https://github.com/kelvinlee97/engineering/blob/main/raw/2026-09-25-what-a-task-costs-on-opus-5-5.md
    title: What a task costs on Opus 5.5
    author: Addy Osmani
    last_modified: 2026-09-25T00:00:00Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---

A claude.dev blog post by Addy Osmani, published Sep 25, 2026, snapshotted the same day. It explains what sets the cost of a Claude Code task, what the Opus 5.5 price cut changes, and which settings (effort, model, caching, compaction) trade tokens against a finished task.

**Scope and gaps:** most dollar figures are illustrations the author built from API list prices, and the post says so. The interactive calculators (Fig A to C) were captured only as the default values shown in the page text. The "40% less" headline is Anthropic's estimate for typical workloads, which the post separates from the per-token price change. The prompt-audit result comes from one internal benchmark of 44 tickets.[^opus-5-5-task-cost]

## Takeaways

- A task is a loop, and four things set its cost: turns, cache reads, output tokens (thinking included), and the model. See [Claude Code session cost](../engineering/claude-code/session-cost.md#what-sets-the-cost-of-a-task).
- Opus 5.5 cuts input and output prices by 20% and cache reads by 60% against Opus 5; the illustrative session in the post costs about 31% less from price alone. See [Opus 5.5 pricing](../engineering/claude-code/session-cost.md#what-opus-55-changed).
- Raise effort before changing models; Opus 5.5 defaults to medium. See [effort](../engineering/claude-code/session-cost.md#effort-levels).
- Use Sonnet or Haiku subagents for lookups, Opus 5.5 for supervised work, Fable 5.1 for the hardest unsupervised runs. See [model choice](../engineering/claude-code/session-cost.md#choosing-a-model) and [Subagents](../engineering/claude-code/subagents.md).
- Keep the cache warm, compact at a break, and measure with `/usage`. See [caching and compaction](../engineering/claude-code/session-cost.md#caching-and-compaction).[^opus-5-5-task-cost]

[^opus-5-5-task-cost]: [What a task costs on Opus 5.5 (summary)](opus-5-5-task-cost.md), [original](https://github.com/kelvinlee97/engineering/blob/main/raw/2026-09-25-what-a-task-costs-on-opus-5-5.md)
