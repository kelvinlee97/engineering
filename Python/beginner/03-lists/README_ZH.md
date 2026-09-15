# Python 列表速查表

English version: [README.md](README.md)

## 心智模型

> 列表是有序、可变、可伸缩的引用序列。返回新结果的方法（`sorted`、`copy`）会创建新列表；就地修改的方法（`sort`、`append`、`remove`）会直接改动原列表并返回 `None`。

## 创建和访问

```python
numbers = [10, 20, 30]
empty = []

numbers[0]   # 10
numbers[-1]  # 30
numbers[1:]  # [20, 30]
numbers[::-1]  # [30, 20, 10]
```

索引超出列表范围会抛出 `IndexError`；切片则会安全地停在列表边界。

## 添加、修改和删除

```python
numbers.append(40)       # 添加一个元素
numbers.extend([50, 60]) # 添加多个元素
numbers.insert(1, 15)    # 插入到索引 1 之前
numbers[0] = 5

last = numbers.pop()     # 删除并返回最后一个元素
numbers.remove(20)       # 删除第一个匹配值
del numbers[0]           # 按索引删除
```

值不存在时，`remove()` 会抛出 `ValueError`。如果值可以不存在，应先检查 `value in numbers`。

## 查找和汇总

```python
20 in numbers
numbers.index(20)
numbers.count(20)

len(numbers)
sum(numbers)
min(numbers)
max(numbers)
```

## 排序和复制

```python
ascending = sorted(numbers)       # 返回新列表
descending = sorted(numbers, reverse=True)

numbers.sort()                    # 修改原列表
copy = numbers.copy()             # 浅复制
```

需要保留原顺序时使用 `sorted()`。浅复制不会复制列表中的嵌套对象。

## 列表推导式

```python
squares = [number * number for number in numbers]
even = [number for number in numbers if number % 2 == 0]
```

需要多个条件或副作用时，应改用普通循环。

## 常见错误

```python
# 两行指向同一个内部列表。
grid = [[0] * 3] * 2

# 每一行互相独立。
grid = [[0] * 3 for _ in range(2)]
```
