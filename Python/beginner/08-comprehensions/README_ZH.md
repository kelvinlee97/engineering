# Python 推导式速查表

English version: [README.md](README.md)

## 心智模型

> 推导式是把循环改写成表达式：`[表达式 for 元素 in 可迭代对象 if 条件]` 从左到右读作「当条件成立时，为每个元素生成这个结果」。外层括号（`[]`、`{}`、`()`）决定最终容器的类型。

```python
squares = [number**2 for number in range(5)]
even = {number for number in range(10) if number % 2 == 0}
lengths = {name: len(name) for name in services}
total = sum(number**2 for number in range(5))
```

先写结果表达式，再写循环和可选的过滤条件。

```python
flattened = [item for row in matrix for item in row]
```

嵌套推导式中的 `for` 顺序与普通嵌套循环相同。嵌套或条件导致表达式难以阅读时，应改用普通循环。圆括号创建惰性生成器表达式，方括号会立即创建完整列表。
