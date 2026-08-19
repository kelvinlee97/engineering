# Amazon API Gateway - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon API Gateway is a managed service for creating, publishing, maintaining, monitoring, and securing REST, HTTP, and WebSocket APIs at any scale. It acts as a "front door" to backends such as Lambda functions, EC2 workloads, or any HTTP endpoint.

## Key concepts

- **API types**: REST APIs (full-featured), HTTP APIs (lighter, for serverless), and WebSocket APIs (stateful, full-duplex).
- **Resources and methods**: URL paths with HTTP methods mapped to integrations.
- **Integrations**: AWS Lambda (proxy), HTTP endpoints, AWS services, or mock.
- **Stages and deployments**: publish API versions; canary deployments for gradual rollout.
- **Authentication**: IAM, Lambda authorizers, Amazon Cognito user pools.
- **Throttling and quotas**: account- and per-API rate limits; API keys + usage plans.
- **Monitoring**: CloudWatch logs/metrics, CloudTrail, X-Ray tracing; WAF integration.

## Common operations (AWS CLI)

```bash
# REST API (v1)
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

# HTTP API (v2, simpler for serverless)
aws apigatewayv2 create-api --name my-http-api --protocol-type HTTP \
  --target arn:aws:lambda:ap-southeast-1:123456789012:function:my-function
```

## Best practices

- Use **HTTP APIs** for simple serverless backends; REST APIs when you need the full feature set.
- Enable **throttling** and use API keys + usage plans for client quotas.
- Authenticate with **Cognito or Lambda authorizers**; never leave routes open by default.
- Enable **CloudWatch logging** and alarms on `4XXError`, `5XXError`, and latency.
- Use **canary deployments** for safe releases; use **WAF** for web-layer protection.
- Use X-Ray to trace end-to-end latency through the API.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| `429 Too Many Requests` | Check account/per-API throttling limits and usage plans; raise quotas or add caching. |
| `500` from Lambda integration | Check Lambda function logs and the execution role; verify the integration URI/ARN. |
| `403 Forbidden` | Check IAM authorization, authorizer configuration, WAF rules, and API key requirements. |
| CORS errors | Configure CORS on the method/API and verify preflight (`OPTIONS`) handling. |
| High latency | Use X-Ray to trace; enable stage caching for repeated responses. |
| Changes not live | Redeploy to the stage; check stage variables and aliases. |

## Limits

Default account-level throttling is 10,000 requests per second per Region (adjustable); per-API limits and regional availability apply. See Service Quotas.

## Official references

- [What is Amazon API Gateway? - API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
- [AWS CLI: apigateway commands](https://docs.aws.amazon.com/cli/latest/reference/apigateway/)
