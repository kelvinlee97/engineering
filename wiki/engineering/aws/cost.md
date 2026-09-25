---
type: Pattern
title: AWS cost
description: How AWS charges (pricing models) and the Billing and Cost Management tools for tracking and controlling spend.
tags:
- aws
- cost
aliases:
- engineering/aws/pricing-models
- engineering/aws/billing-cost-management
sources:
- id: aws-pricing-models
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/pricing-models/README.md
  title: AWS pricing models - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-billing-cost-management
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/billing-cost-management/README.md
  title: AWS Billing and Cost Management - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
How AWS charges for resources, and the Billing and Cost Management tools for seeing and controlling that spend.

## AWS pricing models

All AWS pricing models sit on one axis: On-Demand gives full flexibility at the highest unit price, commitments trade flexibility for savings, and Spot trades availability for the deepest discount.

| Model | Trade |
| --- | --- |
| On-Demand | No commitment, highest unit price |
| Savings Plans | Commit to compute spend for 1 or 3 years, flexible across families or Regions by plan |
| Reserved Instances | Commit to configurations for 1 or 3 years, Standard or Convertible |
| Spot | Spare capacity, reclaimable with notice |
| Dedicated Hosts/Instances | Physical isolation for licensing or compliance |
| Free Tier | Limited usage in the first 12 months, always-free offers, trials |

As listed in the note. Outbound and cross-Region data transfer are billed; inbound is typically free.[^aws-pricing-models]

### Practices

- Start On-Demand, then cover steady state with Savings Plans or reservations; use Spot for interruptible work such as batch, CI, and ML training.
- Consolidated billing shares volume discounts and reservations across an organization.
- Estimate with the Pricing Calculator; watch data transfer.[^aws-pricing-models]

## AWS Billing and Cost Management

Billing and Cost Management is five capabilities in one console: paying the bill, seeing where money went, labeling it by team or app, forecasting and capping it, and buying capacity cheaper in advance. IAM access to all of it is off by default.

| Task | Tool |
| --- | --- |
| Pay and invoice | Billing and payments; consolidated billing through Organizations at no extra fee |
| Analyze | Cost Explorer, data exports, Cost Anomaly Detection |
| Label | Cost categories and cost allocation tags |
| Plan | Budgets with threshold alerts, Pricing calculator |
| Save | Cost Optimization Hub, Savings Plans, reservations |

As tabled in the note.[^aws-billing-cost-management]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| IAM user sees no billing | Enable Activate IAM Access and grant billing permissions |
| Tags show no costs | Activate cost allocation tags; tagging alone is not enough |
| Budget alerts silent | Thresholds, subscribers, scope |
| Member account costs missing | Consolidated billing and linked-account preferences |

As tabled in the note.[^aws-billing-cost-management]

## Related
- [Domain index](index.md): other pages in this domain.

[^aws-pricing-models]: [AWS pricing models - Runbook & Reference](../../sources/aws-pricing-models.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/pricing-models/README.md)
[^aws-billing-cost-management]: [AWS Billing and Cost Management - Runbook & Reference](../../sources/aws-billing-cost-management.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/billing-cost-management/README.md)
