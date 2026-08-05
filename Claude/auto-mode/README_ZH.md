# Claude Code Auto Mode 如何工作

[English](README.md) | 简体中文

## 来源

- 视频：[How auto mode works with Claude Code](https://www.youtube.com/watch?v=b8SV4U6fEIc)
- 发布者：Claude
- 发布日期：2026-08-04
- 时长：5:41
- 来源覆盖：已完整读取 YouTube 英文自动字幕

本文是根据视频整理的原创摘要，不是逐字稿，也不能替代官方文档。

## 一句话总结

Claude Code 的 Auto Mode 并不是让 Claude 审批自己的操作，而是通过独立 classifier 检查高风险操作是否符合用户意图，从而减少重复确认，同时保留安全控制。

## 为什么需要 Auto Mode

Anthropic 在视频中表示，其研究发现大约 97% 的 Claude Code 权限请求最终都会被用户批准。逐项审批虽然提供控制权，但在多步骤任务中也容易产生 approval fatigue，并阻碍长时间运行的任务。

Auto Mode 的目标是：

- 自动执行低风险、可恢复的操作
- 检查潜在的破坏性或越界操作
- 减少不必要的人工确认
- 无法安全判断时重新交给用户审批

视频依据：[00:00–00:43](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=0s)

## Auto Mode 如何检查操作

### Claude 不会审批自己的操作

Claude 提出工具调用后，会交给独立 classifier 检查，而不是由 Claude 自己决定是否批准。

Classifier 可以看到：

- 用户消息
- Claude 提出的工具调用

Classifier 看不到：

- Claude 的内部推理
- Claude 给用户的回复
- 工具执行结果

这样可以降低 Claude 同时充当执行者和审核者所造成的偏差。

视频依据：[00:49–01:31](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=49s)

### 对照用户意图检查风险

Classifier 会判断 Claude 是否超出用户要求的范围、尝试不可逆或破坏性操作，或者访问配置的信任边界之外的系统。

例如，用户只要求清理本地内容，但 Claude 尝试删除远程 Git branches，这项操作应当被拒绝。操作被拒绝后，Claude 通常会寻找更安全的方法。如果 force push 到 `main` 被拒绝，它可以改为推送到新 branch。如果操作持续被拒绝，Auto Mode 会暂停并要求用户亲自决定。

视频依据：[01:31–02:03](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=91s)

### 防御 Prompt Injection

网页、代码或文件可能包含隐藏指令，试图让 Claude 偏离用户原本的目标。视频描述了两层防御：

1. Server-side probe 扫描工具返回的内容并标记可疑指令。
2. Classifier 检查 Claude 的下一步操作是否仍符合用户意图。

攻击必须同时绕过这两层才能影响后续操作。Anthropic 表示，在其内部 prompt-injection evaluations 中，同时启用 probe 和 Auto Mode 后，攻击成功率降至零。

这是 Anthropic 对内部评估结果的陈述，不代表所有真实环境都能获得相同结果。

视频依据：[02:03–02:46](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=123s)

## 哪些操作需要 Classifier 检查

大致检查顺序是：

1. 执行 `deny`、`ask` 和 `allow` permission rules。
2. 判断操作风险等级。
3. 必要时交给 classifier。
4. 执行、改用更安全方案，或暂停询问用户。

通常可以跳过 classifier 的操作：

- 搜索代码库
- 读取文件
- 修改项目内文件
- 其他只读或容易恢复的操作

通常需要 classifier 检查的操作：

- Shell commands
- Web fetches
- 访问当前环境之外的资源
- 难以撤销或可能造成破坏的操作

视频依据：[02:46–03:20](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=166s)

## 配置信任边界

默认情况下，Auto Mode 只把当前 working directory 和 Git remotes 视为内部环境。公司的 cloud buckets、internal services 和其他基础设施仍可能被视为外部资源。

可以使用 `environment` 字段，以自然语言描述可信环境，例如：

- GitHub organization
- AWS accounts 或 cloud buckets
- Internal services
- Development 和 staging infrastructure

管理员可以通过 managed settings 配置组织级环境。开发者可以增加个人配置，但不能删除管理员配置。

设置 `environment` 会替换 Claude 内置的默认内容，因此如需保留默认配置，应同时加入默认环境字符串。

视频依据：[03:20–04:10](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=200s)

## Guidance 与强制规则

Classifier guidance 包括：

- `allow`：通常可以接受的例外
- `soft deny`：除非用户明确要求，否则应拒绝
- `hard deny`：即使用户要求也应该拒绝

这些字段是 classifier 的判断依据，不是确定性的强制规则。

需要确定性限制时，应使用 Claude Code permission rules：

- `deny`：阻止匹配的工具调用
- `ask`：即使在 Auto Mode 下也强制询问用户
- `allow`：允许匹配操作

过于宽泛、足以执行任意代码的 `allow` rule 仍可能进入 classifier。

视频依据：[04:10–04:48](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=250s)

## Auto Mode 不是什么

Auto Mode 不是：

- Claude 自己批准自己的操作
- 完全取消权限控制
- 所有操作都无条件自动执行
- 对生产环境人工审核的替代品
- 绝对安全的 Prompt Injection 防护

## 对 DevOps 工作的建议

适合先尝试 Auto Mode：

- 在 feature branch 修改 Terraform
- 读取 Kubernetes manifests
- 分析 CI logs
- 更新项目文档
- 执行本地测试和 lint
- 创建新的修复 branch

建议继续强制人工确认：

- `terraform apply`
- Kubernetes production mutations
- 删除 cloud resources
- 修改 IAM permissions
- Force push protected branches
- Secrets 相关操作
- 数据库 migration 或 destructive SQL
- 修改生产 DNS、TLS 或 network policies

## 推荐启用方式

1. 从较小的权限范围开始。
2. 配置真实的环境边界。
3. 保留明确的 `deny` 和 `ask` rules。
4. 观察经常被拒绝的操作。
5. 确认风险后再逐步扩大范围。
6. 对生产基础设施继续人工审核。
7. 为团队环境建立自己的 evaluations。

视频依据：[05:13–05:32](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=313s)

## 核心结论

Auto Mode 的价值不是取消安全确认，而是把确认从每个工具调用提升到风险边界和用户意图层面。

它依赖四项主要机制：

1. 独立 classifier
2. 操作风险分级
3. Prompt-injection probe
4. 可配置的 environment trust boundary

## 延伸阅读

- [Anthropic Engineering Announcement](https://www.anthropic.com/engineering/claude-code-auto-mode)
- [Claude Code Auto Mode Configuration](https://code.claude.com/docs/en/auto-mode-config)
