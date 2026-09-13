# Python SRE HackerRank 速查

English version: [README.md](README.md)

以下题目使用 [`examples/app.log`](examples/app.log)。它模拟 Nginx combined access log，字段依次包括客户端 IP、身份字段、时间、HTTP 请求、状态码、响应字节数、Referer 和 User-Agent。运行命令时请位于仓库根目录。

## 入门

| 主题 | 速查表 |
|---|---|
| 00. 变量与类型 | [English](beginner/00-variables-and-types/README.md) · [中文](beginner/00-variables-and-types/README_ZH.md) |
| 01. 字符串 | [English](beginner/01-strings/README.md) · [中文](beginner/01-strings/README_ZH.md) |
| 02. 流程控制 | [English](beginner/02-control-flow/README.md) · [中文](beginner/02-control-flow/README_ZH.md) |
| 03. 列表 | [English](beginner/03-lists/README.md) · [中文](beginner/03-lists/README_ZH.md) |
| 04. 循环 | [English](beginner/04-loops/README.md) · [中文](beginner/04-loops/README_ZH.md) |
| 05. 字典 | [English](beginner/05-dictionaries/README.md) · [中文](beginner/05-dictionaries/README_ZH.md) |
| 06. 元组与集合 | [English](beginner/06-tuples-and-sets/README.md) · [中文](beginner/06-tuples-and-sets/README_ZH.md) |
| 07. 函数 | [English](beginner/07-functions/README.md) · [中文](beginner/07-functions/README_ZH.md) |
| 08. 推导式 | [English](beginner/08-comprehensions/README.md) · [中文](beginner/08-comprehensions/README_ZH.md) |
| 09. 异常 | [English](beginner/09-exceptions/README.md) · [中文](beginner/09-exceptions/README_ZH.md) |
| 10. 文件与路径 | [English](beginner/10-files-and-paths/README.md) · [中文](beginner/10-files-and-paths/README_ZH.md) |
| 11. 模块与包 | [English](beginner/11-modules-and-packages/README.md) · [中文](beginner/11-modules-and-packages/README_ZH.md) |
| 12. 测试 | [English](beginner/12-testing/README.md) · [中文](beginner/12-testing/README_ZH.md) |

## 进阶

| 主题 | 速查表 |
|---|---|
| 00. 类 | [English](advanced/00-classes/README.md) · [中文](advanced/00-classes/README_ZH.md) |
| 01. 类型标注 | [English](advanced/01-typing/README.md) · [中文](advanced/01-typing/README_ZH.md) |
| 02. 迭代器与生成器 | [English](advanced/02-iterators-and-generators/README.md) · [中文](advanced/02-iterators-and-generators/README_ZH.md) |
| 03. 上下文管理器 | [English](advanced/03-context-managers/README.md) · [中文](advanced/03-context-managers/README_ZH.md) |
| 04. 装饰器 | [English](advanced/04-decorators/README.md) · [中文](advanced/04-decorators/README_ZH.md) |

## 先看懂一行 Nginx 日志

```text
10.1.1.4 - - [04/Sep/2026:10:00:05 +0800] "GET /api/ads HTTP/1.1" 500 64 "-" "Mozilla/5.0"
```

| 内容 | 含义 |
|---|---|
| `10.1.1.4` | 发出请求的客户端 IP |
| `- -` | 未提供远程用户等身份信息 |
| `[04/Sep/2026:10:00:05 +0800]` | 请求时间及时区 |
| `GET` | HTTP 请求方法 |
| `/api/ads` | 请求路径 |
| `HTTP/1.1` | HTTP 协议版本 |
| `500` | HTTP 响应状态码 |
| `64` | 返回给客户端的字节数 |
| `"-"` | 没有 Referer |
| `"Mozilla/5.0"` | 客户端的 User-Agent |

这些题先用双引号拆出 Nginx 的请求部分，再用空格拆出其中的字段。这比一开始写复杂的正则表达式更容易理解和检查。

## Q1：统计 5xx 请求数量

