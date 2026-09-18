# Claude

English version: [README.md](README.md)

本模块收录 Anthropic Claude 开发者工具的学习笔记：编程 agent 本身、运行它的各种 harness，以及围绕它们建立的交付实践。

## 笔记

| 笔记 | 说明 |
| --- | --- |
| [Claude Code Agent Skills 入门](agent-skills/README_ZH.md) | skill 是什么、何时加载，以及它如何改变一次会话。 |
| [Claude Code Auto Mode 的工作方式](auto-mode/README_ZH.md) | auto mode 启用的工具选择行为，以及它在实践中改变了什么。 |
| [Claude Code Subagents 入门](subagents/README_ZH.md) | Anthropic Academy subagents 入门课程的学习指南。 |
| [Claude Code GitHub Actions](github-actions/README_ZH.md) | 在明确的权限与安全边界下运行交互式和自动化的 Claude 工作流。 |
| [Claude Managed Agents](managed-agents/README_ZH.md) | 面向长时间异步任务的托管 agent harness，作为 Messages API 之外的另一种选择。 |
| [AI 原生 SDLC 实践手册](ai-native-sdlc-playbook/README_ZH.md) | 围绕版本化产物、反馈回路和明确的治理关卡重新设计交付流程。 |
| [Warp 如何在 Claude 上构建自我改进的 agent](self-improving-agents/README_ZH.md) | inner skill 负责干活，定时运行的 outer skill 把人类反馈变成针对它的 pull request。 |
| [Claude Code 云端会话](cloud-sessions/README_ZH.md) | 运行在 Anthropic 托管虚拟机中的会话：环境、GitHub 访问、终端交接与 PR 自动修复。 |
| [构建 AI 原生的收入组织](ai-native-revenue-org/README_ZH.md) | Anthropic 面向销售组织推广 Claude 的指南：成熟度阶梯、三阶段推广、ROI 度量，以及会让推广卡住的陷阱。 |
| [Claude Projects 改版](projects/README_ZH.md) | Project 变成一场对话：coordinator 把工作拆成并行的云端会话 thread，共享 memory 与 library。 |
