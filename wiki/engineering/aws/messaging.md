---
type: Comparison
title: AWS messaging
description: Choosing between SQS queues, SNS topics, and EventBridge event buses for decoupling AWS services.
tags:
- aws
- messaging
aliases:
- engineering/aws/messaging-choices
- engineering/aws/sqs
- engineering/aws/sns
- engineering/aws/eventbridge
sources:
- id: aws-sqs
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/sqs/README.md
  title: Amazon SQS - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-sns
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/sns/README.md
  title: Amazon SNS - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-eventbridge
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/eventbridge/README.md
  title: Amazon EventBridge - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
SQS, SNS, and EventBridge all decouple AWS components by passing messages between them. This page compares them by number of receivers and how routing is decided, then covers each service.

## Choosing a service

Three AWS services move messages between components. Pick by how many receivers there are and how routing is decided.

| | [SQS](#amazon-sqs) | [SNS](#amazon-sns) | [EventBridge](#amazon-eventbridge) |
| --- | --- | --- | --- |
| Shape | Queue, consumers pull | Topic, pushed to subscribers | Bus, rules route by event content |
| Max size | 1 MiB | 256 KB | 256 KB |
| Keeps messages | 60 seconds to 14 days | No; DLQs for failed deliveries | Archive up to 14 days for replay |
| Delivery | At least once; FIFO exactly-once[^aws-sqs] | At least once[^aws-sns] | Retry policy per target[^aws-eventbridge] |

### Combining them

SNS plus SQS fanout is the SNS note's recommended pattern for reliable asynchronous processing: each subscriber gets its own buffered queue. All three recommend DLQs and idempotent consumers.[^aws-sqs][^aws-sns][^aws-eventbridge]

## Amazon SQS

SQS is a managed message queue for decoupling distributed systems; messages are stored redundantly.[^aws-sqs]

### Concepts

- Standard queues deliver at least once with high throughput; FIFO queues give ordered, exactly-once processing per message group.
- Visibility timeout hides a received message while it is processed; set it above the maximum processing time.
- Retention defaults to 4 days, configurable from 60 seconds to 14 days.
- Dead-letter queues catch messages that keep failing, via `maxReceiveCount`.
- Long polling (`ReceiveMessageWaitTimeSeconds=20`) and batches of up to 10 messages cut cost.[^aws-sqs]

### Troubleshooting and limits

| Symptom | Check |
| --- | --- |
| Messages stuck | Visibility timeout versus processing time, consumer errors |
| Duplicates | Expected on standard queues; idempotent consumers |
| DLQ filling | Fix the consumer, then redrive |
| FIFO order broken | Same message group ID per workflow |

As tabled in the note. Messages are 1 KB to 1 MiB; up to 120,000 in-flight messages per standard queue.[^aws-sqs] See [AWS messaging choices](#choosing-a-service).

## Amazon SNS

SNS is managed pub/sub: publishers send to a topic, which delivers to every subscribed endpoint (SQS, Lambda, HTTP(S), email, mobile push, SMS, Data Firehose).[^aws-sns]

### Concepts and practices

- Fanout: one publish reaches many endpoints; SNS plus SQS gives buffered, reliable processing.
- Filter policies on subscriptions so each receives only relevant messages.
- DLQs on subscriptions; SSE-KMS; payloads up to 256 KB.
- Delivery is at least once, so consumers must be idempotent.[^aws-sns]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Not delivered to SQS | Subscription, SQS queue policy allows SNS, DLQ |
| Email/HTTP inactive | Confirm the subscription |
| Filtered messages missing | Filter policy versus message attributes |
| SMS not sending | SMS sandbox, spending limits, Region |

As tabled in the note.[^aws-sns] See [AWS messaging choices](#choosing-a-service).

## Amazon EventBridge

EventBridge ingests, filters, transforms, and delivers events between AWS services, your applications, and SaaS. It includes event buses with rules, Pipes for point-to-point integrations, and Scheduler for cron, rate, and one-time schedules.[^aws-eventbridge]

### Concepts

- Events are JSON state changes; AWS services emit them automatically to each account's default bus.
- Rules match events by pattern (source, detail-type, detail fields) and route to targets such as Lambda, SQS, SNS, and Step Functions, optionally transforming input.
- Archives keep events up to 14 days for replay.
- Pipes connect one source (including DynamoDB streams or Kinesis) to one target with filtering and enrichment.
- Events are up to 256 KB.[^aws-eventbridge]

### Practices

- Versioned `detail-type` and stable `source`; custom buses per domain; Pipes instead of Lambda glue.
- Test replay before relying on it; alarm on target delivery failures.[^aws-eventbridge]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Rule doesn't fire | Pattern matches source and detail-type; bus and Region |
| Target not invoked | Target ARN, permissions, transformation syntax |
| Replay not delivering | Archive contents, destination rule active |

As tabled in the note.[^aws-eventbridge] See [AWS messaging choices](#choosing-a-service).

## Related
- [Application integration](application-integration.md): APIs, workflows, and message brokers.
- [Streaming and search](streaming-and-search.md): Kinesis and MSK for ordered, replayable streams.
- [Domain index](index.md): other pages in this domain.

[^aws-sqs]: [Amazon SQS - Runbook & Reference](../../sources/aws-sqs.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/sqs/README.md)
[^aws-sns]: [Amazon SNS - Runbook & Reference](../../sources/aws-sns.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/sns/README.md)
[^aws-eventbridge]: [Amazon EventBridge - Runbook & Reference](../../sources/aws-eventbridge.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/eventbridge/README.md)
