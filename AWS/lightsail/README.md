# Amazon Lightsail - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Lightsail is the simplest way to launch and manage virtual private servers and web applications on AWS, with low, predictable monthly pricing. It bundles instances, containers, managed databases (MySQL/PostgreSQL), load balancers, CDN distributions, block/object storage, static IPs, DNS, and snapshots in one console.

## Key concepts

- **Instance**: a virtual private server with a click-to-launch blueprint (OS, WordPress, LAMP, Nginx, etc.) and a built-in firewall.
- **Blueprints and bundles**: preconfigured OS/app images and fixed instance sizes (RAM, vCPU, storage, transfer).
- **Managed database**: fully configured MySQL or PostgreSQL that scales independently of instances.
- **Container service**: run containerized apps with a load balancer and HTTPS.
- **Load balancer**: distributes traffic across instances with health checks and session persistence.
- **CDN distribution**: CloudFront-based content distribution for lower latency.
- **Block/object storage**: SSD disks attached to instances and S3-compatible buckets for static content.
- **Snapshots**: instance/disk backups that can create new resources.
- **VPC peering**: connect Lightsail resources to the broader AWS VPC ecosystem.

## Common operations (AWS CLI)

```bash
# Create an instance (WordPress blueprint)
aws lightsail create-instances --instance-names web-1 \
  --blueprint-id wordpress --bundle-id nano_2_0 \
  --availability-zone ap-southeast-1a

# List instances and get details
aws lightsail get-instances
aws lightsail get-instance --instance-name web-1

# Networking
aws lightsail open-instance-public-ports --instance-name web-1 \
  --port-info fromPort=443,toPort=443,protocol=HTTPS
aws lightsail allocate-static-ip --static-ip-name web-ip
aws lightsail attach-static-ip --static-ip-name web-ip --instance-name web-1

# Snapshot and database
aws lightsail create-instance-snapshot --instance-name web-1 --instance-snapshot-name web-1-backup
aws lightsail create-relational-database --relational-database-name app-db \
  --relational-database-blueprint-id mysql_8_0 --relational-database-bundle-id micro_2_0
```

## Best practices

- Use Lightsail for simple, predictable workloads; move to EC2/RDS when you need advanced features or deep AWS integration.
- Enable the built-in firewall and only open required ports; use snapshots before changes.
- Use managed databases instead of running MySQL/PostgreSQL on instances.
- Put a load balancer (with HTTPS) in front of production instances; use CDN for static content.
- Peer the VPC when you need other AWS services; keep static IPs for stable DNS.
- Monitor metrics in the Lightsail console/CloudWatch and set up instance health alarms.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Instance unreachable | Check instance state, firewall rules, and static IP attachment. |
| Slow site | Review bundle size, add a load balancer, or use the CDN distribution. |
| Database connection fails | Check database endpoint, credentials, and public/private access settings. |
| Snapshot restore issues | Create a new instance from the snapshot and verify data/configuration. |
| Data transfer overage | Monitor monthly transfer allowance and use CDN/compression. |

## Limits

Instances, databases, load balancers, static IPs, and transfer allowances are capped per account and plan. See the Lightsail pricing page and Service Quotas console for current values.

## Official references

- [What is Amazon Lightsail?](https://docs.aws.amazon.com/lightsail/latest/userguide/what-is-amazon-lightsail.html)
- [Amazon Lightsail pricing](https://aws.amazon.com/lightsail/pricing/)
- [AWS CLI: lightsail commands](https://docs.aws.amazon.com/cli/latest/reference/lightsail/)
