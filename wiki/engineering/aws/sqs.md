---
type: Service
title: Amazon SQS
description: AWS's managed message queue for decoupling producers from consumers, with standard and FIFO queues.
tags: [aws, messaging]
sources:
  - id: aws-sqs
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/sqs/README.md
    title: "Amazon SQS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

SQS is a managed message queue for decoupling distributed systems; messages are stored redundantly.[^aws-sqs]

## Concepts

- Standard queues deliver at least once with high throughput; FIFO queues give ordered, exactly-once processing per message group.[^aws-sqs]
- Visibility timeout hides a received message while it is processed; set it above the maximum processing time.[^aws-sqs]
- Retention defaults to 4 days, configurable from 60 seconds to 14 days.[^aws-sqs]
- Dead-letter queues catch messages that keep failing, via `maxReceiveCount`.[^aws-sqs]
- Long polling (`ReceiveMessageWaitTimeSeconds=20`) and batches of up to 10 messages cut cost.[^aws-sqs]

## Troubleshooting and limits

| Symptom | Check |
| --- | --- |
| Messages stuck | Visibility timeout versus processing time, consumer errors |
| Duplicates | Expected on standard queues; idempotent consumers |
| DLQ filling | Fix the consumer, then redrive |
| FIFO order broken | Same message group ID per workflow |

As tabled in the note.[^aws-sqs] Messages are 1 KB to 1 MiB; up to 120,000 in-flight messages per standard queue.[^aws-sqs] See [AWS messaging choices](messaging-choices.md).

## Related

- Source: [Amazon SQS - Runbook & Reference](../../sources/aws-sqs.md)

[^aws-sqs]: Amazon SQS - Runbook & Reference
