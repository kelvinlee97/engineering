---
type: Service
title: AWS machine learning platforms
description: Building and serving your own models with SageMaker, plus the managed Personalize and Forecast services.
tags: [aws, machine-learning]
sources:
  - id: aws-sagemaker
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/sagemaker/README.md
    title: "Amazon SageMaker AI - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-personalize
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/personalize/README.md
    title: "Amazon Personalize - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-forecast
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/forecast/README.md
    title: "Amazon Forecast - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
SageMaker is AWS's platform for building, training, and deploying your own models; Personalize and Forecast package specific model types (recommendations and time-series forecasts) as managed services.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [Amazon SageMaker AI](#amazon-sagemaker-ai) | SageMaker AI carries you from a notebook, through a managed training job, to a hosted endpoint (real-time, serverless, or batch) |
| [Amazon Personalize](#amazon-personalize) | Personalize turns imported interaction data into a trained solution version, then serves it either as a live campaign for real-time recommendations or as a batch job for offline lists and segments |
| [Amazon Forecast](#amazon-forecast) | Amazon Forecast is a fully managed time-series forecasting service that uses statistical and machine learning algorithms to predict future values from historical data, with no ML experience required |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## Amazon SageMaker AI

SageMaker AI carries you from a notebook, through a managed training job, to a hosted endpoint (real-time, serverless, or batch): and the 2024 rename to SageMaker AI changed the product's place in a larger unified data/AI platform without changing any existing `sagemaker` API, CLI, or resource name. Amazon SageMaker AI (renamed from Amazon SageMaker on December 3, 2024) is a fully managed machine learning service for building, training, and deploying ML models in production. It provides managed algorithms, distributed training, notebooks and Studio, model deployment, and MLOps tools. The next generation of Amazon SageMaker is a unified platform for data, analytics, and AI that also includes Lakehouse, Data and AI Governance, SQL analytics, data processing, Unified Studio, and Amazon Bedrock.

Key points:

- Legacy names unchanged: the `sagemaker` API namespace, CLI commands, managed policies, endpoints, CloudFormation resources, service-linked roles, and console/doc URLs remain the same after the rename.
- SageMaker AI: build, train, and deploy ML and foundation models with fully managed infrastructure, tools, and workflows.
- Studio / Unified Studio: integrated development environments for data preparation, experimentation, and MLOps.
- Training: managed algorithms and bring-your-own algorithms/frameworks with flexible distributed training options.
- Deployment: deploy models to secure, scalable hosted endpoints with a few steps from the console; supports real-time, serverless, and batch inference.

Practices:

- Use SageMaker Studio/Unified Studio for the full workflow and keep experiments tracked and reproducible.
- Store training data in S3 with versioning; use managed feature stores for feature reuse.
- Choose the smallest sufficient instance and use managed spot training for cost savings.

| Symptom | Check |
| --- | --- |
| Training job fails | Review the job logs in CloudWatch, input data format, and IAM role permissions. |
| Endpoint creation fails | Check the model artifact path, instance type, and the production variant configuration. |
| Notebook cannot access S3 | Verify the notebook role and instance profile permissions. |
| Slow inference | Right-size the endpoint instance, use serverless inference for spiky traffic, or batch inference for non-real-time loads. |

Notebook instances, training jobs, endpoints, and model sizes per account have quotas. See the Amazon SageMaker endpoints and quotas page and Service Quotas console for current values.[^aws-sagemaker]


## Amazon Personalize

Personalize turns imported interaction data into a trained solution version, then serves it either as a live campaign for real-time recommendations or as a batch job for offline lists and segments. Amazon Personalize is a fully managed machine learning service that generates item recommendations for users and creates user segments based on affinity, using your own data. It supports real-time personalization APIs and batch operations, and offers use-case optimized recommenders as well as fully customizable resources.

Key points:

- Datasets: interactions (user-item events), items, users, actions, and action interactions; bulk data from CSV plus real-time events.
- Recommenders and solutions: use-case optimized recommenders (for example, Top picks, More like X, Recommended for you) or custom solutions trained on your data.
- Real-time vs. batch: real-time API for live recommendations; batch inference for email lists, marketing campaigns, and user segments.
- User segments: groups of users likely to interact with items, for targeted campaigns.
- Next best action: recommend actions (for example, loyalty enrollment, app download) based on user behavior.

Practices:

- Collect clean interaction data (user, item, timestamp) and use real-time events for fresh recommendations.
- Start with use-case optimized recommenders, then move to custom solutions when you need deeper tuning.
- Evaluate campaigns with offline metrics and A/B tests before rolling out.

| Symptom | Check |
| --- | --- |
| No recommendations | Check dataset import status, user/item IDs, and campaign/solution version state. |
| Import job failed | Verify CSV schema, S3 permissions, and the IAM role for the import. |
| Cold-start users | Use popular-items recipes/fallback for users without history. |
| Recommendations stale | Import fresh interactions and retrain/update the solution version. |

Datasets, solutions, campaigns, and API request rates per account have quotas. See the Amazon Personalize endpoints and quotas page and Service Quotas console for current values.[^aws-personalize]


## Amazon Forecast

Amazon Forecast is a fully managed time-series forecasting service that uses statistical and machine learning algorithms to predict future values from historical data, with no ML experience required. Note: Amazon Forecast is no longer available to new customers; existing customers can continue using the service as normal.

Key points:

- Time-series forecasting: predict future data points (demand, traffic, capacity, financial metrics) based on historical series.
- Datasets: import time-series data (and related item/user metadata) through the console, API, CLI, or SDK.
- Predictor: a trained forecasting model built from your datasets; Forecast automates algorithm selection and training.
- Forecast generation: produce forecasts for the horizon you define; evaluate against backtests for accuracy.
- Features: automated ML, state-of-the-art algorithms, missing-value handling, and built-in feature-engineered datasets (for example, holidays).

Practices:

- Prepare clean, regular time-series data (timestamps, item IDs, target values) and use related time-series metadata when available.
- Use AutoPredictor for automated algorithm selection; validate accuracy with backtests before production.
- Choose a forecast horizon that matches your planning cycle (for example, 30 or 90 days).

| Symptom | Check |
| --- | --- |
| Dataset import fails | Check CSV format, S3 permissions, and the dataset schema. |
| Predictor training fails | Verify data frequency, item count limits, and horizon settings. |
| Forecast accuracy poor | Add related time-series data, clean outliers, and evaluate with backtest metrics. |
| Cannot onboard new account | Forecast is closed to new customers; use documented alternatives. |

Datasets, predictors, and forecasts per account and dataset sizes have quotas; service onboarding is limited to existing customers. See the Amazon Forecast endpoints and quotas page for current values.[^aws-forecast]


## Related

- [AWS AI services](ai-services.md)
- [Domain index](index.md)

[^aws-sagemaker]: [Amazon SageMaker AI - Runbook & Reference](../../sources/aws-sagemaker.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/sagemaker/README.md)
[^aws-personalize]: [Amazon Personalize - Runbook & Reference](../../sources/aws-personalize.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/personalize/README.md)
[^aws-forecast]: [Amazon Forecast - Runbook & Reference](../../sources/aws-forecast.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/forecast/README.md)
