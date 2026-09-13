# Python 类型标注速查表

English version: [README.md](README.md)

```python
def count_errors(statuses: list[int]) -> int:
    return sum(500 <= status < 600 for status in statuses)


def find(name: str) -> str | None:
    return name if name else None
```

类型标注用于说明意图并支持静态检查器；Python 不会在运行时强制执行这些类型。

```python
from collections.abc import Iterable, Mapping
from typing import TypeAlias

StatusCounts: TypeAlias = dict[int, int]


def summarize(values: Iterable[int]) -> Mapping[int, int]:
    return {value: 1 for value in values}
```

函数只需要某种行为时，输入应接受 `Iterable` 或 `Mapping` 等抽象类型。调用方需要知道具体结果时，返回值可使用具体类型。未知值应使用 `object`，并在使用前缩小类型；只有确实要绕过类型检查时才使用 `Any`。
