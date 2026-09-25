---
type: Concept
title: AI-native company
description: A company designed around AI loops from the start, with work made legible to agents and people at the boundary with reality, as argued in several founder and investor talks.
tags: [ai-adoption, agents, organization]
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
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:45:00Z }
status: draft
---
An AI-native company, as the speakers in these sources use the term, is designed around AI from the ground up rather than adding chatbots or copilots to existing workflows. They argue that with add-on tools, people remain the coordination and approval bottleneck.[^ai-native-company-structure-video] All three sources are talks; their figures are the speakers' own and none was independently verified.[^kavak-agents-video][^ai-native-company-structure-video][^ai-company-ground-up-video]

## The loop at the centre

Both YC talks describe the company as closed loops: act, observe the result, feed evidence back, adjust.[^ai-company-ground-up-video] One lists five parts: real-world signals, a policy layer (constraints, approvals, logging), a tool layer (internal APIs or MCP tools), quality gates (sometimes a person, often a second adversarial model), and a learning step that keeps improvements.[^ai-native-company-structure-video]

## What the speakers say it takes

| Practice | Source claim |
| --- | --- |
| Make the company legible | Record meetings, keep work in accessible channels, and leave an artifact for every action; "otherwise, from the AI's perspective, it did not happen"[^ai-native-company-structure-video][^ai-company-ground-up-video] |
| Rebuild systems, not just add chat | Kavak rebuilt systems and APIs so agents could act, and measured long-term customer value instead of transactions[^kavak-agents-video] |
| Humans own intent and acceptance | In an "AI software factory", people write specs and tests and judge results; agents implement until tests pass[^ai-company-ground-up-video] |
| Flatter roles | Builder-operators, one directly responsible individual per outcome, and a founder who keeps building[^ai-company-ground-up-video] |
| Evals as brakes | Kavak says it spends roughly as much engineering time, tokens, and money on evals as on agents, measuring business outcomes rather than call counts[^kavak-agents-video] |

## Where people remain

At the boundary with reality: intuition, trust, ethics, novel situations, and high-stakes decisions, such as visiting a customer or pitching an investor.[^ai-native-company-structure-video] Kavak still has mechanics, supported by an agent sidekick, and says physical handover of the car stays with people.[^kavak-agents-video]

## Reported results, as claimed

Kavak says agents handle 96% of interactions and 95% of transactions, and that its sales agents later exceeded the human conversion benchmark by 2.1 times.[^kavak-agents-video] The ground-up talk mentions teams halving sprint time but supplies no benchmark method.[^ai-company-ground-up-video]

## Related

- [Company brain](company-brain.md)
- [Self-improving skill loop](self-improving-skill-loop.md)
- [AI adoption maturity](ai-adoption-maturity.md)
- Source: [What happens when AI agents run the business](../../sources/kavak-agents-video.md)
- Source: [Building and structuring an AI-native company](../../sources/ai-native-company-structure-video.md)
- Source: [How to build a company with AI from the ground up](../../sources/ai-company-ground-up-video.md)

[^ai-native-company-structure-video]: Building and Structuring an AI-Native Company (video summary)
[^kavak-agents-video]: What Happens When AI Agents Run the Business? (video summary)
[^ai-company-ground-up-video]: How to Build a Company With AI From the Ground Up (video summary)
