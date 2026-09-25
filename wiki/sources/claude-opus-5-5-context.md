---
type: Source Summary
title: Claude Opus 5.5 and longer coding sessions (summary)
description: Summary of Anthropic's 2026-09-24 post on Claude Code usage trends and why Opus 5.5 costs about 40% less to run than Opus 5.
tags: [claude-code, cost, prompt-caching, models]
sources:
- id: claude-opus-5-5-context
  resource: https://github.com/kelvinlee97/engineering/blob/main/raw/2026-09-25-claude-opus-5-5-context.md
  title: Coding sessions are longer and use more context. Claude Opus 5.5 is built with that in mind.
  author: Michael Segner
  last_modified: 2026-09-24T00:00:00Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:30:00Z }
status: draft
---

An Anthropic blog post by Michael Segner, dated 2026-09-24, about how Claude Code sessions changed between March and September 2026 and how Claude Opus 5.5 is priced and tuned for them.

**Caveat:** this is vendor marketing. Every number is Anthropic-reported, with no method, sample, or workload definition given; "typical workloads" is not defined. The post does not list absolute prices.[^claude-opus-5-5-context]

## Headline numbers

| Claim | Figure |
| --- | --- |
| Cost to run versus Opus 5, typical token-billed workloads | about 40% less |
| Input and output token price | 20% lower |
| Cached token read price | 60% lower |
| Input missing the cache | down more than 50% |
| Output speed versus Opus 5 | over 30% faster |

As reported in the post.[^claude-opus-5-5-context]

## Takeaways

- Sessions got longer and heavier on context, so cached reads now dominate agentic cost. See [Claude Code session cost](../engineering/claude-code/session-cost.md#how-coding-sessions-changed).
- Savings come from lower prices, fewer cache misses, and fewer turns. See [Where the savings come from](../engineering/claude-code/session-cost.md#where-the-savings-come-from).
- Subagents now start from the parent's cache. See [Subagents](../engineering/claude-code/subagents.md#what-it-costs).
- Watch cached reads with `/usage`, pick the model at session start, and use a one-hour cache for long API sessions.[^claude-opus-5-5-context] See [Keeping the cache warm](../engineering/claude-code/session-cost.md#keeping-the-cache-warm).

[^claude-opus-5-5-context]: [Claude Opus 5.5 and longer coding sessions](claude-opus-5-5-context.md), [original](https://github.com/kelvinlee97/engineering/blob/main/raw/2026-09-25-claude-opus-5-5-context.md)
