# AWS SDKs and Tools - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS SDK 是各语言的 AWS 服务 API 客户端库：Python（boto3）、Java、JavaScript（v3）、Go、.NET、Ruby、PHP、C++ 等。SDK 负责请求签名、重试和错误映射。AWS SDKs and Tools 参考指南统一说明所有 SDK 和工具的共享配置、凭据和维护策略。

## 核心概念

- **凭据解析**：与 CLI 相同的链式顺序 - 环境变量、共享 config/credentials 文件、IAM 角色、SSO、容器凭据。
- **Signature Version 4**：SDK 对每个请求签名；支持 STS 临时凭据。
- **重试与超时**：SDK 默认对瞬时故障重试；按 SDK 配置重试模式（`standard`、`adaptive`、`legacy`）。
- **身份提供方**：EC2 实例角色、EKS IRSA、ECS 任务角色、Lambda 执行角色、IAM Identity Center SSO。
- **AWS Common Runtime（CRT）**：多个 SDK 共享的库，提供 HTTP/2、事件流、重试和校验和实现。
- **维护策略**：AWS 对 SDK 主版本有明确支持窗口；到期前要升级。

## 常见配置（共享配置）

```ini
# ~/.aws/config
[default]
region = us-east-1
output = json

[profile dev]
role_arn = arn:aws:iam::123456789012:role/Developer
source_profile = default

[profile sso-dev]
sso_session = my-sso
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
region = ap-southeast-1

[sso-session my-sso]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
```

```bash
# 环境变量
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...        # 仅临时凭据
export AWS_DEFAULT_REGION=us-east-1
```

## 最佳实践

- 优先 IAM 角色而非静态密钥：EC2 实例配置、EKS IRSA、ECS/Lambda 执行角色或 SSO。
- 无法避免静态密钥时用短时 STS 凭据（CI/CD 用 Secrets Manager 保管）。
- 对延迟敏感路径显式设置超时、重试模式和最大重试次数。
- 按需开启 SDK 日志/遥测；绝不记录凭据或签名载荷。
- 固定 SDK 版本并关注维护策略；先在预发环境测试升级。
- 用 SDK 自带的 paginator/waiters，而不是自己写轮询。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 代码里找不到凭据 | 检查环境变量、共享文件和角色配置；核对解析顺序。 |
| 间歇性失败 | 配置重试模式和指数退避；检查限流和配额。 |
| 时钟偏移/签名错误 | 确认系统时间已通过 NTP 同步。 |
| 区域端点不对 | 在配置/凭据链或客户端里设置区域。 |
| SDK API 已废弃 | 按 SDK 维护策略迁移到当前主版本。 |

## 配额

SDK 本身没有配额；服务 API 和 IAM 策略决定代码能做什么。以 Service Quotas 控制台各服务当前值为准。

## 官方参考

- [AWS SDKs and Tools 参考指南](https://docs.aws.amazon.com/sdkref/latest/guide/overview.html)
- [AWS SDK for Python（boto3）](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Tools to Build on AWS](https://aws.amazon.com/developer/tools/)
