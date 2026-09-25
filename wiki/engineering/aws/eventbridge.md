---
type: Service
title: Amazon EventBridge
description: "AWS's serverless event router: buses and rules match JSON events to targets, with Pipes and Scheduler alongside."
tags: [aws, messaging, events]
sources:
  - id: aws-eventbridge
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/eventbridge/README.md
    title: "Amazon EventBridge - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

EventBridge ingests, filters, transforms, and delivers events between AWS services, your applications, and SaaS. It includes event buses with rules, Pipes for point-to-point integrations, and Scheduler for cron, rate, and one-time schedules.[^aws-eventbridge]

## Concepts

- Events are JSON state changes; AWS services emit them automatically to each account's default bus.[^aws-eventbridge]
- Rules match events by pattern (source, detail-type, detail fields) and route to targets such as Lambda, SQS, SNS, and Step Functions, optionally transforming input.[^aws-eventbridge]
- Archives keep events up to 14 days for replay.[^aws-eventbridge]
- Pipes connect one source (including DynamoDB streams or Kinesis) to one target with filtering and enrichment.[^aws-eventbridge]
- Events are up to 256 KB.[^aws-eventbridge]

## Practices

- Versioned `detail-type` and stable `source`; custom buses per domain; Pipes instead of Lambda glue.[^aws-eventbridge]
- Test replay before relying on it; alarm on target delivery failures.[^aws-eventbridge]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Rule doesn't fire | Pattern matches source and detail-type; bus and Region |
| Target not invoked | Target ARN, permissions, transformation syntax |
| Replay not delivering | Archive contents, destination rule active |

As tabled in the note.[^aws-eventbridge] See [AWS messaging choices](messaging-choices.md).

## Related

- Source: [Amazon EventBridge - Runbook & Reference](../../sources/aws-eventbridge.md)

[^aws-eventbridge]: Amazon EventBridge - Runbook & Reference
