# AWS AppSync - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS AppSync 是托管的 GraphQL 与 Pub/Sub API 服务。它通过一个 GraphQL 端点把应用连接到数据与事件，后端可挂一个或多个数据源（DynamoDB、Lambda、RDS、HTTP），并通过订阅和 AppSync Events（2025 年 3 月起的 WebSocket pub/sub）提供实时更新。

## 核心概念

- **GraphQL API**：客户端查询的端点；schema 定义类型、查询、变更和订阅。
- **数据源**：DynamoDB 表、Lambda 函数、RDS 集群、OpenSearch、HTTP 端点。
- **Resolver（解析器）**：把 GraphQL 字段映射到数据源操作的函数；可用 VTL 或 JavaScript/TypeScript 编写。
- **订阅（Subscriptions）**：变更发生时通过 WebSocket 推送给客户端的实时更新。
- **AppSync Events**：基于 WebSocket 的 pub/sub 通道，用于实时消息。
- **授权**：API key、IAM、Amazon Cognito 用户池、OpenID Connect、Lambda authorizer；私有 API 可挂 AWS WAF。
- **合并 API（Merged APIs）**：把多个 GraphQL API 合并为一个端点，支持联邦架构。
- **缓存**：服务端缓存降低延迟。

## 常用操作（AWS CLI）

```bash
# 创建 GraphQL API
aws appsync create-graphql-api --name my-api --authentication-type AMAZON_COGNITO_USER_POOLS \
  --user-pool-config file://user-pool-config.json

# 上传 schema
aws appsync start-schema-creation --api-id <api-id> \
  --definition fileb://schema.graphql

# 添加数据源和 resolver
aws appsync create-data-source --api-id <api-id> --name PostsTable \
  --type AMAZON_DYNAMODB \
  --dynamodb-config tableName=posts,awsRegion=us-east-1
aws appsync create-resolver --api-id <api-id> --type-name Query --field-name getPost \
  --data-source-name PostsTable --request-mapping-template file://request.vtl \
  --response-mapping-template file://response.vtl

# 创建 API key（API_KEY 认证时）
aws appsync create-api-key --api-id <api-id>

# 查看
aws appsync get-graphql-api --api-id <api-id>
aws appsync list-resolvers --api-id <api-id> --type-name Query
```

## 最佳实践

- schema 优先，resolver 保持精简；复杂逻辑用 JS/TS resolver。
- 按场景选授权：面向用户用 Cognito，服务间用 IAM，公开/开发用 API key。
- DynamoDB 数据源批量分页请求，避免逐条延迟。
- 只有客户端确实需要实时数据时才用订阅/AppSync Events。
- 开启 CloudWatch 日志和 X-Ray 追踪；监控 resolver 错误和延迟。
- 用合并 API 避免团队间重复定义共享 GraphQL schema。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| Resolver 返回 null | 检查数据源 IAM 权限和映射模板。 |
| 订阅收不到事件 | 核对订阅认证、WebSocket 连接，以及 mutation 是否发布到对应主题。 |
| 请求 `401/403` | 检查 API key 有效期、Cognito token 和 IAM 签名。 |
| 查询慢 | 启用缓存、排查 N+1 resolver 模式，给底层数据源加索引。 |
| Schema 上传失败 | 校验 GraphQL 语法和不支持的指令。 |

## 配额

API 数量、每 API resolver 数、请求/响应大小、订阅连接数和缓存有每账号配额。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 AWS AppSync？](https://docs.aws.amazon.com/appsync/latest/devguide/what-is-appsync.html)
- [AWS AppSync 服务配额](https://docs.aws.amazon.com/appsync/latest/devguide/limits.html)
- [AWS AppSync 定价](https://aws.amazon.com/appsync/pricing/)
- [AWS CLI：appsync 命令](https://docs.aws.amazon.com/cli/latest/reference/appsync/)
