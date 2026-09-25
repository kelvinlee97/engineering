---
type: Concept
title: Company brain
description: An organization's curated memory plus the retrieval that selects what an agent needs, kept useful by provenance, contradiction checks, and pruning.
tags: [ai-adoption, memory, skills]
sources:
  - id: company-brain-video
    resource: https://github.com/kelvinlee97/engineering/blob/main/YouTube/startup/every-company-should-have-a-brain--eBUyTS7SzV4/summary.md
    title: Every Company Should Have a Brain (video summary)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: ai-native-company-structure-video
    resource: https://github.com/kelvinlee97/engineering/blob/main/YouTube/startup/building-and-structuring-an-ai-native-company--Z3JyAqh4ixg/summary.md
    title: Building and Structuring an AI-Native Company (video summary)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:45:00Z }
status: draft
---
A company brain, in Garry Tan's framing, is both a library (emails, meetings, decisions, customer conversations, postmortems) and a librarian that selects the small subset relevant to the current task. A company holds far more than any single context window, so the selection is the point.[^company-brain-video] Another YC talk describes the same idea as organizational data plus reinforcing loops that can access it, so intelligence lives in the system rather than being routed through management.[^ai-native-company-structure-video]

## Memory needs hygiene

Tan warns that an uncurated brain becomes a searchable garbage dump: stale facts come back confidently, and a bad skill preserves a bad process. His remedy is memory plus hygiene: provenance for facts, contradiction checks, and human-plus-agent curation that prunes obsolete material, treated as production infrastructure.[^company-brain-video]

(Analysis: this is the problem this wiki's own conventions address: `sources` and footnotes for provenance, a `## Contradictions` section, and lint passes for stale pages.)

## Skills as the organization

Tan maps agent infrastructure to a company: a skill file is an employee with one capability, a resolver table is the org chart, filing rules are procedures, and trigger evaluations are performance reviews.[^company-brain-video] His rule is never to do one-off work: once a recurring task comes out right, keep the process as a skill; "model quality is rented, but the accumulated organizational brain is owned."[^company-brain-video]

## Put each computation on the right side

Use the model for judgment and vague intent; use ordinary code and data structures for exact storage and repeatable computation. In his seating example, a model can judge who should meet, but the exact arrangement of 800 seats belongs in deterministic structures.[^company-brain-video] See [Deterministic checks and model judgment](deterministic-vs-model-work.md).

## Related

- [AI-native company](ai-native-company.md)
- [Agent skill](../claude-code/agent-skill.md)
- Source: [Every company should have a brain](../../sources/company-brain-video.md)
- Source: [Building and structuring an AI-native company](../../sources/ai-native-company-structure-video.md)

[^company-brain-video]: Every Company Should Have a Brain (video summary)
[^ai-native-company-structure-video]: Building and Structuring an AI-Native Company (video summary)
