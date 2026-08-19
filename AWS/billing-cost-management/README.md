# AWS Billing and Cost Management - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Billing and Cost Management is a suite of features for setting up billing, retrieving and paying invoices, and analyzing, organizing, planning, and optimizing costs. It covers billing and payments, cost analysis, cost organization, budgeting and planning, and savings and commitments, with centralized management for organizations via AWS Organizations consolidated billing.

## Key concepts

- **Billing and payments**: monthly bills, invoices, purchase orders, payment profiles, credits, and billing preferences (email delivery, alerts, discount sharing).
- **Consolidated billing**: AWS Organizations gives one bill across accounts, combined usage for volume discounts and reservation/Savings Plans sharing; no extra fee.
- **Billing transfer**: one account manages and pays the consolidated bills of multiple AWS Organizations, separating billing from security/governance management.
- **Cost analysis**: AWS Cost Explorer (visual analysis, forecasting, custom reports), data exports (custom exports of cost/usage datasets), Cost Anomaly Detection, Free Tier monitoring, and split cost allocation for shared ECS resources.
- **Cost organization**: cost categories (map costs to teams/applications/environments, split charge rules) and cost allocation tags (view costs by tag).
- **Budgets and planning**: budgets for cost/usage with threshold alerts; in-console Pricing calculator and public Pricing calculator for estimates.
- **Savings and commitments**: Cost Optimization Hub (recommendations), Savings Plans, and Reservations (EC2, RDS, Redshift, DynamoDB) management.
- **Billing Conductor**: custom showback/chargeback billing for partners and resellers without changing how AWS bills you.
- **Price List API**: programmatic access to current pricing data (bulk JSON/CSV).
- **IAM access**: by default IAM users/roles cannot access the Billing console; enable the Activate IAM Access setting and grant permissions.

## Common operations (AWS CLI)

```bash
# Cost and usage
aws ce get-cost-and-usage --time-period Start=2026-08-01,End=2026-08-19 \
  --granularity MONTHLY --metrics UnblendedCost --group-by file://group.json
aws ce get-cost-forecast --time-period Start=2026-08-20,End=2026-09-19 \
  --granularity MONTHLY --metric UNBLENDED_COST

# Budgets
aws budgets create-budget --account-id 123456789012 --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json

# Data exports and anomaly detection
aws bcm-data-exports list-exports
aws ce get-anomaly-subscriptions
```

## Best practices

- Enable consolidated billing in Organizations and use cost allocation tags/cost categories consistently.
- Set budgets with alerts at multiple thresholds and enable Cost Anomaly Detection.
- Review Cost Explorer and Cost Optimization Hub recommendations (rightsizing, Savings Plans, reservations) regularly.
- Export cost/usage data to a data warehouse for deep analysis and forecasting.
- Restrict billing console access with IAM; keep root user for billing-only tasks.
- Use the Pricing calculator before launching new workloads and Billing Conductor for partner showback/chargeback.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| No access to billing console | Enable Activate IAM Access and grant the IAM principal the required billing permissions. |
| Tags not showing costs | Activate cost allocation tags for the accounts/Regions; tagging alone does not enable cost breakdown. |
| Budget alerts not firing | Verify budget thresholds, notifications/subscribers, and account scope. |
| Costs missing for member accounts | Confirm consolidated billing and Cost Management preferences for linked account data. |
| Forecast inaccurate | Provide longer historical data and check forecast granularity/time period. |

## Limits

Budgets, data exports, and API request rates have quotas; access depends on IAM and account settings. See the AWS Billing endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is AWS Billing and Cost Management?](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-what-is.html)
- [AWS Billing endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/billing.html)
- [AWS Cost Management](https://aws.amazon.com/aws-cost-management/)
- [AWS CLI: ce and budgets commands](https://docs.aws.amazon.com/cli/latest/reference/ce/)
