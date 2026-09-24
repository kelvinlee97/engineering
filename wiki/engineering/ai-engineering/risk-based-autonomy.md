---
type: Pattern
title: Risk-based autonomy
description: Give agents more autonomy on low-risk, reversible work and keep human approval for high-risk and production changes, widening scope gradually.
tags: [agents, governance, security]
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
  - id: claude-auto-mode
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/auto-mode/README.md
    title: How Claude Code Auto Mode Works
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T16:05:00Z }
status: draft
---

Risk-based autonomy means the amount of work an agent may finish without a person depends on how risky and reversible the change is, and grows only as verification and rollback prove trustworthy. All three sources that discuss it keep production behind a human gate.

## Sizing by path (GH-600)

| Risk | Example paths | Design |
| --- | --- | --- |
| Low | `docs/`, formatting | Auto-merge after required checks |
| Medium | `src/`, dependency bumps | PR, checks, at least one review |
| High | `infra/`, `.github/workflows/` | CODEOWNERS, multiple reviews, stricter rulesets |
| Critical | Production deploys, settings, secrets | Environment approval: the agent prepares but does not execute |

As described in module 2.[^gh-600-study-notes] A GitHub Actions environment with required reviewers pauses any job targeting it until a person approves.[^gh-600-study-notes]

## Widening in steps (AI-native SDLC playbook)

1. Start with read-only work such as build-failure triage and changelog drafts.
2. Let agents propose changes only through pull requests and branch protection.
3. Run jobs in sandboxes with short-lived, scoped credentials.
4. Expose deployment and rollback as allowlisted tools per environment.
5. Allow more autonomy in development than in production.
6. Keep the production gate human and rehearse rollback.

[^ai-native-sdlc-playbook]

## Rolling out Claude Code Auto Mode

The [Auto Mode](../claude-code/auto-mode.md) guidance follows the same shape: start narrow, keep explicit `deny` and `ask` rules, watch what is denied, widen gradually, and keep human review for production infrastructure.[^claude-auto-mode]

## Reliability assumptions

GH-600 adds that agent workflows should assume failure: bounded retries for transient check failures, escalation to a person after a check fails twice (with what failed, what was tried, and a suggested next step), and rollback readiness for high-risk changes.[^gh-600-study-notes]

## Related

- [Agents propose, people and policy accept](propose-accept-boundary.md)
- [Least-privilege tool access](../claude-code/least-privilege-tool-access.md)
- Source: [GitHub Certified: Agentic AI Developer](../../sources/gh-600-study-notes.md)
- Source: [The AI-Native SDLC Playbook](../../sources/ai-native-sdlc-playbook.md)
- Source: [How Claude Code Auto Mode Works](../../sources/claude-auto-mode.md)

[^gh-600-study-notes]: GitHub Certified: Agentic AI Developer (study notes)
[^ai-native-sdlc-playbook]: The AI-Native SDLC Playbook
[^claude-auto-mode]: How Claude Code Auto Mode Works
