# AWS Global Accelerator - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Global Accelerator 为全球用户提升互联网应用程序的可用性和性能。它提供静态任播 IP 地址，并基于健康状态、客户端位置和你的策略，通过 AWS 全球网络将流量路由到最优的区域端点。

## 核心概念

- **Accelerator**：引导流量的全局资源；提供两个静态 IPv4 地址（双栈为四个），在加速器整个生命周期内保持不变。
- **Listener**：在指定端口/协议（TCP/UDP）上接收流量并路由到端点组。
- **Endpoint group**：区域端点组；根据健康状态和权重切换流量。
- **Endpoints**：一个或多个区域中的 NLB、ALB、EC2 实例或弹性 IP。
- **自定义路由加速器**：将用户映射到特定目标（VPC 子网私有 IP），而不是负载均衡端点。
- **健康检查**：Global Accelerator 对端点健康变化即时响应；支持 Application Recovery Controller 可用区切换。

## 常用操作（AWS CLI）

```bash
# 创建加速器
aws globalaccelerator create-accelerator --name prod --ip-address-type IPV4

# 添加监听器（443/TCP）
aws globalaccelerator create-listener --accelerator-arn <accelerator-arn> \
  --port-ranges From=443,To=443 --protocol TCP

# 创建带 ALB 端点的端点组
aws globalaccelerator create-endpoint-group --listener-arn <listener-arn> \
  --endpoint-group-region us-east-1 \
  --endpoint-configurations EndpointId=arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/web/1234567890abcdef,Weight=100

# 列出和查看
aws globalaccelerator list-accelerators
aws globalaccelerator describe-accelerator --accelerator-arn <accelerator-arn>
aws globalaccelerator list-listeners --accelerator-arn <accelerator-arn>
```

## 最佳实践

- 对全球性、延迟敏感或可用性关键的应用程序使用 Global Accelerator，而不是仅依赖 DNS 故障切换。
- 后端使用 ALB/NLB，保持 DNS TTL 较短；基础设施变化时更新加速器端点。
- 在多个区域配置端点组并使用权重，实现主备或双活路由。
- 使用健康检查并演练故障切换；注意 VPC Block Public Access 设置。
- 用 IAM/标签策略保护加速器不被删除；加速器删除后静态 IP 将丢失。
- 游戏/实时应用需要绑定特定目标时，使用自定义路由加速器。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 客户端无法连接 | 检查监听器端口/协议、端点组健康状态以及端点是否接受流量。 |
| 流量走向不健康区域 | 检查端点健康状态和权重，确认健康检查通过。 |
| 静态 IP 丢失 | 静态 IP 仅在加速器删除时释放；避免删除生产加速器。 |
| 端点不可达 | 核对安全组/NACL 是否允许来自 Global Accelerator 的流量（使用 AWS 公布的地址段）。 |
| 性能未提升 | 确认 DNS 指向加速器静态 IP，客户端到达最近的边缘节点。 |

## 配额

每账户加速器、监听器、端点组和端点数都有配额。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Global Accelerator？- 开发者指南](https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html)
- [AWS Global Accelerator 配额](https://docs.aws.amazon.com/global-accelerator/latest/dg/limits.html)
- [AWS Global Accelerator 定价](https://aws.amazon.com/global-accelerator/pricing/)
- [AWS CLI：globalaccelerator 命令](https://docs.aws.amazon.com/cli/latest/reference/globalaccelerator/)
