# Python 变量与类型速查表

English version: [README.md](README.md)

```python
name = "api"
port = 8080
ratio = 0.75
enabled = True
result = None

type(port)             # <class 'int'>
isinstance(port, int)  # True
int("42")              # 42
str(42)                # "42"
```

变量名指向对象；给可变对象赋予另一个名称不会复制对象。

```python
first = [1, 2]
second = first
second.append(3)  # first 也变成 [1, 2, 3]
```

使用 `==` 比较值，使用 `is` 判断是否为同一个对象，尤其是 `value is None`。`int`、`float`、`bool`、`str`、`tuple` 和 `frozenset` 是常见不可变类型；`list`、`dict` 和 `set` 是常见可变类型。
