---
type: Pattern
title: Agents propose, people and policy accept
description: Route every agent change through pull requests so that required checks, code owners, and approval gates, not the agent, decide what is accepted.
tags: [agents, governance, github]
sources:
  - id: gh-600-study-notes
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-agentic-ai-developer/README.md
    title: "GitHub Certified: Agentic AI Developer (study notes)"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: ai-native-sdlc-playbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-sdlc-playbook/README.md
    title: The AI-Native SDLC Playbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: warp-self-improving-agents
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/self-improving-agents/README.md
    title: How Warp Builds Self-Improving Agents on Claude
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T16:05:00Z }
status: draft
---

The boundary in this pattern is simple: an agent may propose work (a plan, a branch, a pull request), but controls outside the agent decide whether it is accepted. A confident agent cannot skip a gate, because the gate is enforced by the platform, not by instructions the agent is trusted to follow.[^gh-600-study-notes]

## The same boundary in three sources

| Source | Where the boundary sits |
| --- | --- |
| GH-600 course, module 2 | Required checks, CODEOWNERS review, branch protection, and environment approvals decide what merges and deploys.[^gh-600-study-notes] |
| AI-native SDLC playbook | Agents propose changes only through pull requests and branch protection; the production gate stays human-controlled.[^ai-native-sdlc-playbook] |
| Warp's self-improving agents | Improvements to an agent's own skill file arrive as pull requests the team reviews and can revert.[^warp-self-improving-agents] |

## Making it enforceable on GitHub

The GH-600 module turns the boundary into three mechanisms:[^gh-600-study-notes]

1. A pull request template requiring goal, scope, steps, verifiable success criteria, risks, and a rollback plan.
2. A required status check (for example a "Plan Gate" workflow) that fails when the plan is missing.
3. CODEOWNERS, so changes under paths such as `/security/`, `/.github/workflows/`, or `/infra/` need the owners' sign-off.

## Plan first, or plan with the code

| | Plan-first PR | Plan and execution in one PR |
| --- | --- | --- |
| Plan visible | Before any code exists | Alongside the first commits |
| Human validation | Before code is written | Before merge |
| Suited to | High-risk, hard-to-reverse changes | Low or medium risk, easily reversed |

Both are safe when GitHub protections are configured; the only variable is when code may exist relative to approval. Planning agents should get read-only tools, with a deliberate handoff to an implementation agent.[^gh-600-study-notes]

Version control also supplies the audit log, approval gate, and rollback that a bespoke agent-memory system would have to build (analysis in the Warp note).[^warp-self-improving-agents] The SDLC playbook makes the same point: Git history records what was asked, what the agent produced, which policy applied, and who approved it.[^ai-native-sdlc-playbook]

## Related

- [Risk-based autonomy](risk-based-autonomy.md): how much each kind of change is allowed to do before a person looks.
- [Delegation contract](../claude-code/delegation-contract.md): what the proposal must contain.
- Source: [GitHub Certified: Agentic AI Developer](../../sources/gh-600-study-notes.md)
- Source: [The AI-Native SDLC Playbook](../../sources/ai-native-sdlc-playbook.md)
- Source: [How Warp Builds Self-Improving Agents on Claude](../../sources/warp-self-improving-agents.md)

[^gh-600-study-notes]: GitHub Certified: Agentic AI Developer (study notes)
[^ai-native-sdlc-playbook]: The AI-Native SDLC Playbook
[^warp-self-improving-agents]: How Warp Builds Self-Improving Agents on Claude
