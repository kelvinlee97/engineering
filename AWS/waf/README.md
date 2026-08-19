# AWS WAF - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS WAF is a web application firewall that monitors HTTP(S) requests to protected resources and controls access based on rules (IP addresses, query strings, headers, body). It responds with the content, an HTTP 403, or a custom response.

## Protected resources

- CloudFront distributions
- API Gateway REST APIs
- Application Load Balancers
- AWS AppSync GraphQL APIs
- Amazon Cognito user pools
- AWS App Runner, AWS Amplify, AWS Verified Access

## Key concepts

- **Web ACL**: the container of rules associated with a protected resource.
- **Rules and rule groups**: individual match statements or reusable groups; AWS managed rule groups cover common threats.
- **Rate-based rules**: limit requests from an IP within a window; useful against DDoS/bot traffic.
- **Actions**: allow, block, count, or custom response; use `count` to test before blocking.
- **Labels and logging**: label matching requests and send logs to S3, CloudWatch Logs, or Kinesis Data Firehose.

## Common operations (AWS CLI)

```bash
# Create a web ACL (default action file)
aws wafv2 create-web-acl --name my-acl --scope REGIONAL \
  --default-action file://default-action.json \
  --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=my-acl

# Associate with a resource (ALB/API Gateway)
aws wafv2 associate-web-acl --web-acl-arn <acl-arn> --resource-arn <resource-arn>

# Update rules
aws wafv2 update-web-acl --name my-acl --scope REGIONAL --id <acl-id> \
  --default-action file://default-action.json \
  --rules file://rules.json \
  --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=my-acl

# List and inspect
aws wafv2 list-web-acls --scope REGIONAL
aws wafv2 get-web-acl --name my-acl --scope REGIONAL --id <acl-id>

# Enable logging
aws wafv2 put-logging-configuration --logging-configuration file://logging.json
```

## Best practices

- Start with **AWS managed rule groups** and add custom rules for your use case.
- Add **rate-based rules** for DDoS/bot protection.
- Test rules in **count mode** first, then switch to block after reviewing logs.
- Use **labels** and logging to understand which rule matched.
- Scope correctly: `CLOUDFRONT` for CloudFront, `REGIONAL` for ALB/API Gateway.
- Monitor WAF metrics in CloudWatch and alert on blocked-request spikes.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| Legitimate traffic blocked | Review the matching rule in logs; run in count mode; adjust IP sets or rule scope. |
| Unexpected `403` | Check web ACL association, rule actions, and managed rule group behavior. |
| Logs not appearing | Verify logging configuration and destination permissions. |
| Performance impact | Keep rule count manageable and use efficient match statements. |
| Rate-based false positives | Increase the rate threshold or use scope-down statements. |

## Limits

Rule, rule group, and web ACL quotas apply per account and scope. See the Service Quotas console for current values.

## Official references

- [AWS WAF - WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html)
- [AWS WAF pricing](https://aws.amazon.com/waf/pricing/)
- [AWS CLI: wafv2 commands](https://docs.aws.amazon.com/cli/latest/reference/wafv2/)
