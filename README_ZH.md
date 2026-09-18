# Kelvin 的工程笔记

[English](README.md) · 简体中文 · [浏览知识库站点](https://blog.kelvin.ink/)

记录系统故障怎么查、AI 编程工具怎么用，以及怎样让日常工程工作更顺手。

我把值得回头查阅的解释、命令和参考资料整理在这里，内容涵盖 SRE 排障手册与开发工具实践，提供中英文版本。

## 从一个实际问题开始

- **[Git 分支分叉了，接下来怎么办？](Git/README_ZH.md)** 先看清状态，再选择同步方式，并了解如何安全恢复。
- **[怎样正确地把改动发布到 GitHub？](Git/publish-to-github/README_ZH.md)** 按适合初学者的分支、提交、推送、Pull Request 和 squash merge 流程操作。
- **[Pod 一直 Pending，是 IP 不够吗？](Kubernetes/runbooks/insufficient-ip-or-eni/README_ZH.md)** 区分子网容量、节点限制和其他原因。

## 按你想做的事探索

### 排查故障与维护系统

- [Git](Git/README_ZH.md) — 安全同步、发布追溯、回滚与恢复；初学者可先阅读[发布流程](Git/publish-to-github/README_ZH.md)。
- [Kubernetes](Kubernetes/README_ZH.md) — 运维与事故处理手册。
- [AWS](AWS/README_ZH.md) — 以官方文档为依据的云服务参考与排障手册。
- [Nginx 与 OpenResty](Nginx/README_ZH.md) — 面向初学者的部署与运维指南。
- [Node.js 与 Express](Nodejs/README_ZH.md) — BFF 部署与事故处理。
- [ZooKeeper](ZooKeeper/README_ZH.md) — 运维与故障处理。

### 使用 AI 编程工具

- [Claude 子代理](Claude/subagents/README_ZH.md) — Anthropic Academy 入门课程学习指南。
- [Claude Code GitHub Actions](Claude/github-actions/README_ZH.md) — 通过明确的权限与安全边界运行交互式和自动化 Claude workflow。
- [Claude Managed Agents](Claude/managed-agents/README_ZH.md) — 面向长时间运行、异步任务的托管 agent 环境，是 Messages API 之外的另一种选择。
- [AI 原生 SDLC 实践手册](Claude/ai-native-sdlc-playbook/README_ZH.md) — 以版本化工件、反馈闭环和明确治理关口重新设计交付流程。
- [Warp 的自我改进 agent](Claude/self-improving-agents/README_ZH.md) — 把人类对 agent 输出的反馈，变成针对 agent 自身 skill 文件的、经过评审的 pull request。
- [Claude Code 云端会话](Claude/cloud-sessions/README_ZH.md) — 在 Anthropic 托管虚拟机中运行会话，在终端与云端之间交接工作，并自动修复 pull request。
- [构建 AI 原生的收入组织](Claude/ai-native-revenue-org/README_ZH.md) — 在销售组织推广 Claude：成熟度阶梯、三阶段计划、ROI 度量与常见陷阱。

### 准备 SRE 面试

- [Python 练习](Python/README_ZH.md) — 日志处理与算法。
- [Bash 练习](Bash/README_ZH.md) — 日志分析与进程检查。

### 配置开发环境

- [Ghostty 与终端工具](Ghostty/README_ZH.md) — 按平台整理的配置指南，附可复用的 [Ghostty 配置](Ghostty/config.ghostty)。
- [Ubuntu APT](Ubuntu/apt/README_ZH.md) — 软件包安装、升级、检查与排障。
- [Apple Container](apple/container/README_ZH.md) — 架构、用法与限制。

### 从视频里探索新想法

- [YouTube 学习笔记](YouTube/README_ZH.md) — 按主题浏览视频摘要，涵盖创业与 AI 代理等话题。

## 关于这些笔记

这些笔记来自个人学习与实践，不代表产品官方文档。我优先引用第一手资料，并区分个人理解与文档明确说明的行为。内容会随着新主题的学习和旧笔记的复查持续更新。

配对文章提供中英文版本，保持结构、链接和事实范围一致。可通过文章顶部的语言链接切换。

## 给贡献者与维护者

请保持内容聚焦、可复用且适合公开。不要加入凭据、公司或客户代码、机密数据、会话历史、缓存或机器专属信息。

- [视觉优先笔记工作流](.agents/skills/visual-first-notes/SKILL.md) — 将来源材料转化为心智模型、适当图表和精简的辅助文字。
- [YouTube 字幕工作流](.agents/skills/youtube-transcript/SKILL.md) — 视频摘要的制作与检查方式。
- [字幕工具模块](youtube-transcript/) — 配套工具。
