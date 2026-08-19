# Amazon Detective - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Detective 帮助你分析、调查并快速定位安全 finding 和可疑活动的根因。它自动从 AWS CloudTrail 和 VPC Flow Logs 提取基于时间的事件（登录、API 调用、网络流量），摄取 GuardDuty finding，并使用机器学习和图分析构建交互式可视化用于安全调查。

## 核心概念

- **行为图（Behavior graph）**：来自一个或多个账户的提取与分析事件的数据集合；启用 Detective 的账户成为图的 admin 账户，并邀请成员（或使用 AWS Organizations）。
- **数据源**：CloudTrail 管理事件、VPC Flow Logs 和 GuardDuty finding；保留最多一年历史事件数据。
- **Finding groups**：围绕潜在安全事件关联的 finding 和实体，用于分析高严重性 GuardDuty finding 的根因。
- **Detective Investigation**：使用失陷指标（IOC）对 IAM 用户/角色进行分流；可从控制台或 `StartInvestigation` API 启动。
- **Security Lake 集成**：查询和检索存储在 Amazon Security Lake 中的原始日志（CloudTrail、VPC Flow Logs、EKS 审计日志）。
- **VPC flow volume**：按 EC2 实例或 Kubernetes Pod 展示网络流的可视化摘要。
- **多账户**：admin 账户管理行为图；成员账户贡献数据。与 Security Hub CSPM 集成，可从 finding 直接跳转调查。

## 常用操作（AWS CLI）

```bash
# 创建行为图
aws detective create-graph
aws detective list-graphs

# 运行调查并查看结果
aws detective start-investigation --graph-arn <graph-arn> \
  --entity-arn <entity-arn> --scope-start-time 2026-08-18T00:00:00Z
aws detective list-investigations --graph-arn <graph-arn>
aws detective get-investigation --graph-arn <graph-arn> --investigation-id <id>

# 管理成员
aws detective list-members --graph-arn <graph-arn>
aws detective create-members --graph-arn <graph-arn> --accounts file://accounts.json
```

## 最佳实践

- 在 admin 账户启用 Detective，并纳入所有产生 GuardDuty finding 或敏感流量的账户。
- 使用 finding groups 调查高严重性 GuardDuty finding，看清完整攻击序列和影响范围。
- 先使用 Detective Investigation 快速分流用户/角色，再深入原始数据。
- 与 Security Hub CSPM 集成，让分析师能从 finding 直接跳转到 Detective。
- 需要原始日志取证时启用 Security Lake 集成。
- 监控行为图健康和成员注册；移除离开组织的账户。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 行为图没有数据 | 确认账户已启用 CloudTrail 和 VPC Flow Logs，且成员已接受/注册。 |
| GuardDuty finding 缺失 | 确认 GuardDuty 集成已启用，且 finding 在同一区域生成。 |
| 调查无结果 | 检查时间范围，以及实体（用户/角色/IP）在图内是否有活动。 |
| 成员不贡献数据 | 确认成员账户在图中，且权限允许数据采集。 |
| 成本高于预期 | Detective 按分析的数据量（GB）收费；审查数据量并关闭不需要的账户。 |

## 配额

每账户行为图、每图成员数以及调查数量有限制；首次启用有 30 天免费试用。以 Amazon Detective 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Detective？- 用户指南](https://docs.aws.amazon.com/detective/latest/userguide/what-is-detective.html)
- [Amazon Detective 端点和配额](https://docs.aws.amazon.com/general/latest/gr/detective.html)
- [Amazon Detective 定价](https://aws.amazon.com/detective/pricing/)
- [AWS CLI：detective 命令](https://docs.aws.amazon.com/cli/latest/reference/detective/)
