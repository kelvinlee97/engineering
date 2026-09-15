# Python 字典速查表

English version: [README.md](README.md)

## 心智模型

> 字典把可哈希的键映射到值，并记住插入顺序。键缺失属于错误时用 `mapping[key]`，需要默认值时用 `get()` 或 `setdefault()`。

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

字典键必须可哈希。键缺失属于错误时使用 `mapping[key]`；允许默认值时使用 `get()`。字典保留插入顺序，但字典是否相等只取决于键值对，不取决于顺序。
