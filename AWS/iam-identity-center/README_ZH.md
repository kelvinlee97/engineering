# AWS IAM Identity Center - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS IAM Identity Center（AWS Single Sign-On 的继任者，2022 年 7 月更名）集中管理员工身份以及对 AWS 账户和云应用的访问。它是多账户访问的推荐方案：创建用户/组或连接外部身份提供方，分配 permission set，用户通过访问门户登录。

## 核心概念

- **Instance**：Identity Center 实例；多账户访问时，在组织管理账户创建实例，使其能管理 AWS Organizations 中的账户（最佳实践）。
- **Permission set**：一组命名 IAM 策略（AWS 托管、客户托管或内联）加上会话时长，定义用户在一个 AWS 账户中能做什么；分配给账户。
- **Account assignment**：授予用户或组通过某个 permission set 访问某个 AWS 账户；按组而不是按个人分配。
- **访问门户（Access portal）**：终端用户登录（带 MFA）并启动账户/应用的 URL。
- **身份来源**：Identity Center 目录，或外部 IdP（Okta、Microsoft Entra ID 等），支持 SCIM 自动供给和/或 SAML 2.0 联合。
- **可信身份传播（Trusted identity propagation）**：将终端用户身份和上下文从 Identity Center 传递给应用（例如 Amazon Q Business），而不是共享服务账户。
- **旧命名空间**：服务 API 仍使用 `sso`、`sso-admin` 和 `identitystore` 命名空间；CLI 命令为 `aws sso-admin ...` 和 `aws identitystore ...`，CLI 登录使用 `aws sso login`。

## 常用操作（AWS CLI）

```bash
# 列出实例并创建 permission set
aws sso-admin list-instances
aws sso-admin create-permission-set \
  --instance-arn <instance-arn> --name PowerUser \
  --session-duration PT2H

# 附加托管策略并分配访问权限
aws sso-admin attach-managed-policy-to-permission-set \
  --instance-arn <instance-arn> --permission-set-arn <ps-arn> \
  --managed-policy-arn arn:aws:iam::aws:policy/PowerUserAccess
aws sso-admin create-account-assignment \
  --instance-arn <instance-arn> --target-type AWS_ACCOUNT \
  --target-id 123456789012 --principal-type GROUP \
  --principal-id <group-id> --permission-set-arn <ps-arn>

# 列出身份库中的用户/组
aws identitystore list-users --identity-store-id <store-id>
aws identitystore list-groups --identity-store-id <store-id>

# 登录 CLI 会话（浏览器流程）
aws configure sso
aws sso login --sso-session prod
```

## 最佳实践

- 将 Identity Center 实例放在组织管理账户，按组分配访问而不是按个人。
- 使用最小权限的 permission set 和合理的会话时长；优先以 AWS 托管的工作职能策略作为基线。
- 以外部 IdP 为身份源，用 SCIM 自动供给用户/组。
- 强制 MFA，并使用自己的域名配置访问门户。
- 分析、安全等应用账户与生产账户分开分配访问权限。
- 用 CloudTrail 监控登录和分配活动，定期审查分配。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 用户无法访问门户/账户 | 检查账户分配、组成员、permission set，以及实例是否在管理账户。 |
| 外部 IdP 用户缺失 | 核对 SCIM 供给已启用且 bearer token 有效；确认 SAML 元数据为最新。 |
| 带 MFA 登录失败 | 检查 MFA 注册状态以及访问门户 URL/域配置。 |
| CLI 登录报错 | 重新运行 `aws configure sso`；确认 SSO 会话名和 start URL 匹配。 |
| 新账户不可见 | 确认账户在 AWS Organizations 中，并重新执行供给/分配。 |

## 配额

permission set、账户分配、Identity Center 目录中的用户/组以及实例配额都有限制。以 IAM Identity Center 配额文档和 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS IAM Identity Center？- 用户指南](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
- [AWS IAM Identity Center permission sets](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html)
- [AWS IAM Identity Center 配额](https://docs.aws.amazon.com/singlesignon/latest/userguide/quotas.html)
- [AWS IAM Identity Center 定价](https://aws.amazon.com/iam/identity-center/pricing/)
- [AWS CLI：sso-admin 和 identitystore 命令](https://docs.aws.amazon.com/cli/latest/reference/sso-admin/)
