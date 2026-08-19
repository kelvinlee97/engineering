# AWS Service Quotas - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Service Quotas 让你从单一位置查看和管理 AWS 服务的配额（限制）。配额是账户中资源、操作和项目的最大值（例如每账户 IAM 角色数或每区域 VPC 数）。当默认值无法满足需求时，你可以集中申请提升配额并监控用量。

## 核心概念

- **服务配额**：账户、区域或资源的资源/操作最大值；每个 AWS 服务定义自己的配额和默认值。
- **默认配额与应用配额**：默认值是 AWS 设定的初始值；应用配额是提升获批后的值。
- **可调整配额**：可以在账户级或资源级提升的配额；通过控制台/CLI/API 申请，AWS Support 会批准、拒绝或部分批准。
- **全局配额**：所有区域可用的账户级配额；提升申请在 us-east-1（公共 AWS）、GovCloud（US-West）或中国（北京）提交。
- **用量与利用率**：Service Quotas 显示当前资源用量和利用率百分比（例如 200 个资源中的 150 个 = 75%）。
- **自动管理（Automatic Management）**：监控配额用量，在耗尽前通知你。
- **资源级配额**：对于 OpenSearch Service 域实例数等配额，可针对单个资源应用值（context ID 为 ARN 或 `*`）。

## 常用操作（AWS CLI）

```bash
# 列出服务和配额
aws service-quotas list-services
aws service-quotas list-service-quotas --service-code ec2 --region us-east-1

# 获取当前配额和用量
aws service-quotas get-service-quota --service-code ec2 \
  --quota-code L-1234567890abcdef0
aws service-quotas get-aws-default-service-quota --service-code ec2 \
  --quota-code L-1234567890abcdef0

# 申请提升并跟踪
aws service-quotas request-service-quota-increase --service-code ec2 \
  --quota-code L-1234567890abcdef0 --desired-value 100
aws service-quotas list-requested-service-quota-change-history \
  --service-code ec2
```

## 最佳实践

- 大规模工作负载启动前跟踪配额；用自动管理在接近限制时获得通知。
- 尽早申请提升；审批可能需要时间，且可能部分批准。
- 全局配额从正确的 Home Region 提交申请（公共 AWS 为 us-east-1）。
- 用 CloudWatch/配额告警监控利用率，将配额检查集成到供给管道。
- 区分账户级与资源级配额；服务支持时使用资源级提升。
- 自动化中使用 Service Quotas API，而不是硬编码限制。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 配额提升被拒 | 检查服务可调整性和申请值；部分配额不可调整或有审批标准。 |
| 找不到配额 | 核对服务代码和区域；部分配额是全局或区域专属。 |
| 提升长期未决 | 在控制台检查申请状态；延迟时联系 AWS Support。 |
| 资源级配额不可用 | 确认服务支持资源级配额；必要时使用 CLI 2.13.20+。 |
| 配额指标告警 | 对已发布配额用量指标的服务设置 CloudWatch 告警。 |

## 配额

配额提升申请和 API 请求速率有限制。以 Service Quotas 用户指南和各服务配额页面为准。

## 官方参考

- [什么是 Service Quotas？- 用户指南](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html)
- [Service Quotas 端点和配额](https://docs.aws.amazon.com/general/latest/gr/servicequotas.html)
- [AWS CLI：service-quotas 命令](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/)
