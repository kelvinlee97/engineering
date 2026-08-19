# AWS Pricing Models - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS prices services on a pay-as-you-go basis: you pay only for what you use, with no upfront contracts, and you can save by committing to usage or using spare capacity. Understanding the pricing models (On-Demand, Savings Plans, Reserved Instances, Spot, and the Free Tier) helps you control cost while meeting availability needs.

## Key concepts

- **On-Demand**: pay per use (per second/minute/hour or per request/storage unit depending on service) with no commitment; flexible but most expensive per unit.
- **Savings Plans**: commit to a consistent amount of compute usage (1 or 3 years) for lower prices than On-Demand, with flexibility across instance families/Regions depending on plan type.
- **Reserved Instances**: commit to specific instance configurations (1 or 3 years, Standard or Convertible) for discounted EC2/RDS/Redshift/etc.; regional and zonal scopes.
- **Spot Instances**: use spare EC2 capacity at significant discounts for fault-tolerant, interruptible workloads; capacity can be reclaimed with notice.
- **Dedicated Hosts/Instances**: physical isolation for licensing and compliance needs.
- **Free Tier**: limited free usage for eligible services in the first 12 months, always-free offers, and trials.
- **Volume discounts**: usage aggregated across an organization (consolidated billing) can qualify for tiered discounts.
- **Data transfer**: outbound data transfer and cross-Region traffic are billed; inbound is typically free.
- **Price List API**: programmatically query current service pricing (bulk JSON/CSV).

## Common operations

```bash
# Price List API examples
aws pricing get-products --service-code AmazonEC2 \
  --filters 'Type=TERM_MATCH,Field=instanceType,Value=m5.large'

# Cost tools
aws ce get-cost-and-usage --time-period Start=2026-08-01,End=2026-08-19 \
  --granularity MONTHLY --metrics UnblendedCost
aws budgets create-budget --account-id 123456789012 --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

## Best practices

- Start with On-Demand, then add Savings Plans/Reserved Instances for steady-state workloads.
- Use Spot for stateless, fault-tolerant work (batch, CI, ML training) with interruption handling.
- Track usage and costs with Cost Explorer, budgets, and Cost Anomaly Detection.
- Consolidate billing in AWS Organizations to share volume discounts and reservations.
- Review outbound data transfer; use CloudFront/Direct Connect where they reduce cost.
- Estimate new workloads with the AWS Pricing Calculator before building.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Bill higher than expected | Use Cost Explorer and data exports to find the top services; check data transfer and underused resources. |
| Savings Plans not covering usage | Check coverage/utilization in the Savings Plans console and adjust purchase recommendations. |
| Spot instance terminated | Verify the workload handles interruption (checkpoints, queues) or use Capacity Rebalancing. |
| Free Tier charges | Confirm the service/usage is within free tier limits and the account is not past 12 months. |
| Prices in API look wrong | Filter by Region/term attributes; the Price List API includes many dimensions. |

## Limits

Pricing models and discounts vary by service, Region, and commitment terms. See the AWS pricing pages and Price List API documentation for current details.

## Official references

- [How AWS Pricing Works](https://docs.aws.amazon.com/whitepapers/latest/how-aws-pricing-works/introduction.html)
- [AWS Pricing](https://aws.amazon.com/pricing/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Price List API](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-pelong.html)
