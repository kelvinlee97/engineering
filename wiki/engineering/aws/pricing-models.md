---
type: Concept
title: AWS pricing models
description: "AWS pricing trades flexibility for discount: On-Demand is flexible and dearest, commitments are cheaper, and Spot is cheapest but reclaimable."
tags: [aws, cost]
sources:
  - id: aws-pricing-models
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/pricing-models/README.md
    title: "AWS pricing models - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

All AWS pricing models sit on one axis: On-Demand gives full flexibility at the highest unit price, commitments trade flexibility for savings, and Spot trades availability for the deepest discount.[^aws-pricing-models]

| Model | Trade |
| --- | --- |
| On-Demand | No commitment, highest unit price |
| Savings Plans | Commit to compute spend for 1 or 3 years, flexible across families or Regions by plan |
| Reserved Instances | Commit to configurations for 1 or 3 years, Standard or Convertible |
| Spot | Spare capacity, reclaimable with notice |
| Dedicated Hosts/Instances | Physical isolation for licensing or compliance |
| Free Tier | Limited usage in the first 12 months, always-free offers, trials |

As listed in the note.[^aws-pricing-models] Outbound and cross-Region data transfer are billed; inbound is typically free.[^aws-pricing-models]

## Practices

- Start On-Demand, then cover steady state with Savings Plans or reservations; use Spot for interruptible work such as batch, CI, and ML training.[^aws-pricing-models]
- Consolidated billing shares volume discounts and reservations across an organization.[^aws-pricing-models]
- Estimate with the Pricing Calculator; watch data transfer.[^aws-pricing-models]

## Related

- [AWS Billing and Cost Management](billing-cost-management.md)
- Source: [AWS pricing models - Runbook & Reference](../../sources/aws-pricing-models.md)

[^aws-pricing-models]: AWS pricing models - Runbook & Reference
