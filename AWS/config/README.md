# AWS Config - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Config records the configuration of supported AWS resources in an account and Region, tracks how configurations and relationships change over time, and evaluates compliance with rules. It delivers configuration history and snapshots to S3, sends change notifications through SNS, and supports conformance packs, aggregators, and advanced queries.

## Key concepts

- **Configuration item (CI)**: a record of a resource state at a point in time, including relationships.
- **Configuration recorder**: captures changes; one customer managed recorder per account per Region (service-linked recorders are created by integrated services such as Security Hub CSPM).
- **Configuration history and snapshot**: delivered to an S3 bucket on a schedule or on demand.
- **Configuration stream**: SNS notifications when recorded resource changes occur.
- **Rules**: managed or custom (Lambda) evaluations that report compliant/noncompliant.
- **Conformance packs**: YAML collections of rules and remediation actions deployed as one unit.
- **Aggregators**: centralize configuration and compliance data from multiple accounts and Regions.
- **Advanced queries**: SQL-like queries (`SELECT`) over recorded resource configuration.

## Common operations (AWS CLI)

```bash
# Configure the recorder (AWS Config service-linked role)
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123456789012:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig

# Set the delivery channel (S3 + SNS)
aws configservice put-delivery-channel \
  --delivery-channel s3BucketName=config-bucket,snsTopicARN=arn:aws:sns:us-east-1:123456789012:config-topic

# Start recording
aws configservice start-configuration-recorder --configuration-recorder-name default

# Rules
aws configservice put-config-rule --config-rule file://rule.json
aws configservice describe-config-rules
aws configservice describe-compliance-by-config-rule --config-rule-names s3-bucket-ssl-requests-only
aws configservice get-compliance-details-by-config-rule --config-rule-name <rule-name>

# Advanced query
aws configservice select-resource-config \
  --expression "SELECT resourceId, resourceType WHERE resourceType = 'AWS::EC2::Instance'"

# Aggregator (multi-account / multi-Region view)
aws configservice put-configuration-aggregator --configuration-aggregator-name org-aggregator \
  --organization-aggregation-source AllRegions=true
```

## Best practices

- Record all supported resource types (or at least the ones your compliance scope needs); use continuous recording for real-time monitoring.
- Use managed rules and conformance packs to standardize compliance checks across accounts.
- Keep the delivery S3 bucket private and encrypted; grant AWS Config only the permissions it needs.
- Use an aggregator for multi-account and multi-Region compliance dashboards.
- Use organization-level rules and conformance packs where supported for central governance.
- Use advanced queries for inventory and drift checks; save reusable queries.
- Test remediation actions (SSM Automation documents) before applying them automatically.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Resources not recorded | Confirm the recorder is started, the IAM role has permissions, and the resource type is supported in the Region. |
| No compliance results | Ensure rules are deployed, the evaluated resource types are recorded, and evaluations have completed. |
| Delivery to S3/SNS failing | Check bucket policy and topic permissions, and the delivery channel configuration. |
| Aggregator shows no data | Verify source accounts authorized the aggregation and required Regions are selected. |
| Advanced query returns nothing | Check that resource types are recorded and property names match the configuration schema. |
| Stale results after deletions | The recorder must be running to capture deletion events; restart it. |

## Limits

Up to 1,000 rules per Region per account; 50 conformance packs; 130 rules per conformance pack; 50 aggregators (adjustable); 10,000 accounts per aggregator; 300 saved queries; 50 tags per resource; one customer managed configuration recorder per account per Region. Check the Service Quotas console for current values.

## Official references

- [What Is AWS Config? - AWS Config Developer Guide](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
- [Service limits for AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/configlimits.html)
- [AWS Config pricing](https://aws.amazon.com/config/pricing/)
- [AWS CLI: configservice commands](https://docs.aws.amazon.com/cli/latest/reference/configservice/)
