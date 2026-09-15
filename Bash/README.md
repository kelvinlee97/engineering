# Bash SRE HackerRank Quick Reference

Chinese version: [README_ZH.md](README_ZH.md)

## Mental model

> Each question below is answered by chaining a few small Unix filters (`awk`, `cut`, `sort`, `uniq`, `grep`) into one pipeline over the same log file; the same handful of building blocks recombine to answer almost any "top N", "count per X", or "filter by Y" interview question.

Use [`access.log`](access.log) below. It simulates an Nginx combined access log containing the client IP, identity fields, time, HTTP request, status, response size, Referer, and User-Agent. Run commands from the repository root.

## Command guides

- [`awk`](awk/README.md): select columns, filter rows, and aggregate text.
- [`uniq`](uniq/README.md): remove or count adjacent duplicate lines.

## Q1: Find the top five client IPs

```bash
awk '{print $1}' Bash/access.log | sort | uniq -c | sort -nr | head -5
```

**Output:** `10.1.1.1` has 4 requests and `10.1.1.2` has 2; the remaining IPs have 1 each. `awk` prints field 1; `sort` groups identical values; `uniq -c` counts adjacent duplicates; `sort -nr` sorts numerically in reverse; `head -5` keeps five lines.

## Q2: Count requests per path

```bash
cut -d'"' -f2 Bash/access.log | cut -d' ' -f2 | sort | uniq -c | sort -nr
```

**Output:** `5 /api/ads`, `3 /api/click`, and `2 /health`. The first `cut` extracts the quoted request. The second extracts its space-delimited path. `sort`, `uniq -c`, and `sort -nr` group, count, and rank the paths.

## Q3: Count distinct IPs

```bash
awk '{print $1}' Bash/access.log | sort -u | wc -l
```

**Output:** `6`. `sort -u` sorts and removes duplicates; `wc -l` counts lines.

## Q4: Select exact `/api/ads` requests

```bash
grep ' /api/ads HTTP/' Bash/access.log
```

`grep` prints matching lines. Including the following `HTTP/` avoids matching a path such as `/api/ads-v2` while keeping the command easy to write.

## Q5: Count each HTTP method

```bash
cut -d'"' -f2 Bash/access.log | cut -d' ' -f1 | sort | uniq -c | sort -nr
```

**Output:** `8 GET` and `2 POST`. The two `cut` commands extract the quoted request and then its method. The remaining pipeline groups, counts, and ranks the methods.

## Q6: Show the five most memory-intensive Linux processes

```bash
ps aux --sort=-%mem | head -6
```

`ps aux` shows detailed processes; `--sort=-%mem` sorts memory percentage descending; six lines retain the header and five processes. On macOS use:

```bash
ps aux | head -1 && ps aux | tail -n +2 | sort -k4 -nr | head -5
```

`tail -n +2` removes the header, and `sort -k4 -nr` sorts numerically and descending from column 4.

## Common options

| Command | Option | Meaning |
|---|---|---|
| `sort` | `-n` | Compare numbers |
| `sort` | `-r` | Reverse order |
| `sort` | `-u` | Remove duplicate lines |
| `sort` | `-k4` | Sort starting at field 4 |
| `cut` | `-d'"'` | Use a double quote as the field delimiter |
| `cut` | `-f2` | Print field 2 |
| `uniq` | `-c` | Count adjacent duplicates |
| `head` | `-n 5` | Print the first five lines |
| `tail` | `-n 20` | Print the last 20 lines |
| `tail` | `-f` | Follow appended content |
| `wc` | `-l` | Count lines |
| `grep` | `-i` | Ignore case |
| `grep` | `-v` | Print nonmatching lines |
| `grep` | `-c` | Count matching lines |

## Interview sequence

1. Confirm columns and delimiters.
2. Explain each pipeline stage's input and output.
3. Verify counts and sort direction with a small log.
4. Remember that `uniq` normally needs sorted input.
5. Distinguish Linux GNU options from macOS BSD options.
