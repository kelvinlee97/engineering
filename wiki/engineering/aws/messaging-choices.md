---
type: Comparison
title: AWS messaging choices
description: SQS queues work for one consumer, SNS fans out to many, and EventBridge routes events by content; the limits and delivery guarantees differ.
tags: [aws, messaging]
sources:
  - id: aws-sqs
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/sqs/README.md
    title: "Amazon SQS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-sns
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/sns/README.md
    title: "Amazon SNS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-eventbridge
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/eventbridge/README.md
    title: "Amazon EventBridge - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Three AWS services move messages between components. Pick by how many receivers there are and how routing is decided.

| | [SQS](sqs.md) | [SNS](sns.md) | [EventBridge](eventbridge.md) |
| --- | --- | --- | --- |
| Shape | Queue, consumers pull | Topic, pushed to subscribers | Bus, rules route by event content |
| Max size | 1 MiB[^aws-sqs] | 256 KB[^aws-sns] | 256 KB[^aws-eventbridge] |
| Keeps messages | 60 seconds to 14 days[^aws-sqs] | No; DLQs for failed deliveries[^aws-sns] | Archive up to 14 days for replay[^aws-eventbridge] |
| Delivery | At least once; FIFO exactly-once[^aws-sqs] | At least once[^aws-sns] | Retry policy per target[^aws-eventbridge] |

## Combining them

SNS plus SQS fanout is the SNS note's recommended pattern for reliable asynchronous processing: each subscriber gets its own buffered queue.[^aws-sns] All three recommend DLQs and idempotent consumers.[^aws-sqs][^aws-sns][^aws-eventbridge]

## Related

- Source: [Amazon SQS - Runbook & Reference](../../sources/aws-sqs.md)
- Source: [Amazon SNS - Runbook & Reference](../../sources/aws-sns.md)
- Source: [Amazon EventBridge - Runbook & Reference](../../sources/aws-eventbridge.md)

[^aws-sqs]: Amazon SQS - Runbook & Reference
[^aws-sns]: Amazon SNS - Runbook & Reference
[^aws-eventbridge]: Amazon EventBridge - Runbook & Reference
