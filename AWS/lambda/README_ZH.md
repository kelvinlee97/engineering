# AWS Lambda - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-18

## 概述

AWS Lambda 是无服务器计算服务：无需预置或管理服务器即可运行代码。AWS 负责底层基础设施（维护、容量、扩缩容、补丁），你专注应用逻辑。Lambda 提供两种计算原语：

- **Lambda Functions（函数）**：响应事件或 API 调用运行代码；每次调用独立运行，水平扩展。
- **Lambda MicroVMs**：近瞬时启动、状态可保留最长 8 小时的隔离计算环境，适合需要为每个用户/任务提供独立环境的工作负载（例如运行不可信代码）。

## 核心概念

- **Handler 与运行时**：代码暴露 handler 函数；Lambda 提供托管语言运行时，也支持自定义运行时。
- **触发器**：可连接 200+ AWS 服务和 HTTP 端点（API Gateway、S3、SQS、EventBridge 等）。
- **执行环境**：基于 Firecracker 的隔离环境；环境可在调用间复用（warm start）。
- **并发**：每账户每区域默认 1,000 并发执行（可调）；每个执行环境每秒最多处理 10 个同步请求。
- **版本、别名与层**：管理函数版本、稳定别名和共享依赖。
- **计费**：按请求数 + GB-秒计算时间付费；代码不运行时不收费。

## 配额（2026-08-18 核对）

| 资源 | 配额 |
|------|------|
| 内存 | 128 MB - 10,240 MB，按 1 MB 递增（1,769 MB 约等于 1 vCPU） |
| 函数超时 | 900 秒（15 分钟） |
| `/tmp` 存储 | 512 MB - 10,240 MB |
| 部署包 | 50 MB（zip，API/SDK），解压后 250 MB；容器镜像 10 GB |
| 环境变量 | 合计 4 KB |
| 函数层 | 5 个 |
| 调用负载 | 同步 6 MB，异步 1 MB |
| 并发执行 | 每区域默认 1,000（可调；新账户更低） |
| MicroVM 时长 | 每个会话最长 8 小时 |

## 常用操作（AWS CLI）

```bash
# 部署函数
aws lambda create-function --function-name my-function \
  --runtime python3.13 --role arn:aws:iam::123456789012:role/lambda-exec \
  --handler lambda_function.handler --zip-file fileb://function.zip

# 同步调用
aws lambda invoke --function-name my-function \
  --cli-binary-format raw-in-base64-out \
  --payload '{"key":"value"}' response.json

# 更新代码或配置
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip
aws lambda update-function-configuration --function-name my-function --memory-size 1024 --timeout 60

# 查看
aws lambda list-functions
aws lambda get-function --function-name my-function

# 函数 URL
aws lambda create-function-url-config --function-name my-function --auth-type NONE
```

## 最佳实践

- 写**无状态**函数；状态存到外部服务（DynamoDB、S3 等）。
- 给函数**最小权限的执行角色**；不要把长期凭证写进代码。
- 用环境变量做配置和密钥（或 AWS Secrets Manager / Parameter Store）。
- handler 要**幂等**，以应对重试。
- 异步调用配置**死信队列 / on-failure 目的地**。
- 用 CloudWatch 日志和指标监控；对错误、节流和时长设置告警。
- 延迟敏感路径用**预置并发（provisioned concurrency）**；缩小部署包以减少冷启动。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 函数超时 | 调大超时；检查阻塞调用和下游服务慢查询。 |
| 冷启动影响延迟 | 用预置并发、更小的包、精简初始化代码。 |
| 节流（`429`） | 检查预留并发和账户并发；把 API Gateway 节流（默认 10,000 rps）与 Lambda 并发对齐。 |
| `/tmp` 满了 | 调大临时存储或处理完及时清理。 |
| CloudWatch 没有日志 | 确认执行角色有 `logs:CreateLogGroup`、`logs:CreateLogStream`、`logs:PutLogEvents` 权限。 |
| 异步调用丢失 | 配置 DLQ 或 on-failure 目的地；Lambda 默认对异步事件重试两次。 |
| 内存不足 | 调大内存并关注内存利用率指标。 |

## 官方参考

- [什么是 AWS Lambda？- AWS Lambda 开发者指南](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Lambda 配额](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)
- [AWS Lambda 定价](https://aws.amazon.com/lambda/pricing/)
- [AWS CLI：lambda 命令](https://docs.aws.amazon.com/cli/latest/reference/lambda/)
