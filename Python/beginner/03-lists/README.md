# Python Lists Cheatsheet

> A list is an ordered, mutable, resizable sequence of references. Methods that end in a return value (`sorted`, `copy`) build a new list; methods that mutate (`sort`, `append`, `remove`) change the original in place and return `None`.

## Create and access

```python
numbers = [10, 20, 30]
empty = []

numbers[0]   # 10
numbers[-1]  # 30
numbers[1:]  # [20, 30]
numbers[::-1]  # [30, 20, 10]
```

Indexes outside the list raise `IndexError`. Slices safely stop at the list boundary.

## Add, update, and remove

```python
numbers.append(40)       # add one item
numbers.extend([50, 60]) # add many items
numbers.insert(1, 15)    # insert before index 1
numbers[0] = 5

last = numbers.pop()     # remove and return the last item
numbers.remove(20)       # remove the first matching value
del numbers[0]           # remove by index
```

`remove()` raises `ValueError` when the value is absent. Check `value in numbers` first when absence is valid.

## Search and summarize

```python
20 in numbers
numbers.index(20)
numbers.count(20)

len(numbers)
sum(numbers)
min(numbers)
max(numbers)
```

## Sort and copy

```python
ascending = sorted(numbers)       # new list
descending = sorted(numbers, reverse=True)

numbers.sort()                    # changes the original list
copy = numbers.copy()             # shallow copy
```

Use `sorted()` when the original order must remain unchanged. A shallow copy does not copy nested objects.

## List comprehensions

```python
squares = [number * number for number in numbers]
even = [number for number in numbers if number % 2 == 0]
```

Use a normal loop when the comprehension needs multiple conditions or side effects.

## Common pitfall

```python
# Both rows refer to the same inner list.
grid = [[0] * 3] * 2

# Each row is independent.
grid = [[0] * 3 for _ in range(2)]
```