**题目：** 逐行读取 Nginx 日志，输出 HTTP 状态码为 500–599 的请求数。日志可能很大，不能一次全部读入内存。

**Answer：**

```python
server_errors = 0

with open("Python/examples/app.log", encoding="utf-8") as file:
    for line in file:
        parts = line.split('"')
        if len(parts) >= 3:
            response = parts[2].split()
            if not response:
                continue

            status = int(response[0])
            if 500 <= status <= 599:
                server_errors += 1

print(server_errors)
```

**输出：**

```text
3
```

### 逐步拆解

1. `server_errors = 0` 创建计数器。每发现一条 5xx 日志就加一。
2. `open(..., encoding="utf-8")` 以只读方式打开文件。没有指定 `"w"` 或 `"a"`，所以不会修改日志。
3. `with` 会在代码块结束时自动关闭文件，即使中途发生错误也不需要手动调用 `close()`。
4. `for line in file` 每次只读取一行。对于很大的日志，不应使用 `file.read()` 把全部内容一次放进内存。
5. `line.split('"')` 使用双引号作为“切割位置”。`split()` 会删除分隔符本身，所以结果中不会保留双引号。例如：

   ```python
   '前面"中间"后面'.split('"')
   # ['前面', '中间', '后面']
   ```

   Nginx 日志可以先这样观察：

   ```text
   IP和时间 | " | HTTP请求 | " | 状态码和字节数 | " | Referer | " | 空格 | " | User-Agent | "
   ```

   每个 `| " |` 都是一次切割位置。对示例日志执行后，主要结果是：

   ```python
   parts[0]  # '10.1.1.4 - - [04/Sep/2026:10:00:05 +0800] '
   parts[1]  # 'GET /api/ads HTTP/1.1'
   parts[2]  # ' 500 64 '
   parts[3]  # '-'
   parts[4]  # ' '
   parts[5]  # 'Mozilla/5.0'
   ```

   原始日志的状态码部分本来就在 HTTP 请求的结束双引号和 Referer 的开始双引号之间，因此它成为 `parts[2]`。变量名 `parts` 只是我们为切割结果取的名字，与日志中有没有这个单词或双引号无关。

6. `len(parts) >= 3` 确认行中存在状态码所在部分，避免直接访问不存在的 `parts[2]`。
7. `parts[2].split()` 再按空白拆分，得到 `['500', '64']`。
8. `if not response` 检查列表是否为空。空列表没有 `response[0]`，所以使用 `continue` 跳到下一行日志，避免 `IndexError`。
9. `status = int(response[0])` 先把字符串 `'500'` 转换成整数并保存。单独命名后，下一行更容易阅读和解释。
10. `500 <= status <= 599` 表示状态码位于 500 到 599 之间，也就是所有 5xx 状态码。
11. 条件成立时执行 `server_errors += 1`。

程序只扫描一次日志，所以时间复杂度是 `O(n)`；它只保留当前行和一个计数器，额外空间是 `O(1)`。

## Q2：统计每种 HTTP 状态码

**题目：** 统计每种 HTTP 状态码，并按出现次数从高到低输出。

**Answer：**

```python
statuses = {}

with open("Python/examples/app.log", encoding="utf-8") as file:
    for line in file:
        parts = line.split('"')
        if len(parts) >= 3:
            response = parts[2].split()
            if response:
                status = response[0]
                statuses[status] = statuses.get(status, 0) + 1

for status in sorted(statuses, key=lambda key: statuses[key], reverse=True):
    print(status, statuses[status])
```

**输出：**

```text
200 4
201 2
500 1
502 1
404 1
503 1
```

### 逐步拆解

1. `statuses = {}` 创建空字典。字典最终会是下面的形式：

   ```python
   {"200": 4, "201": 2, "500": 1}
   ```

2. 读取和拆分日志的方式与 Q1 相同。
3. `status = response[0]` 取得状态码。这里不需要计算数值范围，因此保留为字符串即可。
4. 计数的核心是：

   ```python
   statuses[status] = statuses.get(status, 0) + 1
   ```

   如果 `status` 第一次出现，`get(status, 0)` 返回默认值 `0`，加一后保存为 `1`。如果已有 `"200": 3`，它就读取 `3`，加一后更新为 `4`。

