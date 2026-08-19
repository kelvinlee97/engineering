# AWS Global Accelerator - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Global Accelerator improves the availability and performance of internet applications for a global audience. It provides static anycast IP addresses and routes traffic over the AWS global network to the optimal regional endpoint based on health, client location, and your policies.

## Key concepts

- **Accelerator**: the global resource that directs traffic; provides two static IPv4 addresses (or four for dual-stack) that stay assigned for the accelerator's lifetime.
- **Listener**: receives traffic on specific ports/protocols (TCP/UDP) and routes to endpoint groups.
- **Endpoint group**: a regional group of endpoints; traffic shifts based on health and weights.
- **Endpoints**: NLB, ALB, EC2 instances, or Elastic IPs in one or more Regions.
- **Custom routing accelerator**: maps users to specific destinations (VPC subnet private IPs) instead of load-balanced endpoints.
- **Health checks**: Global Accelerator reacts instantly to endpoint health changes; respects Application Recovery Controller zonal shifts.

## Common operations (AWS CLI)

```bash
# Create an accelerator
aws globalaccelerator create-accelerator --name prod --ip-address-type IPV4

# Add a listener (443/TCP)
aws globalaccelerator create-listener --accelerator-arn <accelerator-arn> \
  --port-ranges From=443,To=443 --protocol TCP

# Create an endpoint group with an ALB endpoint
aws globalaccelerator create-endpoint-group --listener-arn <listener-arn> \
  --endpoint-group-region us-east-1 \
  --endpoint-configurations EndpointId=arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/web/1234567890abcdef,Weight=100

# List and inspect
aws globalaccelerator list-accelerators
aws globalaccelerator describe-accelerator --accelerator-arn <accelerator-arn>
aws globalaccelerator list-listeners --accelerator-arn <accelerator-arn>
```

## Best practices

- Use Global Accelerator for global, latency-sensitive, or availability-critical applications instead of DNS-based failover only.
- Put ALB/NLB behind it and keep DNS TTLs short; update endpoints in the accelerator when infrastructure changes.
- Configure endpoint groups in multiple Regions with weights for active/passive or active/active routing.
- Use health checks and test failover behavior; respect VPC Block Public Access settings.
- Protect accelerator deletion with IAM/tag policies; the static IPs are lost if the accelerator is deleted.
- Use custom routing accelerators for gaming/real-time apps that need affinity to a specific destination.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Clients can't connect | Check listener ports/protocol, endpoint group health, and that endpoints accept traffic. |
| Traffic to unhealthy Region | Review endpoint health status and weights; confirm health checks pass. |
| Static IPs lost | Static IPs are released only on accelerator deletion; avoid deleting production accelerators. |
| Endpoint unreachable | Verify security groups/NACLs allow traffic from Global Accelerator (use the AWS published ranges). |
| Performance not improved | Confirm DNS points to the accelerator static IPs and clients reach the nearest edge. |

## Limits

Accelerators per account, listeners, endpoint groups, and endpoints have quotas. See the Service Quotas console for current values.

## Official references

- [What is AWS Global Accelerator?](https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html)
- [AWS Global Accelerator quotas](https://docs.aws.amazon.com/global-accelerator/latest/dg/limits.html)
- [AWS Global Accelerator pricing](https://aws.amazon.com/global-accelerator/pricing/)
- [AWS CLI: globalaccelerator commands](https://docs.aws.amazon.com/cli/latest/reference/globalaccelerator/)
