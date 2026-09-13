# Bash SRE HackerRank 速查

English version: [README.md](README.md)

以下题目使用 [`access.log`](access.log)。它模拟 Nginx combined access log，字段依次包括客户端 IP、身份字段、时间、HTTP 请求、状态码、响应字节数、Referer 和 User-Agent。运行命令时请位于仓库根目录。

## 命令主题

- [`awk`](awk/README_ZH.md)：提取列、筛选行和统计文本。
- [`uniq`](uniq/README_ZH.md)：删除或统计相邻的重复行。

## Q1：找出请求次数最多的 5 个 IP

**题目：** 从访问日志中提取客户端 IP，按请求次数从高到低输出前 5 名。

**Answer：**

```bash
awk '{print $1}' Bash/access.log | sort | uniq -c | sort -nr | head -5
```

**输出：**

```text
   4 10.1.1.1
   2 10.1.1.2
   1 10.1.1.6
   1 10.1.1.5
   1 10.1.1.4
```

管道 `|` 把左边命令的输出交给右边：

- `awk '{print $1}'`：输出每行第一个字段，即 IP。`$1` 表示第一个由空白分隔的字段。
- `sort`：先把相同 IP 排在一起，因为 `uniq` 只处理相邻的重复行。
- `uniq -c`：合并相邻重复行；`-c` 在每行前显示出现次数。
- `sort -nr`：按次数排序。`-n` 表示按数字比较，`-r` 表示倒序。
- `head -5`：只保留前 5 行；也可写成 `head -n 5`。

## Q2：统计每个请求路径的访问次数

**题目：** 输出每个 URL path 的请求次数，并按次数从高到低排序。

**Answer：**

```bash
cut -d'"' -f2 Bash/access.log | cut -d' ' -f2 | sort | uniq -c | sort -nr
```

**输出：**

```text
   5 /api/ads
   3 /api/click
   2 /health
```

- `cut -d'"' -f2`：以双引号作为分隔符，取第 2 段，即 `GET /api/ads HTTP/1.1`。
- `cut -d' ' -f2`：再以空格作为分隔符，取第 2 段，即 URL path。
- `sort | uniq -c | sort -nr`：把相同路径放在一起、计数，再按数字从大到小排序。

最后不使用 `head`，因此输出全部路径。

## Q3：统计不同 IP 的数量

**题目：** 输出访问日志中不同客户端 IP 的总数。

**Answer：**

```bash
awk '{print $1}' Bash/access.log | sort -u | wc -l
```

**输出：**

```text
6
```

- `sort -u`：排序并去重；`-u` 是 `--unique` 的缩写。
- `wc -l`：统计输入行数；`-l` 表示 lines。

这里的行数就是不同 IP 的数量。

## Q4：只显示访问 `/api/ads` 的请求

**题目：** 找出 path 精确等于 `/api/ads` 的所有 Nginx 日志行。

**Answer：**

```bash
grep ' /api/ads HTTP/' Bash/access.log
```

**输出：**

```text
10.1.1.1 - - [04/Sep/2026:10:00:01 +0800] "GET /api/ads HTTP/1.1" 200 512 "-" "curl/8.7.1"
10.1.1.1 - - [04/Sep/2026:10:00:03 +0800] "GET /api/ads HTTP/1.1" 200 498 "-" "curl/8.7.1"
10.1.1.4 - - [04/Sep/2026:10:00:05 +0800] "GET /api/ads HTTP/1.1" 500 64 "-" "Mozilla/5.0"
10.1.1.1 - - [04/Sep/2026:10:00:07 +0800] "GET /api/ads HTTP/1.1" 404 32 "-" "curl/8.7.1"
10.1.1.6 - - [04/Sep/2026:10:00:09 +0800] "GET /api/ads HTTP/1.1" 503 64 "-" "Mozilla/5.0"
```

`grep` 输出包含指定文本的整行。搜索内容同时包含 path 后面的 `HTTP/`，因此不会匹配 `/api/ads-v2`；这个写法比拆分多个 Nginx 字段更容易在面试中直接写出。

## Q5：统计每种 HTTP 方法

**题目：** 输出 GET、POST 等 HTTP 方法各自出现的次数。

**Answer：**

```bash
cut -d'"' -f2 Bash/access.log | cut -d' ' -f1 | sort | uniq -c | sort -nr
```

**输出：**

```text
8 GET
2 POST
```

- 第一个 `cut` 取得引号内的完整 HTTP 请求。
- 第二个 `cut` 取得请求的第 1 段，即 GET 或 POST。
- `sort` 让相同方法相邻，`uniq -c` 负责计数，最后的 `sort -nr` 按次数倒序排列。

## Q6：查看最占内存的 5 个进程

**题目：** 在常见 Linux HackerRank 环境中，显示按内存占用率排序的前 5 个进程。

**Answer：**

```bash
ps aux --sort=-%mem | head -6
```

**输出格式：**

```text
USER  PID  %CPU  %MEM  VSZ  RSS  ...  COMMAND
...
```

- `ps aux`：列出所有用户的进程及详细信息。`a` 包含其他用户的进程，`u` 使用面向用户的列格式，`x` 包含没有终端的进程。
- `--sort=-%mem`：按 `%MEM` 排序；字段前的 `-` 表示降序。
- `head -6`：保留标题行和 5 个进程。

`--sort` 是 GNU/Linux `ps` 选项。macOS 的 BSD `ps` 不支持它，可使用：

```bash
ps aux | head -1 && ps aux | tail -n +2 | sort -k4 -nr | head -5
```

其中 `sort -k4` 从第 4 列 `%MEM` 开始排序；`tail -n +2` 从第 2 行开始输出，用于移除标题。

## 常用参数速查

| 命令 | 参数 | 含义 |
|---|---|---|
| `sort` | `-n` | 按数字而非文本比较 |
| `sort` | `-r` | 倒序排列 |
| `sort` | `-u` | 去除重复行 |
| `sort` | `-k4` | 从第 4 个字段开始排序 |
| `cut` | `-d'"'` | 使用双引号作为字段分隔符 |
| `cut` | `-f2` | 输出第 2 个字段 |
| `uniq` | `-c` | 显示相邻重复行的次数 |
| `head` | `-n 5` | 输出前 5 行 |
| `tail` | `-n 20` | 输出最后 20 行 |
| `tail` | `-f` | 持续等待并显示追加内容 |
| `wc` | `-l` | 统计行数 |
| `grep` | `-i` | 忽略大小写 |
| `grep` | `-v` | 输出不匹配的行 |
| `grep` | `-c` | 输出匹配行数 |

## 面试答题顺序

1. 先确认每一列的含义和分隔符。
2. 说明管道中每个阶段的输入和输出。
3. 用小日志验证计数和排序方向。
4. 提醒面试官 `uniq` 前通常需要 `sort`。
5. 区分 HackerRank 的 Linux 命令与 macOS 的 BSD 命令差异。
