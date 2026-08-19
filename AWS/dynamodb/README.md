# Amazon DynamoDB - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon DynamoDB is a serverless, fully managed NoSQL database with single-digit millisecond performance at any scale. It supports key-value and document data models and requires no server provisioning, patching, or maintenance.

## Key concepts

- **Tables, items, attributes**: a table stores items; each item has attributes. The **partition key** (and optional sort key) determines distribution.
- **Capacity modes**: on-demand (pay per request, scales to zero) or provisioned (RCU/WCU with auto scaling).
- **Secondary indexes**: global (GSI) and local (LSI) for querying by alternate keys.
- **Streams**: DynamoDB Streams and Kinesis Data Streams for DynamoDB capture item-level changes (CDC).
- **Global tables**: multi-active replication across Regions with 99.999% availability.
- **Transactions**: ACID across one or more tables.
- **DAX**: in-memory cache for up to 10x read performance.
- **Backups**: point-in-time recovery (up to 35 days) and on-demand backups; AWS Backup integration.
- **Security**: IAM only (no usernames/passwords), encryption at rest by default (KMS), fine-grained access control.

## Common operations (AWS CLI)

```bash
# Create a table (on-demand)
aws dynamodb create-table --table-name orders \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# CRUD
aws dynamodb put-item --table-name orders --item '{"id":{"S":"1001"},"amount":{"N":"250"}}'
aws dynamodb get-item --table-name orders --key '{"id":{"S":"1001"}}'
aws dynamodb query --table-name orders --key-condition-expression "id = :id" \
  --expression-attribute-values '{":id":{"S":"1001"}}'
aws dynamodb update-item --table-name orders --key '{"id":{"S":"1001"}}' \
  --update-expression "SET #a = :a" --expression-attribute-names '{"#a":"amount"}' \
  --expression-attribute-values '{":a":{"N":"300"}}'
aws dynamodb delete-item --table-name orders --key '{"id":{"S":"1001"}}'

# Admin
aws dynamodb list-tables
aws dynamodb describe-table --table-name orders
aws dynamodb update-table --table-name orders --billing-mode PROVISIONED \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

# Backups
aws dynamodb create-backup --table-name orders --backup-name orders-backup
aws dynamodb restore-table-to-point-in-time --source-table-name orders \
  --target-table-name orders-restored --use-latest-restorable-time
```

## Best practices

- Design tables around **access patterns** (single-table design where it fits); use `query` over `scan`.
- Distribute partition keys to avoid hot partitions; use sort keys for ordering.
- Use **on-demand** for variable/unpredictable workloads; provisioned + auto scaling for steady loads.
- Enable **point-in-time recovery**; use **TTL** to expire data automatically.
- Use **DAX** for read-heavy, latency-sensitive workloads.
- Use **fine-grained IAM** (attribute-level conditions) and resource-based policies where needed.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| Throttling (`ProvisionedThroughputExceededException`) | Switch to on-demand or raise capacity; retry with exponential backoff; check for hot keys. |
| Hot partition | Redesign the key (add entropy, use sort key, or shard); review access patterns. |
| `scan` too slow | Replace with `query` on a GSI designed for the access pattern. |
| Item too large | Item size limit is 400 KB; store large payloads in S3 with a pointer in DynamoDB. |
| Stream lag | Check Lambda consumer concurrency and error handling; use event filtering. |
| DAX not helping | Verify DAX cluster in the same VPC and the client uses the DAX endpoint. |

## Limits

- Item size: up to 400 KB.
- Per-partition throughput: 3,000 RCU / 1,000 WCU.
- Table size: virtually unlimited; see Service Quotas for account-level limits.

## Official references

- [What is Amazon DynamoDB? - DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [AWS CLI: dynamodb commands](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/)
