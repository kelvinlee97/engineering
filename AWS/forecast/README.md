# Amazon Forecast - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Forecast is a fully managed time-series forecasting service that uses statistical and machine learning algorithms to predict future values from historical data, with no ML experience required. Note: Amazon Forecast is no longer available to new customers; existing customers can continue using the service as normal.

## Key concepts

- **Time-series forecasting**: predict future data points (demand, traffic, capacity, financial metrics) based on historical series.
- **Datasets**: import time-series data (and related item/user metadata) through the console, API, CLI, or SDK.
- **Predictor**: a trained forecasting model built from your datasets; Forecast automates algorithm selection and training.
- **Forecast generation**: produce forecasts for the horizon you define; evaluate against backtests for accuracy.
- **Features**: automated ML, state-of-the-art algorithms, missing-value handling, and built-in feature-engineered datasets (for example, holidays).
- **Use cases**: retail demand planning, supply chain, resource planning, operational planning (web traffic, server capacity).

## Common operations (AWS CLI)

```bash
# Create a dataset group, import data, and create a predictor
aws forecast create-dataset-group --dataset-group-name retail \
  --domain RETAIL --dataset-arns <dataset-arn>
aws forecast create-dataset-import-job --dataset-arn <dataset-arn> \
  --dataset-import-job-name initial \
  --data-source '{"S3Config":{"Path":"s3://bucket/data","RoleArn":"arn:aws:iam::123456789012:role/forecast-role"}}'
aws forecast create-auto-predictor --predictor-name demand \
  --forecast-horizon 30 --data-config file://data.json

# Generate and retrieve forecasts
aws forecast create-forecast --forecast-name demand-30 \
  --predictor-arn <predictor-arn>
aws forecast describe-forecast --forecast-arn <forecast-arn>
```

## Best practices

- Prepare clean, regular time-series data (timestamps, item IDs, target values) and use related time-series metadata when available.
- Use AutoPredictor for automated algorithm selection; validate accuracy with backtests before production.
- Choose a forecast horizon that matches your planning cycle (for example, 30 or 90 days).
- Handle missing values deliberately; Forecast provides filling methods.
- Store forecasts in S3/Redshift for downstream planning systems.
- Existing customers: track the service status; plan alternatives if you start new forecasting initiatives.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Dataset import fails | Check CSV format, S3 permissions, and the dataset schema. |
| Predictor training fails | Verify data frequency, item count limits, and horizon settings. |
| Forecast accuracy poor | Add related time-series data, clean outliers, and evaluate with backtest metrics. |
| Cannot onboard new account | Forecast is closed to new customers; use documented alternatives. |
| Costs higher than expected | Forecast charges depend on generated forecasts, storage, and training hours; review usage. |

## Limits

Datasets, predictors, and forecasts per account and dataset sizes have quotas; service onboarding is limited to existing customers. See the Amazon Forecast endpoints and quotas page for current values.

## Official references

- [What is Amazon Forecast?](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html)
- [Amazon Forecast endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/forecast.html)
- [Amazon Forecast pricing](https://aws.amazon.com/forecast/pricing/)
- [AWS CLI: forecast commands](https://docs.aws.amazon.com/cli/latest/reference/forecast/)
