# Diagram Selection

Choose the visual by the relationship in the source, not by appearance.

| Reader question or information structure | Preferred form | Notes |
| --- | --- | --- |
| What is inside the system and where is its boundary? | Architecture or layer diagram | Group by boundary and keep one abstraction level |
| How does a request, event, or message move? | Sequence diagram | Use when actor order and interaction timing matter |
| What happens next or which branch should I take? | Flowchart or decision tree | Make the start and terminal states obvious |
| Which states exist and what causes transitions? | State diagram | Label transition conditions |
| How do concepts depend on or specialize each other? | Concept or relationship map | Use meaningful linking phrases |
| What caused the incident and what follows from it? | Cause-effect diagram | Separate evidence from inference |
| How do options differ on shared dimensions? | Markdown comparison table | Do not use a diagram for tabular facts |
| What happened in chronological order? | Timeline | Use only when dates or sequence are the point |
| How does a broad topic decompose? | Knowledge tree or mind map | Prefer a hierarchy for readers new to the topic |

## Selection test

Before keeping a visual, answer all four questions:

1. What precise reader question does it answer?
2. Which relationship becomes clearer than it was in prose?
3. Can the diagram be understood without guessing what an edge means?
4. Would removing it make the article harder to understand?

If the fourth answer is no, remove the diagram.

## Complexity guidance

- Aim for roughly 5–12 meaningful nodes in one figure; this is guidance, not a hard limit.
- Split figures that mix overview, normal flow, failure flow, and implementation detail.
- Use top-to-bottom direction for narrow/mobile layouts unless left-to-right materially improves the relationship.
- Keep labels short and place essential qualifications in adjacent prose.
- Reuse consistent terms and shapes within an article.
