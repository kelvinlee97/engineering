---
type: Service
title: AWS CloudTrail
description: AWS's audit log of API and console actions, from a free 90-day event history to long-term trails and a queryable data lake.
tags: [aws, security, audit, logging]
sources:
  - id: aws-cloudtrail
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudtrail/README.md
    title: "AWS CloudTrail - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

CloudTrail records actions taken by users, roles, and AWS services as events, for auditing, governance, and compliance.[^aws-cloudtrail] It has three layers of increasing commitment.[^aws-cloudtrail]

| Layer | What it keeps |
| --- | --- |
| Event history | The past 90 days of management events per Region; free, on by default, cannot be extended |
| Trail | Management events and selected data and Insights events delivered to S3, optionally to CloudWatch Logs and EventBridge |
| CloudTrail Lake | An event data store queried with SQL, kept up to 2,557 days (about 7 years) or 3,653 days (about 10 years) depending on pricing |

As described in the note.[^aws-cloudtrail]

**Management events** are control-plane operations; **data events** are resource operations such as S3 object access or Lambda invocations, which is why they are recorded selectively to control cost.[^aws-cloudtrail] Insights events flag unusual API rates and errors.[^aws-cloudtrail]

## Practices

- An organization trail from the management account to a dedicated, encrypted, private, versioned S3 bucket; member accounts cannot disable it.[^aws-cloudtrail]
- Alarm on trail status so logging does not stop silently, and restrict `StopLogging` and `DeleteTrail` with IAM and SCPs.[^aws-cloudtrail]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| No events delivered | Trail logging, bucket policy, KMS key permissions |
| Data events missing | Event selectors |
| Only 90 days available | Event history is fixed; create a trail or Lake store |

As tabled in the note.[^aws-cloudtrail]

## Related

- Source: [AWS CloudTrail - Runbook & Reference](../../sources/aws-cloudtrail.md)

[^aws-cloudtrail]: AWS CloudTrail - Runbook & Reference
