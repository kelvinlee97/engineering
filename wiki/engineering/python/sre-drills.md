---
type: Playbook
title: SRE Python drills
description: Six interview-style Python drills on an Nginx access log, each solved with the smallest correct algorithm and its time and space cost.
tags: [python]
sources:
  - id: py-sre-drills
    resource: https://github.com/kelvinlee97/engineering/blob/main/Python/README.md
    title: Python SRE HackerRank Quick Reference
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T13:00:00Z }
status: draft
---
The index of the Python notes doubles as a drill set: small HackerRank-style SRE questions on a sample Nginx combined access log, each answered with the smallest correct algorithm and its stated time and space cost.

## The drills

| Drill | Technique | Cost |
| --- | --- | --- |
| Count 5xx requests | Stream the file line by line and read the status after the quoted request | `O(n)` time, `O(1)` space |
| Count each status | `dict.get(status, 0)`, then `sorted` by count | `O(n)` scan, `O(k log k)` sort |
| Top N paths | Split the quoted request into method, path, protocol; slice `[:n]` | `O(m)` scan, `O(k log k)` sort |
| Duplicate request IDs | A `seen` set and a `duplicates` set | `O(n)` average |
| Two Sum | A dictionary of complements | `O(n)` time and space |
| Maximum fixed-window count | Slide the window, adding the entering value and removing the leaving one | `O(n)` time, `O(1)` space |

As listed in the source.[^py-sre-drills]

## Answering in an interview

```mermaid
flowchart LR
    accTitle: Interview answer sequence
    accDescr: Confirm the contract, explain with a small example, write the smallest runnable solution, test edge cases, then state complexity.
    A[Confirm inputs and outputs] --> B[Explain with an example]
    B --> C[Smallest runnable solution]
    C --> D[Test edge cases]
    D --> E[State time and space]
```

Confirm input, output, and invalid-input behavior; explain the algorithm on a small example; write the smallest runnable solution; test empty input, duplicates, no result, and boundaries; then state time and space complexity.[^py-sre-drills]

## Related

- [Text processing](../linux/text-processing.md): the same log parsing with awk and uniq.
- [Python language fundamentals](fundamentals.md)
- [Python program structure](structure.md)
- [Domain index](index.md)

[^py-sre-drills]: [Python SRE HackerRank Quick Reference](../../sources/py-sre-drills.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Python/README.md)
