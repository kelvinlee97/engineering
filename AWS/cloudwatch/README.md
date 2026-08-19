# Amazon CloudWatch - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon CloudWatch is the AWS monitoring and observability service. It collects and tracks metrics, logs, and traces from AWS resources and applications, and provides alarms, dashboards, and automated actions. It also offers application performance monitoring (Application Signals), log analytics (Logs Insights), synthetic monitoring, and cross-account observability.

## Key concepts

- **Metrics**: time-series data points; AWS services publish metrics automatically, and you can publish custom metrics from your applications.
- **Alarms**: watch a metric against a threshold and trigger actions (SNS, EC2 Auto Scaling, Systems Manager).
- **Dashboards**: unified, customizable views of metrics and logs; shareable across accounts and Regions.
- **Logs**: log groups and streams from AWS services and applications; query with Logs Insights (SQL/PPL); create metric filters and subscription filters.
- **CloudWatch agent**: collects system-level metrics (CPU, memory, disk, network), logs, and traces from EC2 and on-premises servers.
- **Application Signals / SLOs**: monitor latency, error, and request rates without code changes; define service level objectives with error budgets.
- **Synthetics and RUM**: canaries simulate user flows; RUM collects real user performance data.
- **Container Insights / Lambda Insights / Database Insights**: service-specific monitoring views.
- **OpenTelemetry**: native OTLP ingestion for metrics, logs, and traces.

## Common operations (AWS CLI)

```bash
# Publish a custom metric
aws cloudwatch put-metric-data --namespace App --metric-name Latency \
  --value 120 --unit Milliseconds --dimensions Service=checkout

# Get statistics
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-0123456789abcdef0 \
  --start-time 2026-08-18T00:00:00Z --end-time 2026-08-19T00:00:00Z \
  --period 300 --statistics Average

# Alarm
aws cloudwatch put-metric-alarm --alarm-name high-cpu --alarm-description "CPU > 80%" \
  --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average \
  --period 300 --threshold 80 --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 --alarm-actions arn:aws:sns:us-east-1:123456789012:alerts

# Logs
aws logs create-log-group --log-group-name /app/prod
aws logs filter-log-events --log-group-name /app/prod --filter-pattern "ERROR"
aws logs start-query --log-group-name /app/prod \
  --start-time 1784332800 --end-time 1784419200 \
  --query-string "fields @timestamp, @message | stats count(*) by bin(5m)"
aws logs get-query-results --query-id <query-id>

# Dashboards
aws cloudwatch put-dashboard --dashboard-name ops --dashboard-body file://dashboard.json
```

## Best practices

- Use standard (free) metrics for broad coverage and detailed monitoring only where needed to control cost.
- Publish custom metrics with consistent namespaces/dimensions and use them for application-level alarms.
- Centralize logs in log groups and use Logs Insights queries for troubleshooting; stream critical logs to S3 for retention.
- Use the CloudWatch agent (or OpenTelemetry) on EC2/on-premises for OS-level metrics.
- Set alarms for operational signals (CPU, memory, error rates, queue depth) and review them regularly.
- Use cross-account observability from a central monitoring account in multi-account environments.
- Combine metrics, logs, and traces (X-Ray/OTLP) for end-to-end root cause analysis.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| No metrics for an instance | Confirm the CloudWatch agent is installed/running and the IAM role allows `cloudwatch:PutMetricData`. |
| Alarm not firing | Check metric name/namespace, period, thresholds, and that the alarm state is not INSUFFICIENT_DATA. |
| Logs missing | Verify log group/stream names, agent config, and permissions. |
| High CloudWatch cost | Reduce custom metric volume, log ingestion, or detailed monitoring; use metric filters efficiently. |
| Logs Insights query errors | Validate the query language (SQL/PPL) and time range. |

## Limits

Metric resolution, retention (standard metrics 15 months), alarms per account, and log ingestion rates have quotas. See the Service Quotas console for current values.

## Official references

- [What is Amazon CloudWatch?](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [Amazon CloudWatch service quotas](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_limits.html)
- [Amazon CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/)
- [AWS CLI: cloudwatch and logs commands](https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/)