5. `sorted(statuses, ...)` 对字典的键，也就是各状态码进行排序。
6. `key=lambda key: statuses[key]` 告诉 `sorted()`：比较状态码时，要看它对应的次数。
7. `reverse=True` 表示次数从大到小排列。
8. 最后的循环逐个打印状态码以及 `statuses[status]` 中保存的次数。

扫描 `n` 行需要 `O(n)` 时间。若有 `k` 种状态码，排序需要 `O(k log k)` 时间，字典需要 `O(k)` 空间。

## Q3：找出访问次数最多的 N 个路径

**题目：** 实现 `top_paths(path, n)`，返回访问次数最多的 `n` 个 URL path 及其次数。

**Answer：**

```python
def top_paths(path: str, n: int) -> list[tuple[str, int]]:
    paths = {}

    with open(path, encoding="utf-8") as file:
        for line in file:
            parts = line.split('"')
            if len(parts) >= 2:
                request = parts[1].split()
                if len(request) == 3:
                    url_path = request[1]
                    paths[url_path] = paths.get(url_path, 0) + 1

    ranked = sorted(paths.items(), key=lambda item: item[1], reverse=True)
    return ranked[:n]


print(top_paths("Python/examples/app.log", 2))
```

**输出：**

```text
[('/api/ads', 5), ('/api/click', 3)]
```

### 逐步拆解

1. `def top_paths(path, n)` 定义函数。`path` 是日志文件路径，`n` 是需要返回的结果数量。
2. `paths = {}` 保存每个 URL path 及其出现次数。
3. `parts = line.split('"')` 后，`parts[1]` 是：

   ```text
   GET /api/ads HTTP/1.1
   ```

4. `request = parts[1].split()` 把它拆成：

   ```python
   ["GET", "/api/ads", "HTTP/1.1"]
   ```

5. `len(request) == 3` 检查请求中确实有方法、路径和协议三个部分。
6. `request[1]` 取得路径 `/api/ads`。列表索引从 `0` 开始，所以索引 `1` 是第二项。
7. `paths.get(url_path, 0) + 1` 使用与 Q2 相同的方法累计次数。
8. `paths.items()` 把字典变成 `(路径, 次数)` 形式的数据，例如：

   ```python
   [("/api/ads", 5), ("/api/click", 3), ("/health", 2)]
   ```

9. `key=lambda item: item[1]` 使用每一项的第二个值，也就是次数排序。
10. `ranked[:n]` 是列表切片。当 `n` 为 `2` 时，只返回前两项。

若日志有 `m` 行、不同路径有 `k` 个，扫描是 `O(m)`，排序是 `O(k log k)`，字典需要 `O(k)` 空间。

## Q4：找出重复的请求 ID

**题目：** 输入请求 ID 列表，按首次重复出现的顺序返回重复 ID，每个 ID 只返回一次。

**Answer：**

```python
def find_duplicates(request_ids: list[str]) -> list[str]:
    seen = set()
    duplicates = set()
    result = []

    for request_id in request_ids:
        if request_id in seen and request_id not in duplicates:
            duplicates.add(request_id)
            result.append(request_id)
        seen.add(request_id)

    return result


print(find_duplicates(["a1", "a2", "a3", "a1", "a4", "a2", "a1"]))
```

**输出：**

```text
['a1', 'a2']
```

### 逐步拆解

三个变量有不同职责：

- `seen`：记录至少出现过一次的 ID。
- `duplicates`：记录已经确认为重复、并已加入答案的 ID。
- `result`：保存最终答案，并维持发现重复项的顺序。

以 `a1` 为例：

1. 第一次遇到 `a1` 时，它不在 `seen`，所以不加入答案；随后把它加入 `seen`。
2. 第二次遇到 `a1` 时，它已经在 `seen`，但不在 `duplicates`，所以把它加入 `duplicates` 和 `result`。
3. 第三次遇到 `a1` 时，它同时存在于两个集合，因此不会重复加入 `result`。

