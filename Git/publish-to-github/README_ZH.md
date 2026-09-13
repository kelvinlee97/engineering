# 正确地把改动发布到 GitHub：初学者指南

English version: [README.md](README.md)

安全发布代码不是一条命令，而是一条完整流程：

```text
修改 -> 检查 -> 测试 -> commit -> 推送分支 -> 创建 Pull Request -> 合并
```

Git 在本机记录改动；GitHub 托管远端仓库，并提供 Pull Request、评审和自动检查。
commit 之后代码仍在本地；推送分支也不会改变 `main`，只有合并后才会进入目标分支。

## 开始前的准备

你需要安装 Git、注册 GitHub 账号，并在本地 clone 仓库。先配置以后写入 commit 的姓名和邮箱：

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

如果使用 [GitHub CLI](https://cli.github.com/)，对多数初学者来说，浏览器登录是最简单的认证方式：

```bash
gh auth login
gh auth status
```

密码、访问令牌、私钥、`.env` 文件、客户私密数据绝不能进入 commit。敏感信息一旦被推送，
事后把仓库改成 private 也不代表安全；必须撤销或轮换该凭据。

## 日常发布流程

下面假设基础分支叫 `main`，远端叫 `origin`。仓库可能使用其他名称，因此不要凭感觉操作，
先确认实际状态：

```bash
git status
git remote -v
git branch --show-current
```

### 1. 从最新的基础分支开始

先提交或 stash 当前工作，再更新 `main`，并避免意外产生 merge commit：

```bash
git switch main
git pull --ff-only
```

如果 `--ff-only` 失败，先停下来检查历史。不要为了消除提示就在共享分支上强推或 reset。

### 2. 创建一个目标明确的分支

```bash
git switch -c docs/explain-squash-merge
```

分支名要简短并能说明改动，例如 `fix/login-timeout` 或 `docs/install-guide`。一个分支和
一个 Pull Request 尽量只处理一个目标。

### 3. 完成改动并运行相关检查

先阅读仓库的 `README`、`CONTRIBUTING.md` 或 `AGENTS.md`。运行能覆盖本次改动的最小范围
测试、格式检查、构建或文档检查，然后查看结果：

```bash
git status
git diff
```

`git status` 显示哪些文件发生变化；`git diff` 显示尚未暂存的具体修改。继续前检查是否
混入调试输出、生成文件、敏感信息或无关修改。

### 4. 只暂存准备提交的文件

```bash
git add path/to/file another/file
git diff --staged
```

暂存区决定下一次 commit 的准确内容。对初学者而言，显式写出文件路径比 `git add .` 更安全，
因为后者可能带入无关文件。如果暂存错了，下面的命令会取消暂存，但保留文件修改：

```bash
git restore --staged path/to/file
```

### 5. 创建清楚的 commit

```bash
git commit -m "docs: explain the GitHub publishing workflow"
git show --stat HEAD
```

好的消息应说明这次 commit 完成了什么。遵循仓库已有的消息风格；只有项目使用
Conventional Commits 时，才需要添加 `feat:` 等前缀。

一个 Pull Request 可以有多个有意义的 commit。如果仓库使用 squash merge，这些 commit
不必为了追求完美而反复改写，因为 GitHub 可以在合并时把它们压缩成一个。

### 6. 推送分支

确认目的地后，再发布当前分支：

```bash
git remote -v
git push --set-upstream origin HEAD
```

`--set-upstream` 会关联本地与远端分支。之后通常只需运行 `git push`。分支推送完成，仍不代表
它已经合并到 `main`。

### 7. 创建 Pull Request

在 GitHub 仓库页面选择 **Compare & pull request**，或使用 GitHub CLI：

```bash
gh pr create --web
```

提交前确认：

- **Base** 是准备修改的目标分支，通常为 `main`。
- **Compare/head** 是你的功能分支。
- 标题说明改动结果。
- 描述写清楚改了什么、为什么改、如何检查。
- `Files changed` 没有无关内容或敏感信息。

简短的描述已经足够：

```markdown
## Summary

- 为初学者解释从分支到 PR 的发布流程。
- 添加 commit 和 push 前的安全检查。

## Checks

- 已检查 Markdown 链接和格式。
```

工作尚未完成时，可以创建 Draft Pull Request。继续向同一个分支推送的新 commit 会自动加入
已有的 Pull Request，不需要重新创建。

### 8. 处理评审意见和自动检查

在本地修改、检查、提交，然后再次推送：

```bash
git status
git diff
# 修改并运行相关检查
git add path/to/file
git diff --staged
git commit -m "docs: clarify branch selection"
git push
```

不要为每次修改新建 Pull Request。关注 GitHub 的 **Checks** 标签页，合并前修复失败的检查。
只有问题真正处理后，才标记评审对话为 resolved。

### 9. 合并并清理分支

所需评审和检查通过后才能合并。如果仓库提供 **Squash and merge**，GitHub 会把 PR 中的所有
commit 合并成目标分支上的一个 commit。功能分支包含多次小修正、而项目希望保持 `main` 历史
简洁时，这种方式很合适。应遵循仓库规定的合并方式；并非所有项目都启用 squash。

Pull Request 合并后：

```bash
git switch main
git pull --ff-only
git fetch --prune
```

如果仓库没有自动删除远端分支，可使用 GitHub 的 **Delete branch** 按钮。普通 merge 后，可用
`git branch -d docs/explain-squash-merge` 删除本地分支。squash merge 后，Git 通常无法从提交历史
确认原始 commit 已合并；确认 PR 已合并、分支已推送且工作区干净后，才使用
`git branch -D docs/explain-squash-merge`。

## 没有仓库推送权限时

开源项目通常使用 fork-and-pull 模式：

1. 在 GitHub 上 fork 项目。
2. clone 自己的 fork。
3. 把原始仓库添加为 `upstream`。
4. 把功能分支推送到自己的 fork（`origin`）。
5. 从 fork 向原始仓库创建 Pull Request。

```bash
git clone https://github.com/YOUR-USER/PROJECT.git
cd PROJECT
git remote add upstream https://github.com/OWNER/PROJECT.git
git fetch upstream
git switch -c docs/example upstream/main
# 修改、检查、暂存并提交
git push -u origin HEAD
gh pr create --web
```

这里的 `origin` 是你的 fork，`upstream` 是原始项目。大幅修改前一定先阅读项目的贡献指南。

## 可选：用 worktree 并行处理任务

`git worktree` 可以让另一个分支拥有独立目录，同时共享同一个仓库历史。当你需要保留当前未完成
工作，又要另外处理修复或 Pull Request 时，它很实用；普通 GitHub 发布流程不要求使用它。

在主仓库目录中运行：

```bash
git fetch origin
git worktree add -b fix/login-timeout ../project-login-timeout origin/main
cd ../project-login-timeout
# 像平常一样修改、检查、暂存、提交、推送并创建 PR
git push -u origin HEAD
gh pr create --web
```

Pull Request 合并后，先离开 worktree 目录，再通过 Git 清理：

```bash
cd ../project
git worktree remove ../project-login-timeout
git fetch --prune
```

worktree 中还有未提交内容时，不要直接删除目录；先在该目录运行 `git status`。同一个分支同一时间
只能在一个 worktree 中被检出。之后用 `git branch -d fix/login-timeout` 删除分支；只有确认完成
上述 squash merge 检查后才使用 `-D`。

## 可选：理解流程后再自动化

Anthropic 公开的 Claude Code 仓库提供带 `/commit-push-pr` 的 `commit-commands` 插件。该流程会
检查改动、在需要时创建分支、commit、推送到 `origin`，并通过 `gh pr create` 创建 Pull Request。

它只是方便的流程封装，不能代替人工检查。接受自动 commit 或 push 前，应核对分支、远端、diff、
commit 消息、测试结果和 PR 的 base。工具是否可用以及具体行为可能随版本变化，因此请查看插件
当前的 README，不要假设命令一定已经安装。

## 初学者常见错误

| 错误 | 更好的习惯 |
|---|---|
| 直接在 `main` 上修改 | 创建短期功能分支。 |
| 不检查就运行 `git add .` | 暂存明确路径，再运行 `git diff --staged`。 |
| 把 commit 和 push 当成同一步 | 记住：commit 保存在本地，push 才发布分支。 |
| 推送秘密后再删除 | 从一开始就不让秘密进入 Git；暴露后立即轮换凭据。 |
| push 被拒绝就强推 | 先 fetch 并弄清楚分支为什么分叉。 |
| 创建 PR 时选错 base | 提交前检查 base 和 compare 分支。 |
| 检查失败仍然合并 | 修复失败，或记录经过批准的例外。 |
| 不检查 AI 生成的 PR 描述 | 用实际 diff 和检查结果逐项验证。 |

## 快速检查清单

```text
[ ] 当前是目标明确的功能分支，而不是 main。
[ ] git status 和 git diff 只显示预期改动。
[ ] 相关检查已经通过。
[ ] git diff --staged 与 commit 消息一致。
[ ] push 前已经确认远端和分支。
[ ] PR 指向正确的 base，并说明改动和检查方法。
[ ] 合并前所需评审和 CI 已通过。
[ ] 合并后已更新 main，并删除本地功能分支。
```

## 官方参考

- GitHub Docs：[关于 Pull Request](https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- GitHub Docs：[将 commit 推送到远程仓库](https://docs.github.com/zh/get-started/using-git/pushing-commits-to-a-remote-repository)
- GitHub Docs：[创建 Pull Request](https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
- GitHub Docs：[合并 Pull Request](https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request)
- GitHub Docs：[关于 Pull Request 合并](https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges)
- GitHub CLI：[`gh auth login`](https://cli.github.com/manual/gh_auth_login) 与 [`gh pr create`](https://cli.github.com/manual/gh_pr_create)
- Git：[`git worktree`](https://git-scm.com/docs/git-worktree)
- Anthropic：[Claude Code commit commands](https://github.com/anthropics/claude-code/tree/main/plugins/commit-commands)
