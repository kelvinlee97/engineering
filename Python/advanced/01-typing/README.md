# Python Type Hints Cheatsheet

> Type hints are documentation checked by external tools, not by the interpreter: accept the most abstract type a function can work with, and return the most concrete type callers can rely on.

```python
def count_errors(statuses: list[int]) -> int:
    return sum(500 <= status < 600 for status in statuses)


def find(name: str) -> str | None:
    return name if name else None
```

Type hints document intent and support static checkers; Python does not enforce them at runtime.

```python
from collections.abc import Iterable, Mapping
from typing import TypeAlias

StatusCounts: TypeAlias = dict[int, int]


def summarize(values: Iterable[int]) -> Mapping[int, int]:
    return {value: 1 for value in values}
```

Accept abstract input types such as `Iterable` or `Mapping` when the function needs only that behavior. Return concrete types when callers benefit from knowing the result. Use `object` for an unknown value that must be narrowed before use; avoid `Any` unless type checking truly needs to be bypassed.
