# Claude Code Agent Skills 完整课程指南

English version: [README.md](README.md)

这是 Anthropic Academy **Introduction to agent skills** 的完整学习指南，覆盖全部六课的
官方文章及可读取的官方视频字幕。本文是原创总结，不是逐字稿，也不能替代官方课程。

## 来源覆盖情况

| 课程 | 官方文章 | 官方视频 | 覆盖状态 |
| --- | --- | --- | --- |
| [What are skills?](https://anthropic.skilljar.com/introduction-to-agent-skills/434525) | 已完整读取 | [视频](https://www.youtube.com/watch?v=bjdBVZa66oU)，无可用字幕 | 文章完整；视频字幕不可用 |
| [Creating your first skill](https://anthropic.skilljar.com/introduction-to-agent-skills/434527) | 已完整读取 | [视频](https://www.youtube.com/watch?v=Wx6_vjFFyHM)，已完整读取英文自动字幕 | 完整 |
| [Configuration and multi-file skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434526) | 已完整读取 | [视频](https://www.youtube.com/watch?v=98KaK_rn5rQ)，已完整读取英文自动字幕 | 完整 |
| [Skills vs. other Claude Code features](https://anthropic.skilljar.com/introduction-to-agent-skills/434528) | 已完整读取 | [视频](https://www.youtube.com/watch?v=IgNN4v0BJdU)，已完整读取英文自动字幕 | 完整 |
| [Sharing skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434529) | 已完整读取 | [视频](https://www.youtube.com/watch?v=OCBi3eScNLk)，已完整读取英文自动字幕 | 完整 |
| [Troubleshooting skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434530) | 已完整读取 | [视频](https://www.youtube.com/watch?v=YBa1cwaG7is)，已完整读取英文自动字幕 | 完整 |

第一课的嵌入视频没有可导出的字幕。其书面课程包含相同的学习目标与关键结论，因此该课
仅依据文章整理；本文没有虚构字幕或时间戳。

## 用一个心智模型理解整门课

> Skill 是 Claude 根据 description 发现、只在相关时加载的任务型知识。始终生效的规则
> 应放在其他位置；委派工作用 subagent 隔离；事件自动化或外部能力则分别交给 hook 与 MCP。

六节课组成一条完整链路：

1. **判断是否适合：** 把反复出现、只与特定任务相关的指令编码成 skill。
2. **从最小结构开始：** 创建一个具名目录，其中只需包含 `SKILL.md`。
3. **通过渐进披露扩展：** 保持入口精简，需要时再读取参考资料或运行脚本。
4. **选择正确机制：** 不要把项目规则、任务委派、事件或外部工具硬塞进 skill。
5. **按受众分发：** 根据使用范围选择 Git、plugin 或企业托管设置。
6. **系统排障：** 先验证结构，再检查匹配、优先级和运行时失败。

## 第一课 — What are skills?

### 定义与发现机制

Skill 是一组指令与可选资源，用来教 Claude Code 处理某类特定任务。必须存在的
`SKILL.md` 以包含 `name` 和 `description` 的 frontmatter 开头，后面才是具体指令。

Claude 起初只看到 skill 的名称和描述。收到请求后，它会比较请求与所有描述，并按需加载
匹配的 skill。因此，description 同时承担发现元数据与核心触发信号两项职责。

### Skill 存放位置

| 范围 | 课程中的路径 | 适用内容 |
| --- | --- | --- |
| 个人 | `~/.claude/skills/<skill-name>/SKILL.md` | 跨项目使用的个人偏好与工作流 |
| 项目 | `.claude/skills/<skill-name>/SKILL.md` | 通过版本控制共享的仓库专属规范 |

Windows 的个人目录为 `C:/Users/<your-user>/.claude/skills`。

### Skill 的独特之处

- `CLAUDE.md` 每次对话都会加载，适合永远生效的规则。
- Skill 只在相关时加载，避免无关内容占用上下文。
- Slash command 必须显式输入；skill 可以根据普通请求的意图自动激活。

适合的场景包括代码审查清单、commit 格式、品牌规范、文档模板，以及特定框架的调试流程。
课程给出的实用判断是：如果你不断向 Claude 重复解释同一种任务，它很可能值得做成 skill。

官方来源：[What are skills?](https://anthropic.skilljar.com/introduction-to-agent-skills/434525)

## 第二课 — Creating your first skill

### 最小结构

先创建与 skill 同名的目录，再添加 `SKILL.md`：

```text
~/.claude/skills/pr-description/
└── SKILL.md
```

```markdown
---
name: pr-description
description: Writes pull request descriptions. Use when creating or summarizing a pull request.
---

When writing a PR description:

1. Inspect the complete branch diff.
2. Explain what changed and why.
3. List the concrete changes and any renamed or deleted files.
```

三部分职责清楚分离：`name` 标识 skill，`description` 决定何时匹配，正文则定义加载后
Claude 应该执行的流程。

视频依据：[00:18–00:46](https://www.youtube.com/watch?v=Wx6_vjFFyHM&t=18s)

### 加载与匹配

Claude Code 启动时扫描配置好的 skill 位置，但起初只加载名称与描述。它按照语义重叠匹配，
并不要求请求与某条命令完全一致。课程要求在新增、修改或删除 skill 后重启 Claude Code，
然后再测试变更。

测试时应使用真实表达，而不是只重复 description 中的原句。成功测试既要确认 skill 被发现，
也要确认最终结果遵循正文指令。

### 同名冲突的优先级

课程给出的优先顺序是：

1. 企业托管 skill。
2. 个人 skill。
3. 项目 skill。
4. Plugin skill。

与其使用 `review` 这种宽泛名称，不如使用 `frontend-review` 等具体名称来减少意外冲突。

官方来源：[Creating your first skill](https://anthropic.skilljar.com/introduction-to-agent-skills/434527)

## 第三课 — Configuration and multi-file skills

### Frontmatter 字段

| 字段 | 是否必需 | 课程指导 |
| --- | --- | --- |
| `name` | 必需 | 只用小写字母、数字和连字符；不超过 64 字符；与目录名一致 |
| `description` | 必需 | 不超过 1,024 字符；说明做什么以及何时使用 |
| `allowed-tools` | 可选 | 为只读或安全敏感流程限制工具 |
| `model` | 可选 | 必要时为 skill 指定模型 |

Description 应包含用户实际会说的话。如果一个性能 skill 应匹配“为什么这么慢？”或
“帮我做性能分析”，描述就必须与这些请求有足够的语义重叠。

视频依据：[00:12–00:43](https://www.youtube.com/watch?v=98KaK_rn5rQ&t=12s)

### 最小工具权限

`allowed-tools` 会限制 skill 激活期间无需额外许可即可使用的工具。只读的 onboarding skill
可以允许 `Read`、`Grep`、`Glob` 和 `Bash`，但不提供编辑工具。完全省略此字段时，Claude
继续使用正常权限模型。

### 渐进披露

把核心流程留在 `SKILL.md`，只在需要时读取支持文件：

```text
my-skill/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

入口文件应明确说明何时读取每份 reference 或运行每个 script。课程建议把 `SKILL.md` 控制在
500 行以内，超出后考虑拆分支持资料。脚本尤其节省上下文：让 Claude 运行经过测试的脚本，
只有输出而非源代码需要进入工作上下文。

官方来源：[Configuration and multi-file skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434526)

## 第四课 — Skills vs. other Claude Code features

### 按行为选择

| 机制 | 核心区别 | 适用内容 |
| --- | --- | --- |
| `CLAUDE.md` | 始终加载 | 项目级规则与约束 |
| Skill | 根据请求匹配并按需加载 | 特定任务的知识与流程 |
| Subagent | 独立执行上下文 | 隔离委派工作或使用不同工具权限 |
| Hook | 由事件触发 | 围绕工具操作运行固定检查或副作用 |
| MCP server | 提供外部能力 | 集成、数据源与工具 |

视频依据：[00:02–00:38](https://www.youtube.com/watch?v=IgNN4v0BJdU&t=2s)

Skill 扩展当前对话。Subagent 离开当前上下文，独立工作后返回结果。Hook 响应事件，而不是
理解请求意图。MCP 是能力边界，不是指令格式。

这些机制可以组合：项目用 `CLAUDE.md` 保存长期规则，用 skill 提供 PR 审查知识，用 hook
自动验证，用 subagent 隔离审查，再用 MCP 访问外部服务，无需让任何单一机制包办全部职责。

官方来源：[Skills vs. other Claude Code features](https://anthropic.skilljar.com/introduction-to-agent-skills/434528)

## 第五课 — Sharing skills

### 分发方式

| 受众 | 分发方式 | 最适合 |
| --- | --- | --- |
| 一个仓库或团队 | 把 `.claude/skills` 提交到 Git | 项目专属流程与规范 |
| 多个仓库或社区 | 把 skills 打包进 plugin 与 marketplace | 可复用、非项目专属的 skills |
| 整个组织 | 企业托管设置 | 强制执行的安全、合规与编码标准 |

仓库 skill 通过团队正常的 pull 流程更新；plugin 让可复用组合能够跨项目安装；企业 skill
具有最高优先级，适合必须在组织范围内生效的标准。

视频依据：[00:20–00:41](https://www.youtube.com/watch?v=OCBi3eScNLk&t=20s)

### Skills 与 subagents

Subagent 不会自动继承主对话的 skills：

- Explorer、Plan 和 Verify 等内置 agent 无法访问 skills。
- 自定义 subagent 只有在 frontmatter 显式列出时才能使用 skills。
- 列出的 skills 在自定义 subagent 启动时加载，不会像主对话一样按需匹配。

```yaml
---
name: frontend-reviewer
description: Review frontend changes for accessibility and performance.
tools: Bash, Glob, Grep, Read
model: sonnet
skills: accessibility-audit, performance-check
---
```

被引用的 skills 必须已经存在于可用的 skills 目录。这种组合适合让隔离任务始终应用一组
明确、固定的标准。

官方来源：[Sharing skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434529)

## 第六课 — Troubleshooting skills

### 按顺序诊断

先运行 Agent Skills validator，排除结构问题后再调试行为。然后按症状分类：

| 症状 | 常见原因 | 第一项修复 |
| --- | --- | --- |
| 没有触发 | Description 与真实请求缺少语义重叠 | 加入用户实际会说的具体触发短语 |
| 没有加载 | 目录、文件名或 YAML 错误 | 把精确命名的 `SKILL.md` 放入具名目录并检查 `claude --debug` |
| 使用了错误 skill | Descriptions 太相似 | 明确区分范围与触发语言 |
| 个人 skill 被忽略 | 同名的高优先级 skill 覆盖它 | 检查优先级并重命名低优先级 skill |
| Plugin skill 不出现 | 缓存、安装或 plugin 结构问题 | 验证结构、清缓存、重启并重装 |
| 运行时失败 | 依赖、权限或路径错误 | 安装依赖、赋予脚本执行权限并使用正斜杠 |

视频依据：[00:03–00:38](https://www.youtube.com/watch?v=YBa1cwaG7is&t=3s)

测试触发时应尝试多种自然表达，而不是只用一条理想 prompt。处理运行时问题时，在 skill
文档中注明依赖，为可执行脚本运行 `chmod +x`，并在 Windows 上也使用可移植的正斜杠路径。

官方来源：[Troubleshooting skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434530)

## 实践检查清单

分享 skill 前：

1. 确认这个任务会重复出现，并且只在特定场景相关。
2. 让目录名与 frontmatter 使用同一个具体名称。
3. 在 description 中同时说明做什么与何时激活。
4. `SKILL.md` 只保留核心流程。
5. 仅在流程确实需要权限边界时限制工具。
6. 用多种真实触发语句及实际结果进行测试。
7. 运行 validator，并在重启后的 Claude Code 会话中复测。
8. 根据目标受众选择 Git、plugin 或企业托管设置。
