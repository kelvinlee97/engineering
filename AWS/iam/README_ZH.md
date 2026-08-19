# AWS IAM - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-18

## 概述

AWS Identity and Access Management（IAM）控制 AWS 资源的认证（谁登录）与授权（谁有权限）。IAM、IAM Identity Center 和 AWS STS 包含在 AWS 账号中，不额外收费。IAM 是最终一致（eventually consistent）的。

## 核心概念

- **根用户**：创建账号时的初始身份，拥有全部权限；日常操作不要使用。
- **IAM 用户、用户组、角色**：你创建的身份，用于给人和工作负载授权；角色提供临时凭证。
- **策略（Policies）**：附加到身份或资源的 JSON 文档，定义权限。
- **身份提供商与联邦**：人类用户应通过身份提供商登录（AWS 建议用 IAM Identity Center 做集中访问管理）。
- **AWS STS**：签发临时凭证（例如 `AssumeRole`）。
- **权限边界（Permissions boundaries）**：限制身份策略能授予的最大权限。
- **组织护栏**：AWS Organizations 的服务控制策略（SCP）和资源控制策略（RCP）设定跨账户边界；它们本身不授予权限。

## 常用操作（AWS CLI）

```bash
# 我是谁
aws sts get-caller-identity

# 用户和用户组
aws iam create-user --user-name alice
aws iam create-group --group-name developers
aws iam add-user-to-group --user-name alice --group-name developers

# 策略
aws iam create-policy --policy-name s3-read-only --policy-document file://policy.json
aws iam attach-user-policy --user-name alice --policy-arn arn:aws:iam::123456789012:policy/s3-read-only

# 角色：先建信任策略，再挂权限
aws iam create-role --role-name app-role --assume-role-policy-document file://trust.json
aws iam attach-role-policy --role-name app-role --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# 扮演角色、查看访问密钥
aws sts assume-role --role-arn arn:aws:iam::123456789012:role/app-role --role-session-name my-session
aws iam list-access-keys --user-name alice
```

## 安全最佳实践

- 一律使用**临时凭证**：人类用户走联邦登录（IAM Identity Center），工作负载用 IAM 角色（EC2 实例角色、Lambda 执行角色、ECS/EKS 任务角色）。
- 根用户和所有长期凭证**强制 MFA**。
- 保护根用户凭证，绝不用于日常操作。
- 遵循**最小权限**：从 AWS 托管策略开始，逐步收敛为客户托管策略。
- 用 **IAM Access Analyzer** 从 CloudTrail 活动生成最小权限策略、校验策略、发现公有/跨账户访问。
- 定期清理未使用的用户、角色、策略和访问密钥（利用 last accessed 信息）。
- 使用**条件**（例如强制 TLS）和**权限边界**来委派权限管理。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| `AccessDenied` | 检查身份策略、资源策略、SCP/RCP、权限边界和会话策略；IAM 最终一致，传播完成后重试。 |
| `AssumeRole` 失败 | 确认角色信任策略允许该主体；检查 external ID，以及请求的会话时长是否超过角色最大时长（最长 12 小时）。 |
| 无法删除用户/角色 | 先移除附加与内联策略、访问密钥和组成员关系。 |
| 访问密钥轮换 | 用 `aws iam list-access-keys` 和 last accessed 信息停用并删除不用的密钥。 |

## 配额（每账户默认值）

| 资源 | 默认配额 |
|------|---------|
| 角色 | 1,000 |
| 客户托管策略 | 1,500 |
| 用户组 | 300 |
| 实例配置文件 | 1,000 |
| 每个角色 / 用户可挂托管策略 | 20 / 10 |
| 托管策略大小 | 6,144 字符 |
| 内联策略大小（用户 / 角色 / 用户组） | 2,048 / 10,240 / 5,120 字符 |
| 角色信任策略大小 | 2,048 字符（最大 8,192） |
| 角色会话最大时长 | 12 小时 |
| STS 请求 | 每账户每区域每秒 600 次 |

可调配额和当前值以 Service Quotas 为准。

## 官方参考

- [什么是 IAM？- IAM 用户指南](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [IAM 安全最佳实践](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [IAM 与 AWS STS 配额](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html)
- [AWS CLI：iam 命令](https://docs.aws.amazon.com/cli/latest/reference/iam/)
