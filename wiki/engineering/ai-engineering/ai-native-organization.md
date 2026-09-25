---
type: Concept
title: AI-native organization
description: What an AI-native company is and the company brain that feeds its agents, as argued in founder and investor talks.
tags:
- ai-engineering
- organization
aliases:
- engineering/ai-engineering/ai-native-company
- engineering/ai-engineering/company-brain
sources:
- id: kavak-agents-video
  resource: https://github.com/kelvinlee97/engineering/blob/main/YouTube/claude/what-happens-when-ai-agents-run-the-business--n34CIw3gk1k/summary.md
  title: What Happens When AI Agents Run the Business? (video summary)
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: ai-native-company-structure-video
  resource: https://github.com/kelvinlee97/engineering/blob/main/YouTube/startup/building-and-structuring-an-ai-native-company--Z3JyAqh4ixg/summary.md
  title: Building and Structuring an AI-Native Company (video summary)
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: ai-company-ground-up-video
  resource: https://github.com/kelvinlee97/engineering/blob/main/YouTube/startup/how-to-build-a-company-with-ai-from-the-ground-up--EN7frwQIbKc/summary.md
  title: How to Build a Company With AI From the Ground Up (video summary)
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: company-brain-video
  resource: https://github.com/kelvinlee97/engineering/blob/main/YouTube/startup/every-company-should-have-a-brain--eBUyTS7SzV4/summary.md
  title: Every Company Should Have a Brain (video summary)
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
An AI-native company, as several founder and investor talks use the term, is built around AI loops from the start instead of adding tools to existing workflows. Its agents depend on a company brain: curated organizational memory plus the retrieval that feeds it to them. The claims here are the speakers' own.

## AI-native company

An AI-native company, as the speakers in these sources use the term, is designed around AI from the ground up rather than adding chatbots or copilots to existing workflows. They argue that with add-on tools, people remain the coordination and approval bottleneck. All three sources are talks; their figures are the speakers' own and none was independently verified.[^kavak-agents-video][^ai-native-company-structure-video][^ai-company-ground-up-video]

### The loop at the centre

Both YC talks describe the company as closed loops: act, observe the result, feed evidence back, adjust.[^ai-company-ground-up-video] One lists five parts: real-world signals, a policy layer (constraints, approvals, logging), a tool layer (internal APIs or MCP tools), quality gates (sometimes a person, often a second adversarial model), and a learning step that keeps improvements.[^ai-native-company-structure-video]

### What the speakers say it takes

| Practice | Source claim |
| --- | --- |
| Make the company legible | Record meetings, keep work in accessible channels, and leave an artifact for every action; "otherwise, from the AI's perspective, it did not happen"[^ai-native-company-structure-video] |
| Rebuild systems, not just add chat | Kavak rebuilt systems and APIs so agents could act, and measured long-term customer value instead of transactions |
| Humans own intent and acceptance | In an "AI software factory", people write specs and tests and judge results; agents implement until tests pass |
| Flatter roles | Builder-operators, one directly responsible individual per outcome, and a founder who keeps building[^ai-company-ground-up-video] |
| Evals as brakes | Kavak says it spends roughly as much engineering time, tokens, and money on evals as on agents, measuring business outcomes rather than call counts[^kavak-agents-video] |

### Where people remain

At the boundary with reality: intuition, trust, ethics, novel situations, and high-stakes decisions, such as visiting a customer or pitching an investor.[^ai-native-company-structure-video] Kavak still has mechanics, supported by an agent sidekick, and says physical handover of the car stays with people.[^kavak-agents-video]

### Reported results, as claimed

Kavak says agents handle 96% of interactions and 95% of transactions, and that its sales agents later exceeded the human conversion benchmark by 2.1 times.[^kavak-agents-video] The ground-up talk mentions teams halving sprint time but supplies no benchmark method.[^ai-company-ground-up-video]

## Company brain

A company brain, in Garry Tan's framing, is both a library (emails, meetings, decisions, customer conversations, postmortems) and a librarian that selects the small subset relevant to the current task. A company holds far more than any single context window, so the selection is the point.[^company-brain-video] Another YC talk describes the same idea as organizational data plus reinforcing loops that can access it, so intelligence lives in the system rather than being routed through management.[^ai-native-company-structure-video]

### Memory needs hygiene

Tan warns that an uncurated brain becomes a searchable garbage dump: stale facts come back confidently, and a bad skill preserves a bad process. His remedy is memory plus hygiene: provenance for facts, contradiction checks, and human-plus-agent curation that prunes obsolete material, treated as production infrastructure.[^company-brain-video]

(Analysis: this is the problem this wiki's own conventions address: `sources` and footnotes for provenance, a `## Contradictions` section, and lint passes for stale pages.)

### Skills as the organization

Tan maps agent infrastructure to a company: a skill file is an employee with one capability, a resolver table is the org chart, filing rules are procedures, and trigger evaluations are performance reviews. His rule is never to do one-off work: once a recurring task comes out right, keep the process as a skill; "model quality is rented, but the accumulated organizational brain is owned."[^company-brain-video]

### Put each computation on the right side

Use the model for judgment and vague intent; use ordinary code and data structures for exact storage and repeatable computation. In his seating example, a model can judge who should meet, but the exact arrangement of 800 seats belongs in deterministic structures.[^company-brain-video] See [Deterministic checks and model judgment](ai-native-sdlc.md#deterministic-checks-and-model-judgment).

## Related

- [Self-improving skill loop](self-improving-skill-loop.md)
- [AI adoption maturity](ai-adoption.md#ai-adoption-maturity)
- [Agent skills](../claude-code/agent-skills.md)

[^kavak-agents-video]: [What Happens When AI Agents Run the Business? (video summary)](../../sources/kavak-agents-video.md), [original](https://github.com/kelvinlee97/engineering/blob/main/YouTube/claude/what-happens-when-ai-agents-run-the-business--n34CIw3gk1k/summary.md)
[^ai-native-company-structure-video]: [Building and Structuring an AI-Native Company (video summary)](../../sources/ai-native-company-structure-video.md), [original](https://github.com/kelvinlee97/engineering/blob/main/YouTube/startup/building-and-structuring-an-ai-native-company--Z3JyAqh4ixg/summary.md)
[^ai-company-ground-up-video]: [How to Build a Company With AI From the Ground Up (video summary)](../../sources/ai-company-ground-up-video.md), [original](https://github.com/kelvinlee97/engineering/blob/main/YouTube/startup/how-to-build-a-company-with-ai-from-the-ground-up--EN7frwQIbKc/summary.md)
[^company-brain-video]: [Every Company Should Have a Brain (video summary)](../../sources/company-brain-video.md), [original](https://github.com/kelvinlee97/engineering/blob/main/YouTube/startup/every-company-should-have-a-brain--eBUyTS7SzV4/summary.md)
