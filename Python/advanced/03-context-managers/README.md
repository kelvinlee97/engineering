# Python Context Managers Cheatsheet

> `with` guarantees a cleanup call happens exactly once, whether the block finishes normally or raises: entry runs before the block, and exit always runs after it, even on an exception.

```mermaid
flowchart TD
    accTitle: with-statement acquire, run, and guaranteed release
    accDescr: The with statement calls enter to acquire the resource, then runs the block. Whether the block finishes normally or raises an exception, exit always runs to release the resource; an unhandled exception propagates afterward.
    A[__enter__ acquires resource] --> B[Run with-block body]
    B --> C{Exception raised in block?}
    C -- No --> D[__exit__ releases resource]
    C -- Yes --> E[__exit__ releases resource]
    D --> F[Continue after with-block]
    E --> G{__exit__ suppresses exception?}
    G -- No --> H[Exception propagates]
    G -- Yes --> F
```

A context manager acquires a resource on entry and reliably releases it on exit.

```python
from pathlib import Path

with Path("app.log").open(encoding="utf-8") as file:
    first_line = file.readline()
```

Use `contextlib.contextmanager` for a small function-based context manager:

```python
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def transaction(database: object) -> Iterator[object]:
    try:
        yield database
        database.commit()
    except Exception:
        database.rollback()
        raise
```

Use `with` for files, locks, database transactions, and temporary state. Do not replace it with manual cleanup when the object already supports the context-manager protocol.
