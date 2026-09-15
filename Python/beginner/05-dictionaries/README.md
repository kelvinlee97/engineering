# Python Dictionaries Cheatsheet

Chinese version: [README_ZH.md](README_ZH.md)

## Mental model

> A dictionary maps hashable keys to values and remembers insertion order. Choose `mapping[key]` when a missing key is an error and `get()`/`setdefault()` when a default is valid.

```python
status_counts = {200: 4, 500: 1}
status_counts[200]             # 4
status_counts.get(404, 0)      # 0
status_counts[503] = 1
status_counts[500] += 1
status_counts.setdefault(429, 0)
```

```python
for status, count in status_counts.items():
    print(status, count)

keys = status_counts.keys()
values = status_counts.values()
removed = status_counts.pop(500, None)
merged = status_counts | {201: 2}  # Python 3.9+
```

Keys must be hashable. Access with `mapping[key]` when absence is an error; use `get()` when a default is valid. Dictionaries preserve insertion order, but equality depends on key-value pairs rather than order.
