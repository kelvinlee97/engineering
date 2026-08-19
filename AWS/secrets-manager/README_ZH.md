# AWS Secrets Manager - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Secrets Manager 帮助你管理、获取和轮换数据库凭证、应用凭证、OAuth token、API key 等机密，覆盖完整生命周期。密钥在运行时获取，而不是硬编码在应用代码里。

## 核心概念

- **机密（Secrets）**：带版本的机密值，使用暂存标签（`AWSCURRENT`、`AWSPREVIOUS`）。
- **自动轮换**：用 AWS Lambda 函数按计划轮换；长期凭证变成短期凭证。
- **加密**：默认用 AWS 托管密钥 `aws/secretsmanager`（免费）或客户 KMS key 加密。
- **服务边界建议**：AWS 凭证 → IAM；加密密钥 → KMS；SSH 密钥 → EC2 Instance Connect；证书 → ACM。
- **审计**：所有 API 调用作为管理事件记入 CloudTrail。

## 常用操作（AWS CLI）

```bash
# 创建与获取
aws secretsmanager create-secret --name prod/db-password \
  --secret-string '{"username":"admin","password":"ChangeMe123!"}'
aws secretsmanager get-secret-value --secret-id prod/db-password

# 更新版本
aws secretsmanager put-secret-value --secret-id prod/db-password \
  --secret-string '{"username":"admin","password":"NewPass456!"}'

# 轮换
aws secretsmanager rotate-secret --secret-id prod/db-password \
  --rotation-lambda-arn arn:aws:lambda:ap-southeast-1:123456789012:function:rotate-db \
  --rotation-rules AutomaticallyAfterDays=30

# 列出与查看
aws secretsmanager list-secrets
aws secretsmanager describe-secret --secret-id prod/db-password

# 删除（带恢复窗口）/ 恢复
aws secretsmanager delete-secret --secret-id prod/db-password --recovery-window-in-days 7
aws secretsmanager restore-secret --secret-id prod/db-password
```

## 最佳实践

- 数据库和应用凭证开启**自动轮换**（30-90 天）。
- IAM **最小权限**（`secretsmanager:GetSecretValue` 限定到具体 ARN）。
- 运行时用 SDK/CLI 获取密钥；不要明文放进配置文件或环境变量。
- 保留**删除恢复窗口**（7-30 天），除非密钥可丢弃。
- 需要时用**多区域复制**；用 CloudTrail 审计。
- 非密钥配置用 SSM Parameter Store；机密用 Secrets Manager。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 轮换失败 | 检查轮换 Lambda 的日志、权限和机密的轮换配置。 |
| `GetSecretValue` 被拒 | 核对调用者 IAM 策略和机密的资源策略。 |
| 找不到机密 | 检查区域、ARN/名称，以及是否处于删除恢复窗口。 |
| 误删 | 在恢复窗口内 `restore-secret`；否则重建。 |
| KMS 解密报错 | 确保机密的 KMS 密钥策略授予调用者 `kms:Decrypt`。 |

## 配额

每账户机密数量和轮换配置有配额；以 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Secrets Manager？- Secrets Manager 用户指南](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [AWS Secrets Manager 定价](https://aws.amazon.com/secrets-manager/pricing/)
- [AWS CLI：secretsmanager 命令](https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/)
