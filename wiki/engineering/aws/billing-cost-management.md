---
type: Service
title: AWS Billing and Cost Management
description: "AWS's billing console: paying, analyzing, tagging, budgeting, and buying commitments, with IAM access off by default."
tags: [aws, cost]
sources:
  - id: aws-billing-cost-management
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/billing-cost-management/README.md
    title: "AWS Billing and Cost Management - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Billing and Cost Management is five capabilities in one console: paying the bill, seeing where money went, labeling it by team or app, forecasting and capping it, and buying capacity cheaper in advance. IAM access to all of it is off by default.[^aws-billing-cost-management]

| Task | Tool |
| --- | --- |
| Pay and invoice | Billing and payments; consolidated billing through Organizations at no extra fee |
| Analyze | Cost Explorer, data exports, Cost Anomaly Detection |
| Label | Cost categories and cost allocation tags |
| Plan | Budgets with threshold alerts, Pricing calculator |
| Save | Cost Optimization Hub, Savings Plans, reservations |

As tabled in the note.[^aws-billing-cost-management]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| IAM user sees no billing | Enable Activate IAM Access and grant billing permissions |
| Tags show no costs | Activate cost allocation tags; tagging alone is not enough |
| Budget alerts silent | Thresholds, subscribers, scope |
| Member account costs missing | Consolidated billing and linked-account preferences |

As tabled in the note.[^aws-billing-cost-management]

## Related

- [AWS pricing models](pricing-models.md)
- Source: [AWS Billing and Cost Management - Runbook & Reference](../../sources/aws-billing-cost-management.md)

[^aws-billing-cost-management]: AWS Billing and Cost Management - Runbook & Reference
