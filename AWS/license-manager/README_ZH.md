# AWS License Manager - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS License Manager 帮助你在多个 AWS 账户和区域管理 Microsoft、SAP、Oracle、IBM 等软件厂商的许可证。它提供统一可见性和报告，支持自带许可证（BYOL），用规则强制许可证限额，并帮助独立软件供应商（ISV）通过托管权益（managed entitlements）分发和跟踪许可证。

## 核心概念

- **许可证配置（License configuration）**：定义产品许可证消耗的硬/软限制规则（vCPU、物理核、插槽、机器数）。
- **许可证规则与执行**：管理员设置限制，防止不合规服务器使用；违规会被报告。
- **License asset groups**：在组织内跨多个区域/账户集中管理和跟踪许可证。
- **自管许可证**：基于企业协议在单账户内定义规则。
- **已授予许可证（Granted licenses）**：治理来自 AWS Marketplace、AWS Data Exchange 或已集成托管权益的卖家的许可证。
- **托管权益（Managed entitlements）**：ISV 创建许可证，通过 IAM 身份或签名令牌分发给终端用户，并跟踪带数量和时限的 check-out/check-in。
- **清单（Inventory）**：用 Systems Manager Inventory 和许可证规则发现本地应用与许可证。
- **集成**：Amazon EC2、Amazon RDS（Oracle/Db2 vCPU BYOL）、AWS Marketplace、Systems Manager、Organizations 和用户订阅。

## 常用操作（AWS CLI）

```bash
# 创建许可证配置并列出
aws license-manager create-license-configuration --name sql-byol \
  --license-counting-type vCPU --license-count 100 \
  --license-rules '{"hardLimit":true}'
aws license-manager list-license-configurations

# 管理托管权益的授权
aws license-manager create-license --license-configuration-arn <config-arn> \
  --license-name prod --product-name my-product --issuer file://issuer.json \
  --entitlements file://entitlements.json --consumption-configuration file://consumption.json
aws license-manager list-licenses
aws license-manager check-in-license --license-arn <license-arn> \
  --beneficiary 123456789012 --principal 123456789012
```

## 最佳实践

- 将厂商协议建模为带硬/软限制的许可证配置，并关联到 EC2/RDS 资源。
- 多账户/多区域用 license asset groups 集中治理；从管理账户集中管理。
- 迁移前用 Systems Manager Inventory 跟踪本地使用量。
- 受支持产品用用户订阅简化按用户许可。
- 监控许可证使用仪表盘，用量接近限制时设置告警。
- ISV 用托管权益分发，跟踪 check-out 数据用于审计。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 许可证用量未跟踪 | 核对资源是否关联到许可证配置，以及所在区域是否受支持。 |
| 规则未执行 | 检查许可证配置的硬/软限制设置和资源关联。 |
| 授权不可见 | 确认授权状态、受益账户和 IAM 权限。 |
| RDS BYOL 不匹配 | 使用 RDS 的 Oracle/Db2 vCPU 许可集成；核对实例类和许可模型。 |
| 清单缺失 | 确认本地服务器上 Systems Manager Inventory 已运行且已注册。 |

## 配额

每账户许可证配置、许可证和授权数量有限制。以 AWS License Manager 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS License Manager？- 用户指南](https://docs.aws.amazon.com/license-manager/latest/userguide/license-manager.html)
- [AWS License Manager 端点和配额](https://docs.aws.amazon.com/general/latest/gr/license-manager.html)
- [AWS License Manager 定价](https://aws.amazon.com/license-manager/pricing/)
- [AWS CLI：license-manager 命令](https://docs.aws.amazon.com/cli/latest/reference/license-manager/)
