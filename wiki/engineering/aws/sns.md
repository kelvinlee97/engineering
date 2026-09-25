---
type: Service
title: Amazon SNS
description: AWS's managed publish/subscribe service that fans one message out to many subscribers.
tags: [aws, messaging]
sources:
  - id: aws-sns
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/sns/README.md
    title: "Amazon SNS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

SNS is managed pub/sub: publishers send to a topic, which delivers to every subscribed endpoint (SQS, Lambda, HTTP(S), email, mobile push, SMS, Data Firehose).[^aws-sns]

## Concepts and practices

- Fanout: one publish reaches many endpoints; SNS plus SQS gives buffered, reliable processing.[^aws-sns]
- Filter policies on subscriptions so each receives only relevant messages.[^aws-sns]
- DLQs on subscriptions; SSE-KMS; payloads up to 256 KB.[^aws-sns]
- Delivery is at least once, so consumers must be idempotent.[^aws-sns]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Not delivered to SQS | Subscription, SQS queue policy allows SNS, DLQ |
| Email/HTTP inactive | Confirm the subscription |
| Filtered messages missing | Filter policy versus message attributes |
| SMS not sending | SMS sandbox, spending limits, Region |

As tabled in the note.[^aws-sns] See [AWS messaging choices](messaging-choices.md).

## Related

- Source: [Amazon SNS - Runbook & Reference](../../sources/aws-sns.md)

[^aws-sns]: Amazon SNS - Runbook & Reference
