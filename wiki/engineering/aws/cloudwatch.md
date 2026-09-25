---
type: Service
title: Amazon CloudWatch
description: "AWS's monitoring service: metrics, logs, and traces feed alarms and dashboards, and alarms only ever watch metrics."
tags: [aws, observability, monitoring]
sources:
  - id: aws-cloudwatch
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudwatch/README.md
    title: "Amazon CloudWatch - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

CloudWatch collects metrics, logs, and traces and provides alarms, dashboards, and automated actions. An alarm only ever watches a metric, never a log or a trace, so alarming on a log pattern needs a metric filter in between.[^aws-cloudwatch]

```mermaid
flowchart LR
    accTitle: From logs to a CloudWatch alarm
    accDescr: Logs can be queried in Logs Insights, but only a metric filter turns a log pattern into a metric, and only metrics can drive alarms, which then trigger actions.
    L[Log group] --> Q[Logs Insights: query only]
    L --> F[Metric filter]
    F --> M[Metric]
    M --> A[Alarm]
    A --> Act[SNS, Auto Scaling, Systems Manager]
```

## Concepts

- AWS services publish metrics automatically; you add custom metrics; standard metrics are kept 15 months.[^aws-cloudwatch]
- Logs Insights queries in SQL or PPL; subscription filters stream logs elsewhere.[^aws-cloudwatch]
- The CloudWatch agent adds OS-level metrics (memory, disk) from EC2 and on-premises.[^aws-cloudwatch]
- Application Signals with SLOs, Synthetics canaries, RUM, Container/Lambda/Database Insights, and native OTLP ingestion.[^aws-cloudwatch]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| No instance metrics | Agent running; role allows `cloudwatch:PutMetricData` |
| Alarm not firing | Metric name, namespace, period; state not `INSUFFICIENT_DATA` |
| High cost | Custom metric volume, log ingestion, detailed monitoring |

As tabled in the note.[^aws-cloudwatch]

## Related

- Source: [Amazon CloudWatch - Runbook & Reference](../../sources/aws-cloudwatch.md)

[^aws-cloudwatch]: Amazon CloudWatch - Runbook & Reference
