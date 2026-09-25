---
type: Source Summary
title: Bash SRE quick reference (summary)
description: Summary of the legacy interview quick reference that answers log questions with short Unix filter pipelines.
tags: [bash, linux, interview]
sources:
  - id: bash-quick-reference
    resource: https://github.com/kelvinlee97/engineering/blob/main/Bash/README.md
    title: Bash SRE HackerRank Quick Reference
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:15:00Z }
status: draft
---
A quick reference in this repository, `Bash/README.md`, answering SRE interview questions over a simulated Nginx combined access log (`Bash/access.log`) with pipelines of `awk`, `cut`, `sort`, `uniq`, `grep`, and `wc`.[^bash-quick-reference]

## Takeaways

- A few filters recombine to answer most "top N", "count per X", and "filter by Y" questions.[^bash-quick-reference] See [Text-processing pipelines](../engineering/linux/text-processing.md#text-processing-pipelines).

[^bash-quick-reference]: Bash SRE HackerRank Quick Reference, [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/Bash/README.md)
