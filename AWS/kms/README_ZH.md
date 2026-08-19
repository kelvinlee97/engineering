# AWS KMS - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Key Management Service（AWS KMS）让你创建并控制用于加密和签名的密钥。KMS key 由通过 FIPS 140-3 安全级别 3 验证的硬件安全模块（HSM）保护，且永远不会以明文形式离开服务。

## 核心概念

- **KMS key**：对称、非对称和 HMAC 密钥；在 KMS 内部完成创建、管理、使用和删除。
- **密钥策略与授权（Grants）**：控制谁能使用和管理密钥。
- **别名（Alias）**：友好名称（`alias/my-key`）映射到密钥；应用应引用别名。
- **轮换**：对称密钥默认每年自动轮换；非对称和 HMAC 密钥支持按需轮换。
- **数据密钥与信封加密**：`GenerateDataKey` 返回明文数据密钥和加密副本；用数据密钥在本地加密数据。
- **加密上下文（Encryption context）**：绑定到加密操作的附加认证数据。
- **集成**：S3、EBS、RDS 等服务的 SSE-KMS。

## 常用操作（AWS CLI）

```bash
# 创建密钥和别名
aws kms create-key --description "app encryption key"
aws kms create-alias --alias-name alias/my-key --target-key-id <key-id>

# 加密 / 解密（二进制输入用 fileb://）
aws kms encrypt --key-id alias/my-key --plaintext fileb://secret.bin \
  --encryption-context env=prod --output text --query CiphertextBlob > secret.enc
aws kms decrypt --ciphertext-blob fileb://secret.enc \
  --encryption-context env=prod --output text --query Plaintext > secret.bin

# 信封加密（数据密钥）
aws kms generate-data-key --key-id alias/my-key --key-spec AES_256 \
  --output json > data-key.json

# 轮换与删除
aws kms enable-key-rotation --key-id <key-id>
aws kms schedule-key-deletion --key-id <key-id> --pending-window-in-days 7

# 审计
aws kms list-keys
aws kms describe-key --key-id alias/my-key
```

## 最佳实践

- 大数据或本地数据用**信封加密**（数据密钥）；不要直接用 KMS 加密大对象。
- 用**别名**引用密钥，轮换不影响应用。
- 密钥策略/授权**最小权限**；按环境和团队分开密钥。
- 开启**轮换**，用**加密上下文**把密文绑定到用途。
- 用 **CloudTrail** 审计所有密钥使用；对异常的 `kms:Decrypt` 告警。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| `kms:Decrypt` 的 `AccessDenied` | 检查密钥策略和授权；核对调用者 IAM 权限。 |
| `InvalidCiphertextBlob` | 确认使用正确的密钥和加密上下文；密文与区域、密钥绑定。 |
| 密钥被删除 | 待删除期过后不可恢复；从备份恢复或重新加密。 |
| 限流 | KMS 请求配额设计上较低；指数退避重试或减少调用量。 |
| 找不到密钥 | 核对别名/密钥 ARN 和区域；别名和密钥是区域性的。 |

## 配额

每区域每秒请求配额（例如对称密钥 encrypt/decrypt 默认 5,500 次/秒，可调）。以 Service Quotas 为准。

## 官方参考

- [AWS Key Management Service - KMS 开发者指南](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
- [AWS KMS 定价](https://aws.amazon.com/kms/pricing/)
- [AWS CLI：kms 命令](https://docs.aws.amazon.com/cli/latest/reference/kms/)