`request_id in seen` 用于判断是否出现过，`request_id not in duplicates` 用于保证答案不重复。集合的查找和插入平均为 `O(1)`，所以整体平均时间是 `O(n)`，空间是 `O(n)`。

## Q5：Two Sum

**题目：** 返回两个元素的索引，使它们的和等于目标值；不存在时返回空列表。

**Answer：**

```python
def two_sum(numbers: list[int], target: int) -> list[int]:
    seen = {}

    for index, number in enumerate(numbers):
        required = target - number
        if required in seen:
            return [seen[required], index]
        seen[number] = index

    return []


print(two_sum([2, 7, 11, 15], 9))
```

**输出：**

```text
[0, 1]
```

### 逐步拆解

目标是找两个数相加等于 `9`。当当前数字是 `7` 时，需要寻找的另一个数字就是 `9 - 7 = 2`。

1. `seen = {}` 保存已经看过的数字及其索引，格式为 `{数字: 索引}`。
2. `enumerate(numbers)` 同时提供索引和值。第一次循环得到 `index = 0`、`number = 2`。
3. `required = target - number` 计算当前数字需要的配对数字。
4. 必须先检查 `required in seen`，再保存当前数字。这样同一个元素不会与自己配对。
5. 第一次循环需要 `7`，但字典为空，于是保存 `seen[2] = 0`。
6. 第二次循环当前数字是 `7`，需要的数字是 `2`。字典中已经有 `2: 0`，因此返回已有数字的索引 `0` 和当前索引 `1`。
7. 如果循环结束仍未找到，就返回空列表 `[]`。

字典查询平均为 `O(1)`。整个列表只遍历一次，所以平均时间是 `O(n)`，最多保存 `n` 个数字，因此空间是 `O(n)`。

## Q6：固定窗口内的最大请求数

**题目：** 给定每分钟请求数，找出连续 `size` 分钟内的最大总请求数。

**Answer：**

```python
def max_window_sum(requests: list[int], size: int) -> int:
    if size <= 0 or size > len(requests):
        raise ValueError("size must be between 1 and len(requests)")

    current = sum(requests[:size])
    maximum = current

    for index in range(size, len(requests)):
        current += requests[index] - requests[index - size]
        maximum = max(maximum, current)

    return maximum


print(max_window_sum([10, 20, 30, 10, 50], 3))
```

**输出：**

```text
90
```

### 逐步拆解

输入是 `[10, 20, 30, 10, 50]`，窗口大小是 `3`：

```text
[10, 20, 30]             总和 60
     [20, 30, 10]         总和 60
          [30, 10, 50]    总和 90
```

1. 首先检查 `size`。窗口不能小于 `1`，也不能比列表长度更大；无效时抛出 `ValueError`。
2. `requests[:size]` 取出第一个窗口 `[10, 20, 30]`。
3. `current = sum(...)` 得到第一个窗口总和 `60`。
4. `maximum = current` 把当前总和设为目前最大值。
5. 循环从索引 `size`，也就是索引 `3` 开始。此时新进入窗口的是 `requests[3] = 10`。
6. `requests[index - size]` 是离开窗口的旧值。第一次移动时，它是 `requests[0] = 10`。
7. `current += 新值 - 旧值`，因此不用对整个窗口重新调用 `sum()`。
8. `maximum = max(maximum, current)` 保留目前见过的最大总和。
9. 最后一个窗口加入 `50`、移除 `20`，总和从 `60` 变成 `90`，所以返回 `90`。

每个元素最多被加入和移除一次，时间复杂度是 `O(n)`。算法只保存当前总和和最大值，额外空间是 `O(1)`。

## 面试答题顺序

1. 确认输入、输出和异常输入。
2. 用一个小例子说明算法。
3. 写出最小可运行解法。
4. 测试空输入、重复值、无结果和边界值。
5. 说明时间与空间复杂度。
