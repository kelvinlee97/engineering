# Amazon Route 53 - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Route 53 is a highly available and scalable Domain Name System (DNS) web service with three main functions: domain registration, DNS routing, and health checking.

## Key concepts

- **Hosted zones**: public (internet-facing) and private (VPC-internal) containers for DNS records.
- **Record types**: A, AAAA, CNAME, MX, TXT, NS, SOA, and alias records.
- **Alias records**: map a name to an AWS resource (ELB, CloudFront, S3) with no charge and no TTL issues.
- **Routing policies**: simple, weighted, latency, failover, geolocation, geoproximity, and multivalue.
- **Health checks**: verify resource reachability and combine with failover routing.
- **DNSSEC**: sign zones to prevent DNS spoofing.
- **VPC Resolver / DNS Firewall**: private DNS resolution and outbound DNS filtering.

## Common operations (AWS CLI)

```bash
# Hosted zone
aws route53 create-hosted-zone --name example.com --caller-reference "$(date +%s)"
aws route53 list-hosted-zones

# Change records (batch JSON)
aws route53 change-resource-record-sets --hosted-zone-id Z0123456789ABCDEF \
  --change-batch file://change-batch.json

cat > change-batch.json <<'EOF'
{
  "Changes": [
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "www.example.com.",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z35SXDOTRQ7X7K",
          "DNSName": "my-alb-1234567890.ap-southeast-1.elb.amazonaws.com.",
          "EvaluateTargetHealth": false
        }
      }
    }
  ]
}
EOF

# Health check
aws route53 create-health-check --caller-reference "$(date +%s)" \
  --health-check-config Type=HTTPS,ResourcePath=/health,FullyQualifiedDomainName=example.com

# Inspect
aws route53 list-resource-record-sets --hosted-zone-id Z0123456789ABCDEF
aws route53 get-change --id /change/C01234567890
```

## Best practices

- Use **alias records** for AWS resources (free, auto-updating) instead of CNAME/A.
- Combine **health checks** with failover routing for high availability across regions.
- Use weighted/latency/geolocation policies for global traffic management; verify expected behavior in staging.
- Enable **DNSSEC** for critical zones; enable **DNS Firewall** to filter outbound queries.
- Use **private hosted zones** and Resolver for internal DNS; document NS delegation at the registrar.
- Monitor health check status with CloudWatch and alert on failures.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| DNS not resolving | Verify NS delegation at the registrar and that records exist; account for TTL caching. |
| Failover not working | Check health check status, evaluation windows, and failover record configuration. |
| Alias record errors | Use the correct hosted zone ID for the target service and a fully qualified DNS name. |
| Private DNS not working in VPC | Enable `enableDnsHostnames`/`enableDnsSupport`; check Resolver rules and VPC association. |
| Slow propagation | Lower TTL before planned changes; use change batch review (`get-change`). |
| DNSSEC issues | Validate key signing and DS record publication at the registrar. |

## Limits

Default quotas: 500 hosted zones and 10,000 records per zone (adjustable), plus health check quotas. See Service Quotas.

## Official references

- [What is Amazon Route 53? - Route 53 Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)
- [AWS CLI: route53 commands](https://docs.aws.amazon.com/cli/latest/reference/route53/)
