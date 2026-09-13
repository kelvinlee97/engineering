# Python Variables and Types Cheatsheet

Chinese version: [README_ZH.md](README_ZH.md)

```python
name = "api"
port = 8080
ratio = 0.75
enabled = True
result = None

type(port)          # <class 'int'>
isinstance(port, int)  # True
int("42")           # 42
str(42)             # "42"
```

Names point to objects; assignment does not copy mutable objects.

```python
first = [1, 2]
second = first
second.append(3)  # first is now [1, 2, 3]
```

Use `==` for equal values and `is` for identity, especially `value is None`. Immutable basics include `int`, `float`, `bool`, `str`, `tuple`, and `frozenset`; mutable basics include `list`, `dict`, and `set`.
