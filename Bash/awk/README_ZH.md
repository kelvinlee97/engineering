# `awk` 命令介绍

English version: [README.md](README.md)

`awk` 是处理一行一行文本的工具，名字来自三位作者 Aho、Weinberger 和 Kernighan 的姓氏首字母。它特别适合从日志或表格文本中取出某一列、筛选符合条件的行，以及做简单统计。

## 基本写法

```bash
awk '条件 {动作}' 文件
```

`awk` 默认用空白分列：`$1` 是第一列，`$2` 是第二列，`$0` 是整行，`NF` 是当前行的列数。

```bash
awk '{print $1}' ../access.log       # 输出第一列 IP
awk '$9 >= 500 {print $1, $9}' ../access.log  # 输出发生 5xx 错误的 IP 和状态码
awk '{print $NF}' ../access.log      # 输出最后一列
```

使用其他分隔符时通过 `-F` 指定。例如读取冒号分隔的 `/etc/passwd`：

```bash
awk -F: '{print $1}' /etc/passwd
```

## 怎么判断是第几列

让 `awk` 把第一行的字段编号和值直接打印出来：

```bash
awk 'NR == 1 {for (i = 1; i <= NF; i++) print i, $i}' ../access.log
```

部分输出如下：

```text
1 10.1.1.1
2 -
3 -
4 [04/Sep/2026:10:00:01
5 +0800]
6 "GET
7 /api/ads
8 HTTP/1.1"
9 200
10 512
```

因此，这个文件按空白分列后，常用字段是：

| `awk` 字段 | 内容 |
|---|---|
| `$1` | 客户端 IP |
| `$7` | 请求路径 |
| `$9` | HTTP 状态码 |
| `$10` | 响应字节数 |

双引号不会阻止 `awk` 按空格拆分，所以 `"GET /api/ads HTTP/1.1"` 会成为 `$6`、`$7`、`$8`。真实 User-Agent 可能包含多个空格，后面的字段编号便不固定；处理这类内容时应改用双引号作为分隔符，而不是猜列号。

## 常见场景

- 从访问日志提取 IP、状态码等字段。
- 按字段值筛选记录，例如找出所有 5xx 请求。
- 对数字列求和或计算行数。
- 把某一列交给 `sort`、`uniq` 等命令继续处理。

统计 `access.log` 中每个 IP 的请求次数：

```bash
awk '{print $1}' ../access.log | sort | uniq -c | sort -nr
```

这里 `awk` 只负责取第一列；后面的命令负责排序、计数和排名。

## 现场查帮助

在常见 GNU/Linux 环境中先试：

```bash
awk --help
```

如果不支持 `--help`，使用系统手册：

```bash
man awk
```

在 `man` 中输入 `/pattern` 搜索 `pattern`，按 `n` 跳到下一个结果，按 `q` 退出。HackerRank 等受限环境可能没有 `man`；帮助内容太长时可用 `awk --help 2>&1 | less` 分页阅读。
