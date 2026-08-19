# AWS Directory Service - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Directory Service 提供托管目录选项，让 Microsoft Active Directory（AD）和 LDAP 与 AWS 服务及工作负载配合使用。你可以根据需求在云中运行全托管的 Microsoft AD、将 AWS 应用连接到现有本地 AD，或使用低成本的 AD 兼容目录。

## 核心概念

- **AWS Managed Microsoft AD**：由 AWS 管理的真实 Microsoft Windows Server Active Directory；支持 AD 感知应用、EC2 加域、RDS for SQL Server、WorkSpaces、组策略、schema 扩展、LDAPS、MFA，以及与本地 AD 的信任关系。
  - **Standard 版**：适合中小型组织，约最多 30,000 个目录对象。
  - **Enterprise 版**：适合大型组织，约最多 500,000 个目录对象。
  - **Hybrid**：将现有自管理 AD 扩展到 AWS 云。
- **AD Connector**：代理服务，让兼容的 AWS 应用（WorkSpaces、EC2 Windows 加域、控制台登录）针对现有本地 AD 认证，无需目录同步或联邦基础设施。
- **Simple AD**：基于 Samba 4 的低成本 AD 兼容目录，支持基本的用户/组管理、加域、基于 Kerberos 的 SSO 和组策略；不支持 MFA、信任、schema 扩展、LDAPS 或 RDS SQL Server。
- **托管运维**：AWS 为 Managed Microsoft AD 和 Simple AD 提供监控、每日快照和恢复。
- **身份选项**：需要大规模 SaaS 用户目录并支持社交身份时，AWS 推荐 Amazon Cognito。

## 常用操作（AWS CLI）

```bash
# 创建目录
aws ds create-microsoft-ad --name corp.example.com \
  --password '<admin-password>' --edition Enterprise \
  --vpc-settings VpcId=vpc-0123456789abcdef0,SubnetIds=subnet-0123456789abcdef0,subnet-1234567890abcdef0
aws ds create-connector --name onprem-connector \
  --connect-settings file://connector.json
aws ds create-simple-ad --name small.example.com \
  --password '<admin-password>' --size Small \
  --vpc-settings VpcId=vpc-0123456789abcdef0,SubnetIds=subnet-0123456789abcdef0,subnet-1234567890abcdef0

# 查看和删除
aws ds describe-directories --directory-ids <directory-id>
aws ds get-directory-limits
aws ds delete-directory --directory-id <directory-id>
```

## 最佳实践

- 需要真实 AD 功能、RDS SQL Server、信任或 LDAPS 时选择 Managed Microsoft AD；仅需基础低成本场景用 Simple AD。
- 身份源必须保留在本地且只需要 AWS 应用认证时，使用 AD Connector。
- 跨多个可用区部署域控制器（Managed Microsoft AD 自动完成），并监控目录健康。
- 保护管理员凭证、实施密码策略；面向互联网的访问按需启用 MFA。
- 通过 Systems Manager 或目录感知启动设置将 EC2 实例加域；与本地一致地应用组策略。
- 监控快照并在依赖前演练目录恢复。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 加域失败 | 检查到目录的 DNS 解析、安全组规则（TCP/UDP 389、445、88、464、3268）和凭证。 |
| 用户无法认证 | 核对目录状态为 ACTIVE、信任（如有）已配置、密码策略正确。 |
| LDAPS 不工作 | 确保已导入 CA 证书且 LDAPS 端口（636）可达。 |
| AD Connector 报错 | 确认本地 AD 中的服务账户具备所需读取权限，且网络连通。 |
| RDS SQL Server 加域失败 | 使用 AWS Managed Microsoft AD；Simple AD 和 AD Connector 不兼容 RDS SQL Server。 |

## 配额

每账户每区域目录数、按版本的目录对象数以及域控制器数量有限制。以 AWS Directory Service 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Directory Service？- 管理指南](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/what_is.html)
- [AWS Directory Service 配额](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/limits.html)
- [AWS Directory Service 定价](https://aws.amazon.com/directoryservice/pricing/)
- [AWS CLI：ds 命令](https://docs.aws.amazon.com/cli/latest/reference/ds/)
