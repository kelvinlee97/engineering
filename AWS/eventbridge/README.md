# Amazon EventBridge - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon EventBridge is a serverless event-routing service for building event-driven applications. It ingests, filters, transforms, and delivers events between AWS services, your applications, and third-party SaaS. It includes event buses and rules, EventBridge Pipes (point-to-point integrations with enrichment), and EventBridge Scheduler (cron/rate/one-time scheduling).

## Key concepts

- **Event**: a JSON structure representing a state change; AWS services emit events automatically.
- **Event bus**: a router that receives events and delivers them to zero or more targets; every account has a default bus, plus custom buses and event buses from other accounts.
- **Rule**: matches events by event pattern and routes them to targets (Lambda, SQS, SNS, Step Functions, API destinations, etc.).
- **Event pattern**: JSON matching (source, detail-type, detail fields) that decides which events a rule receives.
- **Targets and transformation**: target services plus optional input transformation of the event payload.
- **Archives and replay**: store events for up to 14 days (archive) and replay them to test or recover.
- **Pipes**: point-to-point integration from a single source (including non-EventBridge sources like DynamoDB streams, Kinesis) to a single target, with filtering and enrichment.
- **Scheduler**: serverless scheduling with cron/rate expressions, one-time invocations, flexible time windows, and retry limits.
- **Schemas**: discover and manage event schemas; generate code bindings.

## Common operations (AWS CLI)

```bash
# Create a rule on the default bus and add a target
aws events put-rule --name order-created \
  --event-pattern '{"source":["app.orders"],"detail-type":["OrderCreated"]}'
aws events put-targets --rule order-created \
  --targets 'Id=1,Arn=arn:aws:lambda:us-east-1:123456789012:function:on-order'

# Put a custom event
aws events put-events \
  --entries 'Source=app.orders,DetailType=OrderCreated,Detail="{\"orderId\":\"123\"}",EventBusName=default'

# List and remove rules
aws events list-rules
aws events delete-rule --name order-created

# Archive and replay
aws events create-archive --archive-name orders-archive --event-source-arn arn:aws:events:us-east-1:123456789012:event-bus/default
aws events start-replay --replay-name replay-1 --destination '{"Arn":"arn:aws:events:us-east-1:123456789012:event-bus/default"}' \
  --event-start-time 2026-08-18T00:00:00Z --event-end-time 2026-08-19T00:00:00Z \
  --source-arn arn:aws:events:us-east-1:123456789012:event-bus/default

# Scheduler
aws scheduler create-schedule --name nightly-cleanup --schedule-expression "cron(0 2 * * ? *)" \
  --flexible-time-window Mode=OFF \
  --target '{"Arn":"arn:aws:lambda:us-east-1:123456789012:function:cleanup","RoleArn":"arn:aws:iam::123456789012:role/scheduler-role"}'
```

## Best practices

- Model events explicitly: use a versioned `detail-type` and stable `source` so consumers can evolve independently.
- Use custom event buses per domain and keep rules focused on one concern.
- Use Pipes for simple source-to-target pipelines instead of Lambda glue.
- Archive critical events and test replay before relying on it for recovery.
- Validate event patterns and transformation in a staging bus first.
- Grant targets least privilege via resource-based policies and IAM; audit with CloudTrail.
- Monitor with CloudWatch (invocations, failures, throttles) and set alarms on target delivery failures.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Rule doesn't fire | Verify event pattern matches the event (source/detail-type), and the bus/rule region. |
| Target not invoked | Check target ARN, IAM/resource-based permissions, and input transformation syntax. |
| Events dropped | Confirm the rule is enabled, targets exist, and delivery retry policy is configured. |
| Replay not delivering | Verify archive contains the events and the destination bus/rule is active. |
| Scheduler invocations fail | Check schedule expression, flexible time window, and target role permissions. |

## Limits

Rules per bus, targets per rule, event size (256 KB), archive retention (up to 14 days), and scheduler quotas have per-account limits. See the Service Quotas console for current values.

## Official references

- [What Is Amazon EventBridge?](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
- [Amazon EventBridge quotas](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-quota.html)
- [Amazon EventBridge pricing](https://aws.amazon.com/eventbridge/pricing/)
- [AWS CLI: events and scheduler commands](https://docs.aws.amazon.com/cli/latest/reference/events/)
