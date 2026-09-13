# Python SRE HackerRank Quick Reference

Chinese version: [README_ZH.md](README_ZH.md)

Use [`examples/app.log`](examples/app.log) below. It simulates an Nginx combined access log containing the client IP, identity fields, time, HTTP request, status, response size, Referer, and User-Agent. Run examples from the repository root.

## Beginner

| Topic | Cheatsheet |
|---|---|
| 00. Variables and types | [English](beginner/00-variables-and-types/README.md) · [中文](beginner/00-variables-and-types/README_ZH.md) |
| 01. Strings | [English](beginner/01-strings/README.md) · [中文](beginner/01-strings/README_ZH.md) |
| 02. Control flow | [English](beginner/02-control-flow/README.md) · [中文](beginner/02-control-flow/README_ZH.md) |
| 03. Lists | [English](beginner/03-lists/README.md) · [中文](beginner/03-lists/README_ZH.md) |
| 04. Loops | [English](beginner/04-loops/README.md) · [中文](beginner/04-loops/README_ZH.md) |
| 05. Dictionaries | [English](beginner/05-dictionaries/README.md) · [中文](beginner/05-dictionaries/README_ZH.md) |
| 06. Tuples and sets | [English](beginner/06-tuples-and-sets/README.md) · [中文](beginner/06-tuples-and-sets/README_ZH.md) |
| 07. Functions | [English](beginner/07-functions/README.md) · [中文](beginner/07-functions/README_ZH.md) |
| 08. Comprehensions | [English](beginner/08-comprehensions/README.md) · [中文](beginner/08-comprehensions/README_ZH.md) |
| 09. Exceptions | [English](beginner/09-exceptions/README.md) · [中文](beginner/09-exceptions/README_ZH.md) |
| 10. Files and paths | [English](beginner/10-files-and-paths/README.md) · [中文](beginner/10-files-and-paths/README_ZH.md) |
| 11. Modules and packages | [English](beginner/11-modules-and-packages/README.md) · [中文](beginner/11-modules-and-packages/README_ZH.md) |
| 12. Testing | [English](beginner/12-testing/README.md) · [中文](beginner/12-testing/README_ZH.md) |

## Advanced

| Topic | Cheatsheet |
|---|---|
| 00. Classes | [English](advanced/00-classes/README.md) · [中文](advanced/00-classes/README_ZH.md) |
| 01. Type hints | [English](advanced/01-typing/README.md) · [中文](advanced/01-typing/README_ZH.md) |
| 02. Iterators and generators | [English](advanced/02-iterators-and-generators/README.md) · [中文](advanced/02-iterators-and-generators/README_ZH.md) |
| 03. Context managers | [English](advanced/03-context-managers/README.md) · [中文](advanced/03-context-managers/README_ZH.md) |
| 04. Decorators | [English](advanced/04-decorators/README.md) · [中文](advanced/04-decorators/README_ZH.md) |

## Q1: Count 5xx requests

**Question:** Read a potentially large Nginx log line by line and count HTTP status codes from 500 through 599.

**Answer:**

```python
server_errors = 0

with open("Python/examples/app.log", encoding="utf-8") as file:
    for line in file:
        parts = line.split('"')
        if len(parts) >= 3:
            response = parts[2].split()
            if not response:
                continue

            status = int(response[0])
            if 500 <= status <= 599:
                server_errors += 1

print(server_errors)
```

**Output:** `3`

After splitting around quoted fields, `parts[2]` starts with the status code. Iterating over the file avoids loading it into memory. Time is `O(n)` and extra space is `O(1)`.

## Q2: Count each HTTP status code

**Question:** Count each HTTP status code and print the results by decreasing frequency.

**Answer:**

```python
statuses = {}

with open("Python/examples/app.log", encoding="utf-8") as file:
    for line in file:
        parts = line.split('"')
        if len(parts) >= 3:
            response = parts[2].split()
            if response:
                status = response[0]
                statuses[status] = statuses.get(status, 0) + 1

for status in sorted(statuses, key=lambda key: statuses[key], reverse=True):
    print(status, statuses[status])
```

**Output:**

```text
200 4
201 2
500 1
502 1
404 1
503 1
```

`dict.get(status, 0)` starts unseen statuses at zero. `sorted()` uses the dictionary count as its key, and `reverse=True` orders the result from largest to smallest. Scanning is `O(n)`; sorting `k` statuses is `O(k log k)`.

## Q3: Find the top N request paths

**Question:** Implement `top_paths(path, n)` to return the most frequently requested URL paths and their counts.

**Answer:**

```python
def top_paths(path: str, n: int) -> list[tuple[str, int]]:
    paths = {}
    with open(path, encoding="utf-8") as file:
        for line in file:
            parts = line.split('"')
            if len(parts) >= 2:
                request = parts[1].split()
                if len(request) == 3:
                    url_path = request[1]
                    paths[url_path] = paths.get(url_path, 0) + 1
    ranked = sorted(paths.items(), key=lambda item: item[1], reverse=True)
    return ranked[:n]


print(top_paths("Python/examples/app.log", 2))
```

**Output:** `[('/api/ads', 5), ('/api/click', 3)]`. The quoted request is split into method, path, and protocol, and `ranked[:n]` returns only the requested results. Scanning `m` lines is `O(m)`; sorting `k` paths is `O(k log k)` and uses `O(k)` counting space.

## Q4: Find duplicate request IDs

```python
def find_duplicates(request_ids: list[str]) -> list[str]:
    seen = set()
    duplicates = set()
    result = []
    for request_id in request_ids:
        if request_id in seen and request_id not in duplicates:
            duplicates.add(request_id)
            result.append(request_id)
        seen.add(request_id)
    return result


print(find_duplicates(["a1", "a2", "a3", "a1", "a4", "a2", "a1"]))
```

**Output:** `['a1', 'a2']`. Set operations are `O(1)` on average, giving `O(n)` average time and `O(n)` space.

## Q5: Two Sum

```python
def two_sum(numbers: list[int], target: int) -> list[int]:
    seen = {}
    for index, number in enumerate(numbers):
        required = target - number
        if required in seen:
            return [seen[required], index]
        seen[number] = index
    return []


print(two_sum([2, 7, 11, 15], 9))
```

**Output:** `[0, 1]`. The dictionary makes complement lookup `O(1)` on average, for `O(n)` time and space.

## Q6: Maximum fixed-window request count

```python
def max_window_sum(requests: list[int], size: int) -> int:
    if size <= 0 or size > len(requests):
        raise ValueError("size must be between 1 and len(requests)")
    current = sum(requests[:size])
    maximum = current
    for index in range(size, len(requests)):
        current += requests[index] - requests[index - size]
        maximum = max(maximum, current)
    return maximum


print(max_window_sum([10, 20, 30, 10, 50], 3))
```

**Output:** `90`. Updating the entering and leaving values gives `O(n)` time and `O(1)` extra space.

## Interview sequence

1. Confirm input, output, and invalid-input behavior.
2. Explain the algorithm with a small example.
3. Write the smallest runnable solution.
4. Test empty input, duplicates, no result, and boundaries.
5. State time and space complexity.
