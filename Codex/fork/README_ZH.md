# 在 ChatGPT Desktop 中 Fork Codex 对话

English version: [README.md](README.md)

本指南说明如何在 ChatGPT Desktop 的本地 Codex 对话中使用 fork。Fork 会将当前对话复制为一个新分支，因此你可以测试另一条思路，同时保留原对话。

本文只覆盖桌面版 composer 的交互，不覆盖 Codex CLI。控件会随 app 版本和账户权限变化；请以在 composer 输入 `/` 后实际显示的命令列表为准。

## `/fork` 是什么

在 composer 中使用 `/fork`，可将本地对话复制到：

- 一个新的本地对话：适合独立推理、排障或审查；或
- 一个新的 Git worktree：适合分支可能改动文件、且不能与原工作目录共享改动的情况。

新对话会获得 fork 前的对话上下文。但它从 fork 后就是独立对话：任一分支后续的消息、结论或修改不会自动同步到另一分支。

Fork 不表示前一段对话中的结论已经正确。把它们视为上下文，并要求新分支区分已验证证据和假设。

## 日常工作流

日常工作留在当前对话。发现 Codex 重复同一条失败路线、需要独立复核，或想比较不同方案时，再 fork。

1. 停止无效运行；不要让它基于同一个假设不断重试。
2. 在对话 composer 输入 `/fork`，并从命令列表中选择它。
3. 若只做分析，选择 **new local chat**；若 fork 可能改文件且需要隔离，选择 **new worktree**。
4. 在新分支中，必要时用 `/model` 选择更强模型，再用 `/reasoning` 选择推理强度。
5. 发送一段“重置排障”提示词：

   ```text
   不要继续沿用之前的假设。列出已验证事实、失败证据和未验证假设；
   给出互斥的根因，并为每个根因设计最小验证步骤。在有新证据前不要修改文件。
   ```

6. 用 `/status` 确认新对话实际使用的模型、reasoning、context 使用量和额度，再继续依赖它的输出。
7. 保留证据更强的分支。若需要回到原对话，请带回简短且基于证据的结论。

## Plan mode 与 reasoning

`/plan` 用于切换到 Plan mode；它本身不等于 reasoning 已经切换成功。本机 `config.toml` 请求 Default mode 使用 `low`、Plan mode 使用 `high`，但 Desktop app 可以保留对话级选择。

进入 `/plan` 后先运行 `/status`。若显示的 effort 不是 `high`，再运行 `/reasoning` 并手动选择 **high**。只有生产迁移、数据丢失风险或复杂安全审查等高风险、高不确定性决策，才使用 `xhigh`。

## 何时 fork、继续或新开对话

| 情况 | 建议操作 |
| --- | --- |
| 当前路线仍正确，只是还有下一步工作 | 继续当前对话。 |
| 对话开始兜圈，或需要独立诊断 | Fork 到新的本地对话。 |
| 需要竞争方案，且不能共享文件改动 | Fork 到新的 worktree。 |
| 旧对话已经不相关或带着错误前提 | 新建对话，只提供当前证据。 |

## 安全的分支习惯

- 在新分支第一条消息说明目的，例如“独立根因复核”或“替代实现审查”。
- 对话卡住时，要求新的验证步骤，而不是更多解释。
- 合并两个分支的结论前，检查它们的证据和真实文件状态。
- 普通 local-chat fork 共享同一个仓库文件；若两个分支都要独立修改同一项目，请使用 worktree fork。
- 不要在任一分支中粘贴凭据、令牌、私钥、生产数据或雇主/客户机密资料。

## 参考资料

- [OpenAI: Slash commands](https://learn.chatgpt.com/docs/reference/slash-commands)：ChatGPT Desktop 中 `/fork`、`/model`、`/reasoning`、`/plan` 和 `/status` 的说明。
- [OpenAI: Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)：用户级 `~/.codex/config.toml` 与配置优先级说明。
