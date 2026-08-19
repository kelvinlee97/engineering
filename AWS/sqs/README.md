# Amazon SQS - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Simple Queue Service (Amazon SQS) is a fully managed message queue for decoupling distributed systems. Messages are stored redundantly across servers; queues support dead-letter queues and cost allocation tags.

## Key concepts

- **Queue types**: standard (at-least-once delivery, high throughput) and FIFO (exactly-once processing, ordered, high-throughput mode).
- **Visibility timeout**: how long a received message is hidden from other consumers while being processed.
- **Message retention**: default 4 days; configurable 60 seconds to 14 days.
- **Dead-letter queue (DLQ)**: a queue that receives messages the source queue failed to process.
- **Long polling**: reduces cost and latency; recommended (`ReceiveMessageWaitTimeSeconds=20`).
- **Security**: server-side encryption (SQS-managed or KMS), IAM policies, queue policies.

## Common operations (AWS CLI)

```bash
# Create queues (standard + FIFO + DLQ)
aws sqs create-queue --queue-name my-queue \
  --attributes VisibilityTimeout=60,ReceiveMessageWaitTimeSeconds=20,MessageRetentionPeriod=345600
aws sqs create-queue --queue-name my-queue.fifo --attributes FifoQueue=true
aws sqs create-queue --queue-name my-queue-dlq

# Send
aws sqs send-message --queue-url https://sqs.ap-southeast-1.amazonaws.com/123456789012/my-queue \
  --message-body '{"order": "1001"}'

# Receive and delete
aws sqs receive-message --queue-url .../my-queue --max-number-of-messages 10 --wait-time-seconds 20
aws sqs delete-message --queue-url .../my-queue --receipt-handle <receipt-handle>

# Configure DLQ (RedrivePolicy on the source queue)
aws sqs set-queue-attributes --queue-url .../my-queue \
  --attributes '{"RedrivePolicy":"{\"deadLetterTargetArn\":\"arn:aws:sqs:...:my-queue-dlq\",\"maxReceiveCount\":5}"}'

# Inspect
aws sqs list-queues
aws sqs get-queue-attributes --queue-url .../my-queue --attribute-names All
```

## Best practices

- Configure a **DLQ** with a sensible `maxReceiveCount` and alarm on its depth.
- Set **visibility timeout** longer than the maximum processing time; use long polling.
- Use **batch** APIs (up to 10 messages) to reduce cost.
- Make consumers **idempotent** (standard queues deliver at-least-once).
- Use **FIFO** when order or exactly-once matters; choose a message group ID per workflow.
- Encrypt sensitive payloads (SSE-KMS) and scope IAM policies to queue ARNs.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| Messages stuck / not consumed | Check visibility timeout vs. consumer processing time; check consumer errors. |
| Duplicate processing | Expected with standard queues; make consumers idempotent. |
| DLQ filling up | Inspect messages and consumer errors; fix the consumer, then redrive. |
| Throttling | Use batch sends/receives and exponential backoff. |
| FIFO order broken | Verify all messages for one workflow use the same message group ID. |
| Messages > 1 MiB | Store the payload in S3 and put the pointer in the message. |

## Limits

- Message size: 1 KB - 1 MiB.
- Retention: 60 seconds - 14 days.
- In-flight messages (standard): 120,000 per queue.
- See Service Quotas for account-level limits.

## Official references

- [What is Amazon SQS? - Amazon SQS Developer Guide](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [AWS CLI: sqs commands](https://docs.aws.amazon.com/cli/latest/reference/sqs/)
