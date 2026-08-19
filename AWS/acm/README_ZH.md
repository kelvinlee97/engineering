# AWS Certificate Manager (ACM) - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Certificate Manager（ACM）负责为 AWS 服务创建、存储和自动续期公有及私有 SSL/TLS X.509 证书。它可以直接签发证书，也可以导入第三方证书进行管理，支持单域名、多域名和通配符证书。

## 核心概念

- **证书**：绑定到一个或多个域名（SAN）的 X.509 证书。
- **验证**：DNS 验证（推荐）或电子邮件验证证明域名所有权；续期时会重新验证。
- **自动续期**：ACM 签发的证书由 ACM 自动续期和重新验证；导入的证书不会自动续期。
- **区域资源**：证书是区域性的；每个区域都需要申请/导入证书（CloudFront 需要 us-east-1）。
- **ACM Private CA**：为内部 PKI 使用场景签发私有证书。
- **导出**：AWS Private CA 签发的证书可导出用于 AWS 之外；ACM 签发的公有证书不可导出。

## 常用操作（AWS CLI）

```bash
# 使用 DNS 验证申请公有证书
aws acm request-certificate --domain-name example.com \
  --validation-method DNS \
  --subject-alternative-names "*.example.com"

# 查看状态并获取 DNS 验证记录
aws acm describe-certificate --certificate-arn <certificate-arn>

# 列出证书
aws acm list-certificates --certificate-statuses ISSUED

# 导入第三方证书
aws acm import-certificate --certificate fileb://cert.pem \
  --private-key fileb://private.key \
  --certificate-chain fileb://chain.pem

# 删除证书
aws acm delete-certificate --certificate-arn <certificate-arn>
```

## 最佳实践

- 使用 DNS 验证，续期无需手动处理邮件步骤即可自动完成。
- 在与使用资源相同的区域创建证书；CloudFront 使用 us-east-1。
- 谨慎使用通配符证书，将其限定在你拥有的域名范围内。
- AWS 服务（ALB、CloudFront、API Gateway）优先使用 ACM 签发的证书，续期全自动。
- EC2/本地服务器使用 ACME 自动化或 ACM Private CA，而不是 ACM 公有证书（不可导出）。
- 在过期前轮换导入的证书，并用 CloudWatch 监控过期时间。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 证书卡在待验证 | 核对 DNS 记录是否与显示的值一致，且 DNS 传播已完成。 |
| 续期失败 | 重新验证 DNS/邮件；确认域名仍解析到预期的验证记录。 |
| 服务找不到证书 | 确认证书与资源在同一区域（CloudFront：us-east-1）。 |
| 导入失败 | 检查 PEM 格式，确认私钥与证书匹配。 |
| 通配符未覆盖子域 | 确认证书覆盖了所需的确切名称（包括点号）。 |

## 配额

每账户每区域证书数、每证书域名数以及 ACM Private CA 配额都有限制。以 Service Quotas 控制台为准。用于 AWS 服务的 ACM 公有证书无额外 ACM 费用。

## 官方参考

- [什么是 AWS Certificate Manager？- ACM 用户指南](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)
- [AWS Certificate Manager 配额](https://docs.aws.amazon.com/acm/latest/userguide/acm-limits.html)
- [AWS Certificate Manager 定价](https://aws.amazon.com/certificate-manager/pricing/)
- [AWS CLI：acm 命令](https://docs.aws.amazon.com/cli/latest/reference/acm/)
