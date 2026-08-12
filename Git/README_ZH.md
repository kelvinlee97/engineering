# Git 运维常用命令指南

English version: [README.md](README.md)

面向已有终端和基础 Git 使用经验的运维工程师。本文的原则很简单：**先观察，再操作；共享分支优先追加可审计的修复，不改写历史。**

本文只讲 Git 原生命令。GitHub、GitLab、Bitbucket 等平台的按钮、保护规则和 CI 配置是平台能力，不能与 Git 本身混为一谈。

## 目录

- [先记住这张关系图](#先记住这张关系图)
- [每次操作前：先看事实](#每次操作前先看事实)
- [本地修改与提交](#本地修改与提交)
- [分支、同步与冲突](#分支同步与冲突)
- [发布、tag 与变更追溯](#发布tag-与变更追溯)
- [回滚、恢复与排障](#回滚恢复与排障)
- [高风险操作与安全边界](#高风险操作与安全边界)
- [每日最小命令集](#每日最小命令集)
- [高风险操作前检查清单](#高风险操作前检查清单)

## 先记住这张关系图

```text
工作区 (working tree) --git add--> 暂存区 (index) --git commit--> 本地仓库
       ^                                                               |
       |---------------------- git restore / reset --------------------|
                                                                       |
远端仓库 <----------------------------- git push ----------------------+
    |
    +------------------------------ git fetch ------------------> 远端跟踪分支
```

- **工作区**：你当前看到和编辑的文件。
- **暂存区**：下一次提交准备包含的文件内容。
- **本地仓库**：当前机器保存的提交历史；`HEAD` 通常指向当前分支的最新提交。
- **远端仓库**：如 `origin`；`origin/main` 是本地记录的远端分支状态，先 `fetch` 才会更新。
- **分支分叉（diverged）**：本地和远端从同一提交各自继续产生了提交。此时 Git 无法猜测你要 merge 还是 rebase，必须明确选择整合策略。

## 每次操作前：先看事实

以下命令只读取信息（`fetch` 会更新本地的远端跟踪引用，但不会合并工作区或推送远端）。先运行它们，再决定下一步。

| 目的 | 命令 | 说明 |
|---|---|---|
| 看工作区、暂存区、上下游关系 | `git status` | 最先运行；确认当前分支、未提交文件、领先/落后状态。 |
| 用适合脚本的简短格式看状态 | `git status --short --branch` | `--porcelain` 格式才适合自动化解析。 |
| 看所有分支与提交图 | `git log --oneline --graph --decorate --all` | 排查 merge、tag、分叉时最有用。 |
| 看未暂存差异 | `git diff` | 比较工作区与暂存区。 |
| 看已暂存差异 | `git diff --staged` | **提交前必看**。 |
| 看某次提交 | `git show <commit>` | 回滚、审查或排障前核对实际修改。 |
| 看本地分支及其上游 | `git branch -vv` | 确认每个分支跟踪哪个远端分支。 |
| 看远端 URL | `git remote -v` | 推送前确认目标，避免推错仓库。 |
| 获取远端状态并清理已删远端分支 | `git fetch --prune` | 安全同步的起点；不等于 `pull`。 |

官方参考：[git-status](https://git-scm.com/docs/git-status)、[git-diff](https://git-scm.com/docs/git-diff)、[git-log](https://git-scm.com/docs/git-log)、[git-fetch](https://git-scm.com/docs/git-fetch)。

## 本地修改与提交

### 安全提交闭环

```bash
git diff
git add path/to/file
git diff --staged
git commit -m "feat: explain the change"
git show --stat HEAD
```

1. 先用 `git diff` 确认你实际改了什么。
2. 用精确路径 `git add path/to/file` 暂存，避免不小心把无关文件加入提交。
3. 用 `git diff --staged` 确认“将要提交”的内容。
4. `git commit` 创建本地历史；它还没有发送到远端。
5. `git show --stat HEAD` 确认新提交内容和范围。

### 撤销、修正与临时搁置

| 需求 | 命令 | 影响与注意事项 |
|---|---|---|
| 丢弃某个未暂存文件的修改 | `git restore path/to/file` | 会覆盖工作区该文件；先 `git diff -- path/to/file`。 |
| 把文件从暂存区移回工作区 | `git restore --staged path/to/file` | 不会丢弃工作区修改。 |
| 修改最后一次**未共享**提交 | `git commit --amend` | 改写提交 ID；已推送/共享后不要随意使用。 |
| 临时保存已跟踪文件的修改 | `git stash push -m "reason"` | 不包含未跟踪或已忽略文件。用 `git stash list` 查看；`stash pop` 会应用并删除该条目，可能冲突。 |
| 同时保存已检查的未跟踪文件 | `git stash push --include-untracked -m "reason"` | 包含未跟踪文件，但不包含已忽略文件。 |
| 恢复某条搁置但保留记录 | `git stash apply stash@{0}` | 先检查目标分支是否兼容。 |

官方参考：[git-add](https://git-scm.com/docs/git-add)、[git-restore](https://git-scm.com/docs/git-restore)、[git-commit](https://git-scm.com/docs/git-commit)、[git-stash](https://git-scm.com/docs/git-stash)。

## 分支、同步与冲突

### 创建、切换和发布分支

```bash
git switch -c feature/example
git push --set-upstream origin feature/example
```

`--set-upstream`（可缩写为 `-u`）会把本地分支和远端分支关联起来；之后可以使用不带参数的 `git push` 和 `git pull`。不要假设当前分支或 `origin` 一定正确，先看 `git status` 与 `git remote -v`。

### 同步远端：先 fetch，再选择策略

```bash
git fetch --prune
git status
git log --oneline --graph --decorate HEAD..@{upstream}
git log --oneline --graph --decorate @{upstream}..HEAD
```

上面两条 `log` 分别列出“远端有而本地没有”和“本地有而远端没有”的提交。依据结果选择：

| 情况 | 建议 | 原因 |
|---|---|---|
| 本地没有独有提交，只是落后 | `git pull --ff-only` | 只允许快进；遇到分叉会失败，避免意外 merge。 |
| 个人、未共享功能分支分叉 | `git pull --rebase` | 将自己的提交重放在远端最新提交之后，历史保持线性。 |
| 共享分支且倾向使用 merge 整合 | `git pull --no-rebase` 或 `git merge @{upstream}` | 使用 merge 整合，不改写已有共享提交；只有无法快进时才会创建 merge commit（除非另有 merge 策略配置）。 |
| 即使可以快进也必须保留 merge commit | `git pull --no-rebase --no-ff` 或 `git merge --no-ff @{upstream}` | 强制创建 merge commit；仅在团队历史策略要求保留该节点时使用。 |
| 本地和远端都没有新提交 | 不操作 | 不要为“同步”制造空操作。 |

`git pull` 等于先获取远端更新，再按配置或参数整合。分叉时出现 “Need to specify how to reconcile divergent branches” 不是错误数据，而是 Git 要你明确选择 merge、rebase 或仅允许 fast-forward。对于个人功能分支，确认没有他人基于本地历史协作后，通常使用 `git pull --rebase`；对共享分支，优先 merge 或团队既定流程。

### 发生冲突怎么办

**rebase 冲突：**

```bash
git status
# 编辑冲突文件，删除冲突标记并确认语义
git add path/to/resolved-file
git rebase --continue

# 不确定或发现方向错误时：
git rebase --abort
```

**merge 冲突：**

```bash
git status
# 编辑并验证冲突文件
git add path/to/resolved-file
git commit

# 不确定时：
git merge --abort
```

不要为让冲突“消失”而盲目保留某一侧。冲突是两个版本对同一语义做了不同修改；解决后至少运行与该改动有关的测试或检查。

官方参考：[git-switch](https://git-scm.com/docs/git-switch)、[git-pull](https://git-scm.com/docs/git-pull)、[git-merge](https://git-scm.com/docs/git-merge)、[git-rebase](https://git-scm.com/docs/git-rebase)。

## 发布、tag 与变更追溯

Git tag 标记的是源码提交，**不等于该版本已经成功部署或生产验证通过**。建议为可发布版本创建带说明的 annotated tag：

```bash
git status
git show --stat HEAD
git tag -a v1.2.0 -m "Release v1.2.0"
git show v1.2.0
git push origin v1.2.0
```

查看两个发布版本之间的范围：

```bash
git log --oneline v1.1.0..v1.2.0
git diff --stat v1.1.0 v1.2.0
git describe --tags --always
```

- `git push origin <tag>` 只推指定 tag；`git push origin --tags` 会推送所有本地 tag，发布时更容易带出不该发布的 tag。
- CI/CD 应记录触发构建的 commit SHA、tag、构建产物标识和部署结果，才能回答“生产跑的是什么”。
- 浅克隆可能缺少早期 tag 或提交，导致 `describe`、跨版本比较、`blame`、`bisect` 的结论不完整；排障时先确认历史深度。

官方参考：[git-tag](https://git-scm.com/docs/git-tag)、[git-describe](https://git-scm.com/docs/git-describe)。

## 回滚、恢复与排障

### 已推送或已部署的错误：优先 revert

```bash
git show <bad-commit>
git revert <bad-commit>
git show HEAD
git branch --show-current
git branch -vv
git remote -v
git push <confirmed-remote> HEAD:<confirmed-branch>
```

`git revert` 会创建一个新的反向提交，保留完整审计历史，适合共享分支和发布后的修复。仅在 `git branch --show-current`、`git branch -vv` 和 `git remote -v` 已确认当前分支与其预期远端目标后，才替换 `<confirmed-remote>` 和 `<confirmed-branch>`。`HEAD:<confirmed-branch>` 会推送刚刚创建的回滚提交，而不是由隐式推送规则选择的本地分支。若回滚 merge commit，必须指定主线父提交（例如 `git revert -m 1 <merge-commit>`）；在执行前先确认团队的合并方向与实际影响。

### 本地错误提交：理解 reset 的差别

| 命令 | 提交历史 | 暂存区 | 工作区 | 适用边界 |
|---|---|---|---|---|
| `git reset --soft HEAD~1` | 回退 | 保留 | 保留 | 想重新组织最后一次未共享提交。 |
| `git reset --mixed HEAD~1` | 回退 | 清除 | 保留 | 想重新选择暂存内容；默认模式。 |
| `git reset --hard HEAD~1` | 回退 | 覆盖 | 覆盖 | **高风险**；只用于确认可丢弃的未共享工作。 |

`reset` 会移动当前分支引用。不要在已经共享或已推送的 `main`、发布分支上 reset 后强推；这会让其他人的历史失去共同基础。共享分支的业务回滚优先 `revert`。

### 误删分支、错误 reset：用 reflog 找回

```bash
git reflog
git show <recovered-commit>
git switch -c recovery/example <recovered-commit>
```

`reflog` 记录本地引用（如 `HEAD`）过去指向过的位置。找到疑似提交后，先 `show` 核对，再创建**新恢复分支**保护它；不要直接覆盖正在使用的分支。reflog 是本地记录，不是远端备份，也会随保留策略被清理。

### 找到是谁引入了问题

```bash
git blame -- path/to/file
git bisect start
git bisect bad <known-bad>
git bisect good <known-good>
# 对每个 Git 选出的提交运行可重复的检查，标记 good 或 bad
git bisect reset
```

`blame` 用于定位某行最后由哪个提交修改；它不等于责任归属。`bisect` 用二分法缩小引入回归的提交范围。结束时一定运行 `git bisect reset` 回到开始前的分支。

官方参考：[git-revert](https://git-scm.com/docs/git-revert)、[git-reset](https://git-scm.com/docs/git-reset)、[git-reflog](https://git-scm.com/docs/git-reflog)、[git-blame](https://git-scm.com/docs/git-blame)、[git-bisect](https://git-scm.com/docs/git-bisect)。

## 高风险操作与安全边界

| 操作 | 风险 | 安全做法 |
|---|---|---|
| `git push --force` | 可覆盖远端他人提交 | 个人分支必须改写历史时使用 `git push --force-with-lease`；先 fetch 并确认远端目标。 |
| `git reset --hard` | 丢弃工作区、暂存区或未共享提交 | 先 `status`、`diff`、`reflog`；需要保留时先建分支或 stash。 |
| 删除远端分支 | 会影响所有协作者和自动化 | 先确认 PR、部署和保护规则；使用明确分支名并获得授权。 |
| `git clean -fd` | 删除未跟踪文件/目录 | 先 `git clean -nd` 预演；不要把它当作常规清理。 |
| 重写共享历史 | 破坏协作者共同基础 | 共享分支优先 `revert`；确需重写时按团队变更窗口执行。 |

`--force-with-lease` 会在远端引用仍符合本地预期时才允许强推，因此比裸 `--force` 更安全；它不是共享分支强推的通行证。

### 秘密与敏感文件

- 不提交 token、私钥、`.env`、`kubeconfig`、云凭据、生产备份或客户数据。
- `.gitignore` 只影响**尚未被跟踪**的文件；已经提交过的文件不会因加入忽略规则而自动消失。
- 已跟踪的敏感文件可用 `git rm --cached path/to/file` 停止后续跟踪，但这不会清除历史或使已经泄露的凭据失效。
- 凭据泄露时：**先立即吊销或轮换凭据**，再评估访问日志、影响范围和平台允许的历史清理流程。只删除文件或重写历史都不能保证旧凭据未被复制。

官方参考：[git-push](https://git-scm.com/docs/git-push)、[git-clean](https://git-scm.com/docs/git-clean)、[gitignore](https://git-scm.com/docs/gitignore)。

## 每日最小命令集

```bash
# 开始工作或准备同步
git status
git fetch --prune
git status

# 检查并提交
git diff
git add path/to/file
git diff --staged
git commit -m "type: short description"

# 推送前再次确认目标和历史
git branch --show-current
git branch -vv
git remote -v
git push <confirmed-remote> HEAD:<confirmed-branch>
```

## 高风险操作前检查清单

- [ ] 我是否在正确的仓库和分支？（`git status`、`git remote -v`）
- [ ] 工作区和暂存区是否有要保留的内容？（`git diff`、`git diff --staged`）
- [ ] 我是否已获取远端最新状态？（`git fetch --prune`）
- [ ] 这是个人未共享分支，还是共享/受保护分支？
- [ ] 我能否用 `revert`、新分支或 `--force-with-lease` 等更安全方式达到目的？
- [ ] 若操作失败或判断错误，我的恢复点是什么？（commit、tag、stash、reflog、备份）
- [ ] 是否涉及生产、发布或凭据？如是，是否已遵循团队授权与变更流程？

## 官方文档入口

Git 的行为会随版本演进；执行不熟悉或高风险命令前，优先阅读对应的官方手册：<https://git-scm.com/docs>。
