# AWS Service Quotas - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Service Quotas lets you view and manage the quotas (limits) for AWS services from one place. Quotas are the maximum values for resources, actions, and items in your account (for example, IAM roles per account or VPCs per Region). When defaults don't meet your needs, you can request quota increases and monitor usage centrally.

## Key concepts

- **Service quota**: the maximum number of resources/operations for an account, Region, or resource; each AWS service defines its own quotas and defaults.
- **Default vs. applied quota**: the default is the initial value AWS establishes; the applied quota is the value after an increase is approved.
- **Adjustable quotas**: quotas that can be increased, at the account level or resource level; request through console/CLI/API and AWS support approves, denies, or partially approves.
- **Global quotas**: account-level quotas available in all Regions; increases are requested from us-east-1 (Public AWS), GovCloud (US-West), or China (Beijing).
- **Usage and utilization**: Service Quotas shows current resource usage and utilization percentages (for example, 150 of 200 resources = 75%).
- **Automatic Management**: monitors quota usage and notifies you before you run out.
- **Resource-level quotas**: for quotas like instances per OpenSearch Service domain, you can apply values per resource (context ID is an ARN or `*`).

## Common operations (AWS CLI)

```bash
# List quotas and service codes
aws service-quotas list-services
aws service-quotas list-service-quotas --service-code ec2 --region us-east-1

# Get current quota and usage
aws service-quotas get-service-quota --service-code ec2 \
  --quota-code L-1234567890abcdef0
aws service-quotas get-aws-default-service-quota --service-code ec2 \
  --quota-code L-1234567890abcdef0

# Request an increase and track it
aws service-quotas request-service-quota-increase --service-code ec2 \
  --quota-code L-1234567890abcdef0 --desired-value 100
aws service-quotas list-requested-service-quota-change-history \
  --service-code ec2
```

## Best practices

- Track quotas before launching large workloads; use Automatic Management to be notified near limits.
- Request increases early; approval can take time and may be partial.
- For global quotas, submit increase requests from the correct home Region (us-east-1 for Public AWS).
- Monitor utilization with CloudWatch/quota alarms and integrate quota checks into provisioning pipelines.
- Distinguish account-level from resource-level quotas; use resource-level increases where the service supports them.
- Use the Service Quotas API in automation instead of hard-coding limits.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Quota increase denied | Check the service's adjustability and the requested value; some quotas are not adjustable or have approval criteria. |
| Quota not found | Verify the service code and Region; some quotas are global or Region-specific. |
| Increase pending for long | Check request status in the console; contact AWS Support for delays. |
| Resource-level quota unavailable | Confirm the service supports resource-level quotas and use CLI version 2.13.20+ if needed. |
| Alarms on quota metrics | Set CloudWatch alarms on the service's quota usage metrics where published. |

## Limits

Quota increase requests and API request rates have quotas. See the Service Quotas user guide and the per-service quotas pages for current values.

## Official references

- [What is Service Quotas?](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html)
- [Service Quotas endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/servicequotas.html)
- [AWS CLI: service-quotas commands](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/)
