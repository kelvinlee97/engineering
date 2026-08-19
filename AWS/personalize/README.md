# Amazon Personalize - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Personalize is a fully managed machine learning service that generates item recommendations for users and creates user segments based on affinity, using your own data. It supports real-time personalization APIs and batch operations, and offers use-case optimized recommenders as well as fully customizable resources.

## Key concepts

- **Datasets**: interactions (user-item events), items, users, actions, and action interactions; bulk data from CSV plus real-time events.
- **Recommenders and solutions**: use-case optimized recommenders (for example, Top picks, More like X, Recommended for you) or custom solutions trained on your data.
- **Real-time vs. batch**: real-time API for live recommendations; batch inference for email lists, marketing campaigns, and user segments.
- **User segments**: groups of users likely to interact with items, for targeted campaigns.
- **Next best action**: recommend actions (for example, loyalty enrollment, app download) based on user behavior.
- **Search re-ranking**: re-rank search results (for example, from OpenSearch) for personalization.
- **Data preparation**: import data from 40+ sources with SageMaker AI Data Wrangler; record real-time events with Amplify or SDKs.

## Common operations (AWS CLI)

```bash
# Create a dataset group and import interactions
aws personalize create-dataset-group --name app-personalization
aws personalize create-dataset --dataset-group-arn <group-arn> \
  --dataset-type Interactions --schema-arn <schema-arn>
aws personalize create-dataset-import-job --dataset-arn <dataset-arn> \
  --job-name interactions-import \
  --data-source '{"dataLocation":"s3://bucket/interactions.csv"}' \
  --role-arn arn:aws:iam::123456789012:role/personalize-role

# Create a solution version and deploy a campaign
aws personalize create-solution --dataset-group-arn <group-arn> \
  --name top-picks --recipe-arn <recipe-arn>
aws personalize create-solution-version --solution-arn <solution-arn>
aws personalize create-campaign --name prod --solution-version-arn <sv-arn> \
  --min-provisioned-tps 1

# Get recommendations (runtime)
aws personalize-runtime get-recommendations --campaign-arn <campaign-arn> \
  --user-id user-123
```

## Best practices

- Collect clean interaction data (user, item, timestamp) and use real-time events for fresh recommendations.
- Start with use-case optimized recommenders, then move to custom solutions when you need deeper tuning.
- Evaluate campaigns with offline metrics and A/B tests before rolling out.
- Use batch workflows for email/marketing and segments; reserve real-time endpoints for live traffic.
- Re-rank search results with Personalize for e-commerce/streaming experiences.
- Monitor data quality, event ingestion, and campaign latency; retrain on a schedule.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| No recommendations | Check dataset import status, user/item IDs, and campaign/solution version state. |
| Import job failed | Verify CSV schema, S3 permissions, and the IAM role for the import. |
| Cold-start users | Use popular-items recipes/fallback for users without history. |
| Recommendations stale | Import fresh interactions and retrain/update the solution version. |
| High endpoint cost | Reduce min-provisioned TPS or use batch operations for non-interactive use cases. |

## Limits

Datasets, solutions, campaigns, and API request rates per account have quotas. See the Amazon Personalize endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Personalize?](https://docs.aws.amazon.com/personalize/latest/dg/what-is-personalize.html)
- [Amazon Personalize endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/personalize.html)
- [Amazon Personalize pricing](https://aws.amazon.com/personalize/pricing/)
- [AWS CLI: personalize and personalize-runtime commands](https://docs.aws.amazon.com/cli/latest/reference/personalize/)
