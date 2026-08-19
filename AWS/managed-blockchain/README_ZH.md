# Amazon Managed Blockchain（AMB）- Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Managed Blockchain（AMB）提供对公共区块链网络（Ethereum 和 Bitcoin）的访问，并支持用 Hyperledger Fabric 框架创建私有、许可制区块链网络。AMB Access 为公共节点提供全托管、专用（单租户）和无服务器多租户 API 操作；需要访问控制的使用场景可选择全托管私有网络。

## 核心概念

- **AMB Access**：标准化的区块链基础设施 API 访问。
  - **公共网络**：Ethereum 和 Bitcoin 节点，支持多租户 API 访问或专用节点。
  - **私有网络**：几分钟内创建的许可制 Hyperledger Fabric 网络，包含成员和 peer 节点。
- **网络（Network）**：私有区块链网络（Fabric）或公共网络成员资格。
- **成员（Member）**：Fabric 网络中的组织；成员运行 peer 节点，并可发起提案（chaincode、成员资格）进行投票。
- **Peer 节点**：承载账本和 chaincode 的 Fabric 组件；多 peer 实现高可用。
- **Accessor 与令牌**：对 Ethereum 节点的令牌访问（accessor 是包含令牌访问信息的容器）。
- **用途**：联盟网络、供应链、金融应用，以及用模拟成员搭建的开发/测试网络。

## 常用操作（AWS CLI）

```bash
# 创建 Fabric 网络和成员
aws managedblockchain create-network --framework HYPERLEDGER_FABRIC \
  --framework-version 2.2 --voting-policy file://voting.json \
  --member-configuration file://member.json
aws managedblockchain create-member --network-id <network-id> \
  --member-configuration file://member.json

# 节点和 accessor
aws managedblockchain create-node --network-id <network-id> \
  --member-id <member-id> --node-configuration file://node.json
aws managedblockchain create-accessor --accessor-type BILLING_TOKEN \
  --accessor-name ethereum-mainnet

# 查看资源
aws managedblockchain list-networks
aws managedblockchain list-members --network-id <network-id>
aws managedblockchain list-nodes --network-id <network-id> --member-id <member-id>
```

## 最佳实践

- 按需求选择部署模式：公共 API 访问（AMB Access）、专用节点，或需要许可制场景的私有 Fabric 网络。
- Fabric 网络中跨可用区运行多个 peer 节点实现高可用。
- 谨慎管理成员资格：提案和投票控制谁能加入和改变网络。
- 用 IAM 和令牌保护访问；Ethereum 令牌要轮换和保护。
- 监控节点健康和账本活动，失败时设置告警。
- 公共网络使用按吞吐需求选择 API 规模，用无服务器多租户访问控制成本。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 节点不可用 | 检查网络/成员状态、节点健康及 IAM 权限。 |
| 令牌访问被拒 | 核对 accessor 存在，令牌对目标网络有效。 |
| Chaincode 提案失败 | 确认投票策略阈值和成员权限。 |
| Fabric 网络创建失败 | 校验成员配置（管理员用户、密码策略、实例类型）。 |
| API 被限流 | 审查请求速率并按需提高配额。 |

## 配额

每账户网络、成员、节点和 accessor 数量有限制；框架版本在网络创建时固定。以 Amazon Managed Blockchain 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Managed Blockchain？- 开发者指南](https://docs.aws.amazon.com/managed-blockchain/latest/hyperledger-fabric-dev/what-is-managed-blockchain.html)
- [Amazon Managed Blockchain 端点和配额](https://docs.aws.amazon.com/general/latest/gr/managedblockchain.html)
- [Amazon Managed Blockchain 定价](https://aws.amazon.com/managed-blockchain/pricing/)
- [AWS CLI：managedblockchain 命令](https://docs.aws.amazon.com/cli/latest/reference/managedblockchain/)
