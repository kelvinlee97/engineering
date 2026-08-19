# AWS Organizations - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Organizations 用于集中管理多个 AWS 账号：创建和邀请账号、按组织单元（OU）分组、应用治理策略、跨账号共享资源，以及合并为一张账单结算。它是全球服务，托管在美东（弗吉尼亚北部）区域（us-east-1）。

## 核心概念

- **管理账号（Management account）**：创建组织的账号，用于账单和管理。
- **成员账号（Member accounts）**：组织内的账号，可以创建或邀请。
- **Root（根）**：顶层容器；每个组织只有一个。
- **组织单元（OU）**：账号分组，用于应用策略和组织结构。
- **服务控制策略（SCP）**：为成员账号设定权限边界；只能限制、不能授予权限。
- **资源控制策略（RCP）**：集中防止资源被意外的外部访问。
- **其他策略类型**：标签策略、备份策略、AI 服务退出策略、聊天应用策略。
- **委派管理员（Delegated administrator）**：代表组织管理某个受支持 AWS 服务的成员账号。
- **全部功能 vs 仅合并账单**：全部功能额外提供策略、集成和账号管理能力。

## 常用操作（AWS CLI）

```bash
# 创建启用全部功能的组织
aws organizations create-organization --feature-set ALL

# 列出账号和 root
aws organizations list-accounts
aws organizations list-roots

# 创建 OU
aws organizations create-ou --parent-id <root-id> --name Production

# 创建成员账号（异步）
aws organizations create-account --email admin-prod@example.com --account-name prod-account

# 创建并附加 SCP
aws organizations create-policy --name DenyUnapprovedRegions \
  --type SERVICE_CONTROL_POLICY --content file://scp.json
aws organizations attach-policy --policy-id <policy-id> --target-id <ou-id>

# 查看策略
aws organizations list-policies --filter SERVICE_CONTROL_POLICY
aws organizations list-targets-for-policy --policy-id <policy-id>

# 在 OU 之间移动账号
aws organizations move-account --account-id <account-id> \
  --source-parent-id <source-ou-id> --destination-parent-id <dest-ou-id>

# 注册委派管理员
aws organizations register-delegated-administrator --account-id <account-id> \
  --service-principal guardduty.amazonaws.com
```

## 最佳实践

- 采用多账号架构：账号是安全、成本和爆炸半径的自然边界。
- 管理账号只做账单和管理，不要运行工作负载。
- 按环境（dev/staging/prod）组织 OU，SCP 用拒绝列表；SCP 是边界，具体权限仍由 IAM 授予。
- 启用全部功能，使用 CloudTrail 组织追踪，成员账号无法关闭或篡改审计日志。
- 用委派管理员（GuardDuty、Security Hub CSPM、Config、IAM Identity Center），而不是都在管理账号操作。
- 在 Organizations 之上用 AWS Control Tower 提供预置治理护栏。
- 用 AWS Resource Access Manager（RAM）共享 VPC、子网、目录等公共资源，用 License Manager 集中管理许可。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 账号创建失败 | 检查账号配额和并发创建限制（最多 5 个进行中）；通过 Service Quotas 申请提高配额。 |
| SCP 不起作用 | SCP 不授予权限，也不作用于管理账号；确认目标账号是成员且 IAM 允许该操作。 |
| 无法移除账号 | 新建账号至少存在 4 天后才能移除；邀请 15 天后过期。 |
| 其他区域 API 调用失败 | Organizations 是全局服务；CLI/API 从 us-east-1 调用。 |
| 策略报错 | 检查 SCP 大小（10,240 字符）和每个实体的附加上限（10 个 SCP）。 |

## 配额

每个组织默认最多 10 个账号（可调整至最多 50,000）；1 个 root；2,000 个 OU；OU 最多嵌套 5 层；10,000 个 SCP；每个实体最多附加 10 个 SCP；每个 root/OU/账号最多 50 个标签。配额按组织生效；请在 us-east-1 的 Service Quotas 申请调整。

## 官方参考

- [什么是 AWS Organizations？](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html)
- [AWS Organizations 配额与服务限制](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html)
- [AWS Organizations 定价](https://aws.amazon.com/organizations/pricing/)
- [AWS CLI：organizations 命令](https://docs.aws.amazon.com/cli/latest/reference/organizations/)
