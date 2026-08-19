# AWS Shield - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Shield is a managed Distributed Denial of Service (DDoS) protection service. **Shield Standard** is enabled automatically for all AWS customers at no additional cost and protects internet-facing applications against common volumetric attacks (for example, UDP reflection and TCP SYN floods). **Shield Advanced** is a paid tier that adds enhanced detection and mitigation, protection groups, health-based detection, cost protection, and access to the AWS Shield Response Team (SRT).

## Shield Standard vs. Shield Advanced

| Capability | Shield Standard | Shield Advanced |
|---|---|---|
| Cost | Included with AWS | Paid subscription plus data-transfer charges |
| Automatic protection | Common volumetric DDoS protection on AWS edge (CloudFront, Route 53, etc.) | Standard protection plus enhanced mitigation |
| Protecting specific resources | Not applicable | Add protections by resource ARN |
| Visibility and detection | Basic | Near-real-time metrics and health-based detection |
| Response support | Self-service | AWS Shield Response Team (SRT) and DDoS cost protection |
| Web-layer attacks | Requires AWS WAF | AWS WAF integration recommended |

## Key concepts

- **Volumetric attack**: floods bandwidth (UDP reflection, SYN floods); mostly absorbed by the AWS edge.
- **State-exhaustion / application-layer attack**: targets connection state or the application; mitigated with Shield Advanced and AWS WAF.
- **Protection**: a Shield Advanced configuration that monitors a specific resource ARN, such as CloudFront distributions, Route 53 hosted zones, Global Accelerator accelerators, Elastic IPs, and load balancers.
- **Protection group**: a collection of protections aggregated for monitoring and attack response; patterns include `ALL`, `ARBITRARY`, and `BY_RESOURCE_TYPE`.
- **Health-based detection**: uses Route 53 health checks and CloudWatch metrics to detect attacks that affect availability.
- **Cost protection**: credits or refunds for scaling and data-transfer charges incurred during detected attacks.

## Common operations (AWS CLI)

```bash
# List existing protections
aws shield list-protections

# Protect a resource
aws shield create-protection --name web-prod --resource-arn <resource-arn>

# Inspect or update a protection
aws shield describe-protection --protection-id <protection-id>
aws shield update-protection --protection-id <protection-id> --name web-prod-new

# Protection groups
aws shield create-protection-group --protection-group-id web-tier --aggregation SUM --pattern ALL
aws shield list-protection-groups

# Remove a protection
aws shield delete-protection --protection-id <protection-id>
```

## Best practices

- Design for DDoS resiliency: put traffic behind CloudFront, Global Accelerator, or a load balancer; never expose origin IPs publicly.
- Use Shield Advanced for business-critical, customer-facing applications and add protections for every relevant resource ARN.
- Combine with AWS WAF (managed rule groups, rate-based rules) for application-layer attacks.
- Configure Route 53 health checks and health-based detection; set CloudWatch alarms and EventBridge responses.
- Engage the Shield Response Team through AWS Support (Business or Enterprise) during active attacks.
- Review protections, protection groups, and coverage in every account and Region regularly.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Attack reaches the origin | Verify origin IPs are not exposed; route all traffic through CloudFront/ALB/Global Accelerator and restrict direct access. |
| Shield Advanced not detecting an attack | Confirm the resource ARN is protected and health checks/metrics are configured and healthy. |
| Cost spike during an attack | Enable cost protection and billing alerts; review usage after the event. |
| Application-layer attacks still succeed | Add AWS WAF rate-based rules and managed rule groups; keep the resource protected with Shield Advanced. |
| Slow response during an event | Engage SRT through AWS Support and share the incident timeline, metrics, and logs. |

## Limits

Shield Advanced: up to 1,000 protected resources per account per resource type (adjustable), up to 100 protection groups, and up to 1,000 individually listed members per protection group. Check the Service Quotas console for current values.

## Official references

- [AWS Shield - WAF & Shield Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html)
- [AWS Shield Advanced quotas](https://docs.aws.amazon.com/waf/latest/developerguide/shield-limits.html)
- [AWS Shield pricing](https://aws.amazon.com/shield/pricing/)
- [AWS CLI: shield commands](https://docs.aws.amazon.com/cli/latest/reference/shield/)
