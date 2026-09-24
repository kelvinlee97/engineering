# Python Comprehensions Cheatsheet

> A comprehension is a loop rewritten as an expression: `[expression for item in iterable if condition]` reads left to right as "produce this, for each item, when this holds." The enclosing bracket (`[]`, `{}`, `()`) picks the resulting container.

```python
squares = [number**2 for number in range(5)]
even = {number for number in range(10) if number % 2 == 0}
lengths = {name: len(name) for name in services}
total = sum(number**2 for number in range(5))
```

The expression comes first, followed by the loop and optional filter.

```python
flattened = [item for row in matrix for item in row]
```

Nested comprehensions follow the same order as nested `for` loops. Prefer an ordinary loop when nesting or conditions make the expression hard to scan. Parentheses create a lazy generator expression; brackets create the complete list immediately.
