# AWS WAF - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS WAF 是 Web 应用防火墙，监控发往受保护资源的 HTTP(S) 请求，并根据规则（IP、查询字符串、请求头、请求体）控制访问。命中时返回内容、HTTP 403 或自定义响应。

## 可保护的资源

- CloudFront 分发
- API Gateway REST API
- Application Load Balancer
- AWS AppSync GraphQL API
- Amazon Cognito 用户池
- AWS App Runner、AWS Amplify、AWS Verified Access

## 核心概念

- **Web ACL**：与受保护资源关联的规则容器。
- **规则与规则组**：单个匹配语句或可复用组；AWS 托管规则组覆盖常见威胁。
- **基于速率的规则**：在时间窗口内限制某个 IP 的请求数；适合 DDoS/爬虫防护。
- **动作**：allow、block、count 或自定义响应；先 `count` 测试再阻断。
- **标签与日志**：给匹配请求打标签，日志发送到 S3、CloudWatch Logs 或 Kinesis Data Firehose。

## 常用操作（AWS CLI）

```bash
# 创建 Web ACL（默认动作文件）
aws wafv2 create-web-acl --name my-acl --scope REGIONAL \
  --default-action file://default-action.json \
  --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=my-acl

# 关联资源（ALB/API Gateway）
aws wafv2 associate-web-acl --web-acl-arn <acl-arn> --resource-arn <resource-arn>

# 更新规则
aws wafv2 update-web-acl --name my-acl --scope REGIONAL --id <acl-id> \
  --default-action file://default-action.json \
  --rules file://rules.json \
  --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=my-acl

# 查看
aws wafv2 list-web-acls --scope REGIONAL
aws wafv2 get-web-acl --name my-acl --scope REGIONAL --id <acl-id>

# 开启日志
aws wafv2 put-logging-configuration --logging-configuration file://logging.json
```

## 最佳实践

- 从 **AWS 托管规则组**开始，再加业务自定义规则。
- 加**基于速率的规则**防 DDoS/爬虫。
- 先 **count 模式**测试，看日志确认后再改 block。
- 用**标签和日志**定位命中规则。
- 作用域要正确：CloudFront 用 `CLOUDFRONT`，ALB/API Gateway 用 `REGIONAL`。
- 用 CloudWatch 监控 WAF 指标，对拦截请求激增告警。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 正常流量被拦 | 从日志确认命中规则；先用 count 模式；调整 IP set 或规则范围。 |
| 意外 `403` | 检查 Web ACL 关联、规则动作、托管规则组行为。 |
| 日志不出现 | 核对日志配置和目标权限。 |
| 性能影响 | 控制规则数量，用高效匹配语句。 |
| 速率规则误伤 | 调高速率阈值或使用 scope-down 语句。 |

## 配额

规则、规则组、Web ACL 有每账户和作用域配额。以 Service Quotas 控制台为准。

## 官方参考

- [AWS WAF - WAF 开发者指南](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html)
- [AWS WAF 定价](https://aws.amazon.com/waf/pricing/)
- [AWS CLI：wafv2 命令](https://docs.aws.amazon.com/cli/latest/reference/wafv2/)
