# AWS Transfer Family - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Transfer Family 是全托管服务，通过 SFTP、FTPS、FTP、AS2 和浏览器 Web 传输，将文件移入/移出 AWS 存储（Amazon S3 和 Amazon EFS）。你保留现有客户端、认证和防火墙配置；AWS 托管服务器并自动扩展。只为使用量付费。

## 核心概念

- **服务器（Server）**：托管端点（公有或 VPC），支持一种或多种协议（SFTP v3、FTPS、FTP、AS2）；将主机名和 DNS 关联到端点。
- **存储**：数据存放在 Amazon S3（数据湖、第三方上传、分发）或 Amazon EFS（内容管理、供应链、Web 服务）。
- **身份提供方**：服务托管用户、AWS Directory Service，或自定义身份提供方（Lambda 支撑、API Gateway）用于用户认证。
- **Web apps**：面向 S3 的托管浏览器传输界面，集中管理访问。
- **托管工作流（MFTW）**：无服务器、自动化处理上传文件（复制、打标签、扫描、过滤、压缩/解压、加密/解密），端到端可见。
- **AS2**：面向合规敏感工作流（供应链、支付、ERP/CRM 集成）的 B2B 协议。
- **端口**：FTP/FTPS 数据连接使用 8192-8200 端口范围。

## 常用操作（AWS CLI）

```bash
# 创建服务器和用户
aws transfer create-server --protocols SFTP --identity-provider-type SERVICE_MANAGED \
  --endpoint-type PUBLIC --region us-east-1
aws transfer create-user --server-id <server-id> --user-name uploader \
  --role arn:aws:iam::123456789012:role/transfer-role \
  --home-directory /bucket/home/uploader

# 列出和管理
aws transfer list-servers
aws transfer describe-server --server-id <server-id>
aws transfer update-user --server-id <server-id> --user-name uploader \
  --role arn:aws:iam::123456789012:role/transfer-role
aws transfer delete-server --server-id <server-id>
```

## 最佳实践

- 私有传输使用 VPC 端点，安全组只放开所用协议的端口。
- 强制强认证：服务托管加强密码，支持的场景启用 MFA，或集成 Directory Service/自定义 IdP。
- 用户 IAM 角色限定主目录和最小权限 S3/EFS 访问；用逻辑目录隔离。
- 启用 CloudTrail 和 CloudWatch 审计传输活动；用托管工作流自动处理文件。
- 合规 B2B 工作流用 AS2；广范围业务用户访问 S3 用 Web apps。
- 监控服务器健康和传输指标；对登录失败和传输错误设置告警。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 客户端无法连接 | 检查端点类型（公有/VPC）、安全组、DNS 和协议配置。 |
| 登录被拒 | 核对身份提供方配置、用户名/密码和用户 IAM 角色。 |
| 上传失败 | 检查用户主目录、S3/EFS 权限和服务器角色。 |
| FTP/FTPS 数据连接失败 | 确保数据连接端口范围 8192-8200 已开放。 |
| 托管工作流未运行 | 检查工作流步骤配置、IAM 角色和执行日志。 |

## 配额

每账户服务器、用户、托管工作流和 API 请求速率有限制；FTP/FTPS 数据连接使用固定端口范围。以 AWS Transfer Family 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Transfer Family？- 用户指南](https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html)
- [AWS Transfer Family 端点和配额](https://docs.aws.amazon.com/general/latest/gr/transfer.html)
- [AWS Transfer Family 定价](https://aws.amazon.com/aws-transfer-family/pricing/)
- [AWS CLI：transfer 命令](https://docs.aws.amazon.com/cli/latest/reference/transfer/)
