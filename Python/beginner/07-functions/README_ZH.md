# Python 函数速查表

English version: [README.md](README.md)

```python
def connect(host: str, port: int = 443, *, timeout: float = 5.0) -> str:
    """返回用于显示的地址。"""
    return f"{host}:{port} ({timeout}s)"


connect("example.com", timeout=2.0)
```

`*` 后面的参数只能按名称传入。函数执行到末尾而没有遇到 `return` 时会返回 `None`。

```python
def total(*numbers: int) -> int:
    return sum(numbers)


def request(**options: object) -> None:
    print(options)
```

避免使用可变默认值。默认值应设为 `None`，再在函数内创建对象：

```python
def add(value: int, items: list[int] | None = None) -> list[int]:
    items = [] if items is None else items
    items.append(value)
    return items
```
