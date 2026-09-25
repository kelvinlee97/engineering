---
type: Source Summary
title: "GitHub Certified: Agentic AI Developer (study notes)"
description: Study notes for GitHub's GH-600 exam and its Microsoft Learn course, with one architecture module read in full.
tags: [github, agents, certification]
sources:
  - id: gh-600-study-notes
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-agentic-ai-developer/README.md
    title: "GitHub Certified: Agentic AI Developer (study notes)"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T16:05:00Z }
status: draft
---

A note in this repository, `Claude/github-agentic-ai-developer/README.md`: study notes for the **GitHub Certified: Agentic AI Developer** exam (GH-600) and course GH-600T00 *Developing in Agentic AI Systems*.[^gh-600-study-notes]

## Coverage

Only module 2, *Designing Agent Architecture and SDLC Integration*, was read unit by unit; the other five modules are summarized from their unit titles and the course and exam pages.[^gh-600-study-notes] Wiki pages citing this source draw on module 2.

## Exam facts

- GH-600: provided by Microsoft, maintained by GitHub; proctored, 120 minutes, English only, through Pearson VUE; intermediate level.
- Retake after 24 hours following a first failure; later waits grow.

| Domain | Weight |
| --- | --- |
| Prepare agent architecture and SDLC processes | 15–20% |
| Implement tool use and environment interaction | 20–25% |
| Manage memory, state, and execution | 10–15% |
| Perform evaluation, error analysis, and tuning | 15–20% |
| Orchestrate multi-agent coordination | 15–20% |
| Implement guardrails and accountability | 10–15% |

As listed in the notes.[^gh-600-study-notes]

## Takeaways

- Agents propose work through branches and pull requests; GitHub controls decide whether it is accepted. See [Agents propose, people and policy accept](../engineering/ai-engineering/ai-native-sdlc.md#agents-propose-people-and-policy-accept).
- Autonomy should be sized to the risk of the paths a change touches. See [Risk-based autonomy](../engineering/ai-engineering/ai-native-sdlc.md#risk-based-autonomy).
- A task needs defined inputs, outputs, and success criteria.[^gh-600-study-notes] See [Delegation contract](../engineering/claude-code/subagents.md#delegation-contract).

[^gh-600-study-notes]: GitHub Certified: Agentic AI Developer (study notes), [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/Claude/github-agentic-ai-developer/README.md)
