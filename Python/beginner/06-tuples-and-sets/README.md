# Python Tuples and Sets Cheatsheet

Chinese version: [README_ZH.md](README_ZH.md)

## Tuples

```python
point = (10, 20)
x, y = point
single = (10,)
host, port = "localhost", 8080
```

Tuples are immutable and useful for fixed records or multiple return values. A one-item tuple needs a trailing comma.

## Sets

```python
left = {"api", "web"}
right = {"web", "worker"}

left | right  # union
left & right  # intersection
left - right  # difference
left ^ right  # symmetric difference

left.add("cron")
left.discard("missing")  # no error when absent
```

Sets store unique hashable values and do not support indexing. Create an empty set with `set()`, because `{}` creates a dictionary.
