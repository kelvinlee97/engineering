# Amazon Kinesis - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Kinesis is the AWS streaming data platform. It collects, processes, and analyzes real-time data at scale. The platform includes Kinesis Data Streams, Amazon Data Firehose, Managed Service for Apache Flink, and Kinesis Video Streams.

## Service components

| Service | Purpose |
|---|---|
| Kinesis Data Streams | Durable, scalable stream ingestion with ordered records per shard; producers push, consumers poll |
| Amazon Data Firehose | Fully managed streaming delivery to S3, Redshift, OpenSearch, Splunk, and third parties; no consumers to run |
| Managed Service for Apache Flink | Stream processing with Apache Flink (SQL and DataStream API) |
| Kinesis Video Streams | Ingestion and playback of video streams for ML and analytics |

## Key concepts

- **Stream and shard**: a shard is a unit of capacity; data is ordered within a shard, and throughput scales with shard count.
- **Record**: the unit of data (partition key + data blob), retained for a configurable period (default 24 hours, up to 365 days).
- **Producers and consumers**: producers use `PutRecord`/`PutRecords`; consumers poll with `GetRecords` using the Kinesis Client Library (KCL) for fault tolerance.
- **On-demand vs. provisioned mode**: on-demand scales shards automatically; provisioned uses a fixed shard count you manage.
- **Enhanced fan-out**: dedicated 2 MB/s read throughput per consumer via `SubscribeToShard`.
- **Data Firehose buffering**: accumulates records by size (up to 128 MB) or interval (up to 900 seconds) before delivery.

## Common operations (AWS CLI)

```bash
# Create a stream (provisioned, 2 shards)
aws kinesis create-stream --stream-name events --shard-count 2

# List streams and put a record
aws kinesis list-streams
aws kinesis put-record --stream-name events \
  --partition-key order-123 --data "$(printf '{"event":"created"}' | base64)"

# Get a shard iterator and read records
aws kinesis get-shard-iterator --stream-name events \
  --shard-id shardId-000000000000 --shard-iterator-type TRIM_HORIZON
aws kinesis get-records --shard-iterator <shard-iterator>

# Scale
aws kinesis update-shard-count --stream-name events --target-shard-count 4 --scaling-type UNIFORM_SCALING

# Data Firehose
aws firehose create-delivery-stream --delivery-stream-name app-logs \
  --extended-s3-destination-configuration RoleARN=arn:aws:iam::123456789012:role/firehose-role,BucketARN=arn:aws:s3:::logs-bucket
aws firehose put-record --delivery-stream-name app-logs \
  --record "Data=$(printf '{"level":"info"}' | base64)"
```

## Best practices

- Choose Data Firehose when you just need reliable delivery to storage/analytics; use Data Streams when you need custom consumers or replay.
- Design partition keys so hot keys don't skew a shard; monitor `WriteProvisionedThroughputExceeded`.
- Use the Kinesis Client Library (KCL) for exactly-once-ish, fault-tolerant consumption and dynamic shard handling.
- Set retention to match your replay window; longer retention costs more.
- Use enhanced fan-out for many consumers needing full throughput.
- Buffer and compress records before `PutRecords` to cut costs; use batches instead of single records.
- Encrypt streams with KMS (SSE) and control access with IAM; monitor with CloudWatch metrics.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| `ProvisionedThroughputExceededException` | Increase shards, improve partition key distribution, or use on-demand mode. |
| Records lost | Verify retention and consumer checkpointing; KCL checkpoints lag behind if the consumer is slow. |
| High consumer lag | Add shards/consumers, use enhanced fan-out, or move heavy processing downstream. |
| Firehose delivery failures | Check destination permissions, buffering settings, and CloudWatch metrics for the delivery stream. |
| Data appears unordered | Ordering is only guaranteed within a shard; design partition keys accordingly. |

## Limits

Each shard supports 1 MB/s (or 1,000 records/s) write and 2 MB/s read; default retention is 24 hours and can be extended up to 365 days. Stream, shard, and Firehose counts have per-account quotas. See the Service Quotas console for current values.

## Official references

- [What is Amazon Kinesis Data Streams?](https://docs.aws.amazon.com/streams/latest/dev/introduction.html)
- [What is Amazon Data Firehose?](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html)
- [Amazon Kinesis pricing](https://aws.amazon.com/kinesis/pricing/)
- [AWS CLI: kinesis and firehose commands](https://docs.aws.amazon.com/cli/latest/reference/kinesis/)
