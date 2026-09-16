← [返回目录](../basics/README_ZH.md) ｜ 上一站：[Git/commit](../commit/README_ZH.md)

English version: [README.md](README.md)

# `git log` —— 查看提交历史

## 这一步在做什么

`git log` 显示当前分支的提交历史，从最新的提交往回追溯到最早的提交，是"时间机器的目录索引"。每条记录包含：提交哈希、作者、时间、提交信息。

```mermaid
flowchart RL
    accTitle: 提交历史链，最新提交在前
    accDescr: 从最早的 c1 提交开始，c2 指向 c1，最新的 c3 指向 c2，HEAD 和 main 分支都指向 c3；git log 默认按从新到旧的顺序打印这条链。
    C3["提交 c3 (HEAD → main)<br/>fix: 修复登录bug"] --> C2["提交 c2<br/>feat: 添加登录页"]
    C2 --> C1["提交 c1<br/>init: 项目初始化"]

    style C3 fill:#22a06b,color:#fff
```

`git log` 的默认输出就是把这条链**从右往左**（从新到旧）打印出来。

## 常用操作

```bash
# 默认详细模式
git log

# 每条提交压缩成一行，最常用的日常查看方式
git log --oneline

# 图形化展示分支合并关系（团队协作时非常有用）
git log --oneline --graph --all

# 只看最近 5 条
git log -5

# 只看某个作者的提交
git log --author="张三"

# 只看某个文件的修改历史
git log --follow -- src/app.js

# 搜索提交信息里包含关键词的记录
git log --grep="fix"

# 显示每次提交具体改了哪些内容（结合了 diff）
git log -p
```

## 参数说明

| 参数 | 作用 |
|---|---|
| `--oneline` | 每条提交精简为一行：`哈希前缀 + 提交信息` |
| `--graph` | 用 ASCII 图形画出分支和合并的走向 |
| `--all` | 显示所有分支的提交，不止当前分支 |
| `-p` / `--patch` | 附带显示每次提交的具体代码差异 |
| `--stat` | 显示每次提交改了哪些文件、加减了多少行（比 `-p` 更简洁） |

## 实用组合（建议加进你的 alias）

```bash
git config --global alias.lg "log --oneline --graph --all --decorate"
# 之后直接输入
git lg
```

## 验证你理解对了

```bash
git log --oneline
# 每一行最前面的 7 位字符（如 a1b2c3d）就是提交哈希
# 可以用它定位到具体某次提交，例如 git show a1b2c3d
```

## 常见坑

- ⚠️ 默认 `git log` 输出很长，按 `q` 退出分页器（Git 默认用 `less` 分页）。
- ⚠️ `--follow` 只能跟踪单个文件的重命名历史，多个文件要分别执行。

## 承上启下

`git log` 告诉你**历史上发生过什么**，但如果你想知道**现在**和**某次提交之间**、或者**两次提交之间**具体差了哪些代码行，就需要最后一节——**`git diff`**。

👉 下一站：[Git/diff —— 对比具体差异](../diff/README_ZH.md)

---
参考：[Pro Git 2.3 - 查看提交历史](https://git-scm.com/book/zh/v2/Git-基础-查看提交历史) ｜ [git-log 官方手册](https://git-scm.com/docs/git-log)
