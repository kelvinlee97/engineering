---
type: Pattern
title: Text-processing pipelines
description: Answer log questions by chaining small Unix filters such as awk, cut, sort, uniq, grep, and wc into one pipeline.
tags: [bash, linux, logs]
sources:
  - id: bash-quick-reference
    resource: https://github.com/kelvinlee97/engineering/blob/main/Bash/README.md
    title: Bash SRE HackerRank Quick Reference
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: bash-awk
    resource: https://github.com/kelvinlee97/engineering/blob/main/Bash/awk/README.md
    title: The awk command
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: bash-uniq
    resource: https://github.com/kelvinlee97/engineering/blob/main/Bash/uniq/README.md
    title: The uniq command
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:15:00Z }
status: draft
---
A handful of small Unix filters, chained into one pipeline over a log file, answer most "top N", "count per X", and "filter by Y" questions.[^bash-quick-reference] Each stage does one thing: select a field, group identical values, count them, rank them.

## The standard shape

`awk '{print $1}' Bash/access.log | sort | uniq -c | sort -nr | head -5` finds the top five client IPs: [`awk`](awk.md) prints field 1, `sort` groups identical values, [`uniq`](uniq.md) `-c` counts adjacent duplicates, `sort -nr` ranks numerically in reverse, and `head -5` keeps five lines.[^bash-quick-reference]

| Question | Pipeline |
| --- | --- |
| Requests per path | `cut -d'"' -f2` then `cut -d' ' -f2`, then `sort \| uniq -c \| sort -nr` |
| Distinct IPs | `awk '{print $1}' \| sort -u \| wc -l` |
| Exact path match | `grep ' /api/ads HTTP/'`, so `/api/ads-v2` does not match |
| Requests per method | `cut -d'"' -f2 \| cut -d' ' -f1 \| sort \| uniq -c \| sort -nr` |
| Top memory processes | `ps aux --sort=-%mem \| head -6` on Linux |

As given in the quick reference.[^bash-quick-reference]

## Pitfalls

- `uniq` only collapses adjacent identical lines, so it normally needs sorted input.[^bash-uniq]
- Quotes do not stop `awk` from splitting on spaces, and User-Agent values contain spaces, so later field numbers are unstable; cut on the quote character instead.[^bash-awk]
- GNU and BSD options differ: `ps --sort` is Linux-only, and macOS needs `ps aux | tail -n +2 | sort -k4 -nr`.[^bash-quick-reference]

## Related

- Source: [Bash SRE quick reference](../../sources/bash-quick-reference.md)
- Source: [The awk command](../../sources/bash-awk.md)
- Source: [The uniq command](../../sources/bash-uniq.md)

[^bash-quick-reference]: Bash SRE HackerRank Quick Reference
[^bash-uniq]: The uniq command
[^bash-awk]: The awk command
