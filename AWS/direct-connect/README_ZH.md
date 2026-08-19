# AWS Direct Connect - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Direct Connect 在本地网络与 AWS 之间建立专用的私有网络连接。它绕过公共互联网，提供一致的网络体验，并在传输大量数据时可降低网络成本。连接在 AWS Direct Connect 站点以专线（dedicated）或托管（hosted）方式接入。

## 核心概念

- **专线连接（Dedicated connection）**：由 AWS 在 Direct Connect 站点提供的物理以太网端口（1、2、5 或 10 Gbps）；可通过链路聚合组（LAG，最多 4 条连接）提升容量。
- **托管连接（Hosted connection）**：由 AWS Direct Connect Delivery Partner 按增量提供容量（50 Mbps 至 10 Gbps）；向合作伙伴申请，可关联到 Direct Connect gateway。
- **虚拟接口（VIF）**：连接上的逻辑分段，使用 802.1Q VLAN 标签和 BGP 对等（支持 BGP MD5 认证，可选 BFD）。
  - **Private VIF**：连接到同一账户/区域的单个 VPC。
  - **Public VIF**：通过公有 IP 连接公有 AWS 服务（例如 S3、DynamoDB）。
  - **Transit VIF**：连接到 Direct Connect gateway，用于多个 VPC、账户和区域。
- **Direct Connect gateway**：全局资源，将 transit VIF 与跨账户、跨区域的 VPC 关联，包括到 VPC 的跨区域路由。
- **MACsec**：专线连接可选的 IEEE 802.1AE 物理层加密。

## 常用操作（AWS CLI）

```bash
# 列出连接和虚拟接口
aws directconnect describe-connections
aws directconnect describe-virtual-interfaces

# 创建虚拟接口（配置通过文件传入）
aws directconnect create-virtual-interface \
  --connection-id dxcon-0123456789abcdef0 \
  --new-virtual-interface-name prod-vif \
  --new-virtual-interface file://vif.json

# 查看 Direct Connect gateway 及其关联
aws directconnect describe-direct-connect-gateways
aws directconnect describe-direct-connect-gateway-associations \
  --direct-connect-gateway-id dxgw-0123456789abcdef0

# 列出 LAG
aws directconnect describe-lags
```

## 最佳实践

- 在至少两个 Direct Connect 站点使用冗余连接，并配置 BGP 实现自动故障切换。
- 多个 VPC、账户或区域时，优先使用 transit VIF 搭配 Direct Connect gateway。
- 持续监控 BGP 会话（状态、通告前缀），支持 BFD 时启用以获得更快收敛。
- 物理路径穿过不可信设施时，对专线使用 MACsec。
- 根据实测利用率确定带宽；高流量 S3/DynamoDB 可考虑 Public VIF 以降低互联网传输费用。
- 可用性要求高时，可结合 VPN 作为备份路径。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 连接状态 `down` | 确认交叉连接（cross-connect）已完成且站点设备已接入；端口持续 down 时联系 AWS/合作伙伴。 |
| BGP 无法建立 | 检查 VLAN、对端 IP、ASN、BGP MD5 密码以及使用的是否为正确的 VIF。 |
| VIF 状态 `pending` 或 `confirming` | 完成必要的验收（专线）或确认合作伙伴创建的托管 VIF。 |
| 流量未路由 | 核对 Direct Connect gateway 关联、路由传播和通告前缀。 |
| 延迟高于预期 | 确认流量实际走 Direct Connect（而非 VPN/互联网回退）。 |

## 配额

每账户连接、LAG、虚拟接口和 Direct Connect gateway 有配额；每连接的 VIF 数和每账户 gateway 数也有限制。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Direct Connect？- 用户指南](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)
- [AWS Direct Connect 虚拟接口](https://docs.aws.amazon.com/directconnect/latest/UserGuide/WorkingWithVirtualInterfaces.html)
- [AWS Direct Connect 配额](https://docs.aws.amazon.com/directconnect/latest/UserGuide/limits.html)
- [AWS Direct Connect 定价](https://aws.amazon.com/directconnect/pricing/)
- [AWS CLI：directconnect 命令](https://docs.aws.amazon.com/cli/latest/reference/directconnect/)
