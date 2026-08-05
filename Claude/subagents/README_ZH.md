# Claude Code Subagents 完整课程指南

English version: [README.md](README.md)

这是 Anthropic Academy **Introduction to subagents** 的完整学习指南，覆盖全部四课及可读取的官方视频字幕。本文是原创总结，不是逐字稿，也不能替代官方课程。

## 来源覆盖情况

| 课程 | 官方文章 | 官方视频 | 覆盖状态 |
| --- | --- | --- | --- |
| [What are subagents?](https://anthropic.skilljar.com/introduction-to-subagents/450698) | 已完整读取 | [视频](https://www.youtube.com/watch?v=jKErNxuxPXg)，已完整读取英文自动字幕 | 完整 |
| [Creating a subagent](https://anthropic.skilljar.com/introduction-to-subagents/450699) | 已完整读取 | [嵌入视频](https://www.youtube.com/watch?v=arD6qEWa2Xc)目前因版权主张而无法播放 | 文章完整；视频不可用 |
| [Designing effective subagents](https://anthropic.skilljar.com/introduction-to-subagents/450700) | 已完整读取 | [视频](https://www.youtube.com/watch?v=WPxWKT_OaU4)，已完整读取英文自动字幕 | 完整 |
| [Using subagents effectively](https://anthropic.skilljar.com/introduction-to-subagents/450701) | 已完整读取 | [视频](https://www.youtube.com/watch?v=n5LoKZ8Oa-A)，已完整读取英文自动字幕 | 完整 |

第二课的课程播放器和 YouTube 直达链接都明确显示：视频因 Lynda 提出的版权主张而被阻止。本文没有为它虚构字幕或时间戳；其内容依据完整的官方文章整理。

## 用一个心智模型理解整门课

> 当一个聚焦的工作者可以隔离完成大量中间工作，并向主对话返回一个可验证、定义清楚的小结果时，subagent 才真正有价值。

四节课组成一条完整链路：

1. **理解隔离：** subagent 在独立上下文中工作并返回总结。
2. **有意识地创建：** 定义范围、描述、工具、模型和 system prompt。
3. **设计成可以完成：** 明确输入、输出格式、障碍报告和最小工具权限。
4. **选择性委派：** 当结果比中间过程更重要时才使用 subagent。

## 第一课 — What are subagents?

### 定义与生命周期

Subagent 是 Claude Code 可以委派任务的专用助手。它在独立对话上下文中运行，完成任务后向父 agent 返回聚焦总结，随后其独立对话被丢弃。

它会接收两个输入：

1. 配置文件中的自定义 system prompt，用来定义角色和行为。
2. 父 agent 根据用户请求编写的任务描述。

它读取的文件、执行的搜索、编辑和工具结果都留在隔离上下文中。主对话保留原始请求与返回的总结，而不是完整调查过程。

视频依据：[00:03–00:24](https://www.youtube.com/watch?v=jKErNxuxPXg&t=3s)、[00:40–01:12](https://www.youtube.com/watch?v=jKErNxuxPXg&t=40s)

### 为什么隔离很重要

每次对话和工具结果都会占用主上下文窗口。大型调查可能用已经不再有用的材料填满有限空间。Subagent 会把这些嘈杂的探索过程移到别处，从而保护主上下文。

代价同样重要：父 agent 无法完整看到 subagent 如何得出结论，也看不到它发现但未写入总结的信息。

视频依据：[00:24–00:40](https://www.youtube.com/watch?v=jKErNxuxPXg&t=24s)、[01:52–02:02](https://www.youtube.com/watch?v=jKErNxuxPXg&t=112s)

### 课程示例

为了在陌生代码库中确认哪个服务负责退款，Claude 可能读取约 15 个文件、运行搜索并追踪函数调用。不使用 subagent 时，即使最终只需要一个事实，全部过程都会进入主上下文。使用 Explore subagent 后，调查过程保持隔离，只有聚焦答案返回。

视频依据：[01:13–01:52](https://www.youtube.com/watch?v=jKErNxuxPXg&t=73s)

### 内置 subagents

| Subagent | 课程中的用途 |
| --- | --- |
| General purpose | 同时需要探索与执行操作的多步骤任务 |
| Explore | 快速搜索和浏览代码库 |
| Plan | 在 plan mode 中研究和分析代码库 |

Claude Code 还支持拥有独立 system prompt 和工具权限的自定义 subagents。

视频依据：[02:01–02:30](https://www.youtube.com/watch?v=jKErNxuxPXg&t=121s)

## 第二课 — Creating a subagent

### 创建流程

课程建议通过 `/agents` 命令创建自定义 subagent：

1. 运行 `/agents`，选择 **Create new agent**。
2. 选择范围：
   - **Project-level：** 只在当前项目中可用。
   - **User-level：** 在本机所有项目中共享。
3. 选择手动配置，或者描述期望行为并让 Claude 生成初始名称、描述和 system prompt。课程推荐把自动生成作为更容易的起点。
4. 选择工具、模型和 UI 颜色。
5. 保存生成的 Markdown 配置。
6. 使用代表性任务测试；如果没有按预期触发委派，就继续优化描述。

官方来源：[Creating a subagent](https://anthropic.skilljar.com/introduction-to-subagents/450699)

### 选择工具

创建界面把工具分为只读、编辑、执行、MCP 和其他工具。选择应由任务决定：

- 代码审查者通常只需要读取和分析代码，不应该编辑代码。
- 为了检查待处理变更，执行权限仍可能有用。
- 只有工作本身需要修改时，才应该授予编辑和写入权限。

这是课程第一次体现最小权限原则：先确认 subagent 必须完成什么，再只授予完成该工作所需的工具。

### 模型与颜色

课程中的模型选择器提供四个选项：

| 选项 | 课程指导 |
| --- | --- |
| Haiku | 快速、轻量任务 |
| Sonnet | 速度与深度之间的平衡 |
| Opus | 复杂分析 |
| Inherit | 使用主对话当前运行的模型 |

颜色是 UI 提示，可帮助用户辨认当前活跃的 subagent。

### 配置文件

Project-level subagent 通常存放于：

```text
.claude/agents/your-agent-name.md
```

最小配置由 YAML frontmatter 和后面的 system prompt 组成：

```markdown
---
name: code-quality-reviewer
description: Review specified code changes for quality and risk.
tools: Bash, Glob, Grep, Read
model: sonnet
color: purple
---

Review only the files named in the delegated task. Report findings by
severity and include enough evidence for the parent agent to verify them.
```

| 字段 | 作用 |
| --- | --- |
| `name` | 唯一标识，也可使用 `@agent <name>` 引用 subagent |
| `description` | 告诉 Claude 何时委派，并帮助形成委派输入 prompt |
| `tools` | 定义 subagent 可以使用的工具 |
| `model` | 在课程示例中选择 `sonnet`、`opus`、`haiku` 或 `inherit` |
| `color` | 在 UI 中标识当前活跃的 subagent |
| Markdown 正文 | 定义关注点、方法和汇报行为的 system prompt |

Description 必须保持单行；需要换行时可以使用转义的 `\n`。具体的触发示例能帮助 Claude 识别合适的委派场景。

### 自动使用与测试

当 subagent 应被自动考虑时，课程建议在 description 中加入 **“proactively”**。在 description 中添加示例，可以让触发条件更加具体。

创建后，应使用真实任务测试。如果 Claude 没有在预期时使用它，应该为 description 加入更明确的触发条件和示例，而不是认为只有 system prompt 会控制选择行为。

## 第三课 — Designing effective subagents

课程总结出有效 subagent 的四项特征：

1. 具体的 description。
2. 结构化输出。
3. 障碍报告。
4. 受限的工具权限。

视频总览：[00:03–00:10](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=3s)、[03:27–03:37](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=207s)

### Description 有两个作用

所有可用 subagent 的 name 和 description 都会进入主 agent 的 system prompt。父 agent 根据它们决定何时启动哪个 subagent。

Description 还会指导父 agent 编写输入 prompt。模糊的 reviewer 描述可能只产生“寻找当前变更”这种模糊指令；更强的描述可以要求父 agent 明确列出要检查的文件。同样，在研究 subagent 的 description 中要求可引用来源，也会把该要求带入委派 prompt。

视频依据：[00:17–00:49](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=17s)、[00:49–01:39](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=49s)

### 工作开始前先定义输出

课程把明确输出格式称为最重要的改进。它为 subagent 提供检查清单和自然停止条件。没有输出格式时，研究 subagent 很难判断信息是否已经足够，往往会运行过久。

代码审查输出可以要求：

1. 总结。
2. 严重问题。
3. 主要问题。
4. 次要问题。
5. 建议。
6. 批准状态。
7. 遇到的障碍。

具体标题取决于任务，但不变的原则是：完成状态必须可以被观察。

视频依据：[01:41–02:03](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=101s)

### 把障碍纳入结果

如果 subagent 发现了 workaround、特殊环境设置、必要参数或有问题的依赖，却没有写入总结，主线程就必须重新发现一次。输出格式应该明确要求汇报：

- 设置问题与环境特性；
- 工作过程中发现的 workaround；
- 需要特殊参数或配置的命令；
- 导致问题的依赖或 import。

视频依据：[02:04–02:42](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=124s)

### 按角色限制工具

| Subagent 角色 | 课程建议的权限 |
| --- | --- |
| 研究／只读 | `Glob`、`Grep`、`Read` |
| 代码审查 | 只读工具，加上用于 `git diff` 等命令的 `Bash`；不提供编辑／写入 |
| 样式或代码修改 | 因为工作本身需要修改，所以增加编辑／写入权限 |

最小权限既能减少意外副作用，也能让每个 subagent 的职责更加清晰。

视频依据：[02:42–03:26](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=162s)

## 第四课 — Using subagents effectively

### 决策规则

只问一个问题：

> **中间过程对主线程重要吗？**

- 如果只有最终结果重要，适合考虑委派。
- 如果主线程必须看到、保留或根据中间发现及时反应，就应该让工作留在主线程。

当探索能够与执行分开时，subagent 最有效。步骤彼此依赖时，多次交接会造成信息损失。

视频依据：[00:03–00:32](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=3s)、[04:33–04:41](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=273s)

### 强使用场景

#### 研究与探索

研究 subagent 可以搜索大量文件和代码路径，只返回父 agent 所需的位置与解释。课程以在陌生代码库中定位 JWT 验证逻辑为例。

视频依据：[00:32–01:17](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=32s)

#### 使用新上下文进行代码审查

如果同一个主对话经过很多轮协助创建了代码，Claude 可能很难重新以批判角度审查自己的工作。Reviewer subagent 没有这段创建历史，可以运行 `git diff`、读取修改文件并应用专门审查标准。它的 system prompt 还可以编码项目专属规范，让团队得到一致的审查标准。

视频依据：[01:15–02:01](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=75s)

#### 真正需要不同 system prompt 的任务

- Copywriting subagent 可以使用关于受众、语气、声音和结构的指令，而不是 Claude Code 简洁、技术化的默认风格。
- Styling subagent 可以把 design system 文件加载到自己的上下文中，在编写 CSS 前先掌握项目的颜色、间距和组件约定。

视频依据：[01:59–03:00](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=119s)

### 反模式

#### 空洞的专家人设

“Python expert”或“Kubernetes specialist”这种标签本身不会增加能力，因为主 Claude 对话本来就具备这些知识。只有在 subagent 真正提供不同 system prompt、聚焦上下文或受控工具时，隔离的成本才值得承担。

视频依据：[02:57–03:27](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=177s)

#### 各步骤相互依赖的顺序流水线

“复现 → 调试 → 修复”流水线会在每个 agent 依赖上一步发现时丢失信息。只有任务真正独立时才适合流水线；否则应该留在同一个上下文完成。

视频依据：[03:27–03:46](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=207s)

#### Test-runner subagent

测试失败往往需要完整输出。Subagent 如果只把它压缩成“测试失败”，就隐藏了诊断所需证据，反而需要额外工作找回信息。课程表示，在其测试过的配置中，test-runner 模式表现较差。

视频依据：[03:46–04:09](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=226s)

## 端到端设计检查清单

创建或使用 subagent 前，回答以下问题：

### 委派

- 工作是否足够聚焦，可以被描述为一个任务？
- 主线程需要中间过程，还是只需要结果？
- 相互依赖的步骤是否留在同一个上下文？

### 配置

- 应该选择 project-level 还是 user-level？
- Name 与单行 description 是否解释了何时委派？
- Description 是否能帮助父 agent 编写精确任务 prompt？
- 模型的速度与深度是否适合任务？

### 安全与完成条件

- 工具是否被限制到最低需求？
- 输出格式是否让完成状态可以被观察？
- 是否必须返回证据、来源、文件或行号？
- 是否有专门的障碍与 workaround 部分？

### 验证

- 父 agent 能否验证返回的总结？
- 是否使用代表性任务测试过 subagent？
- 如果没有触发委派，是否为 description 增加了具体示例？

## 知识检查

不要重读指南，直接回答：

1. Subagent 会接收哪两个输入？
2. 返回总结后，它的独立对话会怎样？
3. 上下文隔离获得了什么，又失去了什么？
4. Project-level 与 user-level 有什么区别？
5. 哪个配置字段同时控制 subagent 选择和父 agent 编写的委派 prompt？
6. 为什么结构化输出能让 subagent 更可靠地结束？
7. 哪些障碍必须返回主线程？
8. 只读研究者、reviewer 和修改者分别应该有哪些工具？
9. 为什么 reviewer subagent 可能得到更“新鲜”的审查视角？
10. 为什么单纯的“专家”标签不是有用的 subagent？
11. 为什么步骤相互依赖的顺序流水线有风险？
12. 决定是否委派时应该问哪一个问题？

## 实践练习

设计一个 **repository authentication researcher** subagent。

产出：

1. 一行 `description`，说明何时使用，并要求父 agent 提供准确目标问题。
2. 最小 `tools` 列表。
3. 把任务限制为只读研究的 system prompt。
4. 包含结论、证据、相关文件与行号、不确定性和遇到的障碍的输出格式。
5. 一个应该触发 subagent 的示例，以及一个应该留在主线程的示例。
6. 父 agent 可以对返回总结执行的一项验证。

最后必须使用课程的决策规则进行论证：解释中间过程是否重要。

## 来源

### 官方课程文章

- [What are subagents?](https://anthropic.skilljar.com/introduction-to-subagents/450698)
- [Creating a subagent](https://anthropic.skilljar.com/introduction-to-subagents/450699)
- [Designing effective subagents](https://anthropic.skilljar.com/introduction-to-subagents/450700)
- [Using subagents effectively](https://anthropic.skilljar.com/introduction-to-subagents/450701)

全部文章均于 2026-08-05 通过已注册的 Anthropic Academy 课程会话读取。

### 官方课程视频

- [What are subagents?](https://www.youtube.com/watch?v=jKErNxuxPXg) — 2026-08-05 已读取英文自动字幕。
- [Creating a subagent](https://www.youtube.com/watch?v=arD6qEWa2Xc) — 2026-08-05 因版权主张而无法播放；未使用字幕。
- [Designing effective subagents](https://www.youtube.com/watch?v=WPxWKT_OaU4) — 2026-08-05 已读取英文自动字幕。
- [Using subagents effectively](https://www.youtube.com/watch?v=n5LoKZ8Oa-A) — 2026-08-05 已读取英文自动字幕。

