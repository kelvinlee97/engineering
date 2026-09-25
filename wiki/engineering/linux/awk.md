---
type: Command
title: awk
description: A small per-line language that splits each line into numbered fields and runs condition-action rules against them.
tags: [bash, awk, linux]
sources:
  - id: bash-awk
    resource: https://github.com/kelvinlee97/engineering/blob/main/Bash/awk/README.md
    title: The awk command
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:15:00Z }
status: draft
---
`awk` processes text one line at a time: it splits each line into fields and runs `condition { action }` rules against them. The name comes from its authors, Aho, Weinberger, and Kernighan.[^bash-awk]

## Essentials

| Syntax | Meaning |
| --- | --- |
| `$1`, `$2` | First and second fields (whitespace-separated by default) |
| `$0` | The whole line |
| `NF`, `$NF` | Number of fields; the last field |
| `NR` | Current line number |
| `-F:` | Use another delimiter, such as `:` for `/etc/passwd` |

As described in the note.[^bash-awk] Examples: `awk '$9 >= 500 {print $1, $9}'` prints the IP and status of 5xx requests in the sample log.[^bash-awk]

## Finding a field number

`awk 'NR == 1 {for (i = 1; i <= NF; i++) print i, $i}' file` prints every field of the first line with its number. In the sample combined log, `$1` is the client IP, `$7` the path, `$9` the status, and `$10` the response size.[^bash-awk]

When `--help` is unsupported, use `man awk`; in restricted environments such as HackerRank, `awk --help 2>&1 | less`.[^bash-awk]

## Related

- [Text-processing pipelines](text-processing-pipelines.md)
- Source: [The awk command](../../sources/bash-awk.md)

[^bash-awk]: The awk command
