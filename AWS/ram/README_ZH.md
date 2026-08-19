# AWS Resource Access Manager (RAM) - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Resource Access Manager（AWS RAM）让你跨 AWS 账户、组织单元或整个组织共享 AWS 资源。你创建 resource share、选择主体（principal），附加的托管权限控制接收方对共享资源的操作，避免在每个账户重复创建相同基础设施。

## 核心概念

- **Resource share**：包含资源和主体（账户、OU 或整个组织）的共享单元。
- **主体（Principals）**：获得访问权限的账户；在组织外共享时，会发送邀请，接收方必须接受。
- **托管权限（Managed permissions）**：服务定义或客户定义的权限，指定共享资源上允许的操作（例如子网只读与读写）；客户托管权限使用 RAM 管理的策略。
- **Home Region**：对于 Aurora global database 等全局资源，resource share 在 Home Region（全局资源为 us-east-1）创建，并从该区域共享。
- **标签与共享**：用标签组织 resource share，并用标签策略管理访问。

RAM 常见共享资源包括 VPC 子网、Transit Gateway、Route 53 Resolver 规则、License Manager 许可证、Aurora/DocumentDB/Neptune/RDS 数据库、SageMaker 笔记本等。

## 常用操作（AWS CLI）

```bash
# 创建 resource share
aws ram create-resource-share --name shared-subnets \
  --resource-arns arn:aws:ec2:us-east-1:123456789012:subnet/subnet-0123456789abcdef0 \
  --principals 210987654321

# 列出和查看共享
aws ram list-resource-shares --resource-owner SELF
aws ram list-resources --resource-share-owner SELF

# 邀请（组织外共享时）
aws ram get-resource-share-invitations
aws ram accept-resource-share-invitation \
  --resource-share-invitation-arn <invitation-arn>

# 删除共享
aws ram delete-resource-share --resource-share-arn <share-arn>
```

## 最佳实践

- 尽可能按 OU 或整个组织共享，新账户自动获得访问，无需维护账户列表。
- 使用最小权限的托管权限；够用时优先选择服务托管的只读权限。
- VPC 共享时向目标账户共享子网，让它们在子网内直接启动资源；不要重复创建重叠 VPC。
- 资源生命周期由资源所有者负责；接收方不能修改或删除共享资源本身。
- 定期审查 resource share 和主体，清理过期共享。
- 用 CloudTrail 监控共享活动以留审计。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 接收方看不到共享资源 | 确认资源在相同区域/Home Region、主体已添加、邀请已接受。 |
| 共享资源上操作被拒 | 检查共享附带的托管权限以及接收方的 IAM 权限。 |
| 共享创建失败 | 核对资源是否支持共享，ARN/主体值是否正确。 |
| 全局资源未共享 | 全局资源在 Home Region（us-east-1）创建/关联共享。 |
| 删除共享失败 | 先分离所有主体/资源，或共享处于 `deleting` 状态；等待后重试。 |

## 配额

AWS RAM 本身无额外费用；你为共享的资源付费。resource share 数、每共享主体数和每账户共享资源数有配额。以 AWS RAM 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Resource Access Manager？- 用户指南](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html)
- [AWS RAM 支持的资源](https://docs.aws.amazon.com/ram/latest/userguide/shareable.html)
- [AWS RAM 配额](https://docs.aws.amazon.com/ram/latest/userguide/quotas.html)
- [AWS RAM 定价](https://aws.amazon.com/ram/pricing/)
- [AWS CLI：ram 命令](https://docs.aws.amazon.com/cli/latest/reference/ram/)
