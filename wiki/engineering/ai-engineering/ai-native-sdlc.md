---
type: Pattern
title: AI-native SDLC
description: A software delivery loop where each stage leaves a committed artifact, agents work between human approval gates, and production evidence returns as new intent.
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

An AI-native software delivery lifecycle (SDLC) is a loop of versioned artifacts: each stage consumes the previous stage's committed output, agents speed up the work between gates, and people stay accountable for approvals involving risk or judgment. The goal is not unrestricted autonomy.[^ai-native-sdlc-playbook]

## Stages and their artifacts

| Stage | Committed artifact | Main change |
| --- | --- | --- |
| Plan | `intent.md` | Record the problem, outcome, constraints, and open questions; a product owner accepts it |
| Design | `spec.md` | Turn intent into requirements while applying versioned security, compliance, brand, and UX policy |
| Build | `plan.md`, code, tests | An engineer approves the plan (files, order, risks, proof) before implementation |
| Test | Test, build, screenshot, eval results | The agent runs a runnable definition of done and fixes its work before review |
| Deploy | PR and review findings | Several focused automated reviews; branch protection; human approval for critical changes |
| Maintain | Incident record, then a new `intent.md` | Deterministic monitoring detects; agents diagnose through gated routes; findings return to planning |

As described in the playbook.[^ai-native-sdlc-playbook] The return edge from Maintain to Plan is what makes it a loop rather than a pipeline.[^ai-native-sdlc-playbook]

## Practices worth reusing

- Keep a short, reviewed `CLAUDE.md` for build commands, conventions, and recurring mistakes, and put organization-wide policy in skills.[^ai-native-sdlc-playbook] See [Claude Code extension mechanisms](../claude-code/extension-mechanisms.md).
- Parallel sessions use separate Git worktrees on independent files; start with two or three streams, because review capacity is the limit.[^ai-native-sdlc-playbook]
- For a bug fix, first reproduce the failure as a test and protect that test while the agent fixes the code. Run evaluations whenever instructions, prompts, tools, or models change: evals test the development system, ordinary tests test the product.[^ai-native-sdlc-playbook]
- Escalate production signals in tiers: log a small deviation, run a read-only diagnosis for a larger one, allow only a pre-approved PR or runbook at the top tier. A shipped fix adds a regression eval.[^ai-native-sdlc-playbook]
- Measure rework, first-pass CI success, review time, change failure rate, and repeat incidents, not lines generated.[^ai-native-sdlc-playbook]

## Adoption order

1. Make build, test, and lint runnable with simple commands.
2. Add a concise, maintained `CLAUDE.md`.
3. Require reviewed intent and implementation plans for meaningful changes.
4. Give agents local feedback loops and add evals for recurring failures.
5. Add read-only CI triage and focused PR reviewers.
6. Permit agent-written changes only through existing review and deployment gates.
7. Close one maintenance loop around a stable, low-noise production signal.

[^ai-native-sdlc-playbook]

## Related

- [Risk-based autonomy](risk-based-autonomy.md)
- [Agents propose, people and policy accept](propose-accept-boundary.md)
- Source: [The AI-Native SDLC Playbook](../../sources/ai-native-sdlc-playbook.md)

[^ai-native-sdlc-playbook]: The AI-Native SDLC Playbook
