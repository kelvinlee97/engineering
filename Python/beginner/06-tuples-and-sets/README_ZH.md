# Python 元组与集合速查表

English version: [README.md](README.md)

## 心智模型

> 元组是不可变的有序记录，集合是可变的无序去重容器。根据数据需要的是「顺序与不可变」还是「唯一性」来选择。

## 元组

```python
point = (10, 20)
x, y = point
single = (10,)
host, port = "localhost", 8080
```

元组不可变，适合固定记录或返回多个值。只有一个元素的元组必须保留末尾逗号。

## 集合

```python
left = {"api", "web"}
right = {"web", "worker"}

left | right  # 并集
left & right  # 交集
left - right  # 差集
left ^ right  # 对称差集

left.add("cron")
left.discard("missing")  # 不存在也不会报错
```

集合保存唯一且可哈希的值，不支持索引。空集合要写成 `set()`，因为 `{}` 创建的是字典。
