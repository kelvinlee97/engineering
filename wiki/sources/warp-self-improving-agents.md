---
type: Source Summary
title: How Warp Builds Self-Improving Agents on Claude (summary)
description: Summary of an Anthropic post and Warp webinar on agents that improve their own skill files through reviewed pull requests.
tags: [agents, skills, feedback-loops]
sources:
  - id: warp-self-improving-agents
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/self-improving-agents/README.md
    title: How Warp Builds Self-Improving Agents on Claude
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T16:05:00Z }
status: draft
---

A note in this repository, `Claude/self-improving-agents/README.md`, on Anthropic's post *How Warp builds self-improving agents on Claude* (from a webinar with Warp's founder and Anthropic's Applied AI team) and Warp's related posts, reviewed on 2026-09-16.

**Sourcing caveat carried from the note:** the primary pages were not reachable, so the note was assembled from search-result excerpts and secondary coverage; wording and figures are second-hand.[^warp-self-improving-agents] Its "Where it breaks down" section is the author's analysis.

## Takeaways

- A scheduled outer skill reads human feedback on an agent's work and opens a pull request editing the inner skill the agent reads. See [Self-improving skill loop](../engineering/ai-engineering/self-improving-skill-loop.md).
- Improvements arrive as pull requests, so the team, not the agent, accepts them. See [Agents propose, people and policy accept](../engineering/ai-engineering/ai-native-sdlc.md#agents-propose-people-and-policy-accept).
- A few detailed, domain-specific comments beat many thumbs-downs.[^warp-self-improving-agents]

[^warp-self-improving-agents]: How Warp Builds Self-Improving Agents on Claude, [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/Claude/self-improving-agents/README.md)
