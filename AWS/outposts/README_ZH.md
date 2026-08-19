# AWS Outposts - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Outposts 把 AWS 基础设施、服务、API 和工具带到你的现场。Outpost 是安装在你站点的一组 AWS 计算和存储容量，由 AWS 作为某区域的一部分运营和管理。你在本地使用与区域相同的 API 和控制台，获得低延迟和本地数据处理。

## 核心概念

- **Outpost 站点**：安装 Outpost 的客户管理物理位置。
- **Outposts racks**：行业标准 42U 机架，含服务器、交换机和线缆，由 AWS 拥有和管理。
- **Outposts servers**：1U/2U 服务器，适合空间有限或容量较小的站点。
- **ACE 机架**：四个及以上计算机架部署时要求的聚合/核心/边缘机架。
- **Service link**：Outpost 与其关联区域之间的网络路由。
- **本地网关（LGW）**：把 Outposts rack 资源连接到本地网络的逻辑路由器。
- **Outpost 子网**：在 Outpost 上创建子网并启动本地资源（EC2、EBS、ECS、EKS、RDS、EMR、ElastiCache、S3 on Outposts、ALB）。
- **所有权与管理**：AWS 负责交付、安装、监控、打补丁和维护硬件。

## 常用操作（AWS CLI）

```bash
# 创建站点和 Outpost
aws outposts create-site --name dc-south --country-code MY
aws outposts create-outpost --name prod-outpost --site-id <site-id> \
  --availability-zone ap-southeast-1a --availability-zone-id apse1-az4

# 列出和查看
aws outposts list-outposts
aws outposts get-outpost --outpost-id <outpost-id>
aws outposts list-sites

# 容量管理（查看/更新）
aws outposts get-outpost-instance-types --outpost-id <outpost-id>
aws outposts update-outpost --outpost-id <outpost-id> --name prod-outpost-v2
```

## 最佳实践

- 下单前验证场地条件（电力、散热、空间、网络），并规划到区域的 service link 带宽。
- 选对形态：容量大用 racks，小站点用 servers；扩展到四个及以上计算机架时安装 ACE 机架。
- 设计 VPC/子网架构，让 Outpost 资源既隔离又与区域连通。
- 延迟敏感和数据驻留场景用本地计算/存储；备份和快照同步到区域。
- 监控 Outpost 容量和利用率；与 AWS 一起规划硬件增长。
- 把 Outpost 视为区域的延伸：使用同样的 IAM、安全组和监控工具。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 实例启动失败 | 核对 Outpost 容量、子网放置和实例类型在 Outpost 上的可用性。 |
| 到区域延迟高 | 检查 service link 带宽和本地网关路由。 |
| 本地存储打满 | 监控 EBS/S3 on Outposts 容量，把冷数据迁到区域。 |
| 硬件问题 | AWS 负责监控和管理硬件；开支持单申请更换。 |
| 网络问题 | 核对 LGW 配置和本地路由/对等。 |

## 配额

Outpost 容量、实例类型、每站点机架数和受支持服务取决于区域与订单配置。以 AWS Outposts 文档和 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 AWS Outposts？](https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html)
- [AWS Outposts 产品页](https://aws.amazon.com/outposts/)
- [AWS Outposts 定价](https://aws.amazon.com/outposts/pricing/)
- [AWS CLI：outposts 命令](https://docs.aws.amazon.com/cli/latest/reference/outposts/)
