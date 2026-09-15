# Python Functions Cheatsheet

Chinese version: [README_ZH.md](README_ZH.md)

## Mental model

> A function signature is a contract: positional parameters, `*`-separated keyword-only parameters, and defaults each control how callers may pass arguments. Defaults are evaluated once, at definition time, which is why mutable defaults are a trap.

```python
def connect(host: str, port: int = 443, *, timeout: float = 5.0) -> str:
    """Return a display address."""
    return f"{host}:{port} ({timeout}s)"


connect("example.com", timeout=2.0)
```

Parameters after `*` are keyword-only. A function returns `None` when execution reaches the end without `return`.

```python
def total(*numbers: int) -> int:
    return sum(numbers)


def request(**options: object) -> None:
    print(options)
```

Avoid mutable defaults. Use `None` and create the object inside the function:

```python
def add(value: int, items: list[int] | None = None) -> list[int]:
    items = [] if items is None else items
    items.append(value)
    return items
```
