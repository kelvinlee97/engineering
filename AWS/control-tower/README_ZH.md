# AWS Control Tower - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Control Tower 编排多账户 AWS 环境（landing zone），并附带治理控制和自动化。它基于 AWS Organizations、AWS Service Catalog 和 AWS IAM Identity Center 供给账户、强制执行护栏（guardrails），并提供组织合规与漂移的仪表盘。

## 核心概念

- **Landing zone**：Control Tower 创建和管理的良好架构多账户基线（管理账户、组织单元、护栏和共享账户）。
- **组织单元（OU）**：Control Tower 管理根 OU 和自定义 OU（例如 workload、sandbox），并注册账户。
- **Controls（护栏）**：应用到 OU 和账户的治理规则。
  - **预防性控制（Preventive）**：使用服务控制策略（SCP）拒绝操作（例如禁止公开 S3 存储桶）。
  - **检测性控制（Detective）**：使用 AWS Config 规则检测并报告不合规资源。
  - **主动性控制（Proactive）**：使用 CloudFormation hooks 在供给前阻止不合规资源。
- **Account Factory**：自动化账户创建、基线和账户定制；可通过控制台、AWS Service Catalog 或 API 供给账户。
- **漂移检测**：Control Tower 定期检查违反 landing zone 的变更（例如手动修改 SCP），并在仪表盘上报。
- **扩展**：Control Tower 与 AWS Service Catalog（Account Factory portfolios）和 IAM Identity Center（访问管理）集成。

## 常用操作（AWS CLI）

```bash
# 检查 landing zone 状态并列出 OU/账户
aws controltower get-landing-zone --landing-zone-identifier <lz-id>
aws organizations list-roots
aws organizations list-accounts

# 列出 OU 上启用的控制
aws controltower list-enabled-controls --target-identifier <ou-arn>
aws controltower get-enabled-control --control-identifier <control-arn>
```

## 最佳实践

- 创建 landing zone 前先规划 OU 结构和护栏；之后变更结构需要漂移审查。
- 工作负载使用 Control Tower 管理的账户，管理账户仅保留管理任务。
- 对高影响操作（区域限制、公开访问）启用预防性控制，用检测性控制做监控。
- 使用带基线模板的 Account Factory，让每个账户一开始就合规。
- 监控仪表盘漂移并及时修复；不要手动修改 Control Tower 管理的资源。
- 与 IAM Identity Center 集成，对已注册账户集中管理最小权限访问。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| Landing zone 显示漂移 | 检查仪表盘中的不合规资源/SCP，修复或重新注册相关账户。 |
| OU 无法注册 | 确认 OU 在组织根层级中，且不与 Control Tower 管理结构冲突。 |
| 控制状态 `not applicable` | 检查控制范围：某些控制只适用于特定资源类型或区域。 |
| Account Factory 失败 | 检查账户供给基线的 AWS Service Catalog 和 CloudFormation StackSet 状态。 |
| 护栏执行延迟 | 检测性控制依赖 AWS Config；确认目标账户/区域已启用 Config 记录。 |

## 配额

Control Tower 支持特定的 OU 和账户结构，部分控制有区域范围；landing zone、账户和控制数量有限制。以 AWS Control Tower 端点和配额文档及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Control Tower？- 用户指南](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html)
- [AWS Control Tower controls](https://docs.aws.amazon.com/controltower/latest/userguide/controls.html)
- [AWS Control Tower 端点和配额](https://docs.aws.amazon.com/general/latest/gr/controltower.html)
- [AWS Control Tower 定价](https://aws.amazon.com/controltower/pricing/)
- [AWS CLI：controltower 命令](https://docs.aws.amazon.com/cli/latest/reference/controltower/)
