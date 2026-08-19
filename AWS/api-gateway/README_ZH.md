# Amazon API Gateway - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon API Gateway 是托管服务，用于在任意规模下创建、发布、维护、监控和保护 REST、HTTP 与 WebSocket API。它是访问后端（Lambda 函数、EC2 工作负载或任意 HTTP 端点）的"前门"。

## 核心概念

- **API 类型**：REST API（功能最全）、HTTP API（更轻量，适合无服务器）、WebSocket API（有状态、全双工）。
- **资源与方法**：URL 路径 + HTTP 方法，映射到集成。
- **集成**：AWS Lambda（proxy）、HTTP 端点、AWS 服务、mock。
- **阶段与部署**：发布 API 版本；canary 部署做灰度。
- **认证**：IAM、Lambda authorizer、Amazon Cognito 用户池。
- **限流与配额**：账户级与 API 级速率限制；API key + usage plan。
- **监控**：CloudWatch 日志/指标、CloudTrail、X-Ray 追踪；支持 WAF。

## 常用操作（AWS CLI）

```bash
# REST API（v1）
aws apigateway create-rest-api --name my-api
aws apigateway get-resources --rest-api-id <api-id>
aws apigateway create-resource --rest-api-id <api-id> --parent-id <root-id> --path-part orders
aws apigateway put-method --rest-api-id <api-id> --resource-id <res-id> \
  --http-method GET --authorization-type NONE
aws apigateway put-integration --rest-api-id <api-id> --resource-id <res-id> \
  --http-method GET --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:ap-southeast-1:lambda:path/2015-03-31/functions/arn:aws:lambda:ap-southeast-1:123456789012:function:my-function/invocations
aws apigateway create-deployment --rest-api-id <api-id> --stage-name prod

# HTTP API（v2，无服务器更简单）
aws apigatewayv2 create-api --name my-http-api --protocol-type HTTP \
  --target arn:aws:lambda:ap-southeast-1:123456789012:function:my-function
```

## 最佳实践

- 简单无服务器后端用 **HTTP API**；需要完整功能时用 REST API。
- 开启**限流**，用 API key + usage plan 管理客户端配额。
- 用 **Cognito 或 Lambda authorizer** 做认证；路由不要默认开放。
- 开启 **CloudWatch 日志**，对 `4XXError`、`5XXError` 和延迟设置告警。
- 用 **canary 部署**安全发布；用 **WAF** 做 Web 层防护。
- 用 X-Ray 追踪 API 端到端延迟。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| `429 Too Many Requests` | 检查账户/API 限流和 usage plan；提升配额或加缓存。 |
| Lambda 集成返回 `500` | 检查 Lambda 日志和执行角色；核对集成 URI/ARN。 |
| `403 Forbidden` | 检查 IAM 授权、authorizer 配置、WAF 规则、API key 要求。 |
| CORS 报错 | 在方法/API 上配置 CORS，核对预检（`OPTIONS`）处理。 |
| 延迟高 | 用 X-Ray 追踪；对重复响应开启阶段缓存。 |
| 改动未生效 | 重新部署到阶段；检查阶段变量和别名。 |

## 配额

账户级默认限流为每区域每秒 10,000 次请求（可调）；API 级限制和区域可用性以 Service Quotas 为准。

## 官方参考

- [什么是 Amazon API Gateway？- API Gateway 开发者指南](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
- [AWS CLI：apigateway 命令](https://docs.aws.amazon.com/cli/latest/reference/apigateway/)
