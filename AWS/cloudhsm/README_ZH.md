# AWS CloudHSM - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS CloudHSM 在 AWS 云中提供专用的单租户硬件安全模块（HSM）。HSM 是处理密码学操作并在防篡改硬件中安全存储密钥的计算设备。CloudHSM 让你完全控制密钥和算法，由 AWS 管理 HSM 的供给、备份、配置和维护。当你需要自有 HSM 时选择 CloudHSM；需要托管密钥服务时选择 AWS KMS。

## 核心概念

- **集群（Cluster）**：一个 VPC 中的一组 HSM；集群运行在 FIPS 模式（仅使用 FIPS 140-2/140-3 Level 3 验证的密钥和算法）或非 FIPS 模式（支持全部算法）。
- **单租户与私有**：HSM 专属于你的账户，数据平面端到端加密，AWS 无法看到你的密钥。
- **HSM 用户**：你在 HSM 内部管理用户和权限（在 IAM 之外）；IAM 控制 CloudHSM API，HSM 用户控制密钥。
- **客户端 SDK**：使用 PKCS #11、Java Cryptography Extension（JCE）、Cryptography API: Next Generation（CNG）或 Key Storage Provider（KSP）集成应用。
- **完整密钥控制**：生成、存储、导入、导出并使用对称密钥和非对称密钥对；控制算法。
- **备份**：AWS 自动执行 HSM 备份；你负责管理集群及其 HSM。

## 常用操作（AWS CLI）

```bash
# 创建集群和 HSM
aws cloudhsmv2 create-cluster --hsm-type hsm1.medium \
  --subnet-ids subnet-0123456789abcdef0
aws cloudhsmv2 describe-clusters
aws cloudhsmv2 create-hsm --cluster-id <cluster-id> \
  --availability-zone us-east-1a

# 初始化和管理集群
aws cloudhsmv2 initialize-cluster --cluster-id <cluster-id> \
  --signed-cert file://cluster-cert.pem \
  --trust-anchor file://customer-ca.pem
aws cloudhsmv2 list-tags --resource-id <cluster-id>

# 备份
aws cloudhsmv2 describe-backups --filters clusterIds=<cluster-id>
aws cloudhsmv2 restore-backup --backup-id <backup-id>

# 删除 HSM 或集群
aws cloudhsmv2 delete-hsm --cluster-id <cluster-id> --hsm-id <hsm-id>
aws cloudhsmv2 delete-cluster --cluster-id <cluster-id>
```

## 最佳实践

- 在不同可用区至少部署两个 HSM 实现高可用。
- 仅在需要 FIPS 验证时选择 FIPS 模式；工作负载需要其他算法时使用非 FIPS 模式。
- 职责分离：IAM 管理 CloudHSM API，HSM 用户管理密钥，两边都遵循最小权限。
- 自动化备份，并在依赖之前演练恢复到新集群。
- 需要托管密钥服务时优先 KMS；需要单租户 HSM 或 PKCS #11、JCE、CNG/KSP 等标准时使用 CloudHSM。
- 监控集群健康和 HSM 数量；HSM 放在私有子网，安全组仅允许应用 CIDR 访问。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 集群初始化失败 | 核对签名证书是否与集群匹配，trust anchor 是否为有效 CA 证书。 |
| 客户端无法连接 | 检查安全组、客户端 SDK 配置，以及 HSM 是否处于 active 状态。 |
| HSM 用户登录被拒 | 确认 HSM 中存在该用户，并了解密码策略/重试限制。 |
| 备份恢复慢 | 在同一区域恢复到新集群；跨区域恢复有其他约束。 |
| 混淆 KMS/CloudHSM | KMS 是全托管；CloudHSM 需要你管理 HSM 用户和应用集成。 |

## 配额

每集群 HSM 数、每账户每区域集群数以及备份数量有限制。以 AWS CloudHSM 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS CloudHSM？- 用户指南](https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html)
- [AWS CloudHSM 配额](https://docs.aws.amazon.com/cloudhsm/latest/userguide/limits.html)
- [AWS CloudHSM 定价](https://aws.amazon.com/cloudhsm/pricing/)
- [AWS CLI：cloudhsmv2 命令](https://docs.aws.amazon.com/cli/latest/reference/cloudhsmv2/)
