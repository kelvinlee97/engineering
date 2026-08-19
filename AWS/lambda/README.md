# AWS Lambda - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-18

## Overview

AWS Lambda is a serverless compute service: you run code without provisioning or managing servers. AWS manages the underlying infrastructure (maintenance, capacity, scaling, patching) and you focus on application logic. Lambda provides two compute primitives:

- **Lambda Functions**: run code in response to events or API calls; each invocation runs independently and scales horizontally.
- **Lambda MicroVMs**: isolated compute environments with near-instant startup and state retention for up to 8 hours, designed for workloads that need a dedicated environment per user or job (for example, running untrusted code).

## Key concepts

- **Handler and runtimes**: your code exposes a handler function; Lambda provides managed language runtimes and supports custom runtimes.
- **Triggers**: connect functions to 200+ AWS services and HTTP endpoints (API Gateway, S3, SQS, EventBridge, and more).
- **Execution environment**: isolated, Firecracker-based; environments can be reused between invocations (warm starts).
- **Concurrency**: default 1,000 concurrent executions per account per Region (adjustable); each execution environment serves up to 10 synchronous requests/second.
- **Versions, aliases, and layers**: manage function versions, stable aliases, and shared dependencies.
- **Pricing**: pay per request plus GB-seconds of compute time; nothing while your code is not running.

## Quotas (verified 2026-08-18)

| Resource | Quota |
|----------|-------|
| Memory | 128 MB - 10,240 MB in 1-MB increments (1,769 MB approx. 1 vCPU) |
| Function timeout | 900 seconds (15 minutes) |
| `/tmp` storage | 512 MB - 10,240 MB |
| Deployment package | 50 MB zipped (API/SDK), 250 MB unzipped; 10 GB for container images |
| Environment variables | 4 KB in aggregate |
| Function layers | 5 |
| Invocation payload | 6 MB (synchronous), 1 MB (asynchronous) |
| Concurrent executions | 1,000 default per Region (adjustable; new accounts start lower) |
| MicroVM duration | Up to 8 hours per session |

## Common operations (AWS CLI)

```bash
# Deploy a function
aws lambda create-function --function-name my-function \
  --runtime python3.13 --role arn:aws:iam::123456789012:role/lambda-exec \
  --handler lambda_function.handler --zip-file fileb://function.zip

# Invoke (synchronous)
aws lambda invoke --function-name my-function \
  --cli-binary-format raw-in-base64-out \
  --payload '{"key":"value"}' response.json

# Update code or configuration
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip
aws lambda update-function-configuration --function-name my-function --memory-size 1024 --timeout 60

# List and inspect
aws lambda list-functions
aws lambda get-function --function-name my-function

# Function URL
aws lambda create-function-url-config --function-name my-function --auth-type NONE
```

## Best practices

- Write **stateless** functions; store state in external services (DynamoDB, S3, etc.).
- Give the function a **least-privilege execution role**; do not embed long-term credentials.
- Use environment variables for configuration and secrets (or AWS Secrets Manager / Parameter Store).
- Make handlers **idempotent** for retried invocations.
- Configure **dead-letter queues / on-failure destinations** for asynchronous invocations.
- Monitor with CloudWatch logs and metrics; set alarms on errors, throttles, and duration.
- Use **provisioned concurrency** for latency-sensitive paths; keep deployment packages small to reduce cold starts.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| Function times out | Increase timeout; check for blocking calls and slow downstream services. |
| Cold starts hurt latency | Use provisioned concurrency, smaller packages, and minimize initialization code. |
| Throttling (`429`) | Check reserved concurrency and account concurrency; align API Gateway throttle limits (default 10,000 rps) with Lambda concurrency. |
| `/tmp` full | Increase ephemeral storage or clean up files after processing. |
| No logs in CloudWatch | Verify the execution role has `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`. |
| Async invocations lost | Configure a DLQ or on-failure destination; Lambda retries asynchronous events twice by default. |
| Out of memory | Increase memory and watch the memory utilization metric. |

## Official references

- [What is AWS Lambda? - AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Lambda quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)
- [AWS Lambda pricing](https://aws.amazon.com/lambda/pricing/)
- [AWS CLI: lambda commands](https://docs.aws.amazon.com/cli/latest/reference/lambda/)
