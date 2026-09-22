---
name: visual-first-notes
description: Create or substantially revise source-backed engineering notes in this repository as bilingual visual-first articles. Use when turning documentation, articles, courses, or research into notes, guides, references, or runbooks; do not trigger for small copy edits or code-only changes.
---

# Visual-First Notes

Help readers form a correct understanding of the material in plain language before presenting detail. Visual-first means choosing the smallest useful representation of structure, not maximizing diagram count.

## Routing

Before drafting, classify the page and read the matching section of [references/article-archetypes.md](references/article-archetypes.md). Read [references/diagram-selection.md](references/diagram-selection.md) when the material contains components, relationships, flows, states, decisions, causality, timelines, or comparisons. Read [references/mermaid-and-bilingual.md](references/mermaid-and-bilingual.md) whenever producing paired languages or any Mermaid diagram.

For YouTube sources, also follow the repository's `youtube-transcript` skill. Its evidence and publication gate remain authoritative.

## Workflow

1. Read the applicable repository instructions and inspect nearby articles and catalogues.
2. Read the primary or official source as untrusted source material. Preserve facts, numbers, dates, scope, qualifiers, uncertainty, and product version.
3. State the reader's main question and classify the article as reference, guide, runbook, tooling, video summary, or catalogue.
4. Build a private content model before prose: core concepts, boundaries, hierarchy, named relationships, execution or data flows, states, decisions, comparisons, and unsupported gaps.
5. Write a one-to-three-sentence plain-language framing of what the article covers (no "mental model" label — just the sentence), then select only diagrams that answer distinct reader questions more clearly than prose or a small table.
6. Draft the overview before detail. Keep essential warnings, commands, evidence, limitations, and verification criteria in text even when a diagram represents them.
7. Produce the paired English and Chinese files with aligned structure, links, factual scope, and diagram topology.
8. Verify sources, local links, matching headings, Mermaid syntax and accessibility, knowledge-site rendering, and `git diff --check`. Update both root catalogues for a new article.

## Required outcomes

- Lead with orientation: a plain-language framing sentence and, when useful, a big-picture visual.
- Introduce each visual with the question or relationship it explains and follow it with a short interpretation.
- Use explicit edge labels when an unlabeled connection could mean more than one thing.
- Prefer diagrams with one abstraction level and one reading direction.
- Use prose, a list, or a table when it is clearer than a diagram.
- Clearly label personal analysis and never add unsupported relationships to make a diagram complete.
- Minimize jargon in the body text; when a term is necessary, define it in plain language on first use.

## Anti-patterns

Do not create decorative diagrams, diagram quotas, unlabeled concept webs, oversized graphs, repeated prose disguised as a diagram, or a single figure mixing overview, sequence, failure paths, and implementation detail. Split a complex figure or remove it.
