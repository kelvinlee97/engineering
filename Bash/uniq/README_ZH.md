# `uniq` 命令介绍

English version: [README.md](README.md)

`uniq` 不是缩写，没有所谓“全称”；它的名字来自英文单词 **unique**（唯一的）。它把连续出现的相同行合并成一行。

```text
输入               输出
apple              apple
apple    uniq      banana
banana    ───▶     apple
apple
```

最后一个 `apple` 没有与前两个挨在一起，所以仍会保留。实际数据通常没有排好顺序，因此常常先用 `sort` 把相同内容放到一起：

```bash
sort names.txt | uniq
```

## 常见场景

- 删除名单、IP 或日志字段中的重复项。
- 统计每个 IP、用户名或错误信息出现的次数。
- 找出重复出现或只出现一次的内容。

## 常用参数

```bash
sort names.txt | uniq -c  # 显示每行出现次数
sort names.txt | uniq -d  # 只显示重复行
sort names.txt | uniq -u  # 只显示仅出现一次的行
sort names.txt | uniq -i  # 比较时忽略大小写
```

如果只需要排序并去重，可直接使用：

```bash
sort -u names.txt
```

统计 `access.log` 中每个 IP 的请求次数：

```bash
awk '{print $1}' ../access.log | sort | uniq -c | sort -nr
```

## 现场查帮助

在常见 GNU/Linux 环境中先试：

```bash
uniq --help
```

如果不支持 `--help`，使用系统手册：

```bash
man uniq
```

在 `man` 中输入 `/-c` 搜索 `-c`，按 `n` 跳到下一个结果，按 `q` 退出。macOS/BSD 的 `uniq` 不一定支持 `--help`，此时以 `man uniq` 为准。
