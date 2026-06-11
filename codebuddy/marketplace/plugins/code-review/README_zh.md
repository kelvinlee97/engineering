# Code Review Plugin

使用多个专业 Agent 自动审查 Pull Request，通过基于置信度的评分来过滤误报。

## 概述

Code Review Plugin 通过并行启动多个 Agent，从不同角度独立审计变更，实现 Pull Request 审查的自动化。它使用置信度评分来过滤误报，确保只发布高质量、可执行的反馈。

## 命令

### `/code-review`

使用多个专业 Agent 对 Pull Request 执行自动代码审查。

**功能：**
1. 检查是否需要审查（跳过已关闭、草稿、微不足道或已审查的 PR）
2. 从仓库中收集相关的 CODEBUDDY.md 指南文件
3. 总结 Pull Request 的变更
4. 启动 4 个并行 Agent 独立审查：
   - **Agent #1 和 #2**：审计 CODEBUDDY.md 合规性
   - **Agent #3**：扫描变更中的明显 bug
   - **Agent #4**：分析 git blame/历史以发现基于上下文的问题
5. 对每个问题按 0-100 分进行置信度评分
6. 过滤掉低于 80 置信度阈值的问题
7. 仅发布高置信度问题的审查评论

**用法：**
```bash
/code-review
```

**示例工作流：**
```bash
# 在 PR 分支上，运行：
/code-review

# CodeBuddy 将：
# - 并行启动 4 个审查 Agent
# - 对每个问题进行置信度评分
# - 发布置信度 ≥80 的问题评论
# - 如果未发现高置信度问题则跳过发布
```

**特性：**
- 多个独立 Agent 进行全面审查
- 基于置信度的评分减少误报（阈值：80）
- CODEBUDDY.md 合规性检查，带明确的指南验证
- Bug 检测专注于变更（而非预先存在的问题）
- 通过 git blame 进行历史上下文分析
- 自动跳过已关闭、草稿或已审查的 PR
- 直接链接到带有完整 SHA 和行范围的代码

**审查评论格式：**
```markdown
## Code review

Found 3 issues:

1. Missing error handling for OAuth callback (CODEBUDDY.md says "Always handle OAuth errors")

https://github.com/owner/repo/blob/abc123.../src/auth.ts#L67-L72

2. Memory leak: OAuth state not cleaned up (bug due to missing cleanup in finally block)

https://github.com/owner/repo/blob/abc123.../src/auth.ts#L88-L95

3. Inconsistent naming pattern (src/conventions/CODEBUDDY.md says "Use camelCase for functions")

https://github.com/owner/repo/blob/abc123.../src/utils.ts#L23-L28
```

**置信度评分：**
- **0**：不确信，误报
- **25**：有些确信，可能是真的
- **50**：中等确信，真实但不重要
- **75**：高度确信，真实且重要
- **100**：绝对确信，肯定真实

**过滤的误报：**
- PR 中未引入的预先存在的问题
- 看起来像 bug 但实际不是的代码
- 过于挑剔的小问题
- Linter 会捕获的问题
- 一般质量问题（除非在 CODEBUDDY.md 中）
- 带有 lint 忽略注释的问题

## 安装

此 Plugin 已包含在 CodeBuddy Code 仓库中。使用 CodeBuddy Code 时该命令自动可用。

## 最佳实践

### 使用 `/code-review`
- 维护清晰的 CODEBUDDY.md 文件以获得更好的合规性检查
- 相信 80+ 的置信度阈值——误报已被过滤
- 对所有非平凡的 Pull Request 运行
- 将 Agent 发现作为人工审查的起点
- 根据重复的审查模式更新 CODEBUDDY.md

### 何时使用
- 所有有重要变更的 Pull Request
- 涉及关键代码路径的 PR
- 来自多个贡献者的 PR
- 合规性重要的 PR

