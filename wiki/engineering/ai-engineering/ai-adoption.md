---
type: Pattern
title: AI adoption and measurement
description: The four-stage AI adoption ladder and how to measure whether a rollout is paying off.
tags:
- ai-engineering
- adoption
aliases:
- engineering/ai-engineering/ai-adoption-maturity
- engineering/ai-engineering/ai-rollout-measurement
sources:
- id: ai-native-revenue-org
  resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-revenue-org/README.md
  title: Building an AI-Native Revenue Organization
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
Rolling out AI in an organization, as the sources describe it, is a climb through four stages rather than a one-off deployment, and each step up needs evidence that the last one paid off. This page covers the maturity ladder and how to measure a rollout.

## AI adoption maturity

Anthropic's revenue-organization guide frames rolling out Claude as climbing a maturity ladder rather than a one-off deployment: seats and training are the first step, and returns grow as the organization extends more access and trust.[^ai-native-revenue-org] The source is vendor material; see the [source summary](../../sources/ai-native-revenue-org.md).

### The ladder

1. **Individual gains:** chat assistant for drafting and research.
2. **Team workflows:** connected systems and shared skills.
3. **Department workflows:** plugins and managed agents.
4. **KPI and OKR gains:** processes run end to end.

Three enablers grow alongside: fluency (from one task to parallel workflows), access and autonomy (from pasted notes to live CRM data), and governance (who publishes skills, what data each workflow reaches, who owns the results). The guide treats governance as continuous, not a phase.[^ai-native-revenue-org]

### Decisions before a pilot

| Decision | Recommendation |
| --- | --- |
| Owner | RevOps, who own the CRM and the pipeline reporting |
| Connectors | Connect the tools people already use; manual uploads signal a missing connector |
| IT and security | Name an IT owner and agree provisioning dates before the pilot date; start the security review early |
| Metrics | One activity metric and one revenue metric, both baselined before deployment |
| Spend | Limits by org, group, and user, and usage analytics from day one |
| Cohort | Two or three teams with motivated leads |

As recommended in the guide.[^ai-native-revenue-org]

### Rollout and the gate to scale

Set up (IT, connectors, champions), pilot (two or three teams, two or three use cases each), then scale in waves of about 25, then 150, then everyone, moving champion-built skills into a shared bundle. Scaling requires all three: people still producing after the novelty wears off, quality checks holding, and pilot teams ahead on the outcome metric. The guide's best early predictor is how many champion-created skills pilot teams use regularly.[^ai-native-revenue-org]

### Pitfalls

| Pitfall | Fix at setup |
| --- | --- |
| Pilot with no end date or decider | Put the scale decision, its owner, and its criteria on the sponsor's calendar |
| Seats scaled, champions not | Keep one champion per 25–50 users through every wave |
| Spend ignored until the invoice | Set limits before the pilot; read usage weekly |

As described in the guide; the note's author reads all three as a decision never given an owner and a date.[^ai-native-revenue-org]

## Measuring an AI rollout

To judge whether an AI rollout works, compare teams using it with teams not using it over the same period, against metrics fixed and baselined before deployment. The note's author considers this measurement design the part that transfers to any internal tooling rollout.[^ai-native-revenue-org]

### Rules

- **Baseline first.** Pick one activity metric and one revenue metric and baseline both before deployment; without a baseline and a concurrent control group, the readout becomes anecdotes.
- **Compare cohorts, not calendars.** Compare pilot and non-pilot teams in the same quarter (pipeline per rep, cycle length, win rate) rather than one team before and after, so market and season affect both.
- **Don't lead with hours saved.** Time saved is capped at what the team is paid for that time; lead with expansion and new capabilities.
- **Read spend against output.** High spend alone is not a signal: a heavy user who also produces daily is the program working; a heavy user producing little gets coaching first, and a lower cap only if coaching fails.[^ai-native-revenue-org]

### Where returns show up

Returns appear in order: usage, then output, then CRM outcomes, then cost.

| Group | Meaning | Example |
| --- | --- | --- |
| Efficiency | Same work, faster | Deal prep from 3–4 hours to 45 minutes |
| Expansion | More output from the same team | More accounts covered, more pipeline per rep |
| New capabilities | Work that did not happen before | Every account in a book scored overnight |

As described in the guide.[^ai-native-revenue-org]

## Related

- [Agent skills](../claude-code/agent-skills.md): the shared-skill mechanics behind stage 2.

[^ai-native-revenue-org]: [Building an AI-Native Revenue Organization](../../sources/ai-native-revenue-org.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-revenue-org/README.md)
