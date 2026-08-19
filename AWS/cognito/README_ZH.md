# Amazon Cognito - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Cognito 为 Web 和移动应用提供认证、授权和用户管理。它包含两个主要组件：user pool 负责注册/登录和身份联合，identity pool 将已认证或访客身份交换为临时 AWS 凭证。

## 核心概念

- **User pool**：带注册/登录流程的用户目录，支持密码策略、MFA（TOTP、短信）、账户恢复和托管登录页面。它支持与社交 IdP（Apple、Facebook、Google、Amazon）以及 OIDC/SAML 提供方联合，并向应用客户端签发 JWT。
- **App client**：user pool 中的应用配置，包含 ID/密钥、允许的 OAuth 范围与回调 URL。
- **Identity pool**：将来自 user pool 或外部 IdP 的令牌通过 AWS Security Token Service（STS）交换为临时 AWS 凭证；支持基于角色的访问（按身份映射角色）和基于属性的访问控制；未认证（访客）身份可获取受限凭证。
- **User pool + identity pool 流程**：用户先在 user pool 认证，再由 identity pool 授予访问应用 AWS 资源（例如 S3、DynamoDB、API Gateway）所需的 AWS 凭证。
- **托管登录（Managed login）**：Cognito 托管的登录页面，可自定义，并支持 OAuth 2.0 和 OIDC 流程。

## 常用操作（AWS CLI）

```bash
# User pool 和应用客户端
aws cognito-idp create-user-pool --pool-name app-users \
  --policies "PasswordPolicy={MinimumLength=12,RequireUppercase=true}"
aws cognito-idp create-user-pool-client --user-pool-id <pool-id> \
  --client-name web --no-generate-secret

# 管理员用户操作
aws cognito-idp admin-create-user --user-pool-id <pool-id> --username alice
aws cognito-idp admin-set-user-password --user-pool-id <pool-id> \
  --username alice --password 'ChangeMe-123!' --permanent
aws cognito-idp list-users --user-pool-id <pool-id>

# Identity pool
aws cognito-identity create-identity-pool --identity-pool-name app \
  --allow-unauthenticated-identities \
  --cognito-identity-providers ProviderName=cognito-idp.us-east-1.amazonaws.com/<pool-id>,ClientId=<client-id>
aws cognito-identity list-identity-pools --max-results 10
```

## 最佳实践

- 注册/登录使用 user pool；仅在应用确实需要 AWS 凭证时使用 identity pool，保持两者职责清晰。
- 对敏感应用实施强密码策略和 MFA；优先 TOTP 而非短信。
- 限制应用客户端的 scope、来源和回调 URL；每个平台使用独立客户端。
- 在 identity pool 中使用基于属性的访问控制，最小化每个用户获得的权限。
- 除非访客确实需要受限访问，否则禁用未认证身份；绝不给未认证角色宽泛策略。
- 密钥（应用客户端密钥、IdP 凭证）存入 Secrets Manager 并轮换；监控登录失败。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 登录失败 | 检查用户状态（例如 FORCE_CHANGE_PASSWORD）、账户确认和 MFA 配置。 |
| 令牌被 API Gateway/ALB 拒绝 | 核对授权器/JWT 的 audience 是否与应用客户端 ID 匹配，令牌是否过期。 |
| identity pool 拿不到 AWS 凭证 | 确认 identity pool 已关联 user pool/IdP，角色映射和信任策略正确。 |
| 访客访问报错 | 核对未认证身份已启用，未认证角色具备所需的最小范围权限。 |
| 联合回调失败 | 检查允许的回调 URL、scope 和 IdP 配置（客户端 ID/密钥、元数据）。 |

## 配额

每区域 user pool 数、每池用户数、每池应用客户端数、每区域 identity pool 数以及 API 请求速率都有配额。以 Amazon Cognito 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Cognito？- 开发者指南](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)
- [Amazon Cognito user pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)
- [Amazon Cognito identity pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html)
- [Amazon Cognito 端点和配额](https://docs.aws.amazon.com/general/latest/gr/cognito_identity.html)
- [Amazon Cognito 定价](https://aws.amazon.com/cognito/pricing/)
- [AWS CLI：cognito-idp 和 cognito-identity 命令](https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/)