### 何时不使用
- 已关闭或草稿 PR（无论如何会自动跳过）
- 微不足道的自动 PR（自动跳过）
- 需要立即合并的紧急热修复
- 已审查过的 PR（自动跳过）

## 工作流集成

### 标准 PR 审查工作流：
```bash
# 创建带变更的 PR
/code-review

# 审查自动反馈
# 进行必要的修复
# 准备好后合并
```

### 作为 CI/CD 的一部分：
```bash
# 在 PR 创建或更新时触发
# 自动发布审查评论
# 如果审查已存在则跳过
```

## 要求

- 集成 GitHub 的 Git 仓库
- 已安装并认证 GitHub CLI (`gh`)
- CODEBUDDY.md 文件（可选但建议用于指南检查）

## 故障排除

### 审查耗时过长

**问题**：Agent 在大型 PR 上运行缓慢

**解决方案**：
- 大型变更的正常现象——Agent 并行运行
- 4 个独立 Agent 确保彻底性
- 考虑将大型 PR 拆分为更小的 PR

### 误报过多

**问题**：审查标记了不真实的问题

**解决方案**：
- 默认阈值为 80（已过滤大部分误报）
- 使 CODEBUDDY.md 更具体地说明什么重要
- 考虑标记的问题是否实际有效

### 未发布审查评论

**问题**：`/code-review` 运行但未出现评论

**解决方案**：
检查是否：
- PR 已关闭（跳过审查）
- PR 是草稿（跳过审查）
- PR 微不足道/自动生成（跳过审查）
- PR 已有审查（跳过审查）
- 没有得分 ≥80 的问题（无需评论）

### 链接格式损坏

**问题**：代码链接在 GitHub 中无法正确渲染

**解决方案**：
链接必须遵循此确切格式：
```
https://github.com/owner/repo/blob/[full-sha]/path/file.ext#L[start]-L[end]
```
- 必须使用完整 SHA（非缩写）
- 必须使用 `#L` 表示法
- 必须包含至少 1 行上下文的行范围

### GitHub CLI 不工作

**问题**：`gh` 命令失败

**解决方案**：
- 安装 GitHub CLI：`brew install gh`（macOS）或参阅 [GitHub CLI installation](https://cli.github.com/)
- 认证：`gh auth login`
- 验证仓库有 GitHub 远程

## 提示

- **编写具体的 CODEBUDDY.md 文件**：清晰的指南 = 更好的审查
- **在 PR 中包含上下文**：帮助 Agent 理解意图
- **使用置信度评分**：≥80 的问题通常是正确的
- **迭代改进指南**：根据模式更新 CODEBUDDY.md
- **自动审查**：设置为 PR 工作流的一部分
- **信任过滤**：阈值防止噪音

## 配置

### 调整置信度阈值

默认阈值为 80。要调整，修改命令文件 `commands/code-review.md`：
```markdown
Filter out any issues with a score less than 80.
```

将 `80` 更改为你首选的阈值（0-100）。

### 自定义审查重点

编辑 `commands/code-review.md` 以添加或修改 Agent 任务：
- 添加安全导向的 Agent
- 添加性能分析 Agent
- 添加可访问性检查 Agent
- 添加文档质量检查

## 技术细节

### Agent 架构
- **2x CODEBUDDY.md 合规性 Agent**：指南检查的冗余
- **1x bug 检测器**：仅专注于变更中的明显 bug
- **1x 历史分析器**：来自 git blame 和历史的上下文
- **Nx 置信度评分器**：每个问题一个用于独立评分

### 评分系统
- 每个问题独立评分 0-100
- 评分考虑证据强度和验证
- 阈值（默认 80）过滤低置信度问题
- 对于 CODEBUDDY.md 问题：验证指南明确提及

### GitHub 集成
使用 `gh` CLI 用于：
- 查看 PR 详细信息和差异
- 获取仓库数据
- 读取 git blame 和历史
- 发布审查评论

## 作者

Boris Cherny (boris@anthropic.com)

## 版本

1.0.0
