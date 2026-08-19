# AWS Security Hub CSPM - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Security Hub Cloud Security Posture Management（AWS Security Hub CSPM）提供 AWS 环境安全态势的综合视图。它收集 AWS 服务（如 GuardDuty、Inspector、Macie）和受支持合作伙伴产品的安全发现，按安全标准持续执行检查，并通过安全评分给出整合、按优先级排序的视图。

## 核心概念

- **Finding（安全发现）**：按 AWS 安全发现格式（ASFF）标准化记录的安全问题。
- **安全标准与控制**：AWS Foundational Security Best Practices（FSBP）以及 CIS、PCI DSS、NIST 等外部框架；每个标准包含若干执行配置检查的控制项。
- **安全评分**：聚合合规结果，标出需要关注的账号和资源。
- **Insight（洞察）**：相关发现的集合；可创建自定义洞察。
- **自动化规则**：按你的条件自动更新或抑制发现。
- **跨账号与跨区域聚合**：指定聚合区域并关联其他区域，形成统一视图。
- **依赖 AWS Config**：大多数控制项要求账号和区域已启用 AWS Config 记录。

## 常用操作（AWS CLI）

```bash
# 在当前区域启用（含默认标准）
aws securityhub enable-security-hub --enable-default-standards

# 停用
aws securityhub disable-security-hub

# 标准与控制项
aws securityhub get-enabled-standards
aws securityhub batch-enable-standards --standards-subscription-requests file://standards.json
aws securityhub list-security-controls --standards-arn <standards-arn>

# Finding
aws securityhub get-findings
aws securityhub batch-import-findings --findings file://findings.json
aws securityhub batch-update-findings --finding-identifiers file://identifiers.json --note "reviewed"

# 洞察
aws securityhub create-insight --name open-critical --filters file://filters.json --group-by-attribute Severity
aws securityhub get-insight-results --insight-arn <insight-arn>
```

## 最佳实践

- 在所有受支持区域启用 Security Hub CSPM（CIS Foundations 完全合规要求），并配置跨区域聚合。
- 启用 AWS Config 并记录标准要检查的资源类型。
- 通过 AWS Organizations 使用委派管理员账号做多账号管理。
- 用安全评分和关键/高危发现排序，用自动化规则加速分诊。
- 将发现接入 EventBridge 做修复（工单、Lambda、runbook）。
- 定期检查已启用标准，关闭用不到的标准以控制成本。
- 规划初始基线：启用之后才会产生新发现。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 启用后没有发现 | 确认 AWS Config 在记录、标准已启用、区域受支持。 |
| 控制项不评估 | 在账号/区域启用 AWS Config 并记录所需资源类型。 |
| 聚合视图不完整 | 正确配置聚合区域，并在关联区域启用 Security Hub CSPM。 |
| GuardDuty/Inspector 发现缺失 | 在同一区域启用对应服务及其 Security Hub CSPM 集成。 |
| 成本异常 | 关闭未使用的标准/控制项；在 Settings → Usage 查看用量。 |

## 配额

每个管理员账号每区域最多 11,000 个成员账号；1,000 个待处理邀请；50 个自定义操作；100 个自定义洞察；100 个洞察结果；发现保留 90 天（如需更久，通过 EventBridge 归档到 S3）。以 Service Quotas 控制台当前值为准。

## 官方参考

- [AWS Security Hub CSPM 简介](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html)
- [Security Hub 配额](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub_limits.html)
- [AWS Security Hub 定价](https://aws.amazon.com/security-hub/pricing/)
- [AWS CLI：securityhub 命令](https://docs.aws.amazon.com/cli/latest/reference/securityhub/)
