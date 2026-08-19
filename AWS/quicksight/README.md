# Amazon QuickSight - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon QuickSight is the business intelligence and data visualization capability of Amazon Quick (the AI-powered service that evolved from QuickSight). It connects to data sources, builds interactive dashboards and analyses, and supports embedding analytics in applications. All existing QuickSight APIs, SDKs, and integrations continue to work.

## Key concepts

- **Data sources**: connect to AWS services (Athena, Redshift, RDS, S3), SaaS applications, and databases; data can be imported into SPICE (the in-memory engine) or queried live.
- **SPICE**: the Super-fast, Parallel, In-memory Calculation Engine that caches imported data for fast interactive analysis.
- **Analyses and dashboards**: analyses are working documents; dashboards are published, read-only views shared with users.
- **Datasets and fields**: datasets define the data and its transformations (calculated fields, joins, filters) used in analyses.
- **Identity and access**: users are managed with IAM Identity Center, IAM federation, or QuickSight-managed users; access is per-user with reader/author/admin roles.
- **Embedding**: embed dashboards and analyses in applications; supports API-based access.
- **Amazon Quick evolution**: Quick adds AI agents, flows, automations, research, and app building; QuickSight remains the analytics feature, and sign-in is available with or without an AWS account depending on the plan.

## Common operations (AWS CLI)

```bash
# Data source, dataset, and analysis
aws quicksight create-data-source --aws-account-id 123456789012 \
  --data-source-id athena-prod --name athena-prod \
  --type ATHENA --parameters file://params.json
aws quicksight create-data-set --aws-account-id 123456789012 \
  --data-set-id orders --name orders --physical-table-map file://tables.json
aws quicksight create-analysis --aws-account-id 123456789012 \
  --analysis-id orders-analysis --name orders-analysis \
  --source-entity file://source.json

# Publish a dashboard and list assets
aws quicksight create-dashboard --aws-account-id 123456789012 \
  --dashboard-id orders-dashboard --name orders-dashboard \
  --source-entity file://source.json
aws quicksight list-dashboards --aws-account-id 123456789012
aws quicksight list-data-sources --aws-account-id 123456789012
```

## Best practices

- Use SPICE for large, read-heavy datasets and live queries where freshness matters; monitor SPICE capacity.
- Model data in datasets (joins, calculated fields) rather than duplicating transformations in each analysis.
- Publish curated dashboards and restrict access by user/group; use row-level security for multi-tenant data.
- Set up IAM Identity Center or federation so identity and lifecycle are centralized.
- Monitor usage and cost per user; enable capacity and API controls where needed.
- For embedding, use the same data-source governance and refresh schedules as the console experience.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Data source connection fails | Verify network access (VPC/security groups), credentials, and the data source type/region. |
| SPICE refresh fails | Check dataset refresh schedule, source permissions, and SPICE capacity. |
| Dashboard not visible to users | Confirm the user/group has access and the dashboard is published (not just an analysis). |
| Embedding blank | Verify the embed URL/domain allowlist and IAM/QuickSight session permissions. |
| Slow queries | Use SPICE for imported data or optimize the underlying query (Athena/Redshift). |

## Limits

SPICE capacity, users, datasets, dashboards, and API request rates have quotas. See the Amazon QuickSight endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon QuickSight?](https://docs.aws.amazon.com/quicksight/latest/user/welcome.html)
- [Amazon QuickSight endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/quicksight.html)
- [Amazon QuickSight pricing](https://aws.amazon.com/quicksight/pricing/)
- [AWS CLI: quicksight commands](https://docs.aws.amazon.com/cli/latest/reference/quicksight/)
