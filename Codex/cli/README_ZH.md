# Codex CLI Slash Command：快速指南

English version: [README.md](README.md)

Codex CLI 是在终端中使用的互动式编程助手。Slash command 用于控制当前对话：查看状态、规划任务、审查改动，以及管理已保存会话。它们不是 shell 命令，也不能替代正常的 Git 审查或仓库规则。

请以你安装版本中输入 `/` 后显示的菜单为准。可用命令会随 Codex 版本、配置、操作系统和账户而变化。

## 从这里开始

在要处理的仓库中运行 `codex`，然后给出简短且有边界的任务。一个实用的起步闭环是：

```text
/status
/mention AGENTS.md
/plan 只更新文档。保留无关改动，并在报告结果前运行相关检查。
```

- `/status` 显示当前模型、审批策略、可写根目录与 context 使用情况。
- `/mention path/to/file` 将重要文件加入当前 chat，供后续请求直接引用。
- `/plan` 帮助你在改动前规划多步骤任务；Codex 正在工作时不能使用它。

## 最常用命令

| 命令 | 作用 |
| --- | --- |
| `/permissions` | 选择 Codex 无需再次询问即可执行的权限。选择所需最小权限，然后用 `/status` 确认。 |
| `/diff` | 在检查点或 commit 前显示 staged、unstaged 与 untracked 改动。 |
| `/review` | 审查 working tree 中的问题与缺失测试。它是额外检查，不是正确性的证明。 |
| `/compact` | 压缩很长的对话以释放 context，并保留关键决策。 |
| `/side` | 不离开父对话，临时开启一个聚焦调查。用于只读问题。 |
| `/fork` | 从当前对话创建一个新 chat，探索可持续的替代方案。 |
| `/resume` | 通过会话选择器重新打开已保存的活动 chat。 |
| `/rename` | 为当前 chat 命名，方便之后查找。 |
| `/archive` | 归档当前 chat 并退出 Codex。之后可用 `codex unarchive <SESSION>` 恢复。 |
| `/exit` | 不归档当前 chat，直接离开 CLI。 |

## 日常安全工作流

1. 运行 `/status`，再用 `/mention` 附加相关规则。
2. 对非简单改动，用 `/plan` 写明范围、检查项和不能改动的内容。
3. 让 Codex 完成有边界的改动。
4. 查看 `/diff`，运行仓库相关检查，再用 `/review`。
5. 只通过正常 Git 命令保存或提交目标文件。

只读审查时，在 `/permissions` 中选择 `Read Only`。任何改动都应保留无关 working tree 改动，并在批准操作前核对目标路径。不要把 `/delete`、`/logout` 或其他会改变状态的命令放入无人值守流程。

## 参考资料

- [OpenAI: Developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [OpenAI: Codex CLI overview](https://developers.openai.com/codex/cli)
- [在 ChatGPT Desktop 中 Fork Codex 对话](../fork/README_ZH.md)
