---
type: Command
title: uniq
description: Collapses or counts adjacent identical lines, which is why it almost always follows sort.
tags: [bash, uniq, linux]
sources:
  - id: bash-uniq
    resource: https://github.com/kelvinlee97/engineering/blob/main/Bash/uniq/README.md
    title: The uniq command
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:15:00Z }
status: draft
---
`uniq` (from "unique") combines identical lines only when they are adjacent; it has no memory of earlier lines. That is why it almost always comes right after `sort`.[^bash-uniq]

| Option | Effect |
| --- | --- |
| `-c` | Prefix each line with its count |
| `-d` | Show only repeated lines |
| `-u` | Show only lines that occur once |
| `-i` | Ignore case |

As listed in the note.[^bash-uniq] If you only need sorted, deduplicated output, `sort -u` does both.[^bash-uniq] The macOS/BSD version may not support `--help`; use `man uniq`.[^bash-uniq]

## Related

- [Text-processing pipelines](text-processing-pipelines.md)
- Source: [The uniq command](../../sources/bash-uniq.md)

[^bash-uniq]: The uniq command
