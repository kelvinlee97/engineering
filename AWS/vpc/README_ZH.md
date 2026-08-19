# Amazon VPC - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Virtual Private Cloud（Amazon VPC）让你在自定义的逻辑隔离虚拟网络中启动 AWS 资源。每个 AWS 区域都有一个默认 VPC，可直接使用。VPC 本身不收费；部分组件（如 NAT 网关）收费。

## 核心概念

- **VPC**：带 IP CIDR 网段（IPv4 和/或 IPv6）的虚拟网络。
- **子网（Subnet）**：VPC 内的 IP 地址范围；一个子网只属于一个可用区。
- **路由表**：决定子网或网关的流量去向。
- **网关与端点**：互联网网关提供公网访问；VPC 端点提供访问 AWS 服务的私有通道；NAT 网关让私有子网只出不进地上网。
- **对等连接与 Transit Gateway**：连接多个 VPC；Transit Gateway 作为中心枢纽。
- **VPN / Direct Connect**：连接 VPC 与本地网络。
- **安全**：安全组（有状态、实例级）和网络 ACL（无状态、子网级）；VPC Flow Logs 记录 IP 流量元数据。

## 常用操作（AWS CLI）

```bash
# VPC 与子网
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.1.0/24 --availability-zone ap-southeast-1a

# 互联网访问
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --internet-gateway-id igw-xxx --vpc-id vpc-xxx
aws ec2 create-route-table --vpc-id vpc-xxx
aws ec2 create-route --route-table-id rtb-xxx --destination-cidr-block 0.0.0.0/0 --gateway-id igw-xxx
aws ec2 associate-route-table --route-table-id rtb-xxx --subnet-id subnet-xxx

# 私有子网出网（NAT 网关）
aws ec2 create-nat-gateway --subnet-id subnet-xxx --allocation-id eipalloc-xxx

# 私有访问 AWS 服务（VPC 端点）
aws ec2 create-vpc-endpoint --vpc-id vpc-xxx --service-name com.amazonaws.ap-southeast-1.s3

# 可观测性
aws ec2 create-flow-logs --resource-type VPC --resource-id vpc-xxx \
  --traffic-type ALL --log-group-name my-flow-logs --deliver-logs-permission-arn arn:aws:iam::123456789012:role/flowlogs
```

## 最佳实践

- 提前规划 CIDR，避免 VPC 之间及与本地网络重叠；日后要对等连接时尤其注意。
- 使用多个可用区；数据库和内部服务放在**私有子网**。
- 访问 AWS 服务优先用 **VPC 端点**（S3/DynamoDB 用网关端点，其他用接口端点）而不是 NAT。
- 开启 **VPC Flow Logs** 并分析，用于安全和排障。
- 安全组默认拒绝；安全组管实例级、NACL 管子网级护栏。
- 多个 VPC 互联时用 Transit Gateway 做中心枢纽。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 实例无法访问互联网 | 检查路由表（默认路由指向 IGW）、安全组出站、NACL、是否分配了公网 IPv4。 |
| 私有子网实例无法上网 | 确认 NAT 网关在公有子网且有弹性 IP，路由存在。 |
| 连不上私有子网的 RDS | 检查 RDS 安全组来源（应用安全组/CIDR）和子网路由。 |
| AWS 服务访问被拒 | 添加 VPC 端点及其安全组；核对端点策略。 |
| DNS 解析失败 | 检查 VPC DNS 设置（`enableDnsSupport`、`enableDnsHostnames`）和 Resolver 规则。 |

## 配额

默认配额：每区域 5 个 VPC（可调）、每个 VPC 200 个子网。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon VPC？- Amazon VPC 用户指南](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [Amazon VPC 定价](https://aws.amazon.com/vpc/pricing/)
- [AWS CLI：ec2 命令（VPC）](https://docs.aws.amazon.com/cli/latest/reference/ec2/)
