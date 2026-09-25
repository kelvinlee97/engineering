---
type: Service
title: Amazon DynamoDB
description: AWS's serverless key-value and document database, designed around access patterns and partition keys.
tags: [aws, database, nosql]
sources:
  - id: aws-dynamodb
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/dynamodb/README.md
    title: "Amazon DynamoDB - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

DynamoDB is a serverless NoSQL database with single-digit millisecond performance at any scale and nothing to patch. Items are distributed by partition key (plus an optional sort key), so tables are designed around access patterns.[^aws-dynamodb]

## Concepts

- On-demand capacity (per request, scales to zero) or provisioned RCU/WCU with auto scaling.[^aws-dynamodb]
- Global and local secondary indexes; Streams for change data capture; ACID transactions.[^aws-dynamodb]
- Global tables: multi-active replication across Regions with 99.999% availability.[^aws-dynamodb]
- DAX in-memory cache for up to 10x read performance.[^aws-dynamodb]
- Point-in-time recovery up to 35 days; IAM-only access with encryption at rest by default.[^aws-dynamodb]

## Practices

- `query` rather than `scan`; spread partition keys to avoid hot partitions; TTL to expire data.[^aws-dynamodb]

## Troubleshooting and limits

| Symptom | Check |
| --- | --- |
| `ProvisionedThroughputExceededException` | On-demand or more capacity, backoff, hot keys |
| Slow `scan` | A GSI and `query` |
| Item too large | Limit is 400 KB; store the payload in S3 |

As tabled in the note.[^aws-dynamodb] Per-partition throughput is 3,000 RCU and 1,000 WCU.[^aws-dynamodb] See [AWS database choices](database-choices.md).

## Related

- Source: [Amazon DynamoDB - Runbook & Reference](../../sources/aws-dynamodb.md)

[^aws-dynamodb]: Amazon DynamoDB - Runbook & Reference
