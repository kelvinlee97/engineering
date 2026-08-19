# Codex Goals：`/goal` Slash Command 指南

English version: [README.md](README.md)

`/goal` 给 Codex 一个持久目标，让它跨多轮持续推进，而不是完成一轮普通对话就停下来。它适合有明确目标、有验证循环、且足够空间让 Codex 自行推进的工作。goal 激活后，Codex 可以连续工作数小时，并在它认为已达到停止条件时自行结束。

本指南覆盖 Codex CLI 和 ChatGPT Desktop composer 中的 `/goal`。命令菜单和功能可用性会随 Codex 版本、配置和账户变化；以输入 `/` 后实际显示的命令列表为准。

## `/goal` 能做什么

- `/goal <objective>`：设置新 goal。
- `/goal`：查看当前 goal。
- `/goal edit <objective>`：修改 goal。
- `/goal pause`、`/goal resume`、`/goal clear`：控制运行。

Goal 绑定当前对话。目标文本必须非空且不超过 4,000 字符；更长的说明请放进文件（例如 `PLAN.md`），再让 goal 指向它。

如果命令列表里没有 `/goal`，在 `~/.codex/config.toml` 中启用 goals 功能：

```toml
[features]
goals = true
```

也可以运行 `codex features enable goals`，或直接让 Codex 帮你启用。编写本指南的机器上，`codex features list` 显示 `goals` 为 stable 且已启用。

## 什么样的工作适合 goal

好的 goal 大于一条 prompt，但小于一个没有边界的 backlog。它要说明：Codex 应达成什么、不应改动什么、如何验证进展、何时停止。

适合：

- 目标栈、一致性检查和约束都明确的代码迁移
- 每个 checkpoint 后都跑测试的大型重构
- 有可量化健康检查的部署重试循环
- 以"能构建、能启动"为完成标准的实验、原型或游戏
- 针对目标分数的 prompt 或 eval 优化

避免：松散且互不相关的任务清单、没有可验证终态的模糊目标、需要频繁改变方向的工作。

## 建立执行循环

1. 明确一个目标和一条停止条件。
2. 告诉 Codex 先读哪些文件、文档、issue、日志或计划。
3. 定义证明进展的命令或产物。
4. 要求分 checkpoint 推进，并保留简短进度日志。
5. 用 `/goal` 查看状态；按需 `/goal pause`、`/goal resume` 或 `/goal clear`。

示例提示词：

```text
/goal 把项目从 [旧技术栈] 迁移到 [新技术栈]，保持所有页面视觉一致，
并用 playwright interactive 验证输出。
```

```text
/goal 按 PLAN.md 实现。为每个里程碑补充测试，并用 playwright interactive
验证输出。
```

```text
/goal 优化 [文件或目录] 中的 prompts，直到 eval 达到 [目标分数]。
每次修改后运行 [eval 命令] 并检查失败用例；达到目标或需要产品/策略决策时停止。
```

```text
/goal 部署到 staging 并持续重试，直到健康检查通过、smoke test 成功。
```

## 日常工作流

- 常规有边界的小任务留在普通对话；需要先定方案的多步改动先用 `/plan`。
- 任务会跨很多轮且停止条件清晰时，用 `/goal`。
- 运行期间要求紧凑的状态更新：当前 checkpoint、已验证内容、剩余工作、是否被阻塞。状态变得含糊时，收紧 goal 而不是追加零散指令。
- 把激活中的 goal 当作后台任务：Codex 会一直工作到它确信达到停止条件，然后停下。
- 对话在同一错误假设上兜圈、goal 本身需要换方向时，fork 或新开对话。

| 情况 | 建议操作 |
| --- | --- |
| 小的有界任务 | 普通对话。 |
| 需要先定方案的多步改动 | `/plan`，然后普通对话。 |
| 有可验证终态的长任务 | `/goal <objective>`。 |
| 对话在错误假设上兜圈 | `/fork` 到新对话。 |

## 触发 goal 的其他方式

斜杠命令不是唯一入口：

- 直接在对话里让 Codex 设置 goal 并开始工作；官方指南建议先简短讨论，再让它设置 goal。
- 在仓库 `AGENTS.md` 中加规则（例如"任务匹配 X 时，先设置 goal 并做到停止条件为止"），让该仓库的会话自动使用 goal。这是基于 `AGENTS.md` 指导 Codex 的实践，官方没有单独承诺其与 goal 的组合。
- 定义一个把任务拆成多个 goal 的 skill，再通过 `AGENTS.md`、定时任务提示词（`$skill-name`）或其他 agent 调用。
- 在 ChatGPT Desktop 中创建定时任务，让每次新 run 的提示词要求设置 goal；skill 也可以创建定时任务。

定时任务和 skill 的支持是 OpenAI 官方文档化的；它们与 goal 的组合遵循同一 agent 循环，编写本指南时官方尚未单独文档化。

## 参考资料

- [OpenAI: Follow a goal](https://developers.openai.com/codex/use-cases/follow-goals)
- [OpenAI: Developer commands](https://learn.chatgpt.com/docs/developer-commands)
- [OpenAI: Scheduled tasks](https://developers.openai.com/codex/app/automations)
