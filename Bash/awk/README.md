# The `awk` command

Chinese version: [README_ZH.md](README_ZH.md)

## Mental model

> `awk` is a tiny per-line programming language: for every input line it splits the line into numbered fields (`$1`, `$2`, ... `$NF`) and runs your `condition { action }` against them, so most tasks reduce to picking the right field number and the right condition.

`awk` processes text one line at a time. Its name uses the initials of its authors: Aho, Weinberger, and Kernighan. It is useful for selecting columns, filtering rows, and performing simple calculations on logs or tabular text.

## Basic syntax

```bash
awk 'condition { action }' file
```

By default, `awk` splits fields on whitespace: `$1` is the first field, `$2` the second, `$0` the whole line, and `NF` the number of fields in the current line.

```bash
awk '{print $1}' ../access.log       # print the client IP
awk '$9 >= 500 {print $1, $9}' ../access.log  # print IPs and 5xx statuses
awk '{print $NF}' ../access.log      # print the last field
```

Use `-F` for another delimiter. For example, `/etc/passwd` uses colons:

```bash
awk -F: '{print $1}' /etc/passwd
```

## Finding the field number

Ask `awk` to print each field number and value from the first line:

```bash
awk 'NR == 1 {for (i = 1; i <= NF; i++) print i, $i}' ../access.log
```

Part of the output is:

```text
1 10.1.1.1
2 -
3 -
4 [04/Sep/2026:10:00:01
5 +0800]
6 "GET
7 /api/ads
8 HTTP/1.1"
9 200
10 512
```

The useful whitespace-separated fields in this file are:

| `awk` field | Content |
|---|---|
| `$1` | Client IP |
| `$7` | Request path |
| `$9` | HTTP status code |
| `$10` | Response size in bytes |

Quotes do not stop `awk` from splitting on spaces, so `"GET /api/ads HTTP/1.1"` becomes `$6`, `$7`, and `$8`. Real User-Agent values may contain several spaces, making later field numbers unstable; use quotes as the delimiter for such content instead of guessing a field number.

## Common use cases

- Extract IP addresses, status codes, or other fields from logs.
- Filter records by a field value, such as all 5xx requests.
- Sum a numeric field or count rows.
- Pass one field to commands such as `sort` and `uniq`.

Count requests per IP in `access.log`:

```bash
awk '{print $1}' ../access.log | sort | uniq -c | sort -nr
```

Here `awk` only selects the first field; the remaining commands sort, count, and rank it.

## Looking up help on site

Try this first in a typical GNU/Linux environment:

```bash
awk --help
```

If `--help` is unsupported, use the system manual:

```bash
man awk
```

Inside `man`, type `/pattern` to search for `pattern`, press `n` for the next match, and `q` to quit. Restricted environments such as HackerRank may omit `man`; use `awk --help 2>&1 | less` when the available help is too long for one screen.
