---
type: Pattern
title: Measuring an AI rollout
description: Judge an AI tooling rollout by comparing concurrent cohorts against pre-set baselines, and lead with expansion rather than hours saved.
tags: [ai-adoption, measurement]
sources:
  - id: ai-native-revenue-org
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-revenue-org/README.md
    title: Building an AI-Native Revenue Organization
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T16:05:00Z }
status: draft
---

To judge whether an AI rollout works, compare teams using it with teams not using it over the same period, against metrics fixed and baselined before deployment.[^ai-native-revenue-org] The note's author considers this measurement design the part that transfers to any internal tooling rollout.[^ai-native-revenue-org]

## Rules

- **Baseline first.** Pick one activity metric and one revenue metric and baseline both before deployment; without a baseline and a concurrent control group, the readout becomes anecdotes.[^ai-native-revenue-org]
- **Compare cohorts, not calendars.** Compare pilot and non-pilot teams in the same quarter (pipeline per rep, cycle length, win rate) rather than one team before and after, so market and season affect both.[^ai-native-revenue-org]
- **Don't lead with hours saved.** Time saved is capped at what the team is paid for that time; lead with expansion and new capabilities.[^ai-native-revenue-org]
- **Read spend against output.** High spend alone is not a signal: a heavy user who also produces daily is the program working; a heavy user producing little gets coaching first, and a lower cap only if coaching fails.[^ai-native-revenue-org]

## Where returns show up

Returns appear in order: usage, then output, then CRM outcomes, then cost.[^ai-native-revenue-org]

| Group | Meaning | Example |
| --- | --- | --- |
| Efficiency | Same work, faster | Deal prep from 3–4 hours to 45 minutes |
| Expansion | More output from the same team | More accounts covered, more pipeline per rep |
| New capabilities | Work that did not happen before | Every account in a book scored overnight |

As described in the guide.[^ai-native-revenue-org]

## Related

- [AI adoption maturity](ai-adoption-maturity.md)
- Source: [Building an AI-Native Revenue Organization](../../sources/ai-native-revenue-org.md)

[^ai-native-revenue-org]: Building an AI-Native Revenue Organization
