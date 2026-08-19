# Elastic Load Balancing - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Elastic Load Balancing（ELB）自动把入站流量分发到多个目标（EC2 实例、容器、IP 地址、Lambda 函数），可跨一个或多个可用区，只把流量路由到健康目标。容量自动扩展。

## 负载均衡器类型

- **Application Load Balancer（ALB）**：第 7 层 HTTP/HTTPS；支持基于路径/主机的路由、WAF 集成、Lambda 目标、WebSocket。
- **Network Load Balancer（NLB）**：第 4 层 TCP/UDP；超高性能、静态 IP、TLS 终止；适合极致吞吐。
- **Gateway Load Balancer（GWLB）**：第 3 层；把流量路由给第三方虚拟设备。
- **Classic Load Balancer**：上一代产品；建议迁移到 ALB/NLB。

## 核心概念

- **监听器（Listener）**：检查连接请求（协议/端口）并路由。
- **目标组（Target group）**：向注册目标路由请求，带健康检查。
- **健康检查**：可配置路径/端口；只有健康目标接收流量。
- **跨可用区负载均衡**：跨 AZ 均匀分发。
- **TLS 终止**：用 ACM 证书在负载均衡器上卸载加密。
- **访问日志**：把详细请求数据记录到 S3。

## 常用操作（AWS CLI）

```bash
# ALB
aws elbv2 create-load-balancer --name my-alb --type application \
  --subnets subnet-xxx subnet-yyy --security-groups sg-xxx

# 目标组与注册
aws elbv2 create-target-group --name my-tg --protocol HTTP --port 80 \
  --vpc-id vpc-xxx --health-check-path /health
aws elbv2 register-targets --target-group-arn <tg-arn> \
  --targets Id=i-0123456789abcdef0

# 监听器
aws elbv2 create-listener --load-balancer-arn <alb-arn> \
  --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn=<tg-arn>

# 查看
aws elbv2 describe-load-balancers
aws elbv2 describe-target-health --target-group-arn <tg-arn>

# 删除
aws elbv2 delete-load-balancer --load-balancer-arn <alb-arn>
```

## 最佳实践

- HTTP(S) 工作负载选 **ALB**；TCP/UDP 或静态 IP 需求选 **NLB**。
- 目标分布在**多个可用区**；开启跨可用区负载均衡。
- 健康检查（路径、间隔、阈值）要真实反映应用健康。
- 用 **ACM** 证书在负载均衡器终止 TLS。
- 开启**访问日志**到 S3，用 CloudWatch 监控；ALB 集成 **AWS WAF**。
- 配合 **Auto Scaling**，新启动的实例自动注册。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| `503 Service Unavailable` | 没有健康目标：检查目标健康、健康检查配置和应用状态。 |
| 目标不健康 | 核对健康检查路径/端口、安全组、目标应用。 |
| 连接超时 | 检查空闲超时设置和应用 keepalive 行为。 |
| TLS/证书错误 | 确认证书有效、覆盖域名、已挂到监听器。 |
| NLB 客户端 IP 行为 | NLB 保留客户端 IP；检查目标安全组是否允许客户端网段流量。 |
| 流量分布不均 | 检查跨可用区负载均衡和目标注册。 |

## 配额

每区域负载均衡器、目标组、监听器配额（例如默认每区域 20 个负载均衡器，可调）。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 Elastic Load Balancing？- ELB 用户指南](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)
- [AWS CLI：elbv2 命令](https://docs.aws.amazon.com/cli/latest/reference/elbv2/)
