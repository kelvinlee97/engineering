# Elastic Load Balancing - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Elastic Load Balancing (ELB) automatically distributes incoming traffic across targets (EC2 instances, containers, IP addresses, Lambda functions) in one or more Availability Zones, routing traffic only to healthy targets. Capacity scales automatically.

## Load balancer types

- **Application Load Balancer (ALB)**: Layer 7 HTTP/HTTPS; path- and host-based routing, WAF integration, Lambda targets, WebSocket support.
- **Network Load Balancer (NLB)**: Layer 4 TCP/UDP; ultra-high performance, static IPs, TLS termination; best for extreme throughput.
- **Gateway Load Balancer (GWLB)**: Layer 3; routes traffic through third-party virtual appliances.
- **Classic Load Balancer**: previous generation; migrate to ALB/NLB.

## Key concepts

- **Listeners**: check for connection requests (protocol/port) and route them.
- **Target groups**: route requests to registered targets with health checks.
- **Health checks**: configurable path/port; only healthy targets receive traffic.
- **Cross-zone load balancing**: distribute evenly across AZs.
- **TLS termination**: offload encryption with certificates from ACM.
- **Access logs**: record detailed request data to S3.

## Common operations (AWS CLI)

```bash
# ALB
aws elbv2 create-load-balancer --name my-alb --type application \
  --subnets subnet-xxx subnet-yyy --security-groups sg-xxx

# Target group and registration
aws elbv2 create-target-group --name my-tg --protocol HTTP --port 80 \
  --vpc-id vpc-xxx --health-check-path /health
aws elbv2 register-targets --target-group-arn <tg-arn> \
  --targets Id=i-0123456789abcdef0

# Listener
aws elbv2 create-listener --load-balancer-arn <alb-arn> \
  --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn=<tg-arn>

# Inspect
aws elbv2 describe-load-balancers
aws elbv2 describe-target-health --target-group-arn <tg-arn>

# Delete
aws elbv2 delete-load-balancer --load-balancer-arn <alb-arn>
```

## Best practices

- Choose **ALB** for HTTP(S) workloads and **NLB** for TCP/UDP or static IP requirements.
- Register targets across **multiple AZs**; enable cross-zone load balancing.
- Tune health checks (path, interval, thresholds) to reflect real application health.
- Terminate TLS at the load balancer with **ACM** certificates.
- Enable **access logs** to S3 and monitor with CloudWatch; integrate **AWS WAF** with ALB.
- Combine with **Auto Scaling** so launched instances register automatically.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| `503 Service Unavailable` | No healthy targets: check target health, health check config, and application status. |
| Target unhealthy | Verify the health check path/port, security group, and target application. |
| Connection timeouts | Check idle timeout settings and keepalive behavior of the application. |
| TLS/certificate errors | Confirm the certificate is valid, covers the domain, and is attached to the listener. |
| NLB client IP behavior | NLB preserves client IPs; check that target security groups allow traffic from the client CIDR. |
| Uneven traffic distribution | Check cross-zone load balancing and target registration. |

## Limits

Per-Region quotas apply to load balancers, target groups, and listeners (for example, 20 load balancers per Region by default; adjustable). See the Service Quotas console.

## Official references

- [What is Elastic Load Balancing? - ELB User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)
- [AWS CLI: elbv2 commands](https://docs.aws.amazon.com/cli/latest/reference/elbv2/)
