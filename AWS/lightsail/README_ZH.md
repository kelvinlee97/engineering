# Amazon Lightsail - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Lightsail 是启动和管理虚拟私有服务器及 Web 应用最简单的 AWS 服务，采用低且可预测的月度定价。一个控制台内集成实例、容器、托管数据库（MySQL/PostgreSQL）、负载均衡器、CDN 分发、块/对象存储、静态 IP、DNS 和快照。

## 核心概念

- **实例（Instance）**：带一键启动 blueprint（OS、WordPress、LAMP、Nginx 等）和内建防火墙的虚拟私有服务器。
- **Blueprint 与 bundle**：预配置的 OS/应用镜像和固定实例规格（内存、vCPU、存储、流量）。
- **托管数据库**：独立于实例伸缩的 MySQL 或 PostgreSQL。
- **容器服务**：运行容器化应用，自带负载均衡和 HTTPS。
- **负载均衡器**：跨实例分发流量，支持健康检查和会话保持。
- **CDN 分发**：基于 CloudFront 的内容分发，降低延迟。
- **块/对象存储**：挂到实例的 SSD 磁盘，以及面向静态内容的 S3 兼容桶。
- **快照**：实例/磁盘备份，可基于快照创建新资源。
- **VPC 对等**：把 Lightsail 资源连接到更广的 AWS VPC 生态。

## 常用操作（AWS CLI）

```bash
# 创建实例（WordPress blueprint）
aws lightsail create-instances --instance-names web-1 \
  --blueprint-id wordpress --bundle-id nano_2_0 \
  --availability-zone ap-southeast-1a

# 列出实例和详情
aws lightsail get-instances
aws lightsail get-instance --instance-name web-1

# 网络
aws lightsail open-instance-public-ports --instance-name web-1 \
  --port-info fromPort=443,toPort=443,protocol=HTTPS
aws lightsail allocate-static-ip --static-ip-name web-ip
aws lightsail attach-static-ip --static-ip-name web-ip --instance-name web-1

# 快照和数据库
aws lightsail create-instance-snapshot --instance-name web-1 --instance-snapshot-name web-1-backup
aws lightsail create-relational-database --relational-database-name app-db \
  --relational-database-blueprint-id mysql_8_0 --relational-database-bundle-id micro_2_0
```

## 最佳实践

- 简单、可预测的工作负载用 Lightsail；需要高级功能或深度 AWS 集成时迁移到 EC2/RDS。
- 启用内建防火墙，只开放必要端口；变更前做快照。
- 用托管数据库，而不是在实例上自建 MySQL/PostgreSQL。
- 生产实例前面加负载均衡器（HTTPS），静态内容用 CDN。
- 需要其他 AWS 服务时做 VPC 对等；稳定 DNS 用静态 IP。
- 在 Lightsail 控制台/CloudWatch 监控指标，设置实例健康告警。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 实例无法访问 | 检查实例状态、防火墙规则和静态 IP 挂载。 |
| 网站慢 | 检查 bundle 规格、加负载均衡器，或用 CDN 分发。 |
| 数据库连接失败 | 检查数据库端点、凭据和公网/私网访问设置。 |
| 快照恢复问题 | 从快照创建新实例，验证数据和配置。 |
| 流量超额 | 监控月度流量额度，用 CDN 和压缩。 |

## 配额

实例、数据库、负载均衡器、静态 IP 和流量额度按账号和套餐有限制。以 Lightsail 定价页和 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 Amazon Lightsail？](https://docs.aws.amazon.com/lightsail/latest/userguide/what-is-amazon-lightsail.html)
- [Amazon Lightsail 定价](https://aws.amazon.com/lightsail/pricing/)
- [AWS CLI：lightsail 命令](https://docs.aws.amazon.com/cli/latest/reference/lightsail/)
