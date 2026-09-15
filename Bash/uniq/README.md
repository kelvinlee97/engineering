# The `uniq` command

Chinese version: [README_ZH.md](README_ZH.md)

## Mental model

> `uniq` only collapses lines that are already **adjacent and identical**; it has no memory of lines seen earlier. That is why it is almost always chained right after `sort`, which brings matching lines next to each other first.

`uniq` is not an acronym and has no expanded form; its name comes from **unique**. It combines identical lines that appear next to each other.

```text
input              output
apple              apple
apple    uniq      banana
banana    ───▶     apple
apple
```

The last `apple` remains because it is separated from the first two. Real data is often unordered, so `sort` normally comes first to place identical lines together:

```bash
sort names.txt | uniq
```

## Common use cases

- Remove duplicate names, IP addresses, or log fields.
- Count occurrences of each IP, username, or error message.
- Find values that occur more than once or exactly once.

## Common options

```bash
sort names.txt | uniq -c  # show the count for each line
sort names.txt | uniq -d  # show only repeated lines
sort names.txt | uniq -u  # show only lines that occur once
sort names.txt | uniq -i  # compare without regard to case
```

If only sorting and deduplication are needed, use:

```bash
sort -u names.txt
```

Count requests per IP in `access.log`:

```bash
awk '{print $1}' ../access.log | sort | uniq -c | sort -nr
```

## Looking up help on site

Try this first in a typical GNU/Linux environment:

```bash
uniq --help
```

If `--help` is unsupported, use the system manual:

```bash
man uniq
```

Inside `man`, type `/-c` to search for `-c`, press `n` for the next match, and `q` to quit. The macOS/BSD version of `uniq` may not support `--help`; rely on `man uniq` there.
