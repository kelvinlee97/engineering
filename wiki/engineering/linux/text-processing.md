---
type: Command
title: Text processing on the command line
description: Building shell pipelines for text, with awk for fields and uniq for duplicates.
tags:
- linux
- bash
- text-processing
aliases:
- engineering/linux/text-processing-pipelines
- engineering/linux/awk
- engineering/linux/uniq
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
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
Most log questions (top N, count per X, filter by Y) are answered by chaining small Unix filters into one pipeline. This page shows the standard pipeline shape, then the two filters that need the most explanation: `awk` for picking fields and `uniq` for collapsing duplicates.

## Text-processing pipelines

A handful of small Unix filters, chained into one pipeline over a log file, answer most "top N", "count per X", and "filter by Y" questions.[^bash-quick-reference] Each stage does one thing: select a field, group identical values, count them, rank them.

### The standard shape

`awk '{print $1}' Bash/access.log | sort | uniq -c | sort -nr | head -5` finds the top five client IPs: [`awk`](#awk) prints field 1, `sort` groups identical values, [`uniq`](#uniq) `-c` counts adjacent duplicates, `sort -nr` ranks numerically in reverse, and `head -5` keeps five lines.

| Question | Pipeline |
| --- | --- |
| Requests per path | `cut -d'"' -f2` then `cut -d' ' -f2`, then `sort \| uniq -c \| sort -nr` |
| Distinct IPs | `awk '{print $1}' \| sort -u \| wc -l` |
| Exact path match | `grep ' /api/ads HTTP/'`, so `/api/ads-v2` does not match |
| Requests per method | `cut -d'"' -f2 \| cut -d' ' -f1 \| sort \| uniq -c \| sort -nr` |
| Top memory processes | `ps aux --sort=-%mem \| head -6` on Linux |

As given in the quick reference.[^bash-quick-reference]

### Pitfalls

- `uniq` only collapses adjacent identical lines, so it normally needs sorted input.[^bash-uniq]
- Quotes do not stop `awk` from splitting on spaces, and User-Agent values contain spaces, so later field numbers are unstable; cut on the quote character instead.[^bash-awk]
- GNU and BSD options differ: `ps --sort` is Linux-only, and macOS needs `ps aux | tail -n +2 | sort -k4 -nr`.[^bash-quick-reference]

## awk

`awk` processes text one line at a time: it splits each line into fields and runs `condition { action }` rules against them. The name comes from its authors, Aho, Weinberger, and Kernighan.[^bash-awk]

### Essentials

| Syntax | Meaning |
| --- | --- |
| `$1`, `$2` | First and second fields (whitespace-separated by default) |
| `$0` | The whole line |
| `NF`, `$NF` | Number of fields; the last field |
| `NR` | Current line number |
| `-F:` | Use another delimiter, such as `:` for `/etc/passwd` |

As described in the note. Examples: `awk '$9 >= 500 {print $1, $9}'` prints the IP and status of 5xx requests in the sample log.[^bash-awk]

### Finding a field number

`awk 'NR == 1 {for (i = 1; i <= NF; i++) print i, $i}' file` prints every field of the first line with its number. In the sample combined log, `$1` is the client IP, `$7` the path, `$9` the status, and `$10` the response size.

When `--help` is unsupported, use `man awk`; in restricted environments such as HackerRank, `awk --help 2>&1 | less`.[^bash-awk]

## uniq

`uniq` (from "unique") combines identical lines only when they are adjacent; it has no memory of earlier lines. That is why it almost always comes right after `sort`.

| Option | Effect |
| --- | --- |
| `-c` | Prefix each line with its count |
| `-d` | Show only repeated lines |
| `-u` | Show only lines that occur once |
| `-i` | Ignore case |

As listed in the note. If you only need sorted, deduplicated output, `sort -u` does both. The macOS/BSD version may not support `--help`; use `man uniq`.[^bash-uniq]

## Related
- [Domain index](index.md): other pages in this domain.

[^bash-quick-reference]: [Bash SRE HackerRank Quick Reference](../../sources/bash-quick-reference.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Bash/README.md)
[^bash-awk]: [The awk command](../../sources/bash-awk.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Bash/awk/README.md)
[^bash-uniq]: [The uniq command](../../sources/bash-uniq.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Bash/uniq/README.md)
