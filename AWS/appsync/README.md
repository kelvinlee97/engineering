# AWS AppSync - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS AppSync is a managed GraphQL and Pub/Sub API service. It connects your applications to data and events through a single GraphQL endpoint backed by one or more data sources (DynamoDB, Lambda, RDS, HTTP), with real-time updates via subscriptions and AppSync Events (WebSocket pub/sub, available since March 2025).

## Key concepts

- **GraphQL API**: the endpoint your clients query; schemas define types, queries, mutations, and subscriptions.
- **Data sources**: DynamoDB tables, Lambda functions, RDS clusters, OpenSearch, HTTP endpoints.
- **Resolvers**: functions that map GraphQL fields to data source operations; written in VTL or JavaScript/TypeScript.
- **Subscriptions**: real-time updates pushed to clients over WebSockets when mutations occur.
- **AppSync Events**: WebSocket-based pub/sub channels for real-time messaging.
- **Authorization**: API keys, IAM, Amazon Cognito user pools, OpenID Connect, and Lambda authorizers; private APIs with AWS WAF.
- **Merged APIs**: combine multiple GraphQL APIs into one endpoint for federated architectures.
- **Caching**: server-side caching for low latency.

## Common operations (AWS CLI)

```bash
# Create a GraphQL API
aws appsync create-graphql-api --name my-api --authentication-type AMAZON_COGNITO_USER_POOLS \
  --user-pool-config file://user-pool-config.json

# Upload the schema
aws appsync start-schema-creation --api-id <api-id> \
  --definition fileb://schema.graphql

# Add a data source and resolver
aws appsync create-data-source --api-id <api-id> --name PostsTable \
  --type AMAZON_DYNAMODB \
  --dynamodb-config tableName=posts,awsRegion=us-east-1
aws appsync create-resolver --api-id <api-id> --type-name Query --field-name getPost \
  --data-source-name PostsTable --request-mapping-template file://request.vtl \
  --response-mapping-template file://response.vtl

# Create an API key (for API_KEY auth)
aws appsync create-api-key --api-id <api-id>

# Inspect
aws appsync get-graphql-api --api-id <api-id>
aws appsync list-resolvers --api-id <api-id> --type-name Query
```

## Best practices

- Define schema-first and keep resolvers thin; use JS/TS resolvers for complex logic.
- Choose authorization per API: Cognito for user-facing apps, IAM for service-to-service, API keys for public/development.
- Batch and paginate DynamoDB data source requests to avoid per-item latency.
- Use subscriptions/AppSync Events only for data that clients need in real time.
- Enable CloudWatch logs and X-Ray tracing; monitor resolver errors and latency.
- Use merged APIs to avoid duplicating shared GraphQL schemas across teams.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Resolver returns null | Check data source permissions (IAM role) and resolver mapping templates. |
| Subscription not receiving events | Verify subscription auth, WebSocket connection, and that the mutation publishes to the topic. |
| `401/403` on requests | Check API key validity, Cognito tokens, and IAM signing. |
| Slow queries | Enable caching, review N+1 resolver patterns, and index the underlying data source. |
| Schema upload fails | Validate GraphQL schema syntax and unsupported directives. |

## Limits

API count, resolvers per API, request/response sizes, subscription connection counts, and caching have per-account quotas. See the Service Quotas console for current values.

## Official references

- [What is AWS AppSync?](https://docs.aws.amazon.com/appsync/latest/devguide/what-is-appsync.html)
- [AWS AppSync service quotas](https://docs.aws.amazon.com/appsync/latest/devguide/limits.html)
- [AWS AppSync pricing](https://aws.amazon.com/appsync/pricing/)
- [AWS CLI: appsync commands](https://docs.aws.amazon.com/cli/latest/reference/appsync/)
