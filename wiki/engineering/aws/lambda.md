---
type: Service
title: AWS Lambda
description: "AWS's serverless compute: functions run per event with no servers to manage, billed per request and GB-second."
tags: [aws, compute, serverless]
sources:
  - id: aws-lambda
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/lambda/README.md
    title: "AWS Lambda - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Lambda runs code without provisioning servers; AWS handles capacity, scaling, and patching. It offers Lambda Functions, which run per event or API call and scale horizontally, and Lambda MicroVMs, isolated environments with state kept for up to 8 hours for per-user or per-job work such as running untrusted code.[^aws-lambda]

## Concepts

- Handlers on managed or custom runtimes; triggers from 200+ AWS services and HTTP endpoints.[^aws-lambda]
- Isolated Firecracker-based execution environments, reused between invocations (warm starts).[^aws-lambda]
- Versions, aliases, and layers; pay per request plus GB-seconds.[^aws-lambda]

## Quotas

| Resource | Quota |
| --- | --- |
| Memory | 128 MB to 10,240 MB (1,769 MB is about 1 vCPU) |
| Timeout | 900 seconds (15 minutes) |
| `/tmp` | 512 MB to 10,240 MB |
| Package | 50 MB zipped, 250 MB unzipped; 10 GB container images |
| Environment variables | 4 KB total |
| Layers | 5 |
| Payload | 6 MB synchronous, 1 MB asynchronous |
| Concurrency | 1,000 per Region by default, adjustable |

As tabled in the note, verified 2026-08-18.[^aws-lambda] Each execution environment serves up to 10 synchronous requests per second.[^aws-lambda]

## Practices

- Stateless, idempotent handlers with least-privilege execution roles.[^aws-lambda]
- DLQs or on-failure destinations for async invocations; Lambda retries async events twice by default.[^aws-lambda]
- Provisioned concurrency and small packages against cold starts.[^aws-lambda]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Timeouts | Timeout value, blocking calls, slow downstreams |
| Throttling (`429`) | Reserved and account concurrency; API Gateway default is 10,000 rps |
| No logs | Execution role has the three `logs:` permissions |
| Async events lost | DLQ or on-failure destination |

As tabled in the note.[^aws-lambda] See [AWS compute options](compute-options.md).

## Related

- Source: [AWS Lambda - Runbook & Reference](../../sources/aws-lambda.md)

[^aws-lambda]: AWS Lambda - Runbook & Reference
